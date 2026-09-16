#!/usr/bin/env python3
"""Mutation controls for check.py (candidate 02). Each control copies the subject input files into its own
tmp/selftest/<control>/ directory, seeds one defect, runs check.py there as a subprocess with that copy's own TMPDIR and
bytecode prefix, and requires that at least one of the control's EXPECTED checks fails (not merely any failure).
Includes the 14 reviewer-01 mutants adapted to candidate 02 structures. Proves the reference check can fail; not
approval.

Run: OPENSIP_ARCH=... TMPDIR=<subject>/tmp PYTHONDONTWRITEBYTECODE=1 \
       /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B selftest.py
"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
INPUT_FILES = json.loads((HERE / "subject-files.json").read_text())["inputs"]


def J(path):
    return json.loads(path.read_text())


def W(path, obj):
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def mem(d, rec, name):
    return next(m for m in d["records"][rec]["members"] if m["name"] == name)


def rule(d, rid):
    return next(r for r in d["admission"] if r["id"] == rid)


def on_wire(fn):
    def apply(root):
        d = J(root / "wire-carriers.v1.json")
        fn(d)
        W(root / "wire-carriers.v1.json", d)
    return apply


def on_file(name, fn):
    def apply(root):
        d = J(root / name)
        fn(d)
        W(root / name, d)
    return apply


def on_text(name, old, new):
    def apply(root):
        s = (root / name).read_text()
        if old not in s:
            raise RuntimeError("control anchor missing: " + old[:60])
        (root / name).write_text(s.replace(old, new, 1))
    return apply


CONTROLS = {
    # ---- reviewer-01 mutants, adapted
    "r_prepared_total_widened": (on_wire(lambda d: (mem(d, "Rust3PreparedOutputManifestV3", "entries")["type"].update(maxItems="2000256"),
                                                    mem(d, "Rust3PreparedOutputEntryV3", "outputOrdinal")["type"].update(max="2000255"))), ["limit-literals"]),
    "r_canonical_path_native_pattern": (on_wire(lambda d: d["scalars"]["Rust3CanonicalPath"]["type"].update(
        pattern="^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])", lexical=None) or d["scalars"]["Rust3CanonicalPath"]["type"].pop("lexical")),
        ["path-scalars-lexical-no-pattern", "wire-rust3-path-newline-dotdot"]),
    "r_exec_minlength1": (on_wire(lambda d: d["scalars"].__setitem__("Ts2ExecutionIdText", dict(d["scalars"]["Ts2ExecutionIdText"], type={"t": "text", "nfc": True, "minScalars": "1"}))), ["wire-ts2-execution-id-grammar"]),
    "r_anchor_4096": (on_wire(lambda d: (mem(d, "Rust3FactCandidateV1", "anchors")["type"].update(maxItems="4096"), rule(d, "ANCHOR-WIRE-SPAN")["params"].update(maxCount="4096"))), ["limit-literals"]),
    "r_ts_path_bytes": (on_wire(lambda d: (d["scalars"]["Ts2ProjectPath"]["type"].pop("maxScalars"), d["scalars"]["Ts2ProjectPath"]["type"].update(maxUtf8Bytes="4096"))), ["scalar-shapes-match-externs", "ts2-path-bound-matches-owner"]),
    "r_fault_phase_host_receipt": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"].update(phaseSemantics="host-receipt")), ["vectors:RUST3-PROVIDER-FAULT", "provider-fault-semantics-declared"]),
    "r_cancel_in_start_allowed": (on_wire(lambda d: d["protocols"]["rust-semantic"]["transitions"]["cancel"].update(hostMaySendInStart=True)), ["cancel-in-start-consistent-with-p3", "vectors:P3-OVERLAY"]),
    "r_depsrc_order_path_first": (on_wire(lambda d: rule(d, "DEPSRC-CUSTODY")["params"].update(entryOrder=["path", "name", "version", "sourceId"])), ["vectors:DEPSRC-CUSTODY", "depsrc-order-derived-from-owner"]),
    "r_scope2_drop_closure": (on_wire(lambda d: rule(d, "PER-KEY-SCOPE2")["params"]["descriptorMembers"].remove("enumeratorClosure")), ["vectors:PER-KEY-SCOPE2", "scope2-descriptor-members-match-owner"]),
    "r_identitytext_no_bytes": (on_wire(lambda d: d["scalars"]["Rust3IdentityText"]["type"].pop("maxUtf8Bytes")), ["json-schema-maxlength-not-byte-bound"]),
    "r_package_key_min5": (on_wire(lambda d: d["scalars"]["Rust3PackageKey"]["type"].update(minScalars="5")), ["package-key-bounds-derived-from-owner", "wire-depsrc-chunk-empty-sourceid-key"]),
    "r_outputseen_not_reset": (on_wire(lambda d: d["protocols"]["rust-semantic"]["transitions"].update(stateUpdateAdditions=[{"onFrames": ["FactBatch", "CoverageV3"], "sets": {"outputSeen": True}}])), ["p3-overlay-updates-match-rust2"]),
    "r_prepared_count_directives_only": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"].update(countScope="build-script-directives-only")), ["vectors:PREPARED-V3-WIRE-LIMIT", "prepared-refusal-row-family"]),
    "r_commit_unavailable_stagecoverage": (on_wire(lambda d: next(r for r in d["commitmentMap"]["rows"] if r["field"] == "Startup1UnavailableV3.coverageCommitment").update(domain="opensip.rust-provider.stage-coverage.v2", valueClass="stage-entries")),
                                           ["commit-map-value-classes-match-owner", "vectors:COMMIT-MAP"]),
    # ---- candidate-02 required findings
    "rf3_prepared_host_invariant_fate": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["refusal"].update({"class": "operational-failed", "code": "SYSTEM.OUTCOME.ILLEGAL_STATE"})), ["prepared-refusal-row-family"]),
    "rf3_prepared_frame_check_removed": (on_wire(lambda d: rule(d, "PREPARED-V3-WIRE-LIMIT")["params"].update(maxManifestBytes="999999999")), ["limit-literals", "vectors:PREPARED-V3-WIRE-LIMIT"]),
    "rf4_fault_nulls_independent": (on_wire(lambda d: rule(d, "RUST3-PROVIDER-FAULT")["params"].update(jointConsistency=False)), ["vectors:RUST3-PROVIDER-FAULT", "provider-fault-semantics-declared"]),
    "rf5_dependency_path_native_only": (on_wire(lambda d: rule(d, "CANONICAL-PATH-ADMISSION")["params"].update(lexical="logical-path-segments")), ["vectors:CANONICAL-PATH-ADMISSION"]),
    "rf5_lookaround_lowering_undeclared": (on_wire(lambda d: d["privateRepresentation"]["patternDialect"].update(lowering="patterns are used as-is")), ["pattern-lowering-required-declared"]),
    "rf6_key_space_allowed_in_name": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(forbidInNameVersionAtOrBelow="31")), ["vectors:DEPSRC-SET-KEY-CONSTRAINTS", "package-key-bounds-derived-from-owner"]),
    "rf6_key_bound_4610": (on_wire(lambda d: rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"].update(maxKeyScalars="4610")), ["vectors:DEPSRC-SET-KEY-CONSTRAINTS", "package-key-bounds-derived-from-owner"]),
    "adv6_linktarget_bound_restored": (on_wire(lambda d: d["records"]["Ts2SnapshotEntryV1"]["variants"]["symlink"]["linkTarget"].update(maxScalars="4096")), ["path-members-bound-to-lexical-rules", "ts2-manifest-digest-raw"]),
    "adv7_anchor_order_swapped": (on_wire(lambda d: rule(d, "ANCHOR-WIRE-SPAN")["params"].update(order={"typescript-semantic": "cve1-bytes-strict", "rust-semantic": "cbor-bytes-strict"})), ["anchor-order-tokens-follow-language-owner", "vectors:ANCHOR-WIRE-SPAN"]),
    "adv3_gap_detached": (on_file("field-coverage.json", lambda c: c["recordLevelGaps"].pop("R3-G19")), ["field-coverage-gaps-resolved"]),
    "adv2_vector_removed": (on_file("admission-vectors.json", lambda v: v["vectors"].pop("PACKAGE-KEY-JOIN")), ["vectors-cover-every-rule"]),
    # ---- RF-1 / RF-2 closure controls (tools and inputs)
    "rf2_architecture_pin_dropped": (on_text("tools/common.py", '    "capabilityMatrix": ("docs/coop/design-corrections/native/native-capability-matrix.v2.json", "4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14", 36595),\n', ""),
                                     ["closure-architecture-reads-pinned"]),
    "rf2_architecture_pin_tampered": (on_text("tools/common.py", "7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be", "0" * 64), ["architecture-pins-verified-before-import"]),
    "rf1_frozen_input_changed": (on_file("inputs/rust3-fields.json", lambda r: r["gaps"].pop("R3-G19")), ["subject-inputs-pinned:rustFields"]),
    "rf2_reference_env_version": (on_file("reference-environment.json", lambda e: e["packages"].update(jsonschema="0.0.0")), ["reference-environment-matches"]),
    # ---- carried over from candidate 01
    "c_member_rename": (on_wire(lambda d: mem(d, "Rust3PreparedOutputEntryV3", "planRow").update(name="setRow")), ["carrier-member-lists"]),
    "c_bare_name": (on_wire(lambda d: d["records"].__setitem__("CoverageKeyV2", d["records"].pop("Rust3CoverageKeyV2"))), ["namespaced-type-names"]),
    "c_frame_terminal": (on_wire(lambda d: next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Cancel").update(workerTerminal=True)), ["rust3-frame-directions-terminals"]),
    "c_bytes_as_text": (on_wire(lambda d: mem(d, "Rust3SnapshotFileChunkV2", "bytes").update(type={"t": "text", "nfc": True})), ["wire-bytes-as-json-array", "wire-bytes-empty"]),
    "c_fact_ref_dropped": (on_wire(lambda d: d["records"]["Ts2AnchorRefV1"]["variants"].pop("fact-ref")), ["input-grammar"]),
    "c_selector": (on_wire(lambda d: next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Unavailable")["payload"].update(alternatives={
        "READY_ANALYZE": {"t": "extern", "schemaRef": "opensip.product.provider-startup.1#/$defs/UnavailableV3", "generatedType": "Startup1UnavailableV3"},
        "WAIT_NATIVE_CONTEXT_VERIFIED": {"t": "extern", "schemaRef": "opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1", "generatedType": "Startup1PreAnalyzeUnavailableV1"}})),
        ["unavailable-selector-phases"]),
    "c_nullable_to_optional": (on_wire(lambda d: mem(d, "Ts2CancelV1", "executionId").update(presence="optional")), ["wire-ts2-cancel-null-omitted-refused"]),
    "c_successor_check": (on_file("successor.json", lambda s: s["rows"][0]["referenceChecks"].append("nonexistent-check")), ["successor-check-exists:nonexistent-check"]),
}


def run_control(name):
    apply, expected = CONTROLS[name]
    root = HERE / "tmp" / "selftest" / name
    shutil.rmtree(root, ignore_errors=True)
    for f in INPUT_FILES:
        dst = root / f["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / f["path"], dst)
    try:
        apply(root)
    except Exception as exc:  # noqa: BLE001
        return {"control": name, "caught": False, "error": "apply failed: " + repr(exc)}
    (root / "tmp").mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(root / "tmp"), PYTHONDONTWRITEBYTECODE="1", PYTHONPYCACHEPREFIX=str(root / "tmp" / "pycache"))
    proc = subprocess.run([PY, "-I", "-B", "check.py", "--out", str(root / "tmp" / "result.json")], cwd=root, env=env,
                          capture_output=True, text=True, timeout=1500)
    try:
        failed = [f["id"] for f in J(root / "tmp" / "result.json")["failures"]]
    except Exception:  # noqa: BLE001
        failed = ["no-result:" + proc.stdout[-300:]]
    hit = [e for e in expected if e in failed]
    return {"control": name, "expected": expected, "caught": bool(hit), "expectedFailed": hit, "failedChecks": failed[:12]}


def main():
    workers = int(os.environ.get("SELFTEST_WORKERS", "4"))
    with ThreadPoolExecutor(workers) as ex:
        controls = list(ex.map(run_control, sorted(CONTROLS)))
    baseline = run_control_baseline()
    out = {"standing": "AUTHOR candidate 02 mutation controls; not approval", "baselineFailures": baseline,
           "controls": controls, "caught": sum(c["caught"] for c in controls), "total": len(controls),
           "reviewerMutantsAdapted": sum(1 for c in controls if c["control"].startswith("r_")),
           "allCaught": all(c["caught"] for c in controls) and not baseline}
    W(HERE / "selftest-result.json", out)
    print(json.dumps({k: out[k] for k in ("baselineFailures", "caught", "total", "reviewerMutantsAdapted", "allCaught")} |
                     {"missed": [c["control"] for c in controls if not c["caught"]]}, indent=1))
    return 0 if out["allCaught"] else 1


def run_control_baseline():
    CONTROLS["baseline"] = (lambda root: None, [])
    res = run_control("baseline")
    del CONTROLS["baseline"]
    shutil.rmtree(HERE / "tmp" / "selftest", ignore_errors=True)
    return res["failedChecks"]


if __name__ == "__main__":
    sys.exit(main())
