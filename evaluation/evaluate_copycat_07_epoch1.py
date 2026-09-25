"""Evaluate Copycat 07 epoch 1 on all frozen benchmarks."""
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
ADAPTER = ROOT / "copycat_07_epoch1_adapter"
EDIT_SOURCE = ROOT / "benchmark_copycat_03_on_04.py"
LESSON05 = ROOT / "benchmark_romana_05.jsonl"
LESSON06 = ROOT / "benchmark_ambiguitate_06.jsonl"
LESSON07 = ROOT / "benchmark_eliminare_07.jsonl"
OUTPUT = ROOT / "evaluate_copycat_07_epoch1_results.jsonl"
EXPECTED = {
    EDIT_SOURCE.name: "8b27807ea0350b13297e4201234582a3a27a626047710f96c27ebe08ed247ad0",
    LESSON05.name: "733bc505e4feaa3388a19490c8733adf71053bdd16055492b3832b2b56cd7aac",
    LESSON06.name: "117ec316c4f596ddd02b4314f1ad005fcc89d1ba71017bfb70eb1aa9a3023332",
    LESSON07.name: "e783ec268ffcc7758d6473f3cbaa47d0e99436d544e7f05104e17dfa180b15e6",
}

for path in (EDIT_SOURCE, LESSON05, LESSON06, LESSON07):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[path.name]
tree = ast.parse(EDIT_SOURCE.read_text(encoding="utf-8"))
edit = ast.literal_eval(next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "TESTS" for target in node.targets)))
lesson05 = [json.loads(line) for line in LESSON05.read_text(encoding="utf-8").splitlines() if line.strip()]
lesson06 = [json.loads(line) for line in LESSON06.read_text(encoding="utf-8").splitlines() if line.strip()]
lesson07 = [json.loads(line) for line in LESSON07.read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(edit) == 36 and len(lesson05) == 16 and len(lesson06) == 24 and len(lesson07) == 24

tokenizer = AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map="auto")
model = PeftModel.from_pretrained(base, str(ADAPTER))
model.eval()

def generate(prompt_text):
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": prompt_text}], tokenize=False, system_message="")
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=160, do_sample=False, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

with OUTPUT.open("w", encoding="utf-8") as out:
    exact = 0
    for index, (identifier, prompt, target) in enumerate(edit, 1):
        answer = generate(prompt)
        passed = answer == target
        exact += passed
        out.write(json.dumps({"benchmark":"editare_36","id":identifier,"prompt":prompt,"target":target,"answer":answer,"pass":passed},ensure_ascii=False)+"\n")
        out.flush(); print(f"EDIT {index}/36 {identifier} {'PASS' if passed else 'FAIL'}",flush=True)
    print(f"EDIT SCORE {exact}/36",flush=True)
    for index,item in enumerate(lesson05,1):
        answer=generate(item["prompt"])
        out.write(json.dumps({"benchmark":"lectia_05",**item,"answer":answer},ensure_ascii=False)+"\n")
        out.flush(); print(f"L05 {index}/16 {item['id']}: {answer}",flush=True)
    for index,item in enumerate(lesson06,1):
        answer=generate(item["prompt"])
        out.write(json.dumps({"benchmark":"lectia_06",**item,"answer":answer},ensure_ascii=False)+"\n")
        out.flush(); print(f"L06 {index}/24 {item['id']}: {answer}",flush=True)
    for index,item in enumerate(lesson07,1):
        answer=generate(item["prompt"])
        out.write(json.dumps({"benchmark":"lectia_07",**item,"answer":answer},ensure_ascii=False)+"\n")
        out.flush(); print(f"L07 {index}/24 {item['id']}: {answer}",flush=True)

for path in (EDIT_SOURCE, LESSON05, LESSON06, LESSON07):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[path.name]
print("ALL BENCHMARKS UNCHANGED",flush=True)
