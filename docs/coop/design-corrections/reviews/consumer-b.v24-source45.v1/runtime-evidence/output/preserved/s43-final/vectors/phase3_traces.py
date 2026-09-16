"""Phase 3: provider protocol traces over the published protocol3 transition table.

source42.v3 (HC-53): every FactBatch now carries a payload, and the prose-owned FactBatch payload law is applied at each FactBatch that
reaches ANALYZING. That law covers negotiated payload selection, exact payload bytes and request/batch correlation (ref/factbatch.py).
The source42.v2 version of this file carried frame names only and is preserved at preserved/s42-v2-final/vectors/phase3_traces.py.
"""
import json
import sys

OUTP = '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/'
sys.path.insert(0, OUTP + 'ref')
sys.path.insert(0, OUTP + 'tools')
sys.path.insert(0, OUTP + 'vectors')
import factbatch as FB  # noqa: E402
import payload_fixtures as PF  # noqa: E402
import protocol3 as P  # noqa: E402
import schemas  # noqa: E402
import status as S  # noqa: E402

KIT = schemas.kit()
M = P.Protocol3()
EX = {shape: FB.PayloadExchange(M, PF.RETAINED, shape, PF.HOST[shape]) for shape in ("ts", "rust")}
failures = []


def check(c, label):
    if not c:
        failures.append(label)


NES = "native/native-evidence.schemas.v2.json"
hello_schemas = {}
# HelloV3/HelloAckV3 (native-evidence.schemas.v2.json lines 4025-4124) are the rust-semantic major-3 payloads: protocolMajor const 3. No
# typescript-semantic major-2 Hello/HelloAck schema is published (s9.4 lists deltas only; advisory A-s42v3-1). The first s42v3-p3 run sent
# protocolMajor 2 to HelloV3 and failed (logs/s42v3-p3.1.phase3_traces.log). TypeScript payloads are therefore admitted on every
# shared HelloV3 member with protocolMajor alone substituted; that substitution is recorded, and major 2 is checked by the s9.1 text.
for shape in ("ts", "rust"):
    for token in (True, False):
        h_payload = {k: v for k, v in PF.hello(shape, token).items() if k != "frame"}
        a_payload = {k: v for k, v in PF.ack(shape, token).items() if k != "frame"}
        substituted = shape == "ts"
        if substituted:
            check(h_payload["protocolMajor"] == 2 == a_payload["protocolMajor"], "typescript-semantic protocol major 2 (s9.1 line 2774)")
            h_payload, a_payload = dict(h_payload, protocolMajor=3), dict(a_payload, protocolMajor=3)
        hs = KIT.admit(h_payload, NES, "#/$defs/HelloV3")
        hk = KIT.admit(a_payload, NES, "#/$defs/HelloAckV3")
        hello_schemas[f"{shape}{'-token' if token else ''}"] = {
            "hello": hs, "helloAck": hk,
            "protocolMajorSubstitutedForSchema": "2 -> 3 (no published TypeScript major-2 Hello schema; A-s42v3-1)" if substituted else None}
        check(hs["ok"] and hk["ok"], f"hello schemas {shape} token={token}: {hs['stock'][:2]} {hk['stock'][:2]}")

HOST_ASSUMPTIONS = ["actual worker process spawn and supervision", "OS exit status / signal / EOF observation",
                    "frame envelope byte framing and chunk digest verification against the sealed snapshot",
                    "worker-side recomputation of NativeContextV2 / TypeScriptNativeContextV2 (s9.5)",
                    "deadline and stdout-byte detection", "cancellation delivery timing bounds (security S6)",
                    "that an actual worker emits the constructed FactBatch payload bytes and companions (the host-side payload law itself is executed here)"]
EXECUTED = ["transition interpretation from protocol3-transitions.v1.json (rows, guards, pre-match/no-match laws, state updates, stage-dependent P3-24)",
            "s9.1 Hello/HelloAck exact-echo check as a host payload rule",
            "FactBatch payload law at every FactBatch reaching ANALYZING (ref/factbatch.py buffer_fact_batch_occupancy): negotiated selection (FactBatchV3 iff "
            "target-attribution-v2 echoed; historical FactBatchV2 otherwise); schema admission of the exact payload; restricted deterministic-CBOR decode-once/re-encode "
            "of every canonicalRelationPayload against its hex and decoded observation; DispatchBindingV1 derived from the current Analyze stage request and the retained "
            "Plan fragment with stageId/analysisOrdinal/batchIndex/candidate-stream correlation; companion association; atomic refusal routed to the s10 fault projection",
            "s10 terminal -> StageAuthorityV1 projection validated against the native schema"]
