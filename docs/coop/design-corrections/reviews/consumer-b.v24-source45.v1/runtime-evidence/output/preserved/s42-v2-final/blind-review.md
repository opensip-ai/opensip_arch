# Blind review — consumer-b.v24, source42 (runtime consumer-b.v24-source42.v2)

**Verdict: ACCEPT-RECONSTRUCTABLE** (`blind-review.json#/verdict`, derived by `tools/finalize_review.py` from measured standing).

- **Standing.** This continues my original blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 over the source42 normative kit. Fresh-origin independence is not claimed anew.
- **Runtimes.** The work began in runtime `consumer-b.v24-source42.v1`. That process ended without checkpoints or a review, so it is incomplete, not a verdict; it is preserved in place. The work was completed here, in `consumer-b.v24-source42.v2`, from its byte-identical copied output.
- **Own history.** My earlier consumer-b.v24, source39.v1–v3 and source41.v1 results are preserved read-only and establish nothing about this kit.
- **This review corrects my own source41 result.** The source41 exports carried a helper omission of a published schema law (details below), so that ACCEPT recommendation rested on exports a conforming admission refuses.
- **Claims.** This review makes no product qualification claim, grants no implementation authorization, and implies no acceptance by any root or owner.
- **Root admission.** External root admission of the exported bytes is a separate gate; its outcome is unobserved here.
- **Future qualification.** Real OS/compiler/crypto/SQLite measurement, provider execution as enforcement proof, host authentication and synthetic TCB enforcement (`F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST`) are unperformed and not counted as design omissions.

## Why the verdict is ACCEPT-RECONSTRUCTABLE

Every charter condition was evaluated on executed results, not counts:

- **Requirements.** All 123 requirements and 8 standing rules are executed; none failed and none is unexecuted (`requirement-status.json`; checkpoints 0–11 with unioned ID sets). The 3 future-qualification items are recorded as not demanded.
- **Positives.** All 27 claimed complete positives were:
  - validated against their owning schemas, including the published kit keywords (typed scalars, stock schema, `x-opensip-order`, `x-opensip-digest`, payload and relation registries);
  - admitted by owner graph admission with every cross-record join, including the source42 enumeration-binding and execution-inputs laws;
  - closed by the independent retained-closure walker;
  - replayed from the exported store with byte-equal proofs and reachable output-set equality;
  - exported with complete object tables and every blob keyed by digest.
  From-scratch closure, export replay and the admission log were re-executed fresh in this runtime.
- **Negatives and controls.** The designed negative refuses. All 32 retention/reference-class negatives pass. All nine closure controls refuse on their own laws under the corrected code: the five source42 controls and the four carried source41 controls.
- **Kit custody** is PASS at phase 0 and again at the end, in this runtime.
- **No new MUST or SHOULD issue** is supported by the source42 text.
- **No open helper failure.** Every helper defect found (HC-47..HC-50) had a precise kit or own-tool answer; it was corrected with its original failure preserved. Every current-source-dependent result was re-executed after the last change to the code it uses.

## Input custody

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `9c90a1e849b1a33fb1aec507d6a4f59632fc3497922c99de847e4802fb89db05`, parent frozen manifest `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307`, 104 members. Every member's SHA-256 and length verified; no unlisted file; byte-identical to the v1 runtime's kit (`vectors/phase0-custody.json`).
- **Re-verified at the end** (`runs/final-custody.json`: PASS; charter SHA-256 `b93f3ff8…`, requirements SHA-256 `7190eccb…`). Charter and requirements equal the v1 runtime's apart from the runtime path.
- **Kit delta.** Against my own source41 custody rows, exactly two documents changed, both read in full: `foundation/enumeration-contract.v1.md` and `foundation/execution-inputs-contract.v1.md`.

## Continuation record: what was reused and what was executed here

