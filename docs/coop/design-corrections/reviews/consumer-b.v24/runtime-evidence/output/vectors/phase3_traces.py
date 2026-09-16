"""Phase 3: provider protocol traces over the published protocol3 transition table."""
import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24/output/ref')
sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24/output/tools')
import protocol3 as P
import schemas
import status as S

KIT = schemas.kit()
M = P.Protocol3()
failures = []


def check(c, label):
    if not c:
        failures.append(label)


LIMITS = {"maxDependencySourcePackages": 4096, "maxDependencySourceEntries": 1000000, "maxDependencySourceTotalBytes": 8589934592,
          "maxDependencySourceChunkBytes": 1048576, "maxUnresolvedEdgesPerStage": 1000000, "maxCfgSets": 4,
          "maxExpansionRows": 1000000, "maxGeneratedFileRows": 1000000}
CAPS = P.IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "rust-semantic-facts-v1", "resolution-completeness-v2",
                            "unresolved-edge-v1", "dependency-source-v1", "prepared-output-v3", "native-context-v2", "target-attribution-v2"]
HELLO = {"frame": "Hello", "protocolMajor": 3, "expectedCapabilities": CAPS, "identityVersions": P.IDENTITY_VERSIONS, "limits": LIMITS}
ACK = {"frame": "HelloAck", "protocolMajor": 3, "capabilities": CAPS, "identityVersions": P.IDENTITY_VERSIONS}
hello_schema = KIT.admit({k: v for k, v in HELLO.items() if k != "frame"}, "native/native-evidence.schemas.v2.json", "#/$defs/HelloV3")
ack_schema = KIT.admit({k: v for k, v in ACK.items() if k != "frame"}, "native/native-evidence.schemas.v2.json", "#/$defs/HelloAckV3")
check(hello_schema["ok"] and ack_schema["ok"], "hello schemas")

HOST_ASSUMPTIONS = ["actual worker process spawn and supervision", "OS exit status / signal / EOF observation",
                    "frame byte framing, payload schema validation and chunk digest verification against the sealed snapshot",
                    "worker-side recomputation of NativeContextV2 / TypeScriptNativeContextV2 (s9.5)",
                    "deadline and stdout-byte detection", "cancellation delivery timing bounds (security S6)"]


def ev(frame, **kw):
    d = {"frame": frame}
    d.update(kw)
    return d


def record(name, events, expect_rules, expect_phase, expect_terminal, faulted, notes, extra_checks=None):
    res = M.run(events)
    rules = [t["rule"] for t in res["trace"]]
    # identity-before-source observable: sourceBytesSent must be false on every step before OpenUniverse is admitted
    source_flags = []
    probe = []
    for i in range(len(events)):
        sub = M.run(events[:i + 1])
        source_flags.append({"afterFrame": events[i]["frame"], "identityNegotiated": sub["state"]["identityNegotiated"],
                             "sourceBytesSent": sub["state"]["sourceBytesSent"], "phase": sub["state"]["phase"]})
    first_source = next((f for f in source_flags if f["sourceBytesSent"]), None)
    idx_neg = next((i for i, f in enumerate(source_flags) if f["identityNegotiated"]), None)
    idx_src = next((i for i, f in enumerate(source_flags) if f["sourceBytesSent"]), None)
    identity_before_source = idx_src is None or (idx_neg is not None and idx_neg < idx_src)
    authority = P.stage_authority(res["state"]["terminalKind"], faulted) if (res["state"]["terminalKind"] or faulted) else None
    if authority:
        sa = KIT.admit(authority, "native/native-evidence.schemas.v2.json", "#/$defs/StageAuthorityV1")
        check(sa["ok"], f"{name} stage authority schema")
    ok = rules == expect_rules and res["state"]["phase"] == expect_phase and res["state"]["terminalKind"] == expect_terminal
    check(ok, f"trace {name}: {rules} {res['state']}")
    check(identity_before_source, f"{name} identity before source")
    if extra_checks:
        for label, cond in extra_checks(res, source_flags):
            check(cond, f"{name}: {label}")
    return {"name": name, "class": "valid" if not faulted else "invalid", "events": events, "trace": res["trace"],
            "finalState": res["state"], "expectedRules": expect_rules, "matchesExpected": ok,
            "identityNegotiatedBeforeSourceBytes": identity_before_source, "firstSourceByteStep": first_source,
            "stateTimeline": source_flags, "stageAuthority": authority,
            "executedVsHost": {"executed": ["transition interpretation from protocol3-transitions.v1.json (rows, guards, pre-match/no-match laws, state updates, stage-dependent P3-24)",
                                            "s9.1 Hello/HelloAck exact-echo check as a host payload rule",
                                            "s10 terminal -> StageAuthorityV1 projection validated against the native schema"],
                               "futureHostAssumptions": HOST_ASSUMPTIONS}, "notes": notes}


