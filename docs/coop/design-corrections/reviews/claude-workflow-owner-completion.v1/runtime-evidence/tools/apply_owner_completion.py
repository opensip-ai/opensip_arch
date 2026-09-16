"""Owner completion edits over the fixed capture copy.

Q1: evaluator3 repair:2 constructor at the workflow owner entry point (workflows_model.v3.repair_preview) with plan
    admission; historical workflows_model.v1.repair_preview keeps major 1 by default.
Q2: policy-test suite admission route: errorCode CONFIG.INVALID always; detail POLICY.IMPERATIVE_KEY_REFUSED for a
    candidate-policy grammar violation, otherwise the registered shared CONFIG.INVALID detail; resolver refusals are
    request rejections (existing goldens), so only resolver-accepted results are carried.
"""
import copy, json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1/tools')
import textedit as T  # noqa: E402

DRY = '--dry' in sys.argv


def apply(label, rel, pairs):
    """--dry: every anchor must occur exactly once before ANY file is written; otherwise the exact-once helper."""
    if DRY:
        text = (T.ROOT / rel).read_text()
        bad = [(i, text.count(old), old[:80]) for i, (old, _) in enumerate(pairs) if text.count(old) != 1]
        if bad:
            raise SystemExit('DRY %s: %s anchors not exactly once: %r' % (label, rel, bad))
        return {'label': label, 'path': rel, 'dry': True, 'replacements': len(pairs)}
    return T.apply(label, rel, pairs)


def edit_json(label, rel, fn):
    if DRY:
        fn(copy.deepcopy(json.loads((T.ROOT / rel).read_text())))
        return {'label': label, 'path': rel, 'dry': True}
    return T.edit_json(label, rel, fn)

WF = 'docs/coop/design-corrections/workflows/'
V1 = WF + 'workflows_model.v1.py'
V3 = WF + 'workflows_model.v3.py'
CWP = WF + 'check-workflow-projection.v3.py'
WPC = WF + 'workflow-projection-contract.v3.md'
ENV = WF + 'schemas/evaluator3/command-envelope.schema.json'
INV = WF + 'command-inventory.v3.json'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
rows = []

# ------------------------------------------------------------------ Q1 historical builder: additive keyword, default 1
rows.append(apply('Q1 v1 builder descriptor major keyword', V1, [
    ('''def repair_preview(project_id, snapshot_tree, run, recipe, targets, edits, evidence_requirements, permitted_scope, trust, ephemeral=False):
    """trust: the security unit's current admitted closure set {closureId: 'admitted'|'revoked'}; ABSENCE is not admission.
''', '''def repair_preview(project_id, snapshot_tree, run, recipe, targets, edits, evidence_requirements, permitted_scope, trust, ephemeral=False, *, descriptor_major=1):
    """trust: the security unit's current admitted closure set {closureId: 'admitted'|'revoked'}; ABSENCE is not admission.

    descriptor_major: 1 (the default) is the HISTORICAL major-1 plan, and every existing caller keeps it byte-identically.
    Only the evaluator3 owner (workflows_model.v3.repair_preview) passes 2, after its own retained-Run joins, so the
    descriptor is BUILT at its major before the repairPlanId preimage exists; no plan is relabelled or reminted.
'''),
    ('''    unmet = []
    if ephemeral or run.get('authority') != 'authoritative':''', '''    if descriptor_major not in (1, 2):
        raise ValueError('repair plan descriptor major is 1 (historical) or 2 (evaluator3)')
    unmet = []
    if ephemeral or run.get('authority') != 'authoritative':'''),
    ("""    desc = {'schemaFamily': 'opensip.product.repair-plan', 'schemaMajor': 1, 'projectId': project_id,""",
     """    desc = {'schemaFamily': 'opensip.product.repair-plan', 'schemaMajor': descriptor_major, 'projectId': project_id,"""),
]))

