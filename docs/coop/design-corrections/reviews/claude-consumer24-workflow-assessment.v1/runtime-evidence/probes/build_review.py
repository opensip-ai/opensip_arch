"""Assemble review.json from the authored assessment plus this runtime's receipts (exact hashes and probe results)."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1'
R = RT + '/receipts'


def load(name):
    return json.load(open(R + '/' + name))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


review = json.load(open(RT + '/review.authored.json'))
review['inputVerification'] = {'initial': load('verify-inputs.initial.json'), 'final': load('verify-inputs.final.json')}
review['readHashes'] = load('read-hashes.json')
review['probeResults'] = {t: load('probe-owner-laws.' + t + '.json') for t in ('source37', 'source38')}
review['probeA11Retry'] = {t: load('probe-a11-retry.' + t + '.json') for t in ('source37', 'source38')}
same = {}
for sec in review['probeResults']['source38']['sections']:
    a = json.dumps(review['probeResults']['source37']['sections'].get(sec), sort_keys=True)
    b = json.dumps(review['probeResults']['source38']['sections'].get(sec), sort_keys=True)
    same[sec] = a == b
review['probeResultsIdentical37vs38'] = same
review['commands'] = [
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/verify_inputs.py initial', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/probe_owner_laws.py source38', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/probe_owner_laws.py source37', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/probe_a11_retry.py source38', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/probe_a11_retry.py source37', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/collect_hashes.py', 'exitCode': 0},
    {'command': '/tmp/opensip-architecture-review-env/bin/python -I -B probes/verify_inputs.py final', 'exitCode': 0},
]
review['receiptSha256'] = {f: sha(os.path.join(R, f)) for f in sorted(os.listdir(R))}
json.dump(review, open(RT + '/review.json', 'w'), indent=1, default=str)
print(json.dumps({'reviewJsonSha256': sha(RT + '/review.json'), 'identical37vs38': same}, indent=1))
