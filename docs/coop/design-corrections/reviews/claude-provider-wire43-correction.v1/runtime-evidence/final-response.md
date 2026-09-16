All of P1–P4 and the Rust counterpart are implemented in the work copy, and every focused reference control passes. Four adjacent handshake-to-Analyze problems (ADJ-2 to ADJ-5) turned out to need owner decisions, so I recorded them with exact selectors and alternatives rather than fixing them. Frozen43 was verified before and after, the last time after all writes, with 0 mismatches. The prior assessment runtime is byte-identical. Nothing was frozen, committed, repinned in a global ledger, or activated.

## What changed (13 files: 11 edited, 2 new)

**One decision to know first:** I did not edit `native-evidence.schemas.v2.json`. Its raw SHA-256 is a registered payload schema digest, so any byte change would re-register identities. Instead, a new closed document, `native/provider-handshake.schemas.v1.json`, holds the corrected records. A §0 row supersedes the old `HelloV3`, `HelloAckV3` and `ProtocolLimitsV3` definitions, following the existing "registered bytes kept" precedent in §10.

- **TypeScript major-2 handshake:**
  - **Hello:** `TypeScriptHelloV2` keeps every `HelloV1` member and adds the token array and `identityVersions`. It has no payload `protocolMajor`; the envelope major is 2.
  - **HelloAck:** `TypeScriptHelloAckV2` keeps all 14 `HelloAckV1` members, so every provider/runtime descriptor check survives. Its major becomes 2 and `capabilities` becomes an exact echo of Hello.
  - **Limits:** `TypeScriptProtocolLimitsV1` is exactly the ten numeric `delivery.v2` limits; `limitRule` is not a member.
- **Rust major-3 handshake:**
  - **Hello:** `HelloV3` keeps `hostBuildId`, `expectedProtocolContractSha256` and `expectedIdentity`.
    - The contract digest is the raw SHA-256 of `rust-provider-protocol.v2.json` (`6308a98c…`). It authenticates only that inherited base; I added no new digest input.
    - The identity values come from the Plan's retained `rust-v1` row.
  - **HelloAck:** `HelloAckV3` echoes the five identity fields, the token array and `identityVersions`.
  - **Limits:** `ProtocolLimitsV3` is the 24 inherited limits plus the 8 successor limits (32 in all).
- **Token-array order (both languages):** strictly unique, ascending UTF-8 order. TypeScript inherits this; for Rust it replaces the old unordered annotation.
- **FactBatch (P1–P4):**
  - **Not negotiated:** TypeScript keeps `delivery.v2` `FactBatchV1` with `batchCommitment`; Rust keeps `FactBatchV2`.
  - **Negotiated:** `FactBatchV3` is unchanged.
  - **Commitments:** `FactBatchV3` has no per-batch commitment. The TypeScript `factBatch` commitment domain applies to `FactBatchV1` only. Stage and stream commitments stay over the ordered candidate stream.
  - **Limit names:** `maxFactBatchFacts` (TS) and `maxFactBatchCandidates` (Rust), both 4096.
  - **CBOR projection:** stated explicitly in §9.6 and in `fact-batch.schema.v3.json`.
- **Conflicting notes corrected:** §0/§9 of `native-evidence.md`, the fact-batch and occupancy schemas, the attribution return schema, the execution-inputs model and contract, and the native README.
  - The occupancy token gate behaves as before; its docstring now says it only gates capture, and its label is renamed `unnegotiated-historical-fact-batch`.
  - Root's earlier generic-V2 reading is recorded as a lawful alternate interpretation, not a helper error.

## Controls (all receipts in `receipts/`)

| Control | Result |
|---|---|
| Native checker, frozen baseline | 388/388 pass |
| Native checker, corrected | 428/428 pass (40 new cases: 9 positive, 31 negative); new drift checks report no faults |
| Attribution checker, before / after | 47/47 both |
| Execution-inputs checker, before / after | exit 0, no mismatches, both |
| Before/after discriminator | Frozen `HelloV3` accepts the unauthenticated 4-field Hello and refuses the full one; frozen `ProtocolLimitsV3` refuses the 32-member map; the frozen token gate treats valid, wrong-shape, bad-commitment and junk batches identically. Corrected owners reverse or discriminate each. |
| Refusal audit | Every negative case is refused for its stated reason |
| Mutation controls | First run: 2 of 6 mutations were not applied because I built their search strings wrong (kept as receipt 32). Corrected run (receipt 34): 6/6 applied, every one made the checker fail. |

The new drift checks derive their expected values from the inherited artifacts and the §9.3/§9.4 prose, not from the new schema itself. The case expectations were computed without the model, using `hashlib` and `cbor2`. The checker needs pins that match, so it ran in scratch copies with a pin refresh done only there.

## Still open (not fixed)

- **ADJ-2 (MUST):** in both languages, `Unavailable(native-context-mismatch)` must be sent before Analyze, but the inherited `UnavailableV1`/`UnavailableV2` payloads need Analyze-derived stage IDs and coverage. TypeScript ordering also forbids `Unavailable` before Analyze.
- **ADJ-3 (MUST):** no field-level successor is published for OpenUniverse/UniverseAccepted in either language. §9.1 step 3 applies Rust-only `RepositoryResolutionV3` to both.
- **ADJ-4 (SHOULD):** Coverage frame name. For Rust, §9.2 and the transition table already make it `CoverageV3` (only a §0 row is missing); for TypeScript it is undetermined.
- **ADJ-5 (SHOULD):** `CancelledV1.observedPhase` has no value for a Cancel sent while waiting for `NativeContextVerified`.
- **Resolved adjacent item:** the TypeScript success path now places `NativeContextVerified` between `SnapshotAccepted` and Analyze.

## What you need to do at integration

- **Repin:** 10 ledgers still name old digests (listed in `delta-final/repin-index.json`), and the two new native files must be added to the native pin ledger.
- **Regenerate:** the work copy's `native-evidence-report.v2.json` was left stale on purpose.
- **Expect one output change:** the execution-inputs checker's `neededRootInputs` text now reflects the corrected note.

None of this is worker, process or compiler qualification: frame bytes and real CBOR frame decoding were not exercised.

Everything is in `/private/tmp/opensip-design-corrections/claude-provider-wire43-correction.v1/`:
- `review.md`
- `review.json`
- `hash-index.json`
- `delta-final/files.json`
- `delta-final/unified.patch`
- `delta-final/repin-index.json`
- `work/candidate`
