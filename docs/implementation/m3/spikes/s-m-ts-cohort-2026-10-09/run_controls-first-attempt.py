from pathlib import Path
import os,subprocess,json,hashlib,tempfile,time
B=Path(__file__).resolve().parent;NODE='/Users/sb/.nvm/versions/node/v24.16.0/bin/node';TS=Path('/Users/sb/code/.opensip-implementation-cache/sm-tools-2026-10-09/typescript/package/lib/typescript.js');DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned control lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']];T=Path(tempfile.mkdtemp(prefix='opensip-sm-ts-cohort-controls-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T));env.pop('NODE_OPTIONS',None);env.pop('NODE_PATH',None);libraries=[]
 for p in sorted(TS.parent.iterdir()):
  if p.name.endswith('.d.ts')and p.is_file()and not p.is_symlink():b=p.read_bytes();libraries.append(dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 controlSources={'positive':{'tsconfig.json':json.dumps(dict(compilerOptions=dict(target='ES2022',strict=True),include=['*.ts'])),'a.ts':'export const value: number = 1;\n'},'type-error':{'tsconfig.json':json.dumps(dict(compilerOptions=dict(target='ES2022',strict=True),include=['*.ts'])),'a.ts':'export const value: number = "wrong";\n'},'outside-import':{'tsconfig.json':json.dumps(dict(compilerOptions=dict(target='ES2022',strict=True),include=['*.ts'])),'a.ts':'import {value} from "../outside"; export const n = value;\n'},'nested-reference':{'tsconfig.json':json.dumps(dict(files=[],references=[dict(path='./child')])),'child/tsconfig.json':json.dumps(dict(compilerOptions=dict(target='ES2022',strict=True,composite=True),include=['*.ts'])),'child/a.ts':'export const value: number = 1;\n'},'no-config':{'a.ts':'export const value: number = 1;\n'}}
 controls=[];outside=T/'outside.ts';outside.write_text('export const value: number = 11;\n');outsideHash=hashlib.sha256(outside.read_bytes()).hexdigest()
 for label,sources in controlSources.items():
  root=T/label;root.mkdir(mode=0o700);rows=[]
  for i,(path,text)in enumerate(sources.items()):
   dest=root/str(i);b=text.encode();dest.write_bytes(b);dest.chmod(0o400);rows.append(dict(path=path,sealed=str(dest),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
  configs=sorted([p for p in sources if p.endswith('tsconfig.json')]);inp=root/'input.json';v=dict(id=label,virtualRoot=str(root),files=rows,libraries=libraries,configurations=configs);inp.write_text(json.dumps(v,indent=2)+'\n');(B/'evidence'/f'control-{label}-input.json').write_text(json.dumps(v,indent=2)+'\n');child=subprocess.run(['/usr/bin/nice','-n','10',NODE,'--no-addons',str(B/'cohort.cjs'),str(TS),str(inp)],cwd=T,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(B/'evidence'/f'control-{label}.stdout.json').write_bytes(child.stdout);(B/'evidence'/f'control-{label}.stderr').write_bytes(child.stderr);assert child.returncode==0,child.stderr;out=json.loads(child.stdout);codes={k:sum(r.get('diagnosticCounts',{}).get(k,0)for r in out['configurations'])for k in ['2322','2307']}
  if label=='positive':assert out['configurations'][0]['diagnosticsCount']==0
  if label=='type-error':assert codes['2322']==1
  if label=='outside-import':assert codes['2307']==1 and str(outside)in out['blockedPaths']and str(outside)not in out['readPaths']
  if label=='nested-reference':assert len(out['configurations'])==2 and sum(r.get('diagnosticsCount',0)for r in out['configurations'])==0 and any(r.get('reason')=='no-configured-source-files'for r in out['configurations'])
  if label=='no-config':assert out['configurationCount']==0 and not out['configurations']
  controls.append(dict(label=label,exitCode=child.returncode,synthetic=True,diagnosticCounts=codes,configurationCount=out['configurationCount']))
 assert hashlib.sha256(outside.read_bytes()).hexdigest()==outsideHash;(B/'controls.json').write_text(json.dumps(dict(standing='UNREVIEWED FIRSTPARTY SYNTHETIC COHORT API CONTROLS',controls=controls,outsideImportTarget=str(outside),outsideImportTargetSha256=outsideHash,ownTMPDIR=str(T),TMPDIRMode='0700',laneHeld=True,nice=10,productSecurityEnforcementClaimed=False),indent=2)+'\n');print('Five cohort controls passed',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
