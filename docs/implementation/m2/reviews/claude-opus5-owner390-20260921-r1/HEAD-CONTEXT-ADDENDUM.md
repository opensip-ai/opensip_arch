# Addendum — stale architecture/product HEAD context fields

Separate note appended after the fact. **`REVIEW.md`, `findings.json`, `hashes.txt` and `evidence/`
are unchanged and remain the report of record.** This addendum is deliberately not listed in that
`hashes.txt`, so the original evidence set stays exactly as signed off. The NEEDS-CHANGES verdict,
RF-1…RF-4 and every finding are unaffected.

## What was wrong

`REVIEW.md` §1 and `findings.json` → `observedHeads` (also `evidence/review-pins.json`) record
`arch: 42b5c52c2` and `product: 526a1867a34d…`.

## What is correct — independently verified, not taken on report

Root states the HEADs at this review were architecture `cd753cc02` and product `cd5af4d`. I checked
this myself rather than accepting it:

| Fact | Evidence |
|---|---|
| arch HEAD is `cd753cc022f34e0bf7fa293dbf8457576327e518` | `git rev-parse HEAD`, committed 2026-09-21T14:29:02-07:00, "Integrate reviewed path mechanism and propose atomic initial root protocol" |
| product HEAD is `cd5af4dbf524b81ac98876029798d569ccdc0052` | `git rev-parse HEAD`, committed 2026-09-21T14:25:22-07:00, "Capture native project paths without relaxing internal name rules" |
| `42b5c52c2` is the **parent** of `cd753cc02` | 2026-09-21T14:08:53-07:00 |
| `526a186` is the **parent** of `cd5af4d` | 2026-09-21T13:01:41-07:00 |
| The 390 trial is tracked at `cd753cc02` and **absent** at `42b5c52c2` | `git ls-tree` at both commits |

So the recorded labels were the parent commits in both repositories.

## Two different causes, worth separating

- **Architecture: sampled live, then went stale during the review.** I did run `git log` in this
  session — at the start, while preparing the runtime30 addendum — and it showed `42b5c52c2` at the
  top. Root committed `cd753cc02` at 14:29:02, i.e. while the review was still in progress, so a
  single early sample was correct when taken and wrong by the time the report was written.
- **Product: carried forward and never re-sampled.** `526a186` came from the previous (389) session.
  In this session I confirmed the tree was clean but did not re-derive HEAD. This is the same
  omission as the earlier runtime30 addendum.

## Why the substance is unaffected

**The reviewed subject bytes are exactly what is committed at `cd753cc02`.** `subject.tar.xz` is
Git-LFS tracked (`filter: lfs`), so `git show` returns the pointer rather than the archive; the
correct comparison is the blob id. `git rev-parse cd753cc02:…/subject.tar.xz` and
`git hash-object` of the working-tree file are both `1dfd3b830b6f0e1d6b98d16f0758b48aab3f007c`, and
`git status` for that path is clean. The archive I verified — 17424 bytes, sha256
`3cbd6b9668c4b27bd4583530139be45b7a58357762c9a1df53e3960faee63ddd`, 17/17 members — is therefore the
committed content, and `subject.json` (`0754ee77…4e73`) matches at that commit directly.

**The 19 declared source pins are insensitive to the product move.** `cd5af4d` changed exactly two
files, `crates/platform/src/filesystem/path_binding.rs` (20526 → 25337 bytes) and
`design-lock.json`. Neither is among the 19 pinned files, so the pin verification recorded in the
review holds identically at `526a186` and at `cd5af4d`. The same applies to the probe's 19 identity
sources, which `cd5af4d` did not touch — the "unchanged selected identity source" conclusion stands
at either HEAD.

## Scope, and a process note

This corrects **context labels only**: no pin, finding, required finding, limit or verdict changes,
and it is not a re-review. Having now made the same class of error twice, for two different reasons,
the durable fix is not "remember to run `git log`" but to bind every claim to content hashes — which
both reports already do — and to sample HEAD at the *end* of a review rather than the beginning,
since the repository can legitimately advance while the review runs.

Addendum author: Claude Opus 5 (1M context). Read-only; no live, frozen, history, product or lock
bytes edited; no commits; no pushes.
