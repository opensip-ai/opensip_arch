**Verdict: ACCEPT-RECONSTRUCTABLE.** The provider-trace payload obligation is now actually executed, with 0 assertion failures. Final kit custody passed again just before phase 11, and all child processes have finished. The review is in `output/blind-review.md` and `output/blind-review.json`.

## My v2 statement was wrong
The charter's provider-trace sentence is part of R-TRACE-*. My v2 traces negotiated `target-attribution-v2` but every `FactBatch` was a bare frame name with no payload. They also listed payload schema validation as "future host", while the review marked R-TRACE-* executed. So those traces only ever checked state transitions. I withdrew the "read but not exercised" statement (HC-53). The v2 bytes of every file I changed are kept in `preserved/s42-v2-final/`. No complete Run holds FactBatch frames, so nothing earlier counts as payload evidence.

## What was executed (`logs/s42v3-p3b.*`)
New code in `ref/factbatch.py`, built from the kit only, applies the payload law when a FactBatch arrives mid-analysis. It runs in 71 standalone vectors (`traces/payload-vectors.json`) and in 25 protocol traces.
- **Negotiated vs unnegotiated:**
  - V3 with the token and V2 without it are both admitted (V2 captures no occupancy).
  - V3 without the token refuses `PROVIDER_RETURN_UNNEGOTIATED_V3`; V2 with the token refuses `PROVIDER_RETURN_SCHEMA`.
  - If only Hello or only HelloAck carries the token, the exchange faults at HelloAck.
- **Exact bytes:** I wrote my own deterministic-CBOR encoder and decoder from the kit's encoding profile. Both kit vectors reproduce byte-for-byte, and every forbidden encoding has a refusing vector.
  - `PROVIDER_RETURN_PAYLOAD_CBOR` refuses: hex of canonical JSON instead of CBOR, wrong key order, a non-shortest length header, an indefinite-length map, a trailing byte, and valid CBOR of a different payload.
  - Uppercase hex of the correct bytes fails only the schema pattern.
- **Request/batch correlation:** the dispatch binding is derived from the Analyze request plus a Plan fragment.
  - A TypeScript Analyze that selects Plan stages 1 and 3 admits, and batches continue one candidate stream (second batch starts at candidate 3).
  - Refused: a `stageId` echoing either ordinal, `analysisOrdinal` or `batchIndex` mismatches, a restarted or skipped stream, and a missing or mis-derived dispatch.
- **Traces:** of 21 FactBatch payloads, 19 were validated (14 admitted, 5 refused). The other 2 arrive after the protocol has already faulted, so they are never validated. Each refusal's public route matches the expected fault projection.

## New helper corrections and advisory
- **HC-51:** my schema helper didn't know the kit's `candidateOrdinal` array-order token, so it refused every valid FactBatchV3 (40 of 40 measured). The fix lives in a new subclass, and only `fact-batch.schema.v3.json` uses that token, so no earlier result changes.
- **HC-52:** runtime rebinding to the v3 path and runtime labels.
- **A-s42v3-1 (advisory):** the kit publishes TypeScript major 2 only as deltas on the major-1 wire.
  - Without the token, it names the payload "historical FactBatchV2", but the only published TypeScript payload is FactBatchV1 (`facts`, `batchCommitment`).
  - There is no major-2 Hello schema.
  - The current native §9.1 text decides the payload, so I apply FactBatchV2, and a FactBatchV1-shaped payload refuses. TypeScript Hellos are checked against the shared HelloV3 fields with `protocolMajor` swapped.

My first run failed on two of my own construction errors, a list edit and sending major 2 to HelloV3. Both logs are kept (`logs/s42v3-p3.*`).

## Reused vs fresh
- **Fresh in v3:**
  - the payload vectors and payload-carrying traces;
  - phase 0 custody and checkpoints 0–3;
  - final custody (run twice);
  - phases 10 and 11.
- **Reused unchanged from v2:** the 27 exported positives and run IDs, closure, replay, negatives, the pre/post matrix, provenance, and phases 4–9. Nothing they execute changed.

The charter and requirements hashes differ from v2 only because the runtime path moved. The 123/8/3 requirement IDs are unchanged.

## Not claimed
- **Real workers:** no actual worker-process enforcement, and no OS, provider or compiler qualification.
- **Not built by these vectors:**
  - the post-terminal occupancy capture into TargetAttributionV2;
  - payload bodies of the other frames;
  - anchor admission for the constructed candidates.

Root admission of the exports remains unobserved.
