# Bounded execution-account source corrections — author review

**Standing.** Fresh actual-Claude **source author** on the isolated exact32 successor copy
`/tmp/opensip-design-corrections/execution-account-successor.v1/source`
(base custody `manifestSha256 3897e8d1…10bf2`, 12 898 files, 736 666 114 bytes; frozen32 itself
untouched and read-only). This is **not** an acceptance, not an independent design review, not a
blind consumer review and not product qualification. No product implementation, no live edit, no
commit, no push. Every report, probe, receipt, BEFORE/AFTER image and temporary output lives in
this runtime. No other agent was contacted or resumed. No consumer helper was imported. This
session goes on the final application's exclusion list; I cannot be its acceptor.

**Source of authority.** Root's six decisions in
`root-blind19-diagnosis-assessment.v1/assessment.md`. The earlier diagnostic prose
(`claude-blind19-disagreement-assessment.v1`) is evidence; where it and root differ, root governs —
see §6 for the two places it mattered.

---

## 1. What changed, by decision

Nine files. `changed-file-handoff.json` carries before/after SHA256, byte counts, line counts and
per-file purpose. Two files named in the bounded list were read and left byte-identical.

### D1 — account `sourceUniverse` is the binding's universe

`execution_inputs_model.v1.py:1140` becomes `want_u = uni` for **every** applicability, with the
rationale in place; `execution_inputs_fixture.v3.py` mirrors it. Contract §5 gains the rule as an
explicit **external join** to `EnumerationPlanV1.cells[ci].programBindings[po].universe`, states
plainly that JSON Schema cannot express it, and records that the competing "null whenever
`coverageIds` is empty" rule is *also* internally consistent — which is exactly why the normative
one had to be published. `NativeCoverageAccountV1` gains `x-opensip-external-joins`, so the schema
**publishes the join** rather than pretending a per-record schema compares an external binding.
A null binding U stays null.

**Honest measurement, and it matters.** Over every *lawful* binding shape this rule is
**behaviourally identical to the expression it replaces** (`probes/p8`, empty delta list; the
`check-execution-replay.v3.py` manifest digest `e9d9d313…` and Run id `run3:094a41bd…` are byte-
unchanged before and after). The old expression nulled the universe only for
`unavailable-unselected` and `unavailable-null-universe`, and both of those are reachable only at
`universe=null` anyway. So D1 is a **publication plus a uniformity fix**, not a behaviour change:
it closes the trap where a future shape would silently null a real coordinate, and it gives a
conforming host a rule to read. Blind19's refusal on this point stands, because it emitted `null`
for `inapplicable-vcs` where the (then unpublished) rule already wanted the binding U.

### D2 — FIRST-MATCH applicability, unselected before null-U

`derived_applicability` now tests, in order: VCS-none → matrix `UNSUPPORTED-TYPED` → enumerator
`unselected` → null binding U → `supported-available`. `APPLICABILITY_PRECEDENCE` states it in
code, contract §5 states it as a normative table with a `sourceUniverse` column, and
`x-opensip-applicability-precedence` states it on the schema.

**This is a real behaviour change and I measured its whole extent**: exactly **10** of 72 argument
combinations move, all of them lawful, all of them
`unavailable-null-universe → unavailable-unselected` for an unselected binding (`probes/p8`).
Nothing else moves; `unsupported-typed` was already ahead of both.

The reachability argument is the point, and it is now written down in all three places:
`enumeration-contract.v1.md` §1 refuses a non-null universe on an unselected enumerator, so testing
the universe first made `unavailable-unselected` **dead code**. With the corrected order the two
advertised states have distinct reachable meanings — *the enumerator was not selected* versus *a
selected enumerator whose binding has no universe* — and a control now exhibits both on admitted
owner fixtures.

### D3 — selected capability request vs selected enumerator

`enumeration-contract.v1.md` gains the distinction: `enumerator.status` is about the **provider
binding**; the capability request/cell is a different selection; native's "answered by disclosure
rather than omitted" is a rule about the **cell's answer** and requires neither a selected
enumerator nor an executed provider. Matrix-unsupported outranks both unavailable tokens, so the
matrix deficiency/cause is disclosed at null U without fabricating Coverage there. Required-cell
totality/indeterminacy and the `required=true` + unselected refusal are restated unchanged. An
explicit optional-unselected binding is retained typed disclosure, and a control shows an optional
unsupported cell closing a full Run at `pass` without executing a provider.

