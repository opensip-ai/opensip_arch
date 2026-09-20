# Independent review — native retained recovery 264 + reference length 265

**Standing:** bounded review of frozen `native-retained-recovery-checkpoint-264` and `retained-document-length-reference-wip-265-r1`. Enforces existing DocRef/BlobRef length meaning on already-captured recovery pairs. **Not** catalog/list/component body+quorum admission, current+incoming revocation union, policy/repair/artifact semantics, held custody/ancestry/floors/S4, batch/effects, fence/slot/census/durability, source selection, or M3–M6. Archived 263 (`ba7895f5…dca9`) and the length-investigation `REVIEW.md` (`367ae8b1…9b96`) were not edited. Wording-only `CORRECTION.md` (`efd4d80f…f428`) sits beside that investigation. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Historical wording (investigation, not this freeze)

The length-investigation sentence that “261 already bounds both SignedDocument inputs by declared size” is wrong. Frozen 261 `SignedDocument::capture` still applies two 4 MiB caps, parses the raw envelope, then copies; there is **no** BlobRef `bytes` input. Declared-length ownership is new 264 `Budget.load`. The inventory gap and captured-pair comparison remain valid. See `/tmp/opensip-implementation/reviews/grok-retained-length264-20260920-r1/CORRECTION.md`.

---

## Verification

| Subject | Bytes | Members | SHA256 |
|---|---|---|---|
| Frozen 264 | 4431648 | 513 | `1e505a86141e7cb29b2d5b72532c91df4120a66d89c7b6ca899d82be0f9e2d08` |
| Frozen 265 | 2290904 | 1630 | `73c3b3f55052cb2dd4623616fc68e887d7d4b0497bd941f7182059c2788986df` |

Pin, tar, member count, and every `subject.json` hash matched **before** extract. Extract rehashed 513/513 and 1630/1630. 264 product-inputs 371/371 live-equal. Parent 263 pin `d79bed87…b15d` (368 files). Nested 258 `b36518ef…f622`, 252 r2 `3816972f…ccff`, 250 r2 `dbf1aa27…cf85`, 265 `73c3b3f5…86df` match reviewed archives.

264 product vs 263: **371** files, **367** unchanged, **1** changed (`trust.rs` `45877753…fb9d`), **3** new fixtures (`retained-recovery264-{cases,lengths,shape}.ndjson`). `trust-before.rs` equals parent 263 `trust.rs` (`a64e1c34…899f`). `trust-before-length-binding.rs` (`f6af76ca…6cb7`) is the r1 port (SHA-only pair join); r1 mutation baseline SHA-equals that file.

265 candidate vs 258: **1374** files. **1365** unchanged, **8** changed, **1** added. The eight changes are `trust_payload_reference.py` plus seven pin inventories (including r2 `current-source-pins.v1.json`). Added `docs/v2/architecture/trust-retained-document-lengths.v1.md` (`da0762c8…7a27`). Payload helper vs 258 is **one added require**. `command_metadata_reference.py` is byte-identical (`72c1696f…95af`).

---

## What 265 adds

After `index.select`, the existing SHA join is kept (`retained-document-envelope-binding`) and a second private require compares **already captured** pair lengths to both DocRef BlobRefs (`retained-document-byte-binding`). No extra load, edge, object, or crypto. Outer Operation guard still latches. Closed BlobRef schema is unchanged (1..4MiB). This is enforcement of existing DocRef meaning, not a new wire format.

Nine focused cases (live core-equal frozen `length-check-r1/report.json`): three coherent positives including an extra retained root (counters 16/46/27105; that root is **not** authenticated); six catalog/list/other-root envelope-length lies that **258 admits** and **265 plus 258 graph walk refuse**. Fail-stop `operation-budget-closed` on the same Operation. Baseline catalog/list counters remain 14/40/18329.

---

## What 264 adds

Private `retained_recovery_payload` under one borrowed `Budget`:

- Closed BlobRef `load`: charge every reference edge including cache hits; check declared length **before** the store callback and against cached length; `reference_fields` requires exactly `{sha256,bytes}`.
- `Capture` trait takes the **same** budget. `RetainedCapture` loads the listed member BlobRef through that budget. `HostCapture` remains the 263 direct-path adapter (budget unused there). Inherited 263 oracles still run.
- Closed canonical recovery `PayloadMetadataClosureV1` via NodeRef; replacement DocRef must be in `rootChain`; manifest/auth/replacement via `Budget.load` then 260/261 crypto (`SignedDocument::capture` still cap → parse → copy).
- Signed↔retained joins: root order/cardinality, catalog/list/auth docs, per-slot sets/order, repair presence/typed absence, artifact observation set/order/hash. One Index, exactly one ninth-kind RA envelope, `select` every metadata body, bind selected pair **raw SHA + length**, retain all non-artifact members including policy/repair. Artifact `observedBytes` never recaptured (`artifact.bin` absent from retained members). Other-root pairs are unauthenticated pairing evidence.
- `prepare` is `budget.scope(|b| prepare_inner(...))`. Input store may be cleared after success; owned evidence remains.

