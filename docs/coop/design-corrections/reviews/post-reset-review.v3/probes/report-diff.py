import json,hashlib,os
S='/tmp/opensip-design-corrections/candidate-subject.v3/docs/coop/design-corrections'
R='/tmp/opensip-design-corrections/post-reset-review.v3/reports'
SC='/tmp/opensip-design-corrections/post-reset-review.v3/scratch/docs/coop/design-corrections'
pairs=[('foundation/foundation-report.json',R+'/foundation-reports/foundation-report.json'),
('foundation/identity-report.json',R+'/foundation-reports/identity-report.json'),
('foundation/product-quality-report.json',R+'/foundation-reports/product-quality-report.json'),
('foundation/product-configuration-report.json',R+'/foundation-reports/product-configuration-report.json'),
('security/security-lifecycle-report.v1.json',R+'/security-lifecycle-report.rerun.json'),
('native/native-evidence-report.v2.json',R+'/native-evidence-report.rerun.json'),
('workflows/workflows-report.v1.json',R+'/workflows-report.rerun.json'),
('integration-report.v1.json',R+'/integration-report.rerun.json')]
out=[]
def h(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
for a,b in pairs:
    ra=h(os.path.join(S,a)); rb=h(b)
    out.append({'retained':a,'retainedSha256':ra,'rerun':os.path.relpath(b,'/tmp/opensip-design-corrections/post-reset-review.v3'),'rerunSha256':rb,'identical':ra==rb})
    if ra!=rb:
        A=json.load(open(os.path.join(S,a)));B=json.load(open(b))
        diffs=[k for k in set(A)|set(B) if A.get(k)!=B.get(k)]
        out[-1]['differingTopLevelKeys']=diffs
# counts
fl=json.load(open(R+'/foundation-launcher.json'))
counts={}
for c in fl['checks']:
    rep=json.load(open(R+'/foundation-reports/'+{'check-foundation.py':'foundation-report.json','check-identity.py':'identity-report.json','check-product-quality.py':'product-quality-report.json','check-product-configuration.py':'product-configuration-report.json'}[c['script']]))
    counts[c['script']]={k:v for k,v in rep.items() if k in('passed','failed','total','checks','summary','counts')} 
    counts[c['script']]['exit']=c['exitCode']
sec=json.load(open(R+'/security-lifecycle-report.rerun.json'))
nat=json.load(open(R+'/native-evidence-report.rerun.json'))
wf=json.load(open(R+'/workflows-launcher.json'))
wfr=json.load(open(R+'/workflows-report.rerun.json'))
wfv=json.load(open(SC+'/workflows/workflows-validation-report.json'))
integ=json.load(open(R+'/integration-report.rerun.json'))
summary={'foundation':counts,'foundationPins':fl['sourceFileCount'],'security':{'counts':sec.get('counts'),'sweeps':len(sec.get('sweeps',[])),'pins':sec.get('pins',{}).get('verified') if isinstance(sec.get('pins'),dict) else sec.get('sourcePinsValid'),'schemasValidated':sec.get('outputSchemasValidated') or sec.get('schemasValidated')},
'native':{'cases':nat.get('cases'),'matrix':nat.get('matrix'),'pins':nat.get('pins',{}).get('verified'),'result':nat.get('result')},
'workflows':{'launcherPassed':wf['passed'],'pins':wf['sourceFileCount'],'report':{k:v for k,v in wfr.items() if k in('checks','passed','failed','counts','schemas','total')},'validation':wfv},
'integration':{'passed':integ['passed'],'failed':integ['failed']},
'reportDiff':out}
print(json.dumps(summary,indent=1,default=str)[:6000])
json.dump(summary,open(R+'/report-diff.json','w'),indent=1,default=str)
