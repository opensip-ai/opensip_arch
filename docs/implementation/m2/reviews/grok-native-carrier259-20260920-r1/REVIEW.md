# Independent review — native recovery carrier 259

**Standing:** bounded native-Rust review of frozen `native-recovery-carrier-checkpoint-259`. Ports reviewed 233 carrier behavior onto a 223 product snapshot. **Not** body admission, current authority, filtered revocation population, held-root/S4, operation budget, native publication, or source selection. Next 260 is expected to join authorization bodies; mismatched body authority is still only carrier evidence here. Archived 258 (`4c33b6c8…6e96`) and 255 were not edited.

Rust 1.95.0. Review-local `product/` copy only; installed product and the author tree under `/tmp/opensip-implementation/m2-native-recovery-carrier-259` were not written. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4267240 B, 441 members, SHA256 `233fee7d1f1fa0caa0e7083f607221cd5b42e31201524e913d028b3b4b62da4b`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 441/441. Standing: Unaccepted private 259; no installation/selection.

Parent 223 pin `482759b7…51e2` (4099076 B / 384 members / 356 product files). Nested 258 pin `b36518ef…f622` matches the reviewed 258 archive.

Product: **359** files vs 223. **355** byte-identical, **1** changed (`crates/security/src/trust.rs`), **3** new fixtures (`recovery-carrier259-cases.ndjson`, `-historical-deltas.json`, `-roots.json`). Product-input hashes match extract bytes 359/359. Historical `envelope-cases.ndjson` (1284 rows) and `complete-envelope-cases.ndjson` (1805 rows) are byte-identical to the 223 parent.

---

## What 259 ports

Private `EnvelopeKind` grows a ninth variant `RootRecoveryAuthorization`: kind `root-recovery-authorization`, domain `opensip.metadata.root-recovery.1`, role `RECOVERY`. `from_name` has no unknown-kind fallback.

Payload dispatch requires an **exact integer** `payloadSchema` 1 or 2, matching domain `opensip.metadata.payload.{1|2}`, before preimage/signer work. Bool/string/zero/three/missing/array discriminators refuse. `CURRENT_ENVELOPE_READER.payload_schemas` is `[true, false]` — existing callers are not opted into payload 2. Empty capability/kind/root declarations refuse `ReaderDeclaration` before signatures.

Existing Ed25519, profile, and quorum implementation is reused. `verify_envelope` is `pub(super)`; `EnvelopeKind` / `EnvelopeReader` are not public. This is not lasting custody or a public carrier API.

r2 vs the r1 security snapshot of `trust.rs`: **only** the historical-delta inventory assertion `[19, 52]` → `[14, 47]`. Carrier dispatch/capability/domain/recovery-role bytes are otherwise identical.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test --offline --locked -p opensip-security` | **175/175** |
| Exact live | Four compiled controls + baseline | **5/5**, source SHA equal frozen `mutation-check-r1` |
| Inspected | Recording r2 report | **52/52** assertions; **44** signed native rows (outcome/roots/keys/threshold/message/stored/preimage) |
| Inspected | Historical deltas | complete **47** SHA+before equal reviewed 233; older **14** against own bytes; outcome-string changes **32 / 12**; all listed after=`RJ-4 ENVELOPE_MISMATCH` |
| Inspected | Workspace `workspace-r2.stdout` | **472** crate tests + **2** doctests = **474** passed, 0 failed (request said 473+2; the receipt sum is 472+2) |
| Inspected | Clippy r2 `-D warnings` | pass (r1 compile log retained) |

Recording r1 stopped **before crypto**: 233 editable candidate lacked pinned `docs/coop/architecture-depth-review/REVIEW.md`. r2 recording driver uses the 258 candidate; frozen report `verifierSha256` `ea06a785…69d1` equals 233/258 `envelope_reference.py`; schema `3657ef69…a045`, routes `674c1bf5…4057`. Source pins checked before/after. No pin bypass.

r2 oracle narrowing removed five unchanged strict-parse failures per historical corpus (duplicate key, float, NaN, BOM, integer overflow). Those rows remain in `historical-deltas-before-r2.json`. Root placeholders stay skipped in the inherited old test; full successor root cases remain. No unused exemption of the 47/14 reviewed rows.

Controls (compile, then fail tests): omit payload dispatch; omit capability check; omit domain match; select `QuorumRole::Root` for the RECOVERY ninth kind. Baseline `envelope_tests::` passes.

---

## Independent probes

| Probe | Result |
|---|---|
| Ninth kind domain/role | `root-recovery.1` / `RECOVERY` |
| Payload integer 1/2 only | bool/string/zero/three refuse in recording |
| Default capability | payload1 only; empty decl `ReaderDeclaration` |
| Public API | `EnvelopeKind`/`EnvelopeReader`/`verify_envelope` not `pub` |
| 44 signed rows admit all 9 kinds | `admitted.len()==9` in the native test |
| Frozen old fixture bytes | equal 223 parent |
| 258/255 REVIEW.md | hashes unchanged |

Mismatched authorization **body** vs carrier still verifies as carrier evidence only.

---

## Remaining (do not count closed)

Authorization/bundle/metadata body joins (260); current filtered revocation population; held-root, ancestry, floors, S4; role/batch/whole-image effects; native fence/slot/custody/census/durability/writers; full operation budget. Workspace build is a local development check, not isolated-host or release qualification. 259 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 359 product files: 355 unchanged vs 223, `trust.rs` + 3 fixtures. Old 1284/1805 fixture bytes unmodified.
- [x] **175** security tests reproduced. Four omission controls caught; baseline passes. 52 recording assertions / 44 signed rows inspected; verifier byte-equal 233.
- [x] Historical 47 complete rows match reviewed 233 hashes and before-results; r2 only dropped five unchanged parse failures per corpus and the matching test counts.
- [ ] **Not** body admission, current authority, native publication, or product selection.
