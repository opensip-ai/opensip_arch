"""S03 — what do my ALREADY-MEASURED receipts say about the composition-contract change, and is
frozen32 available for a bounded section-level confirmation? No new suites either way."""
import json, os

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
R = {}

print('=== sibling runtimes present ===')
sib = sorted(d for d in os.listdir('/tmp/opensip-design-corrections') if d.startswith('candidate-subject'))
R['candidateSubjectDirs'] = sib
print(sib)

for n in ('p02-execlaw.json', 'p06-fallback-planning.json'):
    p = os.path.join(V33, 'receipts', n)
    if not os.path.isfile(p):
        continue
    d = json.load(open(p))
    print('\n===== %s  keys: %s' % (n, list(d)[:20]))
    blob = json.dumps(d, default=str, indent=1)
    keep = []
    for i, line in enumerate(blob.splitlines()):
        if 'composition' in line.lower() or '9.6' in line or 'fallback' in line.lower():
            keep.append(line.strip()[:300])
    R['receipt_' + n] = keep
    for k in keep[:28]:
        print('   ', k)
json.dump(R, open(os.path.join(OUT, 's03-compositiondelta.json'), 'w'), indent=1, default=str)
print('\nwrote s03-compositiondelta.json')
