"""Which of the ten guarded handler lines actually EXECUTE during the real canonical workflow run
on the unchanged frozen corpus. This separates real positive-control execution from root's synthetic
handler-body executions.

Limit: line-execution counts only. Executing a handler does not mean the guard was discriminating
there; it means the branch is reachable from the real corpus."""
import json, pathlib, sys, importlib.util, os
TARGET = os.environ['CHECKER']
LINES = {171, 384, 407, 1112, 1158, 1171, 1203, 1226, 1320, 1360}
hits = {l: 0 for l in LINES}
def tracer(frame, event, arg):
    if event == 'line' and frame.f_code.co_filename == TARGET and frame.f_lineno in hits:
        hits[frame.f_lineno] += 1
    return tracer
os.chdir(str(pathlib.Path(TARGET).parent))
sys.argv = ['x', '--report', os.environ['REPORT']]
spec = importlib.util.spec_from_file_location('cw', TARGET)
m = importlib.util.module_from_spec(spec)
sys.settrace(tracer)
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass
finally:
    sys.settrace(None)
executed = {str(k): v for k, v in sorted(hits.items()) if v}
print(json.dumps({'standing': __doc__, 'checker': TARGET,
 'handlerLinesExecutedInRealRun': executed,
 'handlerLinesNeverExecuted': sorted(str(k) for k, v in hits.items() if not v),
 'realExecutionCoverage': '%d of 10' % len(executed)}, indent=1))
