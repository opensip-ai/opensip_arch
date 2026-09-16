import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/tools')
import hc_source42 as HC
import status as S

OUT = S.OUT
p1 = json.load(open(OUT + 'vectors/phase1-canonical.json'))
p2 = json.load(open(OUT + 'vectors/capability-manifests.json'))
p3 = json.load(open(OUT + 'traces/controls.json'))
# source42.v3 (HC-53): the provider-trace requirements also require the charter-incorporated FactBatch payload law, executed in the
# payload-carrying exchanges (traces/*.json payloadResults) and in the standalone vectors (traces/payload-vectors.json).
p3p = json.load(open(OUT + 'traces/payload-vectors.json'))
assert p1["assertionFailures"] == [] and p2["assertionFailures"] == [] and p3["assertionFailures"] == [] and p3p["assertionFailures"] == []
trace_files = {k: json.load(open(OUT + f'traces/{k}.json'))["traces"] for k in ("complete", "unavailable", "cancel", "fault", "terminal")}
all_traces = [t for ts in trace_files.values() for t in ts]
assert all(t["matchesExpected"] and t["payloadResultsMatch"] and "executedVsHost" in t for t in all_traces)
payloads = [p for t in all_traces for p in t["payloadResults"]]
fb = p3["factBatchPayloads"]
assert fb["validated"] + fb["notValidatedBeforePayload"] == fb["total"] == len(payloads) and fb["negotiatedV3Admitted"] > 0 and fb["unnegotiatedV2Admitted"] > 0
groups = p3p["groups"]
st = S.load_status()
for rid in ['R-H-HELPER', 'R-CVE1-EIGHT-TYPES', 'R-LEXICAL-ADMISSION', 'R-SEMANTIC-VS-OPERATIONAL', 'R-RAW-VS-PARSED', 'R-ACYCLIC-JOINS']:
    S.set_status(st, rid, 'executed', artifact='vectors/phase1-canonical.json')
S.set_status(st, 'R-CVE1-EIGHT-TYPES', 'executed', artifact='vectors/cve1-eight-types.json')
S.set_status(st, 'R-LEXICAL-ADMISSION', 'executed', first_refusal='raw-input lexical boundary (see firstRefusal per vector)')
S.save_status(st)
S.write_checkpoint(1, st, ['ref/canonical.py', 'ref/schemas.py', 'ref/cve1.py', 'vectors/phase1_canonical.py', 'vectors/phase1-canonical.json', 'vectors/cve1-eight-types.json'], [],
                   "C/H, CVE1, raw lexical admission, raw-vs-parsed, semantic-vs-operational and acyclic-join vectors executed with assertions (exit 0). Chain vector is explanatory (no replay).")
for rid in ['R-CAP-ADMISSION', 'R-CAP-NAMED-GATES']:
    S.set_status(st, rid, 'executed', artifact='vectors/capability-manifests.json', first_refusal='per negative: ADM-TYPE|ADM-CLOSED|ADM-DOMAIN|ADM-ORDER|CVE1-ENCODE|LEX_*')
S.save_status(st)
S.write_checkpoint(2, st, ['vectors/phase2_capmanifest.py', 'vectors/capability-manifests.json'], [],
                   "Four gates in registry gateOrder before CVE1 encoding; masking recorded; successor RELATION-DOMAIN-V2/LADDER mirror drift-checked.")
law = ("FactBatch payload law applied (negotiated FactBatchV3/FactBatchV2 selection, deterministic-CBOR payload bytes, DispatchBindingV1 request/batch "
       "correlation, companion association; source42.v3 HC-53)")
refused = {t["name"]: [p["firstRefusal"] for p in t["payloadResults"] if p.get("result") == "REFUSE"] for t in all_traces}
trace_notes = {
    'R-TRACE-COMPLETE': f"traces/complete.json: {len(trace_files['complete'])} complete traces, including a TypeScript Analyze selecting Plan stages 1 and 3 with a "
                        f"two-batch candidate stream and a Rust unnegotiated FactBatchV2 exchange; {law}.",
    'R-TRACE-UNAVAILABLE': f"traces/unavailable.json: {len(trace_files['unavailable'])} traces; payloads admitted before the terminal; {law}.",
    'R-TRACE-CANCEL': f"traces/cancel.json: {len(trace_files['cancel'])} traces; a FactBatch in WAIT_CANCELLED faults before payload validation.",
    'R-TRACE-FAULT': f"traces/fault.json: {len(trace_files['fault'])} traces, including payload-law faults "
                     f"{sorted(k for t in trace_files['fault'] for k in refused[t['name']])} routed to the s10 fault projection, and a HelloAck omitting the attribution token.",
    'R-TRACE-IDENTITY-BEFORE-SOURCE': "identityNegotiated precedes sourceBytesSent on every trace (stateTimeline); the optional target-attribution-v2 token is not an identity token but its echo is exact.",
    'R-TRACE-TERMINAL': f"traces/terminal.json: {len(trace_files['terminal'])} terminal/post-terminal traces; a post-terminal FactBatch faults before payload validation.",
    'R-TRACE-EXECUTED-VS-HOST': (f"executedVsHost on every trace: transitions, s9.1 echo, FactBatch payload schema/bytes/correlation and s10 projection executed; "
                                 f"futureHostAssumptions are process/OS/framing/actual worker emission; notConstructedHere lists payload bodies of other frames and post-terminal "
                                 f"bind_worker_occupancy. Standalone traces/payload-vectors.json: {len(p3p['vectors'])} vectors {json.dumps(groups)}, "
                                 f"{len(p3p['decoderVectors'])} decoder and {len(p3p['encoderVectors'])} encoder vectors; actual worker-process enforcement not claimed.")}
for rid, notes in trace_notes.items():
    S.set_status(st, rid, 'executed', artifact='traces/', notes=notes)
S.save_status(st)
cp = S.write_checkpoint(3, st, ['ref/protocol3.py', 'ref/factbatch.py', 'vectors/payload_fixtures.py', 'vectors/phase3_traces.py', 'vectors/phase3_payload_vectors.py',
                                'traces/complete.json', 'traces/unavailable.json', 'traces/cancel.json', 'traces/fault.json', 'traces/terminal.json', 'traces/controls.json',
                                'traces/payload-vectors.json', 'logs/s42v3-p3b.0.phase3_payload_vectors.log', 'logs/s42v3-p3b.1.phase3_traces.log',
                                'logs/s42v3-p3.0.phase3_payload_vectors.log (own construction error, preserved)', 'logs/s42v3-p3.1.phase3_traces.log (own construction error, preserved)',
                                'preserved/s42-v2-final/vectors/phase3_traces.py'], HC.for_phase(3),
                        f"All 34 published rows exercised; rows pairwise disjoint; executed-vs-future-host recorded per trace. HelloAck echo mismatch modeled as s9.1 payload "
                        f"rule (not a table row). Runtime source42.v3: {law}; FactBatch payloads in traces {json.dumps(fb)}; standalone vectors 0 assertion failures.")
print(json.dumps({"phase3Unexecuted": cp["requirementIdsUnexecuted"], "executed": len(cp["requirementIdsExecuted"])}))
