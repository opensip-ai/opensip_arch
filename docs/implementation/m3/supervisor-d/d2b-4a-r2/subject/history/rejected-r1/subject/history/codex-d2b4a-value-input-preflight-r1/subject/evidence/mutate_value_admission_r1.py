from pathlib import Path
import os,json,subprocess,tempfile,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'value-admission-mutations-r1';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/';own=json.loads((F/'value-admission-r3/report.json').read_text());assert own['allPassed'];pins=own['sourcePins'];fixture='crates/components/tests/data/rust3-startup-shape.v1.json';raw=(W/fixture).read_bytes();pins=pins+[dict(path=fixture,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())];assert len(pins)==12;baseline={r['path']:(W/r['path']).read_bytes() for r in pins}
def restored():
 for r in pins:assert hashlib.sha256((W/r['path']).read_bytes()).hexdigest()==r['sha256']
restored();T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR='/tmp/opensip-implementation/d2b3c-takeover-2026-10-20/native-resume-r1/target',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());SC='crates/identity/src/schema.rs';REG='crates/identity/src/schema_registry.rs'
cases=[
 dict(id='decoded-model-nfc-guard-skipped',package='opensip-identity',path=SC,old='if !model(value, 0) {',new='if false && !model(value, 0) {',test='schema_tests::structured_value_admission_rejects_non_nfc_and_preserves_model_depth',witness='right: Err(Json)'),
 dict(id='decoded-input-precharge-skipped',package='opensip-identity',path=SC,old='m.value(value, 0)?;',new='// mutation: complete input precharge skipped',test='schema_tests::structured_value_input_scan_is_charged_even_without_an_item_schema',witness='right: Err(Limit)'),
 dict(id='canonical-order-error-becomes-mismatch',package='opensip-identity',path=SC,old='Err(crate::ArrayOrderError::Canonical(_)) => return Err(Error::Json),',new='Err(crate::ArrayOrderError::Canonical(_)) => return Ok(false),',test='schema_tests::structured_canonical_order_errors_cannot_be_negated_into_admission',witness='right: Err(Json)'),
 dict(id='shape-handle-bypasses-selected-evaluator',package='opensip-components',path=REG,old='if !self\n            .registry\n            .program\n            .admit_value(&self.entry, value, budget)?',new='if false && !self\n            .registry\n            .program\n            .admit_value(&self.entry, value, budget)?',test='provider_protocol::rust3::schemas::tests::wide_rust3_universe_shape_uses_the_wire_bound_without_an_extra_json_byte_cap',witness='the full original schema must still reject the bad large-map value'),
]
for m in cases:assert baseline[m['path']].decode().count(m['old'])==1,m['id']
report=dict(standing='STRUCTURED SHAPE SOURCE REGRESSION CONTROLS; NOT FULL RUST3 UNIT ACCEPTANCE',baselineSourcePins=pins,cases=[],unitAccepted=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def compile_binary(folder,package,require_fresh):
 folder.mkdir(parents=True,exist_ok=True);r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p',package,'--lib'],cwd=W,env=E,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,'Rust compile failure never counts as runtime catch';name=package.replace('-','_');rows=[j for line in r.stdout.splitlines() if line.startswith(b'{') and (j:=json.loads(line)).get('reason')=='compiler-artifact' and j.get('executable') and j['target']['name']==name];assert len(rows)==1;row=rows[0];assert row['target']['src_path']==str(W/('crates/'+package.removeprefix('opensip-')+'/src/lib.rs'));assert not require_fresh or not row['fresh'];binary=Path(row['executable']);return binary,dict(path=str(binary),bytes=binary.stat().st_size,sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not row['fresh'])
def execute(folder,binary,test):
 r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(folder/'runtime.log').write_bytes(raw);return r.returncode,raw.decode(errors='replace')
for package in ['opensip-identity','opensip-components']:
 binary,meta=compile_binary(B/('baseline-'+package),package,False);shutil.copyfile(binary,B/('positive-'+package));report.setdefault('positiveBinaries',{})[package]=meta
save()
for m in cases:
 restored();folder=B/m['id'];row=dict(m,caught=False,allSourcesRestored=False,restoredPositive=False);report['cases'].append(row);save();error=None
 try:
  (W/m['path']).write_text(baseline[m['path']].decode().replace(m['old'],m['new']));binary,meta=compile_binary(folder,m['package'],True);code,output=execute(folder,binary,m['test']);row.update(binary=meta,runtimeExitCode=code,witnessObserved=m['witness'] in output);assert code!=0 and '0 passed; 1 failed' in output and m['witness'] in output,(m['id'],output[-2000:]);row['caught']=True
 except BaseException as ex:error=ex;row['error']=repr(ex)
 finally:
  for path,raw in baseline.items():
   if (W/path).read_bytes()!=raw:(W/path).write_bytes(raw)
  restored();row['allSourcesRestored']=True;save();positive=folder/'restored-positive';binary,meta=compile_binary(positive,m['package'],True);code,output=execute(positive,binary,m['test']);row.update(restoredPositive=code==0 and '1 passed; 0 failed' in output,restoredBinary=meta);save();assert row['restoredPositive'],m['id']
 if error:raise error
 print(m['id'],'runtime-caught/restored-positive',flush=True)
restored();report.update(allCaught=True,allRestored=True,compiledRuntimeMutants=4);save();print('ALL4VALUE-ADMISSION MUTANTS CAUGHT;12SOURCE PINS RESTORED; FULL RUST3 RECEIVE INCOMPLETE',flush=True)
