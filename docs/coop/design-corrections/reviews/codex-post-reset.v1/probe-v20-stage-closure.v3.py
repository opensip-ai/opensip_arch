from pathlib import Path
import json,hashlib,importlib.util,copy
R=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
T=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/v20-stage-closure-root.v3');T.mkdir(exist_ok=False)
base=R/'v20-advisory-assessment.v1/probe-tree-pristine/docs/coop/design-corrections/foundation'
s=importlib.util.spec_from_file_location('root_stage_fixtures',base/'_probe_fixtures.py');F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
M,C=F.M,F.C
schemas={'before':base/'identity-schemas.v2.json','rejected-root-proposal':Path('/tmp/opensip-design-corrections/v20-stage-proposal.v1/work/docs/coop/design-corrections/foundation/identity-schemas.v2.json'),'claude-overlay':R/'v20-stage-proposal-review.v1/overlay/docs/coop/design-corrections/foundation/identity-schemas.v2.json'}
results=[]
def build_case(spec_domains,stage_domains):
 run,objects,blobs=F.build()
 seal=objects[run['evaluationSealId']][1];epid=seal['executionPlanId'];ep=copy.deepcopy(objects[epid][1])
 spec=C.parse(blobs[ep['stages'][0]['stageSpecDigest']]);spec['outputDomains']=spec_domains
 raw=C.canonical(spec);h=hashlib.sha256(raw).hexdigest();blobs[h]=raw
 ep['stages'][0]['stageSpecDigest']=h;ep['stages'][0]['outputDomains']=stage_domains
 F.rekey(objects,epid,ep,run)
 return run,objects,blobs
for name,p in schemas.items():
 target_schema=json.loads(p.read_text())
 for case,spec_domains,stage_domains in [('valid',['view'],['view']),('empty',[],[]),('unregistered',['View'],['View']),('wrong-prefix',['view2'],['view2']),('mismatched-registered',['fact'],['view'])]:
  row={'schema':name,'schemaSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'case':case}
  try:
   M.SCHEMA=json.loads(schemas['before'].read_text());row['phase']='fixture-construction'
   r,o,b=build_case(spec_domains,stage_domains)
   M.SCHEMA=target_schema;row['phase']='actual-close-run';row['runId']=M.close_run(r,o,b);row['result']='CLOSURE_ADMITTED'
  except Exception as e:row.update(result='REFUSED_OR_CRASHED',exception=type(e).__name__,detail=str(e).splitlines()[0])
  results.append(row)
checks=[]
def select(s,c):return next(r for r in results if r['schema']==s and r['case']==c)
checks.append({'id':'root-rejected-proposal-valid-graph-crashes','passed':select('rejected-root-proposal','valid').get('exception')=='KeyError' and select('rejected-root-proposal','valid').get('detail')=="'domain'"})
for c in ['valid','empty']:
 b=select('before',c);a=select('claude-overlay',c)
 checks.append({'id':'overlay-preserves-'+c,'passed':b.get('runId') is not None and b.get('runId')==a.get('runId')})
for c in ['unregistered','wrong-prefix']:
 checks.append({'id':'overlay-refuses-'+c,'passed':select('before',c)['result']=='CLOSURE_ADMITTED' and select('claude-overlay',c).get('exception')=='ValidationError'})
for n in ['before','claude-overlay']:
 checks.append({'id':n+'-preserves-domain-equality-guard','passed':select(n,'mismatched-registered').get('exception')=='AdmissionError' and select(n,'mismatched-registered').get('detail')=='STAGE_SPEC_OUTPUT_DOMAIN_JOIN'})
out={'standing':'Actual frozen19 close_run code and fixture constructors with fixture construction/reminting always using the original schema, then only the actual close_run call receives each exact in-memory schema. Supersedes v1 ambiguous failure-phase attribution; no source edits. Measures complete identity/schema/closure admission, not semantic proof replay or final merged20.','schemaInputs':{n:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in schemas.items()},'results':results,'checks':checks,'passed':all(x['passed'] for x in checks)}
(T/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(r['phase']=='actual-close-run' for r in results);assert out['passed']
