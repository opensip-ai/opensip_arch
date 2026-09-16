from pathlib import Path
import shutil,hashlib,json,subprocess
L=Path('/Users/sb/code/opensip-ai/opensip'); B=Path('/tmp/opensip-implementation/m1-typescript-lane-isolation-01'); assert not B.exists(); B.mkdir()
node='/Users/sb/.nvm/versions/node/v24.16.0/bin/node'; npm='/Users/sb/.nvm/versions/node/v24.16.0/lib/node_modules/npm/bin/npm-cli.js'; cache='/tmp/opensip-implementation/m1-typescript-bootstrap-candidate-01/provision-cache'
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
commands=[]; results=[]
for name,src in [('report','apps/report'),('typescript-provider','providers/typescript')]:
 D=B/name; D.mkdir(); P=D/'package'; shutil.copytree(L/src,P,ignore=shutil.ignore_patterns('node_modules','dist')); home=D/'home'; home.mkdir(); user=D/'user.npmrc'; user.write_bytes(b''); globalconf=D/'global.npmrc'; globalconf.write_bytes(b'')
 files=[]
 for p in sorted(P.rglob('*')):
  assert not p.is_symlink()
  if p.is_file(): files.append({'path':str(p.relative_to(P)),**pin(p.read_bytes())})
 env={'PATH':'/Users/sb/.nvm/versions/node/v24.16.0/bin:/usr/bin:/bin','HOME':str(home),'LANG':'C','LC_ALL':'C','TZ':'UTC'}
 for step,cmd in [('provision',[node,npm,'ci','--offline','--ignore-scripts','--no-audit','--no-fund','--cache',cache,'--userconfig',str(user),'--globalconfig',str(globalconf)]),('compile',[node,str(P/'node_modules/typescript/bin/tsc'),'--project',str(P/'tsconfig.json')])]:
  with (D/(step+'.stdout')).open('wb') as out,(D/(step+'.stderr')).open('wb') as err: r=subprocess.run(cmd,cwd=P,env=env,stdout=out,stderr=err,timeout=300)
  row={'lane':name,'step':step,'command':cmd,'exitCode':r.returncode}; commands.append(row); (B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert r.returncode==0,(name,step); print(name+' '+step+' passed',flush=True)
 for row in files: assert pin((P/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']}
 outputs=[{'path':str(p.relative_to(P)),**pin(p.read_bytes())} for p in sorted((P/'dist').rglob('*')) if p.is_file()]; assert outputs
 results.append({'lane':name,'repositorySource':src,'sources':files,'outputs':outputs,'environment':env,'sourceAndLockUnchanged':True,'separatePackageOnly':True})
(B/'receipt.json').write_text(json.dumps({'standing':'Current selected per-lane offline install/compile evidence, not full provider/report application or release/toolclosure qualification','lanes':results,'commands':commands,'node':{'path':node,**pin(Path(node).read_bytes())},'npmEntry':{'path':npm,**pin(Path(npm).read_bytes())},'fullM1Complete':False,'releaseQualification':False},indent=2)+'\n')
