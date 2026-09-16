"""Record phase-7 standing from the executed source39 artifacts (reads the produced files; refuses to mark executed on missing/failed output)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_source42 as HC  # noqa: E402
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
disc = load("vectors/discovery-membership.json")
rt = load("vectors/run-termination.json")
mut = load("runs/replay-all.summary.json")
mutation = {r["run"]: r for r in mut["replays"]}

arrows_ok = all(os.path.exists(OUT + a["executedArtifact"].split(" ")[0].split("#")[0].rstrip(";,")) or "(" in a["executedArtifact"] or "*" in a["executedArtifact"]
                for a in chain["arrows"])
mark("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "vectors/chain-zero-config.json",
     arrows_ok and not disc["assertionFailures"] and not rt["assertionFailures"]
     and (mutation.get("syntax-code~membership-reordered") or {}).get("firstFault", "").startswith("ENUMERATION_MEMBERSHIP_ORDER")
     # source41 (HC-39): U-4b.5 unitKind and U-0 root representation enforced at Run closure over the retained record
     and (mutation.get("syntax-code~unit-kind-other-family") or {}).get("firstFault", "").startswith("ENUMERATION_MEMBERSHIP_ORDER:unitKind-family")
     and (mutation.get("ts-pass~unit-kind-not-mode-projection") or {}).get("firstFault", "").startswith("ENUMERATION_MEMBERSHIP_ORDER:unitKind:")
     and (mutation.get("syntax-code~unit-root-external-sentinel") or {}).get("firstFault", "").startswith("ENUMERATION_MEMBERSHIP_UNIT_ROOT")
     # source42 (HC-47): discovery -> enumeration binding joins the U-1 unit to programEntry and the retained config-graph entry
     and (mutation.get("ts-pass~default-unit-program-entry") or {}).get("firstFault", "").startswith("ENUMERATION_BINDING_PROGRAM_ENTRY"),
     "Every arrow maps to an executed artifact (notes/07-phase7-reconstruction.md). Measured links: U-1 unit -> enumeration binding programEntry law "
     "(runs/ts-pass~default-unit-program-entry refuses ENUMERATION_BINDING_PROGRAM_ENTRY); U-0/U-1/U-4b/U-9 discovery, membership, "
     "effective-allowJs mode selection and zero-config selection (vectors/discovery-membership.json); retained membership enforcement at closure "
     "(runs/syntax-code~membership-reordered, ~unit-kind-other-family, ~unit-root-external-sentinel and ts-pass~unit-kind-not-mode-projection refuse); "
     "run termination by its owner (vectors/run-termination.json). Real discovery/provider/durability processes not executed (future qualification).")
mark("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/authority-and-steps.json#/identities", bool(auth["identities"]),
     "Semantic content identities vs request/execution/receipt/intent operational identities; same run3 cited under different RequestIds; a committed Run "
     "termination omits authority (vectors/run-termination.json#/hostComposition).")
mark("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/authority-and-steps.json#/stepKinds", all(c["pass"] for c in auth["stepSpecControls"]),
     "Only analysis/verify seal or link run3; receipt-bearing kinds from repair #/x-opensip-mutation-operation-map/byStepKindReceiptOperation; retry none "
     "enforced by StepSpec allOf; repair-apply refused as generic mutation.")
mark("R-MULTI-UNIT-MISSING-CAPS", "vectors/multi-unit-missing-caps.json", mu["analysisSpecAdmitted"] and mu["availability"]["totalNoticeCount"] > 0
     and all(r["pass"] for r in mu["releaseNegatives"]),
     f"{len(mu['units']) if 'units' in mu else 'multi'} units, {len(mu['defaultAnalysisSpec']['requestedCapabilities'])} default rows, "
     f"{mu['availability']['totalNoticeCount']} availability notices; U-9 zero-config fallback selection in vectors/discovery-membership.json#u9-zero-config-syntax-only.")
mark("R-CANDIDATE-ONLY-CLONES", "vectors/multi-unit-missing-caps.json#/candidateOnly", mu["candidateOnly"]["admitted"] and mu["candidateOnly"]["equivalenceClaimRefused"]
     and mu["candidateOnly"]["noRelationMapsToCandidateCapabilities"],
     "clones-near/clones-cross-tsjs projected selection-account-only; CandidateProducerResultV1 admitted; equivalence claim refused by const.")
mark("R-INVOCATION-DISCLOSURE", "envelopes/invocation-disclosure.json", not inv["envelopeFaults"] and inv["invocationRecordAdmitted"], "ts-pass Run under default invocation.")
mark("R-SINGLE-STEP", "envelopes/single-step.json", not single["envelopeFaults"], "help: one render step.")
mark("R-MULTI-STEP-DIFFERENT-SELECTIONS", "envelopes/multi-step.json", not multi["envelopeFaults"] and multi["differentSelectionsMeasured"],
     "rust-mixed and rust-mixed-clones-required as two analysis steps with different required rows and different per-step notices.")
mark("R-PROMISE-VS-AVAILABILITY", "vectors/multi-unit-missing-caps.json#/promiseAvailabilityOverridePrerequisite", bool(mu["promiseAvailabilityOverridePrerequisite"]),
     "Promise, installed availability, explicit override and semantic prerequisite kept distinct; explicit override removes notices without changing promise.")
mark("R-PUBLIC-FROM-INTERNAL-REFUSAL", "envelopes/public-from-internal.json", all(not c["faults"] for c in pfi["cases"]) and all(c["pass"] for c in pfi["routeControls"]),
     "Actual internal refusals through the published route registry; origin controls and subject elision.")
for rid, name in (("R-ENVELOPE-CONFIG-INPUT", "config-input"), ("R-ENVELOPE-EXTERNAL-INPUT", "retained-external-input"),
                  ("R-ENVELOPE-HOST-INVALID", "host-invalid-internal"), ("R-ENVELOPE-PRODUCER-BOUNDARY", "producer-boundary")):
    mark(rid, f"envelopes/{name}.json", not env[name]["envelopeFaults"], f"{env[name]['internalRefusal']} @ {env[name]['originatingBoundary']}")
mark("R-FAILURE-ENVELOPES-D9", "envelopes/config-input.json", all(not e["envelopeFaults"] for e in env.values()),
     "Complete kind=failure CommandEnvelopes (errors per envelopeErrorsComposition, exit from class table) validated against evaluator3 command-envelope; plus "
     "retained-external-input, host-invalid-internal and producer-boundary envelopes.")
mark("R-D9-EXTENSION-PRECEDENCE", "vectors/d9-extension-precedence.json", all(d9["measured"].values()) and not rt["assertionFailures"],
     "Selected composition admits host-invariant; inherited v1.14 alone refuses it; everything else unchanged. Source39 native s10 routes applied through "
     "codeMaps.deficiencyToReasonCode (vectors/run-termination.json#/causeBridge).")
mark("R-DURABLE-RECEIPT-AVAILABILITY", "envelopes/receipt-availability.json", all(v["admitted"] for v in rec["admission"].values()) and not rec["purgeEnvelopeFaults"],
     "commit-inventory/commit-receipt/availability generations and MutationReceiptV1 for ts-pass; receipt joins of run-termination s7.3 measured in "
     "vectors/run-termination.json. Signing/fsync not performed.")
S.save_status(st)
cp = S.write_checkpoint(7, st, ["tools/phase7_vectors.py", "tools/discovery_vectors.py", "tools/run_termination_vectors.py", "ref/run_termination.py",
                                "vectors/multi-unit-missing-caps.json", "vectors/d9-extension-precedence.json", "vectors/authority-and-steps.json",
                                "vectors/chain-zero-config.json", "vectors/discovery-membership.json", "vectors/run-termination.json",
                                "envelopes/invocation-disclosure.json", "envelopes/single-step.json", "envelopes/multi-step.json",
                                "envelopes/public-from-internal.json", "envelopes/config-input.json", "envelopes/retained-external-input.json",
                                "envelopes/host-invalid-internal.json", "envelopes/producer-boundary.json", "envelopes/receipt-availability.json",
                                "runs/replay-all.summary.json", "notes/07-phase7-reconstruction.md",
                                "logs/s42-fin-p4to9.3.phase7_vectors.log", "logs/s42-fin-disc.0.discovery_vectors.log", "logs/s42-fin-p4to9.8.run_termination_vectors.log",
                                "logs/s42-original-disc.0.discovery_vectors.log (unchanged tool failed on a source41 path: HC-49)",
                                "preserved/pre-s42/logs/s42-pre-p4to9.3.phase7_vectors.log (unchanged helpers)",
                                "preserved/pre-s42/logs/s42-pre-p4to9.8.run_termination_vectors.log (unchanged helpers)"],
                        HC.for_phase(7),
                        "Phase 7: phase7_vectors, discovery_vectors and run_termination_vectors re-executed in runtime source42.v1 on the source42 kit after "
                        "HC-47..HC-49; the unchanged helpers' runs are retained beside them. Problems: " + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
