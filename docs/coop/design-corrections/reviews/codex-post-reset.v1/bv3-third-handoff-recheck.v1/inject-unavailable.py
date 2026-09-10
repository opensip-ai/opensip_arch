from pathlib import Path
import copy,importlib.util,json
base=Path(__file__).parent
s=importlib.util.spec_from_file_location('f',base/'work/docs/coop/design-corrections/integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
rows=[]
for relation,path,pure in [('declares','README.md',True),('clones','README.md',True),('clones','README.md',False),('references','src/plain.rs',True)]:
 for name,change,expected in [
  ('control',{},None),
  ('false-complete',dict(coverage='complete',deficiency=None,nativeCause=None),'SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE:'),
  ('null-cause',dict(nativeCause=None),'SYNTAX_CAPABILITY_CAUSE_MISMATCH:'),
  ('wrong-cause',dict(nativeCause='no-program-unit'),'SYNTAX_CAPABILITY_CAUSE_MISMATCH:'),
  ('wrong-deficiency',dict(deficiency='budget-exhausted'),'SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH:')]:
  run,objects,blobs=f.build(resolved=False,has_match=False,universe_language='syntax',relation=relation,source_path=path,pure_syntax=pure)
  k=next(k for k,(d,v) in objects.items() if d=='coverage');v=copy.deepcopy(objects[k][1]);p=f.C.parse(blobs[v['payloadDigest']]);p['entry'].update(change);v['payloadDigest']=f.put_blob(blobs,p);f.rekey(objects,k,v,run);f.resync_witness(objects,blobs,run)
  row=dict(relation=relation,path=path,pureSyntax=pure,case=name,constructionSucceeded=True,expectedCause=expected)
  try:row.update(runId=f.M.close_run(run,objects,blobs),cause=None)
  except Exception as exc:row.update(cause=str(exc))
  row['pass']=row['cause'] is None if expected is None else (row['cause'] or '').startswith(expected)
  rows.append(row)
report=dict(standing='Codex injected full-Run unavailable Coverage controls on released v3. Synthetic construction only; closure itself must refuse each invalid claim. Not independent acceptance.',cases=rows,failed=sum(not r['pass'] for r in rows))
out=base/'injected-unavailable.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['failed']==0
