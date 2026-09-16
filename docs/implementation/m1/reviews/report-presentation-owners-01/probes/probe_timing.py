import copy
import json
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, DC, load, jload, Recorder
from jsonschema import Draft202012Validator, validators
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

S = ROOT / 'm1-workflow-timing-subject-01'
t = load(S / 'timing.py', 'timing_subject')
v4 = jload(S / 'invocation-record.v4.schema.json')
v3 = jload(DC / 'workflows/schemas/evaluator3/invocation-record.schema.json')
common = jload(DC / 'workflows/schemas/evaluator3/common.schema.json')
V = validators.extend(Draft202012Validator, type_checker=Draft202012Validator.TYPE_CHECKER.redefine('integer', lambda _, v: type(v) is int))
reg = Registry().with_resources((d['$id'], Resource(contents={k: v for k, v in d.items() if k != '$schema'}, specification=DRAFT202012)) for d in (v4, common))
R = Recorder('m1-workflow-timing-subject-01')
attempt = V({'$ref': v4['$id'] + '#/$defs/Attempt'}, registry=reg)
eid = 'exec1_' + '1' * 32
eid_ok = V({'$ref': common['$id'] + '#/$defs/ExecutionId'}, registry=reg).is_valid(eid)
if not eid_ok:
    import re
    pat = common['$defs']['ExecutionId']['pattern']
    eid = None
R.record('TIM-D0', 'derivation', 'fixture ExecutionId valid under pinned common', {'pattern': common['$defs']['ExecutionId'].get('pattern'), 'fixture': eid}, eid_ok)

# Controls
R.record('TIM-C1', 'control-valid', 'completed + measured Attempt valid under v4', None,
         attempt.is_valid({'executionId': eid, 'outcome': 'completed', 'observedDuration': {'state': 'measured', 'milliseconds': 0}}))
R.record('TIM-C2', 'control-invalid', 'v4 Attempt without observedDuration invalid; not-retained invalid', None,
         not attempt.is_valid({'executionId': eid, 'outcome': 'completed'}) and
         not attempt.is_valid({'executionId': eid, 'outcome': 'failed', 'observedDuration': {'state': 'unavailable', 'reason': 'not-retained'}}))
rng = random.Random(20260914); bad = []
for _ in range(20000):
    s = rng.randrange(-2**70, 2**70); d = rng.choice([rng.randrange(0, 10**7), rng.randrange(0, 2**80)])
    got = t.observe_terminal('failed', s, s + d); want = d // 1_000_000
    exp = {'state': 'measured', 'milliseconds': want} if want <= t.U64_MAX else t.unavailable('duration-overflow')
    if got != exp: bad.append((s, d, got))
R.record('TIM-C3', 'control-valid', '20000 random (origin, delta) pairs equal floor(delta/1e6) or overflow', {'mismatches': bad[:3]}, not bad)
R.record('TIM-C4', 'control-valid', 'abandoned never measured; supervisor-lost only for abandoned (reference helper)', None,
         t.observe_terminal('abandoned', 0, 10**9) == t.unavailable('supervisor-lost'))

# F: schema (the generated/typed carrier) admits outcome/reason contradictions
cases = {'abandoned+measured': {'executionId': eid, 'outcome': 'abandoned', 'observedDuration': {'state': 'measured', 'milliseconds': 5}},
         'completed+supervisor-lost': {'executionId': eid, 'outcome': 'completed', 'observedDuration': {'state': 'unavailable', 'reason': 'supervisor-lost'}},
         'abandoned+clock-unavailable': {'executionId': eid, 'outcome': 'abandoned', 'observedDuration': {'state': 'unavailable', 'reason': 'clock-unavailable'}}}
res = {k: attempt.is_valid(v) for k, v in cases.items()}
R.record('TIM-F1', 'finding', 'invocation:4 Attempt schema enforces the contract outcome/reason law', res, all(res.values()),
         'Attempt already uses allOf if/then (installationRecoveryStartRef); the join exists only in timing.admit_duration')

# F: malformed samples become clock-unavailable when the other sample is None
o = [R.outcome(lambda: t.observe_terminal('completed', None, 4.0)), R.outcome(lambda: t.observe_terminal('completed', '0', None)),
     R.outcome(lambda: t.observe_terminal('completed', True, None))]
R.record('TIM-F2', 'finding', 'malformed caller types are admission errors, not clock states (contract)', o, all(x.get('returned') == t.unavailable('clock-unavailable') for x in o))

# F: summarize_attempts trusts unadmitted projections
o = [R.outcome(lambda: t.summarize_attempts([{'duration': {'state': 'bogus'}}])),
     R.outcome(lambda: t.summarize_attempts([{'executionId': eid, 'duration': {'state': 'measured', 'milliseconds': 1}}] * 2)),
     R.outcome(lambda: t.summarize_attempts([{'duration': {'state': 'measured', 'milliseconds': -5}}]))]
R.record('TIM-F3', 'finding', 'step sum refuses unadmitted/duplicate-ExecutionId/negative projections', o,
         o[0].get('raised') == 'KeyError' and 'returned' in o[1] and o[2].get('returned', {}).get('milliseconds') == -5)

# F: legacy invocation major 1 exists; projection refuses instead of owner "incompatible" panel state
legacy = jload(DC / 'workflows/schemas/invocation-record.schema.json')
report = jload(ROOT / 'm1-report-projection-subject-07/report-projection.schema.json')
o = R.outcome(lambda: t.project_attempt(1, {'executionId': eid, 'outcome': 'completed'}))
R.record('TIM-F4', 'finding', 'retained older majors map to a disclosed report state rather than a projection refusal',
         {'legacyMajor': legacy['properties']['schemaMajor'], 'projection': o,
          'reportIncompatibleState': report['$defs']['PanelNotPresentV1']['oneOf'][3]},
         o.get('raised') == 'TimingRefusal', 'contract "Other source majors are refused" leaves the ledger state for retained major-1 records unowned')

# F/derivation: current report ledger consumes invocation:3 Attempt properties
led = report['$defs']['LedgerStepV1']['properties']['attempts']['items']
R.record('TIM-D1', 'derivation', 'report LedgerStepV1 attempts still $ref invocation:3 and have no duration member', sorted(led['properties']), 'observedDuration' not in led['properties'])
R.dump(Path(__file__).resolve().parent / 'timing-results.json')
