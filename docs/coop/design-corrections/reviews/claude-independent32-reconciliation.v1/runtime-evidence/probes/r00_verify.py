"""R00 — verify the reconciliation inputs, then independently test RR32-01..04 against my ACTUAL
v32 review.json and the frozen source32 snapshot. Root is assessed, not rubber-stamped."""
import hashlib, json, os

V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
OUT = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1/receipts'
os.makedirs(OUT, exist_ok=True)
EXP_MAN = '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
R['manifestSha256'] = sha(MAN)
R['manifestMatchesRequired'] = R['manifestSha256'] == EXP_MAN
man = {f['path']: f for f in json.load(open(MAN))['files']}
R['manifestFileCount'] = len(man)
print('source32 manifest sha matches required:', R['manifestMatchesRequired'], '| files', len(man))

rj = os.path.join(V32, 'review.json')
R['myV32ReviewSha256'] = sha(rj)
R['rootQuotedReviewSha256'] = '90abddbbdee7877925d4973ed1bed40c78f156000a4f8d0c300e5054f0e044fe'
R['rootQuotedShaMatchesMyFile'] = R['myV32ReviewSha256'] == R['rootQuotedReviewSha256']
print('my review32 sha            :', R['myV32ReviewSha256'][:24])
print('root quoted sha matches it :', R['rootQuotedShaMatchesMyFile'])
V = json.load(open(rj))

# ---------------- RR32-01 ----------------
dr7 = V['inheritedResidualDispositions']['DR-007']
owners7 = dr7['currentOwnerFiles']
R['RR32_01'] = {'DR007_currentOwnerFiles': owners7,
                'DR007_unchangedList': dr7['ownerFilesUnchangedIn31to32'],
                'eachPathInFrozen32': {p: (p in man) for p in owners7}}
faultdir = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
cands = sorted(n for n in os.listdir(faultdir) if 'evaluator-fault-contract' in n)
R['RR32_01']['actualFaultContractFiles'] = cands
R['RR32_01']['citedV1Exists'] = any(p.endswith('evaluator-fault-contract.v1.md') and p in man
                                    for p in owners7)
R['RR32_01']['rootIsCorrect'] = (
    any('evaluator-fault-contract.v1.md' in p for p in owners7)
    and not R['RR32_01']['citedV1Exists'])
print('\nRR32-01: DR-007 owners =', owners7)
print('   each in frozen32   :', R['RR32_01']['eachPathInFrozen32'])
print('   actual fault-contract files on disk:', cands)
print('   root correct       :', R['RR32_01']['rootIsCorrect'])

# ---------------- RR32-02 ----------------
f04 = V['fDispositions']['F-04']
R['RR32_02'] = {'F04_limits': f04.get('limits'),
                'saysPrecedes': 'precedes structural custody' in str(f04.get('limits', ''))}
allhits = []
s = json.dumps(V)
import re
for m in re.finditer(r'[^"]{0,140}precede[sd][^"]{0,140}', s):
    t = m.group(0)
    if 'structural' in t or 'enumeration' in t:
        allhits.append(t)
R['RR32_02']['everyPrecedenceSentence'] = allhits
R['RR32_02']['rootIsCorrect'] = R['RR32_02']['saysPrecedes']
print('\nRR32-02: F-04 limits =', f04.get('limits'))
print('   root correct       :', R['RR32_02']['rootIsCorrect'])
print('   all precedence sentences in review32:')
for t in allhits:
    print('      ...', t[:190])

# ---------------- RR32-03 ----------------
res13 = V['evaluationResidualDispositions']['RES-EP13-13']
R['RR32_03'] = {'readingStanding': res13.get('readingStanding'),
                'fileLastChangedWindow': res13.get('fileLastChangedWindow'),
                'claimsReadInThatSession': 'read fresh in that session' in str(res13.get('readingStanding'))}
R['RR32_03']['myActualReviewLineage'] = ['source26', 'source27', 'source31', 'source32',
                                         'bounded glob/repair (no source version)']
R['RR32_03']['noV28ReviewSessionExists'] = True
R['RR32_03']['rootIsCorrect'] = R['RR32_03']['claimsReadInThatSession']
print('\nRR32-03: RES-EP13-13 readingStanding =', str(res13.get('readingStanding'))[:220])
print('   claims it was read in "that session":', R['RR32_03']['claimsReadInThatSession'])
print('   my lineage has no source28 review    :', R['RR32_03']['noV28ReviewSessionExists'])
print('   root correct                         :', R['RR32_03']['rootIsCorrect'])

# ---------------- RR32-04 ----------------
inh = V['inheritedResidualDispositions']
r16 = {k: v for k, v in inh.items() if k.startswith('DR-011-R')}
R['RR32_04'] = {'rowCount': len(r16), 'reported': {}, 'measured': {}, 'disagreements': []}
for k, v in sorted(r16.items()):
    rep = v.get('ownerPathsResolveInFrozen32')
    owners = v['currentOwnerFiles']
    measured = all(p in man for p in owners)
    R['RR32_04']['reported'][k] = rep
    R['RR32_04']['measured'][k] = {'allInFrozen32': measured,
                                   'missing': [p for p in owners if p not in man]}
    if rep != measured:
        R['RR32_04']['disagreements'].append(k)
print('\nRR32-04: the 16 DR-011-R rows')
print('%-14s %-10s %-10s %s' % ('row', 'reported', 'measured', 'missing paths'))
for k in sorted(r16):
    m = R['RR32_04']['measured'][k]
    flag = '  <-- DISAGREES' if R['RR32_04']['reported'][k] != m['allInFrozen32'] else ''
    print('%-14s %-10s %-10s %s%s' % (k, R['RR32_04']['reported'][k], m['allInFrozen32'],
                                      m['missing'], flag))
R['RR32_04']['rootIsCorrect'] = bool(R['RR32_04']['disagreements'])
print('rows where the reported boolean disagrees with measurement:', R['RR32_04']['disagreements'])

# ---------------- every owner path in all 107 rows ----------------
MAPS = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
bad = {}
for mp in MAPS:
    for rid, row in V[mp].items():
        miss = [p for p in row.get('currentOwnerFiles', []) if p not in man]
        if miss:
            bad[mp + '/' + rid] = miss
# evaluation residuals use currentOwnerSelectors
for rid, row in V['evaluationResidualDispositions'].items():
    miss = [p for p in row.get('currentOwnerSelectors', []) if p not in man]
    if miss:
        bad['evaluationResidualDispositions/' + rid] = miss
R['ownerPathsNotInFrozen32'] = bad
print('\n--- every owner path across all 107 rows ---')
print('rows citing a path absent from frozen32:', len(bad))
for k, v in bad.items():
    print('   %-52s %s' % (k, v))
json.dump(R, open(os.path.join(OUT, 'r00-verify.json'), 'w'), indent=1, default=str)
print('\nwrote r00-verify.json')
