# B2-d implementation plan r1: framework recognition, the YAML subset reader and recommendation evidence (M3-B items 16 and 18)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product `a50ae96`: inventory v209, 170 contract successors;
- architecture `4415adb5`: shared status r102.

**What precedes it.**
- B2-a, B2-b and B2-c are bound. B2-c delivers the native unit instrument (`crates/host/src/discovery.rs`), its JSONC reader (`jsonc.rs`) and the TypeScript configuration reader.
- B3-b is bound.
- B2-d is the last B2 unit in the law's table: PROPOSAL-r9.md:1125, "Host-side recognition (item 16), the YAML subset reader, and the recommendation evidence (item 18)", size M, after B2-c.

**Authority:**
- law M3-B r9, items 15 (FW-01), 16, 17 and 18, and the unit table;
- NE §8 (native-evidence.md:2749-2777): `FrameworkRecognitionV1`, the nine recognizers and FR-1 to FR-5;
- CH13:59-75: discovered values, the resolver's precedence, and recommendations;
- the bound `FrameworkRecognitionPlanV1` schema (`schemas/sources/framework-recognition-plan-v1.schema.json`, selected by source-selection-v3; generated types `RecognitionPlan1*` in `crates/contracts/src/generated/identity.rs`);
- the B-S9 native reference model, contract successor 81 (`b-s9/reference/native_evidence_model.py`), whose `recognize_frameworks` (lines 3529-3589) is the accepted reference for §8;
- the B1 resolver (`crates/host/src/configuration.rs`, `resolve`), which is item 18's "actual resolver".

## 0. What B2-d delivers, and what it does not

**Delivers**, all pure and first-party in `crates/host`, with no caller:
- **the nine recognizers of NE §8,** producing one `FrameworkRecognitionV1` per `rust` or `tsjs` unit of B2-c's instrument. They read manifests as data:
  - `package.json` through exact JSON admission (`opensip_identity::parse_json`);
  - `tsconfig.json` and `jsconfig.json` through B2-c's JSONC reader;
  - `Cargo.toml` through the pinned `toml` (`opensip_identity::parse_toml`);
  - `pnpm-workspace.yaml` through the new reader below.

  FR-1 to FR-5 hold exactly. Each `UnitRecognitionV1` carries its `recognitionId` (domain `native.framework-recognition.v1`, as `closure.rs` checks it);
- **a closed YAML subset reader** (`crates/host/src/yaml_subset.rs`) for a `packages:` sequence of plain or quoted scalars, with no dependency;
- **the recommendation evidence of item 18:** one pure function in `discovery.rs`, whose every proposed setting round-trips through `configuration::resolve`;
- **the Cargo workspace fact** that B2-c's instrument takes as an input (`MarkerFact.is_cargo_workspace`). It is derived from the same parse as `cargo-workspace` recognition, so recognition and discovery cannot disagree. J1 supplies it through this function.

**Not delivered:**
- **Reading the files** (C1 or J1). B2-d takes file bytes and membership as inputs, as B2-c does.
- **Committing `FrameworkRecognitionPlanV1` into a Plan,** with its `snapshotId` and `membershipDigest` (C4). B2-d produces the per-unit `UnitRecognitionV1` rows, validated against the schema's `$defs`.
- **A `recommend` command** (M4; M3 wires none, item 18).
- **The provider-side consumer** (`providers/typescript/src/framework-recognition.ts`; F, item 16).
- **FR-6 to FR-8.** These are the unaccepted owner proposal S1, `m1/trials/report-evidence-design-02/subject/owner/native-recognition-successor.v1.json`; Grok's review states that "S1–S4 remain unaccepted proposals". See Q2.

## 1. B2-d0: the recognition reference (design unit; contract successor 171)

