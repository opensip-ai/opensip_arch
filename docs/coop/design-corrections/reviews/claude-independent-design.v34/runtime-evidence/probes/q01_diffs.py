"""Q01 — exact 33->34 diffs of all nine changed files (read-only on both frozen snapshots), and layer4
input exposure: does any of layer4's 29 pinned input bytes change in source34?"""
import difflib, hashlib, json, os, re

S33 = '/tmp/opensip-design-corrections/candidate-subject.v33'
S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
DIFFS = os.path.join(OUT, 'diffs')
os.makedirs(DIFFS, exist_ok=True)
q00 = json.load(open(os.path.join(OUT, 'q00-custody.json')))
R = {'files': {}}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


for c in q00['delta']['changed']:
    p = c['path']
    a, b = os.path.join(S33, p), os.path.join(S34, p)
    assert sha(a) == c['sha33'] and sha(b) == c['sha34'], p
    A = open(a, encoding='utf-8').read().splitlines()
    B = open(b, encoding='utf-8').read().splitlines()
    d = list(difflib.unified_diff(A, B, 'v33/' + p, 'v34/' + p, lineterm='', n=3))
    plus = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    fn = os.path.join(DIFFS, p.replace('/', '__') + '.diff')
    open(fn, 'w', encoding='utf-8').write('\n'.join(d) + '\n')
    R['files'][p] = {'lines33': len(A), 'lines34': len(B), 'plus': plus, 'minus': minus, 'diffFile': fn}
    print('%-80s lines %5d->%5d  +%-4d -%-4d' % (p, len(A), len(B), plus, minus))
    if p.endswith('.json') and plus + minus <= 40:
        for l in d:
            if l.startswith(('+', '-')) and not l.startswith(('+++', '---')):
                print('      %s' % l.strip()[:200])

# section-level view of the contract
p = 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md'


def sections(path):
    out, cur, buf = {}, '(preamble)', []
    for line in open(path, encoding='utf-8'):
        if re.match(r'^#{1,4} ', line):
            out[cur] = ''.join(buf)
            cur, buf = line.strip(), []
        else:
            buf.append(line)
    out[cur] = ''.join(buf)
    return out


sa, sb = sections(os.path.join(S33, p)), sections(os.path.join(S34, p))
R['contractSections'] = {'n33': len(sa), 'n34': len(sb),
                         'added': [k for k in sb if k not in sa], 'removed': [k for k in sa if k not in sb],
                         'changed': [k for k in sb if k in sa and sa[k] != sb[k]]}
print('\ncontract sections 33/34: %d/%d' % (len(sa), len(sb)))
print('  added  :', R['contractSections']['added'])
print('  removed:', R['contractSections']['removed'])
print('  changed:', R['contractSections']['changed'])

# python files: which top-level functions changed?
for p in ('docs/coop/design-corrections/foundation/atom_model.v1.py',
          'docs/coop/design-corrections/foundation/check-atoms.v1.py'):
    import ast
    def funcs(path):
        src = open(path, encoding='utf-8').read()
        t = ast.parse(src)
        lines = src.splitlines()
        o = {}
        for n in t.body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                o[n.name] = '\n'.join(lines[n.lineno - 1:n.end_lineno])
            elif isinstance(n, ast.Assign):
                for tg in n.targets:
                    if isinstance(tg, ast.Name):
                        o['=' + tg.id] = '\n'.join(lines[n.lineno - 1:n.end_lineno])
        return o
    fa, fb = funcs(os.path.join(S33, p)), funcs(os.path.join(S34, p))
    ch = {'added': [k for k in fb if k not in fa], 'removed': [k for k in fa if k not in fb],
          'changed': [k for k in fb if k in fa and fa[k] != fb[k]]}
    R['files'][p]['topLevel'] = ch
    print('\n%s\n  added  : %s\n  removed: %s\n  changed: %s' % (p, ch['added'], ch['removed'], ch['changed']))

# layer4 exposure
L4 = os.path.join(S34, 'docs/v2/architecture/implementation-normative-inputs.v4.json')
l4 = json.load(open(L4))
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
changedpaths = {c['path'] for c in q00['delta']['changed']}
R['layer4'] = {'sha34': sha(L4), 'sha33': sha(os.path.join(S33, 'docs/v2/architecture/implementation-normative-inputs.v4.json')),
               'pins': len(pins),
               'pinsResolveAgainst34': sum(1 for pth, d in pins if os.path.isfile(os.path.join(S34, pth)) and sha(os.path.join(S34, pth)) == d),
               'pinnedPathsInDelta': sorted({pth for pth, _ in pins if pth in changedpaths})}
print('\nlayer4: file unchanged 33->34 = %s | pins=%d | resolve vs 34 = %d | pinned paths in delta = %s'
      % (R['layer4']['sha33'] == R['layer4']['sha34'], len(pins), R['layer4']['pinsResolveAgainst34'],
         R['layer4']['pinnedPathsInDelta']))
json.dump(R, open(os.path.join(OUT, 'q01-diffs.json'), 'w'), indent=1, default=str)
print('wrote q01-diffs.json and receipts/diffs/*.diff')
