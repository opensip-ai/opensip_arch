"""PROBE 22b (v31) — corrects p22's fixture (I passed targetKind 'ts-program' against the Rust
target-kind enum lib/bin/test/bench/example/build-script; that was my error, not a source defect).

Recompute the `derived` identity from the published recipe and show that the retention kind is
decidable end to end: a correct row derives, a tampered row is named by the owning fault.
"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
N = os.path.join(SRC, 'docs/coop/design-corrections/native')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
spec = importlib.util.spec_from_file_location('nem31b', os.path.join(N, 'native_evidence_model.v2.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['nem31b'] = M
spec.loader.exec_module(M)
R = {'corrects': "p22 used targetKind 'ts-program', which the Rust target-kind enum rejects"}

unit = {'markerPath': 'crates/alpha/Cargo.toml', 'targetKind': 'lib', 'targetName': 'alpha',
        'crateName': 'alpha', 'targetEdition': 2018}
ident = M.source_unit_id(unit)
R['recomputedIdentity'] = ident
R['projection'] = M.unit_identity_projection(unit)
print('projection :', json.dumps(R['projection']))
print('identity   :', ident)
R['identityIsStable'] = M.source_unit_id(dict(unit)) == ident
print('stable across equal rows:', R['identityIsStable'])

# a different targetName must give a different identity (the recipe is injective over its 4 fields)
other = dict(unit, targetName='beta')
R['differentNameDifferentIdentity'] = M.source_unit_id(other) != ident
print('different targetName -> different identity:', R['differentNameDifferentIdentity'])
# markerPath containing '#', which the docstring says an earlier delimiter recipe had to exclude
hashy = dict(unit, markerPath='crates/a#b/Cargo.toml')
R['hashMarkerPathAdmitted'] = True
try:
    R['hashMarkerIdentity'] = M.source_unit_id(hashy)
    print("markerPath containing '#' derives fine:", R['hashMarkerIdentity'][:28])
except Exception as ex:
    R['hashMarkerPathAdmitted'] = False
    R['hashMarkerError'] = str(ex)[:160]
    print("markerPath containing '#' REFUSED:", R['hashMarkerError'])

# end-to-end: the ownership fault names a tampered unitId
ownership = {'units': [dict(unit, unitId=ident)], 'selectedUnitIds': [ident],
             'ownership': [{'path': 'crates/alpha/src/lib.rs', 'unitId': ident}]}
universe = {'edition': {'alpha': 2018}}
inventory = {'crates/alpha/Cargo.toml': 1, 'crates/alpha/src/lib.rs': 1}
clean = M.source_unit_ownership_faults(ownership, universe, inventory)
R['cleanFaults'] = clean
print('\nfaults for a correctly derived record :', clean)

import copy
bad = copy.deepcopy(ownership)
bad['units'][0]['unitId'] = 'sha256:' + '0' * 64 if ident.startswith('sha256:') else '0' * 64
tampered = M.source_unit_ownership_faults(bad, universe, inventory)
R['tamperedFaults'] = tampered
R['tamperNamedByOwningFault'] = any('sourceUnitOwnership.unitId' in f for f in tampered)
print('faults for a tampered unitId          :', tampered)
print('tampering named by the owning fault   :', R['tamperNamedByOwningFault'])

bad2 = copy.deepcopy(ownership)
bad2['selectedUnitIds'] = ['0' * 64]
sel = M.source_unit_ownership_faults(bad2, universe, inventory)
R['selectedNotInTableFaults'] = sel
R['selectedMembershipEnforced'] = any('selectedUnitIds' in f for f in sel)
print('selectedUnitIds outside the table     :', sel)
R['derivedRetentionIsDecidableEndToEnd'] = (not clean and R['tamperNamedByOwningFault']
                                            and R['selectedMembershipEnforced'])
print('\n`derived` retention decidable end to end:', R['derivedRetentionIsDecidableEndToEnd'])
json.dump(R, open(os.path.join(OUT, 'p22b-derivedrecompute.json'), 'w'), indent=1, default=str)
print('wrote p22b-derivedrecompute.json')
