# Source-author correction — per-subject dependency totality

**Standing: authorship only.** Actual Claude source-author origin
`823bf66b-e92a-4789-ab81-63a1a9dc371d`, author and **never acceptor**. Architecture, design and reference
work.

- **Written:** only three files in `/tmp/opensip-design-corrections/dependency-totality-successor.v1/source`,
  plus this runtime.
- **Not written:** the dependency-scope successor, older runtimes, pins, schemas, generated reports and
  live files.
- **Not done:** commit, push, other agents, or any consumer material.
- **Not read:** reviewer ce3's in-progress assessment.
- **Grants nothing:** no acceptance, readiness, application or product qualification.

Interpreter for every command: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Every command's
argv, stdout, stderr, exit and stdout/stderr SHA-256 are kept under `probes/receipts/<label>/`, including
failed and superseded attempts. `review.json#/commands` lists all of them.

---

## 1. Inputs and custody

- Root's `totality-copy-verification.json` was read before any edit. The copy is exactly frozen35
  (`eb45c22b…6c85`, 12,899 files) plus my completed three-file dependency-scope delta. I verified this
  independently: the only differences from frozen35 are the three owned files, each byte-equal to the
  dependency-scope successor.
- Root's `root-dependency-totality35-investigation.v1` probe and receipt were read as evidence. They
  show incoming merged {f, g} is `true` for f-only or g-only while outgoing distinguishes them; I reproduced
  that independently.
- **BEFORE** is the completed dependency-scope author bytes, not raw frozen35. Pins remain the 35 digests.
- Watched runtimes after this runtime began: the dependency-scope successor, my previous runtime and root's
  investigation are unmodified. Root added 5 files to its own `root-source36-preparation.v1`, as it said it
  might; I did not read them.

## 2. The defect

The dependency view has **one position per dependency relation**, filled by folding whatever selected
partitions exist.

- **Outgoing** evaluates one source subject, so a present position covers it.
- **Incoming per scope** evaluates the source scope's whole subject set. A calls partition for f alone
  filled the position for primary {f, g}.
- **The whole-source attestation view** folded every S dependency partition with no subject check at all.

So a universal incoming negative, completeness or bound was established without g's dependency ever
existing. Splitting {f, g} into disjoint {f}, {g} partitions turned the same evidence back into unknown,
so the answer depended on grouping, not evidence.

**Measured on the previous model** (synthetic atom-api, `z1-shapes-previous.2`), all incoming `true`:

- merged f-only and g-only;
- f plus g having only a scope without Coverage, Coverage at another target, a wrong-universe scope, or
  only an unrelated h partition;
- the attestation route with f only;
- a known-fact atom's `count-at-most 1` and `all-covered`;
- a synthetic depth-2 declares-f-only case.

Split {f}, {g} with f-only was already unknown.

## 3. Decision and law

**Corrected** with the smallest rule that retains evidence. It is published in §4 **Dependency totality
(same kind)**:

- **Owed subjects of a view.**
  - Outgoing: the current source subject.
  - Incoming per scope: the evaluated source scope's `subjects`.
  - Incoming whole-source attestation view: the union of `subjects` of the provider group's owned scopes.
- **Covered.** An owed subject is covered for dependency *R* when a scope selected at exact `(R, rung, S)`
  contains it **and** pairs at least one Coverage at exact `(R, rung, S, T)`.
- **Totality gap.** *R*'s position is present but some owed subject is uncovered: no exact scope, an exact
  scope with no Coverage, Coverage only at another target, or only a non-selected scope.
- **Evaluation with a gap.**
  1. Keep the actual view: every consulted partition, fold, carrier, deficiency and cited id.
  2. Evaluate native sufficiency on it **and** on the same view with the gap positions removed.
  3. Keep both native answers; the removed position answers `required-relation-missing`, exactly as an
     absent relation does.
  4. The view is satisfied only if both are.
- **Causes.** `coverage-unknown` is emitted once, with its `nativeCause` from the actual view. **Nothing is
  fabricated**: no Coverage, scope, subject or cause.
- **Stated consequences.** Regrouping cannot change the value or cause set. Outgoing is unchanged. Known
  matches still decide `exists`, `none` and exceeded bounds. An absent position is already the owner's
  answer. An empty owed set owes no subject check. Different-kind dependencies stay whole-source and
  unchecked. The rule applies at every depth.
- **Cost.** One scan of exact dependency scopes of S per same-kind dependency relation per view, plus at
  most one extra sufficiency evaluation for a view with a gap. No per-subject view expansion.

**Code.**

