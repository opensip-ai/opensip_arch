"""Vector group B: the mixed-edition Rust workspace - contexts, nested input
records and their H preimages, SourceUnitOwnershipV1 selection law, the same
physical file under two explicitly selected target editions, and a complete
minimal positive Rust Run descriptor graph."""
import sys, os, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import (S, V, PROJECT_ID, PLATFORM, blob, inv, closure, EVAL_CID)
from build_ts2 import (CapRegistry, CAP_MANIFEST, CAP_BYTES, CAP_ID, CAP_BYTES_DIGEST,
                       subject_scope, fact, snapshot_joins, coverage, entry,
                       NA_RC, CW_CLOSED)
import build_ts2 as B2
from build_ts3 import LEVEL_SPEC, body_identity_join

RSU = "native.semantic-universe.rust.v2"

# ---------------------------------------------------------------- Rust closures
rustc_b, _ = blob("bin/rustc", "RUSTC-EXE")
cargo_b, _ = blob("bin/cargo", "CARGO-EXE")
linker_b, _ = blob("bin/ld", "LINKER-EXE")
ar_b, _ = blob("bin/ar", "AR-EXE")
pms_b, _ = blob("bin/proc-macro-server", "PMS-EXE")
RS_TOOL_CID, RS_TOOL = closure("toolchain", [rustc_b, cargo_b, linker_b, ar_b, pms_b],
                               "1.83.0", 3, PLATFORM, b"RUST-TOOLCHAIN-MANIFEST-BODY")
llvm_b, _ = blob("lib/librustc_llvm.so", "LLVM-BYTES")
RS_LLVM_CID, RS_LLVM = closure("rust-dev-llvm", [llvm_b], "1.83.0", 3, PLATFORM,
                               b"RUST-DEV-LLVM-MANIFEST-BODY")
prov_rs, _ = blob("bin/provider-rust", "RUST-PROVIDER-BYTES")
RS_PROV_CID, RS_PROV = closure("provider", [prov_rs], "1.0.0", 3, PLATFORM,
                               b"RUST-PROVIDER-MANIFEST-BODY")

# ------------------------------------------------------------ repository R2
# Mixed-edition Cargo workspace. `tool#1` exercises a VALID `#` marker directory,
# which the withdrawn delimiter-joined unitId recipe would have had to forbid.
SHARED_RS = 'pub fn shared() -> u32 { let x = 1; x + 1 }\n'
r2 = {}
r2["Cargo.toml"], _ = blob("Cargo.toml", '[workspace]\nmembers=["crates/core","crates/legacy","tool#1"]\n')
r2["Cargo.lock"], _ = blob("Cargo.lock", 'version = 4\n[[package]]\nname="serde"\nversion="1.0.0"\n')
r2[".cargo/config.toml"], _ = blob(".cargo/config.toml", '[build]\nrustflags=["-C","opt-level=2"]\n')
r2["crates/core/Cargo.toml"], _ = blob("crates/core/Cargo.toml", '[package]\nname="core"\nedition="2021"\n')
r2["crates/core/src/lib.rs"], _ = blob("crates/core/src/lib.rs", 'pub mod shared;\n')
r2["crates/core/src/shared.rs"], _ = blob("crates/core/src/shared.rs", SHARED_RS)
r2["crates/legacy/Cargo.toml"], _ = blob("crates/legacy/Cargo.toml", '[package]\nname="legacy"\nedition="2015"\n')
r2["crates/legacy/src/lib.rs"], _ = blob("crates/legacy/src/lib.rs", 'pub fn old() -> u32 { let y = 2; y }\n')
r2["tool#1/Cargo.toml"], _ = blob("tool#1/Cargo.toml", '[package]\nname="tool1"\nedition="2024"\n')
r2["tool#1/src/main.rs"], _ = blob("tool#1/src/main.rs", 'fn main() { let z = 3; println!("{}", z); }\n')
R2_INV = inv(list(r2.values()))
R2_MAP = {r["path"]: r for r in R2_INV}

# ------------------------------------------------- nested semantic input records
DEP_FILES = [{"path": "src/lib.rs", "contentSha256": S.put_blob(b"pub fn de(){}\n", "serde src"),
              "byteLength": 14},
             {"path": "Cargo.toml", "contentSha256": S.put_blob(b'[package]\nname="serde"\n', "serde manifest"),
              "byteLength": 23}]
