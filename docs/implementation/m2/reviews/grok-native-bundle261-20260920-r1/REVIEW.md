# Independent review — native recovery bundle document 261

**Standing:** bounded native-Rust review of frozen `native-recovery-bundle-checkpoint-261`. Exact raw-document capture plus prospective payload2/TR-BUNDLE over internally captured sources, invoking 260 on those Docs. **Not** complete retained inventory, path alias/NFC/casefold/preflight (262), listed envelope selection, all-member pairing, extra RA envelope restriction, catalog/list/component/policy/repair/artifact semantics, aggregate Operation, current revocation population, or native publication. Archived 260 (`2f263ca5…861e`) and 259 were not edited. 259 workspace 472+2 was **not** rerun.

Rust 1.95.0. Review-local `product/` copy only; installed product was not written. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4241932 B, 488 members, SHA256 `4eff98e1b6be980bc88246987f70f6eb997efcd0d3f5a12df88b0de843ff61bc`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 488/488.

Parent 260 pin `d5ac8acd…5e50` matches the reviewed 260 archive. Nested 252 r2 pin `3816972f…ccff` (20908 B / 211 members) matches the frozen 252 r2 trial; all 211 members rehashed. Reviewed helper bytes equal that extract: `payload_reference.py` `f6403a40…edaf`.

Product: **362** files vs 260. **359** byte-identical, **1** changed (`crates/security/src/trust.rs`), **2** new fixtures (`recovery-bundle261-cases.ndjson`, `recovery-bundle261-shape.ndjson`). `trust-before.rs` is byte-identical to 260 `trust.rs`. Product-input hashes match 362/362.

---

## What 261 adds

Private `mod verified_recovery_bundle`. `SignedDocument::capture` copies body and **raw envelope** bytes only after both 4 MiB caps, then **internally** parses the envelope. No caller-supplied parsed env. Getters still match the original source after the test harness clears the input buffers.

`verify_recovery_bundle_document` then: closed payload2 schema (`payloadSchema` integer 2, kind `recovery`; member lists syntax-only — 1..=1024 chars, no leading `/`, no NUL); exact **raw SHA** of captured RA body **and** raw envelope vs the payload pair; replacement **body** member in `rootChain`; 260 `verify_root_recovery` on internally captured Docs; prospective TR-BUNDLE under `EnvelopeReader { payload_schemas: [false, true] }` (payload2 only, no payload1 fallback) against the **new** root, filtered by supplied retained keys. Result owns three raw Docs plus 260 proof plus bundle quorum.

Path shape is schema **syntax** only. Unicode NFC, casefold, 1024-char preflight, aliases, reserved frames, and file-parent conflicts remain 262 / index owners.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **179/179** (includes 20 focused, 379 shape, two 4 MiB capture bounds) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | 6 compiled omission controls + baseline | **7/7**, SHA equal frozen `mutation-check-r1` |
| Exact live | extra-field permissive control | compiled, **wrong admission of `payload-extra`**, SHA `9fe7534c…e37b` |
| Inspected | r1 harness failure note + r1 keys | serialization of bytes in full 252 result; r2 records standing/manifest/authorization/quorum only; production unchanged |

20 focused cases: 17 aligned with 252 reference plus 3 native capture negatives (`raw-envelope-malformed`, `duplicate`, `body-swap`). Three successes: valid prospective BUNDLE, two surviving BUNDLE keys, coherent raw-envelope whitespace. Unbound whitespace bytes refuse even if a parsed envelope would still verify. Actual source envelope hash is raw stored bytes, not canonical re-encoding.

**Controls (honest, not all exploits):**

- Omit body pair / envelope pair / replacement member / BUNDLE revocation filter: tests fail as intended.
- `omit-schema-gate`: first failure is `BundleEnvelope` vs expected `PayloadShape` — private diagnostic order, **not** proof that extra fields would be admitted.
- Extra compiled control (`closed(..., &["extra"])`): **does** admit a validly signed extra-field payload (`payload-extra: left true / right false`).
- `held-root-bundle-keys`: positive `valid-prospective-bundle` fails (`BundleEnvelope`) because old BUNDLE keys are not the replacement set.

No compile errors counted as successes. No native-exploit claim.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`SignedDocument` not `pub`; fields private |
| Caps before copy | oversize body or envelope → `Limit` |
| Payload2 only | `[false, true]`; bool schema refuses |
| Pair hashes | `raw_sha256` of captured body and raw envelope |
| 252 helper/tar | byte-equal frozen 252 r2 |
| 260/259 REVIEW.md | hashes unchanged |

This still does not prove path identity, full member inventory, extra RA envelope absence, or current authority.

---

## Remaining (do not count closed)

Cross-slot path normalization/aliases/reserved frames/file-parent conflicts and NFC/casefold/preflight (262); exact listed envelope selection; all-member capture/presence/pairing; other-root chain; extra authorization envelope restriction; catalog/list/component/policy/repair/artifact; aggregate Operation; retained+incoming union; ancestry/floors/S4; batch/effects; custody/fence/slot/census/durability; source selection; M3–M6. 261 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 362 product files: 359 unchanged vs 260. Nested 252 r2 211/211 rehashed.
- [x] **179** security tests and workspace Clippy reproduced. Six omission controls plus extra-field wrong-admission control behave as documented.
- [x] `SignedDocument` owns raw body+envelope; payload2 opt-in; 260 invoked on captured Docs; prospective BUNDLE on replacement keys. Path checks are syntax only.
- [ ] **Not** full inventory, path semantics, envelope-index pairing, current authority, or native publication.
