"""Run unchanged 36-item edit benchmark and 16-item Lesson 05 benchmark on three adapters."""
import ast
import hashlib
import json
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
DESKTOP = Path(r".")
MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
ADAPTERS = {
    "Copycat 04": DESKTOP / "copycat_editare_04_adapter",
    "Română 01": DESKTOP / "copycat_romana_naturala_01_adapter",
    "Copycat 05": ROOT / "copycat_05_adapter",
}
SOURCE_36 = ROOT / "benchmark_copycat_03_on_04.py"
SOURCE_16 = ROOT / "benchmark_romana_05.jsonl"
OUTPUT = ROOT / "evaluate_copycat_05_results.jsonl"

tree = ast.parse(SOURCE_36.read_text(encoding="utf-8"))
tests_node = next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "TESTS" for target in node.targets))
tests_36 = ast.literal_eval(tests_node)
tests_16 = [json.loads(line) for line in SOURCE_16.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(tests_36) == 36 and len(tests_16) == 16
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE_36, SOURCE_16]}

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
model = PeftModel.from_pretrained(base, str(ADAPTERS["Copycat 04"]), adapter_name="copycat04")
model.load_adapter(str(ADAPTERS["Română 01"]), adapter_name="romana01")
model.load_adapter(str(ADAPTERS["Copycat 05"]), adapter_name="copycat05")
model.eval()

def answer(question):
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": question}], tokenize=False, system_message="")
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=160, do_sample=False, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

names = {"Copycat 04": "copycat04", "Română 01": "romana01", "Copycat 05": "copycat05"}
with OUTPUT.open("w", encoding="utf-8") as out:
    for label, adapter in names.items():
        model.set_adapter(adapter)
        correct = 0
        print(label, flush=True)
        for n, (name, question, target) in enumerate(tests_36, start=1):
            response = answer(question)
            passed = response == target
            correct += passed
            out.write(json.dumps({"benchmark": "editare_36", "model": label, "id": name, "prompt": question, "target": target, "answer": response, "pass": passed}, ensure_ascii=False) + "\n")
            out.flush()
            print(f"edit {n}/36 {name} {'PASS' if passed else 'FAIL'}", flush=True)
        print(f"Editare: {correct}/36", flush=True)
        for n, item in enumerate(tests_16, start=1):
            response = answer(item["prompt"])
            out.write(json.dumps({"benchmark": "romana_05_16", "model": label, **item, "answer": response}, ensure_ascii=False) + "\n")
            out.flush()
            print(f"05 {n}/16 {item['id']}: {response}", flush=True)

after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE_36, SOURCE_16]}
assert before == after, (before, after)
print("Benchmarks unchanged", before, flush=True)
