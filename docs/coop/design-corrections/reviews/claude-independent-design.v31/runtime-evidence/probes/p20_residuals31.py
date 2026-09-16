"""PROBE 20 (v31) — bind all 30 residual rows to frozen31 and measure what changed since 27.

The proposal itself is unchanged 27->31; the AUTHOR assessment file changed. I check the ids, the
selectors, every cited evidence path/sha against frozen31, the change claims against my own delta,
and the shared TCB dependency list, classifying the dependents myself rather than adopting the list.
"""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
delta = json.load(open(os.path.join(OUT, 'p01-delta.json')))['cumulative']
changed31 = {c['path'] for c in delta['changed']} | {a['path'] for a in delta['added']}
R = {}

PP = 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'
prop = json.load(open(os.path.join(SRC, PP)))
R['proposalSha256'] = hashlib.sha256(open(os.path.join(SRC, PP), 'rb').read()).hexdigest()
R['proposalChangedSince27'] = PP in changed31
R['proposalStanding'] = prop['standing']
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
R['authorAssessmentSha256'] = hashlib.sha256(
    open(os.path.join(PKG, 'evaluation-residual-author-assessment.json'), 'rb').read()).hexdigest()
pids = [i['id'] for i in prop['items']]
aids = [i['id'] for i in era['items']]
R['proposalIds'] = pids
R['idsIdentical'] = pids == aids
R['rowCount'] = len(pids)
print('proposal unchanged 27->31 :', not R['proposalChangedSince27'])
print('30 ids identical          :', R['idsIdentical'], len(pids))
print('author sourceSha256 claim matches proposal:',
      era.get('sourceSha256') == R['proposalSha256'])
R['authorSourceShaMatches'] = era.get('sourceSha256') == R['proposalSha256']
R['authorSubjectManifestSha256'] = era.get('subjectManifestSha256')
R['authorBindsFrozen31Manifest'] = era.get('subjectManifestSha256') == \
    'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
print('author assessment binds frozen31 manifest :', R['authorBindsFrozen31Manifest'])

rows = []
for n, (p, a) in enumerate(zip(prop['items'], era['items'])):
    row = {'id': p['id'], 'selector': a.get('sourceSelector'),
           'selectorAddressesRow': a.get('sourceSelector') == '/items/%d' % n,
           'proposedDisposition': p['proposedDisposition'],
           'reviewStatus': p['reviewStatus'],
           'correctionIdentical': p['correction'] == a.get('sourceCorrection'),
           'independentGrade': a.get('independentGrade'),
           'applied': a.get('applied'),
           'hasInlineOriginal': bool(p.get('original')),
           'hasOriginalTitle': bool(p.get('originalTitle')),
           'sourceField': p.get('source'),
           'sourceResolvesInFrozen31': p.get('source') in man if p.get('source') else None,
           'evidence': []}
    for ev in a.get('evidence', []):
        rel = ev['path']
        rec = man.get(rel)
        e = {'path': rel, 'inFrozen31': rec is not None, 'citedSha': ev.get('sha256'),
             'claimsBytesChanged': ev.get('sourceBytesChanged'),
             'currentIndependentAssessment': ev.get('currentIndependentAssessment')}
        if rec:
            e['shaMatchesFrozen31'] = rec['sha256'] == ev.get('sha256')
            e['myDeltaSaysChanged27to31'] = rel in changed31
            e['changeClaimAgreesWithMyDelta'] = bool(ev.get('sourceBytesChanged')) == (rel in changed31)
        row['evidence'].append(e)
    rows.append(row)
R['rows'] = rows

bad_sel = [r['id'] for r in rows if not r['selectorAddressesRow']]
bad_corr = [r['id'] for r in rows if not r['correctionIdentical']]
unres = [(r['id'], e['path']) for r in rows for e in r['evidence'] if not e['inFrozen31']]
shamis = [(r['id'], e['path']) for r in rows for e in r['evidence'] if not e.get('shaMatchesFrozen31', True)]
claimdis = [(r['id'], e['path'], e.get('claimsBytesChanged'), e.get('myDeltaSaysChanged27to31'))
            for r in rows for e in r['evidence'] if not e.get('changeClaimAgreesWithMyDelta', True)]
notpend = [r['id'] for r in rows if r['independentGrade'] != 'PENDING' or r['reviewStatus'] != 'PENDING']
appl = [r['id'] for r in rows if r['applied']]
R.update(selectorMismatches=bad_sel, correctionMismatches=bad_corr,
         evidenceNotInFrozen31=unres, evidenceShaMismatches=shamis,
         changeClaimDisagreements=claimdis, rowsNotPending=notpend, rowsApplied=appl)
print('\nselector mismatches            :', bad_sel)
print('correction mismatches          :', bad_corr)
print('evidence paths not in frozen31 :', unres)
print('evidence sha mismatches        :', shamis)
print('change-claim disagreements     :', claimdis)
print('rows not PENDING               :', notpend)
print('rows claiming applied          :', appl)

R['rowsWithNeitherOriginal'] = [r['id'] for r in rows if not r['hasInlineOriginal'] and not r['hasOriginalTitle']]
R['sourceFieldsResolving'] = {r['id']: r['sourceResolvesInFrozen31'] for r in rows}
R['allSourceFieldsResolve'] = all(v for v in R['sourceFieldsResolving'].values() if v is not None)
print('\nrows with neither inline original nor title :', R['rowsWithNeitherOriginal'])
print('all `source` fields resolve in frozen31     :', R['allSourceFieldsResolve'], '(A-5)')

docs = {}
for r in rows:
    for e in r['evidence']:
        docs.setdefault(e['path'], []).append(r['id'])
R['citedDocuments'] = {k: {'rows': len(v), 'changed27to31': k in changed31} for k, v in sorted(docs.items())}
print('\ncited documents:')
for k, v in R['citedDocuments'].items():
    print('   %-72s rows=%-3d changed=%s' % (k[-72:], v['rows'], v['changed27to31']))

# ---- shared TCB dependency ----
dep = era.get('sharedReviewDependencies')
R['sharedReviewDependencies'] = dep
if dep:
    d0 = dep[0]
    R['tcbId'] = d0.get('id')
    R['tcbDependents'] = d0.get('dependentResidualIds')
    R['tcbDependentCount'] = len(d0.get('dependentResidualIds', []))
    print('\n%s dependents (%d): %s' % (R['tcbId'], R['tcbDependentCount'], R['tcbDependents']))
    print('assumption :', str(d0.get('assumption'))[:240])
    print('consequence:', str(d0.get('consequence'))[:240])

verd = {}
for i in era['items']:
    verd[i.get('authorAssessment')] = verd.get(i.get('authorAssessment'), 0) + 1
R['authorVerdictCounts'] = verd
print('\nauthor self-assessment verdict counts:', verd)

json.dump(R, open(os.path.join(OUT, 'p20-residuals31.json'), 'w'), indent=1, default=str)
print('\nwrote p20-residuals31.json')
