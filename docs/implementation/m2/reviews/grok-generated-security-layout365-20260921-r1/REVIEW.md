# Independent review — generated security source layout 365

**Standing:** bounded **generated-source layout** of frozen `generated-security-layout-checkpoint-365`. Three schema files move byte-for-byte into `crates/security/src/generated/`; two Unicode tables split out of handwritten wrappers; `tools/generate_security_tables.py` is a stdlib-only offline `--check`/`--write` driver. This is **not** inventory/runtime/source selection, five-member `StoreGenerationBindingV1`, current authority, writers, or product installation. Product remains `fa72e50`. Selected inventory remains **v32**. Inventory **v53** (633 planned paths; 470 inherited + 163 new; unselected 33–52 preserved; scratch 33 never overwrote v32) is **outside** this verdict. 365 README’s inventory33 draft is author prose, not this review’s acceptance.

Prior 364 REVIEW `d93e0f3f…4f37` (6713 B), ADDENDUM `39e812a1…5eac` (2104 B), and CORRECTION-REVIEW `0a65bc79…b1d7` (2288 B) were read and are **unchanged**. Frozen 364-r2 **240 / 764572 B / `349697ec6f7f8a8909ef51c6765bade1d15b66facdaf3d17a8663b5d5e565c17`** is metadata-only (README 80 Rust / 133 fixtures; machine JSON always 213/133/80). 362 REVIEW `168809c4…dff1` and SOURCE-NOTE `772694b0…0cb8` unchanged.

Python 3.12.13 `-I -B` (`source-audit364-env`). rustc/cargo/rustfmt **1.95.0** (`rustfmt 1.9.0`). Isolated `grok-out/`; freeze workdir **not** overwritten (freeze `generator-check-r2/report.json` still `44cb6a45…8edc` / 102102 B). **No** root/other processes were signalled.

---

## Verification

Archive-pin and every `subject.json` member matched **before** extract. Frozen archive: **6959576 B, 585 members, SHA256 `99312716fc0d05d8024dcdf3f1adc67b73a665cf638a47bd21f55c56a0a32792`**. Standing: “Private365 generated source layout; no source/runtime selection”. Parent 363 rehashed before extract: **574 / 6895004 B / `b07f1a6d…e3ad` / 508 product pins**. Extract rehash: 0 mismatches; **519** product files.

Vs 363:

| Class | Count |
|---|---|
| Unchanged | **500** |
| Byte-identical physical moves | **3** |
| Wrapper `#[path]` / table-split changes | **5** |
| Added (2 Unicode tables + 9 tools/inputs) | **11** |
| Leftover old paths | **0** (the 3 old paths exist only as the moves) |

Moves (SHA/bytes equal 363 and 364 regen):

| New path | SHA256 / bytes |
|---|---|
| `generated/component_manifest_shape.rs` | `efb068ac…70d8` / 23210 |
| `generated/trust_record_shape_nodes.rs` | `8446f0f8…10d3` / 203595 |
| `generated/trust_record_visit_nodes.rs` | `43836933…2249` / 140150 |

Added tables: `generated/metadata_unicode15_tables.rs` `5a7f97fd…09bb` / 16086 (707 `UNASSIGNED` ranges); `generated/metadata_casefold15_tables.rs` `63a8fa7a…6ffa` / 40065 (1530 `TABLE` rows). `Cargo.lock`, `crates/security/Cargo.toml`, `lib.rs` module list, fixtures, and public API are in the 500 unchanged. Wrappers keep the same inner module names (`generated` / `nodes` / `visit` / `tables`); only `#[path]` gains a `generated/` prefix. Visibility stays `pub(super)` / `pub(in super::super)`.

---

## Generator (this review reproduced)

Input pins matched `sources.json` **before** generation (manifest `a5140714…90af`; trust-record schema `a0431300…7928`; registry `bf219954…9216`; casefold JSON `b4a7fe49…998e`; UnicodeData.txt `806e9aed…6a73`). Formatter string **`rustfmt 1.9.0`** matches `/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt --version`. Driver is stdlib-only (no `unicodedata`, `jsonschema`, network, or Cargo hook). Helpers run `-I -B` in a tempfile; `--check` does not write the repository.

`record_visits.py` loads frozen **136**-site / **29**-root `reference-registry.json` (schema SHA `a0431300…7928`) via `SimpleNamespace`; it does **not** import the reference canonicalizer or jsonschema. `assert len(bindings)==136`. Manifest/record-shape helpers keep 268/313 algorithms with path adapters only.

Live `--check` (Python 3.12.13, not the author’s 3.14): exit 0, “Verified five security tables from pinned local inputs.” Three schema outputs byte-equal 363. Unicode **table bodies** byte-equal the old inline 363 tables; both original `#[cfg(test)]` modules byte-equal 363. Frozen `initial-unicode-wrappers/` have **no** `#[cfg(test)]` (1617 / 575 B) — the first extractor dropped trailing Unicode tests; both modules were restored before the author’s final 388. Initial `cargo check` / Clippy are **not** this review’s final.

