import json, collections
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/docs/coop/design-corrections/'
R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
O = open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p16b_out.txt', 'w')
def P(*a): print(*a, file=O)
dr = json.load(open(R + 'claude-independent-design.v45/review.json'))
def t(x, n=700):
    s = x if isinstance(x, str) else json.dumps(x)
    return s if len(s) <= n else s[:n] + '...'
ev = json.load(open(S + 'evaluation-residual-dispositions.applied.v1.json'))
dmap = {x['id']: x for x in dr['evaluationResidualDispositions']}
P('##### EVALUATION 30')
for it in ev['items']:
    d = it['independentDisposition']
    P('==', it['id'], '| status', it.get('reviewStatus'), '| design', d['disposition'], '| sharedDependency', d.get('sharedDependency'), '| authorGrade', d.get('authorGrade'), '| literal==review', d == dmap[it['id']], '| keys', sorted(it.keys()))
    P('   original:', t(it.get('original') or it.get('text') or it.get('residual'), 500))
    P('   proposed:', t(it.get('proposedDisposition'), 200), '| correction:', t(it.get('correction'), 700))
    P('   designAssessment:', t(d['currentAssessment'], 700))
P('sharedDependency rows', [x['id'] for x in dr['evaluationResidualDispositions'] if x.get('sharedDependency') == 'TCB-SCOPE-01'])
ir = json.load(open(S + 'inherited-residuals.applied.v1.json'))
imap = {x['id']: x for x in dr['inheritedResidualDispositions']}
P('##### INHERITED lists', [(k, len(ir[k])) for k in ir if isinstance(ir[k], list)])
for k in [k for k in ir if isinstance(ir[k], list)]:
    for it in ir[k]:
        d = it['independentDisposition']
        P('==', it['id'], '| grade', it.get('designGrade'), '| design', d['disposition'], '| literal==review', d == imap[it['id']], '| carried', 'carriedCrossUnitObligation' in it)
        P('   text:', t(it.get('dispositionText'), 900))
        P('   design:', t(d['currentAssessment'], 600), '| consequence', d.get('consequence'))
        extra = sorted(set(it) - {'id', 'dispositionText', 'source', 'designGrade', 'effectiveWhen', 'independentDisposition', 'gradeAuthority', 'finalApplicationReviewBinding', 'reviewEvidence', 'carriedCrossUnitObligation'})
        if extra: P('   EXTRA', extra, t({e: it[e] for e in extra}, 1200))
P({k: t(v, 400) for k, v in ir.items() if not isinstance(v, list)})
cw = json.load(open(S + 'correction-crosswalk.applied.v1.json'))
amap = {x['id']: x for x in dr['arDispositions']}
P('##### AR 16')
for it in cw['items']:
    d = it['independentDisposition']
    P('==', it['id'], it['obligation'], '|', it['contract'].split('/')[-1], it['selector'], '| owners', it['ownerRows'], '| design', d['disposition'], '| statusRecorded', d.get('statusRecorded'), '| literal==review', d == amap[it['id']], '| app', it['applicationDisposition'])
    P('   sourceItem', t(it['sourceItem'], 500))
    P('   design:', t(d['currentAssessment'], 500))
fmap = {x['id']: x for x in dr['fwDispositions']}
P('FW literal==review', all(cw['fallowDispositions'][k] == fmap[k] for k in fmap), len(fmap))
P('scoped owner literal==review', [x == {k: v for k, v in y.items()} for x, y in zip(dr['scopedReviewOwnerDispositions'], [{k: v for k, v in r.items() if k in dr['scopedReviewOwnerDispositions'][0]} for r in json.load(open(S + 'review-owner-dispositions.v1.json'))['records']])])
P('##### F dispositions')
for x in dr['fDispositions']:
    P('-', x['id'], x['disposition'], '| basis', x['assessmentBasis'], '| priorRoot', x.get('priorRootStanding'), '| owner', x.get('currentOwner'), '| applied', x.get('appliedByThisReview'), x.get('finalApplicationOutcomeGranted'))
    P('   ', t(x['currentAssessment'], 600))
P('##### retained', json.dumps(dr['retained'], indent=1))
P('##### readScope counts', dr['readScope']['counts'])
P('##### itemDispositions'); [P('-', x['id'], x['disposition']) for x in dr['itemDispositions']]
P('##### priorFindingDispositions'); [P('-', x['id'], x.get('currentDisposition')) for x in dr['priorFindingDispositions']]
P('##### observations'); [P('-', x['id'], t(x['text'], 1600)) for x in dr['observations']]
O.close()
