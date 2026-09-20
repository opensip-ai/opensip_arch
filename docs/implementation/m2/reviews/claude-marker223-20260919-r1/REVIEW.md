# Independent review — frozen checkpoint 223 (marker read-bound rows and complete freeze)

Reviewer: Claude (independent; root/Codex is implementation and decision owner). Date 2026-09-19.
Scope: only the frozen 223 bytes — closure of my 221 **E-1** and **T-1**. No cumulative, host, OS, target, release or inventory approval. No frozen/selected/product edit, install, commit, push or delegation; no deletions (fresh, uniquely named scratch dirs asserted absent).

## 1. Identity (recomputed)
| Item | Value |
|---|---|
| `subject.tar.xz` | SHA-256 `482759b7ffedbadff3eb0ad641ad27ad230cd8ff89828e426c594de1279751e2`, 4,099,076 bytes — equals request and pin |
| members | 384; each hashed **from the tar before extraction**; 0 non-regular, unsafe, mismatched or extra; end pass `re-verified` |
| product pins | 356 rows; **356 present**, 0 bad, 0 unpinned files on disk |
| exact parents | `parent221` and `parent220` manifest/pin hashes equal those of **my own verified 221 and 220 extractions**; the retained 221 archive on disk still has its original hash (not rewritten) |
| change vs my 221 bytes | exactly one file: `crates/storage/src/store_root.rs` → `11f04d2c…c36c3`; `author-final.patch` applied to my 221 bytes reproduces it |
| fixtures | 0 mismatches |

## 2. Closure of 221 E-1 — **closed**
Independently of the extraction, I read the product members straight from the tar: the set of `product/` members equals the 356-row pin set **exactly**, with every size and hash equal (`tarEqualsPinsExactly: true`). `tools/typescript-boundary/tests/fixtures/product/design-lock.json` is present and its bytes equal my verified 220 bytes.
The cause is fixed, not patched around: `freeze_marker223.py` now builds the product member list **from the verified pin rows** (no directory walk can prune it), walks evidence separately with exact-path exclusions (`product`, `mutation-check-r1/product`, `mutation-check-r1/target`) rather than a basename test, asserts product-membership equality before writing and again from the written tar, re-hashes each pin from tar bytes, and cross-checks the previously missing file against the 220 archive. The self-check no longer shares the generator's walk — the defect class in my 221 note. 221 stays as it was, incomplete archive included.

## 3. Closure of 221 T-1 — **closed**
Source diff vs 221 is 13 added test lines in `marker_policy_composes_actor_groups_parent_file_and_decode_causes`: valid marker JSON space-padded to 73, 127 and 128 bytes must reach `Marker(NonCanonical)` through `observe_marker`; the existing 129-byte row stays `Capture(Read(_))`. Everything before `#[cfg(test)] mod tests {` is byte-identical to 221 (checked).
My 221 harness re-run with only paths, the frozen hash and two added mutants changed (`diffs/harness.221-223.diff`), judged by the **owner's** tests:
| Mutant | 221 | 223 |
|---|---|---|
| m2 capture limit 127 | survived | **killed** (line 603, new loop) |
| m3 capture limit 72 | survived | **killed** (603) |
| m9 limit 100 (new) | — | killed |
| m10 limit 129 (new) | — | killed (611: 129 bytes now reach the decoder) |
| m4 limit 71; m1, m6, m7, m8 | killed | killed |
| m5 bytes from a second capture | survived | survived — the disclosed structural limit (221 T-2), not reopened |
The rows pin the bound from both sides: any limit ≤71 loses `Present`, 72–127 fails a padded row, ≥129 turns the 129 row into a decoder cause. The composition's bound is now fixed at exactly 128 independent of the constant. Owner's two mutants compile and die at the same semantic line; baseline hash equals the frozen source. cfg-separation probe unchanged (`E0425`). 0 compile failures counted as kills.

## 4. Owner re-runs (fresh scratch, archive bytes, `--offline --locked`, dedicated target)
storage 94/94; workspace clippy `--all-targets -D warnings` clean; `store_root` tests with HOME and TMPDIR unset 7/7. Owner logs and mine: 0 files containing home or per-user temp paths.

## 5. Scope statements checked
Host isolation 133 is **not** carried in this archive and is not relabelled; its 221 qualification does not extend to 223, and for a test-only change I agree no rerun is needed for this scope. README's restatement of the busy-ancestor `ChangedDuringRead` result (fail-closed, single attempt, future host policy, never absence/corruption) matches what I measured in 221 (`p7`). No production, schema, dependency or inventory change.

## 6. Findings
None.

## 7. Limits
macOS only. I did not re-run my 221 probe modules (production prefix is byte-identical, so their results carry by identity, not by re-execution). Full-workspace tests and host isolation not run. Inventory v52 not reviewed.

## 8. Verdict (bounded)
**221 E-1 and T-1 are closed; no finding in the frozen 223 bytes.** Scope only; nothing cumulative is approved.
