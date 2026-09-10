"""Execution-inputs reference admission (design evidence, not a host runtime).

Host-captured evaluator INPUT observation. Does not admit findings, proofs, or
native Coverage producer internals beyond named locator joins. Not a Run.
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
AdmissionError = C.AdmissionError

SCHEMA = json.loads((HERE / "execution-inputs.schema.v1.json").read_text(encoding="utf-8"))
PLAN_SCHEMA = json.loads((HERE / "enumeration-plan.schema.v1.json").read_text(encoding="utf-8"))
KIND_MAP = PLAN_SCHEMA["x-opensip-kind-derivation"]
MATRIX = json.loads((NATIVE / "native-capability-matrix.v2.json").read_text(encoding="utf-8"))
OWNER_DEF = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["DeficiencyV2"]["enum"]
OWNER_CAUSE = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["NativeCause"]["enum"]
CAUSE_REG = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))[
    "x-opensip-deficiency-cause-registry"
]["deficiencies"]

CAP_BY_ID = {row["id"]: row for row in MATRIX["capabilities"]}
CELL_STATE = {(row["capability"], row["mode"]): row for row in MATRIX["cells"]}
CANDIDATE_CAPS = frozenset({"clones-near", "clones-cross-tsjs"})
OUTPUT_DOMAINS = frozenset({"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"})
HEX64 = __import__("re").compile(r"^[0-9a-f]{64}$")

INTERNAL_FAULTS = (
    "EXECUTION_INPUTS_SCHEMA",
    "EXECUTION_INPUTS_PLAN_JOIN",
    "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN",
    "EXECUTION_INPUTS_ENUMERATION_DIGEST",
    "EXECUTION_INPUTS_EVALUATOR_CLOSURE",
    "EXECUTION_INPUTS_CELL_TOTALITY",
    "EXECUTION_INPUTS_VIEW_TOTALITY",
    "EXECUTION_INPUTS_REF_POINTER",
    "EXECUTION_INPUTS_REF_LOST_BYTES",
    "EXECUTION_INPUTS_REF_INVALID_BYTES",
    "EXECUTION_INPUTS_STAGE_PRODUCER",
    "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
    "EXECUTION_INPUTS_CANDIDATE_REQUIRED",
    "EXECUTION_INPUTS_CANDIDATE_EMPTY_COMPLETE",
    "EXECUTION_INPUTS_OUTPUT_BACKLINK",
    "EXECUTION_INPUTS_VCS_APPLICABILITY",
    "EXECUTION_INPUTS_CAUSE_CARRIER",
    "EXECUTION_INPUTS_CAUSE_ENUM_DRIFT",
    "EXECUTION_INPUTS_KIND_MAP",
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


def _matrix_pairs(capability_id: str) -> list[tuple[str, str]]:
    cap = CAP_BY_ID.get(capability_id) or {}
    pairs = []
    for item in cap.get("relations") or []:
        if isinstance(item, list) and len(item) == 2:
            pairs.append((item[0], item[1]))
    return pairs


def admit_execution_inputs(
    *,
    plan: dict,
    execution_plan: dict,
    execution_plan_id: str,
    stage_specs: dict,
    enumeration_plan: dict,
    analysis_spec: dict,
    execution_inputs: dict,
    inventories: dict,
    views: dict,
    coverages: dict,
    candidate_results: dict,
    retained_blobs: dict | None = None,
    store_pointers: list | None = None,
    closures: dict | None = None,
    vcs_observation: dict | None = None,
) -> dict:
    """Join-admit a host-captured execution-inputs record.

    inventories/views/coverages/candidate_results: digest-hex -> typed record.
    store_pointers: digests the evidence store claims (SUBJECT-D6 pointer set).
    retained_blobs: digest -> exact bytes. Missing key vs pointer-only is lost bytes.
    """
    faults: list[str] = []
    empty = {
        "result": "REFUSE", "refusals": faults, "digest": None,
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "execution-inputs join admission only; not a Run",
    }
    if SCHEMA["$defs"]["DeficiencyV2"]["enum"] != OWNER_DEF or SCHEMA["$defs"]["NativeCause"]["enum"] != OWNER_CAUSE:
        empty["refusals"] = ["EXECUTION_INPUTS_CAUSE_ENUM_DRIFT"]
        return empty
    try:
        C.validate(SCHEMA, execution_inputs)
    except (AdmissionError, ValidationError):
        empty["refusals"] = ["EXECUTION_INPUTS_SCHEMA"]
        return empty

    closures = closures or {}
    inventories = inventories or {}
    views = views or {}
    coverages = coverages or {}
    candidate_results = candidate_results or {}
    retained_blobs = retained_blobs if isinstance(retained_blobs, dict) else {}
    pointers = set(store_pointers) if store_pointers is not None else None

    if plan.get("planId") and execution_inputs["planId"] != plan["planId"]:
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["analysisSpecDigest"] != plan.get("analysisSpecDigest"):
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["analysisSpecDigest"] != raw_digest(analysis_spec):
        _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")
    if execution_inputs["enumerationPlanDigest"] != raw_digest(enumeration_plan):
        _add(faults, "EXECUTION_INPUTS_ENUMERATION_DIGEST")
    if execution_inputs["executionPlanId"] != execution_plan_id:
        _add(faults, "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN")
    if execution_plan.get("planId") != execution_inputs["planId"]:
        _add(faults, "EXECUTION_INPUTS_EXECUTION_PLAN_JOIN")
    ev = execution_inputs["evaluatorClosure"]
    if ev not in (plan.get("semanticClosures") or []):
        _add(faults, "EXECUTION_INPUTS_EVALUATOR_CLOSURE")
    elif closures and closures.get(ev, {}).get("kind") not in (None, "evaluator"):
        _add(faults, "EXECUTION_INPUTS_EVALUATOR_CLOSURE")

    req_tuples = [(r["capabilityId"], r["languageMode"], r["workspaceRoot"], r["required"])
                  for r in analysis_spec["requestedCapabilities"]]
    cell_tuples = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"])
                   for c in enumeration_plan["cells"]]
    if len(req_tuples) != len(cell_tuples) or sorted(req_tuples) != sorted(cell_tuples):
        _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")

    bindings = _bindings(enumeration_plan)
    outcomes = execution_inputs["cellOutcomes"]
    if len(outcomes) != len(bindings):
        _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
    for i, row in enumerate(outcomes):
        if row.get("ordinal") != i:
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
    seen_keys = []
    returned_views = set()
    required_candidate = []
    for row, (ci, po, cell, binding) in zip(outcomes, bindings):
        key = (row["cellOrdinal"], row["programOrdinal"])
        if key in seen_keys or key != (ci, po):
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        seen_keys.append(key)
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
        want_status = en.get("status")
        if row["enumeratorStatus"] != want_status:
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        if row["state"] == "complete":
            if row["deficiency"] is not None or row["nativeCause"] is not None:
                _add(faults, "EXECUTION_INPUTS_CAUSE_CARRIER")
        else:
            _carrier(row["deficiency"], row["nativeCause"], faults)
        if expected_kinds:
            if row["candidateResultDigest"] is not None:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            if len(row["inventoryDigests"]) != len(expected_kinds):
                _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
            for d in row["inventoryDigests"]:
                inv = inventories.get(d)
                if inv is None:
                    _add(faults, "EXECUTION_INPUTS_REF_POINTER")
                elif inv.get("kind") not in expected_kinds:
                    _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
        else:
            if row["inventoryDigests"]:
                _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
            if cell["required"] and row["candidateResultDigest"] is None:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            if row["candidateResultDigest"]:
                required_candidate.append(row["candidateResultDigest"])
        returned_views.update(row["viewDigests"])
        so = row.get("stageOrdinal")
        if so is not None:
            stages = execution_plan.get("stages") or []
            if so >= len(stages):
                _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
            else:
                spec_d = stages[so]["stageSpecDigest"]
                spec = stage_specs.get(spec_d)
                if not isinstance(spec, dict):
                    _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                else:
                    producer = spec.get("producerClosure")
                    for vd in row["viewDigests"]:
                        view = views.get(vd)
                        if isinstance(view, dict) and view.get("producerClosure") != producer:
                            _add(faults, "EXECUTION_INPUTS_STAGE_PRODUCER")
                        if isinstance(view, dict) and view.get("planId") != execution_inputs["planId"]:
                            _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")

    selected = execution_inputs["selectedRefs"]
    for ref in selected:
        if ref["domain"] in OUTPUT_DOMAINS:
            _add(faults, "EXECUTION_INPUTS_OUTPUT_BACKLINK")
    selected_views = {r["digest"] for r in selected if r["domain"] == "view"}
    if selected_views != returned_views or selected_views != set(views):
        _add(faults, "EXECUTION_INPUTS_VIEW_TOTALITY")

    typed_maps = {
        "view": views,
        "subject-inventory": inventories,
        "coverage": coverages,
        "candidate-producer-result": candidate_results,
        "import": None,
        "target-attribution": None,
        "incoming-search": None,
    }
    for ref in selected:
        d = ref["digest"]
        if pointers is not None and d not in pointers:
            _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            continue
        if pointers is not None and d not in retained_blobs:
            _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            continue
        if d in retained_blobs:
            blob = retained_blobs[d]
            if type(blob) is not bytes or hashlib.sha256(blob).hexdigest() != d:
                _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
        mmap = typed_maps.get(ref["domain"])
        if isinstance(mmap, dict):
            rec = mmap.get(d)
            if rec is None and pointers is None:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            elif rec is not None:
                try:
                    if raw_digest(rec) != d and ref["domain"] != "view":
                        # view2 identity is H, not raw C; raw C check applies to canonical-record inputs
                        if ref["domain"] in ("subject-inventory", "candidate-producer-result"):
                            if raw_digest(rec) != d:
                                _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
                    if ref["domain"] == "subject-inventory" and raw_digest(rec) != d:
                        _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
                    if ref["domain"] == "candidate-producer-result" and raw_digest(rec) != d:
                        _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
                except (AdmissionError, TypeError, KeyError):
                    _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")

    # Native coverage totality: every fact-producing matrix pair of every binding.
    owed = []
    for ci, po, cell, binding in bindings:
        cap = cell["capabilityId"]
        if cap in CANDIDATE_CAPS:
            continue
        mode = cell["languageMode"]
        state_row = CELL_STATE.get((cap, mode))
        if state_row and state_row.get("state") == "NOT-SELECTED":
            _add(faults, "EXECUTION_INPUTS_CELL_TOTALITY")
            continue
        for rel, rung in _matrix_pairs(cap):
            owed.append((ci, po, rel, rung, binding.get("universe"), state_row))
    accounts = execution_inputs["nativeCoverageAccounts"]
    have = [(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]) for a in accounts]
    owed_keys = [(a[0], a[1], a[2], a[3]) for a in owed]
    if sorted(have) != sorted(owed_keys):
        _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
    by_acc = {(a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"]): a for a in accounts}
    vcs_kind = (vcs_observation or {}).get("kind")
    for ci, po, rel, rung, uni, state_row in owed:
        acc = by_acc.get((ci, po, rel, rung))
        if acc is None:
            continue
        if acc.get("sourceUniverse") != uni and uni is not None:
            _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
        cd = acc.get("coverageDigest")
        if cd is not None:
            payload = coverages.get(cd)
            if payload is None and pointers is None:
                _add(faults, "EXECUTION_INPUTS_REF_POINTER")
            elif isinstance(payload, dict):
                key = payload.get("key") or {}
                if key.get("relation") != rel or key.get("resolution") != rung:
                    _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
                if uni is not None and key.get("sourceUniverse") != uni:
                    _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")
        if rel == "vcs-change" and vcs_kind == "none":
            # Lawful empty / not-applicable account; omitting was already totality.
            if acc["resolutionCompletenessState"] not in ("not-applicable", "complete"):
                _add(faults, "EXECUTION_INPUTS_VCS_APPLICABILITY")
        if state_row and state_row.get("state") == "UNSUPPORTED-TYPED":
            if acc["coverage"] != "unknown":
                _add(faults, "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY")

    cand_refs = set(execution_inputs["candidateResultRefs"])
    if set(required_candidate) != cand_refs:
        _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
    for digest in cand_refs:
        rec = candidate_results.get(digest)
        if rec is None:
            if pointers is not None and digest in pointers and digest not in retained_blobs:
                _add(faults, "EXECUTION_INPUTS_REF_LOST_BYTES")
            else:
                _add(faults, "EXECUTION_INPUTS_CANDIDATE_REQUIRED")
            continue
        cand_schema = {"$defs": SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
        try:
            C.validate(cand_schema, rec)
        except (AdmissionError, ValidationError):
            _add(faults, "EXECUTION_INPUTS_SCHEMA")
            continue
        try:
            if raw_digest(rec) != digest:
                _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
        except AdmissionError:
            _add(faults, "EXECUTION_INPUTS_REF_INVALID_BYTES")
            continue
        if rec.get("state") == "complete" and rec.get("groupDigests") == [] and rec.get("examinedPaths") is None:
            _add(faults, "EXECUTION_INPUTS_CANDIDATE_EMPTY_COMPLETE")
        if rec.get("planId") != execution_inputs["planId"]:
            _add(faults, "EXECUTION_INPUTS_PLAN_JOIN")

    retained = set(execution_inputs["hostCapture"]["retainedDigests"])
    named = {r["digest"] for r in selected} | cand_refs
    named |= {a["coverageDigest"] for a in accounts if a.get("coverageDigest")}
    if not named <= retained:
        _add(faults, "EXECUTION_INPUTS_REF_POINTER")

    if faults:
        empty["refusals"] = faults
        return empty
    return {
        "result": "ADMIT",
        "refusals": [],
        "digest": raw_digest(execution_inputs),
        "cellCount": len(outcomes),
        "viewCount": len(returned_views),
        "coverageAccountCount": len(accounts),
        "candidateCount": len(cand_refs),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "execution-inputs join admission only; not a Run",
    }
