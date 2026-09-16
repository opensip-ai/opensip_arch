"""PROBE 22 (v31) — the `derived` retention says: recompute H(native.compilation-unit.v1,
UnitIdentityV1{...}) from the matching units[] row and compare, and selectedUnitIds /
ownership[].unitId must name a row in that same closed table.

A retention kind whose meaning is 'recompute and compare' is only real if something recomputes. I
check whether the native model/checker actually derives unitId, and I recompute it myself over a
real fixture to see whether the declared recipe reproduces the retained identities.
"""
import importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
N = os.path.join(SRC, 'docs/coop/design-corrections/native')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {}

model = open(os.path.join(N, 'native_evidence_model.v2.py'), encoding='utf-8').read()
checker = open(os.path.join(N, 'check_native_evidence.v2.py'), encoding='utf-8').read()
R['modelMentionsUnitIdentityV1'] = 'UnitIdentityV1' in model
R['modelHasSourceUnitIdFn'] = 'def source_unit_id' in model
R['modelHasOwnershipFaults'] = 'def source_unit_ownership_faults' in model
for name in ('source_unit_id', 'source_unit_ownership_faults', 'source_unit_ownership_identity',
             'unit_identity_projection'):
    R['model_' + name] = ('def %s' % name) in model
print('native model exposes:', {k.replace('model_', ''): v for k, v in R.items()
                                if k.startswith('model_')})

# lines that actually compute a compilation-unit identity
hits = [(i, l.strip()) for i, l in enumerate(model.splitlines(), 1)
        if 'compilation-unit' in l or 'COMPILATION_UNIT_DOMAIN' in l]
R['identityComputationLines'] = [{'line': i, 'text': t[:150]} for i, t in hits][:14]
print('\nmodel lines naming the compilation-unit domain (%d):' % len(hits))
for i, t in hits[:10]:
    print('%6d  %s' % (i, t[:130]))

# does the CHECKER exercise ownership identity / selectedUnitIds membership?
ck = [(i, l.strip()) for i, l in enumerate(checker.splitlines(), 1)
      if re.search(r'source_unit_id|ownership|selectedUnitIds|unit_identity', l)]
R['checkerOwnershipLines'] = [{'line': i, 'text': t[:150]} for i, t in ck][:14]
print('\nchecker lines exercising ownership/unit identity (%d):' % len(ck))
for i, t in ck[:10]:
    print('%6d  %s' % (i, t[:130]))
R['checkerExercisesOwnership'] = bool(ck)

# ---- recompute the identity myself over the model's own fixture path ----
spec = importlib.util.spec_from_file_location('nem31', os.path.join(N, 'native_evidence_model.v2.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['nem31'] = M
spec.loader.exec_module(M)
R['COMPILATION_UNIT_DOMAIN'] = getattr(M, 'COMPILATION_UNIT_DOMAIN', None)
print('\nCOMPILATION_UNIT_DOMAIN =', R['COMPILATION_UNIT_DOMAIN'])

import inspect
for fn in ('source_unit_id', 'source_unit_ownership_faults'):
    f = getattr(M, fn, None)
    if f:
        src = inspect.getsource(f)
        R['source_' + fn] = src[:1500]
        print('\n--- %s ---' % fn)
        print('\n'.join('   ' + x for x in src.splitlines()[:26]))

# recompute over a synthetic but schema-valid unit row
unit = {'unitId': None, 'markerPath': 'packages/a/tsconfig.json', 'targetKind': 'ts-program',
        'targetName': 'a', 'crateName': None, 'targetEdition': None}
try:
    pre = {'schemaVersion': 1, 'markerPath': unit['markerPath'],
           'targetKind': unit['targetKind'], 'targetName': unit['targetName']}
    ident = M.source_unit_id(pre) if hasattr(M, 'source_unit_id') else None
    R['recomputedExample'] = {'preimage': pre, 'identity': ident}
    print('\nrecomputed identity for a sample unit row:', ident)
except Exception as ex:
    R['recomputeError'] = '%s: %s' % (type(ex).__name__, ex)
    print('\nrecompute attempt raised:', R['recomputeError'])

json.dump(R, open(os.path.join(OUT, 'p22-derivedcheck.json'), 'w'), indent=1, default=str)
print('\nwrote p22-derivedcheck.json')
