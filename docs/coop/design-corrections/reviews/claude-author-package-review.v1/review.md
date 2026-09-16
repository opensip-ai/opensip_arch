I have completed the review. Writing up now.

---

# Independent Review — Codex author follow-up v2

**Reviewer:** fresh actual Claude (Opus 5) session, non-blind, no prior transcripts read, no other agents used.
**Date:** 2026-09-11

## 1. Bindings (independently verified, not taken from dispatch)

| Object | Expected SHA-256 | Verified |
|---|---|---|
| `input-manifest.json` | `da22d2d5…9792b` | ✅ matches; binds **136** files |
| Supplemental tree | — | ✅ **136/136** hash-match, **0** mismatched, **0** missing, **0** untracked-on-disk |
| Package `artifact-manifest.json` | `c533aa6a…16c4` | ✅ matches; declares **97** files |
| Package tree | — | ✅ **97/97** hash-match; only extra on disk is the manifest itself (consistent with its `standing`) |
| Candidate25 manifest (`candidate-subject.v25.json`) | `fa8cdc79…a536d` | ✅ matches; **12869** files, 735,108,187 bytes |
| Candidate25 tree | — | ✅ **12869/12869** hash-match, 0 mismatch, 0 missing |

The package's `source-manifest.json` internally pins the same candidate SHA, and `verify-package.py` re-asserts it. All three bindings hold. This report is bound to those three SHAs.

## 2. What I executed, and the exact first-refusal boundaries

`verify-package.py` rerun into a **new** scratch directory: `rc=0`, 22.2 s, all four groups `True` — **7 positive Runs** (1 TS + 4 normalized + 2 Rust selection) and **3 negative controls**, `sourceFilesVerified: 12869`, `packageFilesVerified: 97`.

I did not stop at the exit code. I compared **all 18 regenerated artifacts** (4 reports, 4 claims, 10 derived `exact-inputs` stores) against the packaged `*-owner/` outputs: **18/18 byte-identical**. The package is fully reproducible on its replay path.

**First-refusal boundaries encountered:**

| # | Boundary | Exact refusal | Resolution |
|---|---|---|---|
| B-1 | Tooling | `Bash` allow-list is `Bash(python3 *)` only. `shasum -a 256 …`, `/tmp/opensip-architecture-review-env/bin/python --version`, and `ls` outside the four working dirs were all refused | Routed everything through system `python3` (3.14.6), sub-launching the env Python (3.12 + jsonschema) via `subprocess` — the path the request anticipated |
| B-2 | Verifier | `verify-package.py:12` — `assert not a.out.exists(),'Use a new output directory; preserve earlier evidence.'` | Complied; used a fresh scratch dir |
| B-3 | Probe scripts | `probe-mixed-universe-view.py:4`, `check-author-properties.py:5`, `check-author-query.py:4` resolve `ROOT.parent/'candidate-subject.v25'`, which does not exist in the delivered layout, and each **writes into its own frozen package directory** | Did **not** run them as shipped; re-implemented in scratch with corrected paths |
| B-4 | Query checks | `check-author-query.py:7` imports `ROOT.parent/'check-blind13-exported-graphs.v4.py'` — absent from the package, from candidate25, **and from `author-workspace-history.tar.gz`** | Could not regenerate; re-verified assertions against retained observations only |

## 3. Substantive findings

### 3.1 AR-01 — default TypeScript `programEntry` / root: **correct, and normatively enforced**

The three `ts_pilot.py.patch` hunks are `programEntry: None`, `workspace_unit("", …)`, and adding `cov_c_u` to the coverage set. All three are grounded in frozen bytes, and I verified the grounding rather than the prose:

- **`programEntry: null` is not a convention — the owner enforces it.** `enumeration_model.v1.py:707-712`: if `entry is not None` **and** `provenance == "default-unit"`, the owner raises `ENUMERATION_BINDING_PROGRAM_ENTRY`. Lines 719-722 then *derive* the U-1 marker via `_u1_entry(_unit_for_cell(...))` and compare it to the retained `TypeScriptConfigGraphV1.entryConfigPath`. The patch comment ("derive the marker from retained membership/config graph") is exactly right. The schema description in `enumeration-plan.schema.v1.json:387` independently states "U-1 default uses null."
- **`rootPath: ""` matches frozen discovery.** `discovery-defaults.py:55-56` (`ROOT_SENTINEL='.'`, `INTERNAL_ROOT=''`), `_dir_of` = `rpartition('/')[0]`, and `enumerate_units(['tsconfig.json'])` → `{'unitDirs': ['']}`. Confirmed by execution.
- **`cov_c_u` is consumed, not retained-and-ignored.** It is the `coverage:"unknown"` / `language-tier-unsupported` / `capability-missing` partition over `dialect_bad`. In the replayed TS proof it produces a distinct `executionDeficiencies` carrier on coverage `cc962fa0c1…` with `nativeCause: capability-missing`. Its two subject sets (`dialect_ok`/`dialect_bad`) are disjoint, satisfying `coveragePartitionLaw`.

**But AR-01 review question 3 ("are additional-program bindings kept distinct from default-unit bindings?") cannot be answered from this package.** `ts_pilot.py:27-39` hardcodes `"ordinal": 0` and `"provenance": "default-unit"`, so `_binding` can only ever emit a default-unit binding; there is no additional-program binding to be distinct from. The sole call site (`ts_pilot.py:326`) still passes `"tsconfig.json"` into a now-**dead `program_entry` parameter**. The hardcode is lawful, but the parameter is misleading dead code and the fixture structurally cannot express the non-default case.

**And the rule has no negative control anywhere.** `ENUMERATION_BINDING_PROGRAM_ENTRY` occurs **only** in `enumeration_model.v1.py` (5×) across all of candidate25 outside `reviews/`. Neither the frozen reference checkers nor this package demonstrates the refusal.

### 3.2 Root / view attribution: the author's "documentation clarity" question understates a real defect

The author files this as a reviewer question, not a defect. On the evidence I think that is too generous to the contract, and I record it as a normative under-specification with a reproducible counterexample.

`WorkspaceUnitV2.rootPath` is declared as `{"type":"string","maxLength":4096}` — no `minLength`, no pattern, no description. `native-evidence.md:579-591` likewise never states the spelling. I confirmed with `jsonschema` that **both `""` and `"."` validate**. Yet the operative semantics require exactly `""`, and `discovery-defaults.spell_root()` exists precisely because *other* records need the `"."` spelling (`native_evidence_model.v2.py:4171,4179` emit `u["rootPath"] or "."` as `workspaceRoot`).

Measured consequences of the schema-valid wrong spelling:

```
_under_unit(path, root)  [native_evidence_model.v2.py:2024]
  rootPath=''  -> [('src/a.ts', True),  ('src/b.ts', True),  ('index.ts', True)]
  rootPath='.' -> [('src/a.ts', False), ('src/b.ts', False), ('index.ts', False)]

_rel(path, root)  [native_evidence_model.v2.py:2028]
  rootPath=''  -> ['src/a.ts', 'src/b.ts', 'index.ts']
  rootPath='.' -> ['c/a.ts',  'c/b.ts',  'dex.ts']        <-- silent string corruption

_unit_for_cell(...) / _u1_entry(...)  [enumeration_model.v1.py:248,432]
  rootPath=''  -> FOUND | derived U-1 entry 'tsconfig.json' | fault: none
  rootPath='.' -> None  | derived U-1 entry  None          | fault: ENUMERATION_BINDING_PROGRAM_ENTRY
```

