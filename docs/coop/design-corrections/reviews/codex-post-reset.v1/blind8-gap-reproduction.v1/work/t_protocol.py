import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import protocol as P

RESULTS = []
FAIL = []


def ok(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" -> " + str(detail)[:180])
                                                   if detail else ""))
    if not cond:
        FAIL.append(name)


def trace(name, events, stage_count=1, expect_phase=None, expect_terminal=None,
          expect_trace_tail=None):
    m = P.Machine(stage_count).run(events)
    a = P.stage_authority(m)
    good = True
    if expect_phase:
        good &= m.s["phase"] == expect_phase
    if expect_terminal is not None:
        good &= m.s["terminalKind"] == expect_terminal
    if expect_trace_tail:
        good &= m.trace[-len(expect_trace_tail):] == expect_trace_tail
    RESULTS.append({"vector": name,
                    "events": [e if isinstance(e, str) else e[0] for e in events],
                    "trace": m.trace, "finalPhase": m.s["phase"],
                    "terminalKind": m.s["terminalKind"],
                    "sourceBytesSent": m.s["sourceBytesSent"],
                    "identityNegotiated": m.s["identityNegotiated"],
                    "stagesCompleted": m.s["stagesCompleted"],
                    "stageAuthority": a})
    ok(name, good, "%s / %s / %s" % (m.s["phase"], m.s["terminalKind"], m.trace))
    return m


ok("CB-P3-0 the published rows are pairwise disjoint (first-match resolves "
   "no ambiguity today)", P.pairwise_disjoint() == [], P.pairwise_disjoint())

FULL_CAPS = {"capabilities": P.IDENTITY_TOKENS + ["sealed-vfs-v1",
                                                  "multi-stage-analyze-v1",
                                                  "rust-semantic-facts-v1",
                                                  "resolution-completeness-v2",
                                                  "unresolved-edge-v1",
                                                  "dependency-source-v1",
                                                  "native-context-v2"]}
DEP = {"dependencyMode": True, "preparedMode": False}
NODEP = {"dependencyMode": False, "preparedMode": False}
PREP = {"dependencyMode": True, "preparedMode": True}

COMPLETE = [
    "Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", DEP), "UniverseAccepted",
    "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "SnapshotAccepted",
    "DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal",
    "DependencySourceAccepted", "NativeContextVerified", "Analyze",
    "FactBatch", "CoverageV3", "Complete", "zero-exit", "eof"]
trace("CB-P3-1 complete valid Rust trace (dependency mode)", COMPLETE,
      1, "DONE", "complete", ["P3-27", "P3-31", "P3-32"])

trace("CB-P3-2 prepared mode routes through the prepared frames",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", PREP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "DependencySourceManifest", "DependencySourceSeal", "DependencySourceAccepted",
       "PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal",
       "PreparedOutputAccepted", "NativeContextVerified", "Analyze", "CoverageV3",
       "Complete", "zero-exit", "eof"], 1, "DONE", "complete")

trace("CB-P3-3 no dependency and no prepared mode goes straight to context "
      "verification", ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP),
                       "UniverseAccepted", "SnapshotManifest", "SnapshotSeal",
                       "SnapshotAccepted", "NativeContextVerified", "Analyze",
                       "CoverageV3", "Complete", "zero-exit", "eof"],
      1, "DONE", "complete")

# --- identity negotiation BEFORE source disclosure -------------------------
m = trace("CB-P3-4 OpenUniverse before Hello/HelloAck faults with NO source byte "
          "sent", [("OpenUniverse", DEP)], 1, "FAULT", None, ["P3-34"])
ok("CB-P3-4a sourceBytesSent is false", m.s["sourceBytesSent"] is False)

m = trace("CB-P3-5 a HelloAck lacking an identity token leaves identityNegotiated "
          "false, so OpenUniverse is unreachable and no source byte is sent",
          ["Hello", ("HelloAck", {"capabilities": ["sealed-vfs-v1"]}),
           ("OpenUniverse", DEP)], 1, "FAULT", None, ["P3-34"])
