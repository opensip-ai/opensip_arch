"""Assemble independently chosen complete Run graphs."""
from __future__ import annotations

from typing import Any

from helpers import cap_admit, kit_const as KC
from helpers.body_id import suffix_variant
from helpers.canonical import C, sha256_hex
from helpers.evaluator import compose_proof, replay_rule
from helpers.graph import (
    PROJECT,
    Builder,
    TRIPLE,
    TS_COMPILER_VERSION,
    RUSTC_VERSION,
    RUST_COMMIT,
    _cap,
    blob_row,
    make_import,
    sort_paths,
)
from helpers.kit_const import BODY_LANGUAGE_BY_VARIANT
from helpers.store import Store


LEVEL_SPEC = b"opensip.level-spec.v1\nL0:verbatim\nL1:ws-insensitive\n"


def _manifest_for(language: str, extra_relations: dict | None = None) -> dict:
    rels = {"file": "enumerated", "clones": "normalized-body-hash", "package": "manifest-declared"}
    if extra_relations:
        rels.update(extra_relations)
    m = {
        "schemaVersion": 1,
        "profile": "core",
        "providers": [
            {
                "providerId": f"{language}-provider",
                "language": language if language != "syntax" else "*",
                "providerVersionSource": "release",
                "toolchainIdentitySource": "release",
                "relations": rels,
                "platformIds": ["all-supported", "linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"],
            }
        ],
        "coverageForAbsent": [],
    }
    return cap_admit.canonicalise_for_release(m)


def _admit_cap(m: dict) -> dict:
    r = cap_admit.admit(m)
    if not r["ok"]:
        raise RuntimeError(r)
    return r


def _nm_layout(b: Builder) -> str:
    entries = []
    for path, data in b.files.items():
        if path.startswith("node_modules/"):
            # package name from first two segments
            parts = path.split("/")
            pkg = parts[1]
            entries.append(
                {
                    "packageName": pkg,
                    "packageVersion": "1.0.0",
                    "installPath": "/".join(parts[:2]),
                    "realPath": path if path.endswith("index.js") or path.endswith("package.json") else "/".join(parts[:2]),
                    "contentSha256": sha256_hex(data),
                }
            )
    # unique by installPath - keep package.json and index as separate? schema uniqueItems on entries
    # Use one entry per package
    by = {}
    for e in entries:
        by[e["installPath"]] = e
    layout = {"schemaVersion": 1, "entries": sorted(by.values(), key=lambda x: x["installPath"].encode())}
    return b.s.put_canonical(layout)


def _config_graph(b: Builder, path: str) -> tuple[dict, str]:
    data = b.files[path]
    kind = "tsconfig" if path.endswith("tsconfig.json") else ("jsconfig" if path.endswith("jsconfig.json") else "other")
    g = {
        "schemaVersion": 1,
        "entryConfigPath": path,
        "nodes": [
            {
                "path": path,
                "contentSha256": sha256_hex(data),
                "kind": kind,
                "extendsResolved": [],
            }
        ],
    }
    return g, b.s.put_canonical(g)


def _plan(b: Builder, snap: str, cap_id: str, cap_bytes_d: str, closures: list[str], spec_d: str, cfg_d: str, nctx: list[str], imports: list[str], pol_d: str, wai_d: str, scope_d: str, grant_d: str) -> str:
    desc = {
        "schemaVersion": 2,
        "snapshotId": snap,
        "capabilityManifestId": cap_id,
        "semanticClosures": sorted(closures),
        "analysisSpecDigest": spec_d,
        "resolvedConfigDigest": cfg_d,
        "nativeContextDigests": sorted(set(nctx)),
        "importIds": sorted(imports),
        "policyDigest": pol_d,
        "waiverDigest": wai_d,
        "scopeDigest": scope_d,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_d,
        "capabilityManifestBytesDigest": cap_bytes_d,
    }
    return b.s.put_h("plan", desc)


def _blv_ts(ctx: dict, path: str) -> dict:
    var = suffix_variant(path)
    lang = BODY_LANGUAGE_BY_VARIANT[var]
    return {
        "schemaVersion": 1,
        "languageId": lang,
        "compilerName": ctx["toolchain"]["compilerName"],
        "compilerVersion": ctx["toolchain"]["compilerVersion"],
        "compilerBuild": ctx["toolchain"]["compilerPackageDigest"],
        "dialect": {"sourceVariant": var},
    }


def _blv_rust(ctx: dict, edition: int) -> dict:
    return {
        "schemaVersion": 1,
        "languageId": "rust",
        "compilerName": "rustc",
        "compilerVersion": ctx["toolchain"]["rustcVersion"],
        "compilerBuild": ctx["toolchain"]["rustCommitHash"],
        "dialect": {"edition": edition},
    }


