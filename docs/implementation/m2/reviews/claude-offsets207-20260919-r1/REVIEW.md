# Independent review — frozen `retained-offsets-checkpoint-207`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 207 product bytes — closure of my 205 T-1 (reopen-by-name undetected at three outer layers) and N-2 (what the retained `File` is for). Tests and one doc comment only. The owner ran no new host lane (host 127 qualifies 205 pins, not these test sources) and says so. No custody, policy, lease, inventory selection, installation or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `3a188bd0b8ea8e9015f990770f7ec70cba7bd746e8a51b5226e13d19bd2b3e60`, 4,105,628 B = request = `archive-pin.json` |
| Members | 388, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 354/354, none unpinned |
| Parent | equals **my own verified 205 extraction**; three changed: `security/lib.rs` (doc comment), `security/custody.rs` (test), `storage/store_root.rs` (test) |
| Production behaviour | the complete diff is 19 added lines: two test assertions with comments and a three-line `///` on `ObservedOperationalFile::file()`; no non-comment production token changes |

## 2. Owner checks re-run (fresh scratch, offline, locked)
storage 91/91, security 161/161, strict workspace Clippy clean.

## 3. Closure — proved by re-running my 205 harness **verbatim** (paths rewritten only; diffed)
| Mutant (unchanged from 205) | 205 | 207 |
|---|---|---|
| public `observe_bound_operational_file` returns a descriptor reopened by name | survived | **killed** (custody test + marker test) |
| `capture_bound_operational_file` wrapper reopens by name | survived | **killed** (same two) |
| `observe_marker` keeps a reopened descriptor | survived | **killed** (marker test) |
| after-read chain check omitted | killed | killed |
| after-open chain check omitted | killed | killed |
| marker file name drift | killed | killed |

The assertions are at the two sites I proposed (`descriptor.stream_position() == bytes.len()`), each with a comment stating *why* the offset is at EOF ("Bounded capture consumed to EOF to decide that these are complete bytes") — the dependency I asked to have written down. The fixtures used are non-empty (17 and 72 bytes), so offset 0 cannot coincide with `len`.
**205 T-1 closed. 205 N-2 closed**: `file()` now documents "descriptor metadata/policy checks on the object that supplied bytes", that `bytes()` is the evidence, and that reading or seeking the shared-offset handle "does not repeat the capture's checks; a later read is unbracketed".

## 4. The disclosed limit, confirmed
The owner notes that the offset cannot prove against an intentional reopen **plus seek**. Confirmed (`io/limit207.json`): a public-layer mutant that reopens by name and seeks to `bytes.len()` **survives** 161 + 91. This is the right thing to disclose and not something to chase: the oracle targets accidental regression (a refactor that reopens for convenience), not an adversarial implementer, and the only complete oracle remains the inner function's mid-capture hook, which is unchanged. No finding.

## 5. Findings
None. One note: **N-1** the offset property now carries test weight, so a future change to the bounded reader that stops before EOF (e.g. reading exactly `max_bytes` and using a size check instead of the `max+1` probe) would fail these two tests for a reason unrelated to reopening — the in-test comments say so, which is enough.

## 6. Limits
macOS; scratch copies only (`build207-*`, `target207-*`, created after asserting absence), restored from frozen bytes; nothing deleted; no compile failure occurred; build targets excluded from `hashes.txt`. No host-isolation run by me or the owner for these bytes.

## 7. Verdict (bounded)
**207 closes 205 T-1 and N-2: all three reopen-by-name survivors are now killed by the unchanged harness, the documentation states what the descriptor is for, and the stated limit (reopen + seek evades the offset oracle) is real and honestly disclosed. No production behaviour changed.** No approval of policy integration, admission, leases, installation or cumulative readiness.
