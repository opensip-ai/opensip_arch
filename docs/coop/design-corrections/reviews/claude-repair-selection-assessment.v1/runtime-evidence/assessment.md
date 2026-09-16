# Bounded contract assessment — repair's `ClosedWorldV2` selection law

**Verdict: GAP.** For an admitted Run holding more than one retained `ClosedWorldV2`,
no published law names which retained entry, or which deterministic aggregate, the
delete/replace prerequisite reads. I found no existing authoritative selector anywhere
in the frozen source.

This is an independent technical assessment. It is **not** root agreement, **not**
source acceptance, and **not** a readiness, application or qualification claim. I am a
technical peer here, not a design acceptor.

---

## 1. Scope and non-scope

**In scope.** The closed-world prerequisite for `delete`/`replace` in
workflows-and-surfaces §6; the record that prerequisite reads; whether a Run-level
selector or aggregation exists anywhere in the frozen source; and, if not, the
smallest coherent design correction.

**Out of scope, deliberately.** No product implementation, no source modification, no
git operation. No exhaustive whole-product review. I did not audit apply/recover/verify
beyond the gate, the imported evidence plane, or any surface unrelated to this question.
Everything I wrote lives under my own runtime directory.

**Inputs.** Frozen source `/tmp/opensip-design-corrections/candidate-subject.v31` only,
plus the author reference package `claude-author-package-successor.v7` treated strictly
as author synthetic evidence. **No consumer output was read, sought or used.** My own
probes are likewise author-side synthetic evidence, never compiler, provider or consumer
qualification.

---

## 2. Verified manifest

Manifest `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json`
recomputed SHA-256 =
`ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5` — **matches** the
expected value. `snapshotRoot` = `/tmp/opensip-design-corrections/candidate-subject.v31`,
`fileCount` 12895, `totalBytes` 736 536 507, `implementationAuthorized: false`,
`reviewPending: true`.

I then recomputed the SHA-256 of **29 subject files** I rely on and compared each to its
manifest row. **All 29 match** (`probes/verified-subject-files.json`). They include the
six live `docs/v2/contracts/product-v1/*.md` contracts, both `repair.schema.json`
documents, `common.schema.json` (both families), `workflows_model.v1.py`,
`native_evidence_model.v2.py`, `native-evidence.schemas.v2.json`, `atom_model.v1.py`,
`identity-schemas.v3.json`, `identity-model.v3.py`, `workflow_projection_model.v3.py`,
the evaluator3 replay fixtures and `integration-fixtures.py`.

Every claim below cites one of those verified files.

---

## 3. What the owners actually say

### 3.1 The record is per Coverage entry, and only per Coverage entry

`native-evidence.md:1836-1850` defines `ViewEntryV3` **per
`(relation, rung, sourceUniverse, targetUniverse)`**, with `"closedWorld": ClosedWorldV2
(§4.5)` as a member at `:1847`. `:1852` gives
`CoverageResultV3 = {schemaVersion:3, key: CoverageKeyV2, entry}`. §4.5 at `:2030-2033`
closes `ClosedWorldV2` at seven members.

The schema agrees exactly, and I checked it mechanically rather than by reading
(`probes/probe-two-closed-worlds.json`, step `owner-shape`):

* `$defs/ClosedWorldV2.required` — 7 members.
* `$defs/ViewEntryV3.required` — includes `closedWorld`.
* `$defs/CoverageKeyV2.required` — 5 coordinates: `relation`, `resolution`,
  `sourceUniverse`, `targetUniverse`, `subjectScopeCommitment`.
* **The only record in the entire native schema bundle that defines a `closedWorld`
  property is `ViewEntryV3`.**

There is no Run-level, evidence-level or view-level `ClosedWorldV2`. The identifier
table at `identity-and-evidence.md:188-194` lists no such member on `view2`, `evidence3`,
`seal3` or `run3`, and my probe confirmed it on a real closed Run: `run3` carries
`{capabilityManifestId, evaluationSealId, evidenceId, planId, projectId, schemaVersion,
snapshotId}` and `evidence3` carries `{coverageIds, findingIds, importIds, planId,
proofBundleId, schemaVersion, viewIds}`. **No retained record in the closure carried a
`closedWorld` field at all** — the only carriers were the per-entry Coverage payload blobs.

