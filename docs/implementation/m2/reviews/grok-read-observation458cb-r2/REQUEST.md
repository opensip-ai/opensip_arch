Grok re-review: 458c-b1 r2 after your r1 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-observation458cb-r2.

Subject: the same worktree `/Users/sb/code/opensip-ai/opensip-458cb` (base 42ffa91), with the updated product.diff in your output directory, and the v78 arch files. Pins are in hashes.txt. v78 and successor.json are byte-identical to r1. The subject, the draft unit and the README changed, and the README now lists the two platform files.

## Change (RF-1)

- **Platform.** Adds `capture_descriptor_acl_observed`, in the shape of `read_bounded_observed`. It charges `descriptor_acl_capture_cost()` first and returns a native capture failure as `Ok(Err(..))`, so the ledger stays open. A budget refusal from its own charge still closes the ledger (the budget row).
- **Gate.** `installation_admission.rs` gains a shared `judge_capture`, also used by `judge_private_file`. The gate keeps the latching capture, and its 11 tests pass unchanged.
- **Session.** `Reader::member` uses the new capture and records `IoFailure::Capture` as a value. Step 4 runs, and the earlier failure stays the cause.
- **New test.** `a_failed_member_capture_still_runs_step_4_and_stays_the_cause` follows your scenario:
  - the registry is missing, which is a finding;
  - the pair's ACL capture is scripted to fail with `Malformed`;
  - `OpenSIP` is set to 0755 at step 4.

  The steps recorded are Fenced, Reads, Recheck, RecheckRefused. The result is `Io(Capture { selection.pair })`, latched, with the fence free.

Results:
- Workspace: 1120/0, on two runs.
- Session: 14/14. Gate: 11/11.
- Clippy and fmt are clean. `check_package_edges` and `verify_scratch` pass.

## Decide

Is RF-1 closed without changing the gate's behavior? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of read-observation-inventory-v78-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v78, parent (the v77 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
