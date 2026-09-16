# Blind review — consumer-b.v24, runtime consumer-b.v24-source41.v1

**Verdict: ACCEPT-RECONSTRUCTABLE** (`blind-review.json#/verdict`, derived by `tools/finalize_review.py` from measured standing).

- **Standing.** This continues my original blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 over the source41 normative kit. Fresh-origin independence is not claimed anew.
- **Own history.** My earlier consumer-b.v24 and source39.v1–v3 results are preserved read-only and establish nothing about this kit. Source39.v3 ended CHANGES_REQUIRED on the MUST s39-M1.
- **Claims.** This review makes no product qualification claim, grants no implementation authorization, and implies no acceptance by any root or owner.
- **Root admission.** External root admission of the exported bytes is a separate gate. Its outcome is unobserved here and no feedback was supplied.
- **Future qualification.** Real OS/compiler/crypto/SQLite measurement, provider execution as enforcement proof, host authentication and synthetic TCB enforcement (`F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST`) are unperformed and not counted as design omissions.

## Why the verdict is ACCEPT-RECONSTRUCTABLE

Every charter condition was evaluated on executed results, not counts:

- **Requirements.** All 123 requirements and 8 standing rules are executed; none failed and none is unexecuted (`requirement-status.json`; checkpoints 0–11 with unioned ID sets). The 3 future-qualification items are recorded as not demanded.
- **Positives.** All 27 claimed complete positives were:
  - validated against their owning schemas, including the published kit keywords (typed scalars, stock schema, `x-opensip-order`, `x-opensip-digest`, the payload and relation registries);
  - admitted by owner graph admission with every cross-record join;
  - closed by the independent retained-closure walker from the registries alone;
  - replayed from the exported store with byte-equal proofs and reachable output-set equality;
  - exported with complete object tables and every blob keyed by digest.
- **Negatives and controls.** The designed negative refuses. All 32 retention/reference-class negatives pass. All four source41 closure controls refuse.
- **Kit custody** is PASS before and after execution.
- **No new MUST or SHOULD issue** is supported by the source41 text. The one source39 MUST (s39-M1) is resolved by the kit, and the resolution was measured, not assumed.
- **No open helper failure.** Every helper defect found (HC-39..HC-46) had a precise kit or own-tool answer. It was corrected with its original failure preserved, and every current-source-dependent result was re-executed after the last change.

## Input custody

- **Kit manifest.** `subject/consumer-input-manifest.json` SHA-256 `31369cc8c3b71e559c50f107104daff4d6d428e20fb75dc1e3914a2acc1ec6dd`, parent frozen manifest `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236`, 104 members. Every member's SHA-256 and length verified; no unlisted file (`vectors/phase0-custody.json`).
- **Re-verified at the end.** The rows are identical to phase 0 (`runs/final-custody.json`: PASS; charter SHA-256 `35f8babc…`, requirements SHA-256 `f116cad4…`).
- **What changed against my own source39.v3 custody rows (orientation only).** Five documents; nothing added or removed:
  - `execution-inputs-contract.v1.md`;
  - `run-termination-contract.v1.md`;
  - `evaluator3/policy-test.schema.json`;
  - `native-evidence.md`;
  - `workflows-and-surfaces.md`.
- **Reading.** All five changed documents, the charter and the requirements were read in full. The source41 law deltas and the helper check each implies are logged in `notes/01-source41-law-deltas.md`.

## How the reconstruction was carried out

1. **Port.** My own source39.v3 helpers were ported with only the runtime root rebound (`port-manifest.json`).
2. **Unchanged run first.** They were executed unchanged against source41 (logs `s41-original.*`, `s41-original-mut.*`, `s41-original-disc.*`), and the whole output tree was preserved byte-for-byte (`preserved/s41-original-state/`) before any change. That state is re-executable at `preserved/pre-s41/`; the rest of the original chain was run there too (`preserved/pre-s41/logs/s41-pre-*`).
3. **Correct from the kit.** Helpers were corrected only from the kit (`tools/hc_source41.py`):

