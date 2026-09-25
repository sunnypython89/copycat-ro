"""Score Copycat 09, including final-answer and route consistency metrics."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
allrows=[json.loads(x) for x in (ROOT/'evaluate_copycat_09_epoch1_results.jsonl').read_text(encoding='utf-8').splitlines()]
route09=[json.loads(x) for x in (ROOT/'evaluate_copycat_09_route_results.jsonl').read_text(encoding='utf-8').splitlines()]
passes={
'lectia_05':set('I1 U1 U2 U3 U4 T1 T2 T3'.split()),
'lectia_06':set('RA2 RA5 RA6 RA7 NA1 NA3 NA4 NA5 NA6 NA8 TP1 TP2 TP3 TP4'.split()),
'lectia_07':set('R1 R2 R3 R4 R5 R6 R7 R8 I1 I2 I3 I4 M2 M3 M4 M5 M6 D2'.split()),
'lectia_08':set('F1A F2A F2D F3A F3D F4A F5D F6A F7A F7B F7D F8B F8D'.split())}
generic_error={b:{} for b in passes}
for b,ids in {'lectia_05':'A1 A2 A3 A4 I2 I3 I4 T4','lectia_06':'RA1 RA3 RA4 RA8 NA2 NA7 CR1 CR2 CR3 CR4','lectia_07':'I5 I6 M1 D1 D3 D4','lectia_08':'F1B F1C F1D F2B F2C F3B F3C F4B F4C F4D F5A F5B F5C F6B F6C F6D F7C F8A F8C'}.items():
    for x in ids.split(): generic_error[b][x]='altă eroare'

scored=[]
for r in allrows:
    b=r['benchmark']
    if b=='lectia_09': continue
    if b=='editare_36': ok=bool(r['pass']); error=None if ok else 'altă eroare'
    else: ok=r['id'] in passes[b]; error=None if ok else generic_error[b][r['id']]
    scored.append({**r,'pass':ok,'error_class':error})

route_ok=set('F1D2 F2D2 F3D2 F4D2 F5D2 F7D2 F2D3 F3D3 F4D3 F5D3 F7D3 F2AM F3AM F4AM F5AM F7AM F2IR F4IR F6IR'.split())
final_only={'F8IR'}
route_errors={'F1D3':'dovadă relevantă ignorată','F6D2':'candidat inițial omis','F8D2':'candidat inițial omis','F6D3':'concluzia nu corespunde traseului','F8D3':'oprire prea devreme','F1AM':'concluzia nu corespunde traseului','F6AM':'candidat inițial omis','F8AM':'candidat eliminat reapare','F1IR':'indiciu irelevant folosit','F3IR':'indiciu irelevant folosit','F5IR':'indiciu irelevant folosit','F7IR':'indiciu irelevant folosit','F8IR':'oprire prea devreme'}
for r in route09:
    ro=r['id'] in route_ok; final=ro or r['id'] in final_only
    assert ro or r['id'] in route_errors
    scored.append({**r,'benchmark':'lectia_09','pass':final,'route_pass':ro,'outcome':'răspuns final corect + traseu corect' if ro else ('răspuns final corect + traseu greșit' if final else 'răspuns final greșit'),'error_class':None if ro else route_errors[r['id']]})
(ROOT/'evaluate_copycat_09_epoch1_scored.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in scored),encoding='utf-8')

def score(b):
 z=[x for x in scored if x['benchmark']==b]; return sum(x['pass'] for x in z),len(z)
cats={}
for b in ['lectia_05','lectia_06','lectia_07','lectia_08','lectia_09']:
 z=[x for x in scored if x['benchmark']==b]; cats[b]={c:sum(x['pass'] for x in z if x.get('category')==c) for c in dict.fromkeys(x.get('category') for x in z)}

# Manually reviewed baseline outcomes on Benchmark 09.
base={'Copycat 07 epoca 1':{'final_route':19,'final_bad_route':3,'wrong':10,'total':22,'cats':[7,5,4,6]},'Copycat 08 epoca 1':{'final_route':12,'final_bad_route':6,'wrong':14,'total':18,'cats':[6,3,4,5]},'Copycat 09 epoca 1':{'final_route':19,'final_bad_route':1,'wrong':12,'total':20,'cats':[6,5,5,4]}}

lines=['# Raport Copycat 09 — epoca 1','',
'## Training','', '- Pornire: `copycat_08_epoch1_adapter`, trainabil.', '- Exact o epocă, learning rate `2e-5`, seed 42.', '- LoRA r=8, alpha=16, dropout=0,05, `q_proj` și `v_proj`.', '- 336 exemple; 84 pași de optimizare; loss mediu `0,0960052912`.','',
'## Scoruri Copycat 09','',f'- Editare 04: **{score("editare_36")[0]}/36**.',f'- Lecția 05: **{score("lectia_05")[0]}/16** — {cats["lectia_05"]}.',f'- Lecția 06: **{score("lectia_06")[0]}/24** — {cats["lectia_06"]}.',f'- Lecția 07: **{score("lectia_07")[0]}/24** — {cats["lectia_07"]}.',f'- Lecția 08: **{score("lectia_08")[0]}/32** — {cats["lectia_08"]}.',f'- Lecția 09: **{score("lectia_09")[0]}/32** — {cats["lectia_09"]}.','',
'## Consistența traseului pe Lecția 09','',f'- Răspuns final corect + traseu corect: **{len(route_ok)}/32**.',f'- Răspuns final corect + traseu greșit: **{len(final_only)}/32** — F8IR.',f'- Răspuns final greșit: **{32-len(route_ok)-len(final_only)}/32**.','',
'## Comparație Lecția 09','', '| Model | 2 pași /8 | 3+ pași /8 | Ambiguitate /8 | Irelevant /8 | Final /32 | Final+traseu | Final corect, traseu greșit | Greșit |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for m,s in base.items(): lines.append(f"| {m} | {s['cats'][0]} | {s['cats'][1]} | {s['cats'][2]} | {s['cats'][3]} | {s['total']} | {s['final_route']} | {s['final_bad_route']} | {s['wrong']} |")
lines += ['','## Comparație pe benchmarkurile vechi','', '| Model | Editare /36 | L05 /16 | L06 /24 | L07 /24 | L08 /32 |','|---|---:|---:|---:|---:|---:|','| Copycat 07 epoca 1 | 36 | 8 | 14 | 17 | 17 |','| Copycat 08 epoca 1 | 36 | 10 | 10 | 17 | 19 |',f'| Copycat 09 epoca 1 | {score("editare_36")[0]} | {score("lectia_05")[0]} | {score("lectia_06")[0]} | {score("lectia_07")[0]} | {score("lectia_08")[0]} |','',
'## Toate erorile Copycat 09','']
for b in ['lectia_05','lectia_06','lectia_07','lectia_08','lectia_09']:
 lines += [f'### {b}','']
 for x in scored:
  if x['benchmark']==b and (not x['pass'] or (b=='lectia_09' and not x.get('route_pass',True))):
   ref=x.get('reference',''); lines += [f"#### {x['id']} — {x['error_class']}",'',f"**Rezultat:** {x.get('outcome','răspuns greșit')}",'',f"**Prompt:** {x['prompt']}",'',f"**Răspuns:**  \n{x['answer'].replace(chr(10),'  '+chr(10))}",'',f"**Gold:**  \n{ref.replace(chr(10),'  '+chr(10))}",'']
lines += ['## Interpretare','',
'- Față de Copycat 08, Lecția 09 recuperează eliminările secvențiale: pe categoriile 2+3 pași urcă de la 9/16 la 11/16, iar pe Lecția 07 eliminarea multiplă urcă de la 3/6 la 5/6.',
'- Nu depășește Copycat 07 pe verdictul final al benchmarkului 09: 20/32 față de 22/32. Ambele au 19/32 trasee complet corecte; Copycat 09 are mai puține răspunsuri corecte obținute prin traseu greșit.',
'- Câștigul Lecției 08 la prag nu se păstrează: benchmarkul 08 scade de la 19/32 la 13/32, în special la indicii irelevante și variante rezolvate.',
'- Modelul nu forțează sistematic un singur răspuns: păstrează corect ambiguitatea în 5/8 probe după eliminări. Totuși, indiciile irelevante rămân fragile, cu numai 4/8 verdicte finale și 3/8 trasee corecte.',
'- Nu au fost identificate exemple Gold sau benchmark 09 discutabile pentru un vorbitor nativ; toate eliminările sunt formulate explicit.','']
(ROOT/'RAPORT_COPYCAT_09_EPOCH1.md').write_text('\n'.join(lines),encoding='utf-8')
print({'scores':{b:score(b) for b in ['editare_36','lectia_05','lectia_06','lectia_07','lectia_08','lectia_09']},'categories':cats,'route':base['Copycat 09 epoca 1']})
