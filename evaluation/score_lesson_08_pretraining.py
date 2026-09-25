"""Manual semantic rubric for Lesson 08 pretraining outputs."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
IN=ROOT/'benchmark_prag_08_pretraining_results.jsonl'
OUT=ROOT/'benchmark_prag_08_pretraining_scored.jsonl'
REPORT=ROOT/'RAPORT_PRETRAINING_LECTIA_08.md'

passes={
'Copycat 05B epoca 2':set('F1A F2B F2D F3A F3C F3D F4D F5D F6A F6D F7D F8B F8D'.split()),
'Copycat 06 epoca 1':set('F2D F3B F3D F4A F5D F6A F6D F7D F8A F8D'.split()),
'Copycat 07 epoca 1':set('F1A F1C F2B F2D F3A F3C F3D F4D F5B F5C F5D F6D F7C F7D F8A F8B F8D'.split()),
}
errors={
'Copycat 05B epoca 2':{
'F1B':'contradicție între candidați, indiciu și concluzie','F1C':'contradicție între candidați, indiciu și concluzie','F1D':'candidat invalid păstrat','F2A':'certitudine prematură','F2C':'indiciu irelevant folosit','F3B':'indiciu relevant ignorat','F4A':'candidat valid omis','F4B':'indiciu relevant ignorat','F4C':'certitudine prematură','F5A':'candidat valid omis','F5B':'negație/excepție pierdută','F5C':'indiciu irelevant folosit','F6B':'indiciu relevant ignorat','F6C':'contradicție între candidați, indiciu și concluzie','F7A':'candidat valid omis','F7B':'incertitudine păstrată prea mult','F7C':'candidat valid omis','F8A':'candidat valid omis','F8C':'candidat valid omis'},
'Copycat 06 epoca 1':{
'F1A':'certitudine prematură','F1B':'indiciu relevant ignorat','F1C':'indiciu irelevant folosit','F1D':'candidat invalid păstrat','F2A':'certitudine prematură','F2B':'indiciu relevant ignorat','F2C':'indiciu irelevant folosit','F3A':'altă eroare','F3C':'candidat valid omis','F4B':'negație/excepție pierdută','F4C':'certitudine prematură','F4D':'contradicție între candidați, indiciu și concluzie','F5A':'candidat valid omis','F5B':'negație/excepție pierdută','F5C':'indiciu irelevant folosit','F6B':'indiciu relevant ignorat','F6C':'indiciu irelevant folosit','F7A':'candidat valid omis','F7B':'incertitudine păstrată prea mult','F7C':'indiciu irelevant folosit','F8B':'incertitudine păstrată prea mult','F8C':'candidat valid omis'},
'Copycat 07 epoca 1':{
'F1B':'indiciu relevant ignorat','F1D':'candidat invalid păstrat','F2A':'certitudine prematură','F2C':'certitudine prematură','F3B':'incertitudine păstrată prea mult','F4A':'candidat valid omis','F4B':'altă eroare','F4C':'certitudine prematură','F5A':'candidat valid omis','F6A':'candidat valid omis','F6B':'contradicție între candidați, indiciu și concluzie','F6C':'indiciu irelevant folosit','F7A':'certitudine prematură','F7B':'incertitudine păstrată prea mult','F8C':'candidat valid omis'},
}
rows=[json.loads(x) for x in IN.read_text(encoding='utf-8').splitlines()]
scored=[]
for r in rows:
    ok=r['id'] in passes[r['model']]
    assert ok or r['id'] in errors[r['model']], (r['model'],r['id'])
    scored.append({**r,'pass':ok,'error_class':None if ok else errors[r['model']][r['id']]})
OUT.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in scored),encoding='utf-8')

models=list(passes)
categories=['ambiguu','rezolvat','indiciu_irelevant','eliminare_multipla']
lines=['# Raport pre-training — Lecția 08','',
'Rubrică: verdictul trebuie să fie semantic corect și să nu contrazică indiciul. Repetarea enunțului fără verdict nu primește punct.','',
'## Scoruri','',
'| Model | Ambiguu /8 | Rezolvat /8 | Indiciu irelevant /8 | Eliminare multiplă /8 | Total /32 |','|---|---:|---:|---:|---:|---:|']
for model in models:
    mr=[x for x in scored if x['model']==model]
    vals=[sum(x['pass'] for x in mr if x['category']==cat) for cat in categories]
    lines.append(f"| {model} | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | {sum(vals)} |")

lines += ['','## Toate răspunsurile greșite','']
for model in models:
    lines += [f'### {model}','']
    for x in scored:
        if x['model']==model and not x['pass']:
            answer=x['answer'].replace('\n','  \n')
            lines += [f"#### {x['id']} — {x['error_class']}",'',f"**Prompt:** {x['prompt']}",'',f"**Răspuns brut:** {answer}",'',f"**Gold:**  \n{x['reference'].replace(chr(10),'  '+chr(10))}",'']

lines += ['## Analiza familiilor contrastive','']
for model in models:
    mr={x['id']:x for x in scored if x['model']==model}
    a_ok_b_bad=[f'F{i}' for i in range(1,9) if mr[f'F{i}A']['pass'] and not mr[f'F{i}B']['pass']]
    b_ok_a_bad=[f'F{i}' for i in range(1,9) if mr[f'F{i}B']['pass'] and not mr[f'F{i}A']['pass']]
    irrelevant=[f'F{i}C' for i in range(1,9) if not mr[f'F{i}C']['pass'] and mr[f'F{i}C']['error_class']=='indiciu irelevant folosit']
    lines += [f'### {model}','',f"- Ambiguul reușește, versiunea rezolvată eșuează: {', '.join(a_ok_b_bad) or 'niciuna'}.",f"- Rezolvatul reușește, dar versiunea ambiguă inventează certitudine: {', '.join(b_ok_a_bad) or 'niciuna'}.",f"- Influențat explicit de indiciul irelevant: {', '.join(irrelevant) or 'niciuna'}.",'']

lines += ['## Probe și exemple pentru revizuire umană','',
'- **Benchmark F2B:** prezența Sandei la ghișeu „în timpul chemării” nu exclude fără echivoc că ea este persoana chemată; poate fi chemată verbal și să rămână acolo. Gold-ul poate fi prea sigur.',
'- **Benchmark F4B:** afirmația că Nicu nu a avut niciodată stilou face lectura posesivă foarte improbabilă, dar momentul primirii poate constitui chiar prima posesie. Gold-ul depinde de interpretarea temporală.',
'- **Benchmark F5B:** faptul că echipa Centru nu a urcat pe scenă nu exclude strict deschiderea ceremoniei din alt loc. Gold-ul folosește o presupunere despre desfășurarea ceremoniei.',
'- **Gold G21B și G22B:** acordul din propoziția următoare rezolvă cazul numai dacă presupunem că subiectul continuă să fie același. Legătura discursivă ar putea fi făcută mai explicită.',
'- **Gold G25A–C:** posesivul din „raftul ei” admite două lecturi, dar unii vorbitori pot prefera puternic referentul feminin apropiat. Preferința nu este dovadă, conform obiectivului lecției.',
'- **Gold G05B:** absența echipamentului la paznic elimină camera numai dacă „cu camera” exprimă posesia/folosirea echipamentului în acel moment; aceasta este lectura urmărită, dar merită validare nativă.','']
REPORT.write_text('\n'.join(lines),encoding='utf-8')
for model in models:
    mr=[x for x in scored if x['model']==model]
    print(model, sum(x['pass'] for x in mr), {c:sum(x['pass'] for x in mr if x['category']==c) for c in categories}, Counter(x['error_class'] for x in mr if not x['pass']))
