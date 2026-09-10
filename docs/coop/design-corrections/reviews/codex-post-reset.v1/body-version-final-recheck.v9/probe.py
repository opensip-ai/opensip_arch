from pathlib import Path
import ast,hashlib,json,shutil,sys
root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/body-version-final-recheck.v9'
assert not out.exists();handoff=json.loads((dc/'reviews/digest-corrections-author.v6/handoff.json').read_text());owned=handoff['ownedFilesChanged']
for row in owned:assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest()==row['sha256']
p=dc/'foundation/check-identity.py';source=p.read_text();tree=ast.parse(source);last=next(n.end_lineno for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import')
ns={'__file__':str(p),'__name__':'codex_final_body_probe'};sys.argv=[str(p)];exec(compile('\n'.join(source.split('\n')[:last]),str(p),'exec'),ns);M,C=ns['M'],ns['C']
def measure(**kwargs):
 run,objects,blobs=ns['build'](resolved=True,has_match=True,relation='clones',**kwargs)
 fact=next(v for d,v in objects.values() if d=='fact');payload=C.parse(blobs[fact['payloadDigest']]);frame=blobs[payload['bodyIdentity'].removeprefix('sha256:')];parts=M.parse_body_frame(frame)
 universe=M.parse_h_frame(blobs[fact['sourceUniverse']],'native-semantic-universe')[1]
 rid=M.close_run(run,objects,blobs)
 assert len(parts[4])==32
 return {'bodyIdentity':payload['bodyIdentity'],'sourceUniverse':fact['sourceUniverse'],'languageId':parts[3].decode(),'versionComponentBytes':len(parts[4]),'runId':rid},universe,blobs
control,universe,blobs=measure(universe_language='rust')
ownership=M.parse_h_frame(blobs[universe['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')[1]
workspace={k:v for k,v in ownership.items() if k!='schemaVersion'}
original=json.loads((dc/'reviews/codex-post-reset.v1/body-version-draft-counterexample.v9/result.json').read_text())
workspace['edition']=original['largeUniverse']['edition']
large,_,_=measure(universe_language='rust',workspace=workspace)
assert large['bodyIdentity']==control['bodyIdentity'] and large['sourceUniverse']!=control['sourceUniverse']
ts,_,_=measure(universe_language='typescript',source_path='a.ts')
js,_,_=measure(universe_language='typescript',source_path='a.js')
assert ts['languageId']=='typescript' and js['languageId']=='javascript' and ts['bodyIdentity']!=js['bodyIdentity']
out.mkdir();shutil.copyfile(__file__,out/'probe.py')
(out/'result.json').write_text(json.dumps({'standing':'Codex final-source reference Run/projection check using coauthored synthetic builder, not independent acceptance or compiler/store qualification','sourceRows':owned,'originalRawMapBytes':original['languageVersionComponentBytes'],'largeEditionEntries':len(workspace['edition']),'runs':{'rust-control':control,'rust-large-map':large,'typescript':ts,'javascript':js},'stableRustBodyAcrossUnrelatedEditionEntries':True,'allPassed':True},indent=2)+'\n')
print('Four complete clone Run controls close; 21-entry Rust map retains 32-byte version and stable body, JS language stays distinct.')
