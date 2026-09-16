"""Run the changed + relevant regression lanes once, capturing FULL receipts.

Any report a lane writes into the source tree is PRESERVED into this runtime before its
original bytes are restored, per the instruction not to silently discard generated output.
"""
import hashlib, json, os, shutil, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
V1 = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.dirname(HERE)
DC = os.path.join(SRC, 'docs/coop/design-corrections')
REPORTS = os.path.join(HERE, 'lane-reports')
RECEIPTS = os.path.join(HERE, 'receipts')
PRESERVED = os.path.join(HERE, 'preserved-source-reports')
for d in (REPORTS, RECEIPTS, PRESERVED):
    os.makedirs(d, exist_ok=True)

OWNED = {
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py',
}

LANES = [
    ('workflow-projection (CHANGED: hosts the repair-cw section)',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check-workflow-projection.v3.py')],
     os.path.join(DC, 'workflows')),
    ('workflows historical lane (CHANGED: workflows_model.v1 seam)',
     [REF, '-I', '-B', os.path.join(DC, 'workflows/check_workflows.v1.py'),
      '--report', os.path.join(REPORTS, 'workflows-report.json')],
     os.path.join(DC, 'workflows')),
    ('replay (REGRESSION: fixture option added)',
     [REF, '-I', '-B', os.path.join(DC, 'foundation/check-replay.v3.py')],
     os.path.join(DC, 'foundation')),
    ('semantic replay (REGRESSION: fixture)',
     [REF, '-I', '-B', os.path.join(DC, 'foundation/check-semantic-replay.v3.py')],
     os.path.join(DC, 'foundation')),
    ('execution replay (REGRESSION: fixture)',
     [REF, '-I', '-B', os.path.join(DC, 'foundation/check-execution-replay.v3.py')],
     os.path.join(DC, 'foundation')),
    ('enumeration (REGRESSION: enumeration owner untouched)',
     [REF, '-I', '-B', os.path.join(DC, 'foundation/check-enumeration.v1.py')],
     os.path.join(DC, 'foundation')),
    ('identity (REGRESSION)',
     [REF, '-I', '-B', os.path.join(DC, 'foundation/check-identity.py')],
     os.path.join(DC, 'foundation')),
    ('integration (REGRESSION)',
     [REF, '-I', '-B', os.path.join(DC, 'check-integration.py'),
      '--report', os.path.join(REPORTS, 'integration.json')],
     DC),
    ('native evidence (PIN-SEALED lane)',
     [REF, '-I', '-B', os.path.join(DC, 'native/check_native_evidence.v2.py')],
     os.path.join(DC, 'native')),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


baseline = {r['path']: r['sha256']
            for r in json.load(open(os.path.join(HERE, 'v2-source-baseline.json')))['baseline'].items()
            } if False else None
base = json.load(open(os.path.join(HERE, 'v2-source-baseline.json')))['baseline']

results = []
for label, cmd, cwd in LANES:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=2400)
    name = os.path.basename(cmd[3]).replace('.py', '') + '.receipt.json'
    json.dump({'lane': label, 'command': cmd, 'cwd': cwd, 'exitCode': p.returncode,
               'stdout': p.stdout, 'stderr': p.stderr},
              open(os.path.join(RECEIPTS, name), 'w'), indent=2)
    results.append({'lane': label, 'command': cmd, 'cwd': cwd, 'exitCode': p.returncode,
                    'stdoutBytes': len(p.stdout), 'stderrBytes': len(p.stderr),
                    'receipt': 'probes/receipts/' + name,
                    'stdoutTail': (p.stdout or '').strip()[-300:]})
    print(('PASS ' if p.returncode == 0 else 'EXIT%d' % p.returncode), label)

# preserve then restore anything a lane generated inside the source tree
touched = []
for rel, row in sorted(base.items()):
    if rel in OWNED:
        continue
    full = os.path.join(SRC, rel)
    if sha(full) != row['sha256']:
        keep = os.path.join(PRESERVED, rel)
        os.makedirs(os.path.dirname(keep), exist_ok=True)
        shutil.copy2(full, keep)
        origin = os.path.join(V1, rel)
        assert sha(origin) == row['sha256'], rel
        shutil.copy2(origin, full)
        touched.append({'path': rel, 'preservedAt': 'probes/preserved-source-reports/' + rel,
                        'restoredToSha256': row['sha256'],
                        'reason': 'generated report rewritten by running a lane in-tree'})
        print('preserved+restored', rel)

json.dump({'lanes': results, 'generatedSourceReportsPreservedAndRestored': touched},
          open(os.path.join(RT, 'lane-results.json'), 'w'), indent=2)
print('WROTE lane-results.json')
