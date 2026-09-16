"""V06 — confirm the DECLARED remaining integration work ('pin/planning refresh') is real and
scoped: are the changed files pinned, so pinned checkers would refuse until ledgers refresh?
This confirms a declared item; it is not reported as an undiscovered gap."""
import json, os

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
cf = json.load(open(os.path.join(G, 'changed-files.json')))
changed = {f['path']: f for f in cf['files']}
R = {}

LEDGERS = ['docs/coop/design-corrections/foundation/source-pins.v1.json',
           'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
           'docs/coop/design-corrections/native/source-pins.v2.json',
           'docs/coop/design-corrections/security/source-pins.v1.json',
           'docs/coop/design-corrections/workflows/source-pins.v1.json']
rows = []
for led in LEDGERS:
    p = os.path.join(SNAP, led)
    if not os.path.isfile(p):
        continue
    d = json.load(open(p))
    entries = {}

    def walk(o):
        if isinstance(o, dict):
            if 'path' in o and 'sha256' in o and isinstance(o['path'], str):
                entries[o['path']] = o['sha256']
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    for rel, f in changed.items():
        if rel in entries:
            rows.append({'ledger': led, 'pinnedPath': rel, 'pinnedSha': entries[rel],
                         'successorSha': f['sha256'],
                         'pinWouldRefuse': entries[rel] != f['sha256']})
R['pinHits'] = rows
print('--- changed files that appear in a frozen31 pin ledger ---')
for r in rows:
    print('%-52s in %-56s wouldRefuse=%s'
          % (r['pinnedPath'][-52:], os.path.basename(r['ledger']), r['pinWouldRefuse']))
R['changedFilesPinned'] = sorted({r['pinnedPath'] for r in rows})
R['pinsWouldRefuseCount'] = sum(1 for r in rows if r['pinWouldRefuse'])
R['declaredRemaining'] = json.load(open(os.path.join(G, 'integration.json')))['remaining']
print('\ndistinct changed files that are pinned : %d' % len(R['changedFilesPinned']))
print('pin entries that would refuse          : %d' % R['pinsWouldRefuseCount'])
print('declared remaining work                :', R['declaredRemaining'])
R['assessment'] = ('Confirms the author-declared "pin/planning refresh" item. Pinned checkers over '
                   'these files refuse until the ledgers are refreshed at integrated freeze. This is '
                   'a declared integration state, not an undiscovered gap, and it is why my atom '
                   'check ran in a disposable copy of the successor tree.')
json.dump(R, open(os.path.join(OUT, 'v06-pinstate.json'), 'w'), indent=1, default=str)
print('\nwrote v06-pinstate.json')
