# Adoption receipt: C1c plan r4 addendum guard-charge (LD-C1C-7A), 2026-10-29

**Decision LD-COORD-L5 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1.**

The addendum `ADDENDUM-guard-charge-r2.md` is adopted as the successor of C1c plan r4 on the points it names:
- **LD-C1C-7's "charges nothing" and "adds no charge":** sealing's read-set guard is now charged under C2b plan r4
  M1a convention C1.
- **The line-242 control** is replaced by the addendum's §5.

PLAN-r4's other text is unchanged.

## What was reviewed

| Artifact | sha256 |
| --- | --- |
| **Adopted subject:** `ADDENDUM-guard-charge-r2.md` (10,630 bytes, the reviewed bytes, never edited) | `85bbb8ec883b572547215664ac088c2d5ceeea86c82bf71dec2ec95e931dab6f` |
| Amended record: `opensip_arch/docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r4.md` | `d066487af5608b0375bd0ba1f8eaefda9b8bdbe70d27d96a875ba43cca8fe835` |
| Rejected draft: `ADDENDUM-guard-charge-r1.md` | `12f1e2b9895edc21eaeab4b7bc56977928d153115bf4f5bf7789b7a0eef21c38` |
| R3 review r1 (`L5-RULING: A-NEEDS-REVISION`): `REVIEW-r1.md` | `9835ecf79ea39098a2ed78453a030f2d1e0bb6d817fa6c8c4f8b1c90000b3fa3` |
| R3 review r2 (`L5-AMENDMENT: REQUIRED-CHANGES`, finding 1): `REVIEW-r2.md` | `fe84a78df455054d42c1c034a8fb5b26a0ac6f65788ec3ecb0771aef373777f9` |
| **R3 review r3 (`L5-AMENDMENT: ACCEPT`, no required findings):** `REVIEW-r3.md` | `51b854c5b6c048a1a485e16ce5596637e39a52214f569ef012aec4b44fa53091` |
| Requests r1, r2 and r3 | `f92ebf30…e0025`, `ba4a202b…63e6f`, `303b8cd2…cd8b0` |

**The reviewer:** codex-l5-r3, Codex gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the Claude author
(C1c-1, wT) and the Claude coordinator.

**The question came from:** the C1c-1 author's request, `../../c1c1/COORDINATOR-REQUEST-L5.md` (sha256
`6fa98843…d1ce54`), which answers Codex pricing review r1, P-RF-2.

## The authority

The owner's decision OD-AUTO-1 (2026-10-29; the top of `control-2026-10-06/ACTIVE-PLAN.md`) delegates law and cap
changes to the coordinator after an R3 different-vendor review. This adoption:
- changes accepted law (C1c plan r4);
- changes no cap and no *L*max;
- reruns nothing.

## What this adoption does not accept

As REVIEW-r3 states, this adoption does not accept:
- pricing r1 or r2;
- the fit gate (§6);
- the source, the model or the runtime controls;
- any fusion proof;
- C1c-1's acceptance, integration, binding, receipt interval or qualification.

The WIP commit 53d6737 is not accepted.

## Binding

At C1c-1's binding, both of these are copied unchanged beside PLAN-r4 in the architecture repository, and the
inventory records both:
- `ADDENDUM-guard-charge-r2.md`;
- this receipt.

## Owner notification

On 2026-10-29 this is flagged to the owner in the coordinator's session summary as an owner-delegated law change. The
owner can reverse it.
