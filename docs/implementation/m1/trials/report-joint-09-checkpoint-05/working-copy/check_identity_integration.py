"""Execute feature02's retained/new Run bridge on the actual composed bytes."""
from pathlib import Path
import copy,hashlib,importlib.machinery,json,tempfile,types,unittest
HERE=Path(__file__).resolve().parent

def load_local(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
V=load_local('check_model_carriers');R=load_local('retained_fixture');F=load_local('models/feature_model');M=load_local('models/report_model');F.bind(V.C,M)
raw=V.read_unit('report-evidence-design','identity_bridge.py');B=types.ModuleType('bridge');exec(compile(raw,'pinned-feature02-identity-bridge','exec'),B.__dict__)
PARAM=HERE/'composed-sources/framework-recognition-plan.schema.v1.json'
SCHEMA=HERE/'composed-sources/identity.proposed.v3.schema.json'
MODEL=HERE/'models/identity_model.proposed.v3.py'

class IdentityTests(unittest.TestCase):
 def test_selected_parameter_bytes_and_optional_schema_row_are_exact(self):
  original=V.read_unit('report-evidence-design','owner/framework-recognition-plan.schema.v1.json')
  self.assertEqual(PARAM.read_bytes(),original)
  result=json.loads((HERE/'identity-composition-result.json').read_bytes())
  self.assertEqual(result['parameterSha256'],hashlib.sha256(original).hexdigest())
  patch=json.loads(V.read_unit('report-evidence-design','owner/identity-parameter-registry-patch.v2.json'))
  schema=json.loads(SCHEMA.read_bytes());self.assertEqual(schema['x-opensip-payload-registry']['classes']['parameter']['rows'][B.PARAMETER_DOCUMENT],patch['ops'][0]['value'])
  self.assertNotIn('requiredForEvaluatorMajors',patch['ops'][0]['value'])
 def test_actual_retained_and_new_run_closure_use_composed_identity(self):
  fixture=load_local('identity_fixture')
  with fixture.models(V,B) as (parent,successor):
   results=B.demonstrate(types.SimpleNamespace(F=parent['F'],R=parent['R']),successor,F,hashlib.sha256(PARAM.read_bytes()).hexdigest())
   compiled=successor.compiled
   self.assertGreater(len(compiled),0,'verification hook must observe compiled successor sources')
   self.assertIn(B.DC+'foundation/identity-model.v3.py',compiled)
   self.assertEqual(results['predecessorRunClosedByPinnedModel']['result'],'admitted')
   self.assertEqual(results['predecessorRunClosedBySuccessorModel']['result'],'admitted')
   self.assertEqual(results['newPlanRunClosedBySuccessorModel']['result'],'admitted')
   self.assertEqual(results['newPlanRunClosedByPinnedPredecessorModel']['result'],'refused')
   self.assertEqual(results['newPlanRunWithParameterBytesLost']['result'],'refused')
   self.assertTrue(results['planIdsDiffer'])
   (HERE/'identity-bridge-result.json').write_text(json.dumps({'standing':'Actual reference close_run over synthetic evidence and composed optional identity successor; pre-Plan host/native and public routes not yet composed','results':results,'compiledPaths':sorted(set(compiled)),'passed':True},indent=2)+'\n')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IdentityTests))
 out={'standing':'Root composed identity/parameter closure checks; synthetic evidence, not product retention or admission qualification','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'identity-integration-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())
