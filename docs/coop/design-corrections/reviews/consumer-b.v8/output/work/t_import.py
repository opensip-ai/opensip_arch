import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import run_import
import schemas

R = []
FAIL = []


def check(name, mutate=None, expect=None):
    fx, A, run_id = run_import.build_run(mutate)
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    first = rep["firstFault"]
    good = (first == expect) if expect else (first is None)
    if not good:
        FAIL.append(name)
    R.append({"vector": name, "expectedFirstRefusal": expect,
              "observedFirstRefusal": first, "checks": rep["checks"],
              "faults": rep["faults"][:4], "runId": run_id,
              "importId": A.extra["importId"]})
    print(("PASS " if good else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:130] if rep["faults"] else ""))
    return A


a = check("CB-IMP-POS a Run with an admitted registered runtime import2")
print("  importId:", a.extra["importId"])
check("CB-IMP-N1 an unregistered payload schema digest",
      {"unregistered_payload_schema": True}, "IMPORT.PAYLOAD_SCHEMA_UNREGISTERED")
check("CB-IMP-N2 a commit name alone never maps (source mapping is mandatory)",
      {"commit_name_alone": True}, "IMPORT.SOURCE_MAPPING_REQUIRED")
check("CB-IMP-N3 completeness != complete requires non-empty omissions",
      {"incomplete_without_omissions": True}, "IMPORT_INCOMPLETE_WITHOUT_OMISSIONS")
check("CB-IMP-N4 the adapter closure must be of kind adapter",
      {"adapter_closure_is_provider": True}, "IMPORT_CLOSURE_KIND")
try:
    run_import.build_run({"hits_on_unmapped": True})
    print("FAIL CB-IMP-N5"); FAIL.append("CB-IMP-N5")
except AssertionError as e:
    print("PASS CB-IMP-N5 a hit count on an UNMAPPED subject never becomes an "
          "admissible payload ->", str(e)[:150])
    R.append({"vector": "CB-IMP-N5 hits on an unmapped subject",
              "expectedFirstRefusal": "payload schema admission",
              "observedFirstRefusal": "IMPORT_PAYLOAD_SCHEMA (at construction)",
              "detail": str(e)[:300]})

# ---- the imported-observation boundary, stated ---------------------------
law = schemas.LOADED["imported-evidence"]["x-opensip-imported-requirement-law"]
print()
print("imported-requirement law keys:", list(law.keys())[:12])
reg = schemas.LOADED["imported-evidence"]["x-opensip-evidence-relation-registry"]
print("imported evidence relations:", json.dumps(reg, sort_keys=True)[:400])

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-import.json", "w") as f:
    json.dump({"vectors": R, "wrapper": a.extra["wrapper"],
               "payload": a.extra["payload"],
               "correspondence": a.extra["correspondence"],
               "observation": a.extra["observation"]}, f, indent=1, sort_keys=True)
print()
print("FAILURES:", FAIL or "none")
