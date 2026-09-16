"""PROBE N (v27) — bind all 30 residual rows to frozen snapshot27 bytes.

For every row of the AUTHOR assessment I check, against the snapshot and my own 26->27 delta:
  * the 30 ids match source27's evaluation-residual-dispositions.proposed.json exactly;
  * sourceSelector /items/N addresses the row it claims to address;
  * every cited evidence path exists in frozen27 and its sha256 matches the citation;
  * the row's `sourceBytesChanged` claim agrees with my independently derived delta;
  * the `source` field of the proposed file resolves (or is inline-preserved history).
No row is graded from the author's own authorAssessment.
"""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v27.json'

man = {r['path']: r for r in json.load(open(MAN))['files']}
prop = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json')))
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
delta = json.load(open(os.path.join(OUT, 'p01-delta.json')))
changed27 = {c['path']: c for c in delta['changed']}
added27 = {a['path'] for a in delta['added']}

R = {'proposedSha256': hashlib.sha256(open(os.path.join(
    SRC, 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'), 'rb').read()).hexdigest()}
pids = [i['id'] for i in prop['items']]
aids = [i['id'] for i in era['items']]
R['idsIdentical'] = pids == aids
R['proposedIds'] = pids
print('30 ids identical between source27 proposal and author assessment:', R['idsIdentical'])
print('proposed standing:', prop['standing'])
print('author standing  :', str(era.get('standing'))[:300])
print('author sourceSha256 claim:', era.get('sourceSha256'), '== measured:',
      era.get('sourceSha256') == R['proposedSha256'])
R['authorSourceShaMatchesMeasured'] = era.get('sourceSha256') == R['proposedSha256']
R['authorSubjectManifestSha'] = era.get('subjectManifestSha256')
R['authorHistoricalSubjectManifestSha'] = era.get('historicalSubjectManifestSha256')

rows = []
for n, (p, a) in enumerate(zip(prop['items'], era['items'])):
    row = {'id': p['id'], 'selectorClaimed': a.get('sourceSelector'),
           'selectorAddressesThisRow': a.get('sourceSelector') == '/items/%d' % n,
           'proposedDisposition': p['proposedDisposition'],
           'proposedReviewStatus': p['reviewStatus'],
           'correctionsIdentical': p['correction'] == a.get('sourceCorrection'),
           'independentGrade': a.get('independentGrade'),
           'applied': a.get('applied'),
           'historicalLimitationReclassified': a.get('historicalLimitationReclassified'),
           'evidence': []}
    for ev in a.get('evidence', []):
        rel = ev['path']
        rec = man.get(rel)
        e = {'path': rel, 'inFrozen27': rec is not None,
             'citedSha': ev.get('sha256'), 'previousSha': ev.get('previousSha256'),
             'claimsBytesChanged': ev.get('sourceBytesChanged'),
             'resolveAgainst': ev.get('resolveAgainst'),
             'currentIndependentAssessment': ev.get('currentIndependentAssessment')}
        if rec:
            e['frozenSha'] = rec['sha256']
            e['citedShaMatchesFrozen27'] = rec['sha256'] == ev.get('sha256')
            myChanged = rel in changed27 or rel in added27
            e['myDeltaSaysChanged26to27'] = myChanged
            e['changeClaimAgreesWithMyDelta'] = bool(ev.get('sourceBytesChanged')) == myChanged
            if rel in changed27:
                e['myDeltaSha26'] = changed27[rel]['sha26']
                e['prevShaMatchesMyDelta26'] = ev.get('previousSha256') == changed27[rel]['sha26']
            else:
                e['prevShaMatchesMyDelta26'] = ev.get('previousSha256') == ev.get('sha256')
        row['evidence'].append(e)
    rows.append(row)

R['rows'] = rows
bad_sel = [r['id'] for r in rows if not r['selectorAddressesThisRow']]
bad_corr = [r['id'] for r in rows if not r['correctionsIdentical']]
unresolved = [(r['id'], e['path']) for r in rows for e in r['evidence'] if not e['inFrozen27']]
shamis = [(r['id'], e['path']) for r in rows for e in r['evidence'] if not e.get('citedShaMatchesFrozen27', True)]
claimdis = [(r['id'], e['path'], e.get('claimsBytesChanged'), e.get('myDeltaSaysChanged26to27'))
            for r in rows for e in r['evidence'] if not e.get('changeClaimAgreesWithMyDelta', True)]
prevmis = [(r['id'], e['path']) for r in rows for e in r['evidence'] if not e.get('prevShaMatchesMyDelta26', True)]
notPending = [r['id'] for r in rows if r['independentGrade'] != 'PENDING' or r['proposedReviewStatus'] != 'PENDING']
appliedTrue = [r['id'] for r in rows if r['applied']]
reclass = [r['id'] for r in rows if r['historicalLimitationReclassified']]

R.update(selectorMismatches=bad_sel, correctionMismatches=bad_corr,
         evidencePathsNotInFrozen27=unresolved, evidenceShaMismatches=shamis,
         changeClaimDisagreements=claimdis, previousShaMismatches=prevmis,
         rowsNotPending=notPending, rowsClaimingApplied=appliedTrue,
         rowsReclassifyingHistory=reclass)
print('\nselector mismatches            :', bad_sel)
print('correction text mismatches     :', bad_corr)
print('evidence paths not in frozen27 :', unresolved)
print('evidence sha mismatches vs 27  :', shamis)
print('changed-claim disagreements    :', claimdis)
print('previousSha mismatches         :', prevmis)
print('rows not PENDING               :', notPending)
print('rows claiming applied=true     :', appliedTrue)
print('rows reclassifying history     :', reclass)

# distinct evidence documents cited across the 30 rows
docs = {}
for r in rows:
    for e in r['evidence']:
        docs.setdefault(e['path'], []).append(r['id'])
R['citedDocuments'] = {k: v for k, v in sorted(docs.items())}
print('\ndistinct cited documents (%d):' % len(docs))
for k, v in sorted(docs.items()):
    ch = 'CHANGED-26to27' if (k in changed27 or k in added27) else 'unchanged'
    print('  %-72s %-14s rows=%d' % (k, ch, len(v)))

# does the proposed file's own `source` field resolve in 27?
srcs = sorted(set(i.get('source') for i in prop['items'] if i.get('source')))
R['proposedSourceFields'] = {s: (s in man) for s in srcs}
print('\nproposed `source` fields resolve in frozen27:')
for s in srcs:
    print('  %-60s %s' % (s, s in man))

json.dump(R, open(os.path.join(OUT, 'pN-residualbind.json'), 'w'), indent=1, default=str)
print('\nwrote pN-residualbind.json')
