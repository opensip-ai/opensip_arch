"""Reference rerun v46 comparison, workflows report leaf delta, ledger pins, D9 carriage and TCB dependents."""
import json, hashlib, os, re, glob
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
S = PK + 'files/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
out = {}
m = json.load(open(PK + 'application-subject.v46.json'))
fh = {e['path']: e['sha256'] for e in m['files']}
# 1. rerun v46 vs 45.2
a = PK + 'support/reference-rerun/'; b = PK + 'support/reference-rerun.v46/'
ra = {os.path.relpath(p, a): h(p) for p in glob.glob(a + '**', recursive=True) if os.path.isfile(p)}
rb = {os.path.relpath(p, b): h(p) for p in glob.glob(b + '**', recursive=True) if os.path.isfile(p)}
out['rerun'] = {'n45': len(ra), 'n46': len(rb), 'onlyIn45': sorted(set(ra) - set(rb)), 'onlyIn46': sorted(set(rb) - set(ra)),
                'differ': sorted(k for k in ra if k in rb and ra[k] != rb[k]), 'same': sum(1 for k in ra if k in rb and ra[k] == rb[k])}
def jdiff(x, y, p='', acc=None):
    acc = [] if acc is None else acc
    if type(x) != type(y): acc.append((p, str(x)[:200], str(y)[:200])); return acc
    if isinstance(x, dict):
        for k in set(x) | set(y):
            if k not in x or k not in y: acc.append((p + '/' + k, str(x.get(k))[:200], str(y.get(k))[:200]))
            else: jdiff(x[k], y[k], p + '/' + k, acc)
    elif isinstance(x, list):
        if len(x) != len(y): acc.append((p + '#len', len(x), len(y)))
        for i in range(min(len(x), len(y))): jdiff(x[i], y[i], p + '/' + str(i), acc)
    elif x != y: acc.append((p, str(x)[:200], str(y)[:200]))
    return acc
dd = {}
for k in out['rerun']['differ']:
    if k.endswith('.json'):
        try: dd[k] = jdiff(json.load(open(a + k)), json.load(open(b + k)))[:12]
        except Exception as e: dd[k] = str(e)
    else:
        dd[k] = 'text differs'
out['rerunDiffDetail'] = dd
# stdout hashes in staged-reference-checks
src = json.load(open(PK + 'support/staged-reference-checks.v1.json'))
chk = []
for c in src['commands']:
    rel = c['source']
    row = {'name': c['name'], 'srcEqStaged': fh.get(rel) == c['sourceSha256'] if rel in fh else None,
           'srcEqSnapshot': h(SNAP + rel) == c['sourceSha256'] if os.path.exists(SNAP + rel) else None, 'exit': c['exitCode']}
    if 'stdoutSha256' in c:
        cand = [p for p in rb if p.endswith(c['name'] + '.stdout') and '/' not in p]
        row['stdoutFileMatch'] = [h(b + p) == c['stdoutSha256'] for p in cand]
        cand = [p for p in rb if p.endswith(c['name'] + '.stderr') and '/' not in p]
        row['stderrFileMatch'] = [h(b + p) == c['stderrSha256'] for p in cand]
    chk.append(row)
out['stagedReferenceChecks'] = chk
# receipts reportSha256 fields
def find(o, key, p=''):
    r = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: r.append((p + '/' + k, v))
            r += find(v, key, p + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): r += find(v, key, p + '/' + str(i))
    return r
for n in ['workflows.json', 'integration.json', 'security.json', 'foundation.json']:
    j = json.load(open(b + n))
    out.setdefault('receiptReportHashes', {})[n] = find(j, 'reportSha256') + find(j, 'passed')[:3] + find(j, 'exitCode')[:3]
# accepted final-reference reports vs v46 rerun outputs
acc = R + 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/'
pairs = [('foundation/identity-report.json', 'foundation/identity-report.json'), ('foundation/foundation-report.json', 'foundation/foundation-report.json'),
         ('foundation/product-quality-report.json', 'foundation/product-quality-report.json'), ('foundation/product-configuration-report.json', 'foundation/product-configuration-report.json'),
         ('foundation/array-order-report.json', 'foundation/array-order-report.json'), ('security.json', 'security.json'), ('integration.json', 'integration.json'),
         ('foundation.json', 'foundation.json'), ('workflows.json', 'workflows.json'), ('evaluator3/report.json', 'evaluator3/report.json')]
