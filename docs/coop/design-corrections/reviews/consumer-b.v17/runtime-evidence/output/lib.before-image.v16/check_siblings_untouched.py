"""Independent control: THIS generation must not have modified consumer-b.v14 or v15.

It only STATS the sibling trees -- no file is opened, no byte is read -- and reports the
newest modification time found there against the newest under this generation's own output.
A sibling newer than this session's start would be a violation.
"""
import json
import os
import time

BASE = '/tmp/opensip-design-corrections'
OUT = BASE + '/consumer-b.v16/output'


def newest(root):
    best, path, n = 0.0, None, 0
    for d, _dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            try:
                m = os.stat(p).st_mtime
            except OSError:
                continue
            n += 1
            if m > best:
                best, path = m, p
    return best, path, n


rows = {}
for gen in ('consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16'):
    root = os.path.join(BASE, gen)
    if not os.path.isdir(root):
        rows[gen] = {'present': False}
        continue
    m, p, n = newest(root)
    rows[gen] = {'present': True, 'fileCount': n,
                 'newestMtimeUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(m)),
                 'newestPath': p.replace(BASE + '/', '')}

v16 = rows['consumer-b.v16']['newestMtimeUtc']
viol = [g for g in ('consumer-b.v14', 'consumer-b.v15')
        if rows[g].get('present') and rows[g]['newestMtimeUtc'] >= v16]
doc = {'standing': __doc__, 'generations': rows,
       'siblingsNewerThanOrEqualToThisGeneration': viol,
       'result': 'PASS' if not viol else 'FAIL'}
with open(OUT + '/notes/siblings-untouched.json', 'w') as f:
    json.dump(doc, f, indent=1)
for g, r in rows.items():
    print('%-16s files=%-5s newest=%s  %s'
          % (g, r.get('fileCount'), r.get('newestMtimeUtc'), r.get('newestPath', '')[:60]))
print('result:', doc['result'])
assert not viol, viol