So a conforming implementer who writes `"."` gets either a **silently empty analysis** (every file demoted to `syntax-only`/`no-program-unit-for-language`, no fault raised) or a **misattributed fault** blaming `PROGRAM_ENTRY` for what is a root-spelling error. `enumeration_model._internal_root` normalizes `"."`→`""` for the *cell's* `workspaceRoot` but the *unit's* `rootPath` is compared unnormalized — the asymmetry is deliberate but undocumented. This is exactly the class of ambiguity that will diverge an independent consumer-B reconstruction, which AR-03/AR-05 still require.

### 3.3 AR-02 — predicate scope and per-Coverage carriers: **correct, and the controls are genuinely targeted**

The frozen owner independently derives `scopeIds` (`evaluator_composition_model.v3.py:149` for atoms, `:135` union for combinators) and `compare_complete_replay` (`:202-207`) requires **whole-object equality of the entire proof**, plus every expected object and blob — not a field subset. That answers AR-04's "complete expected outputs compared" affirmatively at the code level.

Rather than accept `reason == EVALUATOR_COMPLETE_PROOF_REPLAY`, I diffed each control's claimed proof against the recomputed proof:

| Control | Differing selector(s) | Reading |
|---|---|---|
| `severity` | `proof.findingIds[0]`, `proof.ruleResults[0].findingIds[0]` | finding digest moves with severity — intended |
| `unrelated-scope` | `proof.predicateProofs[0].scopeIds` — claimed **2**, recomputed **1**; extra `scope2:0c37b903…` | **directly validates the AR-02 scope correction** |
| `collapsed-deficiencies` | `proof.executionDeficiencies` — claimed **1** bundled (3 inputRefs), recomputed **2** separate (1 coverage each) | **reproduces the pre-patch behaviour and shows the owner refuses it** |

`build-semantic-controls.py:12-28` confirms these are true remints: each mutation recomputes proof → evidence → seal → run identities and **deletes the superseded records** (`:27`). That is why they legitimately `ADMIT` structurally and `REFUSE` semantically.

**Coverage gap:** operations across all seven Runs are only `exists` and `none`. **No `and`/`or`/`not` appears anywhere**, so the combinator hunks of `evaluator.py.patch` (`evaluator.py:207` and `:222`) are never executed by the shipped evidence. `eval_atom` also raises `NotImplementedError` for `count-at-most` and `all-covered` (`evaluator.py:157-158`). Scope diversity is thin: 6 of 7 Runs have a single distinct scope tuple of size 1; only `rust-partial` discriminates (sizes {0,1}). The correction is validated — but by the negative control, not by the positives.

### 3.4 Evidential weight is not uniform across the seven Runs

`build-normalized-examples6.py:125` and `build-rust-selection-examples.py:138` call `R.derive(...)` — the **frozen** `evaluator_replay_model.v3.py` — to produce the final proof. `build-checkpoint3.py` instead routes through `runs.seal_graph` → `evaluator.compose_proof`, the **author's own** helper.

So only **checkpoint3 (TS)** is a two-implementation agreement; the other six are determinism/self-consistency checks of the frozen owner against itself. The author does disclose this (README ¶5; AR-04 `authorDisposition`: "no independent derivation claim"), so the labelling is **accurate** — but the README's flat "seven synthetic Runs … complete semantic replay" invites equal weighting, and it should not be read that way. The three negative controls derive from the TS store, so they inherit the stronger position.

### 3.5 AR-06 — mixed-universe refusal: **claim correct, citation imprecise**

My independent replication (corrected paths, scratch-only writes) reproduced `mixed-universe-view.probe.json` **exactly**, including `runId: run3:bb3f0c9c…`: unmerged → `ADMIT`; merged → `captureResult: REFUSE ["EXECUTION_INPUTS_COVERAGE_DERIVE"]`, `semantic: REFUSE`. The refusal is a real, pre-existing, codified boundary — `execution_inputs_model.v1.py:1094-1096, 1201-1211` — so "no new normative defect demonstrated" is correct.

However, README ¶13 and AR-06 cite **"execution-inputs contract §3"**. §3 is *Stage ordinal and receipts*; it does state the per-scope `sourceUniverse` vs binding-U rule, but the clause the probe actually trips is **§5 *Native Coverage accounts (derived)*** ("from **all** owner `CoverageResultV3` entries of **this** cell/program's returned views … and **U**"). The citation should name §5 and the observed refusal code.

On the underlying question: the contract nowhere states plainly that *an evidence view referenced by a cell binding must be single-universe*. `coveragePartitionLaw` says a view is "one producer's interpretation" and keys on source/target universe, but permits multiple partitions per view. **The author's request for a normative clarification on per-universe view attribution is well-founded and I endorse it.**

### 3.6 Rust selection properties: **claims true, but the published evidence does not establish them**

My re-implementation reproduced `author-properties.json` **exactly** (`rustComparisons` and `partialRust` both identical). The script does read selected retained evidence (Run → evidence → `viewIds` → facts → payload, plus the universe H preimage), not builder metadata flags — that claim is accurate. `partialRust` re-verified: verdict `indeterminate`, **0** clone facts, `coverage:"unknown"`, `input-closure-incomplete` / `body-language-owner-unenumerated`.

But I found the published property evidence under-determines the README's causal claim. Diffing the three universe payloads, **the only differing field is `sourceUnitOwnershipId`** — `edition`, `cfgSets`, `unifiedFeaturesId`, `crateRootPaths`, `lockfileIdentity`, `rustflags` are byte-identical across lib/bin/lib-only. The `editionMap` that `author-properties.json` publishes is the same in all three, so a reviewer reading that file alone cannot verify "different selected editions."

I resolved the ownership records to settle it. The claim **is** true:

```
units (identical in all three):
  alpha      lib  targetEdition: null   -> falls back to crate edition 2018
  alpha-bin  bin  targetEdition: 2021
selectedUnitIds:
  lib       = [alpha-lib(->2018), hashy-lib]
  bin       = [alpha-bin(2021),   hashy-lib]   <-- effective edition changes 2018->2021
  lib-only  = [alpha-lib(->2018)]              <-- effective edition unchanged
```

So body identity changing lib→bin and holding lib→lib-only is exactly the stated property. The defect is evidential, not substantive: `author-properties.json` should publish `selectedUnitIds` and the effective `targetEdition` per selected unit.

### 3.7 Query checks: assertions hold, but are not regenerable

All seven assertions re-verify independently against the frozen `observations.json`. The honesty framing holds up: the empty incoming traversal is `countBasis: exact, truncated: false` yet carries `resolutionLimitations: [{"kind":"unsupported-rung-omitted", …}]`, so it is a statement about the retained graph, not global absence. `bounded` returns `items: []` with `termination.class: indeterminate` / `QUERY.COMPLETENESS_UNMET`. `wrong-run` → `IDENTITY.UNKNOWN`/`QUERY.VIEW_UNKNOWN`; `purged` → `HOST.IO_FAILURE`/`evidence.purged` with an explicit "cannot be treated as an empty graph" remedy.

These re-verify the author's **own recorded observations**. Because of B-4 I could not regenerate them, and `verify-package.py` does not re-execute them either — it runs only `check-export.v4.py` across the four groups.

### 3.8 Custody gaps affecting AR-03 / AR-05

Two cited chains do not resolve against the frozen bytes a reviewer receives:

- `original-requirement-handoff.json` pins `originalRequirementsSha256: 08dffd7f…5196e`. I searched **every file** in candidate25, in the supplemental inputs, and **every member of `author-workspace-history.tar.gz`**: **zero hits**. The 123 requirements cannot be checked against their cited original.
- AR-03's evidence pointers `../consumer-b.v13-pilot-admission.v6/root-owner-assessment.v1` and `.v7/root-partial-assessment.v1` resolve to nothing; no path containing `consumer-b.v13-pilot-admission` exists in either frozen tree. `starting-custody.json` points at a live working path (`/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output`).

