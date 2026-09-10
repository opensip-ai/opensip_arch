from pathlib import Path
import ast,copy,hashlib,json,shutil,sys
root=Path.cwd();dc=root/'docs/coop/design-corrections';base_manifest=dc/'reviews/candidate-subject.v8.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(base_manifest)=='cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70'
manifest=json.loads(base_manifest.read_text());base=Path(manifest['snapshotRoot'])
tmp=Path('/tmp/opensip-design-corrections/partial-clone-coverage-final-recheck.v9');tmp.mkdir(exist_ok=False);work=tmp/'work';shutil.copytree(base,work)
owned=list({r['path']:r for v in ('v5','v6') for r in json.loads((dc/('reviews/digest-corrections-author.'+v+'/handoff.json')).read_text())['ownedFilesChanged']}.values());rows=[]
for row in owned:
 p=root/row['path'];raw=p.read_bytes();q=work/row['path'];q.write_bytes(raw);rows.append({'path':row['path'],'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
assert all(sha(root/r['path'])==r['sha256'] for r in rows),'Source moved during capture'
here=work/'docs/coop/design-corrections/foundation';fixture=here/'check-identity.py';source=fixture.read_text();tree=ast.parse(source);nodes=[]
for node in tree.body:
 nodes.append(node)
 if isinstance(node,ast.FunctionDef) and node.name=='graph_with_import':break
else:raise AssertionError('Fixture prefix boundary missing')
ns={'__file__':str(fixture),'__name__':'codex_partial_clone_probe'};old_argv=sys.argv;sys.argv=[str(fixture)]
try:exec(compile(ast.Module(body=nodes,type_ignores=[]),str(fixture),'exec'),ns)
finally:sys.argv=old_argv
M=ns['M'];C=ns['C'];build=ns['build'];replay=ns['replay']
initial=build(relation='clones',universe_language='rust',has_match=False,resolved=False)
scope=next(v for d,v in initial[1].values() if d=='subject-scope');_,universe,_=M.parse_h_frame(initial[2][scope['sourceUniverse']],'native-semantic-universe')
_,ownership,_=M.parse_h_frame(initial[2][universe['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')
workspace={'edition':universe['edition'],**{k:copy.deepcopy(v) for k,v in ownership.items() if k!='schemaVersion'}};workspace['enumeration']='partial'
vectors=[]
for name,resolved in [('honest-unknown-control',False),('contradictory-complete-claim',True)]:
 run,objects,blobs=build(relation='clones',universe_language='rust',has_match=False,resolved=resolved,workspace=workspace)
 cov=next(v for d,v in objects.values() if d=='coverage');payload=C.parse(blobs[cov['payloadDigest']]);seal=objects[run['evaluationSealId']][1]
 result={'id':name,'ownershipEnumeration':workspace['enumeration'],'coverage':payload['entry'],'sealVerdict':seal['verdict'],'factCount':sum(d=='fact' for d,v in objects.values()),'closure':{},'store':{}}
 try:
  result['closure']={'admitted':True,'runId':M.close_run(run,objects,blobs)}
  store=M.EvidenceStore();eid='exec1_'+('a' if not resolved else 'b')*32
  result['store']={'preparedRunId':store.prepare(run,objects,blobs,eid,replay),'commit':store.commit(eid)}
 except Exception as exc:result['closure']={'admitted':False,'cause':type(exc).__name__+':'+str(exc)}
 vectors.append(result)
assert vectors[0]['store'].get('commit')=='committed' and vectors[0]['sealVerdict']=='indeterminate',vectors[0]
assert all(sha(root/r['path'])==r['sha256'] for r in rows),'Source moved during probe; no stable-current claim'
out=dc/'reviews/codex-post-reset.v1/partial-clone-coverage-final-recheck.v9';out.mkdir(exist_ok=False)
for row in rows:
 q=out/'source-delta'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/row['path'],q)
shutil.copyfile(Path(__file__),out/'probe.py')
result={'standing':'Codex complete-Run probe using captured released final v9 source over frozen v8. Synthetic trusted observations/reference store, not product qualification or independent acceptance.','baseManifestSha256':sha(base_manifest),'currentSourceStableDuringProbe':True,'sourceDelta':rows,'vectors':vectors,'productQualification':False}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(vectors,indent=2))
