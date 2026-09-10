# Application structural checker

`check-architecture-application.v1.py` checks custody and recording structure. It
does not perform semantic review, certify reviewer independence, apply edits,
authorize implementation, or claim product qualification. Candidate and final
modes both exit nonzero while any required item fails or remains pending.

The checker validates the exact 23 affected, nine deferred and 17 target row
sets; the 47 inherited obligation identities; all 86 source-qualified ID-DEP
identities and pins; exact selectors; unit subject/dependency and verdict pins;
undisposed findings; the 17 MF-6 row edits plus G13; the 28→29 named-gate sets
and G13 owner; and the complete byte application to the proposed register SHA.
It also verifies the accepted reference handoff and the exact twelve-document
publication proposal: all source/post-image digests, the complete path set and
current file custody. The external whole verdict binds `documentationImage`
(proposal SHA plus every path/before/after SHA) and `handoffImage`; these fields
are retained in the structural report to make the final review concrete.
The proposed-edits manifest's `byteEdits` uses exact unique `{before,after}`
UTF-8 blocks. Overlapping original ranges and sequential ambiguities refuse.
It never writes the register. Section pins retain their declared heading-range
hash semantics. Explicit review `contextReadPins` are reported as historical
CONTEXT, never promoted to operative evidence. An inline retained reviewer
reproducer is hash-checked without executing it or requiring its old `/tmp` file.

Run a candidate check with the default draft:

```sh
python3 docs/coop/completion/check-architecture-application.v1.py --mode candidate --report /tmp/application-check.json
```

Finalization fills all final pins, accepted unit verdicts and dispositions,
clears pending-finalization lists, and names the final application file. Each
row's four grade slots and MF6 status may be `EXTERNAL-WHOLE-REVIEW`. This is a
requirement for an external verdict, not a grade: the checker requires a real
independent whole review binding the exact final application SHA and supplying
all 68 grades, zero findings and the before/after row hashes. The whole review
also binds the source and complete proposed register digests. Its exact JSON
shape is documented in the checker's module docstring and `--help`. Keeping it
external avoids an application/review hash cycle.

```sh
python3 docs/coop/completion/check-architecture-application.v1.py --mode final --application docs/coop/completion/architecture-application.v1.json --whole-review /path/to/independent-whole-review.json --report /tmp/final-application-check.json
```

Before publication, capture the validated source bytes in a new directory:

```sh
python3 docs/coop/completion/check-architecture-application.v1.py --application docs/coop/completion/architecture-application.v1.json --whole-review /path/to/independent-whole-review.json --capture-snapshot /path/to/new-application-snapshot --report /tmp/pre-publication-check.json
```

After publication, supply `--snapshot-manifest /path/to/new-application-snapshot/snapshot-manifest.json` with the same application and whole-review arguments. The snapshot contains only successfully pinned inputs. Capturing a pending candidate never accepts it. Existing destination directories refuse. The application and external whole verdict remain their separate immutable files.

The closed snapshot format is `{"schemaVersion":1,"files":[{"path":"docs/example.md","sha256":"<whole-file lowercase SHA-256>","snapshotPath":"files/docs/example.md"}]}`. Logical paths are canonical repository-relative paths; snapshot paths resolve relative to the manifest and may explicitly name an absolute archive. Duplicate logical paths and conflicting overrides refuse. Each archive must match its whole-file hash, and every original whole-file or section pin and selector must still match its original contract. Every active pinned read, including nested freeze/review dependencies, JSON pointers and `qualificationRemainderProposed` sources, uses the same historical-byte resolver. An archive cannot waive a hash or substitute a current version for a pinned historical version.

For a register-only adoption, `--register-source /path/to/archived-before.md` installs that same central override for file 08 before global traversal. It is no longer limited to patch application. The exact original register SHA is still required. A full snapshot is preferable when publishing the twelve-document proposal too.

Live register and documentation custody deliberately bypass historical overrides: each must equal the exact before-image or exact after-image. Thus replay succeeds immediately after adoption and rejects unrelated later drift. Reports separate historical replay inputs from live custody observations; no command applies publication edits.

