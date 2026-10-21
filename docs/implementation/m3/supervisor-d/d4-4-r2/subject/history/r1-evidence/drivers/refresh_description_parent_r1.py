from pathlib import Path
import os,json,subprocess,hashlib,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch'
def git(root,*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=root,text=True).strip()
def pin(p):b=(W/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
old='071dc8a3327c4c6991d6c9ada3036faeb83bda80';new='c31809cb4993c5c2bbba3d004d9337f12f18d17b';assert git(P,'rev-parse','HEAD')==new and git(W,'rev-parse','HEAD')==old
assert git(P,'diff','--name-only',old,new)=='design-lock.json'and not git(P,'status','--porcelain')and not git(W,'diff','--cached','--name-only')
names=sorted(git(W,'ls-files','-m','-o','--exclude-standard').splitlines());assert names==['crates/components/src/lib.rs','crates/components/src/session_factory.rs'];pins=[pin(p)for p in names];before_status=git(W,'status','--porcelain');ah=git(A,'rev-parse','HEAD')
git(W,'merge','--ff-only',new)
assert git(W,'rev-parse','HEAD')==new and pins==[pin(p)for p in names]and before_status==git(W,'status','--porcelain')and (W/'design-lock.json').read_bytes()==(P/'design-lock.json').read_bytes()
report=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),fromParent=old,toParent=new,interveningPaths=['design-lock.json'],candidateSourcePinsPreserved=pins,hostBaseline='host-base-r1/report.json',hostBaselineSourceUnchanged=True,baselineRepeatNeeded=False,standing='Description186 lock-only parent refresh; unaccepted D4 source retained byte-exact, no candidate acceptance.',productQualification=False)
(F/'parent-refresh-r1.json').write_text(json.dumps(report,indent=2)+'\n')
for n in ['PREPARED.json','CURRENT.json']:
 p=F/n;s=json.loads(p.read_bytes());s.update(productParent=new,architectureParent=ah,originalProductParent=old,parentRefresh=str(F/'parent-refresh-r1.json'));p.write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(report,indent=2))
