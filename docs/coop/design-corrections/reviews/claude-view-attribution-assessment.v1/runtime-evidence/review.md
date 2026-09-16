# View attribution for `CellProgramOutcomeV1.viewDigests`: normative completeness on frozen40

**Author:** bounded AUTHOR f5617310-c7c7-4d85-acdd-31370f220944. This is an architecture, design and reference assessment only.

**Standing:**
- It is a proposal, not an acceptance. Nothing was applied to LIVE, frozen40 or the root successor.
- Admission probes show reference self-consistency: the shared host-capture builder reuses the model.
- A result is labelled *closed-run* only when it went through the maintained `check-execution-inputs.v1.full_run` driver (owner ADMIT → `R.derive` → seal → `IDENTITY.close_run`).
- No standalone probe here claims full Run admission.

**Base:** `candidate-subject.v40`. The formal manifest has sha256 `3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072`. All 12911 members were verified before the work (`receipts/frozen40-verify.json`) and re-verified after it (`receipts/frozen40-verify-final.json`). Both runs read 737700535 bytes and found 0 missing, 0 mismatched and 0 extra.

## Disposition: **CORRECTION_REQUIRED** (with one bundled clarification)

1. **Correction.** The model contradicts two explicit laws: §3 "each named scope `sourceUniverse` vs binding U" and the §5 per-universe prohibition. The measured shapes below admit *and close a real Run*. §5 names one of them as the one thing it forbids.
2. **Clarification.** No normative text defines the relation filter or the exact attributed view set. The recipe exists only in the model and the fixture. Where the U match and the relation match fall on different scopes, the choice is observable at Run level. The correction cannot be stated without fixing that recipe, so the two are proposed together.

## 1. Normative selectors (frozen40)

| Selector | What it says | What it does not say |
|---|---|---|
| `execution-inputs.schema.v1.json:621` (`CellProgramOutcomeV1.viewDigests.description`) | "Must equal captured receipt views attributed to this cell/program/U/producer." | What "attributed" means: no relation filter, no scope rule. |
| `execution-inputs-contract.v1.md:12` (§1) | Receipts are one per **stage**, with `outputRefs` per stage. | Which cell a view belongs to. No per-cell carrier exists. |
| `…contract.v1.md:19` (§1 table) | Coverage on `selectedRefs` = `coverageIds` of the captured returned views. | Anything about `viewDigests`. |
| `…contract.v1.md:51` (§3) | For selected producer outputs: "Check … view `planId`, **each named scope `sourceUniverse` vs binding U** …" | Which views are "named" by a row. |
| `…contract.v1.md:114` (§5) | Accounts derive from "**this** cell/program's returned views, own enumerator/provider, U, and pair". | A recipe for "returned by this cell". |
| `…contract.v1.md:172-186` (§5) | A selected-U `UNSUPPORTED-TYPED` cell's answered Coverage "stays in its returned view, in the stage capture, in `selectedRefs`"; the account names none. | Whether that row's `viewDigests` names the view or is empty. |
| `…contract.v1.md:219-244` (§5, per-universe clause) | "Section 3 separately requires each NAMED scope's `sourceUniverse` to equal the binding U"; "It forbids exactly one thing: making a SINGLE view carry two universes' Coverage and then attributing that view to a cell/program binding fixed at one of them"; "both conditions above are what the derivation already decides today". | The attribution recipe. |
| `native-evidence.md:3422-3449` | `UNSUPPORTED-TYPED` is answered with `unknown` Coverage that stays in its view, stage capture and `selectedRefs`. | `viewDigests`. |
| `identity-model.v3.py:1842-1937` (Run closure) | Views are checked for planId, selected producer, per-scope snapshot/enumerator/kind, partition disjointness, fact join, rung ladder and Coverage producer admission. Lines 1860-1863 deliberately admit **coverage-less scopes**. | Any single-universe, same-relation or same-producer rule across a view's scopes. |

**Implementation only (not law):**
- `execution_inputs_model.v1.py:1129-1159` does the following:
  - filters views by producer;
  - checks `planId`;
  - accumulates **separate** booleans `matched_u` (any scope at U) and `matched_rel` (any scope, possibly another one, with a matrix relation);
  - candidate-only capabilities (empty `relations`) attribute on U alone;
  - requires exact set equality (`VIEW_TOTALITY`).
- Line 1152-1153 is a no-op `continue`.
- `execution_inputs_fixture.v3.py:226-244` uses the same separate booleans, without the producer or planId filter.
- The only universe check on a named scope is `load_coverage` (`model:1246-1248`). It runs only on Coverage envelopes, and only inside `partitions_in_cell`, which only `supported-available` accounts reach (`model:1304-1358`). An `unsupported-typed` row, or a coverage-less scope, never meets it.

## 2. Measured diagnosis

