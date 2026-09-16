"""R01 — find the ACTUAL owner paths for the rows RR32-01/04 implicate, and diagnose the root cause
of the four false ownerPathsResolve booleans."""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
OUT = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1/receipts'
man = {f['path']: f for f in json.load(open(MAN))['files']}
V = json.load(open(os.path.join(V32, 'review.json')))
R = {}

# what I INTENDED to cite, from my own build2 source
b2 = open(os.path.join(V32, 'probes/build2.py'), encoding='utf-8').read()
m = re.search(r"R16 = \{(.*?)\n\}\n", b2, re.S)
R['build2R16Excerpt'] = m.group(1)[:1500] if m else None
intended = {}
for mm in re.finditer(r"'(DR-011-R\d\d)': \(\[([^\]]*)\]", b2):
    rid = mm.group(1)
    toks = re.findall(r"(?:([A-Za-z]+) \+ )?'([^']+)'", mm.group(2))
    pre = {'C': 'docs/v2/contracts/product-v1/',
           'F': 'docs/coop/design-corrections/foundation/',
           'N': 'docs/coop/design-corrections/native/',
           'S': 'docs/coop/design-corrections/security/',
           'Wf': 'docs/coop/design-corrections/workflows/',
           'A': 'docs/v2/architecture/'}
    intended[rid] = [(pre.get(p, '') + s) for p, s in toks]
R['intendedOwners'] = intended
print('--- what my build2 INTENDED to cite vs what was stored ---')
lost = {}
for rid, want in sorted(intended.items()):
    stored = V['inheritedResidualDispositions'][rid]['currentOwnerFiles']
    dropped = [p for p in want if p not in stored]
    if dropped:
        lost[rid] = dropped
        print('%-14s dropped: %s' % (rid, dropped))
R['silentlyDroppedOwners'] = lost
R['rootCause'] = (
    'build2 computed present = [p for p in owners if isfile(p)] and stored `present or owners`, then '
    'set ownerPathsResolveInFrozen32 = len(present) == len(owners). So a nonexistent path was '
    'SILENTLY DROPPED from the stored list while the boolean was computed against the original list. '
    'The stored paths therefore all resolve (measured True) yet the boolean reads False, and the '
    'intended owner is missing from the row. DR-007 used a different code path (the BASE_OWN dict, '
    'no filter), so its nonexistent path was stored as-is and no boolean was emitted.')
print('\nroot cause:', R['rootCause'][:260])

# discover the real owners
def find(pat, limit=8):
    return sorted(p for p in man if re.search(pat, p))[:limit]


R['candidates'] = {
    'evaluatorFaultContract': find(r'evaluator-fault-contract'),
    'factIdentityPolicy': find(r'fact-identity-policy'),
    'nativeProtocol': find(r'native-protocol'),
    'd9': find(r'/d9|D9'),
}
print('\n--- actual candidates in frozen32 ---')
for k, v in R['candidates'].items():
    print('   %-24s %s' % (k, v))

json.dump(R, open(os.path.join(OUT, 'r01-owners.json'), 'w'), indent=1, default=str)
print('\nwrote r01-owners.json')
