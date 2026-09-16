"""Read-only compact tree dump of JSON artifacts (generation 22 audit aid). Writes nothing.

    peek22_dump.py DEPTH path [path ...]      (paths relative to output/)

Dicts show their keys, lists their length and a summary of the first item, scalars a short repr.
"""
import json
import os
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def show(node, depth, maxdepth, indent, key=''):
    pad = '  ' * indent
    if isinstance(node, dict):
        print('%s%s{%d keys}' % (pad, key, len(node)))
        if depth < maxdepth:
            for k, v in list(node.items())[:40]:
                show(v, depth + 1, maxdepth, indent + 1, k + ': ')
    elif isinstance(node, list):
        print('%s%s[%d]' % (pad, key, len(node)))
        if node and depth < maxdepth:
            show(node[0], depth + 1, maxdepth, indent + 1, '[0]: ')
    else:
        r = repr(node)
        print('%s%s%s' % (pad, key, r[:150] + ('...' if len(r) > 150 else '')))


def main():
    maxdepth = int(sys.argv[1])
    for rel in sys.argv[2:]:
        print('=' * 30, rel)
        show(json.load(open(os.path.join(OUT, rel))), 0, maxdepth, 0)


main()
