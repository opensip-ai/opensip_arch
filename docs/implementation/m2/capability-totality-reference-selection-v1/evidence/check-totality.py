from pathlib import Path
import argparse,ast,hashlib,importlib.util,json,typing,unicodedata
p=argparse.ArgumentParser();p.add_argument('--architecture',required=True,type=Path);p.add_argument('--output',type=Path);a=p.parse_args();A=a.architecture;U=Path(__file__).resolve().parent.parent
old=A/'docs/coop/design-corrections/native/native_evidence_model.v2.py';new=U/'reference/native_evidence_model.py';registry=A/'docs/coop/design-corrections/native/capability-manifest-domains.v2.json';cp=A/'docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py'
spec=importlib.util.spec_from_file_location('selected_capability_canonical',cp);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
ot=ast.parse(old.read_text());nt=ast.parse(new.read_text());name='admit_capability_manifest'
def remainder(t):return ast.dump(ast.Module(body=[n for n in t.body if not(isinstance(n,ast.FunctionDef)and n.name==name)],type_ignores=[]),include_attributes=False)
assert remainder(ot)==remainder(nt);checks=['only-one-function-AST-delta']
functions={'raw_sha256','cve1_encode','cve1_decode','_cve1_read','capability_manifest_identity',name}
constants={'CAPABILITY_MANIFEST_DOMAIN','_CVE1_MAX_ITEMS','_CVE1_MAX_DEPTH'}
def bind(tree):
 nodes=[n for n in tree.body if(isinstance(n,ast.FunctionDef)and n.name in functions)or(isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id in constants for t in n.targets))]
 assert len(nodes)==9
 ns={'Any':typing.Any,'AdmissionError':C.AdmissionError,'hashlib':hashlib,'unicodedata':unicodedata,'CAPABILITY_DOMAINS':json.loads(registry.read_bytes())}
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'exact-selected-capability-functions','exec'),ns);return ns
before=bind(ot);after=bind(nt)
for function in functions-{name}:
 of=next(n for n in ot.body if isinstance(n,ast.FunctionDef)and n.name==function);nf=next(n for n in nt.body if isinstance(n,ast.FunctionDef)and n.name==function)
 assert ast.get_source_segment(old.read_text(),of)==ast.get_source_segment(new.read_text(),nf)
checks.append('CVE1-and-identity-functions-byte-identical')
rows=json.loads((U/'evidence/root-cases.json').read_bytes());faults=0;changes=0
for row in rows:
 raw=bytes.fromhex(row['committedHex'])
 try:previous=before[name](raw)
 except Exception as exc:previous={'referenceFault':type(exc).__name__,'message':str(exc)}
 if 'referenceFault' in row['before']:
  assert previous.get('referenceFault')==row['before']['referenceFault'],row['label']
 else:assert previous==row['before'],row['label']
 current=after[name](raw);assert current==row['after'],row['label']
 if 'referenceFault'in previous:faults+=1;assert current['result']=='REFUSE'
 else:assert previous['result']==current['result']
 changes+=previous!=current
assert len(rows)==666 and faults==278 and changes==296;checks+=['all666-structured-results-and-exception-types-match','278-original-exceptions-preserved-as-exceptions','278-new-structured-refusals','zero-new-exceptions','existing-structured-classifications-unchanged','golden-identity-unchanged']
result={'checks':checks,'passed':True,'cases':len(rows),'predecessorExceptions':faults,'changedDiagnostics':changes,'candidateExceptions':0,'fullRunTested':False,'runtimeSelected':False,'sourcePins':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [old,new,registry,cp]]}
if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
