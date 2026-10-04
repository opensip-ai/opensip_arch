# S21 r2 — ACCEPT-DESIGN-UNIT

Design-unit re-review of the commit-outcome exception to WS's before-settle rule, contract successor of law M3-J1 r5 (LD-r5-2). Reviewer: Grok. r1 (`reviews/codex2-s21-r1/`, subject `090de59ff7c4281f65d3f0ba2a63b9444d0583c820dc3f01a5c294d47eb72097`) was REQUIRED-FINDINGS with RF-1. This round resolves it.

**Verdict:** ACCEPT-DESIGN-UNIT. No required findings. No non-blocking observations.

**Subject.** `docs/implementation/m3/host-pipeline-j/s21-subject.json`, 1422 bytes, sha256 `5aec0838da6794866bd22a57252b0300c638810d00e9f10db399ce1537ef2515`. Successor `docs/implementation/m3/host-pipeline-j/s21/successor.json`, 6768 bytes, sha256 `df5ab70ac30b86783bf81e8b96ad1c1b4d7c8cd85d3acbc3ebc94f1496e46241`. The other five subject members match the manifest pins. Parents remain WS `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed` (133335 bytes) and WSE `4478ce1a69369cd0b430fd5d3fc695e8372219629b05a08ae6642a845cab794d` (139497 bytes). Product base `6190e66`, read only, 92 contract successors. `tools/verify_design.py` and INV5 at that commit match the r1 pins (`c13d231e…`, 40714 bytes; `28aa0c42…`, 71161 bytes). The lock pin is `8b32ede7c38d4d17a7c5d332637572122fb111cf1b1557fbcfb789c131ee151d`, 505663 bytes.

## RF-1 is resolved

WS:229 and WSE:233 are overridden with the r1 replacement, and each `before` is the parent line:

```text
Per kind: an analysis attempt aborts and leaves no Run; an import discards its
```

```text
Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its
```

The two overrides are byte-identical. Each line still ends "an import discards its". WS:230 and WSE:234 each begin "staged bytes;". WSE:229 stays with S18 (the after-settle line). S21 selects WSE:233.

The assembled cancellation paragraph on each parent states the two exceptions and then "an analysis attempt that the signal aborts leaves no Run". A commit latched after admission stays committed with its `runId` (SL:552-554). An undetermined commit stays the durability row, the attempt admitted, with `DURABILITY.COMMIT_FAILED` and no `runId` (IE:96, IE:1680-1681). Neither is an attempt the signal aborts. The interrupted case still names a Run committed by an earlier step, which is where phase D's committed Run is carried. The per-kind sentence no longer drops that Run.

`PASSAGES.md` still quotes the old sentence in each override's `before` block. The effective paragraphs use the replacement.

## What else moved

The two line-226 overrides, `before` and `after`, are byte-identical to the r1 record, and so are the parents. The standing now names WS:229 and WSE:233. Candidate pins, `PASSAGES.md`, and `reading-report.json` are regenerated for four overrides and base `6190e66`. The reading report gives the per-kind lines to S21 and leaves WSE:227, WSE:229, and WSE:234 with their previous owners (parent or S18). `build_s21.py` and `check_s21.py` build and check the replacement, the free-line claim, the join onto "staged bytes;", and the review path `codex2-s21-r2`. `verify_scratch.py` expects four overrides. README amends LD-1, LD-2, and LD-6, records the r1 rejection, keeps WS:1393, withdraws cross-law item 6, and moves the base to `6190e66`. WS:1393 is unchanged. INV5 stays cross-law item 2.

## Selection at 6190e66

`build_s21.py --check` reported identical bytes. `check_s21.py --rev 6190e66` passed 85 checks. The new text still names only `DURABILITY.COMMIT_FAILED` and `DELIVERY.REQUIRED_FAILED`, fault causes `durability-commit` and `delivery-required`, and exits 4 and 130. The per-kind line adds no code, exit, or class. `verify_scratch.py --rev 6190e66` takes the lock from 92 to 93 contract successors, selects S21, keeps four overrides and no supersession, leaves inventory `repository-file-inventory.v135.json` and 100 inheritance rows, and refuses a later conflicting override of WS:226.

SYN-NS is the 92nd bound successor (`docs/implementation/m3/syntax-e/syn-ns/successor.json`). No bound entry selects WS:226, WS:229, WSE:226, or WSE:233. The only bound entry among lines 226, 229, and 233 on these parents is S18 on WSE:229. S21 selects none of S18's lines.
