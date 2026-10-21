"""Resume in a fresh owned checkout, preserving recovered and original archived drafts."""
from pathlib import Path
import os,subprocess,json,hashlib,shutil,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-resume-r1';assert not B.exists()
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';OLD=P.parent/'opensip-d2b3c-takeover';W=P.parent/'opensip-d2b3c-native-resume'
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,env=E)
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
accepted=json.loads(Path('/tmp/opensip-implementation/native-owner-patterns-2026-10-20/companion-fixture-repair-r1/integration.json').read_text())
ph=git(P,'rev-parse','HEAD').decode().strip();assert ph==accepted['productCode'] and not git(P,'status','--porcelain')
base=git(OLD,'rev-parse','HEAD').decode().strip();assert base=='2b27854b2129e6750c95d83357eb15f013a0979e'
prior=json.loads((F/'owning-initial-r6/report.json').read_text());assert prior['productBase']==base
paths=list(prior['sourcePins']);assert len(paths)==11
for path,h in prior['sourcePins'].items():assert pin(OLD,path)['sha256']==h
status=git(OLD,'status','--porcelain','--untracked-files=all').decode();assert sorted(line[3:] for line in status.splitlines())==sorted(paths)
overlap=set(git(P,'diff','--name-only',base,ph).decode().splitlines())&set(paths);target='crates/components/src/provider_protocol/ts2_send_tests.rs';assert overlap=={target}
basebytes=git(P,'show',base+':'+target);mainbytes=(P/target).read_bytes();assert mainbytes.startswith(basebytes)
accepted_append=mainbytes[len(basebytes):];assert b'fn native_owner_registered_startup_preserves_non_dot_segments_and_refuses_late_dot_segments()' in accepted_append
recovered=(OLD/target).read_bytes();modules=b'#[path = "ts2_census_tests.rs"]\nmod census;\n\n#[path = "ts2_replay_tests.rs"]\nmod replay;\n';assert recovered.endswith(modules)
merged=recovered[:-len(modules)]+accepted_append+modules
assert accepted_append in merged and merged.replace(accepted_append,b'',1)==recovered
assert not W.exists();B.mkdir()
for path in paths:
 dst=B/'preserved-recovered-product'/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(OLD/path,dst)
(B/'preserved-recovered.patch').write_bytes(git(OLD,'diff','--binary'))
git(P,'worktree','add','--detach',str(W),ph);assert not git(W,'status','--porcelain')
for path in paths:
 dst=W/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(merged if path==target else (OLD/path).read_bytes())
assert git(OLD,'rev-parse','HEAD').decode().strip()==base and git(OLD,'status','--porcelain','--untracked-files=all').decode()==status
for path,h in prior['sourcePins'].items():assert pin(OLD,path)['sha256']==h
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),standing='UNACCEPTED RESUMED D2b3c DRAFT; ORIGINAL ARCHIVE AND RECOVERED CHECKOUT UNCHANGED',productBase=ph,architectureBase=git(A,'rev-parse','HEAD').decode().strip(),originalRecoveredBase=base,originalRecoveredWorktree=str(OLD),worktree=str(W),preservedRecoveredPins=[pin(OLD,p) for p in paths],candidatePins=[pin(W,p) for p in paths],overlap=[target],overlapResolution='Preserve accepted native47-line append verbatim before the two recovered test module declarations; removing the exact accepted append reproduces recovered bytes',acceptedNativeAppend=dict(bytes=len(accepted_append),sha256=hashlib.sha256(accepted_append).hexdigest()),receiptRefreshComplete=True,unitAccepted=False,productQualification=False)
(B/'prepared.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['standing','productBase','worktree','overlap','overlapResolution']},indent=2))
