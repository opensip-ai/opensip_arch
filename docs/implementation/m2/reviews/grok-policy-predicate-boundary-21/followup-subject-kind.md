# Follow-up: first-kind is selected law; predicate API must not take caller proof context

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Disposition of advisory21 “ambiguous fallback” and public `inspect_predicate_address` args. Original advisory21 bytes **unchanged**. **Not ACCEPT-DESIGN-UNIT. Not a silent new law.**
**Original pins:** `advisory.md` 12386 / `55f48b2e…e1c6`; `advisory.json` 3342 / `b0c4dffb…7bb5`.
**Probe:** `probes/subject_kind_fallback.py` loading actual `workflows_model.v3.py`.

## (A) First-kind is deterministic selected behavior

v3 `admit_atom` 30:

```
kind = ('symbol' if subject_kind=='export' else subject_kind) if subject_kind else next((k for k in kinds if k), None)
```

`kinds` is the **closed registry row** (`sourceSubjectKinds` or `[sourceSubjectKind]`, else `targetKinds` for `endpoint==target`), list order as in `evaluator-projection-registry.v1.json`. That is a **deterministic** default, not an unspecified choice. Advisory21’s “ambiguous fallback / do not copy” **mischaracterized** the selected function.

**Removing that default, or requiring `subjectEnumeration.subjectKind` on the program path, would change the selected reference.** It must not be implemented in `policy.rs` without an independently reviewed successor.

## (B) No schema-valid rule that policy admits and the program path rejects

`Atom` (policy-document.v2) has **no** `subjectKind` field (`additionalProperties: false`). `_admit_atom` therefore always sees `atom.get("subjectKind") is None` and `_applicable_kinds(..., None)` returns the **full** registry kind list. The program-path first kind is **always a member** of that list.

Probe (actual `W.admit_policy_rule` vs `W.walk_atoms(..., W.admit_atom(atom, rid))`):

| Rule | Policy (`subjectKind` passed) | Program (`subject_kind=None`) |
| --- | --- | --- |
| `file@enumerated`, enumeration `file` | **admit** | **admit** |
| `runtime-observation@observed`, `symbol`, evidenceUse runtime | **admit** | **admit** |
| `runtime-observation@observed`, `file` | **admit** | **admit** |
| `test-execution@observed`, `package` | **admit** | **admit** |
| `calls@resolved-callee`, `symbol`, source or target | **admit** | **admit** |
| `file@enumerated`, enumeration **`symbol`** | **refuse** `POLICY.UNKNOWN_RULE` | **admit** (first kind `file`) |

There is **no** probed schema-valid rule that policy **accepts** and the program path **rejects** because of `subject_kind=None`.

The **opposite** difference exists (`file` atom + enumeration `symbol`: policy refuses, program admits). That rule **cannot** appear in a compiled program: `close_run` 1774–1777 admits every policy rule **before** 1781–1784, and `rule_program_digest` copies those `emitWhen` trees. So the reverse gap is not a live `open_run_closure` success-path split.

Passing `rule['subjectEnumeration']['subjectKind']` into program `admit_atom` would make the reverse case fail on the program path too — still a **new** law if applied outside already-admitted policies, and observationally **redundant** on the selected close_run success path.

**Relation-only** program admission (skip the kind argument): for schema-valid atoms it matches first-kind, because first-kind is already in `_applicable_kinds(None)`. It would **drop** `ATOM_KIND_INCOMPATIBLE` if a future atom carried a kind field; the selected Atom schema has none. It does **not** skip `_admit_atom` filter/endpoint/rung checks (those do not use the synthetic `{kind}` beyond that membership test). Still a successor if specified as a new program-path contract.

**Disposition:** candidate **reference/design correction only if** a later unit wants program-path kind to equal enumeration kind even for callers other than `close_run`. **Do not silently implement.** Keep v3 line 30 as selected.

## (C) `inspect_predicate_address` must not take caller proof context

Advisory21 sketched `inspect_predicate_address(..., emit_when, proof_predicates, evaluation_refs, ...)`. That would let a caller **pretend** selection by supplying trees and sets.

**Revise:** either

1. **Internal-only** helpers (`predicate_node_at`, child addresses, node digest) used by an evaluator function that receives **retained ids** (`proof_id` / `run_id`) and **rehashes** `proof`, `ruleProgramDigest` blob (RuleProgramV2), `plan.policyDigest`, and witness records from `RetainedInputs`; **or**
2. Public `inspect_predicate_address(inputs, proof_id, predicate_index, work)` that **derives** `emitWhen` from `program.rules[ruleId]`, `proof_predicates` from `proof.predicateProofs`, and `evaluation_refs` from `proof.evaluationInputRefs`.

Do **not** accept caller `emit_when` / proof-sets as authority. Same rule as run-links: retained Run/proof ids, not caller arrays.

## (D) Unicode addresses

Unchanged: `followup-predicate-digits.md` / `.json`. Helper `isdigit`+`int` ≠ prose shortest-decimal; superscripts uncaught `ValueError`. Not a Rust ASCII inference.
