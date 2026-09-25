"""Manual semantic scoring and complete report for Copycat 08 epoch 1."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (ROOT/'evaluate_copycat_08_epoch1_results.jsonl').read_text(encoding='utf-8').splitlines()]
passes={
'lectia_05':set('A1 A2 I1 U1 U2 U3 U4 T1 T2 T3'.split()),
'lectia_06':set('RA1 RA2 RA5 RA7 NA4 NA8 TP1 TP2 TP3 TP4'.split()),
'lectia_07':set('R1 R2 R3 R4 R5 I1 I2 I3 I4 I5 I6 M2 M4 M6 D1 D2 D3'.split()),
'lectia_08':set('F1A F1C F2A F2B F2C F2D F3A F3B F3C F6A F6C F6D F7A F7B F7D F8A F8B F8C F8D'.split()),
}
errors={
'lectia_05':{'A3':'certitudine prematură','A4':'certitudine prematură','I2':'altă eroare','I3':'altă eroare','I4':'altă eroare','T4':'altă eroare'},
'lectia_06':{'RA3':'candidat valid omis','RA4':'candidat valid omis','RA6':'concluzia nu rezultă din propriile variante și dovezi','RA8':'candidat valid omis','NA1':'incertitudine păstrată prea mult','NA2':'incertitudine păstrată prea mult','NA3':'incertitudine păstrată prea mult','NA5':'incertitudine păstrată prea mult','NA6':'incertitudine păstrată prea mult','NA7':'incertitudine păstrată prea mult','CR1':'indiciu relevant ignorat','CR2':'indiciu relevant ignorat','CR3':'indiciu relevant ignorat','CR4':'indiciu relevant ignorat'},
'lectia_07':{'R6':'candidat invalid păstrat','R7':'indiciu relevant ignorat','R8':'incertitudine păstrată prea mult','M1':'indiciu relevant ignorat','M3':'indiciu relevant ignorat','M5':'concluzia nu rezultă din propriile variante și dovezi','D4':'candidat valid omis'},
'lectia_08':{'F1B':'indiciu relevant ignorat','F1D':'candidat invalid păstrat','F3D':'concluzia nu rezultă din propriile variante și dovezi','F4A':'certitudine prematură','F4B':'concluzia nu rezultă din propriile variante și dovezi','F4C':'indiciu irelevant folosit','F4D':'concluzia nu rezultă din propriile variante și dovezi','F5A':'candidat valid omis','F5B':'candidat invalid păstrat','F5C':'candidat valid omis','F5D':'concluzia nu rezultă din propriile variante și dovezi','F6B':'indiciu relevant ignorat','F7C':'indiciu irelevant folosit'},
}
# Debatable responses remain failures under the strict benchmark rubric and are also called out for human review.
scored=[]
for r in rows:
    b=r['benchmark']
    if b=='editare_36': ok=bool(r['pass']); error=None if ok else 'altă eroare'
    else:
        ok=r['id'] in passes[b]
        if not ok: assert r['id'] in errors[b],(b,r['id'])
        error=None if ok else errors[b][r['id']]
    scored.append({**r,'pass':ok,'error_class':error})
(ROOT/'evaluate_copycat_08_epoch1_scored.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in scored),encoding='utf-8')

cat_names={'lectia_05':['ambiguitate','idiom','incertitudine','ton'],'lectia_06':['ambiguitate_reala','neambiguu','context_rezolva','trei_plus'],'lectia_07':['context_rezolva','context_insuficient','eliminare_multipla','indiciu_irelevant'],'lectia_08':['ambiguu','rezolvat','indiciu_irelevant','eliminare_multipla']}
def stats(bench):
    z=[x for x in scored if x['benchmark']==bench]
    return sum(x['pass'] for x in z),{c:sum(x['pass'] for x in z if x.get('category')==c) for c in cat_names.get(bench,[])}
comparison={
'Copycat 05B epoca 2':{'editare':36,'l05':7,'l06':16,'l07':15,'l08':13},
'Copycat 06 epoca 1':{'editare':36,'l05':5,'l06':15,'l07':16,'l08':10},
'Copycat 07 epoca 1':{'editare':36,'l05':8,'l06':14,'l07':17,'l08':17},
'Copycat 08 epoca 1':{'editare':stats('editare_36')[0],'l05':stats('lectia_05')[0],'l06':stats('lectia_06')[0],'l07':stats('lectia_07')[0],'l08':stats('lectia_08')[0]},
}
triplets=[]
for i in range(1,9):
    ids=[f'F{i}{s}' for s in 'ABC']; ok={x['id']:x['pass'] for x in scored if x['benchmark']=='lectia_08'}
    triplets.append((f'F{i}',*[ok[x] for x in ids]))
complete=[g for g,a,b,c in triplets if a and b and c]
diag_excluded={'F2B','F4B','F5B'}
l08=[x for x in scored if x['benchmark']=='lectia_08']
diag=[x for x in l08 if x['id'] not in diag_excluded]

lines=['# Raport Copycat 08 — epoca 1','',
'## Configurația trainingului','',
'- Pornire trainabilă: `copycat_07_epoch1_adapter`.','- O epocă, learning rate `3e-5`, seed 42.','- LoRA: r=8, alpha=16, dropout=0,05, `q_proj` și `v_proj`.','- 320 exemple: 104 Editare 04, 35 NOOP, 27 incertitudine, 30 Lecția 06, 30 Lecția 07 și 94 Gold 08 filtrate.','- 80 pași de optimizare; loss mediu: `0,3046272418`.','',
'## Scoruri Copycat 08','',
f"- Editare 04: **{stats('editare_36')[0]}/36**.",f"- Lecția 05: **{stats('lectia_05')[0]}/16** — {stats('lectia_05')[1]}.",f"- Lecția 06: **{stats('lectia_06')[0]}/24** — {stats('lectia_06')[1]}.",f"- Lecția 07: **{stats('lectia_07')[0]}/24** — {stats('lectia_07')[1]}.",f"- Lecția 08 oficial: **{stats('lectia_08')[0]}/32** — {stats('lectia_08')[1]}.",f"- Lecția 08 diagnostic, fără F2B, F4B și F5B: **{sum(x['pass'] for x in diag)}/29**.",'',
'## Comparație','',
'| Model | Editare /36 | L05 /16 | L06 /24 | L07 /24 | L08 /32 |','|---|---:|---:|---:|---:|---:|']
for model,s in comparison.items(): lines.append(f"| {model} | {s['editare']} | {s['l05']} | {s['l06']} | {s['l07']} | {s['l08']} |")
lines += ['','## Triplete A/B/C','',f"Familii cu toate cele trei stări corecte: **{len(complete)}/8** — {', '.join(complete)}.",'']
for g,a,b,c in triplets: lines.append(f"- {g}: A={'✓' if a else '✗'}, B={'✓' if b else '✗'}, C={'✓' if c else '✗'}.")
lines += ['','## Toate răspunsurile greșite','']
for bench in ['lectia_05','lectia_06','lectia_07','lectia_08']:
    lines += [f'### {bench}','']
    for x in scored:
        if x['benchmark']==bench and not x['pass']:
            ref=x.get('reference') or x.get('criteria') or ''
            lines += [f"#### {x['id']} — {x['error_class']}",'',f"**Prompt:** {x['prompt']}",'',f"**Răspuns:**  \n{x['answer'].replace(chr(10),'  '+chr(10))}",'',f"**Gold:**  \n{ref.replace(chr(10),'  '+chr(10))}",'']
lines += ['## Răspunsuri discutabile','',
'- **F2B:** Gold-ul presupune că prezența Sandei la ghișeu în timpul chemării o exclude; chemarea ar putea avea loc chiar la ghișeu. Este corect în scorul oficial, dar exclus din diagnosticul cerut.',
'- **F4B:** „nu a avut niciodată stilou” poate descrie perioada de dinaintea primirii. Răspunsul modelului formulează acțiunea, nu posesia. Este marcat greșit și exclus din diagnosticul cerut.',
'- **F5B:** lipsa urcării pe scenă nu exclude logic deschiderea ceremoniei din alt loc; modelul inventează candidatul „echipa A”. Este marcat greșit și exclus din diagnostic.',
'- **F5A/F5C:** modelul declară ambiguitatea, dar omite candidații reali și îi înlocuiește cu „una/ambele”, respectiv „Vest/niciuna”. Sunt marcate greșit în evaluarea strictă.',
'- **R4, R6 și D3 din benchmarkul 07** rămân probele marcate anterior pentru revizuire umană; benchmarkul nu a fost modificat.','']
lines += ['## Pierderi și câștiguri','',
'- Lecția 08 crește de la 17/32 la 19/32 și urcă simultan la ambiguu (3→6) și rezolvat (3→4).',
'- Indiciile irelevante cresc de la 4/8 la 5/8; erorile explicite rămân F4C și F7C.',
'- Tripletele complete cresc de la 0/8 la 3/8.',
'- Editarea rămâne 36/36. Lecția 05 crește 8→10, Lecția 06 scade 14→10, Lecția 07 rămâne 17/24.',
'- Regresia principală este hiperprudența pe cazurile neambigue/contextuale din Lecția 06 și eliminarea greșită în mai mulți pași. Aceste erori sunt reparabile prin replay țintit, fără a schimba benchmarkurile.','']
(ROOT/'RAPORT_COPYCAT_08_EPOCH1.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'scores':{b:stats(b) for b in ['editare_36','lectia_05','lectia_06','lectia_07','lectia_08']},'diagnostic_08':[sum(x['pass'] for x in diag),len(diag)],'complete_triplets':complete,'errors':Counter(x['error_class'] for x in scored if not x['pass'])},ensure_ascii=False,indent=2))
