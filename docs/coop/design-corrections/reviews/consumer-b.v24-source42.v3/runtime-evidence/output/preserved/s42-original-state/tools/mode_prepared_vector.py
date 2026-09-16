"""R-ADVERTISED-MODE-PATHS residue: an executed representable analysis path for language mode rust-cargo-prepared.

Constructs a Rust context and universe bound to a retained inert PreparedOutputSetV3 (preparation kind imported-descriptor,
preparedResolution imported-inert), admits them through native_ctx (context closures, nested frames, prepared rows,
universe agreement), states the rust-cargo-prepared cell obligation (matrix cell, kind derivation, policy universe token)
and admits a declares@syntactic fact plus scope/Coverage under that universe. Negatives: a non-inert prepared row and a
prepared-resolution / prepared-set disagreement. Writes vectors/mode-rust-cargo-prepared.json.
Usage: python3 tools/runref.py tools/mode_prepared_vector.py
"""
import hashlib
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/builders")

import canonical as K  # noqa: E402
import enumeration as EN  # noqa: E402
import native_ctx as NC  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
from syntax_runs import closure  # noqa: E402

KIT = schemas.kit()
NE = "native/native-evidence.schemas.v2.json"
REL = "foundation/relation-payload-schemas.v2.json"
ID = "foundation/identity-schemas.v3.json"
TRIPLE = "x86_64-unknown-linux-gnu"
failures = []