An older unit review's finding remains intact. An accepted independent
supplement can resolve it using `units.<unit>.findingResolutions`, with
`findingId`, a pinned `review`, optional pinned `repairFreeze`, and a
`resolutionPointer`. The pointed record must name that finding and say
RESOLVED/ADDRESSED/CLOSED. The supplement must bind the original review directly
or through its reviewed repair freeze. MCR-S1 uses the actual retained
`/priorFindingDisposition/0` record; the old SHOULD is not erased.

The retained selftest passes 71/71, including real temporary-file pin mutation,
strict duplicate rejection, exact pointers, byte-patch overlap/ambiguity,
nonzero and Boolean finding counts, and synthetic whole-review mutations for
missing/duplicate rows, wrong application/register/MF6 hashes, a missing gate-2
grade, reviewer authorship, a missing documentation binding, a changed document
post-image and a changed handoff hash. Its synthetic positive is explicitly not a
real review or architecture acceptance. Added filesystem probes cover central qualification selectors, archived section hashes and JSON pointers, wrong or mutated archives, duplicate/noncanonical snapshot entries, conflicting overrides, capture/replay and overwrite refusal, and all twelve publication before/after images with unmasked live drift.

The external whole review has this exact required shape. Angle-bracket values are explanatory placeholders, not an authored review or valid acceptance:

```text
{
  "documentClass": "independent-whole-application-review",
  "reviewer": {"id": "<real independent reviewer>", "authoredNoneOfSubjectBytes": true},
  "subject": {"path": "<final application repository-relative path>", "sha256": "<exact final application SHA>"},
  "verdict": "ACCEPT", "mustFix": 0, "shouldFix": 0, "findings": [],
  "registerImage": {"sourceSha256": "<original register SHA>", "proposedSha256": "<complete proposed register SHA>"},
  "documentationImage": {
    "proposalSha256": "<exact pinned twelve-document proposal SHA>",
    "files": [<all twelve {"path", "beforeSha256", "afterSha256"} objects, sorted lexically by path>]
  },
  "handoffImage": {"path": "<handoff repository-relative path>", "sha256": "<exact pinned handoff SHA>"},
  "rows": [<exactly one object below for each of the seventeen target rows>]
}
```

Each row object contains `row`, `grades`, and `MF6`. `grades` has exactly `application`, `D056_gate2`, `D056_gate3`, and `SATISFIED`; each value is `{"verdict":"ACCEPT","mustFix":0,"shouldFix":0,"findings":[]}`. `MF6` has these same four fields plus `beforeSha256` and `afterSha256`, which hash the exact row strings encoded as UTF-8 **without adding a newline**. `CONSENT` is also accepted in place of `ACCEPT`. Counts must be integer zero, never Boolean false. The exact register/documentation/handoff image objects are retained in checker results (`documentPublicationImages` supplies the latter two). The checker requires all seventeen target IDs; no duplicate or omitted row passes.


The final application must additionally contain `incorporatedDependencySupplement: {"path": "docs/coop/completion/architecture-incorporated-dependency-supplement.v1.json", "pin": "<exact SHA-256>"}`. Its authoring shape is retained in `architecture-incorporated-dependency-supplement.draft.json`. This separate inventory preserves the original 47 obligations, 17 rows and 86-source comparison. It adds exactly eight DR-102 ID-DEP definitions (94 total), eleven separately named FC/UR conditions, and 38 separately classified inherited claim rides. The catalogue's 57 additional source-qualified identities are reconstructed from exact named source containers; records, definitions, SHA/JSON-pointer identities, counts and target references must agree. The thirteen host branches, fourteen EE fixture references and five V1 evidence custody edges are counted separately. Exact predecessor-to-selected-source identity mappings prevent silent lineage drops.

Each inherited claim must classify its active/excluded branch with exact D-002/D-018 authority; authoritative split/excluded branches also require D-077/D-078. These checks verify that concrete scope records and source pointers exist. They do not decide whether an author's semantic scope interpretation is correct; the independent whole review remains necessary. Current inherited authority uses the same archived coordinator before-image as the other frozen units.

