"""D2b plan r3 section 3's duty table against the carriers' admission list ("D2b-3's and D2b-4's lanes check this table
against the carriers' list: every id is present once, and no id is missing"), and D2b-3a's share of it: every row that
applies to TS2 and that section 3 assigns to received-frame admission (or to D2b-3's envelope step) is named where the
receiver implements it. Usage: check_d2b3a_duty_table.py <worktree> <architecture> <out json>."""
from pathlib import Path
import json, re, sys
W, A, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
plan = (A / 'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md').read_text()
section = plan[plan.index('## 3. The duty allocation'):plan.index('## 4. Checks')]
rows = []
for line in section.splitlines():
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) != 3 or cells[0] in ('Carrier row', '---'):
        continue
    ids = [i.strip().strip('`*') for i in cells[0].split(',')]
    rows.append(dict(ids=ids, appliesTo=cells[1], owner=cells[2]))
carriers = json.loads((W / 'schemas/wire/native-carriers-v1.json').read_bytes())
admission = {a['id']: a['appliesTo'] for a in carriers['admission']}
listed = [i for r in rows for i in r['ids']]
duplicates = sorted({i for i in listed if listed.count(i) > 1})
missing = sorted(set(admission) - set(listed))
extra = sorted(set(listed) - set(admission))
code = ''.join((W / p).read_text() for p in ('crates/components/src/provider_protocol/ts2.rs', 'crates/components/src/provider_protocol/ts2/carrier.rs'))
mine, elsewhere = [], []
for r in rows:
    for i in r['ids']:
        if admission.get(i) not in ('both', 'typescript-semantic'):
            continue
        # Received-frame admission, as section 3 assigns it: not H's fact admission and not a Plan-side set admission.
        receive = (('admission' in r['owner'] and not r['owner'].startswith('H:') and '(Plan side' not in r['owner'])
                   or 'D2b-3, envelope' in r['owner'] or r['owner'].startswith("each consumer of the owner schemas"))
        entry = dict(id=i, appliesTo=admission[i], owner=r['owner'], namedInReceiver=i in code)
        (mine if receive else elsewhere).append(entry)
unnamed = [e['id'] for e in mine if not e['namedInReceiver']]
out = dict(rows=len(rows), carrierIds=len(admission), listedOnce=not duplicates and not missing and not extra, duplicates=duplicates, missing=missing,
           extra=extra, receiveRows=mine, otherOwners=elsewhere, unnamedReceiveRows=unnamed)
out['passed'] = out['listedOnce'] and not unnamed
OUT.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(passed=out['passed'], rows=len(rows), carrierIds=len(admission), receiveRows=len(mine), unnamed=unnamed, missing=missing, duplicates=duplicates, extra=extra)))
sys.exit(0 if out['passed'] else 1)
