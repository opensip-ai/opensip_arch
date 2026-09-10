import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import run_ts_config

results = []


def check(name, shape, mutate=None, expect=None):
    fx, A, run_id = run_ts_config.build_run(shape, mutate)
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    first = rep["firstFault"]
    ok = (first == expect) if expect else (first is None)
    results.append({"vector": name, "shape": shape,
                    "expectedFirstRefusal": expect, "observedFirstRefusal": first,
                    "checks": rep["checks"], "faults": rep["faults"][:4],
                    "tsconfigGraphHash": A.extra["tsconfigGraphHash"],
                    "configOrigin": A.extra["configOrigin"],
                    "entryConfigPath": A.extra["entry"],
                    "nodes": A.extra["nodes"], "sourceUniverse": A.extra["universeHex"]})
    print(("PASS " if ok else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:120] if rep["faults"] else ""))
    return A


a = check("CB-CFG-1 synthesized configuration (no tsconfig/jsconfig)", "synthesized")
b = check("CB-CFG-2 explicitly selected CUSTOM-NAMED config, multiple ORDERED "
          "bases incl. a REPEATED base", "custom-multibase")
c = check("CB-CFG-3 jsconfig inheriting a shared base with another filename",
          "jsconfig-shared")

print()
print("CB-CFG-2 entry kind:",
      [n["kind"] for n in b.extra["nodes"] if n["path"] == b.extra["entry"]][0],
      "-> configOrigin", b.extra["configOrigin"])
print("CB-CFG-2 extendsResolved:",
      [n["extendsResolved"] for n in b.extra["nodes"]
       if n["path"] == b.extra["entry"]][0])
print("CB-CFG-3 entry kind:",
      [n["kind"] for n in c.extra["nodes"] if n["path"] == c.extra["entry"]][0],
      "-> configOrigin", c.extra["configOrigin"])
print("CB-CFG-3 base kind (base.settings.json):",
      [n["kind"] for n in c.extra["nodes"] if n["path"] == "base.settings.json"][0])

d = check("CB-CFG-N1 dropping the REPEATED base moves tsconfigGraphHash "
          "(and therefore the universe)", "custom-multibase",
          {"drop_repeated_base": True})
assert d.extra["tsconfigGraphHash"] != b.extra["tsconfigGraphHash"]
assert d.extra["universeHex"] != b.extra["universeHex"]
print("PASS CB-CFG-N1 repeated-base precedence is retained IN THE IDENTITY:",
      b.extra["tsconfigGraphHash"][:16], "vs", d.extra["tsconfigGraphHash"][:16])

check("CB-CFG-N2 custom-named entry relabelled 'tsconfig'", "custom-multibase",
      {"claim_tsconfig_kind": True}, "native.config-graph-kind-contradicts-path")
check("CB-CFG-N3 a jsconfig entry asserting configOrigin tsconfig",
      "jsconfig-shared", {"assert_configorigin_tsconfig_on_jsconfig": True},
      "native.universe-config-origin-not-derived")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-typescript-config.json", "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)
