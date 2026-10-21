from pathlib import Path
import os,json,subprocess,hashlib,difflib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');B=F/'host-format-r1';assert not B.exists();B.mkdir()
d=json.loads((F/'full-r3/report.json').read_text());assert all(r['exitCode']==0 for r in d['runs'])
for p,h in d['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
rows=[]
for p in ['crates/host/src/native_owner_tests.rs','crates/host/tests/admission_tests.rs']:
 before=(W/p).read_bytes();r=subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--emit','stdout'],input=before,capture_output=True);assert r.returncode==0
 after=r.stdout;assert before!=after
 (B/(Path(p).name+'.before')).write_bytes(before);(B/(Path(p).name+'.after')).write_bytes(after)
 diff=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile=p+'.before',tofile=p+'.after'))
 (B/(Path(p).name+'.diff')).write_text(diff);print(diff,flush=True)
 (W/p).write_bytes(after);rows.append(dict(path=p,beforeSha256=hashlib.sha256(before).hexdigest(),afterSha256=hashlib.sha256(after).hexdigest()))
(B/'report.json').write_text(json.dumps(dict(standing='RUSTFMT ONLY; HOST OWNING AND CLIPPY RERUN REQUIRED',rows=rows,unitAccepted=False),indent=2)+'\n')
