"""RUN-RS-*: a mixed-edition Rust workspace.

Exercises, from the normative text:
  * a TARGET-specific edition differing from its package default;
  * the SAME physical file under two distinct explicitly selected target
    editions -- two selections, two universes, two body identities;
  * stable body identity when only the SELECTION changes without changing the
    effective dialect;
  * ambiguity (selected owners disagree) and PARTIAL enumeration, with the
    empty clone view that must NOT claim complete Coverage;
  * a valid `#` marker directory;
  * a representative large edition map (21 crates), which changes the universe
    identity and must NOT change a body identity.
"""
from __future__ import annotations

import hashlib

import assemble as A
import build as B
import canon as K
import kit
import native as N
import scenarios as S
from store import Store, split_id

SHARED_RS = (b"pub fn shared() -> u32 {\n    let value = 7;\n    value + 1\n}\n")
BETA_LIB = b"mod shared;\npub use shared::shared;\n"
ALPHA_LIB = b"pub fn alpha() -> u32 { 1 }\n"
WS_TOML = b"[workspace]\nmembers = [\"crates/#alpha\", \"crates/beta\"]\n"
ALPHA_TOML = b"[package]\nname = \"alpha\"\nedition = \"2021\"\n"
BETA_TOML = (b"[package]\nname = \"beta\"\nedition = \"2018\"\n"
             b"[[test]]\nname = \"beta_it\"\nedition = \"2021\"\n")
LOCK = b"version = 3\n"

BODY_START = SHARED_RS.index(b"{\n")
BODY_END = SHARED_RS.index(b"}\n", BODY_START) + 1
BODY = SHARED_RS[BODY_START:BODY_END]

ALPHA_DIR = "crates/#alpha"          # a valid `#` marker directory

# a representative large edition map: 21 crates, one real + 20 unrelated
LARGE_EDITION_MAP = {"alpha": 2021, "beta": 2018}
for i in range(19):
    LARGE_EDITION_MAP[f"dep{i:02d}"] = [2015, 2018, 2021, 2024][i % 4]


def units():
    u_alpha = S.unit(f"{ALPHA_DIR}/Cargo.toml", "lib", "alpha", "alpha", None)
    u_beta_lib = S.unit("crates/beta/Cargo.toml", "lib", "beta", "beta", None)
    u_beta_test = S.unit("crates/beta/Cargo.toml", "test", "beta_it", "beta", 2021)
    u_beta_bin = S.unit("crates/beta/Cargo.toml", "bin", "beta_cli", "beta", None)
    return u_alpha, u_beta_lib, u_beta_test, u_beta_bin


