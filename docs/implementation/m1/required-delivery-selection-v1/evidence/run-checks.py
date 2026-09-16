from pathlib import Path
import subprocess,json
B=Path('/tmp/opensip-implementation/m1-required-delivery-candidate-01'); P=B/'product'; cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'; commands=[]
p=B/'README.md'; p.write_text(p.read_text().replace('Five planned','Four planned'))
for name,cmd in [('tests',[cargo,'test','--locked','--offline','--workspace','--all-targets']),('clippy',[cargo,'clippy','--locked','--offline','--workspace','--all-targets','--','-D','warnings']),('fmt',[cargo,'fmt','--all','--check'])]:
 r=subprocess.run(cmd,cwd=P,capture_output=True,timeout=300); (B/(name+'.stdout')).write_bytes(r.stdout); (B/(name+'.stderr')).write_bytes(r.stderr); commands.append({'name':name,'command':cmd,'exitCode':r.returncode}); (B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert r.returncode==0,(name,r.stderr.decode()); print(name+' passed',flush=True)