def _finish(
    b: Builder,
    *,
    plan_id: str,
    snap: str,
    view_id: str,
    provider: str,
    evaluator: str,
    detector: str,
    policy: dict,
    program: dict,
    pol_d: str,
    prog_d: str,
    cap_id: str,
    facts: list[dict],
    coverages: list[dict],
    scopes: list[dict],
    inventories: list[dict],
    import_ids: list[str],
    universe_hex: str,
    file_rows: list[dict],
) -> dict[str, Any]:
    spec_d = b.stage_spec(plan_id, provider)
    exec_id = b.execution_plan(plan_id, spec_d)
    # execution inputs
    view_hex = view_id.split(":")[-1]
    host = {
        "custody": "host-tcb-evidence-store",
        "observation": "stage-return",
        "stageReceipts": [
            {
                "ordinal": 0,
                "stageSpecDigest": spec_d,
                "producerClosure": provider,
                "outputDomains": ["view"],
                "outputRefs": [{"domain": "view", "digest": view_hex}],
                "state": "complete",
                "unavailableReason": None,
            }
        ],
        "hostDerivedRefs": [
            {"domain": "subject-inventory", "digest": inv["digest"]} for inv in inventories
        ],
    }
    selected = (
        [{"domain": "view", "digest": view_hex}]
        + [{"domain": "coverage", "digest": c["id"].split(":")[-1]} for c in coverages]
        + [{"domain": "subject-inventory", "digest": inv["digest"]} for inv in inventories]
        + [{"domain": "import", "digest": i.split(":")[-1]} for i in import_ids]
    )
    selected = sorted({(r["domain"], r["digest"]): r for r in selected}.values(), key=lambda r: C(r))
    # cell outcomes — one per inventory binding
    outcomes = []
    for i, inv in enumerate(inventories):
        rec = inv["record"]
        outcomes.append(
            {
                "ordinal": i,
                "cellOrdinal": rec["cellOrdinal"],
                "programOrdinal": rec["programOrdinal"],
                "capabilityId": inv.get("capabilityId", "inventory"),
                "languageMode": inv.get("languageMode", "ts-tsconfig"),
                "workspaceRoot": ".",
                "required": True,
                "kinds": [rec["kind"]],
                "universe": universe_hex,
                "enumeratorStatus": "selected",
                "enumeratorClosure": provider,
                "state": rec["state"],
                "deficiency": rec["deficiency"],
                "nativeCause": rec["nativeCause"],
                "stageOrdinal": 0,
                "stageOrdinalNullReason": None,
                "inventoryDigests": [inv["digest"]],
                "viewDigests": [view_hex],
                "candidateResultDigest": None,
            }
        )
    accounts = [
        {
            "cellOrdinal": 0,
            "programOrdinal": 0,
            "relation": "file",
            "resolution": "enumerated",
            "sourceUniverse": universe_hex,
            "targetUniverse": universe_hex,
            "applicability": "supported-available",
            "coverageIds": sorted(c["id"].split(":")[-1] for c in coverages if c["descriptor"]["scopeId"].startswith("scope2:")),
        }
    ]
    # coverageIds should be hex of coverage2
    accounts[0]["coverageIds"] = sorted(c["id"].split(":")[-1] for c in coverages)
    ei = {
        "schemaVersion": 1,
        "planId": plan_id,
        "executionPlanId": exec_id,
        "evaluatorClosure": evaluator,
        "enumerationPlanDigest": inventories[0]["record"]["parameterDigest"] if inventories else sha256_hex(b""),
        "analysisSpecDigest": b.s.objects[plan_id]["descriptor"]["analysisSpecDigest"],
        "hostCapture": host,
        "selectedRefs": selected,
        "cellOutcomes": outcomes,
        "nativeCoverageAccounts": accounts,
        "candidateResultRefs": [],
    }
    ei_d = b.s.put_canonical(ei)
    # attach universe onto file rows
    rows = []
    for r in file_rows:
        rr = dict(r)
        rr["universe"] = universe_hex
        rows.append(rr)
        b.subject3(universe_hex, r["nativeSubjectId"])
    rr = replay_rule(
        b.s,
        rule=policy["rules"][0],
        program=program,
        program_digest=prog_d,
        subjects=rows,
        facts=facts,
        coverages=coverages,
        scopes=scopes,
        inventories=inventories,
        detector_closure=detector,
        view_ids=[view_id],
        import_ids=import_ids,
    )
    eval_refs = selected + [{"domain": "execution-inputs", "digest": ei_d}]
    eval_refs = sorted(eval_refs, key=lambda r: C(r))
    proof_id, proof = compose_proof(
        b.s,
        plan_id=plan_id,
        exec_plan_id=exec_id,
        evaluator_c=evaluator,
        program_digest=prog_d,
        eval_input_refs=eval_refs,
        rule_results=[rr],
        exec_inputs_digest=ei_d,
    )
    ev = {
        "schemaVersion": 3,
        "planId": plan_id,
        "viewIds": [view_id],
        "coverageIds": sorted(c["id"] for c in coverages),
        "importIds": sorted(import_ids),
        "findingIds": sorted(rr["findingIds"]),
        "proofBundleId": proof_id,
    }
    ev_id = b.s.put_h("semantic-evidence", ev)
    seal = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": exec_id,
        "evidenceId": ev_id,
        "evaluatorClosure": evaluator,
        "policyDigest": pol_d,
        "proofBundleId": proof_id,
        "verdict": proof["verdict"],
    }
    seal_id = b.s.put_h("evaluation-seal", seal)
    run = {
        "schemaVersion": 3,
        "projectId": PROJECT,
        "snapshotId": snap,
        "planId": plan_id,
        "evidenceId": ev_id,
        "evaluationSealId": seal_id,
        "capabilityManifestId": cap_id,
    }
    run_id = b.s.put_h("run", run)
    return {
        "runId": run_id,
        "planId": plan_id,
        "snapshotId": snap,
        "viewId": view_id,
        "proofId": proof_id,
        "evidenceId": ev_id,
        "sealId": seal_id,
        "verdict": proof["verdict"],
        "replay": {
            "ruleResults": [rr],
            "proof": proof,
            "executionInputsDigest": ei_d,
        },
        "store": b.s,
        "classification": "valid",
        "outputMajor": 3,
        "nativeIdentityMajor": 2,
    }


