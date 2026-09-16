"""PROBE M1-C (v27) — corrected re-run of the two calls my first boundary probe
(pM1_boundaries.py) invoked with wrong signatures: buffer_fact_batch_occupancy and
public_observation. The first run's TypeErrors were MY probe defects, not design faults,
and are preserved in receipts/pM1-boundaries.json.

Here I (a) drive the real ANALYZING entry with its actual two keyword arguments, and
(b) derive the real PUBLIC termination for every internal key I observed, end to end.
"""
import importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v27/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


K = load('prov_check2', os.path.join(DC, 'foundation/check-provider-attribution-return.v2.py'))
M, AM = K.M, K.AM
R = {'note': 'corrects two probe-side signature errors in pM1_boundaries.py; those are '
             'preserved as probe defects, not design findings'}
RESOLVED = 'mod:opaque-thing'
rows = []


def mk(kind, occ, logical):
    return K.companion(0, resolved=RESOLVED, kind=kind, occupancy=occ, logical=logical,
                       exported='unknown' if kind == 'symbol' else None)


# ---- (a) the ANALYZING entry, with its real signature ----
for kind, occ, lab, lp in (('unknown', 'external', 'path', 'src/hint.ts'),
                           ('unknown', 'unknown', 'path', 'src/hint.ts'),
                           ('unknown', 'external', 'null', None),
                           ('file', 'external', 'path', 'src/hint.ts'),
                           ('symbol', 'unknown', 'path', 'src/hint.ts')):
    fid = K.fact2('1')
    o = K.owners(fid, resolved=RESOLVED)
    b = K.batch([K.candidate(0, RESOLVED)], [mk(kind, occ, lp)])
    try:
        out = M.buffer_fact_batch_occupancy(
            b, negotiated_tokens=o['negotiated_tokens'], dispatch=o['dispatch'])
        rows.append({'entry': 'buffer_fact_batch_occupancy',
                     'case': '%s/%s hint=%s' % (kind, occ, lab),
                     'outcome': 'ADMIT', 'status': out.get('status'),
                     'phase': out.get('phase')})
    except M.ProviderReturnAdmissionError as e:
        rows.append({'entry': 'buffer_fact_batch_occupancy',
                     'case': '%s/%s hint=%s' % (kind, occ, lab),
                     'outcome': 'REFUSE', 'internalKey': e.key})

for r in rows:
    print('%-30s %-26s %-7s %s' % (r['entry'], r['case'], r['outcome'],
                                   r.get('internalKey') or r.get('status')))

# ---- (b) real public termination for each observed internal key ----
print()
routes = {}
for key in ('PROVIDER_RETURN_SCHEMA', 'TARGET_ATTRIBUTION_SCHEMA',
            'TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY',
            'TARGET_ATTRIBUTION_LOGICAL_PATH_ON_PACKAGE'):
    diag = ('{"internalKey":"%s","detail":"logicalPath"}' % key).encode()
    try:
        cond = M.condition_for_key(key)
        routed = M.route_internal_key(key, 'provider-return', diag)
        term = routed['termination']
        routes[key] = {'condition': cond, 'class': term.get('class'),
                       'errorCode': term.get('errorCode'),
                       'faultCause': term.get('faultCause'),
                       'domainDetail': (term.get('domainDetail') or {}).get('code'),
                       'exitCode': term.get('exitCode')}
    except Exception as e:
        routes[key] = {'error': type(e).__name__ + ': ' + str(e)[:120]}
    print('%-48s %s' % (key, json.dumps(routes[key])))

try:
    diag = b'{"internalKey":"PROVIDER_RETURN_HOST_AUTHORED"}'
    routed = M.route_internal_key('PROVIDER_RETURN_HOST_AUTHORED', 'host-internal', diag)
    routes['host-internal/PROVIDER_RETURN_HOST_AUTHORED'] = {
        'class': routed['termination'].get('class'),
        'errorCode': routed['termination'].get('errorCode'),
        'faultCause': routed['termination'].get('faultCause'),
        'domainDetail': (routed['termination'].get('domainDetail') or {}).get('code')}
except Exception as e:
    routes['host-internal/PROVIDER_RETURN_HOST_AUTHORED'] = {'error': str(e)[:140]}
print('%-48s %s' % ('host-internal origin',
                    json.dumps(routes['host-internal/PROVIDER_RETURN_HOST_AUTHORED'])))

R['bufferRows'] = rows
R['publicRoutes'] = routes
R['distinctPublicDetailCodes'] = sorted(
    {v.get('domainDetail') for v in routes.values() if isinstance(v, dict) and v.get('domainDetail')})
json.dump(R, open(os.path.join(OUT, 'pM1-routes.json'), 'w'), indent=1)
print('\ndistinct public detail codes used:', R['distinctPublicDetailCodes'])
