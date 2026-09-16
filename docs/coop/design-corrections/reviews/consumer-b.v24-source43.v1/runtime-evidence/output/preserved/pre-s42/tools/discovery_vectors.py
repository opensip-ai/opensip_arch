"""Discovery, membership and zero-config selection vectors (native-evidence.md s1.4 U-0..U-4b, U-8, U-9; s1.2 effective allowJs; Config2 join).

source41: section E re-measures the source39 s39-M1 vector under the published U-4b.2/U-4b.5 unitKind law; sections F-H add the U-0
root representation, U-4b.2 nested Cargo workspaces and the U-1/s1.2 mode selection. Every source41 vector also records what the
unchanged ported helper (preserved/s41-original-state/ref/membership.py) did, so the pre-correction behaviour stays measured.

Standalone vectors (not Runs) over independently chosen repository inventories:
  * U-4b units: order by (rootPath, languageFamily), ordinals, co-located rust+tsjs root, deepest-workspace folding and sorted
    memberPackageRoots, Cargo roots from units (member target pruned; src/target and packages/target ordinary), markers inside
    pruned trees never units, tsjs marker precedence and recognizer ids, excluded units at an admitted boundary;
  * U-4b rows: decision (a)-(e) with suffix family and final extension;
  * U-9: zero-config syntax-only fallback unit, unchanged rows, scope workspaceRoots ["."], default selection of every non-NOT-SELECTED
    syntax-only capability, no fallback in a mixed repository or with explicit roots, a default selection over zero units refusing
    NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT;
  * U-4b.5 enforcement over the RETAINED record: ENUMERATION_MEMBERSHIP_ORDER / ENUMERATION_MEMBERSHIP_ROW_DERIVATION controls.
Writes vectors/discovery-membership.json. Usage: python3 tools/seq.py <label> tools/discovery_vectors.py
"""
import copy
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/preserved/pre-s42"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import membership as M  # noqa: E402
import schemas  # noqa: E402
import phase7_vectors as P7  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("membership_s41_original", OUT + "/preserved/s41-original-state/ref/membership.py")
ORIG = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORIG)

KIT = schemas.kit()
NE = "native/native-evidence.schemas.v2.json"
failures = []
vectors = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def record(name, classification, **kw):
    row = dict({"vector": name, "classification": classification}, **kw)
    vectors.append(row)
    return row


def files(*paths):
    out = {}
    for p in paths:
        base = p.split("/")[-1]
        if base == "Cargo.toml":
            out[p] = b"[package]\nname = \"x\"\nversion = \"0.1.0\"\n"
        elif base in ("package.json", "tsconfig.json", "jsconfig.json"):
            out[p] = b"{}\n"
        else:
            out[p] = b"x\n"
    return out


def rows_by_path(membership):
    return {r["path"]: (r["languageFamily"], r["unitOrdinal"], r["membership"], r["reason"]) for r in membership["rows"]}


def default_selection(discovery):
    """U-9 / native default selection: a default selection over zero units is the internal host invariant refusal."""
    if not discovery["units"]:
        return None, "NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT"
    rows, faults = P7.default_capability_selection(discovery["units"])
    return rows, (faults[0] if faults else None)


