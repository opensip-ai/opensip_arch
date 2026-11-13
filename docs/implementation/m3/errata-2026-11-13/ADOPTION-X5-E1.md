# Adoption receipt: ERRATUM X5-E1, Part A only (replay's retained-byte cap, 32 MiB to 256 MiB)

**Prepared by the records clerk on the lead coordinator's binding instruction (OD-LEAD-1); the lead's merge of this branch is its adoption.** This is an erratum to law X5 r4 (`docs/implementation/m2/replay-join-x5/PROPOSAL-r4.md`, sha256 `2734f74b629a0fc27d80e90c38d07a901e21ac625e830b7715897c3151f88b71`). X5's bytes are NOT edited. Where this erratum's Part A speaks, it supersedes the retained-byte value at live `PROPOSAL.md:134` (r4 `:132`) and the reading of live `:130` (r4 `:128`).

**Adopted:** Part A, section X5-E1.1 of the exact bytes `docs/implementation/m3/errata-2026-11-13/ERRATUM-X5-E1.md` (12,920 bytes), sha256 `1375b771be97db9d7754b7f9c1a192bf4c88c4bd319eae1cd06cb3395ab2b44f`, the bytes both reviewers read at head `42c6d51388101a998d3f14eafa42c16d4fb87c6b`.

**Substance (Part A controls):** `REPLAY_LIMITS` retained bytes become 268,435,456 (256 MiB), a local development bound (LD-DEC-7 items 2 and 3), sized from the real closure trees (134,756,890 bytes across 168 additional distinct blobs against the cap). The other eight values of 5e, items 4, 5, 5a to 5d and 5f, every row and remedy, and custody are unchanged. The memory cost disclosure of the erratum stands; the cross-vendor reviewer advises carrying the larger bound (up to the 256 MiB cap held two or three times, roughly 770 MB before other overhead) into the milestone disclosure.

**PART B IS NOT ADOPTED.** Section X5-E1.2 (re-routing a cap crossing at replay from the provider structural-violation row to the host-fault row) has no standing from this receipt. The existing route stays: a replay cap crossing takes the structural row as accepted X5 r4 provides. The cross-vendor reviewer found two required findings against Part B, and both are OPEN:
- **RF-X5-1:** the bound condition must cover nested owner errors (for example `Structure(Graph(Limit))`) through a named evaluator-owned exhaustive classifier, with exact-need and need-minus-one controls for every dimension.
- **RF-X5-2:** the replay-bound remedy must be published before the route is adopted; the provider-output remedy cannot be reused for a host sizing failure.
The text of Part B stays in the file as a proposal and is not law. It becomes effective only after a revision answers both findings, is reviewed again, and is adopted by its own receipt. The other Part-B-dependent work (the X5 row, remedy and bounds-law changes and the design lock's X5a control text) is not authorized by this receipt.

**Basis, bound by value (independent reviews of the bytes above):**
- Codex gpt-6.1-sol/high, session `01a1d3d5-0f2c-7320-b1f7-77b3bca9aff8`, `reviews/codex-errata-2026-11-13-r1/review.json`: X5-E1 REQUIRED-FINDINGS on Part B only; "Part A is acceptable independently ... they do not require postponing a receipt expressly limited to Part A."
- Claude claude-opus-5-5/medium, `reviews/claude-errata-2026-11-13-r1/review.json`: ACCEPT (the whole text).

**Product side:** branch `replay-cap-1-r1` marks the constant "at risk until that binds", naming this erratum; its reference resolves to this file when this receipt is merged. No product code, lane or qualification is accepted here. No design-lock entry (X5 is not a lock input).
