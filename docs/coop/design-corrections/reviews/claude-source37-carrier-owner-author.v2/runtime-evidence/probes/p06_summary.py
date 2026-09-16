"""Read-only summary for the v2 report: receipt digests, discrimination counts, matrix counts, drift rows, diff digests.
With argv[1] == 'final', also digests review.md and review.json and re-verifies frozen37 and the retained v1 runtime.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
R = BASE / 'receipts'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


out = {'receipts': {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()}}
out['receiptExits'] = {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}
d = json.loads((R / 'p04b-discrimination.json').read_text())
out['discrimination'] = {k: {'passed': v['passed'], 'failed': v['failed']} for k, v in d.items() if k != 'expectations'}
out['discriminationExpectations'] = d['expectations']
d0 = json.loads((R / 'p04-discrimination.json').read_text())
out['p04FirstRun'] = {'counts': {k: {'passed': v['passed'], 'failed': v['failed']} for k, v in d0.items() if k != 'expectations'},
                      'unmetExpectations': [k for k, v in d0['expectations'].items() if not v],
                      'nonStorageFailuresInHybridV1ddl': [f for f in d0['hybrid-v1ddl']['failures'] if not f.startswith('source37 storage')]}
for tree in ('frozen37', 'v1final', 'edited'):
    m = json.loads((R / ('p01d-storage-matrix.%s.json' % tree)).read_text())
    cats = {}
    for h in m['holes']:
        col, variant = h.split(' ')[0], h.split(' ')[1]
        cats.setdefault(variant, []).append(col)
    out['matrix.' + tree] = {'variants': m['variantCount'], 'holes': m['holeCount'], 'overRefusals': len(m['overRefusals']),
                             'rootCounterexamplesAllRefused': m['rootCounterexamplesAllRefused'], 'utf16FailsClosed': m['utf16FailsClosed'],
                             'holeVariants': {k: len(v) for k, v in sorted(cats.items())}}
for label in ('p03-integrated-carrier.v1final.json', 'p03-integrated-carrier.edited.json', 'p03b-integrated-carrier.edited.final.json'):
    rep = json.loads((R / label).read_text())
    out[label] = {'passed': rep['passed'], 'failed': rep['failed'],
                  'source37': len([c for c in rep['checks'] if c['check'].startswith('source37')]),
                  'storage': len([c for c in rep['checks'] if c['check'].startswith('source37 storage')])}
p5 = json.loads((R / 'p05b-routes-drift-wording.json').read_text())
out['drift'] = [{'path': x['path'], 'changedInV2': x['changedInV2'], 'manifestPinIsFrozen': x['manifestPinIsFrozen'],
                 'normativeInputsV5': x['normativeInputsV5'], 'coverageSources': len(x['coverageSources']), 'pinLedgers': len(x['pinLedgers'])}
                for x in p5['bindingDrift']]
out['diffs'] = {n: sha(BASE / n) for n in ('proposed-edits.diff', 'v1-to-v2.diff')}
p2b = json.loads((R / 'p02b-apply-v2-final.json').read_text())
out['diffsMatchP02b'] = (out['diffs']['proposed-edits.diff'] == p2b['proposedEditsDiff']['sha256']
                         and out['diffs']['v1-to-v2.diff'] == p2b['v1ToV2Diff']['sha256'])
if len(sys.argv) > 1 and sys.argv[1] == 'final':
    out['review'] = {n: sha(BASE / n) for n in ('review.md', 'review.json')}
    json.loads((BASE / 'review.json').read_text())
    p00 = json.loads((R / 'p00-setup.json').read_text())
    FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
    V1RT = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
    out['frozen37Unchanged'] = all(sha(FROZEN / r['path']) == r['frozenSha256'] for r in p00['rows'])
    out['v1RuntimeUnchanged'] = (sha(V1RT / 'review.json') == p00['v1ReviewJsonSha256'] and sha(V1RT / 'review.md') == p00['v1ReviewMdSha256']
                                 and sha(V1RT / 'proposed-edits.diff') == p00['v1ProposedEditsDiffSha256'])
print(json.dumps(out, indent=1))
if not out['diffsMatchP02b']:
    raise SystemExit(1)
