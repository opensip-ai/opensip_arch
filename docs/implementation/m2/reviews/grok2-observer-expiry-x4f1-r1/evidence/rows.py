"""X4-F1's X9 regression rows: compute them from the required-runs files,
write the OPENSIP_X9_ROWS value for each target, and check that the
harness's own prefix rule (`name.starts_with(p)` for any p) selects exactly
these rows and no other."""
import json
import sys

W = '/Users/sb/code/opensip-ai/opensip-x4f1'
S = '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1'
X94 = ('F06', 'F18', 'F19', 'F26', 'F30', 'F34', 'F38', 'F39', 'F40', 'F41')


def name(r):
    return f"{r['case']}-{r['variant']}"


def in_x94(r):
    return r['unit'] == 'X9-4' if 'unit' in r else r['case'] in X94


def storage_rows(runs):
    out = {}
    for r in runs:
        s = json.dumps(r['script'])
        if 'x4.observer.tick' in s:
            out[name(r)] = 'tick-armed'
        elif in_x94(r):
            out[name(r)] = 'x9-4-other'
        elif 'x4.' in s:
            out[name(r)] = 'checkpoint-kill'
    return out


def host_rows(runs):
    return {name(r): ('tick-armed' if 'x4.observer.tick' in json.dumps(r['script']) else 'f40')
            for r in runs if r['case'] in ('F39', 'F40')}


def main():
    result = {}
    for target, path, pick in (
        ('storage', 'crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json', storage_rows),
        ('host', 'crates/host/tests/fixtures/crash-matrix/required-runs.v1.json', host_rows),
    ):
        runs = json.load(open(f'{W}/{path}'))['runs']
        rows = pick(runs)
        prefixes = sorted(rows)
        selected = {name(r) for r in runs if any(name(r).startswith(p) for p in prefixes)}
        assert selected == set(rows), (target, sorted(selected ^ set(rows)))
        open(f'{S}/rows-{target}.txt', 'w').write(','.join(prefixes))
        counts = {}
        for kind in rows.values():
            counts[kind] = counts.get(kind, 0) + 1
        result[target] = {'rows': len(rows), 'kinds': counts}
    json.dump(result, sys.stdout, indent=1)
    print()


main()
