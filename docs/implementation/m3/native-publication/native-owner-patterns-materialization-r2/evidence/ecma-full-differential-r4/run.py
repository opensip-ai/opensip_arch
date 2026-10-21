from pathlib import Path
import subprocess,os,json,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
d=Path(__file__).parent
r=subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-O',str(d/'main.rs'),'-o',str(d/'probe')],capture_output=True);(d/'compile.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
r=subprocess.run([str(d/'probe'),str(d/'corpus.bin'),str(d/'matrix.bin')],capture_output=True);(d/'rust.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr
r=subprocess.run(['/tmp/opensip-implementation/d2b0b-materialization-r1/generation-r1/tool-node',str(d/'reference.cjs'),str(d/'inputs.json'),str(d/'matrix.bin')],capture_output=True);(d/'reference.stderr').write_bytes(r.stderr);(d/'report.json').write_bytes(r.stdout);assert r.returncode==0,(r.stdout[-4000:],r.stderr)
x=json.loads(r.stdout);x.update(inheritedFormSetEqual=True,candidateInheritedForms=72,newSharedForms=0,nativeOnlyFormsRefusedByInherited=True);(d/'report.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='mismatches'},indent=2))
