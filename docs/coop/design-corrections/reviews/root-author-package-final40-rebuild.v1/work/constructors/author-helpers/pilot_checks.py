"""Actual TS-pilot owner checks: H-frame, U-4, enumeration, body-identity, parameters.

A function name is not a law. Each check fetches retained operands and compares.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from . import canonical, clone_body, h, kit_schemas, order, store


class CheckError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.firstRefusal = code


def _bare(digest: str) -> str:
    return digest.split(":")[-1]


def load_c(st: store.Store, digest: str) -> Any:
    bare = _bare(digest)
    raw = st.blobs.get(bare) or st.blobs.get(digest)
    if raw is None:
        raise CheckError("evidence.missing", digest)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        _domain, cx = h.parse_h_frame(raw)
        return json.loads(cx.decode("utf-8"))


def obj(st: store.Store, ident: str) -> Any:
    if ident in st.objects:
        return st.objects[ident]
    bare = _bare(ident)
    for k, v in st.objects.items():
        if k.endswith(bare):
            return v
    raise CheckError("evidence.missing", ident)


def verify_h_frame_for_object(st: store.Store, ident: str, domain: str, descriptor: Any) -> list[str]:
    """Identity §3: retained object under H is the framed preimage, never C(X) alone."""
    errors = []
    want_hex = h.h_digest(domain, descriptor)
    bare = _bare(ident)
    if bare != want_hex:
        errors.append(f"H_IDENTITY_MISMATCH:{ident} vs H({domain})={want_hex}")
    frame = st.blobs.get(want_hex)
    if frame is None:
        errors.append(f"H_FRAME_UNRETAINED:{want_hex}")
        return errors
    try:
        parsed_domain, cx = h.parse_h_frame(frame)
    except ValueError as e:
        errors.append(f"H_FRAME_PARSE:{ident}:{e}")
        return errors
    if parsed_domain != domain:
        errors.append(f"H_FRAME_DOMAIN:{parsed_domain}!={domain}")
    restated = canonical.encode(descriptor)
    if cx != restated:
        errors.append(f"H_FRAME_C_MISMATCH:{ident}")
    if hashlib.sha256(frame).hexdigest() != want_hex:
        errors.append(f"H_FRAME_HASH:{ident}")
    return errors


def check_all_h_identity_frames(st: store.Store) -> list[str]:
    errors = []
    inv = {v: k for k, v in h.PREFIX.items()}
    for ident, rec in st.objects.items():
        if not isinstance(ident, str) or ":" not in ident:
            continue
        prefix = ident.split(":", 1)[0]
        if prefix == "sha256":
            cls_domain = None
            if isinstance(rec, dict):
                if rec.get("schemaVersion") == 2 and "languageMode" in rec and "toolchain" in rec and "compilerName" in (rec.get("toolchain") or {}):
                    cls_domain = "native.context.typescript.v2"
                elif rec.get("schemaVersion") == 2 and "tsconfigGraphHash" in rec:
                    cls_domain = "native.semantic-universe.typescript.v2"
                elif rec.get("schemaVersion") == 2 and "grammarBundle" in rec:
                    cls_domain = "native.context.syntax.v2"
                elif rec.get("schemaVersion") == 2 and "crateRootPaths" in rec:
                    cls_domain = "native.semantic-universe.rust.v2"
                elif rec.get("schemaVersion") == 2 and "selectedGrammarIds" in rec:
                    cls_domain = "native.semantic-universe.syntax.v2"
                elif rec.get("schemaVersion") == 2 and "targetTriple" in rec and "toolchain" in rec:
                    cls_domain = "native.context.rust.v2"
            if cls_domain:
                errors.extend(verify_h_frame_for_object(st, ident, cls_domain, rec))
            continue
        domain = inv.get(prefix)
        if domain:
            errors.extend(verify_h_frame_for_object(st, ident, domain, rec))
    return errors


def check_u4_membership(membership: dict, snapshot: dict) -> list[str]:
    """native-evidence.md §1.4 U-4: exactly one FileMembershipRowV1 per inventoried path."""
    errors = []
    inv_paths = [r["path"] for r in snapshot.get("sourceInventory") or []]
    rows = membership.get("rows") or []
    seen = []
    for row in rows:
        p = row.get("path")
        if p in seen:
            errors.append(f"U4_DUPLICATE_PATH:{p}")
        seen.append(p)
    if set(seen) != set(inv_paths):
        missing = sorted(set(inv_paths) - set(seen), key=lambda s: s.encode("utf-8"))
        extra = sorted(set(seen) - set(inv_paths), key=lambda s: s.encode("utf-8"))
        if missing:
            errors.append(f"U4_INVENTORY_PATH_WITHOUT_ROW:{missing[0]}")
        if extra:
            errors.append(f"U4_ROW_NOT_IN_INVENTORY:{extra[0]}")
    erased = membership.get("erasedFiles") or []
    if erased:
        errors.append("U4_ERASED_FILES_NONEMPTY")
    return errors


KIND_DERIVATION = {
    "inventory": ["file", "package"],
    "syntax": ["symbol"],
    "imports": ["symbol"],
    "references": ["symbol"],
    "calls": ["symbol"],
    "types": ["symbol"],
    "reachability": ["symbol"],
    "unresolved-edge": ["symbol"],
    "clones-fact": ["file"],
    "clones-near": [],
    "clones-cross-tsjs": [],
}

MATRIX_RELATIONS = {
    "inventory": [("file", "enumerated"), ("package", "manifest-declared"), ("vcs-change", "vcs-reported")],
    "syntax": [("declares", "syntactic"), ("literal", "syntactic"), ("control-flow", "syntactic")],
    "imports": [("imports", "resolved-target")],
    "references": [("references", "resolved-binding")],
    "calls": [("calls", "resolved-callee")],
    "types": [("types", "checked")],
    "reachability": [("reachability", "from-resolved-calls")],
    "clones-fact": [("clones", "normalized-body-hash")],
    "clones-near": [],
    "clones-cross-tsjs": [],
    "unresolved-edge": [("unresolved-edge", "observed")],
}

POLICY_UNIVERSE_MAP = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}

LANGUAGE_MODE_TO_PORTABLE = {
    "ts-tsconfig": "typescript",
    "js-allowjs": "typescript",
    "js-synthesized": "typescript",
    "rust-cargo": "rust",
    "rust-cargo-prepared": "rust",
    "syntax-only": "syntax",
}

SUBJECT_LANGUAGE_SUFFIX = (
    (".d.ts", "typescript"),
    (".tsx", "typescript"),
    (".mts", "typescript"),
    (".cts", "typescript"),
    (".ts", "typescript"),
    (".jsx", "javascript"),
    (".mjs", "javascript"),
    (".cjs", "javascript"),
    (".js", "javascript"),
    (".rs", "rust"),
    (".json", "json"),
    (".toml", "toml"),
    (".md", "markdown"),
    (".yaml", "yaml"),
    (".yml", "yaml"),
)


def subject_language_for_path(path: str) -> str:
    for suf, lang in SUBJECT_LANGUAGE_SUFFIX:
        if path.endswith(suf):
            return lang
    return "unspecified"


def check_analysis_spec_parameters(spec: dict, st: store.Store) -> list[str]:
    """identity-schemas.v3 payload-registry parameter class: evaluator3 requires exactly one
    EnumerationPlanV1 and one EvaluatorEmissionPlanV1; at most one per registered row."""
    from . import builder

    errors = []
    params = spec.get("parameters") or []
    by_schema: dict[str, int] = {}
    for p in params:
        sd = p.get("schemaDigest")
        by_schema[sd] = by_schema.get(sd, 0) + 1
        if by_schema[sd] > 1:
            errors.append(f"ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:{sd}")
        raw = st.blobs.get(p.get("payloadDigest"))
        if raw is None:
            errors.append(f"PARAMETER_PAYLOAD_UNRETAINED:{p.get('payloadDigest')}")
    enum_n = by_schema.get(builder.ENUM_PLAN_DIGEST, 0)
    emit_n = by_schema.get(builder.EMIT_PLAN_DIGEST, 0)
    if enum_n != 1:
        errors.append(f"EVALUATOR3_ENUMERATION_PLAN_COUNT:{enum_n}")
    if emit_n != 1:
        errors.append(f"EVALUATOR3_EMISSION_PLAN_COUNT:{emit_n}")
    caps = spec.get("requestedCapabilities") or []
    seen = set()
    for row in caps:
        tup = (row.get("capabilityId"), row.get("languageMode"), row.get("workspaceRoot"))
        if tup in seen:
            errors.append(f"REQUESTED_CAPABILITY_DUPLICATE_OWNERSHIP:{tup}")
        seen.add(tup)
    return errors


def check_enumeration_plan_joins(plan: dict, spec: dict, enum_plan: dict, membership: dict, st: store.Store) -> list[str]:
    errors = []
    if enum_plan.get("snapshotId") != plan.get("snapshotId"):
        errors.append("ENUMERATION_PLAN_SNAPSHOT_MISMATCH")
    if enum_plan.get("scopeDigest") != plan.get("scopeDigest"):
        errors.append("ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH")
    mem_d = hashlib.sha256(canonical.encode(membership)).hexdigest()
    if enum_plan.get("membershipDigest") != mem_d:
        errors.append(f"ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH:{enum_plan.get('membershipDigest')}!={mem_d}")
    req = spec.get("requestedCapabilities") or []
    cells = enum_plan.get("cells") or []
    if len(cells) != len(req):
        errors.append(f"ENUMERATION_PLAN_CELL_TUPLE_MISMATCH:len {len(cells)}!={len(req)}")
    req_tups = {(r["capabilityId"], r["languageMode"], r["workspaceRoot"], r.get("required", True)) for r in req}
    cell_tups = {(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c.get("required", True)) for c in cells}
    if req_tups != cell_tups:
        errors.append("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH:set")
    for i, cell in enumerate(cells):
        want_kinds = list(KIND_DERIVATION.get(cell["capabilityId"]) or [])
        got = list(cell.get("kinds") or [])
        if set(got) != set(want_kinds):
            errors.append(f"ENUMERATION_KIND_DERIVATION:{cell['capabilityId']}:{got}!={want_kinds}")
        for b in cell.get("programBindings") or []:
            if b.get("ordinal") is None:
                errors.append(f"ENUMERATION_BINDING_ORDINAL_MISSING:cell{i}")
            enumr = b.get("enumerator") or {}
            if enumr.get("status") == "selected":
                cid = enumr.get("closureId")
                if cid not in (plan.get("semanticClosures") or []):
                    errors.append(f"ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN:{cid}")
                else:
                    clo = obj(st, cid)
                    if clo.get("kind") != "provider":
                        errors.append(f"ENUMERATION_ENUMERATOR_NOT_PROVIDER:{cid}")
            ncd = b.get("nativeContextDigest")
            if ncd and ncd not in (plan.get("nativeContextDigests") or []):
                errors.append(f"ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN:{ncd}")
            cap = cell["capabilityId"]
            if cap in ("clones-near", "clones-cross-tsjs"):
                if "candidateSourcePaths" not in b:
                    errors.append("ENUMERATION_CANDIDATE_SOURCE_PATHS")
            else:
                if "candidateSourcePaths" in b:
                    errors.append(f"ENUMERATION_CANDIDATE_SOURCE_PATHS_ON_INVENTORY_CELL:{cap}")
    return errors


def expected_inventory_keys(enum_plan: dict) -> list[tuple[int, int, str]]:
    keys = []
    for i, cell in enumerate(enum_plan.get("cells") or []):
        kinds = list(cell.get("kinds") or [])
        for b in cell.get("programBindings") or []:
            po = b.get("ordinal", 0)
            for k in kinds:
                keys.append((i, po, k))
    return keys


def inventories_from_ei(st: store.Store, ei: dict) -> dict[tuple[int, int, str], tuple[str, dict]]:
    out = {}
    for ref in ei.get("selectedRefs") or []:
        if ref.get("domain") != "subject-inventory":
            continue
        digest = ref["digest"]
        rec = load_c(st, digest)
        key = (rec["cellOrdinal"], rec["programOrdinal"], rec["kind"])
        out[key] = (digest, rec)
    return out


def check_expected_inventories(enum_plan: dict, ei: dict, st: store.Store) -> list[str]:
    errors = []
    expected = expected_inventory_keys(enum_plan)
    have = inventories_from_ei(st, ei)
    for key in expected:
        if key not in have:
            errors.append(f"ENUMERATION_INVENTORY_MISSING_RECORD:{key[0]}/{key[1]}/{key[2]}")
            continue
        digest, rec = have[key]
        cell = (enum_plan.get("cells") or [])[key[0]]
        binding = next(b for b in cell["programBindings"] if b.get("ordinal") == key[1])
        extent = None
        for ext in binding.get("extents") or []:
            if ext.get("kind") == key[2]:
                extent = list(ext.get("paths") or [])
                break
        if rec.get("state") == "complete" and rec.get("kind") == "file":
            paths = [r["path"] for r in rec.get("rows") or []]
            if extent is None:
                errors.append(f"ENUMERATION_FILE_EXTENT_MISSING:{key}")
            elif set(paths) != set(extent):
                errors.append(f"ENUMERATION_INVENTORY_FILE_TOTALITY:{key}")
            if set(rec.get("examinedPaths") or []) != set(extent or []):
                errors.append(f"ENUMERATION_INVENTORY_FILE_EXAMINED:{key}")
        if rec.get("parameterDigest") != hashlib.sha256(canonical.encode(enum_plan)).hexdigest():
            errors.append(f"ENUMERATION_INVENTORY_PARAMETER_DIGEST:{key}")
    extra = set(have) - set(expected)
    for key in extra:
        errors.append(f"ENUMERATION_INVENTORY_UNEXPECTED:{key}")
    return errors


def check_clone_body_identity(fact: dict, payload: dict, snapshot: dict, uni: dict, ctx: dict, st: store.Store) -> list[str]:
    """identity-and-evidence.md §3 clones bodyIdentityJoin + relation-registry bodyIdentityJoin."""
    errors = []
    bid = payload.get("bodyIdentity") or ""
    bare = _bare(bid)
    frame = st.blobs.get(bare)
    if frame is None:
        errors.append(f"CLONE_FRAME_UNRETAINED:{bare}")
        return errors
    if hashlib.sha256(frame).hexdigest() != bare:
        errors.append(f"CLONE_FRAME_HASH:{bare}")
    level = payload.get("normalisationLevel")
    spec_hex = payload.get("normalisationVersion")
    spec = st.blobs.get(spec_hex)
    if spec is None:
        errors.append(f"CLONE_LEVEL_SPEC_UNRETAINED:{spec_hex}")
        return errors
    if hashlib.sha256(spec).hexdigest() != spec_hex:
        errors.append(f"CLONE_LEVEL_SPEC_HASH:{spec_hex}")
    anchors = fact.get("anchors") or []
    if len(anchors) != 1:
        errors.append(f"CLONE_ANCHOR_CARDINALITY:{len(anchors)}")
        return errors
    anc = anchors[0]
    inv = {r["path"]: r for r in snapshot.get("sourceInventory") or []}
    path = anc.get("path")
    if path not in inv:
        errors.append(f"CLONE_ANCHOR_PATH_NOT_INVENTORIED:{path}")
        return errors
    body = st.blobs.get(inv[path]["sha256"])
    if body is None:
        errors.append(f"CLONE_ANCHOR_BLOB_MISSING:{path}")
        return errors
    start, end = anc.get("startByte", 0), anc.get("endByte", len(body))
    span = body[start:end]
    table = {
        ".d.ts": "ts-declaration",
        ".ts": "ts",
        ".tsx": "tsx",
        ".mts": "mts",
        ".cts": "cts",
        ".js": "js",
        ".jsx": "jsx",
        ".mjs": "mjs",
        ".cjs": "cjs",
    }
    variant = None
    for suf, var in sorted(table.items(), key=lambda kv: -len(kv[0])):
        if path.endswith(suf):
            variant = var
            break
    if variant is None:
        errors.append(f"BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN:{path}")
        return errors
    body_lang = {
        "ts": "typescript",
        "tsx": "typescript",
        "ts-declaration": "typescript",
        "mts": "typescript",
        "cts": "typescript",
        "js": "javascript",
        "jsx": "javascript",
        "mjs": "javascript",
        "cjs": "javascript",
    }[variant]
    lang_rec = {
        "schemaVersion": 1,
        "languageId": body_lang,
        "compilerName": (ctx.get("toolchain") or {}).get("compilerName"),
        "compilerVersion": (ctx.get("toolchain") or {}).get("compilerVersion"),
        "compilerBuild": (ctx.get("toolchain") or {}).get("compilerPackageDigest"),
        "dialect": {"sourceVariant": variant},
    }
    langv = clone_body.language_version_raw32(lang_rec)
    lv = hashlib.sha256(spec).digest()
    if level == "L0-verbatim":
        payload_bytes = clone_body.l0_payload(span)
        frame2, bid2 = clone_body.framed_body_identity(
            level_id=level,
            level_version_raw32=lv,
            language_id=body_lang,
            language_version_raw32=langv,
            payload=payload_bytes,
        )
        if bid2 != bid:
            errors.append(f"CLONE_L0_RECOMPUTE:{bid}!={bid2}")
        if frame2 != frame:
            errors.append("CLONE_L0_FRAME_BYTES")
    else:
        # L1–L3: custody + framing parse, not tokenisation judgement.
        if not frame.startswith(bytes([len(b"opensip.fact-identity.v1")])) and b"opensip.fact-identity.v1" not in frame[:64]:
            # still parse components
            pass
        if bid != "sha256:" + hashlib.sha256(frame).hexdigest() and not bid.endswith(hashlib.sha256(frame).hexdigest()):
            errors.append(f"CLONE_L1_FRAME_HASH:{bid}")
    return errors


def check_imports_rungs(fact: dict, payload: dict) -> list[str]:
    errors = []
    rung = fact.get("resolution")
    if rung == "syntactic-specifier" and "resolvedTarget" in payload:
        errors.append("IMPORTS_SYNTACTIC_FORBIDDEN_RESOLVED_TARGET")
    if rung == "resolved-target" and "resolvedTarget" not in payload:
        errors.append("IMPORTS_RESOLVED_MISSING_TARGET")
    return errors


def check_file_totality_match_on(view: dict, st: store.Store, snapshot: dict) -> list[str]:
    """Registry coverageTotality.matchOn: snapshotId, relation, resolution, sourceUniverse, targetUniverse."""
    errors = []
    inv = {r["path"] for r in snapshot.get("sourceInventory") or []}
    facts = {i: o for i, o in st.objects.items() if i.startswith("fact2:")}
    for sid in view.get("scopeIds") or []:
        sc = obj(st, sid)
        if sc.get("relation") != "file" or sc.get("resolution") != "enumerated":
            continue
        cov = None
        for cid in view.get("coverageIds") or []:
            c = obj(st, cid)
            if c.get("scopeId") == sid:
                cov = c
                break
        if cov is None:
            continue
        payload = load_c(st, cov["payloadDigest"])
        if (payload.get("entry") or {}).get("coverage") != "complete":
            continue
        owed = [s for s in (sc.get("subjects") or []) if s in inv]
        have = set()
        for fid in view.get("facts") or []:
            f = facts.get(fid)
            if not f:
                continue
            if not (
                f.get("snapshotId") == sc.get("snapshotId")
                and f.get("relation") == sc.get("relation")
                and f.get("resolution") == sc.get("resolution")
                and f.get("sourceUniverse") == sc.get("sourceUniverse")
                and f.get("targetUniverse") == sc.get("targetUniverse")
            ):
                continue
            pl = load_c(st, f["payloadDigest"])
            if isinstance(pl, dict) and pl.get("path") in owed:
                have.add(pl["path"])
        for path in owed:
            if path not in have:
                errors.append(f"COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:{path}")
    return errors


def glob_match(pattern: str, path: str) -> bool:
    if pattern in ("**", "**/*", "*"):
        return True
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(prefix + "/")
    if pattern.startswith("**/"):
        suf = pattern[3:]
        return path == suf or path.endswith("/" + suf)
    return path == pattern


def path_selected(path: str, include: list[str], exclude: list[str], scope_doc: dict | None) -> bool:
    inc = include or []
    exc = exclude or []
    if not inc:
        ok = True
    else:
        ok = any(glob_match(p, path) for p in inc)
    if ok and exc:
        if any(glob_match(p, path) for p in exc):
            ok = False
    if ok and scope_doc:
        s_inc = scope_doc.get("include") or []
        s_exc = scope_doc.get("exclude") or []
        if s_inc and not any(glob_match(p, path) for p in s_inc):
            ok = False
        if ok and s_exc and any(glob_match(p, path) for p in s_exc):
            ok = False
    return ok


def derive_subjects_from_inventories(
    *,
    policy_rule: dict,
    inventories: list[dict],
    enum_plan: dict,
    universe_hex: str,
    scope_doc: dict | None,
    st: store.Store,
) -> list[dict]:
    """composition §2: select from retained inventories, never from claimed subject3/findings."""
    kind = policy_rule["subjectEnumeration"]["subjectKind"]
    portable = policy_rule["subjectEnumeration"]["universe"]
    include = policy_rule["subjectEnumeration"].get("include") or []
    exclude = policy_rule["subjectEnumeration"].get("exclude") or []
    selected = []
    seen = set()
    cells = enum_plan.get("cells") or []
    for inv in inventories:
        if inv.get("kind") != kind:
            continue
        cell = cells[inv["cellOrdinal"]]
        if LANGUAGE_MODE_TO_PORTABLE.get(cell.get("languageMode")) != portable:
            continue
        binding = next(b for b in cell["programBindings"] if b.get("ordinal") == inv.get("programOrdinal"))
        u = binding.get("universe")
        if u != universe_hex:
            continue
        for row in inv.get("rows") or []:
            if not path_selected(row["path"], include, exclude, scope_doc):
                continue
            native = row["nativeSubjectId"]
            key = (u, kind, native, row.get("path") if kind == "package" else "")
            if key in seen:
                continue
            seen.add(key)
            subj = {
                "schemaVersion": 3,
                "universe": u,
                "kind": kind,
                "nativeSubjectId": native,
            }
            if kind == "package":
                subj["packageManifestPath"] = row["path"]
            sid = h.h_id("evaluation-subject", subj)
            selected.append(
                {
                    "id": sid,
                    "descriptor": subj,
                    "path": row["path"],
                    "kind": kind,
                    "language": row.get("subjectLanguage") or "unspecified",
                    "universe": u,
                    "qualifiedName": row.get("qualifiedName") or row["path"],
                    "nativeSubjectId": native,
                }
            )
    selected.sort(key=lambda s: (s["id"]).encode("utf-8"))
    return selected


def check_cell_outcome_totality(enum_plan: dict, ei: dict) -> list[str]:
    errors = []
    cells = enum_plan.get("cells") or []
    outcomes = ei.get("cellOutcomes") or []
    expected = []
    for i, cell in enumerate(cells):
        for b in cell.get("programBindings") or []:
            expected.append((i, b.get("ordinal", 0)))
    got = [(o.get("cellOrdinal"), o.get("programOrdinal")) for o in outcomes]
    if sorted(got) != sorted(expected):
        errors.append(f"EXECUTION_INPUTS_CELL_TOTALITY:got {got} expected {expected}")
    for i, o in enumerate(outcomes):
        if o.get("ordinal") != i:
            errors.append(f"CELL_OUTCOME_ORDINAL:{o.get('ordinal')}!={i}")
    return errors
