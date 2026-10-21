from pathlib import Path
import subprocess,os,json,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;O=F/'initial-r1';O.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-security-baseline-takeover');P=W.parent/'opensip';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
def git(root,*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=root,text=True).strip()
old=git(W,'rev-parse','HEAD');new=git(P,'rev-parse','HEAD');paths=git(W,'diff','--name-only').splitlines()+git(W,'ls-files','--others','--exclude-standard').splitlines()
if old!=new:
 assert not set(paths)&set(git(P,'diff','--name-only',old,new).splitlines());subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',old,new],cwd=P,check=True);git(W,'checkout','-q','--detach',new)
T=Path(tempfile.mkdtemp(prefix='opensip-security-repair-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(O/'target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
# Format only the new test guard block, without normalizing unrelated production source.
p=W/'crates/security/src/custody/commit_session_tests.rs';s=p.read_text();a=s.index('    // Other owners have private state-machine helpers named `settle`.');b=s.index('    assert!(\n        fs::read_to_string(root.join("security/src/custody/ordinary_writer.rs"))',a);raw='fn reference_block() {\n'+s[a:b]+'}\n';fmt=subprocess.run([R+'rustfmt','--edition','2024','--emit','stdout'],input=raw.encode(),env=E,capture_output=True);assert fmt.returncode==0;body=fmt.stdout.decode().split('\n',1)[1].rsplit('}',1)[0];p.write_text(s[:a]+body+s[b:])
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths};base_log=Path('/tmp/opensip-implementation/ci3l-2026-10-20/full-r1/base-opensip-security.log');failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',base_log.read_text(),re.M)));assert len(failed)==14
report=dict(standing='UNACCEPTED TEST-ONLY SECURITY BASELINE REPAIR',base=old,currentBase=new,sourcePins=pins,runs=[],privateTMPDIR=str(T),baselineFailureSource=dict(path=str(base_log),sha256=hashlib.sha256(base_log.read_bytes()).hexdigest()),baselineFailures=failed)
# Baseline and candidate each own a fresh target and exact artifact provenance.
binaries={}
for tag,root in [('baseline',P),('candidate',W)]:
 env=dict(E,CARGO_TARGET_DIR=str(O/(tag+'-target')))
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-security','--lib'],cwd=root,env=env,capture_output=True);(O/(tag+'-build.log')).write_bytes(r.stderr);(O/(tag+'-artifacts.jsonl')).write_bytes(r.stdout);assert r.returncode==0,r.stderr[-5000:]
 hits=[j for line in r.stdout.splitlines() if line.startswith(b'{') for j in [json.loads(line)] if j.get('reason')=='compiler-artifact' and j.get('target',{}).get('name')=='opensip_security' and j.get('profile',{}).get('test') and j.get('executable')];assert len(hits)==1 and hits[0]['fresh'] is False and hits[0]['target']['src_path']==str(root/'crates/security/src/lib.rs');binary=Path(hits[0]['executable']);binaries[tag]=(binary,env);report[tag+'Binary']=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),srcPath=hits[0]['target']['src_path'],fresh=False)
 with (O/(tag+'-fourteen.log')).open('wb') as log:r=subprocess.run([str(binary),'--exact',*failed],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 s=(O/(tag+'-fourteen.log')).read_text();found=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',s);assert found
 if tag=='baseline':assert r.returncode==101 and found[-1]==('0','14','0') and sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',s,re.M)))==failed
 else:assert r.returncode==0 and found[-1]==('14','0','0')
 report['runs'].append(dict(name=tag+'-fourteen',exitCode=r.returncode,testSummary=found[-1]));(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(tag,'fourteen',found[-1],flush=True)
# New whole owning suite establishes whether any remaining baseline failure is present.
binary,env=binaries['candidate']
for name,args in [('full-security',[str(binary)]),('doctests',[R+'cargo','test','--locked','--offline','-p','opensip-security','--doc']),('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-security','--all-targets','--','-D','warnings'])]:
 print(name,flush=True)
 with (O/(name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT)
 out=(O/(name+'.log')).read_text(errors='replace');summary=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',out);report['runs'].append(dict(name=name,exitCode=r.returncode,testSummary=summary[-1] if summary else None));(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0,(name,out[-5000:]);print(name,summary[-1:] or 'pass',flush=True)
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==sha for p,sha in pins.items());report['allRequiredChecksPassed']=True;report['baselineFourteenReproduced']=True;report['candidateFourteenResolved']=True;report['sourceUnchanged']=True;(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
