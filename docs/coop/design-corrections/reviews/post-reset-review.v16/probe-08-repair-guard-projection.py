#!/usr/bin/env python3
"""Probe 08 (independent): CB5-SHOULD-2 / CX-BV5-03 / BV5A-NEW-2.

Claims under test, on the exact frozen bytes:
  1. The unsafe-repair guard covers EVERY delete and EVERY replace, unqualified.
  2. Eligibility and reasons are read from the evidence Run's FULL native
     ClosedWorldV2 (seven members), BEFORE any descriptor exists.
  3. dynamicDispatch is target-relative and does NOT globally veto an otherwise
     eligible unsafe repair on an unrelated target.
  4. The descriptor closedWorld is exactly the five named fields; a literal
     seven-member copy is schema-REFUSED; a dropped member is schema-invalid.
  5. A copied boolean, a dropped field or a detached descriptor cannot authorize
     destructive repair.
  6. Both reference fixture repairScenario closedWorld records now carry all
     seven normative ClosedWorldV2 members.
"""
import copy, hashlib, importlib.util, json, os, sys

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

spec = importlib.util.spec_from_file_location('rev16_wf', os.path.join(DC, 'workflows/workflows_model.v1.py'))
W = importlib.util.module_from_spec(spec)
sys.modules['rev16_wf'] = W
spec.loader.exec_module(W)

REPAIR_SCHEMA = json.load(open(os.path.join(DC, 'workflows/schemas/repair.schema.json')))
NATIVE_SCHEMAS = json.load(open(os.path.join(DC, 'native/native-evidence.schemas.v2.json')))
CASES_FIXTURE = json.load(open(os.path.join(DC, 'workflows/workflow-cases.v1.json')))

import jsonschema

FULL_CW = {'deadCodeRepairEligible': True, 'exportsClosed': 'closed',
           'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
           'externalConsumers': 'none-declared', 'dynamicDispatch': 'not-applicable',
           'reasons': []}
PROJECTED = ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
             'nonliteralLoading', 'externalConsumers')

TREE = {'src/a.ts': b'export const a = 1;\n', 'src/b.ts': b'export const b = 2;\n'}
PROJECT = 'proj-1'
SNAP = W.fixture_tree_snapshot_id(PROJECT, TREE)

def make_run(cw, findings=('fp-1',), origin='native-analysis'):
    return {'authority': 'authoritative', 'availability': 'retained',
            'sealedAssurance': 'replayable', 'runId': 'run2:' + 'a' * 64,
            'planId': 'plan2:' + 'b' * 64, 'findings': list(findings),
            'snapshotId': SNAP, 'closedWorld': cw, 'evidenceOrigin': origin}

RECIPE = {'closureId': 'closure2:' + 'c' * 64}
TRUST = {RECIPE['closureId']: 'admitted'}

EDITS = {
    'delete-only': [{'path': 'src/b.ts', 'action': 'delete'}],
    'replace-only': [{'path': 'src/a.ts', 'action': 'replace', 'postimage': b'export const a = 9;\n'}],
    'create-only': [{'path': 'src/c.ts', 'action': 'create', 'postimage': b'export const c = 3;\n'}],
    'delete-and-create': [{'path': 'src/b.ts', 'action': 'delete'},
                          {'path': 'src/c.ts', 'action': 'create', 'postimage': b'x'}],
}

def preview(cw, edits_key, origin='native-analysis'):
    run = make_run(cw, origin=origin)
    return W.repair_preview(PROJECT, TREE, run, RECIPE, ['fp-1'], copy.deepcopy(EDITS[edits_key]),
                            [], ['src/**'], TRUST)

rows = []
def case(cid, group, cw, edits_key, exp_gated, why, origin='native-analysis'):
    try:
        out = preview(cw, edits_key, origin)
        codes = [u['code'] for u in out['descriptor']['unmetPreconditions']]
        gated = 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED' in codes
        rows.append({'id': cid, 'group': group, 'edits': edits_key,
                     'closedWorld': cw, 'evidenceOrigin': origin,
                     'expectedClosedWorldGate': exp_gated, 'observedClosedWorldGate': gated,
                     'agrees': gated == exp_gated, 'applicable': out['descriptor']['applicable'],
                     'unmetPreconditions': out['descriptor']['unmetPreconditions'],
                     'descriptorClosedWorld': out['descriptor']['closedWorld'],
                     'repairPlanId': out['repairPlanId'], 'why': why, 'error': None})
    except Exception as e:
        rows.append({'id': cid, 'group': group, 'edits': edits_key, 'closedWorld': cw,
                     'expectedClosedWorldGate': exp_gated, 'observedClosedWorldGate': None,
                     'agrees': False, 'error': type(e).__name__ + ':' + str(e)[:300], 'why': why})

