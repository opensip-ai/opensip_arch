"""Tight parent-plus-new-panel projection against the shared allowance."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
V=load('check_model_carriers');M=load('models/report_model');P=load('joint_placement');PP=load('parent_projection');S=load('parent_fixture_source')
A=load('report_admission');J=load('document_joins');K=load('models/catalog');FJ=load('fit_join')
PRIORITY=[v for v in V.report['$defs']['BudgetProfileV1']['properties']['projectionPriority']['const']]

class SharedTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.doc=json.loads((HERE/'complete-audit-features.fixture.json').read_bytes())
  cls.terminal={n:{'state':'unavailable','reason':'evidence-purged'} for n in ['configuration','descriptions']}
  cls.reserved={**cls.terminal,**{n:copy.deepcopy(P.OMITTED) for n in ['symbolEvidence','coupling']}}
  facade=types.SimpleNamespace(**{k:v for k,v in vars(M).items() if not k.startswith('__')});captured=[]
  def capture(*args):captured.append(args);return {}
  facade.project_exploration=capture
  ctx,cls.material=S.build(V.read_unit,facade,V.report)
  ctx['exploration'](cls.doc['envelope'],'audit',True,cls.doc['invocationLedger'])
  cls.args=captured[0];cls.bound=PP.bind(V.read_unit,M,cls.reserved,P)
 def project(self,cap,sources=None):
  args=list(self.args);args[0]=copy.deepcopy(sources or args[0]);args[3]=cap
  args[5]=M.MockGraphOwner(self.material['facts'],self.material['template'])
  out=self.bound.project_exploration(*args)
  return out,args[5].calls
 def test_reserved_states_count_from_the_first_parent_panel(self):
  results=[]
  for cap in [1024,4096,8192,16384,65536]:
   with self.subTest(cap=cap):
    panels,calls=self.project(cap);again,again_calls=self.project(cap)
    self.assertEqual(M.canonical(panels),M.canonical(again));self.assertEqual(calls,again_calls)
    self.assertLessEqual(len(M.canonical(panels)),cap)
    for name in self.reserved:self.assertEqual(panels[name],self.reserved[name])
    stopped=False
    for name in PRIORITY:
     if name not in panels:continue
     if stopped:self.assertNotEqual(panels[name]['state'],'present')
     stopped=stopped or P.budget_omitted(name,panels[name])
    if panels['catalog']['state']=='omitted':self.assertEqual(calls,[])
    results.append({'cap':cap,'bytes':len(M.canonical(panels)),'graphCalls':len(calls),'states':{k:v['state'] for k,v in panels.items()}})
  (HERE/'shared-projection-cases.json').write_text(json.dumps(results,indent=2)+'\n')
 def test_full_allowance_dense_evidence_admits_complete_report(self):
  sources=copy.deepcopy(self.args[0]);entry=sources['evidence']['entries'][0]
  sources['evidence']['entries']=[]
  for i in range(5000):
   value=copy.deepcopy(entry);value['key']['subjectScopeCommitment']='sha256:'+hashlib.sha256(str(i).encode()).hexdigest()
   sources['evidence']['entries'].append(value)
  cap=4194304;panels,calls=self.project(cap,sources)
  self.assertGreater(panels['evidence']['data']['entriesProjection']['omitted'],0)
  callbacks=[]
  panels,_=P.append(panels,{n:lambda allowed,n=n:callbacks.append(n) for n in ['symbolEvidence','coupling']},self.terminal,PRIORITY,cap,M)
  self.assertLessEqual(len(M.canonical(panels)),cap)
  doc=copy.deepcopy(self.doc);doc['panels']=panels
  doc['disclosures']=J.disclosures(panels,None,M,V.H,doc['envelope']['run']['runId'],lambda v:V.validate(V.history_schema['$id'],v))
  inventory=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'));command=next(c for c in inventory['commands'] if c['name']=='audit')
  text=M.static_parity_text(doc['envelope'],command,doc['disclosures']).encode()
  doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
  A.admit(M.canonical(doc),V,M,J,K,FJ.owner_summary(V.C))
  (HERE/'shared-projection-dense-result.json').write_text(json.dumps({'standing':'Synthetic evidence projection; no retained source or performance qualification','bytes':len(M.canonical(panels)),'projection':panels['evidence']['data']['entriesProjection'],'graphCalls':len(calls),'lateCallbacks':callbacks,'passed':True},indent=2)+'\n')
 def test_overlapping_or_impossible_reservation_refuses(self):
  with self.assertRaisesRegex(ValueError,'reserved panel states'):self.project(1)
  bad=PP.bind(V.read_unit,M,{'catalog':P.OMITTED},P)
  with self.assertRaisesRegex(ValueError,'overlap'):bad.project_exploration(*self.args)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SharedTests))
 out={'standing':'Root shared parent/new projection checks; not host source custody or product qualification','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'shared-projection-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())