DEP_FILES = sorted(DEP_FILES, key=lambda r: r["path"].encode())
check_order(DEP_FILES, "path", "DependencyFileManifestV1")
DEP_MANIFEST_ID = S.put_framed("native.dependency-file-manifest.v1", DEP_FILES)

LOCKID = {"path": "Cargo.lock", "contentSha256": R2_MAP["Cargo.lock"]["sha256"],
          "lockfileVersion": 4}
DEPSET = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": LOCKID,
          "packages": [{"name": "serde", "version": "1.0.0", "sourceKind": "registry",
                        "sourceId": "registry+https://github.com/rust-lang/crates.io-index",
                        "lockChecksum": "ab" * 32,
                        "fileManifestSha256": DEP_MANIFEST_ID,
                        "fileCount": 2, "totalBytes": 37,
                        "acquisition": {"mode": "in-snapshot-vendored", "descriptorId": None,
                                        "vendorPath": "vendor/serde"},
                        "checksumVerification": "self-consistent",
                        "provenanceAssurance": "declared"}],
          "completeness": {"state": "complete", "missing": []}}
DEPSET_ID = "sha256:" + S.put_framed("native.dependency-source-set.v1", DEPSET)

UNIFIED = {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": "aarch64-apple-darwin",
           "activated": [{"packageKey": "serde 1.0.0", "features": ["std"]}],
           "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "adapter-1.0.0"}}
UNIFIED_ID = "sha256:" + S.put_framed("native.unified-features.rust.v1", UNIFIED)

PROJECTED_CONFIG_BYTES = b'[build]\nrustflags = ["-C", "opt-level=2"]\n'
PROJECTION = {"schemaVersion": 2,
              "honoredKeys": ["build.rustflags"],
              "strippedKeys": ["build.rustc", "target.aarch64-apple-darwin.linker"],
              "replacedSnapshotConfigs": [".cargo/config.toml"],
              "rustflags": {"honored": ["-C", "opt-level=2"], "stripped": [],
                            "executableSelected": False},
              "ancestorCarrierVerified": True, "cargoHome": "private-empty",
              "environmentProjection": "none", "claimsCargoSwitch": False,
              "projectionSha256": S.put_blob(PROJECTED_CONFIG_BYTES, "projected .cargo/config.toml")}
PROJECTION_H = S.put_framed("native.cargo-config-projection.v2", PROJECTION)

V["RS-DIG-1-three-distinct-configuration-digests"] = {
    "CargoConfigProjectionV2.projectionSha256 (raw digest of the projected FILE)":
        PROJECTION["projectionSha256"],
    "rust-v2.configProjectionSha256 (64-hex suffix of H over the whole RECORD)":
        PROJECTION_H,
    "raw SHA-256 of C(record)  [NEITHER of the above]": raw(PROJECTION),
    "allThreeDistinct": len({PROJECTION["projectionSha256"], PROJECTION_H, raw(PROJECTION)}) == 3,
    "snapshotJoin": "replacedSnapshotConfigs entries must be inventoried snapshot paths"}

V["RS-DIG-2-native-dependency-and-features-H-preimages"] = {
    "DependencyFileManifestV1 preimage (an ARRAY record)": DEP_FILES,
    "H domain": "native.dependency-file-manifest.v1",
    "fileManifestSha256 (bare hex)": DEP_MANIFEST_ID,
    "framePrefixHex": frame("native.dependency-file-manifest.v1", DEP_FILES)[:40].hex(),
    "DependencySourceSetV1 id (sha256-text)": DEPSET_ID,
    "UnifiedFeaturesV1 id (sha256-text)": UNIFIED_ID,
    "everyManifestMemberByteRetained": all(S.has(r["contentSha256"]) for r in DEP_FILES)}

# -------------------------------------------------------------- Rust context
def rust_context(prepared_id=None):
    return {"schemaVersion": 2, "targetTriple": "aarch64-apple-darwin",
            "hostTriple": "aarch64-apple-darwin",
            "toolchain": {"rustCommitHash": "5d" * 20, "rustcVersion": "1.83.0",
                          "cargoVersion": "1.83.0",
                          "sysrootDigest": S.put_blob(b"SYSROOT-TREE-MANIFEST", "sysroot"),
                          "rustcDevLlvmDigest": RS_LLVM_CID.split(":")[1],
                          "standardLibraryComponentDigests": [],
                          "targetTriple": "aarch64-apple-darwin"},
            "toolClosure": {"rustc": rustc_b["sha256"], "cargo": cargo_b["sha256"],
                            "linker": linker_b["sha256"], "ar": ar_b["sha256"],
                            "procMacroServer": pms_b["sha256"], "closureId": RS_TOOL_CID},
            "baseCfg": ["target_arch=\"aarch64\"", "unix"],
            "resolverVersion": 2, "dependencySourceSetId": DEPSET_ID,
            "unifiedFeaturesId": UNIFIED_ID, "preparedOutputSetId": prepared_id,
            "configProjection": PROJECTION}


def admit_rust_context(ctx, inventory):
    for cid, kind in ((ctx["toolClosure"]["closureId"], "toolchain"),
                      ("closure2:" + ctx["toolchain"]["rustcDevLlvmDigest"], "rust-dev-llvm")):
        d = cid.split(":")[1]
        if not S.has(d):
            raise Refuse("native.native-context-closure-unretained", cid)
        rec = S.reframe_check(d, "closure")
        if rec["kind"] != kind:
            raise Refuse("native.native-context-closure-kind-mismatch", cid)
        if H("closure", rec) != d:
            raise Refuse("native.native-context-closure-identity-mismatch", cid)
    tool = S.reframe_check(ctx["toolClosure"]["closureId"].split(":")[1], "closure")
    tree = {b["sha256"] for b in tool["tree"]}
    for f in ("rustc", "cargo", "linker", "ar", "procMacroServer"):
        if ctx["toolClosure"][f] is not None and ctx["toolClosure"][f] not in tree:
            raise Refuse("native.native-context-tool-not-in-closure", f)
    if ctx["toolchain"]["rustcVersion"] != tool["semanticVersion"]:
        raise Refuse("native.native-context-compiler-version-not-from-manifest",
                     ctx["toolchain"]["rustcVersion"])
    ip = {r["path"] for r in inventory}
    for p in ctx["configProjection"]["replacedSnapshotConfigs"]:
        if p not in ip:
            raise Refuse("native.native-context-config-path-outside-snapshot", p)
    if not S.has(ctx["configProjection"]["projectionSha256"]):
        raise Refuse("native.native-context-projection-unretained", "")
    for f, dom in (("dependencySourceSetId", "native.dependency-source-set.v1"),
                   ("unifiedFeaturesId", "native.unified-features.rust.v1"),
                   ("preparedOutputSetId", "native.prepared-output-set.v3")):
        v = ctx[f]
        if v is None:
            continue
        S.reframe_check(v.split(":")[1], dom)
    return {"language": "rust", "contextId": "sha256:" + H("native.context.rust.v2", ctx)}


def bind_rust_universe(u, admission, ctx, retained, inventory):
    if ctx is None or retained is None:
        raise Refuse("native.universe-retained-inputs-not-supplied", "")
    if admission["language"] != "rust":
        raise Refuse("native.native-context-language-mismatch", admission["language"])
    if u["nativeContextId"] != admission["contextId"]:
        raise Refuse("native.universe-context-binding-mismatch", u["nativeContextId"])
    if "sha256:" + H("native.context.rust.v2", ctx) != u["nativeContextId"]:
        raise Refuse("native.universe-context-binding-mismatch",
                     "context-bytes-are-not-the-admitted-ones")
    for f in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
        if u[f] != ctx[f]:
            raise Refuse("native.universe-context-field-mismatch", f)
    if u["rustflags"] != ctx["configProjection"]["rustflags"]:
        raise Refuse("native.universe-context-field-mismatch", "rustflags")
    if u["configProjectionSha256"] != H("native.cargo-config-projection.v2",
                                        ctx["configProjection"]):
        raise Refuse("native.universe-context-field-mismatch", "configProjectionSha256")
    if u["executionCapableResolution"] != (u["preparedResolution"] != "none"):
        raise Refuse("native.universe-context-field-mismatch", "executionCapableResolution")
    base = set(ctx["baseCfg"])
    seen = set()
    for s in u["cfgSets"]:
        if s["cfgSetId"] in seen:
            raise Refuse("native.universe-cfgset-duplicate", s["cfgSetId"])
        seen.add(s["cfgSetId"])
        if not base <= set(s["cfg"]):
            raise Refuse("native.universe-cfgset-drops-a-base-cfg", s["cfgSetId"])
    ds = retained.get("dependencySourceSet")
    if ds is None or "sha256:" + H("native.dependency-source-set.v1", ds) != u["dependencySourceSetId"]:
        raise Refuse("native.universe-retained-inputs-not-supplied", "dependencySourceSet")
    if ds["lockfileIdentity"] != u["lockfileIdentity"]:
        raise Refuse("native.universe-dependency-set-lockfile-mismatch", "")
    uf = retained.get("unifiedFeatures")
    if uf is None or "sha256:" + H("native.unified-features.rust.v1", uf) != u["unifiedFeaturesId"]:
        raise Refuse("native.universe-retained-inputs-not-supplied", "unifiedFeatures")
    if uf["targetTriple"] != ctx["targetTriple"] or uf["resolverVersion"] != ctx["resolverVersion"]:
        raise Refuse("native.universe-unified-features-context-mismatch", "")
    if u["preparedOutputSetId"] is None and retained.get("preparedOutputSet") is not None:
        raise Refuse("native.universe-prepared-set-retained-but-unselected", "")
    ip = {r["path"]: r for r in inventory}
    if u["lockfileIdentity"]["path"] not in ip or \
            ip[u["lockfileIdentity"]["path"]]["sha256"] != u["lockfileIdentity"]["contentSha256"]:
        raise Refuse("native.universe-lockfile-outside-snapshot", "")
    for p in u["crateRootPaths"]:
        if p not in ip:
            raise Refuse("native.universe-crate-root-not-inventoried", p)
    own = retained.get("sourceUnitOwnership")
    if u["sourceUnitOwnershipId"] is not None:
        if own is None or "sha256:" + H("native.source-unit-ownership.v1", own) != u["sourceUnitOwnershipId"]:
            raise Refuse("native.universe-retained-inputs-not-supplied", "sourceUnitOwnership")
        declared = {x["unitId"] for x in own["units"]}
        for x in own["units"]:
            if x["unitId"] != unit_id(x["markerPath"], x["targetKind"], x["targetName"]):
                raise Refuse("native.source-unit-id-not-derived", x["unitId"])
            if x["markerPath"] not in ip:
                raise Refuse("native.source-unit-marker-not-inventoried", x["markerPath"])
            if x["targetEdition"] is None and x["crateName"] not in u["edition"]:
                raise Refuse("native.source-unit-deferring-crate-not-in-edition-map", x["crateName"])
        if check_order(own["units"], {"by": ["unitId"]}, "units") is not True:
            raise Refuse("native.source-unit-order", "")
        if not own["selectedUnitIds"]:
            raise Refuse("native.source-unit-selection-empty", "")
        for s in own["selectedUnitIds"]:
            if s not in declared:
                raise Refuse("native.source-unit-selection-unbound", s)
        for o in own["ownership"]:
            if o["unitId"] not in declared:
                raise Refuse("native.source-unit-ownership-unbound", o["unitId"])
            if o["path"] not in ip:
                raise Refuse("native.source-unit-owned-path-not-inventoried", o["path"])
    return "sha256:" + H(RSU, u)


RS_CTX = rust_context()
RS_ADM = admit_rust_context(RS_CTX, R2_INV)
S.put_framed("native.context.rust.v2", RS_CTX)

# -------------------------------------------------- compilation-unit ownership
U_CORE_LIB = unit_id("crates/core/Cargo.toml", "lib", "core")
U_CORE_BIN = unit_id("crates/core/Cargo.toml", "bin", "coretool")
U_CORE_TEST = unit_id("crates/core/Cargo.toml", "test", "core_it")
U_LEGACY_LIB = unit_id("crates/legacy/Cargo.toml", "lib", "legacy")
U_TOOL1_BIN = unit_id("tool#1/Cargo.toml", "bin", "tool1")

UNITS = sorted([
    {"unitId": U_CORE_LIB, "markerPath": "crates/core/Cargo.toml", "crateName": "core",
     "targetKind": "lib", "targetName": "core", "targetEdition": None},
    {"unitId": U_CORE_BIN, "markerPath": "crates/core/Cargo.toml", "crateName": "core",
     "targetKind": "bin", "targetName": "coretool", "targetEdition": 2018},
    {"unitId": U_CORE_TEST, "markerPath": "crates/core/Cargo.toml", "crateName": "core",
     "targetKind": "test", "targetName": "core_it", "targetEdition": None},
    {"unitId": U_LEGACY_LIB, "markerPath": "crates/legacy/Cargo.toml", "crateName": "legacy",
     "targetKind": "lib", "targetName": "legacy", "targetEdition": None},
    {"unitId": U_TOOL1_BIN, "markerPath": "tool#1/Cargo.toml", "crateName": "tool1",
     "targetKind": "bin", "targetName": "tool1", "targetEdition": None},
], key=lambda u: u["unitId"])

OWNERSHIP_ROWS = sorted([
    {"path": "crates/core/src/lib.rs", "unitId": U_CORE_LIB},
    {"path": "crates/core/src/shared.rs", "unitId": U_CORE_LIB},
    {"path": "crates/core/src/shared.rs", "unitId": U_CORE_BIN},
    {"path": "crates/core/src/shared.rs", "unitId": U_CORE_TEST},
    {"path": "crates/legacy/src/lib.rs", "unitId": U_LEGACY_LIB},
    {"path": "tool#1/src/main.rs", "unitId": U_TOOL1_BIN},
], key=lambda o: (o["path"], o["unitId"]))

EDITION_MAP = {"core": 2021, "legacy": 2015, "tool1": 2024}


def ownership(selected, enumeration="complete", rows=None, units=None):
    rec = {"schemaVersion": 1, "enumeration": enumeration,
           "units": units if units is not None else UNITS,
           "selectedUnitIds": sorted(selected, key=lambda s: s.encode()),
           "ownership": rows if rows is not None else OWNERSHIP_ROWS}
    return rec, "sha256:" + S.put_framed("native.source-unit-ownership.v1", rec)


def rust_universe(own_id, selection_label):
    return {"schemaVersion": 2, "edition": EDITION_MAP, "lockfileIdentity": LOCKID,
            "dependencySourceSetId": DEPSET_ID, "unifiedFeaturesId": UNIFIED_ID,
            "nativeContextId": RS_ADM["contextId"],
            "cfgSets": [{"cfgSetId": "primary",
                         "cfg": ["target_arch=\"aarch64\"", "unix"]},
                        {"cfgSetId": "primary+test",
                         "cfg": ["target_arch=\"aarch64\"", "test", "unix"]}],
            "rustflags": PROJECTION["rustflags"],
            "crateRootPaths": sorted(["crates/core/src/lib.rs", "crates/legacy/src/lib.rs",
                                      "tool#1/src/main.rs"], key=lambda p: p.encode()),
            "configProjectionSha256": PROJECTION_H,
            "preparedResolution": "none", "executionCapableResolution": False,
            "preparedOutputSetId": None, "sourceUnitOwnershipId": own_id}


RETAINED = {"dependencySourceSet": DEPSET, "unifiedFeatures": UNIFIED}

# ---- selection A: the LIB target only (shared.rs -> package default 2021)
OWN_A, OWN_A_ID = ownership([U_CORE_LIB, U_LEGACY_LIB, U_TOOL1_BIN])
UNIV_A = rust_universe(OWN_A_ID, "lib-only")
UNIV_A_ID = bind_rust_universe(UNIV_A, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV)
S.put_framed(RSU, UNIV_A)

# ---- selection B: the BIN target only (shared.rs -> TARGET edition 2018)
OWN_B, OWN_B_ID = ownership([U_CORE_BIN, U_LEGACY_LIB, U_TOOL1_BIN])
UNIV_B = rust_universe(OWN_B_ID, "bin-only")
UNIV_B_ID = bind_rust_universe(UNIV_B, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_B), R2_INV)
S.put_framed(RSU, UNIV_B)

