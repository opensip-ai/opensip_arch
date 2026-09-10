from pathlib import Path
import json,hashlib,shutil,importlib.util,copy
out=Path(__file__).parent;work=out/'work';dc=work/'docs/coop/design-corrections'
s=importlib.util.spec_from_file_location('f',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f);original=f.N.admit_native_context;rows=[]
for omit_tsx,path,relation,has_match,pure in [(False,'src/plain.tsx','declares',True,True),(True,'src/plain.ts','declares',True,True),(True,'src/plain.tsx','declares',True,True),(False,'README.md','clones',False,False)]:
 def admit(language,descriptor,*args,**kwargs):
  if language=='syntax' and omit_tsx:
   for row in descriptor['grammarBundle']['grammars']:
    if row['languageId']=='typescript':row['suffixes']=[x for x in row['suffixes'] if x!='.tsx']
  return original(language,descriptor,*args,**kwargs)
 f.N.admit_native_context=admit
 row={'omittedTsxOwnership':omit_tsx,'path':path,'relation':relation,'hasMatch':has_match,'pureSyntax':pure}
 try:
  run,objects,blobs=f.build(resolved=True,has_match=has_match,universe_language='syntax',relation=relation,source_path=path,pure_syntax=pure)
  row['constructionSucceeded']=True;row['runId']=f.M.close_run(run,objects,blobs);row['verdict']='ADMIT'
  plan=objects[run['planId']][1]
  contexts=[f.M.parse_h_frame(blobs[d],'native-context') for d in plan['nativeContextDigests']]
  ctx=next(v for domain,v,_ in contexts if domain=='native.context.syntax.v2')
  row['declaredTsxOwnerRows']=[g['grammarId'] for g in ctx['grammarBundle']['grammars'] if '.tsx' in g['suffixes']]
  row['coverage']=[f.C.parse(blobs[v['payloadDigest']])['entry'] for d,v in objects.values() if d=='coverage']
 except Exception as exc:row.update(verdict='REFUSE',cause=type(exc).__name__+':'+str(exc))
 rows.append(row)
f.N.admit_native_context=original
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r={'standing':'Codex rechecks on the released actual coauthor v3 source or independent acceptance. Actual syntax descriptor removes only the .tsx ownership declaration before context admission; closure bytes remain synthetic trusted observations. The .tsx control and selected .ts control must remain legal. Last case is an explicitly README-only clone scope in the existing mixed snapshot.','sourceRoot':str(work),'sources':[{'path':str(p.relative_to(work)),'sha256':sha(p)} for p in [dc/'integration-fixtures.py',dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py',dc/'native/native-evidence.schemas.v2.json']],'cases':rows}
(out/'selected-suffix-details.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps([{k:v for k,v in x.items() if k!='coverage'} for x in rows],indent=2));print([(x['path'],[(v['coverage'],v['deficiency'],v['nativeCause']) for v in x.get('coverage',[])]) for x in rows])
