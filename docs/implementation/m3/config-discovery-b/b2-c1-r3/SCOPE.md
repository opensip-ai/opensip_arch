# B2-c1 r3: the native unit instrument (M3-B unit B2-c, sub-unit B2-c1)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements section 2.1 of the accepted B2-c plan r2 (Codex `codex-b2c-plan-r2`; architecture `7c55cdab`).

**Oracle.** B2-c0, the current native unit reference: contract successor 166, Codex `codex-b2c0-reference-r2`.

**Base.** Product `b0154f0`: 166 contract successors, inventory v200.

## r3 changes (Codex `codex-b2c1-r2`, REQUIRED-FINDINGS)

**B2C1-R2-RF-1: r2's Python-`repr` formatter did not reproduce Python's escaping of non-printable Unicode.**

**The resolution, a lead decision.** A grammar refusal's internal key now names the field, the selector and the class, never the value's spelling: `NATIVE_UNIT_ROOT_REPRESENTATION:<at>:<selector>:grammar`.

**Why not reproduce `repr`.**
- **No stable target.** The reference's key spells the value with Python's `repr`. Its printability follows Python's own Unicode database, including unassigned code points, which changes between Python versions. No other implementation reproduces it stably, and a product key must not depend on a Python build.
- **Nothing public depends on it.** These are internal keys with no public detail (plan r2 section 2.3). The length form (`length=<n>:bounds=<low>..4096`) is unchanged and exact.

**How it is checked.**
- **The tool's normalization.** `error_key` normalizes a reference grammar key to the same form, and the normalization is part of the tool, so it is reviewed.
- **New vectors:** U+0085 and U+2028 after a `/`, a `.` segment, and a trailing `/`, each as a unit root and as a member root (8 steps). Accepted-root semantics are unchanged.
- **Mutation:** `grammar-key-spells-value`.

**Evidence.** Lane r4.

## r2 changes (Codex `codex-b2c1-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2C1-R1-RF-1:** the production entry permitted the standalone lane | **The production entries require `&AdmittedBoundaries`:** `discover_units`, `assign_membership` and `unit_scope_descriptor`. **`require_admitted_boundaries(Option<&AdmittedBoundaries>)`** is the authoritative composition's gate: a missing inventory refuses with the internal key `native.admitted-boundaries-required` (no public detail, plan r2 section 2.3). The `Option`-taking implementations are private. **The standalone lane** (`boundaries=None`, disclosing `source: none`) is the `standalone` module, compiled only under `cfg(test)`. A new test asserts the gate's refusal, that the module is `#[cfg(test)]`, and that no other crate-visible function of `discovery.rs` takes an optional inventory. **Mutation:** `standalone-not-test-only`. |
| **B2C1-R1-RF-2:** string bounds counted UTF-8 bytes | **Every schema-equivalent bound now counts characters:** root admission (`InternalUnitRootV1`, `CanonicalRelativeDirV1`), the scope descriptor's `Text`, and the scenario seam's V3 admission (paths, the selected root, custody reasons). **Root admission returns the reference's exact length keys:** `NATIVE_UNIT_ROOT_REPRESENTATION:<at>:<selector>:length=<n>:bounds=<low>..4096` (the grammar form is r3's). A scope `Text` violation is `schema-invalid`. **New vectors:**<br>• a 2049-character root (4098 UTF-8 bytes) admits in discovery, membership and scope, with a 4096-character exclusion prefix;<br>• a 4097-character prefix refuses `schema-invalid`;<br>• 4097-character unit and member roots refuse with the exact key.<br>**Mutation:** `bounds-count-bytes`. |
| **B2C1-R1-RF-3:** default selection did not admit its own rows | **The vocabulary loop runs over the defaulted rows** in canonical order, after the cardinality bound, as the reference's `admit_requested_capabilities` does: an unregistered capability, an unregistered mode, or a `NOT-SELECTED` cell refuses with the reference's key. **New vector:** a unit with `languageMode` `unknown-mode` refuses `native.requested-capability-mode-unregistered:calls:unknown-mode`. **Mutation:** `mode-vocabulary-dropped`. |
| **NBO-1** | `source.json` no longer carries the stale `contractSuccessorsUnchanged`. It records `publicApiAdded: true`: a Rust crate API, `opensip_security::discovery_export` and the test seam's `scenario::admitted_boundaries`, not a user-facing surface. |

**Evidence.** Lane r3. Lanes r1 and r2 were round 1's.

