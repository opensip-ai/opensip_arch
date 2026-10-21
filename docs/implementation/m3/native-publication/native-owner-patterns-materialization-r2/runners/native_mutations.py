from pathlib import Path
import os,subprocess,tempfile,json,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'mutations-r1';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-native-mutations-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
S='crates/identity/src/schema.rs';M='crates/identity/src/schema_patterns.rs';G='crates/identity/src/schema_registry.rs';N='schemas/sources/native-v2.schema.json'
dispatch='''&& matches!(
                owner,
                "urn:opensip:product-v1:native:evidence-schemas:v2"
                    | "opensip.product.occupancy-companion.1"
                    | "opensip.product.relation-payload.2"
            )'''
mutations=[
 ('native-dispatch-lost','identity',S,'if self.native_owner_patterns','if false && self.native_owner_patterns','runtime'),
 ('native-dispatch-leaks-to-foreign','identity',S,dispatch,'&& (true || '+dispatch[3:]+')','runtime'),
 ('native-terminal-lf-stripped','identity',M,"pub(crate) fn matches_native_owner(pattern: &str, value: &str) -> Result<bool, &'static str> {","pub(crate) fn matches_native_owner(pattern: &str, value: &str) -> Result<bool, &'static str> {\n    let value = value.strip_suffix('\\n').unwrap_or(value);",'runtime'),
 ('corrected-scan-truncated-at-lf','host',M,"!value.split('/').any(|part| matches!(part, \".\" | \"..\"))","!value.split('\\n').next().unwrap().split('/').any(|part| matches!(part, \".\" | \"..\"))",'runtime'),
 ('native-unknown-form-fallback','identity',M,'if !FORMS.contains(&pattern) {','if false && !FORMS.contains(&pattern) {','runtime'),
 ('grant-wildcard-allows-cr-ls-ps','identity',M,"if matches!(first, '\\n' | '\\r' | '\\u{2028}' | '\\u{2029}') {","if matches!(first, '\\n') {",'runtime'),
 ('compiled-native-length-wrong','host',G,'bytes: 295104,','bytes: 295105,','registry-construction-source-refusal'),
 ('compiled-native-digest-wrong','host',G,'113, 121, 213, 46, 59, 124, 231, 64','114, 121, 213, 46, 59, 124, 231, 64','registry-construction-source-refusal'),
 ('native-source-same-length-substituted','host',N,'{\n  "$schema"','{\n\t "$schema"','registry-construction-source-refusal'),
 ('native-source-predecessor-scanner-restored','host',N,r'(?![\\s\\S]*',r'(?!.*','registry-construction-source-refusal'),
]
original={p:(W/p).read_bytes() for p in (S,M,G,N)}
report=dict(standing='COMPILED MUTATION CONTROLS; NOT WHOLE UNIT ACCEPTANCE',privateTMPDIR=str(T),TMPDIRMode='0700',originalPins={p:hashlib.sha256(raw).hexdigest() for p,raw in original.items()},mutations=[],allRestored=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 for name,focus,path,before,after,kind in mutations:
  assert all((W/p).read_bytes()==raw for p,raw in original.items())
  old=original[path].decode();count=old.count(before);assert count==(34 if name=='native-source-predecessor-scanner-restored' else 1),(name,count)
  changed=old.replace(before,after);(W/path).write_text(changed)
  if name=='native-source-same-length-substituted':assert len(changed.encode())==len(original[path])
  print(name,flush=True)
  package='opensip-identity' if focus=='identity' else 'opensip-host';pattern='native_owner_' if focus=='identity' else 'native_owner_registered'
  with (B/(name+'.log')).open('wb') as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p',package,'--lib',pattern],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
  output=(B/(name+'.log')).read_text(errors='replace');failed=re.findall(r'^test (\S+) \.\.\. FAILED$',output,re.M)
  row=dict(name=name,path=path,mutatedSha256=hashlib.sha256(changed.encode()).hexdigest(),classification=kind,exitCode=r.returncode,compileFailure='could not compile' in output,failedTests=failed)
  (W/path).write_bytes(original[path]);report['mutations'].append(row);save()
  assert r.returncode!=0 and failed and not row['compileFailure'],row
finally:
 for p,raw in original.items():(W/p).write_bytes(raw)
 report['allRestored']=all((W/p).read_bytes()==raw for p,raw in original.items());save()
assert len(report['mutations'])==len(mutations)
for package,pattern in [('opensip-identity','native_owner_'),('opensip-host','native_owner_registered')]:
 with (B/(package+'-restored.log')).open('wb') as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p',package,'--lib',pattern],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,package
report['allCaught']=True;report['restoredPositiveControlsPassed']=True;save();print('ALL MUTANTS CAUGHT AND SOURCE PINS RESTORED',flush=True)
