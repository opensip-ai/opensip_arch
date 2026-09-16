"""Dump selected $defs required-lists + property types so the reconstruction is built from
the schema rather than guessed. Usage: run.py peek_defs.py <file> <def> [<def>...]"""
import json
import sys

SUB = '/tmp/opensip-design-corrections/consumer-b.v20/subject'


def shape(s, depth=0, maxd=3):
    if not isinstance(s, dict):
        return s
    if '$ref' in s:
        return '$ref ' + s['$ref']
    out = {}
    for k in ('type', 'const', 'enum', 'required', 'maxItems', 'minItems',
              'additionalProperties', 'pattern', 'x-opensip-order'):
        if k in s:
            out[k] = s[k]
    if 'description' in s and depth == 0:
        out['description'] = s['description'][:500]
    for k in ('oneOf', 'anyOf', 'allOf'):
        if k in s:
            out[k] = [shape(x, depth + 1, maxd) for x in s[k]]
    if 'items' in s and depth < maxd:
        out['items'] = shape(s['items'], depth + 1, maxd)
    if 'properties' in s and depth < maxd:
        out['properties'] = {k: shape(v, depth + 1, maxd)
                             for k, v in s['properties'].items()}
    return out


def main():
    path = sys.argv[1]
    d = json.load(open(SUB + '/' + path))
    for name in sys.argv[2:]:
        node = d
        if name.startswith('x-'):
            node = d.get(name)
            print('==', name)
            print(json.dumps(node, indent=1)[:2500])
            continue
        node = d['$defs'].get(name)
        print('==', name)
        print(json.dumps(shape(node), indent=1)[:3500])


main()
