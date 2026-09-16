"""P7: how CELL_STATE is built, what the matrix row for each disputed cell actually says,
and what _carrier does with it."""
import importlib.util, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
FOUND = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation')
MODEL = os.path.join(FOUND, 'execution_inputs_model.v1.py')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load('owner', MODEL)
src = open(MODEL).read()
lines = src.split('\n')

for pat in (r'CELL_STATE\s*=', r'^def _carrier', r'^def _matrix_cause', r'^def _matrix_pairs'):
    m = re.search(pat, src, re.M)
    if not m:
        print('NOT FOUND', pat)
        continue
    ln = src[:m.start()].count('\n') + 1
    print('\n--- %s  (line %d)' % (pat, ln))
    for i in range(ln - 1, min(len(lines), ln + 24)):
        print(i + 1, lines[i][:180])

print('\n=== CELL_STATE rows for the disputed cells')
disputed = [('imports', 'syntax-only'), ('unresolved-edge', 'syntax-only'),
            ('clones-fact', 'syntax-only'), ('syntax', 'syntax-only'),
            ('inventory', 'syntax-only'), ('inventory', 'rust-cargo'),
            ('inventory', 'js-allowjs')]
rows = {}
for cap, mode in disputed:
    r = M.CELL_STATE.get((cap, mode))
    rows['%s|%s' % (cap, mode)] = r
    print('  %-16s %-12s -> %s' % (cap, mode, json.dumps(r)))

print('\n=== _matrix_pairs for the disputed capabilities')
pairs = {}
for cap in ('imports', 'unresolved-edge', 'clones-fact', 'syntax', 'inventory'):
    p = M._matrix_pairs(cap)
    pairs[cap] = p
    print('  %-16s -> %s' % (cap, p))

print('\n=== _matrix_cause / _carrier behaviour on the disputed deficiency')
probe = {}
for deficiency in (None, 'language-tier-unsupported', 'provider-unavailable'):
    cause = M._matrix_cause(deficiency)
    faults = []
    M._carrier(deficiency, cause, faults)
    probe[str(deficiency)] = {'cause': cause, 'carrierFaults': list(faults)}
    print('  deficiency=%-26s cause=%-20s carrierFaults=%s' % (deficiency, cause, faults))

# what does _carrier do with a null pair, as a partial outcome row would carry?
faults = []
M._carrier(None, None, faults)
print('  _carrier(None, None) -> %s' % faults)
probe['nullPair'] = list(faults)

json.dump({'cellStateRows': rows, 'matrixPairs': pairs, 'carrierProbe': probe},
          open(os.path.join(HERE, 'p7-cellstate.json'), 'w'), indent=2)
print('\nWROTE p7-cellstate.json')
