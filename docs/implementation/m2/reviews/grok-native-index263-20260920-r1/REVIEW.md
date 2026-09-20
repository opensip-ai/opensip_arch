# Independent review — native retained metadata index 263

**Standing:** bounded native-Rust review of frozen `native-metadata-index-checkpoint-263`. Listed payload2 envelope pairing under a shared retained-byte budget, after 262 preflight. **Not** signature proof, filesystem custody, extra ninth-kind RA envelope rejection (252 recovery composition), payload1 preflight, full catalog/list/component/policy/repair/artifact, current+incoming revocations, or native publication. Archived 262 (`486ac7ba…0a54`) and 261 were not edited. 259 workspace 472+2 was **not** rerun. Installed product remains `fa72e50`.

Rust 1.95.0. Review-local `product/` copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4313608 B, 432 members, SHA256 `d79bed87b64cce577c0d6784be45b4112f848ea820d191b903842bb50355b15d`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 432/432.

Parent 262 pin `f78a584d…03cd` matches reviewed 262. Nested 258 pin `b36518ef…f622` matches reviewed 258. Included Index `be87c4c3…f1b7` and Operation `4917f3d7…486d` are byte-identical to that 258 candidate.

Product: **368** files vs 262. **366** byte-identical, **1** changed (`trust.rs`), **1** new fixture (`metadata-index263-cases.ndjson`). Inherited 262 path fixtures unchanged. `trust-before.rs` equals 262 `trust.rs`. Product-input hashes match 368/368.

---

## What 263 adds

`verify_envelope` shape decoding is factored into borrowed `CarrierView`; crypto verifier order (capability/body/shape/digest/domain/preimage/quorum) is preserved. Index pairing uses `parse_carrier` + `route_matches` only — **no signatures**.

Private `retained_metadata_index`:
- Budget: positive lower-only limits (65536 objects / 131072 edges / 256 MiB), 4 MiB per object, physical `(collection, raw SHA)`, Arc sharing, fail-latch. Index **borrows** the original budget; a second Index cannot reset it.
- `new`: retain supplied manifest (not retroactive capture proof) → 262 `admit` → charge **all declared edges** → read **only listed envelopes** in UTF-8 path order. Presence at **every distinct path**, even known content (`presence=true`; cap = retained length when the digest is already held, including zero remaining bytes).
- Cache raw + small decoded header by digest. Candidate lists keep distinct paths for identical bytes (no first-wins).
- `select`: body kind from manifest slot; root domain from exact `rootSchema` 1/2; exactly one `(kind, domain, storedSHA)`; RA must use the explicit envelope path; canonical preimage equality. Unrelated ambiguities do not globally refuse unique pairs.

Trusted capture adapter must enforce the requested cap **before allocation** and supply no-follow/custody. This module checks returned bytes only. 261 `SignedDocument` captures are **not** wired into this aggregate context. Parsed CPU/memory/concurrency are not this budget.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **186/186** (34 oracle cases + budget/presence/repeat-index tests; inherited 183 after parser refactor) |
| Exact live | workspace Clippy `-D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 8 compiled controls + baseline | **9/9**, SHA equal frozen `mutation-check-r1` |
| Inspected | 258 Operation/index oracle | unmodified; synthetic **invalid** signatures; pairing only |
| Inspected | r1 fixture driver | base64 vs required hex; all cases stopped at envelope shape; r2 encoding-only; production unchanged |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): first-candidate-wins; omit preimage; omit carrier route; omit exact RA envelope path; omit failure latch.

First fail **other** contract assertions (not exploit proofs):
- `skip-cached-content-presence`: capture-call list (`duplicate.sig` omitted).
- `omit-capture-digest`: counters (objects 3 vs 2).
- `omit-declared-edges`: counters (edges 0 vs 12).

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`Index` not `pub` |
| Known-content cap | `available` returns retained length for an existing key |
| 258 Index + Operation | byte-equal |
| 262 REVIEW.md | unchanged |

`known-content-at-full-budget` in the 34-case corpus is alias capture under an exact eventual-byte allowance; the direct Budget test is the actual zero-remaining presence case.

---

## Remaining (do not count closed)

Extra ninth-kind authorization envelope rejection (252); payload1 preflight; full catalog/list/component/policy/repair/artifact; complete retained/current+incoming revocations; held selection/ancestry/floors/S4; batch/effects; native fence/slot/census/durability/writers; 261 SignedDocument into this budget; source selection; M3–M6. 263 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 368 product files: 366 unchanged vs 262. 258 Index/Operation byte-equal.
- [x] **186** security tests, Clippy, and fmt reproduced. Eight controls behave as documented (five wrong admission; three other-contract first).
- [x] Listed-envelope pairing under shared budget after 262 preflight; no crypto from pairing; no first-wins on identical bytes.
- [ ] **Not** signature evidence, host capture/custody, extra-RA-envelope composition, current authority, or native publication.
