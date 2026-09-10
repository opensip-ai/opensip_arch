"""Codex adaptation of frozen v8 fixture to exercise authoritative file claims end to end.
Not independent review or product qualification; source models remain frozen and untouched.
"""
from pathlib import Path
import ast,copy,hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';mp=dc/'reviews/candidate-subject.v8.json';manifest=json.loads(mp.read_text());assert hashlib.sha256(mp.read_bytes()).hexdigest()=='cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70'
base=Path('/tmp/opensip-design-corrections/file-payload-final-recheck.v9/work');fixture=base/'docs/coop/design-corrections/foundation/check-identity.py';out=dc/'reviews/codex-post-reset.v1/file-payload-counterexample.v9/final-recheck';out.mkdir(exist_ok=False)
source=fixture.read_text();tree=ast.parse(source);last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
ns={'__file__':str(fixture),'__name__':'codex_frozen_file_fixture'};exec(compile('\n'.join(source.split('\n')[:last]),str(fixture),'exec'),ns)
M,C,N=ns['M'],ns['C'],ns['N'];put,rekey=ns['put_blob'],ns['rekey'];rows=[]
def exercise(kind):
 # This explicit synthetic detector fixture projects the closed DSL subject field onto file.path.
 # No source model is edited and no compiler/parser/evaluator implementation is qualified.
 wanted='absent.ts' if kind=='uninventoried-path' else 'a.ts'
 original_shape=ns['relation_fixture']
 def selected_shape(*args,**kwargs):
  shape=original_shape(*args,**kwargs)
  if args[0]=='file':shape=dict(shape,filter=('subject',wanted))
  return shape
 ns['relation_fixture']=selected_shape
 try:r,o,b=ns['build'](has_match=True,relation='file')
 finally:ns['relation_fixture']=original_shape
 inventory={v['path']:v for v in o[r['snapshotId']][1]['sourceInventory']};actual=inventory['a.ts']
 payload={'path':wanted,'contentSha256':actual['sha256'],'byteLength':actual['bytes']}
 if kind=='wrong-content-hash':payload['contentSha256']='f'*64
 if kind=='wrong-byte-length':payload['byteLength']+=1
 skey=next(k for k,(d,v) in o.items() if d=='subject-scope');scope=copy.deepcopy(o[skey][1]);scope.update(relation='file',resolution='enumerated');rekey(o,skey,scope,r)
 fkey=next(k for k,(d,v) in o.items() if d=='fact');fact=copy.deepcopy(o[fkey][1]);old_payload_digest=fact['payloadDigest'];fact.update(relation='file',resolution='enumerated',payloadDigest=put(b,payload));new_fact=rekey(o,fkey,fact,r)
 for key in [k for k,(d,v) in o.items() if d=='coverage']:
  cov=copy.deepcopy(o[key][1]);sc=o[cov['scopeId']][1];p=ns['coverage_result'](sc,sc['sourceUniverse'],True)
  p['entry']['resolutionCompleteness']=N.completeness_from_stage('file','enumerated',sc['subjects'],[],'complete',False,True)
  admission=N.admit_coverage_result_v3(p,sc,[],cov['payloadSchemaDigest']);assert admission['result']=='ADMIT',admission
  cov['payloadDigest']=put(b,p);rekey(o,key,cov,r)
 ns['resync_witness'](o,b,r);ns['resync_proof_refs'](o,b,r)
 view=o[o[r['evidenceId']][1]['viewIds'][0]][1];assert new_fact in view['facts'];assert kind=='control' or old_payload_digest!=fact['payloadDigest']
 result={'id':kind,'payload':payload,'inventoryTruth':actual,'reachableFactId':new_fact,'coverageAdmission':admission,'resolutionCompleteness':p['entry']['resolutionCompleteness']}
 try:
  rid=M.close_run(r,o,b);result['closure']={'admitted':True,'runId':rid}
  store=M.EvidenceStore();execution='exec1_'+'c'*32
  try:
   prepared=store.prepare(r,o,b,execution,ns['replay']);result['store']={'preparedRunId':prepared,'commit':store.commit(execution)}
  except Exception as e:result['store']={'refused':str(e),'exception':type(e).__name__}
 except Exception as e:result['closure']={'admitted':False,'cause':str(e),'exception':type(e).__name__}
 return result
try:
 for name in ('control','wrong-content-hash','wrong-byte-length','uninventoried-path'):rows.append(exercise(name))
finally:
 (out/'probe.py').write_bytes(Path(__file__).read_bytes());(out/'result.json').write_text(json.dumps({'standing':'Codex coauthor adaptation of frozen v8 synthetic fixtures, not independent review or product qualification','sourceManifestSha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'sourceFixture':str(fixture),'sourceFixtureSha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'vectors':rows},indent=2)+'\n')
print(json.dumps(rows))
