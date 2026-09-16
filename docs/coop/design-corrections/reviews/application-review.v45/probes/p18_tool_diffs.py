import difflib, os, json, hashlib
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
O = '/private/tmp/opensip-design-corrections/application-review.v45/probes/tooldiffs/'
os.makedirs(O, exist_ok=True)
pairs = [
 ('support/root-application45-review-shape-correction.v1/before/review_envelope.py', 'support/root-application45-review-shape-correction.v1/review_envelope.py'),
 ('support/root-application45-review-shape-correction.v1/before/bind-review-receipts.v1.py', 'support/root-application45-review-shape-correction.v1/bind-review-receipts.v1.py'),
 ('support/root-application45-review-shape-correction.v1/before/assemble-records.successor.v1.py', 'support/root-application45-review-shape-correction.v1/assemble-records.successor.v1.py'),
 ('support/root-application45-summary-source-correction.v1/before.py', 'support/root-application45-summary-source-correction.v1/apply-advisory-records.successor.v1.py'),
 ('support/root-application45-reproduction-correction.v1/assemble-before.py', 'support/root-application45-reproduction-correction.v1/assemble-records.successor.v1.py'),
 ('support/root-application45-final-records.v1/before/docs/coop/design-corrections/application.v1.json', 'files/docs/coop/design-corrections/application.v1.json'),
 ('support/root-application45-final-records.v1/before/docs/coop/design-corrections/README.md', 'files/docs/coop/design-corrections/README.md'),
 ('support/root-application45-final-records.v1/before/docs/v2/architecture/08-decision-and-readiness-register.md', 'files/docs/v2/architecture/08-decision-and-readiness-register.md'),
 ('support/root-application45-final-records.v1/before/docs/coop/COORDINATOR-DECISIONS.md', 'files/docs/coop/COORDINATOR-DECISIONS.md'),
 ('support/finalize-application.before-selftest.py', 'files/docs/coop/design-corrections/finalize-application.v1.py'),
 ('support/check-finalizer.initial.py', 'support/check-finalizer.py'),
 ('support/root-final-preflight.before-count.py', 'support/root-final-preflight.py'),
]
def sha(p): return hashlib.sha256(open(S + p, 'rb').read()).hexdigest()
for a, b in pairs:
    A = open(S + a, encoding='utf-8').read().splitlines(); B = open(S + b, encoding='utf-8').read().splitlines()
    ud = list(difflib.unified_diff(A, B, a, b, n=2, lineterm=''))
    name = b.replace('/', '__') + '.diff'
    open(O + name, 'w').write('\n'.join(ud) + '\n')
    print(name, 'lines', len(ud), 'beforeSha', sha(a)[:12], 'afterSha', sha(b)[:12])
# current support helpers equal corrected versions?
for x in ['review_envelope.py', 'bind-review-receipts.v1.py', 'assemble-records.successor.v1.py', 'apply-advisory-records.successor.v1.py']:
    cur = 'support/' + x
    for d in ['support/root-application45-review-shape-correction.v1/', 'support/root-application45-summary-source-correction.v1/', 'support/root-application45-reproduction-correction.v1/']:
        if os.path.exists(S + d + x):
            print('current', x, '==', d + x, sha(cur) == sha(d + x))
fr = json.load(open(S + 'support/root-application45-final-records.v1/corrections.json'))
for f in fr['files']:
    bp = 'support/root-application45-final-records.v1/before/' + f['path']
    print('final-record', f['path'], 'before ok', sha(bp) == f['beforeSha256'], 'after==staged', sha('files/' + f['path']) == f['afterSha256'])
