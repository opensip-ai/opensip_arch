# Review request: D3A-1-r2 (the supervisor's state machine, loop, joins, normal end and fault ladder; M3-D r5 items 12-15, 17 and 19's normal end), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-1-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 17479 bytes, SHA-256 `b6d4c56ef9f62468e2f1d24ca7b70f5de063675fb0286859fae88130fdb6e640`, 74 members. Rehash every member.
- **The candidate base and lane base:** product main `b7538549b727e13013f36d3b7c2e2917e767f3f2`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a1`, detached at `b753854`, holding the exact bytes that `product-map.json` lists (12 files, 3 new).
- **Your round 1:** `codex-d3a-1-r1` (REQUIRED-FINDINGS: D3A1-R1-RF-1 to RF-9, NBO-1), at `/tmp/opensip-implementation/reviews/codex-d3a-1-r1/` and copied under the architecture repository's `docs/implementation/m3/reviews/`. The round-1 package `d3a-1-r1/` is history.

## Authority

As in round 1. In addition, **this round proposes two narrow M3-D content amendments, accepted with the unit**:
- **LD-D3A-18:** a third scratch-retention reason, `root-unreaped`, with no errno, in LD-D3A-17's exact shape (items 12, 20 and 21);
- **LD-D3A-19:** `provider-protocol` includes a component's accepted control `fault` report (item 12's causes; CPC:375).

Judge each as an amendment to the law's text: whether it is narrow, sourced, consistent with items 12, 13, 18, 20, 21 and 22, and correctly aligned in the code. **Accepting the unit accepts both.** A finding against either rejects the unit.

## What to review

`SCOPE.md` opens with a "Round 2" table. Judge each finding's resolution:
1. **RF-1:** the per-turn service quanta for stderr, control and triggers (LD-D3A1-8); the bounded retention (the first control refusal only, later causes kept once each); and the always-ready stderr, sustained control and trigger-storm controls, each on its own thread under a limit.
2. **RF-2:** the clean end's reap ceiling, and its `reap_blocked` control (`unreaped`, `retained {root-unreaped}`, nothing admissible, one settlement).
3. **RF-3:** `wait_ready`'s EINTR retry within the absolute deadline, and the injected always-EINTR control.
4. **RF-4:** the deferred shutdown (after the older frame, and after any outstanding health report), fd3 closed only after the shutdown is written, the deferred T-1 cancel, and the stalled-write and one-byte-write controls.
5. **RF-5:**
   - nothing spawned yields no settlement (`RunError`; `decline` consumes the supervision);
   - `exit` is always present;
   - `Retained(RootUnreaped)` under LD-D3A-18.
6. **RF-6:** D2a's additive `RefusalDetail::HealthNonceMismatch` (families, buffering and bytes unchanged; D2a's suite passing with one new control), the supervisor projecting only that detail to liveness, and the busy, wrong-nonce and sequence-gap controls.
7. **RF-7:** LD-D3A-19 and the control-fault fixture (the cause, fd1's bytes unchanged, protocol process events only).
8. **RF-8:** the independent early death (`exit_independent`) kept first or later, a ladder-caused death never an `unexpected-exit`, and the three controls.
9. **RF-9:** the confirmation before each reap attempt, against the zombie root, and the root-only and missed-member controls.
10. **NBO-1:** the handle's settled flag and late-event count, tested through the public API.
11. **The lane** `evidence/d3a1-r2-checks/` and its attempt history:
    - components 43 → 74 and platform 329 → 331, with equal failure sets;
    - Clippy, rustfmt and the workspace check;
    - the fixture record, the edges, the feature scope, the environment exceptions, operability, the unchanged closure and verify_design;
    - the mutations, round 2's seven among them;
    - r1's `second-settlement-minted` retired as now structurally inapplicable. Judge that reasoning.
12. **No regression** in what round 1 accepted, and the rules: no new mint-census call, no environment read, no `let _ =`, no new dependency.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "amendmentsAccepted": ["LD-D3A-18", "LD-D3A-19"] (only those you accept), "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A1-R2-RF-n` / `D3A1-R2-NBO-n`.
