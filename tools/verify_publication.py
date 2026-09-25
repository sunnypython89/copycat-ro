"""Offline integrity and annotation checks; no model or ML dependencies."""
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((ROOT/'docs/PUBLICATION_MANIFEST.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        path = ROOT/entry['path']
        if digest(path) != entry['sha256']:
            raise SystemExit(f'Publication hash mismatch: {entry["path"]}')
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        if path.suffix == '.jsonl':
            for line in path.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    json.loads(line)
    expected_files = {e['path'] for e in manifest['files']} | {'docs/PUBLICATION_MANIFEST.json'}
    tracked_candidates = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
                          and '.git' not in p.parts and '__pycache__' not in p.parts}
    if tracked_candidates != expected_files:
        raise SystemExit(f'Unexpected or missing publication paths: {sorted(tracked_candidates ^ expected_files)}')
    benchmarks = 0
    for line in (ROOT/'benchmarks/HASHES.sha256').read_text().splitlines():
        expected, name = line.split()
        if digest(ROOT/'benchmarks'/name) != expected:
            raise SystemExit(f'Benchmark hash mismatch: {name}')
        benchmarks += 1
    metadata = json.loads((ROOT/'docs/EXPERIMENT_METADATA.json').read_text(encoding='utf-8'))
    for checkpoint, record in metadata.items():
        training = record['training']
        sources = training.get('sources', [{'name':training.get('dataset'),'count':training.get('num_examples')}])
        for source in sources:
            path = ROOT/'gold'/source['name']
            if len([x for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]) != source['count']:
                raise SystemExit(f'Training count mismatch: {checkpoint}/{path.name}')
            if source.get('sha256') and digest(path) != source['sha256']:
                raise SystemExit(f'Training hash mismatch: {checkpoint}/{path.name}')
    scored = ROOT/'results/evaluate_copycat_10_epoch1_scored.jsonl'
    raw = ROOT/'results/evaluate_copycat_10_epoch1_results.jsonl'
    rows = [json.loads(x) for x in scored.read_text(encoding='utf-8').splitlines()]
    originals = {(x['benchmark'], x['id']):x for x in map(json.loads, raw.read_text(encoding='utf-8').splitlines())}
    scores = defaultdict(lambda:[0,0])
    for row in rows:
        source = originals[(row['benchmark'],row['id'])]
        if row['answer'] != source['answer'] or row['prompt'] != source['prompt']:
            raise SystemExit('Scored/raw content mismatch')
        scores[row['benchmark']][0] += row['pass'] is True
        scores[row['benchmark']][1] += 1
    expected = {'editare_36':[36,36],'lectia_05':[9,16],'lectia_06':[12,24],
                'lectia_07':[17,24],'lectia_08':[19,32],'lectia_09':[20,32],'lectia_10':[22,32]}
    if dict(scores) != expected:
        raise SystemExit('Saved Copycat 10 annotation totals differ from the report.')
    if sum(x['pass'] and x.get('route_pass') is True for x in rows if x['benchmark']=='lectia_10') != 21:
        raise SystemExit('Saved trace total differs from report.')
    print(json.dumps({'verified_files':len(manifest['files']),'frozen_benchmarks':benchmarks,
                      'checkpoint_metadata':len(metadata),'copycat10_recorded_scores':dict(scores),
                      'meaning':'Integrity and historical annotation replay only; no new performance measurement.'}, indent=2))


if __name__ == '__main__':
    main()
