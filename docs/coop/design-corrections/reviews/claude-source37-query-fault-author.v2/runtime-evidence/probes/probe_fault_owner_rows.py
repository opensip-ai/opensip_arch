"""Row-isolated replica of check-evaluator-faults.v3.py main() lines 10-61 over one tree's actual owner model.

usage: python -I -B probe_fault_owner_rows.py TREE   (source37-frozen | source37-pristine | source37-coauthor)
The maintained checker aborts at its first unexpected exception, so later rows (owner carriers, replay reference,
output bound) never execute. This probe runs the same row bodies with the same expectations, each isolated, and
records the actual outcome. It is not the maintained checker and does not relabel that checker's exit status.
"""
import copy, hashlib, importlib.util, json, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
TREE = sys.argv[1]
F = RT + '/work/' + TREE + '/docs/coop/design-corrections/foundation'
s = importlib.util.spec_from_file_location('fault3', F + '/evaluator_fault_model.v3.py')
M = importlib.util.module_from_spec(s)
s.loader.exec_module(M)
raw = b'{"owner":"synthetic-boundary-control","decisions":["original"]}'
rows = []


def obs(condition, origin):
    return {'schemaVersion': 3, 'condition': condition, 'origin': origin,
            'diagnosticDigest': hashlib.sha256(raw).hexdigest(), 'reference': 'retained:fixture',
            'limit': ({'field': 'selectedPrograms', 'observed': 65, 'maximum': 64} if condition == 'selection-limit-exceeded' else
                      {'field': 'proof.predicates', 'observed': 100001, 'maximum': 100000} if condition == 'output-bound-exceeded' else None)}


def admit(case, fn):
    try:
        detail = fn()
        rows.append({'case': case, 'expected': 'ADMIT', 'actual': 'ADMIT', 'asExpected': True, 'detail': detail})
    except Exception as exc:
        rows.append({'case': case, 'expected': 'ADMIT', 'actual': type(exc).__name__, 'asExpected': False,
                     'message': str(exc).splitlines()[0][:300]})


def refuses(case, fn, expected):
    try:
        fn()
        rows.append({'case': case, 'expected': 'REFUSE:' + expected, 'actual': 'ADMIT', 'asExpected': False})
    except Exception as exc:
        text = str(exc)
        rows.append({'case': case, 'expected': 'REFUSE:' + expected, 'actual': 'REFUSE:' + type(exc).__name__,
                     'expectedKeyInMessage': expected in text, 'asExpected': expected in text,
                     'message': text.splitlines()[0][:300]})


def totality():
    pairs = [b['properties']['condition']['const'] + ':' + b['properties']['origin']['const'] for b in M.SCHEMA['allOf'][-1]['anyOf']]
    assert len(pairs) == len(set(pairs)) and set(pairs) == set(M.ROUTES)
    return len(pairs)


admit('schema-and-route-pair-totality', totality)
for key in M.ROUTES:
    def one(key=key):
        condition, origin = key.split(':')
        o = obs(condition, origin)
        r = M.route(o, raw)
        e = M.failure_envelope(o, raw, 'req1_' + '1' * 32)
        assert r['diagnosticBytes'] == raw and r['observation'] == o
        assert e['termination'] == r['termination'] and e['exitCode'] == r['exitCode']
        return {'class': r['termination']['class'], 'errorCode': r['termination']['errorCode'],
                'faultCause': r['termination'].get('faultCause'), 'detail': r['termination']['domainDetail']['code'],
                'remedy': r['termination']['domainDetail']['remedy'], 'exitCode': r['exitCode']}
    admit(key, one)
