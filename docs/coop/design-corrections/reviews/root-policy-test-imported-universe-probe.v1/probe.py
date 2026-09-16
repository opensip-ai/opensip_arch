from pathlib import Path
import copy,hashlib,importlib.util,json
B=Path('/tmp/opensip-design-corrections');P=Path(__file__).parent
rows=[]
for label,source in [('frozen39',B/'candidate-subject.v39'),('author-correction',B/'claude-policy-test-known-hit-author.v1/work/source39')]:
 wf=source/'docs/coop/design-corrections/workflows';s=importlib.util.spec_from_file_location('root_import_universe_'+label.replace('-','_'),wf/'workflows_model.v3.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
 suites=json.loads((wf/'policy-test-cases.v3.json').read_bytes());base=copy.deepcopy(suites['currentSuite']);rule=next(r for r in base['candidatePolicy']['rules']if r['ruleId']=='runtime-hit');rule['subjectEnumeration']['universe']='typescript';rule['gate']=True;rule['severity']='error';base['candidatePolicy']['rules']=[rule];base['waivers']['waivers']=[]
 case=next(c for c in base['cases']if c['id']=='runtime-observed-hit-is-a-known-match');case['subject']['facts']=[f for f in case['subject']['facts']if f['relation']=='runtime-observation'];base['cases']=[case]
 for token in ['typescript','rust']:
  suite=copy.deepcopy(base);suite['cases'][0]['subject']['facts'][0]['universe']=token
  suite['cases'][0]['expectations'] = ([{'kind':'finding','ruleId':'runtime-hit','minCount':1},{'kind':'verdict','verdict':'fail'}] if token=='typescript' else [{'kind':'no-finding','ruleId':'runtime-hit'},{'kind':'verdict','verdict':'indeterminate'}])
  result,refusal=W.run_admitted_policy_test(suite);assert refusal is None and result['resolverAccepted'] is True
  c=result['results'][0];rows.append({'source':label,'factUniverse':token,'ruleUniverse':'typescript','result':c,'modelSha256':hashlib.sha256((wf/'policy_test_model.v3.py').read_bytes()).hexdigest()})
  (P/(label+'-'+token+'-suite.json')).write_text(json.dumps(suite,indent=2)+'\n')
report={'standing':'Root independently authored bounded imported-atom universe discrimination, no full Run or production qualification. No active author or frozen source changed.','rows':rows,'confirmedWrongUniverseKnownHit':all(bool(r['result']['findings']) for r in rows if r['factUniverse']=='rust'),'expected':'Same-universe observed hit remains a known gating finding. A runtime fixture fact of another registered universe must not occupy the evaluated subject per fixture factUniverse law; absence cannot be proved by this imported fixture, so no known finding and indeterminate.','sourceManifestSha256':'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'}
(P/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'confirmedWrongUniverseKnownHit':report['confirmedWrongUniverseKnownHit'],'outcomes':[(r['source'],r['factUniverse'],r['result']['observedVerdict'],len(r['result']['findings']))for r in rows]},indent=2))
