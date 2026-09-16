"""P14: validate the consumer's demonstrated MutationReplayScopeV1 preimage against the
frozen evaluator3 schema, and recompute what the key would be over an admissible record."""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
WF = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows')
sys.path.insert(0, os.path.join(ROOT32, 'docs/coop/design-corrections/foundation'))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

SCHEMAS = {}
for p in sorted(glob.glob(os.path.join(WF, 'schemas', '*.schema.json'))
                + glob.glob(os.path.join(WF, 'schemas', 'evaluator3', '*.schema.json'))):
    s = canonical.parse(open(p, 'rb').read())
    SCHEMAS[s['$id']] = s
FOUNDATION = canonical.parse(open(os.path.join(ROOT32, 'docs/coop/design-corrections/foundation/identity-schemas.v2.json'), 'rb').read())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUNDATION['$id'], Resource(contents=FOUNDATION, specification=DRAFT202012))])
print('schemas loaded:', len(SCHEMAS))


def valid(ref, value):
    sid, _, frag = ref.partition('#')
    v = canonical.ExactValidator({'$ref': sid + '#' + frag} if frag else {'$ref': sid}, registry=REG)
    try:
        canonical.typed(value)
        v.validate(value)
        return True, ''
    except (ValidationError, canonical.AdmissionError) as e:
        return False, str(e).splitlines()[0][:220]


mk = json.load(open('/tmp/opensip-design-corrections/consumer-b.v19/output/vectors/mutation-keys.json'))
pre = mk['genericMutation']['preimage']
out = {'consumerPreimage': pre, 'declaredKey': mk['genericMutation']['key']}

for urn in ('urn:opensip:product-v1:workflows:evaluator3:invocation-record:3',
            'urn:opensip:product-v1:workflows:invocation-record'):
    ref = urn + '#/$defs/MutationReplayScopeV1'
    if urn not in SCHEMAS:
        print('schema id not loaded:', urn)
        continue
    ok, why = valid(ref, pre)
    print('\n=== %s' % ref)
    print('  consumer preimage valid:', ok, '|', why)
    out.setdefault('validation', {})[urn] = {'valid': ok, 'detail': why}
    fixed = dict(pre, requestId='req1_' + 'ab' * 16, stepId=2)
    ok2, why2 = valid(ref, fixed)
    print('  same record with req1_<32hex> + integer stepId valid:', ok2, '|', why2)
    out.setdefault('validationFixed', {})[urn] = {'valid': ok2, 'detail': why2, 'record': fixed}

print('\n=== published id vocabulary the preimage must meet')
common = SCHEMAS.get('urn:opensip:product-v1:workflows:evaluator3:common:3') or {}
for k in ('RequestId', 'StepId'):
    d = (common.get('$defs') or {}).get(k)
    print('  %-10s %s' % (k, json.dumps({kk: vv for kk, vv in (d or {}).items() if kk != 'description'})))
    out.setdefault('idVocabulary', {})[k] = {kk: vv for kk, vv in (d or {}).items() if kk != 'description'}

json.dump(out, open(os.path.join(HERE, 'p14-mutation-validate.json'), 'w'), indent=2, default=str)
print('\nWROTE p14-mutation-validate.json')
