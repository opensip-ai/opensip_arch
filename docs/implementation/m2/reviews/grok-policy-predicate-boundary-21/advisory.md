# Advisory: policy/program admission + predicate-program address

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded next-owner map after run-links-19 (draft: 1651–1687 + 1808–1828, 252 local cases). **Not ACCEPT-DESIGN-UNIT. Not implementation. Not replay. Not run-19 source.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-policy-predicate-boundary-21/review`. No live/frozen/history edits.

Selected identity `619d6e3c…41e6` / 158555. Live lock independently **16 inventory / 21 contract** (runtime v8). Native e678 is **not** a caller here.

`workflow_admission()` (identity 23–31) loads **`HERE.parent/workflows/workflows_model.v3.py`**. The published v3 at `docs/coop/design-corrections/workflows/workflows_model.v3.py` **22494** / `60f28dc9…6123` re-exports historical v1 (`be37023f…66dc` / 142811) then **overrides** `rule_program_digest`, `admit_atom`, `admit_policy_rule`. `walk_atoms` is **not** overridden (v1 1358–1366).

## Actual call order (`open_run_closure`)

After walk, run-root joins (1651–1687), native, `UNIVERSE_FRAME_UNRETAINED` (1755):

**Policy / compiled program (1757–1784)** — before stages (1788) and before run-19 phase-2 (1808–1828):

1. `foreign_payload(plan.policyDigest, 'workflows/schemas/policy-document.v2.schema.json', '#/$defs/PolicyDocumentV2')` (1758)
2. `foreign_payload(plan.waiverDigest, 'workflows/schemas/policy-document.schema.json', '#/$defs/WaiverSetV1')` (1759) — **shape only**; no `admit_policy_rule`
3. `foreign_payload(proof.ruleProgramDigest, same v2 schema, '#/$defs/RuleProgramV2')` (1760)
4. `W=workflow_admission()` (1761)
5. `program.policyDigest == plan.policyDigest` else `RULE_PROGRAM_POLICY_JOIN` (1762)
6. **`W.rule_program_digest(policy) == proof.ruleProgramDigest`** else `RULE_PROGRAM_COMPILATION_JOIN` (1763)
7. **every** `policy.rules`: `W.admit_policy_rule(rule)` → wrap `POLICY_RULE_NOT_ADMISSIBLE:policy:<ruleId>:<detail>` (1774–1777)
8. **every** `program.rules`: `W.walk_atoms(emitWhen, λ atom: W.admit_atom(atom, ruleId))` → `POLICY_ATOM_NOT_ADMISSIBLE:program:<ruleId>:<detail>` (1781–1784)
9. `rules = {ruleId: program rule}` (1785) — used later at 1843

**Predicate-program address (1829–1852)** — after finding membership (1822–1828), **before** per-view joins (1853):

| Line | Check | Refusal |
| ---: | --- | --- |
| 1829–1830 | index `(ruleId, subjectId) → {predicateId}` | (build) |
| 1832 | `pred.inputRefs` ⊆ `proof.evaluationInputRefs` (canonical) | `HIDDEN_PREDICATE_INPUT` |
| 1833–1834 | `pred.scopeIds` ⊆ union of named views’ `scopeIds` | `PREDICATE_SCOPE_ROOTS` |
| 1835–1837 | witness facts/coverages ⊆ those views | `WITNESS_FACT_ROOTS` / `WITNESS_COVERAGE_ROOTS` |
| 1838–1839 | `payload(programPredicateDigest, 'program-predicate')` | shape |
| 1840 | `addressed.ruleProgramDigest == proof.ruleProgramDigest` | `PROGRAM_PREDICATE_PROGRAM_JOIN` |
| 1841–1842 | ruleId / predicateId / operation join pred | `PROGRAM_PREDICATE_ADDRESS_JOIN` / `OPERATION_JOIN` |
| 1843 | `pred.ruleId ∈ rules` (compiled program, not policy) | `PROGRAM_PREDICATE_RULE_UNKNOWN` |
| 1844 | **`predicate_node_at(emitWhen, predicateId)`** (651–665) | `PREDICATE_ADDRESS` / `_LEAF` / `_RANGE` |
| 1845 | `node.op == addressed.operation` | `PROGRAM_PREDICATE_NODE_OPERATION` |
| 1846 | **`admit_program_predicate_node(node)`** (668–681) | `PROGRAM_PREDICATE_NODE_RECORD:<selector>` |
| 1847 | `sha256(C.canonical(node)) == nodeDigest` | `PROGRAM_PREDICATE_NODE_DIGEST` |
| 1848–1849 | `sorted(witness.childPredicateIds) == sorted(predicate_child_addresses)` | `WITNESS_CHILD_ADDRESS_JOIN` |
| 1850 | children ⊆ proof predicates for **same** `(ruleId, subjectId)` | `WITNESS_CHILD_NOT_PROVEN` |
| 1851–1852 | `countLimit` typed-equal `node.n` iff `op==count-at-most` else `None` | `WITNESS_COUNT_LIMIT_JOIN` |

Witness program-predicate is an **address into the admitted RuleProgramV2**, not a second language (identity-v3 2747–2809). `nodeDigest` is **fragment** retention of `#/$defs/Predicate` on `workflows/schemas/policy-document.v2.schema.json`.

