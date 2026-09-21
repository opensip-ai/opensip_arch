# Addendum — stale architecture-HEAD context field

Separate note appended after the fact. **The original `REVIEW.md`, `review.json`, `hashes.txt` and
`evidence/` are unchanged and remain the report of record.** This addendum is deliberately *not*
listed in that `hashes.txt`, so the original evidence set stays exactly as it was signed off. The
ACCEPT-DESIGN-UNIT verdict is unaffected.

## What was wrong

`REVIEW.md` §7 and `review.json` → `observedHeads.arch` (also `evidence/review-pins.json` →
`archHead`) record the architecture HEAD as `55d0f68a2`. That value was carried forward from my
earlier 388 session and was not re-derived when I ran the runtime30/389 review.

## What is correct

At the time of that review the architecture HEAD was **`42b5c52c2`** ("Preserve binding
investigation and freeze raw project path candidate"), the child of `55d0f68a2`. I verified this
independently: `42b5c52c2` is the commit that introduces
`docs/implementation/m2/native-runtime-selection-v30-subject.json`, the v30 unit directory and the
389 trial — i.e. the frozen subject I reviewed could only have existed at `42b5c52c2` or later, so
the recorded `55d0f68a2` is provably the wrong context label.

## Why the verdict is unaffected

Nothing in that review depended on the HEAD label. Every subject and source claim was bound by
**content hash**, not by revision:

- formal subject `21359758b280d44ca094be5f0206d7c0a4af562808092dbb4888021bc557dd3b`, 2521 bytes,
  all 12 members verified by exact bytes and sha256;
- source archive `d5009ba7f4f01f71c912f974f3c52f88fac8b5306606ee54a7a3da1153be2b95` (6894600 bytes)
  and manifest `3e5a26e0ef6c9e5d226b6c038c06bb2bd922d48293833924072575933d792bd8`, 601/601 members
  verified;
- the one changed file, before `82f6db21…` / after `582366ee…`;
- the three parents verified by live hash **and** against the selected `design-lock.json`;
- product HEAD `526a1867a34da023444fd519d5bc8ff5517b7d73`, which was re-derived during that review
  and is correct.

The staging helper additionally re-pins every baseline file and refuses to proceed unless the
product HEAD matches the baseline, so the staged bytes I tested are pinned independently of any
architecture revision I might have recorded.

## Scope of this correction

This corrects a **context label only**. It changes no pin, no finding, no observation, no limit and
no verdict, and it is not a re-review. Root has already qualified the same point in its own assent.

Addendum author: Claude Opus 5 (1M context). Read-only; no live, frozen, history or lock bytes
edited; no commits; no pushes.
