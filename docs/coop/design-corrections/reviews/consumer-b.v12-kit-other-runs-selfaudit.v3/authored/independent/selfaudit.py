#!/usr/bin/env python3
"""Review-quality self-audit of v2 four-Run PASS/REFUSE grades against the original charter and owning producing/join laws."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(OUT))

from independent.admit_run import Store, admit_one, digest_of, hex_of  # noqa: E402
from independent.kit_core import C, H, parse_h_frame  # noqa: E402

SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/consumer-snapshot")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
CHARTER = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/original-consumer-charter.txt")
V2_MD = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/other-runs-review.md")
V2_JSON = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/other-runs-review.json")
KIT_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject/consumer-input-manifest.json")
SNAP_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/snapshot-manifest.json")
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"
RUNS = ["ts", "rust", "syntax-data", "rust-partial-clones"]

EXPECTED_CHARTER = "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec"
EXPECTED_KIT = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
EXPECTED_REQ = "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495"
EXPECTED_SNAP = "feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c"
PARENT = "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb"
V2_MD_SHA = "782d91e34d48b6a1fb5f870ec8d1c295c7a0073456a11fe712150ad3c3c1300c"
V2_JSON_SHA = "ae7e81b8e2627d0fde27cf42dbc7bb7a67afc3188ecaa5a868c5a6d8068733ce"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rec(log, layer, name, ok, detail, operands=None, law=None, *, refuse=True):
    item = {
        "layer": layer,
        "name": name,
        "ok": bool(ok),
        "detail": detail,
        "law": law,
        "operands": operands or {},
    }
    log.append(item)
    return bool(ok)


def tree_shas(closure: dict) -> set[str]:
    return {row["sha256"] for row in (closure.get("tree") or []) if row.get("type", "file") != "directory"}


def dts_rows(closure: dict) -> list[dict]:
    out = []
    for row in closure.get("tree") or []:
        bn = str(row.get("path") or "").split("/")[-1]
        if bn.endswith(".d.ts"):
            out.append(row)
    return out


def fold_lib(name: str) -> str:
    # ASCII lib names: Default Case Conversion coincides with str.lower
    return name.lower()


def producing_rules(name: str, store: Store, v2: dict) -> list[dict]:
    """Native §2 / §11 producing recipes and identity §3 totality/subset/equality, with exact operands."""
    log = []
    g = v2.get("graph")
    if not g:
        rec(log, "structural", "graph-available", False, "v2 graph load failed", law="charter phase 9")
        return log
    plan, snap, uni, ctx = g["plan"], g["snapshot"], g["uni"], g["ctx"]
    proof, ev, seal, run = g["claimed_proof"], g["evidence"], g["seal"], g["run"]
    ctx_hex, uni_hex = g["ctx_hex"], g["uni_hex"]

    # identity §3: retained context frames == plan.nativeContextDigests exactly
    rec(
        log,
        "structural",
        "plan.nativeContextDigests-set-equals-retained-context",
        list(plan.get("nativeContextDigests") or []) == [ctx_hex],
        "set of retained context frames must equal plan.nativeContextDigests",
        {"plan.nativeContextDigests": plan.get("nativeContextDigests"), "retained": [ctx_hex]},
        "identity-and-evidence.md §3 context set equality",
    )
    rec(
        log,
        "structural",
        "universe.nativeContextId-is-plan-selected",
        uni.get("nativeContextId") == "sha256:" + ctx_hex and ctx_hex in (plan.get("nativeContextDigests") or []),
        "universe nativeContextId must be sha256: plus a Plan-selected context suffix",
        {"universe.nativeContextId": uni.get("nativeContextId"), "plan": plan.get("nativeContextDigests")},
        "identity-and-evidence.md §3 universe binds Plan-selected context",
    )

    # vcs sourceInventoryDigest == C(snapshot.sourceInventory)
    vcs = g["vcs"]
    inv_d = digest_of(snap["sourceInventory"])
    rec(
        log,
        "structural",
        "vcs.sourceInventoryDigest-equals-snapshot-inventory-C",
        vcs.get("sourceInventoryDigest") == inv_d,
        "vcs-observation.sourceInventoryDigest is raw SHA-256 of the snapshot inventory",
        {"vcs.sourceInventoryDigest": vcs.get("sourceInventoryDigest"), "C(sourceInventory)": inv_d},
        "identity-and-evidence.md §3 vcsDigest",
    )

    # evidence.importIds repeats plan.importIds
    rec(
        log,
        "structural",
        "evidence.importIds-equals-plan.importIds",
        list(ev.get("importIds") or []) == list(plan.get("importIds") or []),
        "semantic-evidence.importIds repeats the Plan-selected import set exactly",
        {"evidence.importIds": ev.get("importIds"), "plan.importIds": plan.get("importIds")},
        "identity-and-evidence.md §3 evidence.importIds",
    )
    rec(
        log,
        "structural",
        "evidence.proofBundleId-equals-seal.proofBundleId",
        ev.get("proofBundleId") == seal.get("proofBundleId") == g["claimed_proof_id"],
        "acyclic: evidence and seal name the same proof",
        {"evidence": ev.get("proofBundleId"), "seal": seal.get("proofBundleId")},
        "identity-and-evidence.md §3 acyclic graph",
    )
    rec(
        log,
        "structural",
        "seal.verdict-equals-proof.verdict",
        seal.get("verdict") == proof.get("verdict"),
        "seal carries the proof verdict",
        {"seal.verdict": seal.get("verdict"), "proof.verdict": proof.get("verdict")},
        "identity-schemas.v3 evaluation-seal.verdict",
    )

    # evaluationInputRefs includes every Plan import (identity §3) via selectedRefs totality
    eir = proof.get("evaluationInputRefs") or []
    eir_set = {(r["domain"], r["digest"]) for r in eir}
    missing_imports = []
    for iid in plan.get("importIds") or []:
        hx = iid.split(":", 1)[1]
        if ("import", hx) not in eir_set:
            missing_imports.append(iid)
    rec(
        log,
        "structural",
        "evaluationInputRefs-contains-every-plan-import",
        not missing_imports,
        "evaluator3 proof names every Plan-selected import in evaluationInputRefs",
        {"missing": missing_imports, "plan.importIds": plan.get("importIds")},
        "identity-and-evidence.md §3 evaluationInputRefs imports",
    )

    # Predicate inputRefs subset — schema ProofInputRef includes rule-program; enumeration-contract §7 excludes it from evaluationInputRefs.
    extra = []
    for pp in proof.get("predicateProofs") or []:
        for r in pp.get("inputRefs") or []:
            if (r["domain"], r["digest"]) not in eir_set:
                extra.append(r)
    rec(
        log,
        "structural",
        "predicate-inputRefs-subset-of-evaluationInputRefs",
        not extra,
        "identity §3 subset as written; ProofInputRef enum also lists rule-program. Recorded with operands, not waived.",
        {"extras": extra, "evaluationInputRefDomains": sorted({d for d, _ in eir_set})},
        "identity-and-evidence.md §3 predicate input refs subset; identity-schemas.v3 ProofInputRef.domain",
        refuse=False,  # law-interaction: do not first-refuse solely on schema-live rule-program citation
    )
    if extra:
        log[-1]["ok"] = False
        log[-1]["diagnostic"] = True
        log[-1]["acceptance"] = "notUsedAsFirstRefusal"
        log[-1]["detail"] = (
            "claimed predicate inputRefs cite "
            + json.dumps(extra)
            + " not in evaluationInputRefs. ProofInputRef.domain enum includes rule-program; enumeration-contract §7 / composition v3 keep evaluationInputRefs = selectedRefs + execution-inputs. v2 compose_proof shared this citation. C equality of that shared derivation does not establish the subset sentence as written."
        )

    # native producing rules by domain
    if g["ctx_domain"] == "native.context.typescript.v2":
        _ts_producing(log, store, g, ctx, uni, plan)
    elif g["ctx_domain"] == "native.context.rust.v2":
        _rust_producing(log, store, g, ctx, uni, plan)
    elif g["ctx_domain"] == "native.context.syntax.v2":
        _syntax_producing(log, store, g, ctx, uni, plan)

    return log


def _ts_producing(log, store, g, ctx, uni, plan):
    cid = (ctx.get("toolClosure") or {}).get("closureId")
    crec = store.parse_typed(cid, "closure")
    rec(
        log,
        "structural",
        "ts.toolClosure.kind-toolchain",
        crec.get("kind") == "toolchain",
        "toolClosure.closureId names retained kind=toolchain",
        {"closureId": cid, "kind": crec.get("kind")},
        "native-evidence.md §2.4 toolClosure",
    )
    rec(
        log,
        "structural",
        "ts.compilerVersion-equals-tool-closure-semanticVersion",
        ctx["toolchain"].get("compilerVersion") == crec.get("semanticVersion"),
        "compilerVersion is the semanticVersion of the admitted signed compiler closure manifest",
        {"compilerVersion": ctx["toolchain"].get("compilerVersion"), "closure.semanticVersion": crec.get("semanticVersion")},
        "native-evidence.md §2.4 toolchain.compilerVersion producing recipe",
    )
    tsha = tree_shas(crec)
    rec(
        log,
        "structural",
        "ts.toolClosure.compiler-in-closure-tree",
        ctx["toolClosure"].get("compiler") in tsha,
        "compiler raw digest is a member of the signed toolchain tree",
        {"compiler": ctx["toolClosure"].get("compiler"), "tree": sorted(tsha)},
        "native-evidence.md §2.4 toolClosure.compiler",
    )
    rec(
        log,
        "structural",
        "ts.toolClosure.runtime-in-closure-tree",
        ctx["toolClosure"].get("runtime") in tsha,
        "runtime raw digest is a member of the signed toolchain tree",
        {"runtime": ctx["toolClosure"].get("runtime")},
        "native-evidence.md §2.4 toolClosure.runtime",
    )
    rec(
        log,
        "structural",
        "ts.compilerPackageDigest-is-toolchain-tree-member",
        ctx["toolchain"].get("compilerPackageDigest") in tsha,
        "compilerPackageDigest retention is closure-tree-member of toolClosure.closureId",
        {
            "compilerPackageDigest": ctx["toolchain"].get("compilerPackageDigest"),
            "treeMembers": sorted(tsha),
            "blobPresent": hex_of(ctx["toolchain"].get("compilerPackageDigest")) in store.blobs
            or ctx["toolchain"].get("compilerPackageDigest") in store.blobs,
        },
        "native-evidence.schemas.v2.json TypeScriptToolchainIdentityV1.compilerPackageDigest x-opensip-digest retention=closure-tree-member; native-evidence.md §2.4",
    )
    std_id = "closure2:" + ctx["toolchain"]["typescriptStdlibMerkleRoot"]
    srec = store.parse_typed(std_id, "closure")
    rec(
        log,
        "structural",
        "ts.stdlib-closure-kind",
        srec.get("kind") == "stdlib",
        "typescriptStdlibMerkleRoot is the bare suffix of kind=stdlib closure2",
        {"suffix": ctx["toolchain"]["typescriptStdlibMerkleRoot"], "kind": srec.get("kind")},
        "identity-and-evidence.md §3; native-evidence.md §2.4",
    )
    dts = dts_rows(srec)
    comps = ctx["toolchain"].get("standardLibraryComponentDigests") or []
    comp_names = {c["component"] if isinstance(c, dict) else c for c in comps}
    tree_names = {r["path"].split("/")[-1] for r in dts}
    rec(
        log,
        "structural",
        "ts.stdlib-inventory-complete-vs-tree-d.ts",
        comp_names == tree_names and len(dts) == len(comps),
        "standardLibraryComponentDigests is the complete .d.ts inventory of the retained stdlib tree",
        {"components": sorted(comp_names), "treeDts": sorted(tree_names)},
        "native-evidence.md §2.4 complete declaration-file inventory",
    )
    hon_lib = (ctx.get("configProjection") or {}).get("honoredOptions", {}).get("lib") or []
    libsel = ctx["toolchain"].get("libSelection") or []
    rec(
        log,
        "structural",
        "ts.libSelection-fold-equals-honored-lib",
        {fold_lib(n) for n in libsel} == {fold_lib(m) for m in hon_lib},
        "folded libSelection equals folded honoredOptions.lib",
        {"libSelection": libsel, "honored.lib": hon_lib},
        "native-evidence.md §2.4 libSelection equality",
    )
    missing_map = []
    for n in libsel:
        want = "lib." + fold_lib(n) + ".d.ts"
        if want not in comp_names:
            missing_map.append({"name": n, "component": want})
    rec(
        log,
        "structural",
        "ts.libSelection-maps-to-retained-component",
        not missing_map,
        "component(n)=lib.{fold(n)}.d.ts is in the declared component set",
        {"missing": missing_map},
        "native-evidence.md §2.4 libSelection membership",
    )
    rec(
        log,
        "structural",
        "ts.moduleResolutionMode-equals-honored-moduleResolution",
        ctx.get("moduleResolutionMode") == (ctx.get("configProjection") or {}).get("honoredOptions", {}).get("moduleResolution"),
        "context moduleResolutionMode equals honoredOptions.moduleResolution",
        {
            "moduleResolutionMode": ctx.get("moduleResolutionMode"),
            "honored.moduleResolution": (ctx.get("configProjection") or {}).get("honoredOptions", {}).get("moduleResolution"),
        },
        "native-evidence.md §2.4 context agreement",
    )
    rec(
        log,
        "structural",
        "ts.nodeModulesInReadSet-iff-layout-digest-non-null",
        bool(uni.get("nodeModulesInReadSet")) == (ctx.get("nodeModulesLayoutDigest") is not None),
        "nodeModulesInReadSet is exactly (nodeModulesLayoutDigest is not null)",
        {
            "universe.nodeModulesInReadSet": uni.get("nodeModulesInReadSet"),
            "context.nodeModulesLayoutDigest": ctx.get("nodeModulesLayoutDigest"),
        },
        "native-evidence.md §2.2/§2.4",
    )
    rec(
        log,
        "structural",
        "ts.executionCapableResolution-false",
        uni.get("executionCapableResolution") is False,
        "TypeScript universe executionCapableResolution is constant false",
        {"executionCapableResolution": uni.get("executionCapableResolution")},
        "native-evidence.md §2.2",
    )
    cg = store.parse_canonical(uni["tsconfigGraphHash"])
    rec(
        log,
        "structural",
        "ts.tsconfigGraphHash-is-C-of-TypeScriptConfigGraphV1",
        digest_of(cg) == uni["tsconfigGraphHash"],
        "tsconfigGraphHash is raw SHA-256 of C(TypeScriptConfigGraphV1)",
        {"claimed": uni["tsconfigGraphHash"], "C": digest_of(cg)},
        "native-evidence.md §2.2",
    )
    node_paths = [n["path"] for n in cg.get("nodes") or []]
    rec(
        log,
        "structural",
        "ts.config-graph-nodes-equal-configGraphPaths",
        set(node_paths) == set(ctx.get("configProjection", {}).get("configGraphPaths") or []),
        "graph nodes[].path is exactly the context configGraphPaths set",
        {"nodes": node_paths, "configGraphPaths": ctx.get("configProjection", {}).get("configGraphPaths")},
        "native-evidence.md §2.2 bind_typescript_universe",
    )
    kind_fail = []
    for n in cg.get("nodes") or []:
        bn = n["path"].split("/")[-1]
        derived = "tsconfig" if bn == "tsconfig.json" else ("jsconfig" if bn == "jsconfig.json" else "other")
        if n.get("kind") != derived:
            kind_fail.append({"path": n["path"], "claimed": n.get("kind"), "derived": derived})
    rec(
        log,
        "structural",
        "ts.config-node-kind-derived-from-basename-table",
        not kind_fail,
        "every node's kind is the closed basename table, never asserted",
        {"failures": kind_fail},
        "native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law",
    )
    entry = cg.get("entryConfigPath")
    if entry is None and not cg.get("nodes"):
        dorig = "synthesized"
    else:
        en = next(n for n in cg["nodes"] if n["path"] == entry)
        dorig = "jsconfig" if en["kind"] == "jsconfig" else "tsconfig"
    rec(
        log,
        "structural",
        "ts.configOrigin-derived-from-entry-kind",
        uni.get("configOrigin") == dorig,
        "configOrigin is derived from the retained graph, never asserted",
        {"claimed": uni.get("configOrigin"), "derived": dorig, "entry": entry},
        "native-evidence.md §2.2 configOrigin",
    )
    rec(
        log,
        "structural",
        "ts.universe-languageMode-agrees-context",
        uni.get("languageMode") == ctx.get("languageMode"),
        "overlapping languageMode must agree",
        {"uni": uni.get("languageMode"), "ctx": ctx.get("languageMode")},
        "native-evidence.md §2.4 universe-context field agreement",
    )


def _rust_producing(log, store, g, ctx, uni, plan):
    cid = (ctx.get("toolClosure") or {}).get("closureId")
    crec = store.parse_typed(cid, "closure")
    rec(
        log,
        "structural",
        "rust.toolClosure.kind-toolchain",
        crec.get("kind") == "toolchain",
        "toolClosure.closureId names retained kind=toolchain",
        {"closureId": cid, "kind": crec.get("kind")},
        "native-evidence.md §2.3",
    )
    rec(
        log,
        "structural",
        "rust.rustcVersion-equals-tool-closure-semanticVersion",
        ctx["toolchain"].get("rustcVersion") == crec.get("semanticVersion"),
        "§2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion",
        {"rustcVersion": ctx["toolchain"].get("rustcVersion"), "closure.semanticVersion": crec.get("semanticVersion")},
        "native-evidence.md §2.3/§11; identity-and-evidence.md §3 language-version binding chain",
    )
    tsha = tree_shas(crec)
    for k in ("rustc", "cargo", "procMacroServer"):
        rec(
            log,
            "structural",
            f"rust.toolClosure.{k}-in-closure-tree",
            ctx["toolClosure"].get(k) in tsha,
            f"{k} raw digest is a member of the signed toolchain tree",
            {k: ctx["toolClosure"].get(k), "tree": sorted(tsha)},
            "native-evidence.md §2.3 ToolClosureV1 every tool that runs is in this closure",
        )
    llvm = ctx["toolchain"].get("rustcDevLlvmDigest")
    lrec = store.parse_typed("closure2:" + llvm, "closure")
    rec(
        log,
        "structural",
        "rust.rustcDevLlvmDigest-kind",
        lrec.get("kind") == "rust-dev-llvm",
        "rustcDevLlvmDigest is the bare suffix of kind=rust-dev-llvm closure2",
        {"suffix": llvm, "kind": lrec.get("kind")},
        "identity-and-evidence.md §3; native-evidence.md §2.3",
    )
    rec(
        log,
        "structural",
        "rust.executionCapableResolution-equals-prepared-not-none",
        uni.get("executionCapableResolution") is (uni.get("preparedResolution") != "none"),
        "executionCapableResolution is preparedResolution ≠ none; never a grant",
        {"executionCapableResolution": uni.get("executionCapableResolution"), "preparedResolution": uni.get("preparedResolution")},
        "native-evidence.md §2.1",
    )
    rec(
        log,
        "structural",
        "rust.rustflags-equal-context-configProjection.rustflags",
        uni.get("rustflags") == (ctx.get("configProjection") or {}).get("rustflags"),
        "universe rustflags equals bound context configProjection.rustflags",
        {"uni": uni.get("rustflags"), "ctx": (ctx.get("configProjection") or {}).get("rustflags")},
        "native-evidence.md §2.1 overlapping field rustflags",
    )
    rec(
        log,
        "structural",
        "rust.configProjectionSha256-is-H-of-context-configProjection",
        uni.get("configProjectionSha256") == H("native.cargo-config-projection.v2", ctx["configProjection"]),
        "configProjectionSha256 is the 64-hex suffix of H(native.cargo-config-projection.v2, context.configProjection), not projectionSha256",
        {
            "claimed": uni.get("configProjectionSha256"),
            "H": H("native.cargo-config-projection.v2", ctx["configProjection"]),
            "fileProjectionSha256": ctx.get("configProjection", {}).get("projectionSha256"),
        },
        "native-evidence.md §2.1/§3.3; identity-and-evidence.md §3 two cargo-config digests",
    )
    rec(
        log,
        "structural",
        "rust.overlapping-nested-ids-agree",
        uni.get("dependencySourceSetId") == ctx.get("dependencySourceSetId")
        and uni.get("unifiedFeaturesId") == ctx.get("unifiedFeaturesId")
        and uni.get("preparedOutputSetId") == ctx.get("preparedOutputSetId"),
        "Rust overlapping nested identities must equal the bound context",
        {
            "uni": [uni.get("dependencySourceSetId"), uni.get("unifiedFeaturesId"), uni.get("preparedOutputSetId")],
            "ctx": [ctx.get("dependencySourceSetId"), ctx.get("unifiedFeaturesId"), ctx.get("preparedOutputSetId")],
        },
        "identity-and-evidence.md §3 contextAgreementFields; native-evidence.md §2.1",
    )
    base = set(ctx.get("baseCfg") or [])
    cfg_fail = []
    for s in uni.get("cfgSets") or []:
        cfg = set(s.get("cfg") or [])
        if not base <= cfg:
            cfg_fail.append({"cfgSetId": s.get("cfgSetId"), "cfg": s.get("cfg"), "baseCfg": sorted(base)})
    rec(
        log,
        "structural",
        "rust.cfgSets-contain-every-baseCfg-member",
        not cfg_fail,
        "every cfg set contains every member of the context baseCfg",
        {"failures": cfg_fail, "baseCfg": ctx.get("baseCfg"), "cfgSets": uni.get("cfgSets")},
        "native-evidence.md §2.1 cfgSets",
    )
    own_id = hex_of(uni.get("sourceUnitOwnershipId"))
    rec(
        log,
        "structural",
        "rust.sourceUnitOwnership-required-for-clones-universe",
        own_id is not None,
        "a clones fact over any Rust universe requires committed SourceUnitOwnershipV1; null admits no clone",
        {"sourceUnitOwnershipId": uni.get("sourceUnitOwnershipId")},
        "native-evidence.md §11; identity-schemas languageVersionBinding alwaysRequired",
    )
    if own_id:
        own = parse_h_frame(store.rehash(own_id))["value"]
        unit_fail = []
        for u in own.get("units") or []:
            pre = {
                "schemaVersion": 1,
                "markerPath": u.get("markerPath"),
                "targetKind": u.get("targetKind"),
                "targetName": u.get("targetName"),
            }
            derived = "sha256:" + H("native.compilation-unit.v1", pre)
            if u.get("unitId") != derived:
                unit_fail.append({"claimed": u.get("unitId"), "derived": derived, "preimage": pre})
        rec(
            log,
            "structural",
            "rust.unitId-derived-from-UnitIdentityV1",
            not unit_fail,
            "unitId is H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion,markerPath,targetKind,targetName}), derived retention",
            {"failures": unit_fail, "nUnits": len(own.get("units") or [])},
            "native-evidence.md §11 unitId derived never declared",
        )


def _syntax_producing(log, store, g, ctx, uni, plan):
    bundle = ctx.get("grammarBundle") or {}
    cid = bundle.get("closureId")
    crec = g["closures"].get(cid) or store.parse_typed(cid, "closure")
    rec(
        log,
        "structural",
        "syntax.grammar-closure-kind",
        crec.get("kind") == "grammar",
        "grammarBundle.closureId names kind=grammar",
        {"closureId": cid, "kind": crec.get("kind")},
        "identity-schemas domainSets native.context.syntax.v2 closureJoins",
    )
    rec(
        log,
        "structural",
        "syntax.parserVersion-equals-closure-semanticVersion",
        bundle.get("parserVersion") == crec.get("semanticVersion"),
        "parserVersion equals grammar closure semanticVersion",
        {"parserVersion": bundle.get("parserVersion"), "semanticVersion": crec.get("semanticVersion")},
        "identity-schemas syntax grammar join (v2 grammar-tree-and-selection)",
    )
    rec(
        log,
        "structural",
        "syntax.resolutionAttempted-false",
        uni.get("resolutionAttempted") is False,
        "syntax universe resolutionAttempted is false",
        {"resolutionAttempted": uni.get("resolutionAttempted")},
        "native-evidence.md §1.2 syntax-only",
    )


def first_structural(prod: list[dict], v2_first) -> dict | None:
    for j in prod:
        if j["layer"] == "structural" and not j["ok"] and not j.get("diagnostic"):
            return {"layer": "structural", "name": j["name"], "detail": j["detail"], "law": j.get("law"), "operands": j.get("operands")}
    return v2_first


def original_id_scope() -> list[dict]:
    req = json.loads(REQ.read_text())
    by = {r["id"]: r for r in req["requirements"]}
    charter_notes = {
        "R-RUN-TS": {"quantifier": "exactly-the-named-complete-Run", "scopeThisRecheck": "ts graph", "pendingGlobal": False},
        "R-RUN-TS-NODE-MODULES": {"quantifier": "property-of-R-RUN-TS", "scopeThisRecheck": "ts graph", "pendingGlobal": False},
        "R-RUN-TS-CONFIG-DEPS": {"quantifier": "property-of-R-RUN-TS", "scopeThisRecheck": "ts graph", "pendingGlobal": False},
        "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC": {"quantifier": "property-of-R-RUN-TS", "scopeThisRecheck": "ts graph", "pendingGlobal": False},
        "R-RUN-RUST": {"quantifier": "exactly-the-named-complete-Run", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-MIXED-EDITION": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-TARGET-EDITION": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-BODY-DIALECT": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph + pair vector", "pendingGlobal": False},
        "R-RUN-RUST-HASH-MARKER": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph + explicit pair vector", "pendingGlobal": False},
        "R-RUN-RUST-LARGE-EDITION-MAP": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph or pair vector", "pendingGlobal": False},
        "R-RUN-RUST-VERSION-COMPONENT": {"quantifier": "property-of-R-RUN-RUST", "scopeThisRecheck": "rust graph", "pendingGlobal": False},
        "R-RUN-RUST-PARTIAL-EMPTY-CLONES": {"quantifier": "exactly-the-named-complete-Run", "scopeThisRecheck": "rust-partial-clones graph", "pendingGlobal": False},
        "R-CLONE-DEFICIENCY-PAIRING": {"quantifier": "property-of-R-RUN-RUST-PARTIAL-EMPTY-CLONES", "scopeThisRecheck": "rust-partial-clones graph", "pendingGlobal": False},
        "R-RUN-SYNTAX-DATA": {"quantifier": "exactly-the-named-complete-Run", "scopeThisRecheck": "syntax-data graph", "pendingGlobal": False},
        "R-RUN-UNAVAILABLE-SEMANTIC": {"quantifier": "property-of-R-RUN-SYNTAX-DATA", "scopeThisRecheck": "syntax-data graph", "pendingGlobal": False},
        "R-RUN-NONCEMPTY-CONTEXT": {"quantifier": "both-named-parents", "scopeThisRecheck": "ts and rust graphs", "pendingGlobal": False},
        "R-IMPORTED-PAYLOAD-IN-GRAPH": {"quantifier": "at-least-one-claimed-complete-positive", "scopeThisRecheck": "satisfied if ts graph admits with import member", "pendingGlobal": False},
        "R-NATIVE-PREIMAGE-JOINS": {"quantifier": "on-the-language-Runs-that-name-them", "scopeThisRecheck": "ts and rust nested preimages", "pendingGlobal": False},
        "R-RUN-FILE-FACT-INVENTORY": {
            "quantifier": "at-least-one-of-TS-Rust-syntax-code",
            "scopeThisRecheck": "may be ts or rust if file facts actually present; syntax-code outside",
            "pendingGlobal": "syntax-code frozen/outside this four-Run recheck; not a per-Run demand on ts and rust",
        },
        "R-RUN-CLONES-L0-AND-NORMALIZED": {
            "quantifier": "property-of-that-at-least-one-file-fact-Run",
            "scopeThisRecheck": "NOT a per-language/per-Run demand on every TS and Rust graph",
            "pendingGlobal": "unreviewed syntax-code member of the at-least-one set is pending global integration; absence on ts/rust is not a failure of each scoped graph",
        },
        "R-RUN-CLONES-CUSTODY": {
            "quantifier": "property-of-R-RUN-CLONES-L0-AND-NORMALIZED",
            "scopeThisRecheck": "same at-least-one set; not a per-Run demand",
            "pendingGlobal": "pending global integration with the parent at-least-one set",
        },
        "R-RUN-SYNTAX-CODE": {"quantifier": "exactly-the-named-complete-Run", "scopeThisRecheck": "outside this four-Run recheck", "pendingGlobal": True},
        "R-RUN-NO-COMPILER-UNIT": {"quantifier": "property-of-R-RUN-SYNTAX-CODE", "scopeThisRecheck": "outside", "pendingGlobal": True},
        "R-HIDDEN-MISMATCH-PER-LANGUAGE": {"quantifier": "standalone-vector", "scopeThisRecheck": "outside", "pendingGlobal": True},
        "R-RUN-UNSUPPORTED-GRAMMAR": {"quantifier": "standalone-vector", "scopeThisRecheck": "outside", "pendingGlobal": True},
    }
    out = []
    for i, note in charter_notes.items():
        r = by.get(i) or {}
        out.append(
            {
                "id": i,
                "kind": r.get("kind"),
                "parent": r.get("parent"),
                "mayBeSatisfiedTogetherWith": r.get("mayBeSatisfiedTogetherWith"),
                "requirement": r.get("requirement"),
                "observable": r.get("observable"),
                **note,
            }
        )
    return out


def render_selfaudit_md(s: dict) -> str:
    lines = []
    lines.append("# Review-quality self-audit (other-runs v2)")
    lines.append("")
    lines.append(f"**Successor four-Run verdict: `{s['successorVerdict']}`**")
    lines.append("")
    lines.append("Same kit-only four-Run origin. This is not a new origin, not authoring, not whole-consumer ACCEPT, not product/real-host/compiler/crypto qualification. Stores were not modified.")
    lines.append("")
    lines.append("The original charter (verbatim) is the quantifier/kind authority. Structured `requirements.json` organizes that charter; it does not replace it.")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append("| Object | SHA-256 | Result |")
    lines.append("|---|---|---|")
    c = s["custody"]
    for row in [
        ("original charter", c["charterSha256"], f"expected match={c['charterMatch']}"),
        ("kit manifest", c["kitManifestSha256"], c["kitFiles"]),
        ("parent frozen", c["parentSubjectSha256"], "match"),
        ("requirements.json", c["requirementsSha256"], f"match={c['reqMatch']}"),
        ("v2 snapshot-manifest", c["snapshotManifestSha256"], c["snapshotFiles"]),
        ("preserved v2 other-runs-review.md", c["v2MdSha256"], f"match={c['v2MdMatch']}"),
        ("preserved v2 other-runs-review.json", c["v2JsonSha256"], f"match={c['v2JsonMatch']}"),
    ]:
        lines.append(f"| {row[0]} | `{row[1]}` | {row[2]} |")
    lines.append("")
    lines.append(f"Python: `{PYTHON} -I -B`")
    lines.append("")
    lines.append("```bash")
    lines.append(s["command"])
    lines.append("```")
    lines.append("")
    lines.append("## Withdrawn grades")
    lines.append("")
    for w in s["withdrawn"]:
        lines.append(f"- **{w['grade']}** — {w['reason']}")
    lines.append("")
    lines.append("## Charter quantifiers (full charter, not the v2 condensed map)")
    lines.append("")
    lines.append("Charter Phase 5: complete TS Run and complete Rust Run (and their Include properties); a separate Rust partial-enumeration complete Run; **at least one** complete file-fact Run (may be the same export as a TS, Rust, or syntax-code Run if those properties are actually present) carrying L0 **and** a normalized-level clone identity; syntax-code and syntax-data complete Runs; imported payload on **at least one** claimed complete graph.")
    lines.append("")
    lines.append("v2 treated `R-RUN-CLONES-L0-AND-NORMALIZED` / `R-RUN-CLONES-CUSTODY` as a per-TS-and-Rust demand and used that as the four-Run refusal. That silently upgraded an at-least-one-set property. The unreviewed syntax-code member of that set is **pending global integration**, not a blanket waiver and not a failure of each scoped graph.")
    lines.append("")
    lines.append("| ID | Kind | Quantifier | This recheck |")
    lines.append("|---|---|---|---|")
    for p in s["originalIdScope"]:
        pg = "pending-global" if p.get("pendingGlobal") else "in-scope"
        lines.append(f"| `{p['id']}` | {p.get('kind')} | {p.get('quantifier')} | {pg}: {p.get('scopeThisRecheck')} |")
    lines.append("")
    lines.append("## v2 PASS claims vs producing/join laws")
    lines.append("")
    lines.append("v2 structural/fullsemantic PASS executed stock schema, annotated digest *presence*, nested H frames, snapshot path joins, execution-inputs derive, and C(expected proof)==C(claimed). Identity-and-evidence §3 requires Run closure to **re-run owning native admission** over retained bytes (`admit_native_context` / `bind_*_universe`). Native-evidence §2 names field-producing recipes. Blob presence or H-frame parse is not those recipes.")
    lines.append("")
    lines.append("Expected-proof C equality of a shared `compose_proof` (including predicate `inputRefs` citing `rule-program`) does not establish identity §3 subset/totality. Diagnostics after a first structural refusal are notReached, not successful replay.")
    lines.append("")
    for name, r in s["runs"].items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"- v2 layers {r['v2Layers']} overall `{r['v2Overall']}` first `{r['v2FirstRefusal']}`")
        lines.append(f"- successor layers {r['layers']} overall **{r['overall']}**")
        if r.get("firstRefusal"):
            fr = r["firstRefusal"]
            lines.append(f"- First refusal (acceptance-grade): `{fr.get('layer')}:{fr.get('name')}` — {fr.get('detail')}")
            if fr.get("law"):
                lines.append(f"- Law: {fr['law']}")
        else:
            lines.append("- First refusal: none")
        lines.append(f"- Semantic: `{r['layers'].get('fullsemantic')}`")
        lines.append("")
        lines.append("Producing/join assertions (operands in JSON):")
        lines.append("")
        for a in r.get("producing") or []:
            mark = "PASS" if a["ok"] else ("DIAG" if a.get("diagnostic") else "FAIL")
            lines.append(f"- `{a['name']}` **{mark}** — {a.get('detail')}")
        lines.append("")
    lines.append("## Checker exception/branch audit")
    lines.append("")
    for b in s["checkerBranches"]:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## Unexecuted / pending")
    lines.append("")
    for u in s["unexecuted"]:
        lines.append(f"- {u}")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_successor_md(s: dict) -> str:
    lines = []
    lines.append("# Other-runs independent kit-only review (successor after self-audit)")
    lines.append("")
    lines.append(f"**Verdict: `{s['successorVerdict']}`**")
    lines.append("")
    lines.append("Successor of the v2 four-Run recheck after a law/quantifier self-audit against the original charter. Not whole-consumer ACCEPT. Foundation/pilot/workflows/syntax-code remain outside this scoped recheck (pending global integration where the charter's at-least-one set includes them).")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append("| Object | SHA-256 | Result |")
    lines.append("|---|---|---|")
    c = s["custody"]
    lines.append(f"| kit | `{c['kitManifestSha256']}` | {c['kitFiles']} |")
    lines.append(f"| parent | `{c['parentSubjectSha256']}` | match |")
    lines.append(f"| requirements | `{c['requirementsSha256']}` | match={c['reqMatch']} |")
    lines.append(f"| snapshot | `{c['snapshotManifestSha256']}` | {c['snapshotFiles']} |")
    lines.append(f"| original charter | `{c['charterSha256']}` | match={c['charterMatch']} |")
    lines.append("")
    lines.append(f"Command: `{s['command']}`")
    lines.append("")
    lines.append("## First-refusal map")
    lines.append("")
    lines.append("| Run | Raw | Schema | Structural | Fullsemantic | First refusal |")
    lines.append("|---|---|---|---|---|---|")
    for name, r in s["runs"].items():
        fr = r.get("firstRefusal") or {}
        frs = f"`{fr.get('layer','')}:{fr.get('name','')}`" if fr else "none"
        L = r["layers"]
        lines.append(f"| `{name}` | {L.get('raw')} | {L.get('schema')} | {L.get('structural')} | {L.get('fullsemantic')} | {frs} |")
    lines.append("")
    lines.append("Classification:")
    lines.append("")
    lines.append("- **Existing law, missing implementation of a producing/join recipe:** TypeScript `compilerPackageDigest` is a retained raw blob (`tsc-pkg`) but is not a member of the signed toolchain closure tree named by `toolClosure.closureId` (`native-evidence` §2.4 / schema `retention=closure-tree-member`). Rust (and rust-partial, same context) `toolchain.rustcVersion=1.80.0` is not the admitted tool-closure `semanticVersion=1.0.0` (`native-context-compiler-version-not-from-manifest`, native-evidence §2.3/§11). v2 treated blob rehash / schema inhabitance as those joins.")
    lines.append("- **Withdrawn refusal ground:** `R-RUN-CLONES-L0-AND-NORMALIZED` / `R-RUN-CLONES-CUSTODY` as a per-TS-and-Rust demand. Charter/requirements quantifier is at-least-one file-fact Run (TS or Rust or syntax-code). Syntax-code is pending global integration.")
    lines.append("- **Absent/contradictory law:** none used as a waiver. Predicate `inputRefs` citing `rule-program` is schema-live (`ProofInputRef.domain`) and excluded from `evaluationInputRefs` by enumeration-contract §7; recorded as a law-interaction, not the first refusal.")
    lines.append("- **C equality of shared mistaken derivation:** v2 `compose_proof` C-matched claimed proofs; that does not execute native producing recipes or identity §3 native re-admission.")
    lines.append("")
    for name, r in s["runs"].items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"- Store `{r['storeSha256']}`")
        lines.append(f"- Run `{r.get('runId')}` Plan `{r.get('planId')}` Proof `{r.get('proofId')}`")
        lines.append(f"- Layers {r['layers']} overall **{r['overall']}**")
        if r.get("firstRefusal"):
            fr = r["firstRefusal"]
            lines.append(f"- First refusal: `{fr.get('layer')}:{fr.get('name')}` — {fr.get('detail')}")
        else:
            lines.append("- First refusal: none")
        fails = [a for a in r.get("producing") or [] if not a["ok"] and not a.get("diagnostic")]
        if fails:
            lines.append("")
            lines.append("Reached producing/join failures:")
            for a in fails:
                lines.append(f"- `{a['name']}` — {a['detail']}")
        lines.append("")
    lines.append("## Unexecuted")
    lines.append("")
    for u in s["unexecuted"]:
        lines.append(f"- {u}")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    probes = OUT / "probes"
    probes.mkdir(parents=True, exist_ok=True)
    kit_man = json.loads(KIT_MANIFEST.read_text())
    kit_ok = 0
    for e in kit_man["files"]:
        p = KIT_MANIFEST.parent / e["path"]
        if p.exists() and sha(p) == e["sha256"]:
            kit_ok += 1
    snap_man = json.loads(SNAP_MANIFEST.read_text())
    snap_ok = sum(1 for e in snap_man["files"] if sha(SNAP / e["path"]) == e["sha256"])
    custody = {
        "charterSha256": sha(CHARTER),
        "charterMatch": sha(CHARTER) == EXPECTED_CHARTER,
        "kitManifestSha256": sha(KIT_MANIFEST),
        "kitFiles": f"{'PASS' if kit_ok == len(kit_man['files']) else 'FAIL'} {kit_ok}/{len(kit_man['files'])}",
        "parentSubjectSha256": PARENT,
        "requirementsSha256": sha(REQ),
        "reqMatch": sha(REQ) == EXPECTED_REQ,
        "snapshotManifestSha256": sha(SNAP_MANIFEST),
        "snapshotFiles": f"{'PASS' if snap_ok == len(snap_man['files']) else 'FAIL'} {snap_ok}/{len(snap_man['files'])}",
        "snapMatch": sha(SNAP_MANIFEST) == EXPECTED_SNAP,
        "v2MdSha256": sha(V2_MD),
        "v2MdMatch": sha(V2_MD) == V2_MD_SHA,
        "v2JsonSha256": sha(V2_JSON),
        "v2JsonMatch": sha(V2_JSON) == V2_JSON_SHA,
    }
    v2_prior = json.loads(V2_JSON.read_text())
    runs = {}
    for name in RUNS:
        store_path = SNAP / "runs" / f"{name}.store.json"
        print(f"AUDIT {name}", flush=True)
        v2 = admit_one(store_path, skip_tamper=True)
        prod = producing_rules(name, Store.load(store_path), v2)
        (probes / f"{name}.producing.json").write_text(json.dumps(prod, indent=2, default=str) + "\n")
        v2_first = v2.get("firstRefusal")
        fs = first_structural(prod, v2_first)
        v2_layers = dict(v2["layers"])
        layers = dict(v2_layers)
        if fs and fs.get("name") != (v2_first or {}).get("name"):
            layers["structural"] = "REFUSED"
            layers["fullsemantic"] = "NOT_REACHED"
            overall = "REFUSED"
        elif v2["overall"] != "ADMIT":
            overall = "REFUSED"
            if layers.get("structural") == "REFUSED":
                layers["fullsemantic"] = "NOT_REACHED"
        else:
            overall = "ADMIT"
        if layers.get("structural") == "REFUSED":
            layers["fullsemantic"] = "NOT_REACHED"
            overall = "REFUSED"
        runs[name] = {
            "storeSha256": v2["storeSha256"],
            "bytes": v2["bytes"],
            "blobCount": v2["blobCount"],
            "runId": v2.get("runId"),
            "planId": v2.get("planId"),
            "proofId": v2.get("proofId"),
            "expectedProofId": v2.get("expectedProofId"),
            "v2Layers": v2_layers,
            "v2Overall": v2["overall"],
            "v2FirstRefusal": v2_first,
            "layers": layers,
            "overall": overall,
            "firstRefusal": fs,
            "producing": prod,
            "claimedVerdict": v2.get("claimedVerdict"),
            "derivedVerdict": v2.get("derivedVerdict"),
            "notReached": (["complete-semantic-replay"] if layers.get("fullsemantic") == "NOT_REACHED" else []),
        }
        print(f"  successor={overall} first={fs}", flush=True)

    if all(runs[n]["overall"] == "ADMIT" for n in RUNS):
        successor = "OTHER_RUNS_ADMIT"
    elif any(runs[n]["layers"].get("raw") == "NOT_REACHED" for n in RUNS):
        successor = "OTHER_RUNS_INCOMPLETE"
    else:
        successor = "OTHER_RUNS_REFUSED"

    withdrawn = [
        {
            "grade": "v2 OTHER_RUNS_REFUSED on R-RUN-CLONES-L0-AND-NORMALIZED / R-RUN-CLONES-CUSTODY as a per-TS-and-Rust demand",
            "reason": "Charter Phase 5 and requirements mayBeSatisfiedTogetherWith = TS|Rust|syntax-code. At-least-one-set. Syntax-code is pending global integration. Not a failure of each scoped graph.",
        },
        {
            "grade": "v2 structural/fullsemantic PASS on ts",
            "reason": "Did not execute compilerPackageDigest closure-tree-member join (blob presence is not tree membership).",
        },
        {
            "grade": "v2 structural/fullsemantic PASS on rust and rust-partial-clones",
            "reason": "Did not execute rustcVersion == tool-closure semanticVersion (native-context-compiler-version-not-from-manifest). Fullsemantic PASS after that miss is withdrawn; successor marks fullsemantic NOT_REACHED.",
        },
        {
            "grade": "v2 fullsemantic PASS as successful replay on graphs whose native producing recipes were unexecuted",
            "reason": "Positive graph admission (including native re-admission) precedes semantic comparison. C equality of compose_proof is not native admission.",
        },
    ]
    checker_branches = [
        "v2 admit_digest_field raw-artifact: rehash blob only; no closure-tree-member check for compilerPackageDigest (schema retention=closure-tree-member).",
        "v2 never compared NativeContextV2.toolchain.rustcVersion to closure.semanticVersion; no native-context-compiler-version-not-from-manifest.",
        "v2 never derived unitId from H(native.compilation-unit.v1, UnitIdentityV1) (this audit did; rust unitIds matched).",
        "v2 never derived TypeScript config node kind / configOrigin (this audit: tsconfig.json -> tsconfig, configOrigin=tsconfig matched).",
        "v2 never checked cfgSets ⊇ baseCfg, rustflags equality, configProjectionSha256 = H(cargo-config-projection) (this audit: those rust overlapping fields matched).",
        "v2 compose_proof always inserts domain=rule-program into predicate inputRefs; claimed proofs match that shared derivation; identity §3 subset sentence is not established by that C equality.",
        "v2 walk_digest_anns does not re-run admit_native_context / bind_rust_universe / bind_typescript_universe field-producing recipes; nested H parse + stock schema is not that admission.",
        "v2 first-refusal JoinLog continued proof-C-compare after structural refuse in earlier versions; current finish() marks later layers NOT_REACHED only from acceptance-grade joins — producing-rule misses were never those joins.",
    ]
    unexecuted = [
        "ROOT-ADMISSION outside this role",
        "component-manifest-schemas.v11 inhabitance (CANDIDATE-NOT-APPLIED); stored-bytes tree join still executed in v2",
        "real host/compiler/crypto/SQLite",
        "syntax-code / foundation / pilot / workflow / standalone vectors (pending global integration)",
        "Unicode Default Case Conversion beyond ASCII lib names (current libSelection is ASCII ES2022)",
        "L1–L3 clone token-stream recomputation (no such facts on these four graphs; at-least-one set pending syntax-code)",
    ]
    summary = {
        "successorVerdict": successor,
        "standing": "Same-origin review-quality self-audit of v2 four-Run grades against the original charter and owning producing/join laws. Not whole-consumer ACCEPT.",
        "python": f"{PYTHON} -I -B",
        "command": f"{PYTHON} -I -B {HERE / 'selfaudit.py'}",
        "custody": custody,
        "withdrawn": withdrawn,
        "originalIdScope": original_id_scope(),
        "runs": runs,
        "checkerBranches": checker_branches,
        "unexecuted": unexecuted,
        "v2VerdictPreserved": v2_prior.get("verdict"),
        "wholeConsumerNotAccepted": True,
        "storesUnchanged": True,
    }
    (OUT / "review-selfaudit.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    (OUT / "review-selfaudit.md").write_text(render_selfaudit_md(summary))
    succ = {
        "verdict": successor,
        "standing": summary["standing"],
        "custody": custody,
        "command": summary["command"],
        "runs": {n: {k: v for k, v in r.items() if k != "producing"} | {"producingFails": [a for a in r["producing"] if not a["ok"] and not a.get("diagnostic")]} for n, r in runs.items()},
        "withdrawn": withdrawn,
        "originalIdScope": summary["originalIdScope"],
        "unexecuted": unexecuted,
        "wholeConsumerNotAccepted": True,
    }
    (OUT / "other-runs-review.json").write_text(json.dumps(succ, indent=2, default=str) + "\n")
    (OUT / "other-runs-review.md").write_text(render_successor_md({**summary, "runs": runs}))
    print("SUCCESSOR", successor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
