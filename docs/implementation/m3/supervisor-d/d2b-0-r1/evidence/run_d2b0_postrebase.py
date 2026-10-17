"""D2b-0's post-rebase focused check (LD-D2B0-8): with the candidate rebuilt on the package base (the v218 lock commit,
past D2b-1's code commit), the identity suite, host's admission_tests and schema_sources tests, and storage's
schema_sources tests, each run under the lane lock through locked_run.py, and each compared with lane attempt 3's
(base 3e70bbf) result for the same tests. Usage: run_d2b0_postrebase.py <out dir> <attempt-3 lane dir>."""
from pathlib import Path
import json, os, re, subprocess, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b0'); P = W.parent / 'opensip'
O = Path(sys.argv[1]); L3 = Path(sys.argv[2]); O.mkdir(parents=True)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
head = git(W, 'rev-parse', 'HEAD'); assert head == git(P, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
lane_base = json.loads((L3 / 'worktree-base.json').read_bytes())['productBase']
STEPS = [
    ('identity-suite', ['cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', 'opensip-identity'], 'candidate-opensip-identity.log', None),
    ('host-admission-tests', ['cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', 'opensip-host', '--test', 'admission_tests'], 'candidate-opensip-host.log', 'tests/admission_tests.rs'),
    ('host-schema-sources', ['cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'schema_sources'], 'focused-host-schema-sources.log', None),
    ('storage-schema-sources', ['cargo', 'test', '--locked', '--offline', '-p', 'opensip-storage', '--lib', '--', 'schema_sources'], 'focused-storage-schema-sources.log', None),
]
def results(text, binary=None):
    """(passed, failed names) over the whole log, or over one test binary's section of a whole-suite log."""
    if binary is not None:
        parts = re.split(r'^\s+Running ', text, flags=re.M)
        text = ''.join(p for p in parts if p.startswith(binary))
        assert text, binary
    passed = sum(int(p) for p in re.findall(r'test result: \w+\. (\d+) passed', text))
    return passed, sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
rows = []
for name, cmd, attempt3, binary in STEPS:
    log = O / (name + '.log')
    subprocess.run([PY, '-I', '-B', '/tmp/opensip-implementation/locked_run.py', str(W), str(log), R + cmd[0], *cmd[1:]], check=True, env=E)
    text = log.read_text(errors='replace'); now = results(text); before = results((L3 / attempt3).read_text(errors='replace'), binary)
    rows.append(dict(name=name, command=cmd, exit=int(re.findall(r'^EXIT (-?\d+)$', text, re.M)[-1]), passed=now[0], failed=now[1],
                     attempt3=dict(log=attempt3, section=binary, passed=before[0], failed=before[1]), equal=now == before))
    print(name, 'now', now[0], len(now[1]), 'attempt 3', before[0], len(before[1]), 'equal', now == before, flush=True)
import hashlib
mine = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
assert mine == json.loads((L3 / 'edited.json').read_bytes())['paths'], mine
candidate = [dict(path=x, bytes=len((W / x).read_bytes()), sha256=hashlib.sha256((W / x).read_bytes()).hexdigest()) for x in mine]
out = dict(packageBase=head, laneBase=lane_base, candidatePaths=candidate, mainChangedSinceLane=git(P, 'diff', '--name-only', lane_base, head).splitlines(), rows=rows,
           allEqual=all(r['equal'] for r in rows))
(O / 'postrebase.json').write_text(json.dumps(out, indent=2) + '\n')
print('allEqual', out['allEqual']); sys.exit(0 if out['allEqual'] else 1)
