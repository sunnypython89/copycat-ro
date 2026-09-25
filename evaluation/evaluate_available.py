"""Portable semantic-only inference; does not reconstruct or score editing tests."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23'
BENCHMARKS = [
    ('lectia_05', 'benchmark_romana_05.jsonl'),
    ('lectia_06', 'benchmark_ambiguitate_06.jsonl'),
    ('lectia_07', 'benchmark_eliminare_07.jsonl'),
    ('lectia_08', 'benchmark_prag_08.jsonl'),
    ('lectia_09', 'benchmark_eliminare_secventiala_09.jsonl'),
    ('lectia_10', 'benchmark_consolidare_10.jsonl'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', required=True, choices=['04','05','05b','05b_epoch2','06','07','08','09','10'])
    parser.add_argument('--adapter', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--check-only', action='store_true', help='Validate data and planned generation settings without importing ML libraries.')
    args = parser.parse_args()
    limit = int(args.checkpoint[:2])
    selected = BENCHMARKS[:max(1, limit-4)]
    max_new_tokens = 384 if args.checkpoint == '10' else 160
    expected = {line.split()[1]:line.split()[0] for line in (ROOT/'benchmarks/HASHES.sha256').read_text().splitlines()}
    data = {}
    for name, filename in selected:
        path = ROOT/'benchmarks'/filename
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected[filename]:
            raise SystemExit(f'Benchmark hash mismatch: {filename}')
        data[name] = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing output.')
    print(json.dumps({'benchmarks':{k:len(v) for k,v in data.items()},'max_new_tokens':max_new_tokens,'do_sample':False,'scope':'semantic-only; fresh human scoring required'}))
    if args.check_only:
        return
    if not (args.adapter/'adapter_config.json').is_file():
        raise SystemExit('Provide an independently reproduced local adapter directory.')
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                               bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
    base = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=quant, device_map='auto')
    model = PeftModel.from_pretrained(base, str(args.adapter))
    model.eval()
    with args.output.open('x', encoding='utf-8', newline='\n') as output:
        for name, items in data.items():
            for item in items:
                prompt = tokenizer.apply_chat_template([{'role':'user','content':item['prompt']}], tokenize=False, system_message='')
                inputs = tokenizer(prompt, return_tensors='pt', add_special_tokens=False).to(model.device)
                with torch.no_grad():
                    generated = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False,
                                               eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
                answer = tokenizer.decode(generated[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
                output.write(json.dumps({'benchmark':name, **item, 'answer':answer}, ensure_ascii=False)+'\n')
                output.flush()
    for _, filename in selected:
        if hashlib.sha256((ROOT/'benchmarks'/filename).read_bytes()).hexdigest() != expected[filename]:
            raise SystemExit(f'Benchmark changed during evaluation: {filename}')


if __name__ == '__main__':
    main()