# ---- selection C: lib + test (BOTH defer to the package default: SAME dialect)
OWN_C, OWN_C_ID = ownership([U_CORE_LIB, U_CORE_TEST, U_LEGACY_LIB, U_TOOL1_BIN])
UNIV_C = rust_universe(OWN_C_ID, "lib+test")
UNIV_C_ID = bind_rust_universe(UNIV_C, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_C), R2_INV)
S.put_framed(RSU, UNIV_C)

# ---- selection D: lib + bin  (editions DISAGREE -> ambiguous)
OWN_D, OWN_D_ID = ownership([U_CORE_LIB, U_CORE_BIN])
UNIV_D = rust_universe(OWN_D_ID, "lib+bin")
UNIV_D_ID = bind_rust_universe(UNIV_D, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_D), R2_INV)

# ---- selection E: partial enumeration
OWN_E, OWN_E_ID = ownership([U_CORE_LIB], enumeration="partial")
UNIV_E = rust_universe(OWN_E_ID, "partial")
UNIV_E_ID = bind_rust_universe(UNIV_E, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_E), R2_INV)

# ---- selection F: no committed ownership at all
UNIV_F = rust_universe(None, "no-ownership")
UNIV_F_ID = bind_rust_universe(UNIV_F, RS_ADM, RS_CTX, dict(RETAINED), R2_INV)


