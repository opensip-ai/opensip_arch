from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'companion-mutations-r1';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-companion-mutants-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
new='7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132';old='81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712'
C='crates/evaluator/src/coverage-registry.native-owner-r1.json';I='crates/evaluator/src/import-payload-registry.native-owner-r1.json';J='crates/security/tests/fixtures/journal-seal-replay.native-owner-r1.json';H='crates/host/tests/fixtures/replay-fixtures.native-owner-r1.json'
original={p:(W/p).read_bytes() for p in (C,I,J,H)}
def stale_metadata(raw):
 text=raw.decode();assert new in text;return text.replace(new,old).encode()
def old_native_blob(raw):
 doc=json.loads(raw);row=next(r for r in doc['blobPool'].values() if r['digest']==new);row['hex']=(P/'schemas/sources/native-v2.schema.json').read_bytes().hex();assert hashlib.sha256(bytes.fromhex(row['hex'])).hexdigest()==old
 return json.dumps(doc,ensure_ascii=False,separators=(',',':')).encode()+b'\n'
def corrupted_relation_blob(raw):
 doc=json.loads(raw);row=next(r for r in doc['blobPool'].values() if r['digest']=='3add72f2cecd755be5e21795cfee545cdc68ff80ed8c43fedd417093917ade62');bs=bytearray.fromhex(row['hex']);bs[0]=ord('[');row['hex']=bs.hex();return json.dumps(doc,ensure_ascii=False,separators=(',',':')).encode()+b'\n'
host_fact='fact_admission::tests::a_schema_or_identity_failure_is_input_refused_on_the_provider_return_route'
specs=[('stale-coverage-current-digest',C,stale_metadata,'host','native_owner_tests::coverage_producer_recomputes_scope_and_preserves_rc3_rc4_rc6','selected-current-metadata full-document refusal'),('stale-import-current-digest',I,stale_metadata,'host','native_owner_tests::import_payloads_require_exact_kind_domain_and_retained_schema','selected-current-metadata full-document refusal'),('retained-native-blob-substitution',J,old_native_blob,'security','commit_authority::seal_binding_tests','retained raw-blob digest/provenance refusal'),('retained-relation-blob-substitution',H,corrupted_relation_blob,'host',host_fact,'retained raw-blob digest/provenance refusal')]
report=dict(standing='FRESH COMPILED CURRENT-METADATA AND RETAINED-BLOB MUTATIONS; NOT UNIT ACCEPTANCE',privateTMPDIR=str(T),TMPDIRMode='0700',originalPins={p:hashlib.sha256(raw).hexdigest() for p,raw in original.items()},mutations=[],restored=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 for name,path,mutate,pkg,pattern,kind in specs:
  assert all((W/p).read_bytes()==raw for p,raw in original.items());raw=mutate(original[path]);assert raw!=original[path];(W/path).write_bytes(raw);print(name,flush=True)
  with (B/(name+'.log')).open('wb') as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-'+pkg,'--lib',pattern],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
  text=(B/(name+'.log')).read_text(errors='replace');failed=re.findall(r'^test (\S+) \.\.\. FAILED$',text,re.M);row=dict(name=name,path=path,mutatedSha256=hashlib.sha256(raw).hexdigest(),classification=kind,exitCode=r.returncode,compileFailure='could not compile' in text,failedTests=failed)
  (W/path).write_bytes(original[path]);report['mutations'].append(row);save();assert r.returncode!=0 and failed and not row['compileFailure'],row
finally:
 for p,raw in original.items():(W/p).write_bytes(raw)
 report['restored']=all((W/p).read_bytes()==raw for p,raw in original.items());save()
for pkg,pattern in [('host','native_owner_tests::coverage_producer_recomputes_scope_and_preserves_rc3_rc4_rc6'),('host','native_owner_tests::import_payloads_require_exact_kind_domain_and_retained_schema'),('security','commit_authority::seal_binding_tests'),('host',host_fact)]:
 name=pkg+'-'+pattern.split('::')[-1]
 with (B/('restored-'+name+'.log')).open('wb') as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-'+pkg,'--lib',pattern],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,name
report['all4Caught']=True;report['restoredPositiveControlsPassed']=True;save();print('ALL4COMPILED MUTANTS CAUGHT; EXACT FILES RESTORED; POSITIVES PASS',flush=True)
