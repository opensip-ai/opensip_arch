"""Initial full components/operability evidence for recovered D2b-3c; no acceptance."""
from pathlib import Path
import os, subprocess, json, tempfile, hashlib, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'owning-initial-r6';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-takeover');P=W.parent/'opensip';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,text=True).strip()
head=git(P,'rev-parse','HEAD');old=git(W,'rev-parse','HEAD');paths=git(W,'diff','--name-only').splitlines()+git(W,'ls-files','--others','--exclude-standard').splitlines()
if head!=old:
 subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',old,head],cwd=P,check=True)
 assert not set(git(P,'diff','--name-only',old,head).splitlines())&set(paths)
 git(W,'checkout','-q','--detach',head)
T=Path(tempfile.mkdtemp(prefix='opensip-d2b3c-owning-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'initial-r3/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
with (B/'format.log').open('wb') as out:r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p) for p in paths if p.endswith('.rs')]],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
# The selected replay is by-value equal to all original vectors except the
# one explicitly deferred Rust3-only raw float input, which is retained verbatim.
base=json.loads((W/'crates/components/tests/data/trial07-admission-vectors.v1.json').read_text());selection=json.loads((W/'crates/components/tests/data/trial07-integer-replay.v1.json').read_text())
excluded=selection['deferredVectors'];assert len(excluded)==1
seen=[]
for rule,vs in base['vectors'].items():
 expected=[]
 for v in vs:
  if v['id']==excluded[0]['id']:
   assert rule==excluded[0]['rule'] and v==json.loads(excluded[0]['originalVectorJson']);seen.append(v['id'])
  else:expected.append(v)
 assert selection['vectors'][rule]==expected
assert seen==[excluded[0]['id']] and sum(map(len,base['vectors'].values()))==353 and sum(map(len,selection['vectors'].values()))==352
(B/'selection-verification.json').write_text(json.dumps(dict(originalVectors=353,selectedVectors=352,deferredRawRust3Vectors=excluded,allSelectedVectorsEqualByValue=True,fixtureBytesUnchanged=True),indent=2)+'\n')
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True)
(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
artifacts=[json.loads(l) for l in r.stdout.splitlines() if l.startswith(b'{')];bins={j['target']['name']:j for j in artifacts if j.get('reason')=='compiler-artifact' and j.get('executable')}
image=bins['opensip_components'];assert image['target']['src_path']==str(W/'crates/components/src/lib.rs') and not image['fresh']
binary=Path(image['executable']);fixture=Path(bins['supervisor_fixture']['executable'])
(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
report=dict(standing='INITIAL FULL RECOVERED CANDIDATE CHECK; NOT UNIT ACCEPTANCE',productBase=head,rebasedFrom=old,sourcePins=pins,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=True,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],productQualification=False)
steps=[('corrected-hello',[str(binary),'--exact','provider_protocol::ts2::tests::send::the_hello_is_the_selection_and_the_schema_constants']),('corrected-path-sites',[str(binary),'--exact','provider_protocol::ts2::tests::send::replay::replay_path_sites']),('full-components',[str(binary)]),('full-operability',[R+'cargo','test','--locked','--offline','-p','opensip-operability','--lib']),('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','-p','opensip-operability','--all-targets','--','-D','warnings'])]
for name,args in steps:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');summaries=re.findall(r'^test result:.*$',text,re.M)
 report['runs'].append(dict(name=name,exitCode=r.returncode,testSummaries=summaries));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,text[-3000:])
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in pins.items())
report['allPassed']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('INITIAL OWNING CHECKS PASS',flush=True)