refuses('unknown-origin-pair', lambda: M.C.validate(M.SCHEMA, obs('promised-bytes-lost', 'provider-return')), 'is not valid under any of the given schemas')
refuses('invalid-bytes-are-not-loss', lambda: M.C.validate(M.SCHEMA, obs('input-identity-invalid', 'evidence-store')), 'is not valid under any of the given schemas')
refuses('diagnostic-custody-mismatch', lambda: M.route(obs('input-join-invalid', 'provider-return'), raw + b'!'), 'EVALUATOR_FAULT_DIAGNOSTIC_CUSTODY')
bad = obs('selection-limit-exceeded', 'host-pre-plan')
bad['limit']['observed'] = 64
refuses('within-bound-is-not-fault', lambda: M.route(bad, raw), 'EVALUATOR_FAULT_NOT_OVER_LIMIT')
o = obs('required-output-pointer-omitted', 'provider-return')
r = M.route(o, raw)
e = M.failure_envelope(o, raw, 'req1_' + '2' * 32)
for name, mutate in [('exit', lambda x: x.update(exitCode=2)), ('public-detail', lambda x: x['errors'][0].update(code='evidence.missing')),
                     ('termination-origin', lambda x: x['termination'].update(errorCode='HOST.IO_FAILURE'))]:
    bad = copy.deepcopy(e)
    mutate(bad)
    refuses('envelope-' + name, lambda bad=bad: M.validate_envelope(bad, r), 'EVALUATOR_FAULT_ENVELOPE_PARITY')
I = M.load('fault_owner_identity3', F + '/identity-model.v3.py')
for condition, origin, exc in [('promised-bytes-lost', 'evidence-store', I.EvidenceUnavailable('retained:fixture')),
                               ('complete-replay-mismatch', 'retained-regeneration', I.RegenerationMismatch('retained:fixture'))]:
    def carrier(condition=condition, origin=origin, exc=exc):
        ob = M.owner_observation(exc, raw)
        assert (ob['condition'], ob['origin']) == (condition, origin)
        actual = M.route(ob, raw)['termination']
        assert M.C.equal_typed(actual, exc.termination)
        return actual
    admit('owner-carrier-' + condition, carrier)
for origin in ['retained-regeneration', 'host-internal']:
    bad = obs('complete-replay-mismatch', origin)
    bad['reference'] = None
    refuses('replay-reference-required-' + origin, lambda bad=bad: M.C.validate(M.SCHEMA, bad), "is not of type 'string'")
bad = obs('output-bound-exceeded', 'host-serialization')
bad['limit'] = None
refuses('output-bound-measurement-required', lambda: M.C.validate(M.SCHEMA, bad), "is not of type 'object'")
bad2 = obs('output-bound-exceeded', 'host-serialization')
bad2['limit']['observed'] = 100000
refuses('output-within-bound-is-not-fault', lambda: M.route(bad2, raw), 'EVALUATOR_FAULT_NOT_OVER_LIMIT')
exc = I.RegenerationMismatch('retained:fixture')
exc.termination['domainDetail']['remedy'] = 'invented remedy'
refuses('owner-carrier-remedy-mismatch', lambda: M.owner_observation(exc, raw), 'EVALUATOR_FAULT_OWNER_CARRIER')
has_mismatch = hasattr(I, 'CompleteReplayMismatch')
admit('identity-complete-replay-mismatch-has-no-termination-carrier',
      lambda: {'present': has_mismatch, 'termination': getattr(I.CompleteReplayMismatch('x'), 'termination', None) if has_mismatch else None})
if has_mismatch:
    refuses('condition-only-mismatch-is-not-an-owner-carrier', lambda: M.owner_observation(I.CompleteReplayMismatch('EVALUATOR_COMPLETE_PROOF_REPLAY'), raw), 'EVALUATOR_FAULT_OWNER_CARRIER')
report = {'tree': TREE, 'standing': 'row-isolated replica probe; not the maintained checker', 'count': len(rows),
          'notAsExpected': [x['case'] for x in rows if not x['asExpected']], 'rows': rows}
json.dump(report, open(RT + '/receipts/probe-fault-owner-rows.' + TREE + '.json', 'w'), indent=1)
print(json.dumps({'tree': TREE, 'count': len(rows), 'notAsExpected': report['notAsExpected'],
                  'routes': {x['case']: x.get('detail') for x in rows if ':' in x['case'] and x['asExpected']}}, indent=1))
