# B2-d2 r2: host-side framework recognition (M3-B unit B2-d, sub-unit B2-d2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.**

## r2 changes (Codex `codex-b2d2-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2D2-R1-RF-1:** bytes for every present evidence file | `recognize` checks first, before any recognizer or override, that every one of the fifteen `EVIDENCE_FILES` among the member paths has its bytes. Otherwise it gives `MissingEvidenceBytes`, naming the first missing file in `EVIDENCE_FILES` order. Other member content stays optional. `every_present_evidence_file_needs_its_bytes` covers each of the fifteen names alone (with and without an override), the unselected lower-priority files (`jsconfig.json` beside `tsconfig.json`, `next.config.ts` beside `next.config.js`, `vite.config.mjs` beside `vite.config.ts`, and `jest.config.js` without a `package.json`) under an explicit override, and optional non-evidence content. Mutant: `evidence-preflight-dropped`. |
| **RF-2:** real schema admission | `unit_recognition` now takes the host's `RegisteredSchemas` and admits the whole canonical row against the bound schema's `/$defs/UnitRecognitionV1` (`schema(...).admit_json`, as `configuration.rs` admits its semantic record) before reading it as the generated type. The identity computation is unchanged. `a_row_outside_the_schema_is_refused` covers `schemaVersion` 2, `recognizerVersion` 2, empty evidence, a duplicate result, an absolute entry path, 17 unresolved choices, an unknown state, and the roots `..`, `/abs` and `a/../b`. Every reference row is admitted. Round 1's claim that deserializing into the generated type was admission is withdrawn. Mutant: `schema-admission-dropped`. |
| **RF-3:** the TOML profile and recursion controls | The vectors gain `tomlProfile`: usable `[workspace]` and `[package]` tables beside unrelated fields at exactly 4 MiB and one past, and at exactly 1,000,000 nodes and one past. These are reference-equal, including `recognitionId` and the Cargo-workspace fact. There are also two **product-only** recursion cases (128 nested arrays, 100 dotted keys), whose expectation is stated in the tool: `Cargo.toml-not-toml`, no Cargo entry, `partial`, fact unknown. The reference's differing result is recorded beside each, never as the expectation. A 16-deep admitted control is reference-equal. `the_toml_profile_controls_hold_and_the_recursion_divergence_is_product_only` replays them. |

It implements B2-d2 of the B2-d plan r3, sections 3 and 4 (`../b2-d/PLAN-r3.md`; Codex `codex-b2d-plan-r3`), against the bound B2-d0 reference (contract successor 171; Codex `codex-b2d0-reference-r4`). It uses B2-d1's YAML subset reader (Codex `codex-b2d1-r1`).

**Base:** product main `86cf864` (B2-d1 and inventory v210; 171 contract successors); architecture `f8576e5c`. Round 1 is `../b2-d2-r1/`.

## What it delivers

### `crates/host/src/framework_recognition.rs` (new)

Pure, first-party and library only. J1 composes it with C1's snapshot custody, and C4 commits its rows.

**`recognize(&RecognitionInputs) -> Result<FrameworkRecognitionV1 value, RecognitionError>`** recognizes one `rust` or `tsjs` unit. Its inputs are:
- the unit's member paths, unit-root-relative;
- the bytes of each of the fifteen `EVIDENCE_FILES` present;
- the resolved explicit entry points: `None` when the resolved configuration has no `discovery.entryPoints` field, otherwise the list a carrier won, `[]` included.

It is the reference rule for rule:
- **`node-package`, `npm-workspaces`, `vitest-jest` and the FR-3 hints** come from `package.json` read by exact JSON admission (`parse_json`).
  - A refusal (floats, duplicate keys, non-UTF-8) gives the `package.json-not-strict-json` disclosure.
  - An admitted non-object gives nothing.
  - The jest and vitest configs are taken in the model's order and hashed, never parsed.
  - Hints come from `dependencies`, `devDependencies` and `peerDependencies`, in the model's eleven names, sorted and distinct.
- **`typescript-config`:** the first of `tsconfig.json` and `jsconfig.json`, checked by item 14a's JSONC reader (`jsonc::parse`) within 64 KiB (`MAX_CONFIG_FILE_BYTES`). Otherwise it is `inferred`, with `tsconfig-not-jsonc`.
- **`pnpm-workspace`:** checked by B2-d1's `parse_pnpm_packages`; outside the subset it gives `config-requires-evaluation`.
- **`cargo-workspace` and `cargo-package`:** decided on `parse_toml`'s parsed `workspace` and `package` tables, inline tables included. Every parse error gives the `Cargo.toml-not-toml` disclosure.
- **`nextjs`:** routes are selected by the model's prefix and suffix rule. **`vite`:** `index.html` when present. Both configs are hashed, never parsed, and carry `config-requires-evaluation`.
- **The ordering and FR-4 bounds:**
  - results are sorted by recognizer id;
  - `structural_bounds` checks at most 32 results and 1 to 64 evidence files each;
  - `entry_bound` applies the per-unit bound, all or nothing over the distinct union of 65,536 entries, under an explicit override too.
- **FR-2 and FR-1:** an explicit list gives `{all, explicit}`. Otherwise the state is `partial` on any unresolved choice, `all` with entries, and `none` with neither.

Every evidence `contentSha256` is the SHA-256 of the file's bytes.

