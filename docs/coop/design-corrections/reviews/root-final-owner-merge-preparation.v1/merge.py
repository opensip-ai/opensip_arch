"""Apply only explicitly reviewed completed-author deltas to the mutable successor.

The selected policy rows must bind exact before/after hashes. Repair rows come from
the independently tested stage. All guards and three-way merges finish before any
source write; conflicting merges leave only new evidence for manual review.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--policy-source', type=Path, required=True)
p.add_argument('--policy-reviewed', type=Path, required=True)
p.add_argument('--repair-stage', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert not a.out.exists()
a.out.mkdir(parents=True)
policy = json.loads(a.policy_reviewed.read_bytes())
assert policy['completedActualClaude'] is True and policy['rootReviewed'] is True
rows = policy['files']
assert len({r['path'] for r in rows}) == len(rows)
pending = {}
before = {}
provenance = {}
for r in rows:
    rel = r['path']
    assert rel.startswith('docs/') and '..' not in Path(rel).parts and '/reviews/' not in rel
    f = a.source / rel
    old = f.read_bytes() if f.exists() else None
    assert (sha(old) if old is not None else None) == r['beforeSha256'], rel
    new = (a.policy_source / rel).read_bytes()
    assert sha(new) == r['sha256'], rel
    before[rel], pending[rel] = old, new
    provenance[rel] = ['reviewed-policy-author']

repair = json.loads((a.repair_stage / 'integration.json').read_bytes())
for r in repair['files']:
    rel = r['path']
    original = (a.source / rel).read_bytes()
    assert sha(original) == r['beforeSha256'], rel
    edited = (a.repair_stage / 'source' / rel).read_bytes()
    assert sha(edited) == r['sha256'], rel
    current = pending.get(rel, original)
    before.setdefault(rel, original)
    if current == original:
        merged = edited
    else:
        d = a.out / 'merge-inputs' / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        paths = [Path(str(d) + suffix) for suffix in ('.current', '.base', '.repair')]
        for q, raw in zip(paths, (current, original, edited)):
            q.write_bytes(raw)
        result = subprocess.run(['git', 'merge-file', '-p', *map(str, paths)], capture_output=True)
        Path(str(d) + '.stdout').write_bytes(result.stdout)
        Path(str(d) + '.stderr').write_bytes(result.stderr)
        assert result.returncode == 0, 'Resolve retained merge conflict before writing source: ' + rel
        merged = result.stdout
    pending[rel] = merged
    provenance.setdefault(rel, []).append('root-tested-repair-stage')

report = []
for rel, new in pending.items():
    f = a.source / rel
    old = before[rel]
    assert (f.read_bytes() if f.exists() else None) == old, 'Concurrent source change: ' + rel
    if old is not None:
        q = a.out / 'before' / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(old)
    report.append({'path': rel, 'beforeSha256': sha(old) if old is not None else None,
                   'sha256': sha(new), 'bytes': len(new), 'provenance': provenance[rel]})
(a.out / 'prepared.json').write_text(json.dumps({'files': report}, indent=2) + '\n')
for rel, new in pending.items():
    f = a.source / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(new)
for r in report:
    assert sha((a.source / r['path']).read_bytes()) == r['sha256']
(a.out / 'integration.json').write_text(json.dumps({
    'standing': 'Reviewed author deltas merged into mutable successor; combined checks, frozen independent review and readiness pending.',
    'files': report}, indent=2) + '\n')
print('Integrated', len(report), 'reviewed paths; combined validation required')