# ------------------------------------------------------------------ Q1 + Q2 current owner entry points
V3_APPEND = r'''
# ---------------------------------------------------------- evaluator3 repair:2 plan constructor
# The CURRENT preview owner. workflows_model.v1.repair_preview stays the historical major-1 constructor for every
# historical caller (check_workflows.v1, the integration host adapter). This profile builds the descriptor at major 2
# (evidenceRunId run3) and admits the plan before returning it; nothing is relabelled or reminted after identity.
from jsonschema import ValidationError
REPAIR_PLAN_MAJOR=2
REPAIR_PLAN_REF='urn:opensip:product-v1:workflows:evaluator3:repair:2#/$defs/RepairPlanV1'
_PROJECTION=None
def projection_owner():
    """The evaluator3 projection owner: the repair target law (project_repair_targets) and the evaluator3 schema registry."""
    global _PROJECTION
    if _PROJECTION is None:
        spec=importlib.util.spec_from_file_location('workflow_projection_owner3',PROFILE_ROOT/'workflow_projection_model.v3.py')
        _PROJECTION=importlib.util.module_from_spec(spec);spec.loader.exec_module(_PROJECTION)
    return _PROJECTION

def admit_repair_plan_v2(plan):
    """Current preview admission of one RepairPlanV1: repair:2 only, the closed schema, and a repairPlanId that recomputes.
    A historical major-1 plan refuses typed and is never coerced; a relabelled plan whose id was not re-derived is corrupt."""
    desc=plan.get('descriptor') if isinstance(plan,dict) else None
    if isinstance(desc,dict) and desc.get('schemaMajor')!=REPAIR_PLAN_MAJOR:
        raise Refusal('REQUEST.SCHEMA_MAJOR_UNSUPPORTED','EVALUATION.MIXED_OUTPUT_MAJOR','evaluator3 repair admits repair:2 RepairPlanV1 only; a historical major-1 plan is not coerced',str(desc.get('schemaMajor')))
    try:projection_owner().validate_profile(REPAIR_PLAN_REF,plan)
    except (ValidationError,canonical.AdmissionError) as exc:
        raise Refusal('CONFIG.INVALID','IMPORT.ARTIFACT_CORRUPT','the plan does not satisfy repair:2 RepairPlanV1') from exc
    if plan['repairPlanId']!=wid('repairplan2','workflow.repair-plan',desc):
        raise Refusal('CONFIG.INVALID','IMPORT.ARTIFACT_CORRUPT','repairPlanId does not recompute from the descriptor',plan['repairPlanId'])
    return plan

def repair_preview(project_id,snapshot_tree,run,recipe,targets,edits,evidence_requirements,permitted_scope,trust,ephemeral=False):
    """Evaluator3 repair preview: the owner-produced, admitted repair:2 RepairPlanV1.

    Before any descriptor exists: authority (exactly as the historical profile), the retained closure of the evidence
    Run, a run3 evidence Run whose planId is the retained Run's, and every target a matched finding-key2 of THAT
    retained Run with compatible metadata (workflow-projection-contract section 5). The closed-world gate, edits, trust
    and requirements then run through the shared builder with this profile's retained-record selector installed, at
    descriptor major 2, and the plan is admitted before it is returned."""
    if ephemeral or run.get('authority')!='authoritative':
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE','run an authoritative analysis first')
    retained=run.get('retained')
    if retained is None:
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                      'evaluator3 repair preview requires the retained closure of the evidence Run; a caller-selected closed-world record is not admitted here')
    if not str(run.get('runId','')).startswith('run3:'):
        raise Refusal('REQUEST.SCHEMA_MAJOR_UNSUPPORTED','EVALUATION.MIXED_OUTPUT_MAJOR','a repair:2 plan names an authoritative run3 evidence Run',str(run.get('runId')))
    if run.get('planId')!=retained.run.get('planId'):
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_UNAVAILABLE','the retained closure is not the evidence Run this request names',str(run.get('planId')))
    P=projection_owner()
    try:matched=[{'findingId':fid,'finding':f} for fid,f in retained.matched_findings()]
    except Exception as exc:
        if type(exc).__name__!='RetainedEvidenceUnavailable':raise
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_UNAVAILABLE','a retained finding the target join must read is unavailable: '+str(exc)) from exc
    try:P.project_repair_targets(sorted(set(targets)),matched)
    except P.Refusal as exc:raise Refusal(exc.error_code,exc.detail,exc.remedy,exc.subject) from exc
    return admit_repair_plan_v2(_base.repair_preview(project_id,snapshot_tree,run,recipe,targets,edits,evidence_requirements,permitted_scope,trust,ephemeral,descriptor_major=REPAIR_PLAN_MAJOR))

# ---------------------------------------------------------- policy.test suite admission
# errorCode is CONFIG.INVALID (D9 rejection cause config-invalid) for every suite refusal. The DomainDetail is a separate
# registered code: POLICY.IMPERATIVE_KEY_REFUSED for a candidate-policy grammar violation (workflows-and-surfaces section 5),
# otherwise the shared registered CONFIG.INVALID detail. Resolver refusals of an admitted suite keep their own details.
POLICY_TEST_SUITE_REF='urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestSuiteV1'
_POLICY_GRAMMAR=None
def _policy_grammar():
    global _POLICY_GRAMMAR
    if _POLICY_GRAMMAR is None:_POLICY_GRAMMAR=json.loads((PROFILE_ROOT/'schemas'/'policy-document.schema.json').read_text())
    return _POLICY_GRAMMAR

def _grammar_alternatives(nodes,doc):
    """Leaf alternatives admitted at one position: local $refs resolved, oneOf/anyOf/allOf flattened; a non-local $ref is opaque."""
    out,stack=[],list(nodes)
    while stack:
        n=stack.pop()
        if not isinstance(n,dict):continue
        ref=n.get('$ref')
        if isinstance(ref,str):
            stack.append(doc['$defs'][ref.split('/')[-1]]) if ref.startswith('#/$defs/') else out.append({'opaque':True})
            continue
        combined=[c for k in ('oneOf','anyOf','allOf') for c in n.get(k,[])]
        stack.extend(combined)
        if not combined or any(k in n for k in ('type','properties','items','const','enum')):out.append(n)
    return out

def _admits_scalar(a):
    if a.get('opaque'):return True
    if 'properties' in a or 'items' in a:return False
    t=a.get('type')
    return t is None or t=='string' or (isinstance(t,list) and 'string' in t)

def policy_grammar_violation(value,nodes=None,doc=None):
    """True exactly when the closed policy grammar admits the value under NO alternative at its position for one of the two
    reasons section 5 names: an object member that no closed alternative at that position declares (a hook, script,
    include or exec key), or a string where every alternative is an object (a string expression). Every other schema
    failure (a wrong enum value, a missing member, a bound) is not a grammar violation."""
    doc=doc or _policy_grammar()
    alts=_grammar_alternatives(nodes if nodes is not None else [doc['$defs']['PolicyDocumentV1']],doc)
    objects=[a for a in alts if a.get('type')=='object' or 'properties' in a]
    if isinstance(value,str):
        return bool(objects) and not any(_admits_scalar(a) for a in alts)
    if isinstance(value,dict):
        if not objects:return False
        declared=set().union(*(set(a.get('properties',{})) for a in objects))
        if all(a.get('additionalProperties') is False for a in objects) and set(value)-declared:return True
        return any(policy_grammar_violation(v,[a['properties'][k] for a in objects if k in a.get('properties',{})],doc) for k,v in value.items())
    if isinstance(value,list):
        items=[a['items'] for a in alts if isinstance(a.get('items'),dict)]
        return bool(items) and any(policy_grammar_violation(v,items,doc) for v in value)
    return False

def admit_policy_test_suite(suite):
    """policy.test admission, before any evaluation (workflows-and-surfaces section 5)."""
    try:
        projection_owner().validate_profile(POLICY_TEST_SUITE_REF,suite)
        return suite
    except (ValidationError,canonical.AdmissionError) as exc:
        policy=suite.get('candidatePolicy') if isinstance(suite,dict) else None
        if policy is not None and policy_grammar_violation(policy):
            raise Refusal('CONFIG.INVALID','POLICY.IMPERATIVE_KEY_REFUSED','the policy DSL is declarative data only') from exc
        raise Refusal('CONFIG.INVALID','CONFIG.INVALID','correct the suite so it satisfies PolicyTestSuiteV1') from exc

def run_admitted_policy_test(suite):
    """policy.test: admit the suite, then run the authoring test. A resolver refusal returns (result, refusal) and terminates
    request-rejected with its own detail (goldens policy-test-duplicate-waiver, policy-test-imperative-key); only a
    resolver-accepted result is a policy-test-result carrier."""
    return run_policy_test(admit_policy_test_suite(suite))
'''
rows.append(apply('Q1+Q2 current owner entry points', V3, [
    ('''_base.CLOSED_WORLD_SELECTOR=evaluator3_closed_world
CLOSED_WORLD_SELECTOR=evaluator3_closed_world
''', '''_base.CLOSED_WORLD_SELECTOR=evaluator3_closed_world
CLOSED_WORLD_SELECTOR=evaluator3_closed_world
''' + V3_APPEND),
]))


