from pathlib import Path
import importlib.util,json
base=Path(__file__).parent;p=base/'work/docs/coop/design-corrections/integration-fixtures.py';s=importlib.util.spec_from_file_location('f',p);f=importlib.util.module_from_spec(s);s.loader.exec_module(f);rows=[]
for path,relation,match in [('README.md','file',True),('src/plain.rs','clones',True),('src/plain.rs','declares',True),('README.md','declares',True),('README.md','declares',False),('README.md','clones',False)]:
 row={'path':path,'relation':relation,'hasMatch':match}
 try:
  run,objects,blobs=f.build(resolved=True,has_match=match,universe_language='syntax',relation=relation,source_path=path,pure_syntax=True)
  row['runId']=f.M.close_run(run,objects,blobs);plan=objects[run['planId']][1];snapshot=objects[plan['snapshotId']][1];row['snapshotPaths']=[r['path'] for r in snapshot['sourceInventory']];row['contextDomains']=[f.M.parse_h_frame(blobs[d],'native-context')[0] for d in plan['nativeContextDigests']];row['verdict']='ADMIT';row['coverage']=[f.C.parse(blobs[v['payloadDigest']])['entry'] for d,v in objects.values() if d=='coverage']
 except Exception as exc:row.update(verdict='REFUSE',cause=type(exc).__name__+':'+str(exc))
 rows.append(row)
out=base/'pure-syntax-details.json';assert not out.exists();out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
