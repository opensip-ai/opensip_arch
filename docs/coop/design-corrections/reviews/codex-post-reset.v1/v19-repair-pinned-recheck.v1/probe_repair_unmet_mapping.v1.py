"""SYNTHETIC FIXTURE ADAPTER (labelled) for the v19 repair unmet-precondition mapping correction.

WHAT THIS IS: a bounded, read-only direct reference control. It loads the FROZEN v18
workflows_model.v1.py and the frozen workflows schema bundle, and drives `repair_preview`
through the same synthetic in-memory fixture the retained checker uses (workflow-cases.v1.json
`repairScenario`). Nothing under candidate-subject.v18 is written, and no retained case is edited.

WHAT THIS IS NOT: not a host execution, not an authorization execution, not product
qualification. The trees, Runs, closed-world records and requirement rows are synthetic
fixtures; `repair_preview` is called directly as a helper, exactly as the retained checker
calls it. No claim is made here about a real host, a real security unit or a real Run.

Controls (observed values are asserted, not narrated):
  C1  retained/replayable Run, ONE unsatisfied NATIVE requirement
  C1b same, different native cause  -> different remedy, same code
  C2  unsatisfied IMPORTED-plane requirement
  C3  available Run, ALL requirements satisfied
  C4  unavailable (purged) Run, all requirements satisfied
  C5  unavailable Run AND an unsatisfied requirement -> two entries, one code, two remedies
  S1  schema-alone permissiveness: unsatisfied requirement + EMPTY unmetPreconditions
  S2  the clarification's alternative: does the model ever name the closed-world code here?
"""
import importlib.util
import json
import sys
from pathlib import Path

SUBJECT = Path('/tmp/opensip-design-corrections/candidate-subject.v18/docs/coop/design-corrections')
WF = SUBJECT / 'workflows'
sys.path.insert(0, str(SUBJECT / 'foundation'))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location('workflows_model', WF / 'workflows_model.v1.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

SCHEMAS = {}
for p in sorted((WF / 'schemas').glob('*.schema.json')):
    s = canonical.parse(p.read_bytes())
    SCHEMAS[s['$id']] = s
FOUNDATION = canonical.parse((SUBJECT / 'foundation' / 'identity-schemas.v2.json').read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUNDATION['$id'], Resource(contents=FOUNDATION, specification=DRAFT202012))])
U = 'urn:opensip:product-v1:workflows:'

def valid(ref, value):
    sid, _, frag = ref.partition('#')
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': sid + '#' + frag}, registry=REG).validate(value)
        return True, ''
    except (ValidationError, canonical.AdmissionError) as e:
        return False, str(e).splitlines()[0][:160]

# --- the retained synthetic fixture, substituted exactly as the retained checker substitutes it
RAW = canonical.parse((WF / 'workflow-cases.v1.json').read_bytes())
C = dict(RAW['constants'])

def sub(o):
    if isinstance(o, str) and o.startswith('$'):
        return C[o[1:]]
    if isinstance(o, dict):
        return {k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    return o

RS = sub(RAW['repairScenario'])
PRJ, PROD = C['PRJ'], C['PROD']

def preview(requirements, availability='retained', sealed='replayable', closed_world=None, origin=None):
    tree = {k: v.encode() for k, v in RS['tree'].items()}
    run = dict(RS['run'])
    run['availability'] = availability
    run['sealedAssurance'] = sealed
    if closed_world is not None:
        run['closedWorld'] = closed_world
    if origin is not None:
        run['evidenceOrigin'] = origin
    run['snapshotId'] = M.tree_snapshot_id(PRJ, tree)
    edits = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e)
             for e in RS['edits']]
    return M.repair_preview(PRJ, tree, run, RS['recipe'], RS['targets'], edits, requirements,
                            list(RS['permittedScope']), {PROD: 'admitted'})

RESULTS = []

def record(cid, ok, observed):
    RESULTS.append({'id': cid, 'ok': bool(ok), 'observed': observed})
    print(('PASS ' if ok else 'FAIL ') + cid + '  ' + json.dumps(observed))

SATISFIED = [{'relation': 'imports', 'minResolution': 'resolved-target',
              'completeness': 'complete', 'satisfied': True}]
