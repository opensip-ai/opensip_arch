"""Preserve actual independent21 ROUTED-ONLY rows without treating them as grades."""
from pathlib import Path
import json,hashlib,shutil,ast
b=Path(__file__).resolve().parent;root=Path('/Users/sb/code/opensip-ai/opensip_arch');review=root/'docs/coop/design-corrections/reviews/post-reset-review.v21/review.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(review.read_text());assert sha(review)=='f0a2824989ac1741e0f63b57209fbbfd541c715052330085fd5d7a32bd45e3fa'
rows=r['scopedReviewOwnerDispositions'];assert len(rows)==5 and all(x['disposition']=='ROUTED-ONLY' and x['appliedByThisReview'] is False and x['finalApplicationOutcomeGranted'] is False for x in rows.values())
before=b/'v21-owner-account-before.v1';before.mkdir()
p=b/'assemble-records.py';shutil.copyfile(p,before/p.name);s=p.read_text();anchor=" if v.get('disposition') != 'ROUTING-ASSESSED-ONLY-NOT-APPLIED':\n  return False";assert s.count(anchor)==1
s=s.replace(anchor,""" if v.get('disposition') == 'ROUTED-ONLY':
  # Actual independent21 literal scope. Both false flags and a substantive
  # scope account are required; this admits preservation, never a grade.
  return (v.get('appliedByThisReview') is False
          and v.get('finalApplicationOutcomeGranted') is False
          and all(type(v.get(k)) is str and bool(v[k].strip()) for k in ('scope','basis')))
"""+anchor);ast.parse(s);p.write_text(s)
# Exercise the real guard function in isolation. No synthetic project review/grade.
tree=ast.parse(s);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='owner_scope_is_accounted');env={};exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),env);guard=env['owner_scope_is_accounted']
tests=[]
for ident,row in rows.items():
 assert guard(row);tests.append({'id':ident,'literalActualRowAdmittedAsScopeAccount':True,'appliedByThisProbe':False})
for key,val in [('appliedByThisReview',True),('finalApplicationOutcomeGranted',True),('appliedByThisReview',None),('finalApplicationOutcomeGranted',None),('basis',''),('scope','')]:
 changed={**next(iter(rows.values())),key:val};assert not guard(changed);tests.append({'negativeChangedField':key,'value':val,'scopeAccountRefused':True})
q=b/'prepare-validation.py';shutil.copyfile(q,before/q.name);s=q.read_text();anchor="finalizer=files/(dc+'finalize-application.v1.py')";assert s.count(anchor)==1
s=s.replace(anchor,"for name in ['prepare-v21-owner-account.py','v21-owner-account-custody.v1.json']:\n shutil.copyfile(Path(__file__).with_name(name),support/name)\nshutil.copytree(Path(__file__).with_name('v21-owner-account-before.v1'),support/'v21-owner-account-before.v1')\n"+anchor);ast.parse(s);q.write_text(s)
record={'standing':'Prepared application scope-account adapter only. Preserves the exact actual21 ROUTED-ONLY rows and requires both false authority flags. All future proposed outcomes still require substantive independent application review and activation. No actual assembly/application/grade occurred.','actualReview':{'path':str(review.relative_to(root)),'sha256':sha(review)},'files':[{'path':x.name,'beforeSha256':sha(before/x.name),'afterSha256':sha(x)} for x in [p,q]],'actualGuardTests':tests,'actualApplicationPerformed':False}
(b/'v21-owner-account-custody.v1.json').write_text(json.dumps(record,indent=2)+'\n');print('Actual5scopeaccounts admitted,6bad authority/scope variants refused; no application or grade')
