# B2-d implementation plan r2: framework recognition, the YAML subset reader and recommendation evidence (M3-B items 16 and 18)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

## r2 changes (Codex `codex-b2d-plan-r1`, REQUIRED-FINDINGS)

Codex answered the three questions. **Q1:** no law clarification is needed; law item 1 itself says the M3 semantic fold is empty and that discovered values bind through their own Plan records. **Q2:** unit-relative recognition paths stay, and FR-6 to FR-8 are not applied. **Q3:** an internal recommendation type is acceptable. Codex also accepted the B2-d0 wrapper, the two disclosure strings, the narrow YAML subset and the actual-resolver round trip.

| Finding | Resolution |
| --- | --- |
| **B2DPLAN-R1-RF-1:** the inherited `entryPoints.state` rule gives `none` for a config that needs evaluation | **A fifth reference change** (section 1, change 5): `state` is `partial` whenever any result carries an unresolved choice, `all` when entries exist and none does, and `none` only when there is neither. Vectors: `vite.config.ts` without `index.html`, `next.config.js` without routes, an outside-subset `pnpm-workspace.yaml`, and mixed recognizers. |
| **RF-2:** the entry-point ceiling must hold across the unit | **The bound is per unit, all or nothing** (section 3): the distinct union of every result's entry points. One past 65,536, no result emits entry points, each entry-bearing result carries `entry-points-over-bound`, and `state` is `partial`. Cases at 65,536 and 65,537 are split across `nextjs` and `vite`, with and without overlap. |
| **RF-3:** an explicit empty `entryPoints` is not absence | **Explicit intent is the winning leaf's provenance** (section 4). Any `discovery.entryPoints` won by a carrier, including `[]`, is explicit: `{state: all, source: explicit}`, its effective set exactly that list, and no entry-point recommendation. Only a defaulted leaf is absent. Controls: absent, explicit `[]`, and project `[a]` overridden by local `[]`, for both recognition and recommendation. |
| **RF-4:** the YAML grammar admitted non-scalars | **Tightened** (section 2): a block item is `-`, then at least one space, then a scalar. A plain scalar holds no `:`, no tab and no ` #`. `- foo:`, `- foo:\tbar`, `-foo`, a bare `-` and mapping-valued items are outside the subset. Quoted counterparts of each are vectors. The 64 KiB cap is this reader's own selected bound. |
| **RF-5:** TOML resource differences | **The oracle applies `parse_toml`'s profile** (section 1, change 1). The byte cap (4 MiB) and the node limit (1,000,000, counted as `parse_toml`'s walk counts) are mirrored exactly. The `toml` crate's internal recursion limit cannot be mirrored in `tomllib`, so it is a labelled product-bound divergence, with product-only controls. Every `parse_toml` error, whether syntax, byte cap, recursion or node limit, gives the same disposition: the `Cargo.toml-not-toml` disclosure, and the shared Cargo-workspace fact unknown. Differential controls: usable `[package]` and `[workspace]` tables beside unrelated deep or wide fields, at the bound and one past. |
| **RF-6:** recommendations need project paths | **The unit-root join is part of B2-d3** (section 5). Each proposed entry point or ignore path is its recognition path joined to the unit's `rootPath` (`""` is the project root), and the proposal keeps its unit ordinal and recognizer. Equal project paths from two units are one setting citing both. Controls: nested units, colliding relative names, and the round trip on the mapped settings. This is recommendation correctness only; retained recognition rows stay unit-relative (Q2). |

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

**Why a reference unit.** The B-S9 model's `recognize_frameworks` is the accepted §8 reference. It differs from law item 16 in five places, and the product needs one oracle. B2-d0 is a wrapper, as B2-c0 was: it loads the B-S9 model at its accepted bytes, with its loading closure pinned and supplied, and calls `recognize_frameworks`. It changes only:
1. **`Cargo.toml` is parsed, not matched by regex** (law item 16 readers: "the pinned `toml` crate").
   - The model's `^\[workspace\]` and `^\[package\]` regexes become "the parsed document has a `workspace` table" and "has a `package` table" (`tomllib`, as B3-b0 aligned the readers with `toml`).
   - **Differences, each a vector:**
     - `[workspace.dependencies]` alone is a workspace;
     - a header-like line inside a multi-line string is not;
     - an unparseable `Cargo.toml` gives `cargo-package` and `cargo-workspace` nothing, plus one `node-package`-style disclosure: recognizer `cargo-package`, `assurance: inferred`, field `<unparseable>`, `unresolvedChoices: ["Cargo.toml-not-toml"]`. This mirrors the model's own `package.json-not-strict-json` rule (line 3549).
   - **The parser profile is `parse_toml`'s (r2, RF-5).** The wrapper refuses a document over 4 MiB, and one whose parsed value has more than 1,000,000 nodes counted as `parse_toml`'s walk counts them, exactly at the product's bounds.
     - The `toml` crate's internal recursion limit is not mirrored. `tomllib` has no equal bound, so this is the one labelled product-bound divergence. Its controls are product-only, with a stated expectation.
     - **Every parse error has one disposition:** syntax, byte cap, recursion or node limit all give the `Cargo.toml-not-toml` disclosure, and the shared Cargo-workspace fact is unknown (`None`). B2-c's instrument already treats unknown as "not a workspace".
     - **Differential controls:** a usable `[package]` or `[workspace]` table beside unrelated deep or wide fields, at the bound and one past it.
