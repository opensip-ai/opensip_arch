"""EnumerationPlanV1 / SubjectInventoryV1 admission and the independent population (enumeration-contract.v1 s1-s8,
composition s2, s9.5). Host-derived extents are re-derived from the retained snapshot + UnitMembershipV1 + scope."""
import tomllib

import canonical as K
import schemas
import membership as M
from native_ctx import suffix_select

KIT = schemas.kit()
ENUM_DOC = "foundation/enumeration-plan.schema.v1.json"
INV_DOC = "foundation/subject-inventory.schema.v1.json"
NE = "native/native-evidence.schemas.v2.json"
ID = "foundation/identity-schemas.v3.json"
KIND_DERIVATION = KIT.doc(ENUM_DOC)["x-opensip-kind-derivation"]
LANG_TABLE = KIT.doc(INV_DOC)["x-opensip-subject-language-table"]
LANGUAGE_MODES = KIT.doc(ID)["x-opensip-digest-domains"]["languageModes"]["map"]
POLICY_UNIVERSE_MAP = KIT.doc(ID)["x-opensip-evaluator-profile"]["policyUniverseMap"]
MATRIX = KIT.doc("native/native-capability-matrix.v2.json")
EXCLUDE_REASONS = {"host-ignore-convention", "nested-repository", "nested-project", "custody-excluded"}


def cell_state(capability, mode):
    return next(c for c in MATRIX["cells"] if c["capability"] == capability and c["mode"] == mode)


def subject_language(path):
    best, lang = None, "unspecified"
    for m in LANG_TABLE["members"]:
        for s in m["suffixes"]:
            if path.endswith(s) and (best is None or len(s) > len(best)):
                best, lang = s, m["languageId"]
    return lang


def root_internal(ws):
    return "" if ws == "." else ws


def file_extent(membership, scope, workspace_root):
    root = root_internal(workspace_root)
    out = []
    for row in membership["rows"]:
        if row["membership"] == "outside-project-boundary" or row["reason"] in EXCLUDE_REASONS:
            continue
        if not M.under(row["path"], root):
            continue
        if not M.in_foundation_scope(row["path"], scope):
            continue
        out.append(row["path"])
    return sorted(out, key=lambda p: K.C(p))


def named_manifests(inv_bytes, paths):
    """(named rows, failed paths) for first-party package manifests among paths."""
    named, failed = [], []
    for p in paths:
        base = p.split("/")[-1]
        if base not in ("package.json", "Cargo.toml"):
            continue
        try:
            if base == "package.json":
                data = K.parse_raw(inv_bytes[p])
                name = data.get("name") if isinstance(data, dict) else None
                version = data.get("version", "0.0.0") if isinstance(data, dict) else None
                if name is None:
                    continue
                if not isinstance(name, str) or not name:
                    failed.append(p)
                    continue
            else:
                data = tomllib.loads(inv_bytes[p].decode("utf-8"))
                pkg = data.get("package")
                if pkg is None:
                    continue
                name = pkg.get("name") if isinstance(pkg, dict) else None
                version = pkg.get("version", "0.0.0") if isinstance(pkg, dict) else None
                if not isinstance(name, str) or not name:
                    failed.append(p)
                    continue
            named.append({"path": p, "name": name, "version": version})
        except Exception:
            failed.append(p)
    return named, failed


def symbol_extent(bound, file_paths, membership):
    dom = bound["domain"]
    if dom == "native.semantic-universe.syntax.v2":
        ctx = bound["contextAdmission"]["context"]
        sel = set(bound["universe"]["selectedGrammarIds"])
        sufs = [s for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in sel and g["syntaxClass"] == "code" for s in g["suffixes"]]
        return sorted([p for p in file_paths if suffix_select(sufs, p) is not None], key=lambda p: K.C(p))
    if dom == "native.semantic-universe.typescript.v2":
        roots = set(bound["universe"]["programRootFiles"])
        return sorted([p for p in file_paths if p in roots], key=lambda p: K.C(p))
    own = bound["sourceUnitOwnership"]
    if own is None:
        return []
    sel = set(own["selectedUnitIds"])
    paths = {o["path"] for o in own["ownership"] if o["unitId"] in sel}
    return sorted([p for p in file_paths if p in paths], key=lambda p: K.C(p))


