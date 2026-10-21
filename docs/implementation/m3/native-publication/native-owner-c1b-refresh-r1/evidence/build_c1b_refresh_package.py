"""Build the C1b batch refresh's pre-run gate package (run on product main once every unit in joined-units.json is
integrated; the lead's LD-CBR-3 may append C2b-0 and C1c-1 there before the freeze): run the freeze
(freeze_c1b_refresh.py) into evidence/frozen-bindings.json, which must pass; write the reviewed SHA-256 of the frozen
record, the freeze script and the post-run checker into the run script's placeholders (refusing if they were already
filled with other values); record the source; and write the subject manifest. Does not run the blind run, open any
held-out material or move main. Usage: build_c1b_refresh_package.py."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
PRE = 'docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1'; S = Path('/tmp/opensip-implementation/native-owner-patterns-2026-10-20/combined-refresh-r1/architecture').resolve(); U = S / PRE; EV = U / 'evidence'
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(root, rel): raw = (root / rel).read_bytes(); return dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
state = json.loads(Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/CURRENT-STATE.json').read_bytes())
joined = json.loads((EV / 'joined-units.json').read_bytes())['joined']
assert [u['unit'] for u in joined][:4] == ['C1b-0', 'C1c-0', 'C1b-1', 'C1b-2'], 'the batch opens with its four C1b units, in order'
for unit in joined:
    assert state.get(unit['publication'], {}).get('productCode') == unit['productCode'], (unit['unit'], 'not integrated')
    assert subprocess.run(['/usr/bin/git', 'merge-base', '--is-ancestor', unit['productCode'], 'HEAD'], cwd=P, env=E).returncode == 0, unit['unit']
    assert (A / unit['record']).is_file(), unit['record']
r = subprocess.run([PY, '-I', '-B', str(EV / 'freeze_c1b_refresh.py'), str(EV / 'frozen-bindings.json')], cwd=P, env=E, capture_output=True)
(EV / 'freeze.log').write_bytes(r.stdout + r.stderr)
assert r.returncode == 0, r.stderr[-2000:]
run = EV / 'run_c1b_refresh_blind.py'; text = run.read_text()
values = {'@FROZEN_SHA256@': sha(EV / 'frozen-bindings.json'), '@FREEZE_SCRIPT_SHA256@': sha(EV / 'freeze_c1b_refresh.py'),
          '@POST_CHECKS_SHA256@': sha(EV / 'run_c1b_refresh_post_checks.py')}
for placeholder, value in values.items():
    assert text.count("'" + placeholder + "'") == 1, ('placeholder already filled', placeholder)
    text = text.replace("'" + placeholder + "'", "'" + value + "'")
run.write_text(text)
frozen = json.loads((EV / 'frozen-bindings.json').read_bytes())
source = dict(freezeBase=frozen['freezeBase'], architectureBase=git(A, 'rev-parse', 'HEAD'), refreshBaseline=frozen['refreshBaseline'],
              pinned=dict(frozenBindings=values['@FROZEN_SHA256@'], freezeScript=values['@FREEZE_SCRIPT_SHA256@'], postChecks=values['@POST_CHECKS_SHA256@']),
              joinedUnits=dict(file=pin(S, PRE + '/evidence/joined-units.json'), units=[dict(unit=u['unit'], productCode=u['productCode']) for u in joined]),
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r6.md',
                  'docs/implementation/m3/reviews/codex-c1b-plan-r6/review.json',
                  'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2/RUN-PLAN.md',
                  'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1a4-blind-run-r1-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1b-0-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1c-0-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1b-1-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1b-2-r1-unit.json',
                  *[u['record'] for u in joined])])
source['interpreter'] = dict(path=PY,bytes=Path(PY).stat().st_size,sha256=sha(Path(PY)))
source['nativeMetadataBindings'] = {'inventory': {'path': 'docs/implementation/m3/native-publication/native-owner-inventory-v234-subject.json', 'bytes': 735, 'sha256': 'af05535329308565b5071c40411351abf736869f6c7de2e30931b8d3bc82814f'}, 'descriptions': {'path': 'docs/implementation/m3/native-publication/native-owner-descriptions-r1-subject.json', 'bytes': 737, 'sha256': '0802a5ffac79ebf5b79b2836e0bd81e7d125191c970b1adae242848e04e19eda'}}
(U / 'source.json').write_text(json.dumps(source, indent=2) + '\n')
files = sorted([pin(S, p.relative_to(S).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda f: f['path'])
(S / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='NATIVE-OWNER-C1B-REFRESH-r1', productBase=frozen['freezeBase'], architectureBase=source['architectureBase'], files=files), indent=2) + '\n')
print(len(files), 'subject files;', pin(S, PRE + '-subject.json'))
