# bv6-corrections-author.v4 — bounded final-source review

**Role.** Correction **coauthor** reviewing a root-authored patch. Not an
independent reviewer, not an accepting reviewer, and **not an implementation
pass** — I made no source edit. `work/` was treated as read-only; every file I
wrote is under `out/`.

**Verdict: CHANGES_REQUIRED.** All five proposed changes are correct and I assent
to each individually. Aggregate assent to the exact 17-file hash set is **withheld**
for one leftover defect in a file this patch already touches (§4).

---

## 1. Custody — verified, no hashes guessed

| Check | Result |
|---|---|
| Inventory | 6839 declared, 6839 present, 0 missing, 0 mismatched, 0 undeclared |
| Proposal `afterSha256` vs supplied `work/` | all 5 **match** |
| Proposal `beforeSha256` vs prior-handoff `finalV3Sha256` | all 5 **match** |
| Other 12 declared files | all still equal their `finalV3Sha256` |
| Supplied diff files vs `diffSha256` | all 5 **match** |

Every value in `changedSource.files` was recomputed from the actual files; base
values come from `root-input/prior-handoff.json` and were cross-checked against the
proposal's before-hashes.

## 2. Behavioural scope — independently verified

| Claim | My finding |
|---|---|
| Model AST unchanged after stripping docstrings | **Confirmed** for `workflows_model.v1.py`. Only a leading string-literal `Expr` is stripped, so any *other* literal change would still surface. |
| One prose-substring check removed | **Confirmed**: exactly one literal control id removed, none added (339 → 338 static call sites). |
| Count effect | **Measured, not inferred**: `check_workflows.v1.py` gives **1788** rows on final-v3 bytes and **1787** on the proposed bytes, 0 failures each — exactly −1. |
| No payload/authority/permission/retry/capability added | **Confirmed**: the two schema diffs alter only description, citation and law prose; no `$defs` member, enum, required list or field changed. |

Root's `proposal.json` phrases this precisely — *model* AST unchanged, checker
loses one check — and both halves hold. Root's note that its initial AST assertion
was overbroad because it counted a docstring is consistent with what I measured.

## 3. The five items — all AGREE

**Patch 00 — remove the prose-substring lookup control.** Agree, and it corrects a
**false claim of mine**: my v3 handoff said no v3 control proved anything by
matching prose, but I had added
`workflow.native-preparation-lookup-is-not-replay-and-import-is-delivery-only`,
which matched three substrings. What is *retained* matters: I verified the
structural control still requires a non-empty `key` **and** `lookupMeaning` for all
four step kinds, so deleting a lookup law would still be caught. Only the pretence
of proving its *meaning* is dropped — correct, since the reference executes no
receipt delivery and no native preparation.

**Patch 01 — projection `kind` and the uniform limitation.** Agree. The v3 step 3
said "`kind` together with `qualifiedName` is the SYMBOL granularity", contradicting
both the implemented projection (which reads only `logicalPath` and
`qualifiedName`) and the `granularityIsReportedNotClassified` paragraph I added in
the *same* v3 pass. I verified the new limitation **behaviourally**: two distinct
fingerprints whose subject keys agree on path and name but differ on `language`,
`kind` **and** `discriminator` both match one row. Safety holds — this is a
*disclosed coarsening*, not the ambiguity refusal (which remains
many-rows-for-one-target and still refuses), it cannot manufacture support, and the
text explicitly denies establishing execution or non-execution beyond the captured
granularity. The unsafe-repair gate remains the native `ClosedWorldV2`.

**Patch 02 — receipt-domain citation.** Agree. §10 does list two `receipt2:`
domains, so "the one receipt domain" was false; this was a leftover inside a
citation string I wrote in v3 while fixing the main statement. Naming it the
*owning mutation* receipt domain changes no key recipe, lookup meaning or authority.

**Patch 03 — model docstring and comment.** Agree. The widening comment was stale:
v3 already made a path-only *runtime* row a file-level answer too, so restricting it
to history was wrong.

**Patch 04 — prose.** Agree, all four. The `ExecutionId` rationale now matches the
schema `boundTo` I fixed in v3 and is factually right (the preimage *does* carry
`RequestId`). "Across these step kinds, four … Three use generic mutation steps"
matches `renamedRowsNote` exactly. The `HistoryPayloadV1` correction keeps the
load-bearing half — no runtime window, population or observability — which is what
the per-kind projection depends on. And I verified the precise new claim that
`granularityWidenedToFile` is disclosed "in the projection and successful outcome":
it appears on a satisfied outcome and is **absent** from a failing one, where the
deficiency names the cause instead.

## 4. CHANGES_REQUIRED — one item

**BV6-V4-CR-1** (SHOULD; parent BV6-V3-PRECISION / CX-BV6-08) —
`docs/coop/design-corrections/workflows/check_workflows.v1.py`
(`98adcb93…0fa58875`), **lines 711–716**:

```
# The two CROSS-PLANE rows are held separately and deliberately, because the SCHEMA CANNOT DECIDE
# THEM. `relation` is a CanonicalIdentifier, not an enum, so no keyword in this document can look up
# which registry that relation belongs to; ...
```