| HC | What was wrong | Source41 selector | Original failure (preserved) |
|---|---|---|---|
| HC-39 | (a) tsjs `unitKind` projection not enforced; (b) mode selection ignored the s1.2 effective `allowJs` for both markers; (c) no U-0 root decision | native lines 755-760, 797-799; 516-531, 654-659; 626-651; `#/$defs/InternalUnitRootV1`, `CanonicalRelativeDirV1`, `x-opensip-config-node-kind-law` | the s39-M1 alternative spelling passed every check; 3 of 10 mode cases differed; a `.` root was misattributed |
| HC-40 | phase-6 vector universes spelled the pre-HC-20 flag law (no result depended on it) | native lines 538-540 | — |
| HC-41 | own `cb24.` key for a non-object termination candidate | run-termination line 173 | `preserved/pre-s41/logs/s41-pre-p4to9.8.run_termination_vectors.log` |
| HC-42 | view attribution not derived: no `EXECUTION_INPUTS_VIEW_TOTALITY`, no candidate-view plan join; builders put one view on every row; two own follow-on errors | execution-inputs s3 line 53; `CellProgramOutcomeV1.viewDigests` | `logs/s41-hc42-probe.0.syntax_runs.log`; `logs/s41-post-p4to9.0/.5`, `logs/s41-fin-p4to9.0` |
| HC-43 | custody tools asserted the source39 hashes | supplied source41 values | found by reading before execution |
| HC-44 | negatives' pre column pointed at a source39 copy not in this runtime | runtime adaptation | — |
| HC-45 | first omitted-view control built no mutation (store identical, admitted) | own tool | `logs/s41-post-mut.0.replay_all.log` line 42 |
| HC-46 | phase-11 check compared the md with the interim phase-10 verdict | own tool | `logs/s41-phase10.0.finalize_review.log` |

4. **Rebuild with the final code.** Every store was rebuilt and every closure-dependent result re-executed after the last helper change: logs `s41-fin-*`, `s41-fin2-p45.*` and `s41-fin2-prov.*`.
5. **Tooling.** Every script ran as `/tmp/opensip-architecture-review-env/bin/python -I -B` through `tools/seq.py`, with complete retained logs. No subagent, author model, fixture, report, root result, LIVE input or other runtime was read.

## Claimed complete positives and exact exports

Each export is `runs/<run>.store.json` (object table plus every blob). Each Run also has a from-scratch closure (`runs/<run>.replay.fromscratch.json`), an export replay (`runs/<run>.replay-export.json`) and a per-record admission log (`runs/<run>.records.json`).