## What changes

| Path | Change |
| --- | --- |
| `crates/host/src/discovery.rs` | **New: the pure instrument** (U-0 to U-9 over V3; FW-01: no I/O, process, socket, write or environment read). Its functions:<br>• `discover_units`: markers, explicit roots and `Option<&AdmittedBoundaries>` in, `UnitDiscoveryV3` (or the reference's refused shape) out. It covers:<br>  – LD-B2C0-1, a marker whose derived anchor is at or below an admitted boundary withheld from the derivation;<br>  – the U-8 subset test over `(path, reason)`, with the admitted rows carried;<br>  – boundary and custody exclusions of marker directories;<br>  – exact explicit roots (grammar, crossing, without marker) with Cargo workspace members kept folded;<br>  – the 4096 directory cap;<br>  – U-1 kinds and modes, effective `allowJs` an input;<br>  – U-2 folding into the deepest surviving workspace unit;<br>  – U-9's one syntax-only fallback;<br>  – U-4b order and ordinals;<br>  – B-S1's member-consistency check.<br>• `assign_membership`: U-0 root admission, then rows decided first-match per U-4b item 4.<br>• `unit_scope_descriptor`: the foundation scope record, the bounds (1024 roots, 65536 prefixes) as `PROJECT.SCOPE_LIMIT`, `scopeDigest` as the raw SHA-256 of canonical bytes, and the boundary disclosure.<br>• `default_capability_selection`: every non-`NOT-SELECTED` matrix capability per unit, requested; release absences disclosed; the registry's admission keys; the ownership-tuple refusal; the 1024 requested-capability bound; zero units the internal `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT`.<br>• `public_detail`: the closed alias map (plan r2 section 2.3). |
| `crates/host/src/discovery_tests.rs` | **New.** Five tests:<br>• every recorded reference call replays byte for byte in canonical JSON, and a refusal by its internal key (135 steps);<br>• the alias map is exactly the registry's rows, and unknown keys refuse;<br>• the embedded matrix is the architecture's bytes;<br>• only a closed V3 record admits (a version-2 record, a foreign source, unsorted or duplicate members, malformed paths, custody reasons, counts, reasons, or an extra key all refuse);<br>• (r2) production composition cannot take the standalone lane. |
| `crates/host/src/discovery_vectors.json` | **New, generated** by `tools/host/discovery_unit_vectors.py` from the B2-c0 reference at its pinned bytes. It records:<br>• every instrument call of the 26 `units-*` cases (the `typescript_mode` step is C2's and recorded as skipped);<br>• the B2-c0 member, custody and depth controls;<br>• the cap sweeps (4095, 4096 and 4200 first-party, 4200 installed);<br>• the scope sweep (1024 and 1025 roots);<br>• the explicit-root grammar sweep;<br>• default selection over a fallback, a mixed repository, zero units, the cardinality bound and four registry cases;<br>• a deepest-unit membership case: nested units of one family, at every depth (lane r1).<br>It also pins the five architecture inputs and the registry alias rows. |
| `crates/host/src/native_capability_matrix.v2.json` | **New, a byte copy** of `docs/coop/design-corrections/native/native-capability-matrix.v2.json` (pinned by the vectors and a test). |
| `tools/host/discovery_unit_vectors.py` | **New:** the vector tool (`--check` / `--write`). |
| `crates/security/src/discovery_export.rs` | **New: the narrow public surface (LD-B2C-2).**<br>• **Mirror types** of the shared rule's crate-private ones: `PruneReason`, `PrunedAnchor`, `MarkerCountBasis`, `PrunedTreeRow`, `CustodyExcludedUnit`, `RootGrammar`, three constants.<br>• **Thin functions calling the rule:** `normalize_explicit_root`, `spell_root`, `classify_path`, `cargo_roots_from_markers`, `marker_pruned_trees` (the rule's `enumerate_units` over markers alone), `conventional_excluded_prefixes`.<br>• **`AdmittedBoundaries`,** the admitted V3 inventory: constructed in production only by security (`pub(crate) new`, for J1), with read accessors and `boundary_hit`, `is_boundary` and `excluded_prefixes` over the rule. |
| `crates/security/src/scenario.rs` | **Added: `admitted_boundaries(record)`,** the V3 shape admission of a JSON record, for the instrument's vectors. It lives in the existing test seam, which is compiled only under `scenario-fixtures` on macOS. So it adds no new test-feature `cfg` site to `crash_matrix_sites`' pinned list (lane r1 found that a gate in `discovery_export.rs` would). |
| `crates/security/src/lib.rs` | `pub mod discovery_export;` |
| `crates/host/src/lib.rs` | `mod discovery;` and `#[cfg(all(test, target_os = "macos"))] mod discovery_tests;` (the scenario seam is macOS-only) |
| `tools/tests/test_discovery_fw01.py` | FW-01 now covers `discovery.rs` and `discovery_export.rs`. The planned list is empty, and `discovery_tests.rs` is checked to be test scope. |

## Decisions recorded here

- **The rule's file is untouched (a lead decision).**
  - **The constraint.** The T2 census pins `custody/discovery_rule.rs` and `custody.rs` whole (`tools/security/discovery_census.py` CLOSURE). Changing either would make the census refuse, and the blind held-out receipt stale.
  - **The approach.** The export therefore lives in a new file, with mirror types and thin wrappers. The rule is still stated once and only called.
  - **Rejected:** making the rule's items `pub` in place.
- **Cargo `[workspace]` (LD-B2C-5).** The instrument takes `isCargoWorkspace` as an input, as the reference does. The composition (J1, over C1's bytes) reads it with the identity crate's existing public `parse_toml`, so no identity or host dependency change is needed.
- **Default selection and the analysis spec.** The defaulted rows are built from the matrix itself, so the vocabulary closes them. The instrument applies the pre-Plan boundary's cardinality bound (1024, `PROJECT.SCOPE_LIMIT`) and the ownership-tuple law, as the reference's `admit_analysis_spec` does for them. Full admission of an externally supplied spec (schema, vocabulary, parameter selection) is the Plan stage's, J1's.
- **No `membershipDigest` here.** The reference's `assign_membership` emits `UnitMembershipV1` without it. The digest belongs to the Plan stage that binds the record, so plan r2's mention of it under B2-c1 is corrected: it is not this unit's.
- **Refusals.**
  - The instrument decides with the reference's internal keys, and the refused shape carries the reference's `d9` rows.
  - `public_detail` normalizes a key at the host boundary through the alias map.
  - `native.admitted-boundaries-required` stays internal (plan r2 section 2.3). The type system makes the operational lane take an `AdmittedBoundaries`; `None` is the standalone lane.

## Checks

**Round 1's evidence was lane r2, round 2's lane r3, and round 3's is lane r4.** Lane r1 (kept in the work directory) failed two rows:
- **The security suite gained one failure,** `crash_matrix_sites::every_test_feature_site_is_on_the_pinned_list`. A `cfg(any(test, feature = "scenario-fixtures"))` gate in `discovery_export.rs` was a new test-feature site. The record constructor moved into the scenario seam, so no new site exists.
- **The deepest-unit mutation was not caught.** Its replacement text did not compile, and no vector held nested units of one family under a membership call. Both are fixed: the mutation is now `max_by` to `min_by`, and the vectors gain the case.

See `evidence/checks.json`. The rows are:
- the security and host suites at base and candidate, with equal failure sets;
- warning-denied all-targets Clippy on host and security;
- rustfmt on the edited files;
- the unit vectors `--check`;
- the host discovery tests;
- FW-01;
- the census `--check` (its closure is unchanged), the census and blind controls;
- the scan, upward and walk vector checks;
- the walker storage check, the environment pins and the configuration tables;
- the operability census, which passes after one lexical `from(` was removed;
- verify_design.

**Mutations.** Each must make the host discovery tests fail:
- member check dropped;
- LD-B2C0-1 filter dropped;
- U-9 dropped;
- `jsconfig` default `allowJs` flipped;
- an alias row altered;
- cardinality bound dropped;
- explicit-root workspace folding dropped;
- deepest-unit ranking inverted;
- (r2) the mode vocabulary dropped, bounds counting bytes, and the standalone lane not test-only;
- (r3) a grammar key spelling the value.

## Inventory

New paths, for inventory v201:
- `discovery.rs`, `discovery_tests.rs`, `discovery_vectors.json` and `native_capability_matrix.v2.json` in the host;
- `discovery_export.rs` in security;
- `tools/host/discovery_unit_vectors.py`.

## Not claimed

- No production caller (J1).
- No snapshot inventory (C1).
- No effective-`allowJs` reader (B2-c2, after M3-B r8).
- No recognition (B2-d).
- No D15 readers (B3-b).
- No qualification.

B2-c and B2-b are not complete.
