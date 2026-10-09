from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib
os.setpriority(os.PRIO_PROCESS,0,10)
parent_nice=os.getpriority(os.PRIO_PROCESS,0)
assert parent_nice==10
B=Path(__file__).resolve().parent;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for replay control lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-replay-controls-',dir=D)).resolve();T.chmod(0o700);pin=json.loads((B/'build-release.json').read_text());exe=Path(pin['executable']);assert hashlib.sha256(exe.read_bytes()).hexdigest()==pin['sha256'];env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for k in ['HOME','LANG','LC_ALL','TZ']:
  if k in os.environ:env[k]=os.environ[k]
 base=json.loads((B/'control-packet.json').read_text());proof=next(r['descriptor']for r in base['objects']if r['domain']=='proof-bundle');digest=proof['executionInputsDigest'];assert any(r['sha256']==digest for r in base['blobs']);base['blobs']=[r for r in base['blobs']if r['sha256']!=digest];(B/'promised-manifest-missing.json').write_text(json.dumps(base,separators=(',',':'))+'\n')
 rows=[]
 for name,expected,marker in [('control-packet',0,None),('packet-3-selected',0,None),('forged-verdict',101,'EVALUATOR_COMPLETE_PROOF_REPLAY'),('forged-empty-rule-results',101,'EVALUATOR_COMPLETE_PROOF_REPLAY'),('promised-manifest-missing',101,'MissingBlob')]:
  out=B/(name+'-release-control.stdout');err=B/(name+'-release-control.stderr')
  with out.open('wb')as o,err.open('wb')as e:
   r=subprocess.Popen([str(exe),str(B/(name+'.json'))],cwd=T,env=env,stdout=o,stderr=e);child_nice=os.getpriority(os.PRIO_PROCESS,r.pid);assert child_nice==10;r.wait()
  assert r.returncode==expected,(name,r.returncode,err.read_text())
  if marker:assert marker in err.read_text(),(name,err.read_text())
  else:assert json.loads(out.read_text())['fullReplayPassed']is True and err.read_bytes()==b''
  row=dict(case=name,observedParentNiceness=parent_nice,observedChildNiceness=child_nice,exitCode=r.returncode,expectedOutcome='fullreplay-pass'if expected==0 else'exact-native-replay-refusal',expectedNativeDiagnostic=marker,stdout=str(out),stderr=str(err),officialProviderFailureRouteClaimed=False);rows.append(row);(B/'release-controls.json').write_text(json.dumps(dict(standing='UNREVIEWED SYNTHETIC EXACT NATIVE COMPLETE REPLAY CONTROLS; NOT QUALIFICATION',controls=rows),indent=2)+'\n');print(name,'passed',flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
