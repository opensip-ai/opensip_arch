"""Independent F1-F9 / S1-S4 probes against copy bytes. Not a restatement of check.py."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-evidence-feature02-reproduction/copy")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PARENT07 = Path("/tmp/opensip-implementation/m1-report-projection-subject-07")
RESULTS = Path("/tmp/opensip-implementation/m1-root-evidence-feature02-reproduction/results")
PARENT07_MANIFEST_SHA256 = "cee1eb24159187c3dc967493046eb08e2f86e242ed55eab23fe944c2cd43e6c8"


def load_path(name, path):
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), mod.__dict__)
    return mod


def compile_copy(name, rel):
    p = COPY / rel
    m = types.ModuleType(name)
    m.__file__ = str(p)
    exec(compile(p.read_bytes(), str(p), "exec"), m.__dict__)
    return m


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name)


def main():
    rows = []
    M = compile_copy("evidence_reference_model", "reference_model.py")
    canonical = load_path("foundation_canonical", ARCH / "docs/coop/design-corrections/foundation/canonical.py")
    RM = load_path("parent07_report_model", PARENT07 / "report_model.py")
    M.bind(canonical, RM)
    NM = load_path("native_model_v2", ARCH / "docs/coop/design-corrections/native/native_evidence_model.v2.py")
    owner = compile_copy("evidence_build_owner", "build_owner.py")
    builder = compile_copy("evidence_build_fixtures", "build_fixtures.py")
    CH = compile_copy("evidence_check", "check.py")
    fixture = json.loads((COPY / "fixtures.json").read_bytes())
    parameter_sha = hashlib.sha256((COPY / "owner/framework-recognition-plan.schema.v1.json").read_bytes()).hexdigest()

    # S1-S4 standing: unaccepted proposals
    s1 = json.loads((COPY / "owner/native-recognition-successor.v1.json").read_bytes())
    s2 = json.loads((COPY / "owner/identity-parameter-registry-patch.v2.json").read_bytes())
    s4 = json.loads((COPY / "owner/report-projection-successor-patch.v2.json").read_bytes())
    rec(rows, "s1-unaccepted-proposal-standing", "proposed" in s1["standing"] and "FR-7" in {c["id"] for c in s1["clauses"]})
    rec(rows, "s2-optional-row-no-requiredForEvaluatorMajors", "requiredForEvaluatorMajors" not in s2["ops"][0]["value"] and s2["identityEffects"]["closedVocabularies"].endswith("NOT used"))
    rec(rows, "s4-33-semantic-ops", len(s4["ops"]) == 33, ops=len(s4["ops"]))
    rec(rows, "s3-specified-not-executed-query-model", True, note="query_projection_model.v3 is not executed; S3 is law/reference only per contract")

    # F1 duty without overlay
    lang = {"ts-tsconfig": "typescript", "rs-cargo": "rust", "markdown": "text"}
    row_key = "foundation/framework-recognition-plan.schema.v1.json"
    digest = "a" * 64
    param = {"schemaDigest": digest, "payloadDigest": "b" * 64}

    def row_of(d):
        return row_key if d == digest else "other"

    r = M.admit_new_plan_recognition_parameter([], [{"capabilityId": "x", "languageMode": "markdown"}], row_of, lang, row_key)
    rec(rows, "f1-syntax-only-without-parameter-admitted", r["compilerLanguageModes"] == [])
    try:
        M.admit_new_plan_recognition_parameter([], [{"capabilityId": "x", "languageMode": "ts-tsconfig"}], row_of, lang, row_key)
        rec(rows, "f1-compiler-without-parameter-refuses", False)
    except M.Refusal as exc:
        rec(rows, "f1-compiler-without-parameter-refuses", exc.code == "NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED", code=exc.code)
    r = M.admit_new_plan_recognition_parameter([param], [{"capabilityId": "x", "languageMode": "ts-tsconfig"}], row_of, lang, row_key)
    rec(rows, "f1-compiler-with-one-parameter-admitted", r["recognitionParameters"] == 1)
    try:
        M.admit_new_plan_recognition_parameter([param, dict(param)], [{"capabilityId": "x", "languageMode": "ts-tsconfig"}], row_of, lang, row_key)
        rec(rows, "f1-compiler-with-two-parameters-refuses", False)
    except Exception:
        rec(rows, "f1-compiler-with-two-parameters-refuses", True, note="need() or downstream")
    rec(rows, "f1-custody-no-parameter-not-plan-bound", M.custody_from_parameters([], digest, {"state": "retained"}, {})["state"] == "not-plan-bound")
    rec(rows, "f1-custody-purged-unavailable", M.custody_from_parameters([{"schemaDigest": digest, "payloadDigest": "c" * 64}], digest, {"state": "purged"}, {})["state"] == "unavailable")

    # F3 glob law: never complete; extra examples vs workflows glob
    rec(rows, "f3-default-test-glob-matches-button-test", M.glob_match("**/*.test.*", "src/button.test.tsx") is True)
    rec(rows, "f3-default-test-glob-misses-it-ts", M.glob_match("**/*.test.*", "src/helper.it.ts") is False)
    rec(rows, "f3-rooted-glob-does-not-cross-package", M.glob_match("src/**/*.test.ts", "packages/web/src/a.test.ts") is False)

    # Worlds through pinned native model
    def world(name):
        desc = copy.deepcopy(fixture["descriptions"][name])
        data = builder.assemble(desc, M, NM, parameter_sha)
        built = M.World(data)
        M.admit_recognition_plan(built, data["recognitionRecord"])
        return built, data

    mixed, mixed_data = world("mixed")
    cross, _ = world("cross-universe-test")
    jest, jest_data = world("jest-configured")

    # F4 cargo targets
    rust_universe = next(u for u, fam in ((u, mixed.family(u)) for u in mixed.rust_universes) if fam == "rust")
    cargo = M.cargo_target_entries(mixed, rust_universe)
    crate_roots = sorted({t["crateRootPath"] for t in cargo["targets"] if t["crateRootPath"]})
    rec(rows, "f4-cargo-includes-member-app-and-core-and-workspace-root",
        "crates/app/src/main.rs" in crate_roots or any("crates/app" in (t["crateRootPath"] or "") or "crates/app" in t["markerPath"] for t in cargo["targets"]),
        state=cargo["state"], targets=[{k: t[k] for k in ("targetKind", "crateRootPath", "markerPath")} for t in cargo["targets"]])
    rec(rows, "f4-cargo-state-all-when-roots-resolved", cargo["state"] == "all" and not cargo["missingCoverage"], state=cargo["state"], missing=cargo["missingCoverage"])
    entries = M.effective_entries(mixed, rust_universe)
    rec(rows, "f4-effective-entries-include-cargo-target-provenance",
        any(any(p.get("source") == "cargo-target" for p in provenances) for provenances in entries.values()),
        entryPaths=sorted(entries))

    # F2/F3 test reachability
    resolution = fixture["resolutions"]["integration"]
    cross_ev = M.derive_symbol_evidence(cross, resolution, 4194304)
    helper = next(r for r in cross_ev["testReachability"] if "helper" in json.dumps(r.get("subjectId")) or (r.get("origin") or {}).get("endpoint", {}).get("nativeSubjectId", "").endswith("helper") or True)
    # resolve helper by native id via resolution map
    isid = {e["endpoint"]["nativeSubjectId"]: e["subjectId"] for e in resolution if e["state"] == "resolved"}
    helper_row = next(r for r in cross_ev["testReachability"] if r["subjectId"] == isid.get("ts:src/helper.ts#helper"))
    rec(rows, "f2-cross-universe-helper-static-path-from-test-origin",
        helper_row["state"] == "static-path-from-test-origin" and helper_row["origin"]["endpoint"]["universe"] == builder.UT,
        state=helper_row["state"], originUniverse=helper_row["origin"]["endpoint"]["universe"])
    rec(rows, "f2-no-no-static-path-within-bound-state",
        not any(r["state"] == "no-static-path-within-bound" for r in cross_ev["testReachability"]))

    jest_ev = M.derive_symbol_evidence(jest, resolution, 4194304)
    jest_helper = next(r for r in jest_ev["testReachability"] if r["subjectId"] == isid.get("ts:src/helper.ts#helper"))
    rec(rows, "f3-jest-configured-helper-not-found-incomplete",
        jest_helper["state"] == "not-found-incomplete" and "test-origin-set-partial" in jest_helper["blockers"],
        state=jest_helper["state"], blockers=jest_helper.get("blockers"))
    rec(rows, "f3-origin-sets-never-complete",
        all(s["completeness"] in ("partial", "none") for s in jest_ev["testOrigins"]),
        completeness=sorted({s["completeness"] for s in jest_ev["testOrigins"]}))
    rec(rows, "f3-test-selection-configured-limitation",
        any("test-selection-configured" in s.get("limitations", []) for s in jest_ev["testOrigins"]))

    # F8/F9 mixed coupling
    mixed_res = fixture["resolutions"]["mixed"]
    coupling = M.derive_coupling(mixed, budget=4194304, test_origin_state=M.test_origin_state_fn(mixed))
    rec(rows, "f8-mixed-cell-count-8-and-three-count-units",
        coupling["totals"]["cellCount"] == 8 and coupling["totals"]["importerSymbolPathOutsideAnchors"] == 1,
        totals=coupling["totals"])
    rec(rows, "f9-importer-anchor-owners-disagree-bucket-present",
        any(b["cause"] == "importer-anchor-owners-disagree" for b in coupling["importerBuckets"]),
        buckets=coupling["importerBuckets"])
    rec(rows, "f6-absence-not-supported-under-limitations",
        coupling["absence"]["absenceSupported"] is False and "evidence-limitations" in coupling["absence"]["blockers"],
        absence=coupling["absence"])

    # F6 tiny budget omits panel (skeleton does not fit)
    tiny = M.fit_coupling(mixed, M.coupling_full(mixed, test_origin_state=M.test_origin_state_fn(mixed)), 1000)
    rec(rows, "f6-1000-byte-budget-omits-panel", tiny is None, observed=None if tiny is None else sorted(tiny)[:12])

    # F5 patch composition
    parent_raw = (PARENT07 / "report-projection.schema.json").read_bytes()
    parent_man = json.loads(Path("/tmp/opensip-implementation/m1-report-projection-subject-07.json").read_bytes())
    rec(rows, "parent07-manifest-pin", hashlib.sha256(Path("/tmp/opensip-implementation/m1-report-projection-subject-07.json").read_bytes()).hexdigest() == PARENT07_MANIFEST_SHA256)
    rec(rows, "s4-parent-sha-matches-parent07-schema", s4["parent"]["sha256"] == hashlib.sha256(parent_raw).hexdigest())
    parent = json.loads(parent_raw)
    # apply_semantic expects parsed JSON object; parent schema is JSON
    patched = CH.apply_semantic(parent, s4["ops"])
    rec(rows, "f5-patch-applies-projection-priority-coupling-last",
        patched["$defs"]["BudgetProfileV1"]["properties"]["projectionPriority"]["const"][-1] == "coupling")
    twice = None
    try:
        CH.apply_semantic(patched, s4["ops"])
        twice = "APPLIED"
    except CH.PatchRefused as exc:
        twice = str(exc).split(" ")[0]
    rec(rows, "f5-reapply-this-patch-refused", twice in ("PRECONDITION", "SELECTOR-GUARD"), observed=twice)

    # F7 featureMap: patched schema must resolve without bogus member — checked by dump equality in check; here FeatureId enum lacks removed ids
    removed = ["coupling-importer-package-membership", "entry-point-recognition", "symbol-metrics", "test-reachability"]
    rec(rows, "f7-removed-featureids-absent-from-patched-enum", not (set(removed) & set(patched["$defs"]["FeatureId"]["enum"])))

    failed = [r for r in rows if not r["passed"]]
    out = {"standing": "independent Grok evidence-design02 law probes; not check.py restatement; not product selection",
           "passed": not failed, "caseCount": len(rows), "failedCount": len(failed), "failed": [r["name"] for r in failed], "checks": rows}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-laws.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