def program_entry_faults(ci, cell, b, bound, membership_rec):
    """HC-47 (source42 enumeration-contract.v1.md s1 lines 24-47; enumeration-plan.schema.v1.json AvailableProgramBindingV1.programEntry
    description): programEntry is the binding discriminator, not the compiler entry. An available default-unit binding has programEntry
    null. For TS/JS the retained entry is derived and compared: default-unit with a tsconfig.json/jsconfig.json marker -> the U-1 unit's
    markerPath equals TypeScriptConfigGraphV1.entryConfigPath; package.json marker -> entryConfigPath null and nodes []; explicit-plan-selection
    -> entryConfigPath equals programEntry. Rust and syntax-only entries are the universe H. Refusal: ENUMERATION_BINDING_PROGRAM_ENTRY
    (the key the contract publishes; native-evidence.md line 650 names the same join)."""
    key = f"ENUMERATION_BINDING_PROGRAM_ENTRY:{ci}:{b['ordinal']}"
    entry = b["programEntry"]
    if b["provenance"] == "default-unit" and entry is not None:
        return [key + ":default-unit-non-null"]
    if bound["domain"] != "native.semantic-universe.typescript.v2":
        return []
    graph = bound.get("configGraph") or {}
    if b["provenance"] == "explicit-plan-selection":
        return [] if entry is not None and graph.get("entryConfigPath") == entry else [key + ":explicit-entry"]
    root = root_internal(cell["workspaceRoot"])
    units = [u for u in ((membership_rec or {}).get("units") or []) if u.get("languageFamily") == "tsjs" and u.get("rootPath") == root]
    if len(units) != 1:
        return [key + ":no-u1-unit"]
    marker = units[0]["markerPath"]
    if marker.split("/")[-1] in ("tsconfig.json", "jsconfig.json"):
        ok = graph.get("entryConfigPath") == marker
    else:
        ok = graph.get("entryConfigPath") is None and graph.get("nodes") == []
    return [] if ok else [key + ":derived-entry"]