This is a **leftover copy of the rationale root itself declared false**. Two things
are wrong: it reproduces the false causal claim that a broader string type prevents
conditional constraints (JSON Schema *can* branch on a property's `const`/`enum`),
and "cannot decide" is too strong — the schema *could* enumerate the two imported
relation names as consts; what it cannot do is dereference a registry, and the
design **deliberately** leaves that lookup to admission.

It now contradicts, **within this same patch**, the corrected
`EvidenceRequirement.deficiency` description ("THIS SCHEMA DELIBERATELY LEAVES THE
AUTHORITATIVE REGISTRY LOOKUP TO ADMISSION … not a limitation of JSON Schema") and
§6. Leftover copies in a second document are the defect class that has recurred
through v1–v3.

**Remedy:** restate the comment as the deliberate choice, mirroring the corrected
schema wording. **No control change is needed** — the two cross-plane controls are
correct and should stay.

## 5. Qualifications on my own prior handoffs

* v3's "no control proves a claim by matching prose" — **false**; withdrawn.
* v3's assent covering "every final-note point" — **overstated**. My last actual
  Read was 23:26 UTC; the 23:30 and 23:40 additions, which are the origin of these
  five items, were not covered and are dispositioned here for the first time.
* v3's comparative baselines `check-identity v2 = 1344` and
  `check-integration v2 = 378` are **wrong**. Verified against the retained final-v2
  reports: **1345** and **388**. 1344 was an intermediate failing v3 run; 378 was in
  fact the *v1* value. My v2 handoff had recorded both correctly. Historical
  comparatives are not current result evidence in any case.
* v3's FULL RETAINED-RUN scope was already corrected in v3 and is restated: only the
  partition controls reach `close_run`.

## 6. Root qualifications — accepted

Root's final eight projection/outcome rows omit `observationWindow` and
`observedPopulation` in the outcome contexts, so they demonstrate selected helper
**matching only**, not admitted bounded observations. Accepted. My verification
probe supplies bounds where an outcome is computed, so its satisfied rows *are*
bounded-observation rows — but they remain **synthetic helper fixtures**. All
fixtures on both sides are helper fixtures, not closed-Run imports; the fingerprints
are **synthetically formatted labels, not rehashed closure identities**, and no
placeholder fingerprint is evidence of real closure admission. Structural
presence/citation/key checks are presence only. `run-suites` is not the canonical
six.

## 7. Aggregate — 17 files, 5 changed this turn

| Path | frozen16 | final v3 | v4 | this turn |
|---|---|---|---|---|
| `check-integration.py` | `df9fbb2e…` | `4422ec24…` | `4422ec24…` | no |
| `foundation/check-identity.py` | `2724276f…` | `1982e2b6…` | `1982e2b6…` | no |
| `foundation/identity-model.py` | `66d8bd5a…` | `650d7942…` | `650d7942…` | no |
| `foundation/relation-payload-schemas.v2.json` | `ef0c244e…` | `53380a24…` | `53380a24…` | no |
| `native/native-cases.v2.json` | `5740aed5…` | `07d990e2…` | `07d990e2…` | no |
| `native/native-evidence.schemas.v2.json` | `2a5fc493…` | `19eeba46…` | `19eeba46…` | no |
| `native/native_evidence_model.v2.py` | `8301e8e3…` | `01b517d3…` | `01b517d3…` | no |
| `workflows/check_workflows.v1.py` | `0af791d5…` | `29abcb85…` | `98adcb93…` | **yes** |
| `workflows/schemas/common.schema.json` | `3f84dff2…` | `16ff6419…` | `16ff6419…` | no |
| `workflows/schemas/imported-evidence.schema.json` | `8acfd72f…` | `e6c997aa…` | `edce21a3…` | **yes** |
| `workflows/schemas/invocation-record.schema.json` | `3b89b739…` | `6c5ed3f3…` | `6c5ed3f3…` | no |
| `workflows/schemas/repair.schema.json` | `b8fe3464…` | `c577eda9…` | `65d5f639…` | **yes** |
| `workflows/workflow-cases.v1.json` | `688506e6…` | `22b74430…` | `22b74430…` | no |
| `workflows/workflows_model.v1.py` | `8d45d115…` | `6fa97479…` | `a268aa4b…` | **yes** |
| `identity-and-evidence.md` | `64a2a019…` | `3d7ca24e…` | `3d7ca24e…` | no |
| `native-evidence.md` | `b50c814c…` | `fafc4abc…` | `fafc4abc…` | no |
| `workflows-and-surfaces.md` | `4a5f0c4e…` | `f7735807…` | `a6e34134…` | **yes** |

Untruncated values and per-file edit lists are in
`out/handoff.json#/changedSource/files`.

## 8. Prior dispositions preserved by reference

The five v3 root items, the eight v2 root items (CX-BV6-01…08), the seven original
blind v6 findings (CB6-MUST-1/2, CB6-SHOULD-1/2, CB6-ADV-1/2/3) and my four own
findings (CB6-NEW-1/2/4 retained, CB6-NEW-3 withdrawn) all stand with their
**original severities**. This review is bounded to the supplied patch and its owning
contexts and re-opens none of them.

## 9. Limitations

Bounded review of a supplied patch, not a full source review. Design reference
evidence over synthetic inputs — no host enforcement, product emission or closure
admission. A fresh independent full review, a **new blind consumer**, an application
review and the canonical six after integration and pins all remain owed.
