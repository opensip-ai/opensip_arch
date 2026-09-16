# Source-author correction — MUST-34-01 and A-12 (incoming-binding successor)

**Standing.** Architecture/design/reference authorship by the actual Claude source-author origin
`823bf66b-e92a-4789-ab81-63a1a9dc371d`. Written only to this runtime and to three files in
`/tmp/opensip-design-corrections/incoming-binding-successor.v1/source`. Frozen34, the prior authoring
tree, prior reviews, pin ledgers, generated reports, navigation/readiness records and live files were
not edited. **Nothing here is independent acceptance, blind acceptance, application, readiness,
activation or product qualification.** No commit, push or other agent. No consumer, runtime, report
or root-blind data was an input.

Interpreter for every command: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Every command,
stdout, stderr and exit is retained under `probes/receipts/<label>/`; repeated labels take a numeric
suffix, so failed attempts survive. `review.json#/commands` lists all of them.

---

## 1. Inputs and custody

- Frozen34 manifest `bd00c07d…c3f6` matches its declared digest; all **12,899** frozen34 files match
  it, none extra (`p5-custody-delta-pins.2`).
- The three owned files were byte-equal to frozen34 and the manifest before any edit
  (`before-hashes.json`).
- After the correction the successor tree still has 12,899 files, none added or removed, and exactly
  the three owned files differ.
- I read the complete independent `review.md`, the `newMustIssues`, `advisories` and
  `sourceChangeAssessment` portions of `review.json`, and the q09, q10 and q11 probes and receipts.
  **q10's matrix parser measured nothing and is not used**; q11 replaces it.
- The independent-review runtime had 0 files modified after this runtime began. Root's
  `root-source35-preparation.v1` had 3 (`capture-completed-author-delta.py`, `verification-runbook.md`,
  `verification-tool-read.json`). No command here targeted that directory, and I did not read them.

## 2. MUST-34-01 — decision

**Accepted as a real design defect, and corrected conservatively.** It is pre-existing, not a 34
regression.

Frozen34 defines incoming owed programs as the plan bindings for `capabilityForRelation`. The
incoming loop visits only **available** universes. When the subject universe *U* has none, *U→U* is
never accounted. On my own atom-api controls, frozen34 answers a **certain negative** in four shapes:

- *U* unbound with a same-family *U2* fully evidenced
- foreign-family available only
- foreign-family unavailable only
- foreign-family available and unavailable

In each, `none`, `count-at-most 0` and `all-covered` are `true` and `exists` is `false`
(`p1-must-matrix-frozen34.3`).

### The published rule — contract §4, incoming step I1

| | |
|---|---|
| **Precondition** | `endpoint=target`, P2 did not return, and **no available owed binding has `universe = U`** — the same test as outgoing step 1 |
| **Emission** | `selector-unbound`, `evidenceKind: null`, `nativeCause: null`; `universe` key omitted, projected null. Identical to outgoing step 1's record. No coordinate equal to *U* exists to attribute, and naming *U* would present an unsearched program as an examined partition |
| **Effect** | blocking (`complete=false`, `unknown=true`) and **not a return**: every other owed universe and provider is still accounted, and its causes emitted |
| **Precedence** | after P1 and P2, before per-universe accumulation; at most once; order independent |
| **Unavailable bindings** | never satisfy I1 (their universe is null). Beside an owed-family unavailable binding, `unavailable-program-binding` and `selector-unbound` are both kept |
| **Foreign-family-only** | `unknown` with `selector-unbound`; both `cross-family-edge-not-owed` routes (null and *S*) kept |
| **Explicit selection scope** | a narrowed request narrows the work requested, not what an incoming negative must have searched |
| **Known evidence** | matching is untouched: known matches keep `exists`, `none` and an exceeded `count-at-most`; only completeness-dependent answers become `unknown` |

The existing typed vocabulary fits, so no new cause token, field or schema is introduced. The
incoming-owed-programs sentence now states that the subject universe is always an owed source.

