"""Corrected TypeScript complete-Run constructor for the pilot checkpoint.

Keeps original TS/node_modules/config-dependency/import/ScopeDocument/file-inventory/clone
properties. Fills enumeration extents, expected inventories, cell outcomes, native
coverage accounts, candidate envelopes, and independently enumerable file subjects.
"""
from __future__ import annotations

from . import builder, canonical, cap_admit, evaluator, h, order, store
from . import runs
from . import clone_body  # noqa: F401
from .pilot_checks import KIND_DERIVATION, MATRIX_RELATIONS, subject_language_for_path


def sha(b: bytes) -> str:
    return runs.sha(b)


def raw_c(obj) -> str:
    return runs.raw_c(obj)


def _extent(kind: str, paths: list[str]) -> dict:
    return {"kind": kind, "paths": order.cset(list(paths))}


def _binding(provider_id, ctx_hex, uhex, program_entry, extents, candidate_paths=None) -> dict:
    b = {
        "ordinal": 0,
        "provenance": "default-unit",
        "enumerator": runs.selected_enumerator(provider_id),
        "nativeContextDigest": ctx_hex,
        "universe": uhex,
        "programEntry": program_entry,
        "extents": extents,
    }
    if candidate_paths is not None:
        b["candidateSourcePaths"] = order.cset(list(candidate_paths))
    return b


def _inventory(st, plan_id, ep_d, cell_ordinal, program_ordinal, kind, paths, rows) -> tuple[dict, str]:
    rec = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": ep_d,
        "cellOrdinal": cell_ordinal,
        "programOrdinal": program_ordinal,
        "kind": kind,
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": order.cset(list(paths)),
        "rows": rows,
    }
    digest = raw_c(rec)
    st.put_raw_digest_record(rec)
    rec["_digest"] = digest
    return rec, digest


def _file_rows(paths: list[str]) -> list[dict]:
    rows = []
    for p in sorted(paths, key=lambda x: x.encode("utf-8")):
        rows.append(
            {
                "nativeSubjectId": p,
                "kind": "file",
                "path": p,
                "qualifiedName": p,
                "subjectLanguage": subject_language_for_path(p),
                "signatureTokens": [],
                "projections": [],
            }
        )
    rows.sort(key=lambda r: r["nativeSubjectId"].encode("utf-8"))
    return rows


def _package_rows() -> list[dict]:
    return [
        {
            "nativeSubjectId": "demo",
            "kind": "package",
            "path": "package.json",
            "qualifiedName": "demo",
            "subjectLanguage": "json",
            "signatureTokens": [],
            "projections": [],
        }
    ]


def _symbol_rows(detector_id: str) -> list[dict]:
    return [
        {
            "nativeSubjectId": "symbol:src/index.ts::x",
            "kind": "symbol",
            "path": "src/index.ts",
            "qualifiedName": "x",
            "subjectLanguage": "typescript",
            "exported": "exported",
            "signatureTokens": ["x"],
            "projections": [{"closureId": detector_id, "signatureTokens": ["x"]}],
        }
    ]


def _candidate_envelope(st, plan_id, exec_plan_id, cell_ordinal, cap, uhex, producer, examined) -> tuple[dict, str]:
    rec = {
        "schemaVersion": 1,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "cellOrdinal": cell_ordinal,
        "programOrdinal": 0,
        "capabilityId": cap,
        "languageMode": "ts-tsconfig",
        "universe": uhex,
        "producerClosure": producer,
        "stageOrdinal": 0,
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "authority": "candidate-only",
        "semanticEquivalenceClaimed": False,
        "automaticDeletionEligible": False,
        "examinedPaths": order.cset(list(examined)),
        "groupDigests": [],
        "sourceBodies": [],
    }
    digest = raw_c(rec)
    st.put_raw_digest_record(rec)
    rec["_digest"] = digest
    return rec, digest


