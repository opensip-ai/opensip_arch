"""R01 — exact 34->35 diffs of all ten changed files (read-only on both frozen snapshots), section and
top-level changes, JSON-path changes in the schema owner, layer4 exposure, and baseline hash checks."""
import ast, difflib, hashlib, json, os, re

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
DIFFS = os.path.join(OUT, 'diffs')
os.makedirs(DIFFS, exist_ok=True)
r00 = json.load(open(os.path.join(OUT, 'r00-custody.json')))
R = {'files': {}}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


B34 = '/tmp/opensip-design-corrections/claude-independent-design.v34'
R['baseline'] = {'reviewJson': sha(B34 + '/review.json'), 'reviewMd': sha(B34 + '/review.md')}
R['baselineMatches'] = (R['baseline']['reviewJson'] == 'c31f1c4779b8fa60385520009c73139d46572b29a7f22f251c5a0182a2a42bb3'
                        and R['baseline']['reviewMd'] == '72e4e1b04a0d3b905fbbf72b451fbfe7f0e4284c864c9517865ab27eff78c7fd')
print('baseline v34 review.json/md hashes match:', R['baselineMatches'])

for c in r00['delta']['changed']:
    p = c['path']
    a, b = os.path.join(S34, p), os.path.join(S35, p)
    assert sha(a) == c['sha34'] and sha(b) == c['sha35'], p
    A = open(a, encoding='utf-8').read().splitlines()
    B = open(b, encoding='utf-8').read().splitlines()
    d = list(difflib.unified_diff(A, B, 'v34/' + p, 'v35/' + p, lineterm='', n=3))
    plus = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    fn = os.path.join(DIFFS, p.replace('/', '__') + '.diff')
    open(fn, 'w', encoding='utf-8').write('\n'.join(d) + '\n')
    R['files'][p] = {'lines34': len(A), 'lines35': len(B), 'plus': plus, 'minus': minus, 'diffFile': fn}
    print('%-80s lines %5d->%5d  +%-4d -%-4d' % (p, len(A), len(B), plus, minus))
    if p.endswith('.json') and 'schema' not in p and plus + minus <= 20:
        for l in d:
            if l.startswith(('+', '-')) and not l.startswith(('+++', '---')):
                print('      %s' % l.strip()[:170])


def sections(path):
    out, cur, buf = {}, '(preamble)', []
    for line in open(path, encoding='utf-8'):
        if re.match(r'^#{1,4} ', line):
            out[cur] = ''.join(buf); cur, buf = line.strip(), []
        else:
            buf.append(line)
    out[cur] = ''.join(buf)
    return out


cp = 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md'
sa, sb = sections(os.path.join(S34, cp)), sections(os.path.join(S35, cp))
R['contractSections'] = {'n34': len(sa), 'n35': len(sb), 'added': [k for k in sb if k not in sa],
                         'removed': [k for k in sa if k not in sb], 'changed': [k for k in sb if k in sa and sa[k] != sb[k]]}
print('\ncontract sections 34/35 %d/%d changed=%s added=%s removed=%s' % (
    len(sa), len(sb), R['contractSections']['changed'], R['contractSections']['added'], R['contractSections']['removed']))


def funcs(path):
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines()
    o = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            o[n.name] = '\n'.join(lines[n.lineno - 1:n.end_lineno])
        elif isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name):
                    o['=' + tg.id] = '\n'.join(lines[n.lineno - 1:n.end_lineno])
    return o


for p in ('docs/coop/design-corrections/foundation/atom_model.v1.py', 'docs/coop/design-corrections/foundation/check-atoms.v1.py'):
    fa, fb = funcs(os.path.join(S34, p)), funcs(os.path.join(S35, p))
    ch = {'added': [k for k in fb if k not in fa], 'removed': [k for k in fa if k not in fb],
          'changed': [k for k in fb if k in fa and fa[k] != fb[k]]}
    R['files'][p]['topLevel'] = ch
    print('\n%s\n  added  : %s\n  removed: %s\n  changed: %s' % (p.split('/')[-1], ch['added'], ch['removed'], ch['changed']))

sp = 'docs/coop/design-corrections/foundation/incoming-search.schema.v1.json'
ja, jb = json.load(open(os.path.join(S34, sp))), json.load(open(os.path.join(S35, sp)))
paths = []


def jdiff(x, y, path='#'):
    if type(x) != type(y):
        paths.append((path, x, y)); return
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                paths.append((path + '/' + k, x.get(k, '<absent>'), y.get(k, '<absent>')))
            else:
                jdiff(x[k], y[k], path + '/' + k)
    elif isinstance(x, list):
        if len(x) != len(y):
            paths.append((path, x, y)); return
        for n, (u, v) in enumerate(zip(x, y)):
            jdiff(u, v, '%s/%d' % (path, n))
    elif x != y:
        paths.append((path, x, y))


jdiff(ja, jb)
R['schemaJsonPathChanges'] = [{'path': p, 'v34': a, 'v35': b} for p, a, b in paths]
print('\nincoming-search.schema JSON-path changes (%d):' % len(paths))
for p, a, b in paths:
    print('  %s\n     34: %s\n     35: %s' % (p, str(a)[:400], str(b)[:400]))
vocab = ('$schema', 'type', 'required', 'properties', 'minItems', 'maxItems', 'enum', 'const', 'pattern', 'additionalProperties',
         'items', 'oneOf', 'anyOf', 'allOf', 'if', 'then', 'else', '$ref', '$defs', 'uniqueItems', 'minimum', 'maximum')
R['schemaValidationKeywordChanged'] = any(any(seg in vocab for seg in p.split('/')) for p, _, _ in paths)
print('any change under a validation keyword path:', R['schemaValidationKeywordChanged'])

L4 = 'docs/v2/architecture/implementation-normative-inputs.v4.json'
l4 = json.load(open(os.path.join(S35, L4)))
pins = []


def walk(o):
    if isinstance(o, dict):
        if 'path' in o and ('sha256' in o or 'digest' in o):
            pins.append((o['path'], o.get('sha256') or o.get('digest')))
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(l4)
ch = {c['path'] for c in r00['delta']['changed']}
R['layer4'] = {'sha34': sha(os.path.join(S34, L4)), 'sha35': sha(os.path.join(S35, L4)), 'pins': len(pins),
               'pinsResolveAgainst35': sum(1 for p, d in pins if os.path.isfile(os.path.join(S35, p)) and sha(os.path.join(S35, p)) == d),
               'pinnedPathsInDelta': sorted({p for p, _ in pins if p in ch})}
print('\nlayer4 unchanged=%s pins=%d resolve35=%d pinnedInDelta=%s' % (
    R['layer4']['sha34'] == R['layer4']['sha35'], len(pins), R['layer4']['pinsResolveAgainst35'], R['layer4']['pinnedPathsInDelta']))
json.dump(R, open(os.path.join(OUT, 'r01-diffs.json'), 'w'), indent=1, default=str)
print('wrote r01-diffs.json')