**Why a reference unit.** The B-S9 model's `recognize_frameworks` is the accepted §8 reference. It differs from law item 16 in four places, and the product needs one oracle. B2-d0 is a wrapper, as B2-c0 was: it loads the B-S9 model at its accepted bytes, with its loading closure pinned and supplied, and calls `recognize_frameworks`. It changes only:
1. **`Cargo.toml` is parsed, not matched by regex** (law item 16 readers: "the pinned `toml` crate").
   - The model's `^\[workspace\]` and `^\[package\]` regexes become "the parsed document has a `workspace` table" and "has a `package` table" (`tomllib`, as B3-b0 aligned the readers with `toml`).
   - **Differences, each a vector:**
     - `[workspace.dependencies]` alone is a workspace;
     - a header-like line inside a multi-line string is not;
     - an unparseable `Cargo.toml` gives `cargo-package` and `cargo-workspace` nothing, plus one `node-package`-style disclosure: recognizer `cargo-package`, `assurance: inferred`, field `<unparseable>`, `unresolvedChoices: ["Cargo.toml-not-toml"]`. This mirrors the model's own `package.json-not-strict-json` rule (line 3549).
2. **`tsconfig.json` and `jsconfig.json` are parsed** with item 14's JSONC grammar, which B2-c2's accepted reader implements. Today the model only checks they exist.
   - A parse failure keeps the `typescript-config` result and makes it `assurance: inferred`, with `unresolvedChoices: ["tsconfig-not-jsonc"]`. This is the same pattern.
   - The effects stay empty, as in the model.
3. **`pnpm-workspace.yaml` is read by the closed YAML subset** (section 2). Today the model only checks it exists.
   - Inside the subset: the model's result, unchanged.
   - Outside it: FR-1's disclosure (`unresolvedChoices: ["config-requires-evaluation"]`, no effect), as item 16 states.
4. **FR-4's other two bounds, and FR-2's explicit entry points** (sections 3 and 4). Today the model checks only `maxRecognizersPerUnit`.

**Everything else is the model's:**
- the nine recognizers and their evidence fields;
- `node-package`'s `node_modules/` convention;
- `vitest-jest`'s detection (the `jest` key or a config file) and its three default test globs;
- `nextjs`'s route rule and `vite`'s `index.html`;
- `FRAMEWORK_HINTS` (eleven names) for FR-3;
- the sort and the `entryPoints.state` rule.

**Its checker:**
- one positive and one `config-requires-evaluation` case per recognizer;
- the FR-4 bounds at the bound and one past it;
- an `observedHints` case;
- each of the four changes against the unwrapped model, showing the change is exactly the stated one and the rest equal;
- schema validation of every output against `FrameworkRecognitionV1`.

## 2. The closed YAML subset (B2-d1)

**The grammar is closed, and every byte outside it is a disclosure.** A document is in the subset when it is UTF-8 without a BOM and, line by line:
- it holds only blank lines, whole-line `#` comments, the single top-level key `packages:` at column 0, and the block sequence items below that key;
- each item is `-`, at a consistent indentation of at least one space, followed by one scalar and an optional trailing comment;
- a scalar is either
  - **plain:** no leading indicator character (`-?:,[]{}#&*!|>'"%@`` ` ``), no `: ` or ` #` inside, no trailing spaces, or
  - **quoted:** single-quoted (with `''` as its only escape) or double-quoted (with only `\"` and `\\` as escapes);
- the sequence may be empty (`packages: []`), the only flow form admitted;
- there is no other top-level key, document marker (`---`, `...`), anchor, alias, tag, multi-line scalar or flow collection.

**The result** is the ordered list of package globs. Anything else is one typed error, never a partial list.

**Why so narrow (LD-B2D-1).** Item 16 and its "Rejected" line ask for exactly this: no YAML dependency, and no guess. Real `pnpm-workspace.yaml` files often hold other top-level keys (`catalog:`, `onlyBuiltDependencies:`). Those fall outside the subset, so they get FR-1's disclosure.

The recognizer's effects are empty either way. In the model, `pnpm-workspace` contributes evidence only. So the narrowness costs recognition no effect; it only adds a disclosure.

