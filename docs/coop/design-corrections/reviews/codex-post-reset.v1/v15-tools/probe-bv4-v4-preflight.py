"""Root independently chosen pre-Plan boundary and malformed-shape controls. Execute only at a stable checkpoint."""
from pathlib import Path
import argparse,json,hashlib,importlib.util,copy
p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();b=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4');root=b/'work';dc=root/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checkpoint=b/a.checkpoint;r=json.loads(checkpoint.read_text());rows=r['delta']['againstFrozenV14']['changedFiles']
for row in rows:assert sha(root/row['path'])==row['afterSha256'],row['path']
out=a.out;out.mkdir(exist_ok=False)
s=importlib.util.spec_from_file_location('root_v4_native',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N);W=N.IM.workflow_admission()
def explicit(n):return {'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'inventory','languageMode':'ts-tsconfig','workspaceRoot':'apps/u%04d'%i,'required':True} for i in range(n)],'policyPackIds':[],'parameters':[]}
def units(n):return [{'rootPath':'apps/u%03d'%i,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(n)]
results=[]
def run(name,fn,expected):
 try:
  value=fn();actual='ADMIT';detail=None
 except N.ScopeRefusal as e:
  actual='ScopeRefusal';t=N.scope_refusal_termination(e);env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'c'*32,'termination':t,'exitCode':W.EXIT[t['class']],'errors':[t['domainDetail']]}
  W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/StepTermination',t);W.validate_import_record('workflows/schemas/command-envelope.schema.json','',env)
  detail={'observed':e.subject,'termination':t,'failureEnvelopeSchema':'ADMIT','requestId':env['requestId']}
 except Exception as e:actual=type(e).__name__;detail={'messagePrefix':str(e)[:180],'messageScalars':len(str(e))}
 results.append({'id':name,'expected':expected,'actual':actual,'holds':actual==expected,'evidence':detail})
for n in (0,1,1024):run('complete-explicit-'+str(n),lambda n=n:N.admit_analysis_spec(explicit(n)),'ADMIT')
run('complete-explicit-1025',lambda:N.admit_analysis_spec(explicit(1025)),'ScopeRefusal')
for n in (1,93):run('default-ts-'+str(n),lambda n=n:N.default_capability_selection(units(n),[]),'ADMIT')
run('default-ts-94',lambda:N.default_capability_selection(units(94),[]),'ScopeRefusal')
run('raw-retained-schema-1025-is-still-schema-validation',lambda:N.validate_foundation('analysis-spec',explicit(1025)),'ValidationError')
malformed={}
spec=explicit(1);del spec['requestedCapabilities'];malformed['missing-requested-capabilities']=spec
for label,value in [('null',None),('boolean',True),('integer',7),('short-string','bad'),('oversized-string','x'*1025),('object',{})]:
 spec=explicit(1);spec['requestedCapabilities']=value;malformed['wrong-array-type-'+label]=spec
spec=explicit(1);del spec['schemaVersion'];malformed['missing-schema-version']=spec
spec=explicit(1);spec['unexpected']=True;malformed['unknown-property']=spec
for label,spec in malformed.items():run(label,lambda spec=spec:N.admit_analysis_spec(spec),'ValidationError')
for row in rows:assert sha(root/row['path'])==row['afterSha256'],'Source changed during checkpoint probe'
report={'standing':'Root independently selected reference boundary probes on exact halted coauthor source. Synthetic requests and schema-admitted envelope, not actual host, renderer, invocation execution or retained Run closure. Raw retained-schema control only demonstrates schema behavior. No product qualification.','checkpointSha256':sha(checkpoint),'boundChangedSources':rows,'cases':results,'allHold':all(x['holds'] for x in results)}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'probe.py').write_bytes(Path(__file__).read_bytes());print(json.dumps({'cases':len(results),'allHold':report['allHold'],'failures':[x for x in results if not x['holds']]},indent=2))
