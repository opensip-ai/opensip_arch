"""Probe: what repair does with a Run that has more than one retained ClosedWorldV2.

Part A -- cross-RELATION variation inside ONE universe is also admitted (so the
ambiguity is not only a multi-universe artefact).

Part B -- drive the frozen workflows_model.v1.repair_preview twice with the two
ClosedWorldV2 records that probe_two_closed_worlds proved are BOTH retained in the SAME
admitted Run, holding evidenceRunId / targets / edits / requirements fixed. Record the
gate outcome and the minted repairPlanId for each.

Part C -- validate BOTH resulting descriptors against the frozen repair schema, using the
source's own registry construction, to see whether the schema discriminates between them.

Part D -- create-only behaviour, and the all-delete/replace guard, read from the model.

Author synthetic evidence only. No product qualification, no source modification.
"""
import copy, json, glob, importlib.util, sys
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v31')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
WF = SRC / 'docs/coop/design-corrections/workflows'
OUT = Path(__file__).resolve().parent / 'probe-repair-selection.json'

sys.path.insert(0, str(FOUND))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


report = {'scope': 'repair ClosedWorld selection law', 'parts': []}

def step(name, **kw):
    row = {'part': name, **kw}
    report['parts'].append(row)
    print(json.dumps(row, default=str)[:1400])
    return row


# ---------------------------------------------------------------- Part A: one universe,
# two relations, two different ClosedWorldV2 -- still a fully admitted Run.
P = load('probe_replay_check', FOUND / 'check-replay.v3.py')
F, R, M = P.F, P.R, P.M
N = load('probe_native_model', SRC / 'docs/coop/design-corrections/native/native_evidence_model.v2.py')

CLOSED = N.closed_world_v2(package_json={'private': True},
                           entry_points={'state': 'all', 'source': 'explicit'},
                           unresolved=[], external_consumers='none-declared')
OPEN = N.closed_world_v2(package_json={'private': True},
                         entry_points={'state': 'partial', 'source': 'recognized'},
                         unresolved=[], external_consumers='unknown')

_orig_helpers = F.fixture_helpers

def helpers_varying_by_relation():
    H = _orig_helpers()
    base = H.coverage_result

    def coverage_result(scope_descriptor, universe, resolved, blobs=None,
                        inventory_paths=None, unresolved=()):
        payload = base(scope_descriptor, universe, resolved, blobs, inventory_paths, unresolved)
        rel = payload['key']['relation']
        payload['entry']['closedWorld'] = copy.deepcopy(OPEN if rel == 'package' else CLOSED)
        return payload

    H.coverage_result = coverage_result
    return H

F.fixture_helpers = helpers_varying_by_relation
g = F.build_file_inputs()                      # single universe
seed, objects, blobs, _ = F.seal_fixture(g)
_, owner = M.open_run_closure(seed, objects, blobs)
i = g['inputs']
result = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                  i['evaluationInputRefs'], objects, blobs, owner)
run_rec, objects, blobs = P.seal(g, result, objects, blobs)
run_id_a = M.close_run(run_rec, objects, blobs)

evidence = objects[run_rec['evidenceId']][1]
rows = []
for cid in evidence['coverageIds']:
    payload = json.loads(blobs[objects[cid][1]['payloadDigest']])
    rows.append({'relation': payload['key']['relation'],
                 'resolution': payload['key']['resolution'],
                 'sourceUniverse': payload['key']['sourceUniverse'][:12],
                 'deadCodeRepairEligible': payload['entry']['closedWorld']['deadCodeRepairEligible']})
step('A-one-universe-two-relations',
     runId=run_id_a, closeRun='ADMIT', universes=1,
     entries=sorted(rows, key=lambda r: r['relation']),
     distinctDeadCodeRepairEligible=sorted({r['deadCodeRepairEligible'] for r in rows}),
     note='same universe, same snapshot, one Run: the two relations disagree and Run '
          'closure admits it. No cross-entry agreement law was reached.')


