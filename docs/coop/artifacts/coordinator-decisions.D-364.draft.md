# D-364 — The D-294 successor obligation is independent of the D-056 gates

> **Status:** DRAFT — under review.
> **Date:** 2026-09-01
> **Protocol:** D-000 new cycle, turn 1 of 3. Same class as D-294: a reading
> convention adopted at dual CONSENT, COORD-only, no owner act required.
> **Decision type:** RULE-GOVERNED. Reading convention over adopted text.
> This is coordinator decision **D-364**, not a register row.
> **Numbering:** D-363 is an in-flight cycle at turn 1 of 3 (subject
> `coordinator-decisions.D-363.draft.md`
> `134b0bd0754c8a643c8f9b3c6cad1814a4cd9b373bbb62a2e1c6ded50d486815`,
> both turn-1 verdicts OBJECT). Its number stays reserved to it and its two
> remaining turns are unconsumed by this entry. This entry takes the next free
> number and is recorded first. COORD heading order is not monotonic — it
> already carries out-of-order pairs and unrecorded gaps — and D-000 imposes no
> monotonicity.
> **Does not** SATISFY DR-117, DR-131, DR-133, or any row.
> **Does not** perform D-056 Eligibility gate 4 or gate 5 for any row.
> **Does not** re-perform, widen, narrow or re-open the D-316 Class A opening.
> **Does not** amend D-000, D-056, D-133, D-293, D-314, D-315, D-316, or
> D-294 Decisions 1, 2, 3 or 5.
> **Does not** decide any reserved number, list, owner, or Class A question.
> **Does not** record, edit or supersede any artifact, and binds no fixture bytes.
> **Does not** edit file 08. **Does not** change live required-now 28.
> **Does not** authorize `docs/v2/implementation/`.

D-056 is ADOPTED at `75c981dd2b827c5ce11c37013b2e124870ee9c6e`.
D-133 is ADOPTED at `5b6f7232c66d72ae8385f709cf95b9e493c2af59`.
D-293 is ADOPTED at `c10319d207cb90e2bf9df4c5e5997cfd35a30193`.
D-294 is ADOPTED at `f3456575071928022a1f0e3a77e531a87157b365`.
D-295 is ADOPTED at `b993902017d8f8fda5f9fc0590b402ec4c27a41f`.
D-314 is ADOPTED at `f3b05e33479652ede37f0502084b50b590f630f7`.
D-316 is ADOPTED at `76cc272426e13a874b65d62bc2f2ed9771fe7f8f`.
D-340 is ADOPTED at `2c5190db25fd3c802fd7d7412544f7c3ce0ff5b6`.
D-343 is ADOPTED at `dded779167358ec0ac7547ec6740f127f2c22107`.
HEAD is `f7a98a70e650d0ed2639f815fa932bff21a99b83`.
Last live heading is D-362. Required-now is 28.

## Why this entry exists

D-363 turn 1 proposed recording DR-117 `SATISFIED`. Both independent reviewers
returned OBJECT on one shared MUST-FIX: the draft applied D-294 Decision 1 to
`preview-product-boundary-successor.v10` while denying D-294 Decision 2 on the
ground that the same artifact is not a leftover-join. Both clauses open with the
same subject-class predicate, so that reading is not available. Codex's repair
named an either/or — a lawful dispatch-time custody basis, or a reviewed
successor. Claude's repair named the same fork and added that, if the broad
reading is taken, the entry must say why a fired trigger does not require a
successor before gates 4 and 5.

Four candidate successors were authored on the successor limb
(`preview-product-boundary-successor.v11` through `.v14`) and each was rejected
at Stage A by both reviewers. None is recorded. The fork was never settled as a
rule, so each cycle re-litigated it.

This entry settles the reading. It is the same instrument D-294 itself was: a
coordinator reading convention over adopted text, carrying no owner decision.

## Measured position at this dispatch

`preview-product-boundary-successor.v10` cites twelve leftover-joins. Four are
superseded since its D-295 recording. Under D-294 Decision 2's mechanical test,
measured from the two files' bytes for each:

| Lineage | Cited → current | Trigger (b) |
|---|---|---|
| g29 | leftover-join.v4 (D-254) → leftover-join.v7 (D-343) | **fires** — `summary.leftoverDesign` `[OBL-G29-FX-AUTHORING]` → `[]` |
| g30 | leftover-join.v4 (D-255) → leftover-join.v10 (D-340) | **fires** — `summary.leftoverDesign` `[OBL-G30-FX-AUTHORING]` → `[]` |
| g21 | leftover-join.v13 (D-292) → leftover-join.v45 (D-359) | does not fire — partition, `registerRow`, `file08StatusToken`, `liveGateOwners`, and OBL-G21-FX-AUTHORING's `leftoverDesign`, `existingGate`, `rideStanding` and `executionObligationOwnerToday` are equal |
| distribution-core | leftover-join.v9 (D-287) → leftover-join.v10 (D-308) | does not fire — the partition is equal; `summary.d006UnitUndecided` changed true→false and OBL-2's reason text changed, and neither is a member of Decision 2 (b)'s projection |

So a successor is owed on the g29 and g30 grounds, and on those two alone. The
other two citations are refreshed under D-294 Decision 3 when a successor issues
for some other reason; they oblige nothing by themselves, which is what D-294
Decision 1's closing sentence says of version-only staleness.

## Decision

1. **D-294's predicate reaches a recorded leftover remasurement of a
   design-contract candidate.** D-295's heading records
   `preview-product-boundary-successor.v10` "as DR-117 leftover remasurement",
   and that artifact's own `purpose` and `joinCurrencyAudit.standing` state that
   it refreshed its cross-lineage citations "under D-294 Decision 3" at 42 sites.
   The predicate is read by the function the artifact performs in the record, not
   by its filename or its `documentClass`. The narrow reading — that D-294
   reaches nothing but a file whose name ends `leftover-join` — is not adopted.

2. **Decision 1 and Decision 2 are independent limbs and are not an either/or.**
   Decision 1 governs how a cross-lineage citation *reads*: it is custody at the
   citing artifact's own recording heading, not a standing claim about live HEAD.
   Decision 2 governs when the citing artifact *owes a successor*. A citation
   reads as custody whether or not a successor is owed, and an owed successor
   does not convert a custody sentence into a standing currency claim. Applying
   one limb while denying the other on the same predicate is not available; that
   was D-363 turn 1's defect and it is not repeated by reading the limbs apart.

3. **A fired trigger (b) obliges a successor of the citing artifact and
   conditions no D-056 Eligibility gate.** Grounds, each from adopted text:
   (a) D-294 Decision 2 states when a successor is required. It names no act that
   waits on one, and its own text contemplates an owed successor coexisting with
   a live status token: "a join on a SATISFIED row whose consumed occupancy is
   superseded still needs a successor."
   (b) D-056's five Eligibility gates condition nothing on D-294 discharge, and
   D-133 holds those five gates as the definition of eligibility.
   (c) Chronology. D-316 opened Eligibility gate 1 Class A on 2026-08-29 at the
   accepted contract's digest. The remasurements that fired trigger (b) were
   recorded on 2026-08-31 at D-340 and D-343. The obligation arose after the
   acceptance and is therefore not an undischarged condition of that acceptance
   in the T2-02 sense.
   (d) D-293 Decision 5 and D-314 item 1 place the G29 and G30 fixture authoring
   between the owner-controlled opening and the later per-row cycle, and name no
   successor step between them.

4. **A SATISFIED re-record may proceed with the owed successor named as
   outstanding work.** The entry performing gates 4 and 5 measures the row's
   remainder against live bytes at its own dispatch rather than against the
   accepted contract's frozen citation sentences, and names the owed successor,
   its ground, and its owner. Naming it is not discharging it.

5. **A later successor does not move Eligibility gate 1.** When the owed
   successor is recorded as the current remasurement of its lineage, it does not
   reopen, move or re-perform gate 1, which the owner's opening fixed at the
   accepted contract's digest. Whether a later coordinator act rests a cycle on
   the successor's bytes instead is that act's own decision and is not decided
   here.

