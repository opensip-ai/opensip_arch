import json, sys

KIT = '/tmp/opensip-design-corrections/consumer-b.v22/subject'

def load(rel):
    return json.load(open(KIT + '/' + rel))

def main():
    rel = sys.argv[1]
    d = load(rel)
    if len(sys.argv) > 2:
        for sel in sys.argv[2:]:
            node = d
            for part in sel.split('/'):
                if part == '':
                    continue
                if isinstance(node, list):
                    node = node[int(part)]
                else:
                    node = node[part]
            print('===== ' + sel)
            print(json.dumps(node, indent=1))
    else:
        def outline(o, path='', depth=0):
            if depth > 2:
                return
            if isinstance(o, dict):
                for k, v in o.items():
                    print('  ' * depth + str(k), type(v).__name__,
                          (len(v) if isinstance(v, (list, dict)) else repr(v)[:100]))
                    if isinstance(v, (dict, list)):
                        outline(v, path + '/' + str(k), depth + 1)
            elif isinstance(o, list):
                print('  ' * depth + '[%d items]' % len(o))
                if o:
                    outline(o[0], path + '/0', depth + 1)
        outline(d)

main()
