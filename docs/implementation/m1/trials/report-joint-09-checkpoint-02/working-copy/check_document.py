"""Complete document shape + composed addition joins over a replay-admitted Run.

Old graph/evidence panels are explicitly unavailable in this focused fixture;
this does not replace all original report semantic, budget or browser tests.
"""
from pathlib import Path
import ast,copy,json,types,unittest,hashlib
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');R=load(HERE/'retained_fixture.py','r')
J=load(HERE/'document_joins.py','j');M=load(HERE/'models/report_model.py','m')
W=load(HERE/'workflow5_replay.py','w');K=load(HERE/'models/catalog.py','k')
fixture=json.loads(V.read_unit('report-projection','fixtures.json'))
planning=json.loads(V.read_unit('report-projection','owner/builtin-step-planning.v1.json'))
inventory=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'))
command=next(c for c in inventory['commands'] if c['name']=='default')
INV='urn:opensip:product-v1:workflows:evaluator3:invocation:5'
# Execute the unchanged generic envelope and report-at-render ledger joins from
# report08 against the composed source registry. Fit's new path is separately
# covered by check_workflow5; it must not use report08's missing-report exception.
names={'Refused','need','pointer_get','admit_envelope','admit_ledger'}
nodes=[n for n in ast.parse(V.read_unit('report-projection','check.py')).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
assert {n.name for n in nodes}==names
legacy={'copy':copy,'EXIT':M.EXIT,'ENV6':'urn:opensip:product-v1:workflows:evaluator3:command-envelope:7'}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-report08-envelope-ledger-joins#selected-envelope7','exec'),legacy)
ctx=types.SimpleNamespace(M=M,reference=V.C,inventory5=inventory,registry=V.registry,documents=V.schemas,planning=planning,
                         derivations=json.loads((HERE/'joint-budget-derivation.json').read_bytes()))



def validate(kind,value):
 suffix={'planned-steps':'#/properties/orderedSteps','step-params':'#/$defs/FitQueryFromAnalysisParams','invocation':''}[kind]
 V.validate(INV+suffix,value)


def make_document(world):
    g=next(g for g in fixture['interruptionGoldens']['scenarios'] if g['id']=='default/primary/signal-before-required-render')
    base={k:copy.deepcopy(v) for k,v in g['invocationRecord'].items() if k not in ['stepResults','termination','terminationEmitted','cancellation']}
    base.update(schemaMajor=5,projectId=world['pid'])
    script={'0':[{'event':'completed','result':world['result'],'clockSamples':{'startNs':1000,'endNs':7001000}}],
      '1':[{'event':'completed','result':{'kind':'render','format':'html','rendererVersion':1,'bytes':0,'truncation':False,'written':True}}]}
    record,code,_=W.replay(base,script,V.C.canonical,V.T,validate)
    ledger=W.ledger(record,{0:'primary-analysis',1:'render'},'primary',V.T,M,V.report['$defs']['InvocationLedgerV1'])
    # Reconstruct the reference snapshot before the synthetic render observation.
    # No product delivery has taken place; bytes=0 above is not a real receipt.
    step=ledger['steps'][1]
    ledger['steps'][1]={k:copy.deepcopy(v) for k,v in step.items() if k in ['stepId','kind','requirement','dependsOn','dependencyGate','planRole']}
    ledger['steps'][1].update(recorded=False,attemptServiceTime={'state':'not-finalized','reason':'render-in-progress'})
    ledger['missingChildren']=M.missing_children(ledger['steps'])
    doc=copy.deepcopy(fixture['bases']['default-run'])
    doc['envelope']={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'run','requestId':record['requestId'],'projectId':world['pid'],
        'termination':record['termination'],'exitCode':code,'run':world['result'],'availability':{'stepCount':0,'totalNoticeCount':0,'steps':[]}}
    doc['invocationLedger']=ledger
    # Host source loss is an explicit fixture input. No unavailable source is
    # promoted to an empty evidence collection or reconstructed from latest.
    doc['panels']={k:{'state':'unavailable','reason':'evidence-purged'} for k in ['evidence','graph','history','catalog','configuration','descriptions']}
    plan=world['objects'][world['run']['planId']][1]
    config=V.C.parse(world['blobs'][plan['resolvedConfigDigest']])
    disclosure=V.D.project(world['run']['planId'],plan,config,V.policy,V.C,V.identity,V.config_schema)
    doc['panels']['configuration']={'state':'present','data':disclosure}
    condition=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')=='default')
    for key in ['supportedReportViews','featureStates']:doc[key]=copy.deepcopy(condition['then']['properties'][key]['const'])
    doc['budgetProfile']={k:copy.deepcopy(v['const']) for k,v in V.report['$defs']['BudgetProfileV1']['properties'].items()}
    doc['disclosures']=J.disclosures(doc['panels'],None,M,V.H,world['rid'],lambda v:V.validate(V.history_schema['$id'],v))
    refresh_static(doc)
    return doc,record,plan


def refresh_static(doc):
 text=M.static_parity_text(doc['envelope'],command,doc['disclosures']).encode()
 doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
 return text


def admit(doc):
 V.validate(V.report['$id'],doc)
 legacy['admit_envelope'](ctx,doc['envelope'],doc['command'],steps=doc['invocationLedger']['steps'])
 legacy['admit_ledger'](ctx,doc,doc['envelope'],doc['command'])
 J.additions(doc,doc['envelope']['run']['runId'],doc['envelope']['run'],None,M,V.H,V.T,K,V.C,lambda v:V.validate(V.history_schema['$id'],v))
 text=M.static_parity_text(doc['envelope'],command,doc['disclosures']).encode()
 if doc['staticParity']!={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}:raise ValueError('STATIC-PARITY-DIGEST')
 if M.invocation_aggregate(doc['invocationLedger']['steps'],doc['invocationLedger']['cancellation'])!=doc['envelope']['termination']:raise ValueError('AGGREGATE-JOIN')
 budget=doc['budgetProfile']
 for value,limit in [(doc,budget['documentMaxBytes']),(doc['envelope'],budget['envelopeMaxCanonicalBytes']),(doc['invocationLedger'],budget['ledgerMaxBytes']),(doc['panels'],budget['explorationMaxCanonicalBytes'])]:
  if len(M.canonical(value))>limit:raise ValueError('BYTE-BOUND')
 return doc

class DocumentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.context=R.world(V.read_unit,V.subjects);cls.world=cls.context.__enter__()
  cls.doc,cls.record,cls.plan=make_document(cls.world)
 @classmethod
 def tearDownClass(cls):cls.context.__exit__(None,None,None)
 def test_complete_document_joins_configuration_to_actual_replayed_plan(self):
  doc=admit(copy.deepcopy(self.doc));self.assertEqual(doc['panels']['configuration']['data']['source']['planId'],self.world['run']['planId'])
  self.assertEqual(doc['invocationLedger']['steps'][0]['attemptServiceTime'],{'state':'measured','attemptCount':1,'milliseconds':7})
  (HERE/'complete-default.fixture.json').write_text(json.dumps(doc,indent=2)+'\n')
 def test_explicit_current_and_missing_history_in_complete_document(self):
  doc=copy.deepcopy(self.doc);current=self.world['rid'];other='run3:'+'f'*64
  selection=V.H.plan_selection(V.H.admit_request([other,current],'html'),current)
  def lookup(rid):
   return {'query':V.H.QUERY.unavailable(self.world['pid'],rid,'purged'),'history':{'state':'unavailable','runId':rid,'availability':'purged'}}
  rows=V.H.resolve_slots(selection,self.world['pid'],lookup,lambda x:V.validate(V.query_schema['$id']+'#/$defs/GraphQueryResponseV1',x),lambda x:V.validate(V.history_schema['$id']+'#/$defs/RetainedHistorySlotV1',x))
  panel={'selection':selection,'runs':rows,'provenance':copy.deepcopy(V.history_schema['properties']['provenance']['const'])}
  doc['panels']['history']={'state':'present','data':panel}
  doc['disclosures']=J.disclosures(doc['panels'],selection,M,V.H,current,lambda x:V.validate(V.history_schema['$id'],x));text=refresh_static(doc)
  admit(doc);self.assertIn(b'disclosure.explicitHistorySelection:',text)
  self.assertIsNone(doc['disclosures']['historyPriorRunsInSnapshotHostAsserted'])
  # Mandatory requested list survives omission of the optional history panel.
  doc['panels']['history']={'state':'unavailable','reason':'evidence-purged'};refresh_static(doc);admit(doc)
  self.assertEqual(doc['disclosures']['explicitHistorySelection'],selection)
 def test_internal_join_mutations_are_refused(self):
  admit(copy.deepcopy(self.doc))
  for change in ['plan','duration','unrecorded','disclosure','static']:
   d=copy.deepcopy(self.doc)
   if change=='plan':d['panels']['configuration']['data']['source']['planId']='plan2:'+'0'*64
   elif change=='duration':d['invocationLedger']['steps'][0]['attemptServiceTime']['milliseconds']=8
   elif change=='unrecorded':d['invocationLedger']['steps'][1]['attemptServiceTime']['reason']='step-result-not-recorded'
   elif change=='disclosure':d['disclosures']['graphPlannedSubjects']=1
   else:d['staticParity']['textBytes']+=1
   with self.subTest(change=change),self.assertRaises((ValueError,V.C.ValidationError,legacy['Refused'])):admit(d)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DocumentTests))
 out={'standing':'Root complete document shape and additional semantic joins over actual close_run reference; synthetic sources, no product/browser/Claude acceptance',
      'groups':result.testsRun,'passed':result.wasSuccessful(),'limits':['Original graph/evidence/catalog panels are unavailable fixture states','Full original report admission regression and mutation controls remain pending','No store, live timing or renderer delivery qualification']}
 (HERE/'document-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
