"""Author-assisted example construction; incomplete until exact frozen full replay passes."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from . import builder, canonical, cap_admit, clone_body, evaluator, h, native_v2, order, store

KIT = Path(os.environ.get("OPENSIP_AUTHOR_KIT",
                          "/tmp/opensip-design-corrections/consumer-b.v13/subject"))
OUT = Path(os.environ.get("OPENSIP_AUTHOR_OUT",
                          "/tmp/opensip-design-corrections/codex-author-followup.v1/output"))
PLATFORM = "macos-aarch64"
# S1 (native-v2): stage operations a constructor substitutes for a builder's own ("author-synthetic-analysis" in the
# normalized/Rust-selection finalizers) must also be registered by the provider closure the builder mints. A constructor
# sets this list BEFORE calling a builder; builders register their own operation explicitly.
EXTRA_STAGE_OUTPUTS: list = []


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def selected_enumerator(closure_id: str) -> dict:
    """enumeration-plan.schema.v1.json#/$defs/SelectedEnumeratorRef."""
    return {"status": "selected", "closureId": closure_id}


def raw_c(obj: Any) -> str:
    return hashlib.sha256(canonical.encode(obj)).hexdigest()


def put_blob(st: store.Store, data: bytes) -> str:
    return st.put_blob(data)


def lib_d_ts() -> bytes:
    return b"export const ES2022: unique symbol;\n"


def make_stdlib_closure(st: store.Store) -> tuple[str, str, bytes]:
    dts = lib_d_ts()
    files = {"lib.es2022.d.ts": dts}
    rec, ident, blobs = builder.make_closure("stdlib", PLATFORM, files, version="5.4.5", protocol_major=0)
    st.put_canonical_record("closure", rec)
    for p, b in files.items():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:stdlib"])
    suffix = h.suffix(ident)
    return ident, suffix, dts


def make_toolchain_closure(st: store.Store, kind_files: dict[str, bytes], kind="toolchain") -> str:
    rec, ident, blobs = builder.make_closure(kind, PLATFORM, kind_files, version="1.78.0" if "bin/rustc" in kind_files else "5.4.5", protocol_major=2)
    st.put_canonical_record("closure", rec)
    for b in kind_files.values():
        st.put_blob(b)
    st.put_blob(blobs[f"_manifest:{kind}"])
    return ident


def make_provider_closure(st: store.Store, name: str, protocol_major: int, stage_outputs=()) -> str:
    files = {f"bin/{name}": b"provider-binary-" + name.encode()}
    # S1: the producer interface registers each stage operation's output schema document as a tree member.
    files.update(native_v2.stage_output_members(list(stage_outputs) + list(EXTRA_STAGE_OUTPUTS)))
    rec, ident, blobs = builder.make_closure("provider", PLATFORM, files, version="1.0.0", protocol_major=protocol_major)
    st.put_canonical_record("closure", rec)
    for b in files.values():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:provider"])
    return ident


def make_evaluator_closure(st: store.Store) -> str:
    files = {"bin/evaluator": b"evaluator-binary"}
    rec, ident, blobs = builder.make_closure("evaluator", PLATFORM, files, version="3.0.0", protocol_major=3)
    st.put_canonical_record("closure", rec)
    for b in files.values():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:evaluator"])
    return ident


def make_detector_closure(st: store.Store) -> str:
    files = {"bin/detector": b"detector-binary"}
    rec, ident, blobs = builder.make_closure("detector", PLATFORM, files, version="1.0.0", protocol_major=3)
    st.put_canonical_record("closure", rec)
    for b in files.values():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:detector"])
    return ident


def make_grammar_closure(st: store.Store, level_specs=None) -> str:
    files = {"bundle-manifest": b"grammar-bundle-manifest"}
    for grammar in ["json", "markdown", "typescript"]:
        files["grammars/"+grammar+".json"] = json.dumps({"grammar":grammar}).encode()
        files["normalizers/"+grammar] = b"normalizer-spec-" + grammar.encode()
    if level_specs:
        # S2: this grammar closure interprets syntax-only clone bodies, so it publishes the per-level map and specs.
        files.update(native_v2.normalization_members("opensip-clone-normalizer", level_specs))
    rec, ident, blobs = builder.make_closure("grammar", PLATFORM, files, version="1.0.0", protocol_major=1)
    st.put_canonical_record("closure", rec)
    for b in files.values():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:grammar"])
    return ident


def make_adapter_closure(st: store.Store) -> str:
    files = {"bin/adapter": b"adapter-binary"}
    rec, ident, blobs = builder.make_closure("adapter", PLATFORM, files, version="1.0.0", protocol_major=1)
    st.put_canonical_record("closure", rec)
    for b in files.values():
        st.put_blob(b)
    st.put_blob(blobs["_manifest:adapter"])
    return ident


def snapshot_from_files(st: store.Store, files: dict[str, bytes], pid: str, cfg_digest: str, scope_digest: str) -> tuple[dict, str, list[dict]]:
    inv = [builder.blob_row(p, b) for p, b in sorted(files.items())]
    for p, b in files.items():
        st.put_blob(b)
    inv_digest = raw_c(inv)
    st.objects[inv_digest] = inv
    st.blobs[inv_digest] = canonical.encode(inv)
    vcs = {
        "schemaVersion": 2,
        "kind": "none",
        "commitId": None,
        "dirty": False,
        "sourceInventoryDigest": inv_digest,
    }
    vcs_d = raw_c(vcs)
    st.put_raw_digest_record(vcs)
    snap = {
        "schemaVersion": 2,
        "projectId": pid,
        "sourceInventory": inv,
        "resolvedConfigDigest": cfg_digest,
        "scopeDigest": scope_digest,
        "vcsDigest": vcs_d,
    }
    sid = st.put_canonical_record("snapshot", snap)
    return snap, sid, inv


def body_lang_ts(ctx: dict, variant: str, language_id: str) -> dict:
    return {
        "schemaVersion": 1,
        "languageId": language_id,
        "compilerName": ctx["toolchain"]["compilerName"],
        "compilerVersion": ctx["toolchain"]["compilerVersion"],
        "compilerBuild": ctx["toolchain"]["compilerPackageDigest"],
        "dialect": {"sourceVariant": variant},
    }


def body_lang_rust(ctx: dict, edition: int) -> dict:
    return {
        "schemaVersion": 1,
        "languageId": "rust",
        "compilerName": "rustc",
        "compilerVersion": ctx["toolchain"]["rustcVersion"],
        "compilerBuild": ctx["toolchain"]["rustCommitHash"],
        "dialect": {"edition": edition},
    }


def body_lang_syntax(ctx: dict, variant: str, language_id: str) -> dict:
    gb = ctx["grammarBundle"]
    dialect_key = "grammarVariant"
    return {
        "schemaVersion": 1,
        "languageId": language_id,
        "compilerName": gb["parserName"],
        "compilerVersion": gb["parserVersion"],
        "compilerBuild": gb["bundleDigest"],
        "dialect": {dialect_key: variant},
    }


def mint_clone(st: store.Store, *, level: str, body: bytes, lang_rec: dict, lang_id: str, spec_bytes: bytes, anchor: dict) -> tuple[dict, str, str]:
    lv = hashlib.sha256(spec_bytes).digest()
    st.put_blob(spec_bytes)
    langv = clone_body.language_version_raw32(lang_rec)
    if level == "L0-verbatim":
        payload = clone_body.l0_payload(body)
    else:
        # independently chosen token stream (not an oracle): one ident token
        payload = clone_body.token_stream([("ident", body.strip()[:16] or b"x")])
    frame, bid = clone_body.framed_body_identity(
        level_id=level,
        level_version_raw32=lv,
        language_id=lang_id,
        language_version_raw32=langv,
        payload=payload,
    )
    st.put_blob(frame)
    payload_obj = {
        "bodyIdentity": bid,
        "normalisationLevel": level,
        "normalisationVersion": sha(spec_bytes),
    }
    return payload_obj, bid, sha(frame)


def file_payload(path: str, data: bytes) -> dict:
    return {"path": path, "contentSha256": sha(data), "byteLength": len(data)}


def coverage_payload(relation, resolution, uhex, scope_commit, count, **kw) -> dict:
    cov = "complete" if kw.get("coverage", "complete") == "complete" else kw.get("coverage")
    return {
        "schemaVersion": 3,
        "key": {
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": uhex,
            "targetUniverse": uhex,
            "subjectScopeCommitment": scope_commit,
        },
        "entry": {
            "relation": relation,
            "resolution": resolution,
            "coverage": cov,
            "examinedUniverse": {"subjectScopeCommitment": scope_commit, "subjectCount": count},
            "resolutionCompleteness": {
                "state": kw.get("state", "not-applicable"),
                "attempted": kw.get("attempted", False),
                "examinedExhaustive": kw.get("exhaustive", cov == "complete"),
                "stageTerminal": kw.get("stageTerminal", "complete" if cov == "complete" else "unavailable"),
                "unresolvedEdgeCount": 0,
                "unresolvedEdgeClasses": [],
            },
            "closedWorld": builder.closed_world_inapplicable(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": kw.get("deficiency"),
            "nativeCause": kw.get("nativeCause"),
        },
    }


def make_fact(st, snap_id, relation, resolution, uhex, producer, payload, anchors, payload_schema=builder.REL_DIGEST) -> tuple[dict, str]:
    pd = raw_c(payload)
    st.put_raw_digest_record(payload)
    rec = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "relation": relation,
        "resolution": resolution,
        "sourceUniverse": uhex,
        "targetUniverse": uhex,
        "producerClosure": producer,
        "payloadSchemaDigest": payload_schema,
        "payloadDigest": pd,
        "anchors": anchors,
        "confidenceMillionths": 1000000,
        "_payload": payload,
    }
    clean = {k: v for k, v in rec.items() if not k.startswith("_")}
    fid = st.put_canonical_record("fact", clean)
    rec["id"] = fid
    return rec, fid


