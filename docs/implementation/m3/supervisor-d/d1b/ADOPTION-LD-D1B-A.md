# Adoption receipt: LD-D1B-A r2, the confined launch's representation and status settlement (a narrow M3-D F-1 completion), 2026-10-30

**Decision LD-COORD-D1BA (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1.** It is adopted
**before** D1B-S.
- **What it does:** it fills the representation that SD-3 (contract 155) delegates to D1b: the fd 5 record encoding,
  the fd 6 failure codes and their classification.
- **Its route:** LD-Q-35 routed it to R2 plus adoption, with a safeguard. The R2 plan review (D1BPLAN-R1-RF-1) found
  that r1 moved an F-1 row, so it went to **R3**.
- **The R3 verdict on r2:** it states that "No listed SD-3 or F-1 invariant moves in r2": the operation order, the
  64 KiB bound, the positive `A` byte, the existing status classifications and the F-4 refusal rule are preserved.
- **The residual it adopts, disclosed:** a launcher killed from outside between writing `A` and `execve` is classified
  as F-1's `A`/EOF (continue), then handled as an ordinary early exit (§5).

| Artifact | sha256 |
|---|---|
| **Adopted subject:** `LD-D1B-A-r2.md` (the reviewed bytes, never edited) | `5949b6737039dbe59b0fbcbd4144c27eea3218d2790dcbb863f8626d5a8fe24e` |
| **R3 review r2 (`LD-D1B-A: ACCEPT`, one NBO, carried into plan r4's controls):** `REVIEW-A-r2.md` | `7f18a3b77a6bc3341ab1e99f982850f303431226bce285077338123165ee08e5` |
| R3 review r1 (REQUIRED-FINDINGS): `REVIEW-A-r1.md` | `fc60d8f4f9d428066109cc4c6e43e555c718b15a2ec4db7ab161d79f83a2e3f9` |
| R2 plan review that escalated it: `../review/REVIEW-plan-r1.md` | `d330d9a6c9f761d318fb59a74ba650784cf6b1b7f77b2d47d8391a6b2c9119ad` |

- **The reviewer:** codex-l5-r3, Codex gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the Claude author
  (opensip-d1b, w1E:p1).
- **What it unblocks:** D1b-1 and D1b-2 may freeze after the plan's R2 ACCEPT and the pre-lane gate.
- **What it does not do:** it claims no enforcement, and the measured-row table stays empty until CF-1.
- **Binding:** this file and the subject are copied unchanged beside M3-D, at D1b's binding.
- **Owner notification:** it is flagged to the owner as an owner-delegated law adoption.
