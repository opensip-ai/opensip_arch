"""Read-only summary for the v3 report: receipt digests and exits, matrix and ablation verdicts, validator and discrimination
counts, diff digests. With argv[1] == 'final', also digests review.md/review.json and re-verifies custody.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
R = BASE / 'receipts'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


out = {'receipts': {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()},
       'receiptExits': {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}}
for tree in ('frozen37', 'v2final', 'rootalt', 'edited'):
    p = R / ('p01-encoding-matrix.%s.json' % tree)
    if p.exists():
        m = json.loads(p.read_text())
        out['matrix.' + tree] = m['summary']
ab = json.loads((R / 'p01b-conjunction-ablation.json').read_text())
out['ablation'] = {'exactInAllThreeEncodings': ab['exactInAllThreeEncodings'], 'exactPerEncoding': ab['exactPerEncoding']}
for p in sorted(R.glob('p03-integrated-carrier.*.json')):
    rep = json.loads(p.read_text())
    out[p.name] = {'passed': rep.get('passed'), 'failed': rep.get('failed'),
                   'source37': len([c for c in rep.get('checks', []) if c['check'].startswith('source37')]),
                   'storage': len([c for c in rep.get('checks', []) if c['check'].startswith('source37 storage')])}
d = json.loads((R / 'p04-discrimination.json').read_text())
out['discrimination'] = {k: {'passed': v['passed'], 'failed': v['failed']} for k, v in d.items() if k != 'expectations'}
out['discriminationExpectations'] = d['expectations']
p5first = json.loads((R / 'p05-routes-drift-wording.json').read_text())
out['p05FirstRun'] = {'allOk': p5first['allOk'], 'staleWordingHits': p5first['staleWordingHits']}
p5 = json.loads((R / 'p05b-routes-drift-wording.json').read_text())
out['p05'] = {k: v for k, v in p5.items() if k not in ('routes', 'bindingDrift')}
out['routes'] = p5['routes']
out['bindingDrift'] = p5['bindingDrift']
p2 = json.loads((R / 'p02-apply-v3.json').read_text())
out['files'] = p2['files']
out['diffs'] = {n: sha(BASE / n) for n in ('proposed-edits.diff', 'v2-to-v3.diff')}
out['diffsMatchP02'] = out['diffs']['proposed-edits.diff'] == p2['proposedEditsDiff']['sha256'] and out['diffs']['v2-to-v3.diff'] == p2['v2ToV3Diff']['sha256']
if len(sys.argv) > 1 and sys.argv[1] == 'final':
    json.loads((BASE / 'review.json').read_text())
    out['review'] = {n: sha(BASE / n) for n in ('review.md', 'review.json')}
    p00 = json.loads((R / 'p00-setup.json').read_text())
    FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
    V2RT = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
    ROOTREV = Path('/tmp/opensip-design-corrections/root-carrier-encoding-review.v1')
    out['frozen37Unchanged'] = all(sha(FROZEN / r['path']) == r['frozen37'] for r in p00['rows'])
    out['v2RuntimeUnchanged'] = all(sha(V2RT / n) == h for n, h in p00['v2Review'].items())
    out['rootReviewUnchanged'] = all(sha(ROOTREV / n) == h for n, h in p00['rootCaptured'].items())
print(json.dumps(out, indent=1))
if not out['diffsMatchP02']:
    raise SystemExit(1)
