# D-364 — A D-294 Decision 2(b) citation-refresh successor is not a D-056 gate-2 remainder

> **Status:** DRAFT — under review.
> **Date:** 2026-09-01
> **Protocol:** D-000, turn 2 of 3. Turn 1 drew OBJECT from both independent
> reviewers. This turn lands every turn-1 identifier: **CODEX-D364-MF1**,
> **CODEX-D364-SF1**, **CLAUDE-D364-MF1**, **CLAUDE-D364-SF1**,
> **CLAUDE-D364-SF2**, **CLAUDE-D364-SF3**, **CLAUDE-D364-ADV-1**,
> **CLAUDE-D364-ADV-2**, **CLAUDE-D364-ADV-3**. The turn-1 subject
> `coordinator-decisions.D-364.draft.md`
> `5da3c7d3b1923f71f9c94b672003105c830fb7c764d7c562152bd59a01db54e2` remains
> frozen and unrecorded. Same class as D-294: a reading convention adopted at
> dual CONSENT, COORD-only, no owner act required.
> **Decision type:** RULE-GOVERNED. Classification of an artifact class under
> adopted text. This is coordinator decision **D-364**, not a register row.
> **Numbering:** D-363 is an in-flight cycle at turn 1 of 3 (subject
> `coordinator-decisions.D-363.draft.md`
> `134b0bd0754c8a643c8f9b3c6cad1814a4cd9b373bbb62a2e1c6ded50d486815`; Claude 2
> returned CLAUDE-D363-MF1, CLAUDE-D363-MF2 and CLAUDE-D363-SF1, Codex returned
> one unlabeled MUST-FIX and `currentFindingIdentifiers` as the empty list). Its
> number stays reserved to it and its two remaining turns are unconsumed by this
> entry. This entry takes the next free number and is recorded first. COORD
> heading order is not monotonic — it already carries out-of-order pairs and
> unrecorded gaps — and D-000 imposes no monotonicity.
> **Does not** amend D-056. **Does not** create an exception to any D-056 gate.
> **Does not** SATISFY DR-117, DR-131, DR-133, or any row.
> **Does not** perform D-056 Eligibility gate 4 or gate 5 for any row.
> **Does not** re-perform, widen, narrow or re-open the D-316 Class A opening.
> **Does not** amend D-000, D-133, D-293, D-314, D-315, D-316, or D-294
> Decisions 1, 2, 3 or 5.
> **Does not** discharge the successor owed on the g29 and g30 grounds.
> **Does not** decide any reserved number, list, owner, or Class A question.
> **Does not** record, edit or supersede any artifact, and binds no fixture bytes.
> **Does not** edit file 08. **Does not** change live required-now 28.
> **Does not** authorize `docs/v2/implementation/`.

D-056 is ADOPTED at `75c981dd2b827c5ce11c37013b2e124870ee9c6e`; its pinned
turn-2 subject is `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md`
`dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82`.
D-133 is ADOPTED at `5b6f7232c66d72ae8385f709cf95b9e493c2af59`.
D-293 is ADOPTED at `c10319d207cb90e2bf9df4c5e5997cfd35a30193`.
D-294 is ADOPTED at `f3456575071928022a1f0e3a77e531a87157b365`.
D-295 is ADOPTED at `b993902017d8f8fda5f9fc0590b402ec4c27a41f`.
D-314 is ADOPTED at `f3b05e33479652ede37f0502084b50b590f630f7`.
D-316 is ADOPTED at `76cc272426e13a874b65d62bc2f2ed9771fe7f8f`.
D-320 is ADOPTED at `bc1e5304859d675feaf83df8835d26dbfaaccaf7`.
D-321 is ADOPTED at `a126647a5456b9511b5ae6e6387aab67dc530e5f`.
D-340 is ADOPTED at `2c5190db25fd3c802fd7d7412544f7c3ce0ff5b6`.
D-343 is ADOPTED at `dded779167358ec0ac7547ec6740f127f2c22107`.
HEAD is `f7a98a70e650d0ed2639f815fa932bff21a99b83`.
Last live heading is D-362. Required-now is 28.

## What turn 1 got wrong

Turn 1 argued that a fired D-294 trigger (b) "conditions no D-056 Eligibility
gate." Both reviewers landed the same MUST-FIX against it, from the same bytes.
D-056's pinned turn-2 subject, Eligibility (narrow) item 2, reads:

