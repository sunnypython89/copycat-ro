"""Train one new Copycat 05 LoRA from Gold 04 + Gold 05; never overwrite adapters."""
import hashlib
import json
import math
import random
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

ROOT = Path(__file__).resolve().parent
MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
SOURCES = [ROOT / "gold_editare_04.jsonl", ROOT / "gold_romana_05.jsonl"]
BENCHMARKS = [ROOT / "benchmark_romana_05.jsonl", ROOT / "benchmark_copycat_03_on_04.py"]
OUTPUT = ROOT / "copycat_05_adapter"
SEED, EPOCHS, LR, MAX_LENGTH, GRAD_ACCUM = 42, 3, 1e-4, 384, 4

if OUTPUT.exists():
    raise SystemExit(f"Output already exists: {OUTPUT}")
if not torch.cuda.is_available():
    raise SystemExit("CUDA is required")
random.seed(SEED)
torch.manual_seed(SEED)

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

records = [item for path in SOURCES for item in read_jsonl(path)]
benchmark = read_jsonl(BENCHMARKS[0])
benchmark_prompts = {item["prompt"] for item in benchmark}
assert len(benchmark) == 16
assert len(records) == 179
assert not benchmark_prompts.intersection(item["messages"][0]["content"] for item in records)
benchmark_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in BENCHMARKS}

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
base.config.use_cache = False
base = prepare_model_for_kbit_training(base, use_gradient_checkpointing=True)
model = get_peft_model(base, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM", target_modules=["q_proj", "v_proj"]))
model.print_trainable_parameters()

def encode(record):
    messages = record["messages"]
    assert len(messages) == 2 and messages[0]["role"] == "user" and messages[1]["role"] == "assistant"
    prompt = tokenizer.apply_chat_template(messages[:1], tokenize=False, system_message="")
    full = tokenizer.apply_chat_template(messages, tokenize=False, system_message="")
    prompt_ids = tokenizer(prompt, add_special_tokens=False, truncation=True, max_length=MAX_LENGTH)["input_ids"]
    encoded = tokenizer(full, add_special_tokens=False, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    labels = encoded["input_ids"].clone()
    labels[:, :len(prompt_ids)] = -100
    if torch.all(labels == -100):
        raise ValueError(f"No answer tokens for {record['id']}")
    return encoded["input_ids"], encoded["attention_mask"], labels

encoded = [encode(record) for record in records]
trainable = [param for param in model.parameters() if param.requires_grad]
optimizer = torch.optim.AdamW(trainable, lr=LR)
steps = math.ceil(len(records) / GRAD_ACCUM) * EPOCHS
print(f"GPU={torch.cuda.get_device_name(0)} records={len(records)} epochs={EPOCHS} steps={steps}", flush=True)
model.train()
epoch_losses = []
global_step = 0
for epoch in range(EPOCHS):
    order = list(range(len(encoded)))
    random.Random(SEED + epoch).shuffle(order)
    optimizer.zero_grad(set_to_none=True)
    losses = []
    for micro_idx, idx in enumerate(order, start=1):
        input_ids, attention_mask, labels = encoded[idx]
        output = model(input_ids=input_ids.to(model.device), attention_mask=attention_mask.to(model.device), labels=labels.to(model.device))
        loss = output.loss
        (loss / GRAD_ACCUM).backward()
        losses.append(loss.item())
        if micro_idx % GRAD_ACCUM == 0 or micro_idx == len(order):
            torch.nn.utils.clip_grad_norm_(trainable, 1.0)
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            global_step += 1
            if global_step % 10 == 0 or global_step == 1:
                print(f"epoch={epoch+1} step={global_step}/{steps} loss={loss.item():.4f}", flush=True)
    avg = sum(losses) / len(losses)
    epoch_losses.append(avg)
    print(f"epoch={epoch+1} mean_loss={avg:.6f}", flush=True)

OUTPUT.mkdir()
model.save_pretrained(OUTPUT)
tokenizer.save_pretrained(OUTPUT)
meta = {
    "base_model": MODEL, "sources": [{"name": path.name, "count": len(read_jsonl(path)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in SOURCES],
    "benchmark_hashes_before": benchmark_hashes, "epochs": EPOCHS, "learning_rate": LR,
    "max_length": MAX_LENGTH, "gradient_accumulation": GRAD_ACCUM, "batch_size": 1,
    "lora_r": 8, "lora_alpha": 16, "lora_dropout": 0.05, "target_modules": ["q_proj", "v_proj"],
    "seed": SEED, "optimizer_steps": global_step, "epoch_mean_losses": epoch_losses,
    "benchmark_hashes_after": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in BENCHMARKS},
}
(OUTPUT / "copycat_training.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
assert meta["benchmark_hashes_before"] == meta["benchmark_hashes_after"]
print(f"SAVED {OUTPUT}", flush=True)
