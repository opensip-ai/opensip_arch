"""P01 — derive the 31->32 delta myself, then compare with root's inventory (inventory, not approval)."""
import hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'


def load(v):
    return {f['path']: f for f in json.load(open(os.path.join(REV, 'candidate-subject.%s.json' % v)))['files']}


a, b = load('v31'), load('v32')
added = sorted(set(b) - set(a))
removed = sorted(set(a) - set(b))
changed = sorted(p for p in set(a) & set(b) if a[p]['sha256'] != b[p]['sha256'])
R = {'fileCount31': len(a), 'fileCount32': len(b),
     'added': [{'path': p, 'bytes': b[p]['bytes'], 'sha256': b[p]['sha256']} for p in added],
     'removed': removed,
     'changed': [{'path': p, 'bytes31': a[p]['bytes'], 'bytes32': b[p]['bytes'],
                  'sha31': a[p]['sha256'], 'sha32': b[p]['sha256'],
                  'sameByteCount': a[p]['bytes'] == b[p]['bytes']} for p in changed],
     'addedCount': len(added), 'removedCount': len(removed), 'changedCount': len(changed),
     'touched': len(added) + len(changed),
     'netBytes': sum(f['bytes'] for f in b.values()) - sum(f['bytes'] for f in a.values())}
print('=== 31 -> 32 : +%d added, -%d removed, ~%d changed (%d touched), net %+d bytes ==='
      % (len(added), len(removed), len(changed), len(added) + len(changed), R['netBytes']))
print('\n--- ADDED ---')
for p in added:
    print('   %-86s %8d' % (p, b[p]['bytes']))
print('\n--- REMOVED ---')
for p in removed:
    print('   %s' % p)
print('\n--- CHANGED ---')
for p in changed:
    tag = 'SAME-BYTES' if a[p]['bytes'] == b[p]['bytes'] else '%d->%d' % (a[p]['bytes'], b[p]['bytes'])
    print('   %-86s %s' % (p, tag))

# root's inventory
cands = [os.path.join(REV, 'root-delta31-to32.json'),
         '/tmp/opensip-design-corrections/root-delta31-to32.json']
rd = next((c for c in cands if os.path.isfile(c)), None)
R['rootDeltaPath'] = rd
if rd:
    d = json.load(open(rd))
    paths = set()

    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('path', 'file') and isinstance(v, str):
                    paths.add(v)
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
        elif isinstance(o, str) and o.startswith('docs/'):
            paths.add(o)
    collect(d)
    mine = set(added) | set(changed)
    R['rootDeclaredCount'] = len(paths)
    R['inMineNotRoot'] = sorted(mine - paths)
    R['inRootNotMine'] = sorted(paths - mine)
    R['agreesWithRootInventory'] = not (mine - paths) and not (paths - mine)
    R['rootTopKeys'] = sorted(d) if isinstance(d, dict) else '<list>'
    print('\nroot inventory paths: %d | mine: %d | agree: %s'
          % (len(paths), len(mine), R['agreesWithRootInventory']))
    print('in mine not root:', R['inMineNotRoot'])
    print('in root not mine:', R['inRootNotMine'])
else:
    print('\nroot-delta31-to32.json NOT FOUND in the searched locations')
json.dump(R, open(os.path.join(OUT, 'p01-delta.json'), 'w'), indent=1)
print('\nwrote p01-delta.json')