- New `_dependency_totality_gaps`.
- `run_suff` takes `gaps` and evaluates the reduced view beside the actual one.
- Gaps are passed at the outgoing, attestation and per-scope incoming call sites.

Unchanged: selection, pairing, the no-fallback rule, folds, I1, search accounting and admission.

**Alternatives considered and rejected.**

| Alternative | Why not |
|---|---|
| Drop the dependency position when not total | loses f's actual deficiency, typed carrier and cited Coverage; the partial-carrier control shows `input-closure-incomplete` / `lockfile-missing` would vanish |
| Coerce the folded entry to `coverage: unknown` | rewrites actual evidence into a value no partition carries, and the deficiency then reads f's carrier or a default, conflating two facts |
| One sufficiency view per owed subject | multiplies evaluations and cause records by the partition size, duplicates primary causes, and changes cited or cause cardinality for no semantic gain |
| Leave the attestation route whole-source and unchecked | measured: same unsound `true`, and truth would depend on evidence form (Coverage vs attestation). Its whole-source selection and fold are **kept**; only the totality check is added |

**Normative choices a reviewer may see differently** (stated, not forced):

- **Owed set of an attestation view:** owned-scope subjects, or the S inventory population. I chose scope
  subjects, consistent with the per-scope route; inventory-only omissions already emit
  `uncovered-expected-source-subject`.
- **Different-kind dependencies** (clones→declares) are not subject-checkable without a file→symbol
  containment map, so they stay whole-source as published (§8).

## 4. Measurements (synthetic atom-api; `z1-shapes-previous.2` vs `z1-shapes-successor`)

| Case (incoming unless noted) | previous | successor |
|---|---|---|
| merged {f,g}: f-only, g-only, g scope without Coverage, g Coverage at other target, g wrong-universe scope, only unrelated h | `none` true, `exists` false, `count≤0` true, `count≤1` true, `all-covered` true | **all unknown**; `required-relation-missing` plus f's actual dependency still cited |
| merged full covers: disjoint, one spanning scope, disjoint plus unrelated h | true | true; unrelated h not cited |
| split {f},{g}: f-only / g-only / both | unknown / unknown / true | unknown / unknown / true — **equal to merged in value and causes** |
| outgoing f, every variant | as before | **unchanged** |
| f `unknown` carrier + g uncovered | `nativeDeficiencies` `[input-closure-incomplete]` | `[input-closure-incomplete, required-relation-missing]`, carrier `lockfile-missing` kept |
| f `unknown` carrier + g covered | `[input-closure-incomplete]` | unchanged |
| attestation: f-only / both / spanning / none | true / true / true / unknown | **unknown** / true / true / unknown |
| known fact (g reaches f), f-only | `none` false, `exists` true, `count≤0` false, `count≤1` **true**, `all-covered` **true** | first three unchanged; `count≤1`, `all-covered` **unknown**; fact retained |
| synthetic depth 2 (calls→declares), declares f-only / both | true / true | **unknown** / true |
| empty-subject primary scope | unknown (`required-relation-missing`) | unchanged |
| ordering, 48 insertion orders each, f-only and f-and-g | 1 result each | 1 result each |

The changed-cell list is computed in `review.json#/measurements/changedCells`.

## 5. Exact delta

**My delta** (dependency-scope successor → totality successor). Diffs are in
`probes/receipts/z4-diffs/*.dependency-scope-successor.diff`, with digests in `review.json`.

| File | before sha256 | after sha256 | bytes | lines |
|---|---|---|---|---|
| `foundation/atom-evaluation-contract.v1.md` | `72986bd35f7f2b2cd5d4e5e989036a974744c682a9db877ca08bd9ac52aa2d5a` | `2d399ec91b14f22ccb7459d01ead6f54806747b24a9867cc8862fe84afa5b8c0` | 43,729 → 46,639 | +32 / −1 |
| `foundation/atom_model.v1.py` | `2c5fdabb93785349c9c9a77ddf253685309727724d98897f60a0e8abf7177dac` | `4477285c547d6697e8faefea15ed0d05e0f6f0b144e0e5e8706b532451089ade` | 94,415 → 97,581 | +56 / −6 |
| `foundation/check-atoms.v1.py` | `67d8c656ff912e023bc00fb56825568bbae9a3c5641cd23e869c11e5c2f159f5` | `ebb9da8cf07336104441f7ef4b12d0d6f5250ea87542489367cf255d171cae2d` | 141,025 → 151,805 | +173 / −0 |

**Cumulative against frozen35** (`*.frozen35.diff`), covering both my completed dependency-scope delta and
this one: contract +33/−2, model +68/−18, checker +364/−0.

