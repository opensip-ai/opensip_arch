"""Separate offline installs/builds from declared lane source snapshots."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess
H=Path(__file__).resolve().parent
NODE='/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
NPM='/Users/sb/.nvm/versions/node/v24.16.0/lib/node_modules/npm/bin/npm-cli.js'
def pin(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
 root=H/'isolated01';root.mkdir();results=[]
 (root/'empty-user.npmrc').write_text('');(root/'empty-global.npmrc').write_text('')
 for label,rel in [('report','apps/report'),('provider','providers/typescript'),('generator','tools/contracts')]:
  source=H/rel;dest=root/label;dest.mkdir();inputs=[]
  for p in sorted(source.rglob('*')):
   local=p.relative_to(source)
   if any(n in ['node_modules','dist'] for n in local.parts) or not p.is_file():continue
   q=dest/local;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());inputs.append({'path':str(local),**pin(q)})
  assert not (dest/'node_modules').exists()
  lock=pin(dest/'package-lock.json');package=pin(dest/'package.json')
  command=[NODE,NPM,'ci','--offline','--ignore-scripts','--no-audit','--no-fund','--cache',str(H/'provision-cache'),'--userconfig',str(root/'empty-user.npmrc'),'--globalconfig',str(root/'empty-global.npmrc')]
  steps=[('install',command)]
  if label=='report':steps += [('compile',[NODE,'node_modules/typescript/bin/tsc','--project','tsconfig.json']),('bundle',[NODE,'build-probe.mjs'])]
  elif label=='provider':steps += [('compile',[NODE,'node_modules/typescript/bin/tsc','--project','tsconfig.json']),('load',[NODE,'--input-type=module','-e','import {compilerClosureProbe} from "./dist/closure-probe.js";if(compilerClosureProbe()!=="6.0.3")throw Error("compiler");'])]
  else:steps += [('load',[NODE,'closure-probe.mjs'])]
  checks=[]
  env={'PATH':'/Users/sb/.nvm/versions/node/v24.16.0/bin:/usr/bin:/bin'}
  for name,cmd in steps:
   r=subprocess.run(cmd,cwd=dest,env=env,capture_output=True,text=True)
   (H/'logs'/(label+'-isolated-'+name+'.stdout')).write_text(r.stdout);(H/'logs'/(label+'-isolated-'+name+'.stderr')).write_text(r.stderr)
   checks.append({'step':name,'command':cmd,'exitCode':r.returncode});assert r.returncode==0,(label,name,r.stdout,r.stderr)
  assert pin(dest/'package-lock.json')==lock and pin(dest/'package.json')==package
  modules=dest/'node_modules';realized=[]
  for p in sorted(modules.glob('*/package.json'))+sorted(modules.glob('@*/*/package.json')):
   v=json.loads(p.read_bytes());realized.append({'name':v['name'],'version':v['version']})
  expected={'typescript','esbuild','@esbuild/darwin-arm64'} if label=='report' else {'typescript'}
  assert {r['name'] for r in realized}==expected
  outputs=[]
  for p in sorted((dest/'dist').rglob('*')) if (dest/'dist').exists() else []:
   if not p.is_file():continue
   local=p.relative_to(dest);assert p.read_bytes()==(source/local).read_bytes(),(label,str(local));outputs.append({'path':str(local),**pin(p)})
  results.append({'lane':label,'inputs':inputs,'steps':checks,'realizedPackages':realized,'outputs':outputs,'exactReproduction':True,'lockUnchanged':True})
  print(label,'offline closure and exact outputs pass',flush=True)
 (H/'isolated-result01.json').write_text(json.dumps({'passed':True,'lanes':results,'standing':'Three separately installed/built source snapshots with npm offline/ignore-scripts and no sibling package source. Shared provisioned cache, observed tools/loader; not OS confinement or complete product provider/app.'},indent=2)+'\n')
if __name__=='__main__':main()
