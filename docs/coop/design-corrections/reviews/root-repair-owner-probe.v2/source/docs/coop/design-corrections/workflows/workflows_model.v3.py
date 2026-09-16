"""Evaluator3 policy owner. Historical workflow1 is a separate compatibility profile.
No source mutation or data coercion. Full surface migration is separately checked.
"""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('workflows_legacy_profile',HERE/'workflows_model.v1.py')
_base=importlib.util.module_from_spec(spec);spec.loader.exec_module(_base)
for _name in dir(_base):
    if not _name.startswith('__'):globals()[_name]=getattr(_base,_name)
PROFILE_ROOT=Path(__file__).resolve().parent
ATOM_REGISTRY=json.loads((PROFILE_ROOT.parent/'foundation/evaluator-projection-registry.v1.json').read_text())
def rule_program_digest(policy):
    if policy['schemaMajor']!=2:raise canonical.AdmissionError('EVALUATOR_POLICY_MAJOR')
    return doc_digest({'schemaVersion':2,'policyDigest':doc_digest(policy),'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in policy['rules']]})
_ATOM_OWNER=None
def atom_owner():
    global _ATOM_OWNER
    if _ATOM_OWNER is None:
        spec=importlib.util.spec_from_file_location('workflow_atom_admission3',PROFILE_ROOT.parent/'foundation/atom_model.v1.py')
        _ATOM_OWNER=importlib.util.module_from_spec(spec);spec.loader.exec_module(_ATOM_OWNER)
    return _ATOM_OWNER

def admit_atom(atom,rule_id=None,subject_kind=None):
    """Use the exact atom owner's field/endpoint/rung admission even on empty populations."""
    A=atom_owner();row=ATOM_REGISTRY['relations'].get(atom['relation'])
    if row is None:raise Refusal('CONFIG.INVALID','POLICY.UNKNOWN_RULE','unregistered relation',rule_id)
    endpoint=atom.get('endpoint','source')
    kinds=row.get('targetKinds',[]) if endpoint=='target' else row.get('sourceSubjectKinds',[row.get('sourceSubjectKind')])
    kind=('symbol' if subject_kind=='export' else subject_kind) if subject_kind else next((k for k in kinds if k),None)
    try:A._admit_atom(atom,{'kind':kind})
    except A.AtomAdmissionError as exc:raise Refusal('CONFIG.INVALID','POLICY.UNKNOWN_RULE',str(exc),rule_id) from exc
    return atom

def admit_policy_rule(rule):
    declared={x['kind'] for x in rule['evidenceUse']}
    if len(declared)!=len(rule['evidenceUse']):raise Refusal('CONFIG.INVALID','POLICY.UNKNOWN_RULE','duplicate evidence declaration',rule['ruleId'])
    count=0
    def visit(node,depth=1):
        nonlocal count
        count+=1
        if count>64 or depth>8:raise Refusal('CONFIG.INVALID','POLICY.UNKNOWN_RULE','predicate node/depth bound',rule['ruleId'])
        if node['op'] in ('and','or'):
            for child in node['operands']:visit(child,depth+1)
        elif node['op']=='not':visit(node['operand'],depth+1)
        else:
            admit_atom(node,rule['ruleId'],rule['subjectEnumeration']['subjectKind'])
            if node.get('evidence') and node['evidence'] not in declared:raise Refusal('CONFIG.INVALID','IMPORT.ABSENT_FOR_PREDICATE','undeclared evidence',rule['ruleId'])
    visit(rule['emitWhen']);return rule

def resolve_policy(doc):
    ids=[r['ruleId'] for r in doc['rules']]
    if ids!=sorted(set(ids),key=lambda s:s.encode()):raise Refusal('CONFIG.INVALID','POLICY.UNKNOWN_RULE','ruleIds must be unique and sorted')
    for rule in doc['rules']:admit_policy_rule(rule)
    return doc

# ---------------------------------------------------------- repair closed-world selection
# AUTHOR_PENDING_REVIEW. The evaluator3 profile EXPLICITLY selects the new owner for the
# repair closed-world prerequisite. The historical major-1 profile keeps its own behaviour
# (one caller-selected seven-member record) because `_base` is this profile's private module
# instance; installing the selector here changes no other loader of workflows_model.v1.py.
_SELECTION=None
def closed_world_selection():
    global _SELECTION
    if _SELECTION is None:
        spec=importlib.util.spec_from_file_location('repair_closed_world_selection',PROFILE_ROOT/'repair_closed_world_selection.v1.py')
        _SELECTION=importlib.util.module_from_spec(spec);spec.loader.exec_module(_SELECTION)
    return _SELECTION

def evaluator3_closed_world(run,targets,edits):
    """Derive the gate and the display summary from the RETAINED records of the evidence Run.

    `run['retained']` is a repair_closed_world_selection.RetainedRunView over the objects and
    blobs of an ALREADY ADMITTED Run. This profile refuses a pre-selected seven-member record:
    choosing one is exactly the step that had no published law, and a STALE caller-selected
    summary is never evidence authority here. Universe relevance is derived from the RETAINED,
    evaluator3-REQUIRED EnumerationPlan parameter through the identity owner's own registry
    resolution; no optional unsigned map and no filename parsing is consulted. Preview stays a
    Query-class step; recipe trust, policy consent, current-snapshot equality and an
    authorization bound to the exact repairPlanId remain separately required at apply and are
    untouched here.
    """
    S=closed_world_selection()
    retained=run.get('retained')
    if retained is None:
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                      'evaluator3 repair preview requires the retained closure of the evidence Run; a caller-selected closed-world record is not admitted here')
    try:
        return S.derive(retained,targets,edits)
    except S.RetainedEvidenceUnavailable as exc:
        raise Refusal('REQUEST.PRECONDITION_FAILED','REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                      'a retained record the closed-world selection must read is unavailable: '+str(exc)) from exc

_base.CLOSED_WORLD_SELECTOR=evaluator3_closed_world
CLOSED_WORLD_SELECTOR=evaluator3_closed_world

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
