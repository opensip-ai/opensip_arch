"""P15 — corrects p01/build1: root-delta31-to32.json is in MY OWN runtime directory. p01 searched
the reviews tree and a /tmp path but not the runtime, and I reported it as not locatable. Comparing
my independently derived delta against it now. It remains an inventory, not approval."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
REC = os.path.join(BASE, 'receipts')
RD = os.path.join(BASE, 'root-delta31-to32.json')
mine = json.load(open(os.path.join(REC, 'p01-delta.json')))
d = json.load(open(RD))
R = {'corrects': 'p01 reported root-delta31-to32.json as not locatable; it is in my runtime root',
     'rootDeltaTopKeys': sorted(d) if isinstance(d, dict) else '<list>'}
print('root delta top keys:', R['rootDeltaTopKeys'])

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
myset = {a['path'] for a in mine['added']} | {c['path'] for c in mine['changed']}
R['rootDeclaredCount'] = len(paths)
R['myTouchedCount'] = len(myset)
R['inMineNotRoot'] = sorted(myset - paths)
R['inRootNotMine'] = sorted(paths - myset)
R['agrees'] = not (myset - paths) and not (paths - myset)
print('root paths=%d  mine=%d  agree=%s' % (len(paths), len(myset), R['agrees']))
print('in mine not root:', R['inMineNotRoot'])
print('in root not mine:', R['inRootNotMine'])
for k in ('added', 'changed', 'removed'):
    if isinstance(d, dict) and k in d:
        v = d[k]
        R['rootCount_' + k] = len(v) if isinstance(v, (list, dict)) else v
print('root per-kind counts:', {k: v for k, v in R.items() if k.startswith('rootCount_')})
R['myCounts'] = {'added': mine['addedCount'], 'removed': mine['removedCount'],
                 'changed': mine['changedCount']}
print('my counts          :', R['myCounts'])
R['standing'] = ('Root\'s listing is an inventory and is not approval. My delta was derived '
                 'independently from the two frozen manifests before I saw it.')
json.dump(R, open(os.path.join(REC, 'p15-rootdelta.json'), 'w'), indent=1, default=str)
print('\nwrote p15-rootdelta.json')