- **The copy.** `output/` was verified equal file-for-file to the v1 output (4566 files).
- **What v1 finished.** Everything through its final phase 4–9 vectors and retention negatives. It had not finished the pre/post matrix, provenance, final custody, the HC-50 control rebuild, phase 0 custody or any checkpoint.
- **Rebinding.** Before any execution, `output/rebind_v2.py` rebound the copied executable code from the v1 root to this runtime (`output/rebind-v2-manifest.json`: 100 files, 120 occurrences, including the unchanged-helper execution copy `preserved/pre-s42`). Nothing wrote into the v1 runtime.
- **Executed fresh in v2** (`logs/s42v2-*`):
  - the HC-50 control rebuild;
  - replay of all 71 stores;
  - from-scratch closure of all positives;
  - export replay and the per-record admission log;
  - the unchanged-vs-corrected pre/post matrix;
  - provenance and final custody;
  - phase 0 custody and phases 1–3 vectors;
  - checkpoints 0–11 and this review.
- **Reused as exact v1 measurements** (same code and store bytes; logs `s42-original*`, `s42-fin-*`, `preserved/pre-s42/logs/s42-pre-*`):
  - the unchanged-helper run and store builds;
  - tamper controls and discovery/mode vectors;
  - phases 4–8 vectors, graph query and run termination;
  - retention negatives.
- **Own execution errors in v2, preserved.** `logs/s42v2-fin2.7.final_custody.log` failed because I ran final custody before phase 0 had produced `vectors/phase0-custody.json`. It was re-run after phase 0 (`logs/s42v2-cp.5.final_custody.log`: PASS).

## How the reconstruction was carried out

1. **Port.** My own source41 helpers were ported with only the runtime root rebound (`port-manifest.json`).
2. **Unchanged run first.** They ran unchanged against source42 (`logs/s42-original*`), and the output tree was preserved byte-for-byte (`preserved/s42-original-state/`) before any change. That state is re-executable at `preserved/pre-s42/`.
3. **Correct from the kit.** Helpers were corrected only from the kit (`tools/hc_source42.py`):

| HC | What was wrong | Source42 selector | Original failure (preserved) |
|---|---|---|---|
| HC-47 | Enumeration bindings put the U-1 marker into `programEntry` on `default-unit` bindings (`tsconfig.json`, `Cargo.toml`) and labelled the U-9 syntax default `explicit-plan-selection`. Admission had no null rule, no derived-entry join against the retained `entryConfigPath`, no explicit-entry join and no default-unit cardinality check. | `enumeration-contract.v1.md` s1 lines 20-47; `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description` (unchanged since source41) | `logs/s42-original.7.from_scratch.log`: all 27 admit; the rebuilt stores have run ids identical to my 27 source41 exports |
| HC-48 | View-attribution candidates were also drawn from the claimed `selectedRefs`; a `selectedRefs` view on no complete receipt was not refused `EXECUTION_INPUTS_SELECTED_COVER` | `execution-inputs-contract.v1.md` s3 line 53 | unchanged code refuses that control only as `EXECUTION_INPUTS_REF_POINTER` |
| HC-49 | Runtime adaptations: a discovery vector path to the source41 layout; the negatives' pre column; custody hashes; s42 pre/post and provenance tools; the v2 root rebinding | — | `logs/s42-original-disc.0.discovery_vectors.log` (FileNotFoundError) |
| HC-50 | Own control error: the first second-default-binding control lacked a stage observation and was refused by a schema fault of my own capture, masking the law under test | own tool | `logs/s42-fin-mut.0.replay_all.log` |

## Own source41 defect, measured

- **What the unchanged run shows.** The unchanged helpers rebuild all 27 positives with the run ids of my source41 exports and admit them. Their retained enumeration plans carry `programEntry: "tsconfig.json"` (17 ts-/cmp-* Runs) and `programEntry: "Cargo.toml"` (6 rust-* Runs) on `default-unit` bindings.
- **What the corrected code does with those exact original bytes** (`selfcheck/s42-prepost-matrix.json`): it refuses the 23 TS/cmp/Rust positives `ENUMERATION_BINDING_PROGRAM_ENTRY:…:default-unit-non-null` and admits the 4 syntax positives. Their `explicit-plan-selection` spelling is unrefused by any published rule (advisory A-s42-3).
- **Rebuilt positives.** They carry `programEntry: null` on default bindings and a `default-unit` U-9 binding. Both codes admit all 27, and every identity changed.