def build_ts_run() -> dict[str, Any]:
    b = Builder()
    idx = b.add_file(
        "src/index.ts",
        "import pad from 'left-pad';\nexport function hello(n: number) {\n  return pad('x', n);\n}\n",
    )
    b.add_file("package.json", '{"name":"demo","version":"1.0.0","dependencies":{"left-pad":"1.0.0"}}\n')
    b.add_file("tsconfig.json", '{"compilerOptions":{"module":"node16","moduleResolution":"node16","target":"es2022","strict":true,"noEmit":true},"include":["src"]}\n')
    lock = b.add_file("package-lock.json", '{"lockfileVersion":3,"packages":{}}\n')
    b.add_file("node_modules/left-pad/package.json", '{"name":"left-pad","version":"1.0.0","main":"index.js"}\n')
    b.add_file("node_modules/left-pad/index.js", "module.exports = function pad() { return 'x'; };\n")
    inv = b.inventory_from_files()
    cfg, cfg_d = b.empty_config()
    sc, sc_d = b.scope_desc()
    vcs, vcs_d = b.vcs(inv)
    snap = b.snapshot(inv, cfg_d, sc_d, vcs_d)
    nm = _nm_layout(b)
    graph, gh = _config_graph(b, "tsconfig.json")
    ctx_d, ctx = b.ts_context(language_mode="ts-tsconfig", lock_path="package-lock.json", nm_digest=nm, graph=graph, honored=b.honored_ts())
    uni_d, uni = b.ts_universe(
        ctx_d,
        language_mode="ts-tsconfig",
        graph_hash=gh,
        js_roots=["node_modules/left-pad/index.js"],
        prog_roots=["src/index.ts"],
        allow_js=True,
        nm_in_read=True,
        lock_kind="package-lock",
    )
    uni_hex = uni_d
    provider = b.closure("provider", "ts-provider", {"bin/provider": b"ts"}, protocol_major=2, version="1.0.0")
    evaluator = b.closure("evaluator", "eval", {"bin/eval": b"eval"}, protocol_major=3, version="3.0.0")
    detector = b.closure("detector", "det", {"bin/det": b"det"}, protocol_major=3, version="1.0.0")
    adapter = b.closure("adapter", "imp-adapter", {"bin/ad": b"ad"}, protocol_major=1, version="1.0.0")
    cap_m = _manifest_for("typescript")
    cap = _admit_cap(cap_m)
    cap_bytes = bytes.fromhex(cap["committedBytesHex"])
    cap_bytes_d = b.s.put_blob(cap_bytes)
    policy, program, pol_d, prog_d = b.policy_exists_file("typescript")
    em, em_d = b.emission(pol_d, "file-exists", detector)
    scope_doc, scope_doc_d = b.scope_document()
    wai, wai_d = b.waiver_empty()
    # enumeration plan
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap,
        "scopeDigest": sc_d,
        "membershipDigest": "00" * 32,  # filled
        "cells": [],
    }
    unit = {
        "unitOrdinal": 0,
        "rootPath": ".",
        "languageFamily": "tsjs",
        "languageMode": "ts-tsconfig",
        "unitKind": "ts-program",
        "markerPath": "tsconfig.json",
        "markerSha256": sha256_hex(b.files["tsconfig.json"]),
        "recognizerId": "opensip.tsconfig",
        "recognizerVersion": 1,
        "provenance": "DISCOVERED",
        "memberPackageRoots": ["."],
    }
    mem_rows = []
    for p in sorted(b.files):
        fam = "tsjs"
        if p.startswith("node_modules/"):
            mem = "program-member" if p.endswith(".js") or p.endswith(".ts") else "syntax-only"
            reason = "deepest-unit-in-language"
        elif p.endswith(".ts"):
            mem, reason = "program-member", "deepest-unit-in-language"
        else:
            mem, reason = "syntax-only", "grammar-only"
        mem_rows.append({"path": p, "languageFamily": fam, "unitOrdinal": 0, "membership": mem, "reason": reason})
    membership = {
        "schemaVersion": 1,
        "units": [unit],
        "rows": mem_rows,
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }
    mem_d = b.s.put_canonical(membership)
    first_party = [p for p in sorted(b.files) if not p.startswith("node_modules/")]
    enum_plan["membershipDigest"] = mem_d
    enum_plan["cells"] = [
        {
            "capabilityId": "inventory",
            "languageMode": "ts-tsconfig",
            "workspaceRoot": ".",
            "required": True,
            "kinds": ["file", "package"],
            "programBindings": [
                {
                    "ordinal": 0,
                    "provenance": "default-unit",
                    "enumerator": {"status": "selected", "closureId": provider},
                    "nativeContextDigest": ctx_d,
                    "universe": uni_hex,
                    "programEntry": "tsconfig.json",
                    "extents": [
                        {"kind": "file", "paths": sorted(first_party)},
                        {"kind": "package", "paths": ["package.json"]},
                    ],
                }
            ],
        },
        {
            "capabilityId": "clones-fact",
            "languageMode": "ts-tsconfig",
            "workspaceRoot": ".",
            "required": True,
            "kinds": ["file"],
            "programBindings": [
                {
                    "ordinal": 0,
                    "provenance": "default-unit",
                    "enumerator": {"status": "selected", "closureId": provider},
                    "nativeContextDigest": ctx_d,
                    "universe": uni_hex,
                    "programEntry": "tsconfig.json",
                    "extents": [{"kind": "file", "paths": ["src/index.ts"]}],
                }
            ],
        },
    ]
    # sort cells by capabilityId, languageMode, workspaceRoot
    enum_plan["cells"] = sorted(enum_plan["cells"], key=lambda c: (c["capabilityId"], c["languageMode"], c["workspaceRoot"]))
    enum_d = b.s.put_canonical(enum_plan)
    file_rows = [b.file_inventory_row(p, "typescript" if p.endswith(".ts") else ("javascript" if p.endswith(".js") else "json")) for p in first_party]
    # subject language table: json for package.json, ts for ts, etc.
    inv_file = {
        "schemaVersion": 1,
        "planId": "plan2:" + "00" * 32,  # filled after plan
        "parameterDigest": enum_d,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sorted(first_party),
        "rows": file_rows,
    }
    grant, grant_d = b.grant(provider, sc_d, ["read-source", "native-analysis", "read-import"])
    caps = [_cap("inventory", "ts-tsconfig"), _cap("syntax", "ts-tsconfig"), _cap("clones-fact", "ts-tsconfig"), _cap("imports", "ts-tsconfig")]
    spec, spec_d = b.analysis_spec(
        caps,
        [
            b.param(KC.ENUM_PLAN_SHA, enum_plan),
            b.param(KC.EMISSION_SHA, em),
            b.param(KC.POLICY_V1_SHA, scope_doc),
        ],
    )
    imp = make_import(b, snap, adapter, provider, sc_d)
    plan = _plan(
        b, snap, cap["capabilityManifestId"], cap_bytes_d,
        [provider, evaluator, detector, adapter, b.closures["ts-toolchain"], b.closures["ts-stdlib"]],
        spec_d, cfg_d, [ctx_d], [imp], pol_d, wai_d, sc_d, grant_d,
    )
    inv_file["planId"] = plan
    inv_d = b.s.put_canonical(inv_file)
    src = "src/index.ts"
    # function body span: find "export function hello"
    text = b.files[src]
    start = text.find(b"export function hello")
    end = text.find(b"\n}\n") + 2
    blv = _blv_ts(ctx, src)
    b.s.put_canonical(blv)
    file_facts = [b.file_fact(snap, uni_hex, p, provider) for p in first_party]
    clone_ids = b.clone_facts(snap, uni_hex, src, start, end, provider, blv, LEVEL_SPEC, "typescript")
    caller = "ts:src/index.ts:hello"
    callee = "ts:node_modules/left-pad/index.js:pad"
    call_id = b.calls_fact(snap, uni_hex, src, caller, callee, provider)
    scope_file = b.subject_scope(snap, uni_hex, "file", "enumerated", first_party, provider)
    scope_clone = b.subject_scope(snap, uni_hex, "clones", "normalized-body-hash", [src], provider)
    scope_calls = b.subject_scope(snap, uni_hex, "calls", "resolved-callee", [caller], provider)
    cov_file = b.coverage(scope_file, "file", "enumerated", uni_hex, uni_hex, coverage="complete", deficiency=None, native_cause=None, subject_count=len(first_party))
    cov_clone = b.coverage(scope_clone, "clones", "normalized-body-hash", uni_hex, uni_hex, coverage="complete", deficiency=None, native_cause=None, subject_count=1)
    cov_calls = b.coverage(
        scope_calls, "calls", "resolved-callee", uni_hex, uni_hex,
        coverage="complete", deficiency=None, native_cause=None, subject_count=1,
        rc=b.rc_resolved_complete(),
    )
    facts_all = file_facts + clone_ids + [call_id]
    view = b.view(plan, [scope_file, scope_clone, scope_calls], facts_all, [cov_file, cov_clone, cov_calls], provider)
    # wrap facts/coverages/scopes for evaluator
    def wrap_facts(ids):
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = None
            if d["payloadDigest"] in b.s.blobs:
                import json
                payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_cov(ids):
        import json
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_sc(ids):
        return [{"id": i, "descriptor": b.s.objects[i]["descriptor"]} for i in ids]
    result = _finish(
        b,
        plan_id=plan,
        snap=snap,
        view_id=view,
        provider=provider,
        evaluator=evaluator,
        detector=detector,
        policy=policy,
        program=program,
        pol_d=pol_d,
        prog_d=prog_d,
        cap_id=cap["capabilityManifestId"],
        facts=wrap_facts(facts_all),
        coverages=wrap_cov([cov_file, cov_clone, cov_calls]),
        scopes=wrap_sc([scope_file, scope_clone, scope_calls]),
        inventories=[{"digest": inv_d, "record": inv_file, "capabilityId": "inventory", "languageMode": "ts-tsconfig", "universe": uni_hex}],
        import_ids=[imp],
        universe_hex=uni_hex,
        file_rows=file_rows,
    )
    result["kind"] = "typescript"
    result["properties"] = {
        "nodeModules": True,
        "bareSpecifier": "left-pad",
        "configGraph": graph,
        "scopeDocument": scope_doc,
        "scopeDocumentSelector": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1",
        "nativeContextDigest": ctx_d,
        "universe": uni_hex,
        "fileFacts": file_facts,
        "cloneFacts": clone_ids,
        "importedPayload": imp,
        "levelSpecSha256": sha256_hex(LEVEL_SPEC),
        "bodyLanguageVersion": blv,
    }
    return result


