from pathlib import Path
import hashlib,json,shutil
A=Path('/Users/sb/code/opensip-ai/opensip_arch');B=Path('/tmp/opensip-implementation');P=B/'m1-final-source-selection-candidate-02';D=A/'docs/implementation/m1/source-selection-v2';D.mkdir(exist_ok=False)
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)) if p.is_relative_to(A) else str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def copy(src,rel):
 dst=D/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);return pin(dst)
source=json.loads((P/'source-map.proposed.json').read_bytes());rows=[]
for r in source['sources']:
 dst=copy(P/r['implementationPath'],r['implementationPath']);rows.append({k:r[k] for k in ['schemaId','implementationPath','declaredMajor','semanticValidatorOwner','profile']}|{'architectureSource':dst})
save(D/'source-map.json',{'schemaVersion':1,'sources':rows})
save(D/'semantic-owner-joins.json',{'standing':'Proposed semantic-owner allocation; not implemented or source accepted','rows':[{k:r[k] for k in ['schemaId','semanticValidatorOwner','requiredOwnerJoins'] if k in r} for r in source['sources']]})
for p in sorted((P/'reference').rglob('*')):
 if p.is_file():copy(p,'reference/'+str(p.relative_to(P/'reference')))
contracts=[('evidence','m1-report-evidence-design-subject-02',['contract.md']),('catalogue','m1-presentation-catalog-subject-02',['contract.md']),('history','m1-history-selection-subject-03',['contract.md','history-command-flags.json']),('fit','m1-fit-interruption-subject-01',['contract.md']),('required-output','m1-required-output-subject-01',['contract.md']),('timing','m1-workflow-timing-subject-02',['contract.md']),('configuration','m1-config-disclosure-subject-02',['contract.md','field-policy.json'])]
for name,subject,files in contracts:
 for f in files:copy(B/subject/f,'owners/'+name+'/'+f)
native=B/'m1-native-wire-owner-subject-07'
for f in ['contract.md','successor.json','wire-carriers.v1.json','wire-carriers.meta.schema.json','owner-pattern-successor.v1.json','public-route-successor.v1.json','p3-guard-successor.v1.json']:
 copy(native/f,'owners/native/'+f)
j=B/'m1-report-joint-candidate-13'
for f in ['candidate-source-map.json','joint-obligations.json','joint-budget-derivation.json','joint-depth-derivation.json']:
 copy(j/f,'evidence/'+f)
# Explicit selected current source identifiers; source-map also preserves the historical roots.
current=json.loads((j/'candidate-source-map.json').read_bytes())
save(D/'current-dispatch.json',{'schemaVersion':1,'standing':'PROPOSED current producer dispatch; historical schema bytes remain separate','currentSources':[{'schemaId':r['schemaId'],'architectureSource':next(x['architectureSource'] for x in rows if x['schemaId']==r['schemaId'])} for r in current['currentSchemas']],'compatibility':['Never identify an exact retained schema by URI alone. Verify retained descriptor and raw schema digest.','Do not relabel legacy envelope, query, common, invocation or record bytes as current majors.','Identity/native/policy documents have same-URI successors. Historical raw digests remain distinct; current selection does not remint old IDs.','A schema decoder validates shape and exact values, not repository custody or authority. Host admission must issue private handles before projection.']})
reviews=['grok-native-wire-owner-07','grok-report-joint-10','grok-native-integration-02','grok-native-integration-03','grok-report-evidence-design-02','grok-presentation-catalog-02','grok-history-selection-02','grok-required-output-01','grok-fit-interruption-01','grok-report-projection-08','grok-config-disclosure-02']
save(D/'evidence-pins.json',{'standing':'Historical substantive reviews and root checkpoints; no final selection acceptance implied','reviews':[pin(A/'docs/implementation/m1/reviews'/r/'review.json') for r in reviews],'checkpoints':[pin(A/'docs/implementation/m1/trials'/n/'checkpoint.json') for n in ['report-joint-13-checkpoint-01','joint-generation-03-checkpoint-01','report-codec-03-checkpoint-01','native-wire-integration-04-checkpoint-01','final-source-selection-02-checkpoint-01']],'pending':['History03 missing-items delta review','Timing02 original review','Exact final source-unit independent review','Fresh blind consumer/integration review','Inventory/bootstrap/toolchain selection','Product semantic owners and delivery implementation']})
lock=json.loads((A.parent/'opensip/design-lock.json').read_bytes());accepted={}
for key in ['sourceManifest','applicationManifest']:
 for r in json.loads((A/lock['approvals'][key]['path']).read_bytes())['files']:accepted[r['path']]={k:r[k] for k in ['path','sha256','bytes']}
for b in lock['inventorySuccessors']:accepted[b['candidate']['path']]=b['candidate']
for b in lock['contractSuccessors']:
 for r in json.loads((A/b['subjectManifest']['path']).read_bytes())['files']:accepted[r['path']]=r
parents=['docs/v2/contracts/product-v1/workflows-and-surfaces.md','docs/v2/contracts/product-v1/native-evidence.md','docs/v2/contracts/product-v1/identity-and-evidence.md','docs/v2/contracts/product-v1/security-and-lifecycle.md','docs/v2/architecture/report-asset-binding.v1.json','docs/coop/artifacts/d9-exit-contract.v1.14.json','docs/implementation/m1/metadata-v2/successor.json','docs/implementation/m1/control-source-v1/successor.json']
for p in parents:assert pin(A/p)==accepted[p],p
old=json.loads((A/'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_bytes());new=json.loads((D/'reference/composed-owners/d9-exit-contract.proposed.v1.15.json').read_bytes())
save(D/'draft-successor-inputs.json',{'schemaVersion':1,'standing':'DRAFT; not frozen or reviewed. Build successor.json only after complete scope/checker.','parents':[accepted[p] for p in sorted(parents)],'passageOverrides':[{'parent':accepted['docs/coop/artifacts/d9-exit-contract.v1.14.json'],'selector':{'jsonPointer':'/invariants/1/text'},'before':old['invariants'][1]['text'],'after':new['invariants'][1]['text']}],'scope':'Select exact current and historical generator source bytes; compose source successors and ownership. Preserve parent artifacts, identities, historical findings and distinct product qualification.'})
print(D,len(list(D.rglob('*'))))
