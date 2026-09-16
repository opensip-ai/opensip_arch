"""PROBE K3 (v27) — is the new root guard actually WIRED before the binding join, and does any
reference checker on snapshot27 exercise it? A defined-but-uncalled guard would be a real gap,
and F-05's complaint was precisely an enforced-but-unexercised rule."""
import json, os, re, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
F = os.path.join(SRC, 'docs/coop/design-corrections')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
R = {}

enm = open(os.path.join(F, 'foundation/enumeration_model.v1.py'), encoding='utf-8').read()
lines = enm.splitlines()
calls = [(i, l.strip()) for i, l in enumerate(lines, 1) if '_admit_membership_unit_roots' in l]
R['guardDefAndCallSites'] = [{'line': i, 'text': t} for i, t in calls]
print('--- _admit_membership_unit_roots sites ---')
for i, t in calls:
    print('%5d  %s' % (i, t[:170]))
pe = [i for i, l in enumerate(lines, 1) if '_add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")' in l]
uc = [i for i, l in enumerate(lines, 1) if '_unit_for_cell(' in l]
callsite = [i for i, t in calls if not t.startswith('def ')]
R['programEntryRaiseLines'] = pe
R['unitForCellLines'] = uc
R['guardCallLines'] = callsite
print('\nPROGRAM_ENTRY raises at', pe)
print('_unit_for_cell at       ', uc)
print('guard called at         ', callsite)
R['guardPrecedesBindingJoin'] = bool(callsite) and min(callsite) < min(pe + uc)
print('guard precedes binding join:', R['guardPrecedesBindingJoin'])

# is the guard's refusal actually consulted (return value used to stop)?
if callsite:
    i = min(callsite)
    print('\n--- call context %d..%d ---' % (i - 8, i + 10))
    for n in range(max(0, i - 9), min(len(lines), i + 10)):
        print('%5d  %s' % (n + 1, lines[n]))
    R['callContext'] = '\n'.join(lines[max(0, i - 9):i + 10])

# which reference checkers mention the new tokens?
for tok in ('NATIVE_UNIT_ROOT_REPRESENTATION', 'ENUMERATION_MEMBERSHIP_UNIT_ROOT',
            'InternalUnitRootV1', 'admit_unit_roots', 'ENUMERATION_BINDING_PROGRAM_ENTRY'):
    r = subprocess.run(['grep', '-rl', tok, F], capture_output=True, text=True)
    files = [os.path.relpath(x, SRC) for x in r.stdout.split() if x]
    checkers = [f for f in files if '/check' in f or f.rsplit('/', 1)[-1].startswith('check')]
    R.setdefault('tokenFiles', {})[tok] = files
    R.setdefault('tokenCheckers', {})[tok] = checkers
    print('\n%-36s files=%d  checkers=%s' % (tok, len(files), checkers))
    for f in files[:8]:
        print('      ', f)

json.dump(R, open(os.path.join(OUT, 'pK3-rootwiring.json'), 'w'), indent=1, default=str)
print('\nwrote pK3-rootwiring.json')
