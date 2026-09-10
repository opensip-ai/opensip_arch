"""Record measured successor results after checks without changing ANY pinned input."""
from pathlib import Path
import hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((dc/rel).read_text())
pins={}
for unit,name,key in [('foundation','source-pins.v1.json','files'),('security','source-pins.v1.json','pins'),('native','source-pins.v2.json','pins'),('workflows','source-pins.v1.json','files')]:
    for row in read(unit+'/'+name)[key]:
        assert sha(root/row['path'])==row['sha256'],row['path']
        pins[row['path']]=row['sha256']
a=read('reviews/codex-post-reset.v1/successor-source-assessment.v20.json')
assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
f=read('foundation/validation-report.json');s=read('security/security-lifecycle-report.v1.json')
n=read('native/native-evidence-report.v2.json');w=read('workflows/workflows-validation-report.json')
wi=read('workflows/workflows-report.v1.json');i=read('integration-report.v1.json')
assert f['passed'] and s['passed'] and n['result']=='PASS' and w['passed'] and not i['failed']
executed=Path('/tmp/opensip-design-corrections/final-reference-v20-complete/reference-checks.json')
assert json.loads(executed.read_text())['passed']
matrix=read('native/native-capability-matrix.v2.json')
assert len(matrix['cells'])==n['matrix']['cells']==66 and n['matrix']['qualifiedCells']==0
identity=read('foundation/identity-report.json');ids={}
for row in identity['checks']:ids.setdefault(row['id'],[]).append(row['passed'])
assert all(all(v) for v in ids.values())
account={'standing':'Measured passing check calls and distinct IDs; neither is exhaustive coverage, independent acceptance or product qualification. Historical duplicate IDs are preserved.',
    'sourceReport':'docs/coop/design-corrections/foundation/identity-report.json',
    'sourceReportSha256':sha(dc/'foundation/identity-report.json'),
    'passingCalls':identity['passed'],'distinctIds':len(ids),
    'duplicateExtraInstances':sum(len(v)-1 for v in ids.values()),
    'duplicates':{k:{'instances':len(v),'allPass':all(v)} for k,v in sorted(ids.items()) if len(v)>1}}
ap=ev/'identity-check-counts.v20.json';assert not ap.exists();ap.write_text(json.dumps(account,indent=2)+'\n')
counts={name:read('foundation/'+name+'-report.json')['passed'] for name in ['foundation','identity','product-quality','product-configuration']}
orders=read('foundation/array-order-report.json');assert orders['passed'];counts['array-order']=sum(row['passed'] for row in orders['checks'])
summary=read('validation-summary.v1.json')
summary['foundation'].update(checksPassed=sum(counts.values()),sourcePinsVerified=f['sourceFileCount'],components=counts,
    identityCountAccount={'path':'reviews/codex-post-reset.v1/identity-check-counts.v20.json','sha256':sha(ap),
    'passingCalls':account['passingCalls'],'distinctIds':account['distinctIds'],'duplicateExtraInstances':account['duplicateExtraInstances']})
summary['security'].update(casesPassed=s['counts']['pass'],invariantSweepsPassed=len(s['sweeps']))
summary['native'].update(casesPassed=n['cases']['passed'],matrixCells=n['matrix']['cells'],qualifiedCells=n['matrix']['qualifiedCells']);summary['workflows']['checksPassed']=wi['passed'];summary['integration']['checksPassed']=i['passed']
summary['claudePriorReview']='reviews/post-reset-review.v19/review.json'
summary['claudeFinalReview']='PENDING-FROZEN-V20'
summary.pop('claudeEffectivePriorReview', None)
summary['priorReviewLimitation']='Independent19 ACCEPT and root source assent apply only to frozen19. Historical blind8 returned CHANGES_REQUIRED with qualified reconstruction evidence; source20 corrects required gaps and associated route/schema publication defects. Fresh independent20, NEWblind9 and complete independently reviewed application remain required. No earlier acceptance covers changed bytes.'
summary['latestCompletedBlindReview']='reviews/consumer-b.v8/output/blind-review.json'
summary.pop('latestBlindClarification',None)
(dc/'validation-summary.v1.json').write_text(json.dumps(summary,indent=2)+'\n')
d=read('post-reset-dispositions.v20.proposed.json');d['standing']='PROPOSED completed v20 coauthor correction with measured final reference results; fresh independent review, NEW blind and complete application remain required'
d['finalReferenceEvidence']={'path':'reviews/codex-post-reset.v1/final-reference.v20/reference-checks.json','standing':'Executed source-pinned commands, not independent acceptance.'}
d['identityCountAccount']='reviews/codex-post-reset.v1/identity-check-counts.v20.json'
d['finalPinSeal']='Separate final AFTER-ALL-RECORDING live and copied pin checks remain mandatory'
(dc/'post-reset-dispositions.v20.proposed.json').write_text(json.dumps(d,indent=2)+'\n')
h=read('historical-preservation-report.v19.json')
for row in h['files']:
    row['currentSha256']=sha(root/row['path']);row['unchanged']=row['currentSha256']==row['openingSha256']
h['unchanged']=sum(row['unchanged'] for row in h['files']);h['changed']=[row['path'] for row in h['files'] if not row['unchanged']]
assert not h['changed'];hp=dc/'historical-preservation-report.v20.json';assert not hp.exists();hp.write_text(json.dumps(h,indent=2)+'\n')
assert all(sha(root/rel)==digest for rel,digest in pins.items()),'Recording changed a pinned source; do not freeze'
print(json.dumps({'foundation':counts,'identityCounts':{k:account[k] for k in ('passingCalls','distinctIds','duplicateExtraInstances')},'native':n['cases']['passed'],'workflows':wi['passed'],'integration':i['passed'],'historicalUnchanged':h['unchanged']}))