# ------------------------------------------------------------------ Q2 carrier closure and golden (owner mirrors)
def close_policy_test_record(doc):
    rec = doc['$defs']['PolicyTestResultRecordV1']
    assert rec['description'] == 'policy test: the complete PolicyTestResultV1.' and 'allOf' not in rec
    rec['allOf'] = [{'properties': {'result': {'required': ['resolverAccepted'], 'properties': {'resolverAccepted': {'const': True}}}}}]
    rec['description'] = ('policy test: the complete PolicyTestResultV1 of a resolver-accepted suite. A suite admission or resolver refusal '
                          'terminates request-rejected CONFIG.INVALID with its detail (workflows-and-surfaces section 5; goldens '
                          'policy-test-duplicate-waiver, policy-test-imperative-key, policy-test-suite-inadmissible) and is never carried here.')


rows.append(edit_json('Q2 policy-test carrier accepted-only', ENV, close_policy_test_record))


def add_residual_golden(doc):
    ids = [g['id'] for g in doc['goldens']]
    assert 'policy-test-suite-inadmissible' not in ids
    at = ids.index('policy-test-imperative-key') + 1
    doc['goldens'].insert(at, {
        'id': 'policy-test-suite-inadmissible', 'command': 'policy-test',
        'situation': 'the suite fails PolicyTestSuiteV1 admission and the candidate policy has no grammar violation',
        'class': 'request-rejected', 'exitCode': 2, 'errorCode': 'CONFIG.INVALID', 'domainDetail': 'CONFIG.INVALID',
        'remedy': 'correct the suite so it satisfies PolicyTestSuiteV1'})


