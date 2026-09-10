# Law-interaction review: predicate `inputRefs` × `evaluationInputRefs` × `ProofInputRef.domain`

**Disposition: `RESOLVED_EXISTING_LAW`** — jointly satisfiable under existing law. Not a demonstrated normative contradiction.

Bounded follow-through on the self-audit law-interaction. Same original P4 kit-only reviewer session. Not a new origin. Not whole-consumer ACCEPT. No store remint.

## Custody

| Object | SHA-256 | Match |
|---|---|---|
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | True |
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | True |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | True |
| v2 snapshot-manifest | `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` | True |
| preserved selfaudit.md | `b4e8cabd3b8ea92e4dd724f2b27f43a2be8fcd802067d2b485fd8c12211fa469` | True |
| preserved selfaudit.json | `ef06a3c532450fc3eb946f2e7faa5e148e8860622b21a2dac5e95b8a7fb9adc2` | True |

Command: `/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-law-interaction-review.v1/output/independent/law_interaction.py`

Stores were not reminted. Copied checker write paths were redirected; mechanical diff is `probes/admit_run.path-redirect.diff`.

## MUST versus PERMIT

### `M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI` — MUST

Source: `foundation/enumeration-contract.v1.md §7`

> The proof's `evaluationInputRefs` must equal the execution manifest's selected references plus that manifest's own `execution-inputs` reference.

### `M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI-COMPOSITION` — MUST

Source: `foundation/evaluator-composition-contract.v3.md §1`

> `evaluationInputRefs` equals its selected references plus that one manifest reference.

### `M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI-EXEC` — MUST

Source: `foundation/execution-inputs-contract.v1.md §7`

> require `evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest}`. ... Do not add policy/schema roots to `selectedRefs`.

### `M-SELECTEDREFS-DOMAIN-ENUM` — MUST (schema closed enum)

Source: `foundation/execution-inputs.schema.v1.json#/$defs/InputRefV1/properties/domain`

> selectedRefs item domain enum is exactly view|import|coverage|subject-inventory|target-attribution|incoming-search|candidate-producer-result. rule-program is not a member.

### `M-PREDICATE-INPUTREFS-SUBSET` — MUST

Source: `docs/v2/contracts/product-v1/identity-and-evidence.md §3 (closing digest law, lines 515–516)`

> Predicate input refs are a subset of evaluationInputRefs; evidence view roots equal the named views and coverage roots equal their coverage union.

### `M-WITNESSES-CANNOT-ADD-ROOTS` — MUST

Source: `foundation/evaluator-composition-contract.v3.md §3`

> All input references are direct retained roots or members of an evaluated view as the identity closure permits; witnesses cannot add roots.

### `M-FINDING-CITES-NO-EXTRA-ROOTS` — MUST

Source: `docs/v2/contracts/product-v1/identity-and-evidence.md §3 lines 194–200`

> Finding citations cannot introduce extra authoritative input roots. ... A well-formed, hash-valid object outside this closure is refused, rather than admitted as hidden finding evidence.

### `M-PROOF-RULEPROGRAMDIGEST-REQUIRED` — MUST (required field)

Source: `foundation/identity-schemas.v3.json#/$defs/proof-bundle required[] and properties.ruleProgramDigest`

> proof-bundle required includes ruleProgramDigest; x-opensip-digest representation=canonical-record selector #/$defs/RuleProgramV2.

### `M-PROGRAM-PREDICATE-RULEPROGRAMDIGEST` — MUST

Source: `foundation/identity-schemas.v3.json#/$defs/program-predicate properties.ruleProgramDigest description; identity-and-evidence.md §3 lines 1147–1151`

> `ruleProgramDigest` equals the proof bundle's; it addresses one predicate node of the admitted RuleProgramV2; it does not restate the node.

### `M-EVAL-INPUTREFS-NAMES-PLAN-IMPORTS` — MUST

Source: `identity-and-evidence.md §3 lines 517–519`

> The evaluator3 proof also names every Plan-selected import in evaluationInputRefs.

### `P-PROOFINPUTREF-DOMAIN-ENUM` — PERMITS (shared type vocabulary)

Source: `foundation/identity-schemas.v3.json#/$defs/ProofInputRef/properties/domain`

> Closed enum includes rule-program among view, import, coverage, policy, waiver, schema, blob, ... execution-inputs. This is the shared item type of evaluationInputRefs, predicateProofs[].inputRefs, evaluation-deficiency.inputRefs, and cache-key inputRefs. An enum member is admissible in the type; it is not a field-specific requirement that every such array contain that member.

### `P-BYDOMAIN-RULE-PROGRAM` — PERMITS (digest representation when that domain is used)

Source: `identity-schemas.v3.json#/x-opensip-digest-domains/byDomain/rule-program`

> When a ProofInputRef/Ref carries domain=rule-program, representation is canonical-record RuleProgramV2. This is the join recipe IF that domain is selected, not a command to select it in predicate.inputRefs.

## Joint satisfiability

**Contradiction:** `False`

