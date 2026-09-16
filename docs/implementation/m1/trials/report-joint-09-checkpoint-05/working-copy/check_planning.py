"""Every plannable builtin representative against invocation5 and owner DAG law."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');W=load(HERE/'workflow5_replay.py','w')
row=json.loads((HERE/'planning-composition-result.json').read_bytes())['output'];raw=(HERE/row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
planning=json.loads(raw);INV='urn:opensip:product-v1:workflows:evaluator3:invocation:5'
core,_=W.owned_core(V.C.canonical)


def validate(kind,value):
 V.validate(INV+{'step-params':'#/$defs/FitQueryFromAnalysisParams'}[kind],value)

class PlanningTests(unittest.TestCase):
 def test_all_plannable_representative_steps_and_relations(self):
  rows=[]
  for command,variants in planning['commands'].items():
   for variant in variants:
    if variant['status']!='plannable':continue
    with self.subTest(command=command,variant=variant['variant']):
     steps=[]
     for i,row in enumerate(variant['steps']):
      step={k:copy.deepcopy(row[k]) for k in ['kind','requirement','dependsOn','dependencyGate']}
      step.update(stepId=i,retryPolicy='none',params=copy.deepcopy(row['representativeParams']))
      V.validate_sub(row['paramsBinding'],step['params']);steps.append(step)
     base={'schemaFamily':'opensip.product.invocation','schemaMajor':5,'requestId':'req1_'+'1'*32,
          'workflow':{'kind':'builtin','name':command},'mode':{'interactive':False,'ci':True,'ephemeral':False},'orderedSteps':steps}
     V.validate(INV,base);core.validate_dag(steps);W.admit_fit_source_plan(base,validate)
     rows.append({'command':command,'variant':variant['variant'],'steps':len(steps)})
  self.assertEqual(len(rows),12)
  (HERE/'planning-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
 def test_source_bound_query_stays_fit_only(self):
  params=copy.deepcopy(planning['commands']['fit'][0]['steps'][1]['representativeParams'])
  base={'workflow':{'kind':'builtin','name':'analyze'},'orderedSteps':[{'kind':'query','params':params}]}
  with self.assertRaisesRegex(ValueError,'only to the selected fit'):W.admit_fit_source_plan(base,validate)
 def test_fit_binding_refuses_pre_analysis_concrete_request(self):
  step=planning['commands']['fit'][0]['steps'][1];V.validate_sub(step['paramsBinding'],step['representativeParams'])
  before=json.loads((HERE/'planning-composition-result.json').read_bytes())['fitStepBefore']['representativeParams']
  before['request']['schemaMajor']=4
  with self.assertRaises(V.C.ValidationError):V.validate_sub(step['paramsBinding'],before)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PlanningTests))
 out={'standing':'Root source planning representations and unchanged DAG law; no host scheduling/custody implementation','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'planning-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
