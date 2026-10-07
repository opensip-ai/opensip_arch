from pathlib import Path
import subprocess,os,json
b=Path(__file__).resolve().parent;probe=b/'public-probe';probe.mkdir(exist_ok=True);os.chmod(probe,0o700);(probe/'probe.rs').write_text('#![no_std]\npub fn long_form_probe() {}\n');rust='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc';e=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo')
version=subprocess.check_output([rust,'-vV'],env=e,text=True);rows=[]
for name in ['allow','warn','deny','forbid']:
 args=[rust,'--edition','2024','--crate-name','long_form_probe','--crate-type','lib','--emit','metadata','--'+name+'=dead_code',str(probe/'probe.rs'),'-o',str(probe/(name+'.rmeta'))];r=subprocess.run(['/usr/bin/nice','-n','10',*args],env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert r.returncode==0,(name,r.stdout);rows.append(dict(flag='--'+name+'=dead_code',exit=r.returncode,output=r.stdout))
result=dict(passed=True,standing='LOCAL PRIMARY TOOL LONG OPTION SPELLING PROBE ONLY; NO TOOLCHAIN/CONTEXT/PROVIDER QUALIFICATION',version=version,rows=rows,publicOwnedSource=True,cargoInvoked=False,private413Read=False,qualification=False);(b/'primary-probe.json').write_text(json.dumps(result,indent=2)+'\n');print('All four named attached long lint spellings accepted by local rustc1.95; syntax probe only, no qualification claim.')