Every world is a runtime-only mutation of a maintained `evaluator_graph_fixture.v3.build_file_inputs(atom_override=NONE_ATOM, …)` world. New scopes, native-owner-admitted Coverage and views are minted with the checker's own `_mint` and `coverage_result`. Receipts are `receipts/stage{1..4}-*.json`.

### 2.1 The recipe is decided only by the model (host-alternative encodings)

In each pair below, the graph, receipt, `selectedRefs` and Coverage are identical; only `viewDigests` differs. The only refusal on the alternative is `EXECUTION_INPUTS_VIEW_TOTALITY`, which means the model's own recipe is the sole discriminator.

| Case | Builder/model encoding | Alternative encoding | Refusal on alternative |
|---|---|---|---|
| Unsupported-typed selected-U row (`references@syntax-only`, complete inventories) | names its returned references view. A0: ADMIT; closed-run `indeterminate` [`language-tier-unsupported`], digest equal. | row names no view (A1) | `VIEW_TOTALITY`, at admission and in the Run |
| View carrying no relation of the capability (references view vs inventory row) | not named on the inventory row | inventory row also names it (A2) | `VIEW_TOTALITY` |
| One view with several relations of two cells (`file`+`declares` at U) | named on both rows (B2) | syntax row omits it (B2x) | `VIEW_TOTALITY` |
| U on one scope, relation on another (unsupported row: `declares@U0` + `references@U1`) | named on `references@U0` (F2). ADMIT; closed-run `indeterminate`. | same-scope reading: named on no row (F2y) | `VIEW_TOTALITY`, at admission and in the Run |
| Same shape, supported rows (`references@U0` + `package@U1`) | named on **both** `inventory@U0` and `inventory@U1` (F3). ADMIT; closed-run `pass`. | same-scope reading: `inventory@U1` only (F3y) | `VIEW_TOTALITY`, at admission and in the Run |

Earlier owner admission does **not** make the same-scope distinction unobservable, for two reasons:
- Run closure has no per-view universe rule and admits coverage-less scopes.
- F2 and F3 close real Runs with the separate-boolean encoding.

The distinction is masked in one situation only: when the foreign-universe scope carries Coverage *and* the reaching row is `supported-available`. There `load_coverage` refuses `COVERAGE_DERIVE`: D2, and F4, where `inventory@U1` reaches a U0 file Coverage only because of the separate booleans.

A shared view carrying several relations of one cell (B1: `file`+`package` at U) is named once, admits and closes a Run with `pass`. Every reading agrees on that case.

### 2.2 Explicit-law contradictions (closed Runs)

| World | Shape | Model | Law |
|---|---|---|---|
| **D1** | The unsupported `references@U0` row's view carries Coverage at **U0 and U1** | ADMIT. Closed-run `indeterminate`, digest equals admission. Under the unpatched model the owning checker's new control also closes: `run3:a46172327e74ae83886399c49ed51c31ebbcdfc2853f85481e09575239291b4a`. | This is the exact shape §5 `:240-241` "forbids". §3 `:51` also requires a scope check. |
| **F1** | The unsupported row's view names a **coverage-less** `declares@U1` scope | ADMIT. Closed-run `indeterminate` (`run3:562a31fb259160b70b3985d8ae45737c0e0753cdb354909b0b1952ad20c25057`, unpatched model). | §3 `:51` and §5 `:229-231`: each named scope must equal U. |
| **F3** | Supported rows name a view with scopes at U0 and U1 (coverage-less) | ADMIT. Closed-run `pass`. | §3 `:51`, for both rows. |
| **D2** (contrast) | Supported rows, one view carrying two universes' Coverage | REFUSE `COVERAGE_DERIVE` | Agrees. The supported path enforces what the unsupported path does not. |

§5's closing claim, "both conditions above are what the derivation already decides today", is therefore false for `unsupported-typed` rows and for coverage-less scopes.

**Lawful controls.**
- F1-control, with the extra scope at U0, admits and closes.
- F5x implements §5's "one view per universe" lawful construction: the U1 view is captured on the receipt and `selectedRefs` and attributed to no row. It admits and closes `indeterminate`.
- F5, built by the maintained builder, fails closure with `EVALUATION_VIEW_ROOTS`, because the builder captures only attributed views. That is a builder limit, not law.

### 2.3 Not findings
- **A1b.** An unsupported returned view omitted from the capture entirely admits. §1 `:24` says replay "cannot certify a malicious host omission", so this is expected.
- **E1 (standalone).** A candidate-only `clones-near` cell at the same U names every same-provider view at U. That matches the empty-`relations` branch. Plan and spec were not reminted, so this is not a Run.

## 3. Proposed correction and clarification (exact delta)

`correction.patch` has sha256 `f795b00609b4479dc09e5608d9d16cd5d06cf8531f0f324d57f06039d79d91b8` (25791 bytes). `delta-manifest.json` lists each file below; every base file is byte-identical to frozen40.

