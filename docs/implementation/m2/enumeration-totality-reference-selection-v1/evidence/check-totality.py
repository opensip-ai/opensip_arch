from pathlib import Path
import json,hashlib,ast,importlib.util,copy
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--overlay',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();B=args.output;B.mkdir(parents=True,exist_ok=True);U=Path(__file__).resolve().parent.parent;O=args.overlay;p=O/'foundation/enumeration_model.v1.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85'
assert hashlib.sha256((O/'native/native_evidence_model.v2.py').read_bytes()).hexdigest()=='e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9'
sp=importlib.util.spec_from_file_location('enum_totality37',p);E=importlib.util.module_from_spec(sp);sp.loader.exec_module(E)
before=p.read_bytes();after=(U/'reference/enumeration_model.v1.py').read_bytes();assert before.count(b'except tomllib.TOMLDecodeError:')==1;assert after==before.replace(b'except tomllib.TOMLDecodeError:',b'except (tomllib.TOMLDecodeError, UnicodeDecodeError):')

old=E.project_named_packages;tree=ast.parse((U/'reference/enumeration_model.v1.py').read_bytes());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='project_named_packages');ns=dict(E.__dict__);exec(compile(ast.Module(body=[fn],type_ignores=[]),'proposed-enumeration-totality37','exec'),ns);new=ns['project_named_packages']
rows=json.loads((U/'evidence/toml-inputs.json').read_bytes());cases=[(r['label'],'Cargo.toml',bytes.fromhex(r['hex']))for r in rows]
cases += [('json-'+str(i),'package.json',b)for i,b in enumerate([b'{"name":"pkg"}',b'{\n "version":"1", "name": "pkg"\n}',b'{"name":1}',b'{"name":"a","name":"b"}',b'{"name":"a","x":1.0}',b'{"name":"\xff"}',b'{}',b'[]'])]
results=[];miss=[];old_exceptions=0;unchanged=0
for label,path,raw in cases:
 m=E.NV.assign_membership([], [path]);scope={'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]};index={path:{'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}};outcomes=[]
 for f in [old,new]:
  faults=[]
  try:outcomes.append({'value':f([path],scope,'.',m,{path:raw},faults,index),'refusals':faults})
  except Exception as exc:outcomes.append({'exception':type(exc).__name__})
 a,b=outcomes
 if a.get('exception')=='UnicodeDecodeError':
  old_exceptions+=1
  good=b.get('value',{}).get('parseFailed')==[{'path':path,'reason':'syntax'}]and b.get('value',{}).get('candidatePaths')==[path]and not b.get('refusals')
 else:good=a==b;unchanged+=good
 if not good:miss.append({'label':label,'before':a,'after':b})
 results.append({'label':label,'path':path,'rawSha256':hashlib.sha256(raw).hexdigest(),'before':a,'after':b})
(B/'cases.json').write_text(json.dumps(results,indent=2)+'\n');report={'cases':len(cases),'oldUnicodeDecodeExceptions':old_exceptions,'unchangedOtherOutcomes':unchanged,'mismatches':miss,'referenceModuleSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'candidateSha256':hashlib.sha256((U/'reference/enumeration_model.v1.py').read_bytes()).hexdigest(),'standing':'Private comparison only; no reference selection or parser acceptance'};(B/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not miss and old_exceptions==128
