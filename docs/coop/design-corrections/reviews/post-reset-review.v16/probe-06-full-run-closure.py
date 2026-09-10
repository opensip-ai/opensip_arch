#!/usr/bin/env python3
"""Probe 06 (independent): CX-BV5-04 / -08 / -09 through a COMPLETE retained Run
closure, at every one of the four claimed enforcement sites.

Two admission boundaries are exercised per case:
  producer  = native_evidence_model.admit_coverage_result_v3
  retained  = identity_model.close_run over the full rekeyed object graph

Positive controls are complete Run admissions (a closed runId), not schema
fragments. Expected outcomes are authored here from the published RC-0/RC-1/RC-2
text before running.

The shared integration fixture is used as CONSTRUCTION data only; the verdict is
my own expectation, not the fixture's.
"""
import copy, hashlib, importlib.util, json, os, sys, traceback

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

spec = importlib.util.spec_from_file_location('rev16_fix', os.path.join(DC, 'integration-fixtures.py'))
F = importlib.util.module_from_spec(spec)
sys.modules['rev16_fix'] = F
spec.loader.exec_module(F)

BOUND = {p: sha256(os.path.join(DC, p)) for p in [
    'integration-fixtures.py', 'foundation/identity-model.py',
    'native/native_evidence_model.v2.py', 'native/native-evidence.schemas.v2.json',
    'foundation/relation-payload-schemas.v2.json']}

def base_graph():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    baseline = F.M.close_run(run, objects, blobs)
    return run, objects, blobs, baseline

def add_capability(objects, blobs, run, cap='unresolved-edge'):
    plan = copy.deepcopy(objects[run['planId']][1])
    analysis = F.C.parse(blobs[plan['analysisSpecDigest']])
    req = copy.deepcopy(analysis['requestedCapabilities'][0])
    req['capabilityId'] = cap
    if req not in analysis['requestedCapabilities']:
        analysis['requestedCapabilities'].append(req)
    plan['analysisSpecDigest'] = F.put_blob(blobs, F.sort_canonical_sets('analysis-spec', analysis))
    F.rekey_plan(objects, blobs, run, plan)

