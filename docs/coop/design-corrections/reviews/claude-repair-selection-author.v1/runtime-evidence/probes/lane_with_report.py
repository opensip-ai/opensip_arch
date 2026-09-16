"""Run the two lanes that require --report, on both trees, writing reports into MY runtime."""
import json, os, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, 'lane-reports')
os.makedirs(OUTDIR, exist_ok=True)
TREES = {
    'frozen31': '/tmp/opensip-design-corrections/candidate-subject.v31',
    'author': '/tmp/opensip-design-corrections/repair-selection-successor.v1/source',
}
LANES = [
    ('docs/coop/design-corrections/workflows/check-query-projection.v3.py',
     'docs/coop/design-corrections/workflows', '--report'),
    ('docs/coop/design-corrections/check-integration.py',
     'docs/coop/design-corrections', '--report'),
]

out = {}
for tree, root in TREES.items():
    out[tree] = []
    for script, cwd, flag in LANES:
        name = os.path.basename(script).replace('.py', '') + '.' + tree + '.json'
        report = os.path.join(OUTDIR, name)
        p = subprocess.run([REF, '-I', '-B', os.path.join(root, script), flag, report],
                           capture_output=True, text=True, cwd=os.path.join(root, cwd), timeout=1800)
        combined = ((p.stdout or '') + '\n' + (p.stderr or '')).strip()
        out[tree].append({'lane': script, 'exitCode': p.returncode, 'report': report,
                          'tail': combined[-800:]})
        print(tree, 'exit', p.returncode, os.path.basename(script))

for script, _, _ in LANES:
    a = next(r for r in out['frozen31'] if r['lane'] == script)
    b = next(r for r in out['author'] if r['lane'] == script)
    print('\n===', os.path.basename(script))
    print('  frozen31 exit', a['exitCode'], '| author exit', b['exitCode'],
          '| SAME:', a['exitCode'] == b['exitCode'])
    print('  author tail:', b['tail'][-600:])

json.dump(out, open(os.path.join(HERE, 'lane-with-report.json'), 'w'), indent=2)
print('\nWROTE lane-with-report.json')
