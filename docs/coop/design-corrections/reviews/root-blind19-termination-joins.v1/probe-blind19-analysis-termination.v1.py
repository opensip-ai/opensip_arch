from pathlib import Path
import hashlib,importlib.util,json,shutil
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v32';I=B/'consumer-b.v19/output';O=B/'root-blind19-termination-joins.v1';assert not O.exists();O.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
path=S/'docs/coop/design-corrections/workflows/workflows_model.v3.py';sp=importlib.util.spec_from_file_location('root_b19_workflow3',path);W=importlib.util.module_from_spec(sp);sp.loader.exec_module(W)
inputs=[]
for n in ['envelopes/single-step.json','envelopes/multi-step.json','lib/phase7.py']:
 raw=(I/n).read_bytes();p=O/'inputs'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);inputs.append({'path':n,'sha256':sha(raw),'bytes':len(raw)})
one=json.loads((I/'envelopes/single-step.json').read_bytes());multi=json.loads((I/'envelopes/multi-step.json').read_bytes());rows=[]
def check(label,result,term,gate):
 derived=W.analysis_termination(result,gate)
 rows.append({'case':label,'actualResult':result,'declaredTermination':term,'gate':gate,'referenceDerivedTermination':derived,'classMismatch':term['class']!=derived['class']})
check('single-step',one['envelope']['run'],one['envelope']['termination'],'self')
inv=multi['envelope']['invocation'];steps={x['stepId']:x for x in inv['orderedSteps']}
for r in inv['stepResults']:
 if r['result']['kind']=='analysis':check('multi-step:'+str(r['stepId']),r['result'],r['termination'],steps[r['stepId']]['params']['verdictGate'])
assert len(rows)==3 and all(x['classMismatch'] for x in rows)
owners=['docs/v2/contracts/product-v1/workflows-and-surfaces.md','docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json','docs/coop/design-corrections/workflows/workflows_model.v3.py','docs/coop/design-corrections/workflows/workflows_model.v1.py']
report={'standing':'Bounded root evaluation of termination from actual consumer records through current reference analysis_termination. No consumer import or remint; no full invocation execution, native execution, complete Run acceptance or whole charter assent. Prior schema admission does not enforce the published cross-field rule.','sourceManifestSha256':'3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2','scriptSha256':sha(Path(__file__).read_bytes()),'inputs':inputs,'ownerHashes':{p:sha((S/p).read_bytes()) for p in owners},'normativeSelector':'invocation-record.schema.json#/$defs/AnalysisParams/properties/verdictGate/description; workflows section1 Audit gate ownership and Aggregate termination','rows':rows,'finding':{'id':'B19-SURFACE-03','severity':'MUST','classification':'consumer existing-law semantic mismatch','reason':'Three analysis projections carry verdict indeterminate but termination success. The published verdictGate description explicitly says verdict=indeterminate terminates even delegated analysis. Two required delegated analysis steps in audit are affected; its all-success aggregate also cannot follow its own actual results. Consumer phase7.py hardcodes success at these sites rather than deriving it. Exact captures retained; no root outcomes supplied to blind.'},'productQualification':False}
(O/'assessment.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copy2(Path(__file__),O/Path(__file__).name)
print(json.dumps({'checked':len(rows),'mismatches':sum(x['classMismatch'] for x in rows),'expectedClasses':[x['referenceDerivedTermination']['class'] for x in rows]}))
