Codex review: the C1a implementation plan r5, a lead amendment of the accepted r4 (M3-C items 1, 2, 5 and 6). A **plan review**, round 1 of r5. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-c1a-plan-r5.

**Rules:** read-only; no repository edits, commits, pushes or delegation. You may run `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` in the C1a1 worktree `/Users/sb/code/opensip-ai/opensip-c1a1`; no other product build, test or generator run. Reading, hashing and `git show` / `git diff` are fine. Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store or T2 cache. No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/snapshot-plan-c/c1a-plan-r5-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `3e9d3a96b75ace40662d03a8a90a34e8e2784770b1eb6ef1b9a7e4140ad22517`. It pins `c1a/PLAN-r5.md` and the accepted `c1a/PLAN-r4.md` (your `codex-c1a-plan-r4`, ACCEPT; published at `92eaf1d5`).
- **Bases:** product `808ad6476fb848f84e732ee233a47229370081f4` (clean), architecture `5c92b4f7f2055a841347bcaf758844b7a50b6ba9`.
- **Context, not the subject:** the C1a1 candidate in `/Users/sb/code/opensip-ai/opensip-c1a1`:
  - `crates/security/src/snapshot_source.rs`, `snapshot_walk.rs` and `snapshot_walk_tests.rs`;
  - `tools/security/snapshot_ledger_model.py` and `crates/security/src/snapshot_ledger_vectors.json`.
  
  C1a1 itself is reviewed separately, after this amendment.

## What r5 changes

The "r5 changes" section is the whole amendment. Diff `PLAN-r5.md` against `PLAN-r4.md`.
1. **The finding.** r4's adversarial supremum (the byte cap is twice the maximum charge of any walk within the object and edge caps) evaluates to about 35.5 GiB, about 71 GiB doubled, at the stage envelopes. So r4's own trigger ("returns to the law before any constructor lands") fires.
2. **The reading.** r5 re-reads item 2: "the recipe's charge for item 5's maximum population, with a 2× margin", together with the T2 census margin test extended to bytes. The byte cap becomes the smallest power of two at least twice the larger of item 5's maximum row population's model charge and the largest T2 entry's model charge, lead-readable and held-out (blind). A walk beyond it refuses `WORK.BUDGET_EXHAUSTED`. The supremum is reported only.
3. **The reordering.** `snapshot_profile`, the `work_ledger.rs` change and the census re-pin move from C1a1 to C1a4, landing with the derivation. C1a1 changes no closure file.
4. **What C1a1 delivers:** the charge model, with its soundness control exact on 32 trees, and the oracle cross-check against the 28 accepted automatic discovery walk vectors.

## Decide

1. **Q5.** Is r5's reading of item 2 faithful, or must an M3-C r9 law record state the rule before C1a4? Consider M3-B r6's precedent for discovery's caps.
2. **Soundness of the rule.** Is (a) item 5's maximum row population with (b) the T2 maxima, doubled to a power of two, a lawful "maximum population" derivation? Does the model's charge for (a) cover everything a row costs: the open, the samples, the retained row, the read attempts at 8 GiB and the custody charges C1a2 adds? Is reporting entries over item 5 as such, without margins, right?
3. **The reordering.** Does any earlier finding or invariant break? In particular: r1 RF-4 (the constructor never precedes its cap), the receipt's transitions, and C1a1, C1a2 and C1a3 testing on the discovery profile with no production caller before J2b.
4. **The model as evidence.** Is the model's construction sound for its stated purpose: the census imported unchanged, the snapshot anchors, the dearer-branch captures, and native ≤ predicted on 32 trees? (Its full review comes with C1a1.)
5. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1APLAN-R5-RF-n` / `C1APLAN-R5-NBO-n`.
