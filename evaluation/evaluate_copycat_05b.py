"""Evaluate Copycat 05B on the unchanged 36 + 16 benchmarks."""
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
MODEL = "OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23"
ADAPTER = ROOT / "copycat_05b_adapter"
SOURCE_36 = ROOT / "benchmark_copycat_03_on_04.py"
SOURCE_16 = ROOT / "benchmark_romana_05.jsonl"
OUTPUT = ROOT / "evaluate_copycat_05b_results.jsonl"

tree = ast.parse(SOURCE_36.read_text(encoding="utf-8"))
tests_36 = ast.literal_eval(next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "TESTS" for target in node.targets)))
tests_16 = [json.loads(line) for line in SOURCE_16.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(tests_36) == 36 and len(tests_16) == 16
before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (SOURCE_36, SOURCE_16)}

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
model = PeftModel.from_pretrained(base, str(ADAPTER))
model.eval()

def generate(question):
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": question}], tokenize=False, system_message="")
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=160, do_sample=False, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

with OUTPUT.open("w", encoding="utf-8") as out:
    passed = 0
    for index, (identifier, prompt, target) in enumerate(tests_36, 1):
        answer = generate(prompt)
        ok = answer == target
        passed += ok
        out.write(json.dumps({"benchmark": "editare_36", "id": identifier, "prompt": prompt, "target": target, "answer": answer, "pass": ok}, ensure_ascii=False) + "\n")
        out.flush()
        print(f"edit {index}/36 {identifier} {'PASS' if ok else 'FAIL'}", flush=True)
        if not ok:
            print(f"EXPECTED: {target}\nGOT: {answer}", flush=True)
    print(f"EDIT SCORE {passed}/36", flush=True)
    for index, item in enumerate(tests_16, 1):
        answer = generate(item["prompt"])
        out.write(json.dumps({"benchmark": "romana_05_16", **item, "answer": answer}, ensure_ascii=False) + "\n")
        out.flush()
        print(f"05 {index}/16 {item['id']}: {answer}", flush=True)

after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (SOURCE_36, SOURCE_16)}
assert before == after
print("BENCHMARKS UNCHANGED", before, flush=True)
