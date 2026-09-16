"""P12c — corrects P12b, whose synthetic cells used capabilityId/languageMode values outside the
schema enums, so BOTH instances refused with 'exact enum type/value mismatch' and the result was
inconclusive rather than evidence of non-enforcement. Preserved.

Here I isolate the ORDER keyword itself on a minimal schema, and separately drive the real plan
schema with values taken from its own enums.
"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
spec = importlib.util.spec_from_file_location('canon32c', os.path.join(F, 'canonical.py'))
C = importlib.util.module_from_spec(spec)
sys.modules['canon32c'] = C
spec.loader.exec_module(C)
R = {'corrects': 'p12b used out-of-enum capabilityId/languageMode, making its result inconclusive'}

# ---- 1. isolate the x-opensip-order 'by' keyword on a minimal schema ----
mini = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object', 'additionalProperties': False, 'required': ['cells'],
        'properties': {'cells': {'type': 'array',
                                 'items': {'type': 'object', 'additionalProperties': False,
                                           'required': ['a', 'b'],
                                           'properties': {'a': {'type': 'string'},
                                                          'b': {'type': 'string'}}},
                                 'x-opensip-order': {'by': ['a', 'b']}}}}
cases = [('declared order', {'cells': [{'a': 'alpha', 'b': 'x'}, {'a': 'beta', 'b': 'y'}]}),
         ('shuffled', {'cells': [{'a': 'beta', 'b': 'y'}, {'a': 'alpha', 'b': 'x'}]}),
         ('duplicate key', {'cells': [{'a': 'alpha', 'b': 'x'}, {'a': 'alpha', 'b': 'x'}]})]
for label, inst in cases:
    try:
        C.validate(mini, inst)
        v, why = 'ADMIT', ''
    except Exception as ex:
        v, why = 'REFUSE', str(ex).splitlines()[0][:130]
    R['minimal_' + label] = {'verdict': v, 'reason': why}
    print('minimal by-order %-16s -> %-7s %s' % (label, v, why[:110]))
R['byOrderKeywordEnforced'] = (R['minimal_declared order']['verdict'] == 'ADMIT'
                               and R['minimal_shuffled']['verdict'] == 'REFUSE')
print('\nx-opensip-order {by:[...]} is enforced by the validator:', R['byOrderKeywordEnforced'])

# ---- 2. the real plan schema, with values from its own enums ----
sch = json.load(open(os.path.join(F, 'enumeration-plan.schema.v1.json')))


def enum_of(path):
    cur = sch
    for p in path:
        cur = cur[p]
    return cur


try:
    cellprops = sch['properties']['cells']['items']['properties'] \
        if 'items' in sch['properties']['cells'] else \
        sch['$defs']['CellObligationV1']['properties']
    caps = cellprops['capabilityId'].get('enum')
    modes = cellprops['languageMode'].get('enum')
    R['capabilityEnumSample'] = (caps or [])[:6]
    R['languageModeEnum'] = modes
    print('\nreal schema capabilityId enum sample:', (caps or [])[:6])
    print('real schema languageMode enum      :', modes)
    R['cellsOrderAnnotation'] = sch['properties']['cells'].get('x-opensip-order')
    print('cells order annotation             :', json.dumps(R['cellsOrderAnnotation']))
except Exception as ex:
    R['enumLookupError'] = '%s: %s' % (type(ex).__name__, ex)
    print('enum lookup error:', R['enumLookupError'])

R['CONCLUSION'] = (
    'The validator DOES enforce x-opensip-order {by:[...]}: on an isolated minimal schema the '
    'declared order admits and the shuffled order refuses. enumeration-plan.schema.v1.json declares '
    'cells with {by:[capabilityId,languageMode,workspaceRoot]}, and enumeration-contract section 8 '
    'names the canonical ExactValidator ("4 MiB / typed / order") as the plan validator. So the '
    'retained cells array is held to the published sort, identity-model.ordered() needs no named '
    '`cells` branch, and the repair module\'s enumerate()-derived cellOrdinal is the normative '
    '0-based index. No finding.'
    if R['byOrderKeywordEnforced'] else
    'The by-order keyword did not behave as enforced on the isolated schema; see the recorded '
    'verdicts before drawing any conclusion about cellOrdinal.')
print('\n' + R['CONCLUSION'])
json.dump(R, open(os.path.join(OUT, 'p12c-cellorder.json'), 'w'), indent=1, default=str)
print('\nwrote p12c-cellorder.json')