rows.append(edit_json('Q2 residual suite admission golden', INV, add_residual_golden))

# ------------------------------------------------------------------ prose
rows.append(apply('Q1+Q2 workflows-and-surfaces', WS, [
    ('''`enforcementUnchanged=true`; the same suite always yields the same result identity.
''', '''`enforcementUnchanged=true`; the same suite always yields the same result identity.
Admission precedes evaluation. Every refusal is `request-rejected` (exit 2) with `errorCode`
`CONFIG.INVALID`, the D9 rejection cause `config-invalid`; the `DomainDetail` is a separate
registered code. A candidate policy carrying a member that no closed alternative of the policy
grammar declares at that position, or a string where the grammar admits only a predicate object,
is `POLICY.IMPERATIVE_KEY_REFUSED`. Any other `PolicyTestSuiteV1` admission failure carries the
shared registered `CONFIG.INVALID` detail; the public detail registry row is registered by
security, and the native route registry reuses the same detail for external configuration. An
admitted suite whose candidate policy or waivers the resolver refuses terminates the same way
with the resolver's detail (`POLICY.DUPLICATE_WAIVER`, `POLICY.UNKNOWN_RULE`,
`IMPORT.ABSENT_FOR_PREDICATE`); its `resolverAccepted=false` result records the refusal but is
not a query carrier.
'''),
    ('''signal alone never authorizes deletion. Preview never writes.''',
     '''signal alone never authorizes deletion. Preview never writes. In the evaluator3 profile the plan is
`repair:2` (`evidenceRunId` `run3`): the evaluator3 workflow owner joins the targets to matched
`finding-key2` fingerprints of the retained evidence Run (workflow projection contract §5), builds
the descriptor at that major and admits the plan before returning it. The historical major-1 plan
keeps its own constructor and schema, and neither is relabelled into the other.'''),
    ('''` / `PolicyTestResultRecordV1`: `result` (`PolicyTestResultV1`) |''',
     '''` / `PolicyTestResultRecordV1`: `result` (`PolicyTestResultV1`, `resolverAccepted=true` only) |'''),
    ('''`policy-test` a suite that fails `PolicyTestSuiteV1` admission `CONFIG.INVALID` with the registered
`CONFIG.INVALID` detail (candidate-policy and waiver resolver refusals are result data with
`resolverAccepted=false`);''', '''`policy-test` the suite admission and resolver refusals of §5 (`CONFIG.INVALID` with
`POLICY.IMPERATIVE_KEY_REFUSED`, the shared `CONFIG.INVALID` detail, or the resolver's `POLICY.*` /
`IMPORT.ABSENT_FOR_PREDICATE` detail; only a `resolverAccepted=true` result is carried);'''),
    ('''| duplicate waiver / imperative policy key | request-rejected 2 | `CONFIG.INVALID` | `POLICY.DUPLICATE_WAIVER` / `POLICY.IMPERATIVE_KEY_REFUSED` |
''', '''| duplicate waiver / imperative policy key | request-rejected 2 | `CONFIG.INVALID` | `POLICY.DUPLICATE_WAIVER` / `POLICY.IMPERATIVE_KEY_REFUSED` |
| policy test suite otherwise inadmissible | request-rejected 2 | `CONFIG.INVALID` | `CONFIG.INVALID` (shared registered detail) |
'''),
]))
rows.append(apply('Q1 projection contract constructor selector', WPC, [
    ('''- Several configurations, one fingerprint: compatible metadata (ruleId, subjectPath, kind, qualifiedName, ruleClosure) or `REPAIR.TARGET_METADATA_AMBIGUOUS`. Do not collapse `parameterDigest`.
''', '''- Several configurations, one fingerprint: compatible metadata (ruleId, subjectPath, kind, qualifiedName, ruleClosure) or `REPAIR.TARGET_METADATA_AMBIGUOUS`. Do not collapse `parameterDigest`.
- Preview constructor: `workflows_model.v3.repair_preview` is the evaluator3 owner entry. Before any descriptor it refuses non-authoritative evidence (`REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE`), a missing retained closure or a retained closure of another Run (`REPAIR.EVIDENCE_RUN_UNAVAILABLE`), a non-run3 evidence Run (`REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `EVALUATION.MIXED_OUTPUT_MAJOR`) and the two target refusals above over the retained matched findings. It builds the descriptor at major 2 through the shared builder and returns only a plan that `admit_repair_plan_v2` admits: repair:2 schema and a recomputed `repairPlanId`. A major-1 plan refuses `EVALUATION.MIXED_OUTPUT_MAJOR`, and an unreminted relabel refuses `CONFIG.INVALID` / `IMPORT.ARTIFACT_CORRUPT`. `workflows_model.v1.repair_preview` remains the historical major-1 constructor (`descriptor_major` defaults to 1).
'''),
]))

