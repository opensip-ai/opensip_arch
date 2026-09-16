"""Print structural summaries of the source39 root/author evidence records named by the charter (stdout only; writes nothing)."""
import hashlib, json, os
B = '/tmp/opensip-design-corrections'
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def J(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def shape(x, depth=0, width=60):
    if isinstance(x, dict):
        if depth >= 3:
            return '{%d keys: %s}' % (len(x), ','.join(list(x)[:12]))
        return {k: shape(v, depth + 1) for k, v in list(x.items())[:width]}
    if isinstance(x, list):
        if not x or depth >= 3:
            return '[%d]' % len(x)
        return ['[%d]' % len(x), shape(x[0], depth + 1)]
    if isinstance(x, str):
        return x[:240]
    return x


def show(p, limit=6000):
    print('=====', p, sha(p))
    try:
        print(json.dumps(shape(J(p)), indent=1, default=str)[:limit])
    except Exception as exc:  # noqa: BLE001
        print('not json:', exc)


for d in ('claude-author-package-successor.v16', 'root-author-package-final39-rebuild.v1', 'claude-author-package-migration.v1', 'claude-author-package-migration.v1/overlay',
          'author-package-final39-verification.v1'):
    print('== top-level', d, sorted(os.listdir(B + '/' + d)))
show(B + '/claude-author-package-successor.v16/artifact-manifest.json', 3000)
for f in sorted(os.listdir(B + '/claude-author-package-successor.v16')):
    if f.startswith('source-binding') or f in ('package-construction.json', 'overlay-laws.json', 'construction-provenance.json'):
        show(B + '/claude-author-package-successor.v16/' + f, 5000)
for f in sorted(os.listdir(B + '/root-author-package-final39-rebuild.v1')):
    if f.endswith('.json'):
        show(B + '/root-author-package-final39-rebuild.v1/' + f, 5000)
show(B + '/author-package-final39-verification.v1/verification.json', 3000)
mine, root = J(RT + '/work/package-v16-verify/verification.json'), J(B + '/author-package-final39-verification.v1/verification.json')
print('== verification content equal to root:', mine == root)
print('== my groups', json.dumps([{k: g.get(k) for k in g if not isinstance(g.get(k), (dict, list))} for g in mine['groups']], indent=0)[:3000])
show(RT + '/work/probe-native-v2.json', 3000)
for name in ('root-source39-final-reference.v1', 'root-source39-final-reference.v2'):
    p = B + '/' + name + '/reference-checks.json'
    show(p, 4000)
    d = J(p)
    for k, v in d.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            for r in v:
                print('  row', {kk: (str(vv)[-500:]) for kk, vv in r.items() if kk in ('name', 'exitCode', 'passed', 'stdoutTail', 'stderrTail', 'failed', 'failures')})
for name in ('root-source39-final-reference.v1', 'root-source39-final-reference.v2'):
    for f in ('foundation.stdout', 'foundation.stderr', 'foundation.json'):
        p = B + '/' + name + '/' + f
        print('==', name, f, sha(p), open(p, encoding='utf-8', errors='replace').read()[-1500:])
show(B + '/root-foundation-detail-census-correction.v1/assessment.json', 6000)
for f in ('identity-failure.json', 'foundation-failure.json'):
    show(B + '/root-foundation-detail-census-correction.v1/' + f, 2500)
print('== correction.diff', open(B + '/root-foundation-detail-census-correction.v1/correction.diff').read()[:4000])
show(B + '/root-final-owner-integration.v1/integration.json', 5000)
show(B + '/root-final-owner-integration.v1/prepared.json', 2500)
