from pathlib import Path
import json,hashlib,os,time,subprocess
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';S=B/'sm-public-intake-entry-r1-stage';Q=B/'reviews/grok-sm-public-intake-entry-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=O/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
st=json.loads((C/'CURRENT-STATE.json').read_bytes());pub=st['SMPublicIntakeEntryPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert pub['subjectManifest']['sha256']==review['subjectManifestSha256']==subject and review['verdict']=='ACCEPT'and review['requiredFindings']==[]and review['controlsPassed']==2
source=json.loads((S/'source.json').read_bytes())
def check(p,r):raw=p.read_bytes();assert len(raw)==r['bytes']and hashlib.sha256(raw).hexdigest()==r['sha256']
for r in source['finalSourcePins']:check(Path(source['isolatedProducer'])/r['path'],r)
image=Path(source['compiledCargoImage']['path']);check(image,source['compiledCargoImage']);prepared=json.loads((D/'public-intake-packet-r65.json').read_bytes());packet=prepared['packet'];check(Path(packet['path']),packet);root=Path(prepared['root']);assert not(root/'entry-outcome.json').exists()and not(root/'stdout.log').exists()
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary experimental intake lane',flush=True);time.sleep(5)
try:
 env=dict(os.environ);env.update(TMPDIR=str(root),OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET=packet['path'],OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET_SHA256=packet['sha256'],OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET_BYTES=str(packet['bytes']));home=os.environ.get('HOME')
 argv=[str(image),'util::context::experimental_public_cache_intake::supplied_entry::collect_explicit_experimental_public_cache_intake','--exact','--ignored','--nocapture']
 with(root/'stdout.log').open('xb')as stdout,(root/'stderr.log').open('xb')as stderr:
  child=subprocess.Popen(argv,cwd=source['isolatedProducer'],env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,close_fds=True);code=child.wait()
 result=json.loads((root/'entry-outcome.json').read_bytes())if(root/'entry-outcome.json').exists()else None
 receipt=dict(packet=packet,root=str(root),argv=argv,exitCode=code,outcome=result,ownAcceptedEntrySubject=subject,ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,runtimeCompilerQueries=0,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
 (D/'parameterized-public-intake-r65.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Actual66input intake process exit',code,'intakeSuccess',None if result is None else result['success'],flush=True)
 if code!=0 or result is None or not result['success']:raise RuntimeError('Retained experimental intake incomplete; no corpus use')
 assert result['intake']['archives']==66 and result['intake']['indexes']==2 and result['intake']['versionRecords']==66
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
