# D-037 turn 2 — consume file 11 via D-001 routes

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Restates file 08's only-checklist
> rule, file 07/10 competing-list disclaimers, file 11's header, and
> D-001 A/B/C. Adds no fourth route.
> **Supersedes:** CONTESTED D-017 and the unadopted D-025 draft only.
> D-025 has no register entry and is not CONTESTED. D-028, D-029,
> and D-030 from that cycle are ADOPTED and are not superseded.

Turn-1 subject `coordinator-decisions.D-037.draft.md`
`fa793c9d21367e58f28babe9fba105f26f429e71736c9c9cd44c7b18f73b514f`.

Turn-1 verdicts:

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `coordinator-decisions.D-037.review-adversarial.claude2.json` | `e95d1723ed91448dc7fee87f69337ffca85508f6959cc583f5e336f09634ca4a` | OBJECTIONS, 0 MUST-FIX, 2 SHOULD-FIX |
| Codex | `coordinator-decisions.D-037.review-adversarial.codex.json` | `b7e0cc250692b479ef13318d071b96fb61d0b152da6f307ae68ecc4387dd9069` | CONSENT, 0 MUST-FIX, 0 SHOULD-FIX, 1 NOTE |

Claude 2 turn-1 findings, both accepted into these bytes:

| ID | Sev | Disposition |
|---|---|---|
| C2-D037-01 | SHOULD-FIX | ACCEPTED. Header no longer calls D-025 CONTESTED. |
| C2-D037-02 | SHOULD-FIX | ACCEPTED. Clause 6 restores the historical-item and no-checklist sentences. |

Codex NOTE-D037-01 is an adoption-time recording instruction, not a
subject change.

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |
| file 07 | `d3e95060fa81410ae6cd6dc40107d66134fae512db171349dbcba8ea80073a7e` |
| file 10 | `5378cdbab2d7063fb485bea4b9f7133a92698566e3ec3bdae1e03da415298d18` |
| file 11 | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `COORDINATOR-DECISIONS.md` | `54d34099b33313ef3d9383123a59b962d90fd95bfdfb96c994aac0670da810a4` |

If a cited file moves, re-measure. Pins support: file 07/10
competing-list disclaimers; file 11 header; D-001 §3 routes, MF-6,
definition of done.

## Decision

1. File 11 has no authority. File 08 wins on workflow; V1 on
   meaning; D-001 on done.
2. "Complete 08 then turn to 11" is not a lawful sequence.
3. File 11 items become live work only via D-001 A, B, or C.
   Route C recording forms this corpus has used include, but are
   not limited to: product packet; user-made coordinator-register
   record; D-000 on-behalf entry. New forms still need authority
   from the product-disposition process, D-000, or the user.
   File-08 amendments are not a fourth route. Per MF-6, any
   file-08 content change still needs its own D-000-reviewed
   entry. A product act is not a substitute for that review.
4. Scheduling (D-036) authorizes drafting only, not live work.
5. D-001 is not amended. No wholesale gap import. File 11
   placement not decided.
6. After an item becomes live work, file 11 is historical for
   that item, not a queue. This entry creates no execution
   checklist.

## Alternatives

- Treat 11 as a second checklist. Rejected.
- Closed three-form Route C set. Rejected (D-025 defect).
- Product packet substitutes for MF-6. Rejected.
- Call the unadopted D-025 draft CONTESTED. Rejected: no such
  register record exists; CONTESTED is a closed status word.

## Readiness effect

Zero.

## Reversibility

**Class:** total. Overturn: C-D037. If D-036's scheduling citation
of this rule exists, that citation is independent (D-036 already
states the rule in full).
