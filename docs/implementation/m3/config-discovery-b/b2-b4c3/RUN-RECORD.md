# B2-b4c3: the blind receipt refresh, run record (post-run review)

**Lead record, 2026-10-16. Unreviewed: for Codex's post-run review.** The pre-run gate was accepted with `runAuthorized: true` (`codex-b2b4c3-prerun`). `evidence/run_b2b4c3_blind.py` ran once, under the lane lock at nice 10 with a private TMPDIR, in the clean detached worktree `opensip-b2b4c3` at product main `15a8ac0a82bd81bd04d24190ba90539e2a5bd582`.

## The run

- **The tool** was asserted equal to the reviewed bytes (`6ea8a1ab…`). The stale receipt was removed in the worktree only.
- **The blind mode** exited 0 and printed exactly: `Blind held-out census: 10 entries, 10 measured, 10 passing, 0 errors.`. Stderr was empty.
- **The ordinary mode:** `--write` exited 0, and `--check` exited 0.

## The comparison (`evidence/run/run.json`)

| Item | Result |
| --- | --- |
| Receipt rows (ids, verdicts, per-mille margins) | equal to the stale receipt's |
| Receipt state | equal: `holds (blind census)` |
| Receipt standing | equal |
| Changed bindings | `reference` only, and within it only the `tools/contracts/generator-closure.json` row |
| The regenerated census record | byte-identical to main's committed `discovery_census.json` |

**So the product change is the receipt file alone** (`product-map.json`). The held-out margin is restored on current bytes: all ten held-out entries are measured and pass the 2× margin, with the same per-mille margins as B2-b4c2. The census `--check` passes again.

**The lead saw** the summary line, the exit codes, and the receipt (ids, verdicts and margins only), as the owner decision allows. No held-out store was opened outside the reviewed blind mode.

## Next

The lead's assent, then a product commit of the receipt. Inventory is unchanged. Then the B3-b plan r2.
