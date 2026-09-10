# Bounded clarification — consumer-b.v2 finding G8 / S-4 (`plan.budget`)

**Outcome: G8 / S-4 is RETRACTED. The finding was erroneous.**

This is a bounded factual clarification of one finding in my own frozen v7
review. It is **not** a new review and **not** acceptance of any successor. I was
supplied no author implementation code. The other three MUST findings, the other
five SHOULD findings and both advisories are untouched, and the overall verdict
is unchanged.

**Overall verdict remains: CHANGES_REQUIRED** — on M-1, M-2, M-3 and M-4, which
this clarification does not revisit.

---

## 1. Input custody

Same frozen kit as the original review; I re-verified the one file at issue.

| | |
|---|---|
| Selector | `docs/coop/design-corrections/foundation/identity-schemas.v2.json` `#/$defs/plan/properties/budget` |
| Declared SHA-256 (original v7 manifest) | `e7d936045e4ffc67aae9a9248b4cf4bb19bb8c5e2db372df67363b3eadbb52b7` |
| Recomputed SHA-256 | `e7d936045e4ffc67aae9a9248b4cf4bb19bb8c5e2db372df67363b3eadbb52b7` |
| Declared / actual bytes | 87 743 / 87 743 |
| Exact match | **yes** |
| Manifest self-digest | `785b829ae6ad8ac965e159e2397c20eba860fe6562ec01fdf30cd6a45168a004` |
| Whole original 43-file kit re-verified after this work | intact, 0 mismatches |

No original kit, output, review or work file was edited. My probe imports the
frozen original tools read-only and never runs their mains. Everything new is
under `/tmp/opensip-design-corrections/consumer-b.v2-clarification/`.

**Original finding reference:** `output/blind-review.json` → `findings[id=G8]`
(severity SHOULD, reported in `blind-review.md` §4 as **S-4**), and the
`invented[]` row `"plan.budget = {unit: work-units, limit: 100000}"`. Retained
immutable at
`/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/consumer-b.v2/`.

---

## 2. The frozen bytes

```json
{
 "type": "object",
 "additionalProperties": false,
 "required": ["unit", "limit"],
 "properties": {
  "unit":  {"const": "work-units"},
  "limit": {"type": "integer", "minimum": 1, "maximum": 9007199254740991}
 }
}
```

`plan.budget` is a **closed** record: `additionalProperties: false`, both keys
required, `unit` pinned to the constant `work-units`, `limit` a bounded integer.

It is further **byte-identical** to
`#/$defs/semantic-configuration/properties/analysis/properties/budget`
(verified by canonical-key comparison, not by eye).

---

## 3. Discriminating check

I validated the budget **in situ inside the whole `#/$defs/plan` record**, using a
real Plan from my original TypeScript vector, so nothing depends on how the
subschema is quoted. **16 of 16 cases agree with the closed-record expectation;
0 disagreements.**

| Case | Observed |
|---|---|
| `{"unit":"work-units","limit":100000}` | **ADMIT** |
| `limit` = 1 (minimum) | **ADMIT** |
| `limit` = 9007199254740991 (maximum) | **ADMIT** |
| `{}` empty | REFUSE |
| missing `unit` | REFUSE |
| missing `limit` | REFUSE |
| extra key | REFUSE |
| `unit` = `"seconds"` | REFUSE |
| `limit` = 0 | REFUSE |
| `limit` = −1 | REFUSE |
| `limit` = 9007199254740992 (max+1) | REFUSE |
| `limit` = `true` | REFUSE |
| `limit` = `"100000"` | REFUSE |
| `unit` = `true` | REFUSE |
| budget is an array | REFUSE |
| budget is `null` | REFUSE |

Lexical admission, which precedes schema validation
(`admission-and-qualification.md` §1), additionally refuses the float-spelled
forms that JSON Schema alone would treat as integer-valued:

| | |
|---|---|
| `"limit":1.0` | `ADMIT.FLOAT_TOKEN:1.0` |
| `"limit":1e5` | `ADMIT.FLOAT_TOKEN:1e5` |
| duplicate `limit` key | `ADMIT.DUPLICATE_KEY:limit` |

This independently reproduces the result Codex reports.

---

## 4. Confirmation, and how I got it wrong

**I confirm the correction and retract G8 / S-4 in full.** Every factual claim in
the finding is false against the frozen bytes:

| G8 claimed | Frozen bytes |
|---|---|
| "a bare `{\"type\": \"object\"}`" | a closed record with four keywords |
| "no `additionalProperties`" | `additionalProperties: false` |
| "no required keys" | `required: ["unit", "limit"]` |
| "the shape exists [in the configuration]; the Plan just does not reference it" | the Plan carries a **byte-identical** copy of that shape inline |

**Root cause.** In early exploration I dumped the `plan` record through a
whitelist helper that extracted only `type`, `const`, `enum`, `pattern`,
`minimum`, `maximum`, `x-opensip-digest`, `x-opensip-order`, `$ref`, `maxLength`,
`minItems` and `maxItems`. It did not extract `required`, `additionalProperties`
or nested `properties`, so `budget` rendered as `{"type": "object"}`. I wrote the
finding's statement from that truncated rendering.

