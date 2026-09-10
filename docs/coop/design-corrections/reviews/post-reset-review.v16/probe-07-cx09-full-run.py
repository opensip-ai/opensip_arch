#!/usr/bin/env python3
"""Probe 07 (independent): CX-BV5-09 through a COMPLETE retained Run closure on a
RESOLVED rung.

The claim under test: a resolved COMPLETE record with zero unresolved facts and
zero unresolvedEdgeCount can no longer retain a non-empty unresolvedEdgeClasses
set, and the analogous not-attempted hole is closed - while incomplete/partial
remain untouched honest observations that DO carry their classes.

Mutates the fixture's OWN base coverage entry (a resolved rung) rather than
attaching a new scope, so the state-specific law is exercised on the same record
that closes the baseline Run.
"""
import copy, hashlib, importlib.util, json, os, sys, traceback

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

spec = importlib.util.spec_from_file_location('rev16_fix7', os.path.join(DC, 'integration-fixtures.py'))
F = importlib.util.module_from_spec(spec)
sys.modules['rev16_fix7'] = F
spec.loader.exec_module(F)

def mutate_base_coverage(delta):
    run, objects, blobs = F.build(resolved=True, has_match=True)
    baseline = F.M.close_run(run, objects, blobs)
    cid = objects[run['evidenceId']][1]['coverageIds'][0]
    coverage = copy.deepcopy(objects[cid][1])
    payload = F.C.parse(blobs[coverage['payloadDigest']])
    before = copy.deepcopy(payload['entry']['resolutionCompleteness'])
    pair = payload['key']['relation'] + '@' + payload['key']['resolution'] \
        if 'relation' in payload.get('key', {}) else None
    scope = objects[coverage['scopeId']][1]
    pair = scope['relation'] + '@' + scope['resolution']
    payload['entry']['resolutionCompleteness'].update(delta)
    after = copy.deepcopy(payload['entry']['resolutionCompleteness'])
    schema = coverage['payloadSchemaDigest']
    try:
        producer = F.N.admit_coverage_result_v3(payload, scope, [], schema)
    except Exception as e:
        producer = {'result': 'EXCEPTION', 'error': type(e).__name__ + ':' + str(e)[:300]}
    coverage['payloadDigest'] = F.put_blob(blobs, payload)
    F.rekey(objects, cid, coverage, run)
    F.resync_witness(objects, blobs, run)
    F.resync_proof_refs(objects, blobs, run)
    try:
        retained = {'result': 'ADMIT', 'runId': F.M.close_run(run, objects, blobs)}
    except Exception as e:
        retained = {'result': 'REFUSE', 'error': type(e).__name__ + ':' + str(e)[:400]}
    return baseline, pair, before, after, producer, retained

