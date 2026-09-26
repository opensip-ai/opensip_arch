Grok review 462b and 462c (InitialPlatform) and inventory70, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-platform462bc-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-platform-462/PROPOSAL.md items 1–9 (accepted), with 458, 458b, 463 and 469. Product HEAD 430e469 (462a). The uncommitted files are pinned in hashes.txt: two new (initial_platform.rs and initial_platform_tests.rs) and several modified.

## Summary

- **Producer** `produce_initial_platform(attempt, actor, core)`, in one `attempt.run`:
  - P0: lineage.
  - P1–P3: the accounted process, boot and loader observations.
  - P4: `machine()` must equal `core.platform()`; a translated process refuses.
  - P5: the loader filesystem.
  - P6: the profile files through new `InitialCore::open_release_file` (a tree-root dup, judging root, `platform/` and the file under core-tree custody), joined to the platform-row tree entries.
  - P7: authentication. A final root that is schema 2 with TR-PROFILE standing active requires the envelope, verified by the V1OrV2 reader with the inventory pin and `core.revoked()`. Otherwise the core-pinned path checks V1 or V2 shape and that the digest equals the pin.
  - P8: H's fstatfs: local, not union, not read-only, type in `installRootFilesystems`.
  - P9: the decision, with no refusals and the platform matching.
  - P10: the premise, only for a V2 set with `install_acl_omission()` and a non-SYNTHETIC standing (outside tests).
  - P11: the policy is recorded; nothing is probed.
  - P12: recheck, and `recheck_actor`.
- **Premise.** `AclOmissionPremise` moved into initial_platform.rs, with owned filesystem names, a private RowCitation, and a private constructor. installation_root.rs only imports it; `premise.lineage` became `lineage()`.
- **Receipt.** `InitialPlatform` is private and non-Clone. It has `qualifies_installation_filesystem` (matching H's native id) and a recheck that re-samples everything.
- **Other changes.** InitialCore hooks (`final_root`, `revoked`, `profile_pin`, `tree_file`, `open_release_file`, `CoreMember::Platform`, a factored-out `recheck_held`). admitted_profiles has `InitialProfile` plus the signed and core-pinned verifiers. The test Spec signs the index-0 root under `opensip.metadata.root.{schema}` (a fix; it was fixed at `.1`) and gains root_schema, profile_pin and tree_files.
- **Inventory70.** v69 plus initial_platform.rs (validator) and initial_platform_tests.rs (test): 723 rows, with the byte-identical helper giving PASS.

## Tests

The security lib is 491/0, with 12 new tests:
- P469 gives BASELINE-ATTESTED with no premise, and 460 then refuses `AncestorAclOmitted{component 0}`.
- PM gives EXACT-MEASURED with a premise whose citation is the live identity. `admits("/")` is true and `/dev` false, and 460 with the premise gets past `/`.
- The negatives listed in the helper report.

Not covered: 460 on a scratch chain (it ran on the real home chain, read-only); a schema-2 root with typed-absent TR-PROFILE; non-apfs or union mount negatives; Linux. One unrelated flaky test (`policy_capture_tests::public_policy_wiring_checks_real_file_and_directory_permissions_and_actor`) failed once and then passed repeatedly.

## Law questions (confirm or raise findings)

1. Evidence B is minted from a V2 set authenticated by the pin alone (schema-1 root). Item 6 does not require the signed path; the lead reads it as intended, because the pin is TR-CORE-signed.
2. The `platform/` directory is judged under core-tree custody, reading 462 item 1.
3. "Writable" H is the mount's not-read-only flag only, with no probe.
4. "Active TR-PROFILE" is schema 2 plus role standing "active".

## Decide

Does the code implement 462 exactly? Is any fact admitted before authentication? Is every call charged? Is the premise only mintable by InitialPlatform and only under its conditions? Is the auth path chosen by the final root alone? Is the recheck complete? Is v70 exactly v69 plus two rows?

**Output format (verifier shape):** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of docs/implementation/m2/initial-platform-inventory-v70-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v70.json, parent (the v69 pin), successorRecord (the pin of initial-platform-inventory-v70/successor.json)}.

Replay the security lib (twice), the workspace, clippy and fmt. Write REVIEW.md and review.json. Do not commit.
