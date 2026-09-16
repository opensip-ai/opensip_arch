"""Root synthetic full-Run control for an optional selected-U missing candidate.
Transforms an exact reference fixture in a separate namespace, never edits source.
No consumer code, compiler/provider/host qualification or source acceptance.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest();F=a.source/'docs/coop/design-corrections/foundation'
def load(name,n):
 s=importlib.util.spec_from_file_location(name,F/n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def source_hashes():
 return {f.relative_to(a.source).as_posix():sha(f.read_bytes()) for f in sorted(F.glob('*')) if f.is_file()}
before=source_hashes();origin=F/'evaluator_candidate_fixture.v3.py';old=origin.read_text();text=old
needle='"required": True, "kinds": [], "programBindings": [cand_binding]'
assert text.count(needle)==1;text=text.replace(needle,'"required": False, "kinds": [], "programBindings": [cand_binding]')
needle='"workspaceRoot": ".", "required": True,\n    }])'
assert text.count(needle)==1;text=text.replace(needle,'"workspaceRoot": ".", "required": False,\n    }])')
needle='    ed = _blob(blobs, env)\n    candidate_ref = {"domain": "candidate-producer-result", "digest": ed}\n'
assert text.count(needle)==1;text=text.replace(needle,'    # Root control: retain NO candidate envelope and NO candidate reference.\n    candidate_ref = None\n')
(a.out/'fixture.original.py').write_text(old);(a.out/'fixture.root-control.py').write_text(text)
ns={'__file__':str(origin),'__name__':'root_optional_candidate_fixture'};exec(compile(text,str(a.out/'fixture.root-control.py'),'exec'),ns)
R=load('root_optional_candidate_replay','evaluator_replay_model.v3.py');S=load('root_optional_candidate_seal','evaluator_semantic_fixture.v3.py');M=R.M;C=M.C
report={'standing':'Root synthetic fixture control. Exact owner structural admission and full semantic replay measured if reached. No product or consumer acceptance.','source':str(a.source),'sourceBefore':before,'fixtureTransforms':['optional clones-near cell','matching optional requestedCapabilities row','no retained candidate envelope/reference'],'scriptSha256':sha(Path(__file__).read_bytes()),'structuralAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED'}
try:
 graph=ns['build_candidate_graph'](mode='complete-empty');seed,objects,blobs,_=ns['F'].seal_fixture(graph)
 report['structuralAdmission']='REFUSE';_,owner=M.open_run_closure(seed,objects,blobs);report['structuralAdmission']='ADMIT'
 i=graph['inputs'];out=R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner)
 run,objects,blobs=S.seal_derived(graph,out,objects,blobs);report['semanticAdmission']='REFUSE';res=R.replay(run,objects,blobs);assert M.close_run(run,objects,blobs)==res['runId'];report['semanticAdmission']='ADMIT'
 man=C.parse(blobs[out['proof']['executionInputsDigest']]);cell=next(x for x in man['cellOutcomes'] if x['capabilityId']=='clones-near');binding=next(x for x in graph['enumerationPlan']['cells'] if x['capabilityId']=='clones-near')['programBindings'][0]
 assert not cell['required'] and cell['universe'] is not None and cell['enumeratorStatus']=='selected' and cell['candidateResultDigest'] is None and not man['candidateResultRefs']
 assert 'deficiency' not in binding and 'nativeCause' not in binding
 report.update(runId=res['runId'],verdict=res['verdict'],candidateOutcome=cell,candidateBinding=binding,executionDeficiencies=out['proof']['executionDeficiencies'],executionInputsDigest=out['proof']['executionInputsDigest'])
 (a.out/'execution-inputs.json').write_bytes(C.canonical(man));(a.out/'proof.json').write_bytes(C.canonical(out['proof']));(a.out/'run.json').write_bytes(C.canonical(run))
except Exception as e:report['exceptionType']=type(e).__name__;report['reason']=str(e)
after=source_hashes();report['sourceDrift']={k:[before.get(k),after.get(k)] for k in set(before)|set(after) if before.get(k)!=after.get(k)}
report['passed']=report['semanticAdmission']=='ADMIT' and not report['sourceDrift'];(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['sourceBefore','candidateBinding']}));raise SystemExit(not report['passed'])
