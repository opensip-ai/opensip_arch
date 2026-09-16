"""Phase 3: provider protocol traces with admitted payloads over the published event machines.

source42.v3 (HC-53): the prose-owned FactBatch payload law (negotiated selection, exact payload bytes, request/batch correlation) is applied at each
FactBatch that reaches ANALYZING.

source44 (HC-58):
  - typescript-semantic exchanges run on native/typescript-protocol2-order.v1.json (ref/protocol_ts2.py); rust-semantic exchanges run on
    native/protocol3-transitions.v1.json (ref/protocol3.py). The source43 file ran both languages on the Rust table;
  - every Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, Coverage/CoverageV3, BudgetExhausted, Cancelled and
    FactBatch carries a payload admitted before the table (ref/provider_exchange.py, ref/provider_wire.py, ref/factbatch.py);
  - Rust dependencyMode/preparedMode come from the admitted OpenUniverseV3 (derivedObservations). Every admitted Rust exchange therefore takes the
    dependency-source frames. P3-09 and P3-10 are exercised only by labelled abstract table tests;
  - a clean pre-Analyze Unavailable is followed by the s9.7 host conversion. In source44 its closedWorld was my reading A; since source45 (HC-60) it is
    the published hostConversionClosedWorld;
  - Snapshot, dependency-source and prepared frames stay abstract events (s9.7 reference scope).
The source43 bytes are preserved at preserved/s43-final/vectors/phase3_traces.py; their source44-kit run is logs/s44-original.1.run_preserved_s43.log.
"""
import copy
import json
import sys

OUTP = '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/'
sys.path.insert(0, OUTP + 'ref')
sys.path.insert(0, OUTP + 'tools')
sys.path.insert(0, OUTP + 'vectors')
import canonical as K  # noqa: E402
import factbatch as FB  # noqa: E402
import payload_fixtures as PF  # noqa: E402
import protocol3 as P  # noqa: E402
import protocol_ts2 as TS2  # noqa: E402
import provider_exchange as X  # noqa: E402
import provider_wire as W  # noqa: E402
import status as S  # noqa: E402

KIT = FB.K
NES = W.NE
MACHINES = {"ts": TS2.TypeScriptProtocol2(), "rust": P.Protocol3()}
failures = []


def check(c, label):
    if not c:
        failures.append(label)


HOST_ASSUMPTIONS = ["actual worker process spawn and supervision", "OS exit status / signal / EOF observation",
                    "frame envelope byte framing and chunk digest verification against the sealed snapshot",
                    "snapshot, dependency-source and prepared custody payloads (abstract events here)",
                    "worker-side recomputation of NativeContextV2 / TypeScriptNativeContextV2 (s9.5)",
                    "deadline and stdout-byte detection", "cancellation delivery timing bounds (security S6)",
                    "commitment recomputation (coverageCommitment, stream commitments) and descriptor signature verification",
                    "that an actual worker emits the constructed payload bytes (the host-side payload law itself is executed here)"]
EXECUTED = ["transition interpretation from typescript-protocol2-order.v1.json (typescript-semantic) and protocol3-transitions.v1.json (rust-semantic): rows, guards, "
            "derived event observations, pre-match/no-match laws, state updates, stage-dependent transitions",
            "handshake payload admission before the table (provider-handshake.schemas.v1.json): schemas, limits, descriptor/identity joins, exact token and identityVersions echoes",
            "startup payload admission (provider-startup.schemas.v1.json): OpenUniverse identity members and universe identity, handshake joins, repository resolution and derived "
            "modes, UniverseAccepted echo, NativeContextVerified join, Unavailable classification/phase/correlation, Coverage wrapper correspondence, terminal coverage, "
            "TypeScript Cancelled interval",
            "FactBatch payload law at every FactBatch reaching ANALYZING (negotiated FactBatchV3 or the language's historical payload; exact bytes; dispatch correlation; companions)",
            "pre-Analyze host conversion after DONE (CoverageResultV3 admission; stage_authority unavailable)",
            "s10 terminal -> StageAuthorityV1 projection validated against the native schema"]
NOT_CONSTRUCTED = ["post-terminal bind_worker_occupancy (fact2 minting, native views, stageReceipts, TargetAttributionV2 projection and capture, C15)",
                   "anchor admission and fact identity of the constructed candidates", "ProviderFault and Complete payload bodies (frame names only)"]


def ev(frame, **kw):
    d = {"frame": frame}
    d.update(kw)
    return d


