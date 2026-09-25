"""Evaluate the frozen Lesson 08 benchmark before any Lesson 08 training."""
import hashlib
import json
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
BENCHMARK = ROOT / "benchmark_prag_08.jsonl"
OUTPUT = ROOT / "benchmark_prag_08_pretraining_results.jsonl"
ADAPTERS = {
    "Copycat 05B epoca 2": Path(r"copycat_05b_epoch2_adapter"),
    "Copycat 06 epoca 1": Path(r"copycat_06_epoch1_adapter"),
    "Copycat 07 epoca 1": Path(r"copycat_07_epoch1_adapter"),
}
EXPECTED_HASH = "ee1540a10a4b0b98119670fe91018329e1582c7b4e231a6ec707409db6d04104"
assert hashlib.sha256(BENCHMARK.read_bytes()).hexdigest() == EXPECTED_HASH
items = [json.loads(line) for line in BENCHMARK.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(items) == 32 and not OUTPUT.exists()
for path in ADAPTERS.values():
    assert (path / "adapter_config.json").exists(), path

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
base.eval()

def generate(model, question):
    prompt = tokenizer.apply_chat_template([{"role":"user","content":question}], tokenize=False, system_message="")
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=160, do_sample=False, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

labels=list(ADAPTERS)
model=PeftModel.from_pretrained(base,str(ADAPTERS[labels[0]]),adapter_name="copycat05b2")
model.load_adapter(str(ADAPTERS[labels[1]]),adapter_name="copycat06")
model.load_adapter(str(ADAPTERS[labels[2]]),adapter_name="copycat07")
model.eval()
names=dict(zip(labels,["copycat05b2","copycat06","copycat07"]))
with OUTPUT.open("w",encoding="utf-8") as out:
    for label in labels:
        model.set_adapter(names[label])
        print(label,flush=True)
        for index,item in enumerate(items,1):
            answer=generate(model,item["prompt"])
            out.write(json.dumps({**item,"model":label,"answer":answer},ensure_ascii=False)+"\n")
            out.flush()
            print(f"{index}/32 {item['id']}: {answer}",flush=True)

assert hashlib.sha256(BENCHMARK.read_bytes()).hexdigest() == EXPECTED_HASH
print(f"BENCHMARK UNCHANGED {EXPECTED_HASH}",flush=True)
