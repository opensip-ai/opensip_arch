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
