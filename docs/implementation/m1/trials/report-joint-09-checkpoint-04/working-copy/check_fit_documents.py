"""Complete non-interrupted fit report candidates, with retained completion page.

All executions here are pure reference replay over synthetic terminal results.
The report snapshot excludes its synthetic render completion; no HTML delivery
or live query/Run publisher has been implemented by this test.
"""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');W=load(HERE/'workflow5_replay.py','w');F=load(HERE/'models/fit_output.py','f')
Q=load(HERE/'fit_join.py','q');A=load(HERE/'report_admission.py','a');J=load(HERE/'document_joins.py','j')
M=load(HERE/'models/report_model.py','m');K=load(HERE/'models/catalog.py','k')
fixtures=json.loads(V.read_unit('report-projection','fixtures.json'))
golden=next(g for g in fixtures['interruptionGoldens']['scenarios'] if g['id']=='fit/primary/signal-before-required-render')
command=next(c for c in json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'))['commands'] if c['name']=='fit')
INV='urn:opensip:product-v1:workflows:evaluator3:invocation:5'


def validate(kind,value):
 V.validate(INV+{'planned-steps':'#/properties/orderedSteps','step-params':'#/$defs/FitQueryFromAnalysisParams','invocation':''}[kind],value)


def make(name):
 doc=copy.deepcopy(fixtures['bases'][name]);base={k:copy.deepcopy(v) for k,v in golden['invocationRecord'].items() if k not in ['stepResults','termination','terminationEmitted','cancellation']}
 base['schemaMajor']=5;base['orderedSteps'][1]['params']={'kind':'query','operation':'candidate.list','sourceStep':0}
 source=copy.deepcopy(doc['envelope']['run']);page=copy.deepcopy(doc['envelope']['advisoryReport'])
 ephemeral=source['authority']=='ephemeral';base['mode']['ephemeral']=ephemeral
 base['orderedSteps'][0]['params']['durability']='ephemeral' if ephemeral else 'authoritative'
 if ephemeral:query={'kind':'query','items':0,'truncated':False,'completenessMet':False,'advisory':True}
 else:
  # Fresh query4 request constructor from the actual synthetic analysis result.
  page['request']={'schemaFamily':'opensip.product.query','schemaMajor':4,'projectId':base['projectId'],'view':{'runId':source['runId']},
       'operation':'candidate.list','params':{'includeSuppressed':False},'completeness':'best-effort','page':{'size':100}}
  query=Q.admit_page(page,base['projectId'],source['runId'],V.C,M,V.validate)
 script={'0':[{'event':'completed','result':source}],'1':[{'event':'completed','result':query}],
         '2':[{'event':'completed','result':{'kind':'render','format':'html','rendererVersion':1,'bytes':0,'truncation':False,'written':True}}]}
 record,code,availability=W.replay(base,script,V.C.canonical,V.T,validate)
 admit=lambda p,pid,rid:Q.admit_page(p,pid,rid,V.C,M,V.validate)
 handle=F.capture_completed(record,page,admit,V.C.equal_typed)
 envelope={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'run','requestId':record['requestId'],'projectId':record['projectId'],
          'termination':record['termination'],'exitCode':code,'run':source,'advisoryReport':handle['report'],'availability':availability([])}
 V.validate(Q.ENV,envelope)
 ledger=W.ledger(record,{0:'primary-analysis',1:'query',2:'render'},'primary',V.T,M,V.report['$defs']['InvocationLedgerV1'])
 render=ledger['steps'][2]
 ledger['steps'][2]={k:copy.deepcopy(v) for k,v in render.items() if k in ['stepId','kind','requirement','dependsOn','dependencyGate','planRole']}
 ledger['steps'][2].update(recorded=False,attemptServiceTime={'state':'not-finalized','reason':'render-in-progress'})
 ledger['missingChildren']=M.missing_children(ledger['steps'])
 doc.update(envelope=envelope,invocationLedger=ledger)
 doc['panels']={k:{'state':'unavailable','reason':'evidence-purged'} for k in ['evidence','graph','history','catalog','configuration','descriptions']}
 condition=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')=='fit')
 for key in ['featureStates','supportedReportViews']:doc[key]=copy.deepcopy(condition['then']['properties'][key]['const'])
 doc['budgetProfile']={k:copy.deepcopy(v['const']) for k,v in V.report['$defs']['BudgetProfileV1']['properties'].items()}
 doc['disclosures']=M.document_disclosures(doc['panels']);doc['disclosures']['explicitHistorySelection']=None
 text=M.static_parity_text(envelope,command,doc['disclosures']).encode()
 doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
 return doc,record,handle

class FitDocumentTests(unittest.TestCase):
 def test_completed_full_truncated_and_ephemeral_pages_admit_in_complete_reports(self):
  rows={}
  for name in ['fit-sealed','fit-sealed-truncated-150','fit-ephemeral']:
   with self.subTest(name=name):
    doc,record,handle=make(name);A.admit(M.canonical(doc),V,M,J,K,Q.owner_summary(V.C));rows[name]=doc
    self.assertEqual(doc['envelope']['advisoryReport'],handle['report'])
    self.assertEqual(record['stepResults'][1]['outcome'],'completed')
  (HERE/'complete-fit.fixture.json').write_text(json.dumps(rows,indent=2)+'\n')
 def test_completed_page_binding_cannot_be_replaced_with_another_request(self):
  doc,record,handle=make('fit-sealed');A.admit(M.canonical(doc),V,M,J,K,Q.owner_summary(V.C))
  for key,value in [('projectId','prj1-'+'0'*64),('view',{'runId':'run3:'+'0'*64}),('page',{'size':50})]:
   bad=copy.deepcopy(handle['report']);bad['request'][key]=value
   with self.subTest(key=key),self.assertRaises(F.BindingRefusal):
    F.capture_completed(record,bad,lambda p,pid,rid:Q.admit_page(p,pid,rid,V.C,M,V.validate),V.C.equal_typed)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FitDocumentTests))
 out={'standing':'Root complete fit reports with captured admitted-shape candidate pages; synthetic source replay, no actual HTML delivery or Run/query custody','groups':result.testsRun,'reportVariants':3,'passed':result.wasSuccessful()}
 (HERE/'fit-document-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
