# Independent review — native original-core anchor byte bindings 322

**Standing:** bounded native-Rust review of frozen `native-core-anchor-checkpoint-322`. Private unselected resolver: closed RootAdmission `NodeRef` before I/O, `kind: anchor`, six initial object blobs and full embedded root pairs on **one** enclosing `Budget`, 318 inventory projection with 319 SemVer, 229 product-canonical envelope subject/domain/preimage (not signed-metadata authenticity). It does **not** admit signatures, revocation contexts, executable/CATLIST bodies unused here, install/launch TCB, current core, 321 current-S45 standing, or publication. Installed product remains `fa72e50`. Synthetic signatures are **TEST ONLY**, never crypto evidence.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/mutant directories were not overwritten. No workspace rerun. No CPU/RSS/host qualification.

321 has been fully read: option A holds only for current S4.5, with child-census time scoping, current-event shell checks, operation-ref stop, and physical qualification still open. **This review does not close those gaps.**

318 is reused only as the bounded inventory projector (`core_inventory.rs` SHA256 `14499ca3…887c`, byte-identical). It is not original-core TCB here.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **13499412 B, 2063 members, SHA256 `2a1f6ab783085363663f42c34ab46bc621fa0279dc20987ede0bd22411eccb51`**, `allMembersRehashed: true`, **469** product pins. Standing: private unselected 322 complete embedded byte resolution; no signature/TCB authority or native publication. Extract rehashed **2063/2063**.

Nested parent 318 live tar SHA match `83c45684…8847` (13469748 B / 2168 / 467 product). 319 wrapper `core_projection_reference319.py` SHA256 `2a406227…6b3c` byte-identical to reviewed 319. 312 `time_provenance_reference312.py` SHA256 `713ec94c…a9f2` (verified-core319 copy equals `reference312/`). Frozen 229/312 files were **not** edited; the fixture primary wraps `M.project_core` in an isolated imported module.

Product vs 318: **466** unchanged, **1** changed (`trust.rs` private `include!("trust/core_anchor.rs")`, SHA256 `5d4d1287…95ae`), **2** added (`trust/core_anchor.rs` SHA256 `d9fd86d4…1380` 19245 B; `tests/fixtures/core-anchor322.ndjson` SHA256 `c5a669d9…b816` 5275088 B). `lib.rs` has **no** public export of this module.

Preserved unchanged: 318 REVIEW `7748038b…77be`; 321 REVIEW `537a71e7…54ea`; 319 REVIEW `19a4901d…bf5d`; 320 REVIEW `897115e6…f713`.

---

## What `capture` does (byte bindings, not TCB)

`pub(super) fn capture(budget, anchor_ref, store)` is `budget.scope`:

1. Canonicalize and `Shapes::admit(NodeRef)` **before I/O**.
2. Load Records; `Record::parse(RootAdmissionNodeV1)`; require `kind: anchor`.
3. Load six initial object blobs (inventory body/envelope, then after projection bootstrap manifest pair, then index-zero root pair) on the **same** Budget.
4. Product-canonical raw-byte condition (`canonical_bytes == raw`) plus envelope `kind`/`domain`/`storedSha256`/`preimageSha256` (`envelope-subject`). Not the complete signed-metadata consumer.
5. `Core::project` (318 + 319 `Version::parse`) on inventory body; join `coreClosure`.
6. Bootstrap frame hashes/lengths vs inventory `embeddedBootstrap`; ALL declared member tree hashes on **every** platform (`bootstrap-member-tree`).
7. Index-zero body membership; unique listed envelope for the anchor envelope; body/envelope digest+**length** vs **every** platform tree (`anchor-tree-length`).
8. Root document policy `admit(..., [true, true])` then envelope domain `opensip.metadata.root.{schema}`; `RootBinding` equality. No wall expiry.
9. `Index::with_context` (existing 281/263 adapter): file lengths from the **selected** inventory tree; reads **all** listed envelope candidates; every `rootChain` path selected unambiguously; index-zero pair equals `node.root`; adjacent `previousRootVersion` / +1 version / nondecreasing `issuedAt` → **final** declared head (not index zero).

`CapturedCore` owns anchor record/ref, inventory projection, three initial raw pairs, **all** captured listed member bytes (including unused envelopes), selected root pairs, chain, and final binding. Tests inspect after store/Budget/fixture drop.

Catalog/list **BODY** and executable bytes are not loaded when unused; their **declared** tree membership is still checked (`unused-cache-bodies-absent` is a positive). Later ordinary payload/time/auth consumers must load their own evidence.

No new Budget inside the function. Repeat capture charges edges again without store recapture.

---

## Primary oracle (independent)

