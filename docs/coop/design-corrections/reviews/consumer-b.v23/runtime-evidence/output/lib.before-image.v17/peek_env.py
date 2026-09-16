import json

SUB = '/tmp/opensip-design-corrections/consumer-b.v17/subject'
P = SUB + '/docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json'
d = json.load(open(P))


def shape(s, depth=0, maxd=2):
    if not isinstance(s, dict):
        return s
    if '$ref' in s:
        return '$ref ' + s['$ref']
    out = {}
    for k in ('type', 'const', 'enum', 'required', 'additionalProperties'):
        if k in s:
            out[k] = s[k]
    for k in ('oneOf', 'anyOf', 'allOf'):
        if k in s:
            out[k] = [shape(x, depth + 1, maxd) for x in s[k]]
    if 'properties' in s and depth < maxd:
        out['properties'] = {k: shape(v, depth + 1, maxd)
                             for k, v in s['properties'].items()}
    if 'items' in s and depth < maxd:
        out['items'] = shape(s['items'], depth + 1, maxd)
    return out


print(json.dumps(shape(d), indent=1)[:6000])
