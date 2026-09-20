# Independent review — native full manifest and recovery release bindings 268

**Standing:** bounded native-Rust review of frozen `native-manifest-checkpoint-268`. Full completed-manifest structural checker plus authenticated catalog-row joins after 267. **Not** packaged policy/repair/artifact semantics, raw host-context adapter, current registry/custody/population, non-key subjects, other-root contexts, held custody/ancestry/floors/S4, batch/effects, native fence/slot/census/durability/writers, source selection, or M3–M6. Archived 267 (`a527bf53…835ce`), 266, 264/265, and the length investigation were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5001656 B, 587 members, SHA256 `40fbfe5f209b0ee4fae244ab76b708a37d2ab7eb4aad993f602a7e0b15e2a5ba`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 587/587. Product-inputs 383/383 live-equal.

Nested parent 267 pin `dee1d3e8…94e6` (4652440 B / 536 / 377 files) equals the reviewed 267 freeze; `trust-before.rs` equals that 267 `trust.rs` (`069f67d5…ad4b`). Nested 265 `73c3b3f5…86df`, 254 r1 `a22c65bd…5a01`, 253 `164dd2fa…f8b7`, 252 r2 `3816972f…ccff`, 250 r2 `dbf1aa27…cf85` match reviewed archives. 250 helper `44a38c7d…cea2b`. Completed schema `manifest-schema.completed.v1.json` SHA256 `a514071431a79bb7c2aa5d9562125ec29609e0562221e22164ed0b36758c90af` (24193 B) matches README/generator report.

Product vs 267: **383** files, **376** unchanged, **1** changed (`trust.rs` `c135af8f…4297`), **6** added (`component_manifest.rs` `c4daa5dd…e50a`, `component_manifest_shape.rs` `efb068ac…70d8`, four fixtures). Inherited 267 fixtures unchanged. `trust-before-preimage-fix.rs` (`59f73480…64d5`) is the failed first join.

---

## What 268 adds

Private generated `component_manifest_shape.rs`: 123 nodes (`node_0`…`node_122`) from the exact completed schema; every keyword/pattern checked at generation; `uniqueItems` is string-only (`unique` in the semantic module). Static functions, no runtime schema compiler, no new crate dependency. Metadata parse still 4 MiB / 64 depth; `bounded` adds 100000 array caps. Display text is a string with **no** NFC requirement.

Private `component_manifest::validate`: command tree (single root named as the package, sibling/alias uniqueness, option defaults, positional grammar, parent walk depth 32); platform uniqueness; tree paths 1024 **UTF-8 bytes** plus Windows device/trailing-dot-space/drive restrictions, declared directory parents, Unicode 15 NFC+casefold aliases, symlink closure/cycles, executable entrypoint; capability uniqueness and `typescript.reachability`→`calls`; permission/dependency uniqueness, no self-dependency, nonempty version intervals; compatibility echo (`hostCore` nonempty, `manifest` equals `manifestSchemaVersion`); approved exceptions and declaration references; host-reviewed configuration classification/required-field/range. Path profile is **not** 262 logical metadata path. Fixture proof: no non-ASCII Unicode 15 upper aliases into the reserved device-stem alphabet, so ASCII `to_ascii_uppercase` is sufficient there.

Private `recovery_metadata::prepare` is `budget.scope` and calls 267 `recovery_catalog::prepare` **once** on that budget. Presented-manifest path set must equal typed `HostContext` keys; context admits only `approvedExceptions` / `hostClassificationMap` / `liveNames`; reserved names come from the actual catalog. That typed context is supplied evidence, not host custody. Each signed manifest (signed order, not BTreeMap) runs the full structural checker, then joins the unique catalog tuple `(stableId, publisher, sourceClass, version)`, publisher = 266 filtered proof namespace, raw body SHA, **metadata preimage SHA**, raw envelope SHA, and exact `hostCoreConstraint`. Zero or multiple presented manifests are legal; unpresented catalog rows remain allowed. Evidence owns catalog/signed proofs/validated bodies/release rows.

`HostContext` cannot represent extra raw fields; a pending adapter would still have to decode/size/populate host context.

No public API (`component_manifest` is `#[path]` inside private `trust`; `lib.rs` does not export it).