## Claimed complete positives and exact exports

Each export is `runs/<run>.store.json` (object table plus every blob). Each Run also has a from-scratch closure (`runs/<run>.replay.fromscratch.json`), an export replay (`runs/<run>.replay-export.json`) and an admission log (`runs/<run>.records.json`).

| Run | runId |
|---|---|
| cmp-base | `run3:88d6ffc50e2a8d517717056b7c0ccfa3c072be624f6919b733b17514fb987e54` |
| cmp-budget | `run3:75ec6326c6d05a14b38c353d1f777f30a241ad4063f8343e044ddcce914bc32b` |
| cmp-code-det2 | `run3:7a497d82a68ba4e0d00a4d3adcb0f13a7cd9ce649290afc2923113c65386519d` |
| cmp-code-detc | `run3:fea6a4a34d5db63516c21d76b01d42104d694c416b704b83ca06da24168d8ace` |
| cmp-code | `run3:a3bfb0189bb733319998b7e73b591c224af02ab5590807be1f77dc65eea621ee` |
| cmp-empty | `run3:30fa2312888fb3f713f93c16d9d738ceab9f783b1f70cb90ca08887c78aea57c` |
| cmp-evidence | `run3:246a66a78dd5ae2295ca9acddd47da72e8a440597da15db82c45991ba84ff455` |
| cmp-gbase | `run3:aa2f9d693435f628c7a78954caadd4c29555c098b147b0a84b658e00c76b2855` |
| cmp-gevidence | `run3:38035e4aa373bf5d28c6d2c4d09d3fed5504f8e79fb26a5a9292716d802db796` |
| cmp-gmissing | `run3:f835ecc0f6d25ffced088711d86fbf7a79ef1eeca587a9037c52d3e0cb914737` |
| cmp-hidden | `run3:e6fa7975683e9fc3f1ec01cc5cfd4104151d24c3a7a3de4862bbb0d2486614ef` |
| cmp-policy | `run3:593cad18396ebc40f76f84eefb3d3703d8b381ff8cf0cf82a0cc422db79762e2` |
| cmp-scope | `run3:c279f39f370b7f41dd2bb141b746d45a62d69cef16071c47aa92851a78cf3ec6` |
| cmp-waiver | `run3:326ea9f0dabde3ec9e1e64d9255da463335816d449641ab3f0e4cf810896c96c` |
| rust-ambiguous | `run3:bb9ad3b2ae295becbe0ef721b7db00b8c00e12ba633a1f5493547d49e7f33536` |
| rust-extra-unit | `run3:58b08c269351e27614c2f828172cdbbd304c7ab6e29cdb72a25e23790419407a` |
| rust-mixed-clones-required | `run3:359566e8cc476189d433257117f30edea16cfdbc1863e21b17a8e8df7d32398c` |
| rust-mixed | `run3:0552d2c2279cdf940d5826f8f58bf64d78f63a3014838583b47eec2605aa1db7` |
| rust-partial | `run3:77be524d9da78ecfbb0bc0b643f65ddf3e9b6679b940c7bae7ff9588aef60db3` |
| rust-same-file-2021 | `run3:f0293580d253e8f73221970cfa38d87a7006580ba15fae17522f38aa85ab050b` |
| syntax-code | `run3:fffddf0afc41de4ba5053bc5737bb4c2f2bf7e372174891387b31a8094d03d69` |
| syntax-data | `run3:1113e38c6bbcd36d6c84cfebf59293b4eb667d1360d51bb9e78955563f06197d` |
| syntax-mixed-disclosed | `run3:10132b141bb04b7084879388e02561f51182012b00ab3ab05706162a043b68f3` |
| syntax-mixed-omitted | `run3:e401b7165eae4ca77d3de06731450356f1b919162c91a07d71ae5112af6ba43a` |
| ts-clones-required | `run3:cd4a8fe63d4e0fee7179fc7894bd88d1d323c7b16e1c03fdc53938df1c5ca836` |
| ts-fail | `run3:f94885357fa9eb41d92d061283cd83a6e58f2a26893890a219578fb087db321a` |
| ts-pass | `run3:54a0a7cfba1b7061160c481e51cde4a54bae9c0a50a57e63475d4b4a35a9d2fa` |