# ---------------------------------------------------------------- Part B: repair_preview
# driven with each retained candidate. Everything except closedWorld is held fixed.
W = load('probe_workflows_model', WF / 'workflows_model.v1.py')

# Identifier spellings and the repair scenario come from the FROZEN case file, so nothing
# here invents an identifier shape the schema would reject for an unrelated reason.
CASES = canonical.parse((WF / 'workflow-cases.v1.json').read_bytes())
CONST = dict(CASES['constants'])
RS = CASES['repairScenario']

def _subst(value):
    if isinstance(value, str) and value.startswith('$'):
        return CONST[value[1:]]
    if isinstance(value, list):
        return [_subst(v) for v in value]
    if isinstance(value, dict):
        return {k: _subst(v) for k, v in value.items()}
    return value

TREE = {k: v.encode() for k, v in RS['tree'].items()}
PROJECT = CONST['PRJ']
SNAP = W.tree_snapshot_id(PROJECT, TREE)
TARGETS = _subst(RS['targets'])
RECIPE = _subst(RS['recipe'])
TRUST = {RECIPE['closureId']: 'admitted'}
EDITS = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e)
         for e in RS['edits']]
REQS = _subst(RS['evidenceRequirements'])
SCOPE = list(RS['permittedScope'])

def base_run(cw):
    run = _subst(dict(RS['run']))
    run['snapshotId'] = SNAP
    run['closedWorld'] = copy.deepcopy(cw)
    return run

previews = {}
for label, cw in (('entry-with-deadCodeRepairEligible-true', CLOSED),
                  ('entry-with-deadCodeRepairEligible-false', OPEN)):
    previews[label] = W.repair_preview(PROJECT, TREE, base_run(cw), RECIPE, TARGETS,
                                       copy.deepcopy(EDITS), REQS, SCOPE, TRUST)

a, b = previews['entry-with-deadCodeRepairEligible-true'], previews['entry-with-deadCodeRepairEligible-false']
step('B-two-lawful-candidates-one-run',
     sameEvidenceRunId=a['descriptor']['evidenceRunId'] == b['descriptor']['evidenceRunId'],
     sameTargets=a['descriptor']['targets'] == b['descriptor']['targets'],
     sameEdits=a['descriptor']['edits'] == b['descriptor']['edits'],
     candidateA={'applicable': a['descriptor']['applicable'],
                 'repairPlanId': a['repairPlanId'],
                 'unmetPreconditions': a['descriptor']['unmetPreconditions'],
                 'closedWorldProjection': a['descriptor']['closedWorld']},
     candidateB={'applicable': b['descriptor']['applicable'],
                 'repairPlanId': b['repairPlanId'],
                 'unmetPreconditions': b['descriptor']['unmetPreconditions'],
                 'closedWorldProjection': b['descriptor']['closedWorld']},
     repairPlanIdsDiffer=a['repairPlanId'] != b['repairPlanId'],
     applicabilityFlips=a['descriptor']['applicable'] != b['descriptor']['applicable'])


# ---------------------------------------------------------------- Part C: does the schema
# discriminate? Build the registry exactly as check_workflows.v1.py does.
SCHEMAS = {}
for p in sorted(glob.glob(str(WF / 'schemas' / '*.schema.json'))):
    s = canonical.parse(Path(p).read_bytes())
    Draft202012Validator.check_schema(s)
    SCHEMAS[s['$id']] = s
FOUNDATION = canonical.parse((FOUND / 'identity-schemas.v2.json').read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUNDATION['$id'], Resource(contents=FOUNDATION, specification=DRAFT202012))])

def valid(ref, value):
    sid, _, frag = ref.partition('#')
    v = canonical.ExactValidator({'$ref': sid + '#' + frag} if frag else {'$ref': sid}, registry=REG)
    try:
        canonical.typed(value)
        v.validate(value)
        return True, ''
    except (ValidationError, canonical.AdmissionError) as e:
        return False, str(e).splitlines()[0][:180]

