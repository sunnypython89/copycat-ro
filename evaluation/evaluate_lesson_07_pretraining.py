"""Evaluate frozen Lesson 07 benchmark before any Lesson 07 training."""
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
BENCHMARK = ROOT / "benchmark_eliminare_07.jsonl"
OUTPUT = ROOT / "benchmark_eliminare_07_pretraining_results.jsonl"
ADAPTERS = {
    "Copycat 04": Path(r"copycat_editare_04_adapter"),
    "Copycat 05B epoca 2": Path(r"copycat_05b_epoch2_adapter"),
    "Copycat 06 epoca 1": Path(r"copycat_06_epoch1_adapter"),
}

expected_hash = "e783ec268ffcc7758d6473f3cbaa47d0e99436d544e7f05104e17dfa180b15e6"
assert hashlib.sha256(BENCHMARK.read_bytes()).hexdigest() == expected_hash
items = [json.loads(line) for line in BENCHMARK.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(items) == 24
for path in ADAPTERS.values():
    assert (path / "adapter_config.json").exists(), path

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
base.eval()

def generate(model, question):
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": question}], tokenize=False, system_message="")
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=160, do_sample=False, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

with OUTPUT.open("w", encoding="utf-8") as out:
    print("RoMistral bază", flush=True)
    for index, item in enumerate(items, 1):
        answer = generate(base, item["prompt"])
        out.write(json.dumps({**item, "model": "RoMistral bază", "answer": answer}, ensure_ascii=False) + "\n")
        out.flush()
        print(f"{index}/24 {item['id']}: {answer}", flush=True)

    model = PeftModel.from_pretrained(base, str(ADAPTERS["Copycat 04"]), adapter_name="copycat04")
    model.load_adapter(str(ADAPTERS["Copycat 05B epoca 2"]), adapter_name="copycat05b2")
    model.load_adapter(str(ADAPTERS["Copycat 06 epoca 1"]), adapter_name="copycat06")
    model.eval()
    for label, adapter_name in (("Copycat 04", "copycat04"), ("Copycat 05B epoca 2", "copycat05b2"), ("Copycat 06 epoca 1", "copycat06")):
        model.set_adapter(adapter_name)
        print(label, flush=True)
        for index, item in enumerate(items, 1):
            answer = generate(model, item["prompt"])
            out.write(json.dumps({**item, "model": label, "answer": answer}, ensure_ascii=False) + "\n")
            out.flush()
            print(f"{index}/24 {item['id']}: {answer}", flush=True)

assert hashlib.sha256(BENCHMARK.read_bytes()).hexdigest() == expected_hash
print(f"BENCHMARK UNCHANGED {expected_hash}", flush=True)
