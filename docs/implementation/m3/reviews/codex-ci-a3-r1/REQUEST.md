# Review request: CI-A3 r1 (the launch member, a pinned entrypoint recheck; amendment to the component installation law r5), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-a3-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries. Reading the CI-2/CI-3 worktree `/Users/sb/code/opensip-ai/opensip-ci2` read-only is permitted.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-a3-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 862 bytes, SHA-256 `f0c7307625b1496ee6e3be1695b89e86c48ae82af186486795488eaea79ff999`. It has 3 members:
  - `CI-A3-r1.md`, the subject;
  - `PROPOSAL-r5.md`, context: the law amended;
  - `ci-2-r1/SCOPE.md`, context: CI-A2 as proposed and not yet reviewed. That file belongs to the in-flight CI-2/CI-3 package and may change after this manifest. Judge CI-A3 against the hashed bytes.
- Rehash them.
- **Bases:** product main `d704ed4`; architecture `9415426c053c8e2b287022f5db4dd380024d120a`.

## Authority

- **The law:** component release installation and tree custody, r5 with CI-A1 (`docs/implementation/m3/component-install/PROPOSAL.md`, `PROPOSAL-r5.md`), items 4 to 9, and its plan r3 (`PLAN-r3.md`, CI-A1).
- **What asked for CI-A3:** `codex-d4-plan-r1` Q7, at `/tmp/opensip-implementation/reviews/codex-d4-plan-r1/review.json`. It reads: "CI-A3 must define the entrypoint resolution, retained lifetime/path binding, exact prices and typed failures. The launch path, rechecked member identity and selected entrypoint must be joined, and the pin must remain alive through spawn." See also D4 plan r2's X-D4P-2 (`supervisor-d/d4/PLAN-r2.md`, not under review here).
- **The consumers and sources:** M3-D r5 items 2 and 26 (`supervisor-d/PROPOSAL-r5.md`:204-222, :852-878); D1a's `LaunchSpec`, `ClosureRecheck` and `VerifiedLaunch` (`crates/platform/src/process.rs` at `d704ed4`); the security owner's entrypoint resolution (`crates/security/src/component_manifest.rs`:313-379 at `d704ed4`); CI-3's in-flight capability (`opensip-ci2/crates/lifecycle/src/retained_tree.rs`), read-only.

## What to review

1. **Coverage of Q7's requirements:** the entrypoint resolution, the retained lifetime, the path binding, exact prices and typed failures; the launch path, member identity and entrypoint joined; the pin held through spawn.
2. **Each amendment part (CI-A3-a to CI-A3-f):** is the quoted current text exact, and is each replacement or insertion coherent with the rest of LAW, CI-A1 and CI-A2 as proposed?
3. **Soundness of the path binding and the stated residual** under item 5's custody limits.
4. **`B_launch`:** complete, conservative and in item 4's shorthands, with nothing unpriced.
5. **`Binding`:** routed only through existing codes, with no other route changed.
6. **The ordering against the in-flight CI-2/CI-3 unit** (the "Interaction" section) and the CI-3L unit.
7. Answer CI-A3's Q1 to Q6 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `CIA3-R1-RF-n` / `CIA3-R1-NBO-n`.
