I'll resolve the outstanding `rule-program` / `evaluationInputRefs` law-interaction against the kit's actual MUST statements, then update only this origin's successor four-Run grades.Prior bytes are intact. Next I’ll read every MUST on `predicateProofs.inputRefs`, `evaluationInputRefs`, and `ProofInputRef.domain` before deciding whether syntax-data can still admit.I’ll write a bounded analysis script that measures the four claimed proofs, builds kit-derived examples, and records the disposition without reminting graphs.**Disposition: existing law, jointly satisfiable. Not a contradiction.**  
**syntax-data ADMIT is withdrawn.** Successor four-Run verdict remains `OTHER_RUNS_REFUSED`.

Wrote only `/tmp/opensip-design-corrections/consumer-b.v12-kit-law-interaction-review.v1/output/` (`law-interaction-review.md`/`.json`, successor `other-runs-review.md`/`.json`). Prior self-audit bytes unchanged. Stores not reminted.

## MUST vs PERMIT

| Constraint | Strength | What it does |
|---|---|---|
| enumeration §7 / composition §1 / execution-inputs §7 | **MUST** | `evaluationInputRefs` = `selectedRefs` + `{domain:execution-inputs, digest}` |
| `InputRefV1.domain` | **MUST** (closed enum) | selectedRefs may be view/import/coverage/subject-inventory/target-attribution/incoming-search/candidate-producer-result. **`rule-program` is not a member.** |
| identity §3 | **MUST** | “Predicate input refs are a subset of evaluationInputRefs” |
| composition §3 | **MUST** | Witnesses cannot add roots |
| proof-bundle `ruleProgramDigest` | **MUST** (required field) | Program is bound here |
| `program-predicate.ruleProgramDigest` | **MUST** | Equals the proof’s digest; addresses a node; does not restate the program |
| `ProofInputRef.domain` | **PERMITS** | Shared item type for several arrays. Listing `rule-program` is vocabulary, not a command that every array include it |

A shared-type enum member is admissible in the type. It does not override field-specific MUSTs.

## Joint shape

Lawful together:

- `evaluationInputRefs` = selectedRefs ∪ `{execution-inputs}` (no `rule-program`)
- `predicateProofs[].inputRefs` ⊆ that set (therefore no `rule-program`)
- program bound by required `proof.ruleProgramDigest` and `program-predicate.ruleProgramDigest`

Putting `rule-program` on predicate `inputRefs` without putting it on `evaluationInputRefs` breaks the subset MUST (exported shape **B**). Putting it on `evaluationInputRefs` to save the subset breaks enumeration §7 (shape **C**, already refused in v1). Omitting it from both arrays and keeping the required digest fields is shape **A**.

Kit-derived examples are in `probes/logical-examples.json` (reasoning evidence, not replacement admission).

## Measured operands (all four claimed proofs)

Every graph: `evaluationInputRefs = selectedRefs + execution-inputs` holds; `rule-program` is **not** in `evaluationInputRefs`; each predicate `p` cites `{domain:rule-program, digest:<ruleProgramDigest>}`. That is shape **B**. Checker `compose_proof` inserts the same citation; C equality of that shared derivation is not admission.

## Grades

- **Diagnostic exception withdrawn.** The subset sentence is a structural identity-closure MUST, not semantic atom truth, and not optional because the shared type permits the domain.
- **syntax-data:** ADMIT withdrawn → structural `REFUSED`, fullsemantic `NOT_REACHED`. First refusal: `predicate-inputRefs-subset-of-evaluationInputRefs` (extra `71aaef89…`).
- **ts / rust / rust-partial:** native first refusals unchanged (`compilerPackageDigest` tree membership; `rustcVersion` ≠ closure `semanticVersion`). Subset also fails on those claimed proofs; it does not replace those earlier first refusals.

Existing-law correction: stop citing `rule-program` on predicate `inputRefs`; do not add it to `evaluationInputRefs`. No normative edit.

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-law-interaction-review.v1/output/independent/law_interaction.py
```
