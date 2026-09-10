from pathlib import Path
import importlib.util,json
base=Path(__file__).parent;p=base/'work/docs/coop/design-corrections/integration-fixtures.py';s=importlib.util.spec_from_file_location('f',p);f=importlib.util.module_from_spec(s);s.loader.exec_module(f);rows=[]
for relation,match in [('file',True),('declares',True),('declares',False),('clones',False)]:
 run,objects,blobs=f.build(resolved=False,has_match=match,universe_language='syntax',relation=relation,source_path='README.md')
 rows.append({'relation':relation,'hasMatch':match,'runId':f.M.close_run(run,objects,blobs),'coverage':[f.C.parse(blobs[v['payloadDigest']]) for d,v in objects.values() if d=='coverage']})
out=base/'coverage-details.json';assert not out.exists();out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
