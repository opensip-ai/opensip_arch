# Independent review — native original-core inventory projection 318

**Standing:** bounded native-Rust review of frozen **final** `native-core-inventory-checkpoint-318`. Private unselected declared-core projection: 127-definition `CoreInventoryV2` shape, then existing catalog `metadata_versions::Version::parse` (reviewed 319 gate), then 229 tree/protocol/bootstrap/closure2 identity. It does **not** admit inventory signatures, executable custody, install/launch TCB, original authority, 320 scoped standing, or publication. Installed product remains `fa72e50`. Keys/fixtures are **TEST ONLY** / synthetic 229 declared hashes — never crypto evidence. 316, 317, 319, and 320 reports were not edited. 320 has been read; its owner disposition is **not** this freeze.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/mutant directories (including r1/r2/r3) were not overwritten. No workspace rerun. No CPU/RSS/actual-host qualification.

Initial **r1/r2** logs and mutation-check trees are historical (16 controls, no `omit-core-semver`, pre-319 oracle). They are **not** the candidate. Final evidence is security-r3 / Clippy-r3 / fmt13 / mutation-check-r3.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **13469748 B, 2168 members, SHA256 `83c4568426a1b26da84d61724be62a8c44bebc1b37690e2068a58aaafc938847`**, `allMembersRehashed: true`, **467** product pins. Standing: private unselected 318 declared core projection with strict 319 semantic guard; not signature/TCB authority or native publication. Extract rehashed **2168/2168**.

Nested live tars match pins: parent 316 `039392b9…a788` (11199928 B / 1522 / 465 product); 319 `96222a19…32b4` (2322720 B / 513). 319 wrapper `core_projection_reference319.py` SHA256 `2a406227…6b3c` is **byte-identical** to the reviewed 319 freeze.

Product vs 316: **464** unchanged, **1** changed (`trust.rs` private `include!("trust/core_inventory.rs")`, SHA256 `af3e70d5…cc40`), **2** added (`trust/core_inventory.rs` SHA256 `14499ca3…887c` 13322 B; `tests/fixtures/core-inventory318.ndjson` SHA256 `2d42bb5d…991d` 2129737 B). `captured_time_context.rs` remains `a2c29f73…c444`. `lib.rs` has **no** public export of this module.

Preserved unchanged: 319 REVIEW `19a4901d…bf5d` (5749 B); 316 REVIEW `1ef324da…d059` (7497 B); 317 REVIEW `0740164f…2943` (9806 B); 320 REVIEW `897115e6…f713` (16029 B).

---

## What `project` does (declared projection + 319 gate)

`pub(super) fn project(raw, platform)` is a pure function over already-supplied inventory bytes. No `Budget`, no filesystem read, no signatures.

1. `shapes::admit(Definition::CoreInventoryV2, raw)` — full 127 closed shape.
2. `metadata_versions::Version::parse(semanticVersion)` — existing catalog SemVer (267). Failure label **`core-semver`**. This is the 319 gate: after shape, before protocol/tree/platform/closure.
3. Sorted distinct `servedProtocolMajors` containing `protocolMajor`; sorted unique platforms containing the selected id; **every** declared platform tree.
4. Per tree: Unicode 15 NFC + casefold aliases; reserved `inventory.json` / `inventory.sig.json`; explicit directory parents; bounded symlink resolution and cycles; entrypoint is a file; unique file digests; exact layer coverage/order; overlap only `L-DIST`+`L-HOST` on the entrypoint; `requires` DAG.
5. Embedded bootstrap directory/frame paths and body/envelope digest+length must agree with **every** platform tree.
6. Selected descriptor: `kind: core`, raw inventory **BODY** hash as `manifestDigest`, selected file rows in path order (`length` → `bytes`), exact `semanticVersion`, declared primary protocol, selected platform. `closure2:` + `H("closure", descriptor)`.
7. Owns raw, parsed inventory, descriptor, identifier, and **all** platform file maps.

Directory/symlink/mode rows are omitted from the projected file array and remain identity-relevant only through the complete body hash. This matches 229 A.2 / `distribution_model.project_core` plus the 319 wrapper:

```
schema(CoreInventoryV2)
SEM.version(semanticVersion)    # Refusal core-semver
return original project_core(...)
```

Native uses the crate-local `Version::parse` rather than importing Python `SEM.version`. Independent replay of the frozen 125-row fixture through the **pinned 319 wrapper** (not native expected JSON as oracle): **125/125**, **0** mismatches, **53** positives / **72** refusals. Wrapper SHA `2a406227…6b3c`.

---

## Fixtures (final, 319 oracle)

`fixture-report.json`: **125** cases / **53** positive / fixtures SHA `2d42bb5d…991d`.

Original **103** raw inputs (label, platform, bytes) are **byte-identical** to `before-semver319/core-inventory318.ndjson`. Exactly **two** outcomes flipped from accepted to `core-semver`: `version-'1.0.0-01'` and `version-'1.0.0-alpha..x'`. **22** added `strict319-0..21` rows copy 319 `check-report.json` (10 positive / 4 new `core-semver` including `1.0.0+build..x` and the long leading-zero prerelease; remaining are already shape-invalid). Live `SEM.version` vs pinned 319 `strict` flags: **0** mismatches.