The handoff content itself is disciplined — **123/123** `PENDING-ORIGINAL-INDEPENDENT-RECONSTRUCTION`, 8 standing rules, 3 future items, 29 items carrying `authorSupport` links all stamped "not a declaration that this requirement has been independently executed." The problem is verifiability, not intent.

Separately, README ¶21 says "The full working history is in `author-workspace-history.tar.gz`." It is not full: the transport module `check-blind13-exported-graphs.v4.py` that `check-author-query.py` requires is absent from the archive (454 entries, 0 `blind13` matches).

### 3.9 The thirty residuals

All thirty bind correctly: 30 unique IDs, selectors `/items/0`–`/items/29` all in range, every `sourceCorrection` verbatim in the pinned source (`8f7d940e…` — **verified present and matching** in candidate25), **38/38 evidence refs** resolve and hash-match, every ref `resolveAgainst: "frozen candidate25"`. Discipline is uniform and correct: `independentGrade: PENDING` ×30, `applied: false` ×30, `historicalLimitationReclassified: false` ×30.

Reviewing the reasoning rather than the count: **30 distinct rationales and 30 distinct limits** — not boilerplate. Even the four sharing one `sourceCorrection` (AX6/AX9/MD5/RX2c) carry individually reasoned rationales naming their specific variant. History-preservation is consistently honoured; the `limits` fields repeatedly and correctly refuse to convert a scope change into a repair ("Trust-boundary replacement, not elimination of the old attack class"; "No Python containment claim").

Two observations the package does not state:

- **Concentration risk:** **13 of 30** residuals (RES-EP13-02, -04, -12, -13, -16, -18; IR-EP13-NB-01, -03, -04; AX6, AX9, MD5, RX2c) are disposed by the *same* move — declaring same-process adversarial code outside the TCB. If an application reviewer rejects that single assumption, 43% of the residual set reopens at once. That coupling should be disclosed to AR-07.
- **Zero adverse self-assessments:** all 30 are `proposed-account-supported-with-stated-limits`. Legitimate given the author also proposed them and every grade is `PENDING`, but it carries little independent signal.

### 3.10 Minor / informational

`runs.py:543-545` records `"derivedProof": proof, "claimedProof": proof, "comparison": compare_proof(proof, proof)` — a vacuous self-comparison. It is honestly commented ("first mint equals derived") and I confirmed it does **not** reach any shipped artifact (`replay`, `derivedProof`, `claimedProof`, `comparison` are all absent from `ts.store.json`). Fixture wart only.

`runs.py.patch` corrections are sound and consistent with what I measured in the stores: rustc toolchain version `1.78.0`, grammar-closure custody (bundle manifest + 3 grammars + normalizers), `cfgSets` from `ctx["baseCfg"]`, and `crateRootPaths` changed from directories to actual crate root **files** — which matches the `crateRootPaths: ["crates/alpha/src/lib.rs", …]` I read out of the universe payload. The pre-existing `if False else …` dead conditional at the `configProjectionSha256` site is untouched context, not introduced here.

## 4. Disposition of AR-01 … AR-07

| ID | Disposition | Basis |
|---|---|---|
| **AR-01** | **Accepted with corrections required** | Both fixture corrections follow the normative contract and are *enforced* (`enumeration_model.v1.py:711-712`), not conventional. Q2 (root representation) is upheld and **escalated** to a normative under-specification with a counterexample. Q3 (additional-program distinction) is **not demonstrable** from this package. No negative control exists for the rule. |
| **AR-02** | **Accepted** | Scope derivation and per-Coverage carriers match the owner's independent derivation; whole-proof equality enforced; the three remints are true remints and fail on exactly the intended selectors. Gap: no combinator or `count-at-most`/`all-covered` coverage. |
| **AR-03** | **Cannot be advanced here; custody gap recorded** | Correctly left to original independent consumer B. This review does not and cannot waive it. Its cited evidence does not resolve against frozen bytes (F-02). |
| **AR-04** | **Accepted as author-reference evidence, with weighting caveat** | Complete expected outputs *are* compared (`compare_complete_replay:202-207`), and 18/18 owner artifacts reproduced byte-identically. But 6 of 7 proofs were derived by the frozen owner itself; only TS is a two-implementation agreement. Disclosed by the author; weighting must be preserved downstream. |
| **AR-05** | **Handoff honest; verifiability gap recorded** | 123 + 8 + 3 intact, all `PENDING`, no waiver, `authorSupport` correctly caveated. Blocked from verification by F-01. |
| **AR-06** | **Accepted** | "No new normative defect" is correct — refusal reproduced exactly, including runId, and traced to codified checks. §3 citation should be §5. The per-universe view-attribution clarification request is endorsed; I add the root-spelling clarification (F-04) as a second, better-evidenced one. |
| **AR-07** | **Prepared, not gradeable here** | All 30 residuals bind and are individually reasoned; application acceptance remains separate and untouched. TCB concentration (F-13) should be surfaced before application review. |

## 5. Read / execution coverage (honest)

**Executed:** `verify-package.py` (full, fresh out-dir); full byte-comparison of 18 regenerated vs. packaged owner artifacts; independent replay + proof introspection of all **7** positive Runs; claimed-vs-recomputed proof diffs of all **3** controls; independent replication of the mixed-universe probe; independent re-implementation of `check-author-properties.py` plus resolution of 3 `sourceUnitOwnershipId` preimages; re-assertion of all 7 query checks from retained observations; full structural + hash validation of all 30 residuals (38 evidence refs) and of the 123/8/3 handoff; exhaustive content search of candidate25 + inputs + the 454-entry history archive for two pinned artifacts.

**Read substantively:** all 4 governance docs, `verify-package.py`, `check-export.v4.py`, all **3** source patches in full, all 4 `claims.json`, both `construction.json`, `checkpoint3-owner/report.json`, `semantic-controls1/assessment.json`, `query-checks1/assessment.json` + `purged.json`, `author-properties.json`, all 30 residual items, `original-requirement-handoff.json`; plus frozen candidate25: `identity-model.v3.py` (key regions), `evaluator_replay_model.v3.py` (full), `evaluator_composition_model.v3.py` (key regions), `enumeration_model.v1.py` (key regions), `native_evidence_model.v2.py` (key regions), `discovery-defaults.py`, `execution-inputs-contract.v1.md` §3-§6, `coveragePartitionLaw`, `WorkspaceUnitV2` schema.

**Not read:** 21 of 24 `author-helpers/*.py` (~370 KB) — I read `evaluator.py`, `runs.py`, `ts_pilot.py` regions only. These are construction-path only and are **not** in the verification path (`check-export.v4.py` imports the frozen owner and never consumer helpers), which is why I prioritised the owner. The 10 `*.store.json` (~14 MB) and `source-manifest.json` were processed programmatically, not read as text. `author-workspace-history.tar.gz` was enumerated and content-searched, not reviewed.

**Not attempted:** reconstructing any of the seven Runs from source (impossible as shipped — B-3); regenerating query observations (B-4); any blind-consumer reconstruction, application grading, or product-qualification inference.

## 6. Acceptance

**This specific author package is acceptable as an author-assisted reference checkpoint against candidate25 `fa8cdc79…a536d`**, subject to the corrections below. Its central technical claims are true and I verified them by independent execution rather than by reading its reports: the corrections follow the normative laws, the reused frozen derivation is labelled accurately, the asserted properties are load-bearing rather than unused retained data, and the negative controls fail for exactly the intended reasons.

