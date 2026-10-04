# ENUM-1: a required cell whose closure is not admitted (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit. It edits only arch. It changes no product file, code, schema shape, token, refusal code, class, exit code, route or public code. It needs CODEX2's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`. It has no passage supersession, so its review lists `supersededPassages` as `[]`.

**What it is.** M3-C r8, accepted in review by CODEX2 (MC8), records cross-law finding **X-8** (MC8:1266-1270) for the enumeration owner, with J1. A required cell whose closure is not admitted has no lawful binding. Default discovery requests every cell with `required=true` (NE:950-955). The enumeration contract refuses an unselected enumerator on a required cell (ENC:53). No admitted closure can truthfully stand as the selected enumerator instead (MC8 item 9's bound). So two accepted outcomes have no Plan the contract admits:
- **E-3**, an ephemeral request with no admitted trust view (MJ5:464; MC8 item 7, MC8:426-433);
- the durable golden **"required provider closure not installed"** (WS:1374; MJ5 row 27), which is indeterminate 3.

CODEX2 confirmed the gap in its C r8 review (item 7). The lead decided the remedy (below, LD-1). ENUM-1 is that remedy, and it gates C4a's and J2c's legs for the case (MC8:432, :1270).

**Product.** Main `1799d3d` (CRC-2's binding), read only. Its lock has 99 contract successors and 4 contract passage supersessions. The record is built and checked against `1799d3d`'s lock, read with `git show`.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md`, M3-C r8, accepted in review by CODEX2 (`reviews/codex2-snapshot-plan-c-r8`) | `578c186e…` |
| **MJ5** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, M3-J1 r5, accepted by Codex | `4ccb2320…` |
| **ME** | `docs/implementation/m3/syntax-e/PROPOSAL-r3.md`, M3-E1 r3, accepted by Codex | `d71031ff…` |
| **ENC** | `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` (24,366 bytes), the enumeration contract | `b7858bc8…` |
| **EPS** | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/enumeration-plan.schema.v1.json` (20,005 bytes), SYN-1F's complete copy, the selected enumeration-plan schema | `cc29483f…` |
| **EXC** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` (35,845 bytes), the execution-inputs contract | `22ee2507…` |
| **EXS** | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/execution-inputs.schema.v1.json` (39,940 bytes), SYN-1F's complete copy, the selected execution-inputs schema | `0c196cba…` |
| **COMP** | `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`, the evaluator composition contract | `30d4d9d2…` |
| **EXM** | `docs/coop/design-corrections/foundation/execution_inputs_model.v1.py`, the execution-inputs reference model | |
| **ENM** | `docs/implementation/m2/enumeration-locator-totality-reference-selection-v1/reference/enumeration_model.v1.py`, the selected enumeration reference model | |
| **NE** / **WS** / **IE** | `docs/v2/contracts/product-v1/{native-evidence,workflows-and-surfaces,identity-and-evidence}.md` | |
| **NCM** | `docs/coop/design-corrections/native/native-capability-matrix.v2.json` | |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` | `cfe793fc…` |
| **VD** | `tools/verify_design.py` at product `1799d3d` (43,946 bytes) | `7b313de6…` |

The precedents for the form are CRC-2 (`snapshot-plan-c/crc-2/`), SD-7 (`supervisor-d/sd-7/`) and REG v3 (`docs/implementation/m2/project-registry-owner-selection-v3/`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the eleven overrides, each with its exact `before`, its `after` and the word-level changes |
| `successor.json` | the record: five parents, eleven `passageOverrides`, no `passageSupersessions`, four candidates |
| `evidence/build_enum_1.py` | builds the generated files, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_enum_1.py` | read-only, independent checks |
| `../enum-1-subject.json` | the subject manifest (generated) |
| `../enum-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/codex2-enum-1-sd-8-r1/enum-1/review.json`; not part of the subject |

The local binding check runs both units of the request, alone and together. Its script and output are request evidence: `reviews/codex2-enum-1-sd-8-r1/evidence/`.

## Where the refusal lives

The gap is as X-8 states it. One more refusal site, which X-8 does not name, sits downstream in the execution-inputs owner.

| Site | What it says | Kind |
|---|---|---|
| ENC line 53 | "`required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`)" | the rule |
| ENC lines 75-77 | "A `required=true` cell still may not be unselected" | restatement |
| ENC line 145 | the invalid class: "required+unselected enumerator" | restatement |
| EPS `/$defs/SelectedEnumeratorRef/description` | "Missing capability/provider selection for a required cell refuses pre-Plan (no fictional closure)" | the schema's statement |
| EPS `/$defs/UnselectedEnumeratorRef/description` | "Lawful only on UnavailableProgramBindingV1 when the cell required=false" | the schema's statement |
| EPS `/$defs/EnumeratorRef/description` | "unselected optional-unselected when required=false" | the schema's statement |
| EXC line 110 | the enumeration owner "refuses an unselected enumerator on an available binding or a required cell" | restatement |
| EXC line 131 | an unselected binding is "an optional" one | restatement |
| **EXC lines 101-103** | a required candidate cell with no retained envelope "still refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED` first" | **downstream refusal** |
| **EXS `/x-opensip-derived-carrier-law/candidateCarrier`** | the same, in the selected schema copy | **downstream refusal** |
| **COMP line 235** | "A required cell with **no** retained envelope refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before reaching this bridge" | **downstream refusal** |
| ENM `enumeration_model.v1.py:759-760`; product `crates/evaluator/src/enumeration_join.rs:560-566` | the code refusal | code, not contract |
| EXM `execution_inputs_model.v1.py:1198-1199`; product `crates/evaluator/src/execution_inputs.rs:1170-1175` | the candidate code refusal, whatever the enumerator | code, not contract |

**Why the downstream refusal matters.** In the case, a required `clones-near` or `clones-cross-tsjs` cell has an unselected enumerator. No producer can return its `CandidateProducerResultV1`, so it has no envelope. Default discovery requests `clones-near` with `required=true` in every mode, because NCM marks it `SUPPORTED-DESIGN` in all six (NE:1081-1087; NCM `cells`). So every default Plan in the case would still refuse at execution-input admission. E1 r3 assumed this refusal "happens only after a backend fault" (ME:547), which no longer holds once the case is admitted. The rest of EXC and COMP is ready for the case: EXC §4 derives an `unavailable` row and its binding carrier for an unselected enumerator, EXM:528 already names a required unselected row's reason `unavailable-binding`, and COMP:234 already bridges "Required enumerator unselected" to `required-cell-unsatisfied`.

## What changes

Eleven plain overrides. `PASSAGES.md` has the full texts.

| # | Parent | Selector | Change |
|---|---|---|---|
| 1 | ENC | line 53 | "`required=true` plus unselected refuses", now "except in one case (contract successor ENUM-1)": the case, its exact pair, what it covers, "The cell stays required", the inventory-cell clause, who establishes the case, and "A required unselected binding with any other pair still refuses". The rest of the paragraph is unchanged. |
| 2 | ENC | line 75 | "A `required=true` cell still may not be unselected" becomes "Outside ENUM-1's one case (**Enumerator**, above), a `required=true` cell still may not be unselected". Lines 76-77 keep "required-cell totality and indeterminacy are unchanged". |
| 3 | ENC | line 145 | The invalid class reads "required+unselected enumerator outside ENUM-1's one case". |
| 4 | EPS | `/$defs/SelectedEnumeratorRef/description` | "refuses pre-Plan (no fictional closure)" gains the exception: the case's binding is `UnavailableProgramBindingV1` with `UnselectedEnumeratorRef` and the pair, "never a fictional closure". |
| 5 | EPS | `/$defs/UnselectedEnumeratorRef/description` | "Optional-cell enumerator not selected … when the cell required=false" becomes "Enumerator not selected … in two cases": `required=false`, or the case with the pair. The reason token is `optional-unselected` in both. |
| 6 | EPS | `/$defs/EnumeratorRef/description` | The union's note names the case beside `required=false`. |
| 7 | EXC | line 103 | `EXECUTION_INPUTS_CANDIDATE_REQUIRED` gains "except in the enumeration contract's ENUM-1 case": that row is `unavailable` with the binding carrier and emits its `requiredCellDeficiencies` row. |
| 8 | EXC | line 110 | The enumeration owner refuses an unselected enumerator "on a required cell except in its ENUM-1 case, which carries exactly `provider-unavailable` with `nativeCause` null". |
| 9 | EXC | line 131 | "(an optional" becomes "(an optional, or in the enumeration contract's ENUM-1 case a required,". |
| 10 | EXS | `/x-opensip-derived-carrier-law/candidateCarrier` | The schema copy of entry 7's exception. |
| 11 | COMP | line 235 | "refuses … before reaching this bridge, except in the enumeration contract's ENUM-1 case, whose unselected binding takes the row above" (COMP:234, "Required enumerator unselected"). |

Nothing else changes. The schema shapes, the `optional-unselected` token, every refusal code, the inventory and candidate-only rules, the class table's other rows, the account applicability order, the proof bridge, every product copy and all code keep their bytes and meaning. The check script shows that each schema copy changes only at its overridden pointers, and that every sentence outside each rewritten fragment survives verbatim.

## The rule

1. **The case.** A required cell's binding may carry the unselected enumerator only when no admitted closure can lawfully be its selected enumerator, because a closure the cell's mode needs is not admitted for the request. For a TypeScript or Rust mode that is its provider closure. For `syntax-only` it is a grammar closure: without one, no syntax universe exists for the core provider closure to enumerate (CRC-1's use 2 needs a syntax universe).
2. **What it covers.** A required provider closure that is not installed, or that current trust does not admit (WS:1374; MJ5 row 27). An ephemeral request with no admitted trust view, which admits no component closure (MC8 item 7).
3. **The shape.** The existing `{status:"unselected", reason:"optional-unselected"}`, with the token's spelling unchanged. The pair is exactly `provider-unavailable` with `nativeCause` null. The universe is null, host extents stay populated, and inventories are empty `unavailable` with that pair. These are the optional case's shape rules, with the pair fixed.
4. **The cell stays required.** Its unavailable work holds the Run at `indeterminate` through `requiredCellDeficiencies` (EXC §4, §5; COMP:234). Required-cell totality is unchanged, and WS:1374's indeterminate 3 follows.
5. **What never meets it.** A required cell whose closure is admitted: its binding names that closure, available or not. An `inventory` cell: its enumerator is always the core provider closure (CRC-2, use 3). Any other pair, a non-null universe, or an available binding.
6. **Who establishes it.** Closure admission is not an input of enumeration admission. The host establishes the case when it builds the Plan (MC8 item 16, rows 8 and 12), and admission checks the shape.
7. **Downstream.** At execution-input admission, the case's required candidate cell has no envelope and does not refuse. Its row is `unavailable` with the binding carrier and emits its `requiredCellDeficiencies` row.

## Why this form: the lock, selector by selector

`build_enum_1.py` reads the lock at `1799d3d` and checks each key.
- **No target key carries a bound override.** No bound record overrides or supersedes ENC or COMP:235, and EXC's only bound key is line 257 (SYN-1F). No bound record overrides EPS or EXS pointers. So every entry is a plain override. There is nothing to supersede.
- **The markdown parents are the selected texts.** No bound record carries a complete copy of ENC, EXC or COMP.
- **The schema parents are SYN-1F's copies.** Each is the last complete copy of its schema in the chain (SYN-1F LD-F2). So the overrides go there, as CRC-2's did on SYN-1F's identity-schema copy.
- **Product copies keep their bytes.** SYN-1F's and the admission runtime's product copies of the two schemas are annotation prose that no code dispatches on (CRC-1 LD-7). No generation-source, registry or drift change follows.

## Lead decisions

Each is dated 2026-10-04 and made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them. LD-1 is the lead's own decision; LD-2 to LD-7 are the drafter's, for the lead to confirm.

**LD-1. Admit the unselected enumerator in exactly that case, with the `provider-unavailable` pair. Nothing else changes.**

| Rejected | Why |
|---|---|
| **Dropping the cell** | A required cell would disappear. ENC:17 makes `cells` exactly the requested tuples, ENC:79 keeps required cells required, and MC8 item 7 and its forbidden substitutes forbid dropping a cell because its closure is absent. |
| **Refusing the request** | It breaks E-3's accepted outcome (MJ5:464; MC8 item 7) and the durable golden's (WS:1374; MJ5 row 27). Both are a disclosed unavailability, indeterminate 3, not a refusal. |
| **Inventing a synthetic enumerator** | It breaks the producer principle at MC7:458 (MC8:527, and LD8-1 at MC8:54): a closure that did not and could not produce the cell's work would be named as its enumerator. No admitted closure can truthfully stand in (MC8 item 9's bound; MC8 "Forbidden substitutes"). |
| **Widening "required"** | Treating a cell as optional when its closure is missing would let a missing provider turn a required cell's indeterminacy into a quiet success. ENC:79 and NE:1081-1087 forbid that narrowing. |

**LD-2. The pair is exactly `provider-unavailable` with `nativeCause` null.** It is the pair MC8 item 7 and C2-T18 name, and ENC:53's typical pair. NE:3370 makes the cause optional for `provider-unavailable`.
- **Rejected: `capability-missing` as the cause.** That cause says no admitted closure bears the capability: the release-absence account (NCM `absenceProjectionAndPrecedence`) and LD8-3's `vcs-change`. Here a closure that would bear it is not admitted.
- **Rejected: any lawful pair, as for optional cells.** It is wider than the case. A required cell's pair must say why the work is missing, and only one reason applies.

**LD-3. The shape is the existing `UnselectedEnumeratorRef`, and its token keeps its spelling.**
- **Rejected: a new reason token,** such as `required-closure-unadmitted`. `reason` is a `const` (EPS), so a second token is a schema shape change. It would need complete copies of EPS and its product copies, and new generated types. The cell's `required` bit already tells the two cases apart. EXC already does so: EXM:528 names a required unselected row's reason `unavailable-binding`.

**LD-4. The host establishes the case; admission checks the shape.**
- **Rejected: an admission-side check of the closure's mode.** ENC's inputs carry no closure-to-mode relation. A `closure2` descriptor names no mode (IE:180), and ENC:106 checks only kind `provider`. The check would need a new input and a new rule.
- **Why this is safe.** Misuse fails safe. A required unselected cell holds the Run at `indeterminate` (EXC §5), never `complete` or passing. C4a's Plan builder carries the positive and negative controls (below).

**LD-5. The downstream candidate refusal is conformed in the same unit (entries 7, 10 and 11), with EXC's two restatements (entries 8 and 9).**
- **Rejected: leaving them.** Every default Plan in the case requests a required `clones-near` cell, so execution-input admission would still refuse the case, and neither J2c's leg nor the durable golden would hold.
- **Rejected: a separate execution-inputs successor.** It splits one case across two reviews, and neither half binds a working case alone. The lead may still split it out: entries 7 to 11 are separable.
- **Bounded.** Only the case is exempt. A required candidate cell with a selected enumerator and no envelope still refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED`.

**LD-6. Plain overrides, no copies.** Every key is fresh at `1799d3d`.
- **Rejected: complete copies of ENC, EXC, COMP or the schemas.** A copy would move the selected text for every successor in flight.

**LD-7. No code, reference model or product copy changes here.** The reference models are reference selections with their own evidence. The product code is its consumers' work ("Owed code").

## Owed consumers and the controls they gain

| Consumer | Leg | What the control gains |
|---|---|---|
| **C4a** | **the Plan leg** (MC8 item 16, rows 8, 12 and 15) | **C2-T18's required cells.** With I positively absent, and with F absent, every required cell other than an `inventory` cell is an unavailable binding `{status:"unselected", reason:"optional-unselected"}` with `provider-unavailable`, `nativeCause` null, a null universe and populated host extents. Step 15's structural admission admits the Plan. Every `inventory` binding still names the core provider closure. **The durable not-installed Plan (WS:1374).** With the TypeScript provider closure not installed and the Rust one installed, every required TypeScript or JavaScript mode cell takes that shape, and every Rust mode cell names the Rust provider closure. **Negatives.** The builder never emits the shape for a mode whose closure row 8 selected. The shape with any other pair, or with a non-null universe, refuses `ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR` at step 15. |
| **J2c** | **the ephemeral leg** (C2-T18 end to end; MJ5 E-3; MJ5 row 27's ephemeral case) | Full `admit_enumeration` and execution-input admission admit the Plan. Each required row of the case is `unavailable`, with the binding carrier `provider-unavailable` and null, and emits its `requiredCellDeficiencies` row (COMP:234). A required `clones-near` row has no envelope and does not refuse `EXECUTION_INPUTS_CANDIDATE_REQUIRED`. The result is indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, no runId and no `domainDetail` (RTC §7.4; SD-8, this request's other unit). |

The durable golden's committed Run uses the same admissions and keeps `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` under RTC §7.5, row 2.

## Owed code

ENUM-1 changes no code. Until its consumers land, the code still refuses the case.

| Code | Lines | Change owed | Lands with |
|---|---|---|---|
| ENM, the selected enumeration reference | `enumeration_model.v1.py:759-760` | admit an unselected enumerator on a required cell with a null universe and exactly `provider-unavailable` and null | a reference selection successor, before or with C4a |
| product enumeration admission | `crates/evaluator/src/enumeration_join.rs:560-566` | the same | C4a (step 15's structural admission) and J2's full admission |
| EXM, the execution-inputs reference | `execution_inputs_model.v1.py:1198-1199` | no `EXECUTION_INPUTS_CANDIDATE_REQUIRED` when the row's enumerator is unselected | a reference successor, before or with J2c |
| product execution-input admission | `crates/evaluator/src/execution_inputs.rs:1170-1175` | the same | J2c |

No new refusal code is needed. An unselected required binding that passed enumeration admission is the case, so the candidate exemption can key on the enumerator's status alone.

## Cross-law items

1. **X-8 is discharged** once ENUM-1 binds. M3-C's next record notes it, and C4a's and J2c's legs for the case are unblocked.
2. **For C4a: the census on unavailable candidate bindings.** ENM (`enumeration_model.v1.py:776-785`) and the product (`enumeration_join.rs:597-621`) require `candidateSourcePaths` on every binding of a `clones-near` or `clones-cross-tsjs` cell, available or not. ENC:49 names only available bindings. So C4a's unavailable candidate bindings, optional or in ENUM-1's case, must carry a census. This is existing behavior, and ENUM-1 changes nothing here.
3. **For E1's next record.** ME:547 says a required cell with no envelope refuses "only after a backend fault". ENUM-1's case is a second, lawful way to have no envelope, and it does not refuse.
4. **SD-8**, this request's other unit, conforms NE's excluded-form row to RTC §7.4. ENUM-1 and SD-8 are independent, and each binds alone.
5. **Later complete copies** of EPS or EXS must carry ENUM-1's strings in place, as SYN-1F's copies carry earlier meanings. Review must hold this, because VD does not enforce which copy is selected.

## Points for the reviewer

- **R1 (faithfulness).** Is ENUM-1 exactly X-8's case and the lead's decision, neither wider nor narrower?
- **R2 (the case).** Is the case stated precisely enough, including `syntax-only`'s grammar closure and the `inventory` exclusion? Is LD-4, host-established and shape-checked, acceptable?
- **R3 (downstream).** Is LD-5 within the one case? Do entries 7 to 11 exempt only the case and keep every other candidate refusal?
- **R4 (nothing else).** Does every sentence outside each rewritten fragment survive, and does every other refusal of an unselected enumerator stay?
- **R5 (binding).** Does the record bind after main's chain, alone and with SD-8, and does any selected passage conflict?

## Binding

ENUM-1 binds on VD at main `1799d3d`, on top of all 99 contract successors. After `ACCEPT-DESIGN-UNIT`:
1. copy the review into `docs/implementation/m3/reviews/codex2-enum-1-sd-8-r1/enum-1/review.json`;
2. complete `enum-1-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append the four pins to the product lock, in a binding-only product commit, before C4a's Plan leg and J2c's ephemeral leg;
4. run plain VD.

The review lists `"supersededPassages": []`. VD accepts the empty list, or no list, for a record with no supersession.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo or a test.
- **`evidence/build_enum_1.py`**, then `--check`, which reports identical bytes for every generated file, the unit draft included.
- **`evidence/check_enum_1.py`** passes at `1799d3d`.
- **The local binding check** (`reviews/codex2-enum-1-sd-8-r1/evidence/verify_scratch.py`) ran in a throwaway detached worktree of product main `1799d3d`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`. Its output is `local-binding-check.json` beside it. The request states the results.

## Not changed, and noted

- **No refusal code, class, exit, route or token is added.**
- **No product file is touched.** No code, test or build was run, and the reference checkers were not run.
- **No identity moves.** The descriptions are annotation text. A Plan that already admits is unchanged.
