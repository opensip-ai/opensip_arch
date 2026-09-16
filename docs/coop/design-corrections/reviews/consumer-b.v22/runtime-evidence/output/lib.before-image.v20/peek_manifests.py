import base64
import json
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
lab = sys.argv[1] if len(sys.argv) > 1 else 'rust-partial'
d = json.load(open(OUT + '/runs/%s.store.json' % lab))
for t, r in d['objectTable'].items():
    if not t.startswith('snapshot2:'):
        continue
    si = r['record']['sourceInventory']
    print('paths:', [x['path'] for x in si])
    for x in si:
        base = x['path'].split('/')[-1]
        if base in ('Cargo.toml', 'package.json'):
            by = base64.b64decode(d['blobs'][x['sha256']]).decode()
            print('==', x['path'])
            print(by[:260])
    break
