"""Preserve actual v16 no-grade routing statement in prospective application."""
from pathlib import Path
import ast,copy,hashlib,json,shutil
b=Path(__file__).parent;root=Path('/Users/sb/code/opensip-ai/opensip_arch')
before=b/'v16-owner-guard-before.v1';assert not before.exists();before.mkdir()
names=['assemble-records.py','prepare-validation.py']
for n in names:shutil.copyfile(b/n,before/n)
p=b/names[0];s=p.read_text()
old="v.get('authority') == 'Five owner routing assessments do not grant a final application outcome.'"
new="v.get('authority') in ('Five owner routing assessments do not grant a final application outcome.', 'Five owner routing assessments do not grant a final application outcome and are not a grade.')"
assert s.count(old)==1;p.write_text(s.replace(old,new))
fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='owner_scope_is_accounted')
ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'actual-assembly-owner-guard','exec'),ns);guard=ns['owner_scope_is_accounted'];controls=[]
for version in ['v13','v15','v16']:
 r=json.loads((root/f'docs/coop/design-corrections/reviews/post-reset-review.{version}/review.json').read_text())
 for rid,row in r['scopedReviewOwnerDispositions'].items():
  if not rid.startswith('DR-'):continue
  assert guard(row);controls.append({'id':version+'-'+rid,'expected':True,'actual':True})
sample=copy.deepcopy(r['scopedReviewOwnerDispositions']['DR-201'])
bad=[]
for k,val in [('appliedByThisReview',True),('appliedByThisReview',0),('appliedByThisReview',None),('finalApplicationOutcomeGranted',True),('authority','Routing reviewed.'),('scope',''),('basis',None),('disposition','ACCEPTED-BY-INFERENCE')]:
 v=copy.deepcopy(sample);v[k]=val;bad.append((k+'='+repr(val),v))
v=copy.deepcopy(sample);del v['appliedByThisReview'];bad.append(('missing-explicit-false',v))
for name,v in bad:
 assert not guard(v);controls.append({'id':name,'expected':False,'actual':False})
q=b/names[1];s=q.read_text();needle="finalizer=files/(dc+'finalize-application.v1.py')";assert s.count(needle)==1
s=s.replace(needle,"for name in ['prepare-v16-owner-guard.py','v16-owner-guard-custody.v1.json']:\n shutil.copyfile(Path(__file__).with_name(name),support/name)\nshutil.copytree(Path(__file__).with_name('v16-owner-guard-before.v1'),support/'v16-owner-guard-before.v1')\n"+needle);q.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(b/'v16-owner-guard-custody.v1.json').write_text(json.dumps({'standing':'Prepared orchestration adaptation only; no application assembled, accepted or activated.','reason':'Actual v16 adds and are not a grade to explicit no-final-outcome authority. Accept that exact routing-only account while retaining all false-flag guards. Prospective grade still requires substantive final application review and activation.','beforeImages':before.name,'changedFiles':[{'path':n,'beforeSha256':sha(before/n),'afterSha256':sha(b/n)} for n in names],'controls':controls,'productImplementation':False},indent=2)+'\n')
print(json.dumps({'prepared':True,'controls':len(controls),'stageCreated':False}))