NATIVE_A = [{'relation': 'references', 'minResolution': 'resolved-binding', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'resolution-incomplete'}]
NATIVE_B = [{'relation': 'references', 'minResolution': 'resolved-binding', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'external-consumers-unknown'}]
IMPORTED = [{'relation': 'history-change', 'minResolution': 'observed', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'import-unmapped-only'}]

CODE = 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'

# --- C1 / C1b: retained, replayable Run; one unsatisfied NATIVE requirement, two different causes
p1 = preview(NATIVE_A)
d1 = p1['descriptor']
u1 = d1['unmetPreconditions']
record('C1.one-entry-with-the-existing-code-and-the-exact-native-cause',
       d1['applicable'] is False and len(u1) == 1 and u1[0]['code'] == CODE
       and u1[0]['remedy'] == 'evidence requirement unsatisfied: references@resolved-binding '
                              '(native: resolution-incomplete)',
       {'applicable': d1['applicable'], 'entries': len(u1), 'codes': [e['code'] for e in u1],
        'remedies': [e['remedy'] for e in u1]})
record('C1.run-is-retained-and-replayable-so-no-retention-entry-exists',
       RS['run']['availability'] == 'retained' and RS['run']['sealedAssurance'] == 'replayable'
       and all('restore or regenerate' not in e['remedy'] for e in u1),
       {'availability': RS['run']['availability'], 'sealedAssurance': RS['run']['sealedAssurance']})
p1b = preview(NATIVE_B)
u1b = p1b['descriptor']['unmetPreconditions']
record('C1b.different-exact-cause-gives-a-different-remedy-under-the-same-code',
       len(u1b) == 1 and u1b[0]['code'] == u1[0]['code'] and u1b[0]['remedy'] != u1[0]['remedy']
       and 'external-consumers-unknown' in u1b[0]['remedy'],
       {'codeEqual': u1b[0]['code'] == u1[0]['code'], 'remedyA': u1[0]['remedy'],
        'remedyB': u1b[0]['remedy']})
record('C1b.the-two-plans-are-different-repairPlanIds',
       p1['repairPlanId'] != p1b['repairPlanId'],
       {'a': p1['repairPlanId'][:24] + '...', 'b': p1b['repairPlanId'][:24] + '...'})

# --- C2: unsatisfied IMPORTED-plane requirement
p2 = preview(IMPORTED)
u2 = p2['descriptor']['unmetPreconditions']
record('C2.imported-plane-requirement-reaches-the-same-code-with-its-own-plane-and-cause',
       p2['descriptor']['applicable'] is False and len(u2) == 1 and u2[0]['code'] == CODE
       and u2[0]['remedy'] == 'evidence requirement unsatisfied: history-change@observed '
                              '(imported: import-unmapped-only)',
       {'entries': len(u2), 'code': u2[0]['code'], 'remedy': u2[0]['remedy']})

# --- C3: available Run, every requirement satisfied
p3 = preview(SATISFIED)
d3 = p3['descriptor']
record('C3.available-run-all-satisfied-is-applicable-with-zero-entries',
       d3['applicable'] is True and d3['unmetPreconditions'] == [],
       {'applicable': d3['applicable'], 'entries': len(d3['unmetPreconditions'])})

# --- C4: unavailable Run, every requirement satisfied
p4 = preview(SATISFIED, availability='purged')
u4 = p4['descriptor']['unmetPreconditions']
record('C4.unavailable-run-emits-the-same-code-with-the-retention-remedy',
       p4['descriptor']['applicable'] is False and len(u4) == 1 and u4[0]['code'] == CODE
       and u4[0]['remedy'] == 'restore or regenerate the Run evidence; assurance must be replayable',
       {'entries': len(u4), 'code': u4[0]['code'], 'remedy': u4[0]['remedy']})
record('C4.the-purged-run-entry-does-not-carry-the-identity-owned-purge-code',
       u4[0]['code'] != 'evidence.purged',
       {'emitted': u4[0]['code'], 'notEmitted': 'evidence.purged (owner: identity)'})

# --- C5: both branches at once -> two entries, one code, two remedies
p5 = preview(NATIVE_A, availability='purged')
u5 = p5['descriptor']['unmetPreconditions']
record('C5.retention-and-per-requirement-branches-coexist-as-two-distinguishable-entries',
       len(u5) == 2 and {e['code'] for e in u5} == {CODE}
       and len({e['remedy'] for e in u5}) == 2,
       {'entries': len(u5), 'codes': [e['code'] for e in u5], 'remedies': [e['remedy'] for e in u5]})