def build_rust_run(*, partial_clones: bool = False, ownership_alt: bool = False) -> dict[str, Any]:
    b = Builder()
    b.add_file("Cargo.toml", '[workspace]\nmembers=["crates/alpha","crates/beta","crates/#marker"]\nresolver="2"\n')
    b.add_file("Cargo.lock", "# lock\nversion = 3\n")
    b.add_file("crates/alpha/Cargo.toml", '[package]\nname="alpha"\nversion="0.1.0"\nedition="2018"\n')
    b.add_file("crates/alpha/src/lib.rs", "pub fn alpha() { let x = 1; }\n")
    b.add_file("crates/beta/Cargo.toml", '[package]\nname="beta"\nversion="0.1.0"\nedition="2021"\n[[bin]]\nname="beta"\npath="src/main.rs"\nedition="2024"\n')
    shared = "pub fn shared() { let y = 2; }\n"
    b.add_file("crates/beta/src/lib.rs", shared)
    b.add_file("crates/beta/src/main.rs", "fn main() { beta::shared(); }\n")
    b.add_file("crates/#marker/Cargo.toml", '[package]\nname="hashmark"\nversion="0.1.0"\nedition="2021"\n')
    b.add_file("crates/#marker/src/lib.rs", "pub fn hm() {}\n")
    # extra crates for large edition map
    for i in range(8):
        name = f"c{i:02d}"
        ed = [2015, 2018, 2021, 2024][i % 4]
        b.add_file(f"crates/{name}/Cargo.toml", f'[package]\nname="{name}"\nversion="0.1.0"\nedition="{ed}"\n')
        b.add_file(f"crates/{name}/src/lib.rs", f"pub fn f{i}() {{}}\n")
    inv = b.inventory_from_files()
    cfg, cfg_d = b.empty_config()
    sc, sc_d = b.scope_desc()
    vcs, vcs_d = b.vcs(inv)
    snap = b.snapshot(inv, cfg_d, sc_d, vcs_d)
    cargo_bytes = b"\n"
    b.s.put_blob(cargo_bytes)
    cproj = b.cargo_proj([], cargo_bytes)
    cproj_h = b.s.put_native("native.cargo-config-projection.v2", cproj)
    # dependency set empty complete
    lock = {"path": "Cargo.lock", "contentSha256": sha256_hex(b.files["Cargo.lock"]), "lockfileVersion": 3}
    dep = {
        "schemaVersion": 1,
        "language": "rust",
        "lockfileIdentity": lock,
        "packages": [],
        "completeness": {"state": "complete", "missing": []},
    }
    dep_id = b.s.put_native("native.dependency-source-set.v1", dep)
    feat = {
        "schemaVersion": 1,
        "resolverVersion": 2,
        "targetTriple": TRIPLE,
        "activated": [],
        "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "1"},
    }
    feat_id = b.s.put_native("native.unified-features.rust.v1", feat)
    # units
    def uid(marker, kind, name):
        return b.unit_id(marker, kind, name)
    lib_alpha = uid("crates/alpha/Cargo.toml", "lib", "alpha")
    lib_beta = uid("crates/beta/Cargo.toml", "lib", "beta")
    bin_beta = uid("crates/beta/Cargo.toml", "bin", "beta")
    lib_hm = uid("crates/#marker/Cargo.toml", "lib", "hashmark")
    extra_units = []
    for i in range(8):
        extra_units.append(uid(f"crates/c{i:02d}/Cargo.toml", "lib", f"c{i:02d}"))
    units = [
        {"unitId": lib_alpha, "markerPath": "crates/alpha/Cargo.toml", "crateName": "alpha", "targetKind": "lib", "targetName": "alpha", "targetEdition": None},
        {"unitId": lib_beta, "markerPath": "crates/beta/Cargo.toml", "crateName": "beta", "targetKind": "lib", "targetName": "beta", "targetEdition": None},
        {"unitId": bin_beta, "markerPath": "crates/beta/Cargo.toml", "crateName": "beta", "targetKind": "bin", "targetName": "beta", "targetEdition": 2024},
        {"unitId": lib_hm, "markerPath": "crates/#marker/Cargo.toml", "crateName": "hashmark", "targetKind": "lib", "targetName": "hashmark", "targetEdition": None},
    ]
    for i, u in enumerate(extra_units):
        units.append({"unitId": u, "markerPath": f"crates/c{i:02d}/Cargo.toml", "crateName": f"c{i:02d}", "targetKind": "lib", "targetName": f"c{i:02d}", "targetEdition": None})
    units = sorted(units, key=lambda x: x["unitId"].encode())
    ownership = [
        {"path": "crates/alpha/src/lib.rs", "unitId": lib_alpha},
        {"path": "crates/beta/src/lib.rs", "unitId": lib_beta},
        {"path": "crates/beta/src/lib.rs", "unitId": bin_beta},  # same file two targets
        {"path": "crates/beta/src/main.rs", "unitId": bin_beta},
        {"path": "crates/#marker/src/lib.rs", "unitId": lib_hm},
    ]
    for i in range(8):
        ownership.append({"path": f"crates/c{i:02d}/src/lib.rs", "unitId": extra_units[i]})
    ownership = sorted(ownership, key=lambda x: (x["path"].encode(), x["unitId"].encode()))
    selected = [lib_alpha, lib_beta, bin_beta, lib_hm] + extra_units
    if ownership_alt:
        # only lib_beta, not bin — same path, same effective edition for lib (2021)
        selected = [lib_alpha, lib_beta, lib_hm] + extra_units
    selected = sorted(set(selected))
    own = {
        "schemaVersion": 1,
        "enumeration": "partial" if partial_clones else "complete",
        "units": units,
        "selectedUnitIds": selected,
        "ownership": ownership,
    }
    own_id = b.s.put_native("native.source-unit-ownership.v1", own)
    edition_map = {"alpha": 2018, "beta": 2021, "hashmark": 2021}
    for i in range(8):
        edition_map[f"c{i:02d}"] = [2015, 2018, 2021, 2024][i % 4]
    ctx_d, ctx = b.rust_context(dep_id=dep_id, feat_id=feat_id, prep_id=None, cargo_proj=cproj)
    crate_roots = ["crates/alpha", "crates/beta", "crates/#marker"] + [f"crates/c{i:02d}" for i in range(8)]
    uni_d, uni = b.rust_universe(
        ctx_d,
        edition_map=edition_map,
        crate_roots=crate_roots,
        lock=lock,
        dep_id=dep_id,
        feat_id=feat_id,
        own_id=own_id,
        cfg_proj_h=cproj_h,
        prep_id=None,
        prepared="none",
    )
    provider = b.closure("provider", "rust-provider", {"bin/p": b"rust"}, protocol_major=3, version="1.0.0")
    evaluator = b.closure("evaluator", "eval", {"bin/e": b"e"}, protocol_major=3, version="3.0.0")
    detector = b.closure("detector", "det", {"bin/d": b"d"}, protocol_major=3, version="1.0.0")
    adapter = b.closure("adapter", "ad", {"bin/a": b"a"}, protocol_major=1, version="1.0.0")
    cap = _admit_cap(_manifest_for("rust"))
    cap_bytes_d = b.s.put_blob(bytes.fromhex(cap["committedBytesHex"]))
    policy, program, pol_d, prog_d = b.policy_exists_file("rust")
    em, em_d = b.emission(pol_d, "file-exists", detector)
    scope_doc, _ = b.scope_document()
    wai, wai_d = b.waiver_empty()
    rust_src = [p for p in sorted(b.files) if p.endswith(".rs") or p.endswith("Cargo.toml") or p == "Cargo.lock"]
    first_party = rust_src
    unit_ws = {
        "unitOrdinal": 0,
        "rootPath": ".",
        "languageFamily": "rust",
        "languageMode": "rust-cargo",
        "unitKind": "cargo-workspace",
        "markerPath": "Cargo.toml",
        "markerSha256": sha256_hex(b.files["Cargo.toml"]),
        "recognizerId": "opensip.cargo",
        "recognizerVersion": 1,
        "provenance": "DISCOVERED",
        "memberPackageRoots": crate_roots,
    }
    mem_rows = [{"path": p, "languageFamily": "rust", "unitOrdinal": 0, "membership": "program-member" if p.endswith(".rs") else "syntax-only", "reason": "deepest-unit-in-language" if p.endswith(".rs") else "grammar-only"} for p in first_party]
    membership = {"schemaVersion": 1, "units": [unit_ws], "rows": mem_rows, "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
    mem_d = b.s.put_canonical(membership)
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": [
            {
                "capabilityId": "inventory",
                "languageMode": "rust-cargo",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file", "package"],
                "programBindings": [
                    {
                        "ordinal": 0,
                        "provenance": "default-unit",
                        "enumerator": {"status": "selected", "closureId": provider},
                        "nativeContextDigest": ctx_d,
                        "universe": uni_d,
                        "programEntry": None,
                        "extents": [{"kind": "file", "paths": sorted(first_party)}, {"kind": "package", "paths": [p for p in first_party if p.endswith("Cargo.toml") and p != "Cargo.toml"]}],
                    }
                ],
            }
        ],
    }
    enum_d = b.s.put_canonical(enum_plan)
    file_rows = [b.file_inventory_row(p, "rust" if p.endswith(".rs") else "toml") for p in first_party]
    inv_file = {
        "schemaVersion": 1,
        "planId": "plan2:" + "00" * 32,
        "parameterDigest": enum_d,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sorted(first_party),
        "rows": file_rows,
    }
    grant, grant_d = b.grant(provider, sc_d, ["read-source", "native-analysis"])
    spec, spec_d = b.analysis_spec(
        [_cap("inventory", "rust-cargo"), _cap("syntax", "rust-cargo"), _cap("clones-fact", "rust-cargo")],
        [b.param(KC.ENUM_PLAN_SHA, enum_plan), b.param(KC.EMISSION_SHA, em), b.param(KC.POLICY_V1_SHA, scope_doc)],
    )
    plan = _plan(
        b, snap, cap["capabilityManifestId"], cap_bytes_d,
        [provider, evaluator, detector, adapter, b.closures["rust-toolchain"], b.closures["rust-llvm"]],
        spec_d, cfg_d, [ctx_d], [], pol_d, wai_d, sc_d, grant_d,
    )
    inv_file["planId"] = plan
    inv_d = b.s.put_canonical(inv_file)
    file_facts = [b.file_fact(snap, uni_d, p, provider) for p in first_party]
    clone_ids = []
    if not partial_clones:
        path = "crates/alpha/src/lib.rs"
        text = b.files[path]
        start = 0
        end = len(text)
        blv = _blv_rust(ctx, 2018)
        b.s.put_canonical(blv)
        clone_ids = b.clone_facts(snap, uni_d, path, start, end, provider, blv, LEVEL_SPEC, "rust")
        # second edition of shared file under 2024 bin
        path2 = "crates/beta/src/lib.rs"
        blv2 = _blv_rust(ctx, 2024)
        b.s.put_canonical(blv2)
        t2 = b.files[path2]
        clone_ids += b.clone_facts(snap, uni_d, path2, 0, len(t2), provider, blv2, LEVEL_SPEC, "rust")
    scope_file = b.subject_scope(snap, uni_d, "file", "enumerated", first_party, provider)
    cov_file = b.coverage(scope_file, "file", "enumerated", uni_d, uni_d, coverage="complete", deficiency=None, native_cause=None, subject_count=len(first_party))
    scopes = [scope_file]
    covs = [cov_file]
    facts_all = file_facts + clone_ids
    if partial_clones:
        scope_c = b.subject_scope(snap, uni_d, "clones", "normalized-body-hash", ["crates/alpha/src/lib.rs"], provider)
        cov_c = b.coverage(
            scope_c, "clones", "normalized-body-hash", uni_d, uni_d,
            coverage="unknown",
            deficiency="input-closure-incomplete",
            native_cause="body-language-owner-unenumerated",
            subject_count=1,
        )
        scopes.append(scope_c)
        covs.append(cov_c)
    view = b.view(plan, [s if isinstance(s, str) else s for s in scopes], facts_all, covs, provider)
    import json
    def wrap_facts(ids):
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_cov(ids):
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_sc(ids):
        return [{"id": i, "descriptor": b.s.objects[i]["descriptor"]} for i in ids]
    result = _finish(
        b, plan_id=plan, snap=snap, view_id=view, provider=provider, evaluator=evaluator, detector=detector,
        policy=policy, program=program, pol_d=pol_d, prog_d=prog_d, cap_id=cap["capabilityManifestId"],
        facts=wrap_facts(facts_all), coverages=wrap_cov(covs), scopes=wrap_sc(scopes),
        inventories=[{"digest": inv_d, "record": inv_file, "capabilityId": "inventory", "languageMode": "rust-cargo", "universe": uni_d}],
        import_ids=[], universe_hex=uni_d, file_rows=file_rows,
    )
    result["kind"] = "rust-partial" if partial_clones else "rust"
    result["properties"] = {
        "mixedEdition": edition_map,
        "targetEditionDiffers": {"packageDefault": 2021, "binTarget": 2024, "path": "crates/beta/src/lib.rs"},
        "hashMarker": "crates/#marker",
        "sameFileTwoEditions": {"path": "crates/beta/src/lib.rs", "libEdition": 2021, "binEdition": 2024},
        "largeEditionMap": edition_map,
        "partialClones": partial_clones,
        "ownershipAlt": ownership_alt,
        "nativeContextDigest": ctx_d,
        "universe": uni_d,
        "cloneFacts": clone_ids,
        "sourceUnitOwnershipId": own_id,
        "bodyLanguageVersionInputs": {"compilerVersion": RUSTC_VERSION, "rustCommitHash": RUST_COMMIT},
    }
    if partial_clones:
        result["properties"]["deficiencyPairing"] = {
            "deficiency": "input-closure-incomplete",
            "nativeCause": "body-language-owner-unenumerated",
            "coverage": "unknown",
            "selector": "native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete",
        }
    return result


