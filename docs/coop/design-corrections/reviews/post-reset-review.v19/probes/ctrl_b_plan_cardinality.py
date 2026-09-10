"""Independent controls for CB7-SHOULD-2: prospective Plan bounded-selection refusal.

Authored fresh for post-reset-review.v19. Runs against the DISPOSABLE COPY only.
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC = ROOT / 'docs/coop/design-corrections'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

N = load('nem', DC / 'native/native_evidence_model.v2.py')
IM = load('idm', DC / 'foundation/identity-model.py')
W = load('wfm', DC / 'workflows/workflows_model.v1.py')

PLAN_DEFS = IM.SCHEMA['$defs']['plan']['properties']
FIELDS = ('semanticClosures', 'nativeContextDigests', 'importIds')
LIMIT = {f: PLAN_DEFS[f]['maxItems'] for f in FIELDS}

R = []
def ck(cid, desc, got, want):
    R.append({'id': cid, 'desc': desc, 'pass': got == want, 'observed': got, 'expected': want})

def ids(n, prefix=''):
    return [prefix + ('%064x' % i) for i in range(n)]

def refuse(mapping):
    """Return the ScopeRefusal subject, or the pass-through value."""
    try:
        return {'passed': N.admit_plan_selection_cardinality(mapping)}
    except N.ScopeRefusal as e:
        return {'refused': dict(e.subject), 'detail': e.detail, 'd9': e.d9}

# --- B0 the bounds and the order are READ, not restated ---------------------
ck('B0:limits', 'published Plan bounds are 128/128/256',
   [LIMIT[f] for f in FIELDS], [128, 128, 256])
ck('B0:bound-fn', 'plan_selection_bound reads the schema',
   [N.plan_selection_bound(f) for f in FIELDS], [128, 128, 256])
ck('B0:decl-order', 'PLAN_SELECTION_FIELDS is the $defs/plan declaration order',
   list(N.PLAN_SELECTION_FIELDS),
   [k for k in PLAN_DEFS if k in FIELDS])
ck('B0:remedies-distinct', 'each field carries its OWN remedy sentence',
   len({N.SCOPE_LIMIT_REMEDY[f] for f in FIELDS}), 3)

# --- B1 within-bound positives (at the limit exactly) ----------------------
for f in FIELDS:
    got = refuse({f: ids(LIMIT[f])})
    ck('B1:at-limit:' + f, 'exactly at the bound is admitted', 'passed' in got, True)
    got = refuse({f: ids(LIMIT[f] - 1)})
    ck('B1:under:' + f, 'below the bound is admitted', 'passed' in got, True)
    ck('B1:empty:' + f, 'empty array is admitted', 'passed' in refuse({f: []}), True)

# --- B2 first failing boundary: limit+1, exact typed refusal ---------------
for f in FIELDS:
    n = LIMIT[f] + 1
    got = refuse({f: ids(n)})
    ck('B2:subject:' + f, 'limit+1 refuses with exact field/count/limit',
       got.get('refused'), {'field': f, 'count': n, 'limit': LIMIT[f]})
    ck('B2:detail:' + f, 'detail is PROJECT.SCOPE_LIMIT', got.get('detail'), 'PROJECT.SCOPE_LIMIT')
    ck('B2:d9:' + f, 'd9 route is request-rejected / REQUEST.UNSATISFIABLE / exit 2',
       [got['d9']['class'], got['d9']['code'], got['d9']['exitCode']],
       ['request-rejected', 'REQUEST.UNSATISFIABLE', 2])

# --- B3 the bounded public projection, end to end through the workflow seam -
for f in FIELDS:
    n = LIMIT[f] + 1
    try:
        N.admit_plan_selection_cardinality({f: ids(n)})
        ck('B3:' + f, 'expected refusal', 'none', 'ScopeRefusal')
    except N.ScopeRefusal as e:
        t = N.scope_refusal_termination(e)
        ck('B3:subject:' + f, 'termination subject is field:count>limit',
           t['domainDetail']['subject'], '%s:%d>%d' % (f, n, LIMIT[f]))
        ck('B3:remedy:' + f, 'termination carries THIS field remedy',
           t['domainDetail']['remedy'], N.SCOPE_LIMIT_REMEDY[f])
        ck('B3:exit:' + f, 'workflow envelope preserves class/code/exit',
           [t['class'], t['errorCode'], W.exit_code(t)],
           ['request-rejected', 'REQUEST.UNSATISFIABLE', 2])
        ck('B3:remedy-nonempty:' + f, 'remedy names this field surface',
           len(t['domainDetail']['remedy']) > 20, True)

# --- B4 ARRAY-ONLY cardinality: every other shape belongs to the schema ----
for shape, label in [('x' * 500, 'string-longer-than-limit'), ({str(i): 1 for i in range(500)}, 'dict-500-keys'),
                     (None, 'null'), (True, 'bool'), (999, 'int'), (1.5, 'float'),
                     (tuple(ids(300)), 'tuple-not-list')]:
    got = refuse({'importIds': shape})
    ck('B4:passthrough:' + label, 'non-array shape passes to the schema untouched',
       'passed' in got and got['passed']['importIds'] is shape, True)
ck('B4:missing', 'a missing field is not a cardinality breach', 'passed' in refuse({}), True)
ck('B4:identity', 'admitted mapping is returned unchanged (same object)',
   (lambda m: N.admit_plan_selection_cardinality(m) is m)({'importIds': ids(3)}), True)
ck('B4:wrong-elems-in-bound', 'in-bound array of wrong element types is the schema\'s',
   'passed' in refuse({'importIds': [1, 2, 3]}), True)
ck('B4:wrong-elems-over-bound', 'OVER-bound array refuses on cardinality regardless of element type',
   refuse({'importIds': list(range(LIMIT['importIds'] + 1))}).get('refused'),
   {'field': 'importIds', 'count': LIMIT['importIds'] + 1, 'limit': LIMIT['importIds']})
ck('B4:not-a-dict', 'a non-mapping is passed through', N.admit_plan_selection_cardinality(None), None)

# --- B5 multi-field precedence is the fixed declaration order --------------
over = {f: ids(LIMIT[f] + 1) for f in FIELDS}
ck('B5:all-three', 'all three oversized -> first declared field is the subject',
   refuse(dict(over)).get('refused', {}).get('field'), 'semanticClosures')
ck('B5:two-late', 'closures in bound -> nativeContextDigests is the subject',
   refuse({'semanticClosures': ids(LIMIT['semanticClosures']),
           'nativeContextDigests': ids(LIMIT['nativeContextDigests'] + 1),
           'importIds': ids(LIMIT['importIds'] + 1)}).get('refused', {}).get('field'),
   'nativeContextDigests')
ck('B5:insertion-order-irrelevant', 'python insertion order does not change the subject',
   refuse({'importIds': ids(LIMIT['importIds'] + 1),
           'nativeContextDigests': ids(LIMIT['nativeContextDigests'] + 1),
           'semanticClosures': ids(LIMIT['semanticClosures'] + 1)}).get('refused', {}).get('field'),
   'semanticClosures')
ck('B5:wrong-type-does-not-shadow', 'an earlier field of the WRONG TYPE does not mask a later breach',
   refuse({'semanticClosures': 'not-an-array',
           'nativeContextDigests': ids(LIMIT['nativeContextDigests'] + 1)}).get('refused', {}).get('field'),
   'nativeContextDigests')
ck('B5:deterministic', 'same request always yields the same subject',
   len({json.dumps(refuse(dict(over)).get('refused'), sort_keys=True) for _ in range(5)}), 1)

# --- B6 the PRODUCER boundary refuses before any Plan exists ---------------
def admission(digest):
    return {'refusals': [], 'planNativeContextDigest': digest}
try:
    N.plan_native_context_digests([admission('%064x' % i) for i in range(LIMIT['nativeContextDigests'] + 1)])
    ck('B6:producer', 'producer boundary refuses 129 distinct contexts', 'admitted', 'ScopeRefusal')
except N.ScopeRefusal as e:
    ck('B6:producer', 'producer boundary refuses 129 distinct contexts',
       dict(e.subject), {'field': 'nativeContextDigests', 'count': 129, 'limit': 128})
ck('B6:producer-at-limit', 'producer admits exactly 128 distinct contexts',
   len(N.plan_native_context_digests([admission('%064x' % i) for i in range(LIMIT['nativeContextDigests'])])), 128)
ck('B6:producer-dedup', '129 IDENTICAL descriptors collapse and are admitted',
   len(N.plan_native_context_digests([admission('%064x' % 7) for _ in range(129)])), 1)

# --- B7 a RETAINED oversized Plan is corruption, on the SCHEMA route -------
retained = {'schemaVersion': '2', 'importIds': ids(LIMIT['importIds'] + 1, 'import2:')}
try:
    IM.C.validate(IM.SCHEMA['$defs']['plan'], retained)
    ck('B7:schema-route', 'retained oversized Plan refuses', 'admitted', 'schema-error')
except N.ScopeRefusal:
    ck('B7:schema-route', 'retained oversized Plan must NOT take the request-scope route',
       'ScopeRefusal', 'schema-error')
except Exception as e:
    ck('B7:schema-route', 'retained oversized Plan refuses on the SCHEMA route (not ScopeRefusal)',
       not isinstance(e, N.ScopeRefusal), True)
src = (DC / 'foundation/identity-model.py').read_text()
ck('B7:not-in-closure', 'the pre-Plan boundary is NOT called from retained Run closure',
   'admit_plan_selection_cardinality' in src, False)

fails = [r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-b.json').write_text(
    json.dumps({'controls': len(R), 'failed': len(fails), 'failures': fails, 'results': R}, indent=1))
print('CTRL-B controls=%d failed=%d' % (len(R), len(fails)))
for f in fails:
    print('  FAIL', f['id'], f['desc'], '\n    observed=', repr(f['observed'])[:300], '\n    expected=', repr(f['expected'])[:300])
