"""Review02 adversarial positive corpus: single-point mutations of the 1343 witnesses,
kept only when metadata-v2 check_metadata (original schemas, exact codec) accepts them.
Writes Rust carrier cases, TS concrete-assignment files and raw texts for the TS runtime."""
import collections
import copy
import json
import sys
import time
from pathlib import Path

W = Path('/tmp/opensip-implementation/m1-eight-output-review-02/work')
sys.path.insert(0, str(W / 'subject/witness-provenance'))
import witness_common as wc  # noqa: E402  (load/check only; OUT is never written)

reference, registry, _ = wc.load()
corpus = json.loads((W / 'subject/witness-provenance/witnesses.json').read_bytes(), parse_float=wc.no_float)
targets = json.loads((W / 'subject/targets.json').read_bytes())
provider = set(json.loads((W / 'subject/ts-exports.json').read_bytes())['provider'])

INT_VALUES = [2**64 - 1, -(2**63), 2**63, 2**63 - 1, -1, 0]
EXTRA_VALUES = [None, 0, 'x', True, {}, [], 2**64 - 1, -(2**63)]
CLASS_CAP = {'integer-boundary': 10, 'member-absence-or-null': 6, 'extra-member': 4, 'array-shape': 4, 'scalar-change': 4}
TRY_CAP = 70


def walk(value, path=()):
    yield path, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, path + (index,))


def put(root, path, new):
    if not path:
        return copy.deepcopy(new)
    root = copy.deepcopy(root)
    node = root
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = copy.deepcopy(new)
    return root


def remove(root, path):
    root = copy.deepcopy(root)
    node = root
    for key in path[:-1]:
        node = node[key]
    del node[path[-1]]
    return root


def mutations(value):
    out = collections.defaultdict(list)
    for path, node in walk(value):
        if type(node) is int:
            out['integer-boundary'] += [put(value, path, v) for v in INT_VALUES if v != node]
        elif isinstance(node, dict):
            for key in node:
                out['member-absence-or-null'].append(remove(value, path + (key,)))
                if node[key] is not None:
                    out['member-absence-or-null'].append(put(value, path + (key,), None))
            for key in ('zz', 'x-extra', ''):
                if key not in node:
                    out['extra-member'] += [put(value, path + (key,), v) for v in EXTRA_VALUES]
        elif isinstance(node, list):
            if node:
                out['array-shape'] += [put(value, path, []), put(value, path, node + node[:1]),
                                       put(value, path, node[::-1]), put(value, path, node[:-1])]
        elif type(node) is str:
            out['scalar-change'] += [put(value, path, s) for s in ('', 'A', 'é \U0001F600', 'a' * 65) if s != node]
        elif type(node) is bool:
            out['scalar-change'].append(put(value, path, not node))
        elif node is None:
            out['scalar-change'] += [put(value, path, v) for v in (0, 'x', {}, [])]
    return out


def lit(v):
    if v is None:
        return 'null'
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if type(v) is int:
        return '%dn' % v
    if type(v) is str:
        return json.dumps(v)
    if type(v) is list:
        return '[' + ','.join(lit(x) for x in v) + ']'
    if type(v) is dict:
        return '{' + ','.join(('[%s]' % json.dumps(k) if k == '__proto__' else json.dumps(k)) + ':' + lit(x) for k, x in v.items()) + '}'
    raise TypeError(type(v))


def main():
    start = time.time()
    by_ref = collections.defaultdict(list)
    for case in corpus['cases']:
        by_ref[case['ref']].append(case['value'])
    witnesses = [(c['ref'], c['value'], 'witness') for c in corpus['cases']]
    mutants, stats = [], {}
    for ref, values in by_ref.items():
        seen = {bytes(reference.canonical(v)) for v in values}
        per_class = collections.Counter()
        tries = collections.Counter()
        candidates = [mutations(v) for v in values]
        for klass, cap in CLASS_CAP.items():
            for cand in (m for c in candidates for m in c[klass]):
                if per_class[klass] >= cap or tries[klass] >= TRY_CAP:
                    break
                try:
                    key = bytes(reference.canonical(cand))
                except Exception:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                tries[klass] += 1
                if wc.check(reference, registry, ref, cand) is None:
                    per_class[klass] += 1
                    mutants.append((ref, cand, klass))
        stats[ref] = {'valid': dict(per_class), 'tries': dict(tries)}
    wide = sorted({ref for ref, v, k in mutants if k == 'integer-boundary' and any(type(x) is int and x > 2**63 - 1 for _, x in walk(v))})
    neg = sorted({ref for ref, v, k in mutants if k == 'integer-boundary' and any(type(x) is int and x == -(2**63) for _, x in walk(v))})
    mixed = sorted(set(wide) & set(neg))

    def write_set(label, rows):
        d = W / ('rust-' + label)
        d.mkdir(exist_ok=True)
        (d / 'carrier-cases.json').write_text(json.dumps({'rows': [[r, i] for i, (r, _, _) in enumerate(rows)],
                                                           'values': [v for _, v, _ in rows]}) + '\n')
        (W / ('raw-' + label + '.json')).write_text(json.dumps([{'ref': r, 'kind': k, 'raw': json.dumps(v)} for r, v, k in rows]) + '\n')
        ts = W / 'ts-assign'
        ts.mkdir(exist_ok=True)
        files = []
        chunk = 1500
        for part in range(0, len(rows), chunk):
            name = '%s-report-%03d.ts' % (label, part // chunk)
            lines = ['import type * as R from "../subject/output-e/apps/report/src/generated/report.js";']
            lines += ['export const c%d: R.%s = %s;' % (i, targets[r], lit(v)) for i, (r, v, _) in enumerate(rows[part:part + chunk], part)]
            (ts / name).write_text('\n'.join(lines) + '\n')
            files.append(name)
        prows = [(i, r, v) for i, (r, v, _) in enumerate(rows) if targets[r] in provider]
        name = '%s-provider.ts' % label
        lines = ['import type * as P from "../subject/output-e/providers/typescript/src/generated/protocol.js";']
        lines += ['export const p%d: P.%s = %s;' % (i, targets[r], lit(v)) for i, r, v in prows]
        (ts / name).write_text('\n'.join(lines) + '\n')
        files.append(name)
        return files, len(prows)

    wfiles, wprov = write_set('witnesses', witnesses)
    mfiles, mprov = write_set('mutants', mutants)
    summary = {'witnesses': len(witnesses), 'witnessProviderAssignments': wprov, 'mutants': len(mutants),
               'mutantProviderAssignments': mprov, 'mutantsByClass': dict(collections.Counter(k for _, _, k in mutants)),
               'refsWithMutants': len({r for r, _, _ in mutants}),
               'refsWithValidIntegerAboveI64Max': wide, 'refsWithValidI64Min': len(neg), 'refsWithMixedSignedRange': mixed,
               'tsFiles': wfiles + mfiles, 'seconds': round(time.time() - start, 1), 'perRef': stats}
    (W / 'mutation-summary.json').write_text(json.dumps(summary, indent=1) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'perRef'}, indent=1))


main()
