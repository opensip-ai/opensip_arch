# B2-d3 r2: the recommendation evidence (M3-B unit B2-d, sub-unit B2-d3)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.**

## r2 changes (Codex `codex-b2d3-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2D3-R1-RF-1:** keep the recognized results | `detected` is now one `DetectedUnit` per unit. Each holds the unit's ordinal and root, its **complete** `FrameworkRecognitionV1` (every result with its assurance, evidence, unit-relative effects and unresolved choices; the hints; the entry state), and each result's FR-2 provenance in result order. Detected effects stay unit-relative; only proposals are project paths. A new control, `detected_evidence_keeps_what_no_proposal_shows`, has two partial Next.js units with identical configs and different routes, plus a jest config. No entry point is proposed, with configuration absent or explicit `[]`, yet the two detections differ, each keeps its routes, and the `inferred` assurance, the test globs and the `vitest-jest` provenance stay visible. Mutant: `detected-recognition-dropped`. |
| **RF-2:** the resolved configurations | `base` is the actual `ResolvedConfigurationV1` of the input, with no proposal applied. Each `ProposedSetting` carries `resolved_with`, the actual resolution with that setting, and digests remain inside both. When the resolver reorders a proposal, `round_trip` re-resolves the presentation in the resolver's order and requires it to hold. So `resolved_with` is exactly what applying the presented setting gives, carrier bytes and provenance included. Building this found the difference: the first resolution's carrier held the original order. The tests now assert the returned records against actual `resolve` outputs: `base == resolve(input)` (applying none changes nothing), and each `resolved_with == resolve(apply_setting(input, presented))`. Mutant: `effect-not-presented-order`. |

It implements B2-d3 of the B2-d plan r3, section 5 (`../b2-d/PLAN-r3.md`; Codex `codex-b2d-plan-r3`, with Q3 settled: an internal type at M3). It uses B2-d2's recognitions (Codex `codex-b2d2-r2`) and the B1 resolver, item 18's "actual resolver".

**Base:** product main `b68ddee` (B2-d2 and inventory v211; 171 contract successors); architecture `4effe027`. Round 1 is `../b2-d3-r1/`.

## What it delivers

### `crates/host/src/recommendation.rs` (new), exposed by `discovery.rs`

`recommendation_evidence(units, input) -> Result<RecommendationEvidenceV1, ConfigurationRefusal>` is pure and internal. It takes each unit's ordinal, `rootPath` and recognition (B2-d2's `FrameworkRecognitionV1`), plus the actual `ResolverInputV1`. `discovery.rs` re-exports it, because law item 18 says "`discovery.rs` exposes one pure function". The body lives in its own module, so the reviewed B2-c instrument gains only the re-export. Nothing calls it at M3, which wires no command; M4's `recommend` renders it.

It returns CH13:67-73's five parts:
- **detected evidence:** per unit, its complete recognition, with ordinal, root and each result's FR-2 provenance `DISCOVERED:<id>@<version>` (r2);
- **proposed settings:** `discovery.entryPoints` and `discovery.ignorePaths`, each a list of project paths, with every source unit and recognizer behind each path;
- **default rationale:** for each field with nothing proposed, why: `explicit-configuration`, `recognition-incomplete` or `nothing-recognized`. `discovery.workspaceRoots` always gives `not-recognition-evidence`;
- **unresolved choices:** every recognizer's `unresolvedChoices` with its source, and every proposal the resolver refused. FR-3's observed hints come separately, per unit;
- **the effect of each choice:** the actual resolved configuration without any setting (`base`), and with each one (`resolved_with`) (r2).

**The resolver check** (item 18; CH13:69-71).
- **The base:** the base is `resolve(input)`. A refusal there is returned unchanged.
- **The round trip:** each proposal is placed in the project carrier (`apply_setting`, in memory only) and resolved by the actual `configuration::resolve`. It is proposed only when the resolver admits it and gives back exactly the proposed paths. Otherwise it is recorded as unresolved.
- **Applying none changes nothing:** the base is the input as resolved.

## Lead decisions

- **LD-B2D3-1. When entry points are proposed.** Only when two things hold:
  - no layer won `discovery.entryPoints`, which is plan r3's "absent" (no field and no provenance entry). Explicit configuration wins, `[]` included;
  - every unit's recognition `entryPoints.state` is `all`.

  Under FR-2, an explicit list replaces recognition for every unit (plan r3, section 4). A list proposed from only the complete units would therefore make the incomplete units' entry points silently wrong. So an incomplete unit makes the rationale `recognition-incomplete`, and its unresolved choices are carried.