---

## Preimage vs signature message

`verify_envelope` computes **two** digests: `preimage_digest = metadata_digest_for_domain(domain, payload)` and `message = metadata_domain_digest("envelope", subject+role+namespace)`. `QuorumReport.message` is the latter.

The first signed integration (`security-signed-r1`) refused `valid` with `Some(Preimage)` because the join compared `group.proof().message()` to catalog `manifestPreimageSha256`. That failed receipt and `trust-before-preimage-fix.rs` are retained.

Live join parses the **same immutable captured envelope bytes** already verified by 266 (`parse_carrier` → `CarrierView.preimage_digest()`). No new store read, no caller-supplied carrier, no new crypto.

Independent probe on the frozen `valid` fixture: catalog preimage = carrier `preimageSha256` = recomputed domain preimage `a1387507…47aa`; recomputed envelope **message** `7052e32b…0ac7` (role `TR-COMPONENT`, namespace `opensip`) is **not equal**. The compiled control `conflate-signature-message-and-preimage` restores the bug and over-refuses `valid` (`left: false` / `right: true`), not a wrong-admission exploit.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **196/196** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 15 compiled controls + baseline | **16/16**, SHA-equal frozen `mutation-check-r1` |
| Exact live | preimage≠message on `valid` envelope | message `7052e32b…` ≠ preimage `a1387507…` |
| Inspected | 11010 schema differentials / 364 positive | generated closed schema vs original five complete examples |
| Inspected | 186 structural semantic / 26 positive | original 183 + decomposed display/array 100000/100001 |
| Inspected | six structural-projection deltas | open platform, unsupported preview state, two artifact digest cases, missing release artifact, nonempty preview configuration — **not** implemented preview-profile/artifact custody |
| Inspected | 36 signed (32+4 multi) / 8 positive | baseline **14/40/21470**; multi nonlexical/reverse order; missing second context; zero presented |
| Inspected | signed-r1 | first `valid` refused `Preimage`; r2 after preimage fix |
| Inspected | workspace-final-r1 | **493** crate tests + **2** doctests; not rerun |
| Inspected | generator style-before images | parentheses/redundant closures/`len>=1`; no schema/semantic change |

**Controls (honest):**

Wrong signed admission (`left: true` / `right: false`): skip schema; skip command semantics; skip platform tree; skip permission uniqueness; skip host configuration; skip compatibility echo; arbitrary first catalog row; skip namespace; skip body/preimage/envelope digest; skip host-constraint join; allow extra host-context **path**.

First fail **other** assertions:

- `conflate-signature-message-and-preimage`: over-refuses coherent `valid` (`Preimage`).
- `omit-outer-semantic-latch`: follow-up prepare not closed after failure.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | not `pub` |
| Generated nodes | 123 unique `node_0`…`node_122` |
| Path vs 262 | 1024 UTF-8 **bytes**, NFC, Windows stems; 262 is 1024 **chars** logical metadata path |
| Display text | schema node is any string; no NFC gate |
| `x-maxUtf8Bytes` | annotation not generated; `path_ok` is the semantic owner |
| Store cleared after success | owned catalog/components remain |
| Zero presented | legal; extra catalog row unpresented |

---

## Remaining (do not count closed)

Packaged policy/repair/artifact semantics; raw host-context adapter and current registry; population/non-key subjects; other-root contexts; held custody/ancestry/floors/S4; batch/effects; native fence/slot/census/durability/writers; source selection; M3–M6. Full structural acceptance is not artifact or execution admission. 268 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 383 product files: 376 unchanged vs 267. Nested 267/265/254/253/252/250 pins match reviewed archives. Completed schema pin matches generator.
- [x] **196** security tests, Clippy, and fmt reproduced. Fifteen controls behave as documented (13 wrong signed admissions; message/preimage conflation over-refuses valid; outer latch first fails closed-budget).
- [x] Preimage join uses `CarrierView.preimage_digest` from the 266-captured envelope; signature message is distinct (live probe). Same-budget 267 prepare; signed-order components; unpresented catalog rows allowed.
- [ ] **Not** full current authority, artifact/preview custody, native host-context adapter, or product installation.
