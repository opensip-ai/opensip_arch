# Addendum: kernel41 reader-envelope finding (reachability)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded follow-up on advisory finding `reader-refused-precondition-is-not-join-refuse-document`. **Does not rewrite** `advisory.md` / `advisory.json`. **Not** source approval, **not** implementation41, **not** inventory27, **not** reference42, **not** full M2.

Original advisory bytes (unchanged after this addendum):

| File | Bytes | sha256 |
| --- | ---: | --- |
| `advisory.md` | 12987 | `d052f653cab59aa2ba7a252b60eb81ef406ac1aa5efd9634722fbcf7f238dbda` |
| `advisory.json` | 9569 | `8f83508010cd2773bea33c0fe9308dd1d0be6426ff10b6c823fb1a7792514731` |

## Verdict

**The original finding’s public-API reachability claim is not independently reproduced on closed owner schemas.** Same-path/different-bytes snapshot and `bindResult`-bearing universe frames fail typed owner/schema admission **before** the reader `Err(Refused("ENUMERATION_ADMISSION_PRECONDITION"))` guards. Those guards are defensive. Root’s dual envelope is: typed owner/schema/limits `Err` before join; only admitted reconstruct preconditions yield an E39 ADMIT/REFUSE document. No retained counterexample that reaches the two `Refused` branches was found.

This does **not** reopen map-injection `complete_join` vs E39 document equality (kernel-check maps skip owner admission). That surface remains test-only and is not public retained authority.

## Independent reproduction

Root packets `/tmp/opensip-implementation/m2-enumeration-join-trial-41/reader-boundary-check/`:

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| `requests.ndjson` (2 packets) | 1563132 | `1939ffa43c5feaa5d95053de150bb284e744ebc12eafad7dff2d3ee27b9db317` |
| `actual.ndjson` | 151 | `589cbb9c020d759de1e42e4a85972e1a7fc6d8c627f3e6b08c60f7dde851f061` |
| `result.json` | 338 | `6f911d5d081ebeea44bd9ce906a2f64d1c4afcbec6315f18404ca2e628e7f87b` |
| generator `check_enumeration_reader_boundary41.py` | 3168 | `635ea87185e5cc24ba5181fd508377b3b255b8636edb17981b88e4253d37bbe5` |

Replay of the same `requests.ndjson` through the **copied-kernel** isolated harness (`review/probe/harness`, overlay pin `enumeration_join.rs` 51742 / `3f24610941…`):

| Packet | Copied `inspect_enumeration_join` | Equals root `actual.ndjson` |
| --- | --- | --- |
| `duplicate-snapshot-path-owner-refusal` | `{"result":"error","detail":"Record(Input(Candidate(Schema(Mismatch))))"}` | byte-equal |
| `universe-bindresult-owner-refusal` | `{"result":"error","detail":"Plan(Retention(Owner(Frame(Schema(Mismatch)))))"}` | byte-equal |

Copied replay 151 / `589cbb9c020d759de1e42e4a85972e1a7fc6d8c627f3e6b08c60f7dde851f061`. Neither packet is `Err(Refused("ENUMERATION_ADMISSION_PRECONDITION"))`. `result.json` `readerRefusedBranchesReached: false` matches this run.

Draft host fixture now has **34** cases, including these two as `errorClass: invalid` with the same `errorDetail` strings. Ten inventory-shaped packets still return join **REFUSE documents** (admitted reconstruct, then join law). That split is the dual envelope.

## Why the original uniqueItems-only claim does not hold

Copied `read_inputs` still contains both guards (duplicate `sourceInventory` path → `Err(Refused(PRECONDITION))`; universe `bindResult` key → same). Public `RetainedInputs.object` never presents those descriptors to the guards:

1. **Snapshot.** `object(id, Snapshot, …)` → `IdentityCandidate::from_json` → `admit_json` then `ordered()`. `#/$defs/source-inventory` has **both** `uniqueItems: true` (whole-row canonical bytes) **and** `x-opensip-order: "path"`. Schema evaluate (`identity/src/schema.rs` 539–556) runs uniqueItems **then** `ArrayOrder::verify`. Duplicate **path** with different `bytes`/`sha256` passes uniqueItems and fails path order (`prior >= key` → `NonIncreasing`) → `admit_json` `Ok(None)` → `AdmissionError::Mismatch` → `Record(Input(Candidate(Schema(Mismatch))))`. `descriptors.rs` `ordered` also special-cases `sourceInventory` as path order; it is not reached when schema already mismatches.

2. **Universe `bindResult`.** Generator keeps a valid-frame preimage, inserts `bindResult`, and rehashes. `inspect_plan_native` → retention → `frame_candidate` admits `#/$defs/TypeScriptUniverseV2ResolvedInputs` (`additionalProperties: false`, no `bindResult` property). Rust and syntax universe resolved-input defs are the same: `additionalProperties: false`, no `bindResult`. Extra key → frame `Schema(Mismatch)` wrapped `Plan(Retention(Owner(Frame(Schema(Mismatch)))))` **before** `read_inputs` `contains_key("bindResult")`.

No retained packet was constructed that is owner-admitted **and** still hits those two `Refused` lines. A map `complete_join` can still fault `bindResult` as a REFUSE **document** because it skips `object`/`frame_candidate`. That is not the public retained reader.

## Disposition of original finding 1

| Original claim | This addendum |
| --- | --- |
| Public reader returns `Err(Refused(PRECONDITION))` for duplicate snapshot path and universe `bindResult` | **Not reproduced** on closed owner schemas; earlier typed `Err` |
| `uniqueItems` is whole-row so same-path different-sha reaches the reader path check | Incomplete: `x-opensip-order: path` is in the same schema and fires inside `admit_json` |
| Action (a): route those reconstruct refusals through `refuse_result` | **Not required** for these two retained shapes |
| Action (b): freeze dual envelope; do not claim E39 document equality for reconstruct `Err` | **Matches** root’s explicit choice |

Original `requiredFindings[0]` reachability is **corrected here**. The original files are left byte-identical so the record of the first review stays. This addendum is the later independent check.

## requiredFindings

None for this addendum. No retained counterexample to the defensive-guard claim was produced.

## Limits

Not source/runtime/inventory/reference acceptance. Not a claim that every `EnumerationJoinError::Refused` is unreachable (unregistered parameter, duplicate analysis key, missing required enumeration-plan parameter remain reconstruct `Err` on other paths). Not a claim that map-injection 51-case equality is retained-reader proof. Root continues implementation. No live/frozen/history edits.