ok("CB-P3-5a identityNegotiated false, sourceBytesSent false",
   m.s["identityNegotiated"] is False and m.s["sourceBytesSent"] is False)

# --- unavailable ------------------------------------------------------------
trace("CB-P3-6 Unavailable(native-context-mismatch) BEFORE Analyze is a clean "
      "typed terminal", ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP),
                         "UniverseAccepted", "SnapshotManifest", "SnapshotSeal",
                         "SnapshotAccepted", "Unavailable", "zero-exit", "eof"],
      1, "DONE", "unavailable", ["P3-21", "P3-31", "P3-32"])
trace("CB-P3-7 Unavailable DURING Analyze: facts before the terminal are "
      "admitted and the stage is partial",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "FactBatch", "Unavailable",
       "zero-exit", "eof"], 1, "DONE", "unavailable")
trace("CB-P3-8 BudgetExhausted is the other clean typed terminal",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "FactBatch", "BudgetExhausted",
       "zero-exit", "eof"], 1, "DONE", "budget-exhausted")

# --- cancellation -----------------------------------------------------------
trace("CB-P3-9 cancellation: Cancel -> Cancelled -> terminal, then the process "
      "is still observed to zero-exit and EOF",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "Cancel", "Cancelled", "zero-exit",
       "eof"], 1, "DONE", "cancelled", ["P3-29", "P3-30", "P3-31", "P3-32"])

# --- fault ------------------------------------------------------------------
trace("CB-P3-10 ProviderFault mid-analysis: no facts, no Coverage, no Run",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "FactBatch", "ProviderFault",
       "zero-exit", "eof"], 1, "DONE", "provider-fault")
trace("CB-P3-11 an out-of-band PROCESS fault goes to FAULT from any phase",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "nonzero-exit"], 1, "FAULT", None, ["P3-33"])
trace("CB-P3-12 crash mid-stage: signal-death during ANALYZING",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "signal-death"], 1, "FAULT", None,
      ["P3-33"])
trace("CB-P3-13 FAULT is ABSORBING: every further event traces FAULT-absorb",
      ["Hello", "deadline", "Hello", "eof"], 1, "FAULT", None,
      ["P3-33", "FAULT-absorb", "FAULT-absorb"])

# --- terminal process handling ---------------------------------------------
trace("CB-P3-14 a post-terminal FRAME between the terminal and zero-exit faults",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "CoverageV3", "Complete", "FactBatch"],
      1, "FAULT", "complete", ["post-terminal-frame"])
trace("CB-P3-15 a process fault AFTER a clean terminal is still a FAULT, not an "
      "absorbed no-op", ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP),
                         "UniverseAccepted", "SnapshotManifest", "SnapshotSeal",
                         "SnapshotAccepted", "NativeContextVerified", "Analyze",
                         "CoverageV3", "Complete", "nonzero-exit"],
      1, "FAULT", "complete", ["P3-33"])

# --- multi-stage ------------------------------------------------------------
m = trace("CB-P3-16 multi-stage: one CoverageV3 per stage; only the LAST may be "
          "followed by Complete",
          ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP),
           "UniverseAccepted", "SnapshotManifest", "SnapshotSeal",
           "SnapshotAccepted", "NativeContextVerified", "Analyze", "CoverageV3",
           "FactBatch", "CoverageV3", "Complete", "zero-exit", "eof"],
          2, "DONE", "complete")
ok("CB-P3-16a stagesCompleted == stageCount", m.s["stagesCompleted"] == 2)
trace("CB-P3-17 Complete BEFORE the last stage's CoverageV3 has no matching row",
      ["Hello", ("HelloAck", FULL_CAPS), ("OpenUniverse", NODEP), "UniverseAccepted",
       "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
       "NativeContextVerified", "Analyze", "CoverageV3", "Complete"],
      2, "FAULT", None, ["P3-34"])

print()
print("FAILURES:", FAIL or "none")
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-protocol3.json", "w") as f:
    json.dump({"pairwiseDisjoint": P.pairwise_disjoint() == [],
               "traces": RESULTS}, f, indent=1, sort_keys=True)
