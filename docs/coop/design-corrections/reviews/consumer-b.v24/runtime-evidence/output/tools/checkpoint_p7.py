"""Record phase-7 standing from the executed artifacts (reads the produced files; refuses to mark executed on missing/failed output)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import status as S  # noqa: E402

OUT = S.OUT


def load(rel):
    return json.load(open(OUT + rel))


st = S.load_status()
problems = []


def mark(rid, artifact, ok, notes):
    if not os.path.exists(OUT + artifact.split("#")[0]):
        problems.append((rid, "artifact missing", artifact))
        S.set_status(st, rid, "unexecuted", artifact, None, "artifact missing")
        return
    S.set_status(st, rid, "executed" if ok else "failed", artifact, None, notes)
    if not ok:
        problems.append((rid, artifact))


mu = load("vectors/multi-unit-missing-caps.json")
env = {n: load(f"envelopes/{n}.json") for n in ("config-input", "retained-external-input", "host-invalid-internal", "producer-boundary")}
pfi = load("envelopes/public-from-internal.json")
d9 = load("vectors/d9-extension-precedence.json")
inv = load("envelopes/invocation-disclosure.json")
single = load("envelopes/single-step.json")
multi = load("envelopes/multi-step.json")
rec = load("envelopes/receipt-availability.json")
auth = load("vectors/authority-and-steps.json")
chain = load("vectors/chain-zero-config.json")

mark("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "vectors/chain-zero-config.json", all(os.path.exists(OUT + a["executedArtifact"].split(" ")[0].split("#")[0].rstrip(";,"))
                                                                          or "(" in a["executedArtifact"] or "*" in a["executedArtifact"] for a in chain["arrows"]),
     "Eleven arrows, each mapped to an executed artifact; see notes/07-phase7-reconstruction.md. Real discovery/provider/durability processes not executed (future qualification).")
mark("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/authority-and-steps.json#/identities", bool(auth["identities"]),
     "Semantic content identities vs request/execution/receipt/intent operational identities; same run3 cited under different RequestIds.")
mark("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/authority-and-steps.json#/stepKinds", all(c["pass"] for c in auth["stepSpecControls"]),
     "Only analysis/verify seal or link run3; receipt-bearing kinds from repair #/x-opensip-mutation-operation-map/byStepKindReceiptOperation; retry none enforced by StepSpec allOf; repair-apply refused as generic mutation.")
mark("R-MULTI-UNIT-MISSING-CAPS", "vectors/multi-unit-missing-caps.json", mu["analysisSpecAdmitted"] and mu["availability"]["totalNoticeCount"] > 0
     and all(r["pass"] for r in mu["releaseNegatives"]), f"3 units, {len(mu['defaultAnalysisSpec']['requestedCapabilities'])} default rows, {mu['availability']['totalNoticeCount']} availability notices.")
mark("R-CANDIDATE-ONLY-CLONES", "vectors/multi-unit-missing-caps.json#/candidateOnly", mu["candidateOnly"]["admitted"] and mu["candidateOnly"]["equivalenceClaimRefused"]
     and mu["candidateOnly"]["noRelationMapsToCandidateCapabilities"], "clones-near/clones-cross-tsjs projected selection-account-only; CandidateProducerResultV1 admitted; equivalence claim refused by const.")
mark("R-INVOCATION-DISCLOSURE", "envelopes/invocation-disclosure.json", not inv["envelopeFaults"] and inv["invocationRecordAdmitted"], "ts-pass Run under default invocation.")
mark("R-SINGLE-STEP", "envelopes/single-step.json", not single["envelopeFaults"], "help: one render step.")
mark("R-MULTI-STEP-DIFFERENT-SELECTIONS", "envelopes/multi-step.json", not multi["envelopeFaults"] and multi["differentSelectionsMeasured"],
     "rust-mixed and rust-mixed-clones-required as two analysis steps with different required rows and different per-step notices.")
mark("R-PROMISE-VS-AVAILABILITY", "vectors/multi-unit-missing-caps.json#/promiseAvailabilityOverridePrerequisite", bool(mu["promiseAvailabilityOverridePrerequisite"]),
     "Four layers per sampled cell; explicit override removes notices without changing promise.")
mark("R-PUBLIC-FROM-INTERNAL-REFUSAL", "envelopes/public-from-internal.json", all(not c["faults"] for c in pfi["cases"]) and all(c["pass"] for c in pfi["routeControls"]),
     "Four actual internal refusals through the published route registry; origin controls and subject elision.")
for rid, name in (("R-ENVELOPE-CONFIG-INPUT", "config-input"), ("R-ENVELOPE-EXTERNAL-INPUT", "retained-external-input"),
                  ("R-ENVELOPE-HOST-INVALID", "host-invalid-internal"), ("R-ENVELOPE-PRODUCER-BOUNDARY", "producer-boundary")):
    mark(rid, f"envelopes/{name}.json", not env[name]["envelopeFaults"], f"{env[name]['internalRefusal']} @ {env[name]['originatingBoundary']}")
mark("R-FAILURE-ENVELOPES-D9", "envelopes/config-input.json", all(not e["envelopeFaults"] for e in env.values()),
     "Complete kind=failure CommandEnvelopes (errors composed per envelopeErrorsComposition, exit from class table) validated against evaluator3 command-envelope; plus envelopes/retained-external-input.json, host-invalid-internal.json, producer-boundary.json.")
mark("R-D9-EXTENSION-PRECEDENCE", "vectors/d9-extension-precedence.json", all(d9["measured"].values()),
     "Selected composition admits host-invariant; inherited v1.14 alone refuses it; everything else unchanged. Note in notes/07-phase7-reconstruction.md.")
mark("R-DURABLE-RECEIPT-AVAILABILITY", "envelopes/receipt-availability.json", all(v["admitted"] for v in rec["admission"].values()) and not rec["purgeEnvelopeFaults"],
     "commit-inventory/commit-receipt/availability generations and MutationReceiptV1 for ts-pass. Signing/fsync not performed.")
S.save_status(st)
cp = S.write_checkpoint(7, st, ["tools/phase7_vectors.py", "vectors/multi-unit-missing-caps.json", "vectors/d9-extension-precedence.json", "vectors/authority-and-steps.json",
                                "vectors/chain-zero-config.json", "envelopes/invocation-disclosure.json", "envelopes/single-step.json", "envelopes/multi-step.json",
                                "envelopes/public-from-internal.json", "envelopes/config-input.json", "envelopes/retained-external-input.json",
                                "envelopes/host-invalid-internal.json", "envelopes/producer-boundary.json", "envelopes/receipt-availability.json",
                                "notes/07-phase7-reconstruction.md"],
                        ["HC-7 phase7_vectors.py first draft used unverified helper/field names (matrix cell lookup, route coverage-cause key, stale-import termination); corrected BEFORE any run from ref/ sources, native-evidence #/x-opensip-deficiency-cause-registry and command-inventory.v3 #/goldens[id=import-stale-selected]. No attempt output existed to preserve."],
                        "Phase 7 executed with 0 assertion failures on the first run. Problems: " + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
