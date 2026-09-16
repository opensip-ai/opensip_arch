"""Real-path SEAL adapter boundary probe over one copied tree.

usage: python -I -B probe_seal_boundary.py TREE   (source38-integrated | source38-seal-before)
Uses the maintained adapter checker's own constructors (full_admitted_graph, remint_first_finding, journal_seal) and
drives actual identity-model.v3 close_run outcomes through security admit_analysis_seal. Monkeypatches only the loaded
replay stack inside this process, always restored. Reference evidence; not product fault injection.
"""
import copy, importlib.util, json, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1'
TREE = sys.argv[1]
DC = RT + '/work/' + TREE + '/docs/coop/design-corrections'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


CK = load('probe_seal_checker', DC + '/security/check-analysis-seal-adapter.v1.py')
S = CK.S
IM = S._identity_model_v3()
rows = {}


def outcome(record, run, objects, blobs):
    try:
        v = S.admit_analysis_seal(record, run, objects, blobs)
        return {'result': 'ADMIT', 'runId': v['runId'], 'authority': v['authority']}
    except S.Reject as r:
        c = r.__cause__
        return {'result': 'REJECT', 'key': str(r)[:200], 'hasPublicTermination': hasattr(r, 'termination'),
                'causeType': type(c).__name__ if c is not None else None,
                'causeIsIdentityAdmission': isinstance(c, IM.C.AdmissionError),
                'causeExactClass': ('IM.CompleteReplayMismatch' if type(c) is IM.CompleteReplayMismatch else
                                    'IM.EvidenceUnavailable' if type(c) is IM.EvidenceUnavailable else
                                    'IM.C.AdmissionError' if type(c) is IM.C.AdmissionError else 'other'),
                'innerCauseType': type(c.__cause__).__name__ if c is not None and c.__cause__ is not None else None}
    except Exception as e:
        return {'result': 'PROPAGATED', 'type': type(e).__name__, 'module': type(e).__module__, 'message': str(e)[:160],
                'isIdentityAdmission': isinstance(e, IM.C.AdmissionError)}


try:
    run, objects, blobs, run_id, digest = CK.full_admitted_graph()
    rec = CK.journal_seal(run_id)
    rows['lawful-full-run'] = outcome(rec, run, objects, blobs)

    orun, oobj, oblob = CK.remint_first_finding(run, objects, blobs)
    oid, _ = CK.M.open_run_closure(orun, oobj, oblob)
    rows['semantic-false-reminted-run'] = dict(outcome(CK.journal_seal(oid), orun, oobj, oblob), structuralAdmitRunId=oid)

    r2, o2, b2 = copy.deepcopy((run, objects, blobs))
    dom, val = o2[r2['evaluationSealId']]
    o2[r2['evaluationSealId']] = (dom, dict(val, verdict='fail' if val.get('verdict') != 'fail' else 'pass'))
    rows['structural-reference-identity'] = outcome(rec, r2, o2, b2)

    r3, o3, b3 = copy.deepcopy((run, objects, blobs))
    del o3[o3[r3['evaluationSealId']][1]['proofBundleId']]
    rows['missing-promised-proof-object'] = outcome(rec, r3, o3, b3)

    r4, o4, b4 = copy.deepcopy((run, objects, blobs))
    victim = next(k for k in sorted(b4) if o4.get(r4['planId']) and True)
    b4[victim] = b4[victim] + b' '
    rows['corrupt-retained-blob-bytes'] = outcome(rec, r4, o4, b4)

    stack = IM.complete_replay()
    original_atoms = stack.A.admit_atom_inputs

    def raise_(exc):
        def fail(*a, **k):
            raise exc
        return fail
    try:
        stack.A.admit_atom_inputs = raise_(stack.A.AtomAdmissionError('ATOM_PROBE_DECLARED_OWNER_REFUSAL'))
        rows['declared-atom-owner-refusal-inside-stack'] = outcome(rec, run, objects, blobs)
        stack.A.admit_atom_inputs = raise_(type('AdmissionError', (ValueError,), {})('REFERENCE_IDENTITY'))
        rows['undeclared-same-named-class-inside-stack'] = outcome(rec, run, objects, blobs)
        stack.A.admit_atom_inputs = raise_(RuntimeError('EVALUATOR_COMPLETE_PROOF_REPLAY'))
        rows['runtime-error-with-owner-key-text-inside-stack'] = outcome(rec, run, objects, blobs)
    finally:
        stack.A.admit_atom_inputs = original_atoms
    original_compare = stack.E.compare_complete_replay
    try:
        stack.E.compare_complete_replay = raise_(TypeError('simulated comparison defect'))
        rows['type-error-inside-replay-comparison'] = outcome(rec, run, objects, blobs)
    finally:
        stack.E.compare_complete_replay = original_compare
    rows['lawful-after-restore'] = outcome(rec, run, objects, blobs)
    rows['_identity'] = {'identityModule': IM.__name__, 'replayStackIdentityModule': stack.M.__name__,
                         'distinctLoads': stack.M is not IM and stack.M.CompleteReplayMismatch is not IM.CompleteReplayMismatch}
except Exception:
    rows['_error'] = traceback.format_exc()[-3000:]

json.dump({'tree': TREE, 'rows': rows}, open(RT + '/receipts/probe-seal-boundary.' + TREE + '.json', 'w'), indent=1)
print(json.dumps({'tree': TREE, 'rows': rows}, indent=1))
sys.exit(1 if '_error' in rows else 0)