def attach(rel, rung, delta, with_coverage=True, cap='unresolved-edge'):
    """Build a full Run with an extra subject scope (and optionally a Coverage
    entry over it) at (rel, rung), then close the Run."""
    run, objects, blobs, baseline = base_graph()
    add_capability(objects, blobs, run, cap)
    scope = copy.deepcopy(next(v for d, v in objects.values() if d == 'subject-scope'))
    scope.update(relation=rel, resolution=rung)
    sid = F.M.identifier('subject-scope', scope)
    objects[sid] = ('subject-scope', scope)
    vid = objects[run['evidenceId']][1]['viewIds'][0]
    view = copy.deepcopy(objects[vid][1])
    view['scopeIds'].append(sid)
    producer = None
    if with_coverage:
        paths = [r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
        payload = F.coverage_result(scope, scope['sourceUniverse'], True, blobs, paths)
        payload['entry']['resolutionCompleteness'].update(delta)
        schema = next(v['payloadSchemaDigest'] for d, v in objects.values() if d == 'coverage')
        try:
            producer = F.N.admit_coverage_result_v3(payload, scope, [], schema)
        except Exception as e:
            producer = {'result': 'EXCEPTION', 'error': type(e).__name__ + ':' + str(e)[:300]}
        coverage = {'schemaVersion': 2, 'scopeId': sid, 'payloadSchemaDigest': schema,
                    'payloadDigest': F.put_blob(blobs, payload)}
        cid = F.M.identifier('coverage', coverage)
        objects[cid] = ('coverage', coverage)
        view['coverageIds'].append(cid)
        F.rekey(objects, vid, view, run)
        # deepcopy AFTER the view rekey: rekey rewrites evidence.viewIds, and an
        # evidence snapshot taken before it carries a stale, unresolvable view id.
        evidence = copy.deepcopy(objects[run['evidenceId']][1])
        evidence['coverageIds'].append(cid)
        F.rekey(objects, run['evidenceId'], evidence, run)
    else:
        F.rekey(objects, vid, view, run)
    F.resync_witness(objects, blobs, run)
    F.resync_proof_refs(objects, blobs, run)
    try:
        final = F.M.close_run(run, objects, blobs)
        retained = {'result': 'ADMIT', 'runId': final}
    except Exception as e:
        retained = {'result': 'REFUSE', 'error': type(e).__name__ + ':' + str(e)[:400]}
    return baseline, producer, retained

NA = {'state': 'not-applicable', 'attempted': False, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': []}

CASES = [
    # id, relation, rung, completeness delta, with_coverage, expectedProducer, expectedRetained, why
    ('P1-valid-observed-control', 'unresolved-edge', 'observed', {}, True, 'ADMIT', 'ADMIT',
     'VALID OBSERVED CONTROL: registered pair, NA minted per RC-1. A complete Run must still close.'),
    ('P2-cross-relation-rung', 'unresolved-edge', 'enumerated', {}, True, 'REFUSE', 'REFUSE',
     'RC-0: unresolved-edge@enumerated names two registered tokens and no registered pair.'),
    ('P3-attempted-true', 'unresolved-edge', 'observed', {'attempted': True}, True, 'REFUSE', 'REFUSE',
     'RC-1 minting law: not-applicable makes no resolution claim, so attempted must be false.'),
    ('P4-nonempty-registered-classes', 'unresolved-edge', 'observed',
     {'unresolvedEdgeClasses': ['computed-member-access']}, True, 'REFUSE', 'REFUSE',
     'RC-1 minting law: the class list must be empty on a not-applicable entry.'),
    ('P5-state-complete-on-na-rung', 'unresolved-edge', 'observed', {'state': 'complete'}, True,
     'REFUSE', 'REFUSE', 'RC-1: a non-resolved rung must be not-applicable.'),
    ('P6-stageTerminal-free', 'unresolved-edge', 'observed', {'stageTerminal': 'budget-exhausted'},
     True, 'ADMIT', 'ADMIT',
     'stageTerminal is deliberately FREE on not-applicable; a complete Run must still close.'),
    ('P7-examinedExhaustive-independent', 'unresolved-edge', 'observed',
     {'examinedExhaustive': False}, True, 'ADMIT', 'ADMIT',
     'examinedExhaustive stays the independent 4.1 partition claim.'),
    ('P8-retained-scope-no-coverage-badpair', 'unresolved-edge', 'enumerated', {}, False,
     None, 'REFUSE',
     'CX-BV5-08 site 4: a RETAINED scope a view names, with NO Coverage wrapper and no fact, '
     'must still carry a registered pair at closure.'),
    ('P9-retained-scope-no-coverage-goodpair', 'unresolved-edge', 'observed', {}, False,
     None, 'ADMIT',
     'Control for P8: the same shape with a REGISTERED pair must close a complete Run.'),
    ('P10-declares-with-calls-rung', 'declares', 'resolved-callee', {}, False, None, 'REFUSE',
     'CX-BV5-08: a single-rung relation carrying another relation\'s rung is refused at closure.'),
]

rows = []
for cid, rel, rung, delta, withcov, exp_p, exp_r, why in CASES:
    try:
        baseline, producer, retained = attach(rel, rung, dict(NA, **delta) if delta else {}, withcov)
        harness = None
    except Exception as e:
        baseline = producer = retained = None
        harness = type(e).__name__ + ':' + str(e)[:400] + '\n' + traceback.format_exc()[-800:]
    obs_p = None
    if producer is not None:
        obs_p = 'ADMIT' if producer.get('result') == 'ADMIT' else 'REFUSE'
    obs_r = retained['result'] if retained else None
    rows.append({
        'id': cid, 'pair': f'{rel}@{rung}', 'delta': delta, 'withCoverage': withcov,
        'expectedProducer': exp_p, 'observedProducer': obs_p,
        'producerAgrees': (exp_p is None) or (obs_p == exp_p),
        'producerDetail': producer,
        'expectedRetained': exp_r, 'observedRetained': obs_r,
        'retainedAgrees': obs_r == exp_r,
        'retainedDetail': retained,
        'baselineRunId': baseline,
        'harnessError': harness, 'why': why,
    })
    print(f"{cid:42s} producer={obs_p!s:7s}(exp {exp_p!s:7s}) retained={obs_r!s:7s}(exp {exp_r})"
          + ('  HARNESS-ERROR' if harness else ''))

res = {
    'probe': 'probe-06-full-run-closure',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': BOUND,
    'cases': len(rows),
    'producerAgree': sum(1 for r in rows if r['producerAgrees']),
    'retainedAgree': sum(1 for r in rows if r['retainedAgrees']),
    'allAgree': all(r['producerAgrees'] and r['retainedAgrees'] for r in rows),
    'harnessErrors': [r['id'] for r in rows if r['harnessError']],
    'completeRunAdmissionsObserved': sorted({r['retainedDetail']['runId'] for r in rows
                                             if r['retainedDetail'] and r['retainedDetail'].get('runId')}),
    'rows': rows,
    'scope': 'Synthetic full retained Run closure over the shared construction fixture. '
             'No product host, compiler, OS, filesystem or cryptographic qualification.',
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-06-full-run-closure.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=2, sort_keys=True))
