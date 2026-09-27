Grok review 465b (parent preparation and creation permit) and inventory71, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-parent-preparation465b-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

**Safety: never run a premise-bearing preparation against the real home. The tests use scratch homes only; the one real-home test checks the refusal at `/`. After your replay, confirm that ~/Library/Application Support/OpenSIP still does not exist.**

Law: docs/implementation/m2/initial-parent-preparation-465/PROPOSAL.md items 1–11 (accepted; items 4 and 5 are owner decisions). Product HEAD 000c5ce. hashes.txt pins every uncommitted file:
- the 465a platform files you already accepted (directory_effects.rs, filesystem.rs, directory_open.rs, descriptor_filesystem.rs, lib.rs), unchanged since your 465a review;
- 465b's new custody/installation_parent.rs and installation_parent_tests.rs;
- 465b's edits to custody.rs, installation_root.rs, initial_installation.rs, private_access.rs, trust.rs, root_payload.rs, initial_platform.rs and initial_platform_tests.rs.

## 465b summary

`prepare_installation_parent` (A0–A5 with effects E1–E4) and `mint_creation_permit` (B1–B3), each in one attempt. Deviations from the plan, all disclosed by the implementer:
1. The 460 walk gains `OpenSipJudgment::Retain`: it keeps OpenSIP by exact name so that item 5's no-ACL state can be judged read-only before any effect. Other states refuse (`Unfinishable` or `Private`).
2. `preview-v1` is detected in A2, before any effect, giving NotPristine.
3. A reused ancestor is admitted inside a zero-cost `work.effect`, sharing the reserved-form admission code with the create path.
4. `judge_captured_ancestor` is shared, and `AclOmissionPremise::admits_reserved` is added. Evidence B is still only the premise's own fstatfs.
5. The name recheck is the exact descriptor name plus a no-follow reopen with the same device and inode.
6. The item 5 staging scan is bounded to 64 entries.
7. The preparation binds to the intent via a new `CreationIntent::binding()` (RequestId) plus the target.
8. Storage strength is ordered NotBackedUp < Unknown < BackedUp. A stronger class without the flag refuses.
9. FullFlush or Fsync is accepted under apfs; the platform only yields Fsync as the named fallback.
10. `prepare_fresh_private_sample_reserved` is now `pub(crate)`.
11. `#[allow(private_interfaces)]` is added on the initial_core and initial_platform modules.
12. The permit's recheck does not re-observe `preview-v1`; that race belongs to 467.

Tests: 13, listed in the implementer's report; they cover the cases in law items 1–11. Not covered: a different filesystem (needs an APFS image), a live storage-class change (the classifier is constant), a receipt for another handle (unreachable), and names changing mid-act.

## Inventory71

v70 plus three rows: directory_effects.rs (adapter), installation_parent.rs (service) and installation_parent_tests.rs (test); 726 rows, with the byte-identical helper giving PASS. The description overrides for initial_installation.rs and private_access.rs (stale in v70) are NOT included: an inventory successor cannot add new overrides, which come only from contract successors. That is noted as a follow-up.

## Lead's replay

The workspace passed twice, 1022/0; clippy and fmt pass. One earlier full run hit a rare pre-existing race in platform `native_filesystem_original_file_lock_and_all_path_components_stay_owned`, which compares the ancestor metadata of the shared per-user temp directory. At HEAD it passed 5 of 5 runs, and with these changes the platform suite passed 10 of 10. The fix (test isolation) is logged separately. ~/Library/Application Support/OpenSIP does not exist.

## Decide

Does 465b implement items 1–11 exactly?
- Is any effect taken before every recheck?
- Is every create reserved before mkdirat?
- Are the barrier records and seven slots right?
- Is EEXIST handled per item 3?
- Are items 4 and 5 applied in exactly their scope?
- Is the permit single-use and bound to its intent?

Are the deviations acceptable? Is v71 exactly v70 plus three rows?

**Output format (verifier shape):** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of the v71 subject manifest in subjects.txt;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v71.json, parent (v70 pin), successorRecord (the pin of the v71 unit's successor.json)}.

Replay the security and platform libs, the workspace, clippy and fmt. Write REVIEW.md and review.json. Do not commit.
