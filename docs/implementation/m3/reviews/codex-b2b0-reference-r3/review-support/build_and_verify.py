"""Build the B2-b0 current discovery reference package in a local architecture stage and prove it binds with the product's
real verify_design (B-S10 scratch pattern: staged files and synthetic review/assent served in memory; nothing is
written to either repository). Run 1: the base lock passes. Run 2: successor 164 appended passes."""
import copy, hashlib, importlib.util, json, shutil, subprocess, sys
from pathlib import Path

D = Path(__file__).resolve().parent; S = D / 'architecture'
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
PRE = 'docs/implementation/m3/config-discovery-b/b2-b-reference'
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
assert not S.exists()


def pin(root, rel):
    raw = (root / rel).read_bytes(); return dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def put(rel, src):
    t = S / rel; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, t)


put(PRE + '/README.md', D / 'README.md')
put(PRE + '/reference/discovery_scan_reference.py', D / 'discovery_scan_reference.py')
put(PRE + '/evidence/check.py', D / 'check.py')
subprocess.run([PY, '-I', '-B', str(S / PRE / 'evidence/check.py'), '--architecture', str(A), '--reference', str(S / PRE / 'reference/discovery_scan_reference.py'),
                '--packages-root', str(P), '--out', str(S / PRE / 'evidence/checks.json')], check=True, stdout=subprocess.DEVNULL)
assert json.loads((S / PRE / 'evidence/checks.json').read_text())['passed'] is True
DD = 'docs/coop/design-corrections/'
parents = [pin(A, p) for p in [
    DD + 'security/security_lifecycle_model_v1.py', DD + 'security/discovery-cases.v1.json', DD + 'security/security-lifecycle.schemas.v1.json', DD + 'foundation/canonical.py',
    'docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py',
    'docs/implementation/m3/config-discovery-b/b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json',
    'docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/implementation/m2/repository-file-inventory.v191.json']]
parents.sort(key=lambda r: r['path'])
candidates = sorted((pin(S, p.relative_to(S).as_posix()) for p in (S / PRE).rglob('*') if p.is_file()), key=lambda r: r['path'])
record = dict(schemaVersion=1, standing='PROPOSED B2-b0 current discovery reference r3 (upward evidence separated, observed-evidence projection, depth before boundary; Codex B2B0REF-1 to 4): SLM with the bound shared-rule reference over the walker observation population, projected to V3 with workspaceDeclarations pending; no SLM, DD or schema change; no product code or qualification',
              parents=parents, passageOverrides=[], candidates=candidates)
(S / PRE / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
files = sorted((pin(S, p.relative_to(S).as_posix()) for p in (S / PRE).rglob('*') if p.is_file()), key=lambda r: r['path'])
(S / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='B2-B0-REFERENCE-r3', files=files), indent=2) + '\n')

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
review = serve('SCRATCH-B2B0-REF/review.json', json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subj['sha256']}).encode())
assent = serve('SCRATCH-B2B0-REF/assent.json', json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subj, 'independentReview': review, 'acceptedSuccessor': rec}).encode())
lock = copy.deepcopy(base_lock); lock['contractSuccessors'].append({'record': rec, 'subjectManifest': subj, 'review': review, 'assent': assent})
status, result = run(lock); out['withSuccessor164'] = status
if result:
    out['contractSuccessors'] = len(result['contractSuccessors']); out['candidates'] = len(result['contractSuccessors'][-1]['inputs'])
out['subjectManifest'] = subj; out['record'] = rec
(D / 'verify-scratch.json').write_text(json.dumps(out, indent=1) + '\n'); print(json.dumps(out, indent=1)); sys.exit(0 if status == 'PASS' and out['baseLock'] == 'PASS' else 1)
