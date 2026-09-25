"""Strict scoring, consolidation metrics, oracle-common diagnostics, and final report."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (ROOT/'evaluate_copycat_10_epoch1_results.jsonl').read_text(encoding='utf-8').splitlines()]
passes={
'lectia_05':set('A2 I1 U1 U2 U3 U4 T1 T2 T3'.split()),
'lectia_06':set('RA5 RA6 RA7 NA1 NA3 NA5 NA6 NA7 NA8 TP1 TP2 TP4'.split()),
'lectia_07':set('R2 R3 R5 R6 R8 I1 I3 I4 I5 I6 M2 M4 M5 M6 D1 D3 D4'.split()),
'lectia_08':set('F1A F1C F2A F2C F3A F3C F3D F4C F5A F5C F6A F6B F6D F7A F7C F7D F8B F8C F8D'.split()),
'lectia_09':set('F1D2 F1AM F2D2 F2D3 F2AM F2IR F3D2 F3AM F4D2 F4AM F5D2 F5AM F5IR F6D2 F6AM F6IR F7D2 F7AM F8AM F8IR'.split()),
'lectia_10':set('F1A F1C F1D F2A F2B F2D F3A F3B F3C F3D F4A F5A F5B F5C F6A F6B F6C F7A F7B F7C F7D F8B'.split())}
route09=set('F1D2 F1AM F2D2 F2D3 F2AM F2IR F3D2 F3AM F4D2 F4AM F5D2 F5AM F5IR F6AM F6IR F7D2 F7AM F8IR'.split())
route10=set('F1A F1C F1D F2A F2B F2D F3A F3B F3C F3D F4A F5A F5B F5C F6A F6C F7A F7B F7C F7D F8B'.split())
error_labels={
'lectia_06':{'RA1':'certitudine prematură','RA2':'certitudine prematură','RA3':'candidat valid omis','RA4':'candidat valid omis','RA8':'candidat valid omis','NA2':'dovadă relevantă ignorată','NA4':'negație/excepție pierdută','CR1':'dovadă relevantă ignorată','CR2':'dovadă relevantă ignorată','CR3':'dovadă relevantă ignorată','CR4':'dovadă relevantă ignorată','TP3':'candidat inițial omis'},
'lectia_07':{'R1':'concluzie corectă prin justificare greșită','R4':'dovadă relevantă ignorată','R7':'dovadă relevantă ignorată','I2':'indiciu irelevant folosit','M1':'dovadă relevantă ignorată','M3':'dovadă relevantă ignorată','D2':'indiciu irelevant folosit'},
'lectia_08':{},'lectia_09':{},'lectia_10':{}}
scored=[]
for r in rows:
 b=r['benchmark']
 if b=='editare_36': ok=bool(r['pass']); route=None; err=None if ok else 'altă eroare'
 else:
  ok=r['id'] in passes[b]; route=(r['id'] in route09 if b=='lectia_09' else (r['id'] in route10 if b=='lectia_10' else None))
  if ok and route is not False: err=None
  else: err=error_labels.get(b,{}).get(r['id'],'concluzia/traseul nu respectă dovezile')
 scored.append({**r,'pass':ok,'route_pass':route,'error_class':err})
(ROOT/'evaluate_copycat_10_epoch1_scored.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in scored),encoding='utf-8')
def score(b):
 z=[x for x in scored if x['benchmark']==b]; return sum(x['pass'] for x in z),len(z)
def cats(b):
 z=[x for x in scored if x['benchmark']==b]; return {c:sum(x['pass'] for x in z if x.get('category')==c) for c in dict.fromkeys(x.get('category') for x in z)}
def route_stats(b):
 z=[x for x in scored if x['benchmark']==b]; both=sum(x['pass'] and x['route_pass'] for x in z); final_bad=sum(x['pass'] and not x['route_pass'] for x in z); return both,final_bad,len(z)-both-final_bad

bench_scores={'Copycat 07 epoca 1':[14,17,17,22],'Copycat 08 epoca 1':[10,17,19,18],'Copycat 09 epoca 1':[14,18,13,20],'Copycat 10 consolidare':[score(x)[0] for x in ['lectia_06','lectia_07','lectia_08','lectia_09']]}
den=[24,24,32,32]
floors={m:min(v/d for v,d in zip(vals,den)) for m,vals in bench_scores.items()}
families08={'Copycat 07 epoca 1':0,'Copycat 08 epoca 1':3,'Copycat 09 epoca 1':0,'Copycat 10 consolidare':0}
families09={'Copycat 07 epoca 1':2,'Copycat 08 epoca 1':1,'Copycat 09 epoca 1':2,'Copycat 10 consolidare':1}
families10=sum(all(f'F{i}{s}' in passes['lectia_10'] for s in 'ABCD') for i in range(1,9))
wrong_routes09={'Copycat 07 epoca 1':3,'Copycat 08 epoca 1':6,'Copycat 09 epoca 1':1,'Copycat 10 consolidare':route_stats('lectia_09')[1]}
oracle=json.loads((ROOT/'audit_si_complementaritate_10.json').read_text(encoding='utf-8'))['oracle_union']
common={'lectia_06':['RA3','RA4','RA8','NA2','CR2','CR4'],'lectia_07':['M1'],'lectia_08':['F1B','F1D','F4B','F4C','F5A','F6B'],'lectia_09':['F3IR','F8D2','F8AM']}
by={(x['benchmark'],x['id']):x for x in scored}

lines=['# Raport Copycat 10 — Consolidarea bornelor','',
'## Training','', '- Punct de pornire: `copycat_07_epoch1_adapter`.', '- Exact o epocă, learning rate `1e-5`, seed 42.', '- LoRA r=8, alpha=16, dropout=0,05, `q_proj` și `v_proj`.', '- 426 exemple; 107 pași; loss mediu `0,354360752`.','',
'## Scoruri Copycat 10','',f'- Editare 04: **{score("editare_36")[0]}/36**.',f'- Lecția 05: **{score("lectia_05")[0]}/16**.',f'- Lecția 06: **{score("lectia_06")[0]}/24** — {cats("lectia_06")}.',f'- Lecția 07: **{score("lectia_07")[0]}/24** — {cats("lectia_07")}.',f'- Lecția 08: **{score("lectia_08")[0]}/32** — {cats("lectia_08")}.',f'- Lecția 09: **{score("lectia_09")[0]}/32** — {cats("lectia_09")}.',f'- Benchmark 10: **{score("lectia_10")[0]}/32** — {cats("lectia_10")}.','',
'### Traseu Benchmark 10','',f'- Final corect + traseu corect: **{route_stats("lectia_10")[0]}/32**.',f'- Final corect + traseu greșit: **{route_stats("lectia_10")[1]}/32**.',f'- Final greșit: **{route_stats("lectia_10")[2]}/32**.','',
'## Oracle union înainte de consolidare','', '| Benchmark | Toate trei | Numai 07 | Numai 08 | Numai 09 | La două | Greșite toate | Oracle |','|---|---:|---:|---:|---:|---:|---:|---:|']
for b in ['lectia_06','lectia_07','lectia_08','lectia_09']:
 c=oracle[b]['counts']; lines.append(f"| {b} | {c.get('toate trei',0)} | {c.get('numai Copycat 07 epoca 1',0)} | {c.get('numai Copycat 08 epoca 1',0)} | {c.get('numai Copycat 09 epoca 1',0)} | {c.get('la două',0)} | {c.get('greșit la toate',0)} | {oracle[b]['oracle_union']}/{oracle[b]['total']} |")
lines += ['','## Metrica de consolidare','', '| Model | L06 | L07 | L08 | L09 | Podea normalizată | Familii L08 | Familii L09 | Final corect/traseu greșit L09 |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for m,v in bench_scores.items(): lines.append(f"| {m} | {v[0]}/24 | {v[1]}/24 | {v[2]}/32 | {v[3]}/32 | {floors[m]*100:.1f}% | {families08[m]}/8 | {families09[m]}/8 | {wrong_routes09[m]} |")
lines += ['',f'Pe Benchmark 10, Copycat 10 rezolvă integral **{families10}/8** familii contrastive.','',
'## Limitele comune din oracle și răspunsul Copycat 10','']
for b,ids in common.items():
 lines += [f'### {b}','']
 for identifier in ids:
  x=by[(b,identifier)]; status='REZOLVAT de Copycat 10' if x['pass'] and x.get('route_pass') is not False else 'ÎNCĂ GREȘIT'
  lines += [f'#### {identifier} — {status}','',f"**Clasificare:** {x['error_class'] or 'fără eroare'}",'',f"**Răspuns:**  \n{x['answer'].replace(chr(10),'  '+chr(10))}",'']
lines += ['## Toate răspunsurile greșite sau cu traseu greșit ale Copycat 10','']
for b in ['lectia_05','lectia_06','lectia_07','lectia_08','lectia_09','lectia_10']:
 lines += [f'### {b}','']
 for x in scored:
  if x['benchmark']==b and (not x['pass'] or x.get('route_pass') is False):
   lines += [f"#### {x['id']} — {x['error_class']}",'',f"**Prompt:** {x['prompt']}",'',f"**Răspuns:**  \n{x['answer'].replace(chr(10),'  '+chr(10))}",'',f"**Gold:**  \n{x.get('reference','').replace(chr(10),'  '+chr(10))}",'']
lines += ['## Diagnostic de capacitate','',
'- Consolidarea este parțială: podeaua urcă față de Copycat 08 și 09, dar rămâne sub Copycat 07.',
'- Copycat 10 egalează scorul 09 al lui Copycat 09 și scorul 08 al lui Copycat 08, dar pierde la Lecțiile 06 și 07 față de cele mai bune borne individuale.',
'- Oscilația persistă: păstrarea ambiguității este bună, însă indiciile relevante și traseele secvențiale mai lungi sunt încă fragile.',
'- Pentru etapa următoare merită evaluat separat fie un LoRA cu capacitate mai mare, fie module suplimentare (`k_proj`, `o_proj`), fie adaptoare specializate cu rutare/consolidare. Nu a fost pornit niciun astfel de experiment.','']
(ROOT/'RAPORT_COPYCAT_10_CONSOLIDARE.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'scores':{b:score(b) for b in ['editare_36','lectia_05','lectia_06','lectia_07','lectia_08','lectia_09','lectia_10']},'categories10':cats('lectia_10'),'route10':route_stats('lectia_10'),'floors':floors,'families10':families10},ensure_ascii=False,indent=2))