NOT_CONSTRUCTED = ["payload bodies of frames other than Hello/HelloAck, the Analyze correlation members and FactBatch (Snapshot*, DependencySource*, PreparedOutput*, "
                   "NativeContextVerified, CoverageV3, Unavailable, BudgetExhausted, Complete, ProviderFault, Cancel/Cancelled carry their frame names and state-update members only)",
                   "post-terminal bind_worker_occupancy (fact2 minting, native views, stageReceipts, TargetAttributionV2 projection and capture, C15)",
                   "anchor admission and fact identity of the constructed candidates"]


def ev(frame, **kw):
    d = {"frame": frame}
    d.update(kw)
    return d


def record(name, shape, events, expect_rules, expect_phase, expect_terminal, faulted, notes, expect_payload=(), extra_checks=None):
    res = EX[shape].run(events)
    rules = [t["rule"] for t in res["trace"]]
    source_flags = [{"afterFrame": e["frame"], "identityNegotiated": s["identityNegotiated"], "sourceBytesSent": s["sourceBytesSent"], "phase": s["phase"]}
                    for e, s in zip(events, res["states"])]
    first_source = next((f for f in source_flags if f["sourceBytesSent"]), None)
    idx_neg = next((i for i, f in enumerate(source_flags) if f["identityNegotiated"]), None)
    idx_src = next((i for i, f in enumerate(source_flags) if f["sourceBytesSent"]), None)
    identity_before_source = idx_src is None or (idx_neg is not None and idx_neg < idx_src)
    authority = P.stage_authority(res["state"]["terminalKind"], faulted) if (res["state"]["terminalKind"] or faulted) else None
    if authority:
        sa = KIT.admit(authority, NES, "#/$defs/StageAuthorityV1")
        check(sa["ok"], f"{name} stage authority schema")
    ok = rules == expect_rules and res["state"]["phase"] == expect_phase and res["state"]["terminalKind"] == expect_terminal
    check(ok, f"trace {name}: {rules} {res['state']}")
    check(identity_before_source, f"{name} identity before source")
    check(res["analyzeRequestFaults"] == [], f"{name} Analyze request faults {res['analyzeRequestFaults']}")
    observed_payload = [(p["result"], p["firstRefusal"]) if p["payloadChecked"] else ("not-validated", None) for p in res["payloads"]]
    check(observed_payload == list(expect_payload), f"{name} payload results {observed_payload} != {list(expect_payload)}")
    check(len(res["payloads"]) == sum(1 for e in events if e["frame"] == "FactBatch"), f"{name}: every FactBatch carries a payload")
    for p in res["payloads"]:
        if p.get("result") == "REFUSE":
            term = p["publicRoute"]["termination"]
            check(p["violations"][0]["origin"] == "provider-return" and authority is not None and
                  (term["class"], term["errorCode"]) == (authority["d9"]["class"], authority["d9"]["code"]),
                  f"{name}: payload refusal route {term} agrees with the s10 fault projection {authority and authority['d9']}")
    if extra_checks:
        for label, cond in extra_checks(res, source_flags):
            check(cond, f"{name}: {label}")
    return {"name": name, "provider": shape, "class": "valid" if not faulted else "invalid", "events": events, "trace": res["trace"],
            "finalState": res["state"], "expectedRules": expect_rules, "matchesExpected": ok, "negotiatedTargetAttribution": res["negotiated"],
            "identityNegotiatedBeforeSourceBytes": identity_before_source, "firstSourceByteStep": first_source,
            "stateTimeline": source_flags, "stageAuthority": authority,
            "payloadResults": res["payloads"], "expectedPayloadResults": [list(x) for x in expect_payload], "payloadResultsMatch": observed_payload == list(expect_payload),
            "executedVsHost": {"executed": EXECUTED, "futureHostAssumptions": HOST_ASSUMPTIONS, "notConstructedHere": NOT_CONSTRUCTED}, "notes": notes}


def pre(shape, token=True):
    return [PF.hello(shape, token), PF.ack(shape, token)]