**The aggravating part is not the truncation, it is the reconciliation I never
did.** My own probe `gaps.py::g8` later dumped the *complete* subschema into
`observed.planBudgetSchema`, and that field in `gaps.json` and in
`blind-review.json` already showed `additionalProperties: false` and
`required: ["unit","limit"]`. The finding therefore shipped **self-refuting on its
face**: its evidence contradicted its statement, in the same JSON object. I built
the probe to carry the observed bytes precisely so a reader could check the claim,
then did not check it myself. That is a process failure on my side, not a
disagreement about the design.

**Two consequential corrections follow:**

1. The `invented[]` row `"plan.budget = {unit: work-units, limit: 100000}"` is
   withdrawn. That value was **not** an invention — it is the shape the closed
   schema requires, and my original vectors were correct. The claim that "another
   host may lawfully choose a different key set and mint a different PlanId" is
   false: a different key set refuses at admission.
2. `blind-review.md`'s closing paragraph cites "an unconstrained object inside a
   PlanId" among the SHOULD items. That clause is withdrawn with the finding.

Corrected SHOULD count: **five**, not six. Corrected total open design gaps:
**nine** (4 MUST + 5 SHOULD), not ten.

---

## 5. Is there a different, real budget issue?

I looked, and I am reporting **one advisory-level observation with an actual
reproducer**, plus one candidate I considered and am explicitly **not** raising.
Neither restores G8.

### ADV-B1 (advisory) — the Plan commits two independent copies of the budget

**Exact selectors**

- `identity-schemas.v2.json` `#/$defs/plan/properties/budget`
- `identity-schemas.v2.json` `#/$defs/plan/properties/resolvedConfigDigest`
- `identity-schemas.v2.json` `#/$defs/semantic-configuration/properties/analysis/properties/budget`
- `identity-and-evidence.md` §3 closure list: *"Snapshot config/scope, Plan
  config/scope and native-context source correspondence must agree."* — names
  config and scope; the budget field is not named.
- `admission-and-qualification.md` §1.1: *"`analysis` always contains
  `profileId`, `capabilities` and the complete `{unit,limit}` budget supplied by
  the authenticated compiled defaults and then overridden by admitted layers."*

**Observation.** The Plan commits the budget twice — once inline as
`plan.budget`, once transitively through `resolvedConfigDigest`, whose
`semantic-configuration.analysis.budget` is the byte-identical closed record.
Admission §1.1 says the layer resolution already produces *the* budget. No
sentence in the five contracts requires the two to agree.

**Actual reproducer** (executed, `clarification-probe.json` →
`residualBudgetObservation.reproducer`). Both Plans commit the same
`resolvedConfigDigest` `f0b2…`-committed configuration whose
`analysis.budget` is `{unit: "work-units", limit: 100000}`:

| | budget | schema-valid | closes under my original closure checker | PlanId |
|---|---|---|---|---|
| Plan A | `{unit:"work-units", limit:100000}` | yes | **yes** | `plan2:e71889b3eeda043d57ab3ce67e5791d1739caae3cb400abf9180382e6cc07c32` |
| Plan B | `{unit:"work-units", limit:7}` | yes | **yes** | `plan2:bc13a62c0b3af2288e13c41fe8935b516565e6adebe80ba6d68254a5fff672e1` |

Plan B's fully re-keyed Run also closes
(`run2:0d79a3bbca85a79b93e66356d09e74ee2f6b0b13064b0c1d2744444bae90b0dd`). So a
Plan whose inline budget contradicts its own committed configuration is admitted
and seals.

**Countervailing reading, stated because it is strong.** A per-invocation
narrowing of the configured budget is a plausible intended meaning, and either
way the Plan stays deterministic and independently replayable because **both**
values enter PlanId. Nothing about identity, replay or the digest law is broken.
That is precisely why this is **advisory** and not a MUST or a SHOULD, and why it
is not a substitute for the finding I retracted. If the two are meant to be equal,
one sentence in identity §3's closure list ("and Plan budget") closes it; if they
are meant to differ, one sentence saying so closes it equally.

### Considered and NOT raised

`identity-and-evidence.md` §4 says the declarative rule program defines a
"deterministic work bound … for each predicate" and that the predicate DAG "is
bounded by the rule program's admitted work bound", while
`policy-document.schema.json#/$defs/RuleProgramV1` carries no work-bound field
(`schemaVersion`, `policyDigest`, `rules` only) and `Atom.n` is a `count-at-most`
threshold, not a work bound. I am **not** raising this: `workflows-and-surfaces.md`
§5 supplies real structural bounds (depth ≤ 8, ≤ 64 nodes per rule, ≤ 512 rules)
that are schema-enforced, so the DAG *is* bounded and "the rule program's admitted
work bound" reads naturally as those admitted structural caps. Naming it would be
a conjecture about wording, not a reproducible defect, and I have just been
reminded what that costs.

---

## 6. Standing

- G8 / S-4 **retracted**; the `invented[]` row and the closing-paragraph clause
  are withdrawn with it.
- ADV-B1 **newly recorded at advisory severity**, with an executed reproducer.
- M-1 (payload schema document law), M-2 (fact payload encoder), M-3
  (`resolvedNodeModulesLayout`), M-4 (`tsconfigGraphHash`), S-1, S-2, S-3, S-5,
  S-6, A-1, A-2, A-3 and the G12 confirmation: **untouched, not re-examined
  here**, and none of them depends on G8.
- Overall verdict **CHANGES_REQUIRED**, unchanged and not changed *because* G8 was
  erroneous. It rests on the four MUST items.
- No readiness grade, no product qualification, no implementation authorization,
  no acceptance of any successor. No commit, push, or access to current author
  changes.
