"""R08 — carry-forward audit of the COMPLETE source35 baseline for source36.
  * all 107 rows across the six maps, from the v35 review.json (sha-checked)
  * owner arrays 35->36 derived from the two manifests (not prose)
  * the historical source35 classes (91 inherited / 11 package / 5 cross-owner) and nine legacy corrections, re-verified
  * which rows' owners, or subject owners named in the baseline, touch the 10-file 35->36 delta
  * a keyword scan of every row's text for subjects the 36 changes can bear on (candidates for fresh cross-owner reasoning;
    the scan selects rows to READ, it decides nothing)"""
import hashlib, json, os, re

V35 = '/tmp/opensip-design-corrections/claude-independent-design.v35'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {'baselineSha256': sha(os.path.join(V35, 'review.json'))}
R['baselineMatches'] = R['baselineSha256'] == 'd7dc035c532968df80334809815f1257a49b83fd47f880e3a89630df9669cd52'
J = json.load(open(os.path.join(V35, 'review.json')))
r00 = json.load(open(os.path.join(OUT, 'r00-custody.json')))
m36 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v36.json')))['files']}
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
DELTA = {c['path'] for c in r00['delta']['changed']}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
EXPECT = {'fDispositions': 14, 'evaluationResidualDispositions': 30, 'arDispositions': 16, 'fwDispositions': 15,
          'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5}
KW = re.compile(r'(?i)(depend|DEPENDS_ON|sufficien|totality|all-covered|coverage-unknown|carrier|reachab|\bcalls\b|incoming|'
                r'history|HistorySubject|duplicate path|runtime-observation|observab|polarity|importQuantif|projection registry|'
                r'evaluator-projection-registry|atom_model|atom-evaluation|check-atoms|determinis|order independen|regroup|partition)')
R['counts'] = {mp: len(J[mp]) for mp in MAPS}
R['countsMatchExpected'] = R['counts'] == EXPECT
R['rows'] = {}
cls35, cls34 = {}, {}
for mp in MAPS:
    for rid, row in J[mp].items():
        key = mp + '/' + rid
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        subj = row.get('subjectOwnerFilesOn34') or []
        st35, st34 = row.get('statusChangeOn35'), row.get('statusChangeOn34')
        cls35[st35] = cls35.get(st35, 0) + 1
        cls34[st34] = cls34.get(st34, 0) + 1
        text = json.dumps(row, sort_keys=True)
        hits = sorted({m.group(0).lower() for m in KW.finditer(text)})
        R['rows'][key] = {
            'owners': paths, 'ownersIn36Delta': sorted(p for p in paths if p in DELTA),
            'ownersAllResolve36': all(p in m36 for p in paths), 'ownersBytesEqual35and36': all(m35.get(p) == m36.get(p) for p in paths),
            'subjectOwnersOn34': subj, 'subjectOwnersIn36Delta': sorted(p for p in subj if p in DELTA),
            'subjectOwnersBytesEqual35and36': all(m35.get(p) == m36.get(p) and p in m36 for p in subj),
            'statusChangeOn34': st34, 'statusChangeOn35': st35,
            'hasLegacyCorrection': bool(row.get('readingStandingLegacyCorrectionOn34')),
            'legacyStatusOn35': row.get('readingStandingLegacyCorrectionStatusOn35'),
            'keywordHits': hits,
            'appliedByThisReviewOn35': row.get('appliedByThisReview'), 'finalApplicationOutcomeGrantedOn35': row.get('finalApplicationOutcomeGranted'),
            'fieldsOn35': sorted(k for k in row if k.endswith('On35') or '34to35' in k)}
R['statusChangeOn35Counts'] = cls35
R['statusChangeOn34Counts'] = cls34
inh = cls35.get('INHERITED', 0)
pkg = cls35.get('RE-VERIFIED-ON-PACKAGE12', 0)
R['historical35ClassCheck'] = {'inherited': inh, 'package': pkg, 'crossOwner': sum(v for k, v in cls35.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12')),
                               'matches91_11_5': (inh, pkg, sum(v for k, v in cls35.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12'))) == (91, 11, 5)}
R['legacyCorrections'] = sorted(k for k, v in R['rows'].items() if v['hasLegacyCorrection'])
R['rowsWithOwnerIn36Delta'] = sorted(k for k, v in R['rows'].items() if v['ownersIn36Delta'] or v['subjectOwnersIn36Delta'])
R['rowsAllOwnersEqual35and36'] = sum(1 for v in R['rows'].values() if v['ownersBytesEqual35and36'])
R['rowsWithoutOwners'] = sorted(k for k, v in R['rows'].items() if not v['owners'])
R['crossOwnerRows35'] = sorted(k for k, v in R['rows'].items() if v['statusChangeOn35'] not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12'))
R['keywordCandidates'] = sorted(k for k, v in R['rows'].items() if v['keywordHits'])
R['baselineVerdict'] = J['verdict']
R['baselineMust'] = [m['id'] for m in J['newMustIssues']]
R['baselineShould'] = [m['id'] for m in J['newShouldIssues']]
R['baselineAdvisories'] = [a['id'] for a in J['advisories']]
R['baselineTopLevelKeys'] = sorted(J)
R['authorityFlagsFalseOn35'] = all(v['appliedByThisReviewOn35'] is False and v['finalApplicationOutcomeGrantedOn35'] is False for v in R['rows'].values())
R['crossUnitStandingOn35'] = J.get('crossUnitStanding')
R['tcb'] = {k: J['sharedAssumptionTCBSCOPE01'].get(k) for k in ('dependentRows', 'statusOn35')}
print('baseline matches: %s | verdict %s | MUST %s SHOULD %s | advisories %s' % (R['baselineMatches'], R['baselineVerdict'], R['baselineMust'], R['baselineShould'], R['baselineAdvisories']))
print('counts:', R['counts'], '| total', sum(R['counts'].values()), '| expected maps:', R['countsMatchExpected'])
print('statusChangeOn35:', cls35, '| historical 91/11/5:', R['historical35ClassCheck']['matches91_11_5'])
print('legacy corrections (%d):' % len(R['legacyCorrections']), R['legacyCorrections'])
print('rows with any owner / subject owner in the 36 delta:', R['rowsWithOwnerIn36Delta'])
print('rows whose owners are all byte-equal 35/36: %d | rows without owner paths: %s' % (R['rowsAllOwnersEqual35and36'], R['rowsWithoutOwners']))
print('cross-owner rows on 35:', R['crossOwnerRows35'])
print('authority flags false on every 35 row:', R['authorityFlagsFalseOn35'])
print('TCB dependents:', len(R['tcb']['dependentRows'] or []))
print('\nkeyword candidates (%d):' % len(R['keywordCandidates']))
for k in R['keywordCandidates']:
    print('  %-52s %s' % (k, R['rows'][k]['keywordHits']))
json.dump(R, open(os.path.join(OUT, 'r08-rows.json'), 'w'), indent=1, default=str)
print('wrote r08-rows.json')