The designed negative `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.

**From-scratch command** (reads only exported stores and the kit, one fresh process per Run):
`cd /private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py`

## Independent vectors and results

| Area | Result | Artifact / log (runtime) |
|---|---|---|
| C/H, CVE1, lexical admission, raw vs parsed, acyclic joins | 0 failures | `vectors/phase1-canonical.json`, `logs/s42v2-cp.1` (v2) |
| capability manifests, four gates | 5 positives, 19 negatives, 0 failures | `logs/s42v2-cp.2` (v2) |
| protocol3 traces | all 34 rows exercised, pairwise disjoint | `logs/s42v2-cp.3` (v2) |
| relation/rung table, RC-0..RC-6, cell-outcome derivation | 17 rows, 16 RC vectors, 10 outcome vectors, 0 failures | `logs/s42-fin-p4to9.0` (v1) |
| discovery, U-0, U-1/s1.2 modes, U-4b, U-8, U-9 | 29 vectors, 0 failures | `logs/s42-fin-disc.0` (v1) |
| phases 5, 6, 7 and 8 vectors | 0 failures; 45/45 public termination goldens | `logs/s42-fin-p4to9.1`–`.5` (v1) |
| analysis-Run termination | 28 Runs, 9 candidate checks, 30 host compositions, 0 failures | `logs/s42-fin-p4to9.8` (v1) |
| graph query | 53 vectors, 0 failures | `logs/s42-fin-p4to9.6` (v1) |
| from-scratch closure | 27/27 positives admit through all four stages; designed negative refuses | `logs/s42v2-fin2.2` (v2) |
| export replay | 27/27 byte-equal recomputed proofs | `logs/s42v2-fin2.3` (v2) |
| per-record admission log | 27 positives, 0 failures | `logs/s42v2-fin2.4` (v2) |
| mutation replay | 71 stores: 29 admit (27 positives + 2 lawful controls), 42 refuse | `logs/s42v2-fin2.1` (v2) |
| tamper | every semantic control refused by replay; every identity control refused before replay | `logs/s42-fin-tamper.*` (v1) |
| retention/reference-class negatives | 32 constructed, all pass | `logs/s42-fin-neg.0` (v1) |
| unchanged vs corrected helpers | table below | `logs/s42v2-fin2.5` (v2) |

| Control | Unchanged helpers | Corrected helpers |
|---|---|---|
| `ts-pass~default-unit-program-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null` |
| `rust-mixed~default-unit-program-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null` |
| `ts-pass~explicit-entry-not-graph-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:explicit-entry` |
| `syntax-code~second-default-unit-binding` | `ENUMERATION_INVENTORY_MISSING_RECORD` | `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY:0` |
| `syntax-code~selected-view-not-on-receipt` | `EXECUTION_INPUTS_REF_POINTER` | `EXECUTION_INPUTS_SELECTED_COVER:view-not-on-receipt` |
| `syntax-code~unit-kind-other-family`, `~unit-root-external-sentinel`, `~row-view-omitted`, `ts-pass~unit-kind-not-mode-projection` | refused (source41 laws already corrected) | refused on the same laws |

## Issues

### newMustIssues

None.

### newShouldIssues

None.

### Disposition of my own source41 results

- **The source41 claimed positives and their ACCEPT recommendation are superseded** by an own helper omission (HC-47, measured above). This is not a kit gap: the schema description has stated the law since source41.
- **Source41 view attribution (HC-42)** is tightened by the source42 text (HC-48).
- **Source41 advisories** are carried below; their owner documents are unchanged.

### Advisories (nonblocking)

- **A-c1.** Internal refusal names no kit owner publishes are still spelled `cb24.*`; `blind-review.json#/advisories` lists the measured set.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. The successor D9 artifact is a disclosed live obligation (native lines 3313-3327).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5 (native lines 165-172, 741-746, 797-799, 1070-1072, 1842-1847).
- **A-v2-1.** Composition s7 does not scope typed-prefix closure explicitly to outputs (s7 line 74; s5 line 54; identity lines 597-600, 627-631).
- **A-v2-2.** `policy-derivation3` is outside the reachable output set (composition s7 lines 70, 76).
- **A-v2-3.** Identity s3 (lines 441-467) calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** run-termination s7.6 step 1 (line 330) names no key; the s6 key (line 173) is applied at both boundaries.
- **A-s41-2.** U-1's "an omitted value defaults to false" (native lines 656-659) reads against s1.2's `checkJs` fallback (lines 524-526, 562-563); s1.2 is applied.
- **A-s42-1 (new).** Enumeration contract s1 line 21 makes `default-unit` at most one binding per cell at ordinal 0 but names no refusal key; the reconstruction uses its own `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY` (`runs/syntax-code~second-default-unit-binding`).
- **A-s42-2 (new).** The contract names `ENUMERATION_BINDING_PROGRAM_ENTRY` for a non-null default `programEntry` (lines 26, 37) but not for a derived-entry or explicit-entry mismatch against the retained `entryConfigPath`. Native U-0 (line 650) attributes that join to the same key, which is applied to all three (`runs/ts-pass~explicit-entry-not-graph-entry`).
- **A-s42-3 (new).** Lines 21-22 make a sole syntax-only binding `default-unit`, but no published rule or key refuses the `explicit-plan-selection` spelling with `programEntry: null`, and the two spellings mint different enumeration-plan digests.
  - Measured: the 4 original syntax positives with the explicit spelling admit under the corrected code, with identities different from the rebuilt `default-unit` ones.
  - Determinate by text, unenforced; no refusal is invented.