### D4 — selected-U unsupported native Coverage stays; the account names none of it

Contract §5 and a new paragraph in the native main chapter say where that lawfully answered
Coverage lives: retained in its returned view, in the stage capture and in `selectedRefs`, while
its account carries `coverageIds: []` under the existing non-supported rule. Root's correction of
the diagnosis is implemented: the disclosure is **not** "only the token" — `derivedAccounts[]`
carries `accountState: unsupported` with the **matrix** pair, and a required such cell also emits a
`requiredCellDeficiencies` row that bridges to proof. A `complete` cell outcome means *the
execution account was answered*, never that the capability became supported.

The joins are now tested on genuine admitted owner evidence, not hand-made records: the fixture's
`unsupported_cell` option mints a `references@resolved-binding` Coverage whose
`unknown` / `language-tier-unsupported` / `capability-missing` pair is **derived by the native
producer helper from the admitted grammars** and admitted by `admit_coverage_result_v3`. A control
proves that exactly one selected Coverage is named by no account and that it is that record.

### D5 — no fabricated carrier for missing work

`_summarize_coverage_records` loses `or "provider-unavailable"` in both branches. A new
`_primary_source_pair` returns the **first retained record that actually carries a typed pair**, in
a deterministic order (returned partitions in canonical H order, then named-but-not-returned), and
`(None, None)` when none does. The per-record `requiredCellDeficiencies` row stops borrowing the
account summary's deficiency for a record that has none — that was a cross-record re-pairing the
contract already forbade. The genuinely missing-source row (no Coverage at all) is still published,
with null/null and whatever refs the host named.

Contract §4/§5 and composition §9.6 are corrected together; §9.6's table had **literally
specified** the fabricated carrier in two rows, so leaving it would have made the contract
self-contradictory. §9.6 also now records that `uncovered-expected-source-subject` is **not**
registered under `sources.execution` and is not this carrier: no new vocabulary member is minted.

Measured delta (`probes/p8`): `provider-unavailable` disappears from the three missing-work
scenarios; in `untyped-then-typed-partitions` the primary pair becomes the **real**
`input-closure-incomplete` / `lockfile-missing` instead of a manufactured one; scenarios that
already had a typed first record and the fully-complete scenario are unchanged.

**The obligation is kept, and that is shown through `M.close_run`, not asserted.** The full Run
that previously bridged the fabricated `provider-unavailable` into proof now bridges
`required-cell-unsatisfied` with `nativeCause: null`, and the verdict stays `indeterminate`. In the
census case the proof item carries the ExecutionInputsV1 ref **plus the originating Coverage ref**.

### D6 — query/mutation

No feature and no vocabulary was added for it, as root directed. Nothing in this source authorship
addresses Q1–Q4; they are independent consumer corrections after the normative successor, and the
original blind receives only the completed normative kit and its own outputs.

---

## 2. Tests actually run, with receipts

All receipts (exact argv, full stdout, full stderr, exit code) are under
`probes/receipts/<label>/`. Interpreter `/tmp/opensip-architecture-review-env/bin/python -I -B`
throughout.

