GROK review: M3-H r3, the fact admission law. This is a **law and contract-soundness** review, round 3. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-fact-admission-h-r3.

(Lead note: after drafting, the lead renamed the X-H3 successor from "C next / CRC-1" to "M3-C r8 / CRC-2". CRC-1, now in review with GROK2, routes X-H3 to M3-C r8 and a later identity successor, CRC-2. Nothing else changed.)


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- **The subject:** `docs/implementation/m3/fact-admission-h/PROPOSAL.md`, law M3-H r3. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/fact-admission-h/PROPOSAL-r2.md`, the r2 bytes you reviewed (`4ae48f09…`).
- **Your r2 review** is at `/tmp/opensip-implementation/reviews/grok-fact-admission-h-r2/`, copied to `docs/implementation/m3/reviews/grok-fact-admission-h-r2/`. It was REQUIRED-FINDINGS: RF-1 (the internal consistency of the routing) and NBO-1 to NBO-3. r3's "r3 changes and review responses" table maps each one to its change.

**The records** are pinned only by accepted snapshots:
- **One change since r2:** M3-C r7 was accepted (CODEX2, `a1ee9386…`). MC is now cited by `snapshot-plan-c/PROPOSAL-r7.md`. Every MC line was re-mapped mechanically from r6, and r7 changes only item 16 row 8, which H does not cite.
- **The rest are as in r2:**
  - `M3-PLAN-r6.md`;
  - M3-D `PROPOSAL-r3.md`;
  - M3-J1 `PROPOSAL-r4.md`;
  - M3-E1 `PROPOSAL-r3.md`;
  - M3-I1 `PROPOSAL-r2.md` and `UNITS-r2.md`;
  - M3-B `PROPOSAL-r2.md`;
  - AQP `PLAN-r6.md` and OPP `PLAN-r3.md`;
  - X5 `PROPOSAL-r3.md`.
- **M3-L** still has no accepted snapshot. It is cited only as the frozen r1 object of X-H1 and X-H4.
- **FA-2** is drafted and in review with Codex, and **M3-L r3** is in review with you. H depends on neither.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `cd5958b`, read-only. Since `3e64266`, its crates differ only in X4-F1's ten `crates/security` files. Every pinned product file is unchanged.

## The r3 answers to check

1. **RF-1, one authority.** Item 14.4's table is now the only routing authority for view-join keys. Items 5 (F10), 10, 11, 16 and 22 refer to it and restate none of it.
   - Item 22's producer-claim row, item 10's "row 30 or 32" sentence and item 22's blanket host-invariant routing of item 11 are removed.
2. **Anchors.** On a provider-return view, the three anchor keys take MJ row 30 only.
3. **Coverage claim keys.**
   - The prerequisite and totality keys take MJ row 32. This is a lead decision, and 14.4 states the basis.
   - `COVERAGE_PRODUCER_ADMISSION` takes row 32 when any row-32 cause is present, otherwise row 30. That is 14.4a's tie rule, which also answers NBO-3. The row-32 causes are `native.coverage-cause-*`, `native.coverage-source-variant-*` and `RC-6:`.
4. **Origin.** Item 11 is retitled. A provider's terminal Coverage is provider-return origin, and only the pre-Analyze conversion is host-minted.
5. **Key matching.** Keys are matched by their prefix token, the text before the first `:`, so suffixed keys reach their listed rows. The catch-all applies only when no listed token matches.
6. **H-C25** tests the router directly: item 11's two origins, suffixed keys, the tie rule, and a one-table source pin.
7. **NBO-1 and NBO-2.** F7 and item 14.5 cite DLV:972-975, and the product pin base is stated.

## Decide

1. **RF-1.** Does r3 close RF-1? Is item 14.4 the single authority, and do items 10, 11 and 22 now agree with it?
2. **R12 and R13** in the law's "Review questions".
3. **Scope.** Does r3 change anything else of substance in r2? Re-pinned MC lines should carry the same text they did in r2.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. FA-1, FA-2 and CRC-1's widening each need their own `ACCEPT-DESIGN-UNIT`. H's code units need `ACCEPT-UNIT` reviews. Do not commit.
