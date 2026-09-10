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