| Run | runId |
|---|---|
| cmp-base | `run3:5d35fcf55e5241861493e0965d065222abeae07c0a49d08ddc4501ab62ea2f0f` |
| cmp-budget | `run3:1d98ac938f6659668801420f8c79698e3db60440482209116634cad792aec181` |
| cmp-code-det2 | `run3:670a5bc5d8ff5c1eac682de20ae734da605189af48c827506ff2bd6729610d34` |
| cmp-code-detc | `run3:90cdd3ab2ce0b4dd53bbf8a87b158f9be29f75a3c1f830bc36cc0b5736d3d1b0` |
| cmp-code | `run3:9326c8c8a6357bed3529fee00eeccebf018f6c19de3587bf64382b8b375acca1` |
| cmp-empty | `run3:3526a8eca6e72fb608a597c328c950988b027faa4de247a0b2e6c7f503e3f1c4` |
| cmp-evidence | `run3:52e8122c27fca56bf57c53afce0bd92de7cdce647ff950651ab7ed3d78ae39a8` |
| cmp-gbase | `run3:c58194c522c8d73d193ddf2005f687ee7737bca7b87b600a3f00df43b26dbde2` |
| cmp-gevidence | `run3:9145eb6b54534ab910316e4c1b2b1a2538bbf2ae1a07592c96a4efdb0ca4b3f4` |
| cmp-gmissing | `run3:954c7b96b4056e815dfa61eb68c1b8dcd521b676bb0bef47370c7e29f0450c59` |
| cmp-hidden | `run3:8c9aff3547853a5cdbfbe9ae8cb7be38c178eaec818b0ce63b3e2aa6f7f3e857` |
| cmp-policy | `run3:e14fef7e8c4b7f1e7f074533f16005c792ee36707ecd0f6658c6c752bfa36078` |
| cmp-scope | `run3:8d062185f99711c8a519d3b4103ad5a21e747a323e638c37e1cc3a6a37bfe2e9` |
| cmp-waiver | `run3:a8a8137d3dc5a7c7c15511b9b41c0bdae1a47263c40aa5cf5d9c0e88bc129715` |
| rust-ambiguous | `run3:4725bc8dbefc4ee676f7fce51d21a41935571699dd193330f1a7c022bb9f5bdc` |
| rust-extra-unit | `run3:faca3160c1897eed3b3c53160c6cef84fc2d638023b4b147007b0ca657e53aa1` |
| rust-mixed-clones-required | `run3:085f12935f50bfc361ca2910c756239560ca72835e3208de684055655222ca1d` |
| rust-mixed | `run3:c17dab38e1c1878869dd01651123e2372448fcf821994f54e1555d031cad4fbe` |
| rust-partial | `run3:1d9d244284d91cd05b47f8d3ac430549e76a10fe55addbf2a153f5fa4f6bafa2` |
| rust-same-file-2021 | `run3:f5bfe8ca229d8d7d1e7173a0bd1b945834d55d2212aeaa5779a7a39a6f439b1d` |
| syntax-code | `run3:1e254af2f884b996099ae68cf527764b26d5de02a4a49645991f4f88ef389025` |
| syntax-data | `run3:0b262a42f2058066f36994aeb7dad25c2d2946e976be4d7603a1d5a7d9bc55ff` |
| syntax-mixed-disclosed | `run3:c5b0b4e031085e690dd0a05d4bfe2f3739a55daece4db4456b4ccd55db5edff0` |
| syntax-mixed-omitted | `run3:f3d3d83b025dddaeea11d589206811d9d20d52bdafad1a06be6058bd729887da` |
| ts-clones-required | `run3:47122c4202855ab6c4557e90052272ea378ac22604ed98a29a801d98c9d424d6` |
| ts-fail | `run3:3809aba8571fd58014824c7331099d680536e47b1b9d60bf67cbe73c0ed8fa22` |
| ts-pass | `run3:8e61b64f43fe2c36291c219e95704c5473cfbc8a741c49d57fffa42b9822b220` |

