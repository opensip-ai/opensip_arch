"""Current joint evidence dispositions; no historical obligation is silently closed."""
from pathlib import Path
import copy,hashlib,json,types
HERE=Path(__file__).resolve().parent
p=HERE/'check_model_carriers.py';V=types.ModuleType('v');V.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),V.__dict__)
raw=V.read_unit('report-projection','owner/design-obligations.v1.json');value=json.loads(raw)
value['schemaVersion']=2
value['standing']='Joint09 root evidence dispositions; unaccepted candidates do not close reviewed-owner or product-delivery criteria. Historical register remains unchanged.'
value['readiness']['carrierUnit']='Composed reference candidate in progress; actual review and final source succession pending'
value['readiness']['reportDesign']='not-approved: actual owner review, new-Plan native/identity binding and L02 policy disposition remain open'
value['jointParentSha256']=hashlib.sha256(raw).hexdigest()
map={
 'RP-DO-01':('presentation-catalog02','catalogue-source-result.json','Closed receipts, complete synthetic catalogue report, visible registry/key/singular authority joins'),
 'RP-DO-03':('report-evidence-design02','feature-integration-result.json','Coupling counts/anchor membership and dense shared-byte projection; whole-view query remains an internal reference owner'),
 'RP-DO-04':('config-disclosure02','document-result.json','Exact retained Plan configuration blob projected by unchanged redaction owner in complete report'),
 'RP-DO-05':('report-evidence-design02','identity-integration-result.json','Optional parameter registry and T1 composed; actual reference retained/new Run closure passes. Selected v3 pre-Plan registry and origin-dependent public refusal now composed; real host Plan construction remains pending'),
 'RP-DO-06':('presentation-catalog02','catalogue-source-result.json','Complete recipe description report joins exact preview RecipeRef and RepairPlanId; authenticated source custody remains a premise'),
 'RP-DO-07':('presentation-catalog02','catalogue-source-result.json','Existing selected-profile evidenceSource/targets descriptions and target bounds carried; no arbitrary recipe arguments invented'),
 'RP-DO-08':('presentation-catalog02','catalogue-source-result.json','Rule description keys cross-check visible effective policy; selected source/declaration custody remains host-owned'),
 'RP-DO-09':('report-evidence-design02','feature-integration-result.json','Five owned static graph count interpretations with exact/lower-bound/unknown disclosures; this interpretation still requires actual review'),
 'RP-DO-10':('report-evidence-design02','feature-integration-result.json','Static test-origin reach paths retain cross-universe limitations and configured-Jest incompleteness; no execution-coverage claim'),
 'RP-DO-11':('workflow-timing02','workflow5-result.json','Invocation5 retains the exact timing4 attempt law; reference clock samples and whole-report service sums tested'),
 'RP-DO-12':('history-selection02','metadata-result.json','Typed query4 run.show, inventory6 eight selectors, exact static selection and retained prior Run under an in-memory lease tested; real store snapshot remains implementation work')}
for row in value['obligations']:
 if row['id'] not in map:continue
 unit,evidence,summary=map[row['id']]
 row['status']='composed-reference-pending-owner-review-and-source-selection'
 row['jointEvidence']={'ownerCandidate':unit,'result':evidence,'summary':summary,'productDelivered':False,'actualJointReview':False}
 row['standing']='Original closure criterion retained; candidate tests do not confer owner acceptance, source selection or product delivery.'
for row in value['integrationObligations']:
 if row['id']=='RP-OBL-L02':
  row['jointEvidence']={'candidate':'composed-owners/d9-exit-contract.proposed.v1.15.json','result':'output-integration-result.json','standing':'Unaccepted capacity-failure alternative. The original preflight-or-complete-profile criterion is not met by this proposal. Actual review must explicitly assess the replacement criterion; never mark the original criterion satisfied.'}
 if row['id'] in ['RP-OBL-C01','RP-OBL-C02']:
  row['jointEvidence']={'result':'workflow5-result.json','planning':'planning-result.json','standing':'Actual reference replay/composite and all12 planning variants pass under invocation5/envelope7. Full host custody and actual joint review remain pending.'}
value['jointAdditionalFindings']=[
 {'id':'Q-FIT-1','status':'reference-composed-review-pending','evidence':['planning-result.json','workflow5-result.json','fit-document-result.json'],'remaining':['Actual joint review','Host exact source query and completed response custody','Public CLI/renderer integration']},
 {'id':'RP-EV-INT-IDENTITY','status':'reference-composed-review-pending','evidence':['identity-composition-result.json','identity-integration-result.json','new-plan-result.json'],'remaining':['Actual review of the appended new-Plan duty and its one new public detail','Select the new native/common/public-detail sources together','Real host input retention, Plan construction and private source bindings']},
 {'id':'REPORT-CODEC-PROFILE','status':'separate-codec-candidate-implemented-review-pending','evidence':['joint-budget-derivation.json','joint-depth-derivation.json'],'remaining':['Rebase separate fixed Rust/TS report codec candidate onto current provenance, obtain actual review and integrate selected product APIs','Native and browser boundary/performance qualification']}
]
(HERE/'joint-obligations.json').write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({'designObligations':len(value['obligations']),'integrationObligations':len(value['integrationObligations']),'acceptedByThisUpdate':0}))
