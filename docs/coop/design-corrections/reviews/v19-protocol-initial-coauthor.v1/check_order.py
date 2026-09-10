"""Bounded static check over the published table only: which row pairs can BOTH match one
(phase, frame, guard-state), i.e. where declaration order is actually load-bearing.

No host, no environment, no suite. Pure enumeration over the published rows and the three
boolean state fields any guard names.
"""
import itertools
import json
from pathlib import Path

D = json.loads(Path('protocol3-transitions.v1.json').read_text())
RULES = D['rules']
PRE = D['wildcards']['*PRE_COMPLETE']['phases']
PHASES = D['phases']

guard_keys = sorted({k for r in RULES for k in r.get('guard', {})})
print('guard keys used by the table:', guard_keys)
print('guard values used:', sorted({repr(v) for r in RULES for v in r.get('guard', {}).values()}))

def phases_of(r):
    p = r['phase']
    if p == '*ANY':
        return set()          # skipped by the matching loop
    if p == '*PRE_COMPLETE':
        return set(PRE)
    return {p}

def matches(r, phase, frame, st):
    return phase in phases_of(r) and r['frame'] == frame and \
        all(st.get(k) == v for k, v in r.get('guard', {}).items())

states = [dict(zip(guard_keys, combo)) for combo in itertools.product([True, False], repeat=len(guard_keys))]
frames = sorted({r['frame'] for r in RULES})

overlaps = []
for i, a in enumerate(RULES):
    for b in RULES[i + 1:]:
        for phase in PHASES:
            for frame in frames:
                for st in states:
                    if matches(a, phase, frame, st) and matches(b, phase, frame, st):
                        overlaps.append((a['id'], b['id'], phase, frame, dict(st)))
                        break
                else:
                    continue
                break
            else:
                continue
            break

print('\n--- row pairs that can both match one (phase, frame, state) ---')
if not overlaps:
    print('NONE')
for o in overlaps:
    print('  %s vs %s  phase=%s frame=%s state=%s' % o)

def group_report(ids):
    rows = [r for r in RULES if r['id'] in ids]
    print('\n--- group %s ---' % ','.join(ids))
    phase = rows[0]['phase']; frame = rows[0]['frame']
    for st in states:
        hits = [r['id'] for r in rows if matches(r, phase, frame, st)]
        rel = {k: st[k] for k in guard_keys if any(k in r.get('guard', {}) for r in rows)}
        print('   %-46s -> %s' % (rel, hits or ['<none>']))
    total = all(any(matches(r, phase, frame, st) for r in rows) for st in states)
    disjoint = all(sum(matches(r, phase, frame, st) for r in rows) <= 1 for st in states)
    print('   pairwise disjoint: %s   total over the boolean square: %s' % (disjoint, total))
    return disjoint, total

g1 = group_report(['P3-08', 'P3-09', 'P3-10'])
g2 = group_report(['P3-14', 'P3-15'])
print('\nBOTH GROUPS DISJOINT AND TOTAL:', g1 == (True, True) and g2 == (True, True))