`all-platforms-required` changes **nonselected** `linux-aarch64-gnu` `bin/opensip` declared `length` 29→37 with the **same** digest. Selected `macos-aarch64` descriptor tree bytes stay 29. The case is **accepted**. Closure/manifestDigest change because the inventory **body** changed. That is declaration identity, **not** a physical file or content proof. Same-digest different declared length is allowed by this projector (digest uniqueness is hash-only). Documented; not a defect in this freeze.

Valid identities equal original 229 `project_core` on this corpus (319 already checked that for its 10 positives; 318 oracle inherits it).

---

## Reproduction

**Executed** on a review-local product copy (`grok-out/repro/product`), `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **255 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; `Finished` 10.84s; tests 12.20s |
| Ignored | 305 host observation pilot; 313 actual-host composition |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **13** includes (316’s twelve plus `core_inventory.rs`) | exit 0 |

Clippy-r1 rejected a nonminimal boolean in `logical()`. Final code uses the equivalent single negation of a disjunction (`CLIPPY-CORRECTION.md`; before-image `core-inventory-before-clippy.rs` retained). No accepted path-set change. No other test/compile correction.

**Seventeen compiled controls plus baseline** on **final** bytes, replayed into `grok-out/io/mutation-check-live-r3` (frozen `mutation-check-r3` not overwritten). Live `report.json` SHA256 **`4b96d375…365e`**, **byte-identical** to frozen r3. All **18** compiled; baseline exit 0; 17 mutants cargo 101 with `test result: FAILED`. **No compile-fail counted as a kill.** r1/r2 (16 controls, no `omit-core-semver`) were not substituted.

| Control | First frozen/live failure |
|---|---|
| `omit-core-semver` | **False acceptance** of `version-'1.0.0-01'` (`is_ok` true vs expected false) |
| `omit-protocol-membership-order` … `omit-tree-parent-type`, `omit-duplicate-file-digest`, `omit-layer-coverage-order`, `omit-layer-overlap`, `omit-shared-executable-layers`, `omit-bootstrap-tree`, `omit-path-nfc`, `omit-requires-cycle` | **False acceptance** of the named fixture |
| `omit-layer-order` | Still refuses `layer-duplicate`, **wrong stage** (`layer-overlap` vs `layer-order`) |
| `omit-bootstrap-frame` | Still refuses, **wrong stage** (`bootstrap-tree` vs `bootstrap-frame`) |
| `wrong-closure-domain` | **Wrong projected identity** on `baseline-macos` (`closure2:` domain `snapshot` vs `closure`) |

Matcher uniqueness 1 for each replace-target.

---

## Findings

### 1. 319 semantic gate is on the final bytes — hold

`Version::parse` runs immediately after full inventory shape and before protocol/tree. Omitting it is a compiled false-acceptance of catalog-invalid `1.0.0-01`. Original 229 schema-only projection (and 318 r1/r2) accepted that string; final 318 does not. Schema was not mutated. Label `core-semver` matches 319.

### 2. Parity with pinned 319 oracle — hold

125/125 independent Python replay. 53 positives include arbitrary-width numeric cores/prereleases that satisfy strict grammar, build metadata, and the 256-character schema cap case from 319. Closure strings match.

### 3. Bounded loops / Unicode / symlinks / layers / identity — hold on this corpus

NFC/fold aliases, parent-type, symlink cycle/bound, unique digests, layer coverage/order/overlap, requires DAG, bootstrap frame/tree, and `H("closure", …)` are guarded and mutant-caught. Large integers use `i128` from closed JSON integers (`2^63-1` protocol/file-length fixtures). 4 MiB overcap is shape/bytes, not RSS.

### 4. Private capability — hold

Module is `mod core_inventory` inside `trust.rs`, not `lib.rs`. `Projection` fields are `pub(super)` with no JSON constructor. No operational caller. No new operation `Budget`. Enclosing resolver accounting remains later work.

**Actionable defects in this freeze:** none that make the private projector self-contradictory with frozen 229 A.2 + reviewed 319 SEM on the pinned 125 cases.

Not claimed: inventory signatures, core TCB, physical tree contents, 222 unique/durable publication, 320 empty-event standing, source selection, or product installation.

---

## Remaining (do not count closed)

229 executable/signature/root/TCB, 312 embedded resolver, 317/320 scoped constructors (320 disposition separate), whole-operation Budget in a later resolver, custody/fence/census/capacity/final age/writers, M2–M6. No migration from uninstalled format.

---

## Verdicts

- [x] **318 as frozen final native projection:** archive verified; 319 gate present after 127 shape; 125/125 oracle; live 255/2 ignored; Clippy/fmt13; 17 compiled controls + baseline frozen-equal; r1/r2 not substituted; 320 not approved here.
- [ ] **Not** signature/TCB admission, physical core install, 320 standing, 318 public API, or product installation.
