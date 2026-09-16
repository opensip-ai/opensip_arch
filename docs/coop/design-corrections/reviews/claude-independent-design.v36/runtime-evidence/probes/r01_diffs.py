"""R01 — exact 35->36 diffs of all ten changed files (parent bytes from the archive-verified frozen35 extraction in r00;
child bytes from frozen36), contract section and model/checker top-level changes, every JSON-path change in the pin
ledgers, registry and generated workflows report, and planning layer4 exposure. Read-only on both sides."""
import ast, difflib, hashlib, json, os, re

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
PAR = os.path.join(BASE, 'disposable/parent35-delta-files')
DIFFS = os.path.join(OUT, 'diffs')
os.makedirs(DIFFS, exist_ok=True)
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
r00 = json.load(open(os.path.join(OUT, 'r00-custody.json')))
m36 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v36.json')))['files']}
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {'files': {}}
V35 = '/tmp/opensip-design-corrections/claude-independent-design.v35'
FOC = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
R['baselines'] = {'v35ReviewJson': sha(V35 + '/review.json'), 'v35ReviewMd': sha(V35 + '/review.md'),
                  'focusedReviewJson': sha(FOC + '/review.json'), 'focusedReviewMd': sha(FOC + '/review.md')}
R['baselinesMatch'] = (R['baselines']['v35ReviewJson'] == 'd7dc035c532968df80334809815f1257a49b83fd47f880e3a89630df9669cd52'
                       and R['baselines']['v35ReviewMd'] == '687ed3dda5c07e7f8def8e824aff7c135a5cca9a1d91d8705e36bfff010d5a7b'
                       and R['baselines']['focusedReviewJson'] == '4df5fb241d74ec6c3ac15271234b704c7fa2a451149100dcba926e3c2994a421'
                       and R['baselines']['focusedReviewMd'] == 'a4e3f39a092a93643853427a305742803609b7bb68687ed10214e26d1728bd5c')
print('baselines (v35 review json/md, focused json/md) match:', R['baselinesMatch'])
for c in r00['delta']['changed']:
    p = c['path']
    a, b = os.path.join(PAR, p), os.path.join(S36, p)
    assert sha(a) == c['sha35'] and sha(b) == c['sha36'], p
    A = open(a, encoding='utf-8').read().splitlines()
    B = open(b, encoding='utf-8').read().splitlines()
    d = list(difflib.unified_diff(A, B, 'v35/' + p, 'v36/' + p, lineterm='', n=3))
    plus = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    fn = os.path.join(DIFFS, p.replace('/', '__') + '.diff')
    open(fn, 'w', encoding='utf-8').write('\n'.join(d) + '\n')
    R['files'][p] = {'lines35': len(A), 'lines36': len(B), 'plus': plus, 'minus': minus, 'diffFile': fn, 'diffSha256': sha(fn)}
    print('%-80s lines %5d->%5d  +%-4d -%-4d' % (p, len(A), len(B), plus, minus))


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
sa, sb = sections(os.path.join(PAR, cp)), sections(os.path.join(S36, cp))
R['contractSections'] = {'n35': len(sa), 'n36': len(sb), 'added': [k for k in sb if k not in sa], 'removed': [k for k in sa if k not in sb],
                         'changed': [k for k in sb if k in sa and sa[k] != sb[k]]}
bold = lambda t: set(re.findall(r'\*\*([^*]{3,80})\*\*', t))
R['contractBoldLabelsAdded'] = sorted(bold(open(os.path.join(S36, cp)).read()) - bold(open(os.path.join(PAR, cp)).read()))
print('\ncontract sections 35/36 %d/%d changed=%s added=%s removed=%s' % (len(sa), len(sb), R['contractSections']['changed'], R['contractSections']['added'], R['contractSections']['removed']))
print('bold labels added:', R['contractBoldLabelsAdded'])


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
    fa, fb = funcs(os.path.join(PAR, p)), funcs(os.path.join(S36, p))
    ch = {'added': [k for k in fb if k not in fa], 'removed': [k for k in fa if k not in fb], 'changed': [k for k in fb if k in fa and fa[k] != fb[k]]}
    R['files'][p]['topLevel'] = ch
    print('\n%s\n  added  : %s\n  removed: %s\n  changed: %s' % (p.split('/')[-1], ch['added'], ch['removed'], ch['changed']))
ca35, ca36 = funcs(os.path.join(PAR, 'docs/coop/design-corrections/foundation/check-atoms.v1.py')), funcs(os.path.join(S36, 'docs/coop/design-corrections/foundation/check-atoms.v1.py'))
R['checkAtomsExistingCasesBodiesUnchanged'] = sorted(k for k in ca35 if k.startswith('test_') and ca35[k] != ca36.get(k))