def _syntax_grammars(code: bool) -> list[dict]:
    if code:
        return [
            {
                "grammarId": "typescript-ts",
                "grammarVersion": "1",
                "languageId": "typescript",
                "suffixes": [".ts"],
                "syntaxClass": "code",
                "grammarDigest": "00" * 32,
            }
        ]
    return [
        {
            "grammarId": "json-doc",
            "grammarVersion": "1",
            "languageId": "json",
            "suffixes": [".json"],
            "syntaxClass": "data-document",
            "grammarDigest": "00" * 32,
        }
    ]


def build_syntax_run(*, data: bool) -> dict[str, Any]:
    b = Builder()
    if data:
        b.add_file("data/config.json", '{"a":1}\n')
        b.add_file("README.md", "# demo\n")
        mode = "syntax-only"
        grammars = _syntax_grammars(False)
        lang_univ = "syntax"
        file_lang = {"data/config.json": "json", "README.md": "markdown"}
    else:
        b.add_file("src/tool.py", "def main():\n    return 1\n")  # wait - python is unbundled
        # supported code grammar: typescript without being a TS compilation unit
        b.files.clear()
        b.add_file("notes.md", "# not compiled\n")
        b.add_file("src/util.ts", "export function n() { return 1; }\n")
        grammars = _syntax_grammars(True)
        # also include json grammar? code run is typescript grammar
        file_lang = {"notes.md": "markdown", "src/util.ts": "typescript"}
        lang_univ = "syntax"
    inv = b.inventory_from_files()
    cfg, cfg_d = b.empty_config()
    sc, sc_d = b.scope_desc()
    vcs, vcs_d = b.vcs(inv)
    snap = b.snapshot(inv, cfg_d, sc_d, vcs_d)
    ctx_d, ctx = b.syntax_context(grammars, LEVEL_SPEC)
    gids = [g["grammarId"] for g in grammars]
    uni_d, uni = b.syntax_universe(ctx_d, gids)
    provider = b.closure("provider", "syntax-provider", {"bin/p": b"syn"}, protocol_major=1, version="1.0.0")
    evaluator = b.closure("evaluator", "eval", {"bin/e": b"e"}, protocol_major=3, version="3.0.0")
    detector = b.closure("detector", "det", {"bin/d": b"d"}, protocol_major=3, version="1.0.0")
    adapter = b.closure("adapter", "ad", {"bin/a": b"a"}, protocol_major=1, version="1.0.0")
    cap = _admit_cap(_manifest_for("syntax"))
    cap_bytes_d = b.s.put_blob(bytes.fromhex(cap["committedBytesHex"]))
    policy, program, pol_d, prog_d = b.policy_exists_file("syntax")
    em, em_d = b.emission(pol_d, "file-exists", detector)
    scope_doc, _ = b.scope_document()
    wai, wai_d = b.waiver_empty()
    paths = sorted(b.files)
    unit = {
        "unitOrdinal": 0,
        "rootPath": ".",
        "languageFamily": "none",
        "languageMode": "syntax-only",
        "unitKind": "syntax-only",
        "markerPath": paths[0],
        "markerSha256": sha256_hex(b.files[paths[0]]),
        "recognizerId": "opensip.syntax",
        "recognizerVersion": 1,
        "provenance": "DISCOVERED",
        "memberPackageRoots": ["."],
    }
    mem_rows = [{"path": p, "languageFamily": "none", "unitOrdinal": 0, "membership": "syntax-only", "reason": "grammar-only"} for p in paths]
    membership = {"schemaVersion": 1, "units": [unit], "rows": mem_rows, "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
    mem_d = b.s.put_canonical(membership)
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": [
            {
                "capabilityId": "inventory",
                "languageMode": "syntax-only",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file", "package"],
                "programBindings": [
                    {
                        "ordinal": 0,
                        "provenance": "default-unit",
                        "enumerator": {"status": "selected", "closureId": provider},
                        "nativeContextDigest": ctx_d,
                        "universe": uni_d,
                        "programEntry": None,
                        "extents": [{"kind": "file", "paths": paths}],
                    }
                ],
            }
        ],
    }
    enum_d = b.s.put_canonical(enum_plan)
    file_rows = [b.file_inventory_row(p, file_lang.get(p, "unspecified")) for p in paths]
    inv_file = {
        "schemaVersion": 1,
        "planId": "plan2:" + "00" * 32,
        "parameterDigest": enum_d,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": paths,
        "rows": file_rows,
    }
    grant, grant_d = b.grant(provider, sc_d, ["read-source", "native-analysis"])
    requested = [_cap("inventory", "syntax-only"), _cap("syntax", "syntax-only")]
    if data:
        requested.append(_cap("clones-fact", "syntax-only", required=True))
    spec, spec_d = b.analysis_spec(
        requested,
        [b.param(KC.ENUM_PLAN_SHA, enum_plan), b.param(KC.EMISSION_SHA, em), b.param(KC.POLICY_V1_SHA, scope_doc)],
    )
    plan = _plan(
        b, snap, cap["capabilityManifestId"], cap_bytes_d,
        [provider, evaluator, detector, adapter, b.closures["syntax-bundle"]],
        spec_d, cfg_d, [ctx_d], [], pol_d, wai_d, sc_d, grant_d,
    )
    inv_file["planId"] = plan
    inv_d = b.s.put_canonical(inv_file)
    file_facts = [b.file_fact(snap, uni_d, p, provider) for p in paths]
    clone_ids = []
    if not data:
        p = "src/util.ts"
        t = b.files[p]
        blv = {
            "schemaVersion": 1,
            "languageId": "typescript",
            "compilerName": "opensip-syntax",
            "compilerVersion": "1.0.0",
            "compilerBuild": "syntax-bundle-1",
            "dialect": {"grammarVariant": "ts"},
        }
        # grammarVariant branch for syntax-only
        b.s.put_canonical(blv)
        start = t.find(b"export function n")
        end = len(t)
        clone_ids = b.clone_facts(snap, uni_d, p, start, end, provider, blv, LEVEL_SPEC, "typescript")
    scope_file = b.subject_scope(snap, uni_d, "file", "enumerated", paths, provider)
    cov_file = b.coverage(scope_file, "file", "enumerated", uni_d, uni_d, coverage="complete", deficiency=None, native_cause=None, subject_count=len(paths))
    scopes = [scope_file]
    covs = [cov_file]
    if data:
        scope_c = b.subject_scope(snap, uni_d, "clones", "normalized-body-hash", paths, provider)
        cov_c = b.coverage(
            scope_c, "clones", "normalized-body-hash", uni_d, uni_d,
            coverage="unknown",
            deficiency="language-tier-unsupported",
            native_cause="capability-missing",
            subject_count=len(paths),
        )
        scopes.append(scope_c)
        covs.append(cov_c)
    elif clone_ids:
        scope_c = b.subject_scope(snap, uni_d, "clones", "normalized-body-hash", ["src/util.ts"], provider)
        cov_c = b.coverage(scope_c, "clones", "normalized-body-hash", uni_d, uni_d, coverage="complete", deficiency=None, native_cause=None, subject_count=1)
        scopes.append(scope_c)
        covs.append(cov_c)
    facts_all = file_facts + clone_ids
    view = b.view(plan, scopes, facts_all, covs, provider)
    import json
    def wrap_facts(ids):
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_cov(ids):
        out = []
        for i in ids:
            d = b.s.objects[i]["descriptor"]
            payload = json.loads(b.s.blobs[d["payloadDigest"]])
            out.append({"id": i, "descriptor": d, "payload": payload})
        return out
    def wrap_sc(ids):
        return [{"id": i, "descriptor": b.s.objects[i]["descriptor"]} for i in ids]
    result = _finish(
        b, plan_id=plan, snap=snap, view_id=view, provider=provider, evaluator=evaluator, detector=detector,
        policy=policy, program=program, pol_d=pol_d, prog_d=prog_d, cap_id=cap["capabilityManifestId"],
        facts=wrap_facts(facts_all), coverages=wrap_cov(covs), scopes=wrap_sc(scopes),
        inventories=[{"digest": inv_d, "record": inv_file, "capabilityId": "inventory", "languageMode": "syntax-only", "universe": uni_d}],
        import_ids=[], universe_hex=uni_d, file_rows=file_rows,
    )
    result["kind"] = "syntax-data" if data else "syntax-code"
    result["properties"] = {
        "noCompilerUnit": True,
        "grammar": grammars,
        "nativeContextDigest": ctx_d,
        "universe": uni_d,
        "fileFacts": file_facts,
        "cloneFacts": clone_ids,
        "dataUnsupportedClones": data,
        "unavailableSemantic": (
            {"deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"} if data else None
        ),
    }
    return result
