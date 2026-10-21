from pathlib import Path
import os, sys, json, subprocess, tempfile, hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
mode = sys.argv[1]
assert mode in ('red', 'green')
B = F / ('subject-count-' + mode + '-r' + (sys.argv[2] if len(sys.argv) > 2 else '1'))
B.mkdir(exist_ok=False)
W = Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover')
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'
T = Path(tempfile.mkdtemp(prefix='n-', dir=subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR'], text=True).strip()))
T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS, 0, 10)
E = dict(os.environ, CARGO_HOME='/Users/sb/.cargo', CARGO_TARGET_DIR=str(F/'target'), TMPDIR=str(T), CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path'], text=True).strip())
r = subprocess.run([R+'rustfmt', '--edition', '2024', str(W/'crates/components/src/provider_protocol/rust3/receive_tests.rs')], cwd=W, env=E, capture_output=True)
(B/'format.log').write_bytes(r.stdout+r.stderr)
assert r.returncode == 0
paths = sorted(subprocess.check_output(['git', 'ls-files', '-m', '-o', '--exclude-standard'], cwd=W, text=True).splitlines())
pins = []
for path in paths:
    raw = (W/path).read_bytes()
    pins.append(dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
r = subprocess.run([R+'cargo', 'test', '--locked', '--offline', '--no-run', '--message-format=json', '-p', 'opensip-components', '--lib'], cwd=W, env=E, capture_output=True)
(B/'build.log').write_bytes(r.stderr)
(B/'artifacts.jsonl').write_bytes(r.stdout)
assert r.returncode == 0, 'Compilation failure never proves refusal'
rows = [j for l in r.stdout.splitlines() if l.startswith(b'{') and (j:=json.loads(l)).get('reason')=='compiler-artifact' and j.get('executable') and j['target']['name']=='opensip_components']
assert len(rows)==1
row=rows[0]
binary=Path(row['executable'])
test='provider_protocol::rust3::receive::tests::rust3_receive_examined_subject_count_echo_precedes_publication_for_all_coverage_paths'
r=subprocess.run([str(binary), '--exact', test], cwd=W, env=E, capture_output=True)
raw=r.stdout+r.stderr
(B/'runtime.log').write_bytes(raw)
observed = r.returncode != 0 and b'subject-count echo must refuse before publication' in raw and b'0 passed; 1 failed' in raw
report=dict(standing='PRESERVED ACTUAL RF1 RED' if mode=='red' else 'RF1 FOCUSED GREEN; UNIT REVIEW STILL REQUIRED', mode=mode,
    sourcePins=pins, productParent=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=W, text=True).strip(),
    compiled=True, freshCompilerArtifact=not row['fresh'], binary=dict(path=str(binary), sha256=hashlib.sha256(binary.read_bytes()).hexdigest()),
    test=test, runtimeExitCode=r.returncode, actualMissingGuardObserved=observed,
    allPassed=observed if mode=='red' else r.returncode==0 and b'1 passed; 0 failed' in raw,
    forgedCounts=[0,'expected+1','uint64MAX'], stages=2, paths=['CoverageV3','Unavailable','BudgetExhausted'], controls=18,
    productQualification=False, unitAccepted=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['allPassed'], raw.decode()[-4000:]
print(mode.upper(), 'RF1 actual receiver controls compiled and observed')