### Frozen34 versus successor on the real atom API

Standing: atom-api, synthetic inputs (P1, same builders, only the model differs).

| Inputs | incoming `none`/`exists`/`count≤0`/`all-covered` | causes added |
|---|---|---|
| *U* unbound + *U2* evidenced | `true`/`false`/`true`/`true` → **all unknown** | `selector-unbound` |
| *U* unbound + foreign available only | same → **all unknown** | `selector-unbound` (the *UR* disclosure is kept) |
| *U* unbound + foreign unavailable only | same → **all unknown** | `selector-unbound` (the null disclosure is kept) |
| *U* unbound + foreign available and unavailable | same → **all unknown** | `selector-unbound` (both disclosures kept) |
| *U* unavailable same-family + *U2* | already unknown | `selector-unbound` beside `unavailable-program-binding` |
| *U* unbound + unknown-family unavailable (synthetic-only) | already unknown | `selector-unbound` |
| no references binding anywhere (P2) | unchanged | — |
| *U* bound + evidenced (alone, with *U2*, with foreign) | unchanged | — |
| *U* bound, unevidenced | unchanged: unknown with its own *U* causes | — |
| *U* bound + unknown-family unavailable (synthetic-only) | unchanged | — |

That is 24 changed incoming cells (16 value changes, 8 cause-only) and **0** outgoing cells changed.

**Known incoming matches** (`imports`, two known facts, *U* unbound):

- `none` stays `false`, `exists` `true`, `count-at-most 1` `false`; `selector-unbound` is added and
  both known fact ids are retained.
- `count-at-most 2` goes `true` → unknown, and `all-covered` goes `true` → unknown.
- With *U* bound, all five are unchanged.
- Without facts and *U* unbound, all five become unknown.

**Multi-provider:** two providers on *U2* plus a foreign program. Across 12, 12 and 48 insertion
orders, each case gives **one** result on both models. "*U* unbound, both *U2* providers evidenced"
goes `true` → unknown, and "*U* bound" stays `true`.

### Reachability — evaluated honestly

- **Default profile:** the reviewer's q11 finds no engine family mixing `NOT-SELECTED` with
  requested modes. I read its code and receipt and found the logic sound; I did not re-execute it.
- **Explicit narrowing:** the retained analysis-spec and the enumeration cell join are **per ownership
  tuple** (`enumeration_model.v1.py:632-637` compares cells with
  `(capabilityId, languageMode, workspaceRoot, required)`). The capability matrix says an explicit
  override narrows the *request*, not the obligation. In the text I read — enumeration contract §1,
  `enumeration_model.v1.py:615-684`, the matrix `explicitOverride`/`requiredDefault`, and
  `admission-and-qualification.md:60-110` — I found **no rule** requiring a request to cover every
  unit for every capability.
- **Not demonstrated:** I did not run `admit_enumeration`, did not build a retained Run, and did not
  establish whether product-configuration can express per-unit narrowing.
- **Conclusion:** the premise is not shown invalid at any admission boundary I examined, and not shown
  reachable at closed enumeration admission. Root's position of no demonstrated full-Run counterexample
  stands. The correction does not depend on reachability; it removes the ambiguity at the published
  atom API.

## 3. A-12 — decision

**Accepted.** The prose is corrected, plus one atom-api admission tightening that validation of item 2
required.

1. **Scope-less provider group.**
   - Table row 1 now reads "no source scopes (no admitted attestation can exist for it)".
   - A new *Admitted inputs* note states the reasons: `scopeRefs` `minItems: 1` plus the
     exact-owned-scopes join, so an attempt is a **global** `INCOMING_SEARCH_SCHEMA` refusal, not an
     unknown.
   - The note names the admitted closure: an explicit **empty-subject** scope owned by the provider,
     with complete *S→U* Coverage or a qualifying attestation. It qualifies no provider.
   - No schema or admission change. Measured identically on both models (P2): stock schema refuses
     `[]`; atom-api refuses the attestation; an unpaired empty scope gives `scope-without-coverage`;
     paired or attested, it closes; the native carrier admits `subjects: []`.