SNAP = [ev("UniverseAccepted"), ev("SnapshotManifest"), ev("SnapshotFileChunk"), ev("SnapshotFileChunk"), ev("SnapshotSeal"), ev("SnapshotAccepted")]
TAIL = [ev("zero-exit"), ev("eof")]
OU = ev("OpenUniverse", dependencyMode=False, preparedMode=False)
NCV = ev("NativeContextVerified", equal=True)
FB_IMP0 = PF.fb(PF.v3("ts-imports", 0, PF.imports_b0()))
FB_IMP1 = PF.fb(PF.v3("ts-imports", 1, PF.imports_b1()))
FB_CALLS0 = PF.fb(PF.v3("ts-calls", 0, PF.calls_b0()))
FB_RUST0 = PF.fb(PF.v3("rust-calls", 0, PF.rust_calls_b0()))
OPEN_TO_ANALYZE = ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20", "P3-22"]
A = "ADMIT"
traces = {}

traces["complete"] = record(
    "complete (TypeScript major 2, no dependency/prepared, two stages)", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), FB_IMP0, ev("CoverageV3"), FB_CALLS0, ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-24", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "one CoverageV3 per stage; Complete only after the last stage (stageIndex==stageCount); both FactBatchV3 payloads admitted",
    [(A, None), (A, None)], lambda res, fl: [("stagesCompleted==2", res["state"]["stagesCompleted"] == 2)])

traces["complete-rust-dependency-prepared"] = record(
    "complete (Rust dependency + prepared custody)", "rust",
    pre("rust") + [ev("OpenUniverse", dependencyMode=True, preparedMode=True)] + SNAP +
    [ev("DependencySourceManifest"), ev("DependencySourceChunk"), ev("DependencySourceSeal"), ev("DependencySourceAccepted"),
     ev("PreparedOutputManifest"), ev("PreparedOutputChunk"), ev("PreparedOutputSeal"), ev("PreparedOutputAccepted"),
     NCV, PF.analyze_event("rust"), FB_RUST0, ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-08", "P3-11", "P3-12", "P3-13", "P3-14", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20", "P3-22", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "exercises guard-separated rows P3-08 and P3-14", [(A, None)])

traces["unavailable-before-analyze"] = record(
    "unavailable (native-context-mismatch before Analyze)", "ts",
    pre("ts") + [OU] + SNAP + [ev("Unavailable", reason="native-context-mismatch")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-21", "P3-31", "P3-32"],
    "DONE", "unavailable", False, "clean typed terminal: no Analyze, zero facts, Coverage provider-unavailable; Run may still seal indeterminate")

traces["unavailable-during-analyze"] = record(
    "unavailable during ANALYZING after one FactBatch of the second stage", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), FB_IMP0, ev("CoverageV3"), FB_CALLS0, ev("Unavailable", reason="capability-missing")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-24", "P3-23", "P3-25", "P3-31", "P3-32"],
    "DONE", "unavailable", False, "facts before the terminal admitted (factsAdmitted=before-terminal); stage partial", [(A, None), (A, None)])

traces["complete-rust-prepared-only"] = record(
    "complete (prepared custody without dependency sources)", "rust",
    pre("rust") + [ev("OpenUniverse", dependencyMode=False, preparedMode=True)] + SNAP +
    [ev("PreparedOutputManifest"), ev("PreparedOutputChunk"), ev("PreparedOutputSeal"), ev("PreparedOutputAccepted"),
     NCV, PF.analyze_event("rust"), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-09", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20", "P3-22", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "guard dependencyMode=false,preparedMode=true selects P3-09")

traces["complete-rust-dependency-only"] = record(
    "complete (dependency sources, no prepared set)", "rust",
    pre("rust") + [ev("OpenUniverse", dependencyMode=True, preparedMode=False)] + SNAP +
    [ev("DependencySourceManifest"), ev("DependencySourceChunk"), ev("DependencySourceSeal"), ev("DependencySourceAccepted"),
     NCV, PF.analyze_event("rust"), ev("CoverageV3"), ev("Complete")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-08", "P3-11", "P3-12", "P3-13", "P3-15", "P3-20", "P3-22", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "guard preparedMode=false selects P3-15")

traces["complete-negotiated-multibatch-analyze-subset"] = record(
    "complete (TypeScript; Analyze selects Plan stages 1 and 3; two FactBatchV3 frames continue one candidate stream)", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), FB_IMP0, FB_IMP1, ev("CoverageV3"), FB_CALLS0, ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-23", "P3-24", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "dispatch coordinates per batch (retainedStageOrdinal, analyzeRequestOrdinal, batchIndex, first candidate): (1,0,0,0), (1,0,1,3), (3,1,0,0)",
    [(A, None), (A, None), (A, None)],
    lambda res, fl: [("dispatch coordinates", [[p["dispatch"][k] for k in ("retainedStageOrdinal", "analyzeRequestOrdinal", "expectedBatchIndex", "expectedFirstCandidateOrdinal")]
                                               for p in res["payloads"]] == [[1, 0, 0, 0], [1, 0, 1, 3], [3, 1, 0, 0]]),
                     ("companions buffered per batch", [len(p["bufferedCompanions"]) for p in res["payloads"]] == [2, 3, 1])])

traces["complete-unnegotiated-v2"] = record(
    "complete (Rust; target-attribution-v2 absent; historical FactBatchV2)", "rust",
    pre("rust", False) + [OU] + SNAP + [NCV, PF.analyze_event("rust"), PF.fb(PF.v2(FB_RUST0["payload"])), ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False, "FactBatchV2 admitted; occupancy omitted (unknown except exact-id ephemeral)", [(A, None)],
    lambda res, fl: [("not negotiated", res["negotiated"] is False), ("occupancy omitted", res["payloads"][0]["occupancy"].startswith("omitted"))])

traces["budget-exhausted"] = record(
    "budget-exhausted during ANALYZING", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), FB_RUST0, ev("BudgetExhausted", unit="items")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-26", "P3-31", "P3-32"],
    "DONE", "budget-exhausted", False, "clean typed terminal; stage partial; COVERAGE.BUDGET_EXHAUSTED indeterminate unless a more specific entry deficiency applies", [(A, None)])

traces["cancel"] = record(
    "cancellation during ANALYZING", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), FB_RUST0, ev("Cancel"), ev("Cancelled")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-29", "P3-30", "P3-31", "P3-32"],
    "DONE", "cancelled", False, "interrupted (130); no facts, no Run from this stage", [(A, None)])

traces["cancel-then-frame"] = record(
    "cancel requested, worker sends FactBatch instead of Cancelled", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), ev("Cancel"), FB_RUST0, ev("Cancelled")],
    OPEN_TO_ANALYZE + ["P3-29", "P3-34", "FAULT-absorb"],
    "FAULT", None, True, "WAIT_CANCELLED admits only Cancelled (or a process fault); anything else faults before payload validation", [("not-validated", None)])

