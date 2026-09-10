from pathlib import Path
import importlib.util,json
base=Path(__file__).parent;p=base/'work/docs/coop/design-corrections/integration-fixtures.py';s=importlib.util.spec_from_file_location('f',p);f=importlib.util.module_from_spec(s);s.loader.exec_module(f);rows=[]
for relation in ['references','imports','calls','types','reachability']:
 for match in [True,False]:
  row={'relation':relation,'hasMatch':match}
  try:
   run,objects,blobs=f.build(resolved=True,has_match=match,universe_language='syntax',relation=relation,source_path='src/plain.rs',pure_syntax=True)
   row['constructionSucceeded']=True;row['runId']=f.M.close_run(run,objects,blobs);row['verdict']='ADMIT';row['coverage']=[f.C.parse(blobs[v['payloadDigest']])['entry'] for d,v in objects.values() if d=='coverage'];row['factRungs']=[v['resolution'] for d,v in objects.values() if d=='fact']
  except Exception as exc:row.update(verdict='REFUSE',cause=type(exc).__name__+':'+str(exc))
  rows.append(row)
out=base/'semantic-capability-details.json';assert not out.exists();out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k!='coverage'} for r in rows],indent=2))
