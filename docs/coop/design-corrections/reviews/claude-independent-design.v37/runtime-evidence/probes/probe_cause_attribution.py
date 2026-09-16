"""P-CAUSE-2: whole-Run cause order and coverageId attribution (independent reviewer probe).

A. Same actual closed indeterminate Run (receipt probe-semantic-boundaries.json P-CAUSE): every deficient
   Coverage record is a schema-valid StepTermination.coverageId; absence is also valid. No retained field
   selects one, and the sealed proof keeps deficiencies only as canonical sets.
B. Native stage selection where the stage-implied primary differs from the entry detail (native section 10):
   actual run_termination over a clean BudgetExhausted stage terminal and a resolution-incomplete entry.
C. Concurrent D9-member conditions from different owners (requirement sufficiency vs native stage terminal):
   both pre-reduction orders through the D9 concurrentConditionReducer/codeDerivation give schema-valid,
   different reasonCodes (different primary remedy class) for the same sealed Run.
Reference evidence only.
"""
import importlib.util, itertools, json, sys

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SRC = BASE + '/work/source37'
DC = SRC + '/docs/coop/design-corrections'
OUT = BASE + '/receipts/probe-cause-attribution.json'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


Q = load('c37_query', DC + '/workflows/query_projection_model.v3.py')
N = load('c37_native', DC + '/native/native_evidence_model.v2.py')
D9 = json.load(open(SRC + '/docs/coop/artifacts/d9-exit-contract.v1.14.json'))
prior = json.load(open(BASE + '/receipts/probe-semantic-boundaries.json'))['P-CAUSE']
STEP = Q.COMMON_ID + '#/$defs/StepTermination'


def valid(t):
    try:
        Q.validate_schema(STEP, t)
        return True
    except Exception as e:
        return 'INVALID:' + str(e).split('\n')[0][:160]


res = {'standing': 'independent reviewer probe; reference evidence only'}
run_id = prior['run']['runId']
deficient = [e['coverageId'] for e in prior['retainedCoverageEntries'] if e['deficiency']]
A = []
for cid in deficient + [None]:
    t = {'class': 'indeterminate', 'reasonCodes': ['VERDICT.INDETERMINATE'], 'runId': run_id}
    if cid:
        t['coverageId'] = cid
    A.append({'coverageId': cid, 'schemaValid': valid(t)})
res['A-coverageId-candidates'] = {'runId': run_id, 'deficientCoverageRecords': len(deficient), 'candidates': A,
                                  'allValid': all(x['schemaValid'] is True for x in A)}

# B. stage-implied primary differs from entry detail
term_map = getattr(N, 'STAGE_TERMINAL_DEFICIENCY', {})
bx = [k for k, v in term_map.items() if v == 'budget-exhausted']
B = {'stageTerminalMap': term_map}
if bx:
    out = N.run_termination({'authority': 'authoritative', 'terminalKind': bx[0],
                             'd9': {'class': 'success', 'exitCode': 0, 'code': None}},
                            [{'deficiency': 'resolution-incomplete', 'nativeCause': None}])
    B['run_termination'] = out
    B['stagePrimaryCode'] = out['d9']['code']
    B['entryTypedDetailDeficiency'] = (out.get('typedDetail') or {}).get('deficiency')
    B['differs'] = B['entryTypedDetailDeficiency'] is not None and N.native_deficiency_d9(B['entryTypedDetailDeficiency'])['code'] != B['stagePrimaryCode']
res['B-stage-vs-entry'] = B

# C. D9 reducer over two owners' conditions in both lawful orders
dmap = D9['codeMaps']['deficiencyToReasonCode']


def reduce(deficiencies):
    primary, rest = deficiencies[0], []
    for d in deficiencies[1:]:
        if d != primary and d not in rest:
            rest.append(d)
    return {'class': 'indeterminate', 'reasonCodes': [dmap[primary]] + [dmap[d] for d in rest], 'runId': run_id}


conditions = {'requirement-sufficiency': 'required-relation-missing', 'native-stage-terminal': 'budget-exhausted',
              'verdict-composition': 'verdict-indeterminate'}
C = []
for perm in itertools.permutations(conditions.items()):
    t = reduce([d for _, d in perm])
    C.append({'order': [k for k, _ in perm], 'termination': t, 'schemaValid': valid(t)})
res['C-reducer-orders'] = {'conditions': conditions, 'rows': C,
                           'distinctPrimaryCodes': sorted({r['termination']['reasonCodes'][0] for r in C}),
                           'distinctCodeSequences': len({tuple(r['termination']['reasonCodes']) for r in C}),
                           'allValid': all(r['schemaValid'] is True for r in C)}
json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps({'A': res['A-coverageId-candidates']['allValid'], 'A-n': len(A),
                  'B': {k: B.get(k) for k in ('stagePrimaryCode', 'entryTypedDetailDeficiency', 'differs')},
                  'C-primary': res['C-reducer-orders']['distinctPrimaryCodes'],
                  'C-seq': res['C-reducer-orders']['distinctCodeSequences'], 'C-valid': res['C-reducer-orders']['allValid']}, indent=1))
