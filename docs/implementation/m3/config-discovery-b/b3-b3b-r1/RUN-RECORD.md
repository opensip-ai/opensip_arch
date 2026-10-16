# B3-b3b r1: the blind held-out run over the full ledger (run record, for post-run review)

**Lead record, 2026-10-17. Unreviewed: for Codex's post-run review.**

The pre-run gate was B3-b3a2 r1 (`codex-b3b3a2-r1`): ACCEPT-UNIT, `runAuthorized: true`. Its code is product `ffd2c8e740177a33d6fdba04dc551465f863cb27`, with main fast-forwarded and no lock or inventory change; its record is architecture `f27444260`. The reviewed `run_b3b3b_blind.py`, at its committed architecture path, ran once:
- in the clean detached worktree `opensip-b3b3b` at product main `ffd2c8e`;
- under the lane lock, at nice 10, with a private 0700 TMPDIR.

## The run (`evidence/run/`)

- **The tool and the member model** were asserted, in the worktree and on main, equal to the reviewed bytes (`6e52bd5b…99c6`, `582bad12…21f1`).
- **The stale walker-only receipt** was removed, in the worktree only.
- **The blind mode** exited 0 and printed exactly: `Blind held-out census: 10 entries, 10 measured, 10 passing, 0 errors.`. Stderr was empty.
- **The ordinary mode:** `--write` exited 0, then `--check` exited 0.
- **The worktree's changes** are exactly the receipt and the census record. `run.json`'s first `worktreeChanges` line reads `M ` rather than ` M` only because the script strips its Git output; both files are unstaged modifications.

## The comparison (`evidence/run/run.json`)

| Item | Expected (RUN-PLAN) | Result |
| --- | --- | --- |
| Receipt ids | the old receipt's | equal (the ten held-out ids, same order) |
| Receipt state | | `holds (blind census)` |
| Each margin at or below the walker-only one | everywhere | true for all ten |
| Changed bindings | `tool`, `closure`, `memberModel` | `tool`, `closure`, `memberModel` **and `sizes`** |
| Changed census keys | `entries`, `heldOutMargin` (plus `failingEntries` and `caps` on a failure) | `entries`, `heldOutMargin` |
| Lead-readable rows, workspace rows | unchanged | unchanged |
| `failingEntries`, `caps` | | `[]`, `recorded-margin-holds` |

**One expectation in RUN-PLAN was incomplete: `sizes`.** The old receipt was written by B2-b4c3, before B3-b3a1. B3-b3a1 added `DescriptorMetadata` (80) and `(Vec<u8>, DescriptorMetadata)` (104) to the size inventory, so the bound `sizes` changed with the closure. The binding is current against today's bytes, which the ordinary `--check` confirms. The run itself is unaffected; only the stated expectation missed this.

## The result (ids, verdicts and per-mille margins only; the owner's allowlist)

Every held-out entry is measured and holds the 2× margin on the full ledger: the walker plus the D15 reader, member and descent terms. The walker-only column is from the B2-b4c receipt.

| Entry | Objects | Edges | Bytes (R = 4,096) | Lowest, walker-only |
| --- | ---: | ---: | ---: | ---: |
| rs-small-anyhow | 8,943,078 | 2,692,107 | 7,573,241 | 2,709,498 |
| rs-medium-ripgrep | 1,607,013 | 403,608 | 1,265,616 | 451,000 |
| rs-large-rust-analyzer | 242,081 | 91,855 | 212,995 | 94,105 |
| js-medium-axios | 979,977 | 421,962 | 927,545 | 460,103 |
| ts-large-vitest | 131,285 | **38,712** | 108,487 | 39,008 |
| poly-medium-tauri | 300,000 | 86,896 | 246,456 | 89,944 |
| py-small-httpx | 4,378,187 | 4,185,932 | 5,179,876 | 4,228,129 |
| py-medium-healthchecks | 401,445 | 373,624 | 460,438 | 373,957 |
| py-large-zulip | 68,010 | 66,474 | 73,050 | 67,354 |
| ts-small-zustand | 2,931,030 | 923,855 | 2,427,819 | 1,128,714 |

The tightest held-out margin is ts-large-vitest's edges, at 38,712‰ (walker-only 39,008‰). The largest relative drop is ts-small-zustand's bytes, at 21.1%.

**With B3-b3a1's lead-readable rows, every T2 repository entry now holds 2× on the full ledger.** The tightest of the whole corpus is still rs-very-large-aws-sdk-rust, at 2,080‰ edges.

## Post-run checks (`evidence/post-run-checks/`, run worktree, lane lock, nice 10, private TMPDIR)

- `cargo test -p opensip-security --lib -- discovery_census`: 6 passed. These include the margin control, which classifies the ten composed blind rows in their closed format.
- verify_design: passed.
- The 25 blind-receipt controls: passed.

## The record's history, for status r102

- Main's committed census record showed `heldOutMargin: holds (blind census)` from B2-b4c2 (`c0bbdc8`). B2-b4c3 (`2b297e6`) refreshed only the receipt.
- From B3-b2a (`58d450c`, the census closure re-pin), main's committed record has shown `outstanding`. The held-out rows read `outstanding: held-out (blind receipt stale)`, as amendment A1 states, through B3-b3a2.
- This run restores a current held-out margin, now on the full ledger.

Status r101's statement about the held-out margin was already owed a correction (B2-b4c3's `RUN-PLAN.md`, "What went wrong"). r102 corrects it with this history.

## Next

1. Codex's post-run review.
2. The lead's assent.
3. A product commit of exactly the receipt and the census record, with no inventory successor, since both paths exist.
4. B3-b3c, the workspace margins.

## Not claimed

- No held-out content is opened or disclosed beyond the owner's allowlist: ids, verdicts and per-mille margins.
- No second run.
- No workspace full-ledger margin (B3-b3c).
- No qualification.
- No completion of B3-b or M3-B.
