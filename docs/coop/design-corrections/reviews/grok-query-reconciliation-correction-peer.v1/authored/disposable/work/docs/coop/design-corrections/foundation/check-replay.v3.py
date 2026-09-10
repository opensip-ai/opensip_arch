"""Actual retained native/identity admission followed by complete evaluator3 replay.

Synthetic extraction inputs; does not qualify a compiler, provider or real repository.
Mutants are fully reminted output graphs, and must pass owner closure admission before
semantic replay rejects them. Same-count mutations are deliberately included.
"""
import base64,copy,hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,file):
 s=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
F=load('replay_fixture3','evaluator_graph_fixture.v3.py');R=load('replay_reference3','evaluator_replay_model.v3.py');E=R.E;M=R.M;C=M.C

def canonical_sets(value):
 if type(value) is dict:
  for k,v in value.items():
   canonical_sets(v)
   if k in ('findingIds','waivedFindingIds','evidenceRefs','inputRefs','evaluationInputRefs','scopeIds','coverageIds','matchingFactIds','uncertainFactIds','matchingImportRows','uncertainImportRows','deficiencies'):value[k]=E.cset(v)
   if k=='predicateProofs':value[k]=sorted(v,key=lambda x:tuple(x[t].encode() for t in ('ruleId','subjectId','predicateId')))
 elif type(value) is list:
  for x in value:canonical_sets(x)
 return value

def seal(graph,result,objects,blobs):
 objects=copy.deepcopy(objects);blobs=copy.deepcopy(blobs);objects.update(result['objects']);blobs.update(result['blobs']);i=graph['inputs']
 def add(domain,fields):
  value={'schemaVersion':3,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
 evidence=add('semantic-evidence',{'planId':i['planId'],'viewIds':graph['viewIds'],'coverageIds':graph['coverageIds'],'importIds':i['plan']['importIds'],'findingIds':result['proof']['findingIds'],'proofBundleId':result['proofBundleId']})
 sid=add('evaluation-seal',{'planId':i['planId'],'executionPlanId':i['executionPlanId'],'evidenceId':evidence,'evaluatorClosure':i['evaluatorClosure'],'policyDigest':i['plan']['policyDigest'],'proofBundleId':result['proofBundleId'],'verdict':result['proof']['verdict']})
 run={'schemaVersion':3,'projectId':graph['snapshot']['projectId'],'snapshotId':i['plan']['snapshotId'],'planId':i['planId'],'evidenceId':evidence,'evaluationSealId':sid,'capabilityManifestId':i['plan']['capabilityManifestId']}
 return run,objects,blobs

def positive(**options):
 g=F.build_file_inputs(**options);seed,objects,blobs,_=F.seal_fixture(g);_,owner=M.open_run_closure(seed,objects,blobs)
 i=g['inputs'];result=R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner)
 return seal(g,result,objects,blobs)

def remint_finding(run,objects,blobs,change):
 run=copy.deepcopy(run);objects=copy.deepcopy(objects);blobs=copy.deepcopy(blobs)
 evidence=objects[run['evidenceId']][1];seal=objects[run['evaluationSealId']][1];proof=objects[seal['proofBundleId']][1]
 fid=proof['findingIds'][0];finding=copy.deepcopy(objects[fid][1]);change(finding,blobs)
 newfid=M.identifier('finding',finding);objects[newfid]=('finding',finding)
 def replace(value):
  if type(value) is str:return newfid if value==fid else value
  if type(value) is list:return [replace(x) for x in value]
  if type(value) is dict:return {k:replace(v) for k,v in value.items()}
  return value
 proof=canonical_sets(replace(copy.deepcopy(proof)));pid=M.identifier('proof-bundle',proof);objects[pid]=('proof-bundle',proof)
 evidence=canonical_sets(replace(copy.deepcopy(evidence)));evidence['proofBundleId']=pid;eid=M.identifier('semantic-evidence',evidence);objects[eid]=('semantic-evidence',evidence)
 seal=copy.deepcopy(seal);seal['proofBundleId']=pid;seal['evidenceId']=eid;sid=M.identifier('evaluation-seal',seal);objects[sid]=('evaluation-seal',seal)
 run['evidenceId']=eid;run['evaluationSealId']=sid
 return run,objects,blobs