def make_scope(st, snap_id, relation, resolution, uhex, enumerator, subjects) -> tuple[dict, str, str]:
    rec = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "sourceUniverse": uhex,
        "targetUniverse": uhex,
        "relation": relation,
        "resolution": resolution,
        "enumeratorClosure": enumerator,
        "subjects": order.cset(subjects),
    }
    sid = st.put_canonical_record("subject-scope", rec)
    commit = "sha256:" + h.suffix(sid)
    return rec, sid, commit


def make_coverage(st, scope_id, payload) -> tuple[dict, str]:
    pd = raw_c(payload)
    st.put_raw_digest_record(payload)
    rec = {
        "schemaVersion": 2,
        "scopeId": scope_id,
        "payloadSchemaDigest": builder.NAT_DIGEST,
        "payloadDigest": pd,
        "_payload": payload,
    }
    clean = {k: v for k, v in rec.items() if not k.startswith("_")}
    # Producer-boundary CoverageResultV3 admission before coverage2 exists.
    # Retained-byte recheck is the same function at structural_admit.
    from . import closure as _closure
    prod_errs = _closure.admit_coverage_result_v3(st, f"producer:{scope_id}", rec, payload)
    if prod_errs:
        raise ValueError("native.coverage-bijection-mismatch:" + " | ".join(prod_errs))
    cid = st.put_canonical_record("coverage", clean)
    rec["id"] = cid
    return rec, cid


def workspace_unit(root, family, mode, kind, marker_path, marker_sha, ordinal=0):
    return {
        "unitOrdinal": ordinal,
        "rootPath": root,
        "languageFamily": family,
        "languageMode": mode,
        "unitKind": kind,
        "markerPath": marker_path,
        "markerSha256": marker_sha,
        "recognizerId": "opensip.unit-recognizer",
        "recognizerVersion": 1,
        "provenance": "DISCOVERED",
        "memberPackageRoots": [],
    }


CELL_KINDS = {
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


def requested_cap_rows(caps, mode, root=".") -> list[dict]:
    rows = [
        {"capabilityId": c, "languageMode": mode, "workspaceRoot": root, "required": True}
        for c in caps
    ]
    return order.cset(rows)


def membership_rows_generic(paths: list[str], *, code_suffixes: tuple[str, ...], code_family: str, syntax_only: bool = False) -> list[dict]:
    rows = []
    for p in paths:
        is_code = p.endswith(code_suffixes)
        if syntax_only:
            rows.append(
                {
                    "path": p,
                    "languageFamily": code_family if is_code else "none",
                    "unitOrdinal": None,
                    "membership": "syntax-only",
                    "reason": "grammar-only",
                }
            )
        elif is_code:
            rows.append(
                {
                    "path": p,
                    "languageFamily": code_family,
                    "unitOrdinal": 0,
                    "membership": "program-member",
                    "reason": "deepest-unit-in-language",
                }
            )
        else:
            rows.append(
                {
                    "path": p,
                    "languageFamily": "none",
                    "unitOrdinal": None,
                    "membership": "syntax-only",
                    "reason": "grammar-only",
                }
            )
    return rows


def membership_rows_for_ts_files(paths: list[str]) -> list[dict]:
    """U-4: exactly one FileMembershipRowV1 per inventoried path."""
    rows = []
    for p in paths:
        if p.endswith(".ts") or p.endswith(".tsx") or p.endswith(".mts") or p.endswith(".cts"):
            rows.append(
                {
                    "path": p,
                    "languageFamily": "tsjs",
                    "unitOrdinal": 0,
                    "membership": "program-member",
                    "reason": "deepest-unit-in-language",
                }
            )
        else:
            rows.append(
                {
                    "path": p,
                    "languageFamily": "none",
                    "unitOrdinal": None,
                    "membership": "syntax-only",
                    "reason": "grammar-only",
                }
            )
    return rows


def enum_cells_for_caps(caps, mode, provider_id, ctx_hex, uhex, program_entry, candidate_paths) -> list[dict]:
    cells = []
    for cap in caps:
        binding = {
            "ordinal": 0,
            "provenance": "default-unit",
            "enumerator": selected_enumerator(provider_id),
            "nativeContextDigest": ctx_hex,
            "universe": uhex,
            "programEntry": program_entry,
            "extents": [],
        }
        if cap in ("clones-near", "clones-cross-tsjs"):
            binding["candidateSourcePaths"] = order.cset(list(candidate_paths))
        cells.append(
            {
                "capabilityId": cap,
                "languageMode": mode,
                "workspaceRoot": ".",
                "required": True,
                "kinds": order.cset(list(CELL_KINDS.get(cap) or [])),
                "programBindings": [binding],
            }
        )
    cells.sort(key=lambda c: (c["capabilityId"].encode("utf-8"), c["languageMode"].encode("utf-8"), c["workspaceRoot"].encode("utf-8")))
    return cells


def rustflags():
    return {"executableSelected": False, "honored": [], "stripped": []}


def unit_id(marker_path, target_kind, target_name) -> str:
    rec = {
        "schemaVersion": 1,
        "markerPath": marker_path,
        "targetKind": target_kind,
        "targetName": target_name,
    }
    return h.native_sha256_text("native.compilation-unit.v1", rec)


def seal_graph(st: store.Store, *, name, pid, snap, snap_id, plan, plan_id, view, view_id, facts, coverages, scopes, policy, subjects, evaluator_id, detector_id, exec_plan, exec_plan_id, ei, extra_objects=None):
    st.put_blob(builder.REL_BYTES)
    st.put_blob(builder.NAT_BYTES)
    st.put_blob(builder.POL_V2_BYTES)
    st.put_blob(builder.POL_V1_BYTES)
    st.put_blob(builder.IMP_BYTES)
    st.put_blob(builder.ENUM_PLAN_BYTES)
    st.put_blob(builder.EMIT_PLAN_BYTES)
    st.put_blob(builder.ATTR_V2_BYTES)

    fact_ids = [f["id"] for f in facts]
    cov_ids = [c["id"] for c in coverages]
    scope_ids = [s for s in scopes]
    replay = evaluator.compose_proof(
        {
            "policy": policy,
            "planId": plan_id,
            "executionPlanId": exec_plan_id,
            "evaluatorClosure": evaluator_id,
            "executionInputs": ei,
            "facts": facts,
            "factIds": fact_ids,
            "coverages": coverages,
            "coverageIds": cov_ids,
            "subjects": subjects,
            "detectorClosure": detector_id,
            "scopeIds": scope_ids,
            "inventoryRefs": ei.get("_inventoryRefs") or [],
        }
    )
    proof = replay["proof"]
    # retain witnesses, program-predicate records, and predicate node fragments
    for wdig, w in replay["witnesses"].items():
        st.put_raw_digest_record(w)
    for _d, rec in (replay.get("programPredicates") or {}).items():
        st.put_raw_digest_record(rec)
    for _d, node in (replay.get("predicateNodes") or {}).items():
        st.put_raw_digest_record(node)
    finding_ids = []
    for finding in replay["findings"]:
        fp = finding.pop("_fingerprintObject")
        params = finding.pop("_parameters")
        st.put_canonical_record("finding-fingerprint", fp)
        st.put_raw_digest_record(params)
        fid = st.put_canonical_record("finding", finding)
        finding_ids.append(fid)
    proof["findingIds"] = order.cset(finding_ids)
    # re-bind ruleResults finding ids already set
    proof_id = st.put_canonical_record("proof-bundle", proof)
    st.put_raw_digest_record(replay["program"])

    ei_cov = []
    for r in (ei.get("selectedRefs") or []):
        if r.get("domain") == "coverage":
            d = r["digest"]
            ei_cov.append(d if str(d).startswith("coverage2:") else "coverage2:" + d)
    view_cov = list(view.get("coverageIds") or [])
    evidence = {
        "schemaVersion": 3,
        "planId": plan_id,
        "viewIds": order.cset([view_id]),
        "coverageIds": order.cset(list(cov_ids) + view_cov + ei_cov),
        "importIds": order.cset(list(plan.get("importIds") or [])),
        "findingIds": proof["findingIds"],
        "proofBundleId": proof_id,
    }
    evid_id = st.put_canonical_record("semantic-evidence", evidence)
    seal = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evidenceId": evid_id,
        "evaluatorClosure": evaluator_id,
        "policyDigest": plan["policyDigest"],
        "proofBundleId": proof_id,
        "verdict": proof["verdict"],
    }
    seal_id = st.put_canonical_record("evaluation-seal", seal)
    run = {
        "schemaVersion": 3,
        "projectId": pid,
        "snapshotId": snap_id,
        "planId": plan_id,
        "evidenceId": evid_id,
        "evaluationSealId": seal_id,
        "capabilityManifestId": plan["capabilityManifestId"],
    }
    run_id = st.put_canonical_record("run", run)
    st.meta.update(
        {
            "name": name,
            "runId": run_id,
            "planId": plan_id,
            "proofId": proof_id,
            "outputMajors": {"run": "run3", "proof": "proof3", "seal": "seal3", "evidence": "evidence3"},
            "nativeIdentityMajors": {"snapshot": "snapshot2", "plan": "plan2", "fact": "fact2", "coverage": "coverage2", "view": "view2"},
        }
    )
    replay_export = {
        "runId": run_id,
        "derivedProof": proof,
        "claimedProof": proof,  # construction uses the derived bytes, not an independent claim
        "constructionProofSource": "frozen-reference derivation; independent replay is a separate check",
        "witnesses": replay["witnesses"],
        "findings": replay["findings"],
        "program": replay["program"],
        "executionInputsDigest": replay["executionInputsDigest"],
        "inputs": {
            "policy": policy,
            "subjects": subjects,
            "factIds": fact_ids,
            "coverageIds": cov_ids,
        },
    }
    return {
        "store": st,
        "runId": run_id,
        "planId": plan_id,
        "proofId": proof_id,
        "replay": replay_export,
        "objects": {
            "run": run,
            "seal": seal,
            "evidence": evidence,
            "proof": proof,
            "plan": plan,
            "snapshot": snap,
            "view": view,
        },
    }


