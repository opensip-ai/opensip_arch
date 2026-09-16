"""Inventory every original report case against the joint positive constructions.

This first pass records differences rather than treating arbitrary rejection as
success. Obsolete fixtures and earlier schema failures need explicit disposition
and a replacement witness that reaches the intended semantic guard.
"""
from pathlib import Path
import ast,copy,hashlib,json,types
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');A=load(HERE/'report_admission.py','a');M=load(HERE/'models/report_model.py','m')
J=load(HERE/'document_joins.py','j');K=load(HERE/'models/catalog.py','k');Q=load(HERE/'fit_join.py','q')
S=load(HERE/'parent_fixture_source.py','s')
parent=json.loads(V.read_unit('report-projection','fixtures.json'));bases=json.loads((HERE/'parent-bases.fixture.json').read_bytes())
inventory=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'));summary=Q.owner_summary(V.C)
source=V.read_unit('report-projection','check.py')
names={'Refused','need','pointer_get','sha','apply_ops','slot_panel_bytes','worst_values'}
nodes=[n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];assert {n.name for n in nodes}==names
ns={'copy':copy,'json':json,'hashlib':hashlib,'EXIT':M.EXIT};exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-report08-all-mutations','exec'),ns)
common=V.schemas['urn:opensip:product-v1:workflows:evaluator3:common:4']
node=next(n for n in ast.parse(V.read_unit('report-projection','build_fixtures.py')).body if isinstance(n,ast.FunctionDef) and n.name=='pinned_termination')
fixture_ns={'json':json,'COMMON':types.SimpleNamespace(read_bytes=lambda:json.dumps(common).encode())}
exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned-report08-purge-witness','exec'),fixture_ns)

def refresh(doc):
 doc['disclosures']=M.document_disclosures(doc['panels']);doc['disclosures']['explicitHistorySelection']=None
 row=next(c for c in inventory['commands'] if c['name']==doc['command'])
 text=M.static_parity_text(doc['envelope'],row,doc['disclosures']).encode()
 doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
 return doc

_,material=S.build(V.read_unit,M,V.report)
ctx=types.SimpleNamespace(M=M,builder=types.SimpleNamespace(refresh=refresh,pinned_termination=fixture_ns['pinned_termination']),schema=V.report,
 budget={k:v['const'] for k,v in V.report['$defs']['BudgetProfileV1']['properties'].items()},material=material,owner=M.MockGraphOwner(material['facts'],material['template']))
ctx.worst=ns['worst_values'](ctx)
rows=[]
for case in parent['reportCases']:
 stage='construct'
 try:
  raw=ns['apply_ops'](ctx,bases[case['base']],case['ops']);stage='admit'
  A.admit(raw,V,M,J,K,summary);observed='accept'
 except Exception as error:observed=getattr(error,'code',type(error).__name__)
 rows.append({'id':case['id'],'stage':stage,'parentExpected':case['expect'],'observed':observed,'sameOutcome':observed==case['expect']})
 out={'standing':'Root all-parent inventory pass; differences remain unqualified until explicitly reconciled','cases':len(rows),'sameOutcome':sum(r['sameOutcome'] for r in rows),'differences':[r for r in rows if not r['sameOutcome']],'rows':rows}
 (HERE/'all-parent-inventory-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2));raise SystemExit(bool(out['differences']))
