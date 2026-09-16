"""Claude XA-02 / CR-25 correction applier. Applies a staged replacement set to a SEPARATE copy only.

Every replacement must match exactly once. Emits before/after hashes and a unified patch per file.
"""
import argparse, hashlib, json, difflib
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--copy', type=Path, required=True)
p.add_argument('--stage', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
stage = json.loads(a.stage.read_text())
rows = []
for rel, reps in stage.items():
    f = a.copy / rel
    original = f.read_text()
    updated = original
    for before, after in reps:
        n = updated.count(before)
        if n != 1:
            raise SystemExit('AMBIGUOUS-OR-MISSING %s :: %r :: count=%d' % (rel, before[:80], n))
        updated = updated.replace(before, after)
    f.chmod(f.stat().st_mode | 0o200)
    f.write_text(updated)
    patch = ''.join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True),
                                         fromfile=rel, tofile=rel))
    (a.out / (f.name + '.patch')).write_text(patch)
    rows.append({'path': rel,
                 'beforeSha256': hashlib.sha256(original.encode()).hexdigest(),
                 'afterSha256': hashlib.sha256(updated.encode()).hexdigest(),
                 'beforeBytes': len(original.encode()), 'afterBytes': len(updated.encode()),
                 'replacements': len(reps)})
    print('OK %-72s %s -> %s' % (rel, rows[-1]['beforeSha256'][:12], rows[-1]['afterSha256'][:12]))
(a.out / 'changed-source.json').write_text(json.dumps(
    {'standing': 'CLAUDE AUTHORED CORRECTION; no accepted source changed; fresh independent review required',
     'files': rows}, indent=2) + '\n')
