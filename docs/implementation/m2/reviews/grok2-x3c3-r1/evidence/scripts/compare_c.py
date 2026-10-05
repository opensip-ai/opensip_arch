"""X3c-3's regression comparison with C's accepted lead evidence (X9-6 at
3d2d5b5, crash-matrix-x9/evidence/3d2d5b5.../{storage,host}/runs/).

For every landed row (storage's 381 and host's 98), it compares the X3c-3
run record's normalizedSha256 and each child's trace digest with C's lead-1
record, and lists every difference by run and child. For the 19 runs of
X9 r17 §RC.5 it also reports the changed child's outcome under X3c r8 and
R3's nextWriter. timingGuard is not compared.

usage: compare_c.py <C evidence dir> <X3c-3 storage run set> <X3c-3 host run set>
"""
import json
import sys
from pathlib import Path

evidence, storage, host = map(Path, sys.argv[1:4])
RC5 = ['F12-fail-after-evidence-commit', 'F23-delete-receipt', 'F23-delete-association',
       'F27-association-store-generation', 'F27-association-namespace', 'F27-association-operation',
       'F27-association-execution', 'F28-pruned-generations', 'F33-receipt-assurance', 'F33-receipt-signer',
       'F33-association-seal-digest', 'F33-run-material-inventory', 'F40-fail-after-evidence-commit',
       'F49-reader-skewed-by-append', 'F52-association-only', 'F52-no-row-both', 'F52-purged',
       'F52-receipt-only', 'F52-settled-refused-both']
out = {}
for target, mine in (('storage', storage), ('host', host)):
    equal, differ, missing = 0, {}, []
    rc5 = {}
    for c_path in sorted((evidence / target / 'runs').glob('*.json')):
        name = c_path.stem
        m_path = mine / 'runs' / c_path.name
        if not m_path.exists():
            missing.append(name)
            continue
        c, m = json.loads(c_path.read_text()), json.loads(m_path.read_text())
        d = {}
        if c['postState']['normalizedSha256'] != m['postState']['normalizedSha256']:
            d['normalizedSha256'] = True
        cc = [(x['role'], x['ordinal'], x['trace']['sha256']) for x in c['children']]
        mc = [(x['role'], x['ordinal'], x['trace']['sha256']) for x in m['children']]
        if [x[:2] for x in cc] != [x[:2] for x in mc]:
            d['children'] = [cc, mc]
        else:
            changed = [f'{r}#{o}' for (r, o, a), (_, _, b) in zip(cc, mc) if a != b]
            if changed:
                d['childTraces'] = changed
        if c['ladder'] != m['ladder']:
            d['ladder'] = [x for x in m['ladder'] if x not in c['ladder']]
        if d:
            differ[name] = d
        else:
            equal += 1
        if name in RC5:
            outcomes = {f"{x['role']}#{x['ordinal']}": x['outcome'] for x in m['children']
                        if x['role'] in ('commit', 'competitor-writer')}
            c_out = {f"{x['role']}#{x['ordinal']}": x['outcome'] for x in c['children']
                     if x['role'] in ('commit', 'competitor-writer')}
            rc5[name] = {'C': c_out, 'X3c-3': outcomes, 'verdict': m['verdict'],
                         'R3': [x for x in m['ladder'] if x.get('step') == 'R3-sweep']}
    out[target] = {'landedCompared': equal + len(differ), 'equal': equal, 'differ': differ, 'missing': missing}
    if rc5:
        out[target]['rc5'] = rc5
print(json.dumps(out, indent=1, sort_keys=True))
