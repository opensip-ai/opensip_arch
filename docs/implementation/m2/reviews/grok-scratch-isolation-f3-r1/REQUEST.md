Grok review: F3, which isolates test scratch directories from cross-process churn. Test-support code only. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-scratch-isolation-f3-r1.

**Subject:** the worktree `/Users/sb/code/opensip-ai/opensip-f3`, based on 7e676a9. Four existing files change, so there is no inventory successor. Save `git -C <worktree> diff` as subject.diff and report its sha256. Pins are in hashes.txt. Precedent: F1 at b230250, which used the same style of `settled` setup retry.

## Root cause

The census, `native_current` and `store_endpoint` fixtures sat directly in the shared system temp directory. The supplied-root walkers compare every ancestor's metadata and correctly refuse `Root(Descriptor(ChangedDuringRead))` when an ancestor changes. Concurrent test processes, or any other process, changed that directory. Reproduced: create and remove churn in the temp directory failed the census module 30 out of 30 times.

## Fix

- `test_scratch::temp_dir()` returns a per-process private parent, `<temp>/opensip-test/<pid>-<nanos>` (0700). `acl_scratch` keys off it, and 461a's ancestor horizon still works by identity.
- `test_scratch::settled(test)` re-runs a whole test with fresh fixtures only when the failure contains `ChangedDuringRead`. It allows at most 8 attempts with backoff. Any other failure is immediate, and every assertion stays strict. It wraps the 16 census, 6 current and 6 store_endpoint tests.
- The census visitor-stop loop re-raises a refusal that reached no visitor, so it can be retried rather than masked as a count mismatch.

## Results

- Each module alone, 20 runs: 0 failures.
- Two concurrent full security-library runs, 3 rounds: 640/0 each.
- Full workspace, 5 runs in a row: 1216/0.
- Clippy and fmt are clean.

## Decide

- Does it change test code only?
- Is `settled` narrow enough? Can it mask a real defect or a refusal under test?
- Is the root cause right?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff). Write REVIEW.md and review.json. Do not commit.