| File | Base sha256 | After sha256 |
|---|---|---|
| `foundation/execution-inputs-contract.v1.md` | `e953dedee6ef76fec58df8347f327e5ff5d2ed277486f4f4919301c26aeb767f` | `64438ff18364eefc736e877fbce43b0d89e94eca17c41cacb79a08d25b8e7d70` |
| `foundation/execution_inputs_model.v1.py` | `7c6f7c5cb8f9db5fbd8087fe2aa4996c55960fc88ceb8276efd645ef8420ce2a` | `5ea205090c1450a65fb14c29c2e02da7ef91be04baf67cb299fe67fd7bc96157` |
| `foundation/execution_inputs_fixture.v3.py` | `b8ba152cdcd1783aacf9469f8a9e9a64a3a2056dbeeaedb91818cedda3cf42f8` | `a94c971462c4e449d81eee5b1bd7a51c60b8b8b3c2e1b5cb88e32a7b2e13c8fa` |
| `foundation/check-execution-inputs.v1.py` | `5cbe6053f4d98b87ce2e7b3d2945aa18e9e5634b0ba7a49711d959e8a2c49da4` | `b1b5d4be7d0c9e240b258ec9345f4b36eda2d62197994b0e3be6adfda9629d1c` |

`execution-inputs.schema.v1.json` (`604bd941…`) is **deliberately unchanged**: no schema repin, and no new refusal code.

**Contract §3: a new "View attribution" paragraph (normative).**
- **Candidate views:** the captured returned views, meaning `selectedRefs` view refs plus complete-receipt view `outputRefs`. A wrong `planId` refuses `PLAN_JOIN`.
- **Attribution:** V is attributed to a row with a selected closure P and non-null U iff `V.producerClosure = P` **and one and the same** scope S has `S.sourceUniverse = U` and `S.relation ∈ matrix relations`. A candidate-only capability needs U alone.
- **Matrix cell state plays no part.** An `UNSUPPORTED-TYPED` row names its returned view, and its account still names no `coverageIds`.
- **What is and isn't attributed:**
  - A view with none of the capability's relations at U is not attributed.
  - One view may be attributed to several rows.
  - An unselected enumerator or null U attributes nothing.
  - A captured view attributed to no row stays lawful.
- **Exact set:** `viewDigests` is the canonical set of attributed views, otherwise `VIEW_TOTALITY`.
- **Named-scope check:** it applies to every attributed view, for every applicability. Each named scope must be at U, with or without Coverage, otherwise `EXECUTION_INPUTS_COVERAGE_DERIVE`, the existing code §5 already uses.

**Contract §5:** the per-universe clause now refers to §3's attribution. "Forbids exactly one thing" now reads: attributing to a binding at U a view that names a scope of another universe. A two-universe-Coverage view is its principal instance, and the prohibition holds for `unsupported-typed` too. The false "already decides today" sentence is replaced by the §3 refusal key.

**Model (`execution_inputs_model.v1.py`):**
- Same-scope attribution, with the `not cap_rels` candidate branch preserved.
- The named-scope universe check on each attributed view (`COVERAGE_DERIVE`).
- The no-op `continue` is removed (behaviour-neutral).

**Fixture builder (`execution_inputs_fixture.v3.py`):** the same-scope condition only, so the shared builder does not mint rows the model refuses. Root may drop this file from the patch. If it does, the new split-scope control must supply its rows by host edit.

**Reference controls (`check-execution-inputs.v1.py`):**
- 10 view-attribution cases, of which 7 are closed-run standing.
- New oracles:
  - the unsupported row names exactly its references view;
  - `VIEW_TOTALITY` on host misnaming;
  - the shared view is named once and its Run passes;
  - `COVERAGE_DERIVE` at admission **and** in the Run for D1 and F1;
  - the lawful controls close on the same manifest;
  - the split-scope view is on no row;
  - D2 is guarded against regression.

### Why the same-scope recipe, and why the named-scope check covers coverage-less scopes

- **Same scope.** A subject-scope is the only record that carries a (relation, universe) claim.
  - Under separate booleans, a view in which *no* scope claims that capability at U gets attributed (F2).
  - Combined with the §3 check, separate booleans would also turn views that no binding's account derivation reaches into refusals. §5 `:237-240` says those views stay lawful.
- **Coverage-less scopes.** §5 `:229-231` distinguishes "each NAMED scope" from "every resolved Coverage envelope's subject-scope". Reading "named scope" as "Coverage-bearing scope" would collapse that distinction.
- **Root decision point.** The narrower reading would still require the D1 fix; only F1 and F3 would stay admissible. The patch implements the literal reading.

## 4. Focused receipts (owning checker only, on runtime copies)