### 3.2 Several differing records in one Run are explicitly lawful

`identity-and-evidence.md:1320-1332` makes Coverage-scope disjointness a property of the
**full owning tuple** `(snapshotId, relation, resolution, sourceUniverse, targetUniverse)`
and then says in as many words: "A **differing tuple is a different claim, not an
overlap**, which is why the same subject may lawfully appear under two relations, two
rungs or two universes." `:1334-1341` adds that the rule is **per view**, and that two
views of one Run may reference the same scope. `native-evidence.md:355-374` states the
fact/scope `matchOn` join over the four `CoverageKeyV2` coordinates plus `snapshotId`,
and explicitly contemplates "a view carrying more than one universe."

So a single admitted Run holding N distinct `ClosedWorldV2` records is not an edge case
the contract tolerates; it is a shape the contract describes.

### 3.3 Repair's owner text presupposes exactly one

* `workflows-and-surfaces.md:602-611`: the prerequisite "is decided against the evidence
  Run's own native `ClosedWorldV2` (native §4.5) — the record that contract closes at
  seven members".
* `workflows-and-surfaces.md:710-724`: the descriptor is "the **five-field projection**
  of the evidence record", and the authority "stays the sealed Run named by
  `evidenceRunId`: the prerequisite above is decided against **that** Run's own full
  record".
* `workflows-and-surfaces.md:497`: "that gate stays the evidence Run's own
  `ClosedWorldV2` (§6)".
* `repair.schema.json:562` (evaluator3): the five fields are "each taken unchanged from
  that same Run's `ClosedWorldV2`".
* `workflows_model.v1.py:1584`: "run carries the evidence Run's own native
  `ClosedWorldV2` … SEVEN members".

Each of these denotes a singular Run-level record. With N ≥ 2 retained records, **"that
Run's own `ClosedWorldV2`" does not denote.** The `H-5` hand-off at
`native-evidence.md:3590` says only that repair "consume[s] `ClosedWorldV2.deadCodeRepairEligible`
and `affected_targets` as stated in §4.5" — it delegates the consumption, not the selection.

### 3.4 The synthetic adapter is not a derivation

`workflows_model.v1.py:1610` reads `cw = run['closedWorld']` — a singular field on a
caller-supplied dict. `:1621-1626` is the gate; `:1651` is the 7→5 projection. The helper
never sees a Coverage entry, a `CoverageKeyV2`, a universe or a view. Its docstring is
candid that it "consumes that record, it does not re-admit it". This is a **pre-selected
input**, so it cannot be — and does not claim to be — the published derivation from a
full Run. The frozen repair cases in `workflow-cases.v1.json:7610-7630` supply that field
directly, for the same reason.

---

## 4. Is there an existing authoritative selector? No.

