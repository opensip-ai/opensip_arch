import copy, json, sys
from pathlib import Path
W = Path('/tmp/opensip-implementation/m1-eight-output-review-02/work'); T = W / 'targeted2'
sys.path.insert(0, str(W / 'subject/witness-provenance'))
import witness_common as wc
reference, registry, _ = wc.load()
w = json.loads((W / 'subject/witness-provenance/witnesses.json').read_bytes(), parse_float=wc.no_float)['cases']
targets = json.loads((W / 'subject/targets.json').read_bytes()); inv = {v: k for k, v in targets.items()}
rows, log = [], []
def emit(name, value, label):
    ref = inv[name]; err = wc.check(reference, registry, ref, value)
    log.append({'label': label, 'pythonValid': err is None, 'error': err and err[:160]})
    if err is None: rows.append((ref, value, label))
sarif = copy.deepcopy(next(c['value'] for c in w if c['ref'] == inv['Sarif2Result']))
for label, props in [('sarif-min', {'k': -(2**63)}), ('sarif-i64max+1', {'k': 2**63}), ('sarif-u64max', {'k': 2**64 - 1}),
                     ('sarif-mixed', {'a': -(2**63), 'b': 2**64 - 1, 'c': 'x', 'd': True, 'e': 0}), ('sarif-empty-map', {}),
                     ('sarif-u64max+1', {'k': 2**64}), ('sarif-below-min', {'k': -(2**63) - 1})]:
    v = copy.deepcopy(sarif); v['message']['properties'] = props; emit('Sarif2Result', v, label)
ru = copy.deepcopy(next(c['value'] for c in w if c['ref'] == inv['Native2RustUniverseV2ResolvedInputs']))
for label, ed in [('edition-2024', {'crate_a': 2024, 'crate_b': 2015}), ('edition-2023-invalid', {'crate_a': 2023})]:
    v = copy.deepcopy(ru); v['edition'] = ed; emit('Native2RustUniverseV2ResolvedInputs', v, label)
(T / 'rust/carrier-cases.json').write_text(json.dumps({'rows': [[r, i] for i, (r, _, _) in enumerate(rows)], 'values': [v for _, v, _ in rows]}))
(T / 'raw.json').write_text(json.dumps([{'ref': r, 'kind': l, 'raw': json.dumps(v)} for r, v, l in rows]))
def lit(v):
    if v is None: return 'null'
    if v is True: return 'true'
    if v is False: return 'false'
    if type(v) is int: return '%dn' % v
    if type(v) is str: return json.dumps(v)
    if type(v) is list: return '[' + ','.join(lit(x) for x in v) + ']'
    return '{' + ','.join(json.dumps(k) + ':' + lit(x) for k, x in v.items()) + '}'
lines = ['import type * as R from "../subject/output-e/apps/report/src/generated/report.js";']
lines += ['export const t%d: R.%s = %s; // %s' % (i, targets[r], lit(v), l) for i, (r, v, l) in enumerate(rows)]
bad = copy.deepcopy(ru); bad['edition'] = {'crate_a': 2023}
lines += ['// @ts-expect-error edition literal union excludes 2023n', 'export const neg0: R.Native2RustUniverseV2ResolvedInputs = %s;' % lit(bad)]
(T / 'assign.ts').write_text('\n'.join(lines) + '\n')
print(json.dumps(log, indent=1))
