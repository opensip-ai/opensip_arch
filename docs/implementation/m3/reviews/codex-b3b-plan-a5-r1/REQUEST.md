# Review request: B3-b plan r2, amendment A5 (B3-b3a in two units)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b-plan-a5-r1/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing and Git queries.

## Subject

- **The amendment:** `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A5.md` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 5005 bytes, SHA-256 `ad64083ba36ae654d7dfe0a15f28fda1d6b97f761a6c6f8282ef6a16de8aa25b`.
- **Bases:**
  - architecture `18d385688acd95025480fb31e78e657c16c0bbd8`;
  - product main `e367d7f465d8d0a74819cad5010a58b8641e4c7a` (B3-b2 complete: B3-b2b2b and B3-b2b2c bound, inventory v207, 170 contract successors).

## Authority

- The B3-b plan r2 (§4.1 to §4.3) and amendments A1 to A4, including:
  - A1's closure and receipt reasoning;
  - A2-3 step 4's term assignment and its carried NBO.
- Law M3-B r9 item 12.
- The accepted B3-b2b1, B3-b2b2b and B3-b2b2c code on main.

## What to review

1. **The split.** Is dividing B3-b3a into B3-b3a1 (the bound: closure, terms, repository rows, equality projection, validation, mutations) and B3-b3a2 (the blind-mode extension, receipt binding and controls, the pre-run gate) sound? Does it keep §4.3's gate intact, with no held-out store opened before B3-b3a2's acceptance? Does it keep A1's single gated refresh?
2. **The terms.** Does A5-2 keep A2-3 step 4's assignment, including placement and listing at n = 0?
3. **A5-3.**
   - Is the bound the ledger's (item 12)?
   - Is it right that the readers' uncharged parses contribute nothing?
   - Should the decision core charge its parses before the bound is derived?

   If the latter, say where that change belongs.
4. **Steps.** Are B3-b3b and B3-b3c unchanged, and is nothing in A1 to A4 lost?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3BA5-R1-RF-n` / `B3BA5-R1-NBO-n`.