> Every remaining acceptance-evidence member is **only** harness *execution*,
> fixture *execution*, or qualification *measurement*. Authoring of fixtures,
> schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers
> is **not** a remainder this amendment may split.

Gate 2 names **successors** among the authoring categories it excludes, and
D-133 makes those five gates the definition, measured for the row at the moment
of the later cycle. Turn 1 neither quoted that sentence nor pinned the subject it
relied on, and its clause 4 — a SATISFIED entry proceeding with an owed successor
"named as outstanding work" — read against gate 2 is a split of successor
authoring off the remainder. Codex added that gate 3 independently requires each
allowed remainder to be *already* named at a condition-4 / DR-G* obligation, which
naming an outstanding successor inside a future entry does not achieve.

This turn does not repeat that argument. It makes a narrower and different claim:
the owed successor is **not a member of the set gate 2 quantifies over**, so no
exception to gate 2 is needed and D-056 is unamended.

## Measured position at this dispatch

`preview-product-boundary-successor.v10` cites twelve leftover-joins. Four are
superseded since its D-295 recording. Under D-294 Decision 2 (b)'s mechanical
test, measured from the two files' bytes for each pair:

| Lineage | Cited → current | Trigger (b) | Ground |
|---|---|---|---|
| g29 | leftover-join.v4 (D-254) → leftover-join.v7 (D-343) | **fires** | `existingGate` of OBL-G29-FX-AUTHORING, a named obligation, changed at leftover-join.v6 (D-320); `summary.leftoverDesign` `[OBL-G29-FX-AUTHORING]` → `[]` at leftover-join.v7 (D-343) |
| g30 | leftover-join.v4 (D-255) → leftover-join.v10 (D-340) | **fires** | `existingGate` of OBL-G30-FX-AUTHORING changed at leftover-join.v8 (D-321); `summary.leftoverDesign` `[OBL-G30-FX-AUTHORING]` → `[]` at leftover-join.v10 (D-340) |
| g21 | leftover-join.v13 (D-292) → leftover-join.v45 (D-359) | does not fire | partition, `registerRow`, `file08StatusToken` and `liveGateOwners` are equal, and OBL-G21-FX-AUTHORING's `leftoverDesign`, `existingGate`, `rideStanding` and `executionObligationOwnerToday` are equal. The one projected-field change in the pair is `executionObligationOwnerToday` on OBL-DR102-SATISFIED-NOT-REOPENED, an obligation `preview-product-boundary-successor.v10` names nowhere, so it is outside the test |
| distribution-core | leftover-join.v9 (D-287) → leftover-join.v10 (D-308) | does not fire | the partition is equal; `summary.d006UnitUndecided` changed true→false and OBL-2's reason text changed, and neither is a member of Decision 2 (b)'s projection |

`preview-product-boundary-successor.v10` carries no "still measures … leftoverDesign
true/false" sentence, so that limb of the test is vacuous for all four pairs. The
EE-3a partition sentence "leftoverDesign remains [OBL-G21-FX-AUTHORING] on g21
leftover-join.v13" holds at leftover-join.v45.

A successor is therefore owed on the g29 and g30 grounds, and on those two alone.

## Decision

1. **D-294's predicate reaches a recorded leftover remasurement of a
   design-contract candidate.** D-295's heading records
   `preview-product-boundary-successor.v10` "as DR-117 leftover remasurement",
   and that artifact's own `purpose` and `joinCurrencyAudit.standing` state that
   it refreshed its cross-lineage citations "under D-294 Decision 3" at 42 sites.
   The predicate is read by the function the artifact performs in the record, not
   by its filename or its `documentClass`.

2. **Decision 1 and Decision 2 are independent limbs and are not an either/or.**
   Decision 1 governs how a cross-lineage citation *reads*: custody at the citing
   artifact's own recording heading, not a standing claim about live HEAD.
   Decision 2 governs when the citing artifact *owes a successor*. A citation
   reads as custody whether or not a successor is owed, and an owed successor
   does not convert a custody sentence into a standing currency claim. Applying
   one limb while denying the other on the same predicate is not available; that
   was D-363 turn 1's defect.

