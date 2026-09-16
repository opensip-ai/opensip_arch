"""R08 — carry-forward audit of the COMPLETE source34 baseline for source35.
  * owner arrays 34->35 derived from the two manifests (not prose)
  * the source34 classes (91 inherited / 11 F package / 5 cross-owner) and nine legacy corrections, re-verified
    from the baseline itself
  * which rows' owners, or subject owners named in the baseline, touch the 10-file delta"""
import hashlib, json, os

B34 = '/tmp/opensip-design-corrections/claude-independent-design.v34'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
J = json.load(open(os.path.join(B34, 'review.json')))
r00 = json.load(open(os.path.join(OUT, 'r00-custody.json')))
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
m34 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
DELTA = {c['path'] for c in r00['delta']['changed']}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
R = {'rows': {}, 'counts': {mp: len(J[mp]) for mp in MAPS}}
cls = {}
for mp in MAPS:
    for rid, row in J[mp].items():
        key = mp + '/' + rid
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = sorted({o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)})
        subj = row.get('subjectOwnerFilesOn34') or []
        st = row.get('statusChangeOn34')
        cls[st] = cls.get(st, 0) + 1
        R['rows'][key] = {'owners': paths, 'ownersIn35Delta': sorted(p for p in paths if p in DELTA),
                          'ownersAllResolve35': all(p in m35 for p in paths), 'ownersBytesEqual34and35': all(m34.get(p) == m35.get(p) for p in paths),
                          'subjectOwnersOn34': subj, 'subjectOwnersIn35Delta': sorted(p for p in subj if p in DELTA),
                          'statusChangeOn34': st, 'hasLegacyCorrection': bool(row.get('readingStandingLegacyCorrectionOn34')),
                          'appliedByThisReview': row.get('appliedByThisReview'), 'finalApplicationOutcomeGranted': row.get('finalApplicationOutcomeGranted')}
R['statusChangeOn34Counts'] = cls
inh = cls.get('INHERITED', 0)
R['baselineClassCheck'] = {'inherited': inh, 'package': cls.get('RE-VERIFIED-ON-PACKAGE11', 0),
                           'crossOwner': sum(v for k, v in cls.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE11')),
                           'matches91_11_5': (inh, cls.get('RE-VERIFIED-ON-PACKAGE11', 0),
                                              sum(v for k, v in cls.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE11'))) == (91, 11, 5)}
R['legacyCorrections'] = sorted(k for k, v in R['rows'].items() if v['hasLegacyCorrection'])
R['rowsWithOwnerIn35Delta'] = sorted(k for k, v in R['rows'].items() if v['ownersIn35Delta'] or v['subjectOwnersIn35Delta'])
R['rowsAllOwnersEqual34and35'] = sum(1 for v in R['rows'].values() if v['ownersBytesEqual34and35'])
R['crossOwnerRows34'] = sorted(k for k, v in R['rows'].items() if v['statusChangeOn34'] not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE11'))
R['baselineMust'] = [m['id'] for m in J['newMustIssues']]
R['baselineAdvisories'] = [a['id'] for a in J['advisories']]
print('counts:', R['counts'], '| total', sum(R['counts'].values()))
print('statusChangeOn34:', cls, '| 91/11/5:', R['baselineClassCheck']['matches91_11_5'])
print('legacy corrections (%d):' % len(R['legacyCorrections']), R['legacyCorrections'])
print('rows with any owner in the 35 delta:', R['rowsWithOwnerIn35Delta'])
print('rows whose owners are all byte-equal 34/35:', R['rowsAllOwnersEqual34and35'])
print('cross-owner rows on 34:', R['crossOwnerRows34'], '| baseline MUST', R['baselineMust'], '| advisories', R['baselineAdvisories'])
print('authority flags false everywhere:', all(v['appliedByThisReview'] is False and v['finalApplicationOutcomeGranted'] is False for v in R['rows'].values()))
json.dump(R, open(os.path.join(OUT, 'r08-rows.json'), 'w'), indent=1, default=str)
print('wrote r08-rows.json')
