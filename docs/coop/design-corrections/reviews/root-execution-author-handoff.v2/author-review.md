# Bounded execution-account source corrections — author review, v2 follow-up

**Standing.** Same actual-Claude source author (session `823bf66b-…`), continuing on the same
isolated exact32 successor copy. **Not an acceptance**, not an independent design review, not a
blind consumer review, not product qualification. Whole-design and blind acceptance remain
required and are not claimed anywhere here. No frozen or live edit, no pin or planning edit, no
product implementation, no commit, no push, no other agents. The v1 runtime and every v1 report,
receipt and image are preserved byte-unchanged; everything written in this pass is under
`claude-execution-account-author.v2/`.

**Verified starting point.** All nine v2 BEFORE images equal the v1 handoff AFTER bytes
(`before-hashes.json`, `equalsV1After` true on every row). The model image is
`4eaf175ff440f6440230cfaa0e00280d29eea89d0b969da73fe7ce7f8a7127f2` — exactly the SHA root's
`primary-pair-probe.json` was taken against, so root's counterexample and this fix are on the same
bytes.

---

## 1. DRAFT-P1 — the cell row still took `items[0]`

**Root was right, and the probe reproduces.** `_outcome_from_items` selected `items[0]`
unconditionally, so an earlier source carrying no typed pair — typically a census-short or
empty-partition account whose derived pair is explicitly `(null, null)` — masked a later source
that did carry a real carrier. The v1 §4 text promised the first source *actually carrying* a typed
pair. The per-account `_primary_source_pair` helper I added in v1 fixed this **within** one account
and did not fulfil the cross-account promise. Root's characterisation is accurate.

**Correction.** `_outcome_from_items` now walks the sources in the cross-source order (§2 below)
and takes the first that actually carries a pair, falling to `(null, null)` when none does. Nothing
else moves: every item stays in `sources` with its own pair and its own refs, `inputRefs` and
`nativeCauses` are untouched, and the conservative completeness law is not altered — `state` is
computed exactly as before.

**Evidence.**

* Root's own probe inputs replayed against the edited model (`probes/q4c`):
  `[null, null]` → `["budget-exhausted", null]`, with `allSourcesRetainedUnchanged`,
  `inputRefsUnchanged` and `nativeCausesUnchanged` all true.
* **An admitted owner fixture with the same shape**, which root asked for. The `file` account is
  census-short with no typed record; the `package` account carries the producer helper's own
  derived `budget-exhausted`. They are owed in the capability matrix's authored `relations` order
  (`file`, `package`, `vcs-change`), so the untyped account comes **first**. Control
  `mixed-accounts-first-typed-pair-not-first-source`: ADMIT, sources
  `[("account", null, null), ("coverage", "budget-exhausted", null)]`, row pair
  `("budget-exhausted", null)`, state `partial`.
