"""Checker-level targeted refusals for the source45 closedWorld binding, on a disposable scratch copy of this review's verified
source45 probe copy (never the frozen subject or the verified copies). Positive reachability first: the unmutated scratch checker
passes. Then each of the three bound sources is mutated alone (the published startup-law member, the section 9.7 JSON record, the
retained closed_world_v2 no-manifest reason), the native unit's own pin ledger is regenerated inside the scratch copy so the checker
reaches its law checks instead of stopping at pins, the checker is run, and the exact published fault text plus case results are
recorded; the original bytes are restored before the next variant and a final unmutated run must pass again.
Writes only receipts/probes/checker-binding45.json (scratch copy under work/scratch45-checker)."""
import hashlib, json, os, re, shutil, subprocess
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
SRC = RT / 'work/source45-pkg'
SCR = RT / 'work/scratch45-checker'
PY = '/tmp/opensip-architecture-review-env/bin/python'
NAT = 'docs/coop/design-corrections/native/'
CHECK = NAT + 'check_native_evidence.v2.py'
LAW = NAT + 'provider-startup.schemas.v1.json'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
MODEL = NAT + 'native_evidence_model.v2.py'
PINS = NAT + 'source-pins.v2.json'
REPORT = NAT + 'native-evidence-report.v2.json'
FAULT_LAW = 'pre-analysis closedWorld differs from the exact section 9.7 record'
FAULT_HELPER = "pre-analysis closedWorld differs from the retained helper's no-observation result"
FAULT_PROSE = 'section 9.7 does not publish the exact complete pre-analysis closedWorld record'
ROWS = []


def row(case, ok, observed=None):
    ROWS.append({'case': case, 'ok': bool(ok), 'observed': observed})


def run(args):
    p = subprocess.run([PY, '-I', '-B', str(SCR / CHECK)] + args, capture_output=True, text=True, cwd=str(SCR / NAT), timeout=1800)
    rep = None
    if (SCR / REPORT).exists():
        try:
            rep = json.loads((SCR / REPORT).read_text())
        except ValueError:
            rep = None
    return {'exit': p.returncode, 'stdoutTail': p.stdout[-1500:], 'stderrTail': p.stderr[-800:], 'report': rep}


def summary(r):
    rep = r['report'] or {}
    ps = rep.get('providerStartup') or {}
    cases = rep.get('cases') or {}
    return {'exit': r['exit'], 'result': rep.get('result'), 'pinsVerified': (rep.get('pins') or {}).get('verified'), 'providerStartupFaults': ps.get('faults'),
            'casesTotal': cases.get('total'), 'casesFailed': cases.get('failed'), 'failedCaseIds': [c['id'] for c in (cases.get('results') or []) if isinstance(c, dict) and not c.get('passed', True)][:10],
            'stdoutTail': r['stdoutTail'][-600:]}


if SCR.exists():
    raise SystemExit('refusing to reuse scratch copy ' + str(SCR))
shutil.copytree(SRC, SCR)
originals = {p: (SCR / p).read_bytes() for p in (LAW, NE, MODEL, PINS, REPORT)}


def restore():
    for p, b in originals.items():
        (SCR / p).write_bytes(b)


base = run([])
row('scratch-unmutated-checker-passes-positive-reachability', base['exit'] == 0 and FAULT_LAW not in base['stdoutTail'], summary(base))
restore()

law_text = originals[LAW].decode('utf-8')
i = law_text.index('"hostConversionClosedWorld"')
j = law_text.index('"no-manifest"', i)
variants = {
    'law-member': (LAW, (law_text[:j] + '"manifest-not-observed"' + law_text[j + len('"no-manifest"'):]).encode('utf-8'), FAULT_LAW),
}
ne_text = originals[NE].decode('utf-8')
s = ne_text.index('### 9.7')
k = ne_text.index('"no-manifest"', s)
variants['section-9.7-record'] = (NE, (ne_text[:k] + '"manifest-not-observed"' + ne_text[k + len('"no-manifest"'):]).encode('utf-8'), FAULT_PROSE)
model_text = originals[MODEL].decode('utf-8')
m = model_text.index('reasons.append("no-manifest")')
variants['retained-helper'] = (MODEL, (model_text[:m] + 'reasons.append("manifest-not-observed")' + model_text[m + len('reasons.append("no-manifest")'):]).encode('utf-8'), FAULT_HELPER)
for name, (path, mutated, fault) in variants.items():
    (SCR / path).write_bytes(mutated)
    regen = subprocess.run([PY, '-I', '-B', str(SCR / CHECK), '--regenerate-pins'], capture_output=True, text=True, cwd=str(SCR / NAT), timeout=600)
    r = run([])
    sm = summary(r)
    faults = sm['providerStartupFaults'] or []
    others = [f for f in (FAULT_LAW, FAULT_PROSE, FAULT_HELPER) if f != fault]
    in_output = lambda text: any(text in str(f) for f in faults) or text in r['stdoutTail']
    row('mutated-%s-refused-with-its-exact-binding-fault' % name,
        r['exit'] != 0 and sm['pinsVerified'] is True and in_output(fault) and not any(in_output(o) for o in others),
        dict(sm, regenerateExit=regen.returncode, expectedFault=fault))
    restore()
final = run([])
row('scratch-restored-checker-passes-again', final['exit'] == 0, summary(final))
restore()
row('scratch-restored-bytes-equal-verified-copy', all(hashlib.sha256((SCR / p).read_bytes()).hexdigest() == hashlib.sha256((SRC / p).read_bytes()).hexdigest() for p in originals))
out = RT / 'receipts/probes/checker-binding45.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'reviewer mutation discriminator on a disposable scratch copy; native checker only; pins regenerated inside scratch so the law checks are reached; not qualification',
                           'rows': ROWS, 'failed': [x for x in ROWS if not x['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(x['case'], x['observed']) for x in ROWS if not x['ok']], 'rows': [(x['case'], x['ok']) for x in ROWS]}, indent=1, default=str)[:9000])
