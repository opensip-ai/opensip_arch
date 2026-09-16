"""Reading aid only: compact line-per-property summaries of kit JSON schema documents.

Writes to output/notes/schemas/. Not part of admission; reads kit bytes read-only.
"""
import json
import os
import sys

ROOT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/subject/docs/'
OUT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/output/notes/schemas/'

KEYS = ('type', 'const', 'enum', 'pattern', '$ref', 'minItems', 'maxItems', 'minimum', 'maximum',
        'minLength', 'maxLength', 'uniqueItems', 'x-opensip-order', 'x-opensip-digest', 'oneOf',
        'anyOf', 'allOf', 'items', 'additionalProperties', 'required', 'properties', 'not')


def short(v, n=400):
    s = json.dumps(v, ensure_ascii=False, sort_keys=True)
    return s if len(s) <= n else s[:n - 3] + '...'


def prop_line(name, p, indent='  '):
    if not isinstance(p, dict):
        return f"{indent}{name}: {short(p)}"
    parts = []
    for k in KEYS:
        if k in p:
            v = p[k]
            if k == 'properties':
                v = sorted(v.keys())
            parts.append(f"{k}={short(v)}")
    for k in p:
        if k.startswith('x-opensip') and k not in ('x-opensip-order', 'x-opensip-digest'):
            parts.append(f"{k}={short(p[k])}")
    lines = [f"{indent}{name}: " + ' | '.join(parts)]
    if isinstance(p.get('properties'), dict) and len(indent) < 8:
        for pn, pp in p['properties'].items():
            lines.append(prop_line(pn, pp, indent + '    '))
    return '\n'.join(lines)


def dump(rel):
    d = json.load(open(ROOT + rel))
    lines = [f"# {rel}", "top-level keys: " + ', '.join(d.keys())]
    for k, v in d.items():
        if k in ('$defs', 'definitions'):
            continue
        if isinstance(v, dict):
            lines.append(f"## {k}: keys={short(list(v.keys()), 600)}")
        else:
            lines.append(f"## {k}: {short(v, 600)}")
    defs = d.get('$defs', d.get('definitions', {}))
    for name, s in defs.items():
        if not isinstance(s, dict):
            lines.append(f"### {name}: {short(s)}")
            continue
        hdr = [f"### {name}"]
        for k in ('type', 'required', 'additionalProperties', 'oneOf', 'anyOf', 'allOf', 'enum', 'const',
                  'pattern', '$ref', 'x-opensip-order', 'items', 'minItems', 'maxItems', 'uniqueItems', 'description'):
            if k in s:
                v = s[k]
                if k == 'description':
                    v = v[:500]
                hdr.append(f"{k}={short(v, 600)}")
        for k in s:
            if k.startswith('x-opensip') and k != 'x-opensip-order':
                hdr.append(f"{k}={short(s[k], 600)}")
        lines.append(' | '.join(hdr))
        for pn, p in s.get('properties', {}).items():
            lines.append(prop_line(pn, p))
    return '\n'.join(lines) + '\n'


def main(files):
    os.makedirs(OUT, exist_ok=True)
    for f in files:
        txt = dump(f)
        fn = OUT + f.replace('/', '__') + '.txt'
        with open(fn, 'w') as fh:
            fh.write(txt)
        print(len(txt.splitlines()), len(txt), os.path.basename(fn))


if __name__ == '__main__':
    main(sys.argv[1:])
