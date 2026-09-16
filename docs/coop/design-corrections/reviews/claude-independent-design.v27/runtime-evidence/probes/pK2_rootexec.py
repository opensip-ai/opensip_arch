"""PROBE K2 (v27) — EXECUTE the snapshot27 root-representation boundary.

F-04 asked that the sentinel spelling be rejected at admission with a root-specific fault
instead of being misattributed to ENUMERATION_BINDING_PROGRAM_ENTRY (or silently emptying
membership). This runs admit_unit_roots and the enumeration membership join for real.
"""
import importlib.util, inspect, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
F = os.path.join(SRC, 'docs/coop/design-corrections')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
R = {'probeStanding': 'real execution of snapshot27 boundaries; failures preserved verbatim'}


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(F, rel))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


NEM = load('nem27b', 'native/native_evidence_model.v2.py')
ENM = load('enm27b', 'foundation/enumeration_model.v1.py')

print('--- admit_unit_roots source ---')
print(inspect.getsource(NEM.admit_unit_roots))
R['admitUnitRootsSource'] = inspect.getsource(NEM.admit_unit_roots)
print('--- _admit_root_scalar source ---')
print(inspect.getsource(NEM._admit_root_scalar))
R['admitRootScalarSource'] = inspect.getsource(NEM._admit_root_scalar)


def unit(root, members=(), ordinal=0):
    return {'unitOrdinal': ordinal, 'rootPath': root, 'languageFamily': 'tsjs',
            'languageMode': 'ts', 'unitKind': 'ts-program', 'markerPath': 'tsconfig.json',
            'markerSha256': '00' * 32, 'recognizerId': 'ts-tsconfig', 'recognizerVersion': 1,
            'memberPackageRoots': list(members), 'provenance': 'default-unit'}


CASES = [
    ('project root, empty string (lawful)', {'schemaVersion': 1, 'units': [unit('')]}),
    ('SENTINEL rootPath="."', {'schemaVersion': 1, 'units': [unit('.')]}),
    ('rootPath="./"', {'schemaVersion': 1, 'units': [unit('./')]}),
    ('rootPath="packages/a" (lawful)', {'schemaVersion': 1, 'units': [unit('packages/a')]}),
    ('rootPath absolute "/abs"', {'schemaVersion': 1, 'units': [unit('/abs')]}),
    ('rootPath="a/../b"', {'schemaVersion': 1, 'units': [unit('a/../b')]}),
    ('member root "." ', {'schemaVersion': 1, 'units': [unit('', members=['.'])]}),
    ('member root "" (empty, must be NON-EMPTY)', {'schemaVersion': 1, 'units': [unit('', members=[''])]}),
    ('member root "packages/a" (lawful)', {'schemaVersion': 1, 'units': [unit('', members=['packages/a'])]}),
]
rows = []
print('\n--- executed admissions (admit_unit_roots takes the UNIT LIST) ---')
for name, m in CASES:
    try:
        NEM.admit_unit_roots(m['units'])
        v, reason = 'ADMIT', ''
    except Exception as ex:
        v, reason = 'REFUSE', '%s: %s' % (type(ex).__name__, ex)
    rows.append({'case': name, 'verdict': v, 'reason': reason[:220]})
    print('%-44s %-7s %s' % (name, v, reason[:150]))
R['admitUnitRoots'] = rows
R['probeDefectCorrected'] = ('first run of this probe passed the membership wrapper dict instead of '
                             'membership["units"], so all nine cases refused units:not-a-list. That was '
                             'my fixture defect, not a design fault; preserved in pK2-rootexec.first-run.json')

# the enumeration-side translation, executed end to end
ers = []
for name, m in CASES:
    f = []
    ok = ENM._admit_membership_unit_roots(m, f)
    ers.append({'case': name, 'returned': ok, 'faults': f})
    print('  enumeration join %-42s ok=%-5s faults=%s' % (name, ok, f))
R['enumerationMembershipRootJoin'] = ers
R['sentinelRefusedWithRootSpecificFault'] = all(
    r['verdict'] == 'REFUSE' and 'NATIVE_UNIT_ROOT_REPRESENTATION' in r['reason']
    for r in rows if 'SENTINEL' in r['case'] or r['case'].startswith('rootPath="./"'))
R['lawfulStillAdmitted'] = [r for r in rows if 'lawful' in r['case']]

# ---- enumeration side: is the misattribution to PROGRAM_ENTRY gone? ----
src = open(os.path.join(F, 'foundation/enumeration_model.v1.py'), encoding='utf-8').read()
lines = src.splitlines()
print('\n--- enumeration_model.v1.py 495..530 ---')
for i in range(494, 531):
    print('%5d  %s' % (i + 1, lines[i]))
R['enumerationRootRegion'] = '\n'.join(lines[494:531])
print('\n--- enumeration_model.v1.py around BINDING_PROGRAM_ENTRY ---')
for i, l in enumerate(lines, 1):
    if 'ENUMERATION_BINDING_PROGRAM_ENTRY' in l:
        print('%5d  %s' % (i, l.strip()[:170]))
R['programEntryLines'] = [{'line': i, 'text': l.strip()}
                          for i, l in enumerate(lines, 1) if 'ENUMERATION_BINDING_PROGRAM_ENTRY' in l]

json.dump(R, open(os.path.join(OUT, 'pK2-rootexec.json'), 'w'), indent=1, default=str)
print('\nwrote pK2-rootexec.json')