def rs_body(universe, own, path, span, level="L0-verbatim"):
    src = S.cas[R2_MAP[path]["sha256"]]
    blv = body_language_version(RSU, RS_CTX, universe, path, own)
    payload = l0_payload(src[span[0]:span[1]])
    bid, fr = body_identity(level, LEVEL_SPEC[level], blv["languageId"], blv, payload)
    S.put_blob(fr, "body frame " + path)
    return bid, blv, fr


SHARED_SPAN = (SHARED_RS.index("{"), len(SHARED_RS.rstrip("\n")))
BID_A, BLV_A, _ = rs_body(UNIV_A, OWN_A, "crates/core/src/shared.rs", SHARED_SPAN)
BID_B, BLV_B, _ = rs_body(UNIV_B, OWN_B, "crates/core/src/shared.rs", SHARED_SPAN)
BID_C, BLV_C, _ = rs_body(UNIV_C, OWN_C, "crates/core/src/shared.rs", SHARED_SPAN)

V["RS-OWN-1-same-physical-file-under-two-explicitly-selected-target-editions"] = {
    "path": "crates/core/src/shared.rs",
    "packageDefaultEdition": EDITION_MAP["core"],
    "selectionA_units": ["lib core (targetEdition null -> package default)"],
    "selectionA_dialect": BLV_A["dialect"], "selectionA_bodyIdentity": BID_A,
    "selectionA_sourceUniverse": UNIV_A_ID,
    "selectionB_units": ["bin coretool (targetEdition 2018 OVERRIDES the package default)"],
    "selectionB_dialect": BLV_B["dialect"], "selectionB_bodyIdentity": BID_B,
    "selectionB_sourceUniverse": UNIV_B_ID,
    "twoSelectionsAreTwoUniverses": UNIV_A_ID != UNIV_B_ID,
    "twoEditionsAreTwoBodyIdentities": BID_A != BID_B,
    "noRelationPayloadChanged": True,
    "law": "native sec.11: there is NO single-edition fast path; a package map whose "
           "values all agree still does not determine a body's dialect, because Cargo "
           "lets a target override its package edition."}

