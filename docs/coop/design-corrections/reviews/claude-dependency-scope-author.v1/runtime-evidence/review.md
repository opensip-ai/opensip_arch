# Source-author correction — dependency-scope mapped fallback (`_select_dep_coverages`)

**Standing: authorship only.** Written by the actual Claude source-author origin
`823bf66b-e92a-4789-ab81-63a1a9dc371d`, acting as a **coauthor, never an acceptor**. Architecture,
design and reference work only.

- **Written:** three files in `/tmp/opensip-design-corrections/dependency-scope-successor.v1/source`,
  plus this runtime.
- **Not edited:** frozen35, every prior runtime and source, pins, schemas, generated reports and live
  files.
- **Not done:** product implementation, activation, commit, push, or contact with other agents.
- **Not read:** consumer runtime or output, root-blind material, and author-package expected results.
- **Grants nothing:** no acceptance, readiness, application outcome or qualification.

Interpreter for every command: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Every command,
stdout, stderr and exit is kept under `probes/receipts/<label>/`, and failed attempts are kept too.
`review.json#/commands` lists every retained command.

---

## 1. Inputs and custody

- The frozen35 manifest `eb45c22b…6c85` matches its declared digest, and all **12,899** frozen35 files
  match it with nothing extra (`q6-custody-delta-pins`).
- Root's `copy-verification.json` (12,899 files, 736,823,249 bytes) was read **before any mutation**. I
  also verified the mutable copy byte-equal to frozen35 before editing.
- Root's investigation (`assessment.md`, `probe.py`, `probe.json`) was read and treated as evidence,
  not as a requirement.
- No watched runtime was modified after this runtime began: root's investigation, root's source36
  preparation, and my prior incoming-binding author runtime.

**Who wrote the pre-edit bytes.** Frozen35 already contains root's later changes on top of my
completed incoming-binding author v1:

| File | My v1 after-image | frozen35 (this BEFORE) | Root after v1 |
|---|---|---|---|
| contract | `7ee61c18…` | `f6c3b375…` | +7/−5: empty vs borrowed `scopeRefs` refusal wording; generic defensive-fallback sentence |
| model | `c1243ca9…` | `c1243ca9…` | none |
| checker | `258099be…` | `11aa038a…` | +4: borrowed-scope `INCOMING_SEARCH_SCOPE_MISJOIN` assertion |

Only the delta in §5 is mine in this session.

## 2. Decision: substantiated as a reference defect; corrected by removing the fallback

**Mechanism** (frozen35 `atom_model.v1.py:1086-1116`). For a same-kind dependency,
`_select_dep_coverages` pairs Coverage to the scopes `_scopes_exact` selects at exact
`(dependency relation, rung, S)`. When **no** exact scope existed, it fell back to following
`coverageScopes` to whatever scope record the mapping named, and checked only whether the subject was
in it. It checked neither that scope's coordinates nor its carrier.

**Why remove the branch instead of constraining it.**

- Every scope at exact coordinates is already in `_scopes_exact`. So whenever the fallback ran, the
  mapped scope was **necessarily outside** the published selection: absent, null or different
  `sourceUniverse`, `relation` or `resolution`, or not a valid carrier.
- Carrier-validating the fallback would still let a **valid but wrong-coordinate** scope supply the
  dependency.
- Constraining it to exact coordinates makes it identical to the main path, which is dead code.
- The published law already excludes it: §4 "No one-scope/one-coverage fallback", and the dependency
  paragraph's "pair dep Coverage to **current-source** scopes". The reference was looser than the prose.

**The corrected rule.** Same kind, only exact-coordinate scopes containing the current subjects pair,
by mapping or commitment, as outgoing does. A mapping to any other scope pairs **nothing**, whether or
not an exact scope exists. The dependency then occupies no position, and native `sufficiency_v2`
answers `required-relation-missing`.

**Refusal versus ignored-as-absent.**

- A non-exact scope is **ignored as absent**, not refused. That is identical to deleting it, and
  consistent with how outgoing and incoming selection already treat non-exact scopes.
- A **selected** exact-coordinate scope that fails the carrier (for example a missing
  `enumeratorClosure`) still refuses `ATOM_NATIVE_CARRIER` when paired.

**Unchanged:** I1 and the shared prelude; all three cause channels; known-match and count-bound
dominance; exact-rung selection; mapping-or-commitment pairing; ascending dedup and whole-record folds;
different-kind whole-source dependencies; attestation views (`current_subjects=None`); dependency
traversal; and every admission law.

**Normative clarification.** A precision sentence was added rather than a new rule, because the prose
already excluded the branch. The §4 dependency paragraph now states: exact `(relation, rung, S)`
selection; no mapped-scope fallback; non-exact scopes are ignored as absent while a selected scope
still refuses on its carrier; the selection applies at every depth. §9 lists the cases. No new field,
cause token or schema.

## 3. Source35 applicability and reachability — kept separate by standing

