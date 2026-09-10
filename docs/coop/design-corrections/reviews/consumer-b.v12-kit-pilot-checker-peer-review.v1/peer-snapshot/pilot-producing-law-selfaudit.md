# Pilot producing-law self-audit

**Verdict: `PILOT_FULL_ADMITS`**

Same P5 pure-data reviewer origin. This is not a new fresh origin and not whole-consumer ACCEPT.
Focused completeness audit of this origin's own checker against the two exact pilot stores
(export-manifest `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f`).

## Prior grade withdrawn

The previous `PILOT_FULL_ADMITS` from `consumer-b.v12-kit-pilot-full-review.v1` is **WITHDRAWN**.

The prior passing grade compared derived proof C after treating hashed, schema-valid ExecutionInputsV1.selectedRefs / cellOutcomes / nativeCoverageAccounts and SubjectInventoryV1 rows as self-authenticating population and selection. Current law requires those records as inputs subject to producing joins: selectedRefs totality from complete receipts + view coverageIds + expected inventories + Plan importIds; outcome state derived then joined; native coverage accounts derived from CoverageResultV3; file inventory rows[].path equal to independently derived KindExtentV1.paths from snapshot+UnitMembershipV1+scope. A matching C is conclusive only after that entire expected record is produced by current law. The prior grade therefore exceeded measured current-law coverage.

That withdrawal is a coverage defect in the prior grade, not a defect found in the stores after the producing joins were executed.
This origin replaces it with a new `PILOT_FULL_ADMITS` only after the producing joins ran and passed on both graphs, then the entire expected proof record was produced by current atom/composition law, then C and enclosing identities were compared.

## Input custody

| Item | SHA-256 | Result |
|---|---|---|
| original 80-file kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS |
| parent frozen subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | PASS |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | PASS |
| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | PASS |
| export-manifest.json (already supplied) | `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f` | PASS |
| exports/syntax-code.store.json | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` | PASS |
| exports/syntax-code.tamper.store.json | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` | PASS |

No new input files. Stores were not reminted or repaired.

## Coverage is not a paragraph count

Each owning document was read start-to-end. Every applicable normative paragraph and every derived record field is inventoried in `producing-law-inventory.json` / `.md` with checker function, operands, and executed result.

- applicable executed-pass: **60**
- applicable executed-fail: **0**
- inapplicable / notReached (justified by admitted committed inputs): **20**

### Admission-only vs derived

Hashed schema-valid ExecutionInputsV1 and SubjectInventoryV1 are **inputs**, not self-authenticating truth.

Independently reconstructed before proof C:

1. `selectedRefs` = complete receipt `outputRefs` ∪ captured view `coverageIds` ∪ expected inventory locators ∪ Plan `importIds` (empty) ∪ candidate/target/incoming (none owed).
2. File/package/symbol extents from retained snapshot + `UnitMembershipV1` + scope-descriptor using published exclusion/kind laws. Complete file `rows[].path` equals derived file extent `{hello.rs}`. Package named-manifest extent empty; complete-empty inventory. Symbol `examinedPaths` equals `{hello.rs}`; declaration rows not recomputed.
3. Native coverage accounts: matrix relation@rung × captured CoverageResultV3; `vcs-change` is `inapplicable-vcs` because admitted VCS `kind=none`.
4. Cell outcome `state=complete` derived from selected U, complete inventories, complete/inapplicable accounts, no candidate owed; joined to host rows.
5. `evaluationInputRefs` = reconstructed `selectedRefs` ∪ `{execution-inputs}`.
6. `subject3` minted from reconstructed file inventory (`hello.rs`, syntax universe, kind=file), not from claimed `selectedSubjectIds`.

`discover_units` re-execution is **notReached**: `discovery-defaults.py` is not in the allowed 80-file kit. Extents were still derived from the retained admitted membership + snapshot + scope. That is kit-bounded, not a convenience skip of a retained producing field.

### Inapplicable branches (admitted committed inputs)

Committed policy is one enabled gating rule `file-present`: `none` of `file@enumerated` with filter `subject eq hello.rs`, universe token `syntax`, subjectKind `file`. Snapshot is `hello.rs` only. Plan `importIds=[]`. No clones-near/clones-cross-tsjs cell. No target-attribution or incoming-search selectedRefs. VCS `kind=none`.

