"""Admission of annotated owners: x-opensip-digest / x-opensip-order / closureMembership.

Applicability is derived from the published schema annotations on records that
this graph actually contains. A heuristic walk of field names ending in Digest
is not the law. Stock JSON Schema does not execute these annotations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from helper.canonical import C
from helper.component_manifest import admit_component_manifest
from helper.errors import AdmissionError
from helper.execution_inputs import (
    BLOB_INPUT_DOMAINS,
    FORBIDDEN_SELECTED_DOMAINS,
    STAGE_PRODUCED_DOMAINS_REFERENCE,
    blob_selected_equals_host_derived,
    derive_account,
    derive_outcome,
    expected_matrix_accounts,
    join_host_outcome,
    matching_coverages_for_account,
    selected_refs_totality,
    vcs_applicability,
)
from helper.identity import parse_h_frame
from helper.lexical import admit_raw
from helper.order import check_order
from helper.schema_admit import validate_against

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/subject")
IDENT_REL = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
EXEC_REL = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
ENUM_REL = "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EMIS_REL = "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
SINV_REL = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
NATIVE_REL = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
REL_REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
MATRIX_REL = "docs/coop/design-corrections/native/native-capability-matrix.v2.json"


def _load(rel: str) -> dict:
    return json.loads((KIT / rel).read_text())


def _resolve_ref(schema: dict, doc: dict) -> dict:
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/$defs/"):
            name = ref.split("/")[-1]
            merged = dict(doc.get("$defs", {}).get(name) or {})
            extra = {k: v for k, v in schema.items() if k != "$ref"}
            merged.update(extra)
            return merged
        if ref == "#":
            return doc
    return schema


def iter_digest_annotations(schema: dict, doc: dict, path: str = "$"):
    """Yield (json_path, annotation, schema_node) for every x-opensip-digest owner."""
    schema = _resolve_ref(schema, doc)
    if not isinstance(schema, dict):
        return
    if "x-opensip-digest" in schema:
        yield path, schema["x-opensip-digest"], schema
    if "allOf" in schema:
        for i, sub in enumerate(schema["allOf"]):
            yield from iter_digest_annotations(sub, doc, path)
    if schema.get("type") == "object":
        props = schema.get("properties") or {}
        for k, sub in props.items():
            yield from iter_digest_annotations(sub, doc, f"{path}.{k}")
        addl = schema.get("additionalProperties")
        if isinstance(addl, dict):
            yield from iter_digest_annotations(addl, doc, f"{path}.*")
    if schema.get("type") == "array":
        items = schema.get("items")
        if isinstance(items, dict):
            yield from iter_digest_annotations(items, doc, f"{path}[]")


def _get_path(obj: Any, dotted: str) -> list[tuple[str, Any]]:
    """Return (concrete_path, value) for a template path with [] wildcards."""
    parts = dotted.split(".")
    current = [(parts[0], obj)]
    for part in parts[1:]:
        nxt = []
        is_arr = part.endswith("[]")
        key = part[:-2] if is_arr else part
        for p, val in current:
            if not isinstance(val, dict) or key not in val:
                continue
            child = val[key]
            if is_arr:
                if not isinstance(child, list):
                    continue
                for i, el in enumerate(child):
                    nxt.append((f"{p}.{key}[{i}]", el))
            else:
                nxt.append((f"{p}.{key}", child))
        current = nxt
    return current


def _hex_of(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if ":" in value:
        prefix, rest = value.split(":", 1)
        if len(rest) == 64 and all(c in "0123456789abcdef" for c in rest):
            return rest
        return None
    if len(value) == 64 and all(c in "0123456789abcdef" for c in value):
        return value
    return None


def admit_digest_annotation(store, value: Any, ann: dict, *, path: str) -> dict:
    """Admit one annotated digest field against retained bytes."""
    representation = ann.get("representation")
    retention = ann.get("retention")
    hex_d = _hex_of(value)
    if representation == "capability-manifest-id" or retention == "derived":
        return {"path": path, "ok": True, "kind": "derived", "value": value}
    if representation == "snapshot-path":
        return {"path": path, "ok": True, "kind": "snapshot-path", "value": value}
    if hex_d is None:
        raise AdmissionError("DIGEST_FIELD_SHAPE", f"{path}={value!r}")
    if hex_d not in store.blobs:
        raise AdmissionError("DIGEST_PREIMAGE_MISSING", f"{path} {hex_d}")
    raw = store.blobs[hex_d]
    rehash = hashlib.sha256(raw).hexdigest()
    if rehash != hex_d:
        raise AdmissionError("DIGEST_REHASH", f"{path} {hex_d} -> {rehash}")
    if representation == "raw-artifact":
        return {"path": path, "ok": True, "kind": "raw-artifact", "digest": hex_d, "bytes": len(raw)}
    if representation == "canonical-record":
        parsed = admit_raw(raw)
        if C(parsed) != raw:
            raise AdmissionError("CANONICAL_REMAINDER", path)
        rec = ann.get("record") or {}
        document = rec.get("document")
        selector = rec.get("selector")
        stock = None
        if document:
            # Documents in annotations are kit-relative under docs/coop/design-corrections/
            rel = document
            if not rel.startswith("docs/"):
                rel = "docs/coop/design-corrections/" + document
            stock = validate_against(parsed, rel, selector=selector or "#", label=path)
            if not stock["stockOk"]:
                raise AdmissionError("DIGEST_RECORD_SCHEMA", f"{path}: {stock['errors'][:3]}")
        return {"path": path, "ok": True, "kind": "canonical-record", "digest": hex_d, "stock": stock}
    if representation == "h-identity":
        domain = ann.get("domain")
        allowed = {domain} if domain else None
        if ann.get("domainSet"):
            allowed = None  # native domain set; parse without a single domain pin
        parsed = parse_h_frame(raw, allowed_domains=allowed)
        return {
            "path": path,
            "ok": True,
            "kind": "h-identity",
            "digest": hex_d,
            "domain": parsed["domain"],
        }
    # Other representations (payload class, etc.) still require retained bytes.
    return {"path": path, "ok": True, "kind": representation or "retained", "digest": hex_d}


def admit_record_annotations(store, instance: Any, schema: dict, doc: dict, *, root_path: str) -> list[dict]:
    return _walk_instance(store, instance, schema, doc, path=root_path)


def _values_under(instance: Any, rel: str) -> list[tuple[str, Any]]:
    if not rel:
        return [("$", instance)]
    return _get_path({"$": instance}, "$." + rel if not rel.startswith("$") else rel)


def _walk_instance(store, instance: Any, schema: dict, doc: dict, *, path: str) -> list[dict]:
    out: list[dict] = []
    schema = _resolve_ref(schema, doc)
    if not isinstance(schema, dict):
        return out
    if "x-opensip-digest" in schema and instance is not None:
        rec = admit_digest_annotation(store, instance, schema["x-opensip-digest"], path=path)
        out.append(rec)
    if "allOf" in schema:
        for sub in schema["allOf"]:
            out.extend(_walk_instance(store, instance, sub, doc, path=path))
    if schema.get("type") == "array" and isinstance(instance, list):
        ann = schema.get("x-opensip-order")
        if ann is not None:
            check_order(instance, ann, path=path)
        items = schema.get("items") or {}
        for i, el in enumerate(instance):
            out.extend(_walk_instance(store, el, items, doc, path=f"{path}[{i}]"))
    if schema.get("type") == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        for k, v in instance.items():
            if k in props:
                out.extend(_walk_instance(store, v, props[k], doc, path=f"{path}.{k}"))
    return out


def closure_membership_check(*, plan: dict, closures: dict[str, dict], graph: dict) -> list[dict]:
    ident = _load(IDENT_REL)
    law = ident["x-opensip-digest-domains"]["closureMembership"]
    kinds = ident["x-opensip-digest-domains"]["closureKinds"]["byField"]
    selected = set(plan["semanticClosures"])
    joins = []

    def kind_of(cid: str) -> str:
        rec = closures.get(cid)
        if rec is None:
            raise AdmissionError("CLOSURE_NOT_RETAINED", cid)
        return rec["kind"]

    for field, note in law["direct"].items():
        values = graph.get("directMembers", {}).get(field) or []
        for cid in values:
            ok = cid in selected
            k_ok = kind_of(cid) == kinds.get(field)
            joins.append(
                {
                    "field": field,
                    "closure": cid,
                    "selected": ok,
                    "kindOk": k_ok,
                    "expectedKind": kinds.get(field),
                    "actualKind": kind_of(cid),
                    "note": note,
                }
            )
            if not ok:
                raise AdmissionError("UNSELECTED_DIRECT_CLOSURE", f"{field} {cid} not in plan.semanticClosures")
            if not k_ok:
                raise AdmissionError("CLOSURE_KIND", f"{field} kind {kind_of(cid)} != {kinds.get(field)}")
    for field, note in law["equalToDirect"].items():
        values = graph.get("equalToDirect", {}).get(field) or []
        partners = graph.get("equalToDirectPartners", {}).get(field) or []
        for cid, partner in zip(values, partners):
            if cid != partner:
                raise AdmissionError("EQUAL_TO_DIRECT_MISMATCH", f"{field} {cid} != {partner}")
            joins.append({"field": field, "closure": cid, "equals": partner, "note": note})
    return joins


def admit_execution_inputs_laws(store, g: dict, matrix: dict) -> list[dict]:
    joins = []
    ei = g["execution_inputs"]
    plan = g["plan"]
    exec_plan = g["execution_plan"]
    views = g["views_full"]
    inventories_by_digest = {hashlib.sha256(C(inv)).hexdigest(): inv for inv in g["inventories"]}

    # stage outputDomains / receipts
    stages = exec_plan["stages"]
    receipts = ei["hostCapture"]["stageReceipts"]
    if len(stages) != len(receipts):
        raise AdmissionError("EXECUTION_INPUTS_RECEIPT_TOTALITY", f"{len(stages)} vs {len(receipts)}")
    for st, rec in zip(stages, receipts):
        if rec["ordinal"] != st["ordinal"]:
            raise AdmissionError("EXECUTION_INPUTS_STAGE_ORDINAL", str(rec["ordinal"]))
        if rec["outputDomains"] != st["outputDomains"]:
            raise AdmissionError("EXECUTION_INPUTS_STAGE_PRODUCER", "outputDomains")
        if rec["stageSpecDigest"] != st["stageSpecDigest"]:
            raise AdmissionError("EXECUTION_INPUTS_STAGE_PRODUCER", "stageSpecDigest")
        for r in rec["outputRefs"]:
            if r["domain"] not in rec["outputDomains"]:
                raise AdmissionError("EXECUTION_INPUTS_OUTPUT_BACKLINK", r["domain"])
        if rec["state"] == "complete" and rec["unavailableReason"] is not None:
            raise AdmissionError("EXECUTION_INPUTS_STAGE_PRODUCER", "unavailableReason")
    joins.append({"name": "receipt-totality", "ok": True, "detail": f"n={len(receipts)}"})

    # reference fixture: view-only stage
    for st in stages:
        if set(st["outputDomains"]) != STAGE_PRODUCED_DOMAINS_REFERENCE:
            raise AdmissionError(
                "EXECUTION_INPUTS_HOST_DERIVED",
                f"reference derive-inventory-view stage outputDomains {st['outputDomains']} != ['view']",
            )
    joins.append({"name": "stage-outputDomains-view-only", "ok": True, "detail": "view"})

    complete_output_refs = []
    for rec in receipts:
        if rec["state"] == "complete":
            complete_output_refs.extend(rec["outputRefs"])
    expected_selected = selected_refs_totality(
        complete_receipt_output_refs=complete_output_refs,
        views=views,
        cell_outcomes=ei["cellOutcomes"],
        plan_import_ids=plan.get("importIds") or [],
        host_derived_refs=ei["hostCapture"]["hostDerivedRefs"],
    )
    if sort_c(ei["selectedRefs"]) != expected_selected:
        raise AdmissionError(
            "EXECUTION_INPUTS_SELECTED_COVER",
            f"selectedRefs {ei['selectedRefs']} != expected {expected_selected}",
        )
    joins.append({"name": "selectedRefs-exact-totality", "ok": True, "detail": str(len(expected_selected))})
    for r in ei["selectedRefs"]:
        if r["domain"] in FORBIDDEN_SELECTED_DOMAINS:
            raise AdmissionError("EXECUTION_INPUTS_SELECTED_COVER", r["domain"])
    if not blob_selected_equals_host_derived(ei["selectedRefs"], ei["hostCapture"]["hostDerivedRefs"]):
        raise AdmissionError("EXECUTION_INPUTS_HOST_DERIVED", "blob selectedRefs != hostDerivedRefs")
    joins.append({"name": "hostDerivedRefs-equals-blob-selected", "ok": True, "detail": ""})

    # native coverage + derive_outcome
    view_covs = g["view_coverages_full"]
    vcs = g["vcs"]
    derived_by_cell: dict[tuple[int, int], list[dict]] = {}
    expected_pairs_by_cell: dict[tuple[int, int], set[tuple[str, str]]] = {}
    for outcome in ei["cellOutcomes"]:
        loc = (outcome["cellOrdinal"], outcome["programOrdinal"])
        expected_pairs_by_cell[loc] = set(expected_matrix_accounts(outcome["capabilityId"], matrix))
        derived_by_cell.setdefault(loc, [])

    present_pairs: dict[tuple[int, int], set[tuple[str, str]]] = {}
    derived_accounts_all = []
    for acc in ei["nativeCoverageAccounts"]:
        loc = (acc["cellOrdinal"], acc["programOrdinal"])
        present_pairs.setdefault(loc, set()).add((acc["relation"], acc["resolution"]))
        outcome = next(
            o
            for o in ei["cellOutcomes"]
            if o["cellOrdinal"] == acc["cellOrdinal"] and o["programOrdinal"] == acc["programOrdinal"]
        )
        if acc["relation"] == "vcs-change":
            expected_app = vcs_applicability(vcs)
            if acc["applicability"] != expected_app:
                raise AdmissionError("EXECUTION_INPUTS_VCS_APPLICABILITY", acc["applicability"])
        matching = matching_coverages_for_account(
            account=acc,
            view_coverages=view_covs,
            enumerator_closure=outcome["enumeratorClosure"],
            universe=outcome["universe"],
        )
        derived_acc = derive_account(account=acc, matching_coverage_entries=matching)
        derived_by_cell[loc].append(derived_acc)
        derived_accounts_all.append(derived_acc)
    for loc, expected in expected_pairs_by_cell.items():
        present = present_pairs.get(loc, set())
        if present != expected:
            raise AdmissionError(
                "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
                f"cell {loc} present {sorted(present)} expected {sorted(expected)}",
            )
    joins.append(
        {
            "name": "native-coverage-account-totality",
            "ok": True,
            "detail": str({str(k): sorted(v) for k, v in present_pairs.items()}),
        }
    )

    for outcome in ei["cellOutcomes"]:
        loc = (outcome["cellOrdinal"], outcome["programOrdinal"])
        invs = [inventories_by_digest[d] for d in outcome["inventoryDigests"]]
        derived = derive_outcome(
            enumerator_status=outcome["enumeratorStatus"],
            universe=outcome["universe"],
            inventories=invs,
            derived_accounts=derived_by_cell[loc],
            candidate_state=None,
            candidate_owed=False,
        )
        join_host_outcome(outcome, derived)
        if outcome["required"] and derived["state"] != "complete":
            raise AdmissionError(
                "EXECUTION_INPUTS_OUTCOME_DERIVE",
                f"required cell {loc} derived {derived['state']}",
            )
        joins.append(
            {
                "name": f"derive_outcome[{outcome['ordinal']}]",
                "ok": True,
                "detail": derived["reason"] + ":" + derived["state"],
            }
        )
    return joins


def sort_c(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))


def admit_full_pilot(store, g: dict) -> dict:
    """Independent annotated-owner admission of the syntax-code pilot graph."""
    joins: list[dict] = []

    def rec(name: str, ok: bool, detail: str = "") -> None:
        joins.append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            raise AdmissionError(name, detail)

    ident = _load(IDENT_REL)
    exec_doc = _load(EXEC_REL)
    enum_doc = _load(ENUM_REL)
    emis_doc = _load(EMIS_REL)
    sinv_doc = _load(SINV_REL)
    native_doc = _load(NATIVE_REL)
    rel_doc = _load(REL_REL)
    matrix = _load(MATRIX_REL)

    digest_hits = []
    digest_hits.extend(
        admit_record_annotations(store, g["plan"], ident["$defs"]["plan"], ident, root_path="plan")
    )
    digest_hits.extend(
        admit_record_annotations(store, g["run"], ident["$defs"]["run"], ident, root_path="run")
    )
    digest_hits.extend(
        admit_record_annotations(store, g["snapshot"], ident["$defs"]["snapshot"], ident, root_path="snapshot")
    )
    digest_hits.extend(
        admit_record_annotations(
            store, g["claimed_proof"], ident["$defs"]["proof-bundle"], ident, root_path="proof"
        )
    )
    digest_hits.extend(
        admit_record_annotations(store, g["seal"], ident["$defs"]["evaluation-seal"], ident, root_path="seal")
    )
    digest_hits.extend(
        admit_record_annotations(
            store, g["evidence"], ident["$defs"]["semantic-evidence"], ident, root_path="evidence"
        )
    )
    digest_hits.extend(
        admit_record_annotations(store, g["view"], ident["$defs"]["view"], ident, root_path="view")
    )
    for i, f in enumerate(g["facts"]):
        digest_hits.extend(
            admit_record_annotations(store, f["record"], ident["$defs"]["fact"], ident, root_path=f"fact[{i}]")
        )
    for i, c in enumerate(g["coverages_h"]):
        digest_hits.extend(
            admit_record_annotations(
                store, c, ident["$defs"]["coverage"], ident, root_path=f"coverage[{i}]"
            )
        )
    digest_hits.extend(
        admit_record_annotations(
            store, g["execution_inputs"], exec_doc, exec_doc, root_path="execution-inputs"
        )
    )
    digest_hits.extend(
        admit_record_annotations(store, g["enum_plan"], enum_doc, enum_doc, root_path="enumeration-plan")
    )
    digest_hits.extend(
        admit_record_annotations(store, g["emission_plan"], emis_doc, emis_doc, root_path="emission-plan")
    )
    for i, inv in enumerate(g["inventories"]):
        digest_hits.extend(
            admit_record_annotations(store, inv, sinv_doc, sinv_doc, root_path=f"inventory[{i}]")
        )
    digest_hits.extend(
        admit_record_annotations(
            store, g["execution_plan"], ident["$defs"]["execution-plan"], ident, root_path="execution-plan"
        )
    )
    digest_hits.extend(
        admit_record_annotations(
            store, g["stage_spec"], ident["$defs"]["stage-spec"], ident, root_path="stage-spec"
        )
    )
    for cid, crec in g["closures"].items():
        digest_hits.extend(
            admit_record_annotations(
                store, crec, ident["$defs"]["closure"], ident, root_path=f"closure[{crec['kind']}]"
            )
        )
    digest_hits.extend(
        admit_record_annotations(
            store, g["ctx"], native_doc["$defs"]["SyntaxNativeContextV2"], native_doc, root_path="syntax-context"
        )
    )
    digest_hits.extend(
        admit_record_annotations(
            store,
            g["uni"],
            native_doc["$defs"]["SyntaxUniverseV2ResolvedInputs"],
            native_doc,
            root_path="syntax-universe",
        )
    )
    rec("annotated-digest-owners", True, f"n={len(digest_hits)}")

    # closure membership
    memb_graph = {
        "directMembers": {
            "view.producerClosure": [g["view"]["producerClosure"]],
            "stage-spec.producerClosure": [g["stage_spec"]["producerClosure"]],
            "subject-scope.enumeratorClosure": [sc["enumeratorClosure"] for sc in g["scopes"]],
            "evaluation-seal.evaluatorClosure": [g["seal"]["evaluatorClosure"]],
            "finding.ruleClosure": [],
            "cache-key.producerClosure": [],
        },
        "equalToDirect": {
            "fact.producerClosure": [f["record"]["producerClosure"] for f in g["facts"]],
            "proof-bundle.evaluatorClosure": [g["claimed_proof"]["evaluatorClosure"]],
        },
        "equalToDirectPartners": {
            "fact.producerClosure": [g["view"]["producerClosure"]] * len(g["facts"]),
            "proof-bundle.evaluatorClosure": [g["seal"]["evaluatorClosure"]],
        },
    }
    memb = closure_membership_check(plan=g["plan"], closures=g["closures"], graph=memb_graph)
    rec("closure-membership-direct-and-equal", True, json.dumps([m["field"] for m in memb if "field" in m]))

    # extra selected: detector (emission plan) + grammar (also selectedThroughOtherInput)
    selected = set(g["plan"]["semanticClosures"])
    det = g["emission_plan"]["rules"][0]["detectorClosure"]
    if det not in selected:
        raise AdmissionError("UNSELECTED_DETECTOR_CLOSURE_EXTRA", det)
    rec("detector-closure-extra-selected", True, det)
    grammar_id = g["ctx"]["grammarBundle"]["closureId"]
    if g["closures"][grammar_id]["kind"] != "grammar":
        raise AdmissionError("GRAMMAR_CLOSURE_KIND", g["closures"][grammar_id]["kind"])
    rec("grammar-closure-kind", True, grammar_id)

    # component-manifest join on every selected closure
    for cid in sorted(selected):
        cm = admit_component_manifest(store, g["closures"][cid])
        rec(f"component-manifest[{g['closures'][cid]['kind']}]", True, cm["digest"])

    ei_joins = admit_execution_inputs_laws(store, g, matrix)
    joins.extend(ei_joins)

    expected_eirefs = sort_c(
        list(g["execution_inputs"]["selectedRefs"])
        + [{"domain": "execution-inputs", "digest": g["execution_inputs_digest"]}]
    )
    claimed_eirefs = sort_c(list(g["claimed_proof"]["evaluationInputRefs"]))
    if claimed_eirefs != expected_eirefs:
        extra = [r for r in claimed_eirefs if r not in expected_eirefs]
        missing = [r for r in expected_eirefs if r not in claimed_eirefs]
        raise AdmissionError(
            "EVALUATION_INPUT_REFS_EQUALS_SELECTED_PLUS_MANIFEST",
            f"extra={extra} missing={missing}",
        )
    rec(
        "evaluationInputRefs-equals-selected-plus-manifest",
        True,
        f"n={len(claimed_eirefs)}",
    )

    # payload registry for each fact
    relreg = rel_doc["x-opensip-relation-registry"]["relations"]
    for f in g["facts"]:
        rel = f["record"]["relation"]
        row = relreg[rel]
        payload = g["payloads"][f["id"]]
        r = validate_against(payload, REL_REL, selector=row["selector"], label=f"payload-{rel}")
        if not r["stockOk"]:
            raise AdmissionError("FACT_PAYLOAD_SCHEMA", str(r["errors"][:3]))
        if f["record"]["resolution"] not in row["ladder"]:
            raise AdmissionError("RELATION_LADDER", rel)
        if row["universeRule"] == "same-only":
            if f["record"]["sourceUniverse"] != f["record"]["targetUniverse"]:
                raise AdmissionError("UNIVERSE_RULE", rel)
        pd = f["record"]["payloadDigest"]
        if hashlib.sha256(C(payload)).hexdigest() != pd:
            raise AdmissionError("FACT_PAYLOAD_C", rel)
        if f["record"]["payloadSchemaDigest"] != hashlib.sha256((KIT / REL_REL).read_bytes()).hexdigest():
            raise AdmissionError("PAYLOAD_SCHEMA_DIGEST", rel)
    rec("relation-payload-registry", True, str(sorted({f['record']['relation'] for f in g['facts']})))

    return {"ok": all(j["ok"] for j in joins), "joins": joins, "digestHits": len(digest_hits)}
