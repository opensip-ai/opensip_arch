# Independent review — ordinary signed inventory and retained bytes 283

**Standing:** bounded native-Rust review of frozen `native-ordinary-inventory-checkpoint-283`. Composes 282 real BUNDLE authentication with retained ordinary inventory on **one** operation Budget. **Not** other-member signature authentication, current-root/chain/population admission, time, filesystem custody, artifact recapture, operational grant, or M3–M6. The supplied signing root is **context membership** (exact `rootChain` DocRef member whose captured body equals the supplied validated root), not a rule that chooses or admits the current root. Archived 282 (`0e1985be…b6dd`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5626836 B, 584 members, SHA256 `95ef4502c4e957761b4fce7a87ef48f258b07ac6e866b49377b5582bb733fff5`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **584/584**. Product-inputs **426/426** live-equal.

Nested parent 282 pin `4b832a3a…a0eb` (5609660 B / 568 / 424 files) equals the reviewed 282 freeze; live trial tar still matches; `trust-before.rs` equals that 282 `trust.rs`. Nested 265 `73c3b3f5…86df`. `Cargo.lock`, `lib.rs`, `trust_ordinary_bundle.rs`, and 282 fixtures unchanged.

Product vs 282: **426** files, **423** unchanged, **1** changed (`trust.rs` `30940946…ff6c` — `include!("trust_ordinary_inventory.rs")`), **2** added (`trust_ordinary_inventory.rs` `a32bcf19…1c40`, `inventory283.ndjson`). No public API. No full workspace rerun (277 515+2 predecessor only).

---

## What 283 adds

`ordinary_inventory::prepare` admits current-125 **NodeRef** (closure) and **DocRef** (signing root) **before** I/O. Closure loads from Records and is admitted as **PRODUCT** canonical `PayloadMetadataClosureV1` (4MiB / depth 32 / no NFC). Scope must be `ordinary-inert`. The supplied signing-root DocRef must be an exact `rootChain` member, and the retained body must parse equal to the supplied `ValidatedRootPayload`. Then 282 `authenticate` runs on the same Budget through a nested `b.load` capture adapter into 281 `Index`.

Signed root rows bind cardinality, order, and body SHA to closure DocRefs. Catalog/revocation refs, exact retained envelope/manifest/policy **sets**, strictly ordered `(slot,path)` pairs, repair presence/typed absence, and artifact observation path/digest/order are bound. `observedBytes` stay asserted observations, not recaptured artifacts. Selected metadata pairs bind **both** raw SHA **and** byte length of body and envelope. All declared non-artifact bytes are retained, including opaque repair and policy. No recovery-only ninth-envelope rule: `unrelated-envelope-ambiguity` and `unpaired-authorization-header-inert` remain valid.

`Evidence` owns raw/admitted closure, signing-root ref, BUNDLE proof, pairs, artifact observations, and retained members after inputs and Budget drop. Repeat calls charge every reference edge; physical objects stay cached; any error closes the Budget.

Other catalog/list/component envelopes in these fixtures use **zero signatures** and minimal bodies: pairing only, not crypto or semantic admission.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo clean -p opensip-security` then `cargo test -p opensip-security` | **229/229**, `Compiling opensip-security`, includes `ordinary_inventory::tests::ordinary_signed_inventory_binds_exact_retained_members_on_one_budget` |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | `rustfmt --check --edition 2024` on all **3** include files | **pass** |
| Exact live | 15 compiled r2 variants + baseline | **16/16** core-equal frozen `mutation-check-r2`; **14 caught**, **1** documented undetected redundant `omit-member-order` |
| Exact live | Python source/fixture probes | **26/26** |
| Inspected | 49 cases / 8 initial / 8 repeated | baseline 12 objects / 31 edges / 16319 bytes; repeat 12/62/16319; 12 physical captures |
| Inspected | 43-row beforeimage | `inventory-before-docref-isolates.ndjson`; six `isolated-docref/{catalog,revocation}/{length-minus,length-plus,digest}` added |
| Inspected | r1 three undetected | `omit-member-order` (redundant); `omit-exact-document-lengths` / `omit-exact-document-digests` (BlobRef/DocRef alias) |
| Inspected | 277 workspace 515+2 | predecessor only; not rerun |

**Controls (honest). Do not report 15 caught.**

Wrong admission (`left: true` / `right: false`): `omit-ordinary-scope`, `omit-signing-root-membership`, `omit-signing-root-context`, `omit-root-cardinality`, `omit-repair-absence-binding`, `omit-artifact-digest`, `omit-exact-document-lengths`, `omit-exact-document-digests`.

Caught **other** (not exploit proofs):

- `omit-closure-canonical-shape`: counters `(4, 4, 12193)` vs `(1, 1, 1995)` (parse_json without product shape).
- `drop-revoked-key-context`: owned BUNDLE revoked set empty vs supplied keys.
- `omit-member-sets`: later panic/set mismatch (not `left: true`).
- `skip-policy-retention`: counters `(11, 30, 16317)` vs `(12, 31, 16319)`.
- `lose-owned-signing-reference`: `Null` vs owned DocRef after drop.
- `omit-failure-latch`: `(4, 8, 12395)` vs `(4, 4, 12395)`.

**Undetected by design:** `omit-member-order` compiled, exit 0, `caught=false`, `redundantGuard=true`. Full-125 closure admission already enforces strict member order/uniqueness (`members-out-of-order` / `members-duplicate`). This is **not** a caught vulnerability and is **not** a 15th catch.

Frozen `mutation-check-r1`/`r2` were not overwritten. r2 baseline SHA is current `trust_ordinary_inventory.rs` `a32bcf19…1c40`. Production functions did not change for the six DocRef isolates.

---

## Focused findings

### DocRef SHA and length are independent of retained BlobRefs

Original 43 cases aliased closure catalog/list envelope **DocRef** objects with retained envelope **BlobRefs**, so mutating either mutated both and earlier checks still failed. Six r2 isolates change **only** the closure DocRef (`isolated-docref/catalog|revocation/{length-minus,length-plus,digest}`). Omitting exact length or digest checks now **wrongly admits**. That is a real owner requirement, not BlobRef duplication.

### Local member-order guard is redundant

`Error::MemberOrder` repeats what `PayloadMetadataClosureV1` already requires. Removing it does not admit `members-out-of-order`. Documented undetected redundant guard.

### Same Budget, pairing vs crypto

282 BUNDLE is the only cryptographic authentication. Index capture uses nested `Budget.load` so each edge still charges. Unrelated RA-header ambiguity stays inert; no invented recovery-only envelope-count rule. Artifact `observedBytes` are observations, not custody.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | not in `lib.rs`; included from `trust.rs` |
| NodeRef/DocRef before I/O | yes |
| Product canonical closure | `PayloadMetadataClosureV1` then `ordinary-inert` |
| Signing root | exact chain member + captured body equals supplied root |
| 282 then 281 | `B::authenticate` then `Index::with_context` via nested load |
| 49/8/8 | asserted and counted |
| Six isolates | present; 43-row beforeimage |
| r1 vs r2 | three r1 undetected; r2 lengths/digests now wrong admissions; order still redundant |

---

## Remaining (do not count closed)

Ordinary root-chain/catalog/list/component signature and semantic admission; finite revocation union; historical/current context and time; physical capsule admission; accepted-role effects; artifact/repair/command integration; native private-policy custody/absence/adoption; fences/census/durable writers; runtime/source selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 426 product files: 423 unchanged vs 282. Nested 282/265 pins match live trial archives.
- [x] **229** security tests after `cargo clean -p opensip-security`, Clippy, cargo fmt, rustfmt of all three include files. Fourteen compiled r2 variants caught; one redundant `omit-member-order` guard remains undetected as documented. No workspace rerun.
- [x] Same-Budget 282 BUNDLE + 281 index; signing-root membership/context; DocRef SHA **and** length on selected pairs; six isolates expose BlobRef alias; supplied root is not current authority.
- [ ] **Not** other-member crypto, current-root/population, time, custody, operational grant, or product installation.
