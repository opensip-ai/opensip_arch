from pathlib import Path
import argparse,json,hashlib,importlib.util
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();dc=a.root/'docs/coop/design-corrections';source=dc/'workflows/workflows_model.v1.py'
s=importlib.util.spec_from_file_location('root_policy_after',source);w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
# Independent selected contracts, not a copy of the candidate's ladder table.
# These isolate the pure evaluator boundary; full host admission is a separate check.
rows=[]
def case(name,relation,minimum,have,complete,expected,op='exists',available=(),evidence=None):
 atom={'op':op,'relation':relation,'minResolution':minimum,'filters':[]}
 if evidence:atom['evidence']=evidence
 facts=[] if have is None else [{'relation':relation,'subject':'s','target':'t','resolution':have}]
 try:actual=w.eval_pred(atom,'s',facts,complete,set(available),set())
 except w.Refusal as exc:actual={'refusal':exc.detail}
 except Exception as exc:actual={'unexpectedException':type(exc).__name__,'detail':str(exc)}
 passed=actual==expected if type(actual)==type(expected) else False
 rows.append({'case':name,'atom':atom,'facts':facts,'completeCoverageAssumed':complete,'availableEvidence':list(available),'expected':expected,'actual':actual,'pass':passed})
case('resolved-native-import-qualifies','imports','resolved-target','resolved-target',True,True)
case('resolved-import-satisfies-syntactic-minimum','imports','syntactic-specifier','resolved-target',True,True)
case('syntactic-import-cannot-satisfy-resolved-minimum','imports','resolved-target','syntactic-specifier',False,None)
case('partial-no-import-remains-unknown','imports','resolved-target',None,False,None)
case('closed-resolved-import-absence','imports','resolved-target',None,True,False)
case('negative-over-partial-remains-unknown','imports','resolved-target',None,False,None,op='none')
case('negative-over-complete-empty','imports','resolved-target',None,True,True,op='none')
case('positive-witness-defeats-negative-even-partial','imports','resolved-target','resolved-target',False,False,op='none')
case('checked-type-qualifies','types','checked','checked',True,True)
case('annotation-does-not-prove-checked-type','types','checked','annotated',False,None)
case('checked-type-satisfies-annotation-minimum','types','annotated','checked',True,True)
case('foreign-rung-is-admission-fault','imports','resolved-target','resolved-callee',True,{'refusal':'POLICY.UNKNOWN_RULE'})
case('abstract-token-with-real-native-fact-refuses','imports','resolved','resolved-target',True,{'refusal':'POLICY.UNKNOWN_RULE'})
case('observed-runtime-window-with-evidence','runtime-observation','observed','observed',True,True,available=('runtime',),evidence='runtime')
case('absent-runtime-evidence-is-unknown','runtime-observation','observed','observed',True,None,evidence='runtime')
case('runtime-no-hit-with-partial-coverage-is-unknown','runtime-observation','observed',None,False,None,op='none',available=('runtime',),evidence='runtime')
report={'standing':'Codex independently selected pure policy-helper regression cases. Complete Coverage is an explicitly assumed input here, not a proof of native sufficiency, import observability, full policy admission, repair authorization or host enforcement. Original v12 abstract/native mismatch probe retained separately.','sourceRoot':str(a.root),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':rows,'passed':sum(r['pass'] for r in rows),'failed':sum(not r['pass'] for r in rows)}
assert not a.out.exists();a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(report['failed']))