2. **`tsconfig.json` and `jsconfig.json` are parsed** with item 14's JSONC grammar, which B2-c2's accepted reader implements. Today the model only checks they exist.
   - A parse failure keeps the `typescript-config` result and makes it `assurance: inferred`, with `unresolvedChoices: ["tsconfig-not-jsonc"]`. This is the same pattern.
   - The effects stay empty, as in the model.
3. **`pnpm-workspace.yaml` is read by the closed YAML subset** (section 2). Today the model only checks it exists.
   - Inside the subset: the model's result, unchanged.
   - Outside it: FR-1's disclosure (`unresolvedChoices: ["config-requires-evaluation"]`, no effect), as item 16 states.
4. **FR-4's other two bounds, and FR-2's explicit entry points** (sections 3 and 4). Today the model checks only `maxRecognizersPerUnit`.
5. **The `entryPoints.state` rule (r2, RF-1).** The model returns `none` whenever no result has entry points, even when a config needs evaluation. NE FR-1 and item 16 require `partial` there. The corrected rule:
   - `partial` when any result carries a non-empty `unresolvedChoices`;
   - otherwise `all` when any result has entry points;
   - otherwise `none` (FR-3).

   Vectors: `vite.config.ts` without `index.html`, `next.config.js` without routes, an outside-subset `pnpm-workspace.yaml`, a parse-failure disclosure alone, and mixed recognizers. The explicit override is separate (section 4).

**Everything else is the model's:**
- the nine recognizers and their evidence fields;
- `node-package`'s `node_modules/` convention;
- `vitest-jest`'s detection (the `jest` key or a config file) and its three default test globs;
- `nextjs`'s route rule and `vite`'s `index.html`;
- `FRAMEWORK_HINTS` (eleven names) for FR-3;
- the sort.

**Its checker:**
- one positive and one `config-requires-evaluation` case per recognizer;
- the FR-4 bounds at the bound and one past it;
- an `observedHints` case;
- each of the five changes against the unwrapped model, showing the change is exactly the stated one and the rest equal;
- schema validation of every output against `FrameworkRecognitionV1`.

## 2. The closed YAML subset (B2-d1)

**The grammar is closed, and every byte outside it is a disclosure.** A document is in the subset when it is UTF-8 without a BOM and, line by line:
- it holds only blank lines, whole-line `#` comments, the single top-level key `packages:` at column 0, and the block sequence items below that key;
- each item is `-`, at a consistent indentation of at least one space, then **at least one space** (r2, RF-4), then one scalar, then an optional trailing comment (whitespace then `#`);
- a scalar is either
  - **plain:** no leading indicator character (`-?:,[]{}#&*!|>'"%@`` ` ``), and **no `:`, no tab and no ` #` anywhere** (r2, RF-4), with no trailing spaces, or
  - **quoted:** single-quoted (with `''` as its only escape) or double-quoted (with only `\"` and `\\` as escapes). A `:` or `#` is admitted inside quotes;
- **outside the subset (r2, RF-4):**
  - `- foo:` (a mapping entry);
  - `- foo:\tbar`;
  - `-foo` (no separation after the dash);
  - a bare `-` (a null item);
  - any mapping-valued or nested item;
  - tabs in indentation;
- the sequence may be empty (`packages: []`), the only flow form admitted;
- there is no other top-level key, document marker (`---`, `...`), anchor, alias, tag, multi-line scalar or flow collection.

**The result** is the ordered list of package globs. Anything else is one typed error, never a partial list.

**Why so narrow (LD-B2D-1).** Item 16 and its "Rejected" line ask for exactly this: no YAML dependency, and no guess. Real `pnpm-workspace.yaml` files often hold other top-level keys (`catalog:`, `onlyBuiltDependencies:`). Those fall outside the subset, so they get FR-1's disclosure.

The recognizer's effects are empty either way. In the model, `pnpm-workspace` contributes evidence only. So the narrowness costs recognition no effect; it only adds a disclosure.

**Rejected:**
- skipping unknown keys by indentation, which reads bytes outside the subset;
- a YAML crate, rejected by the law and by M3-P0's policy, which has no YAML row.

