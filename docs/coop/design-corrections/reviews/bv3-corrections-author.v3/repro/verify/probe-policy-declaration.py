from pathlib import Path
import json,importlib.util,hashlib
root=Path('/tmp/opensip-design-corrections/bv3-corrections-author.v3/repro/verify/work');dc=root/'docs/coop/design-corrections';source=dc/'integration-fixtures.py';s=importlib.util.spec_from_file_location('root_policy_declaration',source);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
original=f.policy_for;rows=[]
for declared in (True,False):
 def policy_for(language,atom=None,subject_kind='symbol'):
  atom.update(relation='runtime-observation',minResolution='observed',evidence='runtime')
  p=original(language,atom,subject_kind)
  if declared:p['rules'][0]['evidenceUse']=[{'kind':'runtime','requirement':'required'}]
  return p
 f.policy_for=policy_for
 run,objects,blobs=f.build(resolved=False,has_match=False)
 policy=f.C.parse(blobs[objects[run['planId']][1]['policyDigest']]);row={'runtimeEvidenceDeclared':declared,'policy':policy}
 try:f.W.resolve_policy(policy);row['policyAdmission']={'admitted':True}
 except Exception as exc:row['policyAdmission']={'admitted':False,'detail':type(exc).__name__+':'+str(getattr(exc,'detail',exc))}
 try:row['runAdmission']={'admitted':True,'runId':f.M.close_run(run,objects,blobs)}
 except Exception as exc:row['runAdmission']={'admitted':False,'detail':type(exc).__name__+':'+str(exc)}
 rows.append(row)
f.policy_for=original
report={'standing':'Codex same-policy declaration differential between resolve_policy and retained Run closure. Construction helper atom changed in place so policy, compiled program and addressed witness carry the same actual predicate. Both Runs are indeterminate empty views with absent required runtime evidence, not a claim of valid product execution or false-negative exploit. The legal declaration control must close before interpreting the undeclared variant.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [source,dc/'foundation/identity-model.py',dc/'workflows/workflows_model.v1.py']],'cases':rows}
out=Path('/tmp/opensip-design-corrections/bv3-corrections-author.v3/logs/final-policy-declaration.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2));assert rows[0]['policyAdmission']['admitted'] and rows[0]['runAdmission']['admitted'],'Control invalid'