def remint_proof(run,objects,blobs,change):
 run=copy.deepcopy(run);objects=copy.deepcopy(objects);blobs=copy.deepcopy(blobs)
 evidence=copy.deepcopy(objects[run['evidenceId']][1]);seal=copy.deepcopy(objects[run['evaluationSealId']][1]);proof=copy.deepcopy(objects[seal['proofBundleId']][1])
 change(proof,objects,blobs);canonical_sets(proof)
 pid=M.identifier('proof-bundle',proof);objects[pid]=('proof-bundle',proof)
 evidence['proofBundleId']=pid;eid=M.identifier('semantic-evidence',evidence);objects[eid]=('semantic-evidence',evidence)
 seal.update(proofBundleId=pid,evidenceId=eid,verdict=proof['verdict']);sid=M.identifier('evaluation-seal',seal);objects[sid]=('evaluation-seal',seal)
 run.update(evidenceId=eid,evaluationSealId=sid)
 return run,objects,blobs

def main():
 rows=[];exports={};base=positive();exports['complete-file-positive']=base;actual=R.replay(*base);rows.append({'case':'complete-file-positive','ownerAdmission':'ADMIT','replay':actual})
 def parameter_change(finding,blobs):
  p=C.parse(blobs[finding['parameterDigest']]);p['parameters']['matchingFactCount']+=1;raw=C.canonical(p);d=hashlib.sha256(raw).hexdigest();blobs[d]=raw;finding['parameterDigest']=d
 def message_change(finding,blobs):
  p=C.parse(blobs[finding['parameterDigest']]);p['messageCode']='different-message';raw=C.canonical(p);d=hashlib.sha256(raw).hexdigest();blobs[d]=raw;finding['parameterDigest']=d;finding['messageCode']='different-message'
 changes={
  'same-count-severity':lambda f,b:f.update(severity='warning'),
  'same-count-message':message_change,
  'same-count-parameter':parameter_change,
  'same-count-missing-citation':lambda f,b:f.update(evidenceRefs=[]),
 }
 for name,change in changes.items():
  mutant=remint_finding(*base,change);exports[name]=mutant
  rid=M.open_run_closure(*mutant)[0]
  try:R.replay(*mutant)
  except Exception as exc:
   if 'EVALUATOR_COMPLETE_PROOF_REPLAY' not in str(exc):raise
   rows.append({'case':name,'ownerAdmission':'ADMIT','remintedRunId':rid,'replay':'REFUSE','reason':str(exc)})
  else:raise AssertionError('semantic mutant accepted:'+name)
 for name,change in [
  ('same-count-invented-waiver',lambda p,o,b:p.update(waivedFindingIds=[p['findingIds'][0]])),
  ('same-count-omitted-enumeration-subject',lambda p,o,b:p['ruleResults'][0]['enumeration']['selectedSubjectIds'].pop()),
 ]:
  mutant=remint_proof(*base,change);rid=M.open_run_closure(*mutant)[0]
  try:R.replay(*mutant)
  except Exception as exc:
   if 'EVALUATOR_COMPLETE_PROOF_REPLAY' not in str(exc):raise
   rows.append({'case':name,'ownerAdmission':'ADMIT','remintedRunId':rid,'replay':'REFUSE','reason':str(exc)})
  else:raise AssertionError('semantic mutant accepted:'+name)
  exports[name]=mutant
 for name,options,want,count in [
  ('explicit-empty-required-native-work',{'complete_required_native':True},'fail',3),
  ('two-universes-six-full-findings',{'multiple_universes':True},'fail',6),
  ('file-none',{'atom_override':{'op':'none','relation':'file','minResolution':'enumerated','filters':[]}},'pass',0),
  ('file-count-at-most-zero',{'atom_override':{'op':'count-at-most','relation':'file','minResolution':'enumerated','filters':[],'n':0}},'pass',0),
  ('file-all-covered',{'atom_override':{'op':'all-covered','relation':'file','minResolution':'enumerated','filters':[]}},'fail',3),
  ('nongating-live-findings',{'gate':False},'pass',3),
  ('disabled-rule',{'enabled':False},'pass',0),
  ('budget-exhausted',{'budget_limit':1},'indeterminate',0),
  ('selected-scope-document',{'scope_document':{'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**'],'exclude':[]}},'fail',1),
  ('complete-empty-path-selection',{'enumeration_filter':{'include':['absent/**']}},'pass',0),
  ('filter-whole-segment-glob',{'atom_override':{'op':'exists','relation':'file','minResolution':'enumerated','filters':[{'field':'subject','cmp':'glob','value':'src/**'}]}},'fail',1),
 ]:
  graph=positive(**options);actual=R.replay(*graph)
  assert (actual['verdict'],actual['findingCount'])==(want,count),(name,actual)
  if options.get('multiple_universes'):
   run,objects,blobs=graph;proof=objects[objects[run['evaluationSealId']][1]['proofBundleId']][1];findings=[objects[fid][1] for fid in proof['findingIds']]
   assert len({f['subjectId'] for f in findings})==6 and len({f['fingerprint'] for f in findings})==3
   actual['distinctSubjects']=6;actual['distinctFingerprints']=3
  exports[name]=graph
  rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual})
 window={'startUtc':'2026-08-01T00:00:00Z','endUtc':'2026-08-02T00:00:00Z'}
 runtime={'kind':'runtime','payload':{'payloadDomain':'workflow.import-payload.runtime.v1','format':'v8-json','observationWindow':window,'observedPopulation':'synthetic','mappingGaps':[],'subjects':[{'path':'src/index.ts','observability':'observed-hit','hits':2}]},'observation':{'window':window,'population':'synthetic'}}
 for name,op,partial,required,want,count in [
  ('runtime-known-hit', 'exists',False,True,'fail',1),
  ('runtime-missing-subject-negative', 'none',False,True,'indeterminate',0),
  ('runtime-partial-known-hit', 'exists',True,True,'fail',1),
  ('runtime-partial-all-covered', 'all-covered',True,True,'indeterminate',0),
  ('runtime-optional-unknown', 'none',False,False,'pass',0),
 ]:
  item=copy.deepcopy(runtime)
  if partial:item['observation'].update(completeness='partial',omissions=['fixture omitted observations'])
  atom={'op':op,'relation':'runtime-observation','minResolution':'observed','filters':[],'evidence':'runtime'}
  graph=positive(atom_override=atom,import_specs=[item],evidence_use=[{'kind':'runtime','requirement':'required' if required else 'optional'}]);actual=R.replay(*graph)
  assert (actual['verdict'],actual['findingCount'])==(want,count),(name,actual)
  exports[name]=graph
  rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual})
 history={'kind':'history','payload':{'payloadDomain':'workflow.import-payload.history.v1','vcsSystem':'git','revisionRange':{'from':None,'to':'a'*40,'commitCount':0,'truncated':False},'collectionScope':'all-paths','subjects':[]},'observation':{'revisionRange':{'from':None,'to':'a'*40}}}
 for name,scope,partial,want,count in [('history-complete-zero','all-paths',False,'fail',3),('history-listed-zero','listed-paths',False,'indeterminate',0),('history-partial-zero','all-paths',True,'indeterminate',0)]:
  item=copy.deepcopy(history);item['payload']['collectionScope']=scope
  if partial:item['observation'].update(completeness='partial',omissions=['fixture truncated history']);item['payload']['revisionRange']['truncated']=True
  atom={'op':'none','relation':'history-change','minResolution':'observed','filters':[],'evidence':'history'}
  graph=positive(atom_override=atom,import_specs=[item],evidence_use=[{'kind':'history','requirement':'required'}]);actual=R.replay(*graph)
  assert (actual['verdict'],actual['findingCount'])==(want,count),(name,actual)
  exports[name]=graph
  rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual})
 # Complete replay of determinate boolean roots keeps nonblocking branch
 # diagnostics. Their mere presence must not change the admitted verdict.
 partial_history=copy.deepcopy(history)
 partial_history['observation'].update(completeness='partial',omissions=['fixture partial history'])
 partial_history['payload']['revisionRange']['truncated']=True
 for name,op,file_filter,want,count in [
  ('boolean-false-keeps-required-partial-diagnostics','and',[{'field':'subject','cmp':'glob','value':'absent/**'}],'pass',0),
  ('boolean-true-dominates-required-partial-diagnostics','or',[],'fail',3),
 ]:
  atom={'op':op,'operands':[{'op':'exists','relation':'file','minResolution':'enumerated','filters':file_filter},{'op':'none','relation':'history-change','minResolution':'observed','filters':[],'evidence':'history'}]}
  graph=positive(atom_override=atom,import_specs=[partial_history],evidence_use=[{'kind':'history','requirement':'required'}]);actual=R.replay(*graph)
  run,objects,blobs=graph;proof=objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]
  assert proof['ruleResults'][0]['deficiencies']
  assert (actual['verdict'],actual['findingCount'])==(want,count),(name,actual)
  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual})
 argv=C.canonical(['fixture-test']);empty=b'';selection={'mode':'full','completenessEstablished':True}
 test={'kind':'test','payload':{'payloadDomain':'workflow.import-payload.test.v1','producer':'independent-prepared','argvDigest':hashlib.sha256(argv).hexdigest(),'toolClosureId':None,'exitStatus':0,'signal':None,'timedOut':False,'stdoutDigest':hashlib.sha256(empty).hexdigest(),'stderrDigest':hashlib.sha256(empty).hexdigest(),'stdoutBytes':0,'stderrBytes':0,'outputTruncated':False,'tests':[{'testId':'fixture-test-1','subjectPath':'src/index.ts','outcome':'pass'}],'selection':selection},'observation':{'selection':selection},'extra_blobs':[argv,empty]}
 for name,rel,op,filters,partial,want,count in [
  ('test-row-exact-location','test-result','exists',[],False,'fail',1),
  ('test-process-coarse-scope','test-execution','exists',[{'field':'testResult','cmp':'eq','value':'passed'}],False,'fail',3),
  ('test-partial-no-false-all-covered','test-execution','all-covered',[],True,'indeterminate',0),
 ]:
  item=copy.deepcopy(test)
  if partial:item['observation'].update(completeness='partial',omissions=['fixture incomplete test selection'])
  atom={'op':op,'relation':rel,'minResolution':'observed','filters':filters,'evidence':'test'}
  graph=positive(atom_override=atom,import_specs=[item],evidence_use=[{'kind':'test','requirement':'required'}]);actual=R.replay(*graph)
  assert (actual['verdict'],actual['findingCount'])==(want,count),(name,actual)
  exports[name]=graph
  rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual})
 for name,options,want,count,unmatched in [
  ('symbol-with-detector-projection',{'symbol_rows':[{'nativeSubjectId':'symbol:x'}]},'fail',1,0),
  ('symbol-without-detector-projection',{'symbol_rows':[{'nativeSubjectId':'symbol:x','projectionAvailable':False}]},'fail',1,1),
  ('symbol-signature-collision',{'symbol_rows':[{'nativeSubjectId':'symbol:x1'},{'nativeSubjectId':'symbol:x2'}]},'fail',2,2),
  ('symbol-distinct-overload-signatures',{'symbol_rows':[{'nativeSubjectId':'symbol:x1'},{'nativeSubjectId':'symbol:x2','signatureTokens':['function','x','(','number',')']}]},'fail',2,0),
  ('export-membership-unknown',{'symbol_rows':[{'nativeSubjectId':'symbol:x','exported':'unknown'}],'select_exports':True},'indeterminate',0,0),
  ('partial-symbol-known-finding',{'symbol_rows':[{'nativeSubjectId':'symbol:x'}],'symbol_state':'partial'},'fail',1,1),
  ('disabled-required-symbol-partial',{'symbol_rows':[{'nativeSubjectId':'symbol:x'}],'symbol_state':'partial','enabled':False},'indeterminate',0,0),
 ]:
  graph=positive(**options);actual=R.replay(*graph);run,objects,blobs=graph;proof=objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]
  unmatched_count=sum(objects[fid][1]['fingerprint'] is None for fid in proof['findingIds'])
  assert (actual['verdict'],actual['findingCount'],unmatched_count)==(want,count,unmatched),(name,actual,unmatched_count)
  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual,'unmatchedFindings':unmatched_count})
 kind_controls=load('closure_field_kind_controls3','closure_field_kind_controls.v3.py')
 import types
 rows.extend(kind_controls.run_controls(types.SimpleNamespace(M=M,C=C,F=F,R=R,positive=positive)))
 report={'standing':'synthetic admitted native inputs; bounded complete-output replay and explicitly scoped closure-role controls; no real extraction qualification','passed':True,'count':len(rows),'checks':rows}
 if len(sys.argv)>1:
  if len(sys.argv)!=3 or sys.argv[1]!='--export-dir':raise SystemExit('usage: check-replay.v3.py [--export-dir NEW_DIRECTORY]')
  directory=Path(sys.argv[2]);directory.mkdir(parents=True,exist_ok=False)
  for name,(run,objects,blobs) in exports.items():
   artifact={'run':run,'objects':{k:{'domain':d,'descriptor':v} for k,(d,v) in sorted(objects.items())},'blobs':{k:base64.b64encode(v).decode('ascii') for k,v in sorted(blobs.items())}}
   (directory/(name+'.json')).write_text(json.dumps(artifact,indent=2)+'\n')
  report['exportCount']=len(exports)
 print(json.dumps(report,indent=2))
 return report,base
if __name__=='__main__':main()