V["RS-OWN-2-body-identity-is-stable-when-only-the-selection-changes"] = {
    "selectionA": ["lib core"], "selectionC": ["lib core", "test core_it"],
    "bothDeferToPackageDefault": True,
    "dialectA": BLV_A["dialect"], "dialectC": BLV_C["dialect"],
    "bodyIdentityUnchanged": BID_A == BID_C,
    "sourceUniverseChanged": UNIV_A_ID != UNIV_C_ID,
    "factIdentityWouldChange": "yes - fact2 binds sourceUniverse; bodyIdentity does not",
    "law": "Selection establishes the JOIN only: no path, crate name, unit id or "
           "selection enters body-language-version."}

# ---------------------------------------------- the ownership selection refusals
OWN_NEG = {}


def own_neg(name, universe, own, path):
    try:
        rs_body(universe, own, path, SHARED_SPAN)
        OWN_NEG[name] = "NOT-REFUSED (defect)"
    except Refuse as e:
        OWN_NEG[name] = str(e)


own_neg("RS-N1-selected-owners-disagree-on-effective-edition", UNIV_D, OWN_D,
        "crates/core/src/shared.rs")
own_neg("RS-N2-partial-enumeration-refuses-BEFORE-any-row-is-read", UNIV_E, OWN_E,
        "crates/core/src/shared.rs")