def record(name, lang, events, expect_rules, expect_phase, expect_terminal, faulted, notes, expect_payload=(), expect_refusal=None, ctx=None,
           extra_checks=None, conversion=False):
    ctx = ctx or PF.exchange_ctx(lang)
    res = X.ProviderExchange(lang, ctx).run(events)
    rules = [t["rule"] for t in res["trace"]]
    flags = [{"afterFrame": e["frame"], "identityNegotiated": s["identityNegotiated"], "sourceBytesSent": s["sourceBytesSent"], "phase": s["phase"]}
             for e, s in zip(events, res["states"])]
    idx_neg = next((i for i, f in enumerate(flags) if f["identityNegotiated"]), None)
    idx_src = next((i for i, f in enumerate(flags) if f["sourceBytesSent"]), None)
    identity_before_source = idx_src is None or (idx_neg is not None and idx_neg < idx_src)
    refusal = res["refusal"]
    host_refusal = refusal is not None and refusal["origin"] == "host-internal"
    authority = None
    if not host_refusal and (res["state"]["terminalKind"] or faulted):
        authority = P.stage_authority(res["state"]["terminalKind"], faulted)
        sa = KIT.admit(authority, NES, "#/$defs/StageAuthorityV1")
        check(sa["ok"], f"{name} stage authority schema")
    ok = rules == expect_rules and res["state"]["phase"] == expect_phase and res["state"]["terminalKind"] == expect_terminal
    check(ok, f"trace {name}: {rules} {res['state']}")
    check(identity_before_source, f"{name} identity before source")
    observed_payload = [(p["result"], p["firstRefusal"]) if p["payloadChecked"] else ("not-validated", None) for p in res["payloads"]]
    check(observed_payload == list(expect_payload), f"{name} FactBatch payload results {observed_payload} != {list(expect_payload)}")
    check(all("payload" in e for e in events if e["frame"] in ("FactBatch", "Hello", "HelloAck", "OpenUniverse", "UniverseAccepted", "NativeContextVerified",
                                                               "Unavailable", "Coverage", "CoverageV3", "BudgetExhausted", "Cancelled")),
          f"{name}: every payload-carrying frame carries a payload")
    observed_refusal = (refusal["frame"], refusal["firstRefusal"], refusal["origin"]) if refusal else None
    check(observed_refusal == expect_refusal, f"{name}: refusal {observed_refusal} != {expect_refusal}")
    check(all(not a["faults"] for a in res["admissions"] if refusal is None or a["step"] != refusal["step"]), f"{name}: an admission other than the refusal faulted")
    if refusal and refusal["origin"] == "provider-return":
        check(authority is not None and refusal["route"] == authority["d9"], f"{name}: provider refusal route {refusal['route']} agrees with the s10 fault projection")
    if host_refusal:
        check(refusal["route"]["errorCode"] == "SYSTEM.OUTCOME.ILLEGAL_STATE", f"{name}: host-authored refusal is a host invariant {refusal['route']}")
    for p in res["payloads"]:
        if p.get("result") == "REFUSE" and p["violations"][0]["origin"] == "provider-return":
            term = p["publicRoute"]["termination"]
            check(authority is not None and (term["class"], term["errorCode"]) == (authority["d9"]["class"], authority["d9"]["code"]),
                  f"{name}: FactBatch refusal route {term} agrees with the s10 fault projection")
    conv = None
    if conversion:
        conv = W.pre_analyze_conversion(X.requests_of(PF.analyze_event(lang), lang))
        conv = {"closedWorld": "published: provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld (HC-60)",
                "faults": conv["faults"], "entries": conv["entries"], "stageAuthority": conv["stageAuthority"],
                "coverage2PayloadDigests": conv["payloadDigests"]}
        check(res["state"]["phase"] == "DONE" and conv["faults"] == [] and authority is not None and conv["stageAuthority"]["d9"] == authority["d9"]
              and all(e["entry"]["closedWorld"] == W.HOST_CONVERSION_CLOSED_WORLD for e in conv["entries"]),
              f"{name}: host conversion after DONE {conv['faults'][:2]}")
    if extra_checks:
        for label, cond in extra_checks(res, flags):
            check(cond, f"{name}: {label}")
    return {"name": name, "provider": lang, "machine": res["machine"], "class": "valid" if not faulted else "invalid", "events": events, "trace": res["trace"],
            "finalState": res["state"], "expectedRules": expect_rules, "matchesExpected": ok, "negotiatedTargetAttribution": res["negotiated"],
            "identityNegotiatedBeforeSourceBytes": identity_before_source, "stateTimeline": flags, "stageAuthority": authority,
            "admissions": res["admissions"], "refusal": refusal, "expectedRefusal": expect_refusal,
            "payloadResults": res["payloads"], "expectedPayloadResults": [list(x) for x in expect_payload], "payloadResultsMatch": observed_payload == list(expect_payload),
            "hostConversion": conv, "executedVsHost": {"executed": EXECUTED, "futureHostAssumptions": HOST_ASSUMPTIONS, "notConstructedHere": NOT_CONSTRUCTED},
            "notes": notes}


SNAP = [ev("SnapshotManifest"), ev("SnapshotFileChunk"), ev("SnapshotFileChunk"), ev("SnapshotSeal"), ev("SnapshotAccepted")]
DEP_EMPTY = [ev("DependencySourceManifest"), ev("DependencySourceSeal"), ev("DependencySourceAccepted")]
DEP_CHUNK = [ev("DependencySourceManifest"), ev("DependencySourceChunk"), ev("DependencySourceSeal"), ev("DependencySourceAccepted")]
PREP = [ev("PreparedOutputManifest"), ev("PreparedOutputChunk"), ev("PreparedOutputSeal"), ev("PreparedOutputAccepted")]
TAIL = [ev("zero-exit"), ev("eof")]
ST = {"ts": PF.startup_events("ts")[1], "rust": PF.startup_events("rust")[1], "rust-prepared": PF.startup_events("rust", prepared=True)[1]}


def start(lang, token=True, prepared=False, ou=None):
    e = ST["rust-prepared" if prepared else lang]
    return [PF.hello(lang, token), PF.ack(lang, token), ou or e["OpenUniverse"], e["UniverseAccepted"]] + SNAP


def ncv(lang, prepared=False):
    return ST["rust-prepared" if prepared else lang]["NativeContextVerified"]


TS_START = ["T2-01", "T2-02", "T2-03", "T2-04", "T2-05", "T2-06", "T2-06", "T2-07", "T2-08"]
TS_TO_ANALYZE = TS_START + ["T2-09", "T2-11"]
RUST_START = ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-08"]
RUST_DEP_EMPTY = ["P3-11", "P3-13", "P3-15"]
RUST_TO_ANALYZE = RUST_START + RUST_DEP_EMPTY + ["P3-20", "P3-22"]
AE = {"ts": PF.analyze_event("ts"), "rust": PF.analyze_event("rust")}
FB_IMP0 = PF.fb(PF.v3("ts-imports", 0, PF.imports_b0()))
FB_IMP1 = PF.fb(PF.v3("ts-imports", 1, PF.imports_b1()))
FB_CALLS0 = PF.fb(PF.v3("ts-calls", 0, PF.calls_b0()))
FB_RUST0 = PF.fb(PF.v3("rust-calls", 0, PF.rust_calls_b0()))
COV_TS0, COV_TS1, COV_R = PF.coverage("ts", 0), PF.coverage("ts", 1), PF.coverage("rust", 0)
A = "ADMIT"
ABSORB4 = ["FAULT-absorb"] * 4
traces = {}