| Label | What | Exit |
|---|---|---|
| `baseline-check-execution-inputs` | pre-edit `check-execution-inputs.v1.py` (52 cases) | 0 |
| `baseline-check-execution-replay` | pre-edit `check-execution-replay.v3.py` | 0 |
| `p1-explore-unsupported-coverage` | which cells are UNSUPPORTED-TYPED; native owner admits the derived unknown Coverage | 0 |
| `p2-capability-space` | capability/kind/pair space for lawful control shapes | 0 |
| `p3-new-fixture-cells` | new fixture cells admit; account/outcome/selectedRefs shape | 0 |
| `p4g-full-run-bridge` | 8 full Runs through `M.close_run` | 0 |
| `p5-plan-schema`, `p6-unselected-verdict`, `p7-typed-census` | three diagnosed failures during authoring (see §5) | 0 |
| `p8-before-after-delta` | exact BEFORE→AFTER behavioural delta of the model | 0 |
| `p9-existing-callers-byte-identity` | 15 existing `build_file_inputs` option shapes, BEFORE image vs edited | 0 |
| `step5-check-execution-inputs` | edited checker, **71 cases, 0 mismatches, 0 oracle failures** | 0 |
| `suite-after-edits`, `suite-final` | all **16** current `run-evaluator3-checks.py` jobs over edited source | 0 (all 16 exit 0) |
| `suite2-reference-children`, `suite2-final` | all **5** `run-reference-checks.py` children over edited source | 0 (all 5 exit 0) |
| `verify-tree-delta`, `verify-tree-delta-final` | every file of the working copy hashed against frozen32 | 0 |
| `finalize3` | deliverable/hash/receipt consistency; no drift, nothing added or removed | 0 |

The `-final` labels are re-runs after two late prose fixes in the contract (a cross-reference that
said "below" for a rule that had moved above it, and a clearer `sourceUniverse` cell in the §5
table). Both suites and the checker are byte-identical across that re-run, since no checker reads
the contract. Two receipts exit non-zero on purpose: `step2-` and `step3-check-execution-inputs`
are intermediate authoring iterations that caught real mistakes (see §5); they are kept rather than
discarded.

**Whole-tree confinement, hashed rather than counted.** `tree-delta.json`: 12 898 files each side,
frozen side 736 666 114 bytes (equal to `base-custody.json`), **9 changed, 0 added, 0 removed** —
exactly the nine in `changed-file-handoff.json` and exactly the nine both pin sweeps flag. This is
a per-file comparison of my own writable copy; custody of frozen32 itself remains the root
retainer's.

**Source pins.** Both authoritative ledgers are now stale for **exactly the nine changed files**
and nothing else (`suite-report.json`, `suite2-report.json`). I did **not** update them: root owns
the final pin/planning rebinding. To execute the suites at all I made a clearly-labelled
**disposable** rebinding in this runtime
(`DISPOSABLE-rebound-source-pins.json`, `disposable-pin-rebind-launcher.py`,
`disposable-reference-children.py`); it is never copied back, and the two stale-pin facts are
reported rather than repaired. Reports were redirected into this runtime so no report file in the
source was overwritten.

## 3. The meaningful controls, and what each demonstrates

19 new cases in `check-execution-inputs.v1.py` (52 → 71), each with a substantive oracle rather
than an ADMIT/REFUSE token only.

* **Branch precedence intersections** — `applicability-first-match-precedence`: a 10-row table
  covering VCS-none over unsupported+unselected+null, unsupported over unselected and null-U,
  unselected over null-U, selected-null-U, selected-U-supported, and VCS-none *not* touching other
  relations; plus equality of the code table, the contract order and the schema annotation. Only
  lawful shapes; no shape invented to reach a branch.
* **Account source U for empty inapplicable/unsupported accounts** —
  `inapplicable-vcs-account-carries-binding-universe`,
  `unsupported-typed-account-carries-binding-universe` (ADMIT with binding U), and both
  `…-null-source-universe-refuses` negatives.
* **Null binding vs foreign U** — `null-binding-universe-account-must-stay-null` (REFUSE when a
  host puts a real U on a null-binding account), `foreign-universe-account-source-universe-refuses`
  (REFUSE on the sibling universe in a two-universe Run), and
  `cross-universe-target-universe-is-not-constrained` (ADMIT — `targetUniverse` is deliberately not
  joined, so the correction does not accidentally ban cross-universe targets or multi-universe
  Runs).
* **Lawful supported optional-unselected vs selected-unavailable** —
  `optional-unselected-account-retained-typed-disclosure` (`unavailable-unselected`, null U, typed
  `provider-unavailable`/null, empty `coverageIds`, `optional-unselected` null reason, **no**
  required row) against `unavailable-binding-budget-keeps-inventory-causes`
  (`unavailable-null-universe`, selected enumerator). An oracle asserts both tokens are reachable
  and distinct.
