from pathlib import Path
import ast, types, importlib.util, json, time, hashlib, os, sys
sys.path.insert(0,'/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages')
HERE=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation')
B=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def scaled_fixture(count):
    path=HERE/'evaluator_graph_fixture.v3.py';tree=ast.parse(path.read_text());edits=[]
    class Scale(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                key=node.targets[0].id
                if key=='sources' and isinstance(node.value,ast.Dict):
                    node.value=ast.parse("{f'src/file-{i:06}.ts':b'export const x = 1;\\n' for i in range(SYNTHETIC_COUNT)}",mode='eval').body;edits.append(key)
                if key=='languages' and isinstance(node.value,ast.Dict):
                    node.value=ast.parse("{p:'typescript' for p in sources}",mode='eval').body;edits.append(key)
            return self.generic_visit(node)
    tree=Scale().visit(tree);assert edits==['sources','languages'];ast.fix_missing_locations(tree)
    m=types.SimpleNamespace();scope=m.__dict__;scope.update(__file__=str(path),__name__='sm9_scaled_fixture',SYNTHETIC_COUNT=count)
    exec(compile(tree,str(path),'exec'),scope);return m
def main():
    count=int(os.environ['OPENSIP_SM_SYNTHETIC_COUNT']);F=scaled_fixture(count)
    R=load('sm9_replay',HERE/'evaluator_replay_model.v3.py');S=load('sm9_seal',HERE/'evaluator_semantic_fixture.v3.py');M=R.M
    start=time.monotonic_ns();g=F.build_file_inputs(atom_override={'op':'exists','relation':'file','minResolution':'enumerated','filters':[]},budget_limit=max(1000000,count*count*100))
    seed,objects,blobs,_=F.seal_fixture(g);_,owner=M.open_run_closure(seed,objects,blobs);i=g['inputs'];out=R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner);run,objects,blobs=S.seal_derived(g,out,objects,blobs);built=time.monotonic_ns()
    replay_start=time.monotonic_ns();run_id=M.close_run(run,objects,blobs);end=time.monotonic_ns();assert len(out['proof']['findingIds'])==count, out['proof']
    result=dict(standing='UNREVIEWED SYNTHETIC COMPLETE REPLAY PROBE; NO COMPILER OR PRODUCT QUALIFICATION',syntheticSourceFiles=count,findings=len(out['proof']['findingIds']),objects=len(objects),blobs=len(blobs),blobBytes=sum(len(v)for v in blobs.values()),runId=run_id,buildNanos=built-start,completeReplayNanos=end-replay_start,fullCloseRunBoundary=True,graphScalingEdits=['sources population','corresponding source languages'],SM9PlaceholderFilled=False,SMComplete=False,effectiveL=False,productQualification=False)
    tag=os.environ.get('OPENSIP_SM_RUN_TAG',f'probe-{count}');assert all(c.isalnum()or c in '-_'for c in tag)
    (B/f'{tag}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
