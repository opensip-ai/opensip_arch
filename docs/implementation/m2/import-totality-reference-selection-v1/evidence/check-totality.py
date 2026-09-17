from pathlib import Path
import argparse,ast,hashlib,json,itertools
p=argparse.ArgumentParser();p.add_argument('--architecture',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();a.before=a.architecture/'docs/implementation/m2/predicate-matching-reference-selection-v1/reference/workflows_model.v1.py';a.after=Path(__file__).resolve().parent.parent/'reference/workflows_model.v1.py'
def extract(path):
 source=path.read_text();tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='registry_row');reg=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PAYLOAD_REGISTRY'for t in n.targets));ns={};exec(compile(ast.Module(body=[reg,fn],type_ignores=[]),str(path),'exec'),ns);rest=ast.dump(ast.Module(body=[n for n in tree.body if n is not fn],type_ignores=[]),include_attributes=False);return ns,rest
old,ot=extract(a.before);new,nt=extract(a.after);assert ot==nt;assert old['PAYLOAD_REGISTRY']==new['PAYLOAD_REGISTRY'];assert len(new['PAYLOAD_REGISTRY'])==5
values=[None,False,True,0,1,-1,2**64-1,'','unknown','Runtime','runtime\n','workflow.import-payload.runtime.v1\n','Ω','\x00',[],{},[None],[[]],{'key':[]},{'nested':{'a':1}}]+sorted({s for pair in old['PAYLOAD_REGISTRY']for s in pair})
rows=[];exceptions=0;positives=0
for kind,domain in itertools.product(values,repeat=2):
 try:before={'return':old['registry_row'](kind,domain)}
 except Exception as exc:before={'exception':type(exc).__name__,'message':str(exc)}
 after={'return':new['registry_row'](kind,domain)}
 if 'exception'in before:assert before['exception']=='TypeError'and after['return']is None;exceptions+=1
 else:assert before==after
 if after['return']is not None:positives+=1;assert type(kind)is str and type(domain)is str
 rows.append({'kind':kind,'payloadDomain':domain,'before':before,'after':after})
assert positives==5
result={'schemaVersion':1,'passed':True,'cases':len(rows),'previousExceptions':exceptions,'candidateExceptions':0,'registeredPairs':positives,'unchangedOtherAst':True,'unchangedRegistryRows':True,'previousDefinedResultsUnchanged':True,'scope':'Actual selected registry_row and literal PAYLOAD_REGISTRY only. Malformed JSON key types become no-row, not success. Caller phase diagnostics are separately tested; no fullRun/runtime claim.','sources':[{'path':str(x),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()}for x in [a.before,a.after]],'rows':rows};a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='rows'}))
