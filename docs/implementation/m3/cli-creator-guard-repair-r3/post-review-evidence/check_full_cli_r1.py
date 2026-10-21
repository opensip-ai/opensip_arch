from pathlib import Path
import os, subprocess, tempfile, json, hashlib, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
B = F / 'full-creator-suite-r1'
B.mkdir(exist_ok=False)
W = Path('/Users/sb/code/opensip-ai/opensip-cli-gate-repair')
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'
T = Path(tempfile.mkdtemp(prefix='n-', dir=subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR'], text=True).strip()))
T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS, 0, 10)
E = dict(os.environ, CARGO_HOME='/Users/sb/.cargo', CARGO_TARGET_DIR=str(F / 'target'), TMPDIR=str(T), CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path'], text=True).strip())
source = W / 'apps/cli/tests/creator_commands_tests.rs'
sha = hashlib.sha256(source.read_bytes()).hexdigest()
assert sha == '094bd17bf38bc771ebec281d78bce52e6791cf82121dddfd4ab643c154ac00b9'
with (B / 'runtime.log').open('wb') as out:
    r = subprocess.run([R+'cargo', 'test', '--locked', '--offline', '-p', 'opensip-cli', '--test', 'creator_commands_tests'], cwd=W, env=E, stdout=out, stderr=subprocess.STDOUT)
text = (B / 'runtime.log').read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest() == sha
report = dict(standing='POST-ACCEPTANCE COMPLETE X11 CREATOR TEST MATRIX; EXISTING AUTHORITY/NO HOME OVERRIDE', sourceSha256=sha,
    exitCode=r.returncode, summaries=re.findall(r'^test result:.*$', text, re.M),
    realInstallationAccess='Existing accepted X11 test process only stats installation directory identity/metadata; CLI parser refuses before installation reads. Existing synthetic scratch tree checks retained.',
    productQualification=False, noSourceChanges=True, allPassed=r.returncode == 0 and '8 passed; 0 failed' in text)
(B / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
assert report['allPassed'], text[-3000:]
print('ALL8 CREATOR TEST MATRIX PASS; ACCEPTED SOURCE SHA UNCHANGED')
