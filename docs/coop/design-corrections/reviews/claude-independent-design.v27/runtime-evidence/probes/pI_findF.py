import json, os, re

d = '/tmp/opensip-design-corrections/claude-author-package-review.v1'
r = json.load(open(os.path.join(d, 'result.json')))
print('result.json top keys:', list(r)[:30])


def walk(o, path=''):
    found = []
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                ids = [str(x.get('id', '')) for x in v]
                if any(re.fullmatch(r'F-?\d\d', i) for i in ids):
                    found.append((path + '/' + k, len(v), sorted(v[0]), ids))
            found += walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            found += walk(v, path + '/%d' % i)
    return found


hits = walk(r)
for p, n, keys, ids in hits:
    print('LIST at %s  len=%d  keys=%s' % (p, n, keys))
    print('   ids:', ids)
s = json.dumps(r)
print('\nF-tokens found in result.json:', sorted(set(re.findall(r'\bF\d\d\b', s))))
md = open(os.path.join(d, 'review.md'), encoding='utf-8').read()
print('F-tokens in review.md      :', sorted(set(re.findall(r'\bF\d\d\b', md))))
for m in re.finditer(r'^#+ *(F\d\d)[^\n]*', md, re.M):
    print('  heading:', m.group(0)[:150])
