import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import run_rust

results = []
extras = {}


def check(name, selection="lib", mutate=None, expect=None, store_mutate=None):
    fx, A, run_id = run_rust.build_run(selection, mutate)
    note = None
    if store_mutate:
        note = store_mutate(fx, A, run_id)
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    first = rep["firstFault"]
    ok = (first == expect) if expect else (first is None)
    extras[name] = A.extra
    results.append({"vector": name, "selection": selection,
                    "expectedFirstRefusal": expect, "observedFirstRefusal": first,
                    "checks": rep["checks"], "faultCount": len(rep["faults"]),
                    "faults": rep["faults"][:6],
                    "runId": run_id, "bodyIdentity": A.extra["bodyIdentity"],
                    "sourceUniverse": A.extra["universeHex"], "note": note})
    print(("PASS " if ok else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:130] if rep["faults"] else ""))
    return A


a_lib = check("CB-RS-POS1 selection=lib (package default edition 2021)", "lib")
a_test = check("CB-RS-POS2 same physical file, selection=test target edition 2024",
               "test2024")
a_libbin = check("CB-RS-POS3 selection widened by an unrelated target; dialect unchanged",
                 "lib+bin")
check("CB-RS-POS4 ambiguous SELECTED owners: no body, disclosed pair", "ambiguous")
check("CB-RS-POS5 partial enumeration: no body, disclosed pair", "partial")
check("CB-RS-POS6 no committed ownership: no clone admissible", "none")

print()
print("selection=lib      edition ->", a_lib.extra["bodyLanguageVersion"]["dialect"])
print("selection=test2024 edition ->", a_test.extra["bodyLanguageVersion"]["dialect"])
print("bodyIdentity lib      ", a_lib.extra["bodyIdentity"])
print("bodyIdentity test2024 ", a_test.extra["bodyIdentity"])
print("bodyIdentity lib+bin  ", a_libbin.extra["bodyIdentity"])
assert a_lib.extra["bodyIdentity"] != a_test.extra["bodyIdentity"], \
    "two editions must mint two body identities"
assert a_lib.extra["bodyIdentity"] == a_libbin.extra["bodyIdentity"], \
    "a selection change that does not change the EFFECTIVE dialect must not move it"
assert a_lib.extra["universeHex"] != a_libbin.extra["universeHex"], \
    "a different selection is a different sourceUniverse"
print("PASS CB-RS-STABLE body identity stable across a selection-only change,",
      "while sourceUniverse moves")
print("PASS CB-RS-EDITION-MAP entries:", a_lib.extra["editionMapSize"],
      "raw map bytes:",
      len(str(sorted(run_rust.LARGE_EDITIONS.items())).encode()))

print()
check("CB-RS-N1 false complete under partial ownership", "partial",
      {"false_complete_under_partial_ownership": True}, "COVERAGE_DIALECT_PREREQUISITE")
check("CB-RS-N2 undisclosed null deficiency under ambiguous ownership", "ambiguous",
      {"undisclosed_null_deficiency": True}, "COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED")
check("CB-RS-N3 wrong cause under ambiguous ownership", "ambiguous",
      {"wrong_cause": True}, "COVERAGE_DIALECT_CAUSE_MISMATCH")
check("CB-RS-N4 unrelated budget-exhausted deficiency under partial ownership",
      "partial", {"unrelated_budget_deficiency": True},
      "COVERAGE_DIALECT_DEFICIENCY_MISMATCH")
check("CB-RS-N5 cfg set dropping a base cfg", "lib", {"cfgset_drops_base": True},
      "native.universe-cfgset-drops-base-cfg")
check("CB-RS-N6 crate root path outside the analysed snapshot", "lib",
      {"crate_root_outside_snapshot": True}, "UNIVERSE_PATH_OUTSIDE_SNAPSHOT")


def drop_dep_member(fx, A, run_id):
    import osip
    dom, dss = osip.parse_frame(fx.s.blobs[A.contexts[A.extra["contextHex"]][1]
                                           ["dependencySourceSetId"].split(":")[1]])
    fmh = dss["packages"][0]["fileManifestSha256"]
    _, rows = osip.parse_frame(fx.s.blobs[fmh])
    del fx.s.blobs[rows[0]["contentSha256"]]
    return "a dependency package's file-manifest member bytes dropped"


check("CB-RS-N7 dependency file-manifest member bytes not retained", "lib",
      None, "EVIDENCE_UNAVAILABLE", drop_dep_member)

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-rust-run.json",
          "w") as f:
    json.dump({"vectors": results,
               "bodyIdentityLib": a_lib.extra["bodyIdentity"],
               "bodyIdentityTest2024": a_test.extra["bodyIdentity"],
               "bodyIdentityLibBin": a_libbin.extra["bodyIdentity"],
               "bodyLanguageVersionLib": a_lib.extra["bodyLanguageVersion"],
               "bodyLanguageVersionTest2024": a_test.extra["bodyLanguageVersion"],
               "unitIds": a_lib.extra["unitIds"],
               "editionMap": run_rust.LARGE_EDITIONS}, f, indent=1, sort_keys=True)


