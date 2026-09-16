# Atom-cause successor — applied correction and controls

**Standing.** Architecture/design/reference authorship by the actual Claude source-author origin
`823bf66b-e92a-4789-ab81-63a1a9dc371d`. Written only to this runtime and to the isolated source copy
`/tmp/opensip-design-corrections/atom-cause-successor.v1/source`. No source33 edit, no live
repository edit, no commit or push, no pin-ledger or planning-layer edit, no independent/blind/
application acceptance, and **no acceptance claim of any kind**. Root rebinds pins after handoff.

**Interpreter for every command:** `/tmp/opensip-architecture-review-env/bin/python -I -B`.
Every command, stdout, stderr and exit code is retained under `probes/receipts/<label>/`; a repeated
label takes a numeric suffix, so failed attempts are preserved rather than overwritten.

---

## 1. Custody

`probes/receipts/a10-compare-atom-reports/stdout.txt`:

| | |
|---|---|
| successor files | 12 899 |
| frozen33 files | 12 899 |
| only in successor | none |
| only in frozen33 | none |
| changed vs frozen33 | **3 files** (below) |

The copy was an exact copy of frozen33 before the edits (`probes/receipts/a0-custody`), and the
only files that differ now are the three this correction touches. No check wrote into either tree:
every affected checker gates its writes on an explicit flag (`--export-dir`, `--output`,
`--receipt`, `--hashes`) and all were run with no arguments.

## 2. Changed files

| path | before sha256 | after sha256 | bytes |
|---|---|---|---|
| `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` | `681c3da74e6ae1f435361dd6e05a008488a3f73884f9b5bfe5837e367b265013` | `0a3fe11d21505eed65d2a51b870ea2e1914e9052fc48094dee71f2a9865e51a0` | 23 826 → 31 923 |
| `docs/coop/design-corrections/foundation/atom_model.v1.py` | `2023f8d81d83c57773f1826e8b51d0728d99e617f325374bfb47dc12e6353ec9` | `b05642b2d06fc821fb3b762ef2e92ace1e0649337d4a47c5aa83ad3e73c9a61a` | 91 347 → 92 277 |
| `docs/coop/design-corrections/foundation/check-atoms.v1.py` | `b7ae967ea0a61a5040b832dd124d6b9b0add11afbbb365dba7327e91ddb18426` | `77786e887abdc36bde01749428b7e182b3fbe935198f251f35933f6f201d06dd` | 92 949 → 102 550 |

Before-images: `before/`. After-images: `after/`. Every before sha256 equals frozen33's.

### 2.1 Contract — `atom-evaluation-contract.v1.md`

Five blocks, all inside **section 4 (Completeness partitions)**, placed where root directed: the
cause-derivation material beside the completeness partition law, the shared sufficiency detail next
to its dependency paragraph. No `[DECISION]`, `TODO`, `TBD` or `XXX` remains anywhere in the file.

1. **Completeness result and its independence from truth** (beside the outgoing partition law).
   Names the result `{complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies}` and
   states that a **return** ends only the completeness computation, retaining `causes`, `scopeIds`
   and `coverageIds` exactly as accumulated. It does not end matching and does not decide the atom
   value: a known match still makes `exists` true, `none` false, and `count-at-most` false when the
   distinct known count exceeds *n*. Only the *remaining* value is decided by completeness.
2. **Selection order (both endpoints)** — wherever the section selects several scopes or Coverage
   partitions the list is in **ascending scope2 / coverage2 identifier** order, and every first-wins
   fold reads that order.
3. **Outgoing cause derivation (`endpoint=source`), in order** — six numbered steps: cross-family
   accumulation first (`universe: null`, and it can only co-occur with steps 3–6 because it scans
   the *unavailable* bindings); `missing-relation-coverage` when no owed binding exists at all;
   `selector-unbound` when owed bindings exist but none is available at *U*;
   `uncovered-expected-source-subject` with `universe: U` when no retained scope contains the
   subject; `scope-without-coverage` per unpaired scope with `scopeIds` = every containing scope and
   `coverageIds` **empty**; then `coverage-unknown` per unsatisfied paired Coverage, with no return.