| Standing | Evidence | What it shows |
|---|---|---|
| **atom-api** (synthetic) | Q3; root's probe | frozen35 answers `all-covered=true` for **10** mutations of the calls dependency scope on **both** endpoints: absent, null and different `sourceUniverse`/`relation`/`resolution`, including an in-ladder rung `syntactic-callee-name`. Deleting the scope gives unknown. Also a synthetic depth-2 wrong-universe scope |
| **native carrier** | Q2; root | absent/null refused; different values admitted by the carrier alone |
| **native producer** (`admit_coverage_result_v3`) | Q2 | **all 10 excluded**: 6 raise schema validation (absent/null); 4 refuse `native.coverage-key-scope-mismatch` plus commitment mismatches |
| **closed Run** (read, not executed) | `identity-model.v3.py:1598-1603, 1654-1678`; `evaluator_input_model.v3.py:161-163, 193` | closure admits every view scope as `subject-scope`, requires `coverage.scopeId` in `view.scopeIds` (`COVERAGE_SCOPE_JOIN`), and re-runs producer admission, which joins key coordinates to the scope. Reconstruction copies every view scope and maps each Coverage to its envelope `scopeId`. So on reconstructed admitted inputs, an exact-coordinate Coverage always maps to a scope `_scopes_exact` already selects, and the fallback **cannot be taken** |
| **closed enumeration / retained Run** | not run | no full-Run counterexample was constructed or claimed |

**Conclusion.** The defect is at the published synthetic atom API, and the reference is looser than
its own prose. It is excluded by source35's strong admission (producer boundary measured, closure
read). The correction therefore changes no result for any admitted Run input I can identify, and it
removes the looseness at the API.

## 4. Reviewer v35 (final) — accounted

The v35 run finished while I was working (`process-completion.json` exit 0). I read its final
`review.md` and `review.json` (`d7dc035c…`).

- **Its verdict** is ACCEPT of **source35** bytes: MUST-34-01 and A-12 closed, no new MUST or SHOULD.
  That acceptance covers frozen35, **not** these successor bytes, which need root reconciliation and
  review.
- **Its advisory A-13** is this defect. It describes the fallback that "consumes a scope without
  carrier validation or key join", as advisory because `close_run` cannot reach it. That agrees with
  §3.
- **A-13's seven healed cases:** `sourceUniverse` absent/null/U2, `relation` absent/`references`, and
  `resolution` absent/`syntactic-callee-name`. All are inside my matrix, and **none heals on the
  successor**.
- **Difference with A-13's list:** my probe and root's also measured `relation: null` and
  `resolution: null` (and out-of-ladder `resolved-binding`) as healed on frozen35. A-13 does not list
  them. I did not investigate their harness; all of them are unknown on the successor.
- **A-13 says** the §4 carrier sentence is stricter than the reference on this branch. After the
  correction, a non-exact scope is **not consumed at all**. The answer equals the scope-deleted answer,
  which is the reviewer's own lawful criterion ("either a refusal or identical to the scope-deleted
  answer"), and the new sentence says so explicitly.
- **Final disposition** of A-13 against these bytes remains with root.

## 5. Full three-file delta (my bytes only)

Full diffs are in `probes/receipts/q6-diffs/*.author.diff`; root's layer is in `*.root-after-v1.diff`.

| File | frozen35 sha256 | successor sha256 | bytes | lines |
|---|---|---|---|---|
| `foundation/atom-evaluation-contract.v1.md` | `f6c3b375a359d0fcac657ecf2f55213ad80e3c7bb368dd6656d181b9df979ce3` | `72986bd35f7f2b2cd5d4e5e989036a974744c682a9db877ca08bd9ac52aa2d5a` | 42,761 → 43,729 | +2 / −2 |
| `foundation/atom_model.v1.py` | `c1243ca9bd1e2b73aac4456d09df18813b7dc7e72e141a577d908519e2dc9660` | `2c5fdabb93785349c9c9a77ddf253685309727724d98897f60a0e8abf7177dac` | 93,999 → 94,415 | +12 / −12 |
| `foundation/check-atoms.v1.py` | `11aa038a56e84b0142b496d0d3d77beac90d7f323d3c64047294ca50455dd2c8` | `67d8c656ff912e023bc00fb56825568bbae9a3c5641cd23e869c11e5c2f159f5` | 130,180 → 141,025 | +191 / −0 |

- **Model:** `_select_dep_coverages` loses the nine-line mapped fallback and its `dep_scopes` guard, and
  gains a docstring stating the law. Nothing else changed.
- **Contract:** the §4 dependency sentence expanded; §9 cases appended.
- **Checker:** 6 new cases plus builders. **No existing line changed.**
- No `[DECISION]`, `TODO`, `TBD` or `XXX` in any owned file. The successor tree has 12,899 files, none
  added or removed, and exactly these three differ from frozen35.

## 6. Controls, commands and results

