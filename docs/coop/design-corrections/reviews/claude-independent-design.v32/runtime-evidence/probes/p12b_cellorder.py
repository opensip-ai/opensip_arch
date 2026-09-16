"""P12b — decisive test for P12: is the declared cells {by:[...]} order actually ENFORCED, so that
the repair module's enumerate()-derived cellOrdinal equals the normative ordinal?"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
sys.path.insert(0, F)
spec = importlib.util.spec_from_file_location('canon32', os.path.join(F, 'canonical.py'))
C = importlib.util.module_from_spec(spec)
sys.modules['canon32'] = C
spec.loader.exec_module(C)
sch = json.load(open(os.path.join(F, 'enumeration-plan.schema.v1.json')))
R = {}

R['validatorEnforcesOrderKeyword'] = 'x-opensip-order' in open(
    os.path.join(F, 'canonical.py'), encoding='utf-8').read()
print('canonical.py implements x-opensip-order:', R['validatorEnforcesOrderKeyword'])


def cell(cap, mode='ts', root=''):
    return {'capabilityId': cap, 'languageMode': mode, 'workspaceRoot': root, 'required': True,
            'kinds': ['file'],
            'programBindings': [{'ordinal': 0, 'provenance': 'default-unit', 'programEntry': None,
                                 'universe': 'u' * 64, 'nativeContextDigest': 'c' * 64,
                                 'enumerator': {'status': 'selected', 'closureId': 'closure2:' + 'd' * 64},
                                 'extents': [{'kind': 'file', 'paths': ['src/a.ts']}]}]}


def plan(cells):
    return {'schemaVersion': 1, 'snapshotId': 'snapshot2:' + 'e' * 64,
            'scopeDigest': 'f' * 64, 'membershipDigest': '0' * 64, 'cells': cells}


ordered = plan([cell('alpha'), cell('beta')])
shuffled = plan([cell('beta'), cell('alpha')])
for label, inst in (('cells in declared order', ordered), ('cells SHUFFLED', shuffled)):
    try:
        C.validate(sch, inst)
        verdict, reason = 'ADMIT', ''
    except Exception as ex:
        verdict, reason = 'REFUSE', str(ex).splitlines()[0][:150]
    R[label] = {'verdict': verdict, 'reason': reason}
    print('%-28s -> %-7s %s' % (label, verdict, reason[:120]))

R['orderIsEnforced'] = (R['cells in declared order']['verdict'] == 'ADMIT'
                        and R['cells SHUFFLED']['verdict'] == 'REFUSE')
R['CONCLUSION'] = (
    'The cells {by:[capabilityId,languageMode,workspaceRoot]} order IS enforced by the '
    'canonical ExactValidator, which enumeration-contract section 8 names as the plan validator '
    '("4 MiB / typed / order"). identity-model.ordered() has no named `cells` branch, but it does '
    'not need one: the schema validator decides this array. So the repair module\'s '
    'enumerate()-derived cellOrdinal equals the normative 0-based index after the published sort, '
    'and the diagnostic coordinate it prints is correct.'
    if R['orderIsEnforced'] else
    'The declared cells order was NOT refused when shuffled by this validator call, so the '
    'enumerate()-derived cellOrdinal is not guaranteed to equal the normative ordinal. Ownership is '
    'per-binding and unaffected; the exposure is diagnostic-coordinate accuracy in the remedy text.')
print('\norder enforced:', R['orderIsEnforced'])
print(R['CONCLUSION'])
json.dump(R, open(os.path.join(OUT, 'p12b-cellorder.json'), 'w'), indent=1, default=str)
print('\nwrote p12b-cellorder.json')