4. **Incoming cause derivation (`endpoint=target`)** — states explicitly that incoming **never**
   returns early, which is what the existing "account **every** represented Coverage *S→V* **and
   every source scope**" clause requires, and lists each incoming emission with its `universe`
   (notably `cross-family-edge-not-owed` carries `S` incoming and `null` outgoing).
5. **Deterministic dependency view, and the `coverage-unknown` carrier** (beside the `DEPENDS_ON`
   sufficiency paragraph). Four rules: primary at position 0; transitive breadth-first `DEPENDS_ON`
   with each relation visited at most once and no position for a dependency with no selected
   Coverage; one folded position per dependency relation with per-field worst-of ranks and the typed
   carrier `(deficiency, nativeCause)` taken **whole** from the first partition in selection order
   with a non-null `deficiency`, every folded partition still cited; and `coverage-unknown`'s
   `nativeCause` = first non-null scanning positions in that order, `universe` = the evaluated
   Coverage's key `sourceUniverse`.

The fold ranks name the **published** enums: `ViewEntryV3.coverage` (complete < unknown),
`ResolutionCompletenessState` (complete/not-applicable < partial < incomplete < not-attempted), and
`ClosedWorldV2.exportsClosed` (closed < open < unknown).

### 2.2 Reference — `atom_model.v1.py`

Two `return` statements and their explanatory docstrings; nothing else:

```
-    return out                                     # _coverages_exact
+    return sorted(out, key=lambda pair: pair[0])
-    return out                                     # _scopes_exact
+    return sorted(out, key=lambda pair: pair[0])
```

### 2.3 Reference controls — `check-atoms.v1.py`

Six new `test_*` functions plus two shared builders, appended in the file's existing idiom
(`base_inputs` / `plan_one` / `paired` / `scope` / `install_pair`) and registered in `CASES`.

## 3. Root's five corrections to the rejected draft

| # | Root's objection | What the applied design says |
|---|---|---|
| 1 | "stop … for this atom with value=unknown" is wrong | Block 1 above. A return ends **completeness only**; known-match dominance is restated and `test_known_hit_dominates_every_outgoing_early_stop` checks it against **each** of the four outgoing stops. Facts and uncertainty are not erased. |
| 2 | "binding cell universe field" is invented/vague | The clause now names actual admitted structure: a binding is available/unavailable by whether its admitted `universe` coordinate is non-null, `UnavailableProgramBindingV1` fixes it to null, and family comes from `evaluator-projection-registry.v1.json#/engineFamilies` — `families[*].languageModes` for the cell's `languageMode`, `families[*].universeDomain` for a universe. |
| 3 | Line 88 names dependencies but defines no traversal/partition order; read `_depends_chain` / `_conservative_entry` / `_build_sufficiency_view` / `_build_attestation_view` | Those four folds were read, and the nondeterminism root suspected was **demonstrated** (§4). Block 5 publishes the traversal and the per-position fold, and the reference was given a deterministic logical input. |
| 4 | `run_suff`'s `coverage-unknown` and carrier rules also serve **incoming** | Block 5 opens "both endpoints build it the same way"; block 4 says `coverage-unknown` is emitted by the same shared rule as outgoing step 6; and `test_dep_fold_carrier_is_first_partition_in_selection_order` runs every orientation at **both** `endpoint=source` and `endpoint=target`. |
| 5 | No `[DECISION]` placeholders in applied design | None remain; verified by search over the whole contract. |

## 4. The reference defect, and that it is latent

Root asked whether those folds make `deficiency` / `nativeCause` depend on Python dictionary
insertion order. They did.

`evaluator_input_model.v3.py:161-163` builds `facts` / `scopes` / `coverages` from Python **set**
comprehensions, and `-I` implies `-E`, so `PYTHONHASHSEED` is ignored and set iteration order varies
per process. `_coverages_exact` / `_scopes_exact` returned that order verbatim, and two folds are
first-wins over it: `_conservative_entry`'s typed carrier, and `run_suff`'s `nativeCause` scan.

