"""X4-F2's X9 regression rows (law X4T r12 item 13), computed the way X4-F1's
rows.py computed its own: from the two required-runs files, read only, with
a check that the harness's own prefix rule (`name.starts_with(p)` for any p
in OPENSIP_X9_ROWS) selects exactly these rows and no other.

Storage: every row whose script arms an `x4t.floor-publication` point (item
7's write-ahead, which X4-F2's clocked refusal now waits for) and every row
arming an `x3b.floor` point (the first durable points after the fenced read
returns, in `operation_handoff::begin`'s lease-free order). Host: no row arms
a point in or right after the fenced read, so the host set runs its census
alone, under a prefix that matches no row.

Usage: python3 x9-rows.py [product checkout]  (prints JSON; writes nothing)
"""
import json
import sys

P = sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip'
NONE = 'X4F2-NO-ROW'


def name(r):
    return f"{r['case']}-{r['variant']}"


def storage_rows(runs):
    out = {}
    for r in runs:
        s = json.dumps(r['script'])
        if 'x4t.floor-publication' in s:
            out[name(r)] = 'floor-publication-kill'
        elif 'x3b.floor' in s:
            out[name(r)] = 'after-fenced-read'
    return out


def host_rows(runs):
    return {}


def main():
    result = {'product': P}
    for target, path, pick in (
        ('storage', 'crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json', storage_rows),
        ('host', 'crates/host/tests/fixtures/crash-matrix/required-runs.v1.json', host_rows),
    ):
        data = json.load(open(f'{P}/{path}'))
        runs = data['runs']
        rows = pick(runs)
        prefixes = sorted(rows) or [NONE]
        selected = {name(r) for r in runs if any(name(r).startswith(p) for p in prefixes)}
        assert selected == set(rows), (target, sorted(selected ^ set(rows)))
        kinds, cases = {}, {}
        for r in runs:
            if name(r) in rows:
                kinds[rows[name(r)]] = kinds.get(rows[name(r)], 0) + 1
                cases[r['case']] = cases.get(r['case'], 0) + 1
        result[target] = {
            'requiredRuns': len(runs),
            'clockEpoch': data['clockEpoch'],
            'rows': len(rows),
            'kinds': kinds,
            'cases': cases,
            'OPENSIP_X9_ROWS': ','.join(prefixes),
        }
    json.dump(result, sys.stdout, indent=1)
    print()


main()
