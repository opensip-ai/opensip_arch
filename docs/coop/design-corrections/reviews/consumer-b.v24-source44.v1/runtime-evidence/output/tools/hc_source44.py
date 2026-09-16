"""source44 (runtime consumer-b.v24-source44.v1) corrections to this origin's own helpers. They continue HC-1..HC-55: the source42 records remain in
tools/hc_source42.py and the source43 records in tools/hc_source43.py, and both apply unchanged.

Each entry names:
  - the original failure, with where its bytes or results are retained;
  - the source44 kit selector that answers it;
  - the correction and its re-execution.
The source43.v1 final bytes of every changed file are preserved at preserved/s43-final/ (manifest.json).
"""
HC = {
    "HC-56": ("Runtime adaptation for source44.v1, no law change. output/rebind_s44.py rebound the root-copied executable code from the source43.v1 root "
              "(output/rebind-s44-manifest.json: 104 files, 123 occurrences). It exited 1 only on runtime label text in tools/finalize_review.py, "
              "tools/hc_source43.py (a source43 record, left as history) and vectors/phase0_custody.py. output/preserve_s43_final.py then did two things: it "
              "copied the source43.v1 final bytes of the files source44 may change to preserved/s43-final/, and it wrote preserved/s43-final/results-manifest.json, "
              "the sha256 of all 473 copied runs/selfcheck/negatives/traces/vectors/envelopes files (104 stores), before any source44 execution. "
              "tools/run_preserved_s43.py runs the preserved source43 phase-3 scripts, with their source43 helpers, against the source44 kit and redirects their "
              "writes to preserved/s44-original/. Custody expectations in vectors/phase0_custody.py and tools/final_custody.py now assert the supplied source44 "
              "hashes (manifest a3a5fba8..., parent e873c8db...)."),
    "HC-57": ("ref/factbatch.py token-absent historical FactBatch payload. The source43 helper (preserved/s43-final/ref/factbatch.py) admitted "
              "rust-provider-protocol.v2 FactBatchV2 for both languages (my reading A-s42v3-1). Measured with the unchanged helper and vectors on the "
              "source44 kit (logs/s44-original.0.run_preserved_s43.log, outputs preserved/s44-original/traces/payload-vectors.json): all 71 vectors still "
              "matched their source43 expectations, so the helper's own vectors did not discriminate. SEL-ts-unnegotiated-v2 admitted a typescript-semantic "
              "FactBatchV2, and SEL-ts-unnegotiated-delivery-v2-FactBatchV1-shape refused the lawful FactBatchV1 member set. The run exited 1 only on the HC-51 "
              "candidateOrdinal census, because provider-handshake.schemas.v1.json adds two sites. Selectors: native-evidence.md s9.1 and s9.4; "
              "native/fact-batch.schema.v3.json#/x-opensip-negotiation/whenAbsent; native/provider-handshake.schemas.v1.json#/x-opensip-wire-law/factBatch,"
              "commitments,candidateCborProjection and #/$defs/TypeScriptFactBatchV1Vector,RustFactBatchV2Vector; delivery.v2.json typescriptSemanticSubstrate."
              "providerProtocol.wireSchema.commitments and canonicalCbor; occupancy-companion.schema.v1.json#/x-opensip-wire/historicalFactBatchV1,historicalFactBatchV2. "
              "Correction: buffer_fact_batch_occupancy takes the negotiating language. Token-absent typescript-semantic payloads admit as FactBatchV1 with "
              "batchCommitment recomputed over the wire FactCandidateV1 projection (new ref/wirecbor.py, which has byte strings, negatives and a dual map-order "
              "check); rust-semantic payloads admit as FactBatchV2. Keys are cb24.FACT_BATCH_V1_* / cb24.FACT_BATCH_V2_*. The census expects the two new sites. "
              "A-s42v3-1 is withdrawn. Re-executed: logs/s44-p3.0.phase3_payload_vectors.log (78 vectors, 0 failures)."),
    "HC-58": ("Provider traces under the source44 wire and startup law. The source43 traces (preserved/s43-final/vectors/phase3_traces.py with "
              "preserved/s43-final/ref/protocol3.py) ran typescript-semantic exchanges on protocol3-transitions.v1.json. They admitted TypeScript "
              "Hello/HelloAck on HelloV3 with protocolMajor substituted, carried Rust dependency/prepared modes as frame booleans, and carried OpenUniverse, "
              "UniverseAccepted, NativeContextVerified, Unavailable, CoverageV3, BudgetExhausted and Cancelled as frame names only. On the source44 kit they "
              "exited 0 with no failure (logs/s44-original.1.run_preserved_s43.log, outputs preserved/s44-original/traces/), so they did not detect four things: "
              "(1) a TypeScript Unavailable after stage output reaches DONE/unavailable via P3-25, where typescript-protocol2-order T2-14 requires outputSeen=false "
              "and the event faults T2-23; (2) a TypeScript ProviderFault reaches DONE via P3-28, while the TypeScript table has no such row; (3) Rust traces "
              "select P3-09/P3-10, which no admitted OpenUniverseV3 can reach; (4) no startup, coverage, terminal or cancellation payload was admitted. "
              "Selectors: native/typescript-protocol2-order.v1.json; native/protocol3-transitions.v1.json#/stateUpdates,derivedObservations,rowPayloads; "
              "native/provider-handshake.schemas.v1.json; native/provider-startup.schemas.v1.json; native-evidence.md s9.1-s9.4 and s9.7 lines 3151-3294. "
              "Correction: new ref/protocol_ts2.py (reads the TypeScript table at runtime), ref/provider_wire.py (handshake, startup, unavailable, coverage, "
              "budget and cancelled admission; pre-Analyze host conversion) and ref/provider_exchange.py (per-frame payload admission before either table; "
              "worker refusals route PROVIDER.PROTOCOL_VIOLATION, host-authored refusals a host invariant). ref/protocol3.py now derives modes from the admitted "
              "OpenUniverseV3 and reads handshake members from payloads. vectors/payload_fixtures.py joins payloads to my retained ts-pass/rust-mixed Run values. "
              "New vectors/phase3_startup_vectors.py; vectors/phase3_traces.py rewritten, with P3-09/P3-10 only as labelled abstract table tests. "
              "Own errors in this runtime, both preserved: (1) logs/s44-smoke.0.smoke_s44.log, a fixture label-uniqueness assertion over every store label; "
              "(2) logs/s44-p3.1.phase3_startup_vectors.log, a control that presumed native/source-pins.v2.json is a subject member. Re-executed: "
              "logs/s44-p3.2.phase3_traces.log (43 wire traces and 5 abstract tests, 0 failures) and logs/s44-p3b.0.phase3_startup_vectors.log "
              "(116 vectors, 0 failures)."),
}
PHASE = {0: ["HC-56"], 3: ["HC-57", "HC-58"], 9: ["HC-56"]}
CARRIED = ("HC-1..HC-55 (consumer-b.v24, source39.v1-v3, source41.v1, source42.v1-v3, source43.v1) remain in the helper code as prior corrections. The source42 "
           "and source43 records are tools/hc_source42.py and tools/hc_source43.py, and earlier records are preserved inside preserved/. Source44 execution "
           "re-exercises them without re-making them.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
