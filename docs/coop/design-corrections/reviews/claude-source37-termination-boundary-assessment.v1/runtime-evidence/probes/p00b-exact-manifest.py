"""Exact-path manifest verification for p00's key files.

p00 matched manifest pins by path SUFFIX, which also matched review-subtree copies of the same relative path, so
its manifestAgrees=false rows are a probe matching defect. That failed receipt is retained unchanged. This probe
reports every suffix candidate and decides only on an exact path or a non-review prefix.
"""
import hashlib, json
from pathlib import Path

FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
BASE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1')
P00 = json.loads((BASE / 'probes' / 'p00-disposable-copies.json').read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


pins = []


def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            pins.append((o['path'], o['sha256']))
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


mbytes = MANIFEST.read_bytes()
walk(json.loads(mbytes))
rows = []
for row in P00['keyFiles']:
    rel = row['path']
    candidates = [(p, d) for p, d in pins if p == rel or p.endswith('/' + rel)]
    nonreview = [(p, d) for p, d in candidates if 'reviews' not in p[:len(p) - len(rel)].split('/')]
    digests = sorted({d for _, d in nonreview})
    frozen = sha(FROZEN / rel)
    rows.append({'path': rel, 'suffixCandidates': len(candidates), 'nonReviewCandidates': [p for p, _ in nonreview],
                 'nonReviewDigests': digests, 'frozenSha256': frozen,
                 'exactAgrees': len(digests) == 1 and digests[0] == frozen,
                 'baselineEqual': sha(BASE / 'disposable/baseline' / rel) == frozen,
                 'editedEqual': sha(BASE / 'disposable/edited' / rel) == frozen})
record = {'manifestSha256': hashlib.sha256(mbytes).hexdigest(), 'rows': rows,
          'allExactAgree': all(r['exactAgrees'] for r in rows),
          'allCopiesEqual': all(r['baselineEqual'] and r['editedEqual'] for r in rows)}
(BASE / 'probes' / 'p00b-exact-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if not (record['manifestSha256'] == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
        and record['allExactAgree'] and record['allCopiesEqual']):
    raise SystemExit(1)