# ================================================================================================ typescript-semantic (typescript-protocol2-order.v1.json)
traces["complete-ts"] = record(
    "complete (TypeScript major 2, two stages, negotiated FactBatchV3)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, COV_TS0, FB_CALLS0, COV_TS1, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-13", "T2-12", "T2-13", "T2-17", "T2-20", "T2-21"], "DONE", "complete", False,
    "one Coverage per stage; Complete only after the last stage", [(A, None), (A, None)], None,
    extra_checks=lambda res, fl: [("stagesCompleted==2", res["state"]["stagesCompleted"] == 2), ("outputSeen", res["state"]["outputSeen"] is True)])

traces["complete-ts-negotiated-multibatch-analyze-subset"] = record(
    "complete (TypeScript; Analyze selects Plan stages 1 and 3; two FactBatchV3 frames continue one candidate stream)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, FB_IMP1, COV_TS0, FB_CALLS0, COV_TS1, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-12", "T2-13", "T2-12", "T2-13", "T2-17", "T2-20", "T2-21"], "DONE", "complete", False,
    "dispatch coordinates per batch (retainedStageOrdinal, analyzeRequestOrdinal, batchIndex, first candidate): (1,0,0,0), (1,0,1,3), (3,1,0,0)",
    [(A, None), (A, None), (A, None)], None,
    extra_checks=lambda res, fl: [("dispatch coordinates", [[p["dispatch"][k] for k in ("retainedStageOrdinal", "analyzeRequestOrdinal", "expectedBatchIndex", "expectedFirstCandidateOrdinal")]
                                                             for p in res["payloads"]] == [[1, 0, 0, 0], [1, 0, 1, 3], [3, 1, 0, 0]]),
                                  ("companions buffered per batch", [len(p["bufferedCompanions"]) for p in res["payloads"]] == [2, 3, 1])])

traces["complete-ts-unnegotiated-v1"] = record(
    "complete (TypeScript; target-attribution-v2 absent; historical FactBatchV1 with batchCommitment)", "ts",
    start("ts", False) + [ncv("ts"), AE["ts"], PF.fb(PF.v1_ts(FB_IMP0["payload"])), COV_TS0, PF.fb(PF.v1_ts(FB_CALLS0["payload"])), COV_TS1, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-13", "T2-12", "T2-13", "T2-17", "T2-20", "T2-21"], "DONE", "complete", False,
    "source44: the typescript-semantic historical payload is delivery.v2 FactBatchV1; occupancy omitted", [(A, None), (A, None)], None, ctx=PF.exchange_ctx("ts", False),
    extra_checks=lambda res, fl: [("not negotiated", res["negotiated"] is False), ("FactBatchV1 selected", all(p["selectedPayload"] == "FactBatchV1" for p in res["payloads"])),
                                  ("occupancy omitted", all(p["occupancy"].startswith("omitted") for p in res["payloads"]))])

traces["unavailable-ts-before-analyze"] = record(
    "unavailable (native-context-mismatch before Analyze; host conversion after DONE)", "ts",
    start("ts") + [ST["ts"]["PreAnalyzeUnavailable"]] + TAIL, TS_START + ["T2-10", "T2-20", "T2-21"], "DONE", "unavailable", False,
    "clean typed terminal: no Analyze, zero facts; the host mints one provider-unavailable CoverageResultV3 per requested key", (), None, conversion=True,
    extra_checks=lambda res, fl: [("observation pre-analyze", res["admissions"][-3]["observations"] == {"unavailablePayload": "pre-analyze"})])

traces["unavailable-ts-immediately-after-analyze"] = record(
    "unavailable (TypeScriptUnavailableV2 before any stage output)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], PF.post_unavailable("ts")] + TAIL, TS_TO_ANALYZE + ["T2-14", "T2-20", "T2-21"], "DONE", "unavailable", False,
    "delivery.v2 unavailableTerminal: immediately after Analyze (outputSeen false)")

traces["fault-ts-unavailable-after-output"] = record(
    "fault: TypeScript Unavailable after stage output", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, COV_TS0, FB_CALLS0, PF.post_unavailable("ts")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-13", "T2-12", "T2-23", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True,
    "source44 changes this conclusion: source43 ran these events on the Rust table and reached DONE/unavailable through P3-25; T2-14 requires outputSeen=false",
    [(A, None), (A, None)], None)

traces["budget-exhausted-ts-analyzing"] = record(
    "budget-exhausted during ANALYZING (TypeScript)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, PF.budget_exhausted("ts", "ts-imports")] + TAIL, TS_TO_ANALYZE + ["T2-12", "T2-15", "T2-20", "T2-21"],
    "DONE", "budget-exhausted", False, "clean typed terminal", [(A, None)], None)

traces["budget-exhausted-ts-ready-complete"] = record(
    "budget-exhausted in READY_COMPLETE (TypeScript)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, COV_TS0, FB_CALLS0, COV_TS1, PF.budget_exhausted("ts", "ts-calls")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-13", "T2-12", "T2-13", "T2-16", "T2-20", "T2-21"], "DONE", "budget-exhausted", False, "T2-16", [(A, None), (A, None)], None)