CASES = [
    ('Q0-untouched-baseline-control', {}, 'ADMIT', 'ADMIT',
     'POSITIVE CONTROL: the unmutated base coverage entry must close a complete Run.'),
    ('Q1-complete-zerocount-nonempty-classes',
     {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': ['computed-member-access'], 'stageTerminal': 'complete',
      'examinedExhaustive': True}, 'REFUSE', 'REFUSE',
     'CX-BV5-09: a resolved COMPLETE record with zero unresolved facts/count cannot retain a '
     'nonempty class set.'),
    ('Q2-complete-clean-control',
     {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True},
     'ADMIT', 'ADMIT', 'CX-BV5-09 VALID CONTROL: same record with an empty class set admits.'),
    ('Q3-not-attempted-nonempty-classes',
     {'state': 'not-attempted', 'attempted': False, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': ['dynamic-import-expression'], 'stageTerminal': 'unavailable',
      'examinedExhaustive': False}, 'REFUSE', 'REFUSE',
     'CX-BV5-09 analogue: a skipped stage observed nothing, so it can report no class.'),
    ('Q4-not-attempted-clean-control',
     {'state': 'not-attempted', 'attempted': False, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'unavailable', 'examinedExhaustive': False},
     'ADMIT', 'ADMIT', 'PRESERVED not-attempted control.'),
    ('Q5-partial-zero-facts-nonempty-classes',
     {'state': 'partial', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': ['computed-member-access'], 'stageTerminal': 'budget-exhausted',
      'examinedExhaustive': False}, 'REFUSE', 'REFUSE',
     'PRESERVED RC-2: partial still requires exact count AND class equality against admitted facts; '
     'zero facts means the class list must match the empty observation.'),
    ('Q6-partial-zero-facts-clean',
     {'state': 'partial', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'budget-exhausted', 'examinedExhaustive': False},
     'ADMIT', 'ADMIT', 'PRESERVED partial control: an honest partial with nothing observed.'),
    ('Q7-incomplete-zero-facts',
     {'state': 'incomplete', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True},
     'REFUSE', 'REFUSE', 'PRESERVED RC-2: incomplete needs >=1 edge; a zero-edge incomplete is partial.'),
    ('Q8-complete-without-attempted',
     {'state': 'complete', 'attempted': False, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True},
     'REFUSE', 'REFUSE', 'PRESERVED RC-2 precondition: complete requires attempted=true.'),
    ('Q9-complete-without-exhaustive',
     {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': False},
     'REFUSE', 'REFUSE', 'PRESERVED RC-2 precondition: complete requires exhaustive examination.'),
    ('Q10-complete-wrong-stage',
     {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': [], 'stageTerminal': 'budget-exhausted', 'examinedExhaustive': True},
     'REFUSE', 'REFUSE', 'PRESERVED RC-2 precondition: complete requires stageTerminal=complete.'),
    ('Q11-not-applicable-on-resolved-rung',
     {'state': 'not-applicable', 'attempted': False, 'unresolvedEdgeCount': 0,
      'unresolvedEdgeClasses': []}, 'REFUSE', 'REFUSE',
     'PRESERVED RC-1: a resolved rung must never claim not-applicable.'),
]

rows = []
for cid, delta, exp_p, exp_r, why in CASES:
    try:
        baseline, pair, before, after, producer, retained = mutate_base_coverage(delta)
        harness = None
    except Exception as e:
        baseline = pair = before = after = producer = retained = None
        harness = type(e).__name__ + ':' + str(e)[:300] + traceback.format_exc()[-600:]
    obs_p = ('ADMIT' if producer.get('result') == 'ADMIT' else 'REFUSE') if producer else None
    obs_r = retained['result'] if retained else None
    rows.append({'id': cid, 'mutatedPair': pair, 'before': before, 'after': after,
                 'expectedProducer': exp_p, 'observedProducer': obs_p,
                 'producerAgrees': obs_p == exp_p, 'producerDetail': producer,
                 'expectedRetained': exp_r, 'observedRetained': obs_r,
                 'retainedAgrees': obs_r == exp_r, 'retainedDetail': retained,
                 'baselineRunId': baseline, 'harnessError': harness, 'why': why})
    print(f"{cid:40s} pair={pair!s:28s} producer={obs_p!s:7s}(exp {exp_p!s:6s}) "
          f"retained={obs_r!s:7s}(exp {exp_r})" + ('  HARNESS-ERROR' if harness else ''))

res = {'probe': 'probe-07-cx09-full-run', 'copyName': 'copy-B-probes',
       'boundSourceSha256': {p: sha256(os.path.join(DC, p)) for p in [
           'integration-fixtures.py', 'foundation/identity-model.py',
           'native/native_evidence_model.v2.py']},
       'cases': len(rows),
       'producerAgree': sum(1 for r in rows if r['producerAgrees']),
       'retainedAgree': sum(1 for r in rows if r['retainedAgrees']),
       'allAgree': all(r['producerAgrees'] and r['retainedAgrees'] for r in rows),
       'harnessErrors': [r['id'] for r in rows if r['harnessError']],
       'completeRunAdmissionsObserved': sorted({r['retainedDetail']['runId'] for r in rows
                                                if r['retainedDetail'] and r['retainedDetail'].get('runId')}),
       'rows': rows, 'notProductQualification': True}
with open(os.path.join(OUT, 'probe-07-cx09-full-run.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=2, sort_keys=True))