DESC = 'urn:opensip:product-v1:workflows:repair#/$defs/RepairPlanDescriptor'
okA, whyA = valid(DESC, a['descriptor'])
okB, whyB = valid(DESC, b['descriptor'])

# and the literal seven-member copy, which the contract says must be refused
literal = copy.deepcopy(a['descriptor'])
literal['closedWorld'] = copy.deepcopy(CLOSED)
okLit, whyLit = valid(DESC, literal)

step('C-schema-discrimination',
     descriptorSchema='workflows/schemas/repair.schema.json#/$defs/RepairPlanDescriptor',
     candidateAValid=okA, candidateADetail=whyA,
     candidateBValid=okB, candidateBDetail=whyB,
     literalSevenMemberCopyValid=okLit, literalDetail=whyLit,
     note='both candidates validate; the schema closes the projection at five members and '
          'refuses a literal copy, but states no law about WHICH retained entry was projected')


# ---------------------------------------------------------------- Part D: create-only and
# the all-delete/replace guard, exercised on the frozen model.
create_only = W.repair_preview(
    PROJECT, TREE, base_run(OPEN), RECIPE, TARGETS,
    [{'path': 'src/d.ts', 'action': 'create', 'postimage': b'export const d = 4;\n'}],
    REQS, SCOPE, TRUST)
mixed = W.repair_preview(
    PROJECT, TREE, base_run(OPEN), RECIPE, TARGETS,
    [{'path': 'src/d.ts', 'action': 'create', 'postimage': b'export const d = 4;\n'},
     {'path': 'src/a.ts', 'action': 'delete'}],
    REQS, SCOPE, TRUST)
step('D-create-only-and-guard',
     unsafeActions=sorted(W.UNSAFE_ACTIONS),
     createOnlyApplicableUnderIneligibleClosedWorld=create_only['descriptor']['applicable'],
     createOnlyUnmet=create_only['descriptor']['unmetPreconditions'],
     mixedPlanApplicable=mixed['descriptor']['applicable'],
     mixedUnmet=mixed['descriptor']['unmetPreconditions'],
     note='the gate fires on ANY delete/replace in the plan; a create-only plan does not '
          'read closedWorld at all, so the selection question does not arise for it')


# ---------------------------------------------------------------- Part E: negative checks
# the two caller errors the singular-field adapter cannot presently distinguish.
def attempt(label, mutate):
    run = base_run(CLOSED)
    mutate(run)
    try:
        plan = W.repair_preview(PROJECT, TREE, run, RECIPE, TARGETS, copy.deepcopy(EDITS),
                                REQS, SCOPE, TRUST)
        return {'case': label, 'outcome': 'PREVIEWED',
                'applicable': plan['descriptor']['applicable'],
                'closedWorldProjection': plan['descriptor']['closedWorld']}
    except W.Refusal as r:
        return {'case': label, 'outcome': 'REFUSAL', 'detail': r.detail, 'remedy': r.remedy}
    except Exception as exc:
        return {'case': label, 'outcome': 'UNTYPED-' + type(exc).__name__, 'detail': str(exc)[:160]}

def drop(run):
    run.pop('closedWorld')

def five_member(run):
    run['closedWorld'] = {k: CLOSED[k] for k in
                          ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
                           'nonliteralLoading', 'externalConsumers')}

step('E-negative-checks',
     noEvidenceRecordAtAll=attempt('run carries no closedWorld', drop),
     descriptorProjectionFedBackAsEvidence=attempt('run carries the 5-member projection', five_member),
     note='neither is a typed repair refusal today: the first is an untyped KeyError and '
          'the second is silently accepted as if it were the seven-member evidence record')

OUT.write_text(json.dumps(report, indent=2, default=str) + '\n')
print('\nWROTE', OUT)