* **Nonempty complete partitions, missing expected subjects, null/null source** —
  `census-missing-subjects-derive-null-pair`: pairs `(null, null)`, row `partial`, originating
  Coverage ref retained.
* **Empty returned partitions** — `owner-graph-file-missing-required-package` oracle: `(null, null)`
  on both the required row and the cell row, state `partial`.
* **Host may not manufacture the carrier** —
  `census-missing-subjects-host-may-not-claim-provider-unavailable` and
  `empty-returned-partitions-host-may-not-claim-provider-unavailable` both REFUSE
  (`EXECUTION_INPUTS_OUTCOME_DERIVE`).
* **Real typed inventory/native carrier alongside census failure** —
  `typed-native-carrier-survives-alongside-census-failure` (primary pair is the real
  `budget-exhausted`, `censusMissing` nonempty, account still incomplete) and
  `typed-inventory-carriers-survive-alongside-census-failure` (`budget-exhausted` **and**
  `input-closure-incomplete`/`lockfile-missing` both survive beside the null/null census row).
* **Native unsupported selected-U Coverage retained, admitted, unnamed** —
  `selected-u-unsupported-coverage-stays-selected-but-unaccounted` oracle: exactly one selected
  Coverage is named by no account, and it is the `unknown` / `language-tier-unsupported` /
  `capability-missing` record.
* **Required unsupported: outcome complete, assessment indeterminate** —
  `required-unsupported-cell-outcome-complete-but-assessment-indeterminate` oracle (cell rows
  `["complete", "complete"]` while `requiredCellDeficiencies` carries the matrix pair), and
  `optional-unsupported-cell-does-not-execute-a-provider`.

**Four of these run as full retained Runs through the actual `M.close_run`**, on the same route
`check-execution-replay.v3.py` uses (`F.seal_fixture` → `open_run_closure` → `R.derive` →
`S.seal_derived` → `R.replay` → `M.close_run`, with the returned run id compared):

| Control | Verdict | Proof execution cause pairs |
|---|---|---|
| `full-run-empty-returned-partitions-…` | `indeterminate` | `required-cell-unsatisfied` / null |
| `full-run-census-missing-subjects-…` | `indeterminate` | `required-cell-unsatisfied` / null, refs = ExecutionInputs **+ originating Coverage** |
| `full-run-required-unsupported-matrix-pair-bridge` | `indeterminate` | `language-tier-unsupported` / `capability-missing` |
| `full-run-optional-unselected-and-optional-unsupported-…` | `pass` | none |

The census and null-carrier paths and the required-unsupported proof bridge therefore rest on
**admitted owner fixtures through a closed Run**, not on unit branch probes. An oracle also fails
the run if `provider-unavailable` ever reaches a proof item.

## 4. Boundaries

* **No acceptance is claimed**, of anything. Not of this source, not of blind19, not of the
  consumer exports.
* **No compiler, OS, host or product qualification** is claimed or requested. All native
  observations remain synthetic, exactly as the parent reference states.
* **No source pin or planning ledger was changed**; both are stale for the nine changed files and
  root owns the rebinding and the full current-suite run at final integration.
* **No consumer artefact was read into the corrections and no consumer helper was imported.** I did
  not re-run blind19's five exports (see §7).
* The full-Run controls are **synthetic replay controls**, as `check-execution-replay.v3.py`
  already says of itself.
* Only the nine files listed were edited. No other owner's file and no admission boundary was
  touched.

## 5. Three things that went wrong while authoring, and what they taught

Recorded because each one is a fact about the source that root may want.

1. **`ENUMERATION_INVENTORY_SYMBOL_EXAMINED`.** My first unsupported-cell inventory used
   `examinedPaths: []`. The enumeration owner requires a *complete* inventory's `examinedPaths` to
   equal the binding extent. Fixed in the fixture, not worked around.
2. **`cells` ordering is content.** `EnumerationPlanV1.cells` is
   `x-opensip-order {by:[capabilityId, languageMode, workspaceRoot]}` and **`cellOrdinal` is the
   index in that sorted array**. Appending a cell whose id sorts earlier silently renumbers the
   existing cells. The fixture now sorts once and reads every `cellOrdinal` from a map; the same
   applies to `requestedCapabilities`, which is a canonical set.
