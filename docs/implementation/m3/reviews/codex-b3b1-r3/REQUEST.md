# Review request: B3-B1-r3 (X2 r9 item 6b, the member observation; M3-B unit B3-b, sub-unit B3-b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b1-r3/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; `python3 -I -B tools/check_operability.py source --repository <tree>` in the candidate worktree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b1-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7046 bytes, SHA-256 `d05f8074d7b909d5f3f1069104e7aca1e912cbcd99a3818157b09043b964f4dd`, 30 members. Rehash every member.
- **Bases:** product main `25972e1`, clean (168 contract successors, inventory v202); architecture `9e90c68c4e86999758c39511983da3042da16697` (round 2's request named `67b8f8b…` in error; you found the right one).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b1` (detached at the product base). It holds the exact bytes `product-map.json` lists.

## Authority

As in round 2:
- law M3-B r9 item 21 (X2 r9; successor S1, accepted), with items 8, 19 (M1, M2), 23 and 24 (`config-discovery-b/PROPOSAL-r9.md`);
- the B3-b plan r2, section 2;
- item 6a as built at the product base.

## Round 3

Your `codex-b3b1-r2` raised B3B1-R2-RF-1 (`covers` bound pathname labels, not the retained root) and NBO-1 (the custody mutation bypassed the fault injector). `SCOPE.md`'s "r3 changes" table resolves them:
- `RootObservation<'a>` and `observe_root` bind item 6a's observation to the `&ProjectChain` it walked.
- `NoRepository<'a>` is that chain. `MemberInputs` has no chain, and `observe_members` derives W from the proof.
- `covers`, `TrackingObservation::no_repository` and `precondition-root-mismatch` are removed.
- The cross-spelling control is kept, and a same-spelling, different-retained-root control is added.
- A new mutation, `capture-refusal-latches`.

The SCOPE also corrects the evidence-path naming of rounds 1 and 2 (the lanes are `evidence/b3b1-checks-rN/`).

**Judge first** whether RF-1 is resolved:
1. Can any caller still pair a proof with a root other than the one item 6a walked?
2. Is item 6a (`observe_tracking`, `recheck_tracking`, `TrackingObservation` and their callers) unchanged?

Then confirm that round 2's accepted resolutions (R1-RF-1 and R1-NBO-1) still hold, and re-check the controls and evidence:
- lane r3, `evidence/b3b1-checks-r3/`: the security suite with equal failure sets and eleven new passing tests; Clippy; the census check; the mutations;
- the two substitution controls;
- `capture-refusal-latches`.

Is r2's `root-binding-skipped` rightly retired?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B1-R3-RF-n` / `B3B1-R3-NBO-n`.
