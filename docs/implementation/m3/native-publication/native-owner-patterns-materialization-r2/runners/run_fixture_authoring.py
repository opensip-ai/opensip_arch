from pathlib import Path
import os,subprocess,json,tempfile
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
B=Path(__file__).parent/'fixture-authoring-r1';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';runs=[]
T=Path(tempfile.mkdtemp(prefix='opensip-fixture-authoring-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.environ['TMPDIR']=str(T)
for name in ['replay','pooled','native-context','cycle']:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run([PY,'-I','-B',str(B/(name+'.py'))],cwd=B,stdout=out,stderr=subprocess.STDOUT)
 runs.append(dict(name=name,exitCode=r.returncode));(B/'runs.json').write_text(json.dumps(runs,indent=2)+'\n')
 if r.returncode:print((B/(name+'.log')).read_text()[-4000:],flush=True);break
print(json.dumps(runs,indent=2),flush=True)