# ------------------------------------------------------------------ checker: stale statements, relabel removal, controls
OC1 = r'''
# ------------------------------------------------ owner completion 1: the evaluator3 repair:2 constructor
check("oc1-current-constructor-plan-is-repair-2-and-owner-admitted",
      cw_pos_plan["descriptor"]["schemaMajor"] == 2 and WF3.admit_repair_plan_v2(copy.deepcopy(cw_pos_plan)) == cw_pos_plan
      and cw_pos_plan["repairPlanId"] == P.W.wid("repairplan2", "workflow.repair-plan", cw_pos_plan["descriptor"])
      and cw_pos_plan["descriptor"]["evidenceRunId"] == cw_pos_id)
check("oc1-every-current-preview-control-plan-is-repair-2",
      all(p["descriptor"]["schemaMajor"] == 2 for p in (cw_pos_plan, cw_neg_plan, cw_neg_alt, cw_create, cw_dyn_plan)))
check("oc1-current-and-historical-profiles-are-separate-module-instances",
      WF3.repair_preview is not WF3._base.repair_preview and P.W.CLOSED_WORLD_SELECTOR is None
      and WF3._base.CLOSED_WORLD_SELECTOR is WF3.evaluator3_closed_world)
import inspect as _oc1_inspect  # noqa: E402
_oc1_param = _oc1_inspect.signature(P.W.repair_preview).parameters["descriptor_major"]
check("oc1-historical-constructor-keeps-a-keyword-only-major-1-default",
      _oc1_param.default == 1 and _oc1_param.kind is _oc1_inspect.Parameter.KEYWORD_ONLY)
_oc1_hist_adapter = {"authority": "authoritative", "availability": "retained", "sealedAssurance": "replayable",
                     "runId": cw_neg_id, "planId": cw_neg_run["planId"], "snapshotId": P.W.tree_snapshot_id(CW_PROJECT, CW_TREE),
                     "findings": CW_FPS[:1], "closedWorld": copy.deepcopy(CW_CLOSED), "evidenceOrigin": "native-analysis"}
_oc1_hist = P.W.repair_preview(CW_PROJECT, CW_TREE, _oc1_hist_adapter, CW_RECIPE, CW_FPS[:1], CW_DELETE, CW_REQS, ["**"], CW_TRUST)
check("oc1-historical-profile-still-emits-major-1-from-a-caller-selected-record",
      _oc1_hist["descriptor"]["schemaMajor"] == 1
      and _oc1_hist["repairPlanId"] == P.W.wid("repairplan2", "workflow.repair-plan", _oc1_hist["descriptor"]))


def _oc1_refusal(cid, fn, error, detail):
    try:
        fn()
        return check(cid, False, "not refused")
    except WF3.Refusal as exc:
        return check(cid, exc.error_code == error and exc.detail == detail, f"{exc.error_code}/{exc.detail}")


_oc1_refusal("oc1-current-admission-refuses-a-historical-major-1-plan", lambda: WF3.admit_repair_plan_v2(copy.deepcopy(_oc1_hist)),
             "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR")
_oc1_relabel = copy.deepcopy(_oc1_hist)
_oc1_relabel["descriptor"]["schemaMajor"] = 2
must_valid("oc1-unreminted-relabel-is-schema-valid", U + "repair:2#/$defs/RepairPlanV1", _oc1_relabel)
_oc1_refusal("oc1-current-admission-refuses-an-unreminted-relabel", lambda: WF3.admit_repair_plan_v2(_oc1_relabel),
             "CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT")
_oc1_absent = hid("finding-key2", "not-a-finding-of-this-run")
check("oc1-historical-profile-trusts-a-caller-listed-target",
      P.W.repair_preview(CW_PROJECT, CW_TREE, dict(_oc1_hist_adapter, findings=[_oc1_absent]), CW_RECIPE, [_oc1_absent],
                         CW_DELETE, CW_REQS, ["**"], CW_TRUST)["descriptor"]["targets"] == [_oc1_absent])
_oc1_refusal("oc1-current-constructor-refuses-a-target-not-matched-in-the-retained-run",
             lambda: _cw_preview(cw_pos_id, cw_pos_run, cw_pos_obj, cw_pos_blob, [_oc1_absent], CW_DELETE),
             "REQUEST.PRECONDITION_FAILED", "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE")
_oc1_adapter = {"authority": "authoritative", "availability": "retained", "sealedAssurance": "replayable", "runId": cw_pos_id,
                "planId": cw_pos_run["planId"], "snapshotId": WF3.tree_snapshot_id(CW_PROJECT, CW_TREE), "findings": CW_FPS[:1],
                "retained": SEL.RetainedRunView(cw_pos_run, cw_pos_obj, cw_pos_blob), "evidenceOrigin": "native-analysis"}
_oc1_refusal("oc1-current-constructor-refuses-a-retained-closure-of-another-run",
             lambda: WF3.repair_preview(CW_PROJECT, CW_TREE, dict(_oc1_adapter, planId=hid("plan2", "another")), CW_RECIPE,
                                        CW_FPS[:1], CW_DELETE, CW_REQS, ["**"], CW_TRUST),
             "REQUEST.PRECONDITION_FAILED", "REPAIR.EVIDENCE_RUN_UNAVAILABLE")
_oc1_refusal("oc1-current-constructor-refuses-a-historical-run2-evidence-run",
             lambda: WF3.repair_preview(CW_PROJECT, CW_TREE, dict(_oc1_adapter, runId=hid("run2", "historical")), CW_RECIPE,
                                        CW_FPS[:1], CW_DELETE, CW_REQS, ["**"], CW_TRUST),
             "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR")
_oc1_refusal("oc1-current-constructor-keeps-authority-first",
             lambda: WF3.repair_preview(CW_PROJECT, CW_TREE, dict(_oc1_adapter, retained=None), CW_RECIPE, CW_FPS[:1], CW_DELETE,
                                        CW_REQS, ["**"], CW_TRUST, ephemeral=True),
             "REQUEST.PRECONDITION_FAILED", "REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE")
check("oc1-repair-preview-command-surface-admits-the-owner-plan-without-relabel",
      QS.project_command_surface(_R2_ENVS["repair-preview"], _R2_CMD["repair-preview"])["parity"]["repair-plan-id"] == cw_pos_plan["repairPlanId"]
      and _R2_ENVS["repair-preview"]["queryRecord"]["plan"] == cw_pos_plan)
'''