**Must-correct before this package can serve its stated purpose of enabling independent review:** F-01, F-02, F-03 (custody/reproducibility of the AR-03/AR-05 handoff and the query evidence).
**Should-correct:** F-04 (normative clarification + counterexample), F-05, F-06, F-07, F-08, F-09, F-10.

**Explicitly not granted, and not inferable from anything above:** AR-03/AR-05 blind consumer-B reconstruction of all 123 requirements + 8 standing constraints + 3 future items; AR-07 application acceptance; any product qualification or implementation readiness. Acceptance is bound to candidate25 bytes `fa8cdc79…a536d` and **does not transfer** to any separately reviewed XA/COV successor. This package must not be supplied to a consumer described as blind.

---

```json
{
  "report": {
    "reviewer": "fresh independent actual Claude (Opus 5) session, non-blind author-package review",
    "date": "2026-09-11",
    "bindings": {
      "inputManifestSha256": "da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b",
      "inputManifestVerified": true,
      "supplementalFilesBound": 136,
      "supplementalFilesVerified": 136,
      "supplementalMismatches": 0,
      "supplementalUntrackedOnDisk": 0,
      "packageManifestSha256": "c533aa6ab8939e6ecf710d217233aea8818fd1783e770b0db5ba81e375d316c4",
      "packageManifestVerified": true,
      "packageFilesBound": 97,
      "packageFilesVerified": 97,
      "candidateManifestSha256": "fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d",
      "candidateManifestVerified": true,
      "candidateFilesBound": 12869,
      "candidateFilesVerified": 12869,
      "candidateMismatches": 0,
      "frozenInputsModified": false,
      "writesConfinedToScratch": true
    },
    "verifierRerun": {
      "command": "/tmp/opensip-architecture-review-env/bin/python -I -B verify-package.py --source /tmp/opensip-design-corrections/candidate-subject.v25 --out <new scratch dir>",
      "returnCode": 0,
      "seconds": 22.2,
      "groups": [
        {"group": "checkpoint3", "negative": false, "passed": true, "count": 1, "reportSha256": "066de3eae5a2dedf8417bc1c88ca5c386854f3947c36ae868d94caa72b50662d"},
        {"group": "normalized-examples6", "negative": false, "passed": true, "count": 4, "reportSha256": "22f55929e5efad421dfc2094c97f802f413fc83fea0dac33aa15ec059f9c3aba"},
        {"group": "rust-selection-examples1", "negative": false, "passed": true, "count": 2, "reportSha256": "a02dd271cfef5470d48f163b1f61664f55e39adaf69adf0139521468ac789573"},
        {"group": "semantic-controls1", "negative": true, "passed": true, "count": 3, "reportSha256": "922ec3ffbf9ffe71aa1222a387ebb6f87597d4d312f9bc512b1f62fe9b29c1c9"}
      ],
      "positiveRuns": 7,
      "negativeControls": 3,
      "ownerArtifactsByteCompared": 18,
      "ownerArtifactsIdentical": 18,
      "shallowSuccessOnly": false
    },
    "firstRefusalBoundaries": [
      {"id": "B-1", "kind": "tooling", "detail": "Bash allow-list is Bash(python3 *). Refused: 'shasum -a 256 ...', '/tmp/opensip-architecture-review-env/bin/python --version', 'ls /tmp/opensip-design-corrections/'. Resolution: system python3 subprocess-launching the jsonschema env python."},
      {"id": "B-2", "kind": "verifier", "selector": "verify-package.py:12", "detail": "assert not a.out.exists(),'Use a new output directory; preserve earlier evidence.' Complied with a fresh scratch directory."},
      {"id": "B-3", "kind": "packaged-script", "selector": "probe-mixed-universe-view.py:4 / check-author-properties.py:5 / check-author-query.py:4", "detail": "Resolve ROOT.parent/'candidate-subject.v25' (nonexistent in delivered layout) and write into their own frozen package directory. Not run as shipped; re-implemented in scratch."},
      {"id": "B-4", "kind": "missing-dependency", "selector": "check-author-query.py:7", "detail": "Imports ROOT.parent/'check-blind13-exported-graphs.v4.py', absent from package, candidate25 and the history archive. Query observations not regenerable."}
    ],
    "findings": [
      {
        "id": "F-01",
        "severity": "major",
        "area": "custody / AR-03 / AR-05",
        "path": "original-requirement-handoff.json",
        "selector": "$.originalRequirementsSha256",
        "claim": "'The complete original charter, including all 123 requirements, 8 standing rules and 3 future items, remains intact.'",
        "evidence": "Pinned SHA 08dffd7f73d2e8d31830fae66818920488ab5c17d0eb82f6a60576f3bec5196e produces ZERO hits across every file of candidate-subject.v25, every file of the supplemental inputs tree, and every one of the 454 members of author-workspace-history.tar.gz.",
        "impact": "The 123 enumerated requirements cannot be checked against their cited original, so the non-waivable AR-03/AR-05 charter is unverifiable by a reviewer.",
        "requestedCorrection": "Ship the exact pinned charter bytes inside the frozen package (or inside candidate25) so the SHA resolves."
      },
      {
        "id": "F-02",
        "severity": "major",
        "area": "custody / AR-03",
        "path": "review-queue.json",
        "selector": "$.items[?(@.id=='AR-03')].evidence[0..1]",
        "claim": "AR-03 evidence: '../consumer-b.v13-pilot-admission.v6/root-owner-assessment.v1' and '../consumer-b.v13-pilot-admission.v7/root-partial-assessment.v1'.",
        "evidence": "No path containing 'consumer-b.v13-pilot-admission', 'root-owner-assessment' or 'root-partial-assessment' exists in candidate25 or the supplemental inputs (recursive name search, 0 hits). starting-custody.json $.source points at a live working path /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output.",
        "impact": "The preserved independent-consumer evidence AR-03 rests on is not deliverable to this reviewer; 'The old independent output remains unchanged' is unverifiable.",
        "requestedCorrection": "Freeze and include the referenced consumer-b.v13 v6/v7 assessment artifacts, or replace the pointers with resolvable frozen paths plus SHAs."
      },
      {
        "id": "F-03",
        "severity": "major",
        "area": "reproducibility",
        "path": "check-author-query.py; README.md",
        "selector": "check-author-query.py:7; README.md:21",
        "claim": "README: 'The full working history is in author-workspace-history.tar.gz.'",
        "evidence": "check-author-query.py:7 imports ROOT.parent/'check-blind13-exported-graphs.v4.py'. That file is absent from the 97-file package, absent from all 12869 candidate25 files, and absent from all 454 archive members (0 matches for 'blind13'). verify-package.py does not re-execute the query checks either.",
        "impact": "query-checks1/*.json are retained-only evidence; no reviewer can regenerate them. The 'full working history' claim is inaccurate.",
        "requestedCorrection": "Include check-blind13-exported-graphs.v4.py in the package or archive, repoint the import, and either wire the query checks into verify-package.py or state plainly that they are retained-only."
      },
      {
        "id": "F-04",
        "severity": "major",
        "area": "normative under-specification (upholds and escalates the author's own review question)",
        "path": "candidate25: docs/coop/design-corrections/native/native-evidence.schemas.v2.json; docs/v2/contracts/product-v1/native-evidence.md",
        "selector": "$defs.WorkspaceUnitV2.properties.rootPath; native-evidence.md:579-591",
        "claim": "review-queue AR-01 Q2 / README:13 treat internal root spelling as a documentation-clarity question only.",
        "evidence": "rootPath is declared {'type':'string','maxLength':4096} with no minLength/pattern/description; jsonschema accepts BOTH '' and '.'. Measured consequences of the schema-valid wrong spelling: _under_unit (native_evidence_model.v2.py:2024) returns False for every file with '.', True for every file with '' -> whole default unit silently owns zero files (every file demoted to syntax-only/no-program-unit-for-language, no fault). _rel (:2028) with '.' silently corrupts paths: 'src/a.ts'->'c/a.ts', 'index.ts'->'dex.ts'. _unit_for_cell (enumeration_model.v1.py:248) normalizes the CELL workspaceRoot via _internal_root ('.'->'') but compares unit rootPath unnormalized, so '.' -> None -> _u1_entry -> None -> fault raised as ENUMERATION_BINDING_PROGRAM_ENTRY, misattributing a root-spelling error to program entry. spell_root() and native_evidence_model.v2.py:4171,4179 (u['rootPath'] or '.') confirm two deliberate spellings exist in different records.",
        "impact": "A conforming independent implementation (exactly what AR-03/AR-05 require) can write '.', pass schema validation, and get either a silently empty analysis or a misattributed diagnostic. This is stronger than a clarity question.",
        "requestedCorrection": "State the internal-root representation normatively on WorkspaceUnitV2.rootPath and memberPackageRoots (and in native-evidence.md U-1), reject the sentinel spelling at admission with a root-specific fault code, and document the workspaceRoot-vs-rootPath asymmetry."
      },
      {
        "id": "F-05",
        "severity": "minor",
        "area": "control coverage / AR-01",
        "path": "candidate25: docs/coop/design-corrections/foundation/enumeration_model.v1.py; package semantic-controls1/",
        "selector": "enumeration_model.v1.py:711-712",
        "claim": "AR-01 asserts the default-unit programEntry correction follows the normative contract.",
        "evidence": "The rule IS enforced: if entry is not None and provenance=='default-unit' -> ENUMERATION_BINDING_PROGRAM_ENTRY. But that fault token occurs ONLY in enumeration_model.v1.py (5 occurrences) across all of candidate25 outside reviews/; no reference checker exercises it, and the package's three controls cover severity, scope and deficiency collapse only.",
        "impact": "The AR-01 correction has no negative control demonstrating the refusal it relies on.",
        "requestedCorrection": "Add a reminted control with provenance='default-unit' and non-null programEntry, asserting structural ADMIT and the ENUMERATION_BINDING_PROGRAM_ENTRY refusal."
      },
      {
        "id": "F-06",
        "severity": "minor",
        "area": "fixture hygiene / AR-01 Q3 unanswerable",
        "path": "author-helpers/ts_pilot.py",
        "selector": "ts_pilot.py:27 (parameter program_entry), :29-30 (ordinal 0 / provenance 'default-unit'), :34, :326",
        "claim": "AR-01 reviewQuestion 3: 'Are additional-program bindings kept distinct from default-unit bindings?'",
        "evidence": "_binding hardcodes ordinal 0 and provenance 'default-unit' and (post-patch) programEntry None, ignoring its program_entry parameter. The single call site ts_pilot.py:326 still passes 'tsconfig.json' into that now-dead parameter. No non-default binding is constructed anywhere in the package.",
        "impact": "The hardcode is lawful (it is the only legal pairing for default-unit), but the parameter is misleading dead code and the fixture structurally cannot express the non-default case, so AR-01 Q3 cannot be answered from this package.",
        "requestedCorrection": "Remove the dead parameter or honour it, and add an additional-program binding example with non-null programEntry and non-default provenance."
      },
      {
        "id": "F-07",
        "severity": "minor",
        "area": "control coverage / AR-02",
        "path": "author-helpers/evaluator.py; evaluator.py.patch",
        "selector": "evaluator.py:207 (and/or scopeIds union), :222 (not scopeIds), :157-158 (NotImplementedError)",
        "claim": "AR-02: 'Assess the corrected predicate scope derivation.'",
        "evidence": "Measured over all seven positive Runs, predicate operations are only 'exists' and 'none'; no and/or/not node occurs anywhere, so both combinator hunks of evaluator.py.patch are never executed by the shipped evidence. eval_atom raises NotImplementedError for count-at-most and all-covered. Scope diversity: 6 of 7 Runs have exactly 1 distinct scopeId tuple of size 1; only rust-partial discriminates (tuple sizes {0,1}).",
        "impact": "Part of the AR-02 correction is untested; the predicate algebra is exercised for 2 of 4 atom ops and 0 of 3 combinators.",
        "requestedCorrection": "Add at least one Run with a nested and/or/not predicate over differing scopes, or state the combinator paths as unexercised."
      },
      {
        "id": "F-08",
        "severity": "minor",
        "area": "property evidence under-determines its claim",
        "path": "author-properties.json; check-author-properties.py",
        "selector": "$.rustComparisons.*.editionMap; check-author-properties.py:14,19,20",
        "claim": "README:7 'different body identities for the same physical source under different selected editions, and a stable body identity when target selection changes without changing the effective edition'.",
        "evidence": "Diffing the three universe payloads, the ONLY differing field is sourceUnitOwnershipId; edition, cfgSets, unifiedFeaturesId, configProjectionSha256, crateRootPaths, lockfileIdentity and rustflags are byte-identical. The published editionMap is therefore identical in all three. Opening sourceUnitOwnershipId confirms the claim IS true: units are identical (alpha lib targetEdition null->2018; alpha-bin targetEdition 2021) and selectedUnitIds differ - lib=[alpha-lib,hashy], bin=[alpha-bin,hashy] (effective edition 2018->2021), lib-only=[alpha-lib] (effective edition unchanged).",
        "impact": "The claim is correct but not establishable from the published evidence file; I had to resolve a nested record the check never opens.",
        "requestedCorrection": "Record selectedUnitIds and the effective targetEdition of the unit owning the measured body in author-properties.json, and assert the effective-edition change/stability in check-author-properties.py."
      },
      {
        "id": "F-09",
        "severity": "minor",
        "area": "citation accuracy / AR-06",
        "path": "README.md; review-queue.json",
        "selector": "README.md:13; $.items[?(@.id=='AR-06')].authorDisposition",
        "claim": "'mixing universes in one cell-bound view is refused under execution-inputs contract §3'.",
        "evidence": "The reproduced refusal code is EXECUTION_INPUTS_COVERAGE_DERIVE, raised in execution_inputs_model.v1.py:1094-1096, 1201-1211, which implement §5 'Native Coverage accounts (derived)'. §3 is 'Stage ordinal and receipts'; it does state a related per-scope sourceUniverse-vs-binding-U rule but is not the clause the probe trips.",
        "impact": "Imprecise citation on the package's sole 'no new normative defect' claim.",
        "requestedCorrection": "Cite §5 as operative (with §3 as the related scope rule) and name the observed refusal code."
      },
      {
        "id": "F-10",
        "severity": "minor",
        "area": "reproducibility",
        "path": "build-checkpoint3.py; build-normalized-examples6.py; build-rust-selection-examples.py; build-semantic-controls.py; check-author-properties.py; check-author-query.py; assess-author-query.py; probe-mixed-universe-view.py",
        "selector": "sys.path.insert(0,str(ROOT/'output')) / from helpers import ...; ROOT.parent/'candidate-subject.v25'; writes into ROOT",
        "claim": "README:21 'original working paths are retained in construction scripts. Construction scripts are not a portable product harness.'",
        "evidence": "None of the eight scripts is executable as shipped: they import a 'helpers' package from ROOT/'output' (the package ships author-helpers/ instead), resolve candidate25 relative to ROOT.parent, and write outputs into their own frozen directory. Verified by path resolution; not executed.",
        "impact": "Disclosure is honest, but only the replay path is reproducible. The seven Runs can be replayed, never reconstructed, by a reviewer.",
        "requestedCorrection": "Provide a thin path-parameterised entry point, or state explicitly that construction is non-reproducible and only replay is verifiable."
      },
      {
        "id": "F-11",
        "severity": "info",
        "area": "fixture hygiene",
        "path": "author-helpers/runs.py",
        "selector": "runs.py:543-545",
        "claim": "n/a",
        "evidence": "'derivedProof': proof, 'claimedProof': proof, 'comparison': evaluator.compare_proof(proof, proof) is a vacuous self-comparison, honestly commented '# first mint equals derived'. Confirmed it does NOT reach shipped artifacts: tokens replay/derivedProof/claimedProof/comparison are all absent from checkpoint3/ts.store.json.",
        "impact": "None published; internal wart only.",
        "requestedCorrection": "Drop the self-comparison or rename it so it cannot later be mistaken for replay agreement."
      },
      {
        "id": "F-12",
        "severity": "info",
        "area": "evidential weighting / AR-04",
        "path": "README.md; build-normalized-examples6.py; build-rust-selection-examples.py; build-checkpoint3.py",
        "selector": "build-normalized-examples6.py:125; build-rust-selection-examples.py:138; runs.py:456",
        "claim": "README:3 'Seven synthetic Runs pass structural admission and complete semantic replay'.",
        "evidence": "Six of seven proofs are produced by R.derive(...) - the frozen evaluator_replay_model.v3.py - and then re-derived and compared by that same frozen code. Only checkpoint3 (TS) is composed by the author's own evaluator.compose_proof (runs.py:456 via ts_pilot) and independently matched by the frozen owner. The author does disclose this (README:5; AR-04 authorDisposition 'no independent derivation claim'), so labelling is accurate.",
        "impact": "Six Runs are determinism/self-consistency checks, not two-implementation agreement. Equal weighting downstream would overstate them.",
        "requestedCorrection": "State per-group in README/AR-04 which Runs are two-implementation agreements and which are frozen-owner self-derivations."
      },
      {
        "id": "F-13",
        "severity": "minor",
        "area": "AR-07 residual concentration",
        "path": "evaluation-residual-author-assessment.json",
        "selector": "$.items[RES-EP13-02,-04,-12,-13,-16,-18; IR-EP13-NB-01,-03,-04; AX6; AX9; MD5; RX2c]",
        "claim": "'Thirty individually reasoned author assessments are ready for substantive application review.'",
        "evidence": "13 of 30 residuals are disposed by the same single move - declaring same-process adversarial route regions outside the TCB. The package nowhere states this coupling.",
        "impact": "If an application reviewer rejects that one TCB assumption, 43% of the residual set reopens simultaneously. Not disclosed as a shared dependency.",
        "requestedCorrection": "Record the shared TCB-scope dependency and list the 13 dependent residual IDs so AR-07 can adjudicate the assumption once, explicitly."
      },
      {
        "id": "F-14",
        "severity": "info",
        "area": "AR-07 self-assessment signal",
        "path": "evaluation-residual-author-assessment.json",
        "selector": "$.items[*].authorAssessment",
        "claim": "n/a",
        "evidence": "All 30 items carry the identical verdict 'proposed-account-supported-with-stated-limits'; zero adverse or partially-supported self-assessments. Rationales and limits are nonetheless individually written (30 distinct rationales, 30 distinct limits).",
        "impact": "Legitimate given the author is also the proposer and every independentGrade is PENDING, but the uniform verdict carries little independent signal.",
        "requestedCorrection": "None required; noted so the application reviewer does not read uniformity as corroboration."
      }
    ],
    "verifiedPositives": [
      {"claim": "Seven positive Runs + three negative controls", "verified": true, "evidence": "verify-package.py rc=0; counts 1+4+2 positive, 3 negative"},
      {"claim": "Owner outputs reproducible", "verified": true, "evidence": "18/18 regenerated artifacts byte-identical to packaged *-owner outputs"},
      {"claim": "Consumer helpers not imported by the checker", "verified": true, "evidence": "check-export.v4.py:76 loads candidate25 identity-model.v3.py only"},
      {"claim": "Complete expected output compared, not a subset", "verified": true, "evidence": "evaluator_composition_model.v3.py:202-207 require_equal over the whole proof plus every expected object and blob"},
      {"claim": "programEntry null is normatively enforced for default units", "verified": true, "evidence": "enumeration_model.v1.py:711-712 raises ENUMERATION_BINDING_PROGRAM_ENTRY; schema description enumeration-plan.schema.v1.json:387 'U-1 default uses null'"},
      {"claim": "rootPath '' matches frozen discovery", "verified": true, "evidence": "discovery-defaults.INTERNAL_ROOT=''; enumerate_units(['tsconfig.json']) -> unitDirs ['']"},
      {"claim": "Added Coverage carrier is consumed, not unused retained data", "verified": true, "evidence": "cov_c_u yields the language-tier-unsupported / capability-missing execution deficiency on coverage cc962fa0c1 in the replayed proof"},
      {"claim": "scopeIds is independently derived and identity-bearing", "verified": true, "evidence": "evaluator_composition_model.v3.py:135,149; unrelated-scope control refused on selector proof.predicateProofs[0].scopeIds (claimed 2 vs recomputed 1)"},
      {"claim": "Three controls are separately reminted, not tampered", "verified": true, "evidence": "build-semantic-controls.py:23-27 recomputes proof/evidence/seal/run identities and deletes superseded records"},
      {"claim": "Controls fail for the intended reasons", "verified": true, "evidence": "independent claimed-vs-recomputed diffs isolate findingIds / predicateProofs[0].scopeIds / executionDeficiencies respectively"},
      {"claim": "Mixed-universe refusal is an existing boundary", "verified": true, "evidence": "independent replication reproduced the probe exactly incl. runId run3:bb3f0c9c...; code at execution_inputs_model.v1.py:1094-1096,1201-1211"},
      {"claim": "Rust properties read selected retained facts, not builder flags", "verified": true, "evidence": "re-implementation reproduces author-properties.json exactly via Run->evidence->viewIds->facts->payload and the universe H preimage"},
      {"claim": "Rust causal claim about effective edition", "verified": true, "evidence": "sourceUnitOwnershipId resolution: alpha-lib targetEdition null->2018 vs alpha-bin targetEdition 2021; lib-only keeps alpha-lib"},
      {"claim": "partial Rust: 0 clone facts, unknown coverage, indeterminate", "verified": true, "evidence": "independent replay: verdict indeterminate, 0 clones facts, input-closure-incomplete / body-language-owner-unenumerated"},
      {"claim": "Seven query checks", "verified": true, "evidence": "all 7 assertions re-verified against frozen observations.json; empty incoming carries resolutionLimitations unsupported-rung-omitted"},
      {"claim": "Thirty residuals bind to frozen source", "verified": true, "evidence": "source SHA 8f7d940e... matches; 30/30 selectors in range; 30/30 sourceCorrection verbatim; 38/38 evidence refs hash-match candidate25"},
      {"claim": "No acceptance or repair claimed in residuals", "verified": true, "evidence": "independentGrade PENDING x30, applied false x30, historicalLimitationReclassified false x30"},
      {"claim": "123 + 8 + 3 obligations intact and pending", "verified": true, "evidence": "123 unique ids all PENDING-ORIGINAL-INDEPENDENT-RECONSTRUCTION; 8 standingRules; 3 futureQualification; independentAcceptance false"}
    ],
    "arDisposition": {
      "AR-01": {"disposition": "accepted-with-corrections-required", "findings": ["F-04", "F-05", "F-06"], "note": "Both fixture corrections follow and are enforced by the normative contract. Q2 upheld and escalated to a normative defect. Q3 not demonstrable from this package."},
      "AR-02": {"disposition": "accepted", "findings": ["F-07"], "note": "Scope derivation and per-Coverage carriers match the owner's independent derivation; controls refuse on exactly the intended selectors."},
      "AR-03": {"disposition": "not-advanced-remains-pending-original-independent-consumer-b", "findings": ["F-02"], "note": "This review cannot and does not waive or replace the blind reconstruction of 123 requirements + 8 standing + 3 future. Cited evidence does not resolve against frozen bytes."},
      "AR-04": {"disposition": "accepted-as-author-reference-evidence", "findings": ["F-12"], "note": "Complete expected outputs are compared and all owner artifacts reproduce byte-identically; six of seven proofs are frozen-owner self-derivations, disclosed by the author."},
      "AR-05": {"disposition": "handoff-honest-verifiability-gap", "findings": ["F-01"], "note": "All 123/8/3 intact and pending, authorSupport correctly caveated; charter bytes unresolvable."},
      "AR-06": {"disposition": "accepted", "findings": ["F-09", "F-04"], "note": "No new normative defect demonstrated; refusal reproduced exactly. Per-universe view-attribution clarification endorsed; root-spelling clarification added with counterexample."},
      "AR-07": {"disposition": "prepared-not-gradeable-here", "findings": ["F-13", "F-14"], "note": "Application acceptance remains separate and untouched by this review."}
    },
    "residuals": {
      "count": 30,
      "uniqueIds": 30,
      "sourcePinned": "docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json",
      "sourceSha256": "8f7d940ee758633b5a5d97ae3c8fd167bae30ff8242627c334a1a12e31e5eab6",
      "sourceShaVerified": true,
      "structuralValidation": {"selectorsInRange": 30, "sourceCorrectionVerbatim": 30, "evidenceRefsResolved": 38, "evidenceRefsHashMatched": 38, "evidenceRefsMissing": 0, "resolveAgainstFrozenCandidate25": 38},
      "disciplineValidation": {"independentGradePENDING": 30, "appliedFalse": 30, "historicalLimitationReclassifiedFalse": 30, "distinctRationales": 30, "distinctLimits": 30, "boilerplateDetected": false},
      "items": [
        {"id": "RES-EP13-01", "selector": "/items/0", "trustOrHistoryClaim": "replaces defective transitive C-2 join with explicit plan/derivation DAG; EP6/8 checker bytes stay defective history", "reviewerAssessment": "history-preservation sound; explicit non-repair of the old chain is correctly stated", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-02", "selector": "/items/1", "trustOrHistoryClaim": "TCB scope: hostile same-process route regions excluded; untrusted inputs inert typed data", "reviewerAssessment": "scope reduction honestly labelled 'Trust-boundary replacement, not elimination of the old attack class'; shares the F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-03", "selector": "/items/2", "trustOrHistoryClaim": "seven-vector measurement stays finite history, never equivalence proof", "reviewerAssessment": "correct refusal to generalise a finite census; limits accurate", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-04", "selector": "/items/3", "trustOrHistoryClaim": "identifier tripwire is not an authority guard; closed schemas + authenticated code replace it", "reviewerAssessment": "explicitly declines to claim sandboxing; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-05", "selector": "/items/4", "trustOrHistoryClaim": "reviewer pins produced outside the author instrument; no self-authentication by source scan", "reviewerAssessment": "sound; consistent with this package's own external-manifest custody model", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-06", "selector": "/items/5", "trustOrHistoryClaim": "canonical admission rejects float/exponent/negative-zero, distinguishes bool/int; old EP5 bytes remain defective", "reviewerAssessment": "prospective replacement correctly scoped; history preserved", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-07", "selector": "/items/6", "trustOrHistoryClaim": "seal binds Plan/execution/evidence/evaluator/policy/proof/verdict; reminted controls give concrete mismatch checks", "reviewerAssessment": "directly corroborated by my own control diffs (severity -> findingIds; proof id reaches seal and run); limits correctly call the controls 'supporting reference evidence only'", "grade": "author-account-corroborated-independent-grade-pending"},
        {"id": "RES-EP13-08", "selector": "/items/7", "trustOrHistoryClaim": "fourteen-intent family is a bounded historical census, not a proof over all PlanIntents", "reviewerAssessment": "correct; refuses census-to-proof promotion", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-09", "selector": "/items/8", "trustOrHistoryClaim": "provenance is distinct from correctness; qualification needs real native measurements", "reviewerAssessment": "sound and directly applicable to this package's own standing", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-10", "selector": "/items/9", "trustOrHistoryClaim": "candidate self-counters do not decide admission; self-counter loophole stays historical", "reviewerAssessment": "correct; reports kept as observations", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-11", "selector": "/items/10", "trustOrHistoryClaim": "historical checker failures keep recorded causes; new replay must not relabel them or close blind litmus", "reviewerAssessment": "strongest history-preservation statement in the set; consistent with AUTHOR-STANDING.md", "grade": "author-account-corroborated-independent-grade-pending"},
        {"id": "RES-EP13-12", "selector": "/items/11", "trustOrHistoryClaim": "no sole Python answer-provenance guard carried into product authority", "reviewerAssessment": "explicitly declares no historical sole guard repaired; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-13", "selector": "/items/12", "trustOrHistoryClaim": "mutation cases deep-copy hostile inputs; fixture isolation only, no process sandbox claim", "reviewerAssessment": "corroborated: build-semantic-controls.py:12 uses copy.deepcopy on an independently loaded export; the 'fixture isolation only' limit is accurate", "grade": "author-account-corroborated-independent-grade-pending"},
        {"id": "RES-EP13-14", "selector": "/items/13", "trustOrHistoryClaim": "old differential census not used as equivalence proof or release oracle", "reviewerAssessment": "correct separation of reference results from oracle obligations", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-15", "selector": "/items/14", "trustOrHistoryClaim": "C-2 v4 self-census not elevated; blocking adjudication not cleared by changing pins", "reviewerAssessment": "sound; correctly defers to final application reviewer", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-16", "selector": "/items/15", "trustOrHistoryClaim": "producer-supplied flags cannot bypass independent replay; whole evaluator is trusted selected code", "reviewerAssessment": "corroborated by evaluator_replay_model.v3.py, which recomputes rather than trusting claimed verdicts; shares F-13 TCB dependency", "grade": "author-account-corroborated-independent-grade-pending"},
        {"id": "RES-EP13-17", "selector": "/items/16", "trustOrHistoryClaim": "text-only historical disclosures remain text-only; no padding/anchor counter proves completeness", "reviewerAssessment": "correct; deliberately declines mechanical completeness", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-18", "selector": "/items/17", "trustOrHistoryClaim": "hidden-window mechanism not retained; ledger-count attacks valid against historical system, excluded by new TCB scope", "reviewerAssessment": "honest: states the attack remains valid historically rather than repaired; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RES-EP13-19", "selector": "/items/18", "trustOrHistoryClaim": "prose-anchor checker cannot establish surrounding prose truth; independent semantic review required", "reviewerAssessment": "correct and self-limiting", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-01", "selector": "/items/19", "trustOrHistoryClaim": "gate/commitment substitution is a stronger instance of the same excluded hostile-route class; no historical guard repaired", "reviewerAssessment": "correctly generalises to the capability class rather than variant names; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-02", "selector": "/items/20", "trustOrHistoryClaim": "no punctuation/name scan decides scope or authority; old scan overclaim not inherited", "reviewerAssessment": "correct refusal to elevate a grep into a structural guarantee", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-03", "selector": "/items/21", "trustOrHistoryClaim": "no claim that Python modules or verifier instances are unreachable; real provider boundary deferred to implementation", "reviewerAssessment": "honest deferral; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-04", "selector": "/items/22", "trustOrHistoryClaim": "single explicit TCB/scope account; stale nonClaims/guardInventory prose stays historical", "reviewerAssessment": "correctly assigns narrative reconciliation to final application; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-05", "selector": "/items/23", "trustOrHistoryClaim": "message granularity is an operability case, not proof validity", "reviewerAssessment": "correct distinction; relevant to F-04, where a misattributed fault code is exactly an operability/diagnostic defect", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-06", "selector": "/items/24", "trustOrHistoryClaim": "historical parity rule imposed attacker cost without closing the class; preserve as history", "reviewerAssessment": "precise cost-vs-closure distinction; no product guarantee derived", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "IR-EP13-NB-07", "selector": "/items/25", "trustOrHistoryClaim": "original environment and measurements preserved; new reports do not overwrite or reclassify old results", "reviewerAssessment": "corroborated in form by this package's separate *-owner reports and retained history archive; weakened in substance by F-01/F-02/F-03 custody gaps", "grade": "author-account-partially-corroborated-independent-grade-pending"},
        {"id": "AX6", "selector": "/items/26", "trustOrHistoryClaim": "stack-walking witness forgery is hostile code sharing the verifier process; expressly excluded, no Python containment claim", "reviewerAssessment": "shares one sourceCorrection with AX9/MD5/RX2c but carries its own rationale; limits accurate; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "AX9", "selector": "/items/27", "trustOrHistoryClaim": "obfuscated witness forgery defeats identifier scans; boundary does not depend on enumerating spellings", "reviewerAssessment": "individually reasoned; correctly notes the attack class is unbounded; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "MD5", "selector": "/items/28", "trustOrHistoryClaim": "ledger-entry-count discrimination remains a historical escape; no hidden window used as product authority", "reviewerAssessment": "individually reasoned; explicitly disclaims side-channel resistance; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"},
        {"id": "RX2c", "selector": "/items/29", "trustOrHistoryClaim": "unenumerated witness-forgery mechanisms cannot be ruled out by attack-name census", "reviewerAssessment": "individually reasoned; correctly leaves semantic correctness and host qualification open; shares F-13 TCB dependency", "grade": "author-account-plausible-independent-grade-pending"}
      ]
    },
    "coverage": {
      "packageFilesHashVerified": 97,
      "packageFilesReadSubstantively": 40,
      "packageFilesProcessedProgrammatically": 13,
      "packageFilesNotReviewed": 22,
      "notReviewedDetail": "21 of 24 author-helpers/*.py (~370 KB; only evaluator.py, runs.py, ts_pilot.py regions read) and author-workspace-history.tar.gz contents (454 entries enumerated and content-searched, not reviewed). The helpers are construction-path only and are not in the verification path: check-export.v4.py imports the frozen candidate25 owner and never consumer helpers.",
      "candidate25FilesHashVerified": 12869,
      "candidate25FilesRead": ["foundation/identity-model.v3.py (regions)", "foundation/evaluator_replay_model.v3.py (full)", "foundation/evaluator_composition_model.v3.py (regions)", "foundation/enumeration_model.v1.py (regions)", "foundation/enumeration-plan.schema.v1.json (programEntry)", "foundation/execution_inputs_model.v1.py (regions)", "foundation/execution-inputs-contract.v1.md (sections 3-6)", "foundation/relation-payload-schemas.v2.json (coveragePartitionLaw)", "native/native_evidence_model.v2.py (regions)", "native/native-evidence.schemas.v2.json (WorkspaceUnitV2)", "discovery-defaults.py", "docs/v2/contracts/product-v1/native-evidence.md (U-1)", "evaluation-residual-dispositions.proposed.json"],
      "executions": ["verify-package.py full rerun into fresh scratch dir", "byte-comparison of 18 regenerated vs packaged owner artifacts", "independent replay + proof introspection of all 7 positive Runs", "claimed-vs-recomputed proof diff of all 3 negative controls", "independent replication of the mixed-universe probe (exact match incl. runId)", "independent re-implementation of check-author-properties.py (exact match)", "resolution and diff of 3 sourceUnitOwnershipId preimages", "root-spelling counterexample against _under_unit/_rel/_unit_for_cell/_u1_entry plus jsonschema validation of both spellings", "re-assertion of all 7 query checks from retained observations", "full structural+hash validation of 30 residuals and the 123/8/3 handoff", "exhaustive content search of candidate25 + inputs + 454 archive members for two pinned artifacts"],
      "notAttempted": ["reconstruction of any Run from source (blocked by B-3)", "regeneration of query observations (blocked by B-4)", "any blind-consumer reconstruction", "any application grading", "any product-qualification or implementation-readiness inference"],
      "scopeExceededContext": false,
      "remainingWork": "None within the assigned author-package scope. Out of scope by instruction and not performed: AR-03/AR-05 blind consumer B reconstruction, AR-07 application review, and review of the newer layout/carrier proposals."
    },
    "acceptance": {
      "authorPackageAcceptable": true,
      "qualifier": "Acceptable as an author-assisted reference checkpoint against candidate25 fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d, subject to the corrections below. Central technical claims verified by independent execution, not by reading the package's own reports.",
      "mustCorrectBeforeServingItsStatedPurpose": ["F-01", "F-02", "F-03"],
      "shouldCorrect": ["F-04", "F-05", "F-06", "F-07", "F-08", "F-09", "F-10"],
      "blindConsumerAcceptance": false,
      "independentConsumerBReconstructionDischarged": false,
      "ar03Ar05Waived": false,
      "ar07ApplicationAcceptance": false,
      "productQualificationInferred": false,
      "implementationReadinessInferred": false,
      "transfersToSuccessorBytes": false,
      "transferNote": "Acceptance is bound to candidate25 fa8cdc79... only. Any separately reviewed XA/COV successor correction requires its own review; this acceptance does not transfer.",
      "mustNotBeSuppliedToBlindConsumer": true
    },
    "openNormativeQuestions": [
      {"id": "Q-1", "question": "Should WorkspaceUnitV2.rootPath (and memberPackageRoots) normatively fix the internal-root spelling, and should admission raise a root-specific fault instead of ENUMERATION_BINDING_PROGRAM_ENTRY or silently emptying membership?", "reviewerPosition": "Yes. Evidenced by F-04 with a reproducible counterexample. Stronger than the documentation-clarity framing in README:13."},
      {"id": "Q-2", "question": "Should the contract state plainly that an evidence view referenced by a cell binding must be single-universe?", "reviewerPosition": "Yes; endorsed. Today this is only implied by execution-inputs §5 derivation plus coveragePartitionLaw, and surfaces as EXECUTION_INPUTS_COVERAGE_DERIVE rather than as a stated rule."},
      {"id": "Q-3", "question": "Should a normatively enforced rule be permitted with no negative control anywhere in the reference suite?", "reviewerPosition": "No. ENUMERATION_BINDING_PROGRAM_ENTRY is enforced in exactly one file and exercised nowhere (F-05)."}
    ]
  }
}
```
