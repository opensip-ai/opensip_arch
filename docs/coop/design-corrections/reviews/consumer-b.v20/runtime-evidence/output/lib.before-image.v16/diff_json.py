"""Structural diff of one kit JSON document between the prior disclosed kit and v15.
Used only to LOCATE changes; every change is then read in full context from v15 bytes.
"""
import json
import sys

V15 = '/tmp/opensip-design-corrections/consumer-b.v15/subject/'
V14 = '/tmp/opensip-design-corrections/consumer-b.v14/subject/'


def walk(node, path='', out=None):
    out = {} if out is None else out
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + '/' + k, out)
    elif isinstance(node, list):
        out[path + '#len'] = len(node)
        for i, v in enumerate(node):
            walk(v, path + '/%d' % i, out)
    else:
        out[path] = node
    return out


rel = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 400
a = walk(json.load(open(V14 + rel)))
b = walk(json.load(open(V15 + rel)))
only_a = sorted(set(a) - set(b))
only_b = sorted(set(b) - set(a))
chg = sorted(k for k in (set(a) & set(b)) if a[k] != b[k])
print('REMOVED paths (%d)' % len(only_a))
for k in only_a[:limit]:
    print('  -', k, '=', repr(a[k])[:150])
print('ADDED paths (%d)' % len(only_b))
for k in only_b[:limit]:
    print('  +', k, '=', repr(b[k])[:200])
print('CHANGED values (%d)' % len(chg))
for k in chg[:limit]:
    print('  ~', k)
    print('      old:', repr(a[k])[:300])
    print('      new:', repr(b[k])[:300])
