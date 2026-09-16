"""Discovery: reach the retained EnumerationPlan parameter from a full admitted Run."""
import importlib.util, json
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load('dev_replay', FOUND / 'check-replay.v3.py')
F, R, M = P.F, P.R, P.M

g = F.build_file_inputs(multiple_universes=True)
seed, objects, blobs, _ = F.seal_fixture(g)
_, owner = M.open_run_closure(seed, objects, blobs)
i = g['inputs']
res = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
               i['evaluationInputRefs'], objects, blobs, owner)
run, objects, blobs = P.seal(g, res, objects, blobs)
run_id = M.close_run(run, objects, blobs)
print('ADMITTED', run_id)

plan = objects[run['planId']][1]
print('plan keys', sorted(plan.keys()))
spec = json.loads(blobs[plan['analysisSpecDigest']])
print('spec keys', sorted(spec.keys()))
print('parameters', len(spec['parameters']))
for item in spec['parameters']:
    row = M.parameter_row_of(item['schemaDigest'])
    print('  row =', row, '| keys', sorted(item.keys()))

enum_items = [it for it in spec['parameters']
              if M.parameter_row_of(it['schemaDigest']) == 'foundation/enumeration-plan.schema.v1.json']
print('enumeration parameter rows:', len(enum_items))
ep = json.loads(blobs[enum_items[0]['payloadDigest']])
print('\nEnumerationPlanV1 keys', sorted(ep.keys()))
print(json.dumps(ep, indent=1)[:3500])