2. **Scope without `enumeratorClosure`.** The reviewer is right **at the native carrier**: key absent
   and key null both refuse. It was not the whole story at the atom API.
   - Frozen34's `_scope_descriptor` returned `None` when a field was **missing**, so a key-absent scope
     skipped the carrier, reached the untagged fallbacks, and answered **`none=true`** when attested or
     paired (P2).
   - Frozen34 also admitted an attestation naming such a scope, and answered `true` for both a
     `references` and a `calls` incoming atom (P6).
   - `_scope_descriptor` now passes fields through, so the carrier refuses absent exactly like null:
     when an evaluation pairs the scope, and during global `IncomingSearchV1` admission, which pairs
     every named scope.
   - Measured: 4 atom-api cells went ADMIT → `ATOM_NATIVE_CARRIER`, and P6's global admission went
     ADMIT → REFUSE. Key-null results, the empty-subject rows and the stock-schema/native-carrier rows
     are unchanged.
   - The prose states the untagged fallback describes no admitted input. That fallback is a tightening
     toward the owning `subject-scope` schema (all eight fields required); no schema or join law was
     loosened.

## 4. Full three-file delta

Full diffs: `probes/receipts/p5-diffs/`.

| File | frozen34 sha256 | successor sha256 | bytes | lines |
|---|---|---|---|---|
| `foundation/atom-evaluation-contract.v1.md` | `d7ef1336874fb1a70316cad3069725a6178c16c9bd9e39913516fc5c930c3417` | `7ee61c184f8eca780831c6b3c8b1c26c5d07664b670fea6293b0bf7b6d327f85` | 36,951 → 42,624 | +61 / −4 |
| `foundation/atom_model.v1.py` | `a5e082a5490d8babc75756f48649965f1824b9600f34598d50573320fdc23aee` | `c1243ca9bd1e2b73aac4456d09df18813b7dc7e72e141a577d908519e2dc9660` | 93,272 → 93,999 | +21 / −19 |
| `foundation/check-atoms.v1.py` | `c5de4a84167f24de66fd9c0c7a8696c3f081fd6a9ac9efe5a011e97e861d572c` | `258099be979f77f3ce36d7f003d499b20f9c0204a61f7c1a97b1ce2b564c053f` | 111,998 → 129,889 | +312 / −1 |

- **Contract:** the §4 I1 block; "subject universe always owed" in incoming owed programs; table row 1;
  the *Admitted inputs* note; §9 conceptual cases.