traces["fault-identity-echo"] = record(
    "fault: HelloAck does not echo expected capabilities (identity token missing)", "rust",
    [PF.hello("rust"), dict(PF.ack("rust"), capabilities=[c for c in PF.caps("rust") if c != "fact-identity-fact2"]), OU, ev("SnapshotManifest")],
    ["P3-01", "payload:hello-ack-echo-mismatch(s9.1-step2)", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "no snapshot/dependency/prepared byte is ever sent (sourceBytesSent stays false)", (),
    lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-hello-attribution-token-not-echoed"] = record(
    "fault: Hello offers target-attribution-v2, HelloAck omits it", "ts",
    [PF.hello("ts", True), PF.ack("ts", False), OU, ev("SnapshotManifest")],
    ["P3-01", "payload:hello-ack-echo-mismatch(s9.1-step2)", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "the optional token is not an identity token, but the echo is still exact: no payload version is selected and no source byte is sent", (),
    lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-open-universe-before-negotiation"] = record(
    "fault: OpenUniverse while identityNegotiated=false (table guard path)", "rust",
    [dict(PF.hello("rust"), expectedCapabilities=[c for c in PF.caps("rust") if c != "coverage-v3"]), dict(PF.ack("rust"), capabilities=[c for c in PF.caps("rust") if c != "coverage-v3"]), OU],
    ["P3-01", "P3-02", "P3-34"], "FAULT", None, True,
    "echo is exact but the identity token set is incomplete -> identityNegotiated=false; P3-03 guard fails, P3-34 faults before OpenUniverse state updates, so sourceBytesSent=false. (A conforming host would not spawn such a worker at all: s9.1 step 1.)",
    (), lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False), ("identityNegotiated false", res["state"]["identityNegotiated"] is False)])

traces["fault-process-signal"] = record(
    "fault: signal-death mid-ANALYZING, later frames absorbed", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), FB_RUST0, ev("signal-death"), ev("CoverageV3"), ev("Complete")],
    OPEN_TO_ANALYZE + ["P3-23", "P3-33", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "operational-failed PROVIDER.PROTOCOL_VIOLATION; facts already batched are NOT admitted", [(A, None)])

