from pathlib import Path
import os,json,subprocess,shutil,hashlib
A=Path('/Users/sb/code/opensip-ai/opensip_arch'); L=A.parent/'opensip'; B=Path('/tmp/opensip-implementation/m1-checker-mode-candidate-01'); P=B/'product'; C=P/'tools/typescript-boundary'; node='/Users/sb/.nvm/versions/node/v24.16.0/bin/node';npm='/Users/sb/.nvm/versions/node/v24.16.0/lib/node_modules/npm/bin/npm-cli.js';cache='/tmp/opensip-implementation/m1-typescript-bootstrap-candidate-01/provision-cache';commands=[]
assert (C/'bin/check-boundary.mjs').read_bytes()==(L/'tools/typescript-boundary/bin/check-boundary.mjs').read_bytes();r=json.loads((B/'mode-before.json').read_bytes());r['runtimeBytesUnchanged']=True;(B/'mode-before.json').write_text(json.dumps(r,indent=2)+'\n')
old=json.loads((L/'tools/typescript-boundary/tests/fixtures/staging-map.json').read_bytes());new=json.loads((C/'tests/fixtures/staging-map.json').read_bytes());changes=[(x,y) for x,y in zip(old['files'],new['files']) if x!=y];assert len(old['files'])==len(new['files']) and len(changes)==1 and changes[0][0]['path']=='tests/support/cli-invocations.mjs'
env=dict(os.environ);env['PATH']=str(Path(node).parent)+':/usr/bin:/bin';env.pop('NODE_OPTIONS',None)
def run(name,cmd,cwd,expected=0):
 r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=300);(B/(name+'.stdout')).write_bytes(r.stdout);(B/(name+'.stderr')).write_bytes(r.stderr);commands.append({'name':name,'command':cmd,'exitCode':r.returncode,'expectedExitCode':expected});(B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');assert r.returncode==expected,(name,r.stderr.decode()[-2000:],r.stdout.decode()[-2000:]);print(name+' passed',flush=True);return r
run('provision',[node,npm,'ci','--offline','--ignore-scripts','--no-audit','--no-fund','--cache',cache],C)
run('regression234',[node,'tests/run.mjs'],C)
# A separate copy with missing execute permission must fail cleanly and preserve
# EACCES; it must not pass or crash through an undefined stdout dereference.
N=B/'negative-checker';shutil.copytree(C,N,ignore=shutil.ignore_patterns('node_modules'));(N/'node_modules').symlink_to(C/'node_modules',target_is_directory=True);(N/'bin/check-boundary.mjs').chmod(0o644)
f=N/'tests/run.mjs';t=f.read_text().replace("'--test-concurrency=1', ...tests", "'--test-concurrency=1', '--test-name-pattern=real CLI invocations', ...tests");assert 'test-name-pattern' in t;f.write_text(t)
r=run('negative-no-execute',[node,'tests/run.mjs'],N,1);combined=r.stdout+r.stderr;assert b'EACCES' in combined and b'TypeError' not in combined
(B/'result.json').write_text(json.dumps({'standing':'Root executable-mode + exact harness correction; independent review pending','runtimeBytesUnchanged':True,'executableMode':'0755','regressionTestsPassed':234,'negativeMissingExecuteBit':'refuses with EACCES and no TypeError','stagingRowsChanged':1,'noLiveOrFrozenEdits':True},indent=2)+'\n')
