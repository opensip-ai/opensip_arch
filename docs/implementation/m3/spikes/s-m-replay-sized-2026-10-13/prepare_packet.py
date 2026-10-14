from pathlib import Path
import importlib.util,json,hashlib,sys
B=Path(__file__).resolve().parent
probe=Path('/tmp/opensip-implementation/sm-replay-2026-10-09/probe.py')
spec=importlib.util.spec_from_file_location('native_sm_scaled_builder',probe);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
def emit(count):
 F=P.scaled_fixture(count);R=P.load('native_sm_reference',P.HERE/'evaluator_replay_model.v3.py');S=P.load('native_sm_seal',P.HERE/'evaluator_semantic_fixture.v3.py');M=R.M
 g=F.build_file_inputs(atom_override={'op':'exists','relation':'file','minResolution':'enumerated','filters':[]},budget_limit=max(1000000,count*count*100));seed,objects,blobs,_=F.seal_fixture(g);_,owner=M.open_run_closure(seed,objects,blobs);i=g['inputs'];out=R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner);run,objects,blobs=S.seal_derived(g,out,objects,blobs);assert len(out['proof']['findingIds'])==count
 run_id=M.close_run(run,objects,blobs);assert run_id not in objects;objects[run_id]=('run',run)
 packet=dict(standing='LABELLED SYNTHETIC GRAPH; REFERENCE DERIVED OUTPUTS ARE COMPARISON TARGETS ONLY FOR NATIVE REPLAY',syntheticSourceFiles=count,syntheticFindings=count,runId=run_id,objects=[dict(id=k,domain=v[0],descriptor=v[1])for k,v in sorted(objects.items())],blobs=[dict(sha256=k,hex=v.hex())for k,v in sorted(blobs.items())]);path=B/f'packet-{count}.json';path.write_text(json.dumps(packet,separators=(',',':'))+'\n');raw=path.read_bytes();print(json.dumps(dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),findings=count)),flush=True)
if __name__=='__main__':emit(int(sys.argv[1]))
