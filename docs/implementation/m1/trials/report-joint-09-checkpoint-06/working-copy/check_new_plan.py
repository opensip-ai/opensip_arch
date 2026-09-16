"""New-Plan registry binding, original fault ordering and public refusal routes."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
I=load('check_identity_integration');P=load('identity_fixture');A=load('new_plan_admission');V=I.V
NATIVE='urn:opensip:product-v1:native:evidence-schemas:v2';COMMON='urn:opensip:product-v1:workflows:evaluator3:common:4';ENV='urn:opensip:product-v1:workflows:evaluator3:command-envelope:7'

class NewPlanTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.context=P.models(V,I.B);cls.parent,cls.succ=cls.context.__enter__()
  cls.native=cls.succ.load('joint_new_plan_native',cls.succ.root/I.B.DC/'native/native_evidence_model.v2.py')
  raw=cls.succ.expected[I.B.DC+'native/native_evidence_model.v2.py']
  cls.bound=A.bind(raw,cls.native,cls.succ.R.M,I.F,V.schemas[NATIVE])
  _,_,blobs,graph=I.B.positive_run(cls.succ.F,cls.succ.R)
  cls.base=json.loads(blobs[graph['inputs']['plan']['analysisSpecDigest']])
  cls.parameter={'schemaDigest':hashlib.sha256(I.PARAM.read_bytes()).hexdigest(),'payloadDigest':'b'*64}
 @classmethod
 def tearDownClass(cls):cls.context.__exit__(None,None,None)
 def compiler(self,selected=False):
  spec=copy.deepcopy(self.base);spec['requestedCapabilities'][0]['languageMode']='ts-tsconfig'
  if selected:spec['parameters']=sorted(spec['parameters']+[copy.deepcopy(self.parameter)],key=V.C.canonical)
  return spec
 def test_syntax_only_old_spec_and_selected_compiler_spec_admit(self):
  for spec in [copy.deepcopy(self.base),self.compiler(True)]:
   before=copy.deepcopy(spec);self.assertEqual(self.bound.admit_new_plan(spec),before);self.assertEqual(spec,before)
 def test_compiler_missing_parameter_is_new_plan_only(self):
  spec=self.compiler();self.native.admit_analysis_spec(spec)
  with self.assertRaisesRegex(self.native.AdmissionError,A.KEY):self.bound.admit_new_plan(spec)
  # The old retained closure path remains independent of the new-Plan entry.
  self.assertEqual(self.succ.R.M.close_run(self.parent['run'],self.parent['objects'],self.parent['blobs']),self.parent['rid'])
 def test_selected_v3_registry_refuses_two_parameters_before_the_new_duty(self):
  spec=self.compiler(True);other=copy.deepcopy(self.parameter);other['payloadDigest']='c'*64
  spec['parameters']=sorted(spec['parameters']+[other],key=V.C.canonical)
  # The original v2 registry ignores this new row; that was the integration gap.
  self.native.admit_analysis_spec(spec)
  with self.assertRaisesRegex(self.succ.R.M.C.AdmissionError,'ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS'):
   self.bound.admit_new_plan(spec)
 def test_original_cardinality_schema_vocabulary_precedence_is_preserved(self):
  spec=self.compiler();spec['requestedCapabilities']=[{}]*1025
  with self.assertRaises(self.native.ScopeRefusal):self.bound.admit_new_plan(spec)
  spec=self.compiler();spec['requestedCapabilities']=None
  with self.assertRaises(self.native.C.ValidationError):self.bound.admit_new_plan(spec)
  spec=self.compiler();spec['requestedCapabilities'][0]['capabilityId']='invented-capability'
  with self.assertRaisesRegex(self.native.AdmissionError,'native.requested-capability-unregistered'):self.bound.admit_new_plan(spec)
 def test_public_origin_routes_are_complete_selected_envelopes(self):
  results=[]
  for origin,exit_code in [('externally-supplied-spec',2),('host-generated-internal-layer',4)]:
   termination=self.bound.public_termination_for(A.KEY,origin);errors=self.bound.failure_envelope_errors(A.KEY,origin)
   envelope={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'failure','requestId':'req1_'+'1'*32,
    'projectId':'prj1-'+'2'*64,'termination':termination,'exitCode':exit_code,'errors':errors,
    'availability':{'stepCount':0,'totalNoticeCount':0,'steps':[]}}
   V.validate(ENV,envelope);V.C.canonical(envelope)
   self.assertEqual(errors[0]['code'],A.KEY if exit_code==2 else 'HOST.INVARIANT_VIOLATED')
   results.append({'origin':origin,'envelope':envelope})
  for origin in [None,'external-configuration','producer-boundary']:
   with self.assertRaises(self.native.AdmissionError):self.bound.public_termination_for(A.KEY,origin)
  (HERE/'new-plan-route-cases.json').write_text(json.dumps(results,indent=2)+'\n')
 def test_every_existing_native_public_route_remains_identical(self):
  count=0
  for key,row in self.native.PUBLIC_ROUTE_REGISTRY['keys'].items():
   for origin in row['possibleOrigins']:
    with self.subTest(key=key,origin=origin):
     old=self.native.public_termination_for(key,origin);new=self.bound.public_termination_for(key,origin)
     self.assertEqual(new,old)
     if new is not None:
      V.validate(COMMON+'#/$defs/StepTermination',new)
      self.assertEqual(self.bound.failure_envelope_errors(key,origin),self.native.failure_envelope_errors(key,origin))
     count+=1
  self.assertGreater(count,0)
  (HERE/'new-plan-existing-route-count.json').write_text(json.dumps({'branches':count,'unchanged':True})+'\n')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NewPlanTests))
 out={'standing':'Root actual native pre-Plan helpers with selected v3 registry and appended recognition duty; synthetic specs and dependency bindings, no Plan publisher or product qualification','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'new-plan-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())