def _analysis_spec(caps, scope_doc_schema_digest, scope_payload_digest, extra_params=None):
    params = []
    if scope_payload_digest:
        params.append({"schemaDigest": scope_doc_schema_digest, "payloadDigest": scope_payload_digest})
    if extra_params:
        params.extend(extra_params)
    return {
        "schemaVersion": 2,
        "requestedCapabilities": order.cset(caps),
        "policyPackIds": [],
        "parameters": order.cset(params),
    }


def build_ts_run() -> dict:
    from . import ts_pilot
    return ts_pilot.build_ts_run()


def build_ts_run_legacy_v2() -> dict:
    """Historical continuation.v2 constructor retained for failure evidence. Not used."""
    st = store.Store()
    pid = builder.project_id()
    # repository
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
        # node_modules is pruned from snapshot inventory by discovery; layout is a nested record with blobJoins
    }
    # retain node_modules package.json bytes for layout blobJoin even though not inventoried
    st.put_blob(lp_pkg)
    st.put_blob(lp_js)

    stdlib_id, stdlib_suffix, dts = make_stdlib_closure(st)
    tsc_bin = b"typescript-compiler"
    runtime_bin = b"node-runtime"
    tool_id = make_toolchain_closure(st, {"bin/tsc": tsc_bin, "bin/node": runtime_bin})
    provider_id = make_provider_closure(st, "ts-provider", 2)
    evaluator_id = make_evaluator_closure(st)
    detector_id = make_detector_closure(st)
    adapter_id = make_adapter_closure(st)

    default_caps = list(builder.TS_TSCONFIG_DEFAULT_CAPS)
    cfg = builder.semantic_config(default_caps)
    cfg_d = raw_c(cfg)
    st.put_raw_digest_record(cfg)
    sc = builder.scope_desc(["."])
    sc_d = raw_c(sc)
    st.put_raw_digest_record(sc)
    snap, snap_id, inv = snapshot_from_files(st, files, pid, cfg_d, sc_d)

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
            "configGraphPaths": sorted(
                ["tsconfig.json", "tsconfig.base.json"],
                key=lambda p: p.encode("utf-8"),
            ),
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
    ctx_id_text = h.native_sha256_text("native.context.typescript.v2", ctx)
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
        "nativeContextId": ctx_id_text,
    }
    uhex = h.native_bare_hex("native.semantic-universe.typescript.v2", uni)
    st.put_canonical_record("native.semantic-universe.typescript.v2", uni)

    # capability manifest
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

    inv_paths = sorted(files.keys(), key=lambda p: p.encode("utf-8"))
    membership = {
        "schemaVersion": 1,
        "units": [
            workspace_unit(".", "tsjs", "ts-tsconfig", "ts-program", "tsconfig.json", sha(tscfg), 0)
        ],
        "rows": membership_rows_for_ts_files(inv_paths),
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }
    mem_d = raw_c(membership)
    st.put_raw_digest_record(membership)

    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": enum_cells_for_caps(
            default_caps,
            "ts-tsconfig",
            provider_id,
            ctx_hex,
            uhex,
            "tsconfig.json",
            ["src/index.ts"],
        ),
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

    spec = _analysis_spec(
        requested_cap_rows(default_caps, "ts-tsconfig"),
        builder.POL_V1_DIGEST,
        scope_doc_d,
        extra_params=[
            {"schemaDigest": builder.ENUM_PLAN_DIGEST, "payloadDigest": ep_d},
            {"schemaDigest": builder.EMIT_PLAN_DIGEST, "payloadDigest": em_d},
        ],
    )
    spec_d = raw_c(spec)
    st.put_raw_digest_record(spec)

    # import2 runtime
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
    # selection/revisionRange may not allow None - try
    try:
        canonical.encode(obs)
    except Exception:
        pass
    obs_d = raw_c(obs)
    st.put_raw_digest_record(obs)
    imp = {
        "schemaVersion": 2,
        "kind": "runtime",
        "payloadSchemaDigest": builder.IMP_DIGEST,
        "payloadDigest": rp_d,
        "sourceCorrespondenceDigest": corr_d,
        "buildDigest": build_d,
        "producerClosure": adapter_id,
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

    # facts — file@enumerated is total over the snapshot inventory
    file_facts = []
    file_ids = []
    for p, data in sorted(files.items(), key=lambda kv: kv[0].encode("utf-8")):
        ff, fid = make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, file_payload(p, data), [])
        file_facts.append(ff)
        file_ids.append(fid)
    f_file, fid_file = file_facts[inv_paths.index("src/index.ts")], file_ids[inv_paths.index("src/index.ts")]
    f_pkg, fid_pkg = make_fact(st, snap_id, "package", "manifest-declared", uhex, provider_id, {"packageName": "demo", "packageVersion": "0.0.0", "manifestPath": "package.json"}, [])
    spec_l0 = b"level-spec-L0-verbatim-ts"
    spec_l1 = b"level-spec-L1-lexical-ts"
    lang_rec = body_lang_ts(ctx, "ts", "typescript")
    cl0, _, _ = mint_clone(st, level="L0-verbatim", body=src, lang_rec=lang_rec, lang_id="typescript", spec_bytes=spec_l0, anchor=None)
    cl1, _, _ = mint_clone(st, level="L1-lexical", body=src, lang_rec=lang_rec, lang_id="typescript", spec_bytes=spec_l1, anchor=None)
    anchor = {"path": "src/index.ts", "blobDigest": sha(src), "startByte": 0, "endByte": len(src)}
    f_c0, fid_c0 = make_fact(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, cl0, [anchor])
    f_c1, fid_c1 = make_fact(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, cl1, [anchor])
    f_imp, fid_imp = make_fact(
        st,
        snap_id,
        "imports",
        "syntactic-specifier",
        uhex,
        provider_id,
        {"importer": "symbol:src/index.ts::x", "specifier": "left-pad"},
        [anchor],
    )
    f_imp_r, fid_imp_r = make_fact(
        st,
        snap_id,
        "imports",
        "resolved-target",
        uhex,
        provider_id,
        {
            "importer": "symbol:src/index.ts::x",
            "specifier": "left-pad",
            "resolvedTarget": "package:left-pad",
        },
        [anchor],
    )

    sc_file, scid_file, scc_file = make_scope(st, snap_id, "file", "enumerated", uhex, provider_id, inv_paths)
    sc_cl, scid_cl, scc_cl = make_scope(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, ["src/index.ts"])
    sc_im, scid_im, scc_im = make_scope(st, snap_id, "imports", "syntactic-specifier", uhex, provider_id, ["symbol:src/index.ts::x"])
    sc_im_r, scid_im_r, scc_im_r = make_scope(st, snap_id, "imports", "resolved-target", uhex, provider_id, ["symbol:src/index.ts::x"])
    sc_pk, scid_pk, scc_pk = make_scope(st, snap_id, "package", "manifest-declared", uhex, provider_id, ["demo"])

    cp_file = coverage_payload("file", "enumerated", uhex, scc_file, len(inv_paths))
    cp_cl = coverage_payload("clones", "normalized-body-hash", uhex, scc_cl, 1)
    cp_im = coverage_payload("imports", "syntactic-specifier", uhex, scc_im, 1, state="not-applicable")
    cp_im_r = coverage_payload(
        "imports",
        "resolved-target",
        uhex,
        scc_im_r,
        1,
        state="complete",
        attempted=True,
        exhaustive=True,
        stageTerminal="complete",
    )
    cp_pk = coverage_payload("package", "manifest-declared", uhex, scc_pk, 1)
    cov_f, cid_f = make_coverage(st, scid_file, cp_file)
    cov_c, cid_c = make_coverage(st, scid_cl, cp_cl)
    cov_i, cid_i = make_coverage(st, scid_im, cp_im)
    cov_ir, cid_ir = make_coverage(st, scid_im_r, cp_im_r)
    cov_p, cid_p = make_coverage(st, scid_pk, cp_pk)

    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": order.cset([scid_file, scid_cl, scid_im, scid_im_r, scid_pk]),
        "facts": order.cset(file_ids + [fid_pkg, fid_c0, fid_c1, fid_imp, fid_imp_r]),
        "coverageIds": order.cset([cid_f, cid_c, cid_i, cid_ir, cid_p]),
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
        "outputDomains": order.cset(["view", "coverage", "fact"]),
        "outputSchemaDigest": builder.NAT_DIGEST,
    }
    ss_d = raw_c(stage_spec)
    st.put_raw_digest_record(stage_spec)
    exec_plan = {
        "schemaVersion": 2,
        "planId": plan_id,
        "stages": [
            {"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": order.cset(["coverage", "fact", "view"])}
        ],
    }
    exec_plan_id = st.put_canonical_record("execution-plan", exec_plan)

    subj = {
        "schemaVersion": 3,
        "universe": uhex,
        "kind": "file",
        "nativeSubjectId": "src/index.ts",
    }
    subj_id = st.put_canonical_record("evaluation-subject", subj)

    inv_row = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": "0" * 64,  # filled after enum plan
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": ["src/index.ts"],
        "rows": [
            {
                "nativeSubjectId": "src/index.ts",
                "kind": "file",
                "path": "src/index.ts",
                "qualifiedName": "src/index.ts",
                "subjectLanguage": "typescript",
                "signatureTokens": [],
                "projections": [],
            }
        ],
    }

    inv_row["parameterDigest"] = ep_d
    inv_row["examinedPaths"] = inv_paths
    inv_row["rows"] = [
        {
            "nativeSubjectId": p,
            "kind": "file",
            "path": p,
            "qualifiedName": p,
            "subjectLanguage": (
                "typescript"
                if p.endswith((".ts", ".tsx", ".mts", ".cts"))
                else "json"
                if p.endswith(".json")
                else "unspecified"
            ),
            "signatureTokens": [],
            "projections": [],
        }
        for p in inv_paths
    ]
    inv_d = raw_c(inv_row)
    st.put_raw_digest_record(inv_row)

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

    selected_refs = order.cset(
        [
            {"domain": "view", "digest": h.suffix(view_id)},
            {"domain": "coverage", "digest": h.suffix(cid_f)},
            {"domain": "coverage", "digest": h.suffix(cid_c)},
            {"domain": "coverage", "digest": h.suffix(cid_i)},
            {"domain": "coverage", "digest": h.suffix(cid_ir)},
            {"domain": "coverage", "digest": h.suffix(cid_p)},
            {"domain": "import", "digest": h.suffix(imp_id)},
            {"domain": "subject-inventory", "digest": inv_d},
            {"domain": "target-attribution", "digest": attr_d},
        ]
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
                    "outputDomains": order.cset(["coverage", "fact", "view"]),
                    "outputRefs": order.cset(
                        [
                            {"domain": "view", "digest": h.suffix(view_id)},
                            {"domain": "coverage", "digest": h.suffix(cid_f)},
                        ]
                    ),
                    "state": "complete",
                    "unavailableReason": None,
                }
            ],
            "hostDerivedRefs": order.cset(
                [
                    {"domain": "subject-inventory", "digest": inv_d},
                    {"domain": "target-attribution", "digest": attr_d},
                ]
            ),
        },
        "selectedRefs": selected_refs,
        "cellOutcomes": [
            {
                "ordinal": 0,
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "capabilityId": "inventory",
                "languageMode": "ts-tsconfig",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file"],
                "universe": uhex,
                "enumeratorStatus": "selected",
                "enumeratorClosure": provider_id,
                "state": "complete",
                "deficiency": None,
                "nativeCause": None,
                "stageOrdinal": 0,
                "stageOrdinalNullReason": None,
                "inventoryDigests": [inv_d],
                "viewDigests": [h.suffix(view_id)],
                "candidateResultDigest": None,
            }
        ],
        "nativeCoverageAccounts": [
            {
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "relation": "file",
                "resolution": "enumerated",
                "sourceUniverse": uhex,
                "targetUniverse": uhex,
                "applicability": "supported-available",
                "coverageIds": [h.suffix(cid_f)],
            }
        ],
        "candidateResultRefs": [],
        "_inventoryRefs": [{"domain": "subject-inventory", "digest": inv_d}],
    }
    st.put_raw_digest_record({k: v for k, v in ei.items() if not k.startswith("_")})

    subjects = [{"id": subj_id, "path": "src/index.ts", "kind": "file", "language": "typescript", "universe": uhex}]
    facts = list(file_facts) + [f_pkg, f_c0, f_c1, f_imp, f_imp_r]
    coverages = [cov_f, cov_c, cov_i, cov_ir, cov_p]
    g = seal_graph(
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
        scopes=[scid_file, scid_cl, scid_im, scid_im_r, scid_pk],
        policy=policy,
        subjects=subjects,
        evaluator_id=evaluator_id,
        detector_id=detector_id,
        exec_plan=exec_plan,
        exec_plan_id=exec_plan_id,
        ei=ei,
    )
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
    }
    return g