- **LD-B2D3-2. Ignore paths.**
  - **When:** proposed only when no layer set `discovery.ignorePaths`. A carrier-won list is the user's, and a proposal would replace it whole.
  - **Projection:** a directory convention `d/` becomes the logical directory path `<rootPath>/d`. The resolver's logical-path check refuses an empty last segment, and the convention names that directory.
  - **The check:** each candidate is checked alone, so one the resolver refuses (for example `../escape/`) is recorded as unresolved and the rest are still proposed.
- **LD-B2D3-3. Where a proposal is placed.**
  - When the input has a project carrier, it is that carrier, with every other field and section kept.
  - Otherwise it is a new `opensip.json` holding `schemaVersion: 2` and the setting.

  A higher-layer value cannot be overridden this way, because a proposal is made only when no layer set the field.
- **LD-B2D3-4. The resolver's order.** `discovery` arrays are returned in the resolver's normalized order. A proposal is accepted when the resolver gives back exactly its paths, as a set of the same size, and it is then presented in the resolver's order. I found this while building: the two-unit case resolves `["crates/a/src/main.rs", "src/main.rs"]`.
- **LD-B2D3-5. Unit-root projection** (plan r3, RF-6). Each project path is the recognition path joined to its unit's `rootPath`, where `""` is the project root. Equal project paths from different units are one path citing every source. Retained recognition rows stay unit-relative.

### `crates/host/src/recommendation_tests.rs` (new)

The resolver input is the configuration vectors' reviewed `base` case (its defaults layer), with the project carrier set per control. The seven tests (r2 adds the last):
- **every proposal round-trips through the actual resolver.** Two Cargo units at `""` and `crates/a` propose `["crates/a/src/main.rs", "src/main.rs"]` and `["crates/a/target", "target"]`. Each setting applied resolves to its recorded digest and value. The base equals the input as resolved. The provenance is right, and there are no unresolved choices;
- **equal project paths from two units are one setting citing both:** `b/x` under `a` and `x` under `a/b`;
- **explicit entry points are never proposed over:**
  - absent: proposed;
  - explicit `[]`: not proposed;
  - project `["a"]` overridden by local `[]`: not proposed, and resolved to `[]`;
- **incomplete recognition proposes no entry points:** a Vite unit gives `recognition-incomplete`, its `config-requires-evaluation` is carried, and `web/dist` is still proposed;
- **a path the resolver refuses is recorded, not proposed:** `../escape` is refused, `node_modules` is kept, and the observed hint is carried;
- **applying a proposal keeps the rest of the carrier:** `ui` and `workspaceRoots` are kept, and a refused input returns the resolver's refusal unchanged;
- **detected evidence keeps what no proposal shows** (r2).

### `crates/host/src/discovery.rs`, `lib.rs`, FW-01

- `discovery.rs` gains the re-export, `#[allow(unused_imports)]`, because nothing calls it at M3.
- `lib.rs` gains the dead-code-allowed module and its tests.
- `recommendation.rs` joins FW-01's `COVERED` and `PURE`, and its tests are asserted outside production.

## Checks

Lane r2, `evidence/b2d3-checks-r2/`. Attempt 1 (`b2d3-checks-r2-attempt1/`) failed only one mutation control. Its `round-trip-skipped` mutant had been re-anchored on the set-equality guard (the resolver gives back exactly the proposed paths, as a set). That guard is defence in depth: the actual resolver reorders discovery paths but never adds or drops one, so no control can separate it. The mutant now skips the round trip itself, resolving without the proposal. Every other row of attempt 1 passed, and its other nine mutations were caught. The second attempt is the lane of record:
- **the host suite** at base and candidate, with equal failure sets (8 at base) and seven new tests;
- **rustfmt** (new files, plus `discovery.rs` and `lib.rs`, both clean at base) and warning-denied all-targets Clippy;
- **the recommendation tests,** and the recognition and YAML vector checks;
- **FW-01,** environment exceptions, the operability source census and verify_design;
- **ten mutations,** each failing the recommendation tests:
  - explicit entry points ignored;
  - incomplete recognition proposed;
  - the unit root not joined;
  - the round trip skipped;
  - ignore paths not checked alone;
  - the trailing slash kept;
  - equal paths not merged;
  - the carrier's other fields dropped;
  - (r2) the detected recognition dropped;
  - (r2) the effect not resolved in the presented order.

## Not claimed

- No command or caller (M4).
- No write: applying a proposal for real is a separate host operation with normal write authority, CH13:68-70.
- No public record (Q3).
- No qualification.
- B2-d's completion is not claimed here. Its inventory successor and a status round follow.

## Inventory

New paths for the inventory after acceptance:
- `crates/host/src/recommendation.rs`;
- `crates/host/src/recommendation_tests.rs`.
