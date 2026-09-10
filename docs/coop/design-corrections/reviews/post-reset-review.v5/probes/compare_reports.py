import hashlib,os,json
SUB='/tmp/opensip-design-corrections/candidate-subject.v5/docs/coop/design-corrections'
R='/tmp/opensip-design-corrections/post-reset-review.v5/reports'
def h(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
pairs=[
 ('foundation/validation-report.json',R+'/foundation-launcher.json'),
 ('foundation/reports/foundation-report.json',R+'/foundation-reports/foundation-report.json'),
 ('foundation/reports/identity-report.json',R+'/foundation-reports/identity-report.json'),
 ('foundation/reports/product-configuration-report.json',R+'/foundation-reports/product-configuration-report.json'),
 ('foundation/reports/product-quality-report.json',R+'/foundation-reports/product-quality-report.json'),
 ('security/security-lifecycle-report.v1.json',R+'/security-lifecycle-report.rerun.json'),
 ('native/native-evidence-report.v2.json',R+'/native-evidence-report.rerun.json'),
 ('workflows/workflows-validation-report.json',R+'/workflows-launcher.json'),
 ('workflows/workflows-report.v1.json',R+'/workflows-report.rerun.json'),
 ('integration-report.v1.json',R+'/integration-report.rerun.json'),
]
out=[];ok=0
for rel,mine in pairs:
    sp=os.path.join(SUB,rel)
    e=os.path.exists(sp) and os.path.exists(mine)
    if not e: out.append({'report':rel,'status':'MISSING','subjectExists':os.path.exists(sp),'rerunExists':os.path.exists(mine)});continue
    a,b=h(sp),h(mine)
    same=a==b; ok+=same
    out.append({'report':rel,'identical':same,'subjectSha256':a,'rerunSha256':b})
print(json.dumps(out,indent=1))
print('IDENTICAL',ok,'of',len(pairs))
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/report-comparison.json','w'),indent=1)
