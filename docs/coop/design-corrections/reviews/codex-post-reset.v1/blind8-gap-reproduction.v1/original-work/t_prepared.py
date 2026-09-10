import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL, osip, run_rust

R = []
def check(name, mutate=None, expect=None, store_mutate=None):
    fx, A, run_id = run_rust.build_run("lib", mutate, prepared=True)
    note = store_mutate(fx, A, run_id) if store_mutate else None
    rep = CL.Closure(fx.s).close_run(run_id)
    first = rep["firstFault"]
    good = (first == expect) if expect else (first is None)
    R.append({"vector": name, "expectedFirstRefusal": expect,
              "observedFirstRefusal": first, "checks": rep["checks"],
              "faults": rep["faults"][:4], "runId": run_id, "note": note})
    print(("PASS " if good else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:130] if rep["faults"] else ""))
    return fx, A, run_id

fx, A, run_id = check("CB-PREP-POS rust-cargo-prepared: an admitted "
                      "PreparedOutputSetV3 of INERT rows, host-prepared resolution, "
                      "and the prepare-code semantic-grant projection")
uni = [v for v in A.universes.values()][0][1]
print("  preparedResolution:", uni["preparedResolution"],
      "executionCapableResolution:", uni["executionCapableResolution"])
print("  preparedOutputSetId:", uni["preparedOutputSetId"])

def drop_prepare_code(fx, A, run_id):
    """imported-inert projects only read-import; only host-prepared projects
    prepare-code.  Here the grant drops prepare-code while the universe keeps
    host-prepared."""
    return None

# a NON-INERT prepared row must refuse regardless of the media type it claims
check("CB-PREP-N1 a proc-macro-dylib row relabelled with an inert media type",
      {"non_inert_row": True}, "native.prepared-output-not-inert")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-prepared.json",
          "w") as f:
    json.dump(R, f, indent=1, sort_keys=True)

check("CB-PREP-POS2 imported-inert projects only read-import: prepared bytes in "
      "custody never imply a host execution grant", {"imported_inert": True})
check("CB-PREP-N2 a trusted-repository-code principal projected under "
      "imported-inert", {"imported_inert": True, "false_repo_principal": True},
      "GRANT_PREPARE_CODE_PRINCIPAL_JOIN")
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-prepared.json",
          "w") as f:
    json.dump(R, f, indent=1, sort_keys=True)
