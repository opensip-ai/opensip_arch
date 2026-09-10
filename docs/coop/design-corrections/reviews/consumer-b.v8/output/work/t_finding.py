import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL, run_finding

R = []
def check(name, mutate=None, expect=None):
    fx, A, run_id = run_finding.build_run(mutate)
    rep = CL.Closure(fx.s).close_run(run_id)
    first = rep["firstFault"]
    good = (first == expect) if expect else (first is None)
    R.append({"vector": name, "expectedFirstRefusal": expect,
              "observedFirstRefusal": first, "checks": rep["checks"],
              "faults": rep["faults"][:4], "runId": run_id,
              "findingId": A.extra["findingId"],
              "fingerprint": A.extra["fingerprint"]})
    print(("PASS " if good else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:130] if rep["faults"] else ""))
    return A

a = check("CB-FIND-POS a TRUE predicate emits a finding; the Run seals with "
          "verdict fail and the finding citations stay inside the closure")
print("  finding-key2:", a.extra["fingerprint"])
print("  finding2    :", a.extra["findingId"])
print("  discriminator (raw SHA-256 of C(ordered token array)):",
      a.extra["discriminator"])
check("CB-FIND-N1 a finding citing a fact outside the evaluated view",
      {"cite_unretained_fact": True}, "FINDING_FACT_OUTSIDE_EVALUATED_VIEW")
check("CB-FIND-N2 a finding citing a raw blob that is not an explicit blob input",
      {"cite_blob_not_an_input": True}, "FINDING_BLOB_NOT_AN_EXPLICIT_INPUT")
check("CB-FIND-N3 finding-parameters messageCode drifting from the finding's",
      {"finding_message_code_drift": True}, "FINDING_PARAMETER_MESSAGE_CODE")
check("CB-FIND-N4 a rule closure that is not of kind detector",
      {"rule_closure_is_provider": True}, "FINDING_RULE_CLOSURE_KIND")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-finding.json",
          "w") as f:
    json.dump({"vectors": R, "signatureTokens": a.extra["signatureTokens"],
               "discriminator": a.extra["discriminator"],
               "findingParameters": a.extra["findingParameters"]},
              f, indent=1, sort_keys=True)
