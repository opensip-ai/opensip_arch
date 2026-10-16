# Review request: B3-b plan r2, amendment A4 (branch A decides its members before the walk)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b-plan-a4-r1/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing and Git queries.

## Subject

- **The amendment:** `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A4.md` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 5663 bytes, SHA-256 `bf05cd0f00feeb0d0b6c72d94cc15255964e885a69059fa37f2b0a3554fdc9ec`.
- **Bases:**
  - architecture `5c581b5c5a4e22ff3fa28d5e9f522df92a27c4a0`;
  - product main `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`.

## Context

Your `codex-b3b2b2b-r2` (`/tmp/opensip-implementation/reviews/codex-b3b2b2b-r2/review.json`) raised B3B2B2B-R2-RF-1: branch A's first trial walk can enter index-only nested repositories before item 6b reads the member's index. You asked that the gitlink/trial ordering be resolved and its authority bound explicitly, preserving the cap and short-circuit requirements. A4 is that resolution:
- branch A decides grammar first, then the member rules (item 6b included) in path order, then one walk with the admitted members' gitlinks;
- B3-b0 is amended (r4, contract successor 169) to model index gitlinks and the new order;
- the product follows in B3-b2b2b r3.

## Authority

- The B3-b plan r2 with A1 to A3.
- Law M3-B r9 items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`).
- B3-b0 r3 (`b3-b-reference/`; README LD-B3B0-6), and your `codex-b3b0-reference-r1` B3B0REF-R1-RF-2, which allowed a different public priority if settled and documented.
- Your `codex-b3b2b1-r1` B3B2B1-R1-RF-2 (the short circuit).
- Your `codex-b3b2b2b-r1` and `r2`.

## What to review

1. **Necessity.** Is A4-1's argument sound? Is there no order consistent with SLM-first, the index boundary and the short circuit?
2. **The order** (A4-2):
   - Does it guarantee that no walk descends into, lists or judges anything inside an index-only boundary of an admitted member?
   - Does it preserve the cap and the short circuit?
   - Does the grammar-first step faithfully keep SLM's grammar refusal?
   - Is the documented precedence change acceptable as a settled public priority?
3. **The authority** (A4-3). Is a B3-b0 r4 successor, with a `memberGitlinks` side table, the r4 order and the revised and new checker cases, the right binding? Are the two revised `rf2-*` cases correctly identified?
4. **The product step** (A4-4). Is carrying the decision core's restructure into B3-b2b2b r3 with RF-2 and RF-3 sound? Is anything of A3 weakened?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3BA4-R1-RF-n` / `B3BA4-R1-NBO-n`.