**Rejected:**
- skipping unknown keys by indentation, which reads bytes outside the subset;
- a YAML crate, rejected by the law and by M3-P0's policy, which has no YAML row.

**The bound:** the file must be at most 64 KiB, as item 14 bounds a configuration file. A larger file is outside the subset.

**Controls:**
- a hand-written grammar table, with each production accepted at least once and each exclusion refused at least once;
- equality with the B2-d0 Python reader on every vector;
- a byte-flip sweep over each accepted vector, where every result is either accepted or the typed error, never a panic;
- FW-01's structural check extended to `yaml_subset.rs`.

## 3. The recognizers (B2-d2)

**The module.** `crates/host/src/framework_recognition.rs` exposes `recognize_unit(unit: &WorkspaceUnit, inputs: &RecognitionInputs) -> UnitRecognitionV1`, a pure function. Its inputs are:
- the unit's member paths;
- the bytes of each declared evidence file present: `package.json`, `tsconfig.json`, `jsconfig.json`, `Cargo.toml`, `pnpm-workspace.yaml`, the four jest and vitest configs, and the next and vite configs.

  A configuration file that needs evaluation is hashed for its `contentSha256` and never parsed;
- the resolved explicit entry points (Q1).

Its output is the generated `RecognitionPlan1UnitRecognitionV1`, its `recognitionId` computed as `closure.rs` checks it.

**Paths.** Evidence and entry paths are unit-root-relative, as the reference emits them (Q2).

**FR-4** (LD-B2D-2):
- **`maxRecognizersPerUnit` 32:** nine recognizers can never reach it. It is an assertion, and a vector proves the count.
- **`maxEvidenceFilesPerRecognizer` 64:** the model's recognizers cite one file each. It is an assertion as well.
- **`maxEntryPointsPerUnit` 65,536:** reachable, by `nextjs` routes. One past the bound, the recognizer's entry points are not emitted and its result gains `unresolvedChoices: ["entry-points-over-bound"]`, so `entryPoints.state` is `partial` or `none`.

  Nothing is truncated, and there is no refusal: recognition is advisory (FR-3: "no refusal").

  **Rejected:** a typed refusal, which would make an unusually large Next.js tree unanalyzable for an advisory record.

**FR-5.** Each result carries `recognizerVersion` 1. A version-bump control shows `recognitionId` changes.

**FW-01** (item 15) covers the new files:
- the read-only-tree control;
- the canary fixture: `build.rs`, a `postinstall`, `.cargo/config.toml` with `build.rustc-wrapper`, `.npmrc` and `pnpmfile.cjs`, plus `next.config.js` and `vite.config.ts` naming canary paths;
- the structural check over `framework_recognition.rs` and `yaml_subset.rs`.

**Vectors.** Every B2-d0 case is reproduced byte for byte. A drift check pins the reference.

## 4. FR-2 and the declared-input path (Q1)

**What the law says:**
- NE FR-2: every effect enters the declared-input path with provenance `DISCOVERED:<recognizerId>@<version>`; explicit configuration wins and sets `entryPoints.source=explicit`.
- Law item 16 repeats it, and says C4 commits the recognitions in `FrameworkRecognitionPlanV1`.

**What the code has:**
- The B1 resolver has no discovered layer. `ProvenanceSourceV1` is `Defaulted | Carrier | Flags`, and B1-a's own comment says "At M3 the discovery fold is empty".
- The recognition schema has no provenance string.
- The configuration has `discovery.entryPoints` and `ignorePaths`, but no test-glob setting.

**The lead's reading (LD-B2D-3).** The declared-input path for recognition effects is `FrameworkRecognitionPlanV1`, which C4 commits into the Plan:
- Every effect sits inside a result that names its `recognizerId` and `recognizerVersion`. That pair is the `DISCOVERED:<id>@<version>` provenance, and B2-d exposes a pure function that renders it.
- **Explicit configuration wins:** when the resolved configuration's `discovery.entryPoints` is non-empty, every unit's `entryPoints` is `{state: all, source: explicit}`. The recognized results are kept, as disclosure, and C4 commits the explicit list as `explicitEntryPoints`.
- The resolver's discovery fold stays empty. No configuration leaf is `DISCOVERED`. So B1's resolver and digest are unchanged, and a configuration-free repository's `resolvedConfigDigest` is unchanged when its framework files change (law line 204), while the recognition digest changes.

