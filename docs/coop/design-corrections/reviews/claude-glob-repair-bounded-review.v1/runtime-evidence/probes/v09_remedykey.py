"""V09 — RRS-A2 concretely: (a) do two distinct retained Coverage records produce identical dissent
remedy text? (b) what key does the module actually order by, and is UTF-8 byte order published?"""
import json, os, re

RR = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1/captured'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
mod = open(os.path.join(RR, 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py'),
           encoding='utf-8').read()
wfs = open(os.path.join(RR, 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'),
           encoding='utf-8').read()
R = {}

print('--- module header: the declared coverage key ---')
for i, l in enumerate(mod.splitlines()[:20], 1):
    print('%5d  %s' % (i, l[:150]))
R['moduleHeader'] = mod.splitlines()[:20]


def remedy(row):
    """Exactly the construction at repair_closed_world_selection.v1.py:375-379."""
    return ("native deadCodeRepairEligible is false for "
            + row["relation"] + "@" + row["resolution"]
            + " in universe " + row["sourceUniverse"]
            + " (" + ",".join(row["closedWorld"].get("reasons", [])) + "); "
            + "declare entry points/consumers explicitly and re-run analysis")


base = {'relation': 'file', 'resolution': 'enumerated', 'sourceUniverse': 'uA',
        'closedWorld': {'deadCodeRepairEligible': False, 'reasons': ['nonliteral-loading']}}
rowA = dict(base, targetUniverse='uX', subjectScopeCommitment='commit1', coverageId='coverage2:aaa')
rowB = dict(base, targetUniverse='uY', subjectScopeCommitment='commit2', coverageId='coverage2:bbb')
ra, rb = remedy(rowA), remedy(rowB)
R['twoDistinctRecords'] = {'rowA': {k: rowA[k] for k in ('targetUniverse', 'subjectScopeCommitment', 'coverageId')},
                           'rowB': {k: rowB[k] for k in ('targetUniverse', 'subjectScopeCommitment', 'coverageId')},
                           'remedyA': ra, 'remedyB': rb, 'identicalText': ra == rb}
print('\n--- dissent remedy for two DISTINCT retained records ---')
print('rowA differs from rowB in targetUniverse, subjectScopeCommitment and coverage identity')
print('remedy A:', ra[:150])
print('remedy B:', rb[:150])
print('IDENTICAL TEXT:', ra == rb)
R['remedyIsAmbiguous'] = ra == rb

# what does the module sort/partition by?
R['sortCalls'] = [l.strip()[:180] for l in mod.splitlines()
                  if 'sort' in l and ('key=' in l or 'sorted(' in l)]
print('\n--- sort/ordering call sites ---')
for l in R['sortCalls']:
    print('   ', l[:170])
R['usesEncodeForOrdering'] = '.encode()' in mod
R['utf8NamedInModuleProse'] = bool(re.search(r'UTF-8|utf-8', mod))
R['utf8NamedInContractProse'] = bool(re.search(r'UTF-8 byte|utf-8 byte', wfs, re.I))
print('\nmodule orders with .encode() (byte order in code) :', R['usesEncodeForOrdering'])
print('UTF-8 named in module prose                       :', R['utf8NamedInModuleProse'])
print('UTF-8 byte ordering named in the contract prose    :', R['utf8NamedInContractProse'])

# is the full six-member key sequence published in the contract prose?
SEQ = ['relation', 'resolution', 'sourceUniverse', 'targetUniverse', 'subjectScopeCommitment']
win = re.search(r'CoverageKeyV2[^.]{0,400}', wfs)
R['coverageKeyInContractProse'] = win.group(0)[:400] if win else None
print('\nCoverageKeyV2 in the contract prose:', (R['coverageKeyInContractProse'] or 'ABSENT')[:300])
win2 = re.search(r'CoverageKeyV2[^.]{0,400}', mod)
R['coverageKeyInModuleProse'] = win2.group(0)[:400] if win2 else None
print('CoverageKeyV2 in the module prose  :', (R['coverageKeyInModuleProse'] or 'ABSENT')[:300])

R['ASSESSMENT'] = {
    'remedyCannotNameTheActualRecord': R['remedyIsAmbiguous'],
    'utf8ByteOrderingPublishedInProse': R['utf8NamedInContractProse'],
    'moduleAlreadyOrdersByBytesInCode': R['usesEncodeForOrdering']}
print('\nASSESSMENT:', json.dumps(R['ASSESSMENT']))
json.dump(R, open(os.path.join(OUT, 'v09-remedykey.json'), 'w'), indent=1, default=str)
print('wrote v09-remedykey.json')