**`check-atoms.v1.py`: 95/95 pass** (`check-atoms-successor`). The **original 89 passed on the
corrected model before any new control existed** (`check-atoms-model-only`). **No previous expected
outcome, fixture or assertion changed.** Q1 instruments the selector: **0** of the 89 original cases
ever reach the fallback precondition, on frozen35 or on the successor.

Q4 runs every successor case against both models:

| New control | successor | frozen35 model | What it pins |
|---|---|---|---|
| `test_dependency_mapping_to_non_exact_scope_is_absent` | pass | **fail** | 10 mutations × 2 endpoints: unknown, dependency not cited, `coverage-unknown`@U1 + `required-relation-missing`, **equal to the dependency-deleted answer** (ignored, not refused) |
| `test_dependency_non_exact_scope_keeps_known_matches` | pass | **fail** | a known reachability fact keeps `exists` true, `none` false, `count≤0` false and its id; `count≤1` and `all-covered` become unknown (true with an exact dependency) |
| `test_dependency_rule_applies_at_every_depth_synthetic_graph` | pass | **fail** | synthetic `calls→declares` extension, restored afterwards: exact is true; wrong-universe second-level scope is unknown and not cited |
| `test_dependency_exact_scope_pairing_and_carrier_refusal` | pass | pass | exact mapped true; exact commitment-only true; exact unpaired unknown; exact scope over another subject unknown; non-exact beside exact-unrelated unknown (the two branches now agree); exact scope missing `enumeratorClosure` refuses `ATOM_NATIVE_CARRIER` |
| `test_dependency_incoming_disjoint_scopes_order_independent` | pass | pass | lawful disjoint dependency scopes, one mapped and one commitment-paired, over 12 orderings → 1 result, true, cited once ascending |
| `test_dependency_different_kind_whole_source_unchanged` | pass | pass | clones→declares: no declares unknown; unscoped or mapped-to-wrong-universe declares Coverage stays whole-source true |

The original 89 also pass on the frozen35 model.

**Probes.**

- **Q1:** fallback instrumentation.
- **Q2:** native-producer admission of the mutations.
- **Q3:** full shape matrix on both trees. Frozen35 was rerun as `.2` after adding cases.
- **Q4:** discrimination.
- **Q5:** consumers.
- **Q6:** custody, delta and pins.

**Consumers (Q5).** Every checker importing the atom model ran on both trees with no arguments:
`check-replay.v3`, `check-semantic-replay.v3`, `check-candidate-replay.v3`, `check-execution-replay.v3`,
`check-execution-inputs.v1`, `check-provider-attribution-return.v2` and `check-composition.v3`. All
seven exit 0 on both trees with **byte-identical stdout**. That is no-regression evidence only.

**Not run, by instruction:** the integrated groups and pin sealing.

## 7. Dependencies on other owners

- **Pins (root):** 15 rows are intentionally stale and root must reseal them.
  - `native/source-pins.v2.json` and `security/source-pins.v1.json`: `pins/1069`, `1070`, `1073`.
  - `workflows/source-pins.v1.json`, `foundation/source-pins.v1.json` and
    `foundation/evaluator3-source-pins.v1.json`: `files/1069`, `1070`, `1073`.
  - These cover the contract, model and checker respectively. No file was added, so **no pin addition
    is owed**, and `check-atoms.v1.py` is already job `atoms`.
- **Schemas and other owners:** nothing required. The fix needs no schema or join change.
- **Root reconciliation:** reviewer v35 accepted frozen35 and recorded A-13 against it. These successor
  bytes need root reconciliation and a fresh independent review of the final bytes.

## 8. Remaining issues and limits

1. **Pre-existing, not corrected — a partial dependency census in incoming whole-scope views.** Take an
   incoming primary reachability scope over {f, g}, with an exact calls dependency scope for **f
   only** (g's missing, or at the wrong universe). `all-covered` answers **true** on frozen35 **and** on
   the successor (Q3 `incomingPartialDependencyObservation`). One subject's partition fills the
   dependency position for the whole primary scope. The law "pair dep Coverage to current-source scopes
   containing those native ids" does not say every id must be covered. This needs a normative decision
   on per-subject dependency totality, which is outside this bounded correction. It is atom-api evidence
   only; closed-Run reachability is not established.
2. **No closed enumeration admission and no retained or closed Run** was built. Strong-boundary
   applicability is producer-measured plus closure read-level.
3. **The depth-2 control uses a synthetic graph;** the published `DEPENDS_ON` has depth 1.
4. **Stale pins, integrated groups** and independent review of these bytes remain with root.

## 9. Probe history kept

- `q3-shapes-frozen35` is the first matrix run; `.2` added the lawful disjoint-scope ordering and the
  partial-dependency observation after I found that my first two-provider same-subject shape would be
  refused at closure (`SUBJECT_SCOPE_PARTITION_OVERLAP`). That shape remains in Q3 only as a synthetic
  atom-api row, not as a check-atoms control.
- My first model edit attempt failed on text matching and changed nothing; it was redone after reading
  the exact bytes.
