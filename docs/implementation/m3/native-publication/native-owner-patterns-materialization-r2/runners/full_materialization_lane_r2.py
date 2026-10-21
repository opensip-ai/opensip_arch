from pathlib import Path
import os,subprocess,tempfile,json,hashlib,re,sys
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'full-r2';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch'
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
assert json.loads((F/'generation-report-r3.json').read_text())['runs'][-1]['selectionResult']['passed']
T=Path(tempfile.mkdtemp(prefix='opensip-native-full-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=W,text=True).strip()
paths=git('diff','--name-only').splitlines();untracked=git('ls-files','--others','--exclude-standard').splitlines();expected=[r['path'] for r in json.loads((F/'fixture-authoring-r1/staged-companions.json').read_text())['newFiles']];assert sorted(untracked)==sorted(expected);paths=sorted(paths+untracked)
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
report=dict(standing='COMPLETE MATERIALIZATION OWNING LANE; INDEPENDENT UNIT ACCEPTANCE REQUIRED',productBase=git('rev-parse','HEAD'),sourcePins=pins,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],allPassed=False,blindReceiptStanding='STALE/PENDING: generator reference closure intentionally changed; mandatory reviewed refresh after integration before census-dependent consumption',censusModesRun=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def run(name,args):
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 output=(B/(name+'.log')).read_text(errors='replace');row=dict(name=name,args=args,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',output,re.M),failedTests=re.findall(r'^test (\S+) \.\.\. FAILED$',output,re.M));report['runs'].append(row);save();return r.returncode
# Build fixture from this same candidate and bind the exact returned executable.
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True)
(B/'components-artifacts.jsonl').write_bytes(r.stdout);(B/'components-build.log').write_bytes(r.stderr);assert r.returncode==0,r.stderr[-5000:]
artifacts=[json.loads(line) for line in r.stdout.splitlines() if line.startswith(b'{')];bins={j['target']['name']:j for j in artifacts if j.get('reason')=='compiler-artifact' and j.get('executable')}
image=bins['opensip_components'];assert image['target']['src_path']==str(W/'crates/components/src/lib.rs')
binary=Path(image['executable']);fixture=Path(bins['supervisor_fixture']['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
report['componentsBinary']=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),fixture=str(fixture),fixtureSha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),fresh=image['fresh']);save()
for pkg in ['identity','contracts','components','host','security','storage','evaluator','lifecycle']:
 run('owning-'+pkg,[R+'cargo','test','--locked','--offline','--no-fail-fast','-p','opensip-'+pkg])
clippy=[R+'cargo','clippy','--locked','--offline']
for pkg in ['identity','contracts','components','host','security','storage','evaluator','lifecycle']:clippy+=['-p','opensip-'+pkg]
run('clippy',clippy+['--all-targets','--','-D','warnings'])
run('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets'])
run('typescript-lanes',[PY,'-I','-B','tools/check_typescript.py','--root',str(W),'--architecture',str(A),'--node','/tmp/opensip-implementation/d2b0b-materialization-r1/generation-r1/tool-node'])
for pkg,feature in [('security','scenario-fixtures'),('security','crash-matrix'),('lifecycle','scenario-fixtures'),('lifecycle','crash-matrix'),('storage','scenario-fixtures'),('storage','crash-matrix')]:
 run(pkg+'-'+feature,[R+'cargo','check','--locked','--offline','-p','opensip-'+pkg,'--all-targets','--features',feature])
run('environment-exceptions',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v'])
run('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)])
run('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])
r=subprocess.run([R+'cargo','metadata','--locked','--offline','--format-version','1'],cwd=W,env=E,capture_output=True);assert r.returncode==0;(B/'cargo-metadata.json').write_bytes(r.stdout)
L=json.loads((W/'design-lock.json').read_text());inventory=A/L['inventorySuccessors'][-1]['candidate']['path']
run('package-edges',[PY,'-I','-B','tools/check_package_edges.py','--repository',str(W),'--metadata',str(B/'cargo-metadata.json'),'--inventory',str(inventory),'--lane','host','--package-policy',str(A/'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json'),'--architecture',str(A),'--lock','design-lock.json'])
fmt=[]
for p in paths:
 if not p.endswith('.rs'):continue
 old=subprocess.run(['/usr/bin/git','show','HEAD:'+p],cwd=W,capture_output=True).stdout
 def clean(raw):
  r=subprocess.run([R+'rustfmt','--edition','2024','--emit','stdout'],input=raw,env=E,capture_output=True);return r.returncode==0 and r.stdout==raw
 fmt.append(dict(path=p,baseClean=clean(old),candidateClean=clean((W/p).read_bytes())))
report['rustfmtClassification']=fmt;report['formatPassed']=all(r['candidateClean'] for r in fmt if r['baseClean'])
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in pins.items())
mut=json.loads((F/'mutations-r1/report.json').read_text());assert mut['allRestored'] and mut['allCaught'] and mut['restoredPositiveControlsPassed']
for p,h in mut['originalPins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
report['compiledMutationsCaught']=len(mut['mutations']);report['sourcePinsUnchanged']=True;report['allPassed']=all(r['exitCode']==0 for r in report['runs']) and report['formatPassed'];save();print(json.dumps(dict(allPassed=report['allPassed'],failures=[r['name'] for r in report['runs'] if r['exitCode']]),indent=2),flush=True)
closure=json.loads((W/'tools/contracts/generator-closure.json').read_text())
for row in closure['files']:
 raw=(W/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
generated=json.loads((F/'generated-output-audit.json').read_text())
for row in generated['outputs']:
 raw=(W/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
report['selectedGenerationInputsStillExact']=len(closure['files']);report['selectedGeneratedOutputsStillExact']=len(generated['outputs']);save()