PRE = [HELLO, ACK]
SNAP = [ev("UniverseAccepted"), ev("SnapshotManifest"), ev("SnapshotFileChunk"), ev("SnapshotFileChunk"), ev("SnapshotSeal"), ev("SnapshotAccepted")]
TAIL = [ev("zero-exit"), ev("eof")]
traces = {}

traces["complete"] = record(
    "complete (TypeScript-shaped, no dependency/prepared, two stages)",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=2), ev("FactBatch"), ev("CoverageV3"), ev("FactBatch"), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-23", "P3-24", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "one CoverageV3 per stage; Complete only after the last stage (stageIndex==stageCount)",
    lambda res, fl: [("stagesCompleted==2", res["state"]["stagesCompleted"] == 2)])

traces["complete-rust-dependency-prepared"] = record(
    "complete (Rust dependency + prepared custody)",
    PRE + [ev("OpenUniverse", dependencyMode=True, preparedMode=True)] + SNAP +
    [ev("DependencySourceManifest"), ev("DependencySourceChunk"), ev("DependencySourceSeal"), ev("DependencySourceAccepted"),
     ev("PreparedOutputManifest"), ev("PreparedOutputChunk"), ev("PreparedOutputSeal"), ev("PreparedOutputAccepted"),
     ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("FactBatch"), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-08", "P3-11", "P3-12", "P3-13", "P3-14", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20", "P3-22", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "exercises guard-separated rows P3-08 and P3-14")

traces["unavailable-before-analyze"] = record(
    "unavailable (native-context-mismatch before Analyze)",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP + [ev("Unavailable", reason="native-context-mismatch")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-21", "P3-31", "P3-32"],
    "DONE", "unavailable", False, "clean typed terminal: no Analyze, zero facts, Coverage provider-unavailable; Run may still seal indeterminate")

traces["unavailable-during-analyze"] = record(
    "unavailable during ANALYZING after one FactBatch",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=2), ev("FactBatch"), ev("CoverageV3"), ev("FactBatch"), ev("Unavailable", reason="capability-missing")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-23", "P3-24", "P3-23", "P3-25", "P3-31", "P3-32"],
    "DONE", "unavailable", False, "facts before the terminal admitted (factsAdmitted=before-terminal); stage partial")

traces["complete-rust-prepared-only"] = record(
    "complete (prepared custody without dependency sources)",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=True)] + SNAP +
    [ev("PreparedOutputManifest"), ev("PreparedOutputChunk"), ev("PreparedOutputSeal"), ev("PreparedOutputAccepted"),
     ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-09", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20", "P3-22", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "guard dependencyMode=false,preparedMode=true selects P3-09")

