"""Read-only structural survey (generation 22) of every claimed-positive artifact outside runs/.

For each JSON artifact: its top-level keys, and a count of the nested objects that carry the
markers an admission claim would rest on (`admitted`, `schema`/`selector`/`def`, `firstRefusal`,
`classification`, `refused`). Used to decide, per artifact, what its producing module actually
verified. Writes nothing.
"""
import json
import os
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
DIRS = ('vectors', 'query', 'envelopes', 'traces')
MARKERS = ('admitted', 'schema', 'selector', 'def', 'firstRefusal', 'classification', 'refused',
           'schemaDef', 'owningSchema', 'validatedAgainst', 'schemaAdmission')


def walk(node, counts, depth=0):
    if isinstance(node, dict):
        for k in node:
            for m in MARKERS:
                if k == m or (m in ('schema', 'def') and m in k.lower()):
                    counts[k] = counts.get(k, 0) + 1
        for v in node.values():
            walk(v, counts, depth + 1)
    elif isinstance(node, list):
        for v in node:
            walk(v, counts, depth + 1)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for d in DIRS:
        for n in sorted(os.listdir(os.path.join(OUT, d))):
            if not n.endswith('.json'):
                continue
            rel = d + '/' + n
            if only and only not in rel:
                continue
            try:
                doc = json.load(open(os.path.join(OUT, rel)))
            except Exception as e:
                print('%-52s UNREADABLE %s' % (rel, e))
                continue
            counts = {}
            walk(doc, counts)
            keys = list(doc.keys())[:18] if isinstance(doc, dict) else ['<list %d>' % len(doc)]
            print('%-52s keys=%s' % (rel, keys))
            print('%-52s markers=%s' % ('', dict(sorted(counts.items()))))


main()
