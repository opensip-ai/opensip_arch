from pathlib import Path
import os,subprocess,json,tempfile,time,shutil
B=Path('/tmp/opensip-implementation/j3ao-authoring-r1');P=B/'product';O=B/'identity-controls-r2';assert not O.exists();O.mkdir()
root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-j3ao-identity-',dir=root));private.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),CC='/usr/bin/clang',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 variants=[]
 for name,features in [('default',[]),('development',['--features','operability-dev-sinks'])]:
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','-p','opensip-host',*features,'--message-format','json'];r=subprocess.run(cmd,cwd=P,env=env,capture_output=True);(O/(name+'-build.stdout')).write_bytes(r.stdout);(O/(name+'-build.stderr')).write_bytes(r.stderr);assert r.returncode==0,r.stderr.decode()[-4000:]
  artifacts={}
  for line in r.stdout.splitlines():
   item=json.loads(line)
   if item.get('reason')=='compiler-artifact' and item['target']['name'] in ['opensip_host','opensip_operability','opensip_platform']:
    files=[f for f in item['filenames']if f.endswith('.rlib')];assert len(files)==1
    saved=O/name/Path(files[0]).name;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(files[0],saved);artifacts[item['target']['name']]=str(saved)
  assert len(artifacts)==3;variants.append((name,artifacts))
finally:
 if owned:lane.rmdir()
source=O/'identity.rs';source.write_text('''#![forbid(unsafe_code)]
fn main() {
    use opensip_host::{Format, MetadataHost, MetadataRequest};
    use opensip_operability::{Code, EmitOn, HostRepairCompleted, RepairKind, RepairState};
    let mut host=MetadataHost::new();
    let context=host.begin().unwrap();
    let scope=host.logging_scope(&context).expect("own reservation after start");
    let execution=opensip_platform::reserve_execution_id().unwrap();
    let _typed=opensip_operability::ExecutionId::from(&execution);
    let _request=opensip_operability::RequestScope::from(&opensip_platform::RequestIdentity::draw().unwrap());
    let mut foreign=MetadataHost::new();
    let foreign_context=foreign.begin().unwrap();
    assert!(host.logging_scope(&foreign_context).is_none());
    assert!(foreign.logging_scope(&context).is_none());
    assert!(foreign.logging_scope(&foreign_context).is_none());
    HostRepairCompleted::new(Code::from_enum(RepairKind::Registration),Code::from_enum(RepairState::RwR1)).emit(scope);
    let rendered=host.execute(&context,MetadataRequest::Help{topic:None},Format::Json,None,"test").unwrap();
    assert_eq!(rendered.exit_code,0);
    assert!(opensip_operability::frozen_summary().is_some());
    use std::io::Write;
    std::io::stdout().write_all(&rendered.bytes).unwrap();
}
''')
rows=[]
for name,artifacts in variants:
 binary=O/(name+'-identity');cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024',str(source),'-o',str(binary),'-C','linker=/usr/bin/clang','-L','dependency='+str(P/'target/debug/deps')]
 for crate,path in artifacts.items():cmd.extend(['--extern',crate+'='+path])
 r=subprocess.run(cmd,env=env,capture_output=True);(O/(name+'-rustc.log')).write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
 for repeat in range(3):
  r=subprocess.run(['/usr/bin/nice','-n','10',str(binary)],env=env,capture_output=True,timeout=10);prefix=name+'-'+str(repeat);(O/(prefix+'.stdout')).write_bytes(r.stdout);(O/(prefix+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,r.stderr
  envelope=json.loads(r.stdout);ids=[]
  def find(value):
   if isinstance(value,dict):
    for k,v in value.items():
     if k=='requestId':ids.append(v)
     else:find(v)
   elif isinstance(value,list):
    for v in value:find(v)
  find(envelope);assert len(set(ids))==1 and ids,ids
  request=ids[0];assert request.startswith('req1_') and len(request)==37
  if name=='default':assert r.stderr==b''
  else:
   records=[line for line in r.stderr.decode().splitlines() if 'host.repair.completed:' in line];assert len(records)==1,r.stderr
   assert 'requestId="'+request+'"' in records[0],(request,records)
  rows.append({'build':name,'repeat':repeat,'passed':True,'requestId':request,'realEventEmitted':True,'realInstallationRead':False})
assert len({r['requestId'] for r in rows})==6
(O/'checks.json').write_text(json.dumps({'passed':True,'freshChildren':6,'checks':rows,'defaultSinkAbsent':True,'developmentRecordMatchesEnvelope':True,'foreignReservationsRefused':True,'reservedPlatformConversionsCompile':True,'productQualification':False},indent=2)+'\n');print('identity controls:6 fresh children passed')
