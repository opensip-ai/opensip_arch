# bv6-corrections-author.v6 — bounded one-annotation review

**Role.** Coauthor review of a root-authored annotation correction. No source edit;
`work/` read-only. **Coauthor assent only** — not independent acceptance, not
readiness.

**Verdict: ASSENT.** BV6-V5-CR-1 is correctly and completely fixed.
`changesRequired` is empty; no finding of mine remains open.

## 1. Custody — verified, nothing guessed

6839 declared, 6839 present, 0 missing / mismatched / undeclared. The proposal's
`afterSha256` equals the supplied bytes; its `beforeSha256` equals the prior
handoff's `v5Sha256`; the other sixteen files still equal their `finalV5Sha256`;
the diff matches its `diffSha256`. All seventeen `v6Sha256` values were recomputed
from the actual files.

## 2. BV6-V5-CR-1 — CORRECTED, closed

Both defects are retired, and the second is **affirmatively reversed** rather than
merely deleted:

* "which the schema cannot decide" → "this schema **deliberately leaves** the
  authoritative relation-registry lookup to admission".
* "because `relation` is a canonical identifier rather than an enum" → "JSON Schema
  **can** branch on `const`/`enum` under a broader string type … **not a limitation
  caused by the relation type**".

The clause now matches all three already-corrected copies clause by clause —
`repair.schema.json` `EvidenceRequirement.deficiency`, workflows §6, and the
v5-corrected checker comment.

**One narrowing is correct in context.** The clause says admission decides "the
plane", where `repair.schema.json` says "the plane **and** the imported kind". Right
here: this block carries `thisBlockOwnsTheNativePlaneOnly` and delegates imported
specifics to `imported-evidence.schema.json#/x-opensip-imported-requirement-law`,
which owns `perKindApplicability`. The native registry correctly does not restate a
law it does not own.

**Surrounding law intact.** The rest of `presenceLaw` is unchanged — required when
`satisfied` is false, forbidden when true, boolean-typed `satisfied`, explicit null
refused in both branches, `CONFIG.INVALID` routing, no public detail code — and
`authorityLimit`, `vocabulary`, `carries` and every sibling key are byte-identical.

**Structurally verified:** exactly **one** leaf changed of **3757**; no key added or
removed. I re-ran the leftover scan with a **case-insensitive, concept-level**
pattern replacing the narrow CamelCase one that caused my v5 miss: clean across 203
non-review files. Absence of a match is still not proof of consistency.

## 3. Digest consequence — stated, not denied

`CoverageResultV3` is defined in this same document, and a Coverage record commits
its payload **schema document digest**. This file is therefore committed content,
not inert annotation: changing any byte — including a normative annotation string —
changes that digest and **moves the retained-Run identities of the reference
fixtures that commit it**.

I therefore **do not** claim byte identity of the schema document, and **do not**
claim any fixture, coverage, view, evidence, seal or Run identity is unchanged. They
are expected to move; root's canonical six after records and pins recomputes them.
This is the CB6-NEW-4 consequence and is expected for a registered schema document,
not a defect.

## 4. Measurement scope

No suite run; none needed for an annotation. The **1787** workflow figure remains a
**v4 measurement**, not a current result. My v5 `controlIdCount` of 170 was
literal-ID extraction, not a runtime count, and is not comparable to the v4
static call-site figure of 338 — root qualified this and I accept it.

## 5. Prior dispositions — preserved by exact reference

BV6-V4-CR-1 remains closed; all five v4 patch items remain **AGREE**. The five v3
root items, eight v2 root items (CX-BV6-01…08), seven original blind v6 findings and
my four own findings stand with their **original severities**, per
`root-input/prior-handoff.json` (`b51508e1…19c4820d`). Standing qualifications carry
unchanged, including that the neighbouring check id
`repair.the-schema-alone-cannot-decide-the-plane` is accurate of this schema as
written and is deliberately retained, not a finding.

## 6. Aggregate — 17 files, 1 changed this turn

| Path | frozen16 | final v5 | v6 | this turn |
|---|---|---|---|---|
| `check-integration.py` | `df9fbb2e…` | `4422ec24…` | `4422ec24…` | no |
| `foundation/check-identity.py` | `2724276f…` | `1982e2b6…` | `1982e2b6…` | no |
| `foundation/identity-model.py` | `66d8bd5a…` | `650d7942…` | `650d7942…` | no |
| `foundation/relation-payload-schemas.v2.json` | `ef0c244e…` | `53380a24…` | `53380a24…` | no |
| `native/native-cases.v2.json` | `5740aed5…` | `07d990e2…` | `07d990e2…` | no |
| `native/native-evidence.schemas.v2.json` | `2a5fc493…` | `19eeba46…` | `9a5f33f4…` | **yes** |
| `native/native_evidence_model.v2.py` | `8301e8e3…` | `01b517d3…` | `01b517d3…` | no |
| `workflows/check_workflows.v1.py` | `0af791d5…` | `2fe31439…` | `2fe31439…` | no |
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

## 7. Still owed

Fresh independent full Claude review, a **NEW blind consumer** review, a full
application review, and root's canonical six after integration, records and pins.
This assent is coauthor agreement on exact bytes only.