traces["cancel-ts-native-context-interval"] = record(
    "cancellation in WAIT_NATIVE_CONTEXT_VERIFIED (observedPhase snapshot)", "ts",
    start("ts") + [PF.cancel("ts"), PF.cancelled("ts", "snapshot"), ev("eof")], TS_START + ["T2-18", "T2-19", "T2-21"], "DONE", "cancelled", False,
    "after cancelled only eof is required (terminalLaw)", (), None,
    extra_checks=lambda res, fl: [("cancelPhase", res["state"]["cancelPhase"] == "WAIT_NATIVE_CONTEXT_VERIFIED")])

traces["cancel-ts-ready-analyze"] = record(
    "cancellation in READY_ANALYZE (observedPhase snapshot)", "ts",
    start("ts") + [ncv("ts"), PF.cancel("ts"), PF.cancelled("ts", "snapshot"), ev("eof")], TS_START + ["T2-09", "T2-18", "T2-19", "T2-21"], "DONE", "cancelled", False,
    "including after the NativeContextVerified emission", (), None,
    extra_checks=lambda res, fl: [("cancelPhase", res["state"]["cancelPhase"] == "READY_ANALYZE")])

traces["cancel-ts-analyzing"] = record(
    "cancellation during ANALYZING (TypeScript; inherited interval)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, PF.cancel("ts"), PF.cancelled("ts", "analysis"), ev("eof")], TS_TO_ANALYZE + ["T2-12", "T2-18", "T2-19", "T2-21"],
    "DONE", "cancelled", False, "interrupted (130); no facts", [(A, None)], None)

traces["fault-ts-cancelled-observed-phase-universe"] = record(
    "fault: Cancelled reports observedPhase universe for a Cancel in the native-context interval", "ts",
    start("ts") + [PF.cancel("ts"), PF.cancelled("ts", "universe"), ev("eof")], TS_START + ["T2-18", "payload:Cancelled-refused(cb24.CANCELLED_OBSERVED_PHASE)", "FAULT-absorb"],
    "FAULT", None, True, "provider-startup cancellation law", (), ("Cancelled", "cb24.CANCELLED_OBSERVED_PHASE", "provider-return"))

