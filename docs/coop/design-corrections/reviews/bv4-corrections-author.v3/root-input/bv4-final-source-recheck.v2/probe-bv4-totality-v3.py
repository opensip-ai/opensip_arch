"""Root-selected full-Run cross-universe totality diagnostic on released final source."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,shutil
base=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v2/work')
out=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2/totality');out.mkdir(exist_ok=False)
root=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2/work')
dc=root/'docs/coop/design-corrections';source=dc/'foundation/check-identity.py'
raw=source.read_text();tree=ast.parse(raw)
adapter=ast.parse(Path('/tmp/opensip-design-corrections/codex-post-reset.v1/adapt-integration-builder-v13.py').read_text())
names=next(ast.literal_eval(n.value) for n in adapter.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='names' for t in n.targets))
blocks=[];found=set()
for n in tree.body:
 declared={n.name} if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) else ({t.id for t in n.targets if isinstance(t,ast.Name)} if isinstance(n,ast.Assign) else set())
 if names&declared:blocks.append(ast.get_source_segment(raw,n));found|=names&declared
assert found==names
helper=dc/'integration-fixtures.py'
shutil.copyfile(helper,out/'integration-fixtures.before.py')
helper.write_text('''import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('development_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('development_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']
'''+ '\n\n'.join(blocks)+'\n')
spec=importlib.util.spec_from_file_location('root_totality_fixture',helper);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
rows=[]
def record(label,fn):
 try: rows.append({'case':label,'outcome':'ADMIT','detail':fn()})
 except Exception as exc:rows.append({'case':label,'outcome':'REFUSE_OR_HARNESS_ERROR','error':type(exc).__name__+':'+str(exc)})
def build(extra=False,add_fact=False):
 run,objects,blobs=f.build(relation='file',has_match=True,resolved=True,source_path='a.ts')
 if not extra:return {'runId':f.M.close_run(run,objects,blobs)}
 universe=next(k for k,raw in blobs.items() if raw.startswith(f.M.FRAME_PREFIX+b'native.semantic-universe.syntax.v2\0'))
 plan=copy.deepcopy(objects[run['planId']][1])
 spec=f.C.parse(blobs[plan['analysisSpecDigest']])
 spec['requestedCapabilities'].append({'capabilityId':'inventory','languageMode':'syntax-only','workspaceRoot':'.','required':True})
 spec=f.sort_canonical_sets('analysis-spec',spec)
 plan['analysisSpecDigest']=f.put_blob(blobs,spec)
 f.rekey_plan(objects,blobs,run,plan)
 old_scope=next(v for d,v in objects.values() if d=='subject-scope')
 scope=copy.deepcopy(old_scope);scope.update(sourceUniverse=universe,targetUniverse=universe)
 sid=f.M.identifier('subject-scope',scope);objects[sid]=('subject-scope',scope)
 schema=next(v['payloadSchemaDigest'] for d,v in objects.values() if d=='coverage')
 paths=[r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
 cp=f.coverage_result(scope,universe,True,blobs,paths)
 admission=f.N.admit_coverage_result_v3(cp,scope,[],schema)
 assert admission['result']=='ADMIT',admission
 coverage={'schemaVersion':2,'scopeId':sid,'payloadSchemaDigest':schema,'payloadDigest':f.put_blob(blobs,cp)}
 cid=f.M.identifier('coverage',coverage);objects[cid]=('coverage',coverage)
 vid=objects[run['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(objects[vid][1])
 view['scopeIds'].append(sid);view['coverageIds'].append(cid)
 if add_fact:
  fact=copy.deepcopy(next(v for d,v in objects.values() if d=='fact'))
  fact.update(sourceUniverse=universe,targetUniverse=universe)
  fid=f.M.identifier('fact',fact);objects[fid]=('fact',fact);view['facts'].append(fid)
 f.rekey(objects,vid,view,run)
 evidence=copy.deepcopy(objects[run['evidenceId']][1]);evidence['coverageIds'].append(cid)
 f.rekey(objects,run['evidenceId'],evidence,run)
 f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
 return {'runId':f.M.close_run(run,objects,blobs),'extraScope':scope,'extraCoverage':cp,
         'facts':[v for d,v in objects.values() if d=='fact']}
record('valid original one-universe file fact',lambda:build())
record('second complete syntax-universe scope without any syntax-universe file fact',lambda:build(True,False))
record('valid second complete scope with its own syntax-universe file fact',lambda:build(True,True))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Final-source root diagnostic, not final-source assent or independent evidence. Full retained Run closure using author fixture data and root-selected second-universe mutation. No product qualification. Constructor errors are recorded separately from an established admission counterexample.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':sha(p)} for p in [source,helper,dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py']],'cases':rows}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps(report,indent=2))
