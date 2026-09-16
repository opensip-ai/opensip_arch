"""P07 — the four package12->13 changed common members, read and diffed (README.md, evaluation-residual-author-assessment.json,
source-manifest.json, verify-package.py), plus the source-binding v35->v36 field delta. Establishes whether the verifier
changed anything but its source-version binding and whether the residual assessment changed anything but its subject
binding. Binding is not replay: replay standing comes from my own open_run_closure/close_run calls in r05."""
import difflib, hashlib, json, os

P12 = '/tmp/opensip-design-corrections/claude-author-package-successor.v12'
P13 = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
DIFFS = os.path.join(OUT, 'diffs-package12to13')
os.makedirs(DIFFS, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {'textDiffs': {}}
for rel in ('README.md', 'verify-package.py'):
    a = open(os.path.join(P12, rel), encoding='utf-8').read().splitlines()
    b = open(os.path.join(P13, rel), encoding='utf-8').read().splitlines()
    d = list(difflib.unified_diff(a, b, 'package12/' + rel, 'package13/' + rel, lineterm='', n=1))
    fn = os.path.join(DIFFS, rel.replace('/', '__') + '.diff')
    open(fn, 'w').write('\n'.join(d) + '\n')
    changed = [l for l in d if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    R['textDiffs'][rel] = {'plus': sum(1 for l in changed if l[0] == '+'), 'minus': sum(1 for l in changed if l[0] == '-'), 'changedLines': changed[:80], 'diffSha256': sha(fn)}
    print('\n== %s +%d -%d' % (rel, R['textDiffs'][rel]['plus'], R['textDiffs'][rel]['minus']))
    for l in changed[:60]:
        print('   ' + l[:220])


def flat(o, p='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, p + '.' + k)
    elif isinstance(o, list):
        for n, v in enumerate(o):
            yield from flat(v, '%s[%d]' % (p, n))
    else:
        yield p, o


e12 = dict(flat(json.load(open(os.path.join(P12, 'evaluation-residual-author-assessment.json')))))
e13 = dict(flat(json.load(open(os.path.join(P13, 'evaluation-residual-author-assessment.json')))))
R['residualAssessmentJsonPathDelta'] = {'removed': sorted(set(e12) - set(e13))[:40], 'added': sorted(set(e13) - set(e12))[:40],
                                        'changed': [(k, str(e12[k])[:160], str(e13[k])[:160]) for k in sorted(e12) if k in e13 and e12[k] != e13[k]][:60]}
R['residualAssessmentChangedValueKinds'] = sorted({v[0].rsplit('.', 1)[-1] for v in R['residualAssessmentJsonPathDelta']['changed']})
print('\nresidual assessment delta: removed %d added %d changed %d kinds %s' % (len(R['residualAssessmentJsonPathDelta']['removed']), len(R['residualAssessmentJsonPathDelta']['added']),
                                                                          len(R['residualAssessmentJsonPathDelta']['changed']), R['residualAssessmentChangedValueKinds']))
for k, a, b in R['residualAssessmentJsonPathDelta']['changed'][:12]:
    print('   %s: %s -> %s' % (k, a[:90], b[:90]))
b35 = json.load(open(os.path.join(P13, 'source-binding.v35.json')))
b36 = json.load(open(os.path.join(P13, 'source-binding.v36.json')))
R['bindingDelta'] = {k: (b35.get(k), b36.get(k)) for k in sorted(set(b35) | set(b36)) if b35.get(k) != b36.get(k)}
R['bindingV35InPackage13EqualsPackage12'] = sha(os.path.join(P13, 'source-binding.v35.json')) == sha(os.path.join(P12, 'source-binding.v35.json'))
print('\nbinding v35->v36 delta:', R['bindingDelta'], '| v35 binding carried byte-equal:', R['bindingV35InPackage13EqualsPackage12'])
sm12, sm13 = sha(os.path.join(P12, 'source-manifest.json')), sha(os.path.join(P13, 'source-manifest.json'))
R['sourceManifests'] = {'package12': sm12, 'package13': sm13,
                        'package12IsFrozen35': sm12 == 'eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85',
                        'package13IsFrozen36': sm13 == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'}
print('source manifests:', R['sourceManifests'])
json.dump(R, open(os.path.join(OUT, 'p07-package-member-diffs.json'), 'w'), indent=1, default=str)
print('wrote p07-package-member-diffs.json')