# ---- one refused hidden input, and the native H preimages, for Rust --------
print()
import osip


def hidden_rust_context(fx, A, run_id):
    desc = dict(A.contexts[A.extra["contextHex"]][1])
    desc["hostTriple"] = "aarch64-unknown-linux-gnu"
    fx.s.put_h("native.context.rust.v2", desc)
    return "a second hash-valid Rust context no Plan selected"


check("CB-RS-N8 hidden hash-valid Rust context outside plan.nativeContextDigests",
      "lib", None, "PLAN_CONTEXT_SET_MISMATCH", hidden_rust_context)


def mismatched_nested(fx, A, run_id):
    ctx = A.contexts[A.extra["contextHex"]][1]
    dom, dss = osip.parse_frame(fx.s.blobs[ctx["dependencySourceSetId"].split(":")[1]])
    d2 = dict(dss)
    d2["lockfileIdentity"] = dict(d2["lockfileIdentity"])
    d2["lockfileIdentity"]["lockfileVersion"] = 4
    fx.s.blobs[ctx["dependencySourceSetId"].split(":")[1]] = osip.frame(dom, d2)
    return "the retained DependencySourceSetV1 frame edited under its own identity"


check("CB-RS-N9 a nested dependency record that is not the exact H identity of "
      "the retained record of its registered domain", "lib", None,
      "H_IDENTITY_MISMATCH", mismatched_nested)

# the exact native H preimages, computed from the published recipes
fx, A, run_id = run_rust.build_run("lib")
ctx = A.contexts[A.extra["contextHex"]][1]
preimages = {}
for label, domain, ref in [
    ("DependencySourceSetV1", "native.dependency-source-set.v1",
     ctx["dependencySourceSetId"]),
    ("UnifiedFeaturesV1", "native.unified-features.rust.v1", ctx["unifiedFeaturesId"]),
]:
    hexd = ref.split(":")[1]
    fr = fx.s.blobs[hexd]
    d, val = osip.parse_frame(fr)
    assert d == domain and osip.raw_sha256(fr) == hexd
    preimages[label] = {"domain": domain, "identity": ref,
                        "framePrefixHex": fr[:64].hex(),
                        "frameBytes": len(fr),
                        "recomputed": "sha256:" + osip.H(domain, val)}
    print("PASS CB-RS-H %s preimage frame re-hashes to its identity" % label)
fmh = osip.parse_frame(fx.s.blobs[ctx["dependencySourceSetId"].split(":")[1]])[1][
    "packages"][0]["fileManifestSha256"]
d, rows = osip.parse_frame(fx.s.blobs[fmh])
preimages["DependencyFileManifestV1"] = {
    "domain": d, "bareHexIdentity": fmh,
    "recomputed": osip.H(d, rows), "rows": rows}
print("PASS CB-RS-H DependencyFileManifestV1 bare-hex identity re-derives:",
      osip.H(d, rows) == fmh)
cp = ctx["configProjection"]
preimages["CargoConfigProjectionV2"] = {
    "projectionSha256 (raw SHA-256 of the projected .cargo/config.toml FILE)":
        cp["projectionSha256"],
    "configProjectionSha256 (64-hex suffix of H(native.cargo-config-projection.v2, "
    "record))": osip.H("native.cargo-config-projection.v2", cp),
    "rawSha256OfCanonicalRecord (NEITHER of the two)": osip.raw_sha256(osip.C(cp)),
}
three = set(preimages["CargoConfigProjectionV2"].values())
print("PASS CB-RS-H the three cargo-config digests are pairwise distinct:",
      len(three) == 3)
u = A.extra["unitIds"]["lib"]
print("PASS CB-RS-H unitId is DERIVED from the published four-field preimage:",
      u == run_rust.unit_id("crates/core/Cargo.toml", "lib", "cb_core"))
preimages["UnitIdentityV1"] = {
    "preimage": {"schemaVersion": 1, "markerPath": "crates/core/Cargo.toml",
                 "targetKind": "lib", "targetName": "cb_core"},
    "domain": "native.compilation-unit.v1", "unitId": u}
preimages["markerDirectoryWithHash"] = {
    "markerPath": "crates/tools#gen/Cargo.toml",
    "unitId": A.extra["unitIds"]["bin"],
    "note": "H needs no delimiter, so a `#` in a repository directory closes a "
            "complete Run; the withdrawn delimiter recipe would have had to "
            "forbid it"}
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-rust-preimages.json", "w") as f:
    json.dump(preimages, f, indent=1, sort_keys=True)
