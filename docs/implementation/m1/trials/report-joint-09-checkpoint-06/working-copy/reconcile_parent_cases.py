"""Explicitly rebase eight predecessor witnesses without weakening their guards."""
from pathlib import Path
import ast,copy,hashlib,json,types
HERE=Path(__file__).resolve().parent
source=(HERE/'check_all_parent_cases.py').read_bytes();assert source.count(b'\nrows=[]\n')==1
scope={'__file__':str(HERE/'check_all_parent_cases.py')}
exec(compile(source.split(b'\nrows=[]\n')[0],'joint-parent-case-setup','exec'),scope)
V,A,M,J,K,Q= [scope[k] for k in ['V','A','M','J','K','Q']]
feature=scope['load'](HERE/'models/feature_model.py','feature');feature.bind(V.C,M)
parent=scope['parent'];bases=scope['bases'];apply=scope['ns']['apply_ops'];ctx=scope['ctx'];summary=scope['summary']
raw=(HERE/'all-parent-inventory-result.json').read_bytes();prior=json.loads(raw)
assert prior['cases']==194 and len(prior['rows'])==194
expected={
 'feature-state-wrong-reason':('construct','StopIteration','entry-point-recognition placeholder was replaced by its typed evidence owner'),
 'feature-state-step-duration-dropped':('admit','accept','step-duration placeholder was replaced by required ledger timing fields'),
 'review-Q6-audit-envelope-labelled-analyze':('admit','SCHEMA','old command feature list is obsolete; use the current constant'),
 'ledger-analyze-planned-import-step':('admit','SCHEMA','inserted legacy step lacks new required timing fields'),
 'ledger-render-recorded':('admit','SCHEMA','invented completed render lacks new required timing fields'),
 'skipped-step-with-attempt':('admit','SCHEMA','invented legacy attempt lacks new required timing fields'),
 'skipped-record-erased':('admit','SCHEMA','unrecorded step needs the not-finalized timing state'),
 'graph-on-ephemeral-run':('admit','SCHEMA','inserted old graph contains query3; reissue it using the current mock owner'),
}
assert {r['id'] for r in prior['differences']}==set(expected)
rows=[]

def normalize_timing(step):
 projections=[]
 for a in step['attempts']:
  projections.append(V.T.project_attempt(3,a))
 step['attempts']=projections;step['attemptServiceTime']=V.T.summarize_attempts(projections)

for old in prior['differences']:
 name=old['id'];stage,outcome,reason=expected[name]
 assert (old['stage'],old['observed'])==(stage,outcome)
 case=next(c for c in parent['reportCases'] if c['id']==name)
 if name=='feature-state-wrong-reason':
  assert 'entry-point-recognition' not in V.report['$defs']['FeatureId']['enum']
  doc=json.loads((HERE/'complete-audit-features.fixture.json').read_bytes())
  # The successor has actual entry recognition, rather than an unavailable
  # feature placeholder. A fabricated state must fail its closed schema.
  assert doc['panels']['symbolEvidence']['data']['entryRecognition']['state']!='no-admitted-owner'
  doc['panels']['symbolEvidence']['data']['entryRecognition']['state']='no-admitted-owner'
 elif name=='feature-state-step-duration-dropped':
  assert 'step-duration' not in V.report['$defs']['FeatureId']['enum']
  doc=copy.deepcopy(bases[case['base']]);del doc['invocationLedger']['steps'][0]['attemptServiceTime']
 elif name=='review-Q6-audit-envelope-labelled-analyze':
  ops=copy.deepcopy(case['ops']);condition=next(c for c in V.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')=='analyze')
  next(o for o in ops if o.get('path')=='/featureStates')['value']=copy.deepcopy(condition['then']['properties']['featureStates']['const'])
  doc=apply(ctx,bases[case['base']],ops,as_bytes=False)
 elif name=='graph-on-ephemeral-run':
  doc=copy.deepcopy(bases[case['base']]);doc['panels']['graph']=copy.deepcopy(bases['audit-full']['panels']['graph'])
 else:
  doc=apply(ctx,bases[case['base']],case['ops'],as_bytes=False)
  if name=='ledger-analyze-planned-import-step':normalize_timing(doc['invocationLedger']['steps'][0])
  elif name=='ledger-render-recorded':normalize_timing(doc['invocationLedger']['steps'][-1])
  elif name=='skipped-step-with-attempt':normalize_timing(doc['invocationLedger']['steps'][1])
  elif name=='skipped-record-erased':doc['invocationLedger']['steps'][1]['attemptServiceTime']={'state':'not-finalized','reason':'step-result-not-recorded'}
 try:A.admit(M.canonical(doc),V,M,J,K,summary,feature=feature);got='accept'
 except Exception as error:got=getattr(error,'code',type(error).__name__)
 rows.append({'id':name,'priorObserved':outcome,'disposition':reason,'targetGuard':case['expect'],'observed':got,'passed':got==case['expect']})
result={'standing':'Root reconciled predecessor regression:186 unchanged outcomes and8 explicit successor witnesses; not194 unchanged tests or independent approval',
        'inventorySha256':hashlib.sha256(raw).hexdigest(),'parentCases':194,'unchangedOutcomes':186,'rebasedWitnesses':rows,
        'passed':all(r['passed'] for r in rows),'totalExecuted':194+len(rows)}
(HERE/'parent-reconciliation-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
