import hashlib,os,json
SUB='/tmp/opensip-design-corrections/candidate-subject.v5/docs/coop/design-corrections'
V4=SUB+'/reviews/post-reset-review.v4/reports'
R='/tmp/opensip-design-corrections/post-reset-review.v5/reports'
def h(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
pairs=[
 ('foundation/validation-report.json',R+'/foundation-launcher.json',V4+'/foundation-launcher.json'),
 ('foundation/foundation-report.json',R+'/foundation-reports/foundation-report.json',V4+'/foundation-reports/foundation-report.json'),
 ('foundation/identity-report.json',R+'/foundation-reports/identity-report.json',V4+'/foundation-reports/identity-report.json'),
 ('foundation/product-configuration-report.json',R+'/foundation-reports/product-configuration-report.json',V4+'/foundation-reports/product-configuration-report.json'),
 ('foundation/product-quality-report.json',R+'/foundation-reports/product-quality-report.json',V4+'/foundation-reports/product-quality-report.json'),
 ('security/security-lifecycle-report.v1.json',R+'/security-lifecycle-report.rerun.json',V4+'/security-lifecycle-report.rerun.json'),
 ('native/native-evidence-report.v2.json',R+'/native-evidence-report.rerun.json',V4+'/native-evidence-report.rerun.json'),
 ('workflows/workflows-validation-report.json',R+'/workflows-launcher.json',V4+'/workflows-launcher.json'),
 ('workflows/workflows-report.v1.json',R+'/workflows-report.rerun.json',V4+'/workflows-report.rerun.json'),
 ('integration-report.v1.json',R+'/integration-report.rerun.json',V4+'/integration-report.rerun.json'),
]
out=[];ok=0
for rel,mine,v4 in pairs:
    sp=os.path.join(SUB,rel)
    a,b=h(sp),h(mine); c=h(v4) if os.path.exists(v4) else None
    same=a==b; ok+=same
    out.append({'report':rel,'reproducedIdentical':same,'sha256':a,'v4RerunSha256':c,'sameAsV4Rerun':c==a})
print(json.dumps(out,indent=1))
print('REPRODUCED IDENTICAL',ok,'of',len(pairs))
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/report-comparison-final.json','w'),indent=1)
