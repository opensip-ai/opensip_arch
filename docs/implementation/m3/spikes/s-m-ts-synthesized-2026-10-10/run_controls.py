from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time,shutil
B=Path(__file__).resolve().parent;NODE=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node');TS=Path('/Users/sb/code/.opensip-implementation-cache/sm-tools-2026-10-09/typescript/package/lib/typescript.js');inventory=json.loads((B/'evidence/js-medium-express-input-inventory.json').read_bytes());D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());L=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10
while True:
 try:L.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-synth-controls-',dir=D));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T));env.pop('NODE_OPTIONS',None);env.pop('NODE_PATH',None);results=[]
 cases=[('javascript-root',{'index.js':'const answer = 42; exports.answer = answer;\n'},None,None),('typescript-root',{'index.ts':'export const answer: number = 42;\n'},None,None),('typescript-error',{'index.ts':'export const answer: number = "bad";\n'},2322,None),('outside-read',{'index.ts':'import {x} from "../outside"; export const answer=x;\n'},2307,None),('jsx-options',{'index.jsx':'export const node = <div />;\n'},None,None),('tsconfig-refused',{'index.ts':'export const answer=42;\n','tsconfig.json':'{}'},None,'synthesized control requires no tsconfig'),('jsconfig-refused',{'index.js':'exports.answer=42;\n','jsconfig.json':'{}'},None,'jsconfig present; synthesized origin not established')]
 for name,files,code,refusal in cases:
  root=T/name;root.mkdir(mode=0o700);rows=[]
  for rel,text in files.items():
   p=root/rel;p.write_text(text);raw=p.read_bytes();rows.append(dict(path=rel,sealed=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
  inp=root/'input.json';inp.write_text(json.dumps(dict(id=name,virtualRoot=str(root/'virtual'),files=rows,libraries=inventory['libraries'],configurations=['tsconfig.json']if 'tsconfig.json'in files else []))+'\n');out=B/'evidence'/('control-'+name+'.stdout.json');err=B/'evidence'/('control-'+name+'.stderr')
  with out.open('wb')as o,err.open('wb')as e:
   child=subprocess.Popen([str(NODE),'--no-addons',str(B/'synthesized.cjs'),str(TS),str(inp)],env=env,cwd=T,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
  if refusal:assert child.returncode!=0 and refusal in err.read_text();observed=None
  else:
   assert child.returncode==0,err.read_text();observed=json.loads(out.read_text());r=observed['configurations'][0];assert r['selectedOptions']['noEmit']is True and r['selectedOptions']['allowJs']is True and r['selectedOptions']['checkJs']is False;assert len(r['rootFiles'])==1 and observed['repositoryCodeExecuted']is False and observed['emitPerformed']is False
   if code:assert str(code)in r['diagnosticCounts']
   if name=='jsx-options':assert r['selectedOptions']['jsx']=='preserve'
   if name=='outside-read':assert not any(x.endswith('/outside.ts')or x.endswith('/outside.js')for x in observed['readPaths'])
  results.append(dict(case=name,passed=True,diagnosticCode=code,refusal=refusal,exitCode=child.returncode,parentPriority=10,childPriority=priority,rssNative=int(usage.ru_maxrss),rssUnit='bytes',stdout=str(out),stderr=str(err)))
 (B/'controls.json').write_text(json.dumps(dict(passed=True,controls=results,ownedLaneHeldForSet=True,TMPDIR=str(T),TMPDIRMode='0700',repositoryCodeExecuted=False,emitPerformed=False,productQualification=False),indent=2)+'\n');shutil.rmtree(T);print('Seven actual synthesized-program/refusal controls passed')
finally:
 if owned:L.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
