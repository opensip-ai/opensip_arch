"""Scan the author source for (a) every pin ledger my edits invalidate and (b) every other
checker lane, so the handoff can name them exactly instead of guessing."""
import hashlib, json, os, subprocess

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
HERE = os.path.dirname(os.path.abspath(__file__))
REF = '/tmp/opensip-architecture-review-env/bin/python'

CHANGED = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
]

# --- (a) pin ledgers
ledgers = []
for dirpath, _dirs, files in os.walk(SRC):
    for name in files:
        if 'source-pins' in name or 'source-pin' in name:
            ledgers.append(os.path.join(dirpath, name))

impact = []
for ledger in sorted(ledgers):
    try:
        doc = json.load(open(ledger))
    except Exception as exc:
        impact.append({'ledger': os.path.relpath(ledger, SRC), 'error': str(exc)[:120]})
        continue
    files = doc.get('files') or []
    idx = {f.get('path'): f.get('sha256') for f in files if isinstance(f, dict)}
    broken = []
    for rel in CHANGED:
        for pinned, digest in idx.items():
            if pinned and (pinned == rel or pinned.endswith('/' + rel) or rel.endswith(pinned)):
                full = os.path.join(SRC, rel)
                now = hashlib.sha256(open(full, 'rb').read()).hexdigest()
                if now != digest:
                    broken.append({'pinnedPath': pinned, 'authorPath': rel,
                                   'pinnedSha256': digest, 'currentSha256': now})
    impact.append({'ledger': os.path.relpath(ledger, SRC), 'pinnedFiles': len(files),
                   'brokenByThisAuthor': broken})

print('--- pin ledgers')
for row in impact:
    print(' ', row['ledger'], 'pins', row.get('pinnedFiles'), 'broken', len(row.get('brokenByThisAuthor', [])))
    for b in row.get('brokenByThisAuthor', []):
        print('      ', b['pinnedPath'])

# --- (b) other checker lanes
LANES = [
    ('workflows/check-query-projection.v3.py', 'docs/coop/design-corrections/workflows'),
    ('workflows/check-comparison-knowledge.v3.py', 'docs/coop/design-corrections/workflows'),
    ('native/check_native_evidence.v2.py', 'docs/coop/design-corrections/native'),
    ('foundation/check-identity.py', 'docs/coop/design-corrections/foundation'),
    ('foundation/check-atoms.v1.py', 'docs/coop/design-corrections/foundation'),
    ('foundation/check-replay.v3.py', 'docs/coop/design-corrections/foundation'),
    ('check-integration.py', 'docs/coop/design-corrections'),
]
lane_results = []
print('\n--- other lanes')
for script, cwd in LANES:
    path = os.path.join(SRC, 'docs/coop/design-corrections', script) if not script.startswith('check-integration') \
        else os.path.join(SRC, 'docs/coop/design-corrections', script)
    if not os.path.exists(path):
        print('  MISSING', script)
        lane_results.append({'lane': script, 'status': 'missing'})
        continue
    try:
        p = subprocess.run([REF, '-I', '-B', path], capture_output=True, text=True,
                           cwd=os.path.join(SRC, cwd), timeout=1800)
        tail = (p.stdout or '')[-300:].replace('\n', ' ')
        print('  exit', p.returncode, script, '|', tail[-200:])
        lane_results.append({'lane': script, 'exitCode': p.returncode,
                             'stdoutTail': tail, 'stderrTail': (p.stderr or '')[-400:]})
    except subprocess.TimeoutExpired:
        print('  TIMEOUT', script)
        lane_results.append({'lane': script, 'status': 'timeout'})

json.dump({'changedFiles': CHANGED, 'pinLedgers': impact, 'lanes': lane_results},
          open(os.path.join(HERE, 'impact-scan.json'), 'w'), indent=2)
print('\nWROTE impact-scan.json')
