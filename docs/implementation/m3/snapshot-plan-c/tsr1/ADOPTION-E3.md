# Adoption receipt: TSR-1 erratum E3, the R-10.3 remedy that fits the unchanged public record, 2026-10-30

**Decision LD-COORD-E3 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, as a law change of
adopted TSR-1 after R3 review.**

`ERRATUM-E3-r3.md` is adopted. It changes three things:
- **The remedy clause:** R-10.3's 1,545-character quoted clause is replaced by a 290-byte clause. With S10b's 646
  characters, the remedy is 936 characters, within `DomainDetail.remedy`'s `BoundedText.maxLength` of 1024 in
  common-v1, v3 and v4.
- **The attribution wording:** the clause and C30's replacement sentence describe the existing bounded attribution
  honestly. A long subject keeps its leading characters and the sha256 of the full raw subject, so the member may not
  be visible.
- **New controls:** C30b, the schema-only boundary pair with a non-ASCII scalar, and C30c, the long-path and
  short-path attribution control.

**Unchanged:** every TSR-1 limit, refusal, phase order, alias and key, the public record, the D9 row and
`subjectBoundLaw`. E3 is separate from the deferred erratum S2 (LD-Q-17).

| Artifact | sha256 |
|---|---|
| **Adopted subject: `ERRATUM-E3-r3.md`** (the reviewed bytes, never edited; the only bound file) | `1c7901a6814391cd5f83fd524c87137680b93809b9f5ddda5da042022719a0af` |
| **R3 review r3 (`TSR-1-E3: ACCEPT`, no findings): `REVIEW-E3-r3.md`** | `4a9e35f69177ae80fc9e2d2e1fdf921dfac8ab18ce1fac68f03272b26dd4d4fd` |
| R3 review r2 (REQUIRED-FINDINGS: E3-R2-RF-1, the binding list) | `8b7e7f3963f25a7e2b7e7a8f908d5e3ef0fd439df2fbef630e8c5d09c4092ebc` |
| R3 review r1 (REQUIRED-FINDINGS: RF-1, member elision; NB-1) | `ec7222fa3f3f1a7d0a7c4fbd208e814a39306f7c956bed8b934f9c555b32cb4c` |
| Review history, not bound: `ERRATUM-E3-r1.md` and `-r2.md` | `ae8c40be…21f7de`, `a34815b2…3f637d3f` |
| The amended law: `TSR-1-r4.md` (receipt `ADOPTION-TSR-1.md`) | `be654c41dcc310206fca27aa3feaddd9c1d5d9c1f3eeb7f8652dd0026c4e99f3` |

- **The reviewer:** codex-tsr1-r1, Codex gpt-6-astra/high, R3-FRONTIER (w15:p1). It is a different vendor from the
  Claude coordinator, which drafted E3.
- **The origin:** C2b-1b escalation X-C2B1B-4, and LD-Q-34.
- **C2b-1b's obligations:** the remedy constant and both model copies, C28's remedy clause, and C30, C30b and C30c.
- **Binding:** at C2b-1b's binding, `ERRATUM-E3-r3.md` and this receipt are copied unchanged beside TSR-1, and are
  recorded.
- **Owner notification:** it is flagged to the owner as an owner-delegated law change.