Frozen 83-row fixture uses pinned 312 `embedded_bytes` plus isolated 319 `SEM.version` around original `project_core`, plus NodeRef preflight. Independent replay of **frozen ndjson** through that primary (extract-local copies, frozen modules not edited): **83/83**, **0** mismatches, **10** first-round / **7** second-round positives. Baseline **9 objects / 17 edges / 22691 B**, repeat **9 / 34 / 22691**. Live `SEM`/counters/trace/`coreClosure`/`rootChain`/`finalBinding`/`anchorRaw`/`captures`/`failed` equal fixture expected.

Synthetic signatures never counted as crypto.

---

## Reproduction

Author corrections (before-images retained; compile failures are **not** mutation kills):

- security-r1: `parse_carrier` qualifier + `timestamp_seconds` `Result` (grammar refusal as `root-document-policy` before compare).
- Fixture-extension `verifiedInstallRoot` non-NFC setup: corrected to schema-refusal without minting a valid closure; no native verdict rewritten to match.
- Clippy-r1 `type_complexity`: local `RawPair` alias only. Final bytes are the alias version.

**Executed** on a review-local product copy (`grok-out/repro/product`), `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **256 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; `Finished` 10.76s; tests 12.22s |
| Ignored | 305 host observation; 313 actual-host composition |
| Workspace Clippy `--all-targets -D warnings` | exit 0 (Clippy-r2 equivalent) |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **14** includes (318’s thirteen plus `core_anchor.rs`) | exit 0 |

**Sixteen compiled controls plus baseline** replayed into `grok-out/io/mutation-check-live-r1` (frozen `mutation-check-r1` not overwritten). Live `report.json` SHA256 **`b3077f43…8c7b`**, **byte-identical** to frozen r1. All **17** compiled; baseline exit 0; 16 mutants cargo 101 with `test result: FAILED`. **No compile-fail counted as a kill.**

| Control | First failure |
|---|---|
| `omit-envelope-subject`, `omit-core-closure`, `omit-bootstrap-member-tree`, `omit-root-binding`, `omit-embedded-chain-gap`, `omit-embedded-chain-backdated` | **False acceptance** |
| `omit-bootstrap-reference`, `omit-anchor-tree-length`, `discard-shared-budget`, `suppress-failure-latch`, `omit-reference-preflight` | Still refuse, **wrong stage/counters** |
| `omit-anchor-index-zero` | Still refuse, **wrong binding stage** (`anchor-tree-length` vs `anchor-index-zero`) |
| `omit-anchor-envelope-membership` | **Panic** (`index out of bounds` on `matching[0]`); guard was required for indexing — **not** false acceptance |
| `wrong-anchor-collection` | **Wrong refusal** of a good case (`Budget(Capture)`) |
| `wrong-final-head` | **Wrong projected identity** (index-zero binding vs final head v4) |
| `discard-unused-envelopes` | **Ownership** (`members` len 4 vs 5) |

Matcher uniqueness 1 for each replace-target. No kernel / Index / body-codec production change.

---

## Findings

### 1. Parity with pinned 312+319 primary — hold

83/83 independent Python replay; live native 256 includes the 83-row test. Closure `closure2:54322a2c…118d` matches 318 baseline macos identity. Final head is the **last** declared pair, not index zero.

### 2. Budget, retention, NodeRef-before-I/O — hold

Shared Budget; repeat 9/34/22691 without recapture; latch covered; unused listed envelopes owned after drop; catalog/list bodies unused are not read. NodeRef shape before Records load.

### 3. Explicit limitation — hold as requested

This is **byte-binding**. Envelope preimage/domain/stored digest is not quorum. `admit([true, true])` is root-document policy, not TCB. No wall expiry, no current-core substitution, no 321 census/standing.

**Actionable defects in this freeze:** none that make the private resolver self-contradictory with frozen 312 `embedded_bytes` + reviewed 319 SEM on the pinned 83 cases. The envelope-membership mutant panics rather than returning `Binding`; production still has the uniqueness `need` before indexing.

Not claimed: signatures, revocation, executable custody, 321 option A constructor, physical fence/census, or product installation.

---

## Remaining (do not count closed)

321 child-census time scoping, current-event shell checks, operation-ref stop, physical qualification. 229 executable/signature/root TCB beyond this byte binding. 312 embedded resolver is composed here as **bytes**, not historical time. Whole-workspace/host. M2–M6.

---

## Verdicts

- [x] **322 as frozen native byte resolver:** archive verified; 318 inventory reused; 319 gate isolated on original `project_core`; 83/83 primary; live 256/2 ignored; Clippy/fmt14; 16 compiled controls + baseline frozen-equal; r1 compile/clippy/fixture-setup corrections preserved and not counted as kills.
- [ ] **Not** signature/TCB admission, 321 standing, public API, or product installation. 321 gaps remain open.