The designed negative `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.

**From-scratch command** (reads only exported stores and the kit, one fresh process per Run):
`cd /private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py`

## Independent vectors and results (final execution)

| Area | Result | Artifact / log |
|---|---|---|
| C/H, CVE1, lexical admission, raw vs parsed | 0 failures | `vectors/phase1-canonical.json`, `logs/s41-post-p123.0` |
| capability manifests, four gates | 5 positives, 19 negatives, 0 failures | `vectors/capability-manifests.json` |
| protocol3 traces | all 34 rows exercised, pairwise disjoint | `traces/`, `logs/s41-post-p123.2` |
| tables, RC-0..RC-6, cell-outcome derivation (incl. s4 cross-source order, s5 applicability) | 17 relation/rung rows, 16 RC vectors, 10 outcome vectors, 0 failures | `vectors/phase4-tables.json`, `logs/s41-fin2-p45.0` |
| discovery, U-0, U-1/s1.2 modes, U-4b (incl. unitKind projection, nested workspaces), U-8, U-9 | 29 vectors, 0 failures | `vectors/discovery-membership.json`, `logs/s41-fin-disc.0` |
| phase 5 (Rust dialect pairs, unsupported grammar, hidden/mismatch per language) | 0 failures | `logs/s41-fin2-p45.1` |
| phase 6 (config, JS body through TS, clones negatives, repair, min resolution, imports, mutation replay scope, pinned purge) | 0 failures | `logs/s41-fin-p4to9.2` |
| phase 7 (multi-unit selection, envelopes, D9 extension, receipts) | 0 failures | `logs/s41-fin-p4to9.3` |
| phase 8 comparisons and envelopes | 0 failures; 45/45 public termination goldens | `logs/s41-fin-p4to9.4`, `.5` |
| analysis-Run termination (incl. s7.3 derivation-binding joins, s6 non-object key) | 28 Runs, 9 candidate checks, 30 host compositions, 0 failures | `vectors/run-termination.json` |
| graph query | 53 vectors, 0 failures | `vectors/graph-query.json` |
| per-record admission log | 27 positives, 0 failures | `runs/phase9-admission-summary.json` |
| mutation replay | 66 stores: 29 admit (27 positives + 2 lawful controls), 37 refuse | `runs/replay-all.summary.json`, `logs/s41-fin-mut.0` |
| tamper | every semantic control refused by replay; every identity control refused before replay | `runs/*.tamper-outputs.json` |
| retention/reference-class negatives | 32 constructed, all pass | `vectors/retention-negatives.json` |
| unchanged vs corrected helpers | see the next table | `selfcheck/s41-prepost-matrix.json` |

Unchanged helpers (pre) vs corrected helpers (post):

| | Unchanged helpers | Corrected helpers |
|---|---|---|
| Positives, original bytes (built by the unchanged helpers) | admit 27/27 | admit 23; refuse `syntax-code`, `syntax-data`, `syntax-mixed-disclosed`, `syntax-mixed-omitted` (`EXECUTION_INPUTS_VIEW_TOTALITY:1:0`) |
| Positives, current bytes (rebuilt) | admit 27/27 | admit 27/27 |
| `syntax-code~unit-kind-other-family` | admitted | refuses `ENUMERATION_MEMBERSHIP_ORDER:unitKind-family:0` |
| `ts-pass~unit-kind-not-mode-projection` | admitted | refuses `ENUMERATION_MEMBERSHIP_ORDER:unitKind:0` |
| `syntax-code~unit-root-external-sentinel` | refused only by generic schema admission | refuses `ENUMERATION_MEMBERSHIP_UNIT_ROOT:0:rootPath` |
| `syntax-code~row-view-omitted` | refused `EXECUTION_INPUTS_OUTCOME_DERIVE` | refuses `EXECUTION_INPUTS_VIEW_TOTALITY:0:0` |

The corrected code also refuses the four syntax positives over the exact bytes the unchanged builder produced. That is the measured evidence that the source41 attribution law was not implemented before.

The per-requirement status is in `requirement-status.json` and `blind-review.json#/requirementStatus`.

## Issues

### newMustIssues

None.

### newShouldIssues

None.

### Disposition of my source39.v3 findings

- **s39-M1: resolved by the kit.**
  - native lines 755-760 (U-4b.2) now assign `ts-program` exactly for `ts-tsconfig`, and `js-program` for `js-allowjs` and `js-synthesized`.
  - Lines 797-799 (U-4b.5) refuse any other spelling.
  - Measured in `vectors/discovery-membership.json#u4b-tsjs-unit-kind-projection`: the source39 alternative is schema-valid, now refuses `ENUMERATION_MEMBERSHIP_ORDER:unitKind:0`, and only the projection admits. Run closure: `runs/ts-pass~unit-kind-not-mode-projection`.
- **A-n2, A-n3, A-n4, A-n5: resolved by the kit** (run-termination lines 174-176, 173 and 85-87, 246-253; native lines 747-754). Each is measured in `vectors/run-termination.json` or `vectors/discovery-membership.json#u4b-nested-cargo-workspace`.

### Advisories (nonblocking)

- **A-c1.** Internal refusal names that no kit owner publishes are still spelled `cb24.*`. `blind-review.json#/advisories` lists the 71 measured keys.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. The successor D9 artifact is a disclosed live cross-unit obligation (native lines 3313-3327).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change, so gating evidence rules attribute INDETERMINATE `evidence-content-changed` (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3), the detector disposition, is unreachable for entries (workflows s3 lines 402-411; `vectors/baseline-e0-e3.json`).
- **A-n6.** The mode table decides a rust unit's `languageMode`, which enters `membershipDigest` and the default rows (native lines 165-172, 1070-1072, 1842-1847). U-4b.2 (lines 741-746) does not restate it, and U-4b.5 (lines 797-799) publishes no retained-record enforcement for it, unlike the tsjs projection.
- **A-v2-1.** Composition s7 does not say whether typed-prefix values inside workflow-owned Plan input documents are closure references. The deterministic reading from s7 line 74, s5 line 54 and identity lines 597-600/627-631 is applied: `cmp-empty` and `cmp-budget` admit.
- **A-v2-2.** `policy-derivation3` is outside the reachable output set and retained as an unreachable non-authoritative frame (composition s7 lines 70, 76).
- **A-v2-3.** Identity s3 (lines 441-467) calls its representation and retention vocabularies closed, while the native and relation bundles publish their own `x-opensip-digest-law` vocabularies (`vectors/reference-census.json`).
- **A-s41-1 (new).** run-termination s7.6 step 1 (line 330) names no key for a non-object. s6 step 1 (line 173) publishes `RUN_TERMINATION_CANDIDATE_NOT_OBJECT`, which is applied at both boundaries.
- **A-s41-2 (new).** U-1's "an omitted value defaults to false for a `tsconfig.json` entry" (native lines 656-659) can be read against s1.2's derivation of an omitted `allowJs` from `checkJs` (lines 524-526, 562-563; mode table line 162).
  - The s1.2 derivation governs and is applied: a `tsconfig.json` with `checkJs:true` selects `js-allowjs`.
  - A literal U-1 reading would change `membershipDigest` (`vectors/discovery-membership.json#s12-effective-allowjs-mode-selection`).

## What required invention

No record, identity or refusal had to be invented. Four places needed a named reading, each measured or stated beside its alternative:
- A-s41-1: the s7.6 key;
- A-s41-2: s1.2 over U-1's wording;
- A-v2-1: typed-prefix closure scope;
- A-n6: the rust unit mode taken from the mode table.

Keys the kit does not publish carry the `cb24.` prefix so they are never mistaken for published vocabulary (A-c1).

## Limitations

- run-termination s7.5 row 2 and s5 stage-terminal carriers are exercised by vectors, not on built Runs.
- The retained-closure walker names what it delegates to owner graph admission, which runs as its own stage: `languageVersionBinding` derivation, clones framed-body-identity parse joins, native context/universe binding, and enumeration and execution-input derivation.
- The census pairs `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` occur in no constructed positive and have no negative.
- **Not constructed by any original requirement; read but not exercised:**
  - PolicyTestSuiteV2 (changed in source41);
  - the U-8 security/host boundary-inventory superset join;
  - `target-attribution-v2` occupancy companions.
- `discovery-defaults.py` was neither read nor used.
- Root admission of the exported bytes is unobserved.
- **Product qualification.** This review makes no product qualification claim and no implementation authorization. All future-qualification items remain unperformed.

## Retained outputs

- **Machine-readable review:** `blind-review.json` (verdict basis, issues, advisories with selectors and measurements, prior dispositions, HC records, positives with run ids, `requirementStatus`).
- **Checkpoints and status:** `checkpoints/phase-0.json` … `phase-11.json`; `requirement-status.json`.
- **Notes:**
  - `notes/00-session-standing.md`;
  - `notes/01-source41-law-deltas.md`;
  - `notes/07-phase7-reconstruction.md`;
  - `notes/08-subsystem-owners.md`;
  - `notes/09-reconstruction.md`;
  - `notes/10-gaps.md`.
- **Code:** `ref/`, `builders/`, `tools/`, `vectors/`.
- **Results and logs:** `runs/`, `envelopes/`, `traces/`, `negatives/`, `selfcheck/`, `logs/`.
- **Own history:** `preserved/`.