I censused every `closedWorld` / `ClosedWorldV2` occurrence in the non-review source: 87
sites across 19 files in `docs/coop/design-corrections`, 11 in the live contracts
(`probes/probe-existing-selector.json`). A regex sweep for aggregation/selection language
near "closed world" (`aggregat*`, `select*`, `reconcil*`, `merge`, "run-level", "which
entry", "per-universe", "per-entry") over the whole non-review tree returned **zero hits**.

Three reads exist. None is a Run-level repair selector.

**(a) `sufficiency_v2` — per entry, and correct.** `native_evidence_model.v2.py:1722`
reads `entry.get("closedWorld")`: the closed world of *the entry the requirement ranges
over*. §4.6 step 7 uses it only for a universal negative about an exported target. This is
unambiguous because the entry is fixed by the requirement. It resolves nothing for a
Run-level gate.

**(b) `atom_model.v1._conservative_entry` — the only aggregation in the source.** At
`atom_model.v1.py:1032` ("AND-compose several same-relation partitions"), with the
closed-world rule at `:1050-1052`: rank `{closed:0, open:1, unknown:2}` on `exportsClosed`
and copy *that entry's whole record*. It is not repair's selector, for four reasons:

1. It composes **same-relation** partitions for one atom query at a fixed
   `(relation, rung, sourceUniverse, endpoint)`. It produces a per-relation entry, never
   a Run-level record.
2. Its owning contract scopes it away from this use. `atom-evaluation-contract.v1.md:84-86`:
   closed world is "copied exact"; `target_exported`/`target_affected` "apply **only** to
   incoming (`endpoint=target`)"; and "Outgoing predicates do not inherit unrelated
   incoming closed-world."
3. No repair owner names it — not §6, not either `repair.schema.json`, not
   `workflows_model.v1`.
4. **It does not minimise the flag repair's gate reads.** I ran it on two schema-valid
   entries — `{exportsClosed: closed, deadCodeRepairEligible: false}` and
   `{exportsClosed: open, deadCodeRepairEligible: true}` — and it returned
   `deadCodeRepairEligible: true`, stably in both input orders. Ranking `exportsClosed`
   carries the *rest* of the winning record along; `deadCodeRepairEligible` is a separate
   schema member with no cross-field constraint. As a repair selector it would be unsafe.

**(c) The plan's targets do not disambiguate it either.** §6:646 says plan `targets`
"supply the per-target scope through the published fingerprint projection". They do not
supply a universe. `identity-schemas.v3.json#/$defs/finding-fingerprint` requires
`{schemaVersion, ruleStableId, detectorSemanticsMajor, subjectKey, relatedSubjectKeys}`
and carries **no universe**; `finding.subject` (display attribution) carries
`{language, kind, logicalPath, qualifiedName}` and **no universe**. Worse, the repair
target law positively *admits* the cross-universe case:
`repair.schema.json#/x-opensip-evaluator3-repair-target-law.multiConfigSameFingerprint`
compares "ruleId, subjectPath, kind, qualifiedName, detector closure", and
`workflow_projection_model.v3.py:1258-1266` (`_meta`) compares exactly those five.
**Universe is not compared**, so two occurrences in two universes group into one target
without reaching `REPAIR.TARGET_METADATA_AMBIGUOUS`.

That is not hypothetical. In the frozen fixture's own multi-universe Run
(`run3:fbc6cee4…`, the same Run the author's `mixed-universe-view.probe.json` records),
**every finding-key2 fingerprint appears twice, once per universe**, with two different
`subject3` ids.

---

## 5. Reproduction

Three probes, run under `/tmp/opensip-architecture-review-env/bin/python -I -B`
(3.12.13, jsonschema 4.25.1) via a `python3` subprocess launcher, using the frozen
source's own fixtures, producer boundary and closure.

### 5.1 A full admitted Run with two distinct `ClosedWorldV2`

`probes/probe_two_closed_worlds.py` → `probe-two-closed-worlds.json`.

I minted both records with the **owner's own producer**, `native_evidence_model.closed_world_v2`,
not by hand:

| | `exportsClosed` | `entryPointsRecognized` | `deadCodeRepairEligible` | `reasons` |
|---|---|---|---|---|
| A | `closed` | `all` | **true** | `[]` |
| B | `unknown` | `partial` | **false** | `entry-points:partial`, `external-consumers:unknown` |

The only change to `evaluator_graph_fixture.v3.build_file_inputs(multiple_universes=True)`
was which of the two each universe's entries carry. Every entry still passed
`admit_coverage_result_v3` (the real producer boundary), and the Run passed
**`close_run`**, which runs the complete evaluator3 semantic replay — not a schema check.

```
runId run3:56ea69ae352ae95d45dd797a5b43002175602988f1453ba3139d6c798b56d802   ADMIT
4 retained Coverage entries, 2 distinct ClosedWorldV2, deadCodeRepairEligible ∈ {false,true}
  file@enumerated          / universe 17ce4077e698 → eligible true
  package@manifest-declared/ universe 17ce4077e698 → eligible true
  file@enumerated          / universe 03bbcc3284a7 → eligible false
  package@manifest-declared/ universe 03bbcc3284a7 → eligible false
retained records carrying a Run-level closedWorld: []
```

This is **full Run acceptance, not a schema-valid fragment.**

### 5.2 The same disagreement inside one universe

`probes/probe_repair_selection.py`, part A. Varying by **relation** in a **single**
universe:

```
runId run3:fe71c0c1c29c5ed9f81a7f91a46d0d7a79c44db030df6203fe3e1ad417b5753d   ADMIT
  file@enumerated           / universe 17ce4077e698 → eligible true
  package@manifest-declared / universe 17ce4077e698 → eligible false
```

So the ambiguity is not a multi-universe artefact. **Nothing in Run closure requires two
entries of one Run to agree**, and nothing I could find asks.

### 5.3 The material consequence

`probes/probe_repair_selection.py`, parts B–C, driving the frozen
`workflows_model.v1.repair_preview` with each of the two records that §5.1 proved are
**both retained in the same admitted Run**, holding `evidenceRunId`, `targets`, `edits`,
requirements, recipe and trust fixed (identifier spellings taken from the frozen
`workflow-cases.v1.json` constants):

| | `applicable` | `repairPlanId` | unmet |
|---|---|---|---|
| reading A | **true** | `repairplan2:d4f0965761c1…` | — |
| reading B | **false** | `repairplan2:fbe58b21e87a…` | `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` |

`sameEvidenceRunId: true`, `sameTargets: true`, `sameEdits: true`,
`repairPlanIdsDiffer: true`, `applicabilityFlips: true`.

Both descriptors **validate** against
`workflows/schemas/repair.schema.json#/$defs/RepairPlanDescriptor`, and the literal
seven-member copy is correctly refused (`'dynamicDispatch', 'reasons' were unexpected`).
The schema does its stated job — close the projection at five, refuse a literal copy —
and says nothing about **which** retained entry was projected. It is not the disambiguator
and does not claim to be.

**Why this matters.** `repairPlanId = H('workflow.repair-plan', descriptor)` is the
preimage of the apply-time security authorization (§6:717-718, `REPAIR.CONSENT_NOT_BOUND`).
So two conforming implementations reading the same sealed Run mint **two different
authorization subjects** for the same request, and **one authorizes a destructive
delete/replace the other refuses**. This is a determinacy defect of exactly the class the
native contract already names for itself at `native-evidence.md:1880-1888` — "a
determinacy gap in the contract, **not** a digest collision and not a divergence over
byte-identical observations."

### 5.4 Negative checks against today's behaviour

`probes/probe_repair_selection.py`, parts D–E.

* `UNSAFE_ACTIONS == {delete, replace}`; a **create-only** plan is `applicable: true`
  even under the ineligible record, and a create+delete plan is not. The all-delete/replace
  guard fires on any such edit and is not narrowed. Create-only never reads `closedWorld`,
  so the selection question does not arise for it.
* Evidence Run with **no** `closedWorld`: **untyped `KeyError`**, not a typed repair
  refusal.
* The **five-member descriptor projection fed back** where the seven-member evidence
  record is required: **silently accepted**, `applicable: true`. Since that is precisely
  the shape the descriptor emits, the round-trip is reachable.

### 5.5 Feasibility check for the correction

`probes/probe_target_universe_recoverable.py` → `probe-target-universe.json`.

A per-target universe is derivable from records the closure **guarantees**: `finding3`
requires `subjectId`, `evaluation-subject` (`subject3`) requires `universe`, and when I
dropped the six retained `evaluation-subject` records from an otherwise identical Run,
`close_run` **REFUSED** with `EvidenceUnavailable: EVIDENCE_UNAVAILABLE:subject3:65b6ae…`.
So `target fingerprint → finding3 → subject3.universe` is available today, with **no new
identity version**.

---

## 6. Genuine source gap, versus invalid example, versus helper omission

**Genuine source gap** — workflows-and-surfaces §6 (`:602-611`, `:710-724`) and the
`closedWorld` description in both `repair.schema.json` documents assert a singular
Run-level `ClosedWorldV2` that the owning native contract does not define, that no
retained record carries, and that an admitted Run demonstrably contradicts. The gap is a
**missing selection law in the workflow owner**, not a defect in native §4.5: native's
per-entry record is coherent, and `sufficiency_v2` consumes it correctly.

**Helper omission — not the defect, but why it stayed invisible.** `integration-fixtures.py:255-257`
and `check-identity.py:301-303` hard-code one identical `ClosedWorldV2` for **every**
entry, so no reference fixture has ever exhibited two. `workflows_model.v1.repair_preview`
takes a pre-selected singular field. Fixing either would expose the gap; neither *is* it.

**Invalid example — none found.** The `workflow-cases.v1.json` repair scenarios are
lawful adapter inputs for an adapter that takes a pre-selected record.

**One adjacent model limitation, flagged and kept separate.** `native_evidence_model.v2.py:1697`
keys `sufficiency_v2`'s view by `view.get(rel)` — relation alone, not the full
`CoverageKeyV2` tuple. That is a reference-model simplification, not the contract, and it
is **not** this gap; but it would need attention if a selection law is stated over the
full tuple.

---

## 7. Smallest coherent design correction (proposed, not authored)

Design only. I am not writing it, and this is a proposal for the owners to weigh, not an
accepted design.

**Principle.** Make the closed-world prerequisite **target-relative and per-universe**,
the same shape native §4.5 already gives dynamic edges — rather than inventing a
Run-level record the evidence graph does not have. `dynamicDispatch` stays out of it, and
nothing here introduces a global veto.

**7.1 Deterministic target/evidence selection.** For each target *t*, let `U(t)` be the
universes of its matched occurrences via `finding3.subjectId → subject3.universe` (§5.5:
guaranteed retained). Let `E(t)` be the retained Coverage entries of the evidence Run
whose `key.sourceUniverse ∈ U(t)`, restricted to the relations the plan's
`evidenceRequirements` name, at that relation's registered resolved `(relation, rung)`
pair. Select by the **full `CoverageKeyV2` tuple**, never by relation alone — the same
`matchOn` the native contract already publishes. The gate is true iff
`deadCodeRepairEligible` is true for **every** entry in `E(t)` for **every** target
carrying a delete/replace edit. **Conjunction, not a ranked pick**: the prerequisite is a
universal negative, so one dissenting entry defeats it. Deliberately stronger than
`_conservative_entry`, which §4(b) showed does not minimise this flag. Order dissenting
entries by the published partition key so remedies are byte-deterministic.

**7.2 Zero / multiple / mixed-universe.**

* **Zero** selected entries → not applicable, `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED`,
  remedy naming the missing `(relation, rung, universe)`. **No new public detail code**;
  the closed registry is untouched. Vacuous truth is explicitly refused, matching RC-1's
  "`not-applicable` is never a fallback" and the import law's "zero owed wrappers is never
  vacuous true".
* **Multiple, agreeing** → unchanged behaviour, and — importantly — a **bit-identical
  `repairPlanId`** to today for the single-entry case.
* **Multiple, disagreeing** → not applicable, remedy carrying **every** dissenter's own
  `reasons`, deduplicated, sorted, prefixed by universe/relation, so two causes stay two
  remedies (§6's existing rule).
* **Mixed universe on one target.** Recommend **(a) conjoin over all occurrences**:
  cheapest, strictly conservative, leaves the existing target law and
  `REPAIR.TARGET_METADATA_AMBIGUOUS` meaning exactly what they mean today. I considered
  **(b) adding `universe` to the multi-config compatibility metadata** and reject it as
  *the smallest* correction: it repurposes an existing public detail and would refuse
  plans lawful today, including plans with no unsafe edit at all.

**7.3 Descriptor projection.** `RepairPlanDescriptor.closedWorld` stays **exactly five
members**, stays a projection, and keeps **no authority of its own**. Define the projected
record as the *selected conjunctive* record: `deadCodeRepairEligible` = the conjunction;
the four display members = the common value when all selected entries agree, else the
values of the defeating entry lowest in partition-key order. State explicitly that the
four display members are **not** minimised field-by-field, because that would synthesise a
record no producer ever minted — the same objection the contract set raises elsewhere
against collapsing distinct outcomes. **No descriptor member changes**, so the
`repairPlanId` preimage shape, `schemaMajor` 1 (`workflows:repair`) / 2 (evaluator3), and
the apply-time authorization binding to the exact `repairPlanId`, base snapshot and
project are all preserved unchanged.

*Optional disclosure, if the owners want the decision auditable from the plan alone:*
carry the selected `coverage2` ids as an **optional sibling of `descriptor` inside
`RepairPlanV1`** — today `{repairPlanId, descriptor}`, `additionalProperties: false`. A
sibling sits **outside** the `H` preimage, so it discloses without moving any identity.

**7.4 Create-only.** Unchanged and stated: `UNSAFE_ACTIONS = {delete, replace}`; a plan
with no such edit never reads `closedWorld` and never selects an entry (§5.4). Create-only
plans acquire no new failure mode and no new evidence demand.

**7.5 Negative checks, all against existing codes.** Zero selected entries → typed
`REPAIR.CLOSED_WORLD_NOT_ESTABLISHED`, not a `KeyError`. A five-member projection supplied
where the seven-member record is required → refuse at admission. Two disagreeing entries →
not applicable, both reasons carried. Two agreeing entries → `repairPlanId` equal to the
single-entry Run's. **A dissenting entry in a universe no target reaches → does not defeat
the plan** (keeps the gate target-relative, mirroring the existing refusal to read
`dynamicDispatch` as a global veto). A dissenting entry for a relation no requirement names
→ **decide it explicitly**; I recommend "does not defeat", for the same target-relative
reason, recorded as a choice the law makes rather than left to the reader.

**7.6 Preserved.** Security authorization binding; `run3`/`subject3`/`coverage2`/`scope2`/
`repairplan2` and both descriptor majors; the all-delete/replace guard without
qualification; the closed public detail registry; `dynamicDispatch` target-relative and
never a global veto.

**7.7 Tradeoffs.**

* *Conjunction vs. ranked pick.* Conjunction can make a plan that some implementation
  today finds applicable inapplicable on a multi-universe Run. That is the intended
  direction for a universal negative, but it **is** a behaviour change for any
  implementation currently picking arbitrarily — and no change at all for single-entry Runs.
* *Target-relative selection costs a join.* It needs `target → subject3 → universe` at
  preview. Derivable from guaranteed records, but it adds a resolution step to a
  Query-class operation and one more way for preview to fail (unresolvable `subject3` →
  existing `REPAIR.EVIDENCE_RUN_UNAVAILABLE`).
* *Law-only vs. disclosure sibling.* Law-only moves no schema byte and no identity; the
  sibling makes the gate auditable from the plan alone but is a schema edit and a new
  parity surface. I would take law-only first and treat the sibling as a separate question.
* *Narrow vs. wide relation scope.* Scoping to the requirement's relations keeps the gate
  target-relative; scoping to all relations is simpler to state but re-creates a global
  veto through the back door.

---

## 8. Limits of this assessment, and remaining issues

1. **My probes are author-side synthetic evidence.** They exercise the frozen reference
   fixtures, producer boundary and closure. They are not compiler, provider or repository
   qualification. No consumer output was read or sought.
2. **Bounded.** I did not audit apply, recover or verify beyond the gate; nor the imported
   evidence plane; nor any surface unrelated to this question.
3. **Universes exercised** were the fixture's two syntax universes. Rust and TypeScript
   universe interactions were not exercised.
4. I did **not** establish whether any implementation outside the frozen source already
   applies a selector. The claim is about the source.
5. `native_evidence_model.v2.py:1697` keys `sufficiency_v2` by relation alone — a model
   simplification I flag as adjacent, not as this gap.
6. `ClosedWorldV2` has **no cross-field consistency constraint** in schema (e.g.
   `exportsClosed` vs `deadCodeRepairEligible`). I used that in §4(b) to show the existing
   fold is unsafe as a repair selector. Whether the owner wants such a constraint is a
   separate question I did not pursue.
7. **The three candidate readings of §6 — some entry, a Run-wide aggregate, or a
   per-target entry — remain open.** §7 is my recommendation, not a decision, and choosing
   among them is the owners' call.
8. I make **no claim of root agreement and no claim of source acceptance.** Nothing here
   authorizes implementation or application.

---

## Artifacts

| file | what |
|---|---|
| `probes/verify_subject.py`, `probes/verify_more.py` | manifest + 29-file SHA verification |
| `probes/verified-subject-files.json` | the verified rows |
| `probes/probe_two_closed_worlds.py` / `.json` | full admitted Run, two distinct `ClosedWorldV2` |
| `probes/probe_repair_selection.py` / `probe-repair-selection.json` | one-universe case, consequence, schema, create-only, negatives |
| `probes/probe_existing_selector.py` / `probe-existing-selector.json` | selector census and the `_conservative_entry` behavioural test |
| `probes/probe_target_universe_recoverable.py` / `probe-target-universe.json` | target→universe derivability |
| `probes/run.py` | reference-interpreter launcher |
