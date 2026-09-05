# Clean-sheet adjudication rule — v1 (PRE-REGISTERED)

**Status: FROZEN ON FIRST SIGHT OF CLEAN-SHEET OUTPUT.**
Written before any clean-sheet derivation exists. Any amendment made after the
clean-sheet output has been read is **void**, and the pre-amendment text governs.

**Author:** Agent 3 — who authored most of the incumbent design and is therefore
**disqualified from adjudicating it**. That is why this rule exists and why it is
written now.

---

## What this decides

Whether the incumbent architecture (`architecture/`, `artifacts/`) is
**problem-derived** or **codebase-derived**, and what the merged result should be.

The two inputs:

| Label | What it is |
|-------|-----------|
| **INCUMBENT** | The existing design set. Authored with knowledge of the current implementation, audited for migration contamination but **not** independently derived |
| **CLEAN-SHEET** | One or more derivations produced under hard isolation from the codebase and from the incumbent |

## Scope

**In scope:** architecture decisions present in either set.

**Out of scope — the clean-sheet has no authority here:**
- Product decisions (ecosystem goal, contribution ontology, portability depth,
  provider languages). A derivation agent cannot decide product intent.
- Measurement-gated decisions (execution topology deployment questions). No
  derivation settles these; only measurement does.
- Anything already decided by the product owner.

A clean-sheet opinion on an out-of-scope item is recorded as **advisory** and
changes nothing.

---

## The Justification Test

The single load-bearing mechanism. Applied to **incumbent** decisions only,
because the incumbent is the contaminated side.

> **State the requirement that forces this decision — without referring to the
> existing implementation, its history, its structure, its package layout, or any
> measurement taken from it.**
>
> If the requirement cannot be stated that way, the decision is **INHERITED**, not
> derived.

Notes on applying it:

- "The current system does X badly, so we do the opposite" **fails**. Inverting a
  pain point is not a derivation.
- "Users need results to be reproducible later" **passes** — it is a requirement
  statable without the codebase.
- A measurement may support a passing justification only if it is
  **construct-valid, externally valid, and taken on a representative workload**.
  A measurement of the existing rule corpus is none of those for design purposes.
- "It is simpler / more elegant / more symmetric" **fails**. Aesthetics are not
  forcing.

---

## Classification

Every decision is placed in exactly one class.

| Class | Meaning |
|-------|---------|
| **MATCH** | Both sets reach the same decision |
| **DIVERGE** | Both address it; decisions differ |
| **ONLY-INCUMBENT** | The incumbent decided it; no clean-sheet derivation needed to |
| **ONLY-CLEANSHEET** | A clean-sheet decided it; the incumbent never addressed it |

## Disposition rules

### MATCH

| Condition | Disposition |
|-----------|-------------|
| Both FORCED, same requirement | **CORROBORATED** — strongest available evidence of problem-derivation |
| Both FORCED, different requirements | **CORROBORATED-WEAK** — record both requirements; the forcing story is less certain than either side thought |
| Incumbent FORCED, clean-sheet PREFERRED | Incumbent's necessity claim is **DOWNGRADED to PREFERRED**. Reaching the same answer does not validate the claim that it was compelled |
| Both PREFERRED | **CONVERGENT-JUDGMENT** — likely right, explicitly not forced |

### DIVERGE — resolve in this order, stop at the first that applies

1. **Correctness.** If one option violates a stated requirement, it loses. No
   further testing.
2. **Justification Test on the incumbent.** Fails → **CLEAN-SHEET WINS**.
3. **Passes** → a genuine judgment difference. Prefer, in order: fewer public
   versioned contracts; fewer moving parts; fewer irreversible commitments.
4. **Still tied** → record **UNRESOLVED** and escalate to the coordinator.
   **The incumbent does not win by default, and neither does the clean-sheet.**

### ONLY-INCUMBENT — the highest-signal class

**Presumed INHERITED. The burden of proof is on the incumbent.**

A decision that an independent derivation never needed to make is likely solving a
problem that exists only in the current implementation.

| Outcome | Disposition |
|---------|-------------|
| Passes the Justification Test **and** names the forcing requirement | **RETAINED** — record the requirement; it was a genuine gap in the clean-sheet |
| Fails | **REMOVED** from the architecture, or **DEMOTED** to `steering/` if it is a real migration concern |

### ONLY-CLEANSHEET

**Presumed a genuine gap in the incumbent.** Adopt unless it violates a stated
requirement or an out-of-scope product decision. "We considered and rejected it"
counts only if that rejection is recorded in the incumbent set **before** the
clean-sheet output is read.

---

## Multiple derivations

If N independent clean-sheet derivations are run:

| Agreement | Reading |
|-----------|---------|
| All N reach the same decision as the incumbent | **Strong** corroboration |
| Some agree, some diverge | The question is genuinely open. Treat the incumbent decision as **PREFERRED at best**, never FORCED |
| Derivations disagree among themselves and with the incumbent | Evidence the question is under-determined by the requirements — record as such rather than picking a winner |

A decision matched by 1 of 3 derivations is **not** corroborated.

---

## Who adjudicates

- **Not Agent 3** for any incumbent decision it authored.
- **Not the clean-sheet agent** for its own output.
- Agent 1 or Agent 2 — whichever authored less of the disputed artifact.
- The coordinator for out-of-scope product items.

**Every disposition must record the evidence used.** An unevidenced disposition is
void and the decision returns to UNRESOLVED.

---

## Anti-gaming clauses

1. This rule is **frozen** the moment any clean-sheet output is read. Post-hoc
   amendments are void.
2. **Ambiguity in this rule resolves against the incumbent.** The contaminated
   side bears the cost of unclear rules.
3. No decision may be **reclassified** after its disposition is recorded.
4. The incumbent's status markers (`SEALED`, etc.) carry **no weight** in
   adjudication. A sealed incumbent decision that fails the Justification Test
   still loses — sealing recorded agreement among contaminated parties.
5. "It would be expensive to change" is **not** an argument in scope. That is a
   `steering/` concern.

---

## Pre-committed reporting

These figures must be published **regardless of how favourable they are**:

| Metric | Why it is pre-committed |
|--------|-------------------------|
| Incumbent decisions passing / failing the Justification Test | The direct answer to "was this problem-derived?" |
| FORCED claims downgraded to PREFERRED | Measures over-claimed necessity — an error pattern already recorded four times |
| ONLY-INCUMBENT count and dispositions | Measures how much was inherited |
| ONLY-CLEANSHEET count | Measures what codebase familiarity caused us to miss |
| UNRESOLVED count | Honest measure of what this exercise could not settle |

**Interpretation, fixed in advance:**

- **>80% of incumbent decisions pass the Justification Test, few ONLY-INCUMBENT
  removals** → the design is substantially problem-derived. The original concern
  is answered.
- **Significant ONLY-INCUMBENT removals, or many FORCED downgrades** → the design
  is substantially codebase-derived and was rationalised afterward. The merged
  result should be rebuilt from the clean-sheet spine with incumbent decisions
  re-added only as they pass the test.
- **High UNRESOLVED** → the requirements are under-specified, and that is the
  finding. Do not resolve it by preferring either side.

## What this rule cannot do

It cannot detect a decision that **both** sides inherited from a shared prior —
for example anything traceable to the deleted source briefs, whose framing
influenced the incumbent and may have influenced the requirement statement handed
to the clean-sheet agent. The requirement list itself was written by Agent 3 and
is not neutral; one requirement ("a result must be checkable later, against what
inputs, and reproduce it") points fairly directly at part of the answer. Record
this as a known limit on the strength of any convergence.
