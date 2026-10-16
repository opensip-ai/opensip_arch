# B2-d2 r1: host-side framework recognition (M3-B unit B2-d, sub-unit B2-d2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements B2-d2 of the B2-d plan r3, sections 3 and 4 (`../b2-d/PLAN-r3.md`; Codex `codex-b2d-plan-r3`), against the bound B2-d0 reference (contract successor 171; Codex `codex-b2d0-reference-r4`). It uses B2-d1's YAML subset reader (Codex `codex-b2d1-r1`).

**Base:** product main `86cf864` (B2-d1 and inventory v210; 171 contract successors); architecture `f8576e5c`.

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
- **`unit_recognition`** builds the `UnitRecognitionV1` row. Its `recognitionId` is `sha256:` plus the hex of `hash_canonical_value("native.framework-recognition.v1", recognition)`, as `closure.rs` checks it. The whole row is admitted by the generated `RecognitionPlan1UnitRecognitionV1` through its canonical bytes, so a row that does not admit is an error.
- **`cargo_workspace_fact`** gives `MarkerFact.is_cargo_workspace` from the same parse: `None` on a parse error, which B2-c's instrument reads as "not a workspace".
- **`discovered_provenance`** renders `DISCOVERED:<recognizerId>@<version>`.

### The vectors (`tools/host/framework_recognition_vectors.py` → `crates/host/src/framework_recognition_vectors.json`, new)

They are generated from the bound B2-d0 reference, pinned by bytes and loaded with the selected model:
- **49 unit cases:** each recognizer and its configuration-requiring, parse-failure or negative case.
  - The parsers' edges: non-UTF-8, a float, a duplicate key and a non-object `package.json`; JSONC comments, empty, at 64 KiB and one past; the YAML subset in and out; Cargo inline tables, a non-table key, a header inside a string, `[workspace.dependencies]` alone, a BOM, a 5,000-digit integer, `1e9999`.
  - Also: the hints in all three dependency fields; the route selection, including `app/xpage.tsx` and non-route files; the config orders; a mixed unit at root `apps/web`; a canary fixture; and the explicit override.
- **12 bound cases:** 65,536 and 65,537 entries, split across `nextjs` and `vite` and alone in `nextjs`, each with no override, explicit `[]` and an explicit list. This includes the explicit-non-empty single-result case that B2D0REF-R3-NBO-1 and R4-NBO-1 carried here. They are described by parameters, with the expected `recognitionId`, entry state, unresolved choices and entry counts.
- **7 Cargo-workspace facts and 3 provenance renderings.**

### `crates/host/src/framework_recognition_tests.rs` (new)

Six tests:
- **unit vectors:** every one equals the reference's recognition, every row's `recognitionId` matches, and no canary path appears;
- **bound vectors:** every one matches;
- **facts and provenance:** they match;
- **missing bytes:** a present evidence file without bytes is refused;
- **structural bounds:** they hold at 32 and 64 and refuse at 33, 0 and 65, called directly;
- **the entry bound:** it counts the distinct union, keeping 65,536 entries that overlap across results and dropping all of them one past.

### `crates/host/src/lib.rs`

One dead-code-allowed library module declaration, plus its test module.

### FW-01 (`tools/tests/test_discovery_fw01.py`)

`framework_recognition.rs` joins `COVERED` and `PURE`, and its tests are asserted outside production. Item 15's canary control is the vector `canary-configs`:
- `build.rs`, a `postinstall` script, `.cargo/config.toml` with `build.rustc-wrapper`, `.npmrc` and `pnpmfile.cjs`;
- `next.config.js`, `vite.config.ts` and `jest.config.js`, each naming a canary path.

They are hashed or ignored. No canary path appears in the recognition, and the reader is pure, so it opens no path.

## Checks

Lane r1, `evidence/b2d2-checks-r1/`:
- **the host suite** at base and candidate, with equal failure sets (8 at base) and six new tests;
- **rustfmt** and warning-denied all-targets Clippy on host;
- **the recognition tests,** and the recognition and YAML vector `--check`s against the bound reference;
- **FW-01,** environment exceptions, the operability source census and verify_design;
- **ten mutations,** each failing the recognition tests:
  - the state rule reverted;
  - the entry bound per result, or skipped under an override;
  - explicit `[]` read as absent;
  - any `workspace` value counted as a table;
  - the tsconfig bound dropped;
  - the pnpm subset unchecked;
  - the jest config disclosure dropped;
  - the hints unfiltered;
  - evidence hashed over the path.

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
