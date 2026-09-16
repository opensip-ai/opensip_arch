"""QF-I1 correction discrimination probe over one copied tree (production owner model, unmodified).

usage: python -I -B probe_fault_parity.py TREE
Question: does the corrected check-evaluator-faults keep two distinct protections? (a) schema StepTermination pair law
refuses an illegal faultCause/errorCode pair; (b) a structurally LEGAL but wrong pair passes schema admission, so only
evaluator_fault_model owner parity (EVALUATOR_FAULT_ENVELOPE_PARITY) refuses it. Also records validate_envelope order.
"""
import copy, hashlib, importlib.util, inspect, json, sys

RT = '/private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1'
TREE = sys.argv[1]
F = RT + '/work/' + TREE + '/docs/coop/design-corrections/foundation'
s = importlib.util.spec_from_file_location('parity_fault3', F + '/evaluator_fault_model.v3.py')
M = importlib.util.module_from_spec(s)
s.loader.exec_module(M)
raw = b'{"owner":"synthetic-boundary-control","decisions":["original"]}'
obs = {'schemaVersion': 3, 'condition': 'required-output-pointer-omitted', 'origin': 'provider-return',
       'diagnosticDigest': hashlib.sha256(raw).hexdigest(), 'reference': 'retained:fixture', 'limit': None}
r = M.route(obs, raw)
e = M.failure_envelope(obs, raw, 'req1_' + '2' * 32)
ENV = 'urn:opensip:product-v1:workflows:evaluator3:command-envelope:3'
res = {'tree': TREE}


def attempt(fn):
    try:
        fn()
        return {'result': 'ADMIT'}
    except M.C.ValidationError as exc:
        return {'result': 'REFUSE', 'type': 'ValidationError', 'validator': exc.validator, 'absolutePath': list(exc.absolute_path)}
    except Exception as exc:
        return {'result': 'REFUSE', 'type': type(exc).__name__, 'message': str(exc).splitlines()[0][:160]}


cases = {
    'illegal-pair(provider-protocol,HOST.IO_FAILURE)': lambda x: x['termination'].update(errorCode='HOST.IO_FAILURE'),
    'legal-wrong-pair(host-io,HOST.IO_FAILURE)': lambda x: x['termination'].update(errorCode='HOST.IO_FAILURE', faultCause='host-io'),
    'exit-mismatch': lambda x: x.update(exitCode=2),
    'public-detail-mismatch': lambda x: x['errors'][0].update(code='evidence.missing'),
}
for name, mutate in cases.items():
    bad = copy.deepcopy(e)
    mutate(bad)
    res[name] = {'schemaOnly(P.validate_profile)': attempt(lambda: M.P.validate_profile(ENV, bad)),
                 'ownerValidateEnvelope': attempt(lambda: M.validate_envelope(bad, r)),
                 'terminationEqualsRouted': M.C.equal_typed(bad['termination'], r['termination'])}
res['lawful-envelope'] = {'ownerValidateEnvelope': attempt(lambda: M.validate_envelope(copy.deepcopy(e), r))}
src = inspect.getsource(M.validate_envelope)
res['validateEnvelopeOrder'] = {'profileBeforeParity': src.index('validate_profile') < src.index('EVALUATOR_FAULT_ENVELOPE_PARITY'),
                                'sourceSha256': hashlib.sha256(src.encode()).hexdigest()}
legal = res['legal-wrong-pair(host-io,HOST.IO_FAILURE)']
illegal = res['illegal-pair(provider-protocol,HOST.IO_FAILURE)']
res['verdict'] = {
    'schemaRefusesIllegalPair': illegal['schemaOnly(P.validate_profile)']['result'] == 'REFUSE' and illegal['ownerValidateEnvelope'].get('type') == 'ValidationError',
    'schemaAdmitsLegalWrongPairSoOnlyParityRefuses': legal['schemaOnly(P.validate_profile)']['result'] == 'ADMIT'
        and 'EVALUATOR_FAULT_ENVELOPE_PARITY' in legal['ownerValidateEnvelope'].get('message', '') and not legal['terminationEqualsRouted'],
    'lawfulEnvelopeAdmits': res['lawful-envelope']['ownerValidateEnvelope']['result'] == 'ADMIT',
}
json.dump(res, open(RT + '/receipts/probe-fault-parity.' + TREE + '.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