- `ENUM-CANDIDATE-SOURCE-PATHS` — enumeration-contract.v1.md 1: admitted analysis-spec requestedCapabilities are clones-fact, inventory, syntax only
- `ENUM-U1-REDISCOVER` — enumeration-contract.v1.md 1/8: 80-file kit does not include discovery-defaults.py; extents are derived from the retained admitted UnitMembershipV1 + snapshot + scope using published exclusion/kind laws
- `EI-HELPER-FIXTURE` — execution-inputs-contract.v1.md 8: section 8 describes a synthetic host-capture helper, not a retained producing field of these stores
- `EI-IMPORTS-NONE` — execution-inputs-contract.v1.md 1: admitted Plan.importIds = [] on both stores
- `EI-CANDIDATE-NONE` — execution-inputs-contract.v1.md 6: committed capabilities are clones-fact/inventory/syntax; no clones-near or clones-cross-tsjs cell
- `EI-TARGET-ATTR-NONE` — atom-evaluation-contract.v1.md 2: admitted selectedRefs contain no target-attribution; committed rule endpoint defaults to source
- `EI-INCOMING-SEARCH-NONE` — atom-evaluation-contract.v1.md 4: admitted selectedRefs contain no incoming-search; endpoint is source not target
- `EI-ACC-UNSUPPORTED-TYPED` — execution-inputs-contract.v1.md 5: native-capability-matrix.v2.json cells for inventory/syntax/clones-fact × syntax-only are SUPPORTED-DESIGN
- `EI-REQUIRED-CELL-UNSATISFIED` — execution-inputs-contract.v1.md 4: admitted complete inventories and derived complete outcomes; no required-cell-unsatisfied carrier
- `ATOM-TARGET-ATTRIBUTION` — atom-evaluation-contract.v1.md 2: admitted selectedRefs have no target-attribution; committed atom endpoint defaults to source
- `ATOM-INCOMING` — atom-evaluation-contract.v1.md 4: Atom.endpoint defaults to source; emitWhen.relation=file
- `ATOM-ALL-COVERED` — atom-evaluation-contract.v1.md 5: admitted policy emitWhen.op=none
- `ATOM-NONE-TRUE-SUFFICIENCY` — atom-evaluation-contract.v1.md 5: Kleene: none with known match is false; the 'none true also call sufficiency' branch is not taken
- `ATOM-IMPORT` — atom-evaluation-contract.v1.md 6: admitted Plan.importIds=[] and atom.relation=file
- `ATOM-COUNT-AT-MOST` — atom-evaluation-contract.v1.md 3/5: admitted emitWhen.op=none
- `ATOM-EXPORT-KIND` — atom-evaluation-contract.v1.md 1: admitted subjectKind=file
- `COMP-BASELINE` — evaluator-composition-contract.v3.md 6: admitted graph is current-Run evaluator3 only; no baseline2/comparison2 selected
- `COMP-FINDING-EMISSION` — evaluator-composition-contract.v3.md 4: independently, none of file@enumerated with a known hello.rs fact is false, so emitWhen is false and no finding3 is produced
- `COMP-DISABLED-RULE` — evaluator-composition-contract.v3.md 2/5: admitted policy rule file-present enabled=true
- `COMP-BUDGET-EXHAUSTED-OUTPUT` — evaluator-composition-contract.v3.md 3: budget-exhausted output is a conditional branch; it is reached only if preflight exceeds the admitted limit. The preflight assertion itself is executed in Replay._evaluate

Field-specific rules were not waived by a broader schema enum. Example: complete file totality is `rows[].path` set equality to the derived extent, not merely `state` ∈ {complete,partial,unavailable}. Outcome `state` is derived, not accepted because the schema permits `complete`.

## Per-graph result after producing joins

| Graph | Structural | Producing joins | Semantic | First failure |
|---|---|---|---|---|
| syntax-code (positive) | ADMIT | 60 pass / 0 fail | **REPLAY_MATCH** | none |
| syntax-code.tamper | ADMIT | 60 pass / 0 fail | **REPLAY_REFUSE** (required negative) | `REPLAY_PROOF_MISMATCH` after structural admit and producing joins |

Tamper producing inputs are byte-equal to the positive (same selectedRefs, inventories, accounts, views). Independently derived proof C is the positive proof `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71` (`none=false`, verdict `pass`, no findings). Claimed tamper proof disagrees (`fail`, finding3 `0c895614…3cdb`, C `2d2df6df…c9da`). Because the positive has no earlier prerequisite failure, this is an isolated logical-negative.

Atom result (both graphs, independently): occupancy `path=hello.rs` matches retained `file@enumerated` fact ⇒ Kleene **none=false**. `emitWhen` false ⇒ no finding. Gating rule with complete population and no live finding ⇒ rule outcome `pass`, sealed verdict `pass`.

Enclosing identities reconstructed from the derived proof:

- proof3 `8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521`
- evidence3 `4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b`
- seal3 `df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713`
- run3 `4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`
- subject3 `8bf8bec7e09259f035cb9fb392a27ffa0cf7e579b164c20c0181198704b6a3ab`

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-producing-law-selfaudit.v1/output/standalone-checker/check.py
```

Full assertion/operand/result account: `producing-law-inventory.json`.

## Scope

PILOT_FULL_ADMITS scoped to these two stores. Not whole-134 consumer ACCEPT, not product/compiler qualification, not graph-query reconstruction.
