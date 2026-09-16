**Answer: only partly.** For typescript-semantic major 2, the payload when `target-attribution-v2` is negotiated can be reconstructed from the current owners. The handshake cannot, and neither can the default FactBatch payload when the token is absent. There are two MUST findings, two SHOULD and two advisory. This is my author assessment only: nothing in frozen43 or LIVE was edited, nothing was committed, and the proposed corrections are not implemented.

**Custody.** All 12913 manifest members matched and the manifest SHA `db43ee76…` checked out. The pinned `delivery.v2.json` and `rust-provider-protocol.v2.json` match their source pins. Every file I cite was re-hashed after the probe run and is unchanged. The run wrote no `__pycache__` into frozen43.

## Findings

**Precedence baseline.** In §0 of `native-evidence.md` (lines 112-127), the only TS wire selector named is `CoverageResultV1.completenessRule`. The TS `major`, the envelope `protocolMajor`, `HelloV1`, `HelloAckV1`, `FactBatchV1` and the `factBatch` commitment domain are all unnamed there. So every TS change has to come from the prose in §9.

- **M1 (MUST): the TS major-2 Hello/HelloAck payloads cannot be reconstructed.**
  - **What is fixed:** the token set, the `identityVersions` values, the exact-equality rule, the fault on mismatch, and the major value 2.
  - **What is not fixed:**
    - **Fields:** which fields Hello and HelloAck carry.
    - **Limits:** which limits go in Hello (the 10 TS delivery.v2 limits or the 8 in `ProtocolLimitsV3`).
    - **Order:** the order of the capabilities array.
    - **Placement:** where `protocolMajor` sits.
  - **Why not:** `HelloV3`/`HelloAckV3` are closed and fixed to major 3, so the probe refuses major 2. §9.4 is a list of capabilities, not a field-level change. Keeping `HelloAckV1` unchanged can't express the identity tokens at all.
  - **Two incompatible readings:**
    - **A:** use the V3 shape with major 2.
    - **B:** keep the `HelloV1` fields and add the tokens and `identityVersions`.

    A closed decoder following one reading refuses the other's Hello and HelloAck.
  - **Consequence:** a host and a TS worker can both follow frozen43 and still fault with `PROVIDER.PROTOCOL_VIOLATION` at HelloAck. That affects every TS/JS semantic cell. Reading A also loses the descriptor fields that `producerVersion` depends on.

- **M2 (MUST): the FactBatch payload when the token is absent has two incompatible readings.**
  - **Reading U-V1:** the retained TS `FactBatchV1` `{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}` stays. Nothing supersedes it.
  - **Reading U-V2:** the payload is the "historical FactBatchV2" named in §9.1, §9.6, the `whenAbsent` rule of `fact-batch.schema.v3.json` and `occupancy-companion.schema.v1.json`. The only definition of that name is Rust's `{…, candidates}`; TypeScript never had a V2.
  - **Consequence:** a TS batch shaped like V1 is admitted under one reading and is a protocol violation under the other. This is the default path, since the token is optional.
  - **Reference model:** `_token_gate` treats a V1-shaped batch, a V2-shaped batch and junk the same way, so it can't settle the question.

- **S1 (SHOULD):** the TS major value 2 overrides the retained "exactly 1" selectors without §0 rows. There is only one possible value, so this is an incomplete selector table rather than a competing wire reading.

- **Negotiated FactBatchV3 (no defect):** its field set is fixed by an explicit successor whose scope is the token and which names TS itself. The closed payload is:
  - `schemaVersion` 3 and `analysisOrdinal` 0;
  - `stageId` as text and `batchIndex`;
  - 1..4096 `FactCandidateV1`, carrying CBOR bytes on the wire;
  - 0..4096 `occupancyCompanions`;
  - no `facts` and no `batchCommitment`.

  It can only be reached once M1 is fixed.

- **S2 (SHOULD):** V3 drops the TS `batchCommitment`. What happens to that commitment domain is never stated, although the stage and stream commitments still work.
- **A1 (advisory):** the text says `maxFactBatchCandidates`, which is Rust's limit name. TS calls it `maxFactBatchFacts`; both are 4096.
- **A2 (advisory):** how the V3 JSON-vector form maps to the wire is stated only in field descriptions.

## Proposed corrections (not implemented)

- **P1 (fixes M2):** make the absent-token payload language-specific wherever it is stated. TS keeps delivery.v2 `FactBatchV1` and Rust keeps `FactBatchV2`; a language's historical payload sent with the token is a protocol violation. Add a §0 row retaining `FactBatchV1` when the token is absent.
- **P2 (fixes M1 and S1):** add §0 rows superseding the TS `major`, envelope `protocolMajor`, `HelloV1` and `HelloAckV1`. Add an exact TS major-2 handshake to §9.4:
  - keep the `HelloV1` and `HelloAckV1` fields, set major to 2, and keep the TS limits unchanged;
  - add `expectedCapabilities` and `identityVersions`, and make HelloAck echo both exactly;
  - state one array-order rule.
- **P3 / P4 (fix S2, A1 and A2):** one sentence each on the commitment, the limit name and the wire mapping.

Separately, the Rust `HelloV3` and `ProtocolLimitsV3` schemas contradict §9.3's "all 24 v2 limits retained". I noted this but did not classify it; it needs its own question. I did not assess TS `CoverageV3`, `NativeContextVerified` ordering or `Unavailable` reasons. The probes are reference evidence only, not compiler or worker qualification.

Files are in `/private/tmp/opensip-design-corrections/claude-ts-protocol43-publication-assessment.v1/`:
- `review.md`
- `review.json`
- `hash-index.json`
- `probes/ts_protocol_probe.py`
- `probes/probe-output.json`
- `receipts/frozen43-verify.json`
