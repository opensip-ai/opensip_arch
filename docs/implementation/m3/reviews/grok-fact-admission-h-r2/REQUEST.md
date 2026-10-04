GROK review: M3-H r2, the fact admission law. This is a **law and contract-soundness** review, round 2. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-fact-admission-h-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- **The subject:** `docs/implementation/m3/fact-admission-h/PROPOSAL.md`, law M3-H r2. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/fact-admission-h/PROPOSAL-r1.md`, the r1 bytes you reviewed (`69f50bb1…`).
- **Your r1 review** is at `/tmp/opensip-implementation/reviews/grok-fact-admission-h-r1/`, copied to `docs/implementation/m3/reviews/grok-fact-admission-h-r1/`. It was REQUIRED-FINDINGS: RF-1 required, NBO-1 and NBO-2 non-blocking. r2's "r2 changes and review responses" table maps each one to its change.

**The records** are now pinned only by accepted snapshots, never by a live `PROPOSAL.md`:
- `M3-PLAN-r6.md`;
- M3-C `PROPOSAL-r6.md` (r7 is in review and is not cited);
- M3-D `PROPOSAL-r3.md`;
- M3-J1 `PROPOSAL-r4.md`, accepted by GROK2, which adds R10a;
- M3-E1 `PROPOSAL-r3.md`;
- M3-I1 `PROPOSAL-r2.md` and `UNITS-r2.md`;
- M3-B `PROPOSAL-r2.md`;
- AQP `PLAN-r6.md` and OPP `PLAN-r3.md`;
- X5 `PROPOSAL-r3.md`.

**M3-L has no accepted snapshot.** H takes no rule from it, and cites its frozen r1 bytes only as the object of X-H1 and X-H4. FA-2 and M3-L r3 are being drafted separately, and H depends on neither.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `15c0779`, read-only. Since `3e64266`, its crates changed only in X4-F1's ten `crates/security/` trust and custody files, none of which this law cites. Every pinned product file is byte-identical.

## The r2 answers to check

1. **RF-1** (items 5, 14, 16 and 22; controls H-C6, H-C14 and H-C24).
   - **F5** keeps only the anchor count, through the identity owner. F4 and F6 run on `inspect_relation_snapshot` and keep the owner's `RelationRule` text. `FACT_ANCHOR_CARDINALITY` is withdrawn.
   - **The anchor bytes** are checked once, in `inspect_plan_view_joins` over the **provisional view**. H builds that view in a staging overlay before anything joins the return's admitted set (item 14.2). No host copy of the anchor law is added.
   - **Item 14.4's routing rule:**
     - every view has one origin;
     - keys that judge a producer's claim (the three anchor keys; the Coverage producer, prerequisite and totality keys) take MJ row 30 or 32 on a provider-return view and the host-invariant row on a host-minted view;
     - keys that judge H's own assembly are host invariants whatever the origin.
   - **F3** now checks the `(relation, rung)` pair, so `FACT_SCOPE_JOIN` is reachable only through H's assembly.
   - **H-C24** discriminates the three anchor failures on a provider fact from the same failures on an E3 syntax fact.
2. **Item 10, rebuilt** (found while answering NBO-1). r1 called `inspect_coverage_producer` directly, with a per-Analyze census and a host-supplied dialect. The product owner's view join (`view_joins.rs:434-532`) builds the census from the view's own `unresolved-edge` facts, as IE:1481 and NE:3351 require. It derives the dialect table from the universe frame, through a function that is crate-private to the evaluator (`capability_support.rs:279`). r2 moves the producer boundary into that one call. H builds D and a provisional `coverage2` and names them in the view.
3. **NBO-1.** The census slice is caller-supplied (`coverage.rs:28-36`). On H's path its only caller is the owner's view join. H passes no census, and none is taken from a provider or from a caller of H.
4. **NBO-2.** MJ is now cited by J1 r4's accepted lines, and every other law by its accepted snapshot. M3-C r7's row 8 narrowing is noted in item 8.

## Decide

1. **RF-1.** Does r2 close RF-1 without a host copy of the anchor law? Is item 14.4's routing exact?
2. **Item 10.** Is moving the producer boundary into the owner's view-join call sound (R11)? Does it change any accepted interface, or any route in item 22?
3. **R9 to R11** in the law's "Review questions".
4. **Scope.** Does r2 change anything else of substance in r1? Every re-pinned line should carry the same text it did in r1.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. FA-1, FA-2 and CRC-1's widening each need their own `ACCEPT-DESIGN-UNIT`. H's code units need `ACCEPT-UNIT` reviews. Do not commit.
