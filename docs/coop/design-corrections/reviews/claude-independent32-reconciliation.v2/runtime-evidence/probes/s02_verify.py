"""S02 — correct one imprecise sentence in my own V2-03 entry, then verify the COMPLETE final JSON:
no wrong delta arrays anywhere, no contradictory reading history, everything else preserved."""
import hashlib, json, os

V2 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2'
V1 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
RJ = os.path.join(V2, 'review.json')
m31 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v31.json')))['files']}
m32 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v32.json')))['files']}
R = json.load(open(RJ))
OLD = json.load(open(os.path.join(V1, 'review.json')))
C = {}


def chk(name, ok, detail=''):
    C[name] = bool(ok)
    print('%-58s %s %s' % (name, 'OK ' if ok else 'FAIL', detail if not ok else ''))


# precision fix on my own entry
for c in R['correctionsToMyOwnReconciliationV1']:
    if c['id'] == 'V2-03':
        c['evidence'] = (
            'Re-derived every row\'s changed/unchanged arrays from the v31/v32 manifest hashes and '
            'asserted the result. DR-007 was the row that needed adjusting and is corrected under '
            'V2-01; the audit loop ran after that fix, so its "0 rows adjusted" reports the '
            'post-correction state across all 63 owner-bearing rows rather than implying no row ever '
            'needed it.')
        c['fix'] = ('all 63 owner-bearing rows now carry arrays derived from manifest hashes, with an '
                    'assertion that each matches; 0 unresolved owner paths.')

# ---- no wrong delta arrays anywhere ----
MAPS = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
bad, unres = [], []
n = 0
for mp in MAPS:
    for rid, row in R[mp].items():
        n += 1
        ow = row['currentOwnerFiles']
        ch = sorted(p for p in ow if m31.get(p) != m32.get(p))
        un = sorted(p for p in ow if m31.get(p) == m32.get(p))
        if sorted(row['ownerFilesChangedIn31to32']) != ch or sorted(row['ownerFilesUnchangedIn31to32']) != un:
            bad.append(mp + '/' + rid)
        if any(p not in m32 for p in ow):
            unres.append(mp + '/' + rid)
        if set(row['ownerFilesChangedIn31to32']) & set(row['ownerFilesUnchangedIn31to32']):
            bad.append(mp + '/' + rid + ':overlap')
        if sorted(row['ownerFilesChangedIn31to32'] + row['ownerFilesUnchangedIn31to32']) != sorted(ow):
            bad.append(mp + '/' + rid + ':partition')
chk('all %d owner-bearing rows have manifest-correct arrays' % n, not bad, str(bad)[:200])
chk('changed/unchanged partition every owner exactly once', not [x for x in bad if 'partition' in x])
chk('no owner path unresolved in frozen32', not unres, str(unres)[:160])

# ---- DR-007 specifics ----
d = R['inheritedResidualDispositions']['DR-007']
chk('DR-007 names both changed chapters', len(d['ownerFilesChangedIn31to32']) == 2)
chk('DR-007 unchanged is only the v3 fault contract',
    d['ownerFilesUnchangedIn31to32'] == ['docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md'])
chk('DR-007 standing says unchanged SINCE source32, not 31->32',
    'unchanged SINCE source32' in d['readingStanding'] and 'DID change 31->32' in d['readingStanding'])

# ---- RES-EP13-13 ----
r13 = R['evaluationResidualDispositions']['RES-EP13-13']
chk('RES-EP13-13 no longer says "which I reviewed then"',
    'which I reviewed then' not in r13['currentStatusOn32'])
chk('RES-EP13-13 status names the source31 review',
    'source31 review' in r13['currentStatusOn32'])
chk('RES-EP13-13 status and standing agree on source31',
    'source31' in r13['currentStatusOn32'] and 'SOURCE31' in r13['readingStanding'].upper())
