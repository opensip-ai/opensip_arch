import json, os, hashlib, collections, difflib
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
V = '/private/tmp/opensip-design-corrections/application-stage.v45.2-validation/'
wr = 'docs/coop/design-corrections/workflows/workflows-report.v1.json'
print('validation scratch exists', os.path.isdir(V))
if os.path.isfile(V + wr):
    a = open(C + wr).read().splitlines(); b = open(V + wr).read().splitlines()
    print('regenerated workflows report differs', a != b)
    print('\n'.join(difflib.unified_diff(a, b, 'snapshot', 'rerun', n=0, lineterm='')))
for p in ['docs/coop/design-corrections/native/native-evidence-report.v2.json', 'docs/coop/design-corrections/foundation/identity-report.json', 'docs/coop/design-corrections/foundation/validation-report.json', 'docs/coop/design-corrections/integration-report.v1.json', 'docs/coop/design-corrections/security/security-lifecycle-report.v1.json']:
    if os.path.isfile(V + p):
        print('scratch', p, 'equal snapshot', open(V + p, 'rb').read() == open(C + p, 'rb').read())
# support reruns vs accepted executed reports
pairs = [('support/reference-rerun/foundation/identity-report.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/foundation/identity-report.json'),
         ('support/reference-rerun/security.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/security.json'),
         ('support/reference-rerun/integration.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/integration.json'),
         ('support/reference-rerun/workflows.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/workflows.json'),
         ('support/reference-rerun/foundation.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/foundation.json'),
         ('support/reference-rerun/evaluator3/report.json', 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/evaluator3/report.json')]
for a, b in pairs:
    A = open(S + a, 'rb').read(); B = open(R + b, 'rb').read()
    print('rerun', a, 'bytes-equal accepted execution', A == B)
    if A != B:
        try:
            ja = json.loads(A); jb = json.loads(B)
            def flat(o, p=''):
                out = {}
                if isinstance(o, dict):
                    for k, v in o.items(): out.update(flat(v, p + '/' + k))
                elif isinstance(o, list):
                    for i, v in enumerate(o): out.update(flat(v, p + '/' + str(i)))
                else: out[p] = o
                return out
            fa, fb = flat(ja), flat(jb)
            ch = [(k, fb.get(k), fa.get(k)) for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)]
            print('   leaf changes', len(ch)); [print('     ', str(x)[:260]) for x in ch[:12]]
        except Exception as ex:
            print('   non-json', ex)
for f in ['native.stdout', 'evaluator3.stdout', 'foundation.stdout', 'integration.stdout', 'security.stdout', 'workflows.stdout']:
    print('stdout', f, open(S + 'support/reference-rerun/' + f).read().strip()[:400])
# identity report count verification
ir = json.load(open(R + 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/foundation/identity-report.json'))
print('identity report keys', list(ir.keys())[:20])
def find_lists(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from find_lists(v, p + '/' + k)
    elif isinstance(o, list):
        if o and isinstance(o[0], dict): yield p, o
        for i, v in enumerate(o[:1]): yield from find_lists(v, p + '/0')
for p, L in find_lists(ir):
    ids = [x.get('id') or x.get('check') or x.get('name') for x in L]
    if len(L) > 100:
        c = collections.Counter(ids)
        print('list', p, len(L), 'distinct', len(c), 'dups', {k: v for k, v in c.items() if v > 1}, 'passed', collections.Counter(str(x.get('passed', x.get('status'))) for x in L))
# old application review findings
oa = json.load(open(R + 'docs/coop/design-corrections/reviews/application-review.v1/application-review.json'))
print('old app review keys', list(oa.keys()))
for k, v in oa.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and 'id' in v[0]:
        print(' ', k, [x['id'] for x in v])
# blind review advisories and limitations
br = json.load(open(R + 'docs/coop/design-corrections/reviews/consumer-b.v24-source45.v1/blind-review.json'))
for a in br['advisories']:
    print('BLIND-ADV', a['id'], '|', a['title'][:300], '| selectors', json.dumps(a.get('selectors'))[:300])
for l in br['limitations']: print('BLIND-LIM', l[:500])
ba = json.load(open(R + 'docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-assessment.v24-source45.v1.json'))
aa = json.load(open(S + 'files/docs/coop/design-corrections/accepted-review-advisories.v1.json'))
print('blind advisory ids review', [a['id'] for a in br['advisories']])
print('blind items app', [a['id'] for a in aa['blindItems']], 'equal codex account', aa['blindItems'] == ba['newAdvisoryApplicationAccount'])
print('independentBlindReviewFindings equal review advisories', aa['independentBlindReviewFindings'] == br['advisories'])
dr = json.load(open(R + 'docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json'))
print('independentReviewFindings equal review advisories', aa['independentReviewFindings'] == dr['advisories'])
ca = json.load(open(R + 'docs/coop/design-corrections/reviews/codex-post-reset.v1/design-assent.v45.json'))
print('app items first2 == codex advisory account', aa['items'][:2] == ca['advisoryApplicationAccount'])
for a in aa['blindItems']: print('BLIND-ACCOUNT', a['id'], a['disposition'], '|', a['applicationAccount'][:400])
print('codex blind scopeLimits', ba['scopeLimits'])
inv = json.load(open(S + 'files/docs/operations/document-inventory.v1.json'))
print('inventory excludedPaths', inv['workingTreeDelta']['excludedPaths'])
print('finalizer selftest', open(S + 'support/finalizer-selftest.v1.json').read()[:3000])
print('finalizer selftest log', open(S + 'support/finalizer-selftest.log').read())
print('dev note', open(S + 'support/finalizer-selftest-development-note.json').read())