- **Model:** the new helper; `run_suff` gap evaluation; three call sites. The only deletion is the
  `run_suff` satisfied test, refactored into `satisfied`.
- **Contract:** the §4 Dependency totality block; the §9 case.
- **Checker:** 6 cases plus builders. **No existing line changed.**
- No placeholders in any owned file.

## 6. Controls, commands, results

**`check-atoms.v1.py`: 101/101** (`check-atoms-successor`). The **original 95 passed on the corrected model
before any new control existed** (`check-atoms-model-only`). **No previous expected result, fixture or
assertion changed.**

Z2 runs every successor case against the previous model and the corrected one. **All 6 new controls fail
on the previous model and pass on the corrected model**; the 95 originals pass on both.

| Control | What it pins | Previous-model failure |
|---|---|---|
| `test_dependency_totality_regrouping_invariant` | merged vs split, f-only / g-only / both: equal value and causes; `required-relation-missing` when uncovered | f-only/merged true |
| `test_dependency_totality_missing_subject_and_full_cover` | 5 ways g lacks a dependency → unknown, f's Coverage cited, outgoing f still true; 3 full covers true, unrelated not cited | missing-g/absent true |
| `test_dependency_totality_keeps_partial_carrier` | gap keeps `input-closure-incomplete` + `lockfile-missing` and adds `required-relation-missing`; a covered g adds nothing | missing `required-relation-missing` |
| `test_dependency_totality_known_matches_and_bounds` | `exists`/`none`/`count≤0` keep known results; `count≤1`/`all-covered` need totality | `count≤1` true |
| `test_dependency_totality_attestation_route_and_order` | attestation owes owned-scope subjects; full attested covers true; 48 orderings → 1 result | attested f-only true |
| `test_dependency_totality_every_depth_synthetic_graph` | synthetic calls→declares: second-level gap unknown, cited; full cover true | declares-f-only true |

**Downstream checkers (Z3), previous tree vs successor, no arguments:** `check-replay.v3`,
`check-semantic-replay.v3`, `check-candidate-replay.v3`, `check-execution-replay.v3`,
`check-execution-inputs.v1`, `check-provider-attribution-return.v2` and `check-composition.v3`. All seven
exit 0 with **byte-identical stdout**. That is no-regression only.

**Not run:** integrated groups and pin sealing.

## 7. Standings and reachability

| Standing | Used for |
|---|---|
| synthetic atom-api | every control and Z1 row |
| synthetic dependency graph | the depth-2 control (in-process `DEPENDS_ON` extension, restored) |
| native producer | not used for this change |
| closed enumeration | not run |
| retained / closed Run | not run |

**No reachability is claimed.** The fix corrects an unsound reference boundary, not a demonstrated
full-Run failure.

## 8. Cross-owner consequences, dependencies, remaining issues

**Cross-owner.** None required.

- Every caller of the changed functions is private to `atom_model.v1.py` (grep).
- `required-relation-missing` is already a registered native deficiency.
- Z3 consumers are byte-identical.
- Root's planned `historySubjectOrder` and runtime-polarity prose alignments were **not** implemented.

**Pins (root).** 15 rows pin the frozen35 digests and are stale for these bytes:

- `native/source-pins.v2.json` and `security/source-pins.v1.json`: `pins/1069`, `1070`, `1073`;
- `workflows/source-pins.v1.json`, `foundation/source-pins.v1.json` and
  `foundation/evaluator3-source-pins.v1.json`: `files/1069`, `1070`, `1073`.

No pin addition is needed; root reseals after review.

**Remaining issues.**

1. **Different-kind dependency totality** (clones→declares) is not subject-checked. A file subject and
   symbol dependency subjects need a containment map this layer does not have, so it stays whole-source as
   published. Deciding it needs a normative owner decision.
2. **Whole-source attestation owed set:** chosen as owned-scope subjects (§3). The inventory-population
   alternative is sound as well; root and the independent assessment may prefer it.
3. **Empty-subject primary** reachability scope stays conservatively unknown (`required-relation-missing`)
   on both models. Not changed here.
4. **Reachability** beyond synthetic atom-api is unestablished. Reviewer ce3's separate assessment and
   root's reconciliation remain.

## 9. Probe history kept

- `z1-shapes-previous` (first run) also inventoried h, which no primary scope contains. Every incoming row
  therefore carried `uncovered-expected-source-subject`, and that run's incoming verdicts were contaminated.
  It is kept; the inventory was fixed and the probe rerun as `z1-shapes-previous.2`. Its attestation row,
  unaffected by the h inventory, was the first measurement of the attestation-route gap.