def build(store=None, *, selection="lib", enumeration="complete",
          edition_map=None, empty_clone_view=False, tamper=None,
          clone_coverage_override=None):
    """selection: 'lib' | 'test' | 'both' | 'lib+bin'"""
    s = store or Store()
    files = {"Cargo.toml": WS_TOML, "Cargo.lock": LOCK,
             f"{ALPHA_DIR}/Cargo.toml": ALPHA_TOML,
             f"{ALPHA_DIR}/src/lib.rs": ALPHA_LIB,
             "crates/beta/Cargo.toml": BETA_TOML,
             "crates/beta/src/lib.rs": BETA_LIB,
             "crates/beta/src/shared.rs": SHARED_RS}
    scope = B.scope_descriptor(["."], excluded=["target", ".git"])
    config = B.default_config(["inventory", "syntax", "clones-fact"])
    snap_id, snap, inventory = B.make_snapshot(s, files, scope, config)
    inv = {r["path"]: r for r in inventory}

    lockfile = {"path": "Cargo.lock",
                "contentSha256": inv["Cargo.lock"]["sha256"], "lockfileVersion": 3}
    dss_id, _ = S.dependency_source_set(s, lockfile, [])
    uf_id, _ = S.unified_features(s, "x86_64-unknown-linux-gnu")
    ctx, ctx_hex = S.rust_context(s, dependency_set_id=dss_id,
                                  unified_features_id=uf_id)

    u_alpha, u_beta_lib, u_beta_test, u_beta_bin = units()
    all_units = [u_alpha, u_beta_lib, u_beta_test, u_beta_bin]
    sel = {"lib": [u_alpha["unitId"], u_beta_lib["unitId"]],
           "test": [u_beta_test["unitId"]],
           "both": [u_beta_lib["unitId"], u_beta_test["unitId"]],
           "lib+bin": [u_alpha["unitId"], u_beta_lib["unitId"],
                       u_beta_bin["unitId"]]}[selection]
    ownership = [
        {"path": f"{ALPHA_DIR}/src/lib.rs", "unitId": u_alpha["unitId"]},
        {"path": "crates/beta/src/lib.rs", "unitId": u_beta_lib["unitId"]},
        {"path": "crates/beta/src/shared.rs", "unitId": u_beta_lib["unitId"]},
        {"path": "crates/beta/src/shared.rs", "unitId": u_beta_test["unitId"]},
        {"path": "crates/beta/src/lib.rs", "unitId": u_beta_bin["unitId"]},
    ]
    sou_id, _ = S.source_unit_ownership(s, all_units, sel, ownership, enumeration)

    u, u_hex = S.rust_universe(
        s, ctx, ctx_hex, edition=edition_map or {"alpha": 2021, "beta": 2018},
        lockfile=lockfile,
        crate_roots=[f"{ALPHA_DIR}/src/lib.rs", "crates/beta/src/lib.rs"],
        ownership_id=sou_id)

    prov_id, _ = S.provider_closure(s, "rust-semantic")
    eval_id, _ = S.evaluator_closure(s)
    det_id, _ = S.detector_closure(s)

    manifest = B.capability_manifest(providers=[B.provider_capability(
        "rust-semantic", "rust",
        {"clones": "normalized-body-hash", "file": "enumerated"},
        ["linux-x86_64-gnu"])])
    cm_id, cm_bytes_digest, cm_bytes = B.commit_capability_manifest(s, manifest)

    spec = {"schemaVersion": 2, "requestedCapabilities": sorted([
        {"capabilityId": "inventory", "languageMode": "rust-cargo",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "clones-fact", "languageMode": "rust-cargo",
         "workspaceRoot": ".", "required": True}], key=K.C),
        "policyPackIds": ["cb9.pack"], "parameters": []}
    grant_digest, _ = A.semantic_grant(s, snap["scopeDigest"])
    policy_digest = s.put_record(POLICY)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    waiver_digest = s.put_record(waivers)
    plan_id, plan = B.make_plan(s, snap_id, snap, cm_id, cm_bytes_digest,
                                [prov_id, eval_id, det_id], spec, [ctx_hex],
                                policy_digest, waiver_digest, grant_digest,
                                {"unit": "work-units", "limit": 100000})

    file_subjects = [r["path"] for r in inventory]
    s1_id, s1 = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                             prov_id, file_subjects)
    s2_id, s2 = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                             "normalized-body-hash", prov_id,
                             ["crates/beta/src/shared.rs"])

    facts = {}
    for row in inventory:
        fid, f = B.make_fact(s, snap_id, "file", "enumerated", u_hex, u_hex,
                             prov_id,
                             {"path": row["path"], "contentSha256": row["sha256"],
                              "byteLength": row["bytes"]}, [])
        facts[fid] = f

    body_identity = None
    blv = None
    if not empty_clone_view:
        blv, language_id = N.derive_body_language_version(
            "native.semantic-universe.rust.v2", u, ctx,
            "crates/beta/src/shared.rs",
            {"sourceUnitOwnership": s.objects["sha256:" + split_id(sou_id, "sha256")]})
        lv_digest = s.put_blob(S.LEVEL_SPEC_L0)
        frame = K.body_identity_frame(
            "L0-verbatim", hashlib.sha256(S.LEVEL_SPEC_L0).digest(), language_id,
            hashlib.sha256(K.C(blv)).digest(), K.l0_payload(BODY))
        body_hex = s.put_blob(frame)
        body_identity = "sha256:" + body_hex
        anchor = {"path": "crates/beta/src/shared.rs",
                  "blobDigest": inv["crates/beta/src/shared.rs"]["sha256"],
                  "startByte": BODY_START, "endByte": BODY_END}
        cfid, cf = B.make_fact(s, snap_id, "clones", "normalized-body-hash",
                               u_hex, u_hex, prov_id,
                               {"bodyIdentity": body_identity,
                                "normalisationLevel": "L0-verbatim",
                                "normalisationVersion": lv_digest}, [anchor])
        facts[cfid] = cf

    coverages = {}
    for scope_id, sc in ((s1_id, s1), (s2_id, s2)):
        commitment = "sha256:" + split_id(scope_id, "scope2")
        kwargs = {}
        if sc["relation"] == "clones" and empty_clone_view:
            kwargs = {"coverage": "unknown",
                      "deficiency": "input-closure-incomplete",
                      "native_cause": "body-language-owner-unenumerated"
                      if enumeration == "partial" else
                      "body-language-owner-ambiguous"}
            if clone_coverage_override:
                kwargs.update(clone_coverage_override)
        cid, cdesc, payload = B.make_coverage(
            s, scope_id, sc,
            B.coverage_entry(sc["relation"], sc["resolution"], commitment,
                             len(sc["subjects"]), **kwargs))
        coverages[cid] = {"scopeId": scope_id, "payload": payload}

    view_id, view = B.make_view(s, plan_id, [s1_id, s2_id], list(facts),
                                list(coverages), prov_id)
    stage_digest, _ = B.make_stage(s, plan_id, prov_id, "native.analyze",
                                   ["fact", "coverage", "subject-scope"],
                                   kit.doc_digest("native"))
    ep_id, _ = B.make_exec_plan(s, plan_id, [
        {"ordinal": 0, "stageSpecDigest": stage_digest, "requires": [],
         "outputDomains": sorted(["fact", "coverage", "subject-scope"], key=K.C)}])

    out = A.finish_run(s, plan_id=plan_id, plan=plan, snapshot_id=snap_id,
                       views={view_id: view}, view_ids=[view_id],
                       scopes={s1_id: s1, s2_id: s2}, facts=facts,
                       coverages=coverages, policy=POLICY,
                       policy_digest=policy_digest, waivers=waivers,
                       rule_program=A.compile_program(POLICY, policy_digest),
                       evaluator_closure_id=eval_id, detector_closure_id=det_id,
                       exec_plan_id=ep_id, universe_language={u_hex: "rust"},
                       capability_manifest_id=cm_id, tamper=tamper)
    out.update({"store": s, "universeHex": u_hex, "contextHex": ctx_hex,
                "bodyIdentity": body_identity, "bodyLanguageVersion": blv,
                "ownershipId": sou_id, "planId": plan_id,
                "capabilityManifestId": cm_id})
    return out


POLICY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [
        {"ruleId": "cb9.rust-no-clone", "enabled": True, "severity": "error",
         "gate": True,
         "ruleProgramRef": {"contributionId": "cb9.native",
                            "ruleStableId": "cb9.rust-no-clone",
                            "semanticsMajor": 1, "programDigest": "33" * 32},
         "subjectEnumeration": {"universe": "rust", "subjectKind": "file",
                                "include": ["crates/beta/src/shared.rs"]},
         "emitWhen": {"op": "none", "relation": "clones",
                      "minResolution": "normalized-body-hash", "filters": []},
         "evidenceUse": [], "messageCode": "cb9.rust.noclone"},
    ],
}