* **The same shape through a full Run**, `full-run-mixed-accounts-first-typed-pair`:
  `M.close_run` closes, verdict `indeterminate`, and **both** originating refs survive into proof —
  `budget-exhausted` with the package Coverage ref and `required-cell-unsatisfied` (from the file
  account's null pair) with the file Coverage ref.

The discriminating fixture needed one new default-OFF graph-fixture option,
`package_coverage_unknown`, which mints the required package partition as the producer helper's own
honest `unknown` answer. The helper **derives** the pair and `admit_coverage_result_v3` admits it;
the fixture asserts nothing (`probes/q3`).

**Measured extent** (`probes/q5`, 11 enumerated source shapes): 4 row pairs change, every `state` is
unchanged, every `inputRefs` list and every `nativeCauses` list is unchanged.

## 2. DRAFT-P2 — cross-source order was never published

§5 only ever specified partition order *inside* an account, while §4 delegated the whole row to it.
I checked the actual authorities rather than assuming a lexical order (`probes/q1`):

| Leg | Order | Authority, as read |
|---|---|---|
| binding / enumerator | single item, **before** the inventories | it is `items.insert(0, …)` and both branches return immediately |
| inventories | this row's `inventoryDigests` order | `CellProgramOutcomeV1.inventoryDigests` is `x-opensip-order: canonical-set` |
| candidate | at most one | one envelope binds to one `(cellOrdinal, programOrdinal)` |
| accounts | `relations` **array order as authored** in `native-capability-matrix.v2.json#/capabilities[id]/relations`, then §5 partition order | the matrix declares no `x-opensip-order` anywhere, and `syntax` is authored `declares, literal, control-flow` — **not** sorted |

Two findings worth root's attention:

* **The account order is not lexical and must not be re-sorted.** `syntax`'s array is authored out
  of lexical order, so any implementation that "canonicalised" it would silently change which
  source supplies a row carrier. The contract, the schema annotation and an oracle all now pin this.
* **The host's account array order is not read at all.** `nativeCoverageAccounts` declares
  `x-opensip-order: "sequence"`, under which `canonical.py`'s validator enforces nothing; admission
  re-derives the owed order from `programBindings` ordinal × matrix `relations`. So a host cannot
  move a row's carrier by reordering that array. That is a good property and is now published
  rather than incidental.

Published in contract §4 as a normative table, mirrored in `M.SOURCE_ORDER`, and annotated as
`x-opensip-derived-carrier-law.crossSourceOrder` naming the authority for each leg. Three oracles
assert the three copies agree with what the reference walks. **No deterministic behaviour was
changed to publish it** — the order was already what the code did.

## 3. Checker reporting — no more fictional admission rows

Every control now declares a `controlStanding`, and `rec()` reports **null** for admission columns
that do not apply rather than filling them in:

| Standing | Count | Admission columns |
|---|---|---|
| `admission` | 60 | real `admit_execution_inputs` result |
| `closed-run` | 5 | real `M.close_run` proof **plus** real same-graph admission rows |
| `helper-unit` | 7 | not applicable → null |
| `schema-unit` | 3 | not applicable → null |

`full_run_case` no longer returns `derivedOutcomes=[{state:complete}]` and an empty
`requiredCellDeficiencies`. It returns the real rows, and they are honest about partiality — the
three indeterminate Runs now report cell state `partial` with their real `native-work-incomplete`
rows, exactly as root asked. The admission columns come from `admit_execution_inputs` on the same
graph, which is the call the Run performs internally via
`evaluator_input_model.execution_input_account` but does not return; rather than assert that
provenance, each case **tests** it — `bridgedCausesEqualProof` bridges the admission's rows with
§9.6 step 3 and requires the result to equal the proof's own causes. It does in all five.

The pure controls (`applicability-first-match-precedence`, the RC-3 summariser, the ambient-digest
and helper-attach digest checks, the three schema validations) are labelled and no longer
manufacture a complete cell. The RC-3 control keeps its `derivedAccounts` because those are the
summariser's **real** output. An oracle now fails the run if any non-admission control reports an
admission row, and another fails on an undeclared standing. Existing real proof pair and ref
assertions are untouched.

## 4. `rebuild_after_object_mutation` — independence claim corrected

The docstring said the host rows were "produced independently of the admission model". That was
wrong: `execution_inputs_fixture.v3.py` calls `M.derived_applicability`,
`M._summarize_coverage_records` and `M.derive_outcome` to build the very rows admission re-derives.
The docstring now states the correct standing — these are **reference self-consistency** controls
plus explicit oracles, and the independent consumer reconstruction a real acceptance needs is a
separate obligation that no control in this file provides.

## 5. Control naming — `optional-unsupported-cell-does-not-execute-a-provider`

Renamed to **`optional-unsupported-cell-owes-no-required-cell-row`**, with a `note` on the case row
and a comment at the construction site recording what it actually is: a **selected** enumerator at
a **non-null** universe with an admitted synthetic `unknown` Coverage. It establishes the absence
of a `requiredCellDeficiencies` row and nothing about provider execution. No synthetic reference
fixture in this file executes or declines to execute a real provider, and absence of *selection* is
the separate `optional-unselected-account-retained-typed-disclosure` control. The oracle name
(`optional-unsupported-cell-needs-no-required-row`) already stated only that, and is unchanged.

The v1 editorial `above`/`below` crossref was already repaired in the v1 final bytes; all
crossrefs in the contract now read correctly (verified by inspection of every `above`/`below`).

## 6. The candidate path root asked me to assess narrowly

**It is a real, reachable contradiction with the now-explicit no-manufacture rule.** Assessed with
actual admission and schema evidence (`probes/q2`), not helper-only speculation:

* `AvailableProgramBindingV1` has **no** `deficiency` or `nativeCause` property at all
  (`additionalProperties: false`), so on the candidate branch — which runs only under a selected
  enumerator at a non-null universe — `_binding_carrier`'s default produced
  `provider-unavailable` **every time**, on a source item with empty `inputRefs`.
* An **optional** candidate cell with no retained envelope **ADMITs**, with row pair
  `("provider-unavailable", null)` carried on no source record. Reachable, not theoretical.
* A **required** one refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED`, exactly as root said.
* A non-complete envelope with `deficiency: null` is schema-valid (no `allOf` conditional), and it
  took the same manufactured default.

**Minimal correction**, in scope and without broadening: a new `_declared_binding_carrier` reads
the binding's own declared pair with no default, and the candidate item's pair is the envelope's
own pair, else the binding's declared pair, else `(null, null)`. Row state is unchanged
(`unavailable` stays `unavailable`), the candidate source item and its
`candidate-producer-result` ref are retained, and a typed envelope's pair is preserved exactly.
Controls `optional-candidate-absent-envelope-derives-null-pair` (ADMIT, `(null, null)`, still
`unavailable`) and `required-candidate-absent-envelope-still-refuses` (REFUSE,
`EXECUTION_INPUTS_CANDIDATE_REQUIRED`).

**`_binding_carrier` itself is untouched**, and root's bounded assessment is confirmed by direct
reading: `enumeration_model.v1.py:679-683` refuses an unselected enumerator on an available binding
or a required cell, and `:752-754` refuses a null-universe binding whose `deficiency` is null
(`ENUMERATION_BINDING_CAUSE`). On a lawful plan that default is unreachable and the unselected /
null-U branches consume a real typed binding pair — the two control shapes confirm it
(`unselected-binding-with-inventory` keeps `provider-unavailable`/null from the binding's own
declaration, `null-universe-binding-with-inventory` keeps `input-closure-incomplete`/
`lockfile-missing`).

## 7. F4 qualification preserved and strengthened

Root is right that this was a **contradiction between two normative owners**, not merely a
reference-side invention: composition §9.6's table explicitly prescribed the
`provider-unavailable` fallback. The v1 report already recognised the explicit table; that
qualification is now also written into §9.6 itself as a paragraph of record, stating that a host
obeying §4 and a host obeying the old table could not both admit, and that the historical
diagnosis's "reference invention" reading was too narrow. The original diagnosis is preserved
unchanged as historical evidence; this is an added qualification, not a rewrite.

## 8. The optional unavailable inventory / same-kind rule interaction

Restated as root directs: this is **existing, deliberately conservative behaviour**, not a proved
gap. `evaluator_input_model.v3.py:136-138` selects every inventory of the rule's subject kind in
the same mode domain, across cells, so an unavailable one anywhere in that set makes the rule's
enumeration incomplete. Left unchanged and not described as a defect. The v1 optional-unselected
control already avoids the interaction by using a symbol-kind cell against a file-kind rule.

---

## 9. Tests run, with receipts

All under `probes/receipts/<label>/` with exact argv, full stdout, full stderr and exit code.
Interpreter `/tmp/opensip-architecture-review-env/bin/python -I -B`.

| Label | What | Exit |
|---|---|---|
| `q1-ordering-authority` | actual schema order annotations + matrix relation arrays | 0 |
| `q2-candidate-absent` | candidate path admission/schema evidence; root's cited enumeration guards quoted from the file | 0 |
| `q3-unknown-package-coverage` | native owner admits the derived `unknown` package Coverage | 0 |
| `q4c-mixed-account-primary` | root's counterexample + admitted fixture + full Run | 0 |
| `q5-v2-delta` | exact v1→v2 delta over 11 source shapes; 12 fixture caller shapes byte-identical | 0 |
| `v2-step2-checker` | edited checker: **75 cases, 0 mismatches, 0 oracle failures** | 0 |
| `v2-focused-checks-final` | 9 focused current checks over the edited source | 0 (all 9 exit 0) |
| `v2-tree-delta` | every file hashed against frozen32 | 0 |

**Focused, not broad, by root's instruction.** The nine checks run are the ones that exercise what
v2 touched: `execution-inputs`, `execution-replay`, `candidate-replay`, `composition`,
`full-replay`, `native-replay`, `enumeration`, `policy-derivation`, `faults`. The twelve others
were green on the v1 bytes and are untouched by these edits; `focused-checks-report.json` names
them and says why they were not re-run. Root runs the authoritative integrated suites on final
bytes.

**Whole-tree:** 12 898 files, **9 changed, 0 added, 0 removed** vs frozen32 — the same nine as v1.
v2 changed 6 of them; `enumeration-contract.v1.md`, `execution_inputs_fixture.v3.py` and
`native-evidence.md` are byte-unchanged since the v1 handoff. **No new file was touched.** Both
authoritative pin ledgers remain unedited and stale for exactly those nine.

## 10. Limits and remaining issues

1. **No acceptance is claimed.** Whole-design review and blind consumer acceptance remain required
   and outstanding.
2. **Reference self-consistency, not independent reconstruction.** Every ADMIT in
   `check-execution-inputs.v1.py` is the reference agreeing with itself plus explicit oracles,
   because the host-capture builder calls the admission model's own functions. This is now stated
   in the code rather than mis-stated.
3. **No provider execution is established by any control here**, and no compiler/OS/host/product
   qualification is claimed. Native observations remain synthetic.
4. **`full_run_case`'s admission columns are a re-run**, not a value returned by the Run —
   `R.derive` does not expose `execution_input_account`'s result. The `bridgedCausesEqualProof`
   check is what makes that provenance testable rather than asserted; it is an equality of bridged
   causes, not proof that every field of the re-run equals the Run's internal one.
5. **Scope of the order survey.** I read the order annotations for the six arrays that feed a cell
   row and every capability's `relations` array. I did not survey order annotations elsewhere in
   the schema corpus.
6. **blind19's five exports remain un-replayed by me**, as in v1. The v2 changes do not touch the
   F1/F2/F3 grounds on which they refuse; I make no claim that any of them admits.
7. **The candidate correction is narrow by design.** It changes the candidate item's *pair* only.
   Whether a selected-U optional candidate cell with no envelope should be admissible **at all** is
   a different question, owned elsewhere, and I did not change it.
8. Three v2 receipts exit non-zero by design as authoring iterations: `v2-step1-checker` (the
   `standing` key collided with the admission result's own `standing`, fixed by renaming to
   `controlStanding`) and two earlier `q4` runs. They are kept rather than discarded.
