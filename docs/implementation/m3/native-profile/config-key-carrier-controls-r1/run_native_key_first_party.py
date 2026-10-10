from pathlib import Path
import json,hashlib,subprocess,os,time,tempfile
B=Path('/tmp/opensip-implementation');R=B/'native-key-first-party-controls-2026-10-10';P=Path('/Users/sb/code/opensip-ai/opensip');assert not R.exists();R.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());L=D/'opensip-lanes.lock';T=Path(tempfile.mkdtemp(prefix='opensip-key-shape-',dir=D));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
sources=sorted((P/'crates/identity/src').glob('*.rs'))+[P/'Cargo.lock',P/'crates/identity/Cargo.toml'];before=[pin(p)for p in sources];owned=False
while not owned:
 try:L.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 command=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','-p','opensip-identity','--locked','--offline','--target-dir',str(R/'target')];built=subprocess.run(command,cwd=P,env=E,capture_output=True);(R/'build.log').write_bytes(built.stdout+built.stderr);assert built.returncode==0
finally:
 if owned:L.rmdir()
assert [pin(p)for p in sources]==before
libs=list((R/'target/debug/deps').glob('libopensip_identity-*.rlib'));assert len(libs)==1;lib=libs[0]
source=r'''use opensip_identity::{JsonValue, RegisteredSchemas, parse_json};
fn main() {
 let root=std::path::PathBuf::from(std::env::args_os().nth(1).expect("product root"));
 let cases=std::fs::read(std::env::args_os().nth(2).expect("cases")).unwrap();
 let sources:Vec<Vec<u8>>=RegisteredSchemas::source_requirements().iter().map(|p| std::fs::read(root.join(p.source_path())).unwrap()).collect();
 let borrowed:Vec<&[u8]>=sources.iter().map(Vec::as_slice).collect();
 let registry=RegisteredSchemas::from_sources(&borrowed).expect("exact complete current source registry");
 let JsonValue::Array(cases)=parse_json(&cases).unwrap()else{panic!("cases array")};
 let id=RegisteredSchemas::source_requirements().iter().find(|p|p.source_path()=="schemas/sources/native-v2.schema.json").unwrap().schema_id();
 for case in cases {
  let JsonValue::Object(case)=case else {panic!("case object")};
  let JsonValue::String(name)=&case["case"] else {panic!("case name")};
  let JsonValue::Bool(expected)=&case["expectedValid"] else {panic!("expected Boolean")};
  let bytes=opensip_identity::canonical_bytes(&case["record"]).unwrap();
  let observed=registry.schema(id,"/$defs/CargoConfigProjectionV2").unwrap().admit_json(&bytes,200_000_000);
  assert_eq!(observed.is_ok(),*expected,"{name}: {:?}",observed.err());
  println!("PASS {name}");
 }
}
''';(R/'shape_controls.rs').write_text(source);rust='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc';cc=['/usr/bin/nice','-n','10',rust,'--edition=2024','-C','linker=/usr/bin/cc',str(R/'shape_controls.rs'),'--extern','opensip_identity='+str(lib),'-L','dependency='+str(R/'target/debug/deps'),'-o',str(R/'shape_controls')];c=subprocess.run(cc,env=E,capture_output=True);(R/'bridge-build.log').write_bytes(c.stdout+c.stderr);assert c.returncode==0
casepath=B/'native-key-carrier-boundaries-2026-10-10/cases.json';run=subprocess.run(['/usr/bin/nice','-n','10',str(R/'shape_controls'),str(P),str(casepath)],env=E,capture_output=True);(R/'controls.stdout').write_bytes(run.stdout);(R/'controls.stderr').write_bytes(run.stderr);assert run.returncode==0;assert len(run.stdout.decode().splitlines())==24;assert [pin(p)for p in sources]==before;assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists();checks=dict(passed=True,controls=24,actualFirstPartySchemaDecoderRun=True,completeCurrentSourceRegistryChecked=True,sourceBeforeAndAfter=before,cases=pin(casepath),freshIdentityRlib=pin(lib),runtime=pin(R/'shape_controls'),buildCommand=command,bridgeBuildCommand=cc,privateTmpdir=str(T),ownedLaneReleased=True,productCodeChanged=False,actualKeyClassification=False,actualOwnedDiscovery=False,productQualification=False,entirePlanComplete=False,scope='Fresh unchanged first-party identity build and exact current complete schema registry shape controls only. Actual owned native input/config classification/profile/Tool/owner remain open.');(R/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({k:v for k,v in checks.items()if k not in ['sourceBeforeAndAfter','buildCommand','bridgeBuildCommand']},indent=2))
