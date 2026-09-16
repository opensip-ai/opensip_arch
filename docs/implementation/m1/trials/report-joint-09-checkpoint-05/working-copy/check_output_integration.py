"""Required-output01 joined to full proposed envelope7/report inputs.

Uses the exact reference codec and owner admissions with synthetic writers;
this does not implement bounded streaming allocation, live signals or file I/O.
The output-failure policy and D9 prose successor remain unaccepted.
"""
from pathlib import Path
import copy,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
V=load('check_model_carriers');A=load('report_admission');M=load('models/report_model');J=load('document_joins');K=load('models/catalog');FJ=load('fit_join')
F=load('models/output_finalization');W=load('check_workflow5')
# The frozen checker verifies its full original/copy D9 source closure before
# loading the actual derivation owner. Its __main__ test runner is not executed.
V.read_unit('required-output','check.py')
for row in json.loads(V.read_unit('required-output','input-pins.json'))['files']:V.read_unit('required-output',row['copy'])
path=V.subjects['required-output']/'check.py';O=types.ModuleType('pinned_output_helpers');O.__file__=str(path)
exec(compile(path.read_bytes(),str(path),'exec'),O.__dict__)
ENV=FJ.ENV

def encode(envelope):
 try:
  V.validate(ENV,envelope)
  return V.C.canonical(envelope)
 except (V.C.ValidationError,V.C.AdmissionError) as error:
  raise F.SerializationFailure('admitted-codec-refusal') from error

def admitted_encoder(admitted_envelope):
 # Models a private already-admitted projection handle, not a public admission
 # constructor. Full report/interruption owner admission occurs before this.
 expected=copy.deepcopy(admitted_envelope)
 def callback(envelope):
  raw=encode(envelope)
  if not V.C.equal_typed(envelope,expected):
   raise F.SerializationFailure('admitted-projection-mismatch')
  return raw
 return callback

class OutputIntegrationTests(unittest.TestCase):
 def deliver(self,envelope,writer=None,encoder=None):
  before=copy.deepcopy(envelope);out=O.Writer(max_write=257) if writer is None else writer;diag=O.Writer()
  finalizer=F.Finalizer(envelope['termination'],O.FAULT,O.EXITS)
  result=finalizer.deliver(envelope,admitted_encoder(envelope) if encoder is None else encoder,out,diag)
  self.assertEqual(envelope,before);self.assertEqual(finalizer.commit_count,1)
  return finalizer,result,out,diag
 def test_all_complete_parent_reports_deliver_exact_admitted_envelope(self):
  docs=json.loads((HERE/'parent-bases.fixture.json').read_bytes());rows=[]
  for name,doc in docs.items():
   with self.subTest(name=name):
    admitted=A.admit(M.canonical(doc),V,M,J,K,FJ.owner_summary(V.C))
    _,result,out,diag=self.deliver(admitted['envelope'])
    self.assertEqual(result['delivery'],'complete');self.assertEqual(result['termination'],doc['envelope']['termination'])
    self.assertEqual(bytes(out.data),V.C.canonical(doc['envelope']));self.assertEqual(diag.calls,0)
    rows.append({'case':name,'bytes':len(out.data),'exitCode':result['exitCode']})
  self.assertEqual(len(rows),19)
  (HERE/'output-integration-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
 def interrupted(self):
  g=next(g for g in W.GOLDENS if g['scenario']=='signal-before-required-render')
  script=copy.deepcopy(g['ownerScript']);script['cancelAt']['stepId']=1
  record,_,availability=W.W.replay(W.base(g),script,V.C.canonical,V.T,W.validate)
  envelope=FJ.interrupted(record,g['selectionContext'],None,V.C,M,W.F,availability,V.validate)
  return record,envelope
 def test_composite_interruption_is_preserved_on_success_and_output_failure(self):
  record,envelope=self.interrupted();before=copy.deepcopy(record)
  _,result,out,_=self.deliver(envelope)
  self.assertEqual(result['exitCode'],130);self.assertEqual(bytes(out.data),V.C.canonical(envelope))
  self.assertEqual(envelope['advisoryReport']['state'],'unavailable-query-result')
  for writer in [O.Writer(limit=19),O.Writer(flush_fault=True)]:
   f,result,out,diag=self.deliver(envelope,writer)
   self.assertEqual(result,{'termination':O.FAULT,'exitCode':4,'delivery':'failed'})
   self.assertEqual(bytes(out.data),V.C.canonical(envelope)[:len(out.data)])
   self.assertEqual(bytes(diag.data),F.DIAGNOSTIC)
   for event in ['user-signal','transport-close','optional-delivery-failure']:self.assertEqual(f.after_commit(event),O.FAULT)
   with self.assertRaisesRegex(RuntimeError,'already-committed'):f.deliver(envelope,encode,out,diag)
  self.assertEqual(record,before)
 def test_semantic_source_refusal_writes_no_normal_bytes(self):
  _,envelope=self.interrupted();encoder=admitted_encoder(envelope);envelope.pop('advisoryReport')
  # Generic envelope shape has no command discriminator: it admits this
  # otherwise-valid Run envelope. Exact private projection custody must catch it.
  V.validate(ENV,envelope)
  _,result,out,diag=self.deliver(envelope,encoder=encoder)
  self.assertEqual(result['delivery'],'failed');self.assertEqual(result['exitCode'],4)
  self.assertEqual(out.calls,0);self.assertEqual(bytes(diag.data),F.DIAGNOSTIC)

 def test_real_schema_refusal_writes_no_normal_bytes(self):
  _,envelope=self.interrupted();encoder=admitted_encoder(envelope);envelope.pop('availability')
  _,result,out,diag=self.deliver(envelope,encoder=encoder)
  self.assertEqual(result['delivery'],'failed');self.assertEqual(out.calls,0)
  self.assertEqual(bytes(diag.data),F.DIAGNOSTIC)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OutputIntegrationTests))
 out={'standing':'Root full envelope7 admission + exact reference codec + required-output01 composition; synthetic sources/writers, no native maximum-size or live process qualification, policy unaccepted','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'output-integration-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())
