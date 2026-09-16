"""Apply the explicit root L02 choice; final source/implementation stay pending."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
def apply(value):
 decision=json.loads((H/'L02-policy-selection.json').read_bytes())
 pin=decision['review'];raw=Path(pin['path']).read_bytes()
 assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
 review=json.loads(raw)
 assert review['sourceAndProfileAssessment']['L02']['acceptableAsExplicitAlternative'] is True
 assert review['subjectManifestSha256']==decision['reviewSubjectManifestSha256']
 assert hashlib.sha256((H/decision['D9Candidate']['path']).read_bytes()).hexdigest()==decision['D9Candidate']['sha256']
 row=next(r for r in value['integrationObligations'] if r['id']=='RP-OBL-L02')
 assert row['closureCriterion']==decision['originalClosureCriterion']
 row['originalClosureCriterion']=row['closureCriterion']
 row['originalCriterionDisposition']='Superseded by explicit root policy selection after substantive actual Grok combined review; not met or retroactively claimed satisfied.'
 row['closureCriterion']=decision['selectedClosureCriterion']
 row['status']='policy-selected-pending-source-binding'
 row['jointEvidence']['standing']='Root selects the explicit capacity-failure alternative on the substantive Grok joint10 review. Old stronger criterion remains recorded as superseded, not met. Final source binding and product implementation remain pending.'
 row['rootPolicySelection']='L02-policy-selection.md'
 assert row['blocksM1FinalIntegration'] is True
 value['standing']='Joint11 successor in preparation. Root selects L02 policy on actual Grok combined-reference evidence; exact source binding, original unit review duties and product delivery remain pending.'
 value['readiness']['reportDesign']='not-approved: original unit review and final source/version binding remain open; L02 policy is selected, not implemented'
 return value
