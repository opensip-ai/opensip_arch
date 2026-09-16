# Corrections to my repair-selection assessment v1

**Standing.** My original report and probes in
`/tmp/opensip-design-corrections/claude-repair-selection-assessment.v1/` are preserved
unchanged; nothing there was edited. This file records where I overclaimed and what the
claim should have been. I am now a **source coauthor**, not an independent acceptor, and
this origin supplies **no** final design, blind or application acceptance. No consumer
output was read or sought.

**What survives.** The GAP itself, and the full-Run counterexample, survive root's review.
Root reproduced `run3:56ea69ae…` with four Coverage entries and eligible values
`false`/`true`, and verified all 12895 source files unchanged afterwards. The published
workflow presupposed one Run-level `ClosedWorldV2` while retained native evidence carries one
per Coverage entry. That much I stand behind.

**What does not survive** is a set of claims I made around it. Eight corrections follow, in
root's numbering.

---

## 1. Create-only: "never selects/reads `closedWorld`" was wrong

**I wrote** that a create-only plan "does not read `closedWorld` at all, so the selection
question does not arise for it".

**Correct statement.** Only the *unsafe eligibility veto* is skipped. `repair_preview` still
reads a closed-world value and still builds the five-field descriptor member on every path,
including create-only — the member is `required` in both `RepairPlanDescriptor` schemas, and
the whole descriptor is the `repairPlanId` preimage. So the selection question very much
arises for create-only: it decides a descriptor value and therefore a plan identity. My
phrasing left the identity question unsolved while sounding as though it had dissolved it.

**What I did about it.** The correction I authored defines the create-only case explicitly:
the same reduction runs, and with no selected record it yields a fixed summary, so the
descriptor and `repairPlanId` are deterministic even with zero native Coverage. Two full-Run
controls cover it (`repair-cw-create-only-is-not-failed-by-ineligibility-alone`,
`repair-cw-create-only-still-builds-a-deterministic-summary`).

## 2. Probe B's scope was overstated

**I wrote** that probe B showed "the same admitted Run, same targets, same edits" producing
opposite applicability, and presented it as the material consequence.

**Correct statement.** Probe B did **not** run on the admitted Run from probe A. It used the
`workflow-cases.v1.json` constants and `fixture_tree_snapshot_id`, a synthetic tree-snapshot
adapter, and fed `repair_preview` a pre-selected `closedWorld` field. What it demonstrated is
**adapter sensitivity at fixed synthetic inputs** — that the helper's output depends on which
record it is handed. It did not establish a full admitted repair from a real Run, and the two
`ClosedWorldV2` values it used were *shown by probe A to be co-retainable*, which is a
different and weaker thing than deriving both from one Run inside the preview. Its schema
check was against **legacy `workflows:repair` major 1**, not the selected evaluator3 major 2;
I should have said which.

I also allowed "applicable" to carry more weight than it has. **Preview `applicable=true` is
not authorization.** Preview is a Query-class step; trust, consent, current-snapshot equality
and an authorization bound to the exact `repairPlanId` are separate and still required.

**What I did about it.** The new controls do not repeat this. The positive and the conflicting
negative both build a graph, admit it at the native producer boundary, close it with
`identity-model.v3.close_run` (full evaluator3 semantic replay), and drive the **evaluator3**
`repair_preview` from that closure. Both repair schemas are checked, major 1 and major 2, each
named.

## 3. Probe E was not a demonstrated product defect

**I wrote** that a five-member projection fed back where the seven-member record is required
was "silently accepted" and that "the round-trip is reachable", and that a missing
`closedWorld` produced an "untyped `KeyError`" — presenting both as findings.

**Correct statement.** The helper's docstring states its input assumption explicitly: an
already-admitted seven-member record. Probe E violated that documented assumption. Feeding a
helper something its contract says it will not be given, and observing that it misbehaves,
is **not** a product admission bypass and is **not** evidence that the round-trip is reachable
through the owning admission. The actual admission sites are `admit_coverage_result_v3` and
retained Run closure, and probe E never went near them. I withdraw both as defect claims.

I also do **not** propose that the historic adapter become a full native validator. That would
push validation to the wrong boundary.

**What I did about it.** The new evaluator3 owner takes the **retained closure** and refuses a
caller-selected record outright (`repair-cw-evaluator3-refuses-a-caller-selected-record`),
which removes the shape rather than validating it late. The historical major-1 profile keeps
its documented input assumption, now stated in the docstring together with the explicit note
that violating it is not a product admission bypass.

## 4. The `_conservative_entry` test used a non-conforming input

**I wrote** that the existing fold "does not minimise the flag repair's gate reads" and would
be "unsafe as a repair selector", based on inputs including
`{exportsClosed: open, deadCodeRepairEligible: true}`.

**Correct statement.** That combination contradicts native §4.5's **"true only with
`exportsClosed=closed`, `entryPointsRecognized=all` and no nonliteral loading"**. Schema
validity is not normative admission, and the native owner's own producer would never mint it.
A conclusion drawn from an input the owner forbids proves nothing about the fold's behaviour
over conforming evidence, and I withdraw the "unsafe fold" claim.

The sufficient and correct point is the plain one: **`atom_model._conservative_entry` is not a
published repair selector.** It composes same-relation partitions for one atom query, its own
contract scopes it to that use, and no repair owner names it. That alone answers "is there an
existing authoritative selector".