def _empty_ei(plan_id, exec_plan_id, evaluator_id, spec_d, ep_d, provider_id, ss_d, view_id, uhex, mode, inv_d, cov_hexes, extra_refs=None):
    refs = [
        {"domain": "view", "digest": h.suffix(view_id)},
        {"domain": "subject-inventory", "digest": inv_d},
    ]
    for c in cov_hexes:
        refs.append({"domain": "coverage", "digest": c})
    if extra_refs:
        refs.extend(extra_refs)
    return {
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
                    "outputDomains": order.cset(["coverage", "fact", "view"]),
                    "outputRefs": order.cset([{"domain": "view", "digest": h.suffix(view_id)}]),
                    "state": "complete",
                    "unavailableReason": None,
                }
            ],
            "hostDerivedRefs": order.cset([{"domain": "subject-inventory", "digest": inv_d}]),
        },
        "selectedRefs": order.cset(refs),
        "cellOutcomes": [
            {
                "ordinal": 0,
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "capabilityId": "inventory",
                "languageMode": mode,
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file"],
                "universe": uhex,
                "enumeratorStatus": "selected",
                "enumeratorClosure": provider_id,
                "state": "complete",
                "deficiency": None,
                "nativeCause": None,
                "stageOrdinal": 0,
                "stageOrdinalNullReason": None,
                "inventoryDigests": [inv_d],
                "viewDigests": [h.suffix(view_id)],
                "candidateResultDigest": None,
            }
        ],
        "nativeCoverageAccounts": [
            {
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "relation": "file",
                "resolution": "enumerated",
                "sourceUniverse": uhex,
                "targetUniverse": None,  # S4: an account has no target coordinate
                "applicability": "supported-available",
                "coverageIds": cov_hexes[:1],
            }
        ],
        "candidateResultRefs": [],
        "_inventoryRefs": [{"domain": "subject-inventory", "digest": inv_d}],
    }