| probe | receipt | result |
|---|---|---|
| direct fold, 24 processes | `a1-order-trigger` | 6 distinct coverage-dict orders, 2 distinct helper orders; folded deficiency `budget-exhausted` ×14 / `input-closure-incomplete` ×10; nativeCause `None` ×14 / `lockfile-missing` ×10 — **nondeterministic** |
| surfacing as a proof cause, 20 processes | `a2-surfacing` | `coverage-unknown.nativeCause` `lockfile-missing` ×9 / `None` ×11 |
| real retained reference Run, 8 processes, **before** the correction | `a3-realrun-stability` | one proof sha `c18f225f…`, one runId `run3:ecb44874…` — **stable**, so the shipped corpus does not trigger it |
| both probes re-sampled, 20 processes each, **after** the correction | `a4-after-correction` | input dict order still varied (6 and 5 distinct), helper order 1 distinct, deficiency `budget-exhausted` ×20, nativeCause `None` ×20, `coverage-unknown.nativeCause` `None` ×20 — **deterministic** |

So the defect is **real but latent**: it is a genuine divergence of the emitted cause from the
logical input, and no fixture in the retained corpus reaches it. It is not labelled a Run failure.

## 5. Controls added, and which of them discriminate

`check-atoms.v1.py` goes from **70** cases to **76**, all passing
(`probes/receipts/check-atoms-final/stdout.txt`: `ok: true, passed: 76, failed: 0`). The 70
pre-existing case results are byte-identical to frozen33's
(`a10-compare-atom-reports`: `sharedCasesIdentical: true`).

`probes/receipts/a8-controls-discriminate` runs the six new cases against **both** the corrected
model and frozen33's uncorrected model:

| control | corrected | frozen33 | kind |
|---|---|---|---|
| `test_dep_fold_carrier_is_first_partition_in_selection_order` | pass | **fail** (`no-program-unit` where the evidence says `lockfile-missing`) | **discriminating** — detects the defect |
| `test_outgoing_early_stop_cause_and_universe` | pass | pass | publication control |
| `test_unmatched_scope_stop_cites_every_scope_and_no_coverage` | pass | pass | publication control |
| `test_known_hit_dominates_every_outgoing_early_stop` | pass | pass | publication control |
| `test_cross_family_disclosure_survives_outgoing_selector_stop` | pass | pass | publication control |
| `test_incoming_reports_every_universe_without_early_stop` | pass | pass | publication control |

Stated plainly: **five of the six find no defect and were not meant to.** They pin behaviour the
amended prose now states and the reference already had, so contract and reference cannot drift
apart silently. Only the sixth detects the correction, and it does so deterministically rather than
flakily, because within one process the install order fixes the map order.

## 6. Focused affected checks

Root's instruction was focused affected checks, not the six broad groups. Affected = the atom model
itself and everything that imports it (`evaluator_replay_model.v3.py`,
`provider_attribution_return_model.v2.py`) and the checkers over those.

| check | exit | receipt |
|---|---|---|
| `check-atoms.v1.py` | 0 — 76/76 | `check-atoms-final` |
| `check-replay.v3.py` | 0 | `focused-check-replay.v3` |
| `check-semantic-replay.v3.py` | 0 | `focused-check-semantic-replay.v3` |
| `check-candidate-replay.v3.py` | 0 | `focused-check-candidate-replay.v3` |
| `check-execution-replay.v3.py` | 0 | `focused-check-execution-replay.v3` |
| `check-execution-inputs.v1.py` | 0 | `focused-check-execution-inputs.v1` |
| `check-provider-attribution-return.v2.py` | 0 | `focused-check-provider-attribution-return.v2` |

The same seven were then run from the **frozen33** tree (read-only, no flags, no writes) and their
stdout compared byte-for-byte after normalising the foundation path: **all six non-atom checks are
identical across the two models**, and only `check-atoms` differs, by exactly the six added cases.

## 7. Run parity — what was actually replayed