traces["fault-provider-fault-frame"] = record(
    "ProviderFault frame from a pre-complete phase", "ts",
    pre("ts") + [OU] + SNAP + [ev("ProviderFault")] + TAIL,
    ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-28", "P3-31", "P3-32"],
    "DONE", "provider-fault", True, "a clean exchange end does not rescue a provider-fault terminal: no facts, no Run")

PAYLOAD_FAULT_TAIL = ["FAULT-absorb"] * 4
traces["fault-unnegotiated-v3-payload"] = record(
    "fault: FactBatchV3 payload without the negotiated token", "rust",
    pre("rust", False) + [OU] + SNAP + [NCV, PF.analyze_event("rust"), FB_RUST0, ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["payload:fact-batch-refused(PROVIDER_RETURN_UNNEGOTIATED_V3)"] + PAYLOAD_FAULT_TAIL,
    "FAULT", None, True, "s9.1: a FactBatchV3 payload without the token is PROVIDER.PROTOCOL_VIOLATION", [("REFUSE", "PROVIDER_RETURN_UNNEGOTIATED_V3")])

traces["fault-negotiated-v2-payload"] = record(
    "fault: historical FactBatchV2 payload after target-attribution-v2 was negotiated", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), PF.fb(PF.v2(FB_RUST0["payload"])), ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["payload:fact-batch-refused(PROVIDER_RETURN_SCHEMA)"] + PAYLOAD_FAULT_TAIL,
    "FAULT", None, True, "s9.1: a FactBatchV2 payload with the token is PROVIDER.PROTOCOL_VIOLATION (V3 required members absent)", [("REFUSE", "PROVIDER_RETURN_SCHEMA")])

traces["fault-batch-stageid-echoes-analyze-request-ordinal"] = record(
    "fault: second stage's FactBatch echoes its Analyze stageOrdinal as stageId", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), FB_IMP0, ev("CoverageV3"), PF.fb(dict(FB_CALLS0["payload"], stageId="1")), ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "P3-24", "payload:fact-batch-refused(PROVIDER_RETURN_STAGE_ID)"] + PAYLOAD_FAULT_TAIL,
    "FAULT", None, True, "FactBatch.stageId echoes the requested C-2 stageId text, never stageOrdinal", [(A, None), ("REFUSE", "PROVIDER_RETURN_STAGE_ID")])

traces["fault-candidate-stream-restarts-across-batches"] = record(
    "fault: second FactBatch of one stage restarts candidateOrdinal at 0", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), FB_IMP0, PF.fb(PF.renumber(FB_IMP1["payload"], 0)), ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["P3-23", "payload:fact-batch-refused(PROVIDER_RETURN_CANDIDATE_STREAM)"] + PAYLOAD_FAULT_TAIL,
    "FAULT", None, True, "the per-stage candidate stream continues at expectedFirstCandidateOrdinal 3; ordinals restart schema-lawfully inside the batch",
    [(A, None), ("REFUSE", "PROVIDER_RETURN_CANDIDATE_STREAM")])

JSON_HEX = json.dumps(FB_RUST0["payload"]["candidates"][0]["decodedRelationPayload"], sort_keys=True, separators=(",", ":")).encode().hex()
bad_bytes = json.loads(json.dumps(FB_RUST0["payload"]))
bad_bytes["candidates"][0]["canonicalRelationPayloadHex"] = JSON_HEX
traces["fault-payload-hex-is-canonical-json"] = record(
    "fault: canonicalRelationPayloadHex transcribes canonical JSON UTF-8 instead of the deterministic-CBOR bytes", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), PF.fb(bad_bytes), ev("CoverageV3"), ev("Complete")] + TAIL,
    OPEN_TO_ANALYZE + ["payload:fact-batch-refused(PROVIDER_RETURN_PAYLOAD_CBOR)"] + PAYLOAD_FAULT_TAIL,
    "FAULT", None, True, "s9.6 lines 2903-2906: the hex transcribes the same CBOR bytes, never canonical JSON UTF-8", [("REFUSE", "PROVIDER_RETURN_PAYLOAD_CBOR")])

traces["terminal-post-terminal-frame"] = record(
    "terminal: FactBatch after Complete", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), ev("CoverageV3"), ev("Complete"), FB_RUST0, ev("zero-exit")],
    OPEN_TO_ANALYZE + ["P3-24", "P3-27", "post-terminal-frame", "FAULT-absorb"],
    "FAULT", "complete", True, "terminalKind was recorded but the exchange faulted; identity s1 requires successful exit and EOF before facts are admitted; the payload is never validated",
    [("not-validated", None)])

