"""Feature02 owner outputs under composed query4/report carriers; reference only."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');R=load(HERE/'retained_fixture.py','r')
M=load(HERE/'models/feature_model.py','features');RM=load(HERE/'models/report_model.py','report')
M.bind(V.C,RM)
A=load(HERE/'report_admission.py','admission');K=load(HERE/'models/catalog.py','catalogue');FJ=load(HERE/'fit_join.py','fit_join')
PP=load(HERE/'parent_projection.py','parent_projection')
P=load(HERE/'joint_placement.py','placement');S=load(HERE/'parent_fixture_source.py','parent_source');J=load(HERE/'document_joins.py','joins')
V.read_unit('report-evidence-design','build_fixtures.py')
B=load(V.subjects['report-evidence-design']/'build_fixtures.py','feature_builder')
fixture=json.loads(V.read_unit('report-evidence-design','fixtures.json'))
parameter=V.read_unit('report-evidence-design','owner/framework-recognition-plan.schema.v1.json')
sha=hashlib.sha256(parameter).hexdigest()
RID=V.report['$id'];BIG=4194304

class FeatureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.context=R.world(V.read_unit,V.subjects);cls.retained=cls.context.__enter__()
  relative='docs/coop/design-corrections/native/native_evidence_model.v2.py'
  pins=json.loads(V.read_unit('report-evidence-design','source-pins.json'))['files']
  pin=next(r for r in pins if r['path'].endswith('/'+relative))
  raw=(cls.retained['scratch']/relative).read_bytes();assert hashlib.sha256(raw).hexdigest()==pin['sha256']
  cls.native=cls.retained['load']('joint_feature_native',cls.retained['scratch']/relative)
  cls.worlds={};cls.panels={}
  for name in ['mixed','clean','integration','cross-universe-test','jest-configured']:
   data=B.assemble(copy.deepcopy(fixture['descriptions'][name]),M,cls.native,sha)
   world=M.World(data);M.admit_recognition_plan(world,data['recognitionRecord']);cls.worlds[name]=world
   resolution=fixture['resolutions']['mixed' if name in ['mixed','clean'] else 'integration']
   cls.panels[name]={'coupling':M.derive_coupling(world,budget=BIG,test_origin_state=M.test_origin_state_fn(world)),
     'symbolEvidence':M.derive_symbol_evidence(world,resolution,BIG)}
 @classmethod
 def tearDownClass(cls):cls.context.__exit__(None,None,None)
 def admit(self,name,panels):
  world=self.worlds[name];resolution=fixture['resolutions']['mixed' if name in ['mixed','clean'] else 'integration']
  V.validate(RID+'#/$defs/CouplingPanelV1',panels['coupling']);M.admit_coupling(panels['coupling'],world.run_id,BIG)
  V.validate(RID+'#/$defs/SymbolEvidencePanelV1',panels['symbolEvidence'])
  M.admit_symbol_evidence(panels['symbolEvidence'],{'projectId':world.project_id,'runId':world.run_id,'resolution':resolution,'graphResolution':resolution,'bounds':M.PUBLIC_BOUNDS,'budget':BIG})
 def test_five_unchanged_owner_worlds_admit_under_query4_and_report_composition(self):
  for name,panels in self.panels.items():
   with self.subTest(world=name):self.admit(name,panels)
  (HERE/'feature-panels.fixture.json').write_text(json.dumps(self.panels,indent=2)+'\n')
 def test_fresh_query_producers_never_emit_old_major(self):
  counts={'requests':0,'responses':0}
  def walk(node):
   if isinstance(node,dict):
    if node.get('schemaFamily')=='opensip.product.query':
     self.assertEqual(node['schemaMajor'],4);counts['responses' if 'items' in node else 'requests']+=1
    for value in node.values():walk(value)
   elif isinstance(node,list):
    for value in node:walk(value)
  walk(self.panels);self.assertGreater(counts['requests'],0);self.assertGreater(counts['responses'],0)
 def test_cross_universe_and_configured_jest_limitations_survive(self):
  cross=self.panels['cross-universe-test']['symbolEvidence'];jest=self.panels['jest-configured']['symbolEvidence']
  resolution=fixture['resolutions']['integration'];sid=next(r['subjectId'] for r in resolution if r.get('endpoint',{}).get('nativeSubjectId')=='ts:src/helper.ts#helper')
  row=next(r for r in cross['testReachability'] if r['subjectId']==sid)
  self.assertEqual(row['state'],'static-path-from-test-origin');self.assertEqual(row['origin']['endpoint']['universe'],B.UT)
  row=next(r for r in jest['testReachability'] if r['subjectId']==sid)
  self.assertEqual(row['state'],'not-found-incomplete');self.assertIn('test-origin-set-partial',row['blockers'])
  self.assertTrue(all(row['completeness'] in ['partial','none'] for p in self.panels.values() for row in p['symbolEvidence']['testOrigins']))
 def test_complete_audit_reissues_graph_queries_and_places_feature_panels(self):
  bases=json.loads(V.read_unit('report-projection','fixtures.json'))['bases']
  doc=copy.deepcopy(bases['audit-full'])
  terminal={name:{'state':'unavailable','reason':'evidence-purged'} for name in ['configuration','descriptions']}
  reserved={**terminal,**{name:copy.deepcopy(P.OMITTED) for name in ['symbolEvidence','coupling']}}
  parent_model=PP.bind(V.read_unit,RM,reserved,P)
  context,_=S.build(V.read_unit,parent_model,V.report)
  doc['envelope']=context['run_envelope']
  ledger=doc['invocationLedger'];ledger['cancellation']={'requested':False,'phase':'none'}
  for step in ledger['steps']:
   if step['recorded']:
    step['attempts']=[V.T.project_attempt(3,a) for a in step['attempts']]
    step['attemptServiceTime']=V.T.summarize_attempts(step['attempts'])
   else:step['attemptServiceTime']={'state':'not-finalized','reason':'render-in-progress' if step['kind']=='render' else 'step-result-not-recorded'}
  doc['documentProvenance']=copy.deepcopy(V.report['properties']['documentProvenance']['const'])
  doc['budgetProfile']={k:copy.deepcopy(v['const']) for k,v in V.report['$defs']['BudgetProfileV1']['properties'].items()}
  condition=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')=='audit')
  for k in ['supportedReportViews','featureStates']:doc[k]=copy.deepcopy(condition['then']['properties'][k]['const'])
  existing=context['exploration'](doc['envelope'],'audit',True,ledger)
  # Parent projection accounts for later reservations before any owner runs.
  cap=RM.effective_exploration_budget(doc['budgetProfile'],doc['envelope'],ledger,V.report['required'])
  world=self.worlds['integration'];resolution=fixture['resolutions']['integration']
  terminal={name:{'state':'unavailable','reason':'evidence-purged'} for name in ['configuration','descriptions']}
  placed,budgets=P.append(existing,{'symbolEvidence':lambda b:M.derive_symbol_evidence(world,resolution,b),
       'coupling':lambda b:M.derive_coupling(world,budget=b,test_origin_state=M.test_origin_state_fn(world))},terminal,doc['budgetProfile']['projectionPriority'],cap,RM)
  doc['panels']=placed
  doc['disclosures']=J.disclosures(placed,None,RM,V.H,world.run_id,lambda x:V.validate(V.history_schema['$id'],x))
  inventory=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'));command=next(c for c in inventory['commands'] if c['name']=='audit')
  text=RM.static_parity_text(doc['envelope'],command,doc['disclosures']).encode()
  doc['staticParity']={'format':RM.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
  V.validate(RID,doc);J.timing(ledger,V.T,V.C.equal_typed);M.admit_successor_placement(placed,cap);M.admit_panel_prerequisites(placed)
  M.admit_symbol_evidence(placed['symbolEvidence']['data'],{'projectId':world.project_id,'runId':world.run_id,'resolution':resolution,'graphResolution':placed['graph']['data']['subjectResolution'],'bounds':M.PUBLIC_BOUNDS,'budget':budgets['symbolEvidence']})
  M.admit_coupling(placed['coupling']['data'],world.run_id,budgets['coupling'])
  self.assertLessEqual(len(RM.canonical(placed)),cap)
  self.assertTrue(all(slot['request']['schemaMajor']==slot['response']['schemaMajor']==4 for slot in placed['graph']['data']['slots']))
  A.admit(RM.canonical(doc),V,RM,J,K,FJ.owner_summary(V.C),feature=M)
  (HERE/'complete-audit-features.fixture.json').write_text(json.dumps(doc,indent=2)+'\n')
  # Once an earlier panel is budget-omitted, later owners must not execute.
  calls=[];stopped=copy.deepcopy(existing);stopped['history']=copy.deepcopy(P.OMITTED)
  late,_=P.append(stopped,{'symbolEvidence':lambda b:calls.append('symbol'),'coupling':lambda b:calls.append('coupling')},terminal,doc['budgetProfile']['projectionPriority'],cap,RM)
  self.assertEqual(calls,[]);self.assertEqual(late['symbolEvidence'],P.OMITTED);self.assertEqual(late['coupling'],P.OMITTED)

 def test_feature_byte_omission_cannot_claim_a_smaller_hidden_allowance(self):
  doc=json.loads((HERE/'complete-audit-features.fixture.json').read_bytes())
  world=self.worlds['integration'];resolution=fixture['resolutions']['integration']
  full=self.panels['integration']['symbolEvidence'];small=M.derive_symbol_evidence(world,resolution,len(RM.canonical(full))-1)
  self.assertIsNotNone(small);self.assertGreater(small['metricsProjection']['omitted'],0)
  doc['panels']['symbolEvidence']['data']=small
  allowed=P.allocation(doc['panels'],'symbolEvidence',doc['budgetProfile']['projectionPriority'],doc['budgetProfile']['explorationMaxCanonicalBytes'],RM)
  self.assertLess(len(RM.canonical(small))+small['metricsProjection']['rejectedByteDelta'],allowed)
  with self.assertRaisesRegex(ValueError,'FEATURE-BYTE-OMISSION-CAUSE'):
   A.admit(RM.canonical(doc),V,RM,J,K,FJ.owner_summary(V.C),feature=M)

 def test_dense_coupling_retains_legitimate_shared_budget_omissions(self):
  doc=json.loads((HERE/'complete-audit-features.fixture.json').read_bytes())
  data=B.assemble(copy.deepcopy(fixture['descriptions']['dense-120']),M,self.native,sha)
  world=M.World(data);M.admit_recognition_plan(world,data['recognitionRecord'])
  self.assertEqual(world.run_id,doc['envelope']['run']['runId'])
  cap=doc['budgetProfile']['explorationMaxCanonicalBytes']
  panels,budgets=P.append(doc['panels'],{'coupling':lambda b:M.derive_coupling(world,budget=b,test_origin_state=M.test_origin_state_fn(world))},{},doc['budgetProfile']['projectionPriority'],cap,RM)
  self.assertEqual(panels['coupling']['state'],'present')
  self.assertGreater(panels['coupling']['data']['cellsProjection']['omitted'],0)
  self.assertEqual(P.allocation(panels,'coupling',doc['budgetProfile']['projectionPriority'],cap,RM),budgets['coupling'])
  doc['panels']=panels
  A.admit(RM.canonical(doc),V,RM,J,K,FJ.owner_summary(V.C),feature=M)
  (HERE/'dense-shared-budget-result.json').write_text(json.dumps({'standing':'Synthetic dense120 owner under composed shared budget; no performance/Run custody qualification',
    'panelBytes':len(RM.canonical(panels)),'cap':cap,'couplingAllowance':budgets['coupling'],
    'cellsProjection':panels['coupling']['data']['cellsProjection'],'passed':True},indent=2)+'\n')

 def test_document_counterexamples_refuse_in_joined_schema_and_owner(self):
  self.admit('mixed',self.panels['mixed'])
  for change in ['query-major','run','metrics-value','false-absence','count']:
   panels=copy.deepcopy(self.panels['mixed'])
   if change=='query-major':panels['symbolEvidence']['metrics'][0]['request']['schemaMajor']=3
   elif change=='run':panels['coupling']['runId']='run3:'+'0'*64
   elif change=='metrics-value':panels['symbolEvidence']['metrics'][0]['value']+=1
   elif change=='false-absence':panels['coupling']['absence']['absenceSupported']=True
   else:panels['coupling']['totals']['distinctFacts']+=1
   with self.subTest(change=change),self.assertRaises((M.Refusal,V.C.ValidationError)):self.admit('mixed',panels)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FeatureTests))
 out={'standing':'Root feature02 models and complete synthetic audit reports under the composed shared budget; no native query, performance or Run source custody qualification','groups':result.testsRun,'worlds':5,'passed':result.wasSuccessful()}
 (HERE/'feature-integration-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