OC2 = r'''
# ------------------------------------------------ owner completion 2: policy-test suite admission route
_oc2_suite = _r2_sub(_R2_RAW)["policySuite"]
_oc2_result, _oc2_refusal = WF3.run_admitted_policy_test(copy.deepcopy(_oc2_suite))
check("oc2-admitted-suite-runs-the-same-authoring-test",
      _oc2_refusal is None and WF3.admit_policy_test_suite(_oc2_suite) is _oc2_suite
      and _oc2_result["policyTestResultId"] == _r2_policy_result["policyTestResultId"])
_OC2_REGISTRY = {r["code"]: r for r in json.loads((HERE.parent / "public-detail-registry.v1.json").read_text())["records"]}


def _oc2_termination(suite):
    try:
        WF3.admit_policy_test_suite(suite)
        return None
    except WF3.Refusal as exc:
        return exc


def _oc2_route(cid, suite, detail):
    exc = _oc2_termination(suite)
    if exc is None:
        return check(cid, False, "admitted")
    term = exc.termination()
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "e" * 32,
           "termination": term, "exitCode": WF3.exit_code(term), "errors": [term["domainDetail"]]}
    ok_env, why = valid(U + "command-envelope:3", env)
    return check(cid, exc.error_code == "CONFIG.INVALID" and exc.detail == detail and term["class"] == "request-rejected"
                 and term["errorCode"] == "CONFIG.INVALID" and term["domainDetail"]["code"] == detail and env["exitCode"] == 2 and ok_env,
                 f"{exc.error_code}/{exc.detail} {why}")


_oc2_no_cases = {k: v for k, v in copy.deepcopy(_oc2_suite).items() if k != "cases"}
_oc2_route("oc2-suite-missing-cases-is-config-invalid-with-the-shared-config-invalid-detail", _oc2_no_cases, "CONFIG.INVALID")
_oc2_severity = copy.deepcopy(_oc2_suite)
_oc2_severity["candidatePolicy"]["rules"][0]["severity"] = "fatal"
_oc2_route("oc2-policy-enum-violation-is-not-a-grammar-violation", _oc2_severity, "CONFIG.INVALID")
_oc2_waiver_extra = copy.deepcopy(_oc2_suite)
_oc2_waiver_extra["waivers"]["hook"] = "node scripts/waive.js"
_oc2_route("oc2-waiver-set-member-is-not-a-policy-grammar-refusal", _oc2_waiver_extra, "CONFIG.INVALID")
_oc2_cases = {c["id"]: c for c in _R2_RAW["policyRefusals"]}
_oc2_hook = copy.deepcopy(_oc2_suite)
_oc2_hook["candidatePolicy"].update(_oc2_cases["imperative-key-schema-violation"]["policyExtra"])
_oc2_route("oc2-owner-imperative-key-case-is-policy-imperative-key-refused", _oc2_hook, "POLICY.IMPERATIVE_KEY_REFUSED")
_oc2_expr = copy.deepcopy(_oc2_suite)
_oc2_expr["candidatePolicy"]["rules"][0]["emitWhen"] = _oc2_cases["string-expression-schema-violation"]["policyEmitWhen"]
_oc2_route("oc2-owner-string-expression-case-is-policy-imperative-key-refused", _oc2_expr, "POLICY.IMPERATIVE_KEY_REFUSED")
_oc2_include = copy.deepcopy(_oc2_suite)
_oc2_include["candidatePolicy"]["rules"][0]["include"] = "other-policy.json"
check("oc2-include-is-a-declared-member-elsewhere-in-the-policy-grammar",
      '"include"' in json.dumps(SCHEMAS["urn:opensip:product-v1:workflows:policy-document"]["$defs"]["Rule"])
      or '"include"' in json.dumps(SCHEMAS["urn:opensip:product-v1:workflows:policy-document"]["$defs"]))
_oc2_route("oc2-grammar-law-is-positional-for-a-member-declared-elsewhere", _oc2_include, "POLICY.IMPERATIVE_KEY_REFUSED")
check("oc2-grammar-law-does-not-flag-the-admitted-candidate-policy", not WF3.policy_grammar_violation(_oc2_suite["candidatePolicy"]))
_oc2_dup = copy.deepcopy(_oc2_suite)
_oc2_dup["waivers"]["waivers"] = _r2_sub(_oc2_cases["duplicate-waiver"]["waivers"])
_oc2_dup_result, _oc2_dup_refusal = WF3.run_admitted_policy_test(_oc2_dup)
_oc2_dup_term = _oc2_dup_refusal.termination() if _oc2_dup_refusal is not None else {}
_oc2_goldens = {g["id"]: g for g in _R2_INV["goldens"]}
_oc2_gdup = _oc2_goldens["policy-test-duplicate-waiver"]
check("oc2-resolver-refusal-of-an-admitted-suite-is-the-request-rejection-its-golden-names",
      _oc2_dup_refusal is not None and _oc2_dup_result["resolverAccepted"] is False
      and _oc2_dup_term.get("class") == _oc2_gdup["class"] and WF3.exit_code(_oc2_dup_term) == _oc2_gdup["exitCode"]
      and _oc2_dup_term.get("errorCode") == _oc2_gdup["errorCode"]
      and _oc2_dup_term.get("domainDetail", {}).get("code") == _oc2_gdup["domainDetail"], _oc2_dup_term)
must_valid("oc2-resolver-refused-result-is-still-a-valid-policy-test-result",
           "urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1", _oc2_dup_result)
must_invalid("oc2-resolver-refused-result-is-never-a-policy-test-carrier", U + "command-envelope:3#/$defs/PolicyTestResultRecordV1",
             {"surface": "policy-test-result", "result": _oc2_dup_result})
must_valid("oc2-resolver-accepted-result-is-a-policy-test-carrier", U + "command-envelope:3#/$defs/PolicyTestResultRecordV1",
           {"surface": "policy-test-result", "result": _r2_policy_result})
_oc2_residual = _oc2_goldens.get("policy-test-suite-inadmissible", {})
_oc2_residual_term = _oc2_termination(_oc2_no_cases).termination()
check("oc2-residual-route-golden-is-the-owner-termination",
      _oc2_residual.get("command") == "policy-test" and _oc2_residual.get("class") == _oc2_residual_term["class"]
      and _oc2_residual.get("exitCode") == WF3.exit_code(_oc2_residual_term)
      and _oc2_residual.get("errorCode") == _oc2_residual_term["errorCode"]
      and _oc2_residual.get("domainDetail") == _oc2_residual_term["domainDetail"]["code"])
check("oc2-imperative-key-golden-is-the-owner-termination",
      _oc2_goldens["policy-test-imperative-key"]["domainDetail"] == _oc2_termination(_oc2_hook).termination()["domainDetail"]["code"]
      and _oc2_goldens["policy-test-imperative-key"]["errorCode"] == _oc2_termination(_oc2_hook).termination()["errorCode"])
check("oc2-config-invalid-is-a-d9-error-code-and-a-separately-registered-shared-detail",
      "CONFIG.INVALID" in SCHEMAS[U + "common:3"]["$defs"]["D9ErrorCode"]["enum"]
      and "CONFIG.INVALID" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"]
      and "CONFIG.INVALID" in SCHEMAS["urn:opensip:product-v1:workflows:common"]["$defs"]["DomainDetailCode"]["enum"]
      and _OC2_REGISTRY["CONFIG.INVALID"]["owner"] == "security"
      and _OC2_REGISTRY["POLICY.IMPERATIVE_KEY_REFUSED"]["owner"] == "workflows")
'''