traces["terminal-nonzero-exit-after-complete"] = record(
    "terminal: nonzero exit after Complete", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), ev("CoverageV3"), ev("Complete"), ev("nonzero-exit")],
    OPEN_TO_ANALYZE + ["P3-24", "P3-27", "P3-33"],
    "FAULT", "complete", True, "Complete without zero exit is a fault")

traces["terminal-eof-before-exit"] = record(
    "terminal: eof before zero-exit", "rust",
    pre("rust") + [OU] + SNAP + [NCV, PF.analyze_event("rust"), ev("CoverageV3"), ev("Complete"), ev("eof")],
    OPEN_TO_ANALYZE + ["P3-24", "P3-27", "P3-34"],
    "FAULT", "complete", True, "WAIT_ZERO_EXIT has no eof row")

traces["terminal-complete-before-last-stage"] = record(
    "Complete before the last stage's CoverageV3", "ts",
    pre("ts") + [OU] + SNAP + [NCV, PF.analyze_event("ts"), ev("CoverageV3"), ev("Complete")],
    OPEN_TO_ANALYZE + ["P3-24", "P3-34"],
    "FAULT", None, True, "P3-24 resolved ANALYZING because stageIndex 1 != stageCount 2; Complete has no ANALYZING row")

controls = {"pairwiseDisjointOverlaps": M.pairwise_disjoint(),
            "preCompleteDerivation": M.t['wildcards']['*PRE_COMPLETE']['phases'] == M.t['phases'][1:17],
            "ruleCount": len(M.rules),
            "rulesExercised": sorted({t["rule"] for tr in traces.values() for t in tr["trace"]})}
check(controls["pairwiseDisjointOverlaps"] == [], "disjoint rows")
all_rows = {r["id"] for r in M.rules}
controls["rowsNotExercised"] = sorted(all_rows - set(controls["rulesExercised"]))
check(controls["rowsNotExercised"] == [], "every published row exercised")
payload_rows = [p for tr in traces.values() for p in tr["payloadResults"]]
controls["factBatchPayloads"] = {"total": len(payload_rows), "validated": sum(1 for p in payload_rows if p["payloadChecked"]),
                                 "admitted": sum(1 for p in payload_rows if p.get("result") == "ADMIT"),
                                 "refused": sorted(p["firstRefusal"] for p in payload_rows if p.get("result") == "REFUSE"),
                                 "notValidatedBeforePayload": sum(1 for p in payload_rows if not p["payloadChecked"]),
                                 "negotiatedV3Admitted": sum(1 for p in payload_rows if p.get("result") == "ADMIT" and p["selectedPayload"] == "FactBatchV3"),
                                 "unnegotiatedV2Admitted": sum(1 for p in payload_rows if p.get("result") == "ADMIT" and p["selectedPayload"] == "FactBatchV2"),
                                 "standaloneVectors": "traces/payload-vectors.json"}
check(all(tr["payloadResultsMatch"] for tr in traces.values()), "payload results match on every trace")
S.dump('traces/complete.json', {"traces": [traces[k] for k in ("complete", "complete-rust-dependency-prepared", "complete-rust-prepared-only", "complete-rust-dependency-only",
                                                               "complete-negotiated-multibatch-analyze-subset", "complete-unnegotiated-v2")]})
S.dump('traces/unavailable.json', {"traces": [traces["unavailable-before-analyze"], traces["unavailable-during-analyze"], traces["budget-exhausted"]]})
S.dump('traces/cancel.json', {"traces": [traces["cancel"], traces["cancel-then-frame"]]})
S.dump('traces/fault.json', {"traces": [traces[k] for k in ("fault-identity-echo", "fault-hello-attribution-token-not-echoed", "fault-open-universe-before-negotiation",
                                                            "fault-process-signal", "fault-provider-fault-frame", "fault-unnegotiated-v3-payload", "fault-negotiated-v2-payload",
                                                            "fault-batch-stageid-echoes-analyze-request-ordinal", "fault-candidate-stream-restarts-across-batches",
                                                            "fault-payload-hex-is-canonical-json")]})
S.dump('traces/terminal.json', {"traces": [traces["terminal-post-terminal-frame"], traces["terminal-nonzero-exit-after-complete"], traces["terminal-eof-before-exit"], traces["terminal-complete-before-last-stage"]]})
S.dump('traces/controls.json', dict(controls, helloSchemas=hello_schemas, assertionFailures=failures))
print(json.dumps({"failures": failures, "controls": controls}, indent=1))
sys.exit(1 if failures else 0)