traces["fault-ts-pre-analyze-unavailable-after-ncv"] = record(
    "fault: PreAnalyzeUnavailableV1 after NativeContextVerified", "ts",
    start("ts") + [ncv("ts"), ST["ts"]["PreAnalyzeUnavailable"]] + TAIL, TS_START + ["T2-09", "payload:Unavailable-refused(cb24.UNAVAILABLE_PHASE)", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "outside WAIT_NATIVE_CONTEXT_VERIFIED the payload is PROVIDER.PROTOCOL_VIOLATION", (), ("Unavailable", "cb24.UNAVAILABLE_PHASE", "provider-return"))

traces["fault-ts-post-analyze-unavailable-in-native-context-interval"] = record(
    "fault: TypeScriptUnavailableV2 inside the native-context interval", "ts",
    start("ts") + [PF.post_unavailable("ts")] + TAIL, TS_START + ["payload:Unavailable-refused(cb24.UNAVAILABLE_PHASE)", "FAULT-absorb", "FAULT-absorb"],
    "FAULT", None, True, "inside the interval the post-Analyze payload is PROVIDER.PROTOCOL_VIOLATION", (), ("Unavailable", "cb24.UNAVAILABLE_PHASE", "provider-return"))

traces["fault-ts-hello-attribution-token-not-echoed"] = record(
    "fault: Hello offers target-attribution-v2, HelloAck omits it", "ts",
    [PF.hello("ts", True), PF.ack("ts", False), ST["ts"]["OpenUniverse"], ev("SnapshotManifest")],
    ["T2-01", "payload:HelloAck-refused(cb24.HELLOACK_TOKEN_ECHO)", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True,
    "no payload version is selected and no source byte is sent", (), ("HelloAck", "cb24.HELLOACK_TOKEN_ECHO", "provider-return"),
    extra_checks=lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-ts-open-universe-key-not-native-identity"] = record(
    "fault: host OpenUniverse universeKey is the raw SHA-256 of resolvedInputs, not the native semantic-universe identity", "ts",
    [PF.hello("ts"), PF.ack("ts"), dict(ST["ts"]["OpenUniverse"], payload=dict(ST["ts"]["OpenUniverse"]["payload"],
                                                                                universeKey="sha256:" + K.raw_digest(ST["ts"]["OpenUniverse"]["payload"]["universe"]["resolvedInputs"]))),
     ST["ts"]["UniverseAccepted"], ev("SnapshotManifest")],
    ["T2-01", "T2-02", "payload:OpenUniverse-refused(cb24.OPEN_UNIVERSE_UNIVERSE_KEY)", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True,
    "host-authored payload refused before the table: a host invariant; OpenUniverse state updates never apply", (),
    ("OpenUniverse", "cb24.OPEN_UNIVERSE_UNIVERSE_KEY", "host-internal"),
    extra_checks=lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-ts-provider-fault-frame"] = record(
    "fault: ProviderFault frame on typescript-semantic", "ts",
    start("ts") + [ev("ProviderFault")] + TAIL, TS_START + ["T2-23", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True,
    "source44 changes this conclusion: the TypeScript protocol-2 table has no ProviderFault row. source43 ran P3-28 and reached DONE/provider-fault")

traces["fault-ts-batch-stageid-echoes-analyze-request-ordinal"] = record(
    "fault: second stage's FactBatch echoes its Analyze stageOrdinal as stageId", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, COV_TS0, PF.fb(dict(FB_CALLS0["payload"], stageId="1")), COV_TS1, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "T2-13", "payload:FactBatch-refused(PROVIDER_RETURN_STAGE_ID)"] + ABSORB4, "FAULT", None, True,
    "FactBatch.stageId echoes the requested C-2 stageId text, never stageOrdinal", [(A, None), ("REFUSE", "PROVIDER_RETURN_STAGE_ID")],
    ("FactBatch", "PROVIDER_RETURN_STAGE_ID", "provider-return"))

traces["fault-ts-candidate-stream-restarts-across-batches"] = record(
    "fault: second FactBatch of one stage restarts candidateOrdinal at 0", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, PF.fb(PF.renumber(FB_IMP1["payload"], 0)), COV_TS0, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "payload:FactBatch-refused(PROVIDER_RETURN_CANDIDATE_STREAM)"] + ABSORB4, "FAULT", None, True,
    "the per-stage candidate stream continues at expectedFirstCandidateOrdinal 3", [(A, None), ("REFUSE", "PROVIDER_RETURN_CANDIDATE_STREAM")],
    ("FactBatch", "PROVIDER_RETURN_CANDIDATE_STREAM", "provider-return"))

traces["fault-ts-unnegotiated-v2-payload"] = record(
    "fault: TypeScript sends FactBatchV2 without target-attribution-v2", "ts",
    start("ts", False) + [ncv("ts"), AE["ts"], PF.fb(PF.v2(FB_IMP0["payload"])), COV_TS0, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["payload:FactBatch-refused(cb24.FACT_BATCH_V1_SCHEMA)"] + ABSORB4, "FAULT", None, True,
    "source44: the historical TypeScript payload is FactBatchV1", [("REFUSE", "cb24.FACT_BATCH_V1_SCHEMA")], ("FactBatch", "cb24.FACT_BATCH_V1_SCHEMA", "provider-return"),
    ctx=PF.exchange_ctx("ts", False))

traces["fault-ts-v1-batch-commitment-without-domain"] = record(
    "fault: FactBatchV1 batchCommitment omits the fact-batch domain", "ts",
    start("ts", False) + [ncv("ts"), AE["ts"], PF.fb(PF.v1_ts(FB_IMP0["payload"], commitment="sha256:" + K.sha256_hex(b"no-domain"))), COV_TS0, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["payload:FactBatch-refused(cb24.FACT_BATCH_V1_BATCH_COMMITMENT)"] + ABSORB4, "FAULT", None, True,
    "delivery.v2 commitments.domains.factBatch", [("REFUSE", "cb24.FACT_BATCH_V1_BATCH_COMMITMENT")],
    ("FactBatch", "cb24.FACT_BATCH_V1_BATCH_COMMITMENT", "provider-return"), ctx=PF.exchange_ctx("ts", False))

rev_cov = PF.coverage("ts", 0, dict(COV_TS0["payload"], entries=list(reversed(COV_TS0["payload"]["entries"]))))
traces["fault-ts-coverage-entries-reordered"] = record(
    "fault: Coverage entries do not follow requestedCoverageDomain.keys order", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, rev_cov, COV_TS1, ev("Complete")] + TAIL,
    TS_TO_ANALYZE + ["T2-12", "payload:Coverage-refused(cb24.COVERAGE_KEY_CORRESPONDENCE)"] + ["FAULT-absorb"] * 4, "FAULT", None, True,
    "entries[i] answers keys[i]", [(A, None)], ("Coverage", "cb24.COVERAGE_KEY_CORRESPONDENCE", "provider-return"))

traces["fault-ts-process-stdout-byte"] = record(
    "fault: stdout byte mid-ANALYZING (TypeScript)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], FB_IMP0, ev("stdout-byte"), COV_TS0], TS_TO_ANALYZE + ["T2-12", "T2-22", "FAULT-absorb"], "FAULT", None, True,
    "operational-failed PROVIDER.PROTOCOL_VIOLATION", [(A, None)], None)

traces["terminal-ts-complete-before-last-stage"] = record(
    "Complete before the last stage's Coverage (TypeScript)", "ts",
    start("ts") + [ncv("ts"), AE["ts"], COV_TS0, ev("Complete")], TS_TO_ANALYZE + ["T2-13", "T2-23"], "FAULT", None, True,
    "T2-13 resolved ANALYZING because stageIndex 1 != stageCount 2; Complete has no ANALYZING row")

# ================================================================================================ rust-semantic (protocol3-transitions.v1.json)
traces["complete-rust-empty-dependency-set"] = record(
    "complete (Rust; admitted OpenUniverseV3 derives dependencyMode=true; empty dependency set takes manifest, seal and accepted)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, COV_R, ev("Complete")] + TAIL,
    RUST_TO_ANALYZE + ["P3-23", "P3-24", "P3-27", "P3-31", "P3-32"], "DONE", "complete", False,
    "dependency frames are abstract events; the dependency set's emptiness is a fixture assumption (s9.7 reference scope)", [(A, None)], None,
    extra_checks=lambda res, fl: [("derived modes", (res["state"]["dependencyMode"], res["state"]["preparedMode"]) == (True, False))])

traces["complete-rust-dependency-prepared"] = record(
    "complete (Rust dependency chunk + prepared custody; imported-descriptor preparation)", "rust",
    start("rust", prepared=True) + DEP_CHUNK + PREP + [ncv("rust", True), AE["rust"], FB_RUST0, COV_R, ev("Complete")] + TAIL,
    RUST_START + ["P3-11", "P3-12", "P3-13", "P3-14", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20", "P3-22", "P3-23", "P3-24", "P3-27", "P3-31", "P3-32"],
    "DONE", "complete", False,
    "fixture: synthetic preparedOutputSetId over the retained rust-mixed resolvedInputs. The Analyze/FactBatch/Coverage coordinates reuse the retained non-prepared universe",
    [(A, None)], None, ctx=PF.exchange_ctx("rust", prepared=True),
    extra_checks=lambda res, fl: [("derived modes", (res["state"]["dependencyMode"], res["state"]["preparedMode"]) == (True, True))])

traces["complete-rust-unnegotiated-v2"] = record(
    "complete (Rust; target-attribution-v2 absent; historical FactBatchV2)", "rust",
    start("rust", False) + DEP_EMPTY + [ncv("rust"), AE["rust"], PF.fb(PF.v2(FB_RUST0["payload"])), COV_R, ev("Complete")] + TAIL,
    RUST_TO_ANALYZE + ["P3-23", "P3-24", "P3-27", "P3-31", "P3-32"], "DONE", "complete", False, "FactBatchV2 admitted; occupancy omitted", [(A, None)], None,
    ctx=PF.exchange_ctx("rust", False),
    extra_checks=lambda res, fl: [("not negotiated", res["negotiated"] is False), ("FactBatchV2 selected", res["payloads"][0]["selectedPayload"] == "FactBatchV2")])

traces["unavailable-rust-before-analyze"] = record(
    "unavailable (Rust native-context-mismatch before Analyze; host conversion after DONE)", "rust",
    start("rust") + DEP_EMPTY + [ST["rust"]["PreAnalyzeUnavailable"]] + TAIL, RUST_START + RUST_DEP_EMPTY + ["P3-21", "P3-31", "P3-32"], "DONE", "unavailable", False,
    "P3-21 admits only PreAnalyzeUnavailableV1", (), None, conversion=True)

traces["unavailable-rust-during-analyze"] = record(
    "unavailable during ANALYZING after one FactBatch (Rust UnavailableV3)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, PF.post_unavailable("rust")] + TAIL, RUST_TO_ANALYZE + ["P3-23", "P3-25", "P3-31", "P3-32"],
    "DONE", "unavailable", False, "facts before the terminal admitted (factsAdmitted=before-terminal)", [(A, None)], None)

traces["budget-exhausted-rust"] = record(
    "budget-exhausted during ANALYZING (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, PF.budget_exhausted("rust", "rust-calls")] + TAIL, RUST_TO_ANALYZE + ["P3-23", "P3-26", "P3-31", "P3-32"],
    "DONE", "budget-exhausted", False, "clean typed terminal; stage partial", [(A, None)], None)

traces["cancel-rust"] = record(
    "cancellation during ANALYZING (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, PF.cancel("rust"), PF.cancelled("rust", "analysis")] + TAIL,
    RUST_TO_ANALYZE + ["P3-23", "P3-29", "P3-30", "P3-31", "P3-32"], "DONE", "cancelled", False, "interrupted (130); CancelledV2 observedPhase not validated here", [(A, None)], None)

traces["cancel-rust-then-frame"] = record(
    "cancel requested, worker sends FactBatch instead of Cancelled (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], PF.cancel("rust"), FB_RUST0, PF.cancelled("rust", "analysis")],
    RUST_TO_ANALYZE + ["P3-29", "P3-34", "FAULT-absorb"], "FAULT", None, True, "WAIT_CANCELLED admits only Cancelled; the FactBatch payload is never validated",
    [("not-validated", None)], None)

no_fact = [c for c in PF.caps("rust") if c != "fact-identity-fact2"]
traces["fault-rust-helloack-identity-token-missing"] = record(
    "fault: HelloAck does not carry an identity token (Rust)", "rust",
    [PF.hello("rust"), PF.ack("rust", payload=dict(PF.ack_payload("rust"), capabilities=no_fact)), ST["rust"]["OpenUniverse"], ev("SnapshotManifest")],
    ["P3-01", "payload:HelloAck-refused(cb24.HELLOACK_SCHEMA)", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True,
    "the schema's identity-token containment refuses before the echo; no source byte is sent", (), ("HelloAck", "cb24.HELLOACK_SCHEMA", "provider-return"),
    extra_checks=lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-rust-open-universe-mode-boolean-member"] = record(
    "fault: host OpenUniverseV3 carries a dependencyMode member", "rust",
    [PF.hello("rust"), PF.ack("rust"), dict(ST["rust"]["OpenUniverse"], payload=dict(ST["rust"]["OpenUniverse"]["payload"], dependencyMode=False))],
    ["P3-01", "P3-02", "payload:OpenUniverse-refused(cb24.OPEN_UNIVERSE_SCHEMA)"], "FAULT", None, True,
    "modes are host-derived observations, never wire members", (), ("OpenUniverse", "cb24.OPEN_UNIVERSE_SCHEMA", "host-internal"),
    extra_checks=lambda res, fl: [("sourceBytesSent false", res["state"]["sourceBytesSent"] is False)])

traces["fault-rust-dependency-custody-skipped"] = record(
    "fault: admitted OpenUniverseV3 then NativeContextVerified without dependency-source custody", "rust",
    start("rust") + [ncv("rust")], RUST_START + ["P3-34"], "FAULT", None, True,
    "P3-08 went to READY_DEPENDENCY_MANIFEST because dependencyMode is derived true; NativeContextVerified has no row there")

traces["fault-rust-process-signal"] = record(
    "fault: signal-death mid-ANALYZING, later frames absorbed (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, ev("signal-death"), COV_R, ev("Complete")],
    RUST_TO_ANALYZE + ["P3-23", "P3-33", "FAULT-absorb", "FAULT-absorb"], "FAULT", None, True, "facts already batched are NOT admitted", [(A, None)], None)

traces["fault-rust-provider-fault-frame"] = record(
    "ProviderFault frame from a pre-complete phase (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ev("ProviderFault")] + TAIL, RUST_START + RUST_DEP_EMPTY + ["P3-28", "P3-31", "P3-32"], "DONE", "provider-fault", True,
    "a clean exchange end does not rescue a provider-fault terminal: no facts, no Run")

traces["fault-rust-unnegotiated-v3-payload"] = record(
    "fault: FactBatchV3 payload without the negotiated token (Rust)", "rust",
    start("rust", False) + DEP_EMPTY + [ncv("rust"), AE["rust"], FB_RUST0, COV_R, ev("Complete")] + TAIL,
    RUST_TO_ANALYZE + ["payload:FactBatch-refused(PROVIDER_RETURN_UNNEGOTIATED_V3)"] + ABSORB4, "FAULT", None, True,
    "a FactBatchV3 payload without the token is PROVIDER.PROTOCOL_VIOLATION", [("REFUSE", "PROVIDER_RETURN_UNNEGOTIATED_V3")],
    ("FactBatch", "PROVIDER_RETURN_UNNEGOTIATED_V3", "provider-return"), ctx=PF.exchange_ctx("rust", False))

traces["fault-rust-negotiated-v2-payload"] = record(
    "fault: historical FactBatchV2 payload after target-attribution-v2 was negotiated (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], PF.fb(PF.v2(FB_RUST0["payload"])), COV_R, ev("Complete")] + TAIL,
    RUST_TO_ANALYZE + ["payload:FactBatch-refused(PROVIDER_RETURN_SCHEMA)"] + ABSORB4, "FAULT", None, True,
    "that language's historical payload with the token is PROVIDER.PROTOCOL_VIOLATION", [("REFUSE", "PROVIDER_RETURN_SCHEMA")],
    ("FactBatch", "PROVIDER_RETURN_SCHEMA", "provider-return"))

JSON_HEX = json.dumps(FB_RUST0["payload"]["candidates"][0]["decodedRelationPayload"], sort_keys=True, separators=(",", ":")).encode().hex()
bad_bytes = copy.deepcopy(FB_RUST0["payload"])
bad_bytes["candidates"][0]["canonicalRelationPayloadHex"] = JSON_HEX
traces["fault-rust-payload-hex-is-canonical-json"] = record(
    "fault: canonicalRelationPayloadHex transcribes canonical JSON UTF-8 instead of the deterministic-CBOR bytes (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], PF.fb(bad_bytes), COV_R, ev("Complete")] + TAIL,
    RUST_TO_ANALYZE + ["payload:FactBatch-refused(PROVIDER_RETURN_PAYLOAD_CBOR)"] + ABSORB4, "FAULT", None, True,
    "the hex transcribes the same CBOR bytes, never canonical JSON UTF-8", [("REFUSE", "PROVIDER_RETURN_PAYLOAD_CBOR")],
    ("FactBatch", "PROVIDER_RETURN_PAYLOAD_CBOR", "provider-return"))

traces["terminal-rust-post-terminal-frame"] = record(
    "terminal: FactBatch after Complete (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], COV_R, ev("Complete"), FB_RUST0, ev("zero-exit")],
    RUST_TO_ANALYZE + ["P3-24", "P3-27", "post-terminal-frame", "FAULT-absorb"], "FAULT", "complete", True,
    "terminalKind was recorded but the exchange faulted; the payload is never validated", [("not-validated", None)], None)

traces["terminal-rust-nonzero-exit-after-complete"] = record(
    "terminal: nonzero exit after Complete (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], COV_R, ev("Complete"), ev("nonzero-exit")], RUST_TO_ANALYZE + ["P3-24", "P3-27", "P3-33"],
    "FAULT", "complete", True, "Complete without zero exit is a fault")

traces["terminal-rust-eof-before-exit"] = record(
    "terminal: eof before zero-exit (Rust)", "rust",
    start("rust") + DEP_EMPTY + [ncv("rust"), AE["rust"], COV_R, ev("Complete"), ev("eof")], RUST_TO_ANALYZE + ["P3-24", "P3-27", "P3-34"],
    "FAULT", "complete", True, "WAIT_ZERO_EXIT has no eof row")

# ================================================================================================ abstract table tests (event-only; no whole-wire claim)
IV = dict(P.IDENTITY_VERSIONS)


def abstract(name, lang, events, expect_rules, expect_phase, expect_terminal, law, notes):
    res = MACHINES[lang].run(events)
    rules = [t["rule"] for t in res["trace"]]
    ok = rules == expect_rules and res["state"]["phase"] == expect_phase and res["state"]["terminalKind"] == expect_terminal
    check(ok, f"abstract {name}: {rules} {res['state']}")
    return {"name": name, "provider": lang, "standing": "abstract table test: event-only fields; makes no whole-wire claim", "law": law, "events": events,
            "trace": res["trace"], "finalState": res["state"], "expectedRules": expect_rules, "matchesExpected": ok, "notes": notes}


def rust_hs(caps):
    return [{"frame": "Hello", "expectedCapabilities": caps, "identityVersions": IV}, {"frame": "HelloAck", "capabilities": caps, "identityVersions": IV}]


RC = PF.caps("rust")
R_SNAP = [ev("UniverseAccepted")] + SNAP
abstract_tests = [
    abstract("abstract-P3-09", "rust", rust_hs(RC) + [ev("OpenUniverse", dependencyMode=False, preparedMode=True)] + R_SNAP + PREP + [ev("NativeContextVerified")],
             ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-09", "P3-16", "P3-17", "P3-18", "P3-19", "P3-20"], "READY_ANALYZE", None,
             "protocol3-transitions.v1.json#/derivedObservations ('P3-09 and P3-10 are therefore unreachable from an admitted major-3 OpenUniverse')",
             "closed guard partition only"),
    abstract("abstract-P3-10", "rust", rust_hs(RC) + [ev("OpenUniverse", dependencyMode=False, preparedMode=False)] + R_SNAP + [ev("NativeContextVerified")],
             ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-06", "P3-06", "P3-07", "P3-10", "P3-20"], "READY_ANALYZE", None,
             "protocol3-transitions.v1.json#/derivedObservations", "closed guard partition only"),
    abstract("abstract-rust-open-universe-before-negotiation", "rust", rust_hs([c for c in RC if c != "coverage-v3"]) + [ev("OpenUniverse", dependencyMode=True, preparedMode=False)],
             ["P3-01", "P3-02", "P3-34"], "FAULT", None, "protocol3-transitions.v1.json#/guardLaw",
             "an admitted HelloAck always carries the four identity tokens (RustCapabilitiesV3 allOf contains), so this guard path is table-only"),
    abstract("abstract-ts-open-universe-before-negotiation", "ts",
             [ev("Hello"), ev("HelloAck", observations={"capabilities": [c for c in PF.caps("ts") if c != "coverage-v3"]}), ev("OpenUniverse")],
             ["T2-01", "T2-02", "T2-23"], "FAULT", None, "typescript-protocol2-order.v1.json T2-03 guard", "table-only for the same reason"),
    abstract("abstract-ts-unavailable-observation-partition", "ts",
             [ev("Hello"), ev("HelloAck", observations={"capabilities": PF.caps("ts")}), ev("OpenUniverse"), ev("UniverseAccepted")] + SNAP +
             [ev("Unavailable", observations={"unavailablePayload": "post-analyze"})],
             TS_START + ["T2-23"], "FAULT", None, "typescript-protocol2-order.v1.json T2-10 guard / eventObservations.unavailablePayload",
             "payload admission refuses this earlier on the wire (cb24.UNAVAILABLE_PHASE); the table alone also faults")]

# ================================================================================================ controls
controls = {"machines": {}}
all_traces = list(traces.values())
for lang, table_name in (("ts", "typescript-protocol2-order.v1.json"), ("rust", "protocol3-transitions.v1.json")):
    m = MACHINES[lang]
    wire = sorted({t["rule"] for tr in all_traces if tr["provider"] == lang for t in tr["trace"]})
    abst = sorted({t["rule"] for tr in abstract_tests if tr["provider"] == lang for t in tr["trace"]})
    rows = {r["id"] for r in m.rules}
    c = {"table": table_name, "ruleCount": len(m.rules), "pairwiseDisjointOverlaps": m.pairwise_disjoint(), "rulesExercisedByWireTraces": wire,
         "rulesExercisedByAbstractTests": abst, "rowsNotExercised": sorted(rows - set(wire) - set(abst)),
         "rowsOnlyInAbstractTests": sorted((rows & set(abst)) - set(wire))}
    check(c["pairwiseDisjointOverlaps"] == [], f"{lang} disjoint rows")
    check(c["rowsNotExercised"] == [], f"{lang} every published row exercised {c['rowsNotExercised']}")
    controls["machines"][lang] = c
check(controls["machines"]["rust"]["rowsOnlyInAbstractTests"] == ["P3-09", "P3-10"], f"only P3-09/P3-10 are table-only {controls['machines']['rust']['rowsOnlyInAbstractTests']}")
check(controls["machines"]["ts"]["rowsOnlyInAbstractTests"] == [], f"no TypeScript row is table-only {controls['machines']['ts']['rowsOnlyInAbstractTests']}")
payload_rows = [p for tr in all_traces for p in tr["payloadResults"]]
controls["factBatchPayloads"] = {"total": len(payload_rows), "validated": sum(1 for p in payload_rows if p["payloadChecked"]),
                                 "admittedBySelectedPayload": {k: sum(1 for p in payload_rows if p.get("result") == "ADMIT" and p["selectedPayload"] == k)
                                                               for k in ("FactBatchV3", "FactBatchV1", "FactBatchV2")},
                                 "refused": sorted(p["firstRefusal"] for p in payload_rows if p.get("result") == "REFUSE"),
                                 "notValidatedBeforePayload": sum(1 for p in payload_rows if not p["payloadChecked"]),
                                 "standaloneVectors": ["traces/payload-vectors.json", "traces/startup-vectors.json"]}
admissions = [a for tr in all_traces for a in tr["admissions"]]
controls["payloadAdmissions"] = {"framesAdmitted": {}, "refusals": sorted((tr["refusal"]["frame"], tr["refusal"]["firstRefusal"], tr["refusal"]["origin"])
                                                                          for tr in all_traces if tr["refusal"])}
for a in admissions:
    if a["frame"] in ("Hello", "HelloAck", "OpenUniverse", "UniverseAccepted", "NativeContextVerified", "Unavailable", "Coverage", "CoverageV3", "BudgetExhausted",
                      "Cancelled", "FactBatch", "Analyze") and not a["faults"]:
        controls["payloadAdmissions"]["framesAdmitted"][a["frame"]] = controls["payloadAdmissions"]["framesAdmitted"].get(a["frame"], 0) + 1
check(all(tr["payloadResultsMatch"] for tr in all_traces), "payload results match on every trace")
controls["assertionFailures"] = failures
by = {k: [] for k in ("complete", "unavailable", "cancel", "fault", "terminal")}
for k, tr in traces.items():
    bucket = "unavailable" if k.startswith(("unavailable", "budget")) else k.split("-")[0]
    by[bucket].append(tr)
for bucket, rows in by.items():
    S.dump(f"traces/{bucket}.json", {"traces": rows})
S.dump("traces/abstract.json", {"standing": "abstract table tests: event-only fields, no whole-wire claim", "tests": abstract_tests})
S.dump("traces/controls.json", controls)
print(json.dumps({"failures": failures, "controls": controls}, indent=1))
sys.exit(1 if failures else 0)
