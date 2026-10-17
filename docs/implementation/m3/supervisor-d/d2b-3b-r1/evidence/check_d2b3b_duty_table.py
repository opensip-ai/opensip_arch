"""D2b plan r3 section 3's duty table against the carriers' admission list ("D2b-3's and D2b-4's lanes check this table
against the carriers' list: every id is present once, and no id is missing"), and D2b-3b's share of it: every row that
applies to TS2 and that section 3 assigns to D2b's builder (the host payload builders and the schedule constructor) or
to its sender is named where the send side implements it. Usage: check_d2b3b_duty_table.py <worktree> <architecture>
<out json>. (Adapted from D2b-3a's check_d2b3a_duty_table.py.)"""
from pathlib import Path
import json, sys
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
code = ''.join((W / p).read_text() for p in ('crates/components/src/provider_protocol/ts2/send.rs', 'crates/components/src/provider_protocol/ts2/participant.rs'))
mine, elsewhere = [], []
for r in rows:
    for i in r['ids']:
        if admission.get(i) not in ('both', 'typescript-semantic'):
            continue
        # The send side, as section 3 assigns it: the builder (never "not D2b") or the sender.
        send = (r['owner'].startswith('builder') or '; builder' in r['owner'] or 'builder places' in r['owner']
                or r['owner'] == 'sender' or "sender (" in r['owner'] or r['owner'].startswith('D2b-3 and D2b-4\'s sender'))
        entry = dict(id=i, appliesTo=admission[i], owner=r['owner'], namedInSender=i in code)
        (mine if send else elsewhere).append(entry)
unnamed = [e['id'] for e in mine if not e['namedInSender']]
out = dict(rows=len(rows), carrierIds=len(admission), listedOnce=not duplicates and not missing and not extra, duplicates=duplicates, missing=missing,
           extra=extra, sendRows=mine, otherOwners=elsewhere, unnamedSendRows=unnamed)
out['passed'] = out['listedOnce'] and not unnamed and len(mine) > 0
OUT.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(passed=out['passed'], rows=len(rows), carrierIds=len(admission), sendRows=[e['id'] for e in mine], unnamed=unnamed, missing=missing, duplicates=duplicates, extra=extra)))
sys.exit(0 if out['passed'] else 1)
