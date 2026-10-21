# D2b implementation plan r1: the provider codecs, `crates/components/src/provider_protocol.rs` (M3-D items 10 and 11)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product main `56d0eb5` (inventory v214; 173 contract successors);
- architecture as the subject manifest names.

**What precedes it.** D2b's row in M3-D r5's units table is "`components/provider_protocol.rs`: items 10-11, the CBOR reader, P3T and T2O as data, the handshake checks", depending on P0 (met), size L. Its order is D1a → D2a ∥ D2b → D3a.
- D2a's plan is accepted, and its codec is built for its lane.
- D2b does not depend on D2a. They are separate codecs, with no shared frame type (item 11, rule 1).

**Authority:**
- **The law:** M3-D r5 items 10 and 11, with D2b-T1 to T5 and D5-C1's no-translation classes.
- **NE §9** (`docs/v2/contracts/product-v1/native-evidence.md`:2781-3316).
- **DLV** (`docs/coop/artifacts/delivery.v2.json`) and **RPP** (`docs/coop/artifacts/rust-provider-protocol.v2.json`).
- **P3T** (`docs/coop/design-corrections/native/protocol3-transitions.v1.json`), with its guard overlay `docs/implementation/m1/source-selection-v2/owners/native/p3-guard-successor.v1.json`, and **T2O** (`…/native/typescript-protocol2-order.v1.json`).
- **The product schemas:** `schemas/sources/handshake-v1.schema.json` (RCA-1's Rust3 identity, Grok `grok-rust3-identity-materialization-r1`), `startup-v1.schema.json` and `fact-batch-v3.schema.json`.
- **The wire carriers:** `schemas/wire/native-carriers-v1.json`, with their generated types in `crates/contracts/src/generated/protocol.rs`.
- **The bound successors FA-2 and RUST3-LIM** (`docs/implementation/m3/native-successors-fa/`), whose materialization maps and cross-law items X-FA2-D and X-RL-D give D2b their schema materialization.

## 0. What D2b delivers, and what it does not

**Delivers** `crates/components/src/provider_protocol.rs` and its data, library only, with no caller until D3a and D4:
- **the shared wire mechanics:** the 40-byte prefix (`uint64` BE length, 32 raw SHA-256 bytes), the length checked against 67,108,864 before any allocation, exact reads, digest verification, checked arithmetic, and per-direction sequences from 0;
- **a first-party strict deterministic-CBOR reader and encoder** for the two closed profiles, `ts2-cbor` (negative `int64` allowed) and `rust3-cbor` (no negative integers). Canonicality is proved by re-encoding and byte comparison. Text, map keys included, must be NFC;
- **two codecs, one per protocol,** with no common semantic type:
  - TS2 (`typescript-semantic`, major 2) and Rust3 (`rust-semantic`, major 3), selected at session construction from the admitted selection;
  - each payload decoded by hand-written, schema-checked code into the generated carriers (serde never reads wire bytes);
  - each payload checked against its closed product schema;
- **the transition tables as data:** P3T's 34 rows with the guard overlay, and T2O's 23 rows, vendored hash-pinned copies interpreted by one table engine with the pre-match law, first match on phase, frame and guard, the stage-dependent next, and the total fallback;
- **the handshake checks:**
  - exact identity echoes, the identity tokens and `identityNegotiated`;
  - the limits handshakes, TS2's ten-member map and Rust3's 32-member map, with deterministic-CBOR byte equality;
  - reject before disclosure;
- **the commitments,** `C(d, v) = "sha256:" + hex(SHA-256(UTF8(d) ‖ 0x00 ‖ dCBOR(v)))` and the manifest digests, recomputed from the received bytes;
- **the typed events** D2b emits to the host's consumers. It admits no fact and mints no Coverage (item 10).

**Not delivered:**
- the supervisor and its process events (D3a; D2b defines the event input it consumes);
- the session factory and manifest admission (D4);
- fact admission (H);
- the Plan side's pre-spawn sizing (C4);
- any Linux-specific code (none is needed).

## 1. The split (LD-D2B-1): five sub-units, each its own review and lane

The unit is large, so it lands in five sub-units, all under this one plan:

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D2b-1** | The CBOR reader and encoder (both profiles), the framing, the digest, sequences, and the `C(d, v)` and manifest-digest helpers | D2b-T2, D2b-T3; the reference decoder's probes | — |
| **D2b-2** | The table engine over the vendored P3T, its overlay and T2O | D2b-T1 | — |
| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake; then **a reviewed blind refresh** | the materialization's own checks; the refreshed receipt | — |
| **D2b-3** | The TS2 codec | D2b-T4, D2b-T5 (TS2) | D2b-1, D2b-2, D2b-0 |
| **D2b-4** | The Rust3 codec | D2b-T4, D2b-T5 (Rust3) | D2b-1, D2b-2, D2b-0 |

**Order:** D2b-1, then D2b-2, then D2b-0 with its blind refresh, then D2b-3 and D2b-4.
- **D2b-0 comes after the two mechanics units.** Its regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main.
- **So D2b-0 is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence.

## 2. Lead decisions

- **LD-D2B-2. The CBOR depth bound.** No source sets one, and the Python reference has none.
  - **The bound:** the deepest path any closed payload schema admits, plus the envelope's levels. It is computed from the pinned product schemas when the tables load, fixed as a constant, and checked by a test against the schemas.
  - **Over the bound:** refused before any further allocation, as `PROVIDER.PROTOCOL_VIOLATION`.
  - **No recursion:** the reader is iterative, like D2a's.
- **LD-D2B-3. Received bytes are primary.** Each commitment is computed over the received payload's sub-slices: canonicality makes a received array element equal to its dCBOR. The spool entry is built from the decoded value and asserted equal to those received bytes, never sliced from them (RPP:143).
  - **Stream commitments,** whose length prefix is known only at the end, are computed at Coverage or Complete over the retained candidate bytes.
- **LD-D2B-4. The tables are data.** P3T, its guard overlay and T2O are vendored as byte copies under `crates/components/data/`, pinned to their architecture SHA-256, and embedded with `include_bytes!`. There is no code copy of any row (item 10). Every row, both catch-alls and the total fallback are replayed (D2b-T1), with the overlay's five vectors and the `protocol3_run` and T2O cases of `native-cases.v2.json`.
- **LD-D2B-5. TS2's Unavailable payload is selected by phase,** as the carriers do (`native-carriers-v1.json`:5813). A payload that does not match its phase refuses at the precheck, recorded as the precheck's trace rather than T2-23's. The outcome is the same, and the trace id is documented.
- **LD-D2B-6. Process events are D3's.** D2b defines the input `ProcessEvent {ZeroExit, Eof, Fault(kind)}`, with `kind` one of deadline, nonzero-exit, signal-death or stdout-byte. The table engine consumes it through the pre-match law. D3a feeds it under item 13's EOF and exit join.
- **LD-D2B-7. Cancel follows each table.**
  - TS2 permits Cancel from START (T2-18) and `host-shutdown`.
  - Rust3 permits neither: no Cancel in START, and `user-interrupt` only.
  - The reason revocation uses is D3's choice, within what the selected protocol permits.
- **LD-D2B-8. No invented bound.** TS2 has no aggregate response bound in its law (gap 6), so D2b sets none and records the gap as a cross-law item for the protocol owner. Rust3's four aggregates are enforced as RPP:143-146 states them.
- **LD-D2B-9. The send schedule.** D2b owns the host's send-side wire accounting (REQUEST-WIRE-ACCOUNTING and HOST-SEND-SCHEDULE): it never writes a frame the schedule forbids. The pre-spawn refusal of an oversized inline Analyze (RUST3-LIM F-1) is the Plan side's (C4). D2b provides the size function it calls.
- **LD-D2B-10. The Rust3 anchor order** is `cve1-bytes-strict` (carriers ANCHOR-WIRE-SPAN), using `opensip_identity::encode_cve1`. That is a byte ordering, not a CBOR reader, so it is consistent with the law's rejection of `capability_codec` as a reader.
- **LD-D2B-11. NFC.** `opensip-identity` gains one exported predicate, `is_nfc(&str)`, over its existing pinned `unicode-normalization` (=0.1.24). The components crate takes only `opensip-identity` and `opensip-contracts`, among its permitted owners. The Unicode version is pinned in a test against the Python reference's `unicodedata` over the vendored vectors' texts, and any disagreement is reported, never papered over.
- **LD-D2B-12. The check order for one frame:**
  1. the 8 length bytes;
  2. the length against the bound, and against any remaining aggregate;
  3. the 32 digest bytes;
  4. exactly `length` payload bytes, where EOF is truncation;
  5. the digest;
  6. the strict decode and the re-encode comparison;
  7. the envelope (`protocolMajor`, `frameType`, `sequence`, direction);
  8. the closed payload schema, under the negotiated variant;
  9. the transition table.

  A zero-length payload is a decode refusal (TRUNCATED). Each is `PROVIDER.PROTOCOL_VIOLATION` with its detail.
- **LD-D2B-13. RCA-1's product handshake is the base.** The FA-2 and RUST3-LIM materialization maps recorded after-hashes for `handshake-v1.schema.json` that predate RCA-1's product commit `5b53e5e`, so D2b-0 re-derives each materialization on the current product bytes. It reports every difference from the maps' recorded hashes, and its review judges them.
- **LD-D2B-14. Replay.** The reference corpus D2b replays byte for byte is native wire owner trial 07 (`docs/implementation/m1/trials/native-wire-owner-07/subject/`, Grok "ACCEPT WITHIN STATED REFERENCE SCOPE"):
  - its 353 admission vectors and the decoder probes of `tools/check_reference.py` (`wire_examples`);
  - a differential test of D2b-1's decoder against `tools/wirecodec.py`'s refusal codes over the same inputs.

  They are vendored, hash-pinned, under `crates/components/tests/data/`. The native cases' 101 wire and startup cases are replayed where their executors' inputs are wire values.

## 3. Questions for the reviewer

- **Q1.** Is LD-D2B-1's split, with D2b-0 followed at once by a reviewed blind refresh, the right way to land a schema materialization that stales the receipt?
- **Q2.** Is LD-D2B-11's NFC predicate, exported from `opensip-identity`, acceptable, or must the normalization tables come some other way?
- **Q3.** Are LD-D2B-2's computed depth bound and LD-D2B-8's recorded TS2 aggregate gap the right handling of the two values no source fixes?

## 4. Checks (each sub-unit's lane)

- **Suites:** the components suite at base and candidate, and the identity suite for LD-D2B-11, with equal failure sets.
- **Formatting and lints:** rustfmt, and warning-denied Clippy.
- **Repository checks:** the package edges under the O1-a package policy, the operability source census, the census-closure check, and verify_design. For D2b-0, also its generation checks and the census `--check` after the blind refresh.
- **Mutations,** each failing its sub-unit's tests:
  - a non-shortest integer accepted;
  - an unsorted map accepted;
  - a tag accepted;
  - a non-NFC text accepted;
  - the length checked after allocation;
  - the digest unchecked;
  - a table row skipped;
  - the fallback not total;
  - an echo member ignored;
  - a limits member changed;
  - a commitment computed from a re-encoding.

## 5. Not claimed

- No caller, no supervision, and no fact admission.
- No qualification.
- D2's completion is not claimed until D2b-4 lands.