6. **Scope.** This entry governs the reading of the D-294 successor obligation
   from this heading forward. It adopts no measurement as standing beyond the
   dispatch table above, which is dated. It does not amend the entries listed in
   the front matter, records no artifact, and edits no file 08 cell.

## Alternatives

- **Take the narrow reading** — D-294 reaches no design-contract candidate, so
  nothing is owed. Rejected: it contradicts D-295's own heading and
  `preview-product-boundary-successor.v10`'s own bytes, which invoke D-294
  Decision 3 by name.
- **Hold that a fired trigger (b) suspends gates 4 and 5 until the successor is
  recorded.** Rejected: no adopted text says so, and the chronology at 3(c) puts
  the obligation after the acceptance it would be read to condition.
- **Settle it inside D-363 turn 2 rather than as its own entry.** Rejected: it
  would make the SATISFIED cycle a two-limb act, and the same question governs
  DR-131 and DR-133, whose accepted candidates cite joins that can go stale the
  same way.
- **Keep authoring successor candidates until one is accepted.** Not rejected as
  unlawful, and the owed successor remains owed; rejected as the route to gates 4
  and 5, because it settles no reading and each cycle re-litigates the fork.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming
half (28 of 28); required-now stays 28. Condition 5 remains NOT MET and last.
File 08 is untouched. No artifact is recorded or superseded. The successor owed
on the g29 and g30 grounds remains owed after this entry.

## Reversibility

Total. Overturn: C-D364. Restores the unsettled fork as of D-363 turn 1 and, if
a dependent SATISFIED re-record has landed, also requires that re-record's
supersession. Does not unwrite D-056, D-133, D-293, D-294, D-295, D-314, D-315,
D-316, D-340, D-343, or any entry from D-170 through D-362.

## Commit

C-D364.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `bae06532b8417800414ee4fbdcd980135365185ce88b2244f92f6767412f264f` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `f7a98a70e650d0ed2639f815fa932bff21a99b83` |
| preview-product-boundary-successor.v10.json | `8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483` |
| g29-leftover-join.v4.json | `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` |
| g29-leftover-join.v7.json | `ae4b69c109e15eac9a73605881db9de671bdf512aacc3e9df6565acb029747c8` |
| g30-leftover-join.v4.json | `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` |
| g30-leftover-join.v10.json | `4605c2f2abc2150bf49b02f4b9fb97c0a53c1257f521d44269f234b3ab1b7c09` |
| g21-leftover-join.v13.json | `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e` |
| g21-leftover-join.v45.json | `f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc` |
| distribution-core-leftover-join.v9.json | `e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7` |
| distribution-core-leftover-join.v10.json | `1de52b7675925e3ddb1b863113f019d5aec9a1eea760a85e2e857dbf7d3f8ff3` |
| coordinator-decisions.D-363.draft.md | `134b0bd0754c8a643c8f9b3c6cad1814a4cd9b373bbb62a2e1c6ded50d486815` |
| D-056 commit | `75c981dd2b827c5ce11c37013b2e124870ee9c6e` |
| D-133 commit | `5b6f7232c66d72ae8385f709cf95b9e493c2af59` |
| D-293 commit | `c10319d207cb90e2bf9df4c5e5997cfd35a30193` |
| D-294 commit | `f3456575071928022a1f0e3a77e531a87157b365` |
| D-295 commit | `b993902017d8f8fda5f9fc0590b402ec4c27a41f` |
| D-314 commit | `f3b05e33479652ede37f0502084b50b590f630f7` |
| D-316 commit | `76cc272426e13a874b65d62bc2f2ed9771fe7f8f` |
| D-340 commit | `2c5190db25fd3c802fd7d7412544f7c3ce0ff5b6` |
| D-343 commit | `dded779167358ec0ac7547ec6740f127f2c22107` |

If a cited file moves in a way that is not append-only COORD growth or COORD
heading hygiene, with file 08, the six leftover-joins, the accepted contract and
this draft unmoved, re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
