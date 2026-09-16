"""Accommodate actual v15 routing-only wording without granting an owner grade."""
from pathlib import Path
import ast, copy, hashlib, json, shutil
b = Path(__file__).parent
before = b / 'v15-owner-guard-before.v1'
assert not before.exists()
before.mkdir()
paths = ['assemble-records.py', 'prepare-validation.py']
for name in paths:
    shutil.copyfile(b / name, before / name)
p = b / 'assemble-records.py'
s = p.read_text()
old = "assert set(scoped)=={'DR-'+str(i) for i in range(201,206)} and all((v['disposition'] in ('ACCEPT','ACCEPT_SCOPED') or (v['disposition']=='ROUTING-ASSESSED-ONLY-NOT-APPLIED' and v.get('finalApplicationOutcomeGranted') is False)) for v in scoped.values())"
new = '''def owner_scope_is_accounted(v):
 # Preserve literal reviewer rows. This only admits the scope account to a
 # prospective wrapper; the fresh application reviewer must still grade it.
 if v.get('disposition') in ('ACCEPT','ACCEPT_SCOPED'):
  return True
 if v.get('disposition') != 'ROUTING-ASSESSED-ONLY-NOT-APPLIED':
  return False
 flags=[v[k] for k in ('finalApplicationOutcomeGranted','appliedByThisReview') if k in v]
 if not flags or any(x is not False for x in flags):
  return False
 if 'finalApplicationOutcomeGranted' in v:
  return True
 return (v.get('authority') == 'Five owner routing assessments do not grant a final application outcome.'
         and all(type(v.get(k)) is str and bool(v[k].strip()) for k in ('scope','basis')))
assert set(scoped)=={'DR-'+str(i) for i in range(201,206)} and all(owner_scope_is_accounted(v) for v in scoped.values())'''
assert s.count(old) == 1
p.write_text(s.replace(old,new))
tree = ast.parse(p.read_text())
fn = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='owner_scope_is_accounted')
ns = {}; exec(compile(ast.Module(body=[fn],type_ignores=[]),'actual-assembly-owner-guard','exec'),ns)
guard = ns['owner_scope_is_accounted']
root = Path('/Users/sb/code/opensip-ai/opensip_arch')
rows=[]
for version in ['v13','v15']:
 r=json.loads((root/f'docs/coop/design-corrections/reviews/post-reset-review.{version}/review.json').read_text())
 for rid, row in r['scopedReviewOwnerDispositions'].items():
  if not rid.startswith('DR-'): continue
  assert guard(row); rows.append({'id':version+'-'+rid,'expected':True,'actual':True})
sample=copy.deepcopy(r['scopedReviewOwnerDispositions']['DR-201'])
bad=[]
for key,val in [('appliedByThisReview',True),('appliedByThisReview',0),('appliedByThisReview',None),('finalApplicationOutcomeGranted',True),('authority','Routing reviewed.'),('scope',''),('basis',None),('disposition','ACCEPTED-BY-INFERENCE')]:
 v=copy.deepcopy(sample);v[key]=val;bad.append((key+'='+repr(val),v))
v=copy.deepcopy(sample);del v['appliedByThisReview'];bad.append(('missing-explicit-false',v))
for name,v in bad:
 assert not guard(v);rows.append({'id':name,'expected':False,'actual':False})
q=b/'prepare-validation.py';s=q.read_text();needle="finalizer=files/(dc+'finalize-application.v1.py')"
assert s.count(needle)==1
s=s.replace(needle,"for name in ['prepare-v15-owner-guard.py','v15-owner-guard-custody.v1.json']:\n shutil.copyfile(Path(__file__).with_name(name),support/name)\nshutil.copytree(Path(__file__).with_name('v15-owner-guard-before.v1'),support/'v15-owner-guard-before.v1')\n"+needle)
q.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'standing':'Prepared orchestration adaptation only; no application assembled, reviewed or activated.', 'reason':'Actual v15 uses appliedByThisReview:false plus an explicit no-final-outcome authority statement. Preserve that literal account; prospective grades still require substantive fresh application acceptance and activation.', 'beforeImages':before.name,'changedFiles':[{'path':n,'beforeSha256':sha(before/n),'afterSha256':sha(b/n)} for n in paths], 'controls':rows,'productImplementation':False}
(b/'v15-owner-guard-custody.v1.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'prepared':True,'controls':len(rows),'stageCreated':False}))
