from pathlib import Path
import os, subprocess, json, hashlib, tempfile, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
B = F/'owning-r2'
B.mkdir(exist_ok=False)
W = Path('/Users/sb/code/opensip-ai/opensip-doctor-gate-repair')
P = W.parent/'opensip'
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'
path = 'apps/cli/tests/doctor_tests.rs'
prepared = json.loads((F/'PREPARED.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==prepared['parent']
assert subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=W,text=True).strip()==path
assert hashlib.sha256((W/path).read_bytes()).hexdigest()==json.loads((F/'owning-r1/report.json').read_text())['source']['sha256']
(W/path).write_bytes((F/'next-source'/path).read_bytes())
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()))
T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
r=subprocess.run([R+'rustfmt','--edition','2024',str(W/path)],cwd=W,env=E,capture_output=True)
(B/'format.log').write_bytes(r.stdout+r.stderr)
assert r.returncode==0
raw=(W/path).read_bytes()
report=dict(standing='DOCTOR TEST-ONLY SOURCE PROJECTION REPAIR; UNACCEPTED',source=dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),mutants=[],productQualification=False,unitAccepted=False)
def save():
    (B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def compile(folder, fresh):
    folder.mkdir(parents=True,exist_ok=True)
    r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-cli','--test','doctor_tests'],cwd=W,env=E,capture_output=True)
    (folder/'build.log').write_bytes(r.stderr)
    (folder/'artifacts.jsonl').write_bytes(r.stdout)
    assert r.returncode==0,'Compile failure never counts as runtime refusal'
    rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='doctor_tests']
    assert len(rows)==1 and rows[0]['target']['src_path']==str(W/path)
    row=rows[0]
    assert not fresh or not row['fresh']
    binary=Path(row['executable'])
    meta=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not row['fresh'])
    (folder/'binary.json').write_text(json.dumps(meta,indent=2)+'\n')
    return binary
def positive(folder,binary):
    r=subprocess.run([str(binary)],cwd=W,env=E,capture_output=True)
    (folder/'runtime.log').write_bytes(r.stdout+r.stderr)
    assert r.returncode==0 and b'6 passed; 0 failed' in r.stdout
binary=compile(B/'positive',False)
positive(B/'positive',binary)
with (B/'cli-clippy.log').open('wb')as out:
    r=subprocess.run([R+'cargo','clippy','--locked','--offline','-p','opensip-cli','--all-targets','--','-D','warnings'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
mutants=[
    ('surrounding-production-erased','text.replacen(KNOWN_LOGGING_TESTS, "", 1)','String::new()','logging exclusion must preserve surrounding production'),
    ('foreign-path-exception','outcomes && logging_block_is_pinned(text)','(true || outcomes) && logging_block_is_pinned(text)','other paths must not gain the logging exception'),
    ('top-level-prefix-fence-skipped','outcomes && logging_block_is_pinned(text)','outcomes && text.matches(KNOWN_LOGGING_TESTS).count() == 1','nested logging module must remain visible'),
    ('blind-tail-truncation', 'let text = strip_known_test_tail(&text);', 'let text = text.split("#[cfg(test)]\\nmod tests").next().unwrap();', 'production after a final tests module must remain visible'),
    ('feature-graph-widened','matching[0]["features"] != expected_features','(false && matching[0]["features"] != expected_features)','unknown or default features must remain refused'),
    ('unknown-test-shape-hidden','\n        text.to_owned()\n','\n        text.replace("cfg(test)", "")\n','unknown logging test shape must remain visible'),
]
for name,old,new,witness in mutants:
    assert raw.decode().count(old)==1,(name,old)
    (W/path).write_text(raw.decode().replace(old,new))
    error=None
    try:
        binary=compile(B/name,True)
        r=subprocess.run([str(binary),'--exact','doctor_feature_declarations_keep_the_accepted_opt_in_graph' if name=='feature-graph-widened' else 'production_projection_excludes_only_the_exact_logging_test_module'],cwd=W,env=E,capture_output=True)
        log=r.stdout+r.stderr
        (B/name/'runtime.log').write_bytes(log)
        assert r.returncode!=0 and witness.encode() in log and b'0 passed; 1 failed' in log
        report['mutants'].append(dict(id=name,compiled=True,runtimeCaught=True,witness=witness,runtimeExitCode=r.returncode))
    except BaseException as ex:
        error=ex
    finally:
        (W/path).write_bytes(raw)
        assert hashlib.sha256((W/path).read_bytes()).hexdigest()==report['source']['sha256']
        binary=compile(B/(name+'-restored-positive'),True)
        positive(B/(name+'-restored-positive'),binary)
        report['allRestored']=True
        save()
    if error:
        raise error
report.update(allPassed=True,doctorTests=6,cliClippyPassed=True,newPaths=0,productionChanges=False)
save()
print('ALL6 DOCTOR TESTS/CLIPPY PASS;6COMPILED MUTANTS CAUGHT/RESTORED; NO UNIT ACCEPTANCE')