traces["complete-rust-dependency-only"] = record(
    "complete (dependency sources, no prepared set)",
    PRE + [ev("OpenUniverse", dependencyMode=True, preparedMode=False)] + SNAP +
    [ev("DependencySourceManifest"), ev("DependencySourceChunk"), ev("DependencySourceSeal"), ev("DependencySourceAccepted"),
     ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-08", "P3-11", "P3-12", "P3-13", "P3-15", "P3-20", "P3-22", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "guard preparedMode=false selects P3-15")

traces["budget-exhausted"] = record(
    "budget-exhausted during ANALYZING",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("FactBatch"), ev("BudgetExhausted", unit="items")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-23", "P3-26", "P3-31", "P3-32"],
    "DONE", "budget-exhausted", False, "clean typed terminal; stage partial; COVERAGE.BUDGET_EXHAUSTED indeterminate unless a more specific entry deficiency applies")

traces["cancel"] = record(
    "cancellation during ANALYZING",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("FactBatch"), ev("Cancel"), ev("Cancelled")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-23", "P3-29", "P3-30", "P3-31", "P3-32"],
    "DONE", "cancelled", False, "interrupted (130); no facts, no Run from this stage")

traces["cancel-then-frame"] = record(
    "cancel requested, worker sends FactBatch instead of Cancelled",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("Cancel"), ev("FactBatch"), ev("Cancelled")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-29", "P3-34", "FAULT-absorb"],
    "FAULT", None, True, "WAIT_CANCELLED admits only Cancelled (or a process fault); anything else faults")

traces["fault-identity-echo"] = record(
    "fault: HelloAck does not echo expected capabilities (identity token missing)",
    [HELLO, dict(ACK, capabilities=[c for c in CAPS if c != "fact-identity-fact2"]), ev("OpenUniverse", dependencyMode=False, preparedMode=False), ev("SnapshotManifest")],
    ["P3-01", "payload:hello-ack-echo-mismatch(s9.1-step2)", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "no snapshot/dependency/prepared byte is ever sent (sourceBytesSent stays false)",
    lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-open-universe-before-negotiation"] = record(
    "fault: OpenUniverse while identityNegotiated=false (table guard path)",
    [dict(HELLO, expectedCapabilities=[c for c in CAPS if c != "coverage-v3"]), dict(ACK, capabilities=[c for c in CAPS if c != "coverage-v3"]),
     ev("OpenUniverse", dependencyMode=False, preparedMode=False)],
    ["P3-01", "P3-02", "P3-34"], "FAULT", None, True,
    "echo is exact but the identity token set is incomplete -> identityNegotiated=false; P3-03 guard fails, P3-34 faults before OpenUniverse state updates, so sourceBytesSent=false. (A conforming host would not spawn such a worker at all: s9.1 step 1.)",
    lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False), ("identityNegotiated false", res["state"]["identityNegotiated"] is False)])

traces["fault-process-signal"] = record(
    "fault: signal-death mid-ANALYZING, later frames absorbed",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("FactBatch"), ev("signal-death"), ev("CoverageV3"), ev("Complete")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-23", "P3-33", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "operational-failed PROVIDER.PROTOCOL_VIOLATION; facts already batched are NOT admitted")

traces["fault-provider-fault-frame"] = record(
    "ProviderFault frame from a pre-complete phase",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP + [ev("ProviderFault")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-28", "P3-31", "P3-32"],
    "DONE", "provider-fault", True, "a clean exchange end does not rescue a provider-fault terminal: no facts, no Run")

traces["terminal-post-terminal-frame"] = record(
    "terminal: FactBatch after Complete",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("CoverageV3"), ev("Complete"), ev("FactBatch"), ev("zero-exit")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-24", "P3-27", "post-terminal-frame", "FAULT-absorb"],
    "FAULT", "complete", True, "terminalKind was recorded but the exchange faulted; identity s1 requires successful exit and EOF before facts are admitted")

traces["terminal-nonzero-exit-after-complete"] = record(
    "terminal: nonzero exit after Complete",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("CoverageV3"), ev("Complete"), ev("nonzero-exit")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-24", "P3-27", "P3-33"],
    "FAULT", "complete", True, "Complete without zero exit is a fault")

traces["terminal-eof-before-exit"] = record(
    "terminal: eof before zero-exit",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=1), ev("CoverageV3"), ev("Complete"), ev("eof")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-24", "P3-27", "P3-34"],
    "FAULT", "complete", True, "WAIT_ZERO_EXIT has no eof row")

traces["terminal-complete-before-last-stage"] = record(
    "Complete before the last stage's CoverageV3",
    PRE + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + SNAP +
    [ev("NativeContextVerified", equal=True), ev("Analyze", stageCount=2), ev("CoverageV3"), ev("Complete")],
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22", "P3-24", "P3-34"],
    "FAULT", None, True, "P3-24 resolved ANALYZING because stageIndex 1 != stageCount 2; Complete has no ANALYZING row")

controls = {"pairwiseDisjointOverlaps": M.pairwise_disjoint(),
            "preCompleteDerivation": M.t['wildcards']['*PRE_COMPLETE']['phases'] == M.t['phases'][1:17],
            "ruleCount": len(M.rules),
            "rulesExercised": sorted({t["rule"] for tr in traces.values() for t in tr["trace"]})}
check(controls["pairwiseDisjointOverlaps"] == [], "disjoint rows")
all_rows = {r["id"] for r in M.rules}
controls["rowsNotExercised"] = sorted(all_rows - set(controls["rulesExercised"]))

check(controls["rowsNotExercised"] == [], "every published row exercised")
S.dump('traces/complete.json', {"traces": [traces["complete"], traces["complete-rust-dependency-prepared"], traces["complete-rust-prepared-only"], traces["complete-rust-dependency-only"]]})
S.dump('traces/unavailable.json', {"traces": [traces["unavailable-before-analyze"], traces["unavailable-during-analyze"], traces["budget-exhausted"]]})
S.dump('traces/cancel.json', {"traces": [traces["cancel"], traces["cancel-then-frame"]]})
S.dump('traces/fault.json', {"traces": [traces["fault-identity-echo"], traces["fault-open-universe-before-negotiation"], traces["fault-process-signal"], traces["fault-provider-fault-frame"]]})
S.dump('traces/terminal.json', {"traces": [traces["terminal-post-terminal-frame"], traces["terminal-nonzero-exit-after-complete"], traces["terminal-eof-before-exit"], traces["terminal-complete-before-last-stage"]]})
S.dump('traces/controls.json', dict(controls, helloSchema=hello_schema, helloAckSchema=ack_schema, assertionFailures=failures))
print(json.dumps({"failures": failures, "controls": controls}, indent=1))
sys.exit(1 if failures else 0)