out['vsAccepted'] = {x: (h(acc + x) == h(b + y)) if os.path.exists(acc + x) and os.path.exists(b + y) else 'missing' for x, y in pairs}
for x, y in pairs:
    if out['vsAccepted'][x] is False:
        try: out.setdefault('vsAcceptedDiff', {})[x] = jdiff(json.load(open(acc + x)), json.load(open(b + y)))[:10]
        except Exception as e: out.setdefault('vsAcceptedDiff', {})[x] = str(e)
# 2. workflows report leaf delta
wr = 'docs/coop/design-corrections/workflows/workflows-report.v1.json'
out['workflowsReport'] = {'staged': h(S + wr), 'snapshot': h(SNAP + wr), 'leafDiff': jdiff(json.load(open(SNAP + wr)), json.load(open(S + wr))),
                          'stagedLedger': h(S + 'docs/coop/design-corrections/workflows/source-pins.v1.json'), 'snapshotLedger': h(SNAP + 'docs/coop/design-corrections/workflows/source-pins.v1.json'),
                          'liveLedger': h(R + 'docs/coop/design-corrections/workflows/source-pins.v1.json') if os.path.exists(R + 'docs/coop/design-corrections/workflows/source-pins.v1.json') else None,
                          'liveReport': h(R + wr) if os.path.exists(R + wr) else None}
wj = json.load(open(b + 'workflows.json'))
out['workflowsReport']['rerunReceiptMentions'] = [x for x in find(wj, 'reportSha256')]
# which ledgers mention the workflows report path
led = []
for p in glob.glob(S + 'docs/**/*source-pins*.json', recursive=True):
    t = open(p).read()
    if 'workflows-report.v1.json' in t: led.append(os.path.relpath(p, S))
out['ledgersMentioningWorkflowsReport'] = led
out['stagedLedgers'] = {os.path.relpath(p, S): {'staged': h(p), 'snapshot': h(SNAP + os.path.relpath(p, S)) if os.path.exists(SNAP + os.path.relpath(p, S)) else None} for p in glob.glob(S + 'docs/**/*source-pins*.json', recursive=True)}
# 3. D9 carriage
ir = json.load(open(S + 'docs/coop/design-corrections/inherited-residuals.applied.v1.json'))
car = []
for coll in ('parents', 'residuals'):
    for i, r in enumerate(ir.get(coll, [])):
        if 'carriedCrossUnitObligation' in r: car.append((coll, i, r.get('id'), r['carriedCrossUnitObligation']))
out['d9Carriage'] = car
# 4. TCB
app = json.load(open(S + 'docs/coop/design-corrections/application.v1.json'))
out['tcb'] = app.get('sharedTrustedCodeAssumption')
out['referenceEvidenceSummary'] = app.get('referenceEvidenceSummary')
ev = json.load(open(S + 'docs/coop/design-corrections/evaluation-residual-dispositions.applied.v1.json'))
out['evalTop'] = {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in ev.items()}
json.dump(out, open('/private/tmp/opensip-design-corrections/application-review.v46/probes/out/p06.json', 'w'), indent=1, ensure_ascii=False, default=str)
for k in ['rerun', 'rerunDiffDetail', 'stagedReferenceChecks', 'receiptReportHashes', 'vsAccepted', 'vsAcceptedDiff', 'workflowsReport', 'ledgersMentioningWorkflowsReport', 'stagedLedgers', 'referenceEvidenceSummary', 'evalTop']:
    print(k, json.dumps(out.get(k), indent=1, ensure_ascii=False, default=str)[:3000])
print('d9', json.dumps(out['d9Carriage'], indent=1, ensure_ascii=False)[:3500])
print('tcb', json.dumps(out['tcb'], indent=1, ensure_ascii=False)[:3500])
