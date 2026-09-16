import json, sys, re

KIT = '/tmp/opensip-design-corrections/consumer-b.v20/subject'


def walk(node, path=''):
    yield path, node
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + '/%d' % i)


def main():
    rel = sys.argv[1]
    pat = re.compile(sys.argv[2], re.I)
    mode = sys.argv[3] if len(sys.argv) > 3 else 'key'
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    d = json.load(open(KIT + '/' + rel))
    n = 0
    for path, node in walk(d):
        if mode == 'key':
            last = path.rsplit('/', 1)[-1]
            hit = bool(pat.search(last))
        else:
            hit = isinstance(node, str) and bool(pat.search(node))
        if hit:
            n += 1
            print('--- ' + path)
            s = json.dumps(node, indent=1) if not isinstance(node, str) else node
            print(s[:3000])
            if n >= limit:
                print('... (limit)')
                break


main()
