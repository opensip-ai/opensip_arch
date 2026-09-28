Grok review: 468b, the durable write gate after creation, and inventory v75. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root-gate468b-r1.

Law: `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md` r5 (accepted), items 1 to 6.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-468b`, based on f482f98. Its diff, including the two new files, is saved as product.diff in your output directory.
- **Arch:** `repository-file-inventory.v75.json`, `existing-root-gate-inventory-v75-subject.json`, and `existing-root-gate-inventory-v75/`, which holds `successor.json`, the projection verifier and `evidence/verify_scratch.py`.

## What it does

- **`DurableBarrierQualification`:** a sealed capability that only `InitialPlatform` implements. It lends `barrier_policy`, `is_home_filesystem` and `omission_premise`, and nothing else.
- **`DurableWriteGate`:**
  - One gate per process, with one ledger at the owner's caps. Every outcome latches it.
  - `admit(&mut self, &impl DurableBarrierQualification)` accepts no creator value, and a test pins that signature.
- **Step 0.** The account is checked with the 464 predicate. Then the creator's charged 460 walk runs:
  - The premise applies only to the root-to-H prefix, `Library` and `Application Support`, through its own fstatfs.
  - `OpenSIP` and I must be private.
  - I is opened through the retained `OpenSIP` handle.
  - H, `OpenSIP` and I must be on H's filesystem.
- **Step 1.**
  - `lifecycle.fence` is opened no-follow through the retained I handle, judged private and checked by name.
  - One nonblocking exclusive lock is taken on that descriptor. `NativeInstallationFence::try_acquire` is never called.
  - Busy returns `Busy` and latches.
- **Step 2, the recheck set.**
  - The account.
  - Every retained name and component judgment, under the same premise.
  - `OpenSIP` is private, and I is reopened by identity.
  - I is private, and the filesystem checks run again.
  - The fence file by identity, link count, type and name.
  - The required files (fence, registry, pair, marker, node chain, `state.v1`), with the pair, marker and nodes decoded to find each next file.
- **Steps 3 to 5.**
  - Run as one effect that reserves both barriers, plus step 5 at twice step 2's measured cost, before either barrier runs.
  - A failed barrier is a value: step 5 still runs, and step 4 is skipped after a failed step 3.
  - Receipts are checked against their handles.
- **Result.** `DurableInstallation` holds the lock, the chain, the files and both barrier kinds.
- **Refusals.** `Busy`, `Account`, `Absent`, `Custody`, `Filesystem`, `Io`, `Budget` and `Incomplete` are one item 6 row each. The public mapping is 468c.
- **Other product edits.**
  - `admit_account` becomes `pub(crate)`.
  - `create_at` is visible to sibling tests.
  - custody.rs gains the module wiring.
- **Inventory v75.** 733 files. It adds `installation_admission.rs` (service) and its tests. Inheritance is re-projected to 8 rows: the 5 existing rows plus the three 468a description overrides.

## Tests and checks

There are 11 gate tests on scratch chains with real charges:
- the success path and busy;
- recheck refusals before and after the barriers, and a replaced file;
- failed barriers, short ledgers, and one gate per process;
- premise absent refuses at `/`, and premise present admits;
- an `OpenSIP` or I with an omitted ACL refuses even with a premise;
- a deep home (about 56 components) costs 2,019 objects, 39,506 edges and 4.3 MB, under half of each cap.

Results:
- Workspace: 1086/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v75 selected.
- The real `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does the code implement law 468 r5 items 2 to 6 exactly, including the premise scope, step order, recheck set, reservation, latching and receipt checks?
- Can a creator value, or the ordinary fence's uncharged acquire, reach the gate?
- Are the tests honest?
- Are the v75 rows and the inheritance projection right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of existing-root-gate-inventory-v75-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v75.json, parent (the v74 pin), successorRecord (the pin of existing-root-gate-inventory-v75/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
