"""PROBE M1-B (v27) — EXECUTE the real boundaries, which my v26 probe did not.

My v26 pB2 read/imported source (inspect.getsource) and validated constructed instances
against the schemas. It never executed buffer_fact_batch_occupancy,
bind_worker_occupancy, capture_occupancy or the atom sidecar admission. This probe does,
on the corrected v27 bytes, and derives the resulting PUBLIC route rather than assuming it.

I test cells the author's added cases do NOT cover as well:
  - buffer_fact_batch_occupancy (the ANALYZING entry), for both refusing and lawful cases
  - capture_occupancy
  - the public route actually derived from each internal key
  - kind=unknown with occupancy=first-party (must already refuse on evaluationNativeId)
  - atomicity: a refused batch captures nothing
"""
import importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v27/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


K = load('prov_check', os.path.join(DC, 'foundation/check-provider-attribution-return.v2.py'))
M, AM = K.M, K.AM
R = {'evidenceClass': 'BOUNDARY EXECUTION (not source reading, not schema-only validation)'}
rows = []


def run(label, fn):
    try:
        v = fn()
        rows.append({'case': label, 'outcome': 'ADMIT', 'detail': v})
    except M.ProviderReturnAdmissionError as e:
        rows.append({'case': label, 'outcome': 'REFUSE', 'boundary': 'provider-return',
                     'internalKey': e.key, 'detail': str(getattr(e, 'detail', ''))[:90]})
    except AM.AtomAdmissionError as e:
        rows.append({'case': label, 'outcome': 'REFUSE', 'boundary': 'atom-admission',
                     'internalKey': e.key, 'detail': ''})
    except Exception as e:
        rows.append({'case': label, 'outcome': 'ERROR', 'internalKey': type(e).__name__,
                     'detail': str(e)[:140]})


RESOLVED = 'mod:opaque-thing'


def mk(kind, occ, logical, ordinal=0):
    exported = 'unknown' if kind == 'symbol' else None
    return K.companion(ordinal, resolved=RESOLVED, kind=kind, occupancy=occ,
                       logical=logical, exported=exported)


def bnd(kind, occ, logical):
    fid = K.fact2('1')
    b = K.batch([K.candidate(0, RESOLVED)], [mk(kind, occ, logical)])
    return b, K.owners(fid, resolved=RESOLVED), fid


# ---- 1. bind_worker_occupancy (post-terminal capture) ----
for kind in ('unknown', 'file', 'symbol', 'package'):
    for occ in ('external', 'unknown', 'first-party'):
        for lab, lp in (('null', None), ('path', 'src/hint.ts')):
            def f(kind=kind, occ=occ, lp=lp):
                b, o, _ = bnd(kind, occ, lp)
                out = M.bind_worker_occupancy(b, **o)
                return {'status': out['status'],
                        'logicalPath': (out['records'][0]['logicalPath'] if out['records'] else None),
                        'refs': len(out['hostDerivedRefs'])}
            run('bind %-7s/%-11s hint=%-4s' % (kind, occ, lab), f)

# ---- 2. buffer_fact_batch_occupancy (the ANALYZING entry the author did not cover here) ----
for kind, occ, lab, lp in (('unknown', 'external', 'path', 'src/hint.ts'),
                           ('unknown', 'unknown', 'path', 'src/hint.ts'),
                           ('unknown', 'external', 'null', None),
                           ('file', 'external', 'path', 'src/hint.ts')):
    def g(kind=kind, occ=occ, lp=lp):
        b, o, _ = bnd(kind, occ, lp)
        kw = {k: v for k, v in o.items()
              if k in ('negotiated_tokens', 'plan_id', 'execution_plan', 'stage_specs',
                       'closures', 'dispatch')}
        out = M.buffer_fact_batch_occupancy(b, **kw)
        return {'status': out.get('status'), 'buffered': len(out.get('companions', out.get('records', [])))}
    run('buffer %-7s/%-11s hint=%-4s' % (kind, occ, lab), g)

# ---- 3. capture_occupancy ----
for kind, occ, lab, lp in (('unknown', 'external', 'path', 'src/hint.ts'),
                           ('unknown', 'external', 'null', None)):
    def h(kind=kind, occ=occ, lp=lp):
        b, o, _ = bnd(kind, occ, lp)
        out = M.capture_occupancy(b, **o)
        return {'status': out['status'], 'refs': len(out['hostDerivedRefs'])}
    run('capture %-7s/%-11s hint=%-4s' % (kind, occ, lab), h)

# ---- 4. retained atom admission of a projected record ----
for kind, occ, lab, lp in (('unknown', 'external', 'path', 'src/hint.ts'),
                           ('unknown', 'unknown', 'path', 'src/hint.ts'),
                           ('unknown', 'external', 'null', None),
                           ('file', 'external', 'path', 'src/hint.ts')):
    def a(kind=kind, occ=occ, lp=lp):
        fid = K.fact2('1')
        args = K.owners(fid, resolved=RESOLVED)
        comp = mk(kind, occ, lp)
        fact = args['minted_by_ordinal'][0]
        rec = M.project_companion_to_v2(comp, fact, K.PLAN, K.C_PROV)
        inputs = {'planId': K.PLAN, 'facts': {fid: fact}, 'closures': args['closures'],
                  'inventories': args['inventories'],
                  'enumerationPlan': args['enumeration_plan'],
                  'targetAttributions': {fid: rec}}
        AM._admit_target_attributions(inputs)
        return {'admittedLogicalPath': rec['logicalPath']}
    run('atom   %-7s/%-11s hint=%-4s' % (kind, occ, lab), a)

R['rows'] = rows
for r in rows:
    print('%-34s %-7s %-28s %s' % (r['case'], r['outcome'], r.get('internalKey', ''),
                                   json.dumps(r.get('detail'))[:70]))

# ---- 5. derive the PUBLIC route from each observed internal key ----
keys = sorted({r['internalKey'] for r in rows if r['outcome'] == 'REFUSE'})
routes = {}
for k in keys:
    try:
        cond = M.condition_for_key(k)
        obs = M.public_observation(k, 'provider-return')
        routes[k] = {'condition': cond, 'publicObservation': obs}
    except Exception as e:
        routes[k] = {'error': type(e).__name__ + ': ' + str(e)[:120]}
R['observedRefusalKeys'] = keys
R['publicRoutes'] = routes
print('\nobserved refusal keys:', keys)
print('public routes:', json.dumps(routes, indent=1)[:1800])

json.dump(R, open(os.path.join(OUT, 'pM1-boundaries.json'), 'w'), indent=1)
