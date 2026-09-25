"""Continue Copycat 05B epoch 1 for exactly one additional epoch."""
import hashlib
import json
import math
import random
from pathlib import Path

import torch
from peft import PeftModel, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

ROOT = Path(__file__).resolve().parent
MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
START_ADAPTER = ROOT / "copycat_05b_adapter"
SOURCES = [ROOT / "gold_editare_04.jsonl", ROOT / "gold_romana_05b.jsonl"]
BENCHMARKS = [ROOT / "benchmark_romana_05.jsonl", ROOT / "benchmark_copycat_03_on_04.py"]
OUTPUT = ROOT / "copycat_05b_epoch2_adapter"
SEED, EPOCHS, LR, MAX_LENGTH, GRAD_ACCUM = 42, 1, 5e-5, 384, 4

if OUTPUT.exists():
    raise SystemExit(f"Refuz suprascrierea: {OUTPUT}")
if not (START_ADAPTER / "adapter_config.json").exists():
    raise SystemExit(f"Lipsește Copycat 05B epoca 1: {START_ADAPTER}")
if not torch.cuda.is_available():
    raise SystemExit("CUDA este necesar")
random.seed(SEED)
torch.manual_seed(SEED)

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

records = [item for path in SOURCES for item in read_jsonl(path)]
assert [len(read_jsonl(path)) for path in SOURCES] == [104, 167]
assert len(records) == 271
benchmark_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in BENCHMARKS}

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
base.config.use_cache = False
base = prepare_model_for_kbit_training(base, use_gradient_checkpointing=True)
model = PeftModel.from_pretrained(base, str(START_ADAPTER), is_trainable=True)
model.print_trainable_parameters()

config = model.peft_config["default"]
assert (config.r, config.lora_alpha, config.lora_dropout, set(config.target_modules)) == (8, 16, 0.05, {"q_proj", "v_proj"})

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
        raise ValueError(f"Fără tokeni de răspuns: {record.get('id')}")
    return encoded["input_ids"], encoded["attention_mask"], labels

encoded = [encode(record) for record in records]
trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
optimizer = torch.optim.AdamW(trainable, lr=LR)
total_steps = math.ceil(len(encoded) / GRAD_ACCUM)
order = list(range(len(encoded)))
random.Random(SEED).shuffle(order)
optimizer.zero_grad(set_to_none=True)
model.train()
losses = []
global_step = 0
print(f"GPU={torch.cuda.get_device_name(0)} records={len(records)} epochs=1 steps={total_steps}", flush=True)
for micro_step, idx in enumerate(order, start=1):
    input_ids, attention_mask, labels = encoded[idx]
    output = model(input_ids=input_ids.to(model.device), attention_mask=attention_mask.to(model.device), labels=labels.to(model.device))
    loss = output.loss
    (loss / GRAD_ACCUM).backward()
    losses.append(loss.item())
    if micro_step % GRAD_ACCUM == 0 or micro_step == len(order):
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        global_step += 1
        if global_step == 1 or global_step % 10 == 0:
            print(f"step={global_step}/{total_steps} loss={loss.item():.6f}", flush=True)

mean_loss = sum(losses) / len(losses)
OUTPUT.mkdir()
model.save_pretrained(OUTPUT)
tokenizer.save_pretrained(OUTPUT)
metadata = {
    "base_model": MODEL,
    "starting_adapter": str(START_ADAPTER),
    "starting_adapter_sha256": hashlib.sha256((START_ADAPTER / "adapter_model.safetensors").read_bytes()).hexdigest(),
    "sources": [{"name": path.name, "count": len(read_jsonl(path)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in SOURCES],
    "epochs_this_run": 1, "cumulative_epochs": 2, "learning_rate": LR, "seed": SEED, "batch_size": 1,
    "gradient_accumulation": GRAD_ACCUM, "max_length": MAX_LENGTH,
    "lora_r": config.r, "lora_alpha": config.lora_alpha, "lora_dropout": config.lora_dropout,
    "target_modules": sorted(config.target_modules), "optimizer_steps": global_step,
    "mean_loss": mean_loss, "benchmark_hashes_before": benchmark_hashes,
    "benchmark_hashes_after": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in BENCHMARKS},
}
assert metadata["benchmark_hashes_before"] == metadata["benchmark_hashes_after"]
(OUTPUT / "copycat_training.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"epoch=1 mean_loss={mean_loss:.6f}", flush=True)
print(f"SAVED {OUTPUT}", flush=True)
