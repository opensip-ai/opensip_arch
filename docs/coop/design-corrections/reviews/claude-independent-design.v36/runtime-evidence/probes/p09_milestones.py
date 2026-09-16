"""P09 — milestone labels of the (35->36 byte-unchanged) implementation-coverage owner, recorded rather than copied from history."""
import hashlib, json, os

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v36/receipts'
rel = 'docs/v2/architecture/implementation-coverage.v1.json'
cov = json.load(open(os.path.join(S36, rel)))
mo = cov.get('milestoneOrder')
labels = [m if isinstance(m, str) else (m.get('id') or m.get('milestone') or m.get('name')) for m in mo]
R = {'owner': rel, 'sha256': hashlib.sha256(open(os.path.join(S36, rel), 'rb').read()).hexdigest(), 'milestoneOrder': mo, 'labels': labels,
     'isM0toM6': labels == ['M%d' % i for i in range(7)]}
print(json.dumps(R, indent=1, default=str)[:1500])
json.dump(R, open(os.path.join(OUT, 'p09-milestones.json'), 'w'), indent=1, default=str)
print('wrote p09-milestones.json')