def build(row_kind="macro-expansion", resolution="imported-inert", universe_set_null=False):
    store = Store()
    files = {"Cargo.toml": b"[package]\nname = \"p\"\nversion = \"0.1.0\"\nedition = \"2021\"\n",
             "Cargo.lock": b"version = 3\n\n[[package]]\nname = \"p\"\nversion = \"0.1.0\"\n",
             "src/lib.rs": b"#[derive(Debug)]\npub struct S;\npub fn f() -> u8 {\n    1\n}\n"}
    inv = [{"path": p, "sha256": store.put_bytes(files[p]), "bytes": len(files[p])} for p in sorted(files, key=lambda p: p.encode())]
    T, tdesc = closure(store, "toolchain", "cb24-rust-toolchain", {"bin/rustc": b"synthetic rustc\n", "bin/cargo": b"synthetic cargo\n",
                                                                  "bin/proc-macro-srv": b"synthetic proc macro server\n"}, "1.82.0")
    L, ldesc = closure(store, "rust-dev-llvm", "cb24-rust-dev-llvm", {f"lib/rustlib/{TRIPLE}/lib/libstd.rlib": b"std rlib\n"}, "1.82.0")
    tree = {r["path"]: r["sha256"] for r in tdesc["tree"]}
    lock = {"path": "Cargo.lock", "contentSha256": next(r["sha256"] for r in inv if r["path"] == "Cargo.lock"), "lockfileVersion": 3}
    dep = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lock, "packages": [], "completeness": {"state": "complete", "missing": []}}
    dep_id = "sha256:" + store.put_frame("native.dependency-source-set.v1", dep)
    feats = {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": TRIPLE, "activated": [{"packageKey": "p 0.1.0", "features": []}],
             "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "cb24-synthetic"}}
    feats_id = "sha256:" + store.put_frame("native.unified-features.rust.v1", feats)
    toolchain = {"rustCommitHash": "f6e511eec7342f59a25f7c0534f1dbea00d01b14", "rustcVersion": "1.82.0", "cargoVersion": "1.82.0",
                 "sysrootDigest": store.put_bytes(b"sysroot manifest synthetic\n"), "rustcDevLlvmDigest": L.split(":", 1)[1],
                 "standardLibraryComponentDigests": [{"component": "libstd.rlib", "sha256": ldesc["tree"][0]["sha256"]}], "targetTriple": TRIPLE}
    expansion = b"impl ::core::fmt::Debug for S { fn fmt(&self, f: &mut ::core::fmt::Formatter) -> ::core::fmt::Result { f.write_str(\"S\") } }\n"
    tokens = b"#[derive(Debug)]"
    prep = {"schemaVersion": 3,
            "preparation": {"kind": "imported-descriptor", "authorizationId": None, "importId": "import2:" + "4" * 64, "toolchain": toolchain,
                            "dependencySourceSetId": dep_id, "cfgSetId": "default", "producer": {"id": "external", "version": "1.0.0"}},
            "rows": [{"kind": row_kind, "ownerKey": "core derive Debug", "configuration": ["default"],
                      "site": {"path": "src/lib.rs", "startByte": 0, "endByte": len(tokens), "inputTokenDigest": store.put_bytes(tokens)},
                      "inputBinding": {"cfgSetId": "default", "dependencySourceSetId": dep_id, "ownerFileManifestSha256": "5" * 64,
                                       "toolchainDigest": hashlib.sha256(K.C(toolchain)).hexdigest()},
                      "blob": {"sha256": store.put_bytes(expansion), "byteLength": len(expansion),
                               "mediaType": "application/x-sharedlib" if row_kind == "proc-macro-dylib" else "text/x-rust-expansion"},
                      "status": "ok", "failureDetail": None, "generated": None}]}
    prep_id = "sha256:" + store.put_frame("native.prepared-output-set.v3", prep)
    rustflags = {"honored": [], "stripped": [], "executableSelected": False}
    projection = {"schemaVersion": 2, "honoredKeys": [], "strippedKeys": [], "replacedSnapshotConfigs": [], "rustflags": rustflags,
                  "ancestorCarrierVerified": True, "cargoHome": "private-empty", "environmentProjection": "none", "claimsCargoSwitch": False,
                  "projectionSha256": store.put_bytes(b"# empty projected cargo config\n")}
    ctx = {"schemaVersion": 2, "targetTriple": TRIPLE, "hostTriple": TRIPLE, "toolchain": toolchain,
           "toolClosure": {"closureId": T, "rustc": tree["bin/rustc"], "cargo": tree["bin/cargo"], "procMacroServer": tree["bin/proc-macro-srv"], "linker": None, "ar": None},
           "baseCfg": ["unix"], "resolverVersion": 2, "dependencySourceSetId": dep_id, "unifiedFeaturesId": feats_id, "preparedOutputSetId": prep_id,
           "configProjection": projection}
    ctx_hex = store.put_frame("native.context.rust.v2", ctx)
    unit = {"markerPath": "Cargo.toml", "targetKind": "lib", "targetName": "p"}
    uid = NC.compilation_unit_id(unit)
    own = {"schemaVersion": 1, "enumeration": "complete", "units": [dict(unit, unitId=uid, crateName="p", targetEdition=None)],
           "selectedUnitIds": [uid], "ownership": [{"path": "src/lib.rs", "unitId": uid}]}
    uni = {"schemaVersion": 2, "edition": {"p": 2021}, "lockfileIdentity": lock, "dependencySourceSetId": dep_id, "unifiedFeaturesId": feats_id,
           "nativeContextId": "sha256:" + ctx_hex, "cfgSets": [{"cfgSetId": "default", "cfg": ["unix"]}], "rustflags": rustflags,
           "crateRootPaths": ["src/lib.rs"], "configProjectionSha256": store.put_frame("native.cargo-config-projection.v2", projection),
           "executionCapableResolution": resolution != "none", "preparedOutputSetId": None if universe_set_null else prep_id,
           "preparedResolution": resolution, "sourceUnitOwnershipId": "sha256:" + store.put_frame("native.source-unit-ownership.v1", own)}
    U = store.put_frame("native.semantic-universe.rust.v2", uni)
    faults, bound = [], None
    try:
        adm = NC.admit_native_context(store, ctx_hex, inv)
        faults += adm["refusals"]
        bound = NC.bind_universe(store, U, {ctx_hex: adm}, inv)
        faults += bound["faults"]
    except NC.Refusal as exc:
        faults.append(f"{exc.key}:{exc.detail}" if exc.detail else exc.key)
    for label, rec, sel in (("prepared-output-set", prep, "#/$defs/PreparedOutputSetV3"), ("universe", uni, "#/$defs/RustUniverseV2ResolvedInputs")):
        r = KIT.admit(rec, NE, sel)
        if not r["ok"]:
            faults.insert(0, f"cb24.SCHEMA:{label}:{r['stock'][:1]}{r['order'][:1]}")
    return store, inv, ctx_hex, U, uni, bound, faults


def main():
    store, inv, ctx_hex, U, uni, bound, faults = build()
    out = {"classification": "valid", "languageMode": "rust-cargo-prepared", "contextId": "sha256:" + ctx_hex, "universeId": U,
           "admissionFaults": faults, "vectors": []}
    if faults:
        failures.append({"vector": "prepared-positive", "faults": faults})
    token = EN.LANGUAGE_MODES["rust-cargo-prepared"]
    cells = [c for c in EN.MATRIX["cells"] if c["mode"] == "rust-cargo-prepared"]
    out["cellObligation"] = {"policyUniverseToken": token, "universeDomain": EN.POLICY_UNIVERSE_MAP[token],
                             "matrixStates": {c["capability"]: [c["state"], c["deficiency"]] for c in cells},
                             "grantOperationForPreparedResolution": KIT.doc(ID)["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"]
                             ["native.semantic-universe.rust.v2"]["preparedResolutionGrantOperations"][uni["preparedResolution"]]}
    if bound is not None:
        f = {"schemaVersion": 2, "snapshotId": "snapshot2:" + "6" * 64, "relation": "declares", "resolution": "syntactic", "sourceUniverse": U, "targetUniverse": U,
             "producerClosure": "closure2:" + "7" * 64, "payloadSchemaDigest": KIT.digest(REL),
             "payloadDigest": store.put_record({"container": "rs:src/lib.rs", "declared": "rs:src/lib.rs#f", "declarationKind": "function"}),
             "anchors": [{"path": "src/lib.rs", "blobDigest": next(r["sha256"] for r in inv if r["path"] == "src/lib.rs"), "startByte": 31, "endByte": 55}],
             "confidenceMillionths": 1000000}
        ff, _ = NF.fact_faults(store, f, f["snapshotId"], inv, {U: bound})
        rec, lang, refusal = NC.body_language_version(bound, "src/lib.rs")
        out["vectors"].append({"vector": "declares-fact-under-prepared-universe", "faults": ff, "bodyLanguageVersion": rec, "refusal": refusal})
        if ff or refusal:
            failures.append({"vector": "prepared-fact", "faults": ff, "refusal": refusal})
    for label, kwargs, expect in (("non-inert-prepared-row", {"row_kind": "proc-macro-dylib"}, "native.prepared-output-not-inert"),
                                  ("resolution-none-with-prepared-set", {"resolution": "none"}, "native.universe-context-field-mismatch"),
                                  ("universe-omits-context-prepared-set", {"universe_set_null": True}, "native.universe-context-field-mismatch")):
        fl = build(**kwargs)[-1]
        ok = bool(fl) and fl[0].startswith(expect)
        if not ok:
            failures.append({"vector": label, "faults": fl, "expected": expect})
        out["vectors"].append({"vector": label, "classification": "invalid", "firstRefusal": fl[0] if fl else None, "masksLater": fl[1:], "expected": expect, "pass": ok})
    out["selectors"] = ["native-evidence.md s2.1/s3.6 PreparedOutputSetV3 inert rows", "identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.rust.v2",
                        "native-capability-matrix.v2.json cells mode rust-cargo-prepared"]
    out["assertionFailures"] = failures
    with open(OUT + "/vectors/mode-rust-cargo-prepared.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("faults", faults, "failures", json.dumps(failures)[:2000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