3. **An unavailable inventory of the rule's own subject kind makes the rule's enumeration
   incomplete.** My first optional-unselected cell was `clones-fact` (kind `file`), and
   `evaluator_input_model.v3.py:136-144` selects **every** inventory of the rule's subject kind
   across cells, so the Run went `indeterminate` through an *enumeration* deficiency and muddied
   what the control measured. That owner's rule is conservative and, I think, correct; it is
   outside my bounded scope, so I moved the control to `syntax` (kind `symbol`) rather than touch
   it. **Root may want to look at it anyway**: an optional, unselected, non-required cell's own
   empty inventory can make an unrelated required rule's enumeration incomplete.

## 6. Where I followed root against the diagnosis

* The diagnosis proposed, for F4, either a new named deficiency or allowing `(null, null)`. Root
  chose `(null, null)` and "no new vocabulary". Implemented that way;
  `uncovered-expected-source-subject` exists in the *native* registry but is **not** registered
  under `sources.execution`, and §9.6 now says so explicitly so nobody reaches for it later.
* The diagnosis said of an unsupported cell that "the disclosure survives only as the
  `unsupported-typed` token itself". Root called that too narrow. It is: `derivedAccounts[]` and
  `requiredCellDeficiencies` carry it too, and the retained Coverage is still in `selectedRefs`.
  The contract, the native chapter and two controls now say and show this.

## 7. Remaining issues, honestly

1. **Blind19's five exports were not re-run by me.** Under the now-explicit law they should still
   refuse — F1 because the host emitted `null` for `inapplicable-vcs` where the published rule is
   the binding U; F2 because matrix-unsupported still outranks unselected, so `syntax-code`'s
   `unresolved-edge` token is still wrong; F3 because `supported-available` on an
   `UNSUPPORTED-TYPED` cell is still wrong — while **F4 is now gone from the reference side**.
   That is reasoning from the corrected code, **not a re-execution**: replaying them needs root's
   export-transport helper and their captured stores, neither of which is in my bounded source.
   I make **no** claim that any of the five admits, and I reminted none of their bytes.
2. **`_binding_carrier` still defaults to `provider-unavailable`** when a binding declares no
   deficiency (`execution_inputs_model.v1.py`). I left it: it is the *binding owner's* carrier,
   root's decision 5 lists binding carrier pairs among the things to **preserve**, and decision 2
   says malformed binding shapes are rejected by their original owner. But it is the same *shape*
   of default as the one just removed, and for an optional-unselected binding it does assert a
   provider observation. Flagging it as a question for root rather than changing another owner's
   semantics unasked.
3. **D1 has no reachable behavioural effect** (§1). If root expected the account universe rule to
   change some admitted Run, it does not — and the reason is precisely D2's reordering plus the
   enumeration owner's refusal of unselected-with-U. Worth confirming that publication was the
   intent.
4. **Scope of the applicability survey.** I enumerated the token table over
   `{vcs-change, file, references} × {null, U} × {selected, unselected} × {SUPPORTED-DESIGN,
   UNSUPPORTED-TYPED, None} × {none, git}` = 72 combinations. Other relations behave identically
   because `derived_applicability` only special-cases `vcs-change`, but I did not enumerate every
   registered relation.
5. **The native chapter change is explanatory only.** It adds a pointer paragraph and changes no
   native normative statement. If root wants the account law restated *normatively* inside the
   native chapter rather than cross-referenced, that is a further edit.
6. **`check-evaluator-composition.v3.py` does not exist** in this source; the composition checker
   is `check-composition.v3.py`. It needed no change and exits 0.
7. **Full charter artefact assessment remains incomplete**, as root already recorded. Nothing here
   addresses it.

## 8. What this is not

Not an acceptance. Not a freeze. Not a pin or planning update. Not a product implementation. The
corrective source and its controls are complete and executing green over the current suites at the
bounded scope root set; the sealing, the authoritative pin/planning rebinding, the full current
suite run and the independent design and consumer reviews are root's.
