"""P04c — dynamic half of RR31-05, using the construction the reference checker itself uses.

p04b built the graph with build_file_inputs+seal_fixture alone, which does not yield a
replay-consistent Run: RM.replay refused EVALUATOR_COMPLETE_PROOF_REPLAY. That was my construction
error, not a source fault, and is preserved. check-replay.v3.py has a `positive()` helper that does
the full construction; I use it.
"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {'corrects': 'p04b used an incomplete fixture construction for replay'}
sys.path.insert(0, F)
os.chdir(F)

spec = importlib.util.spec_from_file_location('chkreplay32', os.path.join(F, 'check-replay.v3.py'))
CR = importlib.util.module_from_spec(spec)
sys.modules['chkreplay32'] = CR
spec.loader.exec_module(CR)
R['checkerHasPositive'] = hasattr(CR, 'positive')
print('check-replay.v3.py exposes positive():', R['checkerHasPositive'])

WATCH = {'open_run_closure', 'admit_enumeration', 'derive', 'close_run', 'compare_complete_replay'}
seen = []


def tracer(frame, event, arg):
    if event == 'call':
        n = frame.f_code.co_name
        if n in WATCH and (not seen or seen[-1] != n):
            seen.append(n)
    return None


graph = CR.positive()
sys.settrace(tracer)
try:
    out = CR.R.replay(*graph)
except Exception as ex:
    out = {'error': '%s: %s' % (type(ex).__name__, ex)}
finally:
    sys.settrace(None)
R['observedOrder'] = seen
R['replayOut'] = {k: out.get(k) for k in ('result', 'verdict', 'findingCount')} if isinstance(out, dict) else str(out)
print('observed call order:', seen)
print('replay out         :', json.dumps(R['replayOut']))
if 'open_run_closure' in seen and 'admit_enumeration' in seen:
    R['structuralObservedFirst'] = seen.index('open_run_closure') < seen.index('admit_enumeration')
else:
    R['structuralObservedFirst'] = None
print('open_run_closure observed before admit_enumeration:', R['structuralObservedFirst'])
json.dump(R, open(os.path.join(OUT, 'p04c-ordering.json'), 'w'), indent=1, default=str)
print('wrote p04c-ordering.json')
