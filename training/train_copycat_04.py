import json
import math
import random
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
DATA_FILE = "gold_editare_04.jsonl"
OUTPUT_DIR = "copycat_editare_04_adapter"
SEED = 42
EPOCHS = 4
LR = 2e-4
MAX_LENGTH = 384
GRAD_ACCUM = 4

random.seed(SEED)
torch.manual_seed(SEED)

if not torch.cuda.is_available():
    raise SystemExit("EROARE: CUDA nu este disponibil. Ruleaza antrenarea pe placa NVIDIA.")

print("GPU:", torch.cuda.get_device_name(0))
print("Incarc tokenizerul...")

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Incarc RoMistral in 4-bit...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    quantization_config=bnb_config,
    device_map="auto",
)

model.config.use_cache = False
model = prepare_model_for_kbit_training(
    model,
    use_gradient_checkpointing=True,
)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

data_path = Path(DATA_FILE)
if not data_path.exists():
    raise SystemExit(f"EROARE: nu gasesc {DATA_FILE} in folderul curent.")

records = [
    json.loads(line)
    for line in data_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

print(f"Exemple Gold: {len(records)}")

def encode_record(record):
    messages = record["messages"]
    if len(messages) != 2 or messages[0]["role"] != "user" or messages[1]["role"] != "assistant":
        raise ValueError("Fiecare exemplu trebuie sa contina exact user + assistant.")

    # Same chat-template family recommended by the RoMistral model card.
    prompt_text = tokenizer.apply_chat_template(
        [messages[0]],
        tokenize=False,
        system_message=""
    )
    full_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        system_message=""
    )

    prompt_ids = tokenizer(
        prompt_text,
        add_special_tokens=False,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )["input_ids"][0]

    full = tokenizer(
        full_text,
        add_special_tokens=False,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    input_ids = full["input_ids"][0]
    attention_mask = full["attention_mask"][0]
    labels = input_ids.clone()

    # Train only on the assistant answer, not on the user's prompt.
    prompt_len = min(len(prompt_ids), len(labels))
    labels[:prompt_len] = -100

    if torch.all(labels == -100):
        raise ValueError("Exemplu fara tokeni de raspuns dupa mascarea promptului.")

    return input_ids, attention_mask, labels

encoded = [encode_record(r) for r in records]

trainable_params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.AdamW(trainable_params, lr=LR)

total_micro_steps = EPOCHS * len(encoded)
total_optimizer_steps = math.ceil(total_micro_steps / GRAD_ACCUM)

print(f"Epoci: {EPOCHS}")
print(f"Gradient accumulation: {GRAD_ACCUM}")
print(f"Optimizer steps aproximative: {total_optimizer_steps}")
print("Incep antrenarea...\n")

model.train()
optimizer.zero_grad(set_to_none=True)
global_step = 0
running = 0.0

for epoch in range(EPOCHS):
    order = list(range(len(encoded)))
    random.Random(SEED + epoch).shuffle(order)

    epoch_loss = 0.0

    for micro_idx, idx in enumerate(order, start=1):
        input_ids, attention_mask, labels = encoded[idx]

        input_ids = input_ids.unsqueeze(0).to(model.device)
        attention_mask = attention_mask.unsqueeze(0).to(model.device)
        labels = labels.unsqueeze(0).to(model.device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )

        raw_loss = outputs.loss
        loss = raw_loss / GRAD_ACCUM
        loss.backward()

        epoch_loss += raw_loss.item()
        running += raw_loss.item()

        should_step = (micro_idx % GRAD_ACCUM == 0) or (micro_idx == len(order))
        if should_step:
            torch.nn.utils.clip_grad_norm_(trainable_params, 1.0)
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            global_step += 1

            if global_step % 5 == 0 or global_step == 1:
                avg = running / min(5 * GRAD_ACCUM, global_step * GRAD_ACCUM)
                print(
                    f"epoch {epoch+1}/{EPOCHS} | "
                    f"step {global_step}/{total_optimizer_steps} | "
                    f"loss curent {raw_loss.item():.4f}"
                )
                running = 0.0

    print(
        f"==> epoch {epoch+1} terminata | "
        f"loss mediu {epoch_loss / len(encoded):.4f}"
    )

print("\nSalvez adaptorul LoRA...")

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

meta = {
    "base_model": MODEL,
    "dataset": DATA_FILE,
    "num_examples": len(records),
    "epochs": EPOCHS,
    "learning_rate": LR,
    "lora_r": 8,
    "lora_alpha": 16,
    "target_modules": ["q_proj", "v_proj"],
    "seed": SEED,
}
Path(OUTPUT_DIR, "copycat_training.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"Gata. Adaptor salvat in: {OUTPUT_DIR}")
print("Modelul de baza NU a fost suprascris.")