def build_rust_run() -> dict:
    st = store.Store()
    pid = builder.project_id()
    ws = b'[workspace]\nmembers=["crates/alpha","crates/foo#bar"]\n'
    alpha_toml = b'[package]\nname="alpha"\nedition="2018"\n[lib]\npath="src/lib.rs"\n[[bin]]\nname="alpha-bin"\npath="src/main.rs"\nedition="2021"\n'
    hash_toml = b'[package]\nname="hashy"\nedition="2021"\n'
    shared = b"pub fn shared() {}\n"
    lib_rs = b"mod shared;\npub fn libf() { shared::shared(); }\n"
    main_rs = b"mod shared;\nfn main() { shared::shared(); }\n"
    hashy_rs = b"pub fn h() {}\n"
    lock = b"# Cargo.lock version 3\n"
    cargo_cfg = b"[build]\ntarget = \"aarch64-apple-darwin\"\n"
    files = {
        "Cargo.toml": ws,
        "Cargo.lock": lock,
        "crates/alpha/Cargo.toml": alpha_toml,
        "crates/alpha/src/lib.rs": lib_rs,
        "crates/alpha/src/main.rs": main_rs,
        "crates/alpha/src/shared.rs": shared,
        "crates/foo#bar/Cargo.toml": hash_toml,
        "crates/foo#bar/src/lib.rs": hashy_rs,
        ".cargo/config.toml": cargo_cfg,
    }
    llvm_files = {"lib/LLVM": b"llvm-dev"}
    llvm_id = make_toolchain_closure(st, llvm_files, kind="rust-dev-llvm")
    llvm_suffix = h.suffix(llvm_id)
    rustc = b"rustc-bin"
    cargo = b"cargo-bin"
    pm = b"proc-macro-srv"
    spec_l0 = b"level-spec-L0-rust"
    # S2: the Rust toolchain closure interprets the clone body span, so it publishes the per-level map and the spec.
    tool_files = {"bin/rustc": rustc, "bin/cargo": cargo, "bin/pm": pm}
    tool_files.update(native_v2.normalization_members("opensip-clone-normalizer", {"L0-verbatim": spec_l0}))
    tool_id = make_toolchain_closure(st, tool_files, kind="toolchain")
    provider_id = make_provider_closure(st, "rust-provider", 3, stage_outputs=[("analyze", ["coverage", "fact", "view"])])
    evaluator_id = make_evaluator_closure(st)
    detector_id = make_detector_closure(st)

    cfg = builder.semantic_config(["inventory"])
    cfg_d = raw_c(cfg)
    st.put_raw_digest_record(cfg)
    sc = builder.scope_desc(["."])
    sc_d = raw_c(sc)
    st.put_raw_digest_record(sc)
    snap, snap_id, inv = snapshot_from_files(st, files, pid, cfg_d, sc_d)

    depset = {
        "schemaVersion": 1,
        "language": "rust",
        "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha(lock), "lockfileVersion": 3},
        "packages": [],
        "completeness": {"state": "complete", "missing": []},
    }
    dep_id = h.native_sha256_text("native.dependency-source-set.v1", depset)
    st.put_canonical_record("native.dependency-source-set.v1", depset)
    feats = {
        "schemaVersion": 1,
        "resolverVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "activated": [],
        "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "synthetic.1"},
    }
    feat_id = h.native_sha256_text("native.unified-features.rust.v1", feats)
    st.put_canonical_record("native.unified-features.rust.v1", feats)
    proj = {
        "schemaVersion": 2,
        "honoredKeys": [],
        "strippedKeys": [],
        "replacedSnapshotConfigs": [".cargo/config.toml"],
        "rustflags": rustflags(),
        "ancestorCarrierVerified": True,
        "cargoHome": "private-empty",
        "environmentProjection": "none",
        "claimsCargoSwitch": False,
        "projectionSha256": sha(cargo_cfg),
    }
    st.put_blob(cargo_cfg)

    ctx = {
        "schemaVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "a" * 40,
            "rustcVersion": "1.78.0",
            "cargoVersion": "1.78.0",
            "sysrootDigest": sha(b"sysroot"),
            "rustcDevLlvmDigest": llvm_suffix,
            "standardLibraryComponentDigests": [{"component": "core", "sha256": sha(b"core")}],
            "targetTriple": "aarch64-apple-darwin",
        },
        "toolClosure": {
            "rustc": sha(rustc),
            "cargo": sha(cargo),
            "linker": None,
            "ar": None,
            "procMacroServer": sha(pm),
            "closureId": tool_id,
        },
        "baseCfg": ["unix", "target_os=\"macos\""],
        "resolverVersion": 2,
        "dependencySourceSetId": dep_id,
        "unifiedFeaturesId": feat_id,
        "preparedOutputSetId": None,
        "configProjection": proj,
    }
    st.put_blob(b"sysroot")
    st.put_blob(b"core")
    ctx_hex = h.native_bare_hex("native.context.rust.v2", ctx)
    ctx_text = h.native_sha256_text("native.context.rust.v2", ctx)
    st.put_canonical_record("native.context.rust.v2", ctx)

    # large edition map: alpha 2018, hashy 2021, plus representative extras
    edition_map = {"alpha": 2018, "hashy": 2021}
    for i in range(8):
        edition_map[f"extra{i}"] = 2021 if i % 2 == 0 else 2018

    uid_lib = unit_id("crates/alpha/Cargo.toml", "lib", "alpha")
    uid_bin = unit_id("crates/alpha/Cargo.toml", "bin", "alpha-bin")
    uid_h = unit_id("crates/foo#bar/Cargo.toml", "lib", "hashy")

    def ownership(selected, enumeration="complete"):
        units = [
            {
                "unitId": uid_lib,
                "markerPath": "crates/alpha/Cargo.toml",
                "crateName": "alpha",
                "targetKind": "lib",
                "targetName": "alpha",
                "targetEdition": None,  # package default 2018
            },
            {
                "unitId": uid_bin,
                "markerPath": "crates/alpha/Cargo.toml",
                "crateName": "alpha",
                "targetKind": "bin",
                "targetName": "alpha-bin",
                "targetEdition": 2021,  # differs from package default
            },
            {
                "unitId": uid_h,
                "markerPath": "crates/foo#bar/Cargo.toml",
                "crateName": "hashy",
                "targetKind": "lib",
                "targetName": "hashy",
                "targetEdition": None,
            },
        ]
        own = [
            {"path": "crates/alpha/src/lib.rs", "unitId": uid_lib},
            {"path": "crates/alpha/src/shared.rs", "unitId": uid_lib},
            {"path": "crates/alpha/src/shared.rs", "unitId": uid_bin},
            {"path": "crates/alpha/src/main.rs", "unitId": uid_bin},
            {"path": "crates/foo#bar/src/lib.rs", "unitId": uid_h},
        ]
        units.sort(key=lambda u: u["unitId"].encode("utf-8"))
        own.sort(key=lambda r: (r["path"].encode("utf-8"), r["unitId"].encode("utf-8")))
        rec = {
            "schemaVersion": 1,
            "enumeration": enumeration,
            "units": units,
            "selectedUnitIds": sorted(selected, key=lambda s: s.encode("utf-8")),
            "ownership": own,
        }
        ident = h.native_sha256_text("native.source-unit-ownership.v1", rec)
        st.put_canonical_record("native.source-unit-ownership.v1", rec)
        return rec, ident

    own_lib, own_lib_id = ownership([uid_lib, uid_h])
    own_bin, own_bin_id = ownership([uid_bin, uid_h])
    # selection change without dialect change: lib-only vs lib+hashy still 2018 for shared.rs under lib
    own_lib_only, own_lib_only_id = ownership([uid_lib])

    def rust_uni(own_id):
        rec = {
            "schemaVersion": 2,
            "edition": edition_map,
            "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha(lock), "lockfileVersion": 3},
            "dependencySourceSetId": dep_id,
            "unifiedFeaturesId": feat_id,
            "nativeContextId": ctx_text,
            "cfgSets": [{"cfgSetId": "default", "cfg": ctx["baseCfg"]}],
            "rustflags": rustflags(),
            "crateRootPaths": ["crates/alpha/src/lib.rs", "crates/alpha/src/main.rs", "crates/foo#bar/src/lib.rs"],
            "configProjectionSha256": h.suffix(h.native_sha256_text("native.cargo-config-projection.v2", proj))
            if False
            else h.native_bare_hex("native.cargo-config-projection.v2", proj),
            "executionCapableResolution": False,
            "preparedOutputSetId": None,
            "preparedResolution": "none",
            "sourceUnitOwnershipId": own_id,
        }
        st.put_canonical_record("native.cargo-config-projection.v2", proj)
        hx = h.native_bare_hex("native.semantic-universe.rust.v2", rec)
        st.put_canonical_record("native.semantic-universe.rust.v2", rec)
        return rec, hx

    uni_lib, u_lib = rust_uni(own_lib_id)
    uni_bin, u_bin = rust_uni(own_bin_id)
    uni_lib2, u_lib2 = rust_uni(own_lib_only_id)

    cap = builder.minimal_cap_manifest("core", [builder.rust_provider_cap()], [])
    cap["providers"][0]["platformIds"] = sorted(cap["providers"][0]["platformIds"])
    cap_adm = cap_admit.admit(cap)
    st.put_blob(bytes.fromhex(cap_adm["committedBytesHex"]))
    policy = builder.build_policy("file.exists", "rust", "file", builder.file_exists_atom())
    pol_d = raw_c(policy)
    st.put_raw_digest_record(policy)
    wav_d = raw_c(builder.build_waivers())
    st.put_raw_digest_record(builder.build_waivers())
    grant = builder.grant(pid, sc_d, [provider_id, evaluator_id, detector_id], ["read-source", "native-analysis"])
    grant_d = raw_c(grant)
    st.put_raw_digest_record(grant)
    rust_paths = sorted(files.keys(), key=lambda p: p.encode("utf-8"))
    # U-4b: the Cargo workspace unit folds its member packages; rows follow the first-match decision.
    membership = native_v2.membership(
        [native_v2.unit("", "rust", "rust-cargo", "cargo-workspace", "Cargo.toml", sha(ws), recognizer_id="cargo-workspace",
                        member_package_roots=["crates/alpha", "crates/foo#bar"])],
        rust_paths)
    mem_d = raw_c(membership)
    st.put_raw_digest_record(membership)
    rust_caps = ["inventory"]
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": enum_cells_for_caps(rust_caps, "rust-cargo", provider_id, ctx_hex, u_lib, None, []),
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
    spec = _analysis_spec(
        requested_cap_rows(rust_caps, "rust-cargo"),
        None,
        None,
        extra_params=[
            {"schemaDigest": builder.ENUM_PLAN_DIGEST, "payloadDigest": ep_d},
            {"schemaDigest": builder.EMIT_PLAN_DIGEST, "payloadDigest": em_d},
        ],
    )
    spec_d = raw_c(spec)
    st.put_raw_digest_record(spec)
    plan = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "capabilityManifestId": cap_adm["capabilityManifestId"],
        "semanticClosures": order.cset([provider_id, evaluator_id, detector_id, tool_id, llvm_id]),
        "analysisSpecDigest": spec_d,
        "resolvedConfigDigest": cfg_d,
        "nativeContextDigests": order.cset([ctx_hex]),
        "importIds": [],
        "policyDigest": pol_d,
        "waiverDigest": wav_d,
        "scopeDigest": sc_d,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_d,
        "capabilityManifestBytesDigest": cap_adm["committedBytesDigest"],
    }
    plan_id = st.put_canonical_record("plan", plan)

    facts = []
    coverages = []
    scopes = []
    for path, data, uhex in [
        ("crates/alpha/src/lib.rs", lib_rs, u_lib),
        ("crates/alpha/src/shared.rs", shared, u_lib),
        ("crates/alpha/src/shared.rs", shared, u_bin),
        ("crates/alpha/src/main.rs", main_rs, u_bin),
        ("crates/foo#bar/src/lib.rs", hashy_rs, u_lib),
    ]:
        f, fid = make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, file_payload(path, data), [])
        facts.append(f)
        scp, scid, scc = make_scope(st, snap_id, "file", "enumerated", uhex, provider_id, [path])
        scopes.append(scid)
        cp = coverage_payload("file", "enumerated", uhex, scc, 1)
        cov, cid = make_coverage(st, scid, cp)
        coverages.append(cov)

    have_file_paths = {f.get("_payload", {}).get("path") for f in facts if f.get("relation") == "file"}
    for path, data in sorted(files.items(), key=lambda kv: kv[0].encode("utf-8")):
        if path in have_file_paths:
            continue
        f, fid = make_fact(st, snap_id, "file", "enumerated", u_lib, provider_id, file_payload(path, data), [])
        facts.append(f)

    # clones at two editions of shared.rs
    lang_2018 = body_lang_rust(ctx, 2018)
    lang_2021 = body_lang_rust(ctx, 2021)
    cl_a, bid_a, _ = mint_clone(st, level="L0-verbatim", body=shared, lang_rec=lang_2018, lang_id="rust", spec_bytes=spec_l0, anchor=None)
    cl_b, bid_b, _ = mint_clone(st, level="L0-verbatim", body=shared, lang_rec=lang_2021, lang_id="rust", spec_bytes=spec_l0, anchor=None)
    # stable body when ownership selection changes without dialect change (lib vs lib-only, both 2018)
    cl_c, bid_c, _ = mint_clone(st, level="L0-verbatim", body=shared, lang_rec=lang_2018, lang_id="rust", spec_bytes=spec_l0, anchor=None)
    anc = {"path": "crates/alpha/src/shared.rs", "blobDigest": sha(shared), "startByte": 0, "endByte": len(shared)}
    fca, ida = make_fact(st, snap_id, "clones", "normalized-body-hash", u_lib, provider_id, cl_a, [anc])
    fcb, idb = make_fact(st, snap_id, "clones", "normalized-body-hash", u_bin, provider_id, cl_b, [anc])
    fcc, idc = make_fact(st, snap_id, "clones", "normalized-body-hash", u_lib2, provider_id, cl_c, [anc])
    facts.extend([fca, fcb, fcc])
    st.meta["stableBodyPair"] = {"libSelection": bid_a, "libOnlySelection": bid_c, "equal": bid_a == bid_c, "twoEditionsDiffer": bid_a != bid_b}
    st.meta["editionMap"] = edition_map
    st.meta["targetEditionDiffers"] = {"packageDefault": 2018, "binTargetEdition": 2021}
    st.meta["hashMarker"] = "crates/foo#bar/Cargo.toml"
    st.meta["versionComponent"] = {
        "compilerVersion": ctx["toolchain"]["rustcVersion"],
        "compilerBuild": ctx["toolchain"]["rustCommitHash"],
        "derivedRecord": lang_2018,
        "raw32": clone_body.language_version_raw32(lang_2018).hex(),
    }

    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": order.cset(scopes),
        "facts": order.cset([f["id"] for f in facts]),
        "coverageIds": order.cset([c["id"] for c in coverages]),
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
        "outputDomains": order.cset(["coverage", "fact", "view"]),
        "outputSchemaDigest": native_v2.stage_output_schema_digest("analyze", ["coverage", "fact", "view"]),  # S1
    }
    ss_d = raw_c(stage_spec)
    st.put_raw_digest_record(stage_spec)
    exec_plan = {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": order.cset(["coverage", "fact", "view"])}]}
    exec_plan_id = st.put_canonical_record("execution-plan", exec_plan)
    subj = {"schemaVersion": 3, "universe": u_lib, "kind": "file", "nativeSubjectId": "crates/alpha/src/lib.rs"}
    subj_id = st.put_canonical_record("evaluation-subject", subj)
    inv_row = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": "0" * 64,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": ["crates/alpha/src/lib.rs"],
        "rows": [
            {
                "nativeSubjectId": "crates/alpha/src/lib.rs",
                "kind": "file",
                "path": "crates/alpha/src/lib.rs",
                "qualifiedName": "crates/alpha/src/lib.rs",
                "subjectLanguage": "rust",
                "signatureTokens": [],
                "projections": [],
            }
        ],
    }
    # membership + enum_plan already retained before Plan; bind inventory parameterDigest
    enum_plan = {  # noqa: F841 — ep_d already computed
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": [
            {
                "capabilityId": "inventory",
                "languageMode": "rust-cargo",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file"],
                "programBindings": [
                    {
                        "ordinal": 0,
                        "provenance": "default-unit",
                        "enumerator": selected_enumerator(provider_id),
                        "nativeContextDigest": ctx_hex,
                        "universe": u_lib,
                        "programEntry": None,
                        "extents": [],
                    }
                ],
            }
        ],
    }
    ep_d = raw_c(enum_plan)
    st.put_raw_digest_record(enum_plan)
    inv_row["parameterDigest"] = ep_d
    inv_d = raw_c(inv_row)
    st.put_raw_digest_record(inv_row)
    ei = _empty_ei(plan_id, exec_plan_id, evaluator_id, spec_d, ep_d, provider_id, ss_d, view_id, u_lib, "rust-cargo", inv_d, [h.suffix(coverages[0]["id"])])
    st.put_raw_digest_record({k: v for k, v in ei.items() if not k.startswith("_")})
    subjects = [{"id": subj_id, "path": "crates/alpha/src/lib.rs", "kind": "file", "language": "rust", "universe": u_lib}]
    g = seal_graph(st, name="rust", pid=pid, snap=snap, snap_id=snap_id, plan=plan, plan_id=plan_id, view=view, view_id=view_id, facts=facts, coverages=coverages, scopes=scopes, policy=policy, subjects=subjects, evaluator_id=evaluator_id, detector_id=detector_id, exec_plan=exec_plan, exec_plan_id=exec_plan_id, ei=ei)
    g["properties"] = {
        "mixedEdition": True,
        "targetEditionDiffers": True,
        "sameFileTwoEditions": True,
        "hashMarker": True,
        "largeEditionMap": edition_map,
        "stableBody": st.meta["stableBodyPair"],
        "versionComponent": st.meta["versionComponent"],
        "nonemptyContext": True,
        "language": "rust",
    }
    return g


