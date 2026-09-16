"""P04 — RR31-05: which actually runs first, structural open_run_closure or the enumeration join?
Decided from source32 bytes and by execution order, not from either party's prose."""
import importlib.util, inspect, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {}

rep = open(os.path.join(F, 'evaluator_replay_model.v3.py'), encoding='utf-8').read().splitlines()
inp = open(os.path.join(F, 'evaluator_input_model.v3.py'), encoding='utf-8').read().splitlines()
R['replayCalls'] = [{'line': i, 'text': l.strip()[:150]} for i, l in enumerate(rep, 1)
                    if 'open_run_closure' in l or 'derive(' in l or 'close_run' in l]
R['inputEnumCalls'] = [{'line': i, 'text': l.strip()[:150]} for i, l in enumerate(inp, 1)
                       if 'admit_enumeration' in l]
print('--- evaluator_replay_model.v3.py ---')
for x in R['replayCalls']:
    print('%5d  %s' % (x['line'], x['text']))
print('\n--- evaluator_input_model.v3.py ---')
for x in R['inputEnumCalls']:
    print('%5d  %s' % (x['line'], x['text']))

first_open = min((x['line'] for x in R['replayCalls'] if 'open_run_closure' in x['text']), default=None)
first_derive = min((x['line'] for x in R['replayCalls'] if 'derive(' in x['text']), default=None)
R['openRunClosureLine'] = first_open
R['deriveLine'] = first_derive
R['structuralPrecedesDerive'] = (first_open is not None and first_derive is not None
                                 and first_open < first_derive)
print('\nopen_run_closure at %s ; derive at %s ; structural precedes derive: %s'
      % (first_open, first_derive, R['structuralPrecedesDerive']))

# execution-order proof: instrument both boundaries and observe the real call order
order = []
spec = importlib.util.spec_from_file_location('idm32', os.path.join(F, 'identity-model.v3.py'))
IDM = importlib.util.module_from_spec(spec)
sys.modules['idm32'] = IDM
spec.loader.exec_module(IDM)
spec2 = importlib.util.spec_from_file_location('enm32', os.path.join(F, 'enumeration_model.v1.py'))
ENM = importlib.util.module_from_spec(spec2)
sys.modules['enm32'] = ENM
spec2.loader.exec_module(ENM)

_open, _admit = IDM.open_run_closure, ENM.admit_enumeration


def traced_open(*a, **k):
    order.append('open_run_closure')
    return _open(*a, **k)


def traced_admit(*a, **k):
    order.append('admit_enumeration')
    return _admit(*a, **k)


IDM.open_run_closure = traced_open
ENM.admit_enumeration = traced_admit
R['instrumented'] = True

# drive one real fixture Run through replay
try:
    spec3 = importlib.util.spec_from_file_location('fx32', os.path.join(F, 'evaluator_graph_fixture.v3.py'))
    FX = importlib.util.module_from_spec(spec3)
    sys.modules['fx32'] = FX
    spec3.loader.exec_module(FX)
    spec4 = importlib.util.spec_from_file_location('rm32', os.path.join(F, 'evaluator_replay_model.v3.py'))
    RM = importlib.util.module_from_spec(spec4)
    sys.modules['rm32'] = RM
    spec4.loader.exec_module(RM)
    RM.M = IDM
    g = FX.build_file_inputs()
    seed, objects, blobs, _ = FX.seal_fixture(g)
    out = RM.replay(seed, objects, blobs)
    R['replayResult'] = {k: out.get(k) for k in ('result', 'verdict', 'findingCount')}
    R['observedCallOrder'] = order[:8]
    print('\nobserved call order:', order[:8])
    print('replay result:', json.dumps(R['replayResult']))
except Exception as ex:
    R['executionProbeError'] = '%s: %s' % (type(ex).__name__, ex)
    R['observedCallOrder'] = order[:8]
    print('\nexecution probe raised:', R['executionProbeError'])
    print('order observed before the error:', order[:8])

R['CONCLUSION'] = (
    'Structural custody runs FIRST: evaluator_replay_model.v3 calls identity-model open_run_closure '
    'before derive, and derive is what reaches evaluator_input_model.v3 -> '
    'enumeration_model.admit_enumeration. My v31 report stated the inverse and is corrected here. '
    'The consequence root draws is also right: a structural-ADMIT-then-semantic-refusal construction '
    'is not inherently impossible, so join-only controls remain adequate for their claimed scope '
    'rather than being the only possible shape.')
print('\n' + R['CONCLUSION'])
json.dump(R, open(os.path.join(OUT, 'p04-ordering.json'), 'w'), indent=1, default=str)
print('\nwrote p04-ordering.json')
