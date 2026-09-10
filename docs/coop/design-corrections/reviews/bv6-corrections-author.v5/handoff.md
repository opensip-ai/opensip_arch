# bv6-corrections-author.v5 — bounded one-comment review

**Role.** Coauthor review of a root-authored comment correction. No source edit;
`work/` read-only. Not independent acceptance, not readiness.

**Verdict: CHANGES_REQUIRED.** BV6-V4-CR-1 is correctly and completely fixed.
Aggregate assent to the exact 17 hashes is withheld for a **second copy of the same
false rationale** that my v4 scan pattern missed.

## 1. Custody — verified, nothing guessed

6839 declared, 6839 present, 0 missing / mismatched / undeclared. The proposal's
`afterSha256` equals the supplied bytes; its `beforeSha256` equals the prior
handoff's `v4Sha256`; the other sixteen files still equal their `finalV4Sha256`;
the supplied diff matches its `diffSha256`. All seventeen `v5Sha256` values were
recomputed from the actual files.

## 2. BV6-V4-CR-1 — CORRECTED, closed

Both defects I raised are retired, and the second is not merely deleted but
**affirmatively reversed**:

* "the SCHEMA CANNOT DECIDE THEM" → "this schema **deliberately leaves** the
  authoritative relation-registry lookup to admission".
* The false causal claim is replaced by its negation: "JSON Schema **can** branch on
  `const`/`enum` even when a property's base type is a broader string", and the
  division is "**not a limitation caused by the relation type**".

It agrees with its owning contexts clause by clause — `repair.schema.json`
`EvidenceRequirement.deficiency` ("THIS SCHEMA DELIBERATELY LEAVES THE AUTHORITATIVE
REGISTRY LOOKUP TO ADMISSION … not a limitation of JSON Schema") and workflows §6
lines 598–604: deliberate leave-to-admission, `oneOf` admitting either vocabulary on
either relation, admission deciding from registry membership, `const`/`enum`
branching possible, and no registry duplication or row fetching. The comment's
*purpose* is preserved — it still explains why these rows sit outside the agreement
table — so nothing load-bearing went with the wrong rationale.

**Independently verified:** full AST identical **including** docstrings; literal
control ids identical (170); only lines 711–716 differ; every differing line is a
comment; line count unchanged. Root's `fullAstIdentical` claim holds.

**No suite run.** The 1787 workflow count is historical from v4 and is *not*
re-measured here. An unchanged AST cannot change it, but that is an inference and I
do not report it as a measurement.

*Observation, not a finding:* the neighbouring control id
`repair.the-schema-alone-cannot-decide-the-plane` still says "cannot". As a
statement about *this* schema as written it is true, and its own failure message
already anticipates a keyword being added, so it carries no false rationale. I am
not raising it.

## 3. CHANGES_REQUIRED — BV6-V5-CR-1 (SHOULD)

`docs/coop/design-corrections/native/native-evidence.schemas.v2.json`
(`19eeba46…7e8f96573`), at
`#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/consumers/0/presenceLaw`:

> "…except for the cross-plane rows, **which the schema cannot decide because
> `relation` is a canonical identifier rather than an enum**; that limit is stated
> rather than papered over."

Both defects survive here — the over-strong "cannot decide" and the false causal
"because … rather than an enum". It is asserted **in the present tense as current
law inside a published registry**, not narrated as history, so it is more
load-bearing than the code comment just fixed, and it now contradicts
`repair.schema.json`, workflows §6 and the corrected checker comment.

This is distinct from `repair.schema.json`'s "an earlier revision wrongly said
exactly one receipt domain exists", which is correct provenance narration and should
stay.

**Remedy:** restate to match the three corrected copies — the two boundaries are
held equal except for the cross-plane rows, which *this schema* deliberately leaves
to admission because it does not duplicate the relation registry as conditionals or
fetch its rows, not because the relation type prevents conditionals. No behavioural
or control change.

**This is my miss.** My v4 scan required CamelCase `CanonicalIdentifier` or the exact
phrase "not an enum, so no keyword", so it did not match this lower-case wording.
The narrow pattern was mine, and it is why absence of a pattern match is not proof of
consistency.

## 4. Prior dispositions — preserved by exact reference

All five v4 patch items (PATCH-00…04) remain **AGREE**, unchanged and not re-opened.
The five v3 root items, eight v2 root items (CX-BV6-01…08), seven original blind v6
findings and my four own findings all stand with their **original severities**, per
`root-input/prior-handoff.json` (`b1d29fef…03de4d51`). My standing qualifications
also carry: the v3 no-prose-substring claim was false; the v3 every-note-point assent
was overstated; the correct retained final-v2 baselines are identity **1345** and
integration **388**; FULL RETAINED-RUN is reserved for the partition controls; and
all imported fixtures are synthetic helper fixtures with formatted-label
fingerprints, not closure identities.

## 5. Aggregate — 17 files, 1 changed this turn

| Path | frozen16 | final v4 | v5 | this turn |
|---|---|---|---|---|
| `check-integration.py` | `df9fbb2e…` | `4422ec24…` | `4422ec24…` | no |
| `foundation/check-identity.py` | `2724276f…` | `1982e2b6…` | `1982e2b6…` | no |
| `foundation/identity-model.py` | `66d8bd5a…` | `650d7942…` | `650d7942…` | no |
| `foundation/relation-payload-schemas.v2.json` | `ef0c244e…` | `53380a24…` | `53380a24…` | no |
| `native/native-cases.v2.json` | `5740aed5…` | `07d990e2…` | `07d990e2…` | no |
| `native/native-evidence.schemas.v2.json` | `2a5fc493…` | `19eeba46…` | `19eeba46…` | no |
| `native/native_evidence_model.v2.py` | `8301e8e3…` | `01b517d3…` | `01b517d3…` | no |
| `workflows/check_workflows.v1.py` | `0af791d5…` | `98adcb93…` | `2fe31439…` | **yes** |
| `workflows/schemas/common.schema.json` | `3f84dff2…` | `16ff6419…` | `16ff6419…` | no |
| `workflows/schemas/imported-evidence.schema.json` | `8acfd72f…` | `edce21a3…` | `edce21a3…` | no |
| `workflows/schemas/invocation-record.schema.json` | `3b89b739…` | `6c5ed3f3…` | `6c5ed3f3…` | no |
| `workflows/schemas/repair.schema.json` | `b8fe3464…` | `65d5f639…` | `65d5f639…` | no |
| `workflows/workflow-cases.v1.json` | `688506e6…` | `22b74430…` | `22b74430…` | no |
| `workflows/workflows_model.v1.py` | `8d45d115…` | `a268aa4b…` | `a268aa4b…` | no |
| `identity-and-evidence.md` | `64a2a019…` | `3d7ca24e…` | `3d7ca24e…` | no |
| `native-evidence.md` | `b50c814c…` | `fafc4abc…` | `fafc4abc…` | no |
| `workflows-and-surfaces.md` | `4a5f0c4e…` | `a6e34134…` | `a6e34134…` | no |

Untruncated values are in `handoff.json#/changedSource/files`.

## 6. Limitations

Bounded one-comment review, not a full source review. No suite run. Design reference
evidence only — no host enforcement, product emission or closure admission. A fresh
independent full Claude review, a **new blind consumer**, a full application review
and the canonical six after integration and pins all remain required.