def build_rust_partial() -> dict:
    """Partial enumeration, empty clone view, no complete Coverage from partial ownership."""
    # Author: partial fixture does not depend on constructing an unused full Run.
    # independent partial graph: clone coverage unknown + nativeCause
    st = store.Store()
    pid = builder.project_id()
    src = b"pub fn x() {}\n"
    toml = b'[package]\nname="p"\nedition="2021"\n'
    files = {"Cargo.toml": toml, "src/lib.rs": src, "Cargo.lock": b"# lock\n"}
    llvm_id = make_toolchain_closure(st, {"lib/LLVM": b"llvm"}, kind="rust-dev-llvm")
    tool_id = make_toolchain_closure(st, {"bin/rustc": b"rustc", "bin/cargo": b"cargo", "bin/pm": b"pm"})
    provider_id = make_provider_closure(st, "rust-provider", 3, stage_outputs=[("analyze", ["coverage", "fact", "view"])])
    evaluator_id = make_evaluator_closure(st)
    detector_id = make_detector_closure(st)
    cfg = builder.semantic_config(["clones-fact"])
    cfg_d = raw_c(cfg)
    st.put_raw_digest_record(cfg)
    sc = builder.scope_desc(["."])
    sc_d = raw_c(sc)
    st.put_raw_digest_record(sc)
    snap, snap_id, inv = snapshot_from_files(st, files, pid, cfg_d, sc_d)
    # reuse a minimal rust context/universe with partial ownership
    depset = {
        "schemaVersion": 1,
        "language": "rust",
        "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha(files["Cargo.lock"]), "lockfileVersion": 3},
        "packages": [],
        "completeness": {"state": "complete", "missing": []},
    }
    dep_id = h.native_sha256_text("native.dependency-source-set.v1", depset)
    st.put_canonical_record("native.dependency-source-set.v1", depset)
    feats = {
        "schemaVersion": 1,
        "resolverVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "activated": [],
        "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "synthetic.1"},
    }
    feat_id = h.native_sha256_text("native.unified-features.rust.v1", feats)
    st.put_canonical_record("native.unified-features.rust.v1", feats)
    proj = {
        "schemaVersion": 2,
        "honoredKeys": [],
        "strippedKeys": [],
        "replacedSnapshotConfigs": [],
        "rustflags": rustflags(),
        "ancestorCarrierVerified": True,
        "cargoHome": "private-empty",
        "environmentProjection": "none",
        "claimsCargoSwitch": False,
        "projectionSha256": sha(b""),
    }
    st.put_blob(b"")
    ctx = {
        "schemaVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "b" * 40,
            "rustcVersion": "1.78.0",
            "cargoVersion": "1.78.0",
            "sysrootDigest": sha(b"sysroot2"),
            "rustcDevLlvmDigest": h.suffix(llvm_id),
            "standardLibraryComponentDigests": [{"component": "core", "sha256": sha(b"core2")}],
            "targetTriple": "aarch64-apple-darwin",
        },
        "toolClosure": {
            "rustc": sha(b"rustc"),
            "cargo": sha(b"cargo"),
            "linker": None,
            "ar": None,
            "procMacroServer": sha(b"pm"),
            "closureId": tool_id,
        },
        "baseCfg": [],
        "resolverVersion": 2,
        "dependencySourceSetId": dep_id,
        "unifiedFeaturesId": feat_id,
        "preparedOutputSetId": None,
        "configProjection": proj,
    }
    st.put_blob(b"sysroot2")
    st.put_blob(b"core2")
    ctx_hex = h.native_bare_hex("native.context.rust.v2", ctx)
    ctx_text = h.native_sha256_text("native.context.rust.v2", ctx)
    st.put_canonical_record("native.context.rust.v2", ctx)
    uid = unit_id("Cargo.toml", "lib", "p")
    own = {
        "schemaVersion": 1,
        "enumeration": "partial",
        "units": [
            {
                "unitId": uid,
                "markerPath": "Cargo.toml",
                "crateName": "p",
                "targetKind": "lib",
                "targetName": "p",
                "targetEdition": None,
            }
        ],
        "selectedUnitIds": [uid],
        "ownership": [],  # empty clone view / no body rows
    }
    own_id = h.native_sha256_text("native.source-unit-ownership.v1", own)
    st.put_canonical_record("native.source-unit-ownership.v1", own)
    uni = {
        "schemaVersion": 2,
        "edition": {"p": 2021},
        "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha(files["Cargo.lock"]), "lockfileVersion": 3},
        "dependencySourceSetId": dep_id,
        "unifiedFeaturesId": feat_id,
        "nativeContextId": ctx_text,
        "cfgSets": [{"cfgSetId": "default", "cfg": []}],
        "rustflags": rustflags(),
        "crateRootPaths": ["src/lib.rs"],
        "configProjectionSha256": h.native_bare_hex("native.cargo-config-projection.v2", proj),
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
        "preparedResolution": "none",
        "sourceUnitOwnershipId": own_id,
    }
    st.put_canonical_record("native.cargo-config-projection.v2", proj)
    uhex = h.native_bare_hex("native.semantic-universe.rust.v2", uni)
    st.put_canonical_record("native.semantic-universe.rust.v2", uni)
    cap = builder.minimal_cap_manifest("core", [builder.rust_provider_cap()], [])
    cap["providers"][0]["platformIds"] = sorted(cap["providers"][0]["platformIds"])
    cap_adm = cap_admit.admit(cap)
    st.put_blob(bytes.fromhex(cap_adm["committedBytesHex"]))
    policy = builder.build_policy("clones.none", "rust", "file", builder.none_clones_atom())
    pol_d = raw_c(policy)
    st.put_raw_digest_record(policy)
    wav_d = raw_c(builder.build_waivers())
    st.put_raw_digest_record(builder.build_waivers())
    grant = builder.grant(pid, sc_d, [provider_id, evaluator_id, detector_id], ["read-source", "native-analysis"])
    grant_d = raw_c(grant)
    st.put_raw_digest_record(grant)
    rpp = sorted(files.keys(), key=lambda p: p.encode("utf-8"))
    membership = native_v2.membership(
        [native_v2.unit("", "rust", "rust-cargo", "cargo-package", "Cargo.toml", sha(files["Cargo.toml"]), recognizer_id="cargo-package")],
        rpp)
    mem_d = raw_c(membership)
    st.put_raw_digest_record(membership)
    rust_caps = ["clones-fact"]
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": enum_cells_for_caps(rust_caps, "rust-cargo", provider_id, ctx_hex, uhex, None, []),
    }
    ep_d = raw_c(enum_plan)
    st.put_raw_digest_record(enum_plan)
    emission = {
        "schemaVersion": 1,
        "policyDigest": pol_d,
        "rules": [
            {
                "ruleId": "clones.none",
                "contributionId": "contrib.clones-none.v1",
                "ruleStableId": "clones.none",
                "semanticsMajor": 1,
                "detectorClosure": detector_id,
                "stabilityClass": "path-stable",
                "emissionProfile": "declarative-subject-v1",
            }
        ],
    }
    em_d = raw_c(emission)
    st.put_raw_digest_record(emission)
    spec = _analysis_spec(
        requested_cap_rows(rust_caps, "rust-cargo"),
        None,
        None,
        extra_params=[
            {"schemaDigest": builder.ENUM_PLAN_DIGEST, "payloadDigest": ep_d},
            {"schemaDigest": builder.EMIT_PLAN_DIGEST, "payloadDigest": em_d},
        ],
    )
    spec_d = raw_c(spec)
    st.put_raw_digest_record(spec)
    plan = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "capabilityManifestId": cap_adm["capabilityManifestId"],
        "semanticClosures": order.cset([provider_id, evaluator_id, detector_id, tool_id, llvm_id]),
        "analysisSpecDigest": spec_d,
        "resolvedConfigDigest": cfg_d,
        "nativeContextDigests": order.cset([ctx_hex]),
        "importIds": [],
        "policyDigest": pol_d,
        "waiverDigest": wav_d,
        "scopeDigest": sc_d,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_d,
        "capabilityManifestBytesDigest": cap_adm["committedBytesDigest"],
    }
    plan_id = st.put_canonical_record("plan", plan)
    f_file, fid = make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, file_payload("src/lib.rs", src), [])
    extra_files = []
    for pth, data in files.items():
        if pth == "src/lib.rs":
            continue
        ff, _fid = make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, file_payload(pth, data), [])
        extra_files.append(ff)
    scp, scid, scc = make_scope(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, ["src/lib.rs"])
    cp = coverage_payload(
        "clones",
        "normalized-body-hash",
        uhex,
        scc,
        1,
        coverage="unknown",
        deficiency="input-closure-incomplete",
        nativeCause="body-language-owner-unenumerated",
        exhaustive=False,
        state="not-applicable",
        stageTerminal="unavailable",
    )
    cov, cid = make_coverage(st, scid, cp)
    scf, scidf, sccf = make_scope(st, snap_id, "file", "enumerated", uhex, provider_id, rpp)
    covf, cidf = make_coverage(st, scidf, coverage_payload("file", "enumerated", uhex, sccf, len(rpp)))
    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": order.cset([scid, scidf]),
        "facts": order.cset([fid] + [ef["id"] for ef in extra_files]),
        "coverageIds": order.cset([cid, cidf]),
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
        "outputDomains": order.cset(["coverage", "fact", "view"]),
        "outputSchemaDigest": native_v2.stage_output_schema_digest("analyze", ["coverage", "fact", "view"]),  # S1
    }
    ss_d = raw_c(stage_spec)
    st.put_raw_digest_record(stage_spec)
    exec_plan = {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": order.cset(["coverage", "fact", "view"])}]}
    exec_plan_id = st.put_canonical_record("execution-plan", exec_plan)
    subj = {"schemaVersion": 3, "universe": uhex, "kind": "file", "nativeSubjectId": "src/lib.rs"}
    subj_id = st.put_canonical_record("evaluation-subject", subj)
    inv_row = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": "0" * 64,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": ["src/lib.rs"],
        "rows": [
            {
                "nativeSubjectId": "src/lib.rs",
                "kind": "file",
                "path": "src/lib.rs",
                "qualifiedName": "src/lib.rs",
                "subjectLanguage": "rust",
                "signatureTokens": [],
                "projections": [],
            }
        ],
    }
    membership = native_v2.membership(  # already retained before Plan; do not replace with empty rows
        [native_v2.unit("", "rust", "rust-cargo", "cargo-package", "Cargo.toml", sha(toml), recognizer_id="cargo-package")],
        sorted(files.keys(), key=lambda p: p.encode("utf-8")))
    # mem_d already bound into enum_plan; keep equal bytes
    assert raw_c(membership) == mem_d
    st.put_raw_digest_record(membership)
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": [
            {
                "capabilityId": "clones-fact",
                "languageMode": "rust-cargo",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file"],
                "programBindings": [
                    {
                        "ordinal": 0,
                        "provenance": "default-unit",
                        "enumerator": selected_enumerator(provider_id),
                        "nativeContextDigest": ctx_hex,
                        "universe": uhex,
                        "programEntry": None,
                        "extents": [],
                    }
                ],
            }
        ],
    }
    ep_d = raw_c(enum_plan)
    st.put_raw_digest_record(enum_plan)
    inv_row["parameterDigest"] = ep_d
    inv_d = raw_c(inv_row)
    st.put_raw_digest_record(inv_row)
    ei = _empty_ei(plan_id, exec_plan_id, evaluator_id, spec_d, ep_d, provider_id, ss_d, view_id, uhex, "rust-cargo", inv_d, [h.suffix(cid), h.suffix(cidf)])
    st.put_raw_digest_record({k: v for k, v in ei.items() if not k.startswith("_")})
    subjects = [{"id": subj_id, "path": "src/lib.rs", "kind": "file", "language": "rust", "universe": uhex}]
    g2 = seal_graph(st, name="rust-partial", pid=pid, snap=snap, snap_id=snap_id, plan=plan, plan_id=plan_id, view=view, view_id=view_id, facts=[f_file] + extra_files, coverages=[cov, covf], scopes=[scid, scidf], policy=policy, subjects=subjects, evaluator_id=evaluator_id, detector_id=detector_id, exec_plan=exec_plan, exec_plan_id=exec_plan_id, ei=ei)
    g2["properties"] = {
        "partialEnumeration": True,
        "emptyCloneView": True,
        "deficiency": "resolution-incomplete",
        "nativeCause": "body-language-owner-unenumerated",
        "coverage": "unknown",
        "notCompleteFromPartialOwnership": True,
    }
    return g2


