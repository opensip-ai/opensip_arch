"""Run the product's existing design-binding tests (at REV) against the REV tool and against the VD2 prototype.

Each run copies `tools/verify_design.py` and `tools/tests/test_design_binding.py` into a fresh private temporary tree
(mode 0700, under TMPDIR) and runs `python3.14 -B -m unittest discover -s tools/tests -p test_design_binding.py` there.
Nothing is written to either repository. The test file is read with `git show`; it binds its tool by relative path.

Expected (law VD2, "Prototype evidence"): REV, 83 tests OK. Prototype, 82 OK and exactly one failure,
PassageSupersessionTests.test_supersession_of_non_inventory_passage_refuses, whose first half is now VD2's own case
and reaches "contract passage supersession is not listed by its review". VD2-a rewrites that test.

Usage: python3.14 -I -B run_existing_tests.py [--tool PATH] [--product CHECKOUT] [--rev REV] [--json OUT]
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--tool', type=Path, default=HERE.parent / 'reference/verify_design.prototype.py')
ap.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
ap.add_argument('--rev', default='6190e66')
ap.add_argument('--json', type=Path)
args = ap.parse_args()
PY = sys.executable
EXPECTED_FAILURE = 'test_supersession_of_non_inventory_passage_refuses'


def show(path):
    return subprocess.run(['git', '-C', str(args.product), 'show', f'{args.rev}:{path}'], check=True,
                          capture_output=True).stdout


tests = show('tools/tests/test_design_binding.py')
runs = {}
for label, tool in (('rev', show('tools/verify_design.py')), ('prototype', args.tool.read_bytes())):
    with tempfile.TemporaryDirectory() as tmp:
        os.chmod(tmp, 0o700)
        root = Path(tmp)
        (root / 'tools/tests').mkdir(parents=True)
        (root / 'tools/verify_design.py').write_bytes(tool)
        (root / 'tools/tests/test_design_binding.py').write_bytes(tests)
        proc = subprocess.run([PY, '-B', '-m', 'unittest', 'discover', '-s', 'tools/tests', '-p', 'test_design_binding.py'],
                              cwd=root, capture_output=True, text=True,
                              env={'PATH': '/usr/bin:/bin', 'TMPDIR': tmp, 'LANG': 'C', 'LC_ALL': 'C'})
    ran = re.search(r'Ran (\d+) tests', proc.stderr)
    failures = re.findall(r'^(?:FAIL|ERROR): (\w+) \(([\w.]+)\)', proc.stderr, re.M)
    messages = re.findall(r'^AssertionError: (.*)$', proc.stderr, re.M)
    runs[label] = {'tool': {'bytes': len(tool), 'sha256': hashlib.sha256(tool).hexdigest()},
                   'returncode': proc.returncode, 'ran': int(ran.group(1)) if ran else None,
                   'failures': [{'test': t, 'where': w} for t, w in failures], 'assertionMessages': messages,
                   'summary': proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ''}
ok = (runs['rev']['returncode'] == 0 and runs['rev']['ran'] == 83
      and runs['prototype']['ran'] == 83 and [f['test'] for f in runs['prototype']['failures']] == [EXPECTED_FAILURE])
result = {'rev': args.rev, 'testFile': {'bytes': len(tests), 'sha256': hashlib.sha256(tests).hexdigest()},
          'python': PY, 'runs': runs, 'expectedInversion': EXPECTED_FAILURE, 'ok': ok}
print(json.dumps(result, indent=1))
if args.json:
    args.json.write_text(json.dumps(result, indent=1) + '\n')
sys.exit(0 if ok else 1)
