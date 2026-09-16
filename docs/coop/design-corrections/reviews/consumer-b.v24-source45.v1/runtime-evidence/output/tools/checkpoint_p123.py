import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/tools')
import hc_source42 as HC
import hc_source44 as HC44
import hc_source45 as HC45
import status as S

OUT = S.OUT
p1 = json.load(open(OUT + 'vectors/phase1-canonical.json'))
p2 = json.load(open(OUT + 'vectors/capability-manifests.json'))
p3 = json.load(open(OUT + 'traces/controls.json'))
# source42.v3 (HC-53): the provider-trace requirements also require the charter-incorporated FactBatch payload law, executed in the
# payload-carrying exchanges (traces/*.json payloadResults) and in the standalone vectors (traces/payload-vectors.json).
p3p = json.load(open(OUT + 'traces/payload-vectors.json'))
# source44 (HC-57/HC-58): per-language historical payloads; handshake/startup/coverage/terminal/cancel payload admission; TypeScript protocol-2 table;
# derived Rust modes; pre-Analyze host conversion (traces/startup-vectors.json, traces/abstract.json)
p3s = json.load(open(OUT + 'traces/startup-vectors.json'))
p3a = json.load(open(OUT + 'traces/abstract.json'))
assert p1["assertionFailures"] == [] and p2["assertionFailures"] == [] and p3["assertionFailures"] == [] and p3p["assertionFailures"] == [] and p3s["assertionFailures"] == []
trace_files = {k: json.load(open(OUT + f'traces/{k}.json'))["traces"] for k in ("complete", "unavailable", "cancel", "fault", "terminal")}
all_traces = [t for ts in trace_files.values() for t in ts]
assert all(t["matchesExpected"] and t["payloadResultsMatch"] and "executedVsHost" in t for t in all_traces)
assert all(t["matchesExpected"] for t in p3a["tests"])
payloads = [p for t in all_traces for p in t["payloadResults"]]
fb = p3["factBatchPayloads"]
assert fb["validated"] + fb["notValidatedBeforePayload"] == fb["total"] == len(payloads) and all(v > 0 for v in fb["admittedBySelectedPayload"].values())
machines = p3["machines"]
assert all(m["rowsNotExercised"] == [] and m["pairwiseDisjointOverlaps"] == [] for m in machines.values())
assert machines["rust"]["rowsOnlyInAbstractTests"] == ["P3-09", "P3-10"] and machines["ts"]["rowsOnlyInAbstractTests"] == []
conv = p3s["conversion"]["determinacyResolution"]["measured"]
assert all(conv.values()) and p3s["conversion"]["ownersAgree"] and p3s["conversion"]["publishedAdmitsClosedWorldV2"]
groups = p3p["groups"]
st = S.load_status()
for rid in ['R-H-HELPER', 'R-CVE1-EIGHT-TYPES', 'R-LEXICAL-ADMISSION', 'R-SEMANTIC-VS-OPERATIONAL', 'R-RAW-VS-PARSED', 'R-ACYCLIC-JOINS']:
    S.set_status(st, rid, 'executed', artifact='vectors/phase1-canonical.json')
S.set_status(st, 'R-CVE1-EIGHT-TYPES', 'executed', artifact='vectors/cve1-eight-types.json')
S.set_status(st, 'R-LEXICAL-ADMISSION', 'executed', first_refusal='raw-input lexical boundary (see firstRefusal per vector)')
S.save_status(st)
S.write_checkpoint(1, st, ['ref/canonical.py', 'ref/schemas.py', 'ref/cve1.py', 'vectors/phase1_canonical.py', 'vectors/phase1-canonical.json', 'vectors/cve1-eight-types.json'], [],
                   "C/H, CVE1, raw lexical admission, raw-vs-parsed, semantic-vs-operational and acyclic-join vectors executed with assertions (exit 0). Chain vector is explanatory (no replay). "
                   "source45: reused exact source42 measurement (selfcheck/s45-provenance.json).")
for rid in ['R-CAP-ADMISSION', 'R-CAP-NAMED-GATES']:
    S.set_status(st, rid, 'executed', artifact='vectors/capability-manifests.json', first_refusal='per negative: ADM-TYPE|ADM-CLOSED|ADM-DOMAIN|ADM-ORDER|CVE1-ENCODE|LEX_*')
S.save_status(st)
S.write_checkpoint(2, st, ['vectors/phase2_capmanifest.py', 'vectors/capability-manifests.json'], [],
                   "Four gates in registry gateOrder before CVE1 encoding; masking recorded; successor RELATION-DOMAIN-V2/LADDER mirror drift-checked. "
                   "source45: reused exact source42 measurement (selfcheck/s45-provenance.json).")
law = ("provider payload law applied before the published machines: negotiated FactBatchV3 or the language's historical payload (typescript-semantic FactBatchV1 with "
       "recomputed batchCommitment, rust-semantic FactBatchV2), deterministic-CBOR payload bytes, DispatchBindingV1 request/batch correlation and companions "
       "(HC-53, HC-57); handshake, startup, coverage, terminal and cancellation payloads admitted (HC-58)")