own_neg("RS-N3-no-committed-ownership-relation-at-all", UNIV_F, None,
        "crates/core/src/shared.rs")
try:
    rs_body(UNIV_A, OWN_A, "crates/legacy/src/lib.rs", (0, 10))
    OWN_NEG["RS-N4-path-owned-only-by-unselected-targets"] = "admitted (legacy IS selected in A)"
except Refuse as e:
    OWN_NEG["RS-N4-path-owned-only-by-unselected-targets"] = str(e)
OWN_D2, OWN_D2_ID = ownership([U_CORE_LIB])
UNIV_D2 = rust_universe(OWN_D2_ID, "lib-only-narrow")
bind_rust_universe(UNIV_D2, RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_D2), R2_INV)
own_neg2 = None
try:
    rs_body(UNIV_D2, OWN_D2, "tool#1/src/main.rs", (10, 20))
    OWN_NEG["RS-N5-path-owned-only-by-an-unselected-target"] = "NOT-REFUSED (defect)"
except Refuse as e:
    OWN_NEG["RS-N5-path-owned-only-by-an-unselected-target"] = str(e)
try:
    rs_body(UNIV_A, OWN_A, "Cargo.lock", (0, 5))
    OWN_NEG["RS-N6-path-with-no-ownership-row-at-all"] = "NOT-REFUSED (defect)"
