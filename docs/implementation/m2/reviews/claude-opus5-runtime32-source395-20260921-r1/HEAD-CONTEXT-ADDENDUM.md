# Addendum — the runtime32 HEAD context was true at sampling, not at completion

Separate note appended after the fact. **`REVIEW.md`, `review.json`, `hashes.txt` and `evidence/` are
unchanged and remain the report of record.** This addendum is deliberately not listed in that
`hashes.txt`, so the original evidence set stays exactly as signed off. The **ACCEPT-DESIGN-UNIT**
verdict, `requiredFindings: []`, and the RF-1/RF-2/RF-3 closure assessments are unaffected.

## What needs qualifying

Two statements in the original report were derived from a HEAD sample taken at **15:30:36**, and the
report was completed at about **15:34**. In that window root committed. The statements are therefore
true *as of sampling* and stale *as of completion*:

| Where | Original wording | Status |
|---|---|---|
| `REVIEW.md` §8 | "The architecture repository did not advance during this review" | true at 15:30:36, **not true at completion** |
| `REVIEW.md` §6 O-F, `review.json` `observedHeads.v32ArtefactsCommittedAtHead: false` and `untrackedNote` | the v32 subject, its successor and the 395 trial are "untracked at arch HEAD `613d3c7a8`" | true at 15:30:36, **not true at completion** |

## What is correct — independently verified, not taken on report

| Fact | Evidence |
|---|---|
| arch HEAD is now `39015a98da560145e89d301ee977ef3727d9eb50` | `git rev-parse HEAD` |
| its commit time is **2026-09-21T15:32:06-07:00** | `git log -1 --format=%cI` — root's message said 15:31; the recorded time is 15:32:06 |
| its subject is "Clarify initial read and write admission and correct directory barrier candidate" | `git log -1 --format=%s` |
| `613d3c7a8` is its parent | `git log` |
| all four v32/395 artefacts are now **tracked and committed** | `git status --porcelain` clean for those paths |

## The pins are unchanged — which is the point

Every byte I verified is exactly what is now committed. Committed blob id equals worktree blob id for
all four paths, and each sha256 still equals the value recorded in the original report:

| Path | sha256 | blob match |
|---|---|---|
| `…/native-runtime-selection-v32-subject.json` | `1de2e8016adb9bc87737b514f5e0c98dc01e6d9c31f6758a0441f8901852e7e5` | ✓ |
| `…/native-runtime-selection-v32/successor.json` | `15089a49ac02f58eecd0f44a6a3f21cc67024903273177ff94f25ba707ffa293` | ✓ |
| `…/trials/directory-barrier-checkpoint-395/subject.json` | `231adcb36f455b82a96e78cb50530103ee9401d6cd2b5e7fd6508c76753aae16` | ✓ |
| `…/trials/directory-barrier-checkpoint-395/subject.tar.xz` | `70cc98839c68977d381c31298a305e7d645f65f85beb1286f0753c4f199c67cd` | ✓ |

So freezing on disk and committing produced no byte change, and the acceptance attaches to the same
content either way.

## Why the substance is unaffected

The original report already said so in as many words: *"root may commit during the review, so the byte
pins verified here — not the HEAD label — are the authority"* (`review.json` `untrackedNote`, and
§6 O-F). Every verified fact in the review — 12/12 formal members, 607/607 archive members, the
589/2 product delta, the byte-identical `confirm_directory_with`, the 115-test count, the replays, the
rustdoc pass and probes R1–R6 — is bound to content hashes, none of which moved.

## Scope, and the process note

This corrects **context labels only**: no pin, finding, limit or verdict changes, and it is not a
re-review. The end-of-review sampling policy did what it was meant to do — it is only the *claims about
the repository's motion* that a single sample cannot support, because the repository can advance
between the last sample and the last written word. The durable fix is to keep binding every claim to
content hashes (which both this report and its predecessors do) and to phrase HEAD observations as
"as of <timestamp>" rather than as statements about a whole interval. I will write them that way from
here on.

Addendum author: Claude Opus 5 (1M context). Read-only; no live, frozen, history, product or lock
bytes edited; no pin edited; no commits; no pushes.
