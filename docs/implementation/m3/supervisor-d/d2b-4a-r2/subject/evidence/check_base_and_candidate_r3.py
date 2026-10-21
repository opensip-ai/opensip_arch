from pathlib import Path
import os,subprocess,json,hashlib,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'base-candidate-r3';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
common=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
for name,env in [('GIT_DIR',None),('GIT_WORK_TREE',None),('GIT_CONFIG_COUNT',None)]:common.pop(name,None)
source_paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());pins=[]
for path in source_paths:
 raw=(W/path).read_bytes();pins.append(dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
report=dict(standing='D2B4A EXACT BASE/CANDIDATE SUITES AND FINAL SOURCE CHECKS; NO UNIT ACCEPTANCE',baseHead=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=P,text=True).strip(),candidateParent=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=W,text=True).strip(),sourcePins=pins,runs=[],unitAccepted=False,productQualification=False,workspaceTestsPassed=False,inheritedWorkspaceTestFailure=str(F/'inherited-cli-source-guard-failure.json'))
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
own=json.loads((F/'receiver-final-owning-r3/report.json').read_text());assert own['owningLaneComplete'] and own['sourcePins']==pins
report['workspaceTestsPassed']=own['workspaceTestsPassed'];report['inheritedWorkspaceTestFailureResolvedByAcceptedCLIRepair']=str(F.parent/'cli-source-guard-repair-2026-10-21/integration-r3.json')
images={}
for label,root,target in [('base',P,F/'base-components-target')]:
 env=dict(common,CARGO_TARGET_DIR=str(target));folder=B/label;folder.mkdir();r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components','-p','opensip-identity'],cwd=root,env=env,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,'compile failure is not runtime proof';bins={j['target']['name']:j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')};fixture=Path(bins['supervisor_fixture']['executable']);component=Path(bins['opensip_components']['executable']);(component.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n');images[label]={}
 for package in ['opensip_components','opensip_identity']:
  row=bins[package];assert row['target']['src_path']==str(root/('crates/'+package.removeprefix('opensip_')+'/src/lib.rs'));binary=Path(row['executable']);r=subprocess.run([str(binary)],cwd=root,env=env,capture_output=True);raw=r.stdout+r.stderr;(folder/(package+'.log')).write_bytes(raw);text=raw.decode(errors='replace');failed=sorted(re.findall(r'^test (.*?) \.\.\. FAILED$',text,re.M));summaries=re.findall(r'^test result:.*$',text,re.M);entry=dict(name=label+'-'+package,exitCode=r.returncode,failed=failed,testSummaries=summaries,binary=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not row['fresh']));images[label][package]=entry;report['runs'].append(entry);save();print(entry['name'],entry['exitCode'],summaries,flush=True)

# The fresh full workspace run supplies candidate suites; do not rerun the
# identical candidate library suites merely to obtain a second log.
log=(F/'receiver-final-owning-r3/workspace-tests.log').read_text()
artifacts=[j for line in (F/'receiver-final-owning-r3/artifacts.jsonl').read_text().splitlines()if line.startswith('{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')]
images['candidate']={};comparisons={}
for package,expected in [('opensip_components',318),('opensip_identity',86)]:
 rows=[j for j in artifacts if j['target']['name']==package];assert len(rows)==1;artifact=rows[0];binary=Path(artifact['executable']);needle='Running unittests src/lib.rs ('+str(binary)+')';assert log.count(needle)==1
 section=log.split(needle,1)[1];summary=re.search(r'^test result:.*$',section,re.M);assert summary and f'{expected} passed; 0 failed' in summary.group()
 failed=sorted(re.findall(r'^test (.*?) \.\.\. FAILED$',section[:summary.end()],re.M));assert not failed
 entry=dict(name='candidate-'+package,exitCode=0,failed=failed,testSummaries=[summary.group()],evidence=str(F/'receiver-final-owning-r3/workspace-tests.log'),binary=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not artifact['fresh']))
 images['candidate'][package]=entry;report['runs'].append(entry);base=images['base'][package];assert base['exitCode']==0 and base['failed']==failed;comparisons[package]=dict(equalFailureSets=True,base=base['testSummaries'],candidate=entry['testSummaries'])
for row in pins:assert hashlib.sha256((W/row['path']).read_bytes()).hexdigest()==row['sha256']
report.update(allPassed=True,comparisons=comparisons,candidateEvidence='Exact current full workspace suite, not a second candidate run');save();print('FRESH BASE270/81 AND EXACT WORKSPACE CANDIDATE318/86; EQUAL EMPTY FAILURE SETS')
