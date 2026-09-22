from pathlib import Path
import json,subprocess,hashlib,platform
T=Path('/tmp/opensip-implementation');D=T/'joint-acl445';A=Path('/Users/sb/code/opensip-ai/opensip_arch');E=A/'docs/implementation/m2/joint-acl-probe-445';assert not(D/'checks-r2.json').exists()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
env=json.loads((T/'host-materialization368-r1/environment.json').read_bytes());save(D/'environment-r2.json',env);rows=[]
for label,cmd in [('compile-r2',['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Werror',str(D/'probe-r2.c'),'-o',str(D/'probe-r2')]),('probe-r2',[str(D/'probe-r2')])]:
 r=subprocess.run(cmd,env=env,capture_output=True,timeout=60);(D/(label+'.stdout')).write_bytes(r.stdout);(D/(label+'.stderr')).write_bytes(r.stderr);rows.append(dict(name=label,command=cmd,exitCode=r.returncode));save(D/'checks-r2.json',rows);print(label,r.returncode,flush=True)
 if r.returncode:print(r.stderr.decode(),flush=True);raise SystemExit(r.returncode)
print((D/'probe-r2.stdout').read_text(),flush=True)