rows.append(apply('Q1+Q2 checker', CWP, [
    ('''native selection join. The _cw_preview helper separately uses the historical synthetic
# host adapter and major-1 descriptor constructor; it does not establish an admitted current
# descriptor or a joined real-Run snapshot/trust/requirements projection.''',
     '''native selection join. The _cw_preview helper uses a synthetic host adapter (tree, project,
# snapshot, trust, requirements) with the CURRENT evaluator3 owner constructor, which returns an
# owner-admitted repair:2 plan; it does not establish a joined real-Run snapshot/trust/requirements projection.'''),
    ('''    from the Run. The inherited constructor emits a major-1 descriptor; this helper therefore
    demonstrates gate integration only, not current descriptor admission or snapshot joins.
''', '''    from the Run. The evaluator3 owner constructor joins the targets to the retained Run and returns
    an admitted repair:2 plan; snapshot equality is still judged against the synthetic adapter.
'''),
    ('''_cw_preview uses a separate synthetic host adapter and inherited major-1 descriptor constructor; its outputs are not admitted current RepairPlanDescriptors.''',
     '''_cw_preview uses a separate synthetic host adapter with the evaluator3 owner constructor; its outputs are owner-admitted repair:2 RepairPlanV1 whose snapshot join is against that adapter.'''),
    ('''        "current RepairPlanDescriptor admission, real-Run snapshot/project/preimage joins, or sufficiency derivation from the synthetic host projection",''',
     '''        "real-Run snapshot/project/preimage joins, or sufficiency derivation from the synthetic host projection",'''),
    ('''check("r2-policy-test-owner-result-produced", _r2_policy_refusal is None and _r2_policy_result["resolverAccepted"] is True)
''', '''check("r2-policy-test-owner-result-produced", _r2_policy_refusal is None and _r2_policy_result["resolverAccepted"] is True)
''' + OC2),
    ('''# repair preview from the admitted closed-world preview; the reference constructor still emits a major-1 descriptor.
_r2_desc = copy.deepcopy(cw_pos_plan["descriptor"])
check("r2-repair-preview-reference-constructor-emits-historical-major-1", _r2_desc["schemaMajor"] == 1)
_r2_desc["schemaMajor"] = 2
_r2_plan = {"repairPlanId": P.W.wid("repairplan2", "workflow.repair-plan", _r2_desc), "descriptor": _r2_desc}
''', '''# repair preview carries the evaluator3 owner-produced plan exactly as returned (no relabel, no remint).
_r2_plan = copy.deepcopy(cw_pos_plan)
_r2_desc = _r2_plan["descriptor"]
'''),
    ('''_R2_COMMAND_OF["repair-preview"] = "repair-preview"
''', '''_R2_COMMAND_OF["repair-preview"] = "repair-preview"
''' + OC1),
]))
print(json.dumps(rows, indent=1))