## What required invention

No record, identity or refusal outcome had to be invented. Named readings, each measured or stated beside its alternative:
- A-s42-1: a key for the cardinality refusal;
- A-s42-2: one key for all three entry joins;
- A-s42-3: `default-unit` for the sole syntax binding;
- carried: A-s41-1, A-s41-2, A-v2-1, A-n6.

## Limitations

- run-termination s7.5 row 2 and s5 stage-terminal carriers are exercised by vectors, not on built Runs.
- The retained-closure walker names what it delegates to owner graph admission, which runs as its own stage.
- The census pairs `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` occur in no constructed positive and have no negative.
- No positive uses an explicit-plan-selection binding, a js-synthesized or jsconfig default binding, or a Rust explicit binding. Those `programEntry` branches are exercised only by the explicit-entry control and by reading.
- **Not constructed by any original requirement; read but not exercised:** PolicyTestSuiteV2, the U-8 boundary-inventory superset join, and `target-attribution-v2` occupancy companions.
- `discovery-defaults.py` was neither read nor used.
- Root admission of the exported bytes is unobserved.
- **Product qualification.** This review makes no product qualification claim and no implementation authorization; all future-qualification items remain unperformed.

## Retained outputs

- **Machine-readable review:** `blind-review.json` (verdict basis, issues, advisories with selectors and measurements, dispositions, HC records, positives with run ids, `requirementStatus`).
- **Checkpoints and status:** `checkpoints/phase-0.json` … `phase-11.json`; `requirement-status.json`.
- **Notes:**
  - `notes/00-session-standing.md` (including the v2 continuation record);
  - `notes/01-source42-law-deltas.md`;
  - `notes/07-phase7-reconstruction.md`;
  - `notes/08-subsystem-owners.md`;
  - `notes/09-reconstruction.md`;
  - `notes/10-gaps.md`.
- **Code:** `ref/`, `builders/`, `tools/`, `vectors/`.
- **Results and logs:** `runs/`, `envelopes/`, `traces/`, `negatives/`, `selfcheck/`, `logs/`.
- **Own history:** `preserved/`.