3. **A D-294 Decision 2(b) successor of a citing artifact is not a D-056 gate-2
   remainder, because it is not an acceptance-evidence member.** Gate 2
   quantifies over "every remaining **acceptance-evidence member**", and excludes
   authoring that would supply such a member: fixtures, schemas, successors,
   actor-joins, missing design, still-UNDECIDED numbers. D-294 Decision 3 defines
   what the owed successor does: it "refreshes its cross-lineage citations to the
   versions current at its dispatch and labels the superseded ones as not
   current", and "No frozen artifact is edited to achieve this." Such a successor
   supplies no acceptance-evidence member, no design content, no fixture, no
   schema, no number, and changes no binding content of the accepted contract; it
   keeps the citing artifact's own currency sentences accurate. It is therefore
   outside the set gate 2 quantifies over. This is a classification of an
   artifact class, not an exception to gate 2, and D-056 stands unamended.
   Compare D-315 item 4 (G3-HOSTILE), which recognises a mechanical join
   remasurement that "adds no semantic choice" as proceeding under existing
   delegation.

4. **Gate 3 does not reach it either, for the same reason.** Gate 3 requires
   "each such remainder" to be already named as a condition-4 / DR-G* obligation
   with an owner. "Such" refers to the gate-2 remainders. An owed citation-refresh
   successor is not one, so gate 3 imposes no naming duty on it. DR-117's actual
   remainder is the execution of the fourteen enforcement-evidence classes, named
   at DR-G09, DR-G14, DR-G16, DR-G21, DR-G23, DR-G29 and DR-G30.

5. **Relied-upon is not the same as acceptance-evidence.** D-294 Decision 2 (b)
   fires because the citing artifact relied on a changed projected value for the
   accuracy of its own currency sentences. That reliance is what makes a
   citation-refresh successor owed. It does not make the successor a member of
   the row's acceptance evidence, which is what gate 2 quantifies over. The two
   senses of reliance are distinct, and reading them as one is what would create
   the exception this entry declines to create.

6. **A SATISFIED re-record may proceed while a Decision 2(b) citation-refresh
   successor is outstanding.** The entry performing gates 4 and 5 measures the
   row's remainder against live bytes at its own dispatch rather than against the
   accepted contract's frozen citation sentences, and names the owed successor,
   its ground and its owner. Naming is not discharging, and the successor remains
   owed.

7. **A later successor does not move Eligibility gate 1.** When the owed
   successor is recorded as the current remasurement of its lineage, it does not
   reopen, move or re-perform gate 1, which the owner's opening fixed at the
   accepted contract's digest. Whether a later coordinator act rests a cycle on
   the successor's bytes instead is that act's own decision and is not decided
   here.

8. **If clause 3's classification is rejected, clause 6 falls with it.** This
   entry states one reading and holds it. Should a later reviewed act hold that a
   Decision 2(b) successor *is* a gate-2 remainder, the consequence is that the
   successor must be discharged before gates 4 and 5 for the affected row, and
   clause 6 does not stand. The alternative route — a scoped reviewed amendment
   of D-056 making this class of maintenance successor non-blocking — is
   available and is not taken here, because on clause 3's classification no
   amendment is required.

9. **Scope.** This entry governs the classification of a D-294 Decision 2(b)
   citation-refresh successor under D-056 from this heading forward. It adopts no
   measurement as standing beyond the dispatch table above, which is dated. It
   records no artifact and edits no file 08 cell.

## Alternatives

- **Take the narrow reading of D-294's predicate** — it reaches no
  design-contract candidate, so nothing is owed. Rejected: it contradicts
  D-295's own heading and `preview-product-boundary-successor.v10`'s own bytes,
  which invoke D-294 Decision 3 by name.
- **Hold that a fired trigger (b) suspends gates 4 and 5 until the successor is
  recorded.** Rejected on clause 3's classification: gate 2 quantifies over
  acceptance-evidence members and a citation refresh supplies none. Turn 1
  rejected this on the ground that "no adopted text says so", which was
  overstated — gate 2 names successors — and that ground is withdrawn.
- **Adopt a scoped amendment of D-056 instead.** Not unlawful, and expressly
  available per clause 8; not taken, because no amendment is needed if the
  classification holds. Presenting an amendment as a reading that leaves D-056
  unamended is what this entry avoids.
- **Discharge the successor first.** Not unlawful; four candidates
  (`preview-product-boundary-successor.v11` through `.v14`, digests in the
  measured-inputs table) were authored on that route and each was rejected at
  Stage A by both reviewers, and none is recorded. That route stays open and is
  the consequence clause 8 names if clause 3 is rejected.
