"""Execution-inputs reference admission (design evidence, not a host runtime).

Post-Plan evaluator INPUT. Uses M3 objects (H locators) and blobs (raw preimages)
as the EvidenceStore. Does not re-admit native Coverage payloads (M3/N own that);
it verifies joins against caller-supplied already-admitted maps. Completeness is
derived from owner records. Not a Run.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema.exceptions import ValidationError

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent / "native"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("exec_in_canonical", HERE / "canonical.py")
IM = _load("exec_in_identity_v3", HERE / "identity-model.v3.py")
AdmissionError = C.AdmissionError
CATCH = (AdmissionError, IM.C.AdmissionError, ValidationError)

SCHEMA = json.loads((HERE / "execution-inputs.schema.v1.json").read_text(encoding="utf-8"))
PLAN_SCHEMA = json.loads((HERE / "enumeration-plan.schema.v1.json").read_text(encoding="utf-8"))
KIND_MAP = PLAN_SCHEMA["x-opensip-kind-derivation"]
MATRIX = json.loads((NATIVE / "native-capability-matrix.v2.json").read_text(encoding="utf-8"))
NATIVE_SCHEMA = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
OWNER_DEF = NATIVE_SCHEMA["$defs"]["DeficiencyV2"]["enum"]
OWNER_CAUSE = NATIVE_SCHEMA["$defs"]["NativeCause"]["enum"]
CAUSE_REG = NATIVE_SCHEMA["x-opensip-deficiency-cause-registry"]["deficiencies"]

CAP_BY_ID = {row["id"]: row for row in MATRIX["capabilities"]}
CELL_STATE = {(row["capability"], row["mode"]): row for row in MATRIX["cells"]}
CANDIDATE_CAPS = frozenset({"clones-near", "clones-cross-tsjs"})
OUTPUT_DOMAINS = frozenset({"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"})
H_DOMAINS = {"view": "view", "coverage": "coverage", "import": "import"}
BLOB_DOMAINS = frozenset({
    "subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search",
})
HOST_DERIVED_DOMAINS = BLOB_DOMAINS
CAND_MODE = {"clones-near": "near", "clones-cross-tsjs": "cross-tsjs"}
STAGE_PRODUCED_FROM_OWNER = frozenset({"view"})

INTERNAL_FAULTS = (
    "EXECUTION_INPUTS_SCHEMA",
    "EXECUTION_INPUTS_STORE_REQUIRED",
    "EXECUTION_INPUTS_PLAN_JOIN",
    "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN",
    "EXECUTION_INPUTS_ENUMERATION_DIGEST",
    "EXECUTION_INPUTS_EVALUATOR_CLOSURE",
    "EXECUTION_INPUTS_CELL_TOTALITY",
    "EXECUTION_INPUTS_INVENTORY_KIND",
    "EXECUTION_INPUTS_VIEW_TOTALITY",
    "EXECUTION_INPUTS_REF_POINTER",
    "EXECUTION_INPUTS_REF_LOST_BYTES",
    "EXECUTION_INPUTS_REF_INVALID_BYTES",
    "EXECUTION_INPUTS_REF_MISMATCH",
    "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE",
    "EXECUTION_INPUTS_STAGE_PRODUCER",
    "EXECUTION_INPUTS_STAGE_ORDINAL",
    "EXECUTION_INPUTS_RECEIPT_TOTALITY",
    "EXECUTION_INPUTS_COVERAGE_DERIVE",
    "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
    "EXECUTION_INPUTS_OUTCOME_DERIVE",
    "EXECUTION_INPUTS_CANDIDATE_REQUIRED",
    "EXECUTION_INPUTS_CANDIDATE_GROUP",
    "EXECUTION_INPUTS_CANDIDATE_BIND",
    "EXECUTION_INPUTS_OUTPUT_BACKLINK",
    "EXECUTION_INPUTS_VCS_APPLICABILITY",
    "EXECUTION_INPUTS_ORDER",
    "EXECUTION_INPUTS_SELECTED_COVER",
    "EXECUTION_INPUTS_CAUSE_CARRIER",
    "EXECUTION_INPUTS_CAUSE_ENUM_DRIFT",
    "EXECUTION_INPUTS_KIND_MAP",
    "EXECUTION_INPUTS_ENUMERATOR",
)

NEEDED_ROOT = (
    "identity-schemas.v3.json Domain/Ref/byDomain: add candidate-producer-result "
    "(canonical-record → execution-inputs.schema.v1.json#/$defs/CandidateProducerResultV1)",
    "execution-plan stage outputDomains: add subject-inventory / candidate-producer-result "
    "only on stages that produce them; current owner fixture is view-only",
    "ProofInputRef / evaluationInputRefs: register candidate-producer-result",
    "clone member custody: native source-candidate body inventory {id,path,language,universe} "
    "or member_locators when bodies[].id is not an inventory nativeSubjectId / snapshot path",
)


def raw_digest(obj) -> str:
    return hashlib.sha256(C.canonical(obj)).hexdigest()


def canon_str_list(values: list[str]) -> list[str]:
    uniq = list(dict.fromkeys(values))
    return sorted(uniq, key=lambda s: C.canonical(s))


def _add(faults: list[str], key: str) -> None:
    if key not in faults:
        faults.append(key)


def _cap_kinds(capability_id: str) -> list[str]:
    raw = KIND_MAP.get(capability_id)
    if not isinstance(raw, list):
        return []
    return canon_str_list([k for k in raw if isinstance(k, str)])


def _matrix_pairs(capability_id: str) -> list[tuple[str, str]]:
    cap = CAP_BY_ID.get(capability_id) or {}
    out = []
    for item in cap.get("relations") or []:
        if isinstance(item, list) and len(item) == 2:
            out.append((item[0], item[1]))
    return out


def _matrix_cause(deficiency: str | None) -> str | None:
    if deficiency is None:
        return None
    row = CAUSE_REG.get(deficiency) or {}
    rule = row.get("nativeCause")
    allowed = row.get("allowedCauses") or []
    if rule == "required" and len(allowed) == 1:
        return allowed[0]
    if rule == "must-be-null":
        return None
    return None


def _carrier(deficiency, native_cause, faults: list[str]) -> None:
    if deficiency is None:
        if native_cause is not None:
            _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
        return
    row = CAUSE_REG.get(deficiency)
    if row is None:
        _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
        return
    rule = row.get("nativeCause")
    allowed = row.get("allowedCauses") or []
    if rule == "must-be-null" and native_cause is not None:
        _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
    elif rule == "required" and native_cause not in allowed:
        _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
    elif rule == "optional" and native_cause is not None and native_cause not in allowed:
        _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")


def _bindings(enumeration_plan: dict) -> list[tuple]:
    out = []
    for ci, cell in enumerate(enumeration_plan["cells"]):
        for b in cell["programBindings"]:
            out.append((ci, b["ordinal"], cell, b))
    return out


def _canonical_set_ok(arr) -> bool:
    if type(arr) is not list:
        return False
    keys = [C.canonical(v) for v in arr]
    return keys == sorted(keys) and len(keys) == len(set(keys))


def _obj(objects: dict, domain: str, digest: str):
    key = IM.PREFIX[domain] + ":" + digest
    hit = objects.get(key)
    if hit is None:
        return None, key
    return hit, key


def _parse_blob(blobs: dict, digest: str):
    raw = blobs.get(digest)
    if raw is None:
        return None
    if type(raw) is not bytes:
        raise AdmissionError("BLOB_TYPE")
    if hashlib.sha256(raw).hexdigest() != digest:
        raise AdmissionError("BLOB_HASH")
    return C.parse(raw)


def _snapshot_paths(objects: dict, enumeration_plan: dict) -> list[str] | None:
    sid = enumeration_plan.get("snapshotId")
    rec = objects.get(sid) if isinstance(sid, str) else None
    if not rec or rec[0] != "snapshot" or not isinstance(rec[1], dict):
        return None
    inv = rec[1].get("sourceInventory")
    if not isinstance(inv, list):
        return None
    return [r["path"] for r in inv if isinstance(r, dict) and isinstance(r.get("path"), str)]


def _binding_extent(binding: dict) -> list[str]:
    paths = []
    for ext in binding.get("extents") or []:
        if isinstance(ext, dict):
            for p in ext.get("paths") or []:
                if isinstance(p, str):
                    paths.append(p)
    return canon_str_list(paths)


def _clone_source_extent(binding: dict, snapshot_paths: list[str] | None) -> tuple[list[str] | None, str | None]:
    extent = _binding_extent(binding)
    if extent:
        return extent, None
    if snapshot_paths is not None:
        return canon_str_list(snapshot_paths), None
    return None, (
        "snapshot.sourceInventory via enumerationPlan.snapshotId "
        "(kinds=[] clone extent; empty binding.extents is not complete-empty)"
    )


def derived_applicability(rel: str, uni, en_status: str, matrix_state: str | None, vcs_kind) -> str:
    if rel == "vcs-change" and vcs_kind == "none":
        return "inapplicable-vcs"
    if matrix_state == "UNSUPPORTED-TYPED":
        return "unsupported-typed"
    if uni is None:
        return "unavailable-null-universe"
    if en_status == "unselected":
        return "unavailable-unselected"
    return "supported-available"


def derive_outcome_state(
    *,
    enumerator_status: str,
    universe,
    required: bool,
    inventory_states: list[str],
    account_states: list[str],
    candidate_state: str | None,
    candidate_cap: bool,
) -> tuple[str, str | None, str | None, str | None]:
    """Aggregate cell row state from inventories, accounts, and candidate result."""
    if enumerator_status == "unselected":
        reason = "optional-unselected" if not required else "unavailable-binding"
        return "unavailable", reason, "provider-unavailable", None
    if universe is None:
        return "unavailable", "unavailable-binding", "provider-unavailable", None
    if candidate_cap:
        if candidate_state is None or candidate_state == "unavailable":
            return "unavailable", None, "provider-unavailable", None
        if candidate_state == "partial":
            return "partial", None, "provider-unavailable", None
        if candidate_state == "complete":
            return "complete", None, None, None
        return "partial", None, "provider-unavailable", None
    if any(s == "unavailable" for s in inventory_states):
        return "unavailable", None, "provider-unavailable", None
    inv_partial = any(s == "partial" for s in inventory_states)
    acc_incomplete = any(s == "incomplete" for s in account_states)
    acc_unavailable = any(s == "unavailable" for s in account_states)
    if acc_unavailable and not any(s in ("complete", "incomplete", "inapplicable", "unsupported") for s in account_states):
        return "unavailable", None, "provider-unavailable", None
    if inv_partial or acc_incomplete:
        return "partial", None, "provider-unavailable", None
    return "complete", None, None, None


def _summarize_entries(entries: list[dict]) -> dict:
    """Derive coverage answer / completeness / ALL causes from every owner entry."""
    if not entries:
        return {
            "accountState": "incomplete",
            "coverage": "unknown",
            "resolutionCompletenessState": None,
            "examinedExhaustive": None,
            "deficiency": "provider-unavailable",
            "nativeCause": None,
            "nativeCauses": [],
            "deficiencies": ["provider-unavailable"],
        }
    answers = [e.get("coverage") for e in entries]
    rcs = [(e.get("resolutionCompleteness") or {}) for e in entries]
    states = [rc.get("state") for rc in rcs]
    exhaustive_vals = [rc.get("examinedExhaustive") for rc in rcs]
    defs = [e.get("deficiency") for e in entries if e.get("deficiency") is not None]
    causes = [e.get("nativeCause") for e in entries if e.get("nativeCause") is not None]
    all_complete = answers and all(a == "complete" for a in answers)
    all_exh = exhaustive_vals and all(v is True for v in exhaustive_vals)
    coverage = "complete" if all_complete else "unknown"
    if coverage == "complete" and not all_exh:
        coverage = "unknown"
    rc_state = states[0] if states and all(s == states[0] for s in states) else (
        "incomplete" if any(s in ("incomplete", "partial", "not-attempted") for s in states) else states[0]
    )
    exh = True if all_exh else (False if any(v is False for v in exhaustive_vals) else None)
    if coverage == "complete" and not defs:
        account_state = "complete"
        deficiency = None
        native_cause = None
    else:
        account_state = "incomplete"
        deficiency = defs[0] if defs else "provider-unavailable"
        native_cause = causes[0] if causes else None
    return {
        "accountState": account_state,
        "coverage": coverage,
        "resolutionCompletenessState": rc_state,
        "examinedExhaustive": exh,
        "deficiency": deficiency,
        "nativeCause": native_cause,
        "nativeCauses": list(dict.fromkeys(causes)),
        "deficiencies": list(dict.fromkeys(defs)),
    }


def admit_execution_inputs(
    *,
    plan_id: str,
    plan: dict,
    execution_plan_id: str,
    execution_plan: dict,
    enumeration_plan: dict,
    analysis_spec: dict,
    execution_inputs: dict,
    objects: dict,
    blobs: dict,
    store_pointers: list,
    inventories: dict,
    views: dict | None = None,
    coverages: dict | None = None,
    candidate_results: dict | None = None,
    imports: dict | None = None,
    target_attributions: dict | None = None,
    incoming_searches: dict | None = None,
    groups: dict | None = None,
    closures: dict | None = None,
    stage_specs: dict | None = None,
    vcs_observation: dict | None = None,
    member_locators: dict | None = None,
) -> dict:
    """Join-admit host-captured execution inputs against an M3 objects/blobs store.

    plan_id is the actual plan2 locator (Plan descriptor has no planId).
    store_pointers is required. views/coverages/groups/candidate_results maps, when
    supplied, must equal store-resolved records — never a permissive merge.
    member_locators bind CloneCandidateGroupV2 native member IDs to retained
    inventory/snapshot paths; they are not a slash heuristic.
    """
    faults: list[str] = []
    deficiencies: list[dict] = []
    needed: list[str] = list(NEEDED_ROOT)
    derived_accounts: list[dict] = []
    derived_outcomes: list[dict] = []
    empty = {
        "result": "REFUSE", "refusals": faults, "digest": None,
        "requiredCellDeficiencies": [],
        "derivedAccounts": [], "derivedOutcomes": [],
        "neededRootInputs": needed,
        "causeRetention": (
            "derivedAccounts[].nativeCauses retains every owner nativeCause for the pair; "
            "requiredCellDeficiencies is one row per (cell, program, cause, relation) for root aggregation"
        ),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "execution-inputs join admission only; not a Run; host TCB trust boundary",
    }
    if SCHEMA["$defs"]["DeficiencyV2"]["enum"] != OWNER_DEF or SCHEMA["$defs"]["NativeCause"]["enum"] != OWNER_CAUSE:
        empty["refusals"] = ["EXECUTION_INPUTS_CAUSE_ENUM_DRIFT"]
        return empty
    if not isinstance(objects, dict) or not isinstance(blobs, dict) or store_pointers is None:
        empty["refusals"] = ["EXECUTION_INPUTS_STORE_REQUIRED"]
        return empty
    if type(store_pointers) is not list:
        empty["refusals"] = ["EXECUTION_INPUTS_STORE_REQUIRED"]
        return empty
    try:
        C.validate(SCHEMA, execution_inputs)
    except CATCH:
        empty["refusals"] = ["EXECUTION_INPUTS_SCHEMA"]
        return empty

    pointers = set(store_pointers)
    if closures is None:
        closures = {}
    if stage_specs is None:
        stage_specs = {}
    if inventories is None:
        inventories = {}
    if candidate_results is None:
        candidate_results = {}
    if imports is None:
        imports = {}
    if target_attributions is None:
        target_attributions = {}
    if incoming_searches is None:
        incoming_searches = {}
    if groups is None:
        groups = {}
    if member_locators is None:
        member_locators = {}

    if execution_inputs["planId"] != plan_id:
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["analysisSpecDigest"] != plan.get("analysisSpecDigest"):
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["analysisSpecDigest"] != raw_digest(analysis_spec):
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["enumerationPlanDigest"] != raw_digest(enumeration_plan):
        _add(faults, "EXECUTION_INPUTS_ENUMERATION_DIGEST")
    if execution_inputs["executionPlanId"] != execution_plan_id:
        _add(faults, "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN")
    if execution_plan.get("planId") != plan_id:
        _add(faults, "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN")

    ev = execution_inputs["evaluatorClosure"]
    if ev not in (plan.get("semanticClosures") or []):
        _add(faults, "EXECUTION_INPUTS_EVALUATOR_CLOSURE")
    if ev not in closures or not isinstance(closures.get(ev), dict) or closures[ev].get("kind") != "evaluator":
        _add(faults, "EXECUTION_INPUTS_EVALUATOR_CLOSURE")

    req_tuples = [(r["capabilityId"], r["languageMode"], r["workspaceRoot"], r["required"])
                  for r in analysis_spec["requestedCapabilities"]]
    cell_tuples = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"])
                   for c in enumeration_plan["cells"]]
    if len(req_tuples) != len(cell_tuples) or sorted(req_tuples) != sorted(cell_tuples):
        _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")

    selected = execution_inputs["selectedRefs"]
    if not _canonical_set_ok(selected):
        _add(faults, "EXECUTION_INPUTS_ORDER")
    if not _canonical_set_ok(execution_inputs["candidateResultRefs"]):
        _add(faults, "EXECUTION_INPUTS_ORDER")
    for ref in selected:
        if ref["domain"] in OUTPUT_DOMAINS:
            _add(faults, "EXECUTION_INPUTS_OUTPUT_BACKLINK")

    def locate_h(domain: str, digest: str):
        rec, key = _obj(objects, H_DOMAINS[domain], digest)
        if key not in pointers and digest not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if rec is None:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            return None
        obj_domain, value = rec
        if obj_domain != H_DOMAINS[domain]:
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        try:
            minted = IM.identifier(obj_domain, value)
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        if minted != key:
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        return value

    def locate_blob(digest: str, supplied: dict, required_map: bool):
        if digest not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if digest not in blobs:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            return None
        try:
            parsed = _parse_blob(blobs, digest)
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            return None
        if parsed is None:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            return None
        mapped = supplied.get(digest)
        if required_map and mapped is None:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if mapped is not None and not C.equal_typed(mapped, parsed):
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        return mapped if mapped is not None else parsed

    domain_maps = {
        "subject-inventory": (inventories, True),
        "candidate-producer-result": (candidate_results, True),
        "target-attribution": (target_attributions, True),
        "incoming-search": (incoming_searches, True),
    }

    resolved_views = {}
    resolved_coverages = {}
    for ref in selected:
        if ref["domain"] == "view":
            value = locate_h("view", ref["digest"])
            if value is not None:
                resolved_views[ref["digest"]] = value
        elif ref["domain"] == "coverage":
            value = locate_h("coverage", ref["digest"])
            if value is not None:
                resolved_coverages[ref["digest"]] = value
        elif ref["domain"] == "import":
            value = locate_h("import", ref["digest"])
            if value is not None:
                mapped = imports.get(ref["digest"])
                if mapped is None:
                    _add(faults, "EXECUTION_INPUTS_REF_POINTER")
                elif not C.equal_typed(mapped, value):
                    _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        elif ref["domain"] in domain_maps:
            supplied, req = domain_maps[ref["domain"]]
            locate_blob(ref["digest"], supplied, req)

    if views is not None:
        if set(views) != set(resolved_views):
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        for k, v in views.items():
            if k in resolved_views and not C.equal_typed(v, resolved_views[k]):
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
    if coverages is not None:
        if set(coverages) != set(resolved_coverages):
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        for k, v in coverages.items():
            if k in resolved_coverages and not C.equal_typed(v, resolved_coverages[k]):
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")

    bindings = _bindings(enumeration_plan)
    outcomes = execution_inputs["cellOutcomes"]
    if len(outcomes) != len(bindings):
        _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
    for i, row in enumerate(outcomes):
        if row.get("ordinal") != i:
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")

    receipts = execution_inputs["hostCapture"].get("stageReceipts") or []
    stages = execution_plan.get("stages") or []
    stage_ords = [s.get("ordinal") for s in stages]
    rec_ords = [r.get("ordinal") for r in receipts]
    if rec_ords != list(range(len(receipts))) or sorted(rec_ords) != sorted(stage_ords) or len(set(rec_ords)) != len(rec_ords):
        _add(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY")
    receipts_by_ord = {}
    captured_stage_refs = []
    for recp in receipts:
        if not _canonical_set_ok(recp.get("outputRefs") or []):
            _add(faults, "EXECUTION_INPUTS_ORDER")
        if not _canonical_set_ok(recp.get("outputDomains") or []):
            _add(faults, "EXECUTION_INPUTS_ORDER")
        so = recp["ordinal"]
        receipts_by_ord[so] = recp
        if so >= len(stages) or stages[so].get("ordinal") != so:
            _add(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY")
            continue
        st = stages[so]
        if st.get("stageSpecDigest") != recp["stageSpecDigest"]:
            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
        spec_d = recp["stageSpecDigest"]
        spec = stage_specs.get(spec_d)
        if spec is None and spec_d in blobs:
            try:
                spec = _parse_blob(blobs, spec_d)
                if spec is not None:
                    stage_specs[spec_d] = spec
            except CATCH:
                spec = None
        if not isinstance(spec, dict):
            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
        else:
            if recp.get("producerClosure") != spec.get("producerClosure"):
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            if not C.equal_typed(recp.get("outputDomains"), spec.get("outputDomains")):
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            if not C.equal_typed(spec.get("outputDomains"), st.get("outputDomains")):
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
        allowed = set(recp.get("outputDomains") or [])
        if recp.get("state") == "unavailable":
            if recp.get("outputRefs"):
                _add(faults, "EXECUTION_INPUTS_RECEIPT_TOTALITY")
        for ref in recp.get("outputRefs") or []:
            if ref["domain"] not in allowed:
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            if recp.get("state") == "complete":
                captured_stage_refs.append(ref)
            if ref["domain"] == "view" and ref["digest"] not in resolved_views:
                value = locate_h("view", ref["digest"])
                if value is not None:
                    resolved_views[ref["digest"]] = value

    snapshot_paths = _snapshot_paths(objects, enumeration_plan)
    if snapshot_paths is None:
        needed.append("objects[enumerationPlan.snapshotId].sourceInventory (clone examined-path extent)")

    vcs_kind = (vcs_observation or {}).get("kind")
    inventory_named = set()
    outcome_candidate = []
    row_inv_states: dict[tuple, list] = {}
    cell_view_hexes: dict[tuple, list] = {}

    for row, (ci, po, cell, binding) in zip(outcomes, bindings):
        if (row["cellOrdinal"], row["programOrdinal"]) != (ci, po):
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        if (row["capabilityId"] != cell["capabilityId"] or row["languageMode"] != cell["languageMode"]
                or row["workspaceRoot"] != cell["workspaceRoot"] or row["required"] != cell["required"]):
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        expected_kinds = _cap_kinds(cell["capabilityId"])
        if not C.equal_typed(row["kinds"], expected_kinds) or not C.equal_typed(cell["kinds"], expected_kinds):
            _add(faults, "EXECUTION_INPUTS_KIND_MAP")
        uni = binding.get("universe")
        if row["universe"] != uni:
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        en = binding.get("enumerator") or {}
        if row["enumeratorStatus"] != en.get("status"):
            _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
        en_cl = en.get("closureId")
        if en.get("status") == "selected":
            if row.get("enumeratorClosure") != en_cl:
                _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
            if not en_cl or en_cl not in (plan.get("semanticClosures") or []):
                _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
            if not en_cl or en_cl not in closures or not isinstance(closures.get(en_cl), dict) or closures[en_cl].get("kind") != "provider":
                _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
        cap_rels = {p[0] for p in _matrix_pairs(cell["capabilityId"])}
        attributed = []
        producer = row.get("enumeratorClosure")
        for hx, view in resolved_views.items():
            if not isinstance(view, dict):
                continue
            if producer and view.get("producerClosure") != producer:
                continue
            if view.get("planId") != plan_id:
                _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
                continue
            if uni is None:
                continue
            matched_u = False
            matched_rel = False
            for sid in view.get("scopeIds") or []:
                sc = objects.get(sid)
                if not sc or sc[0] != "subject-scope" or not isinstance(sc[1], dict):
                    continue
                if sc[1].get("sourceUniverse") == uni:
                    matched_u = True
                if sc[1].get("relation") in cap_rels or (not cap_rels and cell["capabilityId"] in CANDIDATE_CAPS):
                    matched_rel = True
                if sc[1].get("enumeratorClosure") and producer and sc[1].get("enumeratorClosure") != producer:
                    continue
            if matched_u and (matched_rel or not cap_rels):
                attributed.append(hx)
        attributed = canon_str_list(attributed)
        cell_view_hexes[(ci, po)] = attributed
        if not C.equal_typed(row["viewDigests"], attributed):
            _add(faults, "EXECUTION_INPUTS_VIEW_TOTALITY")
        inv_states = []
        if expected_kinds:
            if row["candidateResultDigest"] is not None:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            kinds_got = []
            for d in row["inventoryDigests"]:
                inv = inventories.get(d)
                if inv is None:
                    _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
                    continue
                kinds_got.append(inv.get("kind"))
                if inv.get("kind") not in expected_kinds:
                    _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
                if inv.get("cellOrdinal") != ci or inv.get("programOrdinal") != po:
                    _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
                if inv.get("planId") not in (None, plan_id) and inv.get("planId") != plan_id:
                    _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
                st = inv.get("state")
                if isinstance(st, str):
                    inv_states.append(st)
                inventory_named.add(d)
            if sorted(kinds_got) != list(expected_kinds) or len(kinds_got) != len(set(kinds_got)):
                _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
        else:
            if row["inventoryDigests"]:
                _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
            if cell["required"] and cell["capabilityId"] in CANDIDATE_CAPS and row["candidateResultDigest"] is None:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            if row["candidateResultDigest"]:
                outcome_candidate.append(row["candidateResultDigest"])
        row_inv_states[(ci, po)] = inv_states

    # Coverage accounts: join totality, then derive from ALL owner entries of THIS cell.
    owed = []
    for ci, po, cell, binding in bindings:
        cap = cell["capabilityId"]
        if cap in CANDIDATE_CAPS:
            continue
        mode = cell["languageMode"]
        state_row = CELL_STATE.get((cap, mode))
        uni = binding.get("universe")
        en_status = (binding.get("enumerator") or {}).get("status")
        for rel, rung in _matrix_pairs(cap):
            owed.append((ci, po, rel, rung, uni, state_row, cell, en_status, binding))
    accounts = execution_inputs["nativeCoverageAccounts"]
    have = [(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]) for a in accounts]
    owed_keys = [(a[0], a[1], a[2], a[3]) for a in owed]
    if sorted(have) != sorted(owed_keys):
        _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
    by_acc = {(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]): a for a in accounts}
    account_states_by_cell: dict[tuple, list] = {}

    def load_coverage(hx: str, uni):
        rec, key = _obj(objects, "coverage", hx)
        if key not in pointers and hx not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if rec is None:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            return None
        if rec[0] != "coverage":
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        env = rec[1]
        try:
            if IM.identifier("coverage", env) != key:
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                return None
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        payload_digest = env.get("payloadDigest")
        if not isinstance(payload_digest, str) or payload_digest not in blobs:
            _add(faults, "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE")
            return None
        try:
            payload = _parse_blob(blobs, payload_digest)
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            return None
        if payload is None:
            _add(faults, "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE")
            return None
        sc = objects.get(env["scopeId"])
        if sc and sc[0] == "subject-scope" and uni is not None and sc[1].get("sourceUniverse") != uni:
            _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        return env, payload

    def partitions_in_cell(ci, po, rel, rung, uni, producer):
        found = []
        for hx in cell_view_hexes.get((ci, po), []):
            view = resolved_views.get(hx)
            if not isinstance(view, dict):
                continue
            if producer and view.get("producerClosure") != producer:
                continue
            for cid in view.get("coverageIds") or []:
                chx = cid.split(":", 1)[1] if isinstance(cid, str) and ":" in cid else cid
                loaded = load_coverage(chx, uni)
                if loaded is None:
                    continue
                env, payload = loaded
                key = payload.get("key") or {}
                if key.get("relation") != rel or key.get("resolution") != rung:
                    continue
                if uni is not None and key.get("sourceUniverse") != uni:
                    continue
                sc = objects.get(env["scopeId"])
                if sc and sc[0] == "subject-scope":
                    if producer and sc[1].get("enumeratorClosure") not in (None, producer):
                        continue
                    if uni is not None and sc[1].get("sourceUniverse") != uni:
                        continue
                found.append((chx, env, payload))
        # unique by hex, canonical order
        by_h = {h: (h, e, p) for h, e, p in found}
        return [by_h[h] for h in canon_str_list(list(by_h))]

    for ci, po, rel, rung, uni, state_row, cell, en_status, binding in owed:
        acc = by_acc.get((ci, po, rel, rung))
        if acc is None:
            continue
        matrix_state = (state_row or {}).get("state")
        want_app = derived_applicability(rel, uni, en_status, matrix_state, vcs_kind)
        if acc.get("applicability") != want_app:
            if want_app == "inapplicable-vcs" or acc.get("applicability") == "inapplicable-vcs":
                _add(faults, "EXECUTION_INPUTS_VCS_APPLICABILITY")
            else:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        want_u = None if want_app in ("unavailable-unselected", "unavailable-null-universe") else uni
        if acc.get("sourceUniverse") != want_u:
            _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        producer = (binding.get("enumerator") or {}).get("closureId")
        if want_app != "supported-available":
            if acc.get("coverageIds"):
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            if want_app == "unsupported-typed":
                want_def = (state_row or {}).get("deficiency")
                want_cause = _matrix_cause(want_def)
                _carrier(want_def, want_cause, faults)
                summary = {
                    "accountState": "unsupported", "coverage": None,
                    "resolutionCompletenessState": None, "examinedExhaustive": None,
                    "deficiency": want_def, "nativeCause": want_cause,
                    "nativeCauses": [want_cause] if want_cause else [],
                    "deficiencies": [want_def] if want_def else [],
                    "scopeIds": [],
                }
                if cell.get("required"):
                    deficiencies.append({
                        "source": "execution", "cause": "unsupported-typed",
                        "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                        "required": True, "relation": rel, "resolution": rung,
                        "deficiency": want_def, "nativeCause": want_cause, "inputRefs": [],
                    })
            elif want_app == "inapplicable-vcs":
                summary = {
                    "accountState": "inapplicable", "coverage": None,
                    "resolutionCompletenessState": None, "examinedExhaustive": None,
                    "deficiency": None, "nativeCause": None, "nativeCauses": [],
                    "deficiencies": [], "scopeIds": [],
                }
            else:
                summary = {
                    "accountState": "unavailable", "coverage": None,
                    "resolutionCompletenessState": None, "examinedExhaustive": None,
                    "deficiency": "provider-unavailable", "nativeCause": None,
                    "nativeCauses": [], "deficiencies": ["provider-unavailable"], "scopeIds": [],
                }
                if cell.get("required"):
                    deficiencies.append({
                        "source": "execution", "cause": "required-cell-unsatisfied",
                        "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                        "required": True, "relation": rel, "resolution": rung,
                        "deficiency": "provider-unavailable", "nativeCause": None, "inputRefs": [],
                    })
            derived_accounts.append({
                "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
                **summary,
            })
            account_states_by_cell.setdefault((ci, po), []).append(summary["accountState"])
            continue

        returned = partitions_in_cell(ci, po, rel, rung, uni, producer)
        returned_ids = [h for h, _, _ in returned]
        named = acc.get("coverageIds") or []
        if canon_str_list(named) != canon_str_list(returned_ids):
            _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        entries = []
        scopes = []
        for hx, env, payload in returned:
            entry = payload.get("entry") or {}
            key = payload.get("key") or {}
            if key.get("relation") != rel or key.get("resolution") != rung:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            if key.get("sourceUniverse") != uni:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            _carrier(entry.get("deficiency"), entry.get("nativeCause"), faults)
            entries.append(entry)
            scopes.append(env["scopeId"])
        # also validate host-named envelopes that were not in returned (subset/extra already flagged)
        for hx in named:
            if hx not in returned_ids:
                loaded = load_coverage(hx, uni)
                if loaded:
                    _env, payload = loaded
                    entry = payload.get("entry") or {}
                    _carrier(entry.get("deficiency"), entry.get("nativeCause"), faults)
                    entries.append(entry)
        summary = _summarize_entries(entries)
        summary["scopeIds"] = canon_str_list(scopes)
        if summary["accountState"] != "complete" and cell.get("required"):
            deficiencies.append({
                "source": "execution", "cause": "native-work-incomplete",
                "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                "required": True, "relation": rel, "resolution": rung,
                "deficiency": summary.get("deficiency"),
                "nativeCause": summary.get("nativeCause"),
                "nativeCauses": list(summary.get("nativeCauses") or []),
                "inputRefs": [{"domain": "coverage", "digest": hx} for hx in named],
            })
        derived_accounts.append({
            "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
            **summary,
        })
        account_states_by_cell.setdefault((ci, po), []).append(summary["accountState"])

    cand_schema = {"$defs": SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
    group_schema = {"$defs": NATIVE_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CloneCandidateGroupV2"}]}
    cand_refs = list(execution_inputs["candidateResultRefs"])
    if canon_str_list(cand_refs) != canon_str_list(outcome_candidate):
        _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
    bound_once = {}
    cand_state_by_cell: dict[tuple, str] = {}
    inventory_rows_index = []
    for d, inv in inventories.items():
        if isinstance(inv, dict):
            inventory_rows_index.append((d, inv))

    for digest in cand_refs:
        rec = locate_blob(digest, candidate_results, True)
        if rec is None:
            continue
        try:
            C.validate(cand_schema, rec)
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_SCHEMA")
            continue
        try:
            if raw_digest(rec) != digest:
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        except CATCH:
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            continue
        if rec.get("planId") != plan_id or rec.get("executionPlanId") != execution_plan_id:
            _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
        matches = [row for row in outcomes if row.get("candidateResultDigest") == digest]
        if len(matches) != 1:
            _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            matched = matches[0] if matches else None
        else:
            matched = matches[0]
            key = (matched["cellOrdinal"], matched["programOrdinal"])
            if key in bound_once:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            bound_once[key] = digest
            cand_state_by_cell[key] = rec.get("state")
            for field in ("cellOrdinal", "programOrdinal", "capabilityId", "languageMode", "universe"):
                if rec.get(field) != matched.get(field):
                    _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            if rec.get("producerClosure") != matched.get("enumeratorClosure"):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            if rec.get("stageOrdinal") != matched.get("stageOrdinal"):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            _carrier(rec.get("deficiency"), rec.get("nativeCause"), faults)
        want_mode = CAND_MODE.get(rec.get("capabilityId"))
        binding = None
        if matched:
            for ci, po, cell, b in bindings:
                if ci == matched["cellOrdinal"] and po == matched["programOrdinal"]:
                    binding = b
                    break
        extent, need = _clone_source_extent(binding or {}, snapshot_paths)
        if need and rec.get("state") == "complete":
            needed.append(need)
            _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
        if rec.get("state") == "complete" and extent is not None:
            if canon_str_list(rec.get("examinedPaths") or []) != canon_str_list(extent):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
        for gd in rec.get("groupDigests") or []:
            g = locate_blob(gd, groups, False)
            if g is None:
                continue
            if groups and gd in groups and not C.equal_typed(groups[gd], g):
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            try:
                C.validate(group_schema, g)
            except CATCH:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
                continue
            if g.get("authority") != "candidate-only":
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            if want_mode and g.get("mode") != want_mode:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            if g.get("automaticDeletionEligible") is True:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            for member in g.get("members") or []:
                if not _member_custody(
                    member, rec, inventory_rows_index, snapshot_paths or [], member_locators, faults,
                ):
                    _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
                    needed.append(
                        "member_locators or native source-candidate body inventory "
                        "{id, path, language, universe} for CloneCandidateGroupV2.members "
                        "(native bodies[].id, not a path slash heuristic)"
                    )
        if rec.get("state") in ("unavailable", "partial") and matched and matched.get("required"):
            deficiencies.append({
                "source": "execution", "cause": "required-cell-unsatisfied",
                "cellOrdinal": rec["cellOrdinal"], "programOrdinal": rec["programOrdinal"],
                "capabilityId": rec["capabilityId"], "required": True,
                "deficiency": rec.get("deficiency"), "nativeCause": rec.get("nativeCause"),
                "inputRefs": [{"domain": "candidate-producer-result", "digest": digest}],
            })

    # Derive each cell outcome and join to the host row.
    for row, (ci, po, cell, binding) in zip(outcomes, bindings):
        cap = cell["capabilityId"]
        cand_cap = cap in CANDIDATE_CAPS
        d_state, d_reason, d_def, d_cause = derive_outcome_state(
            enumerator_status=row["enumeratorStatus"],
            universe=row["universe"],
            required=cell["required"],
            inventory_states=row_inv_states.get((ci, po), []),
            account_states=account_states_by_cell.get((ci, po), []),
            candidate_state=cand_state_by_cell.get((ci, po)),
            candidate_cap=cand_cap,
        )
        derived_outcomes.append({
            "ordinal": row["ordinal"], "cellOrdinal": ci, "programOrdinal": po,
            "state": d_state, "stageOrdinalNullReason": d_reason,
            "deficiency": d_def if d_state != "complete" else None,
            "nativeCause": d_cause if d_state != "complete" else None,
        })
        if row["state"] != d_state:
            _add(faults, "EXECUTION_INPUTS_OUTCOME_DERIVE")
        if d_state == "complete":
            if row["deficiency"] is not None or row["nativeCause"] is not None:
                _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
            if row["stageOrdinal"] is None:
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
        else:
            _carrier(row["deficiency"], row["nativeCause"], faults)
        if row["stageOrdinal"] is None:
            if row.get("stageOrdinalNullReason") not in ("unavailable-binding", "optional-unselected"):
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
            if row["enumeratorStatus"] == "selected" and row["universe"] is not None and d_state != "unavailable":
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
        else:
            if row.get("stageOrdinalNullReason") is not None:
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
            so = row["stageOrdinal"]
            recp = receipts_by_ord.get(so)
            if recp is None:
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            else:
                if recp.get("producerClosure") != row.get("enumeratorClosure") and row.get("enumeratorClosure"):
                    _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                if d_state == "complete" and recp.get("state") != "complete":
                    _add(faults, "EXECUTION_INPUTS_OUTCOME_DERIVE")
                spec = stage_specs.get(recp["stageSpecDigest"])
                if isinstance(spec, dict):
                    for vd in row["viewDigests"]:
                        view = resolved_views.get(vd)
                        if isinstance(view, dict) and view.get("producerClosure") != spec.get("producerClosure"):
                            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")

    # selectedRefs exact totality (stage-produced ∪ view coverages ∪ host-derived ∪ Plan imports)
    expected_set = set()
    for ref in captured_stage_refs:
        expected_set.add((ref["domain"], ref["digest"]))
    view_hexes = {hx for hexes in cell_view_hexes.values() for hx in hexes}
    view_hexes.update(ref["digest"] for ref in captured_stage_refs if ref["domain"] == "view")
    for hx in view_hexes:
        expected_set.add(("view", hx))
        view = resolved_views.get(hx)
        if isinstance(view, dict):
            for cid in view.get("coverageIds") or []:
                chx = cid.split(":", 1)[1] if isinstance(cid, str) and ":" in cid else cid
                expected_set.add(("coverage", chx))
    for d in inventory_named:
        expected_set.add(("subject-inventory", d))
    for d in outcome_candidate:
        expected_set.add(("candidate-producer-result", d))
    for iid in plan.get("importIds") or []:
        hx = iid.split(":", 1)[1] if ":" in iid else iid
        expected_set.add(("import", hx))
    actual_set = {(r["domain"], r["digest"]) for r in selected}
    if actual_set != expected_set:
        _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")

    uniq = []
    seen_d = set()
    for d in deficiencies:
        k = (d.get("cellOrdinal"), d.get("programOrdinal"), d.get("cause"), d.get("relation"))
        if k not in seen_d:
            seen_d.add(k)
            uniq.append(d)

    needed = list(dict.fromkeys(needed))
    standing = "execution-inputs join admission only; not a Run; host TCB trust boundary"
    cause_ret = (
        "derivedAccounts[].nativeCauses retains every owner nativeCause for the pair; "
        "requiredCellDeficiencies is one row per (cell, program, cause, relation) for root aggregation"
    )
    if faults:
        empty["refusals"] = faults
        empty["requiredCellDeficiencies"] = uniq
        empty["derivedAccounts"] = derived_accounts
        empty["derivedOutcomes"] = derived_outcomes
        empty["neededRootInputs"] = needed
        empty["causeRetention"] = cause_ret
        return empty
    return {
        "result": "ADMIT",
        "refusals": [],
        "digest": raw_digest(execution_inputs),
        "requiredCellDeficiencies": uniq,
        "derivedAccounts": derived_accounts,
        "derivedOutcomes": derived_outcomes,
        "neededRootInputs": needed,
        "causeRetention": cause_ret,
        "cellCount": len(outcomes),
        "viewCount": len({hx for hexes in cell_view_hexes.values() for hx in hexes}),
        "coverageAccountCount": len(accounts),
        "candidateCount": len(cand_refs),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": standing,
    }


def _member_custody(member, rec, inventory_rows_index, snapshot_paths, locators, faults) -> bool:
    """Native ID membership. No slash-in-path heuristic."""
    uni = rec.get("universe")
    ci, po = rec.get("cellOrdinal"), rec.get("programOrdinal")
    loc = locators.get(member) if isinstance(locators, dict) else None
    if isinstance(loc, dict):
        path = loc.get("path")
        nsid = loc.get("nativeSubjectId")
        if loc.get("universe") not in (None, uni) and loc.get("universe") != uni:
            return False
        if path in snapshot_paths:
            return True
        for d, inv in inventory_rows_index:
            if inv.get("cellOrdinal") not in (None, ci) and inv.get("programOrdinal") not in (None, po):
                # locators may bind a clone cell (kinds=[]) to a sibling inventory
                pass
            for row in inv.get("rows") or []:
                if row.get("nativeSubjectId") in (member, nsid) or row.get("path") == path:
                    return True
        return path in snapshot_paths or nsid in snapshot_paths
    for d, inv in inventory_rows_index:
        if rec.get("universe") is not None:
            pass
        for row in inv.get("rows") or []:
            if row.get("nativeSubjectId") == member:
                return True
    if member in snapshot_paths:
        return True
    return False
