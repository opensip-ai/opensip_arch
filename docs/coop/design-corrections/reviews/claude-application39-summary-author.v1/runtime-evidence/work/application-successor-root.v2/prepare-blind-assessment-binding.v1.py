from pathlib import Path
import hashlib,json,shutil,ast
b=Path(__file__).parent;p=b/'assemble-records.py';s=p.read_text();dest=b/'blind-assessment-binding-before.v1';assert not dest.exists();dest.mkdir();shutil.copyfile(p,dest/p.name)
needle="blind_response=load(dc+f'reviews/consumer-b.{bv}/output/response.json');assert blind_response.get('is_error') is False\n"
assert s.count(needle)==1
addition="""# A successful blind headline does not establish that its independently built graphs work.
# Require the actual root's full substantive assessment of the exact completed blind evidence.
blind_assessment_ref=ref(dc+f'reviews/codex-post-reset.v1/blind-assessment.{bv}.json')
blind_assessment=load(blind_assessment_ref['path'])
assert blind_assessment['rootBlindAssent'] is True and blind_assessment['fullRead'] is True
assert blind_assessment['actualSessionId']==blind_response['session_id']
assert blind_assessment['parentSubjectSha256']==manifest_ref['sha256']
assert all(blind_assessment['review'][k]==blind_ref[k] for k in ('path','sha256'))
assert all(type(blind_assessment.get(k)) is list and not blind_assessment[k] for k in ('unresolvedRootMustIssues','unresolvedRootShouldIssues'))
blind_new_advisories=blind.get('newAdvisories',blind.get('advisories',[]))
assert type(blind_new_advisories) is list
blind_advisory_account=blind_assessment['newAdvisoryApplicationAccount']
assert type(blind_advisory_account) is list
assert len({x['id'] for x in blind_advisory_account})==len(blind_advisory_account)
assert {x['id'] for x in blind_advisory_account}=={x['id'] for x in blind_new_advisories}
"""
s=s.replace(needle,needle+addition)
needle="'independentReviewFindings':design['newAdvisories'],'bindingImplementationGates'"
assert s.count(needle)==1
s=s.replace(needle,"'independentReviewFindings':design['newAdvisories'],'freshBlindReview':blind_ref,'codexBlindAssessment':blind_assessment_ref,'blindItems':blind_advisory_account,'independentBlindReviewFindings':blind_new_advisories,'bindingImplementationGates'")
needle="'freshBlindConsumerReview':blind_ref,'blindInputManifest':blind_input_ref"
assert s.count(needle)==1;s=s.replace(needle,"'freshBlindConsumerReview':blind_ref,'codexBlindAssessment':blind_assessment_ref,'blindInputManifest':blind_input_ref")
ast.parse(s);p.write_text(s)
# Retain the preparation and before-image in the future application package for fresh review.
pv=b/'prepare-validation.py';v=pv.read_text();shutil.copyfile(pv,dest/pv.name)
needle="finalizer=files/(dc+'finalize-application.v1.py')"
assert v.count(needle)==1
v=v.replace(needle,"""for name in ['prepare-blind-assessment-binding.v1.py','blind-assessment-binding.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copytree(Path(__file__).with_name('blind-assessment-binding-before.v1'),support/'blind-assessment-binding-before.v1')
"""+needle);ast.parse(v);pv.write_text(v)
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
(b/'blind-assessment-binding.v1.json').write_text(json.dumps({'standing':'Prepared application-only assembly guard and advisory evidence routing. No application assembled, accepted or activated. No accepted semantic source modified. Fresh full application reviewer must assess these exact tools.','reason':'Require actual root substantive assent to exact blind evidence and explicitly account all newly reported blind advisories.','changes':[{'path':q.name,'beforeSha256':sha(dest/q.name),'afterSha256':sha(q)} for q in [p,pv]],'validation':'Python AST parses. Actual positive assembly awaits completed blind and root substantive assessment; no fabricated accepted record supplied.'},indent=2)+'\n')
print('Prepared root blind assessment binding and complete blind advisory routing; no stage assembled.')