def _syntax_bundle(st, grammar_id, language_id, suffixes, syntax_class, grammar_closure):
    gbytes = json.dumps({"grammar": grammar_id}).encode()
    st.put_blob(gbytes)
    spec = b"normalizer-spec-" + grammar_id.encode()
    st.put_blob(spec)
    bundle_manifest = b"grammar-bundle-manifest"
    st.put_blob(bundle_manifest)
    rec = {
        "schemaVersion": 1,
        "closureId": grammar_closure,
        "parserName": "opensip-grammar-parser",
        "parserVersion": "1.0.0",
        "bundleDigest": sha(bundle_manifest),
        "grammars": [
            {
                "grammarId": grammar_id,
                "grammarVersion": "1.0.0",
                "languageId": language_id,
                "suffixes": sorted(suffixes, key=lambda s: s.encode("utf-8")),
                "syntaxClass": syntax_class,
                "grammarDigest": sha(gbytes),
            }
        ],
        "normalizer": {
            "normalizerId": "opensip-clone-normalizer",
            "normalizerVersion": "1.0.0",
            "specificationDigest": sha(spec),
        },
    }
    return rec


def build_syntax_run(*, data_document: bool) -> dict:
    st = store.Store()
    pid = builder.project_id()
    syntax_spec_l0 = b"level-spec-L0-syntax-ts"
    # S2: the grammar closure interprets syntax-only clone bodies; it publishes the map when this Run mints bodies.
    gclos = make_grammar_closure(st, level_specs=None if data_document else {"L0-verbatim": syntax_spec_l0})
    provider_id = make_provider_closure(st, "syntax-provider", 1, stage_outputs=[("analyze", ["coverage", "fact", "view"])])
    evaluator_id = make_evaluator_closure(st)
    detector_id = make_detector_closure(st)
    if data_document:
        files = {"docs/note.md": b"# hello\n", "data/config.json": b'{"a":1}\n'}
        bundle = _syntax_bundle(st, "markdown", "markdown", [".md"], "data-document", gclos)
        # add json grammar
        gbytes = json.dumps({"grammar": "json"}).encode()
        st.put_blob(gbytes)
        bundle["grammars"].append(
            {
                "grammarId": "json",
                "grammarVersion": "1.0.0",
                "languageId": "json",
                "suffixes": [".json"],
                "syntaxClass": "data-document",
                "grammarDigest": sha(gbytes),
            }
        )
        bundle["grammars"] = sorted(bundle["grammars"], key=lambda g: g["grammarId"].encode())
        selected = ["json", "markdown"]
        path = "docs/note.md"
        body = files[path]
        lang_mode_caps = ["inventory"]
    else:
        files = {"src/util.ts": b"export function f(){ return 1; }\n"}
        bundle = _syntax_bundle(st, "typescript", "typescript", [".ts", ".tsx", ".mts", ".cts"], "code", gclos)
        selected = ["typescript"]
        path = "src/util.ts"
        body = files[path]
        lang_mode_caps = ["inventory", "syntax", "clones-fact"]
    ctx = {"schemaVersion": 2, "grammarBundle": bundle}
    ctx_hex = h.native_bare_hex("native.context.syntax.v2", ctx)
    ctx_text = h.native_sha256_text("native.context.syntax.v2", ctx)
    st.put_canonical_record("native.context.syntax.v2", ctx)
    uni = {
        "schemaVersion": 2,
        "nativeContextId": ctx_text,
        "selectedGrammarIds": sorted(selected),
        "resolutionAttempted": False,
    }
    uhex = h.native_bare_hex("native.semantic-universe.syntax.v2", uni)
    st.put_canonical_record("native.semantic-universe.syntax.v2", uni)
    cfg = builder.semantic_config(lang_mode_caps)
    cfg_d = raw_c(cfg)
    st.put_raw_digest_record(cfg)
    sc = builder.scope_desc(["."])
    sc_d = raw_c(sc)
    st.put_raw_digest_record(sc)
    snap, snap_id, inv = snapshot_from_files(st, files, pid, cfg_d, sc_d)
    cap = builder.minimal_cap_manifest("core", [builder.syntax_provider_cap()], [])
    cap["providers"][0]["platformIds"] = ["all-supported"]
    cap_adm = cap_admit.admit(cap)
    st.put_blob(bytes.fromhex(cap_adm["committedBytesHex"]))
    policy = builder.build_policy("file.exists", "syntax", "file", builder.file_exists_atom())
    pol_d = raw_c(policy)
    st.put_raw_digest_record(policy)
    wav_d = raw_c(builder.build_waivers())
    st.put_raw_digest_record(builder.build_waivers())
    grant = builder.grant(pid, sc_d, [provider_id, evaluator_id, detector_id, gclos], ["read-source", "native-analysis"])
    grant_d = raw_c(grant)
    st.put_raw_digest_record(grant)
    syn_paths = sorted(files.keys(), key=lambda p: p.encode("utf-8"))
    # U-9 + U-4b: a marker-free project has the single syntax-only fallback unit, which claims no row.
    membership = native_v2.membership([native_v2.syntax_only_fallback_unit()], syn_paths)
    mem_d = raw_c(membership)
    st.put_raw_digest_record(membership)
    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": snap_id,
        "scopeDigest": sc_d,
        "membershipDigest": mem_d,
        "cells": enum_cells_for_caps(lang_mode_caps, "syntax-only", provider_id, ctx_hex, uhex, None, [path] if "clones-fact" in lang_mode_caps else []),
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
    req = requested_cap_rows(lang_mode_caps, "syntax-only")
    spec = _analysis_spec(
        req,
        None,
        None,
        extra_params=[
            {"schemaDigest": builder.ENUM_PLAN_DIGEST, "payloadDigest": ep_d},
            {"schemaDigest": builder.EMIT_PLAN_DIGEST, "payloadDigest": em_d},
        ],
    )
    spec_d = raw_c(spec)
    st.put_raw_digest_record(spec)
    plan = {
        "schemaVersion": 2,
        "snapshotId": snap_id,
        "capabilityManifestId": cap_adm["capabilityManifestId"],
        "semanticClosures": order.cset([provider_id, evaluator_id, detector_id, gclos]),
        "analysisSpecDigest": spec_d,
        "resolvedConfigDigest": cfg_d,
        "nativeContextDigests": order.cset([ctx_hex]),
        "importIds": [],
        "policyDigest": pol_d,
        "waiverDigest": wav_d,
        "scopeDigest": sc_d,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_d,
        "capabilityManifestBytesDigest": cap_adm["committedBytesDigest"],
    }
    plan_id = st.put_canonical_record("plan", plan)
    facts = []
    coverages = []
    scopes = []
    for pth, data in files.items():
        f, fid = make_fact(st, snap_id, "file", "enumerated", uhex, provider_id, file_payload(pth, data), [])
        facts.append(f)
        scp, scid, scc = make_scope(st, snap_id, "file", "enumerated", uhex, provider_id, [pth])
        scopes.append(scid)
        cov, cid = make_coverage(st, scid, coverage_payload("file", "enumerated", uhex, scc, 1))
        coverages.append(cov)
    if not data_document:
        lang_rec = body_lang_syntax(ctx, "ts", "typescript")
        spec_l0 = syntax_spec_l0
        cl0, _, _ = mint_clone(st, level="L0-verbatim", body=body, lang_rec=lang_rec, lang_id="typescript", spec_bytes=spec_l0, anchor=None)
        anc = {"path": path, "blobDigest": sha(body), "startByte": 0, "endByte": len(body)}
        fc, fidc = make_fact(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, cl0, [anc])
        facts.append(fc)
        scp, scid, scc = make_scope(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, [path])
        scopes.append(scid)
        cov, cid = make_coverage(st, scid, coverage_payload("clones", "normalized-body-hash", uhex, scc, 1))
        coverages.append(cov)
        # syntax/declares
        fd, fidd = make_fact(
            st,
            snap_id,
            "declares",
            "syntactic",
            uhex,
            provider_id,
            {"container": "file:src/util.ts", "declared": "symbol:f", "declarationKind": "function"},
            [anc],
        )
        facts.append(fd)
    else:
        # explicit unavailability for clones/types
        scp, scid, scc = make_scope(st, snap_id, "clones", "normalized-body-hash", uhex, provider_id, [path])
        scopes.append(scid)
        cov, cid = make_coverage(
            st,
            scid,
            coverage_payload(
                "clones",
                "normalized-body-hash",
                uhex,
                scc,
                1,
                coverage="unknown",
                deficiency="language-tier-unsupported",
                nativeCause="capability-missing",
                exhaustive=True,
                stageTerminal="unavailable",
            ),
        )
        coverages.append(cov)
        st.meta["unsupported"] = {
            "clones": {"deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"},
            "types": "not requested; class does not support",
        }
    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": order.cset(scopes),
        "facts": order.cset([f["id"] for f in facts]),
        "coverageIds": order.cset([c["id"] for c in coverages]),
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
        "outputDomains": order.cset(["coverage", "fact", "view"]),
        "outputSchemaDigest": native_v2.stage_output_schema_digest("analyze", ["coverage", "fact", "view"]),  # S1
    }
    ss_d = raw_c(stage_spec)
    st.put_raw_digest_record(stage_spec)
    exec_plan = {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": order.cset(["coverage", "fact", "view"])}]}
    exec_plan_id = st.put_canonical_record("execution-plan", exec_plan)
    subj = {"schemaVersion": 3, "universe": uhex, "kind": "file", "nativeSubjectId": path}
    subj_id = st.put_canonical_record("evaluation-subject", subj)
    inv_row = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": "0" * 64,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sorted(files),
        "rows": [
            {
                "nativeSubjectId": pth,
                "kind": "file",
                "path": pth,
                "qualifiedName": pth,
                "subjectLanguage": "markdown" if data_document else "typescript",
                "signatureTokens": [],
                "projections": [],
            }
            for pth in sorted(files)
        ],
    }
    inv_row["parameterDigest"] = ep_d
    inv_d = raw_c(inv_row)
    st.put_raw_digest_record(inv_row)
    ei = _empty_ei(
        plan_id,
        exec_plan_id,
        evaluator_id,
        spec_d,
        ep_d,
        provider_id,
        ss_d,
        view_id,
        uhex,
        "syntax-only",
        inv_d,
        [h.suffix(c["id"]) for c in coverages],
    )
    st.put_raw_digest_record({k: v for k, v in ei.items() if not k.startswith("_")})
    subjects = [{"id": subj_id, "path": path, "kind": "file", "language": "markdown" if data_document else "typescript", "universe": uhex}]
    name = "syntax-data" if data_document else "syntax-code"
    g = seal_graph(st, name=name, pid=pid, snap=snap, snap_id=snap_id, plan=plan, plan_id=plan_id, view=view, view_id=view_id, facts=facts, coverages=coverages, scopes=scopes, policy=policy, subjects=subjects, evaluator_id=evaluator_id, detector_id=detector_id, exec_plan=exec_plan, exec_plan_id=exec_plan_id, ei=ei)
    g["properties"] = {
        "syntaxOnly": True,
        "dataDocument": data_document,
        "noCompilerUnit": True,
        "unsupported": st.meta.get("unsupported"),
        "language": "syntax",
        "fileFacts": True,
        "clones": not data_document,
    }
    return g

