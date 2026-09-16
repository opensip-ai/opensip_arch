**Verdict: CHANGES_REQUIRED** for subject manifest `948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757`, with 0 MUST issues, 1 SHOULD issue and 6 advisories.

The reviewed finalizer refuses any non-ACCEPT review, so nothing will be applied or activated. I rechecked all subject bytes after writing the review, and the manifest and all 519 entries still match.

**The one SHOULD (APP45-S1):** the per-row map drops required release gates that each row's own sources name, with no per-row explanation. This is the same kind of defect as M-5 in the earlier rejected review.

| Row | Missing gates | Source that names them |
|---|---|---|
| DR-117 | G09 (also G14, G16, G23) | Its own successor, admission §5 item 4: "G09/G21/G29/G30 must exercise…"; the three extra gates come from its historical routing |
| DR-119 | G14 | Retained D-008 fragment; G14 is the self-contained-closure gate |
| DR-114 | G12 | G12 is the doctor gate; historical cell says "G12/G32 execution remains" |
| DR-123 | G01, G02, G05, G12 | Retained D-009 fragment: "DR-G01..G05/G12/G17 carry the evidence" |
| DR-103 | G08 | Historical register cell |
| DR-124 | G09 | Historical register cell |

It is SHOULD rather than MUST because all 32 gates are still mandatory and unperformed, so nothing is falsely qualified today. The fix only touches application records: route the gates or record a reasoned disposition per row, rebuild the manifest, and get a fresh final application review. No contract bytes change, so no new design review or blind consumer is needed.

**What checked out:**
- **Custody:** all 519 entries match, the 12,920-file snapshot has 0 mismatches, and every live path still equals its before-image. The activation file does not exist yet.
- **Normative bytes:** every product contract, schema and model is byte-identical to the accepted snapshot.
- **Pin ledgers:** the five-ledger delta matches the recorded delta exactly, and every ledger matches the post-application tree.
- **Reruns and reproduction:** all 7 reference commands exit 0. The v12-A1 identity counts (1596/1584/12) match my own recount, and all 7 v12-A2 reproduction commands normalize exactly.
- **Prior findings:** M-1 through M-7 and S-1 through S-6 are resolved. A-1 is corrected and A-2 stays as the working-tree-only limitation.
- **Row substance:** every successor section selector resolves, and DR-106, DR-117 (7 items), DR-122 (SARIF) and DR-130 (5/5/6) match their contracts. All 28 rows, 27 inherited rows, 30 evaluation residuals, 16 AR, 15 FW, DR-201 to 205 and the 32 gates are individually supported on design substance. None of this takes effect under this verdict.
- **Docs and tooling:** 518 links resolve (plus the 3 to-be-created activation links), the catalog generator check passes, the inventory scope is correct, and the finalizer and three tooling corrections are sound.
- **TCB-SCOPE-01:** accepted once as a single scope assumption. The 13 dependents match every source account, and rejecting or changing it reopens them jointly.
- **D9-APP-1:** resolved. The obligation is carried on exactly DR-007 and DR-011-R08 and remains live and undischarged. The selected composition is complete; the owning unit's future artifact work is not.

**Advisories:**
- **ADV-01:** the preserved workflows report embeds the old ledger hash, and that difference is disclosed only by the rerun hash.
- **ADV-02:** the design-corrections README chronology has confusing heading structure and a historical commit/push sentence.
- **ADV-03:** "fresh" is used for blind consumer B, which is actually a continuation origin.
- **ADV-04:** the finalizer can't resume from a half-written file; it stops safely but recovery is manual.
- **ADV-05:** the applying D-372 body makes precision edits to the pinned act's wording.
- **ADV-06:** CB-ADV-4 only existed in the historical source20/21 account and is not in the current records.

**Limitations:** I did not re-run the reference suites; I compared the retained rerun byte-for-byte instead. My read-only git call was denied, so git tracking state for A-2 is unmeasured. The large contracts and inventories were checked by structured probes rather than read line by line.

Files are in `/private/tmp/opensip-design-corrections/application-review.v45`:
- review.md
- review.json
- probes/
