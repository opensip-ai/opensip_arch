# Assessment corrections — what the earlier diagnosis said, and what the corrected source now says

**Standing.** Written by the source author of the bounded execution-account corrections, on the
isolated exact32 successor copy. Not an acceptance. Root's six decisions govern; the earlier
diagnosis (`claude-blind19-disagreement-assessment.v1/assessment.md`) is evidence.

---

## 1. The four execution-input differences, restated against the corrected source

### F1 — `inapplicable-vcs` account `sourceUniverse`

**Diagnosis said:** genuinely missing normative law. The rule lived in exactly two reference files
(`execution_inputs_model.v1.py:1140`, `execution_inputs_fixture.v3.py:273`), a corpus search for a
published tie returned zero hits, and both readings satisfied the schema and the contract. It
declined to pick a direction.

**Root decided:** the account's `sourceUniverse` denotes its binding's universe, for unsupported
and inapplicable accounts too; a null binding U stays null; publish the external join; do not
restrict `targetUniverse`.

**Now:** the law is published in contract §5 (a table with a `sourceUniverse` column, plus an
explicit external-join clause naming `EnumerationPlanV1.cells[ci].programBindings[po].universe`)
and annotated on `NativeCoverageAccountV1` as `x-opensip-external-joins`, which states in the
schema that the comparand is a different document and the schema therefore cannot check it. The
model enforces `want_u = uni` uniformly. `targetUniverse` carries an explicit non-constraint in
prose, in the annotation and in a control that admits a cross-universe target.

**Correction to the diagnosis, on the facts.** The diagnosis's framing implied the reference had
picked "binding U" only for accounts that *carry* Coverage. It had not: the replaced expression
nulled the universe **only** for `unavailable-unselected` and `unavailable-null-universe`, so
`inapplicable-vcs` and `unsupported-typed` already carried the binding U. Measured consequence
(`probes/p8-before-after-delta`): publishing root's rule changes **no lawful shape at all** —
the delta list is empty, and `check-execution-replay.v3.py`'s manifest digest `e9d9d313…` and Run
id `run3:094a41bd…` are byte-unchanged. D1 is a **publication plus a uniformity fix**, not a
behaviour change. The diagnosis's operative claim — that the rule existed only in reference code
and refused a conforming host for it — was right, and that is what is now fixed.

### F2 — `UNSUPPORTED-TYPED` **and** unselected: which token, and is omission lawful

**Diagnosis said:** ambiguous on the token (no published text ordered the applicability enum);
arguably a consumer defect on choosing omission over disclosure; and it noted the consumer was
internally inconsistent between `syntax-code` and `syntax-data`.

**Root decided:** publish FIRST-MATCH precedence — VCS-none, matrix `UNSUPPORTED-TYPED`,
unselected, null-U, supported — with unselected placed **before** null-U on purpose.

**Now:** the order is published in three places that a control asserts equal to one another
(`APPLICABILITY_PRECEDENCE` in the model, the §5 table, `x-opensip-applicability-precedence` on the
schema). The ambiguity the diagnosis identified is gone: matrix-unsupported outranks both
unavailable tokens, so an `UNSUPPORTED-TYPED` cell discloses its matrix pair even at null U with an
unselected enumerator, and `syntax-code`'s `unresolved-edge` token remains wrong.

**The part the diagnosis did not reach.** Placing unselected before null-U is not cosmetic. Because
`enumeration-contract.v1.md` §1 refuses a non-null universe on an unselected enumerator, the old
order made `unavailable-unselected` **unreachable** — a published enum member that no lawful input
could produce. The corrected order gives the two states distinct reachable meanings and a control
exhibits both on admitted owner fixtures. Measured: exactly **10** of 72 argument combinations
move, all lawful, all `unavailable-null-universe → unavailable-unselected`.

The diagnosis's separate "omission versus disclosure" question is answered by root's decision 3 and
is now written in `enumeration-contract.v1.md`: `enumerator.status` is about the **provider
binding**, the capability request is a different selection, and "answered by disclosure rather than
omitted" is a rule about the cell's answer that requires neither a selected enumerator nor an
executed provider.

### F3 — selected-U `UNSUPPORTED-TYPED` with lawfully minted Coverage

