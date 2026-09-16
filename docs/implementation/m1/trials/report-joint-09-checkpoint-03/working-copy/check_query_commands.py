"""All report query-command envelopes through unchanged typed summary owners."""
from pathlib import Path
import ast,copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');A=load(HERE/'report_admission.py','admission');M=load(HERE/'models/report_model.py','m')
J=load(HERE/'document_joins.py','j');K=load(HERE/'models/catalog.py','k');Q=load(HERE/'fit_join.py','q')
P=load(HERE/'parent_fixture_source.py','source')
parent=json.loads(V.read_unit('report-projection','fixtures.json'))
inventory=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'))
summary=Q.owner_summary(V.C)


def make(command,base):
 doc=copy.deepcopy(parent['bases'][base]);old=doc['envelope']
 # New envelope constructor over pinned synthetic domain fixtures, not a
 # stored-envelope migration function. Each domain summary is re-derived.
 envelope={k:copy.deepcopy(old[k]) for k in ['schemaFamily','kind','requestId','projectId','termination','exitCode','querySurface','queryRecord']}
 envelope['schemaMajor']=7
 envelope['query']=summary(envelope['querySurface'],envelope['queryRecord'],envelope)
 doc['envelope']=envelope
 ledger=doc['invocationLedger'];ledger['cancellation']={'requested':False,'phase':'none'}
 for step in ledger['steps']:
  if step['recorded']:
   step['attempts']=[V.T.project_attempt(3,a) for a in step['attempts']]
   step['attemptServiceTime']=V.T.summarize_attempts(step['attempts'])
  else:step['attemptServiceTime']={'state':'not-finalized','reason':'render-in-progress'}
 if doc['panels'].get('graph',{}).get('state')=='present':
  context,_=P.build(V.read_unit,M,V.report)
  doc['panels']=context['exploration'](envelope,command,False,ledger)
 # These commands do not carry a full analysis Run/Plan. Configuration and
 # Run descriptions remain explicit unavailable source states in this fixture.
 doc['panels'].update({k:{'state':'unavailable','reason':'evidence-purged'} for k in ['configuration','descriptions']})
 condition=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')==command)
 for key in ['featureStates','supportedReportViews']:doc[key]=copy.deepcopy(condition['then']['properties'][key]['const'])
 doc['budgetProfile']={k:copy.deepcopy(v['const']) for k,v in V.report['$defs']['BudgetProfileV1']['properties'].items()}
 doc['disclosures']=M.document_disclosures(doc['panels']);doc['disclosures']['explicitHistorySelection']=None
 row=next(c for c in inventory['commands'] if c['name']==command)
 text=M.static_parity_text(envelope,row,doc['disclosures']).encode()
 doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
 return doc

class QueryTests(unittest.TestCase):
 def test_four_query_command_documents_admit_and_render(self):
  rows={}
  for command,base in [('candidates','candidates-run'),('inspect','inspect-run'),('review-brief','review-brief-run'),('repair-preview','repair-preview')]:
   with self.subTest(command=command):
    doc=make(command,base)
    A.admit(M.canonical(doc),V,M,J,K,summary)
    rows[command]=doc
  (HERE/'query-commands.fixture.json').write_text(json.dumps(rows,indent=2)+'\n')
 def test_preview_identity_and_query_summary_joins_still_refuse_tampering(self):
  doc=make('repair-preview','repair-preview');A.admit(M.canonical(doc),V,M,J,K,summary)
  for change in ['id','applicable','count']:
   bad=copy.deepcopy(doc)
   if change=='id':bad['envelope']['queryRecord']['plan']['repairPlanId']='repairplan2:'+'0'*64
   elif change=='applicable':bad['envelope']['queryRecord']['preview']['applicable']=not bad['envelope']['queryRecord']['preview']['applicable']
   else:bad['envelope']['query']['items']+=1
   try:A.admit(M.canonical(bad),V,M,J,K,summary)
   except Exception as error:
    self.assertTrue(getattr(error,'code','').startswith('J-ENV-'),(change,error));continue
   self.fail('preview counterexample admitted: '+change)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(QueryTests))
 out={'standing':'Root four query-command complete fixture consumers with actual typed summary/identity owners; synthetic source premises, no native/store/browser qualification','groups':result.testsRun,'commands':4,'passed':result.wasSuccessful()}
 (HERE/'query-command-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