For finalization, copy the author supplement into its final version, update copied target source references to the final application target sources and accepted final unit versions, retain the original historical `applicationBasis` and 86-row inventory pins, and pin the final supplement in the final application. Clear pending finalization notes only when the actual reviews/owner acts justify it. A copied pending security/courier pin remains PENDING in this checker, even when the reference's target name exists.

The nine added supplement selftests retain exact source inventory acceptance as a structural test only and reject missing DR-102 definitions, duplicate FC records, wrong-but-valid canonical/lineage pointers, false denominators, missing targets, omitted lineage members and absent scope authority. No selftest supplies a real application grade.


Prospective integrated enactment is acyclic. Freeze the proposal application first, obtain an external whole review bound to those exact bytes, and only then record D-369 and publish the accepted images. The immutable application remains a proposal snapshot even during later replay; its `false` enactment fields do not claim to report live post-publication state. The checker reports proposed images and live file custody separately and still makes no live-readiness claim.

Supported application transformations (do not use these to clear missing unit evidence):

- Add `enactmentPlan` with `status: "PROPOSED-FOR-INTEGRATED-ENACTMENT"`, `declarationKind: "PROPOSAL-NOT-LIVE-ADOPTION-STATE"`, `proposal: {path,pin,selector}`, `alreadyEnacted: false`, `requiresWholeReview: true`, `requiresZeroFindings: true`, `implementationAuthorization: false`, and `recordingOrder: ["independent-whole-review", "integrated-D369-enactment", "verify-published-images", "claim-design-complete"]`.
- For each of the seven existing `ownerActsRequired` entries, keep its exact `requiredAct`, rows, targets and pinned `proposal`. Set `status: "PROPOSED-FOR-INTEGRATED-ENACTMENT"`, `enacted: false`, `enactOnlyAfter: "WHOLE-REVIEW-ACCEPT-0-0"`, and `reviewerGradeRequired: {"status":"EXTERNAL-WHOLE-REVIEW"}`. Do not supply a self-authored verdict. The prerequisite means an accepted whole verdict with zero findings; either ACCEPT or CONSENT is recognized.
- For each SD-1..8, preserve the five-part scope application, source and accepted unit review. Set `adoption` to the same prospective status; add `enacted: false`, the same `enactOnlyAfter` and `reviewerGradeRequired`, and `enactmentProposal` pointing to the exact integrated D-369 proposal.
- Keep `registerMutation: false`, `documentationApplication.applied: false` and `condition5Authorization: false`. Per-row four-grade and MF6 requirements remain EXTERNAL-WHOLE-REVIEW. Completed evidence may leave the pending-unit lists only after its real accepted versions are pinned. Once the remaining application/owner/scope/whole-review tasks are concretely represented above, their old generic pending-finalization reminders may be removed: the mandatory structural/external-grade checks replace those reminders. Retain every actual missing review, source or repair as pending.

The external whole review adds three required fields:

```text
"enactmentImage": <exact enactmentImage object emitted in the structural report>,
"ownerActGrades": {<each of the seven ACT IDs>: {"verdict":"ACCEPT", "mustFix":0, "shouldFix":0, "findings":[]}},
"scopeApplicationGrades": {"SD-1": <same zero-finding grade>, ..., "SD-8": <same zero-finding grade>}
```

`enactmentImage` contains mode `REVIEW-PROPOSED-ACTS-THEN-ENACT`, the normalized integrated proposal `{path,sha256,selector}`, the exact four-step recording order, sorted `ownerActs` entries `{id,proposal}`, and sorted `scopeDispositions` entries `{id,source,proposal}`. All nested source/proposal references normalize to `{path,sha256,selector}`. The application digest additionally binds all concrete act/scope text and evidence. Whole-review approval of proposed acts supplies neither a runtime GRANT nor evidence that D-369 has been enacted. Recording and image verification remain necessary before claiming design completion.

The enactment selftests accept a fully specified but unenacted synthetic proposal and reject missing proposals or grade requirements, self-graded acceptance, omitted acts, substituted proposal hashes, false enactment/adoption/publication claims, and enact-before-review order. Whole-review mutations reject missing owner/scope grades, nonzero findings and a substituted enactment image. The external verdict remains the sole final pending check only when all actual source, unit, prospective-application and grade-declaration checks pass.
