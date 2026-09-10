"""Execution-inputs reference admission (design evidence, not a host runtime).

Post-Plan evaluator INPUT. Uses M3 objects (H locators) and blobs (raw preimages)
as the EvidenceStore. Does not re-admit native Coverage payloads (M3/N own that);
it verifies joins against caller-supplied already-admitted maps. Not a Run.
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
H_DOMAINS = {
    "view": "view",
    "coverage": "coverage",
    "import": "import",
}
BLOB_DOMAINS = frozenset({"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"})
CAND_MODE = {"clones-near": "near", "clones-cross-tsjs": "cross-tsjs"}

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
    "EXECUTION_INPUTS_STAGE_PRODUCER",
    "EXECUTION_INPUTS_STAGE_ORDINAL",
    "EXECUTION_INPUTS_COVERAGE_DERIVE",
    "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
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


def _coverage_payload(envelope: dict, blobs: dict):
    return _parse_blob(blobs, envelope["payloadDigest"])


def _validate_cand_schema(rec) -> None:
    schema = {"$defs": SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
    C.validate(schema, rec)


def _validate_group(rec) -> None:
    schema = {"$defs": NATIVE_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CloneCandidateGroupV2"}]}
    C.validate(schema, rec)


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
) -> dict:
    """Join-admit host-captured execution inputs against an M3 objects/blobs store.

    plan_id is the actual plan2 locator (Plan descriptor has no planId).
    store_pointers is required: object keys (view2:… / coverage2:…) and blob hexes
    the evidence store claims. views/coverages may be omitted; they are then taken
    from objects. inventories/candidate_results/imports/target_attributions/
    incoming_searches must be supplied when selectedRefs name those domains.
    """
    faults: list[str] = []
    deficiencies: list[dict] = []
    empty = {
        "result": "REFUSE", "refusals": faults, "digest": None,
        "requiredCellDeficiencies": [],
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
    except (AdmissionError, ValidationError):
        empty["refusals"] = ["EXECUTION_INPUTS_SCHEMA"]
        return empty

    pointers = set(store_pointers)
    closures = closures or {}
    stage_specs = stage_specs or {}
    inventories = inventories or {}
    candidate_results = candidate_results or {}
    imports = imports if imports is not None else {}
    target_attributions = target_attributions if target_attributions is not None else {}
    incoming_searches = incoming_searches if incoming_searches is not None else {}
    groups = groups or {}

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
    elif closures.get(ev, {}).get("kind") not in (None, "evaluator"):
        if ev in closures and closures[ev].get("kind") != "evaluator":
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

    def locate(domain: str, digest: str, expect_map=None):
        """Resolve a selected ref. Pointer vs lost vs mismatch vs invalid."""
        if domain in H_DOMAINS:
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
            except (AdmissionError, ValidationError):
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                return None
            if minted != key:
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                return None
            return value
        if expect_map is None:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if digest not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if digest not in blobs:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            return None
        try:
            parsed = _parse_blob(blobs, digest)
        except (AdmissionError, ValidationError):
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            return None
        mapped = expect_map.get(digest)
        if mapped is None:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            return None
        if not C.equal_typed(mapped, parsed):
            _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            return None
        return mapped

    domain_maps = {
        "subject-inventory": inventories,
        "candidate-producer-result": candidate_results,
        "target-attribution": target_attributions,
        "incoming-search": incoming_searches,
        "import": imports,
    }
    resolved_views = {}
    for ref in selected:
        if ref["domain"] == "view":
            value = locate("view", ref["digest"])
            if value is not None:
                resolved_views[ref["digest"]] = value
        elif ref["domain"] == "coverage":
            locate("coverage", ref["digest"])
        elif ref["domain"] == "import":
            rec, key = _obj(objects, "import", ref["digest"])
            if key not in pointers and ref["digest"] not in pointers:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            elif rec is None:
                _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            elif rec[0] != "import":
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
            elif ref["digest"] not in imports and key not in imports:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
        elif ref["domain"] in domain_maps:
            locate(ref["domain"], ref["digest"], domain_maps[ref["domain"]])

    if views:
        if set(views) != set(resolved_views) and resolved_views:
            # caller-supplied view map must agree with store-resolved views
            if set(views) != set(resolved_views):
                for k, v in views.items():
                    if k in resolved_views and not C.equal_typed(v, resolved_views[k]):
                        _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        resolved_views.update({k: v for k, v in views.items() if k not in resolved_views})

    bindings = _bindings(enumeration_plan)
    outcomes = execution_inputs["cellOutcomes"]
    if len(outcomes) != len(bindings):
        _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
    for i, row in enumerate(outcomes):
        if row.get("ordinal") != i:
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")

    returned_views = set()
    required_candidate = []
    inventory_named = set()
    coverage_named = set()
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
            if en_cl and (en_cl not in (plan.get("semanticClosures") or [])):
                _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
            elif en_cl and closures.get(en_cl, {}).get("kind") not in (None, "provider"):
                if en_cl in closures and closures[en_cl].get("kind") != "provider":
                    _add(faults, "EXECUTION_INPUTS_ENUMERATOR")
        if row["state"] == "complete":
            if row["deficiency"] is not None or row["nativeCause"] is not None:
                _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
            if row["stageOrdinal"] is None:
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
        else:
            _carrier(row["deficiency"], row["nativeCause"], faults)
        if row["stageOrdinal"] is None:
            if row.get("stageOrdinalNullReason") not in ("unavailable-binding", "optional-unselected"):
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
            if row["enumeratorStatus"] == "selected" and uni is not None and row["state"] != "unavailable":
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
        else:
            if row.get("stageOrdinalNullReason") is not None:
                _add(faults, "EXECUTION_INPUTS_STAGE_ORDINAL")
            stages = execution_plan.get("stages") or []
            so = row["stageOrdinal"]
            if so >= len(stages) or stages[so].get("ordinal") != so:
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            else:
                spec_d = stages[so]["stageSpecDigest"]
                spec = stage_specs.get(spec_d)
                if spec is None and spec_d in blobs:
                    try:
                        spec = _parse_blob(blobs, spec_d)
                        stage_specs[spec_d] = spec
                    except (AdmissionError, ValidationError):
                        spec = None
                if not isinstance(spec, dict):
                    _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                else:
                    producer = spec.get("producerClosure")
                    if row.get("enumeratorClosure") and producer != row["enumeratorClosure"]:
                        _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                    for vd in row["viewDigests"]:
                        view = resolved_views.get(vd)
                        if view is None:
                            view, _key = _obj(objects, "view", vd)
                            view = view[1] if view else None
                        if not isinstance(view, dict):
                            continue
                        if view.get("producerClosure") != producer:
                            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                        if view.get("planId") != plan_id:
                            _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
                        if uni is not None:
                            for sid in view.get("scopeIds") or []:
                                sc = objects.get(sid)
                                if sc and sc[0] == "subject-scope" and sc[1].get("sourceUniverse") != uni:
                                    _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
        returned_views.update(row["viewDigests"])
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
                if inv.get("state") and row["state"] == "complete" and inv["state"] != "complete":
                    _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
                inventory_named.add(d)
            if sorted(kinds_got) != list(expected_kinds) or len(kinds_got) != len(set(kinds_got)):
                _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
        else:
            if row["inventoryDigests"]:
                _add(faults, "EXECUTION_INPUTS_INVENTORY_KIND")
            if cell["required"] and row["candidateResultDigest"] is None:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
                if cell["required"]:
                    deficiencies.append({
                        "source": "execution", "cause": "required-cell-unsatisfied",
                        "cellOrdinal": ci, "programOrdinal": po,
                        "capabilityId": cell["capabilityId"], "required": True,
                        "deficiency": "provider-unavailable", "nativeCause": None,
                        "inputRefs": [],
                    })
            if row["candidateResultDigest"]:
                required_candidate.append(row["candidateResultDigest"])

    selected_views = {r["digest"] for r in selected if r["domain"] == "view"}
    if selected_views != returned_views:
        _add(faults, "EXECUTION_INPUTS_VIEW_TOTALITY")

    receipts = execution_inputs["hostCapture"].get("stageReceipts") or []
    receipt_refs = []
    for recp in receipts:
        if not _canonical_set_ok(recp.get("outputRefs") or []):
            _add(faults, "EXECUTION_INPUTS_ORDER")
        receipt_refs.extend(recp.get("outputRefs") or [])
        stages = execution_plan.get("stages") or []
        so = recp["ordinal"]
        if so >= len(stages) or stages[so]["stageSpecDigest"] != recp["stageSpecDigest"]:
            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
    # selected view/coverage/import refs must be among stage receipts; inventories may be enumeration-retained
    receipt_set = {(r["domain"], r["digest"]) for r in receipt_refs}
    for ref in selected:
        if ref["domain"] in ("view", "coverage", "import") and (ref["domain"], ref["digest"]) not in receipt_set:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")

    vcs_kind = (vcs_observation or {}).get("kind")
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
            owed.append((ci, po, rel, rung, uni, state_row, cell, en_status))
    accounts = execution_inputs["nativeCoverageAccounts"]
    have = [(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]) for a in accounts]
    owed_keys = [(a[0], a[1], a[2], a[3]) for a in owed]
    if sorted(have) != sorted(owed_keys):
        _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
    by_acc = {(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]): a for a in accounts}

    def derive_from_coverage_ids(ids, uni):
        derived = []
        scopes = []
        for hx in ids:
            rec, key = _obj(objects, "coverage", hx)
            if key not in pointers and hx not in pointers:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
                continue
            if rec is None:
                _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
                continue
            if rec[0] != "coverage":
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                continue
            env = rec[1]
            try:
                if IM.identifier("coverage", env) != key:
                    _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                    continue
            except (AdmissionError, ValidationError):
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
                continue
            scopes.append(env["scopeId"])
            try:
                payload = _coverage_payload(env, blobs)
            except (AdmissionError, ValidationError, KeyError):
                _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
                continue
            derived.append((env, payload))
            sc = objects.get(env["scopeId"])
            if sc and sc[0] == "subject-scope" and uni is not None and sc[1].get("sourceUniverse") != uni:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        return derived, scopes

    for ci, po, rel, rung, uni, state_row, cell, en_status in owed:
        acc = by_acc.get((ci, po, rel, rung))
        if acc is None:
            continue
        matrix_state = (state_row or {}).get("state")
        inapplicable_vcs = rel == "vcs-change" and vcs_kind == "none"
        if inapplicable_vcs:
            if acc["accountState"] != "inapplicable" or acc["coverageIds"]:
                _add(faults, "EXECUTION_INPUTS_VCS_APPLICABILITY")
            if acc["sourceUniverse"] is not None and uni is None:
                _add(faults, "EXECUTION_INPUTS_VCS_APPLICABILITY")
            continue
        if vcs_kind not in (None, "none") and rel == "vcs-change" and acc["accountState"] == "inapplicable":
            _add(faults, "EXECUTION_INPUTS_VCS_APPLICABILITY")
        if matrix_state == "UNSUPPORTED-TYPED":
            want_def = state_row.get("deficiency")
            if acc["accountState"] != "unsupported" or acc.get("deficiency") != want_def or acc["coverageIds"]:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            if cell.get("required"):
                deficiencies.append({
                    "source": "execution", "cause": "unsupported-typed",
                    "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                    "required": True, "relation": rel, "resolution": rung,
                    "deficiency": want_def, "nativeCause": "capability-missing",
                    "inputRefs": [],
                })
            continue
        if uni is None or en_status == "unselected":
            if acc["accountState"] != "unavailable" or acc["coverageIds"] or acc["sourceUniverse"] is not None:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            if cell.get("required"):
                deficiencies.append({
                    "source": "execution", "cause": "required-cell-unsatisfied",
                    "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                    "required": True, "relation": rel, "resolution": rung,
                    "deficiency": acc.get("deficiency") or "provider-unavailable",
                    "nativeCause": acc.get("nativeCause"),
                    "inputRefs": [],
                })
            continue
        if acc.get("sourceUniverse") != uni:
            _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
        derived, scopes = derive_from_coverage_ids(acc["coverageIds"], uni)
        if acc["accountState"] == "complete":
            if not derived:
                _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
            else:
                entries = []
                for env, payload in derived:
                    key = payload.get("key") or {}
                    entry = payload.get("entry") or {}
                    if key.get("relation") != rel or key.get("resolution") != rung:
                        _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                    if key.get("sourceUniverse") != uni:
                        _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                    entries.append(entry)
                    in_view = False
                    cid = IM.PREFIX["coverage"] + ":" + next(
                        (hx for hx in acc["coverageIds"]
                         if _obj(objects, "coverage", hx)[1] == IM.PREFIX["coverage"] + ":" + hx), acc["coverageIds"][0])
                    for vd in returned_views:
                        view = resolved_views.get(vd)
                        if view is None:
                            hit, _k = _obj(objects, "view", vd)
                            view = hit[1] if hit else None
                        if isinstance(view, dict) and cid in (view.get("coverageIds") or []):
                            in_view = True
                    # membership: each coverage envelope must appear on a returned view
                for hx in acc["coverageIds"]:
                    cid = IM.PREFIX["coverage"] + ":" + hx
                    member = False
                    for vd in returned_views:
                        view = resolved_views.get(vd)
                        if view is None:
                            hit, _k = _obj(objects, "view", vd)
                            view = hit[1] if hit else None
                        if isinstance(view, dict) and cid in (view.get("coverageIds") or []):
                            member = True
                    if not member:
                        _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                cov_ans = entries[0].get("coverage") if entries else None
                rc_state = (entries[0].get("resolutionCompleteness") or {}).get("state") if entries else None
                exh = (entries[0].get("resolutionCompleteness") or {}).get("examinedExhaustive") if entries else None
                defic = entries[0].get("deficiency") if entries else None
                ncause = entries[0].get("nativeCause") if entries else None
                if acc.get("coverage") != cov_ans or acc.get("resolutionCompletenessState") != rc_state:
                    _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                if acc.get("examinedExhaustive") != exh:
                    _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                if acc.get("deficiency") != defic or acc.get("nativeCause") != ncause:
                    _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                if sorted(acc.get("scopeIds") or []) != sorted(scopes):
                    _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")
                coverage_named.update(acc["coverageIds"])
        elif acc["accountState"] in ("incomplete", "unavailable"):
            if cell.get("required"):
                deficiencies.append({
                    "source": "execution", "cause": "native-work-incomplete",
                    "cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                    "required": True, "relation": rel, "resolution": rung,
                    "deficiency": acc.get("deficiency"), "nativeCause": acc.get("nativeCause"),
                    "inputRefs": [{"domain": "coverage", "digest": hx} for hx in acc.get("coverageIds") or []],
                })
            coverage_named.update(acc.get("coverageIds") or [])
        elif acc["accountState"] == "complete" and not acc.get("coverageIds"):
            _add(faults, "EXECUTION_INPUTS_COVERAGE_DERIVE")

    cand_refs = set(execution_inputs["candidateResultRefs"])
    if set(required_candidate) - cand_refs:
        _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
    cand_schema = {"$defs": SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
    group_schema = {"$defs": NATIVE_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CloneCandidateGroupV2"}]}
    for digest in cand_refs:
        rec = candidate_results.get(digest)
        if digest not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            continue
        if rec is None:
            if digest not in blobs:
                _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            else:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            continue
        try:
            C.validate(cand_schema, rec)
        except (AdmissionError, ValidationError):
            _add(faults, "EXECUTION_INPUTS_SCHEMA")
            continue
        try:
            if raw_digest(rec) != digest:
                _add(faults, "EXECUTION_INPUTS_REF_MISMATCH")
        except AdmissionError:
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            continue
        if rec.get("planId") != plan_id or rec.get("executionPlanId") != execution_plan_id:
            _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
        matched = next((row for row in outcomes if row.get("candidateResultDigest") == digest), None)
        if matched:
            for field in ("cellOrdinal", "programOrdinal", "capabilityId", "languageMode", "universe"):
                if rec.get(field) != matched.get(field):
                    _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            if rec.get("producerClosure") != matched.get("enumeratorClosure"):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
            if rec.get("stageOrdinal") != matched.get("stageOrdinal"):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_BIND")
        want_mode = CAND_MODE.get(rec.get("capabilityId"))
        for gd in rec.get("groupDigests") or []:
            if gd not in pointers:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
                continue
            g = groups.get(gd)
            if g is None:
                if gd not in blobs:
                    _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
                    continue
                try:
                    g = _parse_blob(blobs, gd)
                except (AdmissionError, ValidationError):
                    _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
                    continue
            try:
                C.validate(group_schema, g)
            except (AdmissionError, ValidationError):
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
                continue
            if g.get("authority") != "candidate-only":
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            if want_mode and g.get("mode") != want_mode:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            if g.get("automaticDeletionEligible") is True:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
            examined = set(rec.get("examinedPaths") or [])
            for member in g.get("members") or []:
                if "/" in member and member not in examined:
                    _add(faults, "EXECUTION_INPUTS_CANDIDATE_GROUP")
        if rec.get("state") in ("unavailable", "partial") and matched and matched.get("required"):
            deficiencies.append({
                "source": "execution", "cause": "required-cell-unsatisfied",
                "cellOrdinal": rec["cellOrdinal"], "programOrdinal": rec["programOrdinal"],
                "capabilityId": rec["capabilityId"], "required": True,
                "deficiency": rec.get("deficiency"), "nativeCause": rec.get("nativeCause"),
                "inputRefs": [{"domain": "candidate-producer-result", "digest": digest}],
            })

    # selectedRefs must name every inventory, candidate, returned view, and used coverage
    sel = {(r["domain"], r["digest"]) for r in selected}
    for d in inventory_named:
        if ("subject-inventory", d) not in sel:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")
    for d in cand_refs:
        if ("candidate-producer-result", d) not in sel:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")
    for d in returned_views:
        if ("view", d) not in sel:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")
    for d in coverage_named:
        if ("coverage", d) not in sel:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")
    for iid in plan.get("importIds") or []:
        hx = iid.split(":", 1)[1] if ":" in iid else iid
        if ("import", hx) not in sel:
            _add(faults, "EXECUTION_INPUTS_SELECTED_COVER")

    # Dedup deficiencies per (cell, program, cause, relation)
    uniq = []
    seen_d = set()
    for d in deficiencies:
        k = (d.get("cellOrdinal"), d.get("programOrdinal"), d.get("cause"), d.get("relation"))
        if k not in seen_d:
            seen_d.add(k)
            uniq.append(d)

    if faults:
        empty["refusals"] = faults
        empty["requiredCellDeficiencies"] = uniq
        return empty
    return {
        "result": "ADMIT",
        "refusals": [],
        "digest": raw_digest(execution_inputs),
        "requiredCellDeficiencies": uniq,
        "cellCount": len(outcomes),
        "viewCount": len(returned_views),
        "coverageAccountCount": len(accounts),
        "candidateCount": len(cand_refs),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "execution-inputs join admission only; not a Run; host TCB trust boundary",
    }
