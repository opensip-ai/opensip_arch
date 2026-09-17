from pathlib import Path
import json,hashlib,importlib.util,copy,subprocess,sys,shutil
import argparse
HERE=Path(__file__).resolve().parent
if len(sys.argv)>1 and sys.argv[1]=='child':
    B=Path(sys.argv[3]).parent
else:
    parser=argparse.ArgumentParser();parser.add_argument('--source32',required=True,type=Path);parser.add_argument('--source32-manifest',required=True,type=Path);parser.add_argument('--python',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    B=args.output;assert not B.exists();B.mkdir(parents=True);PY=args.python
    assert hashlib.sha256(args.source32_manifest.read_bytes()).hexdigest()=='c52cf367757970cb072e8ae72e6c29fe8b60741719709eafda2cd5a6f464ec96'
    manifest=json.loads(args.source32_manifest.read_bytes())
    for row in manifest['files']:
        if row['path'].startswith('reference/'):
            source=args.source32/row['path'];raw=source.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
            target=B/row['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    shutil.copy2(HERE/'inputs.json',B/'inputs.json')

if len(sys.argv)>1 and sys.argv[1]=='child':
 source=Path(sys.argv[2]);out=Path(sys.argv[3]);
 if '--set-zero-after-startup' in sys.argv:sys.set_int_max_str_digits(0)
 spec=importlib.util.spec_from_file_location('enumeration_integer39',source);E=importlib.util.module_from_spec(spec)
 try:spec.loader.exec_module(E)
 except RuntimeError as exc:
  out.write_text(json.dumps({'importFailure':str(exc),'exception':type(exc).__name__,'startupIntegerLimit':sys.flags.int_max_str_digits,'integerLimit':sys.get_int_max_str_digits()})+'\n');raise SystemExit(0)
 results=[]
 for case in json.loads((B/'inputs.json').read_bytes()):
  q=case['input'];faults=[]
  try:r={'value':E.project_named_packages(q['snapshotPaths'],q['scope'],q['workspaceRoot'],q['membership'],{k:bytes.fromhex(v)for k,v in q['blobs'].items()},faults,q.get('index')),'refusals':faults}
  except Exception as exc:r={'exception':type(exc).__name__,'message':str(exc)[:200]}
  results.append({'label':case['label'],'outcome':r})
 # A caller changing global state after import gets an explicit tooling failure.
 mutation=None
 if sys.get_int_max_str_digits()==0 and hasattr(E,'_require_reference_integer_profile'):
  sys.set_int_max_str_digits(4300)
  try:E.project_named_packages([],{},'.',{}, {}, [])
  except RuntimeError as exc:mutation=str(exc)
  finally:sys.set_int_max_str_digits(0)
 out.write_text(json.dumps({'integerLimit':sys.get_int_max_str_digits(),'results':results,'afterImportMutationRefused':mutation},separators=(',',':'))+'\n');raise SystemExit(0)
O=B/'reference/archroot/docs/coop/design-corrections'
before=HERE/'before-reference.py';after=HERE.parent/'reference/enumeration_model.v1.py'
assert hashlib.sha256(before.read_bytes()).hexdigest()=='689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072'
assert hashlib.sha256(after.read_bytes()).hexdigest()=='d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992'
shutil.copy2(before,O/'foundation/enumeration_before39.py');shutil.copy2(after,O/'foundation/enumeration_model.v1.py')
cases=json.loads((B/'inputs.json').read_bytes());numeric=[c['label']for c in cases if c['label'].startswith('numeric-')];commands=[]
for label,source,flags in [('before-default','enumeration_before39.py',[]),('before-zero','enumeration_before39.py',['-X','int_max_str_digits=0']),('after-zero','enumeration_model.v1.py',['-X','int_max_str_digits=0']),('after-default','enumeration_model.v1.py',[]),('after-mutated-zero','enumeration_model.v1.py',[]),('after-640','enumeration_model.v1.py',['-X','int_max_str_digits=640'])]:
 cmd=[str(PY),'-I','-B',*flags,__file__,'child',str(O/'foundation'/source),str(B/(label+'.json'))]+(['--set-zero-after-startup']if label=='after-mutated-zero'else[]);r=subprocess.run(cmd,capture_output=True,timeout=180);commands.append({'label':label,'command':cmd,'exitCode':r.returncode});assert r.returncode==0,(label,r.stderr[-2000:])

read=lambda name:json.loads((B/(name+'.json')).read_bytes())
a=read('before-default');z=read('before-zero');b=read('after-zero');exceptions=[];miss=[];unchanged=0
for old,old0,new in zip(a['results'],z['results'],b['results']):
 assert old['label']==old0['label']==new['label']
 if old0!=new:miss.append({'kind':'zero-profile-semantic-change','before':old0,'after':new})
 if 'exception'in old['outcome']:
  exceptions.append({'label':old['label'],'before':old['outcome'],'after':new['outcome']})
  if old['outcome']['exception']!='ValueError' or new['outcome'].get('value',{}).get('namedPaths')!=['Cargo.toml'] or new['outcome'].get('refusals')!=[]:miss.append({'kind':'unexpected-exception-change','before':old,'after':new})
 elif old!=new:miss.append({'kind':'defined-outcome-change','before':old,'after':new})
 else:unchanged+=1
for label in ['after-default','after-640','after-mutated-zero']:
 r=read(label);assert r.get('importFailure')=='enumeration reference requires Python -I -B -X int_max_str_digits=0',r
assert b['afterImportMutationRefused']=='enumeration reference requires Python -I -B -X int_max_str_digits=0'
report={'cases':len(cases),'numericCases':len(numeric),'oldDefaultValueErrorCases':len(exceptions),'unchangedDefinedOutcomes':unchanged,'allZeroProfileOutcomesUnchanged':not miss,'mismatches':miss,'wrongProfileImportControls':3,'postImportProfileMutationRefused':True,'standing':'Private proposed reference-process profile; no selection and no new product syntax/resource outcome'};(B/'result.json').write_text(json.dumps(report,indent=2)+'\n');(B/'exceptions.json').write_text(json.dumps(exceptions,indent=2)+'\n');(B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');print(json.dumps(report));assert not miss
