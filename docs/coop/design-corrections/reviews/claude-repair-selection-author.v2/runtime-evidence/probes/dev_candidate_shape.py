"""Find the exact admissible shape of a candidate-only cell binding."""
import importlib.util, json, sys
from pathlib import Path

FOUND = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source/docs/coop/design-corrections/foundation')
sys.path.insert(0, str(FOUND))
import canonical as C  # noqa: E402

schema = json.load(open(FOUND / 'enumeration-plan.schema.v1.json'))


def attempt(label, binding, kinds=None):
    ep = {'schemaVersion': 1, 'snapshotId': 'snapshot2:' + '0' * 64,
          'scopeDigest': '0' * 64, 'membershipDigest': '0' * 64,
          'cells': [{'capabilityId': 'clones-near', 'languageMode': 'ts-tsconfig',
                     'workspaceRoot': '.', 'required': True,
                     'kinds': [] if kinds is None else kinds,
                     'programBindings': [binding]}]}
    try:
        C.typed(ep)
        C.ExactValidator(schema).validate(ep)
        print('VALID  ', label)
        return True
    except Exception as exc:
        print('INVALID', label, '|', str(exc).splitlines()[0][:200])
        return False


base = {'ordinal': 0, 'provenance': 'explicit-plan-selection',
        'enumerator': {'status': 'selected', 'closureId': 'closure2:' + 'a' * 64},
        'nativeContextDigest': 'b' * 64, 'universe': 'c' * 64,
        'programEntry': 'tsconfig.build.json', 'extents': [],
        'candidateSourcePaths': ['src/b.ts']}

attempt('explicit entry + candidateSourcePaths', dict(base))
attempt('programEntry None', dict(base, programEntry=None, provenance='default-unit'))
attempt('no candidateSourcePaths', {k: v for k, v in base.items() if k != 'candidateSourcePaths'})
attempt('kinds=["symbol"]', dict(base), kinds=['symbol'])

print()
print('ProgramBindingV1:', json.dumps(schema['$defs']['ProgramBindingV1'])[:800])
print()
print('AvailableProgramBindingV1 required:', schema['$defs']['AvailableProgramBindingV1'].get('required'))
print('AvailableProgramBindingV1 props:', sorted(schema['$defs']['AvailableProgramBindingV1'].get('properties', {})))
print()
cell = schema['$defs']['CellObligationV1']
print('CellObligationV1 required:', cell.get('required'))
print('CellObligationV1 allOf:', json.dumps(cell.get('allOf'))[:1200])