# --- S1: schema alone admits the empty array the admission never produces
shape_ok, shape_why = valid(U + 'repair#/$defs/RepairPlanDescriptor', d1)
mutated = json.loads(json.dumps(d1))
mutated['unmetPreconditions'] = []
empty_ok, empty_why = valid(U + 'repair#/$defs/RepairPlanDescriptor', mutated)
record('S1.the-emitted-descriptor-is-schema-valid', shape_ok, {'why': shape_why})
record('S1.schema-alone-also-admits-an-unsatisfied-requirement-with-an-EMPTY-array',
       empty_ok,
       {'unsatisfiedRequirements': sum(1 for r in mutated['evidenceRequirements'] if not r['satisfied']),
        'unmetPreconditions': len(mutated['unmetPreconditions']),
        'schemaValid': empty_ok, 'why': empty_why,
        'note': 'shape validity is not condition-code correctness; the admission never emits this'})
mutated_true = json.loads(json.dumps(mutated))
mutated_true['applicable'] = True
true_ok, _ = valid(U + 'repair#/$defs/RepairPlanDescriptor', mutated_true)
record('S1.schema-alone-even-admits-applicable-true-with-an-unsatisfied-requirement',
       true_ok,
       {'schemaValid': true_ok,
        'note': 'the applicable<->requirement law is stated in prose and decided at admission'})
record('S1.no-schema-conditional-couples-applicable-to-unmetPreconditions',
       'allOf' not in SCHEMAS[U + 'repair']['$defs']['RepairPlanDescriptor']
       and 'if' not in SCHEMAS[U + 'repair']['$defs']['RepairPlanDescriptor'],
       {'descriptorKeywords': sorted(SCHEMAS[U + 'repair']['$defs']['RepairPlanDescriptor'].keys())})

# --- S2: the clarification's alternative example, checked against the model
cw_eligible = dict(RS['run']['closedWorld'])
codes5 = [e['code'] for e in u5] + [e['code'] for e in u1] + [e['code'] for e in u2]
record('S2.model-never-names-the-closed-world-code-while-deadCodeRepairEligible-is-true',
       cw_eligible['deadCodeRepairEligible'] is True
       and 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED' not in codes5
       and any(e['action'] in M.UNSAFE_ACTIONS for e in d1['edits']),
       {'deadCodeRepairEligible': cw_eligible['deadCodeRepairEligible'],
        'planContainsUnsafeAction': sorted({e['action'] for e in d1['edits']}),
        'codesObserved': sorted(set(codes5))})
cw_ineligible = dict(cw_eligible, deadCodeRepairEligible=False, reasons=['entry-points-unknown'])
p6 = preview(SATISFIED, closed_world=cw_ineligible)
u6 = p6['descriptor']['unmetPreconditions']
record('S2.the-closed-world-code-is-reserved-for-its-own-gate-and-fires-only-there',
       len(u6) == 1 and u6[0]['code'] == 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED'
       and 'entry-points-unknown' in u6[0]['remedy'],
       {'entries': len(u6), 'code': u6[0]['code'], 'remedy': u6[0]['remedy']})

# --- authority preservation: descriptor edits do not grant applicability
record('AUTH.evidence-authority-and-plan-binding-are-untouched-by-this-mapping',
       d1['evidenceRunId'] == RS['run']['runId']
       and M.wid('repairplan2', 'workflow.repair-plan', mutated) != p1['repairPlanId'],
       {'evidenceRunId': d1['evidenceRunId'],
        'editingUnmetPreconditionsMintsADifferentRepairPlanId': True})

out = Path(__file__).resolve().parent / 'probe_repair_unmet_mapping.v1.json'
out.write_text(json.dumps({'controls': RESULTS,
                           'allPassed': all(r['ok'] for r in RESULTS),
                           'passed': sum(1 for r in RESULTS if r['ok']),
                           'total': len(RESULTS)}, indent=1) + '\n')
print('\nallPassed=' + str(all(r['ok'] for r in RESULTS))
      + '  ' + str(sum(1 for r in RESULTS if r['ok'])) + '/' + str(len(RESULTS)))
sys.exit(0 if all(r['ok'] for r in RESULTS) else 1)
