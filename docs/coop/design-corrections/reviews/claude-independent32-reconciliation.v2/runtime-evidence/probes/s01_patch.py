"""S01 — apply the two substantiated corrections in place, re-derive EVERY owner changed/unchanged
array from the v31/v32 manifest hashes, and assert the result matches. Small targeted mutation of
the copied JSON; the whole document is not re-emitted by hand."""
import hashlib, json, os

V2 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
OUT = os.path.join(V2, 'receipts')
RJ = os.path.join(V2, 'review.json')
s00 = json.load(open(os.path.join(OUT, 's00-copy-verify.json')))
m31 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v31.json')))['files']}
m32 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v32.json')))['files']}
R = json.load(open(RJ))
rep = {'manifestsUsed': {'v31': s00['manifest31Sha256'], 'v32': s00['manifest32Sha256']}}

# ---------------- 1. DR-007 ----------------
dr7 = R['inheritedResidualDispositions']['DR-007']
owners = list(dr7['currentOwnerFiles'])
changed = sorted(p for p in owners if m31.get(p) != m32.get(p))
unchanged = sorted(p for p in owners if m31.get(p) == m32.get(p))
rep['dr007Before'] = {'changed': dr7['ownerFilesChangedIn31to32'],
                      'unchanged': dr7['ownerFilesUnchangedIn31to32']}
dr7['ownerFilesChangedIn31to32'] = changed
dr7['ownerFilesUnchangedIn31to32'] = unchanged
dr7['readingStanding'] = (
    'The owning fault contract foundation/evaluator-fault-contract.v3.md is UNCHANGED 31->32 and was '
    'READ FRESH in the v1 reconciliation pass. The two product chapters '
    'workflows-and-surfaces.md and native-evidence.md DID change 31->32; their changed regions were '
    'read in my source32 review, and that reading is INHERITED here as unchanged SINCE source32 — not '
    'as unchanged 31->32. No new read or execution is claimed in this pass.')
dr7['recordCorrectionV2'] = (
    'Leftover 1: my v1 pass set ownerFilesChangedIn31to32 to [] and moved both product chapters into '
    'the unchanged list, and its readingStanding called the other owners unchanged 31->32. Compared on '
    'the manifest rows, workflows-and-surfaces.md (3d89b511… -> b2530a31…) and native-evidence.md '
    '(8b2579d8… -> 6bffdeef…) both changed; only evaluator-fault-contract.v3.md (5731b41d…, identical) '
    'did not. Arrays and standing corrected.')
rep['dr007After'] = {'changed': changed, 'unchanged': unchanged}
print('DR-007 changed  :', changed)
print('DR-007 unchanged:', unchanged)

# ---------------- 2. RES-EP13-13 ----------------
res = R['evaluationResidualDispositions']['RES-EP13-13']
old = res['currentStatusOn32']
BAD = ', which is a different concern and which I reviewed then.'
GOOD = (', which is a different concern and which I reviewed in my source31 review of the 27->31 '
        'delta. There was no source28 review session in my lineage.')
assert BAD in old, 'expected clause not found'
res['currentStatusOn32'] = old.replace(BAD, GOOD)
res['recordCorrectionV2'] = (
    'Leftover 2: the status clause still ended "which I reviewed then" about the 27->28 window, which '
    'read as a source28 review even though the readingStanding had already been corrected to source31. '
    'Replaced with the actual source31 review and an explicit statement that no source28 session exists.')
rep['res13ClauseReplaced'] = {'from': BAD.strip(), 'to': GOOD.strip()}
print('\nRES-EP13-13 clause replaced')

# ---------------- 3. re-derive EVERY owner array from the manifests ----------------
MAPS = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
audit = {'rowsProcessed': 0, 'rowsAdjusted': [], 'mismatchesBeforeFix': [], 'unresolvedOwners': []}
for mp in MAPS:
    for rid, row in R[mp].items():
        owners = row.get('currentOwnerFiles', [])
        audit['rowsProcessed'] += 1
        ch = sorted(p for p in owners if m31.get(p) != m32.get(p))
        un = sorted(p for p in owners if m31.get(p) == m32.get(p))
        miss = [p for p in owners if p not in m32]
        if miss:
            audit['unresolvedOwners'].append({'row': mp + '/' + rid, 'missing': miss})
        if sorted(row.get('ownerFilesChangedIn31to32', [])) != ch or \
           sorted(row.get('ownerFilesUnchangedIn31to32', [])) != un:
            audit['mismatchesBeforeFix'].append(
                {'row': mp + '/' + rid,
                 'recordedChanged': row.get('ownerFilesChangedIn31to32'),
                 'derivedChanged': ch,
                 'recordedUnchanged': row.get('ownerFilesUnchangedIn31to32'),
                 'derivedUnchanged': un})
            audit['rowsAdjusted'].append(mp + '/' + rid)
        row['ownerFilesChangedIn31to32'] = ch
        row['ownerFilesUnchangedIn31to32'] = un
        row['ownerPathsResolveInFrozen32'] = not miss
        row['ownerArraysDerivedFromManifestHashes'] = True