def flat(o, p='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, p + '.' + k)
    elif isinstance(o, list):
        for n, v in enumerate(o):
            yield from flat(v, '%s[%d]' % (p, n))
    else:
        yield p, o


R['jsonPathChanges'] = {}
for c in r00['delta']['changed']:
    p = c['path']
    if not p.endswith('.json'):
        continue
    fa, fb = dict(flat(json.load(open(os.path.join(PAR, p))))), dict(flat(json.load(open(os.path.join(S36, p)))))
    changed = sorted(k for k in fa if k in fb and fa[k] != fb[k])
    rec = {'removed': sorted(set(fa) - set(fb)), 'added': sorted(set(fb) - set(fa)), 'changedCount': len(changed), 'changed': []}
    for k in changed:
        va, vb = fa[k], fb[k]
        parent = k.rsplit('.', 1)[0]
        sib = {kk.rsplit('.', 1)[-1]: fb[kk] for kk in fb if kk.rsplit('.', 1)[0] == parent and not kk.endswith(k.rsplit('.', 1)[-1])}
        entry = {'path': k, 'v35': str(va)[:200], 'v36': str(vb)[:200], 'siblingPath': sib.get('path') or sib.get('file') or sib.get('source')}
        if isinstance(va, str) and re.fullmatch(r'[0-9a-f]{64}', va or '') and re.fullmatch(r'[0-9a-f]{64}', vb or ''):
            entry['digestPair'] = True
            entry['v35IsParentDigestOf'] = sorted(q for q, h in m35.items() if h == va)[:3]
            entry['v36IsFrozen36DigestOf'] = sorted(q for q, h in m36.items() if h == vb)[:3]
        rec['changed'].append(entry)
    R['jsonPathChanges'][p] = rec
    print('\n%s: removed %d added %d changed %d' % (p.split('/')[-1], len(rec['removed']), len(rec['added']), len(changed)))
    for e in rec['changed'][:12]:
        print('   %s  sib=%s  35->%s  36->%s' % (e['path'][-60:], e.get('siblingPath'), e.get('v35IsParentDigestOf'), e.get('v36IsFrozen36DigestOf')))
PINS = [p for p in R['jsonPathChanges'] if p.endswith('source-pins.v1.json') or p.endswith('source-pins.v2.json')]
R['pinLedgers'] = {}
for p in PINS:
    rec = R['jsonPathChanges'][p]
    targets = sorted({t for e in rec['changed'] for t in (e.get('v36IsFrozen36DigestOf') or [])})
    R['pinLedgers'][p] = {'onlyDigestPairsChanged': all(e.get('digestPair') for e in rec['changed']) and not rec['added'] and not rec['removed'],
                          'repinnedFiles': targets, 'count': rec['changedCount'],
                          'everyNewDigestIsTheFrozen36DigestOfAChangedFile': all(set(e.get('v36IsFrozen36DigestOf') or []) & set(R['files']) for e in rec['changed'])}
print('\npin ledgers:', json.dumps(R['pinLedgers'], indent=1))
L4 = 'docs/v2/architecture/implementation-normative-inputs.v4.json'
l4 = json.load(open(os.path.join(S36, L4)))
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
R['layer4'] = {'sha35': m35[L4], 'sha36': m36[L4], 'unchanged': m35[L4] == m36[L4], 'pins': len(pins),
               'pinsResolveAgainst36': sum(1 for p, d in pins if os.path.isfile(os.path.join(S36, p)) and sha(os.path.join(S36, p)) == d),
               'pinnedPathsInDelta': sorted({p for p, _ in pins if p in ch})}
PLAN_OWNERS = ('docs/v2/architecture/14-repository-and-module-layout.md', 'docs/v2/architecture/repository-file-inventory.v1.json',
               'docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json')
R['planningOwnersUnchanged35to36'] = {p: m35.get(p) == m36.get(p) for p in PLAN_OWNERS}
print('\nlayer4 unchanged=%s pins=%d resolve36=%d pinnedInDelta=%s | planning owners unchanged %s' % (
    R['layer4']['unchanged'], len(pins), R['layer4']['pinsResolveAgainst36'], R['layer4']['pinnedPathsInDelta'], R['planningOwnersUnchanged35to36']))
json.dump(R, open(os.path.join(OUT, 'r01-diffs.json'), 'w'), indent=1, default=str)
print('wrote r01-diffs.json')
