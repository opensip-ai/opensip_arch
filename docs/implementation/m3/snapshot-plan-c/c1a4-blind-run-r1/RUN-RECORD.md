# C1a4-blind run r1: the blind validation run (run record, for post-run review)

**Lead record, 2026-10-17. Unreviewed: for Codex's post-run review.**

**The pre-run gate:** C1a4-blind r2 (`codex-c1a4b-r2`): ACCEPT-UNIT, `runAuthorized: true`. Its code is product `3742822e2823c3a7624aca3fea11220a46cffa16`, on the frozen base `b753854`, with main fast-forwarded. The run worktree `opensip-c1a4b` was created detached at that commit.

**The reviewed `run_c1a4_blind.py`** ran once, from its committed architecture path, with the pinned interpreter. It ran in the clean detached run worktree, under the lane lock, at nice 10, with a private 0700 TMPDIR and `PATH=/usr/bin:/bin`. The lead read only the two one-line summaries, the exit codes, the empty stderrs and the receipts (ids, verdicts and per-mille margins).

## The run (`evidence/run/`)

- **The preflight passed before anything was removed:**
  - the pinned post-run checker's bytes (`cc0286b9…2c3`);
  - the freeze: main `3742822` is `b753854` plus exactly the gate commit, whose paths and bytes are the gate's product map's;
  - the detached, clean run worktree of the product repository;
  - the five tools at their reviewed bytes, in the worktree and on main;
  - the five architecture-side inputs at their gate bytes;
  - no companion receipt yet.
- **The stale discovery receipt** was removed, in the worktree only.
- **Discovery's blind mode** exited 0 and printed exactly `Blind held-out census: 10 entries, 10 measured, 10 passing, 0 errors.`. Its stderr was empty.
- **The companion's blind mode** exited 0 and printed exactly `Blind held-out snapshot census: 10 entries, 10 measured, 10 passing, 0 over item 5, 0 errors.`. Its stderr was empty.
- **The ordinary modes:** discovery's census `--write` and `--check`, the workspace ledger `--check`, and the companion census `--write` and `--check` all exited 0.
- **The worktree's changes** are exactly the four expected files:
  - the two receipts, the companion's new;
  - the two census records.

  `run.json`'s `worktreeChanges` shows the first status line as `M ` rather than ` M` only because the run script strips its Git output (B3-b3b recorded the same artifact). All four are unstaged; the post-run checker reads status unstripped.

## The comparison (`evidence/run/run.json`), against RUN-PLAN

| Item | Expected | Result |
| --- | --- | --- |
| Discovery receipt ids | the old receipt's ten, in order | equal |
| Discovery rows | equal to the old receipt's | **equal, every row** |
| Discovery changed bindings | `closure` (2 rows), `reference` (1 row), `tool` | `closure`: `work_ledger.rs` and `discovery_rule.rs`; `reference`: `tools/contracts/generator-closure.json`; `tool`. **Exactly as expected** |
| Discovery unchanged bindings | `limits`, `manifest`, `memberModel`, `rootLengths`, `sizes` | unchanged |
| Discovery census changed keys | `entries`, `heldOutMargin` (plus `failingEntries` and `caps` on a failure) | `entries`, `heldOutMargin` |
| Discovery lead-readable and workspace rows | unchanged | unchanged |
| Discovery receipt state | | `holds (blind census)`; `failingEntries` `[]`; caps `recorded-margin-holds` |
| Companion receipt ids | the ten held-out ids | equal, in order |
| Companion bindings | all seven new | `afterWalk`, `caps`, `discovery`, `item5`, `maxUnitDepth`, `snapshotSources`, `tools`. **As expected** |
| Companion census changed keys | `heldOutEntries`, `heldOutMargin` (plus `failing2x` and `capsStatus` on a failure) | `heldOutEntries`, `heldOutMargin` |
| Companion lead-readable and workspace rows | unchanged | unchanged |
| Companion receipt state | | `holds (blind census)`; `failing2x` `[]`; `capsStatus` `recorded-margin-holds` |

## The result (ids, verdicts and per-mille margins only; the owner's allowlist)

**Every held-out entry is measured** against the snapshot profile's caps: 2^21 objects, 2^24 edges and 2^33 bytes, on the full ledger (walk, session, sealing at its envelope and the leftover copy). **Every entry holds the 2× margin.** None is over item 5.

| Entry | Objects | Edges | Bytes |
| --- | ---: | ---: | ---: |
| rs-small-anyhow | 1,872,457 | 6,545,928 | 964,338 |
| rs-medium-ripgrep | 399,914 | 1,167,110 | 817,207 |
| rs-large-rust-analyzer | 45,551 | 216,471 | 378,599 |
| js-medium-axios | 206,229 | 798,915 | 723,057 |
| ts-large-vitest | 30,818 | 97,821 | 256,036 |
| poly-medium-tauri | 81,980 | 208,456 | 448,312 |
| py-small-httpx | 834,853 | 3,672,770 | 924,494 |
| py-medium-healthchecks | 80,783 | 345,879 | 512,449 |
| py-large-zulip | **12,020** | 65,452 | 144,238 |
| ts-small-zustand | 675,628 | 2,157,563 | 890,444 |

The tightest held-out margin is py-large-zulip's objects, at 12,020‰, six times the 2,000‰ the margin needs. The lead-readable corpus's tightest stays poly-large-rspack's objects, at 3,960‰.

**So every T2 entry within item 5 holds 2× on the snapshot ledger at r9's caps:** the 39 lead-readable entries and workspaces, and the ten held-out entries. C1a plan r6 RF-3 step 4's failure branch does not arise, and the caps stand.

**The discovery receipt is current again.** Its rows are unchanged from B3-b3b's, and the tightest held-out margin is still ts-large-vitest's edges, at 38,712‰.

## Post-run checks (`evidence/post-run-checks/`)

**The pinned checker,** `run_c1a4b_post_checks.py` (`cc0286b9…2c3`), ran from its committed path with the pinned interpreter, in the run worktree, under the lane, at nice 10, with a private TMPDIR. It first asserted that the worktree is the run's: detached at main, main the freeze plus the gate commit, and the changes exactly the four run files. It passed every check (`allPassed`):
- `cargo test -p opensip-security --lib`, over the composed records: the snapshot census margin test and the discovery census tests, 8 passed. The margin test classifies the ten composed companion rows in their closed format, and checks their ids against discovery's compiled record (C1A4-R1-NBO-2);
- the companion's 21 and discovery's 25 blind controls;
- verify_design.

**The independent gate identity** (Codex C1A4B-R2-NBO-1), `verify_c1a4b_gate_identity.py`, archived with its output. It works from the completed run record and the gate's product map alone, not from the run's preflight. It checks that:
- main's and the run worktree's HEAD both equal `run.json`'s `productBase` (`3742822`);
- the worktree is detached;
- HEAD's parent is `b753854`, with exactly one commit between;
- that commit changes exactly the gate's product-map paths, each to its candidate bytes.

All pass.

## Next

1. Codex's post-run review.
2. The lead's assent.
3. A product commit of exactly the four files.
4. The one inventory successor, v222, for the two new paths: the companion receipt and the gate's controls (LD-C1A4B-5).
5. C1b-0 may integrate after that; it makes both receipts stale by its generator-closure change.

## Not claimed

- No held-out content is opened or disclosed beyond the owner's allowlist: ids, verdicts and per-mille margins.
- No second run.
- No qualification. C1a's completion is not claimed: C1b and C1c follow.