evaluationInputRefs = selectedRefs ∪ {execution-inputs}; predicateProofs[].inputRefs ⊆ evaluationInputRefs and therefore cannot name rule-program; the program is bound by required proof.ruleProgramDigest and by program-predicate.ruleProgramDigest (equal to the proof field). ProofInputRef.domain remains a shared closed vocabulary that permits rule-program on other ProofInputRef arrays (e.g. a deficiency inputRef) without requiring it on predicate.inputRefs.

The shared `ProofInputRef` type **permits** `domain=rule-program`. Identity §3 **requires** predicate input refs ⊆ evaluationInputRefs. Enumeration §7 / composition §1 / execution-inputs §7 **require** evaluationInputRefs = selectedRefs + execution-inputs. `InputRefV1.domain` **does not include** `rule-program`, so selectedRefs cannot lawfully name it. Therefore a predicate `inputRefs` member `domain=rule-program` cannot be in evaluationInputRefs without breaking enumeration §7, and cannot stay out of evaluationInputRefs without breaking the subset MUST.

That is a constraint on **which array members are selected**, not a hole in the type. The program is already a required proof field (`ruleProgramDigest`) and a required field of `program-predicate` (equal to the proof's digest). Witnesses cannot add roots (composition §3). Binding the program through those required fields, and omitting it from both arrays, satisfies every MUST above. The enum remaining live on other ProofInputRef arrays (deficiencies, cache keys) is not a command to cite it from predicates.

Adding `rule-program` to evaluationInputRefs to save the subset (shape C) is the correction v1 already refused against enumeration §7. It is not available as a waiver.

## Kit-derived logical examples (reasoning evidence, not Run admission)

- **A jointly satisfying:** jointly satisfies enumeration §7 MUST, composition §1 MUST, identity §3 subset MUST, and proof.ruleProgramDigest / program-predicate.ruleProgramDigest MUSTs. ProofInputRef.domain still permits rule-program as a shared-type vocabulary member unused in these two arrays.
- **B exported shape:** enumeration §7 holds; identity §3 subset FAILS. This is the exported four-Run shape.
- **C add to evaluationInputRefs:** subset would hold only by violating enumeration §7 / composition §1 / execution-inputs-contract §7 (do not add policy/schema roots to selectedRefs; evaluationInputRefs = selectedRefs + execution-inputs).

## Actual retained operands (already measured; reconfirmed)

| Run | evaluationInputRefs domains | predicate inputRef domains | subset | eval=selected+EI | extras |
|---|---|---|---|---|---|
| `ts` | ['coverage', 'execution-inputs', 'import', 'subject-inventory', 'view'] | ['coverage', 'rule-program', 'view'] | False | True | `[{'predicateId': 'p', 'ref': {'digest': 'bfc392674a431ed3b5e4ce966011236950fbab873273e86ef9a1319dddbeb615', 'domain': 'rule-program'}}]` |
| `rust` | ['coverage', 'execution-inputs', 'subject-inventory', 'view'] | ['coverage', 'rule-program', 'view'] | False | True | `[{'predicateId': 'p', 'ref': {'digest': '67416e803513efd33d5a80aaef8fb4505da71895add95f763e976950be919e7b', 'domain': 'rule-program'}}]` |
| `syntax-data` | ['coverage', 'execution-inputs', 'subject-inventory', 'view'] | ['coverage', 'rule-program', 'view'] | False | True | `[{'predicateId': 'p', 'ref': {'digest': '71aaef89749857b54552f394b368a64df5a3c70df079daf7109ee1bcc9381b40', 'domain': 'rule-program'}}]` |
| `rust-partial-clones` | ['coverage', 'execution-inputs', 'subject-inventory', 'view'] | ['coverage', 'rule-program', 'view'] | False | True | `[{'predicateId': 'p', 'ref': {'digest': '224cfc675965fb19212f7f84c7b293f0201212aa1f25fac5b03d19a6316e944d', 'domain': 'rule-program'}}]` |

All four claimed proofs match shape **B**. `proof.ruleProgramDigest` is populated on each. Checker `compose_proof` inserts the same `rule-program` citation; C equality of that shared derivation is not admission.

## Disposition of the diagnostic and syntax-data grade

WITHDRAWN as an admission exception. The subset sentence is a MUST. Marking it diagnostic/notUsedAsFirstRefusal was a silent checker branch. C equality of compose_proof (which inserts domain=rule-program into predicate.inputRefs) with the claimed proof is the same derivation, not independent establishment of the subset.

WITHDRAWN ADMIT. Successor: structural REFUSED; fullsemantic NOT_REACHED. First refusal: predicate-inputRefs-subset-of-evaluationInputRefs.

Layer: structural (identity §3 closure of the claimed proof record's citations). Not semantic atom truth. Do not invent semantic comparison as the gate.

## Existing-law correction guidance

Do not place domain=rule-program on predicateProofs[].inputRefs. Bind the program with proof.ruleProgramDigest and program-predicate.ruleProgramDigest. Do not add rule-program to evaluationInputRefs or selectedRefs. Checker compose_proof must stop inserting that citation; expected proofs must obey the same MUSTs without copying claimed inputRefs.

No normative edit. No invented semantics. No whole-consumer ACCEPT.

