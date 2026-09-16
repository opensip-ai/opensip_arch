import json, collections
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/docs/coop/design-corrections/'
R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
dr = json.load(open(R + 'claude-independent-design.v45/review.json'))
def t(x, n=700):
    s = x if isinstance(x, str) else json.dumps(x)
    return s if len(s) <= n else s[:n] + '...'
print('##### DESIGN REVIEW limitations'); [print('-', t(x, 1500)) for x in dr['limitations']]
print('##### DESIGN REVIEW observations'); [print('-', x['id'], t(x['text'], 900)) for x in dr['observations']]
print('##### DESIGN REVIEW advisories'); [print('-', x['id'], t(x['title'], 400), '|', t(x.get('disposition'), 400)) for x in dr['advisories']]
print('##### DESIGN verdictBasis', dr['verdictBasis'])
print('##### priorFindingDispositions'); [print('-', x['id'], x.get('currentDisposition')) for x in dr['priorFindingDispositions']]
print('##### itemDispositions'); [print('-', x['id'], x['disposition']) for x in dr['itemDispositions']]
print('##### F dispositions')
for x in dr['fDispositions']:
    print('-', x['id'], x['disposition'], '|', t(x['currentAssessment'], 900), '| priorRoot', x.get('priorRootStanding'), '| owner', x.get('currentOwner'))
print('##### retained', json.dumps(dr['retained'], indent=1)[:6000])
print('##### readScope counts', dr['readScope']['counts'])
print('##### sharedAssumption substantive'); [print('-', x) for x in dr['sharedAssumptionTCBSCOPE01']['substantiveCurrentAssessment']]
ev = json.load(open(S + 'evaluation-residual-dispositions.applied.v1.json'))
print('##### EVALUATION 30')
dmap = {x['id']: x for x in dr['evaluationResidualDispositions']}
for it in ev['items']:
    d = it['independentDisposition']
    print('==', it['id'], '| status', it['reviewStatus'], '| design', d['disposition'], '| sharedDependency', d.get('sharedDependency'), '| authorGrade', d.get('authorGrade'), '| literal==review', d == dmap[it['id']])
    print('   original:', t(it['original'], 900))
    print('   correction:', t(it['correction'], 900))
    print('   designAssessment:', t(d['currentAssessment'], 900))
tcb = [x['id'] for x in dr['evaluationResidualDispositions'] if x.get('sharedDependency')]
print('rows with sharedDependency in design review', tcb, collections.Counter(str(x.get('sharedDependency')) for x in dr['evaluationResidualDispositions']))
ir = json.load(open(S + 'inherited-residuals.applied.v1.json'))
print('##### INHERITED keys', [k for k in ir if isinstance(ir[k], list)])
imap = {x['id']: x for x in dr['inheritedResidualDispositions']}
for k in [k for k in ir if isinstance(ir[k], list)]:
    for it in ir[k]:
        d = it['independentDisposition']
        print('==', it['id'], '| grade', it.get('designGrade'), '| design', d['disposition'], '| literal==review', d == imap[it['id']], '| carried', 'carriedCrossUnitObligation' in it)
        print('   text:', t(it['dispositionText'], 1000))
        print('   design:', t(d['currentAssessment'], 700), '| consequence', d.get('consequence'))
        extra = sorted(set(it) - {'id', 'dispositionText', 'source', 'designGrade', 'effectiveWhen', 'independentDisposition', 'gradeAuthority', 'finalApplicationReviewBinding', 'reviewEvidence', 'carriedCrossUnitObligation'})
        if extra: print('   EXTRA', extra, t({e: it[e] for e in extra}, 1500))
print({k: t(v, 300) for k, v in ir.items() if not isinstance(v, list)})
cw = json.load(open(S + 'correction-crosswalk.applied.v1.json'))
amap = {x['id']: x for x in dr['arDispositions']}
print('##### AR 16')
for it in cw['items']:
    d = it['independentDisposition']
    print('==', it['id'], it['obligation'], '|', it['contract'].split('/')[-1], it['selector'], '| owners', it['ownerRows'], '| design', d['disposition'], '| statusRecorded', d.get('statusRecorded'), '| literal==review', d == amap[it['id']], '| app', it['applicationDisposition'])
    print('   sourceItem', t(it['sourceItem'], 600))
    print('   design:', t(d['currentAssessment'], 600))
    print('   refs', t(it['referenceEvidence'], 600))
fmap = {x['id']: x for x in dr['fwDispositions']}
print('FW literal==review', all(cw['fallowDispositions'][k] == fmap[k] for k in fmap), len(fmap))
print('scoped owner literal==review', [x == y for x, y in zip(json.load(open(S + 'review-owner-dispositions.v1.json'))['records'], dr['scopedReviewOwnerDispositions'])])
