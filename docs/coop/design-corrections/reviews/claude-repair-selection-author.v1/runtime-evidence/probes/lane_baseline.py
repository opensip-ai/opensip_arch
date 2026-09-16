"""Run the two non-zero lanes against BOTH frozen31 and the author source, so the handoff
can say whether a failure is mine or pre-existing/pin-driven."""
import json, os, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
HERE = os.path.dirname(os.path.abspath(__file__))
TREES = {
    'frozen31': '/tmp/opensip-design-corrections/candidate-subject.v31',
    'author': '/tmp/opensip-design-corrections/repair-selection-successor.v1/source',
}
LANES = [
    ('docs/coop/design-corrections/workflows/check-query-projection.v3.py',
     'docs/coop/design-corrections/workflows'),
    ('docs/coop/design-corrections/check-integration.py',
     'docs/coop/design-corrections'),
    ('docs/coop/design-corrections/native/check_native_evidence.v2.py',
     'docs/coop/design-corrections/native'),
]

out = {}
for tree_name, root in TREES.items():
    out[tree_name] = []
    for script, cwd in LANES:
        path = os.path.join(root, script)
        if not os.path.exists(path):
            out[tree_name].append({'lane': script, 'status': 'missing'})
            continue
        p = subprocess.run([REF, '-I', '-B', path], capture_output=True, text=True,
                           cwd=os.path.join(root, cwd), timeout=1800)
        combined = ((p.stdout or '') + '\n' + (p.stderr or '')).strip()
        out[tree_name].append({'lane': script, 'exitCode': p.returncode,
                               'tail': combined[-900:]})
        print(tree_name, 'exit', p.returncode, script)

for script, _ in LANES:
    a = next(r for r in out['frozen31'] if r['lane'] == script)
    b = next(r for r in out['author'] if r['lane'] == script)
    same = a.get('exitCode') == b.get('exitCode')
    print('\n===', script)
    print('  frozen31 exit', a.get('exitCode'), '| author exit', b.get('exitCode'),
          '| SAME:', same)
    if not same:
        print('  author tail:', b.get('tail', '')[-700:])
    else:
        print('  frozen31 tail:', a.get('tail', '')[-400:])

json.dump(out, open(os.path.join(HERE, 'lane-baseline.json'), 'w'), indent=2)
print('\nWROTE lane-baseline.json')