def admit_enumeration(plan, plan_id, analysis_spec, scope, membership_rec, enum_plan, inventories, bound_by_hex, closures, inv_bytes):
    """Returns (faults, index). index: {(cellOrdinal, programOrdinal, kind): (digest, inventory)} plus derived extents."""
    faults = []
    r = KIT.admit(enum_plan, ENUM_DOC, "#")
    if not r["ok"]:
        return [f"ENUMERATION_PLAN_SCHEMA:{r['stock'][:1]}{r['order'][:1]}"], None
    if enum_plan["snapshotId"] != plan["snapshotId"]:
        faults.append("ENUMERATION_PLAN_SNAPSHOT_MISMATCH")
    if enum_plan["scopeDigest"] != plan["scopeDigest"] or K.raw_digest(scope) != plan["scopeDigest"]:
        faults.append("ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH")
    # HC-39: native U-0 - the unit root representation is decided first, before anything reads a root
    root_faults = M.unit_root_faults(membership_rec.get("units") if isinstance(membership_rec, dict) else None, "ENUMERATION_MEMBERSHIP_UNIT_ROOT")
    faults += root_faults
    mr = KIT.admit(membership_rec, NE, "#/$defs/UnitMembershipV1")
    if not mr["ok"]:
        faults.append("ENUMERATION_MEMBERSHIP_SCHEMA")
    if enum_plan["membershipDigest"] != K.raw_digest(membership_rec):
        faults.append("ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH")
    if mr["ok"] and not root_faults:
        # HC-18: native U-4b.5 - re-derived from the RETAINED record at every enumeration admission
        faults += M.membership_order_faults(membership_rec, list(inv_bytes))
        faults += M.membership_row_faults(membership_rec)
    req = {(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in analysis_spec["requestedCapabilities"]}
    cells = {(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in enum_plan["cells"]}
    if req != cells or len(enum_plan["cells"]) != len(analysis_spec["requestedCapabilities"]):
        faults.append("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH")
    index = {"inventories": {}, "extents": {}, "cells": enum_plan["cells"]}
    semantic = set(plan["semanticClosures"])
    for ci, cell in enumerate(enum_plan["cells"]):
        if sorted(cell["kinds"]) != sorted(KIND_DERIVATION[cell["capabilityId"]]):
            faults.append(f"ENUMERATION_PLAN_KIND_DERIVATION:{ci}")
        if cell_state(cell["capabilityId"], cell["languageMode"])["state"] == "NOT-SELECTED":
            faults.append(f"native.requested-capability-mode-not-selected:{ci}")
        if not any(M.under(root_internal(cell["workspaceRoot"]), root_internal(w)) for w in scope["workspaceRoots"]):
            faults.append(f"ENUMERATION_CELL_ROOT_OUTSIDE_SCOPE:{ci}")
        candidate_only = cell["capabilityId"] in ("clones-near", "clones-cross-tsjs")
        # HC-47 (source42 enumeration contract s1 lines 20-21): provenance=default-unit is at most one binding per cell, at ordinal 0.
        # The contract names no refusal key for this, so the reconstruction's own key carries the cb24 prefix.
        defaults = [b for b in cell["programBindings"] if b["provenance"] == "default-unit"]
        if len(defaults) > 1 or any(b["ordinal"] != 0 for b in defaults):
            faults.append(f"cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY:{ci}")
        if len(cell["programBindings"]) > 128:
            faults.append("ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW")
        for b in cell["programBindings"]:
            po = b["ordinal"]
            avail = b["universe"] is not None
            if avail:
                if b["enumerator"]["status"] != "selected":
                    faults.append("ENUMERATION_BINDING_ENUMERATOR")
                if b["nativeContextDigest"] not in plan["nativeContextDigests"]:
                    faults.append("ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
                bound = bound_by_hex.get(b["universe"])
                if bound is None or bound["universe"]["nativeContextId"] != "sha256:" + str(b["nativeContextDigest"]):
                    faults.append("ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT")
                    continue
                want_dom = POLICY_UNIVERSE_MAP[LANGUAGE_MODES[cell["languageMode"]]]
                if bound["domain"] != want_dom:
                    faults.append(f"ENUMERATION_BINDING_UNIVERSE_DOMAIN:{ci}")
                if bound["domain"] == "native.semantic-universe.typescript.v2" and bound["universe"]["languageMode"] != cell["languageMode"]:
                    faults.append(f"ENUMERATION_BINDING_LANGUAGE_MODE:{ci}")
                faults += program_entry_faults(ci, cell, b, bound, membership_rec)
            else:
                if b["nativeContextDigest"] is not None and b["nativeContextDigest"] not in plan["nativeContextDigests"]:
                    faults.append("ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
                if cell["required"] and b["enumerator"]["status"] == "unselected":
                    faults.append("ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
                if b.get("deficiency") is None:
                    faults.append("ENUMERATION_BINDING_CAUSE")
            if b["enumerator"]["status"] == "selected":
                c = closures.get(b["enumerator"]["closureId"])
                if b["enumerator"]["closureId"] not in semantic or c is None or c["kind"] != "provider":
                    faults.append("ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
            if candidate_only:
                if avail and "candidateSourcePaths" not in b:
                    faults.append("ENUMERATION_CANDIDATE_SOURCE_PATHS")
            elif "candidateSourcePaths" in b:
                faults.append("ENUMERATION_CANDIDATE_SOURCE_PATHS")
            # host-derived extents
            fpaths = file_extent(membership_rec, scope, cell["workspaceRoot"])
            derived = {}
            if "file" in cell["kinds"]:
                derived["file"] = fpaths
            if "package" in cell["kinds"]:
                named, failed = named_manifests(inv_bytes, fpaths)
                derived["package"] = sorted({n["path"] for n in named} | set(failed), key=lambda p: K.C(p))
            if "symbol" in cell["kinds"]:
                if avail:
                    derived["symbol"] = symbol_extent(bound_by_hex[b["universe"]], fpaths, membership_rec)
                else:
                    derived["symbol"] = [p for p in fpaths if M.family_of(p) != "none"]
            got = {e["kind"]: e["paths"] for e in b["extents"]}
            if set(got) != set(cell["kinds"]):
                faults.append(f"ENUMERATION_INVENTORY_KIND_EXTENT_MISMATCH:{ci}:{po}")
            for k, paths in derived.items():
                if got.get(k) != paths:
                    faults.append(f"ENUMERATION_BINDING_EXTENT_MISMATCH:{ci}:{po}:{k}")
            index["extents"][(ci, po)] = derived
    # inventories: exactly one per (cell, program, kind)
    expected = {(ci, b["ordinal"], k) for ci, c in enumerate(enum_plan["cells"]) for b in c["programBindings"] for k in c["kinds"]}
    param_digest = K.raw_digest(enum_plan)
    seen = {}
    for digest, inv in inventories:
        ri = KIT.admit(inv, INV_DOC, "#")
        if not ri["ok"]:
            faults.append(f"ENUMERATION_INVENTORY_SCHEMA:{ri['stock'][:1]}{ri['order'][:1]}")
            continue
        if K.raw_digest(inv) != digest:
            faults.append("EXECUTION_INPUTS_REF_MISMATCH:inventory")
        loc = (inv["cellOrdinal"], inv["programOrdinal"], inv["kind"])
        if inv["planId"] != plan_id or inv["parameterDigest"] != param_digest:
            faults.append("ENUMERATION_INVENTORY_LOCATOR_JOIN")
        if loc not in expected:
            faults.append("ENUMERATION_INVENTORY_ORDINAL_UNBOUND")
            continue
        if loc in seen:
            faults.append("ENUMERATION_INVENTORY_DUPLICATE")
        seen[loc] = (digest, inv)
        ext = index["extents"].get((loc[0], loc[1]), {}).get(inv["kind"], [])
        if not set(inv["examinedPaths"]) <= set(ext):
            faults.append("ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT")
        for row in inv["rows"]:
            if row["path"] not in ext and not (inv["kind"] == "package" and row["path"] in ext):
                faults.append("ENUMERATION_INVENTORY_EXTERNAL_PATH")
            if row["kind"] != inv["kind"]:
                faults.append("ENUMERATION_INVENTORY_ROW_KIND")
            if inv["kind"] == "file":
                if not (row["nativeSubjectId"] == row["path"] == row["qualifiedName"]):
                    faults.append("ENUMERATION_INVENTORY_FILE_ROW")
                if row["subjectLanguage"] != subject_language(row["path"]):
                    faults.append("ENUMERATION_INVENTORY_SUBJECT_LANGUAGE")
            if inv["kind"] == "package":
                if row["nativeSubjectId"] != row["qualifiedName"]:
                    faults.append("ENUMERATION_PACKAGE_NAME")
                if row["subjectLanguage"] != ("json" if row["path"].endswith(".json") else "toml"):
                    faults.append("ENUMERATION_INVENTORY_SUBJECT_LANGUAGE")
        if inv["state"] == "complete":
            if inv["kind"] == "file":
                if set(inv["examinedPaths"]) != set(ext) or {r["path"] for r in inv["rows"]} != set(ext):
                    faults.append("ENUMERATION_INVENTORY_FILE_TOTALITY")
            elif inv["kind"] == "symbol":
                if set(inv["examinedPaths"]) != set(ext):
                    faults.append("ENUMERATION_INVENTORY_SYMBOL_EXTENT")
            else:
                named, failed = named_manifests(inv_bytes, ext)
                if failed:
                    faults.append("ENUMERATION_PACKAGE_PARSE")
                if {(n["path"], n["name"]) for n in named} != {(r["path"], r["nativeSubjectId"]) for r in inv["rows"]}:
                    faults.append("ENUMERATION_PACKAGE_TOTALITY")
    missing = expected - set(seen)
    for m in sorted(missing):
        faults.append(f"ENUMERATION_INVENTORY_MISSING_RECORD:{m}")
    index["inventories"] = seen
    return faults, index


def subject_record(universe, row):
    rec = {"schemaVersion": 3, "universe": universe, "kind": row["kind"], "nativeSubjectId": row["nativeSubjectId"]}
    if row["kind"] == "package":
        rec["packageManifestPath"] = row["path"]
    return rec