- **Settle it inside D-363 turn 2.** Rejected: it would make the SATISFIED cycle
  a two-limb act.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming
half (28 of 28); required-now stays 28. Condition 5 remains NOT MET and last.
File 08 is untouched. No artifact is recorded or superseded. The successor owed
on the g29 and g30 grounds remains owed after this entry.

## Reversibility

Total. Overturn: C-D364. Restores the unsettled fork as of D-363 turn 1 and, if
a dependent SATISFIED re-record has landed, also requires that re-record's
supersession. Does not unwrite D-056, D-133, D-293, D-294, D-295, D-314, D-315,
D-316, D-320, D-321, D-340, D-343, or any entry from D-170 through D-362.

## Commit

C-D364.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `bae06532b8417800414ee4fbdcd980135365185ce88b2244f92f6767412f264f` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `f7a98a70e650d0ed2639f815fa932bff21a99b83` |
| coordinator-decisions.D-056.turn2.draft.md | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| preview-product-boundary-successor.v10.json | `8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483` |
| g29-leftover-join.v4.json | `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` |
| g29-leftover-join.v6.json | `57b188dc4ded78a88b8be221f6c9d08b5bd7fccdade050a21dbe5580f101b0e3` |
| g29-leftover-join.v7.json | `ae4b69c109e15eac9a73605881db9de671bdf512aacc3e9df6565acb029747c8` |
| g30-leftover-join.v4.json | `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` |
| g30-leftover-join.v8.json | `804ce7e91f2f1f1eba04cdb004e5a0f9bacea89635ee7ed6c6f1803edbcde3a6` |
| g30-leftover-join.v10.json | `4605c2f2abc2150bf49b02f4b9fb97c0a53c1257f521d44269f234b3ab1b7c09` |
| g21-leftover-join.v13.json | `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e` |
| g21-leftover-join.v45.json | `f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc` |
| distribution-core-leftover-join.v9.json | `e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7` |
| distribution-core-leftover-join.v10.json | `1de52b7675925e3ddb1b863113f019d5aec9a1eea760a85e2e857dbf7d3f8ff3` |
| preview-product-boundary-successor.v11.json | `d25a7f29148b41e1e1991876c0f2ba549ef2d15834c2776feb52aeac97caf881` |
| preview-product-boundary-successor.v12.json | `2f31ca88e263cd93fd7b3bb97b18d6cecab87df87e661ac90575cfddca4643f9` |
| preview-product-boundary-successor.v13.json | `fd571584e1d8596b279e26977b2dbf708dd900a069a5cc9b3151e6dfb0622f8f` |
| preview-product-boundary-successor.v14.json | `93a8e421234b7cd3f349953e37ba4f6fdaf51cb73706c5f3ceaa420033308ad1` |
| coordinator-decisions.D-363.draft.md | `134b0bd0754c8a643c8f9b3c6cad1814a4cd9b373bbb62a2e1c6ded50d486815` |
| coordinator-decisions.D-364.draft.md (turn 1, frozen, unrecorded) | `5da3c7d3b1923f71f9c94b672003105c830fb7c764d7c562152bd59a01db54e2` |
| D-056 commit | `75c981dd2b827c5ce11c37013b2e124870ee9c6e` |
| D-133 commit | `5b6f7232c66d72ae8385f709cf95b9e493c2af59` |
| D-293 commit | `c10319d207cb90e2bf9df4c5e5997cfd35a30193` |
| D-294 commit | `f3456575071928022a1f0e3a77e531a87157b365` |
| D-295 commit | `b993902017d8f8fda5f9fc0590b402ec4c27a41f` |
| D-314 commit | `f3b05e33479652ede37f0502084b50b590f630f7` |
| D-316 commit | `76cc272426e13a874b65d62bc2f2ed9771fe7f8f` |
| D-340 commit | `2c5190db25fd3c802fd7d7412544f7c3ce0ff5b6` |
| D-343 commit | `dded779167358ec0ac7547ec6740f127f2c22107` |

The eight leftover-join files pinned above — the cited and current version of
each of the four lineages — plus file 08, file 02, the accepted contract, the
D-056 turn-2 subject and this draft are the fixed measurement set. If a cited
file moves in a way that is not append-only COORD growth or COORD heading
hygiene, with those files unmoved, re-measure before adoption. Append-only COORD
after this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
