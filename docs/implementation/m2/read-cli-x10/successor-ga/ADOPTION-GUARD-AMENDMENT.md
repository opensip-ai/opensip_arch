# Adoption receipt: GUARD-AMENDMENT GA-r1, a narrow amendment of two apps/cli guards (2026-10-31)

**Decision LD-COORD-GUARD-AMEND (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3
different-vendor review.** Authority: LD-Q-165-B.

The amendment changes two accepted fail-closed guards. Each admits exactly one thing, and both stay fail-closed for
everything else:
- **The doctor guard** (`apps/cli/tests/doctor_tests.rs`; M3-O1/X10 opt-in graph): it admits exactly one more host
  feature, `profile-allocations = []`. That feature forwards nothing and is never default; nothing outside host's own
  dev-dependencies may enable it; and its existing `compile_error!` refuses any build without debug assertions.
- **The creator guard** (`apps/cli/tests/creator_commands_tests.rs`; RR-G2-2): it admits exactly C2b-1b's five literal
  lines below the logging adapter.

Planted controls GA-1 and GA-2 show that each guard still refuses anything else.

| Artifact | sha256 |
|---|---|
| **The subject:** w2C GA-r1 (doc `b7d6c489…`, exact diff `7e5611d3…`, SUMS `5d4e3298…`) | see the request pins |
| **The request, `REQUEST-guard-amendment-c2b.md`** | `d9cb7faf7dd9b757bdc71b3b95d3ed027bfabc90b8793ed4092dbc69a6e8f490` |
| **R3 review, `review/REVIEW-guard-amendment.md`** (`GUARD-AMENDMENT: ACCEPT`) | `243c5cce7bfc5dd564ecde2d1b28bc624ececf820bf5eca5ea0e7bf9dd3d2c89` |

- **The reviewer:** codex-guard-amend-r3, Codex gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the Claude
  author (w2C).
- **Findings:** no blocking findings; two CARRIED observations, kept as written in the review.
- **What it enables:** H5 = the C2a attribute fix (`8c5faf84…`) plus this patch (`7e5611d3…`) on a03407d.
- **Owner notification:** flagged as an owner-delegated amendment of two accepted security guards. It is narrow by
  literal text and stays fail-closed for everything else.