**Rejected:** adding a `DISCOVERED` layer to the resolver. That would change B1's accepted digest semantics, and CH13 forbids a seventh configuration layer.

**The question for Codex:** is this reading within item 16, or does it need a law clarification (M3-B r10) before B2-d2?

## 5. The recommendation evidence (B2-d3)

**The function.** `discovery::recommendation_evidence(recognitions, configuration) -> RecommendationEvidenceV1` is pure and internal. M4 renders it, and M3 wires no command. It returns CH13:67-73's five parts:
- **detected evidence:** the recognized results, with their evidence;
- **proposed settings:**
  - `discovery.entryPoints` from the recognized entry points, when the configuration has none and recognition's state is `all`;
  - `discovery.ignorePaths` from the ignore conventions. A convention the resolver's logical-path check refuses is recorded as an unresolved choice, not proposed.

  Nothing is proposed for `discovery.workspaceRoots`. That setting is D15's configured member repositories (branch A), not package-workspace membership. Cargo, npm and pnpm workspaces are units B2-c already folds.
- **default rationale:** why each default holds when nothing is proposed;
- **unresolved choices:** every recognizer's `unresolvedChoices`, and `observedHints`;
- **the effect of each choice:** the resolved configuration with and without each proposed setting.

**The resolver check** (item 18, CH13:69-71). Each proposed setting is placed in a project carrier and resolved by `configuration::resolve`, the actual resolver. A proposal the resolver refuses is not emitted; it is recorded as an unresolved choice. The controls show:
- every emitted setting round-trips;
- applying none of them gives a byte-identical resolved configuration and digest.

**Nothing is written** (item 15). The type is internal; it is not a public record (Q3).

## 6. Order, gates and sizes

| Step | What | Gates |
| --- | --- | --- |
| **B2-d0** | The recognition reference (section 1) | Codex design review; bound as contract successor 171 |
| **B2-d1** | `yaml_subset.rs` (section 2) | Codex unit review; inventory |
| **B2-d2** | `framework_recognition.rs`, with FR-1 to FR-5, FW-01 and the vectors (sections 3 and 4) | Q1 settled; Codex unit review; inventory |
| **B2-d3** | The recommendation evidence (section 5) | Codex unit review; inventory |

Each step has its own lane:
- the host suite at base and candidate, with equal failure sets (8 at base);
- Clippy and rustfmt;
- FW-01;
- one mutation per new mechanism.

## 7. Questions for Codex

- **Q1 (section 4):** is LD-B2D-3 within law item 16, or is a law clarification needed? The reading has recognition effects declared through `FrameworkRecognitionPlanV1`, provenance carried by recognizer id and version, explicit `discovery.entryPoints` winning per unit, and the resolver's discovery fold staying empty.
- **Q2 (paths):** the bound schema's `x-opensip-path-law` note is marked PROPOSED and names FR-6 and FR-8, which are unaccepted. B2-d emits the reference's unit-root-relative paths and records the join to repository-relative paths as C4's open item. Is that right? Or must B2-d emit repository-relative paths now, which would be applying an unaccepted clause?
- **Q3:** is an internal `RecommendationEvidenceV1` type acceptable at M3? Or does item 18 need a schema record now, given that M4 renders it?
- **LD-B2D-1, LD-B2D-2:** the YAML subset's narrowness, and FR-4's entry-point disposition (disclosure, not refusal).

## 8. Not claimed

- No caller (J1).
- No Plan commitment (C4).
- No provider-side consumer.
- No FR-6 to FR-8.
- No qualification.
- No completion of B2 or M3-B.
