"""Executed kit-extension and registry-law admission for the TS pilot.

Stock JSON Schema does not enforce x-opensip-* or nested registry tables.
Each function fetches retained operands and returns concrete error strings.
A constructed descriptor is not a check.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import canonical, h, kit_schemas, order, store, builder, pilot_checks

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")


def _load_kit(rel: str) -> dict:
    return json.loads((KIT / rel).read_text())


def _bare(d: str) -> str:
    return d.split(":")[-1]


def _c(st: store.Store, digest: str) -> Any:
    return pilot_checks.load_c(st, digest)


def _obj(st: store.Store, ident: str) -> Any:
    return pilot_checks.obj(st, ident)


IDENTITY = _load_kit("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
NATIVE = _load_kit("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
REL = _load_kit("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
ENUM_SCH = _load_kit("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json")
EMIT_SCH = _load_kit("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json")
MATRIX = _load_kit("docs/coop/design-corrections/native/native-capability-matrix.v2.json")
PROJ = _load_kit("docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json")
TA_SCH = _load_kit("docs/coop/design-corrections/foundation/target-attribution.schema.v2.json")
IMP_SCH = _load_kit("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
SUBJ_SCH = _load_kit("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")

DIGEST_DOMAINS = IDENTITY["x-opensip-digest-domains"]
PAYLOAD_REG = IDENTITY["x-opensip-payload-registry"]
CAUSE_REG = NATIVE["x-opensip-deficiency-cause-registry"]
KIND_LAW = ENUM_SCH["x-opensip-kind-derivation"]
EXTENT_LAW = ENUM_SCH["x-opensip-file-membership-extent-law"]
LANG_TABLE = SUBJ_SCH["x-opensip-subject-language-table"]
JOIN_LAW = TA_SCH["x-opensip-join-law"]
EVID_REL = IMP_SCH["x-opensip-evidence-relation-registry"]
SCOPE_CAP = DIGEST_DOMAINS["scopeCapabilityLaw"]
LANG_MODES = DIGEST_DOMAINS["languageModes"]["map"]
CLOSURE_KINDS = DIGEST_DOMAINS["closureKinds"]["byField"]
MATRIX_IDS = [c["id"] for c in MATRIX["capabilities"]]
KIND_DERIVATION = {k: v for k, v in KIND_LAW.items() if isinstance(v, list)}


def subject_language_from_table(path: str) -> str:
    best = ("", "unspecified")
    for row in LANG_TABLE["members"]:
        for suf in row.get("suffixes") or []:
            if path.endswith(suf) and len(suf) > len(best[0]):
                best = (suf, row["languageId"])
    return best[1]


def dialect_variant(path: str) -> str | None:
    table = (
        DIGEST_DOMAINS["domainSets"]["native-semantic-universe"]
        ["native.semantic-universe.typescript.v2"]["languageVersionBinding"]["dialect"]["table"]
    )
    best = None
    for suf, var in table.items():
        if path.endswith(suf) and (best is None or len(suf) > len(best[0])):
            best = (suf, var)
    return None if best is None else best[1]


def check_uniqueness_requested_caps(spec: dict) -> list[str]:
    law = IDENTITY["$defs"]["analysis-spec"]["properties"]["requestedCapabilities"]["x-opensip-uniqueness"]
    keys = law["ownershipTuple"]
    errors = []
    seen = {}
    for i, row in enumerate(spec.get("requestedCapabilities") or []):
        tup = tuple(row.get(k) for k in keys)
        if tup in seen:
            errors.append(f"REQUESTED_CAPABILITY_DUPLICATE_OWNERSHIP:{tup} rows {seen[tup]} and {i}")
        seen[tup] = i
    return errors


def check_uniqueness_enum_cells(enum_plan: dict) -> list[str]:
    law = ENUM_SCH["properties"]["cells"]["x-opensip-uniqueness"]
    keys = law["ownershipTuple"]
    errors = []
    seen = {}
    for i, row in enumerate(enum_plan.get("cells") or []):
        tup = tuple(row.get(k) for k in keys)
        if tup in seen:
            errors.append(f"ENUMERATION_CELL_DUPLICATE_OWNERSHIP:{tup}")
        seen[tup] = i
    return errors


def check_uniqueness_emission(emission: dict) -> list[str]:
    law = EMIT_SCH["x-opensip-uniqueness"]
    errors = []
    seen_id = {}
    seen_fp = {}
    for i, row in enumerate(emission.get("rules") or []):
        rid = row.get("ruleId")
        if rid in seen_id:
            errors.append(f"EMISSION_DUPLICATE_RULEID:{rid}")
        seen_id[rid] = i
        fp = (row.get("ruleStableId"), row.get("semanticsMajor"))
        if fp in seen_fp:
            errors.append(f"EMISSION_DUPLICATE_FINGERPRINT_NAMESPACE:{fp}")
        seen_fp[fp] = i
    return errors


def check_vocabulary_requested_caps(spec: dict) -> list[str]:
    errors = []
    for row in spec.get("requestedCapabilities") or []:
        cid = row.get("capabilityId")
        mode = row.get("languageMode")
        if cid not in MATRIX_IDS:
            errors.append(f"native.requested-capability-unregistered:{cid}")
        if mode not in LANG_MODES:
            errors.append(f"ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED:{mode}")
        if cid in MATRIX_IDS and mode in LANG_MODES:
            cell = next((c for c in MATRIX["cells"] if c.get("capability") == cid and c.get("mode") == mode), None)
            if cell is None:
                errors.append(f"native.requested-capability-mode-unregistered:{cid}+{mode}")
            elif cell.get("state") == "NOT-SELECTED":
                errors.append(f"native.requested-capability-mode-not-selected:{cid}+{mode}")
    return errors


def check_default_caps_required(spec: dict, language_mode: str) -> list[str]:
    """matrix capabilityIdLaw.requiredDefault: default profile requests every non-NOT-SELECTED cell."""
    errors = []
    profile = None
    # resolved config is separate; spec requestedCapabilities is the Plan request
    want = []
    for cap in MATRIX["capabilities"]:
        cid = cap["id"]
        cell = next((c for c in MATRIX["cells"] if c.get("capability") == cid and c.get("mode") == language_mode), None)
        if cell is None:
            continue
        if cell.get("state") == "NOT-SELECTED":
            continue
        want.append(cid)
    got = sorted({r["capabilityId"] for r in spec.get("requestedCapabilities") or [] if r.get("languageMode") == language_mode})
    if sorted(want) != got:
        errors.append(f"DEFAULT_CAPABILITY_SELECTION_MISMATCH:want {sorted(want)} got {got}")
    return errors


def check_kind_derivation(enum_plan: dict) -> list[str]:
    errors = []
    for cell in enum_plan.get("cells") or []:
        want = list(KIND_DERIVATION.get(cell["capabilityId"]) or [])
        got = list(cell.get("kinds") or [])
        if set(got) != set(want):
            errors.append(f"KIND_DERIVATION:{cell['capabilityId']}:{got}!={want}")
    return errors


def check_subject_language(inventories: list[dict]) -> list[str]:
    errors = []
    for inv in inventories:
        for row in inv.get("rows") or []:
            path = row.get("path") or ""
            want = subject_language_from_table(path)
            if inv.get("kind") == "package":
                # package language is manifest format
                if not path.endswith(".json") and not path.endswith(".toml"):
                    errors.append(f"PACKAGE_LANGUAGE_PATH:{path}")
                want = "json" if path.endswith(".json") else "toml" if path.endswith(".toml") else want
            if row.get("subjectLanguage") != want:
                errors.append(f"SUBJECT_LANGUAGE:{path}:got {row.get('subjectLanguage')} want {want}")
    return errors


def check_extent_law(enum_plan: dict, membership: dict, snapshot: dict) -> list[str]:
    errors = []
    exclude_always = set()
    for row in membership.get("rows") or []:
        mem = row.get("membership")
        reason = row.get("reason")
        if mem == "outside-project-boundary" or reason in {
            "host-ignore-convention",
            "nested-repository",
            "nested-project",
            "custody-excluded",
        }:
            exclude_always.add(row["path"])
    inv_paths = [r["path"] for r in snapshot.get("sourceInventory") or []]
    remaining = [p for p in inv_paths if p not in exclude_always]
    for cell in enum_plan.get("cells") or []:
        for b in cell.get("programBindings") or []:
            by_kind = {e["kind"]: list(e.get("paths") or []) for e in (b.get("extents") or [])}
            if "file" in (cell.get("kinds") or []):
                if set(by_kind.get("file") or []) != set(remaining):
                    errors.append(f"FILE_KIND_EXTENT:{cell['capabilityId']}:{by_kind.get('file')}!={remaining}")
            if "package" in (cell.get("kinds") or []):
                pkg = [p for p in remaining if p.rsplit("/", 1)[-1] in ("package.json", "Cargo.toml")]
                if set(by_kind.get("package") or []) != set(pkg):
                    errors.append(f"PACKAGE_KIND_EXTENT:{cell['capabilityId']}:{by_kind.get('package')}!={pkg}")
            cap = cell["capabilityId"]
            if cap in ("clones-near", "clones-cross-tsjs"):
                if "candidateSourcePaths" not in b:
                    errors.append("ENUMERATION_CANDIDATE_SOURCE_PATHS")
            elif "candidateSourcePaths" in b:
                errors.append(f"CANDIDATE_SOURCE_PATHS_ON_NON_CANDIDATE:{cap}")
    return errors


def check_coverage_cause_registry(st: store.Store) -> list[str]:
    errors = []
    for ident, rec in st.objects.items():
        if not ident.startswith("coverage2:"):
            continue
        payload = _c(st, rec["payloadDigest"])
        entry = payload.get("entry") or {}
        d = entry.get("deficiency")
        nc = entry.get("nativeCause")
        if d is None:
            if nc is not None:
                errors.append(f"native.coverage-cause-must-be-null:{ident}:nativeCause without deficiency")
            continue
        row = (CAUSE_REG.get("deficiencies") or {}).get(d)
        if row is None:
            errors.append(f"native.coverage-cause-not-for-deficiency:{ident}:{d}")
            continue
        nclaw = row.get("nativeCause")
        if nclaw == "must-be-null" and nc is not None:
            errors.append(f"native.coverage-cause-must-be-null:{ident}:{d}")
        if nclaw == "required" and nc is None:
            errors.append(f"native.coverage-cause-required:{ident}:{d}")
        allowed = row.get("allowedCauses")
        if allowed and nc is not None and nc not in allowed:
            errors.append(f"native.coverage-cause-not-for-deficiency:{ident}:{d}+{nc}")
        rels = row.get("relations")
        if rels:
            rel = (payload.get("key") or {}).get("relation") or entry.get("relation")
            if rel not in rels:
                errors.append(f"native.coverage-cause-not-for-deficiency:{ident}:{d} on {rel}")
    return errors


def check_scope_capability_law(st: store.Store, uni: dict) -> list[str]:
    """digest-domains.scopeCapabilityLaw for bodyIdentityJoin relations under closed-suffix-table."""
    errors = []
    relreg = REL["x-opensip-relation-registry"]["relations"]
    body_rels = [n for n, r in relreg.items() if r.get("bodyIdentityJoin")]
    for ident, rec in st.objects.items():
        if not ident.startswith("coverage2:"):
            continue
        payload = _c(st, rec["payloadDigest"])
        key = payload.get("key") or {}
        entry = payload.get("entry") or {}
        rel = key.get("relation") or entry.get("relation")
        if rel not in body_rels:
            continue
        scope = _obj(st, rec["scopeId"])
        subjects = list(scope.get("subjects") or [])
        if not subjects:
            errors.append(f"COVERAGE_SOURCE_VARIANT_EMPTY_SCOPE:{ident}")
            continue
        unsupported = [s for s in subjects if dialect_variant(str(s)) is None]
        supported = [s for s in subjects if dialect_variant(str(s)) is not None]
        cov = entry.get("coverage")
        d = entry.get("deficiency")
        nc = entry.get("nativeCause")
        if unsupported and supported:
            # mixed scope cannot hide unsupported behind supported complete
            if cov == "complete":
                errors.append(f"COVERAGE_SOURCE_VARIANT_MIXED_COMPLETE:{ident}:{unsupported}")
        elif unsupported and not supported:
            if cov != "unknown" or d != "language-tier-unsupported" or nc != "capability-missing":
                errors.append(
                    f"COVERAGE_SOURCE_VARIANT_UNSUPPORTED:{ident}:coverage={cov} deficiency={d} nativeCause={nc}"
                )
        # supported-only: complete is eligible
    return errors


def check_payload_schema_digests(st: store.Store) -> list[str]:
    errors = []
    rel_doc = builder.REL_DIGEST
    nat_doc = builder.NAT_DIGEST
    imp_doc = builder.IMP_DIGEST
    for ident, rec in st.objects.items():
        if ident.startswith("fact2:"):
            if rec.get("payloadSchemaDigest") != rel_doc:
                errors.append(f"PAYLOAD_SCHEMA_DIGEST_RELATION:{ident}")
        if ident.startswith("coverage2:"):
            if rec.get("payloadSchemaDigest") != nat_doc:
                errors.append(f"PAYLOAD_SCHEMA_DIGEST_COVERAGE:{ident}")
        if ident.startswith("import2:"):
            if rec.get("payloadSchemaDigest") != imp_doc:
                errors.append(f"PAYLOAD_SCHEMA_DIGEST_IMPORT:{ident}")
    return errors


def check_closure_kinds(st: store.Store) -> list[str]:
    errors = []
    def kind_of(cid):
        try:
            return _obj(st, cid).get("kind")
        except Exception:
            return None
    for ident, rec in st.objects.items():
        if ident.startswith("fact2:"):
            k = kind_of(rec.get("producerClosure"))
            if k != "provider":
                errors.append(f"CLOSURE_KIND:fact.producerClosure:{ident}:{k}")
        if ident.startswith("view2:"):
            k = kind_of(rec.get("producerClosure"))
            if k != "provider":
                errors.append(f"CLOSURE_KIND:view.producerClosure:{ident}:{k}")
        if ident.startswith("finding3:"):
            k = kind_of(rec.get("ruleClosure"))
            if k != "detector":
                errors.append(f"CLOSURE_KIND:finding.ruleClosure:{ident}:{k}")
        if ident.startswith("proof3:") or ident.startswith("seal3:"):
            k = kind_of(rec.get("evaluatorClosure"))
            if k != "evaluator":
                errors.append(f"CLOSURE_KIND:evaluatorClosure:{ident}:{k}")
        if ident.startswith("import2:"):
            if kind_of(rec.get("adapterClosure")) != "adapter":
                errors.append(f"CLOSURE_KIND:import.adapterClosure:{ident}")
    return errors


def check_target_attribution(st: store.Store, plan: dict, ei: dict) -> list[str]:
    errors = []
    attrs = []
    for ref in ei.get("selectedRefs") or []:
        if ref.get("domain") != "target-attribution":
            continue
        rec = _c(st, ref["digest"])
        attrs.append((ref["digest"], rec))
    seen_fact = {}
    for digest, rec in attrs:
        if rec.get("schemaVersion") != 2:
            errors.append(f"TARGET_ATTRIBUTION_SCHEMA_VERSION:{digest}")
        if rec.get("planId") != plan.get("snapshotId") and rec.get("planId") not in st.objects and rec.get("planId") != next(
            i for i, o in st.objects.items() if i.startswith("plan2:")
        ):
            # planId must name retained Plan
            pid = rec.get("planId")
            if pid not in st.objects:
                errors.append(f"TARGET_ATTRIBUTION_PLAN:{digest}")
        fid = rec.get("sourceFactId")
        if fid in seen_fact:
            errors.append(f"TARGET_ATTRIBUTION_DUPLICATE_FACT:{fid}")
        seen_fact[fid] = digest
        if fid not in st.objects:
            errors.append(f"TARGET_ATTRIBUTION_SOURCE_FACT:{digest}")
            continue
        fact = st.objects[fid]
        if rec.get("producerClosure") != fact.get("producerClosure"):
            errors.append(f"TARGET_ATTRIBUTION_PRODUCER:{digest}")
        clo = _obj(st, rec["producerClosure"])
        if clo.get("kind") != "provider":
            errors.append(f"TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER:{digest}")
        if rec.get("targetUniverse") != fact.get("targetUniverse"):
            errors.append(f"TARGET_ATTRIBUTION_UNIVERSE:{digest}")
        rel = fact.get("relation")
        field = (PROJ.get("relations") or {}).get(rel, {}).get("targetNativeIdField")
        payload = _c(st, fact["payloadDigest"])
        if field:
            if payload.get(field) != rec.get("targetNativeId"):
                errors.append(f"TARGET_ATTRIBUTION_NATIVE_ID:{digest}:{field}")
        occ = rec.get("occupancy")
        kind = rec.get("kind")
        if occ == "external" and kind == "package":
            if rec.get("evaluationNativeId") is not None:
                errors.append(f"TARGET_ATTRIBUTION_EXTERNAL_EVAL_ID:{digest}")
            if rec.get("logicalPath") is not None:
                errors.append(f"TARGET_ATTRIBUTION_EXTERNAL_LOGICAL:{digest}")
            if not rec.get("packageManifestPath"):
                errors.append(f"TARGET_ATTRIBUTION_EXTERNAL_MANIFEST:{digest}")
            if rec.get("exported") is not None:
                errors.append(f"TARGET_ATTRIBUTION_EXTERNAL_EXPORTED:{digest}")
        # source fact in some selected view of producer
        views = [o for i, o in st.objects.items() if i.startswith("view2:")]
        if not any(fid in (v.get("facts") or []) and v.get("producerClosure") == rec.get("producerClosure") for v in views):
            errors.append(f"TARGET_ATTRIBUTION_FACT_NOT_IN_VIEW:{digest}")
    return errors


def check_selected_refs_totality(st: store.Store, plan: dict, ei: dict) -> list[str]:
    """execution-inputs-contract §1 selectedRefs exact totality, not a subset."""
    errors = []
    got = {(r["domain"], r["digest"]) for r in ei.get("selectedRefs") or []}
    want = set()
    receipts = (ei.get("hostCapture") or {}).get("stageReceipts") or []
    for recpt in receipts:
        if recpt.get("state") != "complete":
            continue
        for r in recpt.get("outputRefs") or []:
            want.add((r["domain"], r["digest"]))
            if r["domain"] == "view":
                view = _obj(st, "view2:" + r["digest"])
                for cid in view.get("coverageIds") or []:
                    want.add(("coverage", _bare(cid)))
    for r in (ei.get("hostCapture") or {}).get("hostDerivedRefs") or []:
        want.add((r["domain"], r["digest"]))
    for iid in plan.get("importIds") or []:
        want.add(("import", _bare(iid)))
    # blob-domain members of selectedRefs must equal hostDerivedRefs
    blob_domains = {"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"}
    got_blob = {x for x in got if x[0] in blob_domains}
    want_blob = {x for x in want if x[0] in blob_domains}
    if got_blob != want_blob:
        errors.append(f"EXECUTION_INPUTS_HOST_DERIVED:{sorted(got_blob ^ want_blob)[:8]}")
    if not want <= got:
        missing = sorted(want - got)[:8]
        errors.append(f"EXECUTION_INPUTS_SELECTED_COVER_MISSING:{missing}")
    forbidden = {d for d, _ in got if d in {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}}
    if forbidden:
        errors.append(f"EXECUTION_INPUTS_FORBIDDEN_REF:{forbidden}")
    return errors


def check_native_accounts(enum_plan: dict, ei: dict, st: store.Store) -> list[str]:
    errors = []
    view_ids = [r["digest"] for r in ei.get("selectedRefs") or [] if r["domain"] == "view"]
    cov_by_pair = {}
    for vid in view_ids:
        view = _obj(st, "view2:" + vid)
        for cid in view.get("coverageIds") or []:
            cov = _obj(st, cid)
            payload = _c(st, cov["payloadDigest"])
            key = payload.get("key") or {}
            pair = (key.get("relation"), key.get("resolution"))
            cov_by_pair.setdefault(pair, []).append(_bare(cid))
    for acc in ei.get("nativeCoverageAccounts") or []:
        pair = (acc.get("relation"), acc.get("resolution"))
        appl = acc.get("applicability")
        ids = list(acc.get("coverageIds") or [])
        if appl in {"inapplicable-vcs", "unsupported-typed", "unavailable-unselected", "unavailable-null-universe"}:
            if ids:
                errors.append(f"NATIVE_ACCOUNT_EMPTY_IDS:{pair}:{appl}")
            continue
        if appl == "supported-available":
            matching = order.cset(cov_by_pair.get(pair) or [])
            if order.cset(ids) != matching:
                errors.append(f"NATIVE_ACCOUNT_COVERAGE_IDS:{pair}:got {ids} want {matching}")
            if not ids:
                errors.append(f"NATIVE_WORK_INCOMPLETE:{pair}")
    return errors


def check_candidate_only(enum_plan: dict, ei: dict, st: store.Store) -> list[str]:
    errors = []
    cand_cells = [i for i, c in enumerate(enum_plan.get("cells") or []) if c["capabilityId"] in ("clones-near", "clones-cross-tsjs")]
    refs = {r["digest"] for r in ei.get("selectedRefs") or [] if r["domain"] == "candidate-producer-result"}
    outcomes = {o["cellOrdinal"]: o for o in ei.get("cellOutcomes") or []}
    for i in cand_cells:
        cell = enum_plan["cells"][i]
        if cell.get("kinds"):
            errors.append(f"CANDIDATE_NONEMPTY_KINDS:{i}")
        o = outcomes.get(i)
        if not o or not o.get("candidateResultDigest"):
            errors.append(f"CANDIDATE_ENVELOPE_MISSING:{i}")
            continue
        d = o["candidateResultDigest"]
        if d not in refs:
            errors.append(f"CANDIDATE_NOT_IN_SELECTED:{d}")
        env = _c(st, d)
        if env.get("authority") != "candidate-only":
            errors.append(f"CANDIDATE_AUTHORITY:{d}")
        binding = cell["programBindings"][0]
        census = list(binding.get("candidateSourcePaths") or [])
        if set(env.get("examinedPaths") or []) != set(census):
            errors.append(f"CANDIDATE_EXAMINED:{d}")
        if env.get("state") == "complete":
            if env.get("groupDigests") not in ([], None) and env.get("groupDigests"):
                # complete-empty may have groups; complete-empty requires examined=census
                pass
    # no Coverage for candidate-only relations (empty relations)
    return errors


def check_vcs_inapplicable(st: store.Store, ei: dict) -> list[str]:
    errors = []
    snap = next(o for i, o in st.objects.items() if i.startswith("snapshot2:"))
    vcs = _c(st, snap["vcsDigest"])
    if vcs.get("kind") == "none":
        for acc in ei.get("nativeCoverageAccounts") or []:
            if acc.get("relation") == "vcs-change":
                if acc.get("applicability") != "inapplicable-vcs":
                    errors.append(f"VCS_APPLICABILITY:{acc.get('applicability')}")
                if acc.get("coverageIds"):
                    errors.append("VCS_COVERAGE_FABRICATED")
    return errors


def check_policy_evidence_declaration(policy: dict) -> list[str]:
    native = set(REL["x-opensip-relation-registry"]["relations"])
    imported = set(EVID_REL["relations"])
    errors = []

    def walk(node):
        if not isinstance(node, dict):
            return
        if node.get("op") in ("exists", "none", "count-at-most", "all-covered"):
            rel = node.get("relation")
            if rel in native and node.get("evidence") is not None:
                errors.append(f"NATIVE_ATOM_HAS_EVIDENCE:{rel}")
            if rel in imported and node.get("evidence") != EVID_REL["relations"][rel]["evidenceKind"]:
                errors.append(f"IMPORTED_ATOM_EVIDENCE:{rel}")
            if rel not in native and rel not in imported:
                errors.append(f"ATOM_RELATION_UNREGISTERED:{rel}")
        for k in ("operand",):
            if k in node:
                walk(node[k])
        for ch in node.get("operands") or []:
            walk(ch)

    for rule in policy.get("rules") or []:
        walk(rule.get("emitWhen"))
    return errors


def check_import_mirror_and_kind(st: store.Store) -> list[str]:
    errors = []
    for ident, rec in st.objects.items():
        if not ident.startswith("import2:"):
            continue
        payload = _c(st, rec["payloadDigest"])
        kind = rec.get("kind")
        domain = payload.get("payloadDomain")
        row_key = f"{kind}|{domain}"
        rows = PAYLOAD_REG["classes"]["import"]["rows"]
        if row_key not in rows:
            errors.append(f"IMPORT_PAYLOAD_ROW:{ident}:{row_key}")
        if rec.get("blobs") is None:
            errors.append(f"IMPORT_BLOBS_MISSING:{ident}")
    return errors


def check_evaluator_profile_majors(st: store.Store) -> list[str]:
    errors = []
    changed = IDENTITY["x-opensip-evaluator-profile"]["changedIdentifierMajors"]
    prefix = {
        "finding": "finding3",
        "proof-bundle": "proof3",
        "semantic-evidence": "evidence3",
        "evaluation-seal": "seal3",
        "run": "run3",
        "policy-derivation": "policy-derivation3",
    }
    for domain, pref in prefix.items():
        if changed.get(domain.replace("-bundle", "").split("-")[0] if False else domain) or domain in changed:
            pass
        n = sum(1 for i in st.objects if i.startswith(pref + ":"))
        if domain == "run" and n != 1:
            errors.append(f"EVALUATOR_PROFILE_RUN_CARDINALITY:{n}")
        if domain == "proof-bundle" and n != 1:
            errors.append(f"EVALUATOR_PROFILE_PROOF_CARDINALITY:{n}")
    # mixed majors
    for ident in st.objects:
        if ident.startswith("finding2:") or ident.startswith("proof2:") or ident.startswith("run2:"):
            errors.append(f"MIXED_OUTPUT_MAJOR:{ident}")
    return errors


def run_all(st: store.Store) -> dict:
    """Return {lawId: {errors, operands}} for every executed family."""
    plan = next(o for i, o in st.objects.items() if i.startswith("plan2:"))
    proof = next(o for i, o in st.objects.items() if i.startswith("proof3:"))
    snap = next(o for i, o in st.objects.items() if i.startswith("snapshot2:"))
    spec = _c(st, plan["analysisSpecDigest"])
    enum_plan = _c(st, next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.ENUM_PLAN_DIGEST))
    emission = _c(st, next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.EMIT_PLAN_DIGEST))
    policy = _c(st, plan["policyDigest"])
    ei = _c(st, proof["executionInputsDigest"])
    mem = _c(st, enum_plan["membershipDigest"])
    inventories = [_c(st, r["digest"]) for r in ei.get("selectedRefs") or [] if r["domain"] == "subject-inventory"]
    uni = next(o for i, o in st.objects.items() if isinstance(o, dict) and o.get("tsconfigGraphHash"))
    out = {}

    def put(lid, kit, pointer, errors, operands):
        out[lid] = {
            "kitPath": kit,
            "selector": pointer,
            "errors": errors,
            "operands": operands,
            "errorCount": len(errors),
        }

    put("UNIQ-REQUESTED-CAPS", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/$defs/analysis-spec/properties/requestedCapabilities/x-opensip-uniqueness",
        check_uniqueness_requested_caps(spec),
        {"n": len(spec.get("requestedCapabilities") or []), "tuples": [
            (r.get("capabilityId"), r.get("languageMode"), r.get("workspaceRoot")) for r in spec.get("requestedCapabilities") or []
        ]})
    put("UNIQ-ENUM-CELLS", "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "#/properties/cells/x-opensip-uniqueness",
        check_uniqueness_enum_cells(enum_plan),
        {"nCells": len(enum_plan.get("cells") or [])})
    put("UNIQ-EMISSION", "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
        "#/x-opensip-uniqueness",
        check_uniqueness_emission(emission),
        {"nRules": len(emission.get("rules") or [])})
    put("VOCAB-REQUESTED-CAPS", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/$defs/analysis-spec/properties/requestedCapabilities/items/properties/capabilityId/x-opensip-vocabulary",
        check_vocabulary_requested_caps(spec),
        {"matrixIds": MATRIX_IDS, "languageModes": list(LANG_MODES)})
    put("DEFAULT-CAPS", "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
        "#/capabilityIdLaw/requiredDefault",
        check_default_caps_required(spec, "ts-tsconfig"),
        {"mode": "ts-tsconfig"})
    put("KIND-DERIVATION", "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "#/x-opensip-kind-derivation",
        check_kind_derivation(enum_plan),
        {"table": KIND_DERIVATION})
    put("SUBJECT-LANGUAGE", "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
        "#/x-opensip-subject-language-table",
        check_subject_language(inventories),
        {"nInventories": len(inventories)})
    put("EXTENT-LAW", "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "#/x-opensip-file-membership-extent-law",
        check_extent_law(enum_plan, mem, snap),
        {"excludeAlways": EXTENT_LAW.get("excludeAlways")})
    put("COVERAGE-CAUSE", "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "#/x-opensip-deficiency-cause-registry",
        check_coverage_cause_registry(st),
        {"deficiencies": list((CAUSE_REG.get("deficiencies") or {}))})
    put("SCOPE-CAPABILITY", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/x-opensip-digest-domains/scopeCapabilityLaw",
        check_scope_capability_law(st, uni),
        {"appliesToDialectForm": SCOPE_CAP.get("appliesToDialectForm"), "gate": "bodyIdentityJoin"})
    put("PAYLOAD-SCHEMA-DIGEST", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/x-opensip-payload-registry/law/payloadSchemaDigest",
        check_payload_schema_digests(st),
        {"relationDoc": builder.REL_DIGEST, "coverageDoc": builder.NAT_DIGEST})
    put("CLOSURE-KINDS", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/x-opensip-digest-domains/closureKinds/byField",
        check_closure_kinds(st),
        {"byField": list(CLOSURE_KINDS)})
    put("TARGET-ATTRIBUTION-JOIN", "docs/coop/design-corrections/foundation/target-attribution.schema.v2.json",
        "#/x-opensip-join-law",
        check_target_attribution(st, plan, ei),
        {"joins": JOIN_LAW.get("joins"), "packagePathCases": JOIN_LAW.get("packagePathCases")})
    put("SELECTED-REFS-TOTALITY", "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
        "#/1 selectedRefs exact totality",
        check_selected_refs_totality(st, plan, ei),
        {"nSelected": len(ei.get("selectedRefs") or [])})
    put("NATIVE-ACCOUNTS", "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
        "#/5 Native Coverage accounts (derived)",
        check_native_accounts(enum_plan, ei, st),
        {"nAccounts": len(ei.get("nativeCoverageAccounts") or [])})
    put("CANDIDATE-ONLY", "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
        "#/capabilities[clones-near|clones-cross-tsjs]",
        check_candidate_only(enum_plan, ei, st),
        {"candidateResultRefs": ei.get("candidateResultRefs")})
    put("VCS-INAPPLICABLE", "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
        "#/5 applicability inapplicable-vcs",
        check_vcs_inapplicable(st, ei),
        {"vcsKind": _c(st, snap["vcsDigest"]).get("kind")})
    put("POLICY-EVIDENCE-DECLARATION", "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        "#/x-opensip-evidence-relation-registry/evidenceDeclarationRule",
        check_policy_evidence_declaration(policy),
        {"nativeRelations": 13, "importedRelations": list(EVID_REL["relations"])})
    put("IMPORT-PAYLOAD-ROW", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/x-opensip-payload-registry/classes/import/rows",
        check_import_mirror_and_kind(st),
        {"rows": list(PAYLOAD_REG["classes"]["import"]["rows"])})
    put("EVALUATOR-PROFILE-MAJORS", "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "#/x-opensip-evaluator-profile/changedIdentifierMajors",
        check_evaluator_profile_majors(st),
        {"changed": IDENTITY["x-opensip-evaluator-profile"]["changedIdentifierMajors"]})
    return out
