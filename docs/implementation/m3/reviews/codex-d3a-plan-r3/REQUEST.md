# Review request: D3A-PLAN-r3 (the supervisor plan, M3-D items 12-17 and 20-22), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 752 bytes, SHA-256 `1e6681d3782b91855c59068253550c79c793054238d3e929013e99f2e8422b45`, 3 members: `d3a/PLAN-r3.md` (the subject), and `d3a/PLAN-r2.md` and `d3a/PLAN-r1.md` (history, unchanged). Rehash all three.
- **Bases:** as the manifest names.
- **Your round 2:** `codex-d3a-plan-r2` (REQUIRED-FINDINGS: D3APLAN-R2-RF-1, NBO-1, NBO-2), at `/tmp/opensip-implementation/reviews/codex-d3a-plan-r2/`.

## Authority

As in rounds 1 and 2. In addition, **this round proposes one narrow M3-D content amendment, LD-D3A-17**, for acceptance with the plan. It covers items 12, 20 and 21's scratch-retention text: `retained {reason: io-failure(errno) | work-exhausted}`, and the `supervision.scratch.retained` event's required `reason` field. Judge it as an amendment to the law's text: whether it is narrow, sourced, consistent with items 12, 20 and 21 and S-OP-2 item 23, and correctly gated. Accepting the plan accepts the amendment. A verdict of REQUIRED-FINDINGS against the amendment rejects both.

## What to review

`PLAN-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1's resolution:**
   - LD-D3A-17, and its alignment through LD-D3A-10 and LD-D3A-12 and §3: the settlement type, the event descriptor and `errno`'s presence rule, the C-2 required-field check, and the exhaustion controls;
   - that no errno is manufactured;
   - that cleanup never changes admission;
   - that the `work-exhausted` code waits for the amendment's acceptance.
2. **R2-NBO-1:** the fixture path is bound to this build. A `supervisor_fixture.path` file is written beside the test binary (`std::env::current_exe()`), naming the artifact built in the same invocation, with no environment variable read. The harness-free target has a harmless standalone entry.
3. **R2-NBO-2:** D3-T3 and its mutation are qualified. Killable and removable fixtures keep the absolute assertion. Ceiling and exhaustion fixtures assert finite settlement and the right disclosure, with no later signal or blocking reap.
4. **No regression** in what rounds 1 and 2 accepted or did not find.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3APLAN-R3-RF-n` / `D3APLAN-R3-NBO-n`.
