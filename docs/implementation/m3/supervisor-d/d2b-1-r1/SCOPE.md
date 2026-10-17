# D2b-1 r1: the strict CBOR profiles, the framing and the commitments (M3-D r5 item 10; D2b plan, sub-unit D2b-1)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements sub-unit D2b-1 of the D2b plan (`../d2b/PLAN-r3.md`; LD-D2B-1's split). D2b-1 is the shared wire mechanics: library only, with no caller and no codec. The table engine is D2b-2's, and the two codecs are D2b-3's and D2b-4's.

**Base:** product main as the subject manifest names.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/provider_protocol.rs` (new) | **The frame prefix (DLV:1111; RPP:160-170).** `read_frame` reads the 8 length bytes; checks the length against `MAX_FRAME_PAYLOAD_BYTES` (67,108,864) and any remaining aggregate before reading or allocating anything more; reads the 32 digest bytes and exactly `length` payload bytes (EOF inside a frame is truncation; EOF at a boundary is `Ok(None)`, which only the table may accept); checks the digest; then decodes under the selected profile (LD-D2B-12 steps 1 to 6). `write_frame` writes the prefix and the deterministic encoding, never over the bound.<br>**`FrameAccumulator`** is the same acquisition for a non-blocking stream (for D3a's participant, Codex D3APLAN-R1-RF-1): bytes are pushed in any split and the partial prefix and payload are kept across calls; the length is judged against the bound and the remaining aggregate the moment its eighth byte arrives, before any digest or payload byte is kept; the payload is allocated only then; a completed frame has its digest and strict decode checked; `at_boundary` and `finish` tell EOF at a boundary from truncation; a refusal ends the stream (`AfterRefusal`).<br>**`ReceivedFrame`** keeps the exact payload, its decoded value and each value's received byte range. **`ReceivedBytes`** borrows a value's received bytes from the frame; only `ReceivedFrame::node` makes one (LD-D2B-3 item 5).<br>**`Sequence`:** from 0, stepping by exactly 1, never reaching 2^64 − 1 (DLV:1123).<br>**Commitments (DLV:1077):** `received_commitment(domain, elements)`, `C(d, v)` over an array of received values with the array head computed from the count; `built_commitment(domain, value)` for a value the host builds; `manifest_digest(entries)`, the bare `hex(SHA-256(dCBOR(entries)))`. |
| `crates/components/src/provider_protocol/cbor.rs` (new) | **The strict deterministic-CBOR reader and encoder** for `ts2-cbor` and `rust3-cbor` (DLV:650-656; RPP:172-199): null, false, true, unsigned integers, negative integers under `ts2-cbor` only (to −2^63), NFC UTF-8 text, byte strings, definite arrays and text-keyed definite maps with strictly ascending encoded keys. Shortest heads only; no tag, float, other simple value or indefinite length; nothing after the item; and the value must re-encode to exactly the received bytes. Refusals carry the reference decoder's codes (trial 07 `tools/wirecodec.py`), plus `DEPTH`. The reader is iterative, with an explicit stack bounded by the caller's `max_depth` (LD-D2B-2: the bound's value is D2b-3's and D2b-4's), and never allocates from a claimed length. `decode_spanned` also returns each value's received range in pre-order (map keys are not nodes). The encoder is iterative too. |
| `crates/components/src/provider_protocol/cbor_tests.rs` (new) | 8 tests (below). |
| `crates/components/src/provider_protocol_tests.rs` (new) | 9 tests (below). |
| `crates/components/tests/data/cbor-differential.v1.json` (new) | The differential corpus (LD-D2B-14), 7,550 cases: inputs and the reference decoder's outcome under each profile. Built by `evidence/build_cbor_differential.py` from trial 07's `tools/wirecodec.py`, read in place and pinned by SHA-256 in the corpus and the test. |
| `crates/components/src/lib.rs` | `pub mod provider_protocol`, and the module comment. |
| `crates/components/Cargo.toml` | `opensip-identity` moves from a dev edge to a normal edge (`is_nfc`, SHA-256). Both edges stay among the crate's permitted owners. |
| `crates/identity/src/lib.rs` | `is_nfc(&str)` over the pinned `unicode-normalization` (=0.1.24), and `NFC_UNICODE_VERSION`, its tables' Unicode version (LD-D2B-11). |

## The tests

- **The reference probes** (trial 07 `check_reference.py` `wire_examples`), each with its profile and code: NEGATIVE_INTEGER_FORBIDDEN, NON_SHORTEST, MAP_ORDER (unsorted, and length-first), DUPLICATE_KEY, FLOAT_OR_SIMPLE, TAG, INDEFINITE_OR_RESERVED, NON_NFC; a negative chunk index decodes under `ts2-cbor`.
- **Non-shortest heads:** every wider head of every boundary value refuses, for integers and lengths.
- **Negative integers** follow the profile, down to −2^63; −2^63 − 1 is INT_RANGE.
- **Closed forms:** simple values, floats, the break byte, tags, indefinite lengths, reserved additional information, non-text keys, invalid UTF-8, truncation and trailing bytes; a non-NFC key.
- **Claimed lengths** of up to 2^64 − 1 refuse TRUNCATED at once, with nothing allocated.
- **Depth:** the bound is exact (at the bound decodes, one over refuses `DEPTH`), maps count the same, and a million levels refuse at the bound with no recursion.
- **Deterministic encoding:** map members sort by encoded key; round trip.
- **The differential** (LD-D2B-14): all 7,550 cases decode or refuse exactly as the reference did. Both Unicode versions are pinned (LD-D2B-11): the reference's `unicodedata` (16.0.0, recorded in the corpus) and the tables' `NFC_UNICODE_VERSION` (16, 0, 0).
- **Frames:** a round trip of two frames then EOF at the boundary; an over-bound length (and one over the remaining aggregate) refuses with only the 8 length bytes read; truncation at every cut; a wrong digest (in the prefix or the payload); a zero-length payload (TRUNCATED, LD-D2B-12); a non-canonical payload under a correct digest; a stream error.
- **The accumulator:** at every split of a two-frame stream, and one byte at a time, it yields `read_frame`'s frames, and EOF is the boundary exactly between frames; an over-bound length refuses when its eighth byte arrives, before any digest byte; the remaining aggregate falls by each payload and bounds the next frame; a digest or decode failure refuses; a refusal ends the stream.
- **Sequences:** from 0, by exactly 1, never 2^64 − 1.
- **Commitments:** trial 07's `commit-empty-stream` known answer (`received_commitment` over no elements and `built_commitment` of `[]`), and the empty manifest digest `hex(SHA-256(0x80))`; the domain separator.
- **Received ranges:** every value's bytes in pre-order, members in received (encoded-key) order.
- **Provenance (LD-D2B-3 item 5):** a received commitment's elements are slices inside the received payload's allocation, and it equals the built commitment of the same value; order and domain matter.

## Checks

Lane r1, attempt 3, `evidence/d2b-1-checks-r1/` (the lane of record):
- **Attempt 1** (`evidence/d2b-1-checks-r1-attempt1/`) passed every check and all eight mutations except the package edges, which ran against inventory v214 while the lock had bound v215 ("selected artifact path differs"). The runner now reads the lock's current inventory, and the worktree moved onto main's lock-only v216 commit. Since attempt 1, `FrameAccumulator` and its two tests were added (above), with their mutations.
- **Attempt 2** (`evidence/d2b-1-checks-r1-attempt2/`) passed every check and the first six mutations, then stopped: the `digest-unchecked` mutation's text also matched inside the accumulator's digest check, so its anchor was not unique. The anchor now includes `read_frame`'s preceding lines, and the accumulator's digest check has its own mutation.

The checks:
- **the components and identity suites** at base and candidate, with equal failure sets and the new passing tests (components 17, identity 0);
- **rustfmt** on the new files (and the base-clean edited ones; identity's `lib.rs` is base-dirty and only appended to), and warning-denied all-targets Clippy on `opensip-components` and `opensip-identity`;
- **the provider protocol tests;**
- **the differential corpus regenerated** byte for byte from the reference (`build_cbor_differential.py --check`);
- **the package edges** under the O1-a package policy: components' internal edges are exactly `opensip-contracts` and `opensip-identity`, both normal;
- **repository checks:** the environment exceptions, the operability source census, the census-closure check (no closure file changed) and verify_design;
- **mutations,** each failing the provider protocol tests:
  - a non-shortest integer accepted;
  - an unsorted map accepted;
  - a tag accepted;
  - a non-NFC text accepted;
  - the depth bound unchecked;
  - the length checked after the payload is allocated;
  - the digest unchecked, in `read_frame` and in the accumulator;
  - the accumulator judging the length only once the whole prefix is held;
  - a received node copied rather than borrowed (the provenance control).

## Not claimed

- No caller, no codec, no table, no supervision.
- No depth bound's value (D2b-3 and D2b-4 compute it over the wire closure, LD-D2B-2).
- No qualification; D2b's completion is not claimed.

## Inventory

`crates/components/src/provider_protocol.rs` realizes its planned row ("Dispatch the selected provider wire protocol and validate its transaction boundaries."); D2b-1 delivers only its shared mechanics. New paths: `crates/components/src/provider_protocol/cbor.rs`, `cbor_tests.rs`, `crates/components/src/provider_protocol_tests.rs` and `crates/components/tests/data/cbor-differential.v1.json`.