**Diagnosis said:** consumer defect in the account token, plus a documentation gap — under the
conforming shape the lawfully minted `unknown` / `language-tier-unsupported` Coverage is referenced
by no account and "the disclosure survives only as the `unsupported-typed` token itself", which
sits awkwardly beside `native-evidence.md`'s "omitting it would leave a consumer with no record".

**Root decided:** the Coverage remains in views, `selectedRefs` and stage capture / native
disclosure; the account's `coverageIds` are empty under the existing non-supported rule; a complete
cell outcome means the account was answered, not that the capability became supported; the derived
and native records **also** disclose it, so "only the token discloses" is too narrow; explain and
test the joins.

**Now:** contract §5 and a new paragraph in the native main chapter say exactly that. Two controls
show it on admitted owner evidence: `selected-u-unsupported-coverage-stays-selected-but-unaccounted`
proves exactly one selected Coverage is named by no account and that it is the
`unknown` / `language-tier-unsupported` / `capability-missing` record, and
`unsupported-account-discloses-the-matrix-pair-not-only-the-token` proves `derivedAccounts[]`
carries the matrix pair with `accountState: unsupported`.

**Correction to the diagnosis.** Root is right and the diagnosis was too narrow. The disclosure is
carried by at least four retained places, not one token: the Coverage record itself (retained,
selected), the account's applicability, `derivedAccounts[]`'s matrix pair, and — for a required
cell — a `requiredCellDeficiencies` row that bridges to proof and holds the Run at `indeterminate`.
The "documentation gap" was real; the "only the token" characterisation of it was not.

### F4 — `clones-fact` carrier under census-driven incompleteness

**Diagnosis said:** reference defect. `_summarize_coverage_records:614` takes
`coverage_records[0].get("deficiency") or "provider-unavailable"` and invents a carrier that occurs
on no source record, which the contract itself forbids; census-driven incompleteness currently has
no defined carrier. Its route (b) was: allow `(null, null)` and delete the fallback.

**Root decided:** route (b), plus preserve actual retained carrier pairs and originating refs in
deterministic order, plus verify the existing proof bridge still carries the obligation.

**Now:** both fallback branches are gone. `_primary_source_pair` returns the first retained record
that **actually carries a typed pair**, in a deterministic order, else `(None, None)`.

**Two things beyond what the diagnosis identified**, found while implementing:

1. The same file contained a **second** fabrication of the same kind. The per-record
   `requiredCellDeficiencies` row used `rec.get("deficiency") or summary.get("deficiency")`, so a
   Coverage record carrying no pair silently borrowed either the manufactured
   `provider-unavailable` **or a sibling record's carrier** — a cross-record re-pairing the
   contract's own "never unzip deficiencies and nativeCauses and re-pair" rule already forbade. Now
   the row is the record's exact pair.
2. `evaluator-composition-contract.v3.md` §9.6's originating-refs table **literally specified** the
   fabricated carrier, in two rows ("empty returned partitions use `provider-unavailable`", and
   borrowing the account summary deficiency). The diagnosis assessed the execution-inputs contract
   and did not reach §9.6. Correcting only the code would have left the contract stating the
   defect. Both rows are corrected, and §9.6 now records that the existing `null` →
   `required-cell-unsatisfied` route is the load-bearing carrier for missing work and that
   `uncovered-expected-source-subject` is **not** registered under `sources.execution` and is not a
   candidate for it.

**The obligation is verified, not assumed.** The full Run that previously bridged the fabricated
`provider-unavailable` into `proof.executionDeficiencies` now bridges `required-cell-unsatisfied`
with `nativeCause: null`, verdict still `indeterminate`, through the actual `M.close_run`. In the
census case the proof item carries the ExecutionInputsV1 ref **plus the originating Coverage ref**.
Where a real typed pair exists it survives as the primary pair, alongside a nonempty
`censusMissing` and an `incomplete` account.

**One small correction of my own predecessor's proposal.** Route (b) as written was "delete the
`or "provider-unavailable"` fallback at `:614`". Deleting only that would have left
`coverage_records[0]`'s pair as the primary even when record 0 carries nothing and a later record
carries a real carrier — which contradicts root's "preserve actual typed source pairs". Hence
`_primary_source_pair` selects the first record that actually carries one. Measured effect on the
`untyped-then-typed-partitions` scenario: `provider-unavailable`/null becomes the real
`input-closure-incomplete`/`lockfile-missing`.

---

## 2. The diagnosis's own §5 unresolved questions, now

