# RF-1 closure review — TypeScript closure unit v2 (409 r2)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Read-only; no native or Node job, no select,
no commits, no pushes, no edit outside this directory. **Bounded to closing RF-1 from my 409 r1
review**; r1's substantive conclusions are inherited, not re-derived.

**Verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`. RF-1 is closed.**

Subject `bdf558ec4e938e8ae3c2b6a1fde88f0e96519253222616288bb8d7dc196b3363`, 2 330 B — unchanged.
Prior review pinned at `d0de43f9c3e877ea8ce72a39894c58f3187ec94b3cdf82d129e6428c9f54509b`, 11 127 B.

## RF-1 closure

r1 required either removal of the stale v1 assent **or** recording its existence and inert status, plus
assurance that the v2 selector writes its own assent path and does not read the v1 one. Root took the
preservation option, which r1 explicitly allowed.

`trials/typescript-closure-materialization-408/inert-assent-disposition.json` (1 201 B,
`4cd4db91f83e8975030e1cf4a528aaea2ee7f3ddb6ae50ae56a83b762885579e`) pins the assent at **2 604 B /
`01cf99e26154e863e4111d37649b968a8b5bbea3f88425af2c34b19c2081d79a`** — byte-identical to the value r1
recorded, so the thing described is the thing that exists. It states the v1 successor is structurally
inadmissible for unsorted parents, that the unit was never selected, that the preserved assent "grants
no authority and must not be reused", and carries `selected: false`, `liveProductModified: false`, the
exact failure string, the replacement subject pin, the replacement assent path, `selectorUsesOldAssent:
false` and `rerunOriginalSelector: false`. That is precisely the gap r1 named: the artefact is now
recorded where a reader of the failed trial will find it.

`select_typescript409.py` matches its pinned digest (**7 249 B / `3e6cbbe007406db9d3c2f64ffd058f2b83d17afd21cdb616122ea924145d8013`**)
and satisfies the second half of the remedy. It never references `typescript-closure-selection-v1-unit`.
Its one v1-path reference is `typescript-closure-selection-v1/materialization-map.json` at line 35 —
a reused v2 candidate at its immutable path, not the assent; I checked that distinction rather than
grepping for "v1" and stopping. It writes its own `typescript-closure-selection-v2-unit.json` under
`assert not assent.exists()`, with `acceptedSuccessor` naming the v2 record. It pins the subject at
2 330 B / `bdf558ec…`, asserts 11 members, and requires an r2 review with verdict
`ACCEPT-DESIGN-UNIT`, `requiredFindings == []` and a matching `subjectManifestSha256`, plus a root
assessment containing both digests. Its private output and trial directory are
`typescript-closure409-selected-product` and `trials/typescript-closure-materialization-409` — distinct
from the 408 targets, and asserted absent before use.

It has not run: both targets and the v2 assent are absent.

## State confirmed unchanged

r1 is preserved byte-for-byte: `REVIEW.md`, `review.json` and `hashes.txt` are archived as loose files
and my four evidence files inside `replay-evidence.tar.xz`, each matching my originals exactly, with
`replay-evidence.json` pinning them. Root's archived `status.json` reads
`ACCEPTED_WITH_ONE_PRESELECTION_FINDING`, `selected: false` — accurate.

Live product `7e1e18b`, clean. Lock still 35 inventory / **55** contract successors with **zero**
`typescript-closure` references. Live registry still `7a4f4459…`, uncorrected. No frozen or product byte
changed.

## Inherited and unchanged from r1

The v2 unit's structural admissibility stands as reviewed: all eleven emulated verifier checks pass,
including the sorted-and-unique parent rule that refused v1; candidate reuse at v1 paths is valid
because v1 was never selected; the corrected registry digest is selected zero times today, so no
double-selection hazard exists; and the product delta remains the single `verify_design.py` row with 159
rows, the Node pin and all three lane records byte-identical.

## Limits

No lane has run and none is claimed to pass; 408 was not selected. Root's private and live
`check_typescript` runs across all three lanes remain a required step after acceptance. This grants no
root assent, no selection, and no lane, checker, toolchain, release or M2 qualification. Bounded
closure review, not whole-project approval.
