"""Final verification: run every lane, record exact commands and outcomes, restore any
generated report a lane wrote into the source, and re-prove the changed-file set."""
import hashlib, json, os, shutil, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v31'
HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.dirname(HERE)
DC = os.path.join(SRC, 'docs/coop/design-corrections')
REPORTS = os.path.join(HERE, 'lane-reports')
os.makedirs(REPORTS, exist_ok=True)

LANES = [
    ('workflow-projection (contains the new repair-cw section)',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check-workflow-projection.v3.py')],
     os.path.join(DC, 'workflows')),
    ('historical workflows lane',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check_workflows.v1.py'),
      '--report', os.path.join(REPORTS, 'workflows-report.json')],
     os.path.join(DC, 'workflows')),
    ('query projection',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check-query-projection.v3.py'),
      '--report', os.path.join(REPORTS, 'query-projection.json')],
     os.path.join(DC, 'workflows')),
    ('comparison knowledge',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check-comparison-knowledge.v3.py')],
     os.path.join(DC, 'workflows')),
    ('integration',
     [REF, '-I', '-B', os.path.join(DC, 'check-integration.py'),
      '--report', os.path.join(REPORTS, 'integration.json')],
     DC),
    ('identity', [REF, '-I', '-B', os.path.join(DC, 'foundation/check-identity.py')],
     os.path.join(DC, 'foundation')),
    ('atoms', [REF, '-I', '-B', os.path.join(DC, 'foundation/check-atoms.v1.py')],
     os.path.join(DC, 'foundation')),
    ('replay', [REF, '-I', '-B', os.path.join(DC, 'foundation/check-replay.v3.py')],
     os.path.join(DC, 'foundation')),
    ('native evidence (PIN-SEALED lane)',
     [REF, '-I', '-B', os.path.join(DC, 'native/check_native_evidence.v2.py')],
     os.path.join(DC, 'native')),
]

results = []
for label, cmd, cwd in LANES:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=1800)
    head = (p.stdout or '').strip()
    summary = head[-260:].replace('\n', ' ')
    results.append({'lane': label, 'command': cmd, 'cwd': cwd, 'exitCode': p.returncode,
                    'stdoutTail': summary, 'stderrTail': (p.stderr or '')[-300:]})
    print(('PASS' if p.returncode == 0 else 'EXIT%d' % p.returncode), '|', label)

# restore any generated report a lane wrote into the source tree
DECLARED = {
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
}
baseline = {r['path']: r for r in json.load(open(os.path.join(HERE, 'author-source-baseline.json')))['files']}
restored = []
for rel, row in sorted(baseline.items()):
    if rel in DECLARED:
        continue
    full = os.path.join(SRC, rel)
    if hashlib.sha256(open(full, 'rb').read()).hexdigest() != row['sha256']:
        shutil.copy2(os.path.join(FROZEN, rel), full)
        restored.append(rel)
print('restored generated reports:', restored)

json.dump({'lanes': results, 'restoredAfterRun': restored},
          open(os.path.join(RT, 'lane-results.json'), 'w'), indent=2)
print('WROTE lane-results.json')
