"""CX-BV4-TOTALITY: reproduce root attempt3 and hold the corrected law, over full Run closure.

Construction follows root's attempt3 probe.py: one view carrying a TypeScript and a syntax
file@enumerated scope for the same subject, both `complete`, with the syntax mode explicitly
requested so the Plan admits the second universe."""
import copy,json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from bounded_loader import load
f,hashes=load(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'totality')
rows=[]
def record(label,fn):
    try:rows.append({'case':label,'outcome':'ADMIT','detail':fn()})
    except Exception as exc:rows.append({'case':label,'outcome':'REFUSE','error':type(exc).__name__+':'+str(exc)[:200]})

def build(extra=False,add_fact=False,foreign_snapshot=False):
    run,objects,blobs=f.build(relation='file',has_match=True,resolved=True,source_path='a.ts')
    if not extra:return {'runId':f.M.close_run(run,objects,blobs)}
    universe=next(k for k,raw in blobs.items()
                  if raw.startswith(f.M.FRAME_PREFIX+b'native.semantic-universe.syntax.v2\0'))
    plan=copy.deepcopy(objects[run['planId']][1])
    spec=f.C.parse(blobs[plan['analysisSpecDigest']])
    spec['requestedCapabilities'].append({'capabilityId':'inventory','languageMode':'syntax-only',
                                          'workspaceRoot':'.','required':True})
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
        if foreign_snapshot:fact['snapshotId']='snapshot2:'+'b'*64
        fid=f.M.identifier('fact',fact);objects[fid]=('fact',fact);view['facts'].append(fid)
    f.rekey(objects,vid,view,run)
    evidence=copy.deepcopy(objects[run['evidenceId']][1]);evidence['coverageIds'].append(cid)
    f.rekey(objects,run['evidenceId'],evidence,run)
    f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
    return {'runId':f.M.close_run(run,objects,blobs)}

record('T1 valid one-universe file fact (root control)',lambda:build())
record('T2 two complete scopes, ONLY the TS fact (root counterexample)',lambda:build(True,False))
record('T3 two complete scopes, a matching fact in EACH universe (root valid control)',
       lambda:build(True,True))
record('T4 the same cross-universe borrow with a foreign snapshotId on the second fact',
       lambda:build(True,True,True))
print(json.dumps({'sourceHashes':hashes,'cases':rows},indent=1))
