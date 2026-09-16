"""A11 retry. The first probe_owner_laws attempt used afterStep='analyze' and was refused at /afterStep (StepId is an
integer); that failed attempt is preserved in receipts/probe-owner-laws.<tree>.json. This retry changes only afterStep.

usage: python -I -B probe_a11_retry.py TREE
"""
import hashlib, json, os, sys

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1'
TREE = sys.argv[1]
ROOT = {'source37': '/tmp/opensip-design-corrections/candidate-subject.v37',
        'source38': '/tmp/opensip-design-corrections/candidate-subject.v38'}[TREE]
DC = ROOT + '/docs/coop/design-corrections'
sys.path.insert(0, DC + '/foundation')
import canonical  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

loaded = {}
docs = {}
for d in (DC + '/workflows/schemas', DC + '/workflows/schemas/evaluator3'):
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'):
            p = os.path.join(d, f)
            loaded[os.path.relpath(p, ROOT)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            doc = json.load(open(p))
            if '$id' in doc:
                docs[doc['$id']] = doc
REG = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in docs.items()])


def validate(ref, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': ref}, registry=REG).validate(value)
        return {'result': 'ADMIT'}
    except Exception as exc:
        return {'result': 'REFUSE', 'message': str(exc).splitlines()[0][:220], 'validator': getattr(exc, 'validator', None),
                'path': list(getattr(exc, 'absolute_path', []) or [])}


te = 'urn:opensip:product-v1:workflows:test-execution#/$defs/TestExecutionStepParams'
common = docs['urn:opensip:product-v1:workflows:common']['$defs']
base = {'kind': 'test-execution', 'argv': ['bin/test'], 'argv0Source': {'kind': 'snapshot-member', 'path': 'bin/test'}, 'cwdIsRoot': True,
        'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': 'linux-x86_64-gnu',
        'authorizationRef': 'security.repo-execution-grant.v2:' + 'a' * 64, 'consentSource': 'pre-existing-policy', 'afterStep': 0,
        'timeoutMilliseconds': 1000, 'maxOutputBytes': 1024, 'environmentAllowlist': [],
        'effects': {'network': 'DISCLOSURE-ONLY', 'subprocess': 'DISCLOSURE-ONLY', 'filesystemWrite': 'DISCLOSURE-ONLY', 'environment': 'ENFORCED-BY-CONSTRUCTION'}}
res = {'tree': TREE, 'stepIdSchema': common.get('StepId'), 'baseParams': validate(te, base),
       'platformPrimitiveEffect': validate(te, dict(base, effects=dict(base['effects'], network='ENFORCED-PLATFORM:seatbelt'))),
       'enforcementValueSchema': docs['urn:opensip:product-v1:workflows:test-execution']['$defs']['EnforcementValue'],
       'loadedFileSha256': loaded}
json.dump(res, open(RT + '/receipts/probe-a11-retry.' + TREE + '.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'loadedFileSha256'}, indent=1))
