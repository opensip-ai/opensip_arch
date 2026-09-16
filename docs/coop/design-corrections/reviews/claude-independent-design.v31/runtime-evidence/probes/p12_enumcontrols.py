"""PROBE 12 (v31) — A-4: execute the five native/enumeration root controls and establish that they
are LOAD-BEARING by my own guard-omission mutation in a disposable verified copy.

My v27 advisory A-4 said the internal-root guard was exercised by no reference checker. This
measures whether that gap is now closed, and re-counts the checkers that name the guard.
"""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/enumkit')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
CHK = 'docs/coop/design-corrections/foundation/check-enumeration.v1.py'
ENM = 'docs/coop/design-corrections/foundation/enumeration_model.v1.py'
R = {}


def run(root, label, tag):
    # My first invocation omitted --stdout/--receipt, so stdout was a summary and my JSON parse
    # produced an empty report. The checker writes its receipt to a default scratch path; I direct
    # both the receipt and the hashes into MY tree so nothing is written beside the frozen source.
    p = os.path.join(root, CHK)
    r = subprocess.run([PY, '-I', '-B', p, '--stdout',
                        '--receipt', os.path.join(OUT, 'enum-%s.receipt.json' % tag),
                        '--hashes', os.path.join(OUT, 'enum-%s.hashes.json' % tag)],
                       capture_output=True, text=True, cwd=os.path.dirname(p), timeout=3600)
    o = {'returncode': r.returncode, 'stderrTail': (r.stderr or '')[-500:]}
    try:
        rep = json.loads(r.stdout)
        o['reportTopKeys'] = sorted(rep) if isinstance(rep, dict) else '<list>'
        o['report'] = rep
    except Exception:
        o['stdoutTail'] = (r.stdout or '')[-600:]
    print('\n=== %s : rc=%d ===' % (label, r.returncode))
    return o, r


o, r = run(SRC, 'check-enumeration.v1.py on FROZEN31', 'frozen')
R['frozen'] = {k: v for k, v in o.items() if k != 'report'}
rep = o.get('report') or {}
R['frozenReportKeys'] = sorted(rep) if isinstance(rep, dict) else None
print('report keys:', R['frozenReportKeys'])
# locate the unit-root cases block
def find_rootcases(x, path=''):
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and 'nativeResult' in v[0]:
                out.append((path + '/' + k, v))
            out += find_rootcases(v, path + '/' + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out += find_rootcases(v, path + '/%d' % i)
    return out


blocks = find_rootcases(rep)
R['rootCaseBlockPaths'] = [b[0] for b in blocks]
cases = blocks[0][1] if blocks else []
R['unitRootCases'] = cases
print('\nunit-root control cases (%d) at %s:' % (len(cases), R['rootCaseBlockPaths']))
for c in cases:
    print('   %-20s expected=%-7s native=%-7s enum=%-7s refusals=%-38s passed=%s'
          % (c.get('case'), c.get('expected'), c.get('nativeResult'), c.get('enumerationResult'),
             json.dumps(c.get('refusals')), c.get('passed')))
    if c.get('nativeRefusal'):
        print('        nativeRefusal: %s' % str(c['nativeRefusal'])[:130])
R['allFiveCasesPassed'] = len(cases) == 5 and all(c.get('passed') for c in cases)
R['positiveEmptyRootAdmitted'] = any(c.get('case') == 'project-empty' and c.get('expected') == 'ADMIT'
                                     and c.get('passed') for c in cases)
R['negativesRefuseOnlyTheRootFault'] = all(
    c.get('refusals') == ['ENUMERATION_MEMBERSHIP_UNIT_ROOT']
    for c in cases if c.get('expected') == 'REFUSE')
print('\nall five passed: %s | positive admitted: %s | negatives refuse ONLY the root fault: %s'
      % (R['allFiveCasesPassed'], R['positiveEmptyRootAdmitted'], R['negativesRefuseOnlyTheRootFault']))

# ---- my own guard-omission mutation ----
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or rel.startswith('docs/coop/design-corrections/reviews/'):
        continue
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
        verified += 1
R['disposableCopied'], R['disposableVerified'] = copied, verified
assert copied == verified
txt = open(os.path.join(KIT, ENM), encoding='utf-8').read()
CALL = "    if not _admit_membership_unit_roots(membership, faults):\n"
R['guardCallPresentInFrozen'] = CALL in txt
assert R['guardCallPresentInFrozen'], 'guard call site not found verbatim; not guessing'
mut = txt.replace(CALL, "    if False:\n", 1)
open(os.path.join(KIT, ENM), 'w', encoding='utf-8').write(mut)
R['mutation'] = 'disabled the _admit_membership_unit_roots call in enumeration_model.v1.py'
o2, r2 = run(KIT, 'with the root guard OMITTED', 'guardomitted')
R['mutated'] = {k: v for k, v in o2.items() if k != 'report'}
rep2 = o2.get('report') or {}
b2 = find_rootcases(rep2)
cases2 = b2[0][1] if b2 else []
R['mutatedUnitRootCases'] = cases2
print('\nwith the guard omitted:')
for c in cases2:
    print('   %-20s expected=%-7s enum=%-7s refusals=%-38s passed=%s'
          % (c.get('case'), c.get('expected'), c.get('enumerationResult'),
             json.dumps(c.get('refusals')), c.get('passed')))
negs = [c for c in cases2 if c.get('expected') == 'REFUSE']
R['allFourNegativesFailWithoutGuard'] = len(negs) == 4 and all(not c.get('passed') for c in negs)
R['positiveStillPassesWithoutGuard'] = any(c.get('case') == 'project-empty' and c.get('passed')
                                           for c in cases2)
print('\nall four negatives fail without the guard : %s' % R['allFourNegativesFailWithoutGuard'])
print('positive still passes without the guard   : %s' % R['positiveStillPassesWithoutGuard'])

# ---- re-count checkers naming the guard (my v27 A-4 measured 0 of 27) ----
checkers = []
F = os.path.join(SRC, 'docs/coop/design-corrections')
for dp, dn, fn in os.walk(F):
    if '/reviews/' in dp or '__pycache__' in dp:
        continue
    for n in fn:
        if n.startswith('check') and n.endswith('.py'):
            checkers.append(os.path.join(dp, n))
hits = {}
for tok in ('NATIVE_UNIT_ROOT_REPRESENTATION', 'ENUMERATION_MEMBERSHIP_UNIT_ROOT',
            'admit_unit_roots', 'InternalUnitRootV1'):
    hits[tok] = [os.path.relpath(c, SRC) for c in checkers
                 if tok in open(c, encoding='utf-8', errors='replace').read()]
R['checkerCount'] = len(checkers)
R['checkerHits'] = hits
print('\nreference checkers: %d' % len(checkers))
for t, h in hits.items():
    print('   %-34s %d checker(s): %s' % (t, len(h), [os.path.basename(x) for x in h]))
R['a4GapClosed'] = all(len(h) >= 1 for h in hits.values())

dev = sum(1 for rel, f in man.items()
          if not os.path.isfile(os.path.join(SRC, rel))
          or hashlib.sha256(open(os.path.join(SRC, rel), 'rb').read()).hexdigest() != f['sha256'])
R['frozenDeviationsAfterProbe'] = dev
print('\nfrozen deviations:', dev)
json.dump(R, open(os.path.join(OUT, 'p12-enumcontrols.json'), 'w'), indent=1, default=str)
print('wrote p12-enumcontrols.json')