Not this owner: walk, native, stages (1788–1794), import admission, view-joins, replay, **predicate evaluation** (true/false/unknown).

## Closed vocab / compilation vs declarative admission

**v3 `rule_program_digest` (workflows_model.v3.py 13–15):** refuse `schemaMajor!=2`; `doc_digest({schemaVersion:2, policyDigest: doc_digest(policy), rules: [{ruleId, ruleProgramRef, emitWhen} for each policy rule]})`. **Not** v1’s `schemaVersion:1` (v1 48–52). Using v1 digest fails `RULE_PROGRAM_COMPILATION_JOIN`.

Projection **copies `emitWhen` trees**; it does not compile a new language. Identity 1778–1780: program rules are `{ruleId, ruleProgramRef, emitWhen}` with **no** `evidenceUse`; compilation join already forces exact projection of the **same** admitted policy rules.

**v3 `admit_policy_rule` (35–49)** — **not** v1 1369: unique `evidenceUse` kinds; visit `emitWhen` with **count>64 or depth>8** → `predicate node/depth bound`; leaves call `admit_atom(node, ruleId, subjectEnumeration.subjectKind)` and require `node.evidence ∈ declared`.

**v3 `admit_atom` (24–33)** — **not** v1 1326: registry row from `foundation/evaluator-projection-registry.v1.json` (`65f163cc…5abb` / 60005); `_admit_atom` on `atom_model.v1`; unregistered relation → `POLICY.UNKNOWN_RULE`.

**v1 `admit_atom` (1326–1355)** still exists on `_base` but is **overridden**. v1 also checks relation **ladder** membership. v3 delegates field/endpoint/rung to `A._admit_atom`. Identity 1764–1769 still requires Run closure to close relation/rung (not schema-only).

**`walk_atoms` (v1 1358–1366):** and/or operands, not operand, else visit leaf. **No** 64/8 bound. Program path (1781) uses this + `admit_atom(atom, rid)` with **`subject_kind=None`**.

## Ambiguous fallback (must not copy)

v3 `admit_atom` 30: if `subject_kind` is None, `kind = next((k for k in kinds if k), None)` — **first listed kind**. Policy rules pass `subjectEnumeration.subjectKind`. **Program atoms do not.** Do not treat first-of-`targetKinds`/`sourceSubjectKinds` as the policy subject. Either pass the policy rule’s `subjectKind` into program `admit_atom`, or admit program atoms as **relation/rung only** (identity comment 1778) without inventing a kind. Silent first-kind is an **ambiguous fallback**.

v1 `glob_match` (1296–1321) is the reconstructable predicate of `glob-pattern-contract.v1.md` (`9b12ef44…8ba0` / 3946): case-sensitive, whole-string, split on `/`, `*`/`?` intra-segment, `**` whole segments, no braces/classes/escapes, no `.`/`..` resolution, Unicode **scalars**. Not `fnmatch`, not gitignore. Inventory `policy.rs` description already names this contract.

## Predicate addressing (identity 646–681)

- Root address `p`; `a.i` = i-th and/or operand; `a.0` = not operand. **Shortest decimal, no leading zero** (`01` → `PREDICATE_ADDRESS`).
- Leaf: `predicate_child_addresses` = `[]`; indexing a leaf → `PREDICATE_ADDRESS_LEAF`.
- `admit_program_predicate_node`: memo `(document, selector, C.canonical(node))`; `validate_registered_record` → because document is **`workflows/...`**, identity 51–54 calls **`W.validate_import_record`**, not the foundation ExactValidator. v1 Predicate selector would refuse v2-only `endpoint` / `all-covered` (docstring 672–673).
- Node digest is **raw SHA-256 of canonical node bytes**, not H-frame.

`proof_predicates` is per **(ruleId, subjectId)**; a child proven for another subject does not satisfy `WITNESS_CHILD_NOT_PROVEN`.

## Proposed bounded evaluator APIs

Inventory already plans `crates/evaluator/src/policy.rs` (**compiler**): admit/compile closed declarative policy; own portable glob. **Not live.** Host `policy.rs` is a **different** planned file (binding generation). Do not conflate.