One-off **14** probes in `grok-out/generator-check-r2` (product 519 restored; shadow removed; freeze probe dir not written):

| Probe | Exit | Writes |
|---|---|---|
| baseline `--check` | 0 | none |
| bad-input-0..4 `--check` | 1 each, `input pin mismatch` | none |
| bad-input-write-0..4 `--write` | 1 each, same pin mismatch | none |
| changed-output `--check` | 1, `generated outputs differ: trust_record_visit_nodes.rs` | none |
| explicit-repair `--write` | 0, restores bytes | write |
| restored-baseline `--check` | 0 | none |

`--check` and failed `--write` publish nothing. Invalid input fails before output publication in both modes.

---

## Live cargo / format (exact checks rerun)

`rustfmt --check --edition 2024` of **65** security `.rs` files: exit 0.

Workspace Clippy `--offline --locked --all-targets -- -D warnings`: exit 0 (22.25s). Compile-only; not a native suite.

Frozen author `security-final-r1.command.json` argv is `cargo test --offline --locked -p opensip-security` with **no** `RUST_TEST_THREADS` field. Root states the author suite used `RUST_TEST_THREADS=1`. That contract is **not** in the frozen argv. Default-parallel execution is fragile for native custody tests; this is a **harness/integration** issue, not a reason to drop or weaken those tests.

Independent cargo (isolated `CARGO_TARGET_DIR`; freeze not overwritten). Failed runs **preserved**:

| Run | Env | Result | Observed reason |
|---|---|---|---|
| **r1** | default parallel; `TMPDIR` unset | **381 passed / 7 failed / 2 ignored** (47.37s). stdout SHA `47996934…a0b3` | 5× `Descriptor(ChangedDuringRead)` unwraps; count shortfalls **0 vs 1** and **0 vs 15**. Exact mutator **not** established. **Not a pass.** |
| **r2** | `RUST_TEST_THREADS=1`; `TMPDIR` under `/tmp/opensip-implementation`; overlapped root 366 in time | **309 / 79 / 2** (115.07s). SHA `a31c34cb…2c56` | `Predicate { component: 2, refusal: OthersWrite }` (44 Root / 23 Source / 8 Custody). **0** `ChangedDuringRead`. Cross-suite overlap **does not** establish an exact mutator. **Not a pass.** |
| **r3** | `RUST_TEST_THREADS=1` after `native-review-clear366.json`; `TMPDIR` still under `/tmp/…/tmp-native-r3` | **309 / 79 / 2** (110.73s). SHA `07231121…9e1b` | Same `OthersWrite` ancestor refusal while 366 was **not** running. `/tmp` is others-writable; custody correctly refused. **Not a 365 layout defect and not a pass.** |
| **r4** | `RUST_TEST_THREADS=1`; `TMPDIR` unset (default user temp); after clear366 | **388 passed; 0 failed; 2 ignored** (226.21s); **4** compile-fail doctests ok (0.12s). SHA `037decd3…2e7f` | Isolated serial validation used for this verdict. |

Generated-owner tests (`metadata_unicode15`, `metadata_casefold15`, manifest schema oracle, record shapes, record reader) passed in r1 and r4. Custody checks were **not** weakened. r2/r3 `OthersWrite` is the product enforcing ancestor policy, not a waiver. Initial lint is not counted as final.

---

## Findings

365 is a physical layout + offline generator for already-reviewed 363/364 bytes. Module ancestry, public API, dependencies, and fixtures do not change. Unicode tests that the first extractor dropped are present on the frozen final source and match 363.

**Actionable 365 source defect:** none that make the five generated outputs, `--check` no-write contract, 136/29 registry load, or wrapper `#[path]` moves self-contradictory with r4 388+4, Clippy, rustfmt 65, and the 14 probes.

**Harness:** frozen argv omits the serial-thread contract; default-parallel r1 is real failed evidence (`ChangedDuringRead` / count shortfalls). Review `TMPDIR` under `/tmp` is others-writable and is refused (r2/r3). Do not treat r1–r3 as passes. Do not invent a mutator from 366 overlap.

**Must not be counted closed:** inventory v53 / selected v32; five-member store binding; current authority; writers; release; M2–M6; `trust.rs` decomposition.

---

## Remaining (do not count closed)

Selected inventory still 32. Inventory 53 is a separate cumulative proposal. Native authority / source / runtime selection. TCB/history/original T. Live qualified current/census.

---

## Verdicts

- [x] **365 as frozen generated-source layout:** 585-member archive verified; 500/3/5/11 vs 363; five outputs `--check` against pinned inputs; schema files byte-equal 363; Unicode table bodies and both test modules preserved; 14 probes; rustfmt 65; Clippy `-D warnings`; serial r4 **388 + 4 doctests**. Private/uninstalled.
- [ ] **Not** inventory/runtime/source selection, selected-I/current authority, writers, 364-r2 source change (metadata only), or product installation.
