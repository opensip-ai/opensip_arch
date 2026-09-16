import json, sys
def sk(o, d=0, maxd=3):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str):
                s = v if len(v) < 220 else v[:220] + '...(%d)' % len(v)
                print('  ' * d + k + ': ' + s)
            elif isinstance(v, (int, float, bool)) or v is None:
                print('  ' * d + k + ': ' + json.dumps(v))
            elif isinstance(v, dict):
                print('  ' * d + k + ' {%d}' % len(v))
                if d < maxd: sk(v, d + 1, maxd)
            else:
                print('  ' * d + k + ' [%d]' % len(v))
                if v and d < maxd:
                    if isinstance(v[0], dict):
                        print('  ' * (d + 1) + '[0]:')
                        sk(v[0], d + 2, maxd)
                    else:
                        print('  ' * (d + 1) + json.dumps(v[:6])[:300])
for p in sys.argv[2:]:
    print('=====', p)
    sk(json.load(open(p)), 0, int(sys.argv[1]))