**The bound:** the file must be at most 64 KiB. This is this reader's own selected bound (r2: item 14a's TypeScript cap is not a general rule). A larger file is outside the subset.

**Controls:**
- a hand-written grammar table, with each production accepted at least once and each exclusion refused at least once. It includes the r2 cases: a terminal colon, colon-tab, a dash without separation, a bare dash, and the quoted counterparts that are admitted;
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
- **`maxRecognizersPerUnit` 32 and `maxEvidenceFilesPerRecognizer` 64:** the nine recognizers and their one-file evidence cannot reach them. Both are enforced by a bound validator that runs on every result. Its limit and one-past controls exercise the validator directly on constructed results, not through the nine recognizers (r2).
- **`maxEntryPointsPerUnit` 65,536 is per unit, all or nothing (r2, RF-2).**
  - The unit's effective recognized entry set is the distinct union of every result's entry points.
  - One past the bound, no result emits entry points. Each entry-bearing result gains `unresolvedChoices: ["entry-points-over-bound"]`, so `entryPoints.state` is `partial`.
  - Nothing is truncated, and uncertainty is kept at the unit's scope. The bound does not apply under an explicit override (section 4), where the configuration's own `maxItems` holds.
  - Cases: 65,536 and 65,537 distinct entries, split across `nextjs` routes and `vite`'s `index.html`, with and without overlap.

  **Disposition (LD-B2D-2):** a non-truncating disclosure, not a refusal. Recognition is advisory, and a refusal would make an unusually large Next.js tree unanalyzable. (FR-3's "no refusal" concerns unrecognized frameworks; it is cited here as the analogy, not as the law for overflow.)


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
- **Explicit configuration wins (r2, RF-3).** Explicit intent is the winning leaf's provenance, not emptiness.
  - When the resolved `discovery.entryPoints` was won by a carrier (project or local; `ProvenanceSourceV1::Carrier`), it is explicit, **including `[]`**. Every unit's `entryPoints` is then `{state: all, source: explicit}`, and the effective set is exactly that list, possibly empty.
  - The recognized results are kept as disclosure, and C4 commits the explicit list as `explicitEntryPoints`.
  - Only a `Defaulted` leaf is absent, and then recognition decides.
  - A higher layer's `[]` replacing a lower layer's list is honoured as the resolver merges it.
  - **Controls:** absent; explicit `[]`; and project `["a"]` overridden by local `[]`. Each is run for recognition and for the recommendation.
- The resolver's discovery fold stays empty. No configuration leaf is `DISCOVERED`. So B1's resolver and digest are unchanged, and a configuration-free repository's `resolvedConfigDigest` is unchanged when its framework files change (law line 204), while the recognition digest changes.

**Rejected:** adding a `DISCOVERED` layer to the resolver. That would change B1's accepted digest semantics, and CH13 forbids a seventh configuration layer.

**Settled (Codex Q1):** this is within the law. Law item 1 states that the M3 semantic fold is empty and that discovered entry points, test globs and ignore conventions bind through their own Plan records. Vectors cover the provenance rendering, `DISCOVERED:<recognizerId>@<recognizerVersion>`.

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

**Paths (r2, RF-6).**
- **Projection:** a recognition path is unit-root-relative. A proposed project setting is that path joined to the unit's `rootPath`, where `""` is the project root: `src/main.ts` in the unit at `apps/web` becomes `apps/web/src/main.ts`. An ignore convention such as `node_modules/` joins the same way.
- **Provenance:** each proposal keeps its unit ordinal, root and recognizer.
- **Merging:** equal project paths from two units are one setting, citing both.
- **Controls:** nested units, colliding relative names in two units, and the round trip on the mapped settings.

This projection is recommendation correctness only. Retained recognition rows stay unit-relative (Q2), and C4 settles their join.

**The resolver check** (item 18, CH13:69-71). Each proposed setting is placed in a project carrier and resolved by `configuration::resolve`, the actual resolver. A proposal the resolver refuses is not emitted; it is recorded as an unresolved choice. The controls show:
- every emitted setting round-trips;
- no entry-point proposal is made when entry points are explicit, `[]` included (RF-3);
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

## 7. Questions settled in r1's review

- **Q1:** within the law (section 4).
- **Q2:** unit-relative rows stay, FR-6 to FR-8 are not applied, and C4 settles the join. B2-d3's project settings are joined now (RF-6).
- **Q3:** an internal `RecommendationEvidenceV1` is acceptable at M3.
- **LD-B2D-1 and LD-B2D-2** are defensible, as revised for RF-2 and RF-4.

## 8. Not claimed

- No caller (J1).
- No Plan commitment (C4).
- No provider-side consumer.
- No FR-6 to FR-8.
- No qualification.
- No completion of B2 or M3-B.
