"""Emit the three bounded artifacts for the protocol-3 initial-state publication correction.

Bounded static work only: no host, no environment, no suite. The captured model and artifact
are read-only and are not modified here.
"""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / 'protocol3-transitions.v1.json'
MODEL = HERE / 'native_evidence_model.v2.py'
raw_art = ART.read_text(encoding='utf-8')
raw_model = MODEL.read_bytes()
D = json.loads(raw_art)

# ---------------------------------------------------------------- the model's own literal, via AST
tree = ast.parse(raw_model.decode('utf-8'))
fn = next(n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == 'protocol3_run')
assign = next(n for n in fn.body
              if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'state')
MODEL_LITERAL = ast.literal_eval(assign.value)
assert assign.lineno == 429 and assign.end_lineno == 431, (assign.lineno, assign.end_lineno)
assert all(isinstance(v, (str, bool, int, type(None))) for v in MODEL_LITERAL.values()), \
    'a non-scalar would make dict() an incomplete copy'
assert len(MODEL_LITERAL) == 9, len(MODEL_LITERAL)

# ---------------------------------------------------------------- correction 1: initialState
OLD_MATCHLAW_TAIL = (
    " Order is therefore load-bearing: the three `WAIT_SNAPSHOT_ACCEPTED` rows P3-08..P3-10 are"
    " distinguished only by their guards, and P3-14/P3-15 likewise, so reordering or re-sorting these"
    " rows changes which transition a conforming host takes."
)
NEW_MATCHLAW_TAIL = (
    " First match in the declared order is NORMATIVE and a conforming host must implement it. It is"
    " not, however, what separates the guarded rows of one phase and frame: the three"
    " `WAIT_SNAPSHOT_ACCEPTED` rows P3-08..P3-10, and the pair P3-14/P3-15, are distinguished only by"
    " their guards, and within each set those guards are mutually exclusive and exhaustive over the"
    " admitted boolean state, so exactly one row of the set matches and re-ordering a set among itself"
    " is not observable. Declaration order is what fixes the reading against `preMatchLaw` and what"
    " keeps it stable if a row is ever added."
)
assert D['matchLaw'].endswith(OLD_MATCHLAW_TAIL), 'matchLaw tail not found verbatim'

INITIAL_STATE = dict(MODEL_LITERAL)
ORDER = [
    "Begin with a fresh copy of `initialState` and an EMPTY trace. Every value in `initialState` is a"
    " scalar, so a shallow copy is a complete one.",
    "For each event, apply `preMatchLaw` FIRST, in the order its entries are listed. The order of those"
    " entries is load-bearing: a `*PROCESS_FAULT` frame arriving when the phase is ALREADY FAULT is"
    " absorbed by the first entry and traced `FAULT-absorb`, not `P3-33`.",
    "If no `preMatchLaw` entry applies, select a row by `matchLaw`. If no row matches, apply"
    " `noMatchLaw`.",
    "On a successful row match, in this order: (1) apply the `stateUpdates` of the incoming frame;"
    " (2) resolve the row's `next`, including the `stageDependentTransitions` increment when `next` is"
    " `ANALYZING_OR_READY_COMPLETE`; (3) record `terminalKind` if the row carries `terminal`; (4) set"
    " `phase` to the resolved next and append the row's `id` to the trace.",
]

OUT = {}
for k, v in D.items():
    OUT[k] = v
    if k == 'phases':
        OUT['initialState'] = INITIAL_STATE
        OUT['initializationAndUpdateOrder'] = ORDER
OUT['matchLaw'] = D['matchLaw'][:-len(OLD_MATCHLAW_TAIL)] + NEW_MATCHLAW_TAIL

# every pre-existing field except matchLaw is byte-identical, and all 34 rows are untouched
assert json.dumps(OUT['rules'], sort_keys=True) == json.dumps(D['rules'], sort_keys=True)
assert OUT['ruleCount'] == len(OUT['rules']) == 34
for k in D:
    if k != 'matchLaw':
        assert json.dumps(OUT[k], sort_keys=True) == json.dumps(D[k], sort_keys=True), k
assert set(OUT) - set(D) == {'initialState', 'initializationAndUpdateOrder'}

proposed = json.dumps(OUT, indent=1, ensure_ascii=False) + '\n'
(HERE / 'protocol3-transitions.proposed.json').write_text(proposed, encoding='utf-8')

# the published value must survive a JSON round-trip as the SAME object the model builds today
assert json.loads(proposed)['initialState'] == MODEL_LITERAL

# ---------------------------------------------------------------- correction 2: the model splice
BEFORE = (
    b'    state = {"phase": "START", "dependencyMode": False, "preparedMode": False, "identityNegotiated": False,\n'
    b'             "stageIndex": 0, "stageCount": 0, "terminalKind": None, "sourceBytesSent": False,\n'
    b'             "stagesCompleted": 0}\n'
)
AFTER = b'    state = dict(PROTOCOL3_TRANSITIONS["initialState"])\n'
assert raw_model.count(BEFORE) == 1, raw_model.count(BEFORE)
spliced = raw_model.replace(BEFORE, AFTER)
assert spliced.count(AFTER) == 1 and spliced.replace(AFTER, BEFORE) == raw_model
assert ast.literal_eval(ast.parse(b'D = {' + BEFORE.split(b'{', 1)[1]).body[0].value) == MODEL_LITERAL
ast.parse(spliced)  # the spliced module still parses

(HERE / 'initial-state-before.py').write_bytes(BEFORE)
(HERE / 'initial-state-after.py').write_bytes(AFTER)

def rep(tag, b):
    print('%-34s bytes=%-7d sha256=%s' % (tag, len(b), hashlib.sha256(b).hexdigest()))

print('model literal (9 scalars):', json.dumps(MODEL_LITERAL))
print('published initialState == model literal:', INITIAL_STATE == MODEL_LITERAL)
print('rows preserved:', len(OUT['rules']), 'added keys:', sorted(set(OUT) - set(D)))
print()
rep('protocol3-transitions.v1.json', raw_art.encode())
rep('protocol3-transitions.proposed', proposed.encode())
rep('initial-state-before.py', BEFORE)
rep('initial-state-after.py', AFTER)
rep('native_evidence_model.v2.py', raw_model)
rep('spliced model (NOT written)', spliced)