INELIGIBLE = dict(FULL_CW, deadCodeRepairEligible=False, exportsClosed='open',
                  entryPointsRecognized='partial',
                  reasons=['exports-not-closed', 'entry-points-partial'])

# 1/2. every delete and every replace is guarded; create is not
case('R1-delete-only-ineligible', 'guard scope: EVERY delete', INELIGIBLE, 'delete-only', True,
     'a delete of a NON-exported subject is still an unsafe action')
case('R2-replace-only-ineligible', 'guard scope: EVERY replace', INELIGIBLE, 'replace-only', True,
     'replace is unqualified in UNSAFE_ACTIONS; not narrowed to exported subjects')
case('R3-create-only-ineligible', 'guard scope: create is NOT unsafe', INELIGIBLE, 'create-only', False,
     'NEGATIVE CONTROL: a create-only plan must not be gated even when ineligible')
case('R4-mixed-delete-create-ineligible', 'guard scope: one unsafe edit gates the plan',
     INELIGIBLE, 'delete-and-create', True, 'any() over the plan, not all()')
case('R5-delete-only-eligible', 'POSITIVE CONTROL: eligible unsafe repair admits',
     FULL_CW, 'delete-only', False, 'deadCodeRepairEligible=true from the FULL native record')
case('R6-replace-only-eligible', 'POSITIVE CONTROL: eligible replace admits',
     FULL_CW, 'replace-only', False, 'decidable from full evidence')

# 3. dynamicDispatch is target-relative, not a global veto
for dd in ('present', 'not-applicable', 'absent', 'unknown'):
    case(f'R7-dynamicDispatch-{dd}', 'dynamicDispatch is TARGET-RELATIVE, not a global veto',
         dict(FULL_CW, dynamicDispatch=dd), 'delete-only', False,
         'dynamicDispatch alone must not veto an otherwise eligible unsafe repair on an '
         'unrelated target')
case('R8-dynamicDispatch-present-but-ineligible',
     'dynamicDispatch does not RESCUE an ineligible plan either',
     dict(INELIGIBLE, dynamicDispatch='present'), 'delete-only', True,
     'the gate still reads deadCodeRepairEligible')

# imported DECLARED prepared expansion is still not authority for an unsafe repair
case('R9-imported-declared-origin', 'preserved: imported declared expansion is not repair authority',
     FULL_CW, 'delete-only', True,
     'origin imported-prepared-declared adds CLOSED_WORLD_NOT_ESTABLISHED even when eligible',
     origin='imported-prepared-declared')

# 4/5. projection exactness and the schema's refusal of a literal copy / dropped member
cw_schema = REPAIR_SCHEMA['$defs']['RepairPlanDescriptor']['properties']['closedWorld']
proj_checks = []
def schema_case(cid, value, exp_valid, why):
    try:
        jsonschema.Draft202012Validator(cw_schema).validate(value)
        got, err = True, None
    except jsonschema.ValidationError as e:
        got, err = False, str(e.message)[:220]
    proj_checks.append({'id': cid, 'value': value, 'expectedValid': exp_valid,
                        'observedValid': got, 'agrees': got == exp_valid,
                        'error': err, 'why': why})

schema_case('S1-exact-projection', {k: FULL_CW[k] for k in PROJECTED}, True,
            'the exact five-field projection is the only admitted shape')
schema_case('S2-literal-seven-member-copy', dict(FULL_CW), False,
            'a literal copy of ClosedWorldV2 is REFUSED (additionalProperties false)')
schema_case('S3-copy-plus-dynamicDispatch',
            dict({k: FULL_CW[k] for k in PROJECTED}, dynamicDispatch='present'), False,
            'a detached dynamicDispatch cannot be smuggled into the descriptor')
