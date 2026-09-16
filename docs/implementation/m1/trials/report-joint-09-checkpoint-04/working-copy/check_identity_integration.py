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
  with R.world(V.read_unit,V.subjects) as parent, tempfile.TemporaryDirectory(prefix='opensip-joint09-identity-') as name:
   scratch=Path(name).resolve();expected={}
   for rel in json.loads(V.read_unit('history-selection','fixture-owner-files.json'))['files']:
    target=scratch/rel;target.parent.mkdir(parents=True,exist_ok=True)
    raw=parent['by_path'][str(parent['ARCH']/rel)];target.write_bytes(raw);expected[rel]=raw
   for rel,path in [(B.DC+'foundation/identity-schemas.v3.json',SCHEMA),(B.DC+'foundation/identity-model.v3.py',MODEL),(B.DC+B.PARAMETER_DOCUMENT,PARAM)]:
    raw=path.read_bytes();(scratch/rel).write_bytes(raw);expected[rel]=raw
   # Match the published transformation as JSON values and exact model bytes.
   schema_parent=parent['by_path'][str(parent['ARCH']/(B.DC+'foundation/identity-schemas.v3.json'))]
   self.assertEqual(json.loads(SCHEMA.read_bytes()),json.loads(B.successor_identity_schemas(schema_parent)))
   model_parent=parent['by_path'][str(parent['ARCH']/(B.DC+'foundation/identity-model.v3.py'))]
   self.assertEqual(MODEL.read_bytes(),B.transform(model_parent.decode(),B.OWNER_TRANSFORMS).encode())
   prior=importlib.machinery.SourceFileLoader.get_code;compiled=[]
   def verified(loader,fullname):
    path=Path(loader.path).resolve()
    if path.is_relative_to(scratch):
     rel=str(path.relative_to(scratch));raw=path.read_bytes();assert raw==expected[rel];compiled.append(rel);return compile(raw,str(path),'exec')
    return prior(loader,fullname)
   importlib.machinery.SourceFileLoader.get_code=verified
   try:
    foundation=scratch/B.DC/'foundation'
    ordinary=parent['load']('joint09_successor_fixture',foundation/'evaluator_graph_fixture.v3.py')
    replay=parent['load']('joint09_successor_replay',foundation/'evaluator_replay_model.v3.py')
    rel=B.DC+'foundation/evaluator_graph_fixture.v3.py';changed=B.transform(expected[rel].decode(),B.FIXTURE_TRANSFORMS).encode();expected[rel]=changed;(scratch/rel).write_bytes(changed)
    extended=parent['load']('joint09_successor_extended_fixture',scratch/rel)
    results=B.demonstrate(types.SimpleNamespace(F=parent['F'],R=parent['R']),types.SimpleNamespace(F=ordinary,Fx=extended,R=replay),F,hashlib.sha256(PARAM.read_bytes()).hexdigest())
   finally:importlib.machinery.SourceFileLoader.get_code=prior
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
