from pathlib import Path
import json,hashlib,importlib.util
root=Path.cwd();review=root/'docs/coop/design-corrections/reviews/consumer-b.v2';out=root/'docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-budget-counterevidence.v2';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
custody=[]
for v,expected in [('v1','e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac'),('v7','b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b')]:
 p=root/f'docs/coop/design-corrections/reviews/candidate-subject.{v}.json';assert sha(p)==expected;x=json.loads(p.read_text());snap=Path(x['snapshotRoot'])
 for row in x['files']:
  f=snap/row['path'];assert sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],str(f)
 custody.append({'version':v,'manifestSha256':expected,'fileCount':len(x['files']),'verified':True})
snap=Path(json.loads((root/'docs/coop/design-corrections/reviews/candidate-subject.v7.json').read_text())['snapshotRoot']);path='docs/coop/design-corrections/foundation/identity-schemas.v2.json';p=snap/path
assert p.read_bytes()==(review/'subject'/path).read_bytes()
spec=importlib.util.spec_from_file_location('frozen_c',snap/'docs/coop/design-corrections/foundation/canonical.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
schema=json.loads(p.read_text());budget=schema['$defs']['plan']['properties']['budget'];results=[]
for name,value,expected in [('valid',{'unit':'work-units','limit':1000},True),('empty',{},False),('missing-unit',{'limit':1000},False),('missing-limit',{'unit':'work-units'},False),('extra-field',{'unit':'work-units','limit':1000,'invented':1},False),('wrong-unit',{'unit':'seconds','limit':1000},False),('zero',{'unit':'work-units','limit':0},False),('bool-limit',{'unit':'work-units','limit':True},False)]:
 try:C.validate(budget,value);admitted=True
 except Exception:admitted=False
 assert admitted==expected,(name,admitted)
 results.append({'id':name,'value':value,'admitted':admitted,'expected':expected})
report=json.loads((review/'output/blind-review.json').read_text());g8=next(r for r in report['findings'] if r['id']=='G8')
assert g8['observed']['planBudgetSchema']==budget
(out/'result.json').write_text(json.dumps({'standing':'Codex counterevidence to a contradictory G8 premise; original blind review remains immutable and CHANGES_REQUIRED for other actual gaps. Not independent acceptance.','reviewSha256':sha(review/'output/blind-review.json'),'schemaPath':path,'schemaSha256':sha(p),'selector':'#/$defs/plan/properties/budget','budgetSchema':budget,'sameAsReviewObservedSchema':True,'custody':custody,'vectors':results,'conclusion':'G8 statement that plan.budget is an unconstrained object is false on the exact reviewed bytes; no schema correction needed. Request substantive reviewer reconciliation; no verdict altered.','productQualification':False},indent=2)+'\n')
(out/'probe.py').write_bytes(Path(__file__).read_bytes());print('frozen v1/v7 verified; eight budget vectors match closed schema')