except Refuse as e:
    OWN_NEG["RS-N6-path-with-no-ownership-row-at-all"] = str(e)
V["RS-OWNERSHIP-NEGATIVES"] = OWN_NEG

# --------------------------------------------------- the `#` marker directory
BID_T1, BLV_T1, _ = rs_body(UNIV_A, OWN_A, "tool#1/src/main.rs",
                            (len('fn main() '), len('fn main() { let z = 3; println!("{}", z); }')))
V["RS-UNIT-1-hash-marker-directory-closes-a-complete-run"] = {
    "markerPath": "tool#1/Cargo.toml",
    "unitIdPreimage": {"schemaVersion": 1, "markerPath": "tool#1/Cargo.toml",
                       "targetKind": "bin", "targetName": "tool1"},
    "unitId": U_TOOL1_BIN,
    "domain": "native.compilation-unit.v1",
    "retention": "derived - the preimage IS the unit row; admission re-derives and compares",
    "bodyIdentity": BID_T1, "dialect": BLV_T1["dialect"],
    "withdrawnDelimiterRecipeWouldHaveHadToForbidHashInAPath": True}

# ---------------------------------------- representative LARGE edition map
BIG_MAP = {f"crate_{i:02d}_with_a_reasonably_long_name": (2015, 2018, 2021, 2024)[i % 4]
           for i in range(21)}
_raw_map_bytes = C(BIG_MAP)
V["RS-EDITION-1-representative-large-edition-map-and-the-u8-component-bound"] = {
    "crateCount": len(BIG_MAP),
    "canonicalMapByteLength": len(_raw_map_bytes),
    "u8ComponentMaximum": 255,
    "embeddingTheMapIsUnrepresentable": len(_raw_map_bytes) > 255,
    "whatIsCarriedInstead": "the SELECTED value only: dialect {edition: <year>}",
    "languageVersionComponentWidth": 32,
    "note": "The frame gives every component a u8 length, so a component built by "
            "embedding per-crate data is not representable for ordinary valid inputs. "
            "The bounded version component is derived from the exact ADMITTED compiler "
            "context (rustcVersion/rustCommitHash joined to the tool closure manifest) "
            "plus the body-provenance dialect, hashed to a fixed 32 bytes."}