rep['ownerArrayAudit'] = audit
print('\nrows processed: %d | rows whose arrays needed adjusting: %d'
      % (audit['rowsProcessed'], len(audit['rowsAdjusted'])))
for x in audit['mismatchesBeforeFix']:
    print('   %-44s recorded changed=%s derived=%s' % (x['row'], x['recordedChanged'], x['derivedChanged']))
print('unresolved owner paths:', audit['unresolvedOwners'])

# assert the derivation now matches everywhere
bad = []
for mp in MAPS:
    for rid, row in R[mp].items():
        owners = row['currentOwnerFiles']
        if sorted(row['ownerFilesChangedIn31to32']) != sorted(p for p in owners if m31.get(p) != m32.get(p)):
            bad.append(mp + '/' + rid)
        if sorted(row['ownerFilesUnchangedIn31to32']) != sorted(p for p in owners if m31.get(p) == m32.get(p)):
            bad.append(mp + '/' + rid)
assert not bad, bad
rep['allOwnerArraysMatchManifestDerivation'] = True
print('all owner arrays match the manifest derivation:', True)

# ---------------- 4. lineage + corrections list ----------------
R['recordLineage'] = {
    'thisRuntime': 'claude-independent32-reconciliation.v2',
    'immediateInput': {'path': 'claude-independent32-reconciliation.v1/review.json',
                       'sha256': s00['inputV1ReviewJsonSha256'],
                       'mdSha256': s00['inputV1ReviewMdSha256'],
                       'standing': 'preserved unchanged; copied complete into this runtime and then '
                                   'corrected in place'},
    'originalRecord': {'path': 'claude-independent-design.v32/review.json',
                       'sha256': R.get('recordLineage', {}).get('supersededRecord', {}).get('sha256'),
                       'standing': 'the original source32 review, preserved unchanged'},
    'subjectUnchanged': ('frozen source32 is UNCHANGED. This is a narrow record-only followup: no '
                         'suites rerun, no full-source read, no archive scan, no new executions.'),
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'noSourceEdits': True}
R['correctionsToMyOwnReconciliationV1'] = [
    {'id': 'V2-01', 'issue': 'DR-007 owner changed/unchanged arrays and reading standing were wrong',
     'independentlyVerified': True,
     'evidence': ('compared the three owner rows across the exact v31 and v32 manifests: '
                  'workflows-and-surfaces.md 3d89b511… -> b2530a31… CHANGED; native-evidence.md '
                  '8b2579d8… -> 6bffdeef… CHANGED; evaluator-fault-contract.v3.md 5731b41d… '
                  'identical, UNCHANGED. My v1 pass had recorded changed=[] and placed both chapters '
                  'in the unchanged list.'),
     'agree': True,
     'fix': ('arrays corrected to the derived values, and the standing now says the fault contract is '
             'unchanged 31->32 and was read fresh in v1, while the two chapters changed 31->32 and '
             'their reading is inherited from my source32 review as unchanged SINCE source32.')},
    {'id': 'V2-02', 'issue': 'RES-EP13-13 status still ended "which I reviewed then" about 27->28',
     'independentlyVerified': True,
     'evidence': ('the clause survived in currentStatusOn32 even though readingStanding had already '
                  'been corrected to name the source31 review, so the row contradicted itself.'),
     'agree': True,
     'fix': 'clause replaced with the actual source31 review plus an explicit "no source28 review session".'},
    {'id': 'V2-03', 'issue': 'owner changed/unchanged arrays were not uniformly manifest-derived',
     'independentlyVerified': True,
     'evidence': ('re-derived every row\'s arrays from the v31/v32 manifest hashes; %d of %d rows '
                  'needed adjusting, all of them the DR-007 row and rows whose arrays had been built '
                  'by hand rather than from hashes.' % (len(audit['rowsAdjusted']), audit['rowsProcessed'])),
     'agree': True,
     'fix': 'all owner arrays now derived from manifest hashes and asserted to match.'}]
R['reconciliationStanding']['v2Followup'] = {
    'scope': 'record-only metadata correction; no design reassessment, no suite rerun, no new reads',
    'dispositionsChanged': 0, 'verdictChanged': False,
    'rowsCorrected': ['DR-007', 'RES-EP13-13'] + sorted(set(
        x.split('/')[-1] for x in audit['rowsAdjusted'])),
    'newSourceDefect': False,
    'inheritedReadExecutionScope': ('Where the v1 text says "this pass" it means the v1 '
                                    'reconciliation. This v2 followup claims no new reads and no new '
                                    'executions; all executed evidence remains cited at its original '
                                    'v31/v32 receipt locations.')}
json.dump(R, open(RJ, 'w'), indent=1, default=str)
rep['finalJsonSha256'] = hashlib.sha256(open(RJ, 'rb').read()).hexdigest()
json.dump(rep, open(os.path.join(OUT, 's01-patch.json'), 'w'), indent=1, default=str)
print('\nfinal review.json sha256:', rep['finalJsonSha256'])
print('wrote s01-patch.json')
