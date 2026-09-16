"""Targeted ExactInteger site cases, kept only when metadata-v2 original-schema check accepts them."""
import copy, json, sys
from pathlib import Path
W = Path('/tmp/opensip-implementation/m1-eight-output-review-02/work')
sys.path.insert(0, str(W / 'subject/witness-provenance'))
import witness_common as wc
reference, registry, _ = wc.load()
corpus = json.loads((W / 'subject/witness-provenance/witnesses.json').read_bytes(), parse_float=wc.no_float)
targets = json.loads((W / 'subject/targets.json').read_bytes())
BOUNDS = [-(2**63), -(2**63) + 1, -1, 0, 2**63 - 1, 2**63, 2**64 - 1]
OUT_OF_RANGE = [-(2**63) - 1, 2**64]
rows, report = [], []
def find_paths(value, want, path=()):
    if isinstance(value, dict):
        for k, v in value.items():
            if want(path + (k,), v): yield path + (k,)
            yield from find_paths(v, want, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value): yield from find_paths(v, want, path + (i,))
def put(root, path, new):
    root = copy.deepcopy(root); node = root
    for k in path[:-1]: node = node[k]
    node[path[-1]] = new; return root
def emit(ref, value, label, expect_valid=True):
    err = wc.check(reference, registry, ref, value)
    report.append({'label': label, 'ref': ref, 'pythonValid': err is None, 'error': None if err is None else err[:200]})
    if err is None: rows.append((ref, value, label))
# 1. FindingParameters: parameters map of mixed ints.
fp = 'urn:opensip:product-v1:identity:v3#/$defs/finding-parameters'
base = next(c['value'] for c in corpus['cases'] if c['ref'] == fp)
for b in BOUNDS + OUT_OF_RANGE:
    emit(fp, dict(base, parameters={'a': b}), 'finding-parameters=%d' % b)
emit(fp, dict(base, parameters={'a': -(2**63), 'b': 2**64 - 1, 'c': 'x', 'd': True}), 'finding-parameters-mixed-map')
# 2. Every ref whose witnesses contain Sarif message.properties or edition-like mixed sites: brute force over witnesses,
#    placing boundaries at any object member whose original value is int and whose key path ends in properties/*, edition*.
for case in corpus['cases']:
    ref, value = case['ref'], case['value']
    paths = list(find_paths(value, lambda p, v: len(p) >= 2 and (p[-2] == 'properties' or 'dition' in str(p[-1]) or 'dition' in str(p[-2]))))
    if 'sarif' in ref or 'Edition' in ref or 'edition' in json.dumps(value):
        for p in paths[:6]:
            for b in (-(2**63), 2**63, 2**64 - 1):
                emit(ref, put(value, p, b), 'site %s %s=%d' % (targets[ref], '/'.join(map(str, p)), b))
    # add a properties map where an object has an empty/str-valued `properties` member (Sarif message.properties)
    for p in find_paths(value, lambda p, v: p[-1] == 'properties' and isinstance(v, dict)):
        for b in (-(2**63), 2**64 - 1):
            emit(ref, put(value, p, {'k': b, 's': 'x', 't': False}), 'properties-map %s %s=%d' % (targets[ref], '/'.join(map(str, p)), b))
seen, uniq = set(), []
for r in rows:
    key = (r[0], json.dumps(r[1], sort_keys=True))
    if key not in seen: seen.add(key); uniq.append(r)
(W / 'targeted/rust/carrier-cases.json').write_text(json.dumps({'rows': [[r, i] for i, (r, _, _) in enumerate(uniq)], 'values': [v for _, v, _ in uniq]}))
(W / 'targeted/raw.json').write_text(json.dumps([{'ref': r, 'kind': l, 'raw': json.dumps(v)} for r, v, l in uniq]))
sys.path.insert(0, str(W)); 
lit = None
exec(open(W / 'mutate.py').read().split('def main():')[0].split('reference, registry, _ = wc.load()')[1].split('def lit(v):')[0] and '', {})
def tslit(v):
    if v is None: return 'null'
    if v is True: return 'true'
    if v is False: return 'false'
    if type(v) is int: return '%dn' % v
    if type(v) is str: return json.dumps(v)
    if type(v) is list: return '[' + ','.join(tslit(x) for x in v) + ']'
    return '{' + ','.join(json.dumps(k) + ':' + tslit(x) for k, x in v.items()) + '}'
lines = ['import type * as R from "../subject/output-e/apps/report/src/generated/report.js";']
lines += ['export const t%d: R.%s = %s;' % (i, targets[r], tslit(v)) for i, (r, v, _) in enumerate(uniq)]
(W / 'targeted/assign.ts').write_text('\n'.join(lines) + '\n')
(W / 'targeted/report.json').write_text(json.dumps(report, indent=1))
print(json.dumps({'attempts': len(report), 'pythonValid': len(uniq), 'labelsValid': sorted({l.split(' ')[0] for _, _, l in uniq}),
  'refsValid': sorted({targets[r] for r, _, _ in uniq}), 'outOfRangeRejected': [x['label'] for x in report if not x['pythonValid'] and 'finding' in x['label']],
  'maxAboveI64': sum(1 for _, v, _ in uniq if '18446744073709551615' in json.dumps(v)), 'minI64': sum(1 for _, v, _ in uniq if '-9223372036854775808' in json.dumps(v))}, indent=1))
