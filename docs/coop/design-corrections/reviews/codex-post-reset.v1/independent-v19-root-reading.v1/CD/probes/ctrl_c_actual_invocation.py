"""Independent ACTUAL-INVOCATION controls: refused-step mints no Plan/Run; earlier outcomes
preserved; within-bound positives still close a Run. Disposable copy only."""
import hashlib, json, sys, types
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
CI = ROOT / 'docs/coop/design-corrections/foundation/check-identity.py'

# Execute the OWNING checker's real namespace (its own 1431 checks run as a side effect),
# then drive its real `build` fixture invocation with our own selections.
ns = {'__name__': '__ctrl_c__', '__file__': str(CI)}
sys.argv = ['check-identity.py']
import os
os.chdir(ROOT)
try:
    exec(compile(CI.read_text(), str(CI), 'exec'), ns)
except SystemExit as e:
    ns['_exit'] = e.code

R = []
def ck(cid, desc, got, want):
    R.append({'id': cid, 'desc': desc, 'pass': got == want, 'observed': got, 'expected': want})

build, N, C = ns['build'], ns['N'], ns['C']
ck('C0:owning-suite', 'owning checker suite exits 0 inside this harness', ns.get('_exit'), False)

def ids(n, prefix):
    return [prefix + ('%064x' % i) for i in range(n)]

def invoke(**kw):
    try:
        run, objects, blobs = build(**kw)
        doms = sorted({objects[k][0] for k in objects})
        return {'closed': True, 'runId': run.get('planId') and 'run-present',
                'planId': run['planId'], 'domains': doms,
                'canonical': hashlib.sha256(C.canonical(run)).hexdigest()}
    except N.ScopeRefusal as e:
        return {'closed': False, 'refused': dict(e.subject), 'detail': e.detail,
                'termination': N.scope_refusal_termination(e)}

# --- C1 BASELINE: an ordinary invocation closes a Run ----------------------
base = invoke()
ck('C1:baseline-closes', 'ordinary invocation closes a Run', base['closed'], True)
ck('C1:baseline-mints-plan', 'baseline mints a plan2 and a run', 'plan' in base['domains'], True)

# --- C2 within-bound positives at the exact published bound ----------------
at_limit = invoke(plan_import_ids=ids(256, 'import2:'))
ck('C2:importIds-256', 'exactly 256 importIds still closes a Run', at_limit['closed'], True)

# --- C3 the first failing boundary: 257 importIds --------------------------
over = invoke(plan_import_ids=ids(257, 'import2:'))
ck('C3:refuses', 'ordinary 257-import selection refuses at actual invocation',
   over['closed'], False)
ck('C3:subject', 'exact bounded subject',
   over.get('refused'), {'field': 'importIds', 'count': 257, 'limit': 256})
ck('C3:route', 'request-rejected / REQUEST.UNSATISFIABLE / exit 2 / PROJECT.SCOPE_LIMIT',
   [over['termination']['class'], over['termination']['errorCode'],
    over['termination']['domainDetail']['code'],
    over['termination']['domainDetail']['subject']],
   ['request-rejected', 'REQUEST.UNSATISFIABLE', 'PROJECT.SCOPE_LIMIT', 'importIds:257>256'])
ck('C3:remedy', 'importIds narrowing remedy is the published one',
   over['termination']['domainDetail']['remedy'], N.SCOPE_LIMIT_REMEDY['importIds'])
ck('C3:no-plan-no-run', 'the refused step returns NO Plan and NO Run',
   ['planId' in over, 'domains' in over], [False, False])

# --- C4 semanticClosures at its own bound ----------------------------------
sc = ns.get('_ctrl_closures')
closures_over = invoke(plan_semantic_closures=ids(129, 'closure2:'))
ck('C4:closures-refuses', 'oversized closure selection refuses',
   closures_over.get('refused'), {'field': 'semanticClosures', 'count': 129, 'limit': 128})

# --- C5 earlier committed outcomes preserved -------------------------------
after = invoke()
ck('C5:preserved', 'an identical invocation after the refusal is byte-identical',
   after.get('canonical'), base.get('canonical'))
ck('C5:plan-identity-stable', 'no Plan identity moved across the refusal',
   after.get('planId'), base.get('planId'))
ck('C5:at-limit-repeatable', 'the at-limit positive is repeatable after a refusal',
   invoke(plan_import_ids=ids(256, 'import2:'))['closed'], True)

# --- C6 a retained OVERSIZED Plan is a schema/corruption route -------------
run, objects, blobs = build()
plan_key = run['planId']
import copy as _copy
corrupt = _copy.deepcopy(objects[plan_key][1])
corrupt['importIds'] = ids(257, 'import2:')
try:
    ns['validate_domain']('plan', corrupt) if 'validate_domain' in ns else C.validate(
        ns['M'].SCHEMA['$defs']['plan'], corrupt)
    ck('C6:retained', 'retained oversized Plan refuses', 'admitted', 'refused')
except N.ScopeRefusal:
    ck('C6:retained', 'retained oversized Plan must NOT take the prospective request route',
       'ScopeRefusal', 'schema-refusal')
except Exception as e:
    ck('C6:retained', 'retained oversized Plan refuses on the schema route, not ScopeRefusal',
       type(e).__name__ != 'ScopeRefusal', True)

fails = [r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-c.json').write_text(
    json.dumps({'controls': len(R), 'failed': len(fails), 'failures': fails, 'results': R}, indent=1))
print('CTRL-C controls=%d failed=%d' % (len(R), len(fails)))
for f in fails:
    print('  FAIL', f['id'], f['desc'], '\n   observed=', repr(f['observed'])[:400],
          '\n   expected=', repr(f['expected'])[:400])