I also withdraw the suggestion of an adjacent atom-model correction. **No atom-model change is
inferred or proposed**, and I edited nothing there.

**What I did about it.** Every `ClosedWorldV2` value in the new controls is minted by the
native owner's own `closed_world_v2`, including the dynamic-dispatch one, and a control
(`repair-cw-every-record-used-here-obeys-native-4-5-true-only`) asserts the §4.5 implication
holds for all of them, so no conclusion rests on a forbidden combination.

## 5. "No reference fixture has ever exhibited two" was broader than measured

**I wrote** that "every reference fixture hard-codes one identical `ClosedWorldV2` for every
entry, so no reference fixture has ever exhibited two."

**Correct statement.** I measured **two** files — `integration-fixtures.py:255-257` and
`check-identity.py:301-303` — found via a text census. That supports "the two fixtures I
measured hard-code one identical record", and nothing wider. I did not enumerate every
fixture in the source, and "has ever" is a claim about history I never tested. Withdrawn and
narrowed to the measured scope.

## 6. The equal-`repairPlanId` claim was wrong

**I wrote** that under the proposed correction, "multiple entries, all agreeing" would give a
"bit-identical `repairPlanId` to today for the single-entry case".

**Correct statement.** `evidenceRunId` is part of the descriptor, and the descriptor is the
whole `H` preimage. **A different Run is a different plan identity**, however similar its
evidence — adding an equal Coverage record produces a different Run and therefore a different
id. No such equality is promised and I should not have implied one. The two things to keep
apart:

* the identity **recipe and descriptor shape** are unchanged — same five member names, same
  `additionalProperties: false`, same majors, same `H('workflow.repair-plan', descriptor)`;
* the descriptor **values**, and the **Run identity**, are exactly what move.

Equality holds only where *every* descriptor input, that Run included, is identical.

I add a second correction root raised in the same point and I accept: **source annotations
change actual schema bytes even when field shapes and majors do not.** My two schema edits
change 52576 → 54967 and 54099 → 56494 bytes. Saying "no schema byte moves" would have been
false; the accurate claim is that no field shape, member set or major moves.

**What I did about it.** Three controls hold this line:
`repair-cw-identity-recipe-unchanged-values-may-move`,
`repair-cw-no-equal-id-claim-across-different-runs`, and
`repair-cw-same-inputs-same-run-mint-the-same-id` — the last being the *only* equality
asserted anywhere.

## 7. The proposal was underspecified, and the disclosure sibling is withdrawn

**Correct statement.** My §7 did not define the target-to-edit mapping, the zero-entry display
record, the mixed case where eligibility agrees but display values differ, or tie-breaking
across all coordinates. Worse, one thing I left implicit was an assumption I should not have
made: **an edit does not name a target.** `targets` and `edits` are separate descriptor arrays
with no published correspondence, and inventing a pointer between them would have been a
fabricated join.

I also **withdraw the optional unsigned disclosure sibling** on `RepairPlanV1`. It adds a
surface that carries evidence weight without being in any signed or identity-bearing preimage,
which is the wrong shape for this, and it is not needed: the remedies already name the
dissenting relation, rung, universe and reasons.

**What I did about it.** The authored law defines all four gaps: relevance is the **union** of
target-derived and unsafe-path-derived universes with no pointer between the arrays; the
zero-entry display record is a fixed published value; the reduction is fieldwise so agreeing
eligibility with differing display values is defined; and ordering is the full partition key
`(relation, resolution, sourceUniverse, targetUniverse, subjectScopeCommitment)` then the
retained `coverage2` identity as final tie-break.

## 8. Scoping gate evidence to the recipe's requirements was a real hole

**I wrote** that the selected entries should be "restricted to the relations the plan's
`evidenceRequirements` name".

**Correct statement.** That is exploitable, and root is right to reject it. A recipe would
select a favourable relation and rung while a conflicting closed-world observation **in the
same relevant universe** sat unread. The requirement list is recipe-authored input; it must
not be able to narrow the evidence the gate reads.

**What I did about it.** Selection is now **independent of `evidenceRequirements`** and takes
every retained native `coverage2` of every relevant universe. Two full-Run controls hold it:
the conflicting negative dissents on `package@manifest-declared` while the plan's only
requirement names `imports`
(`repair-cw-requirement-omission-does-not-bypass-the-dissent`), and supplying a *different*
requirement list selects the identical record set
(`repair-cw-selection-is-independent-of-evidence-requirements`).

---

## Two further things I am correcting on my own initiative

**My "material consequence" framing.** I described two conforming implementations minting two
different authorization subjects "for the same request". Given correction 2, the honest
version is: my helper-level probe showed the *helper* is sensitive to which record it is
handed, and probe A showed two such records are co-retainable in one admitted Run. Joining
those two into a statement about a full product repair was a step I had not executed. The new
controls execute the join properly; the original probe did not.

**My checker-standing observation.** While authoring I found
`check-workflow-projection.v3.py` already ran `evaluator_replay_model.v3.derive` and
`close_run` in its candidate section, while its docstring said it "does not". I corrected that
docstring rather than leaving a stale disclaimer next to my new section. That is a
pre-existing inaccuracy I am reporting, not one I introduced.

---

## Standing of the newly written bytes

**AUTHOR_PENDING_REVIEW.** No author acceptance and no root agreement is claimed for anything
I wrote in this session. The unexecuted boundaries and the disclosed limits are listed in
`author-review.md`; they are part of this correction, not separate from it.