1. **F1 direction** — decided by root; published; measured as behaviour-neutral over lawful shapes.
2. **F2 precedence and omission-vs-disclosure** — decided by root; published in three places and
   in `enumeration-contract.v1.md`; controlled.
3. **F4 semantics / does census incompleteness carry a deficiency** — answered: **no**, and it
   needs none. `(null, null)` plus the existing bridge carries it. No vocabulary member added, and
   §9.6 now says explicitly why `uncovered-expected-source-subject` is not it.
4. **Scope beyond the five runs** — still open in part. I enumerated the applicability token over
   72 combinations across three representative relations and exercised the carrier over seven
   record/census scenarios, but I did not survey every capability/mode combination.
5. **Q3 breadth** — untouched. Consumer-side, decision 6.
6. **Root's other hypotheses (scope enumerator / foreign-U filtering)** — untouched. I found no
   evidence for them either and make no claim; `foreign-universe-account-source-universe-refuses`
   controls only the account-level source-U join that decision 1 publishes.

---

## 3. Root's qualifications of the diagnostic report — how they were honoured

Root's assessment §"Qualifications" (Q1–Q4 and the verification limits). None of these are source
corrections; all are constraints on what may be claimed. Recording compliance:

* **Q1 — `truncated=true`.** Root: the pagination error is established, but operations 5/6 must
  **not** be labelled erroneous merely for that boolean, because their `traversalCoverage` is
  truncated-bound and `true` is correct there. **Honoured:** nothing in these corrections cites,
  repeats or relies on the operations-5/6 claim, and no query/pagination law was touched.
* **Q2 — cursor `ord:1`.** Root: opaque spelling alone is not proof of a missing binding (a host
  token may refer to bound retained state); the evidence is the consumer helper's ordinal-only
  parse/reconstruction, and the reference `q3.…` spelling is not required. **Honoured:** no cursor
  or query-schema change was made, and nothing here asserts a required spelling.
* **Q3 — external-import omission.** Root: the evidence is one actual external imported target,
  not a full projection replay. **Honoured:** untouched; no breadth claim made.
* **Q4 — request/step IDs.** Root: the allegation concerned **mutation** scopes, and Q4 never
  refutes a root claim about *query* request IDs. **Honoured:** untouched; no mutation-key or
  request-id vocabulary was added (decision 6: "no new feature or vocabulary").
* **The denied verification command / file-count listing.** Root: a file-count listing would not
  prove write confinement anyway, and full frozen-source byte verification belongs to the root
  retainer and fresh-copy custody. **Honoured:** I make **no** write-confinement claim from any
  count. Instead of counting, I hashed: `verify-tree-delta.py` compares **every** file of the
  working copy against the frozen32 subject it was copied from — 12 898 files each side, frozen
  side 736 666 114 bytes (equal to `base-custody.json`) — and reports **9 changed, 0 added, 0
  removed** (`tree-delta.json`), which is exactly the nine files listed in
  `changed-file-handoff.json` and exactly the nine both pin sweeps flag as stale. That is a
  per-file hash comparison of my own writable copy, not a custody claim over frozen32, which
  remains the root retainer's.
* **Zero-hit corpus regex.** Root: supports the bounded reading, is not universal proof of absence.
  **Honoured:** I did not re-run or rely on that search. The corrections stand on root's decision,
  not on absence-of-evidence.
* **Full charter artefact assessment still incomplete.** **Honoured:** unchanged; nothing here
  addresses it, and nothing here should be read as progress on it.

---

## 4. What the earlier diagnosis got right and is preserved

* The state agreement on F4 (`partial` on both sides) and the discriminator it found — the
  `rust-partial` / `syntax-data` asymmetry, where the two sides agree exactly whenever the Coverage
  record carries a real pair. That is exactly the boundary `_primary_source_pair` now encodes.
* The observation that the reference was **self-consistent but unpublished** on F1 — agreement
  between two reference files is not law. That is the whole shape of the D1/D2 corrections.
* Its own self-correction about `clones-fact` deriving `complete` (it did not; the frozen owner
  does implement the expected-subject census). The census path is preserved and is now controlled
  both at admission and through a closed Run.
* Its limits statement. I kept the same discipline: I did **not** re-run blind19's five exports,
  and I make no claim that any of them admits (see `author-review.md` §7.1).
