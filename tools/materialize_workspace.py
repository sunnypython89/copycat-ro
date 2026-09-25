"""Create an isolated flat runtime; never train, infer, or download models."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MISSING = 'benchmark_copycat_03_on_04.py'


def available_training_copy(text):
    """Only remove the unavailable integrity target; preserve training code."""
    tree = ast.parse(text)
    edits = []
    lines = text.splitlines(keepends=True)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = {n.id for n in node.targets if isinstance(n, ast.Name)}
        if 'BENCHMARKS' in names and isinstance(node.value, ast.List):
            kept = [v for v in node.value.elts if MISSING not in ast.unparse(v)]
            if len(kept) != len(node.value.elts):
                node.value.elts = kept
                edits.append((node.lineno - 1, node.end_lineno, ast.unparse(node) + '\n'))
        elif 'EXPECTED' in names and isinstance(node.value, ast.Dict):
            pairs = [(k, v) for k, v in zip(node.value.keys, node.value.values)
                     if not isinstance(k, ast.Constant) or k.value != MISSING]
            if len(pairs) != len(node.value.keys):
                node.value.keys = [k for k, _ in pairs]
                node.value.values = [v for _, v in pairs]
                edits.append((node.lineno - 1, node.end_lineno, ast.unparse(node) + '\n'))
    for start, end, replacement in reversed(edits):
        lines[start:end] = [replacement]
    result = ''.join(lines)
    compile(result, '<available-training-copy>', 'exec')
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('target', type=Path)
    ap.add_argument('--available-benchmarks-only', action='store_true')
    ap.add_argument('--with-results', action='store_true')
    args = ap.parse_args()
    target = args.target.resolve()
    if target.exists():
        raise SystemExit('Refusing an existing target; choose a new isolated directory.')
    if target.is_relative_to(ROOT):
        raise SystemExit('Choose a runtime outside the publication repository.')
    sources = []
    for folder, suffix in [('benchmarks', '.jsonl'), ('gold', '.jsonl'),
                           ('training', '.py'), ('evaluation', '.py')]:
        sources.extend(sorted((ROOT / folder).glob('*' + suffix)))
    sources = [p for p in sources if p.name != 'evaluate_available.py']
    if args.with_results:
        sources.extend(sorted((ROOT / 'results').glob('*.json*')))
    names = [p.name for p in sources]
    if len(names) != len(set(names)):
        raise SystemExit('Conflicting flattened filenames.')
    target.mkdir(parents=True)
    changes = []
    for p in sources:
        out = target / p.name
        shutil.copyfile(p, out)
        if args.available_benchmarks_only and p.parent.name == 'training':
            source = p.read_text(encoding='utf-8')
            updated = available_training_copy(source)
            if updated != source:
                out.write_text(updated, encoding='utf-8', newline='\n')
                changes.append({'path':p.name,
                                'published_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                'runtime_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                                'change':'Removed only missing editing benchmark from BENCHMARKS/EXPECTED'})
    (target / 'RUNTIME_CHANGES.json').write_text(json.dumps(changes, indent=2)+'\n', encoding='utf-8')
    print(f'Prepared {len(sources)} files; {len(changes)} explicit runtime adjustments. No experiment executed.')
    print('Historical aggregate evaluators still require the missing editing source; use evaluate_available.py for semantic-only inference.')


if __name__ == '__main__':
    main()