def build_ts_run() -> dict:
    st = store.Store()
    pid = builder.project_id()
    src = b'import leftPad from "left-pad";\nexport const x = leftPad("a", 2);\n'
    pkg = b'{"name":"demo","type":"module","dependencies":{"left-pad":"1.3.0"}}\n'
    tscfg = b'{"extends":["./tsconfig.base.json","./tsconfig.base.json"],"compilerOptions":{"module":"nodenext","moduleResolution":"nodenext","strict":true,"noEmit":true},"include":["src"]}\n'
    tscfg_base = b'{"compilerOptions":{"target":"es2022"}}\n'
    lock = b'{"lockfileVersion":3,"packages":{"":{},"node_modules/left-pad":{"version":"1.3.0"}}}\n'
    lp_pkg = b'{"name":"left-pad","version":"1.3.0"}\n'
    lp_js = b"export default function leftPad(s,n){return s;}\n"
    files = {
        "src/index.ts": src,
        "package.json": pkg,
        "tsconfig.json": tscfg,
        "tsconfig.base.json": tscfg_base,
        "package-lock.json": lock,
    }
    st.put_blob(lp_pkg)
    st.put_blob(lp_js)

    stdlib_id, stdlib_suffix, dts = runs.make_stdlib_closure(st)
    tsc_bin = b"typescript-compiler"
    runtime_bin = b"node-runtime"
    tool_id = runs.make_toolchain_closure(st, {"bin/tsc": tsc_bin, "bin/node": runtime_bin})
    provider_id = runs.make_provider_closure(st, "ts-provider", 2)
    evaluator_id = runs.make_evaluator_closure(st)
    detector_id = runs.make_detector_closure(st)
    adapter_id = runs.make_adapter_closure(st)

    default_caps = list(builder.TS_TSCONFIG_DEFAULT_CAPS)
    cfg = builder.semantic_config(default_caps)
    cfg_d = raw_c(cfg)
    st.put_raw_digest_record(cfg)
    sc = builder.scope_desc(["."])
    sc_d = raw_c(sc)
    st.put_raw_digest_record(sc)
    snap, snap_id, inv = runs.snapshot_from_files(st, files, pid, cfg_d, sc_d)
    inv_paths = sorted(files.keys(), key=lambda p: p.encode("utf-8"))
    file_extent = list(inv_paths)
    symbol_extent = ["src/index.ts"]
    package_extent = ["package.json"]
    candidate_paths = ["src/index.ts"]

    layout = {
        "schemaVersion": 1,
        "entries": [
            {
                "packageName": "left-pad",
                "packageVersion": "1.3.0",
                "installPath": "node_modules/left-pad",
                "realPath": "node_modules/left-pad",
                "contentSha256": sha(lp_pkg),
            }
        ],
    }
    layout_d = raw_c(layout)
    st.put_raw_digest_record(layout)

    cfg_graph_nodes = [
        {
            "path": "tsconfig.json",
            "contentSha256": sha(tscfg),
            "kind": "tsconfig",
            "extendsResolved": ["tsconfig.base.json", "tsconfig.base.json"],
        },
        {
            "path": "tsconfig.base.json",
            "contentSha256": sha(tscfg_base),
            "kind": "other",
            "extendsResolved": [],
        },
    ]
    cfg_graph_nodes.sort(key=lambda n: n["path"].encode("utf-8"))
    cfg_graph = {
        "schemaVersion": 1,
        "entryConfigPath": "tsconfig.json",
        "nodes": cfg_graph_nodes,
    }
    cfg_graph_d = raw_c(cfg_graph)
    st.put_raw_digest_record(cfg_graph)

    ctx = {
        "schemaVersion": 2,
        "languageMode": "ts-tsconfig",
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": "5.4.5",
            "compilerPackageDigest": sha(tsc_bin),
            "typescriptStdlibMerkleRoot": stdlib_suffix,
            "standardLibraryComponentDigests": [{"component": "lib.es2022.d.ts", "sha256": sha(dts)}],
            "libSelection": ["es2022"],
        },
        "toolClosure": {
            "compiler": sha(tsc_bin),
            "runtime": sha(runtime_bin),
            "closureId": tool_id,
        },
        "configProjection": {
            "schemaVersion": 2,
            "ancestorCarrierVerified": True,
            "environmentSanitized": True,
            "typeAcquisitionEnabled": False,
            "executableSelected": False,
            "honoredOptions": builder._honored_ts(),
            "strippedOptions": [],
            "configGraphPaths": sorted(["tsconfig.json", "tsconfig.base.json"], key=lambda p: p.encode("utf-8")),
        },
        "moduleResolutionMode": "nodenext",
        "packageModuleType": "module",
        "nodeModulesLayoutDigest": layout_d,
        "lockfileIdentity": {
            "kind": "package-lock",
            "path": "package-lock.json",
            "contentSha256": sha(lock),
        },
    }
    ctx_hex = h.native_bare_hex("native.context.typescript.v2", ctx)
    st.put_canonical_record("native.context.typescript.v2", ctx)

    uni = {
        "schemaVersion": 2,
        "languageMode": "ts-tsconfig",
        "configOrigin": "tsconfig",
        "synthesizerVersion": None,
        "synthesizedOptions": None,
        "packageModuleType": "module",
        "allowJs": False,
        "checkJs": False,
        "jsAdmittedToProgram": False,
        "jsDiagnosticsEnabled": False,
        "resolutionCompletenessImplied": False,
        "jsRootFiles": [],
        "programRootFiles": ["src/index.ts"],
        "lockfileKind": "package-lock",
        "nodeModulesInReadSet": True,
        "executionCapableResolution": False,
        "tsconfigGraphHash": cfg_graph_d,
        "nativeContextId": h.native_sha256_text("native.context.typescript.v2", ctx),
    }
    uhex = h.native_bare_hex("native.semantic-universe.typescript.v2", uni)
    st.put_canonical_record("native.semantic-universe.typescript.v2", uni)

    prov = builder.ts_provider_cap()
    prov["platformIds"] = sorted(prov["platformIds"])
    cap = builder.minimal_cap_manifest("core", [prov], [])
    cap_adm = cap_admit.admit(cap)
    st.put_blob(bytes.fromhex(cap_adm["committedBytesHex"]))

    policy = builder.build_policy("file.exists", "typescript", "file", builder.file_exists_atom())
    pol_d = raw_c(policy)
    st.put_raw_digest_record(policy)
    waivers = builder.build_waivers()
    wav_d = raw_c(waivers)
    st.put_raw_digest_record(waivers)
    scope_doc = builder.build_scope_document()
    scope_doc_d = raw_c(scope_doc)
    st.put_raw_digest_record(scope_doc)
    grant = builder.grant(pid, sc_d, [provider_id, evaluator_id, detector_id], ["read-source", "native-analysis", "read-import"])
    grant_d = raw_c(grant)
    st.put_raw_digest_record(grant)

    membership = {
        "schemaVersion": 1,
        "units": [runs.workspace_unit(".", "tsjs", "ts-tsconfig", "ts-program", "tsconfig.json", sha(tscfg), 0)],
        "rows": runs.membership_rows_for_ts_files(inv_paths),
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }
    mem_d = raw_c(membership)
    st.put_raw_digest_record(membership)

    cells = []
    for cap_id in default_caps:
        kinds = list(KIND_DERIVATION[cap_id])
        if cap_id in ("clones-near", "clones-cross-tsjs"):
            extents = []
            cand = candidate_paths
        else:
            extents = [_extent(k, {"file": file_extent, "package": package_extent, "symbol": symbol_extent}[k]) for k in kinds]
            extents.sort(key=lambda e: e["kind"].encode("utf-8"))
            cand = None
        cells.append(
            {
                "capabilityId": cap_id,
                "languageMode": "ts-tsconfig",
                "workspaceRoot": ".",
                "required": True,
                "kinds": order.cset(kinds),
                "programBindings": [_binding(provider_id, ctx_hex, uhex, "tsconfig.json", extents, cand)],
            }
        )
    cells.sort(key=lambda c: (c["capabilityId"].encode("utf-8"), c["languageMode"].encode("utf-8"), c["workspaceRoot"].encode("utf-8")))
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": cells,
    }
    ep_d = raw_c(enum_plan)
    st.put_raw_digest_record(enum_plan)

    emission = {
        "schemaVersion": 1,
        "policyDigest": pol_d,
        "rules": [
            {
                "ruleId": "file.exists",
                "contributionId": "contrib.file-exists.v1",
                "ruleStableId": "file.exists",
                "semanticsMajor": 1,
                "detectorClosure": detector_id,
                "stabilityClass": "path-stable",
                "emissionProfile": "declarative-subject-v1",
            }
        ],
    }
    em_d = raw_c(emission)
    st.put_raw_digest_record(emission)

    spec = runs._analysis_spec(
        runs.requested_cap_rows(default_caps, "ts-tsconfig"),
        builder.POL_V1_DIGEST,
        scope_doc_d,
        extra_params=[
            {"schemaDigest": builder.ENUM_PLAN_DIGEST, "payloadDigest": ep_d},
            {"schemaDigest": builder.EMIT_PLAN_DIGEST, "payloadDigest": em_d},
        ],
    )
    spec_d = raw_c(spec)
    st.put_raw_digest_record(spec)

    runtime_payload = {
        "payloadDomain": "workflow.import-payload.runtime.v1",
        "format": "v8-json",
        "observationWindow": {"startUtc": "2026-01-15T00:00:00Z", "endUtc": "2026-01-15T01:00:00Z"},
        "observedPopulation": "synthetic",
        "subjects": [],
        "mappingGaps": [],
    }
    rp_d = raw_c(runtime_payload)
    st.put_raw_digest_record(runtime_payload)
    corr = {"kind": "exact-snapshot", "snapshotId": snap_id}
    corr_d = raw_c(corr)
    st.put_raw_digest_record(corr)
    build_id = {"schemaVersion": 1, "buildIdentity": None}
    build_d = raw_c(build_id)
    st.put_raw_digest_record(build_id)
    obs = {
        "schemaVersion": 1,
        "kind": "runtime",
        "window": {"startUtc": "2026-01-15T00:00:00Z", "endUtc": "2026-01-15T01:00:00Z"},
        "population": "synthetic",
        "selection": None,
        "revisionRange": None,
    }
    obs_d = raw_c(obs)
    st.put_raw_digest_record(obs)
    imp = {
        "schemaVersion": 2,
        "kind": "runtime",
        "payloadSchemaDigest": builder.IMP_DIGEST,
        "payloadDigest": rp_d,
        "sourceCorrespondenceDigest": corr_d,
        "buildDigest": build_d,
        "producerClosure": provider_id,
        "adapterClosure": adapter_id,
        "blobs": [],
        "scopeDigest": sc_d,
        "observationDigest": obs_d,
        "completeness": "complete",
        "omissions": [],
    }
    imp_id = st.put_canonical_record("import", imp)

    plan = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "capabilityManifestId": cap_adm["capabilityManifestId"],
        "semanticClosures": order.cset([provider_id, evaluator_id, detector_id, tool_id, stdlib_id, adapter_id]),
        "analysisSpecDigest": spec_d,
        "resolvedConfigDigest": cfg_d,
        "nativeContextDigests": order.cset([ctx_hex]),
        "importIds": order.cset([imp_id]),
        "policyDigest": pol_d,
        "waiverDigest": wav_d,
        "scopeDigest": sc_d,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_d,
        "capabilityManifestBytesDigest": cap_adm["committedBytesDigest"],
    }
    plan_id = st.put_canonical_record("plan", plan)

    # facts
    file_facts, file_ids = [], []
    for p, data in sorted(files.items(), key=lambda kv: kv[0].encode("utf-8")):
        ff, fid = runs.make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, runs.file_payload(p, data), [])
        file_facts.append(ff)
        file_ids.append(fid)
    f_pkg, fid_pkg = runs.make_fact(
        st, snap_id, "package", "manifest-declared", uhex, provider_id,
        {"packageName": "demo", "packageVersion": "0.0.0", "manifestPath": "package.json"}, [],
    )
    spec_l0 = b"level-spec-L0-verbatim-ts"
    spec_l1 = b"level-spec-L1-lexical-ts"
    lang_rec = runs.body_lang_ts(ctx, "ts", "typescript")
    cl0, _, _ = runs.mint_clone(st, level="L0-verbatim", body=src, lang_rec=lang_rec, lang_id="typescript", spec_bytes=spec_l0, anchor=None)
    cl1, _, _ = runs.mint_clone(st, level="L1-lexical", body=src, lang_rec=lang_rec, lang_id="typescript", spec_bytes=spec_l1, anchor=None)
    anchor = {"path": "src/index.ts", "blobDigest": sha(src), "startByte": 0, "endByte": len(src)}
    f_c0, fid_c0 = runs.make_fact(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, cl0, [anchor])
    f_c1, fid_c1 = runs.make_fact(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, cl1, [anchor])
    f_imp, fid_imp = runs.make_fact(
        st, snap_id, "imports", "syntactic-specifier", uhex, provider_id,
        {"importer": "symbol:src/index.ts::x", "specifier": "left-pad"}, [anchor],
    )
    f_imp_r, fid_imp_r = runs.make_fact(
        st, snap_id, "imports", "resolved-target", uhex, provider_id,
        {"importer": "symbol:src/index.ts::x", "specifier": "left-pad", "resolvedTarget": "package:left-pad"}, [anchor],
    )

    def mint_cov(relation, resolution, subjects, **kw):
        rec, sid, commit = runs.make_scope(st, snap_id, relation, resolution, uhex, provider_id, subjects)
        payload = runs.coverage_payload(relation, resolution, uhex, commit, len(subjects), **kw)
        cov, cid = runs.make_coverage(st, sid, payload)
        return rec, sid, cov, cid

    sc_file, scid_file, cov_f, cid_f = mint_cov("file", "enumerated", inv_paths)
    dialect_ok = [p for p in inv_paths if p.endswith((".ts", ".tsx", ".mts", ".cts", ".d.ts", ".js", ".jsx", ".mjs", ".cjs"))]
    dialect_bad = [p for p in inv_paths if p not in dialect_ok]
    sc_cl, scid_cl, cov_c, cid_c = mint_cov("clones", "normalized-body-hash", dialect_ok)
    sc_cl_u, scid_cl_u, cov_c_u, cid_c_u = mint_cov(
        "clones",
        "normalized-body-hash",
        dialect_bad,
        coverage="unknown",
        deficiency="language-tier-unsupported",
        nativeCause="capability-missing",
        state="not-applicable",
        attempted=False,
        exhaustive=True,
        stageTerminal="unavailable",
    )
    sc_im, scid_im, cov_i, cid_i = mint_cov("imports", "syntactic-specifier", ["symbol:src/index.ts::x"], state="not-applicable")
    sc_im_r, scid_im_r, cov_ir, cid_ir = mint_cov(
        "imports", "resolved-target", ["symbol:src/index.ts::x"],
        state="complete", attempted=True, exhaustive=True, stageTerminal="complete",
    )
    sc_pk, scid_pk, cov_p, cid_p = mint_cov("package", "manifest-declared", ["demo"])
    extra_cov = []
    extra_scopes = []
    symbol_subj = ["symbol:src/index.ts::x"]
    resolved_rungs = {
        ("imports", "resolved-target"),
        ("references", "resolved-binding"),
        ("calls", "resolved-callee"),
        ("types", "checked"),
        ("reachability", "from-resolved-calls"),
    }
    for rel, rung in [
        ("declares", "syntactic"),
        ("literal", "syntactic"),
        ("control-flow", "syntactic"),
        ("references", "resolved-binding"),
        ("calls", "resolved-callee"),
        ("types", "checked"),
        ("reachability", "from-resolved-calls"),
        ("unresolved-edge", "observed"),
    ]:
        if (rel, rung) in resolved_rungs:
            _sc, sid, cov, cid = mint_cov(
                rel, rung, symbol_subj, state="complete", attempted=True, exhaustive=True, stageTerminal="complete"
            )
        else:
            # RC-1: non-resolved registered rungs are not-applicable, attempted=false
            _sc, sid, cov, cid = mint_cov(rel, rung, symbol_subj)
        extra_scopes.append(sid)
        extra_cov.append((cov, cid))

    view_facts = order.cset(file_ids + [fid_pkg, fid_c0, fid_c1, fid_imp, fid_imp_r])
    view_cov = order.cset([cid_f, cid_c, cid_c_u, cid_i, cid_ir, cid_p] + [c[1] for c in extra_cov])
    view_scopes = order.cset([scid_file, scid_cl, scid_cl_u, scid_im, scid_im_r, scid_pk] + extra_scopes)
    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": view_scopes,
        "facts": view_facts,
        "coverageIds": view_cov,
        "producerClosure": provider_id,
        "schemaDigests": order.cset([builder.REL_DIGEST, builder.NAT_DIGEST]),
    }
    view_id = st.put_canonical_record("view", view)

    stage_spec = {
        "schemaVersion": 2,
        "planId": plan_id,
        "producerClosure": provider_id,
        "operation": "analyze",
        "parameters": [],
        "outputDomains": order.cset(["view"]),
        "outputSchemaDigest": builder.NAT_DIGEST,
    }
    ss_d = raw_c(stage_spec)
    st.put_raw_digest_record(stage_spec)
    exec_plan = {
        "schemaVersion": 2,
        "planId": plan_id,
        "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": order.cset(["view"])}],
    }
    exec_plan_id = st.put_canonical_record("execution-plan", exec_plan)

    # expected inventories
    inventories = []
    inv_digests_by_cell = {}
    file_rows = _file_rows(file_extent)
    pkg_rows = _package_rows()
    sym_rows = _symbol_rows(detector_id)
    for i, cell in enumerate(cells):
        kinds = list(cell.get("kinds") or [])
        digs = []
        for kind in kinds:
            if kind == "file":
                rec, d = _inventory(st, plan_id, ep_d, i, 0, "file", file_extent, file_rows)
            elif kind == "package":
                rec, d = _inventory(st, plan_id, ep_d, i, 0, "package", package_extent, pkg_rows)
            else:
                rec, d = _inventory(st, plan_id, ep_d, i, 0, "symbol", symbol_extent, sym_rows)
            inventories.append((rec, d))
            digs.append(d)
        inv_digests_by_cell[i] = digs

    # independently derived file subjects from file inventories
    from . import pilot_checks
    subjects_meta = pilot_checks.derive_subjects_from_inventories(
        policy_rule=policy["rules"][0],
        inventories=[r for r, _ in inventories],
        enum_plan=enum_plan,
        universe_hex=uhex,
        scope_doc=scope_doc,
        st=st,
    )
    subjects = []
    for s in subjects_meta:
        sid = st.put_canonical_record("evaluation-subject", s["descriptor"])
        assert sid == s["id"]
        subjects.append(s)

    attr = {
        "schemaVersion": 2,
        "planId": plan_id,
        "sourceFactId": fid_imp_r,
        "producerClosure": provider_id,
        "targetUniverse": uhex,
        "targetNativeId": "package:left-pad",
        "kind": "package",
        "occupancy": "external",
        "exported": None,
        "logicalPath": None,
        "packageManifestPath": "node_modules/left-pad/package.json",
        "evaluationNativeId": None,
    }
    attr_d = raw_c(attr)
    st.put_raw_digest_record(attr)

    # candidate envelopes
    cand_refs = []
    cand_by_cell = {}
    for i, cell in enumerate(cells):
        cap_id = cell["capabilityId"]
        if cap_id in ("clones-near", "clones-cross-tsjs"):
            _rec, d = _candidate_envelope(st, plan_id, exec_plan_id, i, cap_id, uhex, provider_id, candidate_paths)
            cand_by_cell[i] = d
            cand_refs.append({"domain": "candidate-producer-result", "digest": d})

    # coverage id by (relation, resolution)
    cov_index = {
        ("file", "enumerated"): [h.suffix(cid_f)],
        ("clones", "normalized-body-hash"): [h.suffix(cid_c), h.suffix(cid_c_u)],
        ("imports", "resolved-target"): [h.suffix(cid_ir)],
        ("package", "manifest-declared"): [h.suffix(cid_p)],
    }
    extra_pairs = [
        ("declares", "syntactic"),
        ("literal", "syntactic"),
        ("control-flow", "syntactic"),
        ("references", "resolved-binding"),
        ("calls", "resolved-callee"),
        ("types", "checked"),
        ("reachability", "from-resolved-calls"),
        ("unresolved-edge", "observed"),
    ]
    for (rel, rung), (_cov, cid) in zip(extra_pairs, extra_cov):
        cov_index[(rel, rung)] = [h.suffix(cid)]

    accounts = []
    outcomes = []
    for i, cell in enumerate(cells):
        cap_id = cell["capabilityId"]
        kinds = list(cell.get("kinds") or [])
        cand_d = cand_by_cell.get(i)
        clones_partial = cap_id == "clones-fact"
        outcomes.append(
            {
                "ordinal": i,
                "cellOrdinal": i,
                "programOrdinal": 0,
                "capabilityId": cap_id,
                "languageMode": "ts-tsconfig",
                "workspaceRoot": ".",
                "required": True,
                "kinds": order.cset(kinds),
                "universe": uhex,
                "enumeratorStatus": "selected",
                "enumeratorClosure": provider_id,
                "state": "partial" if clones_partial else "complete",
                "deficiency": "language-tier-unsupported" if clones_partial else None,
                "nativeCause": "capability-missing" if clones_partial else None,
                "stageOrdinal": 0,
                "stageOrdinalNullReason": None,
                "inventoryDigests": order.cset(inv_digests_by_cell.get(i) or []),
                "viewDigests": [h.suffix(view_id)],
                "candidateResultDigest": cand_d,
            }
        )
        for rel, rung in MATRIX_RELATIONS[cap_id]:
            if rel == "vcs-change":
                accounts.append(
                    {
                        "cellOrdinal": i,
                        "programOrdinal": 0,
                        "relation": rel,
                        "resolution": rung,
                        "sourceUniverse": uhex,
                        "targetUniverse": uhex,
                        "applicability": "inapplicable-vcs",
                        "coverageIds": [],
                    }
                )
            else:
                ids = cov_index[(rel, rung)]
                if isinstance(ids, str):
                    ids = [ids]
                accounts.append(
                    {
                        "cellOrdinal": i,
                        "programOrdinal": 0,
                        "relation": rel,
                        "resolution": rung,
                        "sourceUniverse": uhex,
                        "targetUniverse": uhex,
                        "applicability": "supported-available",
                        "coverageIds": order.cset(ids),
                    }
                )

    host_derived = (
        [{"domain": "subject-inventory", "digest": d} for _, d in inventories]
        + cand_refs
        + [{"domain": "target-attribution", "digest": attr_d}]
    )
    selected_refs = order.cset(
        [{"domain": "view", "digest": h.suffix(view_id)}]
        + [{"domain": "coverage", "digest": h.suffix(cid)} for cid in view_cov]
        + [{"domain": "import", "digest": h.suffix(imp_id)}]
        + host_derived
    )
    ei = {
        "schemaVersion": 1,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evaluatorClosure": evaluator_id,
        "enumerationPlanDigest": ep_d,
        "analysisSpecDigest": spec_d,
        "hostCapture": {
            "custody": "host-tcb-evidence-store",
            "observation": "stage-return",
            "stageReceipts": [
                {
                    "ordinal": 0,
                    "stageSpecDigest": ss_d,
                    "producerClosure": provider_id,
                    "outputDomains": order.cset(["view"]),
                    "outputRefs": order.cset([{"domain": "view", "digest": h.suffix(view_id)}]),
                    "state": "complete",
                    "unavailableReason": None,
                }
            ],
            "hostDerivedRefs": order.cset(host_derived),
        },
        "selectedRefs": selected_refs,
        "cellOutcomes": outcomes,
        "nativeCoverageAccounts": accounts,
        "candidateResultRefs": order.cset([r["digest"] for r in cand_refs]),
        "_inventoryRefs": [
            {"domain": "subject-inventory", "digest": d}
            for rec, d in inventories
            if rec.get("kind") == "file"
        ],
    }
    st.put_raw_digest_record({k: v for k, v in ei.items() if not k.startswith("_")})

    facts = list(file_facts) + [f_pkg, f_c0, f_c1, f_imp, f_imp_r]
    coverages = [cov_f, cov_c, cov_i, cov_ir, cov_p] + [c[0] for c in extra_cov]
    g = runs.seal_graph(
        st,
        name="ts",
        pid=pid,
        snap=snap,
        snap_id=snap_id,
        plan=plan,
        plan_id=plan_id,
        view=view,
        view_id=view_id,
        facts=facts,
        coverages=coverages,
        scopes=list(view_scopes),
        policy=policy,
        subjects=subjects,
        evaluator_id=evaluator_id,
        detector_id=detector_id,
        exec_plan=exec_plan,
        exec_plan_id=exec_plan_id,
        ei=ei,
    )
    # policy-derivation3 from composition §9.7
    pd = {
        "schemaVersion": 3,
        "planId": plan_id,
        "proofBundleId": g["proofId"],
        "policyDigest": pol_d,
        "waiverDigest": wav_d,
        "verdict": g["objects"]["proof"]["verdict"],
    }
    st.put_canonical_record("policy-derivation", pd)
    g["properties"] = {
        "nodeModules": True,
        "bareSpecifier": "left-pad",
        "configGraph": cfg_graph,
        "scopeDocument": True,
        "importedPayload": True,
        "clonesL0L1": True,
        "fileFacts": True,
        "nonemptyContext": True,
        "language": "typescript",
        "fileSubjectsFromInventory": [s["path"] for s in subjects],
    }
    return g