schema_case('S4-copy-plus-reasons',
            dict({k: FULL_CW[k] for k in PROJECTED}, reasons=[]), False,
            'a detached reasons list cannot be smuggled into the descriptor')
for drop in PROJECTED:
    v = {k: FULL_CW[k] for k in PROJECTED if k != drop}
    schema_case(f'S5-drop-{drop}', v, False, 'a dropped required member is schema-invalid')
schema_case('S6-copied-boolean-only', {'deadCodeRepairEligible': True}, False,
            'a copied boolean alone is not a descriptor and authorizes nothing')

# the model's projection must equal the schema-required set, exactly
model_src = open(os.path.join(DC, 'workflows/workflows_model.v1.py')).read()
projection_line = [l for l in model_src.splitlines() if "'closedWorld': {k: cw[k] for k in" in l]
schema_required = tuple(cw_schema['required'])

# an eligible plan's descriptor must project exactly, and must NOT carry the dropped members
ok_out = preview(dict(FULL_CW, dynamicDispatch='present', reasons=['x']), 'delete-only')
desc_cw = ok_out['descriptor']['closedWorld']

# 6. BV5A-NEW-2: both fixture repairScenario closedWorld records carry seven members
native_cw = NATIVE_SCHEMAS['$defs']['ClosedWorldV2']
native_required = sorted(native_cw['required'])
fixture_cws = []
def collect(o, p=''):
    if isinstance(o, dict):
        if 'closedWorld' in o and isinstance(o['closedWorld'], dict):
            fixture_cws.append({'at': p + '/closedWorld', 'members': sorted(o['closedWorld']),
                                'value': o['closedWorld']})
        for k, v in o.items():
            collect(v, p + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            collect(v, p + f'[{i}]')
collect(CASES_FIXTURE)
for fc in fixture_cws:
    fc['carriesAllSevenNormativeMembers'] = fc['members'] == native_required
    try:
        jsonschema.Draft202012Validator(native_cw).validate(fc['value'])
        fc['validatesAgainstNativeClosedWorldV2'] = True
    except jsonschema.ValidationError as e:
        fc['validatesAgainstNativeClosedWorldV2'] = False
        fc['nativeValidationError'] = str(e.message)[:200]

res = {
    'probe': 'probe-08-repair-guard-projection',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': {p: sha256(os.path.join(DC, p)) for p in [
        'workflows/workflows_model.v1.py', 'workflows/schemas/repair.schema.json',
        'workflows/workflow-cases.v1.json', 'native/native-evidence.schemas.v2.json']},
    'unsafeActions': sorted(W.UNSAFE_ACTIONS),
    'previewCases': len(rows),
    'previewAgree': sum(1 for r in rows if r['agrees']),
    'previewDisagree': [r for r in rows if not r['agrees']],
    'schemaCases': len(proj_checks),
    'schemaAgree': sum(1 for c in proj_checks if c['agrees']),
    'schemaDisagree': [c for c in proj_checks if not c['agrees']],
    'projectionSourceLine': projection_line,
    'schemaRequiredProjection': list(schema_required),
    'modelProjectionEqualsSchemaRequired': sorted(PROJECTED) == sorted(schema_required),
    'observedDescriptorClosedWorldFromSevenMemberEvidence': desc_cw,
    'descriptorDropsDynamicDispatchAndReasons': (
        'dynamicDispatch' not in desc_cw and 'reasons' not in desc_cw
        and sorted(desc_cw) == sorted(schema_required)),
    'nativeClosedWorldV2Required': native_required,
    'fixtureClosedWorldRecords': fixture_cws,
    'fixtureRecordsAllSeven': all(f['carriesAllSevenNormativeMembers'] for f in fixture_cws),
    'rows': rows, 'schemaChecks': proj_checks,
    'notProductQualification': True,
    'scope': 'Pure reference admission over synthetic in-memory inputs. NOT real host enforcement: '
             'no filesystem mutation, no authorization service, no product repair was executed.',
}
with open(os.path.join(OUT, 'probe-08-repair-guard-projection.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ('rows', 'schemaChecks')},
                 indent=2, sort_keys=True, default=str))