refused = {t["name"]: [t["refusal"]["firstRefusal"]] if t["refusal"] else [] for t in all_traces}
by_lang = {lang: sum(1 for t in all_traces if t["provider"] == lang) for lang in ("ts", "rust")}
trace_notes = {
    'R-TRACE-COMPLETE': f"traces/complete.json: {len(trace_files['complete'])} complete traces: TypeScript on typescript-protocol2-order.v1.json (negotiated two-stage, "
                        f"multi-batch Analyze subset, unnegotiated FactBatchV1) and Rust on protocol3-transitions.v1.json (empty dependency set, dependency+prepared "
                        f"imported-descriptor, unnegotiated FactBatchV2), every frame payload admitted; {law}.",
    'R-TRACE-UNAVAILABLE': (f"traces/unavailable.json: {len(trace_files['unavailable'])} traces. Pre-Analyze PreAnalyzeUnavailableV1 (T2-10 / P3-21) is followed after "
                            f"DONE by the s9.7 host conversion (CoverageResultV3 admitted, stage_authority unavailable). The closedWorld of those entries is "
                            f"the source45 published hostConversionClosedWorld. Source44 MUST M-s44-1 is resolved: both owners agree, the value admits, "
                            f"identities are stable, and every source44 candidate refuses (traces/startup-vectors.json#/conversion/determinacyResolution, measured {conv}). "
                            f"Also: post-Analyze TypeScriptUnavailableV2 (T2-14), Rust UnavailableV3 after output (P3-25), and BudgetExhausted in ANALYZING and "
                            f"READY_COMPLETE."),
    'R-TRACE-CANCEL': (f"traces/cancel.json: {len(trace_files['cancel'])} traces. TypeScript Cancel in WAIT_NATIVE_CONTEXT_VERIFIED and READY_ANALYZE with "
                       f"observedPhase snapshot (T2-18/T2-19, eof only), TypeScript and Rust in ANALYZING, and a Rust FactBatch in WAIT_CANCELLED that faults "
                       f"before payload validation."),
    'R-TRACE-FAULT': (f"traces/fault.json: {len(trace_files['fault'])} traces with first refusals {sorted(k for t in trace_files['fault'] for k in refused[t['name']])}. "
                      f"Worker refusals are routed to the s10 fault projection and host-authored OpenUniverse refusals to a host invariant. Also: TypeScript "
                      f"Unavailable after output (T2-23), TypeScript ProviderFault (no T2 row), Rust dependency custody skipped (P3-34), and process faults."),
    'R-TRACE-IDENTITY-BEFORE-SOURCE': ("identityNegotiated precedes sourceBytesSent on every trace (stateTimeline). HelloAck refusals and host OpenUniverse refusals occur "
                                       "before any source byte. The optional target-attribution-v2 token is not an identity token, but its echo is exact."),
    'R-TRACE-TERMINAL': f"traces/terminal.json: {len(trace_files['terminal'])} terminal/post-terminal traces; a post-terminal FactBatch faults before payload validation.",
    'R-TRACE-EXECUTED-VS-HOST': (f"executedVsHost on every trace ({by_lang}). Executed: both published machines with derived observations, handshake/startup/coverage/"
                                 f"terminal/cancel payload admission, the FactBatch payload law, the pre-Analyze host conversion and the s10 projection. futureHostAssumptions: "
                                 f"process/OS/framing, custody payloads, commitment recomputation, descriptor signatures, actual worker emission. Abstract table tests "
                                 f"(traces/abstract.json: {len(p3a['tests'])}) make no whole-wire claim. Standalone traces/payload-vectors.json: {len(p3p['vectors'])} "
                                 f"vectors {json.dumps(groups)}. traces/startup-vectors.json: {len(p3s['vectors'])} vectors {json.dumps(p3s['groups'])}. Actual "
                                 f"worker-process enforcement is not claimed.")}
for rid, notes in trace_notes.items():
    S.set_status(st, rid, 'executed', artifact='traces/', notes=notes)
S.save_status(st)
cp = S.write_checkpoint(3, st, ['ref/protocol3.py', 'ref/protocol_ts2.py', 'ref/factbatch.py', 'ref/wirecbor.py', 'ref/provider_wire.py', 'ref/provider_exchange.py',
                                'vectors/payload_fixtures.py', 'vectors/phase3_traces.py', 'vectors/phase3_payload_vectors.py', 'vectors/phase3_startup_vectors.py',
                                'traces/complete.json', 'traces/unavailable.json', 'traces/cancel.json', 'traces/fault.json', 'traces/terminal.json', 'traces/abstract.json',
                                'traces/controls.json', 'traces/payload-vectors.json', 'traces/startup-vectors.json',
                                'logs/s45-p3.0.phase3_payload_vectors.log', 'logs/s45-p3.1.phase3_startup_vectors.log', 'logs/s45-p3.2.phase3_traces.log',
                                'logs/s45-original.0-.2.run_unchanged_s44.log (unchanged source44 helpers on the source45 kit)', 'preserved/s45-original/traces/',
                                'preserved/s44-final/manifest.json', 'tools/hc_source45.py',
                                'logs/s44-p3.0, s44-p3.2, s44-p3b.0 (source44 history; s44-p3.1 and s44-smoke.0 own errors preserved)',
                                'logs/s42v3-p3b.0.phase3_payload_vectors.log, logs/s42v3-p3b.1.phase3_traces.log (source42.v3 history)'],
                        HC.for_phase(3) + HC44.for_phase(3) + HC45.for_phase(3),
                        f"Runtime source45.v1 on the source45 kit (host conversion closedWorld from the published law, HC-60): typescript-semantic traces on typescript-protocol2-order.v1.json and rust-semantic traces on "
                        f"protocol3-transitions.v1.json. Every row of both tables is exercised, rows are pairwise disjoint, and only P3-09/P3-10 are table-only "
                        f"(derived modes). {law}. FactBatch payloads in traces {json.dumps(fb)}; standalone payload and startup vectors have 0 assertion failures.")
print(json.dumps({"phase3Unexecuted": cp["requirementIdsUnexecuted"], "executed": len(cp["requirementIdsExecuted"])}))
