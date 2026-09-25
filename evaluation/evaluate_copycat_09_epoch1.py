"""Evaluate Copycat 09 epoch 1 on all six frozen benchmarks."""
import ast, hashlib, json, sys
from pathlib import Path
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
MODEL='OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23'
ADAPTER=ROOT/'copycat_09_epoch1_adapter'
OUTPUT=ROOT/'evaluate_copycat_09_epoch1_results.jsonl'
FILES={'editare_36':ROOT/'benchmark_copycat_03_on_04.py','lectia_05':ROOT/'benchmark_romana_05.jsonl','lectia_06':ROOT/'benchmark_ambiguitate_06.jsonl','lectia_07':ROOT/'benchmark_eliminare_07.jsonl','lectia_08':ROOT/'benchmark_prag_08.jsonl','lectia_09':ROOT/'benchmark_eliminare_secventiala_09.jsonl'}
EXPECTED={'benchmark_copycat_03_on_04.py':'8b27807ea0350b13297e4201234582a3a27a626047710f96c27ebe08ed247ad0','benchmark_romana_05.jsonl':'733bc505e4feaa3388a19490c8733adf71053bdd16055492b3832b2b56cd7aac','benchmark_ambiguitate_06.jsonl':'117ec316c4f596ddd02b4314f1ad005fcc89d1ba71017bfb70eb1aa9a3023332','benchmark_eliminare_07.jsonl':'e783ec268ffcc7758d6473f3cbaa47d0e99436d544e7f05104e17dfa180b15e6','benchmark_prag_08.jsonl':'ee1540a10a4b0b98119670fe91018329e1582c7b4e231a6ec707409db6d04104','benchmark_eliminare_secventiala_09.jsonl':'5c7705741c675b2a5df10d0c97b1071f5d46c55c400554bc4abcbf1dd63d6570'}
if OUTPUT.exists(): raise SystemExit(f'Refuz suprascrierea: {OUTPUT}')
for p in FILES.values(): assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED[p.name]
tree=ast.parse(FILES['editare_36'].read_text(encoding='utf-8'))
edit=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TESTS' for t in n.targets)))
sets={k:[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] for k,p in FILES.items() if k!='editare_36'}
assert len(edit)==36 and {k:len(v) for k,v in sets.items()}=={'lectia_05':16,'lectia_06':24,'lectia_07':24,'lectia_08':32,'lectia_09':32}
tokenizer=AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None: tokenizer.pad_token=tokenizer.eos_token
quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
base=AutoModelForCausalLM.from_pretrained(MODEL,quantization_config=quant,device_map='auto')
model=PeftModel.from_pretrained(base,str(ADAPTER)); model.eval()
def generate(text):
    prompt=tokenizer.apply_chat_template([{'role':'user','content':text}],tokenize=False,system_message='')
    inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).to(model.device)
    with torch.no_grad(): out=model.generate(**inputs,max_new_tokens=160,do_sample=False,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(out[0][inputs['input_ids'].shape[1]:],skip_special_tokens=True).strip()
with OUTPUT.open('w',encoding='utf-8') as out:
    exact=0
    for i,(identifier,prompt,target) in enumerate(edit,1):
        answer=generate(prompt); passed=answer==target; exact+=passed
        out.write(json.dumps({'benchmark':'editare_36','id':identifier,'prompt':prompt,'target':target,'answer':answer,'pass':passed},ensure_ascii=False)+'\n'); out.flush()
        print(f'EDIT {i}/36 {identifier} {"PASS" if passed else "FAIL"}',flush=True)
    print(f'EDIT SCORE {exact}/36',flush=True)
    for name,items in sets.items():
        for i,item in enumerate(items,1):
            answer=generate(item['prompt']); out.write(json.dumps({'benchmark':name,**item,'answer':answer},ensure_ascii=False)+'\n'); out.flush()
            print(f'{name} {i}/{len(items)} {item["id"]}: {answer}',flush=True)
for p in FILES.values(): assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED[p.name]
print('ALL BENCHMARKS UNCHANGED',flush=True)