Pair length and SHA both map to private `Error::DocumentEnvelope` (`pub(super)` inside a private module). Length is checked first, then SHA.

---

## Diagnostic names vs public coupling

265 isolates the new assertion with a **distinct private** Python reason. Native 264 reuses the existing private `DocumentEnvelope` for both SHA and length. Searched candidate schemas, architecture, command registry, and native `pub` API: **no** public refusal, schema, command, or envelope token was added. `retained-document-byte-binding` appears only in the helper, the integrator, and test reports that stringify `Refusal`. `DocumentEnvelope` appears only in `trust.rs` (enum + two returns). Command-metadata reports that string because the 256/258 harness records `str(e)`, not because a wire consumer binds it.

Retaining the old SHA reason for the length failure is **advisory**. No public/error-consumer coupling requires it. 265’s distinct private reason is test isolation, not a public token. Native tests match `success` / `Error`, not the Python string. Do not invent a public refusal from a private test reason.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **189/189** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 9 compiled r2 controls + baseline | **10/10**, SHA-equal frozen `mutation-check-r2` |
| Exact live | 265 9 length cases | core-equal frozen `length-check-r1/report.json` |
| Exact live | 265 command-metadata 47 | cases/counters/sourceSha equal frozen `command-check-r2` (18/67/26944) |
| Inspected | workspace-lengths-r2 | **486** crate tests + **2** doctests (488) |
| Inspected | 265 seven root r2 receipts | foundation 231; native 477; workflows 2193; security 580; carrier 479; integration 1787; envelope 168/147/1803 + 55 crypto + 6000 fuzz |
| Inspected | r1 eight controls + baseline | preserved; no length-omit control yet |
| Inspected | 263 Index oracles | synthetic **invalid** signatures; pairing only |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit length binding; omit full document binding; omit repair absence; omit artifact cardinality; omit retained order; omit extra-RA refusal; omit closure canonicality.

First fail **other** contract assertions (not exploit proofs):

- `omit-final-policy-capture`: counters on the positive `valid` case (13/39/18327 vs 14/40/18329).
- `omit-outer-operation-latch`: closed-budget assert (`edge(0)` Ok vs `Err(Closed)` on `bundle-old-bundle`).

---

## Independent probes

| Probe | Result |
|---|---|
| 261 `capture` in 264 `trust.rs` | still cap → parse → copy; no BlobRef `bytes` |
| 264 `Budget.load` | closed BlobRef; length before callback and on cache hit; mismatch `Error::Digest` then latch |
| 258 `_prepare` vs catalog envelope-length lie | still **admits** (265 `oldAccepted`) |
| 265 same lie | `retained-document-byte-binding`; follow-up `operation-budget-closed` |
| Public API | `retained_recovery_payload` / `Error` not `pub` |
| Store cleared after prepare | owned closure/pairs remain |

---

## Remaining (do not count closed)

Catalog/list/component body and quorum; complete current+incoming revocation union; policy/repair/artifact semantics; retained population / non-key subjects; held-root custody/ancestry/floors/S4/current compatibility; batch/whole-image/fence/slot/census/durability/writers; source/runtime selection; M3–M6. Host adapter must still enforce cap before allocation and establish custody. 264/265 are not installed runtime source.

---

## Verdict

- [x] Both archives/pins/members verified. 264: 371 product files, 367 unchanged vs 263. 265: one-line payload require + architecture note + seven pin inventories (r2 pin-only repair preserved).
- [x] Length join is on already-captured pairs; no extra I/O. 261 is not the declared-length owner; 264 `Budget.load` is.
- [x] 189 security tests, Clippy, fmt, r2 mutants, 9 length cases, and 47 command cases reproduced. Seven root r2 receipts inspected, not rerun.
- [x] Distinct 265 private reason vs native `DocumentEnvelope` is test isolation, not a public contract change.
- [ ] **Not** current authority, catalog/list body admission, native filesystem custody, or product installation.
