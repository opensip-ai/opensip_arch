"""Reading aid: extract JSON-pointer selectors from kit documents into output/notes/extract/.

usage: python3 extract.py OUTNAME kitpath#/pointer [kitpath#/pointer ...]
"""
import json
import os
import sys

ROOT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/subject/docs/'
OUT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/preserved/pre-s42/notes/extract/'


def resolve(doc, pointer):
    cur = doc
    if pointer in ('', '/'):
        return cur
    for tok in pointer.lstrip('/').split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, list):
            cur = cur[int(tok)]
        else:
            cur = cur[tok]
    return cur


def main():
    name = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    chunks = []
    for sel in sys.argv[2:]:
        path, _, ptr = sel.partition('#')
        doc = json.load(open(ROOT + path))
        val = resolve(doc, ptr)
        chunks.append(f"=== {sel}\n" + json.dumps(val, indent=1, ensure_ascii=False))
    txt = '\n'.join(chunks) + '\n'
    with open(OUT + name, 'w') as fh:
        fh.write(txt)
    print(name, len(txt.splitlines()), len(txt))


if __name__ == '__main__':
    main()