| Run | Tree | Cases | Mismatches | Receipt sha256 |
|---|---|---|---|---|
| base | a byte copy of the checker's dependency tree (1345 files, 0 SHA mismatches; `receipts/copy-trees.json`) | 76 | 0 (exit 0) | `ff2310481b250cf5744a46f5b3fa637d0a39bfdce41a57c4371bd539175cc5c0` |
| patched | base plus the 4-file delta | 86 | 0 (exit 0) | `a4fee543c78c966493d1364e47bc49d77e375a472927019c1be0d03398532b85` |
| controls-only (discriminator) | base plus the patched checker only | 86 | 7 (exit 1), all on the new view-attribution cases or oracles | `e6e3cfff9131316b89396ff46fa327f133face3b28791818cf652f9b1d926c0f` |

`receipts/compare-base-patched-controls.json` compares base with patched, and base with controls-only, across all 76 maintained cases. It checks result, refusals, deficiency causes and pairs, derived states, coverage records, account universes and full-run records. **There are no differences.** All 5 maintained full-run `runId`s are identical.

The controls-only failures are exactly these:
- D1 and F1 admit and close real Runs;
- host naming of the split-scope view admits;
- the split-scope view sits on the references row.

Probe receipts:

| Stage | File | sha256 |
|---|---|---|
| 1 | `stage1-introspect.json` | `3bfb8ff484348c3d5a88a6098e1cd00e053621c70f311b91bdfc92d84d90f0c6` |
| 2 | `stage2-attribution.json` | `77b29847764c83cf7a5b92499b7b067c80db1102de4122995899b826737f126b` |
| 3 | `stage3-symbol-free.json` | `c47bcd376d4c02129e6f7250dd4716442e93fe079a771960ec4d7ccb815eb136` |
| 4 | `stage4-lawful-split.json` | `e0fa6aab22df693fcbf737d4a0d506da44823357cb9c3e0ccbac6d00d24ecb4a` |

## 5. Identity and behaviour consequences

- **Maintained fixtures:** no change to any `ExecutionInputsV1` digest, admission row or Run id. Every maintained view is single-scope at its binding U.
- **Newly refused** (`COVERAGE_DERIVE`), where previously admitted and Run-closable: any view attributed to a binding at U that names a scope of another universe, on any applicability (D1, F1, F3-type).
  - F4 and D2 were already refused. F4 keeps its key, but the reason is now the §3 check rather than a separate-boolean accident.
- **Re-encoded:** views whose only U match and relation match lie on different scopes are no longer attributed (F2 type).
  - A host that named them must stop doing so.
  - Their `ExecutionInputsV1` digest, and so their Run ids, change.
  - They remain lawful as captured, unattributed views.
- **Unchanged:**
  - candidate-only attribution (U alone);
  - producer and `planId` handling;
  - the refusal registry;
  - the schema.
- **Owned-hash changes:** 4 of the files the checker's `ownedHashes` lists change. Any pins or text sweeps over the contract, model or checker outside this checker were **not** run. Root integration must run them.

## 6. Honest scope limits

- **Standing of the evidence:**
  - Admission results are reference self-consistency, because the builder calls the model.
  - Closed-run results use the maintained reference driver, not an independent consumer reconstruction.
  - E1 is standalone only.
- **Symbol-row worlds** don't close a Run even unmutated (`PAYLOAD_RECORD:#/$defs/DeclaresPayloadV1`; stage-3 S0a/S0b). Their closed-run columns in stage 2 (B2, B2x, C1, C2, C2y) carry no attribution information. Every claim that needed a Run was re-measured in symbol-free worlds.
- **Minted scopes** use `subjects: []`, and extra relations (`declares`, `references`) use universes whose matrix cell may not support them. They are lawful here only to the extent Run closure admitted them, and it did.
- **The maintained builder** captures attributed views only. Lawful unattributed capture (F5x and the new controls) is supplied by an explicit host edit.
- **Not assessed:**
  - whether the producer and `planId` filters have a normative source beyond the schema phrase and §5 "own enumerator/provider" (the builder still lacks both, which predates this work);
  - target universes;
  - incoming-search and target-attribution sidecars;
  - candidate envelopes.
- **Not run:** broad suites, planning or global reports, and repins. No blind, review or root artifacts were read. Writes went only to this runtime.

## 7. Preserved failed attempts

1. The first stage-1 invocation used `cd … && … | tee | head`. The permission mode denied it and it produced no output; it was re-run as a plain python command.
2. Stage 2's closed-run columns for symbol worlds failed with a baseline `PAYLOAD_RECORD`. They are kept verbatim in `receipts/stage2-attribution.json` and explained by stage-3 S0a/S0b.
3. Stage-3 F5, the lawful split through the builder, failed closure with `EVALUATION_VIEW_ROOTS`. It is kept and superseded by stage-4 F5x.
