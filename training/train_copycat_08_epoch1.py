"""Train Lesson 08 for exactly one epoch from Copycat 07 epoch 1."""
import hashlib, json, math, random
from pathlib import Path
import torch
from peft import PeftModel, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

ROOT=Path(__file__).resolve().parent
MODEL='OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23'
START_ADAPTER=ROOT/'copycat_07_epoch1_adapter'
SOURCES=[ROOT/'gold_editare_04.jsonl',ROOT/'replay_05b_incertitudine_noop.jsonl',ROOT/'replay_08_gold06_clean_30.jsonl',ROOT/'replay_08_gold07_clean_30.jsonl',ROOT/'gold_prag_08_training_filtered.jsonl']
BENCHMARKS=[ROOT/'benchmark_copycat_03_on_04.py',ROOT/'benchmark_romana_05.jsonl',ROOT/'benchmark_ambiguitate_06.jsonl',ROOT/'benchmark_eliminare_07.jsonl',ROOT/'benchmark_prag_08.jsonl']
OUTPUT=ROOT/'copycat_08_epoch1_adapter'
EXPECTED={'benchmark_copycat_03_on_04.py':'8b27807ea0350b13297e4201234582a3a27a626047710f96c27ebe08ed247ad0','benchmark_romana_05.jsonl':'733bc505e4feaa3388a19490c8733adf71053bdd16055492b3832b2b56cd7aac','benchmark_ambiguitate_06.jsonl':'117ec316c4f596ddd02b4314f1ad005fcc89d1ba71017bfb70eb1aa9a3023332','benchmark_eliminare_07.jsonl':'e783ec268ffcc7758d6473f3cbaa47d0e99436d544e7f05104e17dfa180b15e6','benchmark_prag_08.jsonl':'ee1540a10a4b0b98119670fe91018329e1582c7b4e231a6ec707409db6d04104'}
SEED,EPOCHS,LR,MAX_LENGTH,GRAD_ACCUM=42,1,3e-5,384,4
if OUTPUT.exists(): raise SystemExit(f'Refuz suprascrierea: {OUTPUT}')
if not (START_ADAPTER/'adapter_config.json').exists(): raise SystemExit('Lipsește adaptorul de pornire')
if not torch.cuda.is_available(): raise SystemExit('CUDA este necesar')
for p in BENCHMARKS: assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED[p.name]
random.seed(SEED); torch.manual_seed(SEED)
def read(path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
counts=[len(read(p)) for p in SOURCES]
assert counts==[104,62,30,30,94],counts
records=[x for p in SOURCES for x in read(p)]
assert len(records)==320
tokenizer=AutoTokenizer.from_pretrained(MODEL)
if tokenizer.pad_token_id is None: tokenizer.pad_token=tokenizer.eos_token
quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
base=AutoModelForCausalLM.from_pretrained(MODEL,quantization_config=quant,device_map='auto')
base.config.use_cache=False
base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=True)
model=PeftModel.from_pretrained(base,str(START_ADAPTER),is_trainable=True)
model.print_trainable_parameters()
config=model.peft_config['default']
assert (config.r,config.lora_alpha,config.lora_dropout,set(config.target_modules))==(8,16,0.05,{'q_proj','v_proj'})
def encode(record):
    messages=record['messages']; assert len(messages)==2
    prompt=tokenizer.apply_chat_template(messages[:1],tokenize=False,system_message='')
    full=tokenizer.apply_chat_template(messages,tokenize=False,system_message='')
    prompt_ids=tokenizer(prompt,add_special_tokens=False,truncation=True,max_length=MAX_LENGTH)['input_ids']
    encoded=tokenizer(full,add_special_tokens=False,truncation=True,max_length=MAX_LENGTH,return_tensors='pt')
    labels=encoded['input_ids'].clone(); labels[:,:len(prompt_ids)]=-100
    assert not torch.all(labels==-100)
    return encoded['input_ids'],encoded['attention_mask'],labels
encoded=[encode(x) for x in records]
trainable=[p for p in model.parameters() if p.requires_grad]
optimizer=torch.optim.AdamW(trainable,lr=LR)
order=list(range(len(encoded))); random.Random(SEED).shuffle(order)
total_steps=math.ceil(len(encoded)/GRAD_ACCUM); optimizer.zero_grad(set_to_none=True); model.train(); losses=[]; global_step=0
print(f'GPU={torch.cuda.get_device_name(0)} records={len(records)} epochs=1 steps={total_steps}',flush=True)
for micro_step,idx in enumerate(order,1):
    ids,mask,labels=encoded[idx]
    output=model(input_ids=ids.to(model.device),attention_mask=mask.to(model.device),labels=labels.to(model.device))
    loss=output.loss; (loss/GRAD_ACCUM).backward(); losses.append(loss.item())
    if micro_step%GRAD_ACCUM==0 or micro_step==len(order):
        torch.nn.utils.clip_grad_norm_(trainable,1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); global_step+=1
        if global_step==1 or global_step%10==0: print(f'step={global_step}/{total_steps} loss={loss.item():.6f}',flush=True)
mean_loss=sum(losses)/len(losses)
OUTPUT.mkdir(); model.save_pretrained(OUTPUT); tokenizer.save_pretrained(OUTPUT)
meta={'base_model':MODEL,'starting_adapter':str(START_ADAPTER),'starting_adapter_sha256':hashlib.sha256((START_ADAPTER/'adapter_model.safetensors').read_bytes()).hexdigest(),'sources':[{'name':p.name,'count':len(read(p)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in SOURCES],'lesson':'08','epochs_this_run':1,'learning_rate':LR,'seed':SEED,'batch_size':1,'gradient_accumulation':GRAD_ACCUM,'max_length':MAX_LENGTH,'lora_r':config.r,'lora_alpha':config.lora_alpha,'lora_dropout':config.lora_dropout,'target_modules':sorted(config.target_modules),'optimizer_steps':global_step,'mean_loss':mean_loss,'benchmark_hashes_before':EXPECTED,'benchmark_hashes_after':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BENCHMARKS}}
assert meta['benchmark_hashes_before']==meta['benchmark_hashes_after']
(OUTPUT/'copycat_training.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'epoch=1 mean_loss={mean_loss:.6f}',flush=True); print(f'SAVED {OUTPUT}',flush=True)
