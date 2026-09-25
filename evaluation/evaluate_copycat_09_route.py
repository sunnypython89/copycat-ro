"""Re-run only frozen Benchmark 09 with enough output budget for full routes."""
import hashlib,json,sys
from pathlib import Path
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent; MODEL='OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23'
BENCH=ROOT/'benchmark_eliminare_secventiala_09.jsonl'; OUT=ROOT/'evaluate_copycat_09_route_results.jsonl'; ADAPTER=ROOT/'copycat_09_epoch1_adapter'
HASH='5c7705741c675b2a5df10d0c97b1071f5d46c55c400554bc4abcbf1dd63d6570'
assert hashlib.sha256(BENCH.read_bytes()).hexdigest()==HASH and not OUT.exists()
items=[json.loads(x) for x in BENCH.read_text(encoding='utf-8').splitlines() if x.strip()]
tok=AutoTokenizer.from_pretrained(MODEL)
if tok.pad_token_id is None: tok.pad_token=tok.eos_token
q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
base=AutoModelForCausalLM.from_pretrained(MODEL,quantization_config=q,device_map='auto'); model=PeftModel.from_pretrained(base,str(ADAPTER)); model.eval()
with OUT.open('w',encoding='utf-8') as out:
  for i,x in enumerate(items,1):
    prompt=tok.apply_chat_template([{'role':'user','content':x['prompt']}],tokenize=False,system_message=''); inputs=tok(prompt,return_tensors='pt',add_special_tokens=False).to(model.device)
    with torch.no_grad(): generated=model.generate(**inputs,max_new_tokens=384,do_sample=False,eos_token_id=tok.eos_token_id,pad_token_id=tok.pad_token_id)
    answer=tok.decode(generated[0][inputs['input_ids'].shape[1]:],skip_special_tokens=True).strip(); out.write(json.dumps({**x,'answer':answer},ensure_ascii=False)+'\n'); out.flush(); print(f'{i}/32 {x["id"]}: {answer}',flush=True)
assert hashlib.sha256(BENCH.read_bytes()).hexdigest()==HASH
print('BENCHMARK 09 UNCHANGED',flush=True)
