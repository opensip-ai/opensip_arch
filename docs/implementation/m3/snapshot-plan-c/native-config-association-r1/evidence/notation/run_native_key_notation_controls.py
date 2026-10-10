from pathlib import Path
import subprocess,json,hashlib,itertools,os
r=Path('/tmp/opensip-implementation/native-config-key-notation-controls-2026-10-10'); rust='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc'; env=dict(os.environ);env['PATH']='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin'; env['SDKROOT']=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(); version=subprocess.check_output([rust,'--version'],env=env).decode().strip(); command=['/usr/bin/nice','-n','10',rust,'--edition=2024','-C','linker=/usr/bin/cc','-A','dead_code',str(r/'key_notation.rs'),'-o',str(r/'key_notation')]; built=subprocess.run(command,env=env,capture_output=True); (r/'build.log').write_bytes(built.stdout+built.stderr);assert built.returncode==0
cases=[(['build','rustflags'],'build.rustflags'),(['dot.key'],'"dot.key"'),(['dot','key'],'dot.key'),([''],'""'),(['a',''],'a.""'),(['*'],'"*"'),(['a[0]'],'"a[0]"'),(['a',0,'b'],'a[0].b'),(['a',0,1,'b'],'a[0][1].b'),(['a',10,'b'],'a[10].b'),(['A_Z-09'],'A_Z-09'),(['é'],'"é"'),(['e\u0301'],'"e\u0301"'),(['a\nb'],'"a\\nb"'),(['a\x00b'],'"a\\u0000b"'),(['a"b'],'"a\\\"b"'),(['a\\b'],'"a\\\\b"'),(['\b\f\r\t'],'"\\b\\f\\r\\t"')]
names=['','a','A','b-0','dot.key','[0]','*','é','e\u0301','a"b','a\\b','\x00','\n','😀']; generated=[]
for a in names:
 generated.append([a])
 for b in names:
  generated.append([a,b])
  for i in [0,1,10]: generated.extend([[a,i,b],[a,i,0,b]])
paths=[p for p,_ in cases]+generated
raw=json.dumps(paths,ensure_ascii=False,separators=(',',':')).encode();(r/'inputs.json').write_bytes(raw)
run=subprocess.run(['/usr/bin/nice','-n','10',str(r/'key_notation')],input=raw,capture_output=True,env=env); (r/'run.stderr').write_bytes(run.stderr); assert run.returncode==0; outputs=json.loads(run.stdout);(r/'outputs.json').write_bytes(run.stdout);assert outputs[:len(cases)]==[s for _,s in cases]
def decode(s):
 pos=0; result=[]; need_name=True
 while pos<len(s):
  if s[pos]=='"':
   value,n=json.JSONDecoder().raw_decode(s[pos:]);assert isinstance(value,str);pos+=n;result.append(value)
  else:
   end=pos
   while end<len(s) and s[end] not in '.[': end+=1
   token=s[pos:end]; assert token and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in token); result.append(token);pos=end
  while pos<len(s) and s[pos]=='[':
   end=s.index(']',pos); token=s[pos+1:end]; assert token.isascii() and token.isdigit() and (token=='0' or not token.startswith('0'));result.append(int(token));pos=end+1
  if pos<len(s): assert s[pos]=='.';pos+=1;assert pos<len(s)
 return result
for path,encoded in zip(paths,outputs):assert decode(encoded)==path,(path,encoded)
seen={}
for path,encoded in zip(paths,outputs):
 if encoded in seen:assert seen[encoded]==path
 seen[encoded]=path
for invalid in [[],[0],['a',-1],['a',True],['a',{}],['a',None]]:
 bad=subprocess.run([str(r/'key_notation')],input=json.dumps([invalid]).encode(),capture_output=True,env=env);assert bad.returncode!=0
pin=json.loads((r/'source-pin.json').read_text()); p=Path(pin['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256'];assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
checks=dict(passed=True,rustcVersion=version,command=command,independentGoldenCases=len(cases),roundTripPaths=len(paths),uniquePaths=len(seen),collisionFree=True,invalidTypedPathRefusals=6,sourceUnchanged=True,productCodeChanged=False,lawAccepted=False,actualOwnedDiscovery=False,actualConfigClassification=False,carrierLimitsTested=False,productQualification=False,entirePlanComplete=False,scope='Bare-rustc test-only notation control against exact existing canonical source and independently specified goldens/inverse grammar. No H domain, product helper, parser/merge/discovery/owner admission or public failure route.')
(r/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
