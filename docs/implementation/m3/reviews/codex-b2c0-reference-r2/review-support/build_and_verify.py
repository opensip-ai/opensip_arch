"""Build the B2-c0 current native unit reference package in a local architecture stage and prove it binds with the
product's real verify_design (the B2-b0 scratch pattern: staged files and synthetic review/assent served in memory; nothing
is written to either repository). Run 1: the base lock passes. Run 2: successor 166, with its NE passage override, passes."""
import copy, hashlib, importlib.util, json, shutil, subprocess, sys
from pathlib import Path

D = Path(__file__).resolve().parent; S = D / 'architecture'
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
PRE = 'docs/implementation/m3/config-discovery-b/b2-c-reference'
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
PKG = P / 'tools/contracts/python-packages'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
LINE = 838
BEFORE = '  inventory must appear in the admitted inventory with the SAME `reason`; a missing'
AFTER = ('  inventory outside every admitted boundary must appear in the admitted inventory with the SAME `reason` (contract '
         'successor B2-c0, LD-B2C0-1: security S3 records a nested repository or project and never enters it, so an anchor '
         'at or below an admitted boundary is not compared); a missing')
assert not S.exists()


def pin(root, rel):
    raw = (root / rel).read_bytes(); return dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def put(rel, src):
    t = S / rel; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, t)


assert (A / NE).read_text().split('\n')[LINE - 1] == BEFORE
put(PRE + '/README.md', D / 'README.md')
put(PRE + '/reference/native_unit_reference.py', D / 'reference/native_unit_reference.py')
put(PRE + '/evidence/check.py', D / 'evidence/check.py')
subprocess.run([PY, '-I', '-B', str(S / PRE / 'evidence/check.py'), '--architecture', str(A), '--packages', str(PKG),
                '--reference', str(S / PRE / 'reference/native_unit_reference.py'), '--out', str(S / PRE / 'evidence/checks.json')], check=True, stdout=subprocess.DEVNULL)
assert json.loads((S / PRE / 'evidence/checks.json').read_text())['passed'] is True
DC = 'docs/coop/design-corrections/'
parents = [pin(A, p) for p in [
    'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py', DC + 'foundation/canonical.py', DC + 'foundation/identity-model.py',
    DC + 'discovery-defaults.py', DC + 'native/native-evidence.schemas.v2.json', DC + 'native/native-capability-matrix.v2.json',
    DC + 'native/native-cases.v2.json', DC + 'native/check_native_evidence.v2.py', DC + 'security/check-security-lifecycle.v1.py',
    'docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py',
    'docs/implementation/m3/config-discovery-b/b-s1/schemas/native-evidence.schemas.v2.b-s1-additions.json',
    'docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py', NE]]
parents.sort(key=lambda r: r['path'])
ne = next(p for p in parents if p['path'] == NE)
candidates = sorted((pin(S, p.relative_to(S).as_posix()) for p in (S / PRE).rglob('*') if p.is_file()), key=lambda r: r['path'])
record = dict(schemaVersion=1, standing='PROPOSED B2-c0 current native unit reference r2 (B2-c plan r2 section 1; Codex B2C0REF-R1-RF-1, the full admitted-boundary predicate): the selected native model (contract successor 81) at its accepted bytes with its loading closure, the B2-a shared rule bound to the admitted members, AdmittedBoundaryInventoryV3 input and UnitDiscoveryV3 output with the B-S1 U-8 member rules; one NE passage override (LD-B2C0-1: anchors at or below an admitted boundary are not compared, because S3 never enters a nested repository or project); no NE schema, SLM, DD or product change; no qualification',
              parents=parents, passageOverrides=[dict(parent=ne, selector={'line': LINE}, before=BEFORE, after=AFTER)], candidates=candidates)
(S / PRE / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
files = sorted((pin(S, p.relative_to(S).as_posix()) for p in (S / PRE).rglob('*') if p.is_file()), key=lambda r: r['path'])
(S / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='B2-C0-REFERENCE-r2', files=files), indent=2) + '\n')

spec = importlib.util.spec_from_file_location('vd', P / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base_lock = json.loads((P / 'design-lock.json').read_text())
synthetic = {p.relative_to(S).as_posix(): p.read_bytes() for p in S.rglob('*') if p.is_file()}
real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256'] and len(raw) == row['bytes']; return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes


def pin_bytes(path, b): return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def serve(path, raw): synthetic[path] = raw; return pin_bytes(path, raw)


def run(lock):
    try: return 'PASS', m.verify(A, lock, P)
    except m.DesignError as exc: return 'REFUSED: ' + str(exc), None


out = {'baseLock': run(base_lock)[0]}
rec = pin_bytes(PRE + '/successor.json', synthetic[PRE + '/successor.json']); subj = pin_bytes(PRE + '-subject.json', synthetic[PRE + '-subject.json'])
review = serve('SCRATCH-B2C0-REF/review.json', json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subj['sha256']}).encode())
assent = serve('SCRATCH-B2C0-REF/assent.json', json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subj, 'independentReview': review, 'acceptedSuccessor': rec}).encode())
lock = copy.deepcopy(base_lock); lock['contractSuccessors'].append({'record': rec, 'subjectManifest': subj, 'review': review, 'assent': assent})
status, result = run(lock); out['withSuccessor166'] = status
if result:
    out['contractSuccessors'] = len(result['contractSuccessors']); out['candidates'] = len(result['contractSuccessors'][-1]['inputs'])
    out['passageOverrides'] = len(result['contractSuccessors'][-1]['passageOverrides'])
out['subjectManifest'] = subj; out['record'] = rec
(D / 'verify-scratch.json').write_text(json.dumps(out, indent=1) + '\n'); print(json.dumps(out, indent=1)); sys.exit(0 if status == 'PASS' and out['baseLock'] == 'PASS' else 1)