A real retained reference Run was replayed end to end through the actually selected owner —
`seal_fixture → open_run_closure → derive → seal_derived → replay → close_run` — 8 processes before
the correction and 8 after:

| | runId | proof sha256 | verdict | findings | predicates |
|---|---|---|---|---|---|
| before (`a3-realrun-stability`) | `run3:ecb4487410dc08f1c08df98af4f1932c06b0be72c412a10510ea64ef8e7352a1` | `c18f225f2a1150020996b7d633527d920e0091bb21761e9de8e6420330bc6337` | fail | 3 | 3 |
| after (`a9-realrun-after-correction`) | identical | identical | fail | 3 | 3 |

**This is not a claim of complete Run parity.** One retained reference Run was replayed, plus the
Runs the six affected checks construct internally. The full retained Run corpus was not replayed,
the six broad reference groups were not run (root runs those after pin reconciliation), and no
product execution or consumer replay was performed.

## 8. Implementability from the normative-only kit

`probes/receipts/a12-kit-implementability.2` recomputes the publication kit on the same boundary the
prior assessment used — `.md` and `.json` under `docs/v2/contracts/` and
`docs/coop/design-corrections/`, **every `.py` excluded**, and `reviews/`, `__pycache__/`,
`disposable/`, `before-image*/`, `quarantine*/` excluded as non-current — giving **169 files**, the
same count as before. Every token the amendment relies on (`capabilityForRelation`,
`UnavailableProgramBindingV1`, `engineFamilies`, `languageModes`, `universeDomain`, `sourceUniverse`,
`coverage2`, `scope2`, each cause code, `confidenceMillionths`, `exportsClosed`, `derivationKinds`,
`resolutionCompleteness`, `not-attempted`, `count-at-most`) occurs in that kit **outside** this
contract: `tokensOnlyInThisContract: []`. The first attempt at this probe used a looser boundary
(5 788 files) and is retained as `a12-kit-implementability`.

No consumer code or expected output was used to construct the amendment. Code comparisons are
author/reference evidence, not normative authority and not blind acceptance.

## 9. Limitations and open observations

1. **Not acceptance.** Nothing here is an acceptance, qualification or approval of the successor.
   Root owns pin reconciliation, the full groups, and any acceptance decision.
2. **15 pin entries go stale** across 5 ledgers, none of which was edited. Enumerated in
   `changed-file-handoff.json` and `probes/receipts/a11-stale-pins/stdout.txt`:
   `native/source-pins.v2.json` (`pins/1069`, `1070`, `1073`), `security/source-pins.v1.json`
   (same three indices), and `workflows/source-pins.v1.json`, `foundation/source-pins.v1.json`,
   `foundation/evaluator3-source-pins.v1.json` (`files/1069`, `1070`, `1073`).
3. **`ViewEntryV3.coverage` is a two-member enum** (`complete`, `unknown`), and
   `native_evidence_model.v2.py` states that the producer boundary schema-validates before its RC
   checks. `_conservative_entry`'s rank table nonetheless carries an intermediate `partial`, and
   several **pre-existing** reference checks build entries with `coverage: "partial"`. On admitted
   input that rank is unreachable, and both `partial` and `unknown` rank worse than `complete`, so
   no existing check's conclusion turns on it. Reported, deliberately **not** changed: it is outside
   this correction's scope and would alter unrelated retained checks.
4. **The defect is latent, not observed in a Run.** No retained fixture reaches the nondeterministic
   fold; the evidence for it is the controlled multi-process probes of §4, not a Run diff.
5. **Cause lists are canonical sets.** `_uniq_causes` dedups and sorts, so emission *order* is not
   observable in a published result and no control asserts it. "One `scope-without-coverage` per
   unpaired scope" is stated in the contract with that consequence made explicit.
6. **No new cause tokens or public fields** were introduced, per root's decision: the amendment only
   makes existing behaviour explicit. `AtomCauseCodeV1`, `DeficiencyV2`, `NativeCause` and the three
   published deficiency channels are untouched.