**The other functions:**
- **`unit_recognition(schemas, ...)`** builds the `UnitRecognitionV1` row. Its `recognitionId` is `sha256:` plus the hex of `hash_canonical_value("native.framework-recognition.v1", recognition)`, as `closure.rs` checks it. The whole row is then admitted by the bound schema's `/$defs/UnitRecognitionV1` before being read as the generated `RecognitionPlan1UnitRecognitionV1`. A row that does not admit is `Shape`.
- **`cargo_workspace_fact`** gives `MarkerFact.is_cargo_workspace` from the same parse: `None` on a parse error, which B2-c's instrument reads as "not a workspace".
- **`discovered_provenance`** renders `DISCOVERED:<recognizerId>@<version>`.

### The vectors (`tools/host/framework_recognition_vectors.py` → `crates/host/src/framework_recognition_vectors.json`, new)

They are generated from the bound B2-d0 reference, pinned by bytes and loaded with the selected model:
- **49 unit cases:** each recognizer and its configuration-requiring, parse-failure or negative case.
  - The parsers' edges: non-UTF-8, a float, a duplicate key and a non-object `package.json`; JSONC comments, empty, at 64 KiB and one past; the YAML subset in and out; Cargo inline tables, a non-table key, a header inside a string, `[workspace.dependencies]` alone, a BOM, a 5,000-digit integer, `1e9999`.
  - Also: the hints in all three dependency fields; the route selection, including `app/xpage.tsx` and non-route files; the config orders; a mixed unit at root `apps/web`; a canary fixture; and the explicit override.
- **12 bound cases:** 65,536 and 65,537 entries, split across `nextjs` and `vite` and alone in `nextjs`, each with no override, explicit `[]` and an explicit list. This includes the explicit-non-empty single-result case that B2D0REF-R3-NBO-1 and R4-NBO-1 carried here. They are described by parameters, with the expected `recognitionId`, entry state, unresolved choices and entry counts.
- **7 TOML profile cases (r2):** byte and node bounds and one past, reference-equal; two product-only recursion cases; one admitted nesting.
- **7 Cargo-workspace facts and 3 provenance renderings.**

### `crates/host/src/framework_recognition_tests.rs` (new)

Nine tests (r2 adds the last three):
- **unit vectors:** every one equals the reference's recognition, every row's `recognitionId` matches, and no canary path appears;
- **bound vectors:** every one matches;
- **facts and provenance:** they match;
- **missing bytes:** a present evidence file without bytes is refused;
- **structural bounds:** they hold at 32 and 64 and refuse at 33, 0 and 65, called directly;
- **the entry bound:** it counts the distinct union, keeping 65,536 entries that overlap across results and dropping all of them one past;
- **the TOML profile:** at and past the byte and node bounds, with the recursion divergence product-only;
- **every present evidence file needs its bytes;**
- **a row outside the schema is refused.**

### `crates/host/src/lib.rs`

One dead-code-allowed library module declaration, plus its test module.

### FW-01 (`tools/tests/test_discovery_fw01.py`)

`framework_recognition.rs` joins `COVERED` and `PURE`, and its tests are asserted outside production. Item 15's canary control is the vector `canary-configs`:
- `build.rs`, a `postinstall` script, `.cargo/config.toml` with `build.rustc-wrapper`, `.npmrc` and `pnpmfile.cjs`;
- `next.config.js`, `vite.config.ts` and `jest.config.js`, each naming a canary path.

They are hashed or ignored. No canary path appears in the recognition, and the reader is pure, so it opens no path.

## Checks

Lane r2, `evidence/b2d2-checks-r2/`. Attempt 1 (`b2d2-checks-r2-attempt1/`) failed only Clippy's `collapsible_if`, in the schema-mutant test, which is now a let-chain. Every other row of attempt 1 passed, and its twelve mutations were caught. The second attempt is the lane of record:
- **the host suite** at base and candidate, with equal failure sets (8 at base) and nine new tests;
- **rustfmt** and warning-denied all-targets Clippy on host;
- **the recognition tests,** and the recognition and YAML vector `--check`s against the bound reference;
- **FW-01,** environment exceptions, the operability source census and verify_design;
- **twelve mutations,** each failing the recognition tests:
  - the state rule reverted;
  - the entry bound per result, or skipped under an override;
  - explicit `[]` read as absent;
  - any `workspace` value counted as a table;
  - the tsconfig bound dropped;
  - the pnpm subset unchecked;
  - the jest config disclosure dropped;
  - the hints unfiltered;
  - evidence hashed over the path;
  - (r2) the evidence preflight dropped;
  - (r2) the schema admission dropped.

## Not claimed

- **No caller:** J1 composes the recognizers with C1's snapshot custody.
- **No Plan commitment:** C4 builds `FrameworkRecognitionPlanV1` with its `snapshotId`, `membershipDigest` and `explicitEntryPoints`.
- **No recommendation evidence** (B2-d3).
- **No FR-6 to FR-8.**
- **No qualification.**
- **No completion** of B2-d, B2 or M3-B.

## Inventory

New paths for the inventory after acceptance:
- `crates/host/src/framework_recognition.rs`;
- `crates/host/src/framework_recognition_tests.rs`;
- `crates/host/src/framework_recognition_vectors.json`;
- `tools/host/framework_recognition_vectors.py`.
