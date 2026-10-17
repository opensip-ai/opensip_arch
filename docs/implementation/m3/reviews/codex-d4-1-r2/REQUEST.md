# Review request: D4-1-r2 (`crates/components/src/manifest.rs`, the manifest-class excluded forms; M3-D r5 item 24), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-1-r2/`).

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

- **Manifest:** `docs/implementation/m3/supervisor-d/d4-1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 11,810 bytes, SHA-256 `b37bdf11cbbfbbc57162d8892e15cf8dbe789f57df4892636e1eebab168096bf`, 51 members (the r2 scope, source record with round 1's subject pinned, product map, archived product files, the lane runner, the builder and the lane evidence `evidence/d4-1-checks-r2b/`). Rehash them.
- **Candidate:** worktree `/Users/sb/code/opensip-ai/opensip-d4-1`, detached at product main `2ead5cf1796bb85f363c34fa8ff8fba715462369` (inventory v228). The same three changed paths as round 1.
- **Architecture base:** `d547f2286bdf02745968caf4399bb7eafe7f0f35`.
- **Round 1:** `/tmp/opensip-implementation/reviews/codex-d4-1-r1/` (REQUIRED-FINDINGS: D41-R1-RF-1). Round 1's package `docs/implementation/m3/supervisor-d/d4-1-r1/` is history and unchanged.
- **Main may move while you review.** Read the base with `git show 2ead5cf:<path>`.

## Round 1 disposition (to verify)

| Round 1 item | r2's answer | Where |
| --- | --- | --- |
| D41-R1-RF-1 (exhaustion before work, not only the ledger prefix) | **The wrappers:** every charge, judged comparison and allocation of the module goes through `charge`, `ordered`/`tested` or `reserve`, each recording its site in a `#[cfg(test)]` thread-local operation log; each `Cleared` push records too. **The oracle grammar** (`blocks`): a charge followed by exactly the work it funds, and no work outside a block. **`accounting`**: the oracle's charges equal the independent model's, in order; at every site a one-unit-short scope gives `Budget`, with the ledger prefix and the oracle's blocks both stopping before the site, so no work at or past it. **Policy order checks** have their own oracle and per-site test. **The source-order guard** pins exactly one raw `work.charge`, `Vec::with_capacity` and `.cmp(` (each inside its wrapper) and the three pushes. **Capacity:** both result vectors are exact. **Mutations:** 28 (round 1's 20 re-anchored, plus the named probe-comparison-before-charge counterexample, the policy, EE-1 and duplicate comparisons before their charges, the three allocations before their charges, and the grown vector), all caught by test failures. | `SCOPE.md` "r2 changes"; `manifest.rs`; `manifest_tests.rs`; `evidence/run_d4_1_checks.py`; `evidence/d4-1-checks-r2b/controls.json` |

## What to review

1. **Is RF-1 resolved?** In particular:
   - Is a mutant that computes `slice[mid].borrow().cmp(key)` (here `ordered(...)`) before `compare(work)?` and matches on it afterwards caught?
   - Is allocating an index buffer or result before its refused charge caught?
   - On the unmutated candidate, do the per-site short allowances show no operation at or past the refused site?
2. **No regression** of round 1's accepted logic: the predicates, the order, the projection, the policy and the prices. The only production change is the recording wrappers, with the same comparison results. The `#[cfg(test)]`-only recording adds nothing to other builds.
3. **The lane evidence** (`evidence/d4-1-checks-r2b/`):
   - Components has 73 → 90 passing tests (17 new: round 1's 15, plus the policy oracle and the source guard). The same 54 D3a supervisor fixture-path failures occur on base and candidate.
   - Clippy, the workspace check, the release build, the focused tests, the environment exceptions, the operability source census, the census-closure check and verify_design all pass.
   - 28 of 28 mutations are caught.

   Lane attempt `d4-1-checks-r2` failed only at Clippy, on a stray doc comment, which was fixed and then fully rerun as `r2b`. That attempt is not in the subject.
4. **Rules:** no new mint-census call, no `let _ =`, no environment read, and rustfmt clean.
5. **The integration path:** `/tmp/opensip-implementation/integrate_d4_1_r2.py` (round 2), then the inventory successor `/tmp/opensip-implementation/prepare_d4_1_inventory.py`.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D41-R2-RF-n` / `D41-R2-NBO-n`.