# classify by JSON path: an occurrence inside recordCorrection / corrections / evidence is a
# DOCUMENTED QUOTATION of the wording being corrected, not a live claim. My first version of this
# check flat-matched the document and flagged those two quotations (see s03-locate.json).
def live_occurrences(token):
    found = []

    def walk(o, path='$'):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + '/%d' % i)
        elif isinstance(o, str) and token in o:
            if not any(t in path for t in ('recordCorrection', 'correctionsToMyOwn',
                                           'rootFinding', 'evidence')):
                found.append(path)
    walk(o=R)
    return found


chk('no LIVE source28 session claim (quotations in corrections excluded)',
    not live_occurrences('read fresh in that session'),
    str(live_occurrences('read fresh in that session'))[:160])

# ---- everything else preserved ----
for k, cnt in (('fDispositions', 14), ('evaluationResidualDispositions', 30), ('arDispositions', 16),
               ('fwDispositions', 15), ('inheritedResidualDispositions', 27),
               ('scopedReviewOwnerDispositions', 5)):
    chk('map %s still has %d rows' % (k, cnt), len(R[k]) == cnt)
    chk('map %s row ids unchanged' % k, sorted(R[k]) == sorted(OLD[k]))
chk('verdict preserved ACCEPT', R['verdict'] == 'ACCEPT' == OLD['verdict'])
chk('manifest binding is source32',
    R['subjectManifestSha256'] == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2')
chk('advisories A-9/A-10 preserved',
    [a['id'] for a in R['advisories']] == [a['id'] for a in OLD['advisories']] == ['A-9', 'A-10'])
chk('TCB assessed once with 13 dependents',
    R['sharedAssumptionTCBSCOPE01']['dependentRowCount'] == 13
    and sum(1 for v in R['evaluationResidualDispositions'].values() if v['sharedAssumption']) == 13)
cu = R['crossUnitStanding']
chk('28 / 32-unperformed / 54 / condition5 intact',
    cu['condition2ObligationsRetained'] == 28 and cu['qualificationGatesPerformed'] == 0
    and cu['commitRecoveryCasesExecuted'] == 0 and cu['condition5'] == 'NOT MET')
chk('D9 successor still assigned', 'ASSIGNED' in cu['d9SuccessorObligation'].upper())
g = R['grantsNothing']
chk('grantsNothing design-only preserved',
    g['grade'] is None and not g['activation'] and not g['implementationAuthorized']
    and not g['blindAcceptance'] and not g['architectureReady'])
applied = [(mp, rid) for mp in ('fDispositions', 'evaluationResidualDispositions') + MAPS
           for rid, v in R[mp].items() if v['appliedByThisReview'] or v['finalApplicationOutcomeGranted']]
chk('no row claims applied or granted', not applied, str(applied)[:140])
chk('v1 corrections list retained', len(R['correctionsToMyOwnV32Record']) >= 4)
chk('v2 corrections list present', len(R['correctionsToMyOwnReconciliationV1']) == 3)
chk('recordLineage points at this runtime and hash-binds v1',
    R['recordLineage']['thisRuntime'].endswith('v2')
    and R['recordLineage']['immediateInput']['sha256'] ==
    hashlib.sha256(open(os.path.join(V1, 'review.json'), 'rb').read()).hexdigest())
chk('original source32 lineage retained',
    R['recordLineage']['originalRecord']['path'].startswith('claude-independent-design.v32'))
chk('inherited read/execution scope stated',
    'this pass" means' in R['reconciliationStanding']['v2Followup']['inheritedReadExecutionScope']
    or 'means the v1' in R['reconciliationStanding']['v2Followup']['inheritedReadExecutionScope'])
chk('v1 reports preserved on disk',
    os.path.isfile(os.path.join(V1, 'review.json')) and os.path.isfile(os.path.join(V1, 'review.md')))

json.dump(R, open(RJ, 'w'), indent=1, default=str)
final = hashlib.sha256(open(RJ, 'rb').read()).hexdigest()
fails = [k for k, v in C.items() if not v]
print('\n%d checks, %d failures %s' % (len(C), len(fails), fails))
print('FINAL review.json sha256:', final)
json.dump({'checks': C, 'failures': fails, 'finalJsonSha256': final},
          open(os.path.join(V2, 'receipts', 's02-verify.json'), 'w'), indent=1)
print('wrote s02-verify.json')
