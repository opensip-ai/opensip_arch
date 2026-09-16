"""Final custody and exact delta for this runtime. Read-only over the application root, repo evidence and frozen39.

usage: python -I -B finalize.py
Writes diffs/app-summary-boundary.diff and receipts/final-custody-and-delta.json in this runtime only.
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-application39-summary-author.v1')
SRC = Path('/tmp/opensip-design-corrections/application-successor-root.v2')
CAP = RT / 'work/application-successor-root.v2'
BEFORE = RT / 'work/before'
REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
DC = 'docs/coop/design-corrections/'
CHANGED = ('apply-advisory-records.successor.v1.py', 'current_reference_summary.py')
EVIDENCE = {
    DC + 'reviews/candidate-subject.v39.json': 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009',
    DC + 'reviews/codex-post-reset.v1/final-reference.v39/reference-checks.json': 'cf31e1315ad63b2a4f20869a67944ac4c6444ecb2a80a6d3d79bf65ee6ba06b1',
    DC + 'reviews/codex-post-reset.v1/final-reference.v39/report.json': '408c3619cfed3bf6240177226240181cc9bab10fb3e0a9b887a10f1d6ca2f836',
    DC + 'reviews/codex-post-reset.v1/final-reference.v39/runner-original-reference-checks.json': '048f979e49debf944d82f51fcc1871286ca59fdb5c8311c92ce8b9749c8d88cc',
    DC + 'reviews/codex-post-reset.v1/identity-check-counts.v39.json': '466a064d826c0e6661168f910d2ae5815d9da49a850babfdefe6c89cb28d9745',
    DC + 'reviews/candidate-subject.v13.json': '8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023',
    DC + 'reviews/candidate-source.v13.tar.gz': '13458c7cebea1d46ec0780b91648159346503dff279e46c19832d31fcfbb0b29',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def walk(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = Path(d) / f
            out[str(p.relative_to(root))] = sha(p)
    return out


capture = json.loads((RT / 'receipts/app-root-capture.json').read_text())
recorded = capture['hashes']
src_now = walk(SRC)
source_drift = sorted(p for p in set(recorded) | set(src_now) if recorded.get(p) != src_now.get(p))
cap_now = walk(CAP)
cap_changed = sorted(p for p in set(recorded) | set(cap_now) if recorded.get(p) != cap_now.get(p))
before_match = {n: sha(BEFORE / n) == recorded[n] for n in CHANGED}
evidence = {p: {'expected': h, 'now': sha(REPO / p), 'ok': sha(REPO / p) == h} for p, h in EVIDENCE.items()}
pycache_new = sorted(p for p in cap_now if p not in recorded and ('__pycache__' in p or p.endswith('.pyc')))
chunks = []
for n in CHANGED:
    chunks.extend(difflib.unified_diff((BEFORE / n).read_text().splitlines(keepends=True), (CAP / n).read_text().splitlines(keepends=True),
                                       fromfile='captured/' + n, tofile='corrected/' + n))
diff = ''.join(chunks)
(RT / 'diffs').mkdir(exist_ok=True)
(RT / 'diffs/app-summary-boundary.diff').write_text(diff)
res = {
    'sourceApplicationRoot': str(SRC), 'sourceFiles': len(src_now), 'sourceDriftSinceCapture': source_drift,
    'captureManifestDigest': capture['manifestDigest'], 'captureFiles': len(cap_now),
    'captureChangedFiles': cap_changed, 'onlyIntendedFilesChanged': cap_changed == sorted(CHANGED),
    'beforeImagesEqualCapture': before_match, 'newPycacheInCapture': pycache_new,
    'delta': [{'path': n, 'beforeSha256': recorded[n], 'afterSha256': cap_now[n]} for n in CHANGED],
    'diff': {'path': 'diffs/app-summary-boundary.diff', 'sha256': hashlib.sha256(diff.encode()).hexdigest(), 'lines': diff.count('\n')},
    'readOnlyEvidence': evidence,
}
res['ok'] = (not source_drift and res['onlyIntendedFilesChanged'] and all(before_match.values()) and not pycache_new
             and all(v['ok'] for v in evidence.values()))
(RT / 'receipts/final-custody-and-delta.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, list) and k not in ('captureChangedFiles', 'delta') else v) for k, v in res.items()}, indent=1))
sys.exit(0 if res['ok'] else 1)
