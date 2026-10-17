# Review request: D4-1-r3 (`crates/components/src/manifest.rs`, the manifest-class excluded forms; M3-D r5 item 24), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-1-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-d4-1`;
  - `python3 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch --implementation /Users/sb/code/opensip-ai/opensip-d4-1`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d4-1-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 12,736 bytes, SHA-256 `fee39eead3461350b4a4bb9e3e1fd59ee228214858cb5c83059cce26bf1dbd8a`, 55 members. They are:
  - the r3 scope, with its "Self-review" section;
  - the source record, pinning rounds 1 and 2's subjects;
  - the product map and the archived product files;
  - the lane runner, the builder, and the lane evidence `evidence/d4-1-checks-r3/`.

  Rehash them.
- **Candidate:** worktree `/Users/sb/code/opensip-ai/opensip-d4-1`, detached at product main `2ead5cf1796bb85f363c34fa8ff8fba715462369`. It has the same three changed paths as before.
- **Architecture base:** `d547f2286bdf02745968caf4399bb7eafe7f0f35`.
- **Prior rounds:** `/tmp/opensip-implementation/reviews/codex-d4-1-r1/` and `-r2/` (both REQUIRED-FINDINGS). Their packages `supervisor-d/d4-1-r1/` and `d4-1-r2/` are history, unchanged.

## Round 2 disposition (to verify; narrow)

| Round 2 item | r3's answer | Where |
| --- | --- | --- |
| D41-R2-RF-1 (observe the boolean predicate's evaluation) | **The lazy predicate:** `tested(predicate: impl FnOnce() -> bool)` records `Compared`, then evaluates the closure, so the predicate runs inside the observed wrapper. **The guard against a precomputed captured boolean:** `rf1_every_predicate_is_evaluated_inside_its_wrapper_after_its_charge` pins all five call sites. Each is exactly a closure over the claim itself, each sits on the line right after its `compare(work)?;`, and each predicate's operands occur exactly once in production. **Mutations:** four are added, one per site: the predicate is precomputed before `compare(work)?` and captured, with `tested(\|\| stored)` still after it (your EE-1 counterexample, and the same pattern at EE-5a's three tests). All are caught by an assertion, not by compilation. The three mutations anchored on `tested` are re-anchored. | `SCOPE.md` "r3 changes"; `manifest.rs` (`tested` and its five calls); `manifest_tests.rs`; `evidence/run_d4_1_checks.py` |

## What to review

1. **Is RF-1 resolved?** Is each predicate's evaluation now inside its observed wrapper and after its charge, and is the stored-result-before-charge pattern caught at every site?
2. **No regression:** round 2's wrappers, oracle, grammar, totals, per-site prefixes, source-order guard, capacity checks and all 28 earlier mutations are retained.
3. **The self-review:** SCOPE's "Self-review" section. Check in particular its stated uncharged bookkeeping:
   - the loop bounds;
   - `slice.is_empty()`;
   - `roots != 1`;
   - `windows(2)`;
   - the analyzer dispatch following (a)'s charged test of the same field.

   Is each correctly outside LD-D4-10's accepted prices, or should one be charged?
4. **The lane evidence** (`evidence/d4-1-checks-r3/`):
   - The components suite has 73 → 91 passing tests (18 new). The same 54 D3a supervisor fixture-path failures occur on base and candidate.
   - Clippy, the workspace check, the release build, the focused tests, the environment exceptions, the operability source census, the census-closure check and verify_design all pass.
   - 32 of 32 mutations are caught.
5. **The integration path:** `/tmp/opensip-implementation/integrate_d4_1_r3.py`, then `prepare_d4_1_inventory.py`.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D41-R3-RF-n` / `D41-R3-NBO-n`.
