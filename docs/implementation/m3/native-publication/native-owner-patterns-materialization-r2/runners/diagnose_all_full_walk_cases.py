"""Temporary strict all-case diagnostic; restore the original test source always.
No product behavior or expected verdict changes. Not final-unit test evidence.
"""
from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'full-walk-all-cases-diagnostic-r1';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
p=W/'crates/host/src/native_owner_tests.rs';original=p.read_bytes();text=original.decode();start=text.index('fn full_retained_walk_checks_complete_inputs_faults_and_separate_limits()');end=text.index('\n#[test]',start);part=text[start:end]
needle='    let f = object(&fixture);\n';assert part.count(needle)==1;part=part.replace(needle,needle+'    let mut mismatches = Vec::new();\n    let mut visited = 0usize;\n')
needle='    for (name, case) in object(&f["cases"]) {\n';assert part.count(needle)==1;part=part.replace(needle,needle+'        visited += 1;\n')
needle='                assert_eq!(string(&expected["result"]), "checked", "{name}");';assert part.count(needle)==1;part=part.replace(needle,'                if string(&expected["result"]) != "checked" { mismatches.push(format!("{name}: expected {}, actual checked", string(&expected["result"]))); }')
needle='                assert_eq!(class, string(&expected["result"]), "{name}: {detail}");';assert part.count(needle)==1;part=part.replace(needle,'                if class != string(&expected["result"]) { mismatches.push(format!("{name}: expected {}, actual {class}: {detail}", string(&expected["result"]))); }')
needle='                        assert!(detail.contains(cause), "{name}: {detail}");';assert part.count(needle)==1;part=part.replace(needle,'                        if !detail.contains(cause) { mismatches.push(format!("{name}: expected cause {cause}: {detail}")); }')
tail='    }\n}\n';assert part.endswith(tail);part=part[:-len(tail)]+'    }\n    eprintln!("FULL_WALK_CASES_VISITED={visited}");\n    assert!(mismatches.is_empty(), "ALL_FULL_WALK_MISMATCHES:\\n{}", mismatches.join("\\n"));\n}\n'
candidate=(text[:start]+part+text[end:]).encode();(B/'original-test-source.rs').write_bytes(original);(B/'diagnostic-test-source.rs').write_bytes(candidate)
T=Path(tempfile.mkdtemp(prefix='opensip-fullwalk-diagnostic-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
try:
 p.write_bytes(candidate)
 with (B/'run.log').open('wb') as out:r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','native_owner_tests::full_retained_walk_checks_complete_inputs_faults_and_separate_limits','--','--nocapture'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
finally:p.write_bytes(original)
assert p.read_bytes()==original
log=(B/'run.log').read_text(errors='replace');report=dict(standing='TEMPORARY STRICT ALL-CASE DIAGNOSTIC; NOT FINAL PRODUCT TEST IMAGE OR UNIT ACCEPTANCE',exitCode=r.returncode,originalSourceSha256=hashlib.sha256(original).hexdigest(),diagnosticSourceSha256=hashlib.sha256(candidate).hexdigest(),originalRestored=True,visited=re.findall(r'FULL_WALK_CASES_VISITED=(\d+)',log),compileFailure='could not compile' in log,privateTMPDIR=str(T),TMPDIRMode='0700',productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
