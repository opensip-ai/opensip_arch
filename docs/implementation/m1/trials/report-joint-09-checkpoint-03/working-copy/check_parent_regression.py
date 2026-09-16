"""Declared subset of unchanged report08 counterexamples on the new audit fixture."""
from pathlib import Path
import ast,copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');A=load(HERE/'report_admission.py','admission');M=load(HERE/'models/report_model.py','model')
F=load(HERE/'models/feature_model.py','feature');F.bind(V.C,M)
J=load(HERE/'document_joins.py','joins');K=load(HERE/'models/catalog.py','catalogue');Q=load(HERE/'fit_join.py','fit')
source=V.read_unit('report-projection','check.py')
names={'Refused','need','pointer_get','sha','apply_ops'}
nodes=[n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];assert {n.name for n in nodes}==names
ns={'copy':copy,'json':json,'hashlib':hashlib};exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-report08-mutations','exec'),ns)
fixture=json.loads((HERE/'complete-audit-features.fixture.json').read_bytes())
parent=json.loads(V.read_unit('report-projection','fixtures.json'))
ops={'set','remove','x-append-copy','x-remove-index','x-provenance-move','x-empty-registry','x-deep-rule-predicate','x-disclosure','x-history-copy-current-findings'}
cases=[c for c in parent['reportCases'] if c['base']=='audit-full' and all(o['op'] in ops for o in c['ops'])]
context=types.SimpleNamespace(M=M,builder=None)
results=[]


def admit(raw):return A.admit(raw,V,M,J,K,Q.owner_summary(V.C),feature=F)

class ParentTests(unittest.TestCase):
 def test_unchanged_counterexamples_against_joint_consumer(self):
  admit(M.canonical(fixture))
  for case in cases:
   with self.subTest(case=case['id']):
    raw=ns['apply_ops'](context,fixture,case['ops'])
    try:admit(raw);observed='accept'
    except Exception as error:observed=getattr(error,'code',type(error).__name__)
    expected=case['expect']
    if case['id']=='review-Q6-audit-envelope-labelled-analyze':
     # Its old featureStates literal now fails schema admission first. Keep
     # that observation, then rebase only the command's admitted feature list
     # so the original ledger-command counterexample remains reachable.
     expected='SCHEMA'
    row={'id':case['id'],'parentExpected':case['expect'],'expected':expected,'observed':observed,'passed':observed==expected};results.append(row)
    self.assertEqual(observed,expected)
    if case['id']=='review-Q6-audit-envelope-labelled-analyze':
     rebased=copy.deepcopy(case['ops'])
     current=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')=='analyze')
     next(o for o in rebased if o.get('path')=='/featureStates')['value']=copy.deepcopy(current['then']['properties']['featureStates']['const'])
     try:admit(ns['apply_ops'](context,fixture,rebased));got='accept'
     except Exception as error:got=getattr(error,'code',type(error).__name__)
     results.append({'id':case['id']+'-current-feature-list','adaptation':'Only replace the old command featureStates literal with its composed schema constant','expected':case['expect'],'observed':got,'passed':got==case['expect']})
     self.assertEqual(got,case['expect'])

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ParentTests))
 out={'standing':'Root declared unchanged report08 mutation subset on newly composed audit fixture; not entire194-case regression or independent review','parentCases':len(cases),'executions':len(results),'passed':result.wasSuccessful(),'rows':results,
      'selection':{'base':'audit-full','allowedOps':sorted(ops)},'remainingParentCases':len(parent['reportCases'])-len(cases)}
 (HERE/'parent-regression-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2));raise SystemExit(not result.wasSuccessful())
