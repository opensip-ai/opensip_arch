from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'composition-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
def pins():return [dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in paths]
before=pins();r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p','opensip-platform','-p','opensip-components'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout)
report=dict(standing='D4-4 factory/participant composition and owning regressions; no actual CI adapter, provider-spoken spawn controls, full unit acceptance or qualification.',buildExit=r.returncode,sourcePins=before,runs=[],allPassed=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
save();assert r.returncode==0
rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')];bins={row['target']['name']:row for row in rows}
for name,target,pattern,min_count in [
 ('priced-launch-specs','opensip_platform','process::accounted::tests',4),
 ('factory-composition','opensip_components','session_factory::tests',6),
 ('rust3-participant-regressions','opensip_components','provider_protocol::rust3::send::participant::tests',8),
 ('ts2-send-participant-regressions','opensip_components','provider_protocol::ts2::tests::send',20),
 ('release-constants','opensip_components','provider_protocol::release_limits::tests',1),
]:
 artifact=bins[target];binary=Path(artifact['executable']);listing=subprocess.check_output([str(binary),'--list',pattern],cwd=W,env=E,text=True);(B/(name+'-list.log')).write_text(listing);selected=[line.removesuffix(': test')for line in listing.splitlines()if line.endswith(': test')];assert len(selected)>=min_count
 r=subprocess.run([str(binary),pattern],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/(name+'.log')).write_bytes(log);summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M);failed=re.findall(r'^test (.+) \.\.\. FAILED$',log.decode(errors='replace'),re.M);passed=re.findall(r'^test (.+) \.\.\. ok$',log.decode(errors='replace'),re.M);row=dict(name=name,selectedTests=selected,selectedCount=len(selected),exitCode=r.returncode,summaries=summaries,failureSet=failed,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=artifact['fresh'],allPassed=r.returncode==0 and not failed and set(passed)==set(selected));report['runs'].append(row);save();assert row['allPassed'];print(name+' '+str(len(selected))+' PASS',flush=True)
assert pins()==before;report['allPassed']=True;save();print('D4 composition/owning checks pass; complete CI and provider-spoken work remains open',flush=True)