```
# policy.rs — borrowed workflow helpers become THIS owner
glob_match(pattern, candidate) -> bool          # glob-pattern-contract.v1 only
admit_atom(atom, rule_id, subject_kind: Option) # no first-kind fallback
admit_policy_rule(rule)                         # evidenceUse + 64/8 + atoms
walk_atoms(node, visit)
rule_program_digest(policy) -> [u8;32]          # v3 schemaVersion 2 projection
admit_policy_document(raw) -> PolicyDocument    # schemaMajor==2; sorted unique ruleIds (v3 resolve_policy 51-58)
```

```
# program_predicate.rs (minimal new validator) — needs compiled program from policy.rs
inspect_predicate_address(
  inputs, proof_id, pred, witness_digest, emit_when, proof_predicates, evaluation_refs, work
) -> Result<PredicateAddressChecks, PredicateAddressError>
```

Implements 1832–1852 using `predicate_node_at` / `predicate_child_addresses` / `admit_program_predicate_node` / canonical node digest. Does **not** evaluate the atom. Does **not** accept PlanNativeChecks or CoverageAdmission tokens. Orchestrator: run-links phase1 → native → **policy.rs 1757–1784** → stages → run-links phase2 → **program_predicate** → view-joins.

Identity stays foreign_payload + joins; evaluator owns the language. **No** identity→evaluator. Waiver remains shape-only until a later owner.

## Distinguishing borrowed helper vs caller

| Helper | Actual close_run role |
| --- | --- |
| v3 `rule_program_digest` | **caller 1763** compilation join |
| v3 `admit_policy_rule` | **caller 1775** every policy rule |
| v1 `walk_atoms` (borrowed) | **caller 1782** program trees only |
| v3 `admit_atom` | policy via admit_policy_rule (with subjectKind); program via walk_atoms (**no** subjectKind — fallback trap) |
| v1 `glob_match` | **not invoked** at 1757–1852; required by policy **filters** / host scope (`in_scope` v1 1323) and inventory `policy.rs` description |
| `predicate_node_at` | **identity 1844**, not workflow |
| `validate_import_record` | node record admission 678 |

Retention: policy/program/waiver/program-predicate/predicate-witness are **retained canonical records** (`foreign_payload` / `payload`). Glob engine is a **pure predicate** over admitted strings, not a filesystem.

## Adversarial cases

| Case | Expect |
| --- | --- |
| Policy `schemaMajor!=2` | `EVALUATOR_POLICY_MAJOR` inside digest / resolver; not relabelled v1 |
| Digest with v1 `{schemaVersion:1,...}` | `RULE_PROGRAM_COMPILATION_JOIN` |
| `declares` atom `minResolution=resolved-callee` | `POLICY_RULE_NOT_ADMISSIBLE` (rung not on that ladder) |
| Evidence atom, empty `evidenceUse` | `IMPORT.ABSENT_FOR_PREDICATE` on **policy** path (1775), not only resolve_policy |
| Program `admit_atom` with `subject_kind=None` using first registry kind | **must not** silently change plane vs policy subjectKind |
| Predicate id `p.01` | `PREDICATE_ADDRESS` |
| Address into exists leaf `.0` | `PREDICATE_ADDRESS_LEAF` |
| `and` children `['p.1','p.0']` vs sorted join | `WITNESS_CHILD_ADDRESS_JOIN` if not permutation-equal after sort — sorted both sides so order of witness list may differ |
| Child proven for other `subjectId` | `WITNESS_CHILD_NOT_PROVEN` |
| `count-at-most` with `countLimit=None` | `WITNESS_COUNT_LIMIT_JOIN` |
| `exists` with `countLimit=0` | same |
| Node digest of parent tree, not located node | `PROGRAM_PREDICATE_NODE_DIGEST` |
| v1 Predicate selector on v2 `all-covered` node | `PROGRAM_PREDICATE_NODE_RECORD` |
| `fnmatch` / gitignore glob | **not** the portable contract (`a/**/b`, terminal `**`, `?` = one scalar) |
| Caller ADMIT / Plan counts as program membership | refuse; rehash retained policy+program |

## Semantic dependencies

- Portable glob: `glob-pattern-contract.v1.md` + v1 `glob_match` (not invoked at these lines but **required** for `policy.rs` as inventoried).
- Atom registry + `atom_model.v1._admit_atom` (v3 admit_atom).
- PolicyDocumentV2 / RuleProgramV2 / Predicate schemas (workflows policy-document.v2).
- Exact canonical `doc_digest` / `C.canonical` for compilation and nodeDigest.
- Relation ladders (v1 admit_atom / atom owner) — closed vocab, no “any rung” fallback.

## Verdict

**NOT ACCEPTANCE.** Next owners: planned evaluator **`policy.rs`** (v3 digest + admit_policy_rule + glob contract, no first-kind fallback) and a **minimal `program_predicate` inspector** for 1829–1852 that requires that compiled program. Run-19 stays 1651–1687 / 1808–1828. No caller ADMIT, count tokens, or replay.