def main():
    # ---- A. U-4b workspace: co-located rust+tsjs root, nested Cargo members, pruned markers, targets, nested tsjs unit
    inv = files("Cargo.toml", "package.json", "src/main.rs", "src/target/x.rs", "target/debug/build.rs",
                "crates/b/Cargo.toml", "crates/b/src/lib.rs", "crates/b/target/out.rs", "crates/a/Cargo.toml", "crates/a/src/lib.rs",
                "node_modules/left-pad/package.json", "node_modules/left-pad/Cargo.toml", "node_modules/left-pad/index.js",
                "packages/web/tsconfig.json", "packages/web/package.json", "packages/web/src/app.ts", "packages/target/index.ts",
                "packages/js/jsconfig.json", "packages/js/lib.js", ".git/config", "README.md", "LICENSE", "docs/notes.txt", "tools/gen.py")
    inv["Cargo.toml"] = b"[workspace]\nmembers = [\"crates/*\"]\n"
    disc = M.discover_units(inv)
    mem = M.assign_membership(inv, disc)
    units = [(u["unitOrdinal"], u["rootPath"], u["languageFamily"], u["languageMode"], u["unitKind"], u["recognizerId"], u["memberPackageRoots"])
             for u in disc["units"]]
    expected_units = [(0, "", "rust", "rust-cargo", "cargo-workspace", "cargo-workspace", ["crates/a", "crates/b"]),
                      (1, "", "tsjs", "js-synthesized", "js-program", "node-package", []),
                      (2, "packages/js", "tsjs", "js-allowjs", "js-program", "typescript-config", []),
                      (3, "packages/web", "tsjs", "ts-tsconfig", "ts-program", "typescript-config", [])]
    must("u4b-units", units == expected_units, units)
    rows = rows_by_path(mem)
    expected_rows = {
        "src/main.rs": ("rust", 0, "program-member", "deepest-unit-in-language"),
        "src/target/x.rs": ("rust", 0, "program-member", "deepest-unit-in-language"),
        "target/debug/build.rs": ("rust", None, "syntax-only", "host-ignore-convention"),
        "crates/b/target/out.rs": ("rust", None, "syntax-only", "host-ignore-convention"),
        "crates/b/src/lib.rs": ("rust", 0, "program-member", "deepest-unit-in-language"),
        "node_modules/left-pad/index.js": ("tsjs", None, "syntax-only", "host-ignore-convention"),
        "node_modules/left-pad/Cargo.toml": ("none", None, "syntax-only", "host-ignore-convention"),
        "packages/web/src/app.ts": ("tsjs", 3, "program-member", "deepest-unit-in-language"),
        "packages/target/index.ts": ("tsjs", 1, "program-member", "deepest-unit-in-language"),
        "packages/js/lib.js": ("tsjs", 2, "program-member", "deepest-unit-in-language"),
        ".git/config": ("none", None, "syntax-only", "host-ignore-convention"),
        "README.md": ("none", None, "syntax-only", "grammar-only"),
        "Cargo.toml": ("none", None, "syntax-only", "grammar-only"),
        "LICENSE": ("none", None, "unsupported-file", "no-bundled-grammar"),
        "docs/notes.txt": ("none", None, "unsupported-file", "no-bundled-grammar"),
        "tools/gen.py": ("none", None, "unsupported-file", "no-bundled-grammar")}
    row_diff = {p: (rows.get(p), want) for p, want in expected_rows.items() if rows.get(p) != want}
    must("u4b-rows", not row_diff, row_diff)
    must("u4b-row-order", [r["path"].encode() for r in mem["rows"]] == sorted(p.encode() for p in inv), None)
    must("u4b-unsupported-projection", mem["unsupportedFiles"] == ["LICENSE", "docs/notes.txt", "tools/gen.py"], mem["unsupportedFiles"])
    must("u4b-pruned-trees", [(t["path"], t["reason"]) for t in disc["prunedTrees"]] ==
         [(".git", "vcs-tree"), ("crates/b/target", "cargo-build-output"), ("node_modules", "dependency-tree"), ("target", "cargo-build-output")],
         disc["prunedTrees"])
    schema_ok = KIT.admit(mem, NE, "#/$defs/UnitMembershipV1")["ok"]
    must("u4b-membership-schema", schema_ok)
    must("u4b-retained-enforcement-positive", not M.membership_order_faults(mem, list(inv)) and not M.membership_row_faults(mem),
         (M.membership_order_faults(mem, list(inv)), M.membership_row_faults(mem)))
    record("u4b-workspace", "valid", inventory=sorted(inv), units=disc["units"], membership=mem, prunedTrees=disc["prunedTrees"],
           scope=M.unit_scope_descriptor(disc), membershipSchemaAdmitted=schema_ok,
           notes=["co-located rust unit precedes its tsjs sibling at rootPath ''", "member crates fold into the root workspace; their target is pruned",
                  "src/target and packages/target are ordinary (no Cargo root parent)", "markers under node_modules are never units",
                  "tsconfig > jsconfig > package.json within one directory"])

    # ---- B. enforcement controls over the retained record
    def control(label, mutate, expect):
        bad = copy.deepcopy(mem)
        paths = mutate(bad) or list(inv)
        faults = M.membership_order_faults(bad, paths) + M.membership_row_faults(bad)
        ok = bool(faults) and faults[0].startswith(expect)
        must(f"enforcement:{label}", ok, faults)
        record(f"enforcement-{label}", "invalid", firstRefusal=faults[0] if faults else None, masksLater=faults[1:], expected=expect,
               schemaValid=KIT.admit(bad, NE, "#/$defs/UnitMembershipV1")["ok"])
    control("units-swapped", lambda m: m["units"].__setitem__(slice(0, 2), [m["units"][1], m["units"][0]]), "ENUMERATION_MEMBERSHIP_ORDER:units")
    control("ordinal-renumbered", lambda m: m["units"][3].__setitem__("unitOrdinal", 7), "ENUMERATION_MEMBERSHIP_ORDER:unitOrdinal")
    control("member-roots-unsorted", lambda m: m["units"][0].__setitem__("memberPackageRoots", ["crates/b", "crates/a"]),
            "ENUMERATION_MEMBERSHIP_ORDER:memberPackageRoots")
    control("rows-reversed", lambda m: m.__setitem__("rows", list(reversed(m["rows"]))), "ENUMERATION_MEMBERSHIP_ORDER:rows")
    control("row-dropped", lambda m: m.__setitem__("rows", [r for r in m["rows"] if r["path"] != "README.md"]),
            "ENUMERATION_MEMBERSHIP_ORDER:rows-not-one-per-inventory-path")
    control("unsupported-projection-wrong", lambda m: m.__setitem__("unsupportedFiles", ["LICENSE"]), "ENUMERATION_MEMBERSHIP_ORDER:unsupportedFiles")
    control("row-claimed-by-wrong-unit", lambda m: next(r for r in m["rows"] if r["path"] == "packages/web/src/app.ts").__setitem__("unitOrdinal", 1),
            "ENUMERATION_MEMBERSHIP_ROW_DERIVATION:packages/web/src/app.ts")
    control("pruned-row-as-member", lambda m: next(r for r in m["rows"] if r["path"] == "crates/b/target/out.rs").update(
        unitOrdinal=0, membership="program-member", reason="deepest-unit-in-language"), "ENUMERATION_MEMBERSHIP_ROW_DERIVATION:crates/b/target/out.rs")
    control("data-row-as-unsupported", lambda m: next(r for r in m["rows"] if r["path"] == "README.md").update(membership="unsupported-file", reason="no-bundled-grammar"),
            "ENUMERATION_MEMBERSHIP_ORDER:unsupportedFiles")
    # source41 U-4b.5 (lines 797-799): a tsjs unitKind is the projection of its mode; ts-program/js-program on another family refuses
    control("tsjs-kind-not-mode-projection", lambda m: m["units"][3].__setitem__("unitKind", "js-program"), "ENUMERATION_MEMBERSHIP_ORDER:unitKind:3")
    control("rust-unit-spelled-ts-program", lambda m: m["units"][0].__setitem__("unitKind", "ts-program"), "ENUMERATION_MEMBERSHIP_ORDER:unitKind-family:0")

    # ---- C. admitted boundary (U-8): nested project excluded, its files outside the boundary, no unit
    inv_b = files("package.json", "src/a.ts", "vendor/sub/package.json", "vendor/sub/lib.ts")
    boundaries = {"nestedRepositories": [], "nestedProjects": ["vendor/sub"], "custodyExcludedUnits": []}
    disc_b = M.discover_units(inv_b, boundaries)
    mem_b = M.assign_membership(inv_b, disc_b)
    must("u8-excluded-unit", disc_b["boundaries"]["excludedUnits"] == [{"path": "vendor/sub", "marker": "package.json", "reason": "nested-project",
                                                                         "anchor": "vendor/sub"}], disc_b["boundaries"])
    must("u8-outside-rows", mem_b["outsideBoundaryFiles"] == ["vendor/sub/lib.ts", "vendor/sub/package.json"] and
         rows_by_path(mem_b)["vendor/sub/lib.ts"] == ("tsjs", None, "outside-project-boundary", "nested-project"), mem_b)
    must("u8-enforcement-positive", not M.membership_order_faults(mem_b, list(inv_b)) and not M.membership_row_faults(mem_b))
    bad = copy.deepcopy(mem_b)
    next(r for r in bad["rows"] if r["path"] == "vendor/sub/lib.ts")["unitOrdinal"] = 0
    b_faults = M.membership_row_faults(bad)
    must("u8-outside-row-with-ordinal", b_faults == ["ENUMERATION_MEMBERSHIP_ROW_DERIVATION:vendor/sub/lib.ts"], b_faults)
    record("u8-boundary", "valid", inventory=sorted(inv_b), units=disc_b["units"], excludedUnits=disc_b["boundaries"]["excludedUnits"], membership=mem_b,
           outsideRowWithOrdinalFirstRefusal=b_faults[0] if b_faults else None)

    # ---- D. U-9 zero-config syntax-only fallback and default selection
    inv_s = files("README.md", "conf/app.yaml", "data/x.json", "tools/run.rs", "scripts/gen.js", "LICENSE")
    disc_s = M.discover_units(inv_s)
    mem_s = M.assign_membership(inv_s, disc_s)
    must("u9-fallback-unit", disc_s["fallback"] and disc_s["units"] == [dict({"unitOrdinal": 0}, **M.FALLBACK_UNIT)], disc_s["units"])
    must("u9-rows-unchanged", rows_by_path(mem_s)["tools/run.rs"] == ("rust", None, "syntax-only", "no-program-unit-for-language") and
         rows_by_path(mem_s)["scripts/gen.js"] == ("tsjs", None, "syntax-only", "no-program-unit-for-language") and
         rows_by_path(mem_s)["data/x.json"] == ("none", None, "syntax-only", "grammar-only") and
         rows_by_path(mem_s)["LICENSE"] == ("none", None, "unsupported-file", "no-bundled-grammar"), mem_s["rows"])
    must("u9-scope-root", M.unit_scope_descriptor(disc_s)["workspaceRoots"] == ["."], M.unit_scope_descriptor(disc_s))
    must("u9-membership-schema", KIT.admit(mem_s, NE, "#/$defs/UnitMembershipV1")["ok"])
    sel, sel_fault = default_selection(disc_s)
    matrix_syntax = sorted(c["capability"] for c in P7.EN.MATRIX["cells"] if c["mode"] == "syntax-only" and c["state"] != "NOT-SELECTED")
    must("u9-default-selection", sel_fault is None and sorted(r["capabilityId"] for r in sel) == matrix_syntax and
         all(r["languageMode"] == "syntax-only" and r["workspaceRoot"] == "." and r["required"] for r in sel), sel)
    must("u9-default-selection-admits", not P7.admit_requested_capabilities(sel), P7.admit_requested_capabilities(sel))
    record("u9-zero-config-syntax-only", "valid", inventory=sorted(inv_s), units=disc_s["units"], membership=mem_s, scope=M.unit_scope_descriptor(disc_s),
           defaultSelection=sel, matrixSyntaxOnlyCells={c["capability"]: c["state"] for c in P7.EN.MATRIX["cells"] if c["mode"] == "syntax-only"})
    inv_m = files("package.json", "src/a.ts", "tools/run.rs", "README.md")
    disc_m = M.discover_units(inv_m)
    must("u9-no-fallback-in-mixed-repository", not disc_m["fallback"] and [u["languageFamily"] for u in disc_m["units"]] == ["tsjs"] and
         rows_by_path(M.assign_membership(inv_m, disc_m))["tools/run.rs"] == ("rust", None, "syntax-only", "no-program-unit-for-language"), disc_m["units"])
    record("u9-mixed-repository-no-fallback", "valid", units=disc_m["units"], membership=M.assign_membership(inv_m, disc_m))
    try:
        M.discover_units(inv_s, None, [""])
        explicit = None
    except K.AdmissionError as exc:
        explicit = exc.boundary
    must("u9-explicit-root-without-marker", explicit == "native.explicit-root-without-marker", explicit)
    record("u9-explicit-dot-root-without-marker", "invalid", firstRefusal=explicit, note="explicit roots are unchanged: no fallback is added")
    empty_disc = {"units": []}
    zero, zero_fault = default_selection(empty_disc)
    must("u9-default-selection-over-zero-units", zero is None and zero_fault == "NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT", zero_fault)
    record("u9-default-selection-over-zero-units", "invalid", firstRefusal=zero_fault,
           note="reachable only when the fallback cannot be minted (explicit roots or a boundary root); never an empty successful request")

    # ---- E. U-4b.2/U-4b.5 tsjs unitKind (source41 lines 755-760, 797-799). source39 measured the absence of this law (s39-M1,
    # preserved/source39-v3/vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned); the same two spellings are re-measured.
    inv_k = files("tsconfig.json", "src/a.ts", "src/b.js")
    inv_k["tsconfig.json"] = b"{\"compilerOptions\":{\"allowJs\":true}}\n"
    disc_k = M.discover_units(inv_k)
    mem_k = M.assign_membership(inv_k, disc_k)
    alt = copy.deepcopy(mem_k)
    alt["units"][0]["unitKind"] = "ts-program"
    spellings = []
    for label, rec in (("mode-projection", mem_k), ("alternative-spelling", alt)):
        spellings.append({"spelling": label, "unitKind": rec["units"][0]["unitKind"], "languageMode": rec["units"][0]["languageMode"],
                          "recognizerId": rec["units"][0]["recognizerId"], "schemaAdmitted": KIT.admit(rec, NE, "#/$defs/UnitMembershipV1")["ok"],
                          "enforcementFaults": M.membership_order_faults(rec, list(inv_k)) + M.membership_row_faults(rec),
                          "originalHelperEnforcementFaults": ORIG.membership_order_faults(rec, list(inv_k)) + ORIG.membership_row_faults(rec),
                          "membershipDigest": K.raw_digest(rec)})
    must("u4b-tsjs-unit-kind-projection-positive", spellings[0]["languageMode"] == "js-allowjs" and spellings[0]["unitKind"] == "js-program"
         and spellings[0]["schemaAdmitted"] and not spellings[0]["enforcementFaults"], spellings)
    must("u4b-tsjs-unit-kind-alternative-refuses", spellings[1]["enforcementFaults"][:1] == ["ENUMERATION_MEMBERSHIP_ORDER:unitKind:0"], spellings)
    record("u4b-tsjs-unit-kind-projection", "invalid", firstRefusal=(spellings[1]["enforcementFaults"] or [None])[0],
           masksLater=spellings[1]["enforcementFaults"][1:], spellings=spellings,
           identityDetermined=bool(spellings[1]["enforcementFaults"]) and not spellings[0]["enforcementFaults"],
           originalHelperAdmittedAlternative=not spellings[1]["originalHelperEnforcementFaults"],
           selectors=["native-evidence.md lines 755-760 (U-4b.2: ts-program exactly when the mode is ts-tsconfig; js-program for js-allowjs and js-synthesized)",
                      "native-evidence.md lines 797-799 (U-4b.5: a tsjs unitKind not the projection of its mode refuses ENUMERATION_MEMBERSHIP_ORDER)",
                      "native-evidence.md lines 733-735 (UnitMembershipV1 enters PlanId through membershipDigest)"],
           note="the source39 s39-M1 alternative spelling is still schema-valid and now refuses at retained enforcement; the unchanged ported helper admitted it (HC-39)")

    # ---- F. U-0 internal root representation (source41 lines 626-651; #/$defs/InternalUnitRootV1, #/$defs/CanonicalRelativeDirV1)
    root_cases = [("external-sentinel-root", 1, "rootPath", "."), ("trailing-slash-root", 2, "rootPath", "packages/js/"),
                  ("leading-slash-root", 2, "rootPath", "/packages/js"), ("empty-segment-root", 2, "rootPath", "packages//js"),
                  ("dotdot-segment-root", 2, "rootPath", "packages/../js"), ("backslash-root", 2, "rootPath", "packages\\js"),
                  ("empty-member-root", 0, "memberPackageRoots", ["", "crates/b"]), ("dot-segment-member-root", 0, "memberPackageRoots", ["crates/./a", "crates/b"])]
    for label, ordinal, field, value in root_cases:
        bad = copy.deepcopy(mem)
        bad["units"][ordinal][field] = value
        enum_faults = M.unit_root_faults(bad["units"], "ENUMERATION_MEMBERSHIP_UNIT_ROOT")
        try:
            M.assign_membership(inv, dict(disc, units=bad["units"]))
            host = None
        except K.AdmissionError as exc:
            host = f"{exc.boundary}:{getattr(exc, 'detail', '')}"
        schema_ok = KIT.admit(bad, NE, "#/$defs/UnitMembershipV1")["ok"]
        must(f"u0:{label}", enum_faults[:1] == [f"ENUMERATION_MEMBERSHIP_UNIT_ROOT:{ordinal}:{field}"]
             and host == f"NATIVE_UNIT_ROOT_REPRESENTATION:{ordinal}:{field}" and not schema_ok, (enum_faults, host, schema_ok))
        record(f"u0-{label}", "invalid", firstRefusal=enum_faults[0] if enum_faults else None, masksLater=enum_faults[1:], hostDecision=host,
               schemaValid=schema_ok, originalHelperEnforcementFaults=ORIG.membership_order_faults(bad, list(inv)) + ORIG.membership_row_faults(bad))
    must("u0-positive", not M.unit_root_faults(mem["units"], "ENUMERATION_MEMBERSHIP_UNIT_ROOT"))
    grammar = []
    for s in ["", ".", "..", "a", "a/b", "a/", "/a", "a//b", "a/./b", "a/../b", "a\\b", "a\x00b", "a\n", "a\n/../b", "a/.\n", ".a", "..a", "a.", "#x/y"]:
        one = {"schemaVersion": 1, "units": [dict(mem["units"][2], unitOrdinal=0, rootPath=s)], "rows": [], "unsupportedFiles": [],
               "outsideBoundaryFiles": [], "erasedFiles": []}
        adm = KIT.admit(one, NE, "#/$defs/UnitMembershipV1")
        grammar.append({"value": s, "helperInternalRoot": not M.unit_root_faults(one["units"], "U0"), "schemaInternalRoot": adm["ok"],
                        "schemaDetail": (adm.get("stock") or [])[:1] + (adm.get("order") or [])[:1]})
    disagree = [g for g in grammar if g["helperInternalRoot"] != g["schemaInternalRoot"]]
    must("u0-helper-grammar-equals-published-pattern", not disagree, disagree)
    record("u0-root-grammar-agreement", "explanatory", rows=grammar, disagreements=disagree,
           note="the helper's split-on-slash predicate against the published InternalUnitRootV1 pattern, judged by schema admission of a one-unit record")

    # ---- G. U-4b.2 nested Cargo workspaces decided shallowest first (source41 lines 747-754; source39 advisory A-n5)
    inv_n = files("Cargo.toml", "crates/inner/Cargo.toml", "crates/inner/sub/Cargo.toml", "crates/inner/sub/src/lib.rs", "crates/inner/src/lib.rs",
                  "crates/other/Cargo.toml", "crates/other/src/lib.rs")
    inv_n["Cargo.toml"] = b"[workspace]\nmembers = [\"crates/*\"]\n"
    inv_n["crates/inner/Cargo.toml"] = b"[workspace]\nmembers = [\"sub\"]\n"
    disc_n = M.discover_units(inv_n)
    mem_n = M.assign_membership(inv_n, disc_n)
    units_n = [(u["unitOrdinal"], u["rootPath"], u["unitKind"], u["memberPackageRoots"]) for u in disc_n["units"]]
    rows_n = rows_by_path(mem_n)
    must("u4b-nested-cargo-workspace", units_n == [(0, "", "cargo-workspace", ["crates/inner", "crates/inner/sub", "crates/other"])] and
         all(rows_n[p] == ("rust", 0, "program-member", "deepest-unit-in-language") for p in ("crates/inner/sub/src/lib.rs", "crates/inner/src/lib.rs", "crates/other/src/lib.rs"))
         and KIT.admit(mem_n, NE, "#/$defs/UnitMembershipV1")["ok"] and not M.membership_order_faults(mem_n, list(inv_n)) and not M.membership_row_faults(mem_n),
         (units_n, mem_n["rows"]))
    record("u4b-nested-cargo-workspace", "valid", inventory=sorted(inv_n), units=disc_n["units"], membership=mem_n,
           originalHelperUnits=ORIG.discover_units(inv_n)["units"],
           note="a nested workspace manifest below a cargo-workspace unit is a member, receives no members, and every Cargo.toml below it folds into the enclosing unit")

    # ---- H. U-1 / s1.2: the effective allowJs selects the mode for both configuration markers (source41 lines 516-531, 654-659)
    t, f = b"{\"compilerOptions\":{\"allowJs\":true}}\n", b"{\"compilerOptions\":{\"allowJs\":false}}\n"
    mode_cases = [
        ("tsconfig-no-js-options", {"tsconfig.json": b"{}\n"}, "ts-tsconfig"),
        ("tsconfig-checkjs-true", {"tsconfig.json": b"{\"compilerOptions\":{\"checkJs\":true}}\n"}, "js-allowjs"),
        ("tsconfig-allowjs-false-checkjs-true", {"tsconfig.json": b"{\"compilerOptions\":{\"allowJs\":false,\"checkJs\":true}}\n"}, "ts-tsconfig"),
        ("jsconfig-no-options", {"jsconfig.json": b"{}\n"}, "js-allowjs"),
        ("jsconfig-writes-allowjs-false", {"jsconfig.json": f}, "ts-tsconfig"),
        ("jsconfig-extends-base-allowjs-false", {"jsconfig.json": b"{\"extends\":\"./base.json\"}\n", "base.json": f}, "js-allowjs"),
        ("tsconfig-extends-base-named-jsconfig", {"tsconfig.json": b"{\"extends\":\"./cfg/jsconfig.json\"}\n", "cfg/jsconfig.json": b"{}\n"}, "js-allowjs"),
        ("later-extends-wins-false", {"tsconfig.json": b"{\"extends\":[\"./a.json\",\"./b.json\"]}\n", "a.json": t, "b.json": f}, "ts-tsconfig"),
        ("later-extends-wins-true", {"tsconfig.json": b"{\"extends\":[\"./b.json\",\"./a.json\"]}\n", "a.json": t, "b.json": f}, "js-allowjs"),
        ("own-option-beats-base", {"tsconfig.json": b"{\"extends\":\"./a.json\",\"compilerOptions\":{\"allowJs\":false}}\n", "a.json": t}, "ts-tsconfig"),
    ]
    mode_rows = []
    for label, cfg_files, want in mode_cases:
        inv_c = dict(cfg_files, **{"src/a.js": b"x\n"})
        disc_c = M.discover_units(inv_c)
        cur = next(u for u in disc_c["units"] if u["rootPath"] == "")
        orig = next(u for u in ORIG.discover_units(inv_c)["units"] if u["rootPath"] == "")
        mem_c = M.assign_membership(inv_c, disc_c)
        must(f"s12-mode:{label}", cur["languageMode"] == want and cur["unitKind"] == M.TSJS_UNIT_KIND[want] and cur["recognizerId"] == "typescript-config"
             and not M.membership_order_faults(mem_c, list(inv_c)) and not M.membership_row_faults(mem_c), cur)
        mode_rows.append({"case": label, "files": {p: b.decode() for p, b in sorted(cfg_files.items())}, "expectedMode": want, "mode": cur["languageMode"],
                          "unitKind": cur["unitKind"], "markerPath": cur["markerPath"], "originalHelperMode": orig["languageMode"], "originalHelperUnitKind": orig["unitKind"]})
    record("s12-effective-allowjs-mode-selection", "valid", rows=mode_rows,
           originalHelperDisagreements=[r["case"] for r in mode_rows if (r["originalHelperMode"], r["originalHelperUnitKind"]) != (r["mode"], r["unitKind"])],
           selectors=["native-evidence.md lines 516-531 (s1.2 effective allowJs over the retained configuration graph; jsconfig nodes supply true)",
                      "native-evidence.md lines 654-659 (U-1: both configuration markers use the effective allowJs)",
                      "native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law (jsconfig kind by exact basename)"],
           note="expected modes follow the cited sentences; no compiler is executed, and TS diagnostic 5052 is not a refusal (lines 550-556)")

    out = {"owners": ["native-evidence.md s1.4 U-1..U-4b, U-8, U-9", NE + "#/$defs/UnitMembershipV1", "foundation/enumeration-plan.schema.v1.json#/x-opensip-new-internal-faults"],
           "vectors": vectors, "assertionFailures": failures}
    with open(f"{OUT}/vectors/discovery-membership.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("vectors", len(vectors), "failures", len(failures))
    print(json.dumps(failures, default=str)[:6000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
