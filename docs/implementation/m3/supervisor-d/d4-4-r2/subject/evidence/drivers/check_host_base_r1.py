from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'host-base-r1';B.mkdir(exist_ok=False);P=Path('/Users/sb/code/opensip-ai/opensip');R='/opt/homebrew/Cellar/rust/1.95.0/bin/';parent=json.loads((F/'PREPARED.json').read_bytes())['productParent']
def git(*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=P,text=True).strip()
assert git('rev-parse','HEAD')==parent and not git('status','--porcelain');tree=git('rev-parse','HEAD^{tree}')
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
target=Path('/tmp/opensip-implementation/d2b4a-takeover-2026-10-21/base-components-target')
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(target),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p','opensip-host'],cwd=P,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_host'];assert len(rows)==1;row=rows[0];binary=Path(row['executable'])
r=subprocess.run([str(binary)],cwd=P,env=E,capture_output=True);log=r.stdout+r.stderr;(B/'host.log').write_bytes(log);text=log.decode(errors='replace');summaries=re.findall(r'^test result:.*$',text,re.M);failures=re.findall(r'^test (.+) \.\.\. FAILED$',text,re.M)
report=dict(standing='Fresh host baseline on exact integrated Rust3 successor parent; not factory candidate evidence or qualification.',productParent=parent,productTree=tree,cargoTarget=str(target),targetSharedOnlyWithinSameMainWorktree=True,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=row['fresh'],exitCode=r.returncode,summaries=summaries,failureSet=failures,defaultParallel=True,productQualification=False,allPassed=r.returncode==0 and not failures and bool(summaries))
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert report['allPassed']
assert git('rev-parse','HEAD')==parent and git('rev-parse','HEAD^{tree}')==tree and not git('status','--porcelain')
print(json.dumps(report,indent=2))