- **Model:** I1 (five lines in `_native_completeness`'s incoming branch). `_scope_descriptor` passes
  fields through, and `_derive_scope_commitment` drops its dead `None` guard. P1/P2 prelude,
  outgoing, pairing and folding, all three cause channels, attestation joins and dependency traversal
  are untouched, and the untagged branches are kept as defensive code.
- **Checker:** 8 new cases plus builders, and one fixture value corrected (§5).

No `[DECISION]`, `TODO`, `TBD` or `XXX` in any owned file.

## 5. Controls, commands and results

`check-atoms.v1.py`: **89/89** pass (`check-atoms-successor.2`). Before the new controls existed, the
original 81 already passed on the changed model (`check-atoms-model-only`). **No previous expected
result changed.**

One previous **fixture** changed. In `test_dep_fold_replaces_whole_records_and_keeps_ties`, the
unresolved-edge class `dynamic-import` became `dynamic-import-nonliteral`. The old value was not a
native `UnresolvedEdgeKindV1` member, and the case asserts whole-record equality, so its expectation
is unchanged.

P3 runs every successor case against both models (`p3-controls-discriminate.2`):

| New control | successor | frozen34 model |
|---|---|---|
| `test_incoming_unbound_subject_universe_is_blocking` | pass | **fail** |
| `test_incoming_unbound_subject_universe_foreign_family_only` | pass | **fail** |
| `test_incoming_unbound_subject_universe_with_unavailable_obligations` | pass | **fail** |
| `test_incoming_unbound_subject_universe_keeps_known_matches` | pass | **fail** |
| `test_incoming_unbound_subject_universe_multi_provider_order_independent` | pass | **fail** |
| `test_scope_without_enumerator_closure_refuses_at_atom_api` (evaluation + global admission) | pass | **fail** |
| `test_incoming_bound_subject_universe_and_p2_unchanged` | pass | pass — non-regression pin |
| `test_scopeless_provider_group_admission_boundary` | pass | pass — pins the A-12(1) facts, which needed no code change |

The original 81 pass on the frozen34 model too.

**Consumers (P4).** The atom model changed, so every checker importing it ran on both trees with no
arguments: `check-replay.v3`, `check-semantic-replay.v3`, `check-candidate-replay.v3`,
`check-execution-replay.v3`, `check-execution-inputs.v1`, `check-provider-attribution-return.v2` and
`check-composition.v3`. All seven exit 0 on both trees, with **byte-identical** stdout. That is
no-regression evidence only; I did not establish that any of those fixtures reaches I1.

**Not run:** the six broad groups, integrated suites and pin validation. Root does those after
resealing.

## 6. Standings — nothing promoted between them

| Standing | What stands on it |
|---|---|
| helper-unit | `test_dep_fold_replaces_whole_records_and_keeps_ties` (unchanged) |
| atom-api | all eight new controls; P1; P2 atom-api rows; P6 |
| stock schema | P2 `IncomingSearchV1` `scopeRefs: []` under jsonschema alone |
| native carrier | P2 `subject_scope_commitment` rows |
| closed enumeration admission | **not run** |
| strong retained Run | **not run**; P4 is reference-checker no-regression only |

## 7. Dependencies on other owners (not edited)

- **`foundation/incoming-search.schema.v1.json`**, joins item "…; untagged scopes fall back to all S
  scopes". It describes no admitted input; the contract now says so, and the owner should drop that
  clause.
- **Pins:** 15 rows go stale — `native/source-pins.v2.json` and `security/source-pins.v1.json`
  `pins/1069,1070,1073`, plus `workflows`, `foundation` and `foundation/evaluator3` `files/1069,1070,1073`.
  No file was added, so **no pin addition is owed**. `check-atoms.v1.py` is already wired as job
  `atoms` in `run-evaluator3-checks.py`.

## 8. Remaining issues and limits

- MUST-34-01 reachability beyond synthetic atom-api plus stock schema is undemonstrated.
- A scope lacking `enumeratorClosure` that no attestation names and the evaluated atom never pairs is
  still not carrier-validated at the atom API; it contributes to no value. I first expected global
  admission not to validate named scopes and drafted that as an issue; P6 showed it does, and the draft
  was withdrawn.
- Unknown-family obligations are measured only with an unregistered `languageMode` that the
  enumeration-plan schema refuses (synthetic-only).
- The untagged-scope branches in `_incoming_groups` and `_admit_incoming_searches` remain as defensive
  code, unreachable for admitted scopes.

## 9. Probe errors kept on the record

- `p1-must-matrix-frozen34`: TypeError sorting None against str in cause tuples, a probe bug; rerun as `.2`.
- `p1-must-matrix-frozen34.2`: the order harness reversed schema-sorted plan cells and corrupted
  `cellOrdinal` joins. Its `distinctResults: 2` is a **probe artefact, not a finding**; rerun as `.3`
  with only admitted-shape-free orders varied.
- A shell scan over `docs/` for the configuration schema was denied by the permission mode and
  replaced by Grep.
- The first `check-atoms-successor`, `p3-controls-discriminate`, `snapshot-after` and
  `p5-custody-delta-pins` runs predate the global-admission extension of the A-12 control and the
  final contract sentence; their `.2` reruns are the final results.
