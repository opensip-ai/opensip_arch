Grok review: law X8 r5, a record-only revision of the opaque API refusal suite. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-refusal-suite-x8-r5. This is a law review with no product cargo. Run git only read-only. Never touch the real home (`~/Library/Application Support/OpenSIP` must stay absent), and never read the private 413 UUID fixture.

## What is asked

X8 r5 records five things decided elsewhere and makes no new decision. The main question: **does any accepted outcome change?** That covers any item, trial result, case, group, code, fragment rule, feature, module, behavioural case, expected outcome or row, unit scope or dependency, or forbidden substitute of X8 r4, and any accepted outcome of another law. A record that goes beyond its source, or misstates it, is a finding.

## Pins

Pins are in hashes.txt. The accepted predecessor is preserved byte for byte, without its "ACCEPTED" note: `refusal-suite-x8/PROPOSAL-r4.md` is X8 r4, 46639 bytes, sha256 `3b0ead97b2e925ad1eef2456ad0f47b4fd5b963ffd0bfaea960faa7e83c85b00`, equal to `subjectSha256` in `reviews/grok-refusal-suite-x8-r4/review.json`. The snapshot already existed. It was checked, not rewritten.

## The revision (diff PROPOSAL.md against PROPOSAL-r4.md)

Every line of r4 survives verbatim, with two exceptions: the title (r4 to r5), and the "r4 ACCEPTED by Grok on 2026-10-02." note that the working law already carried. Three insertions:
- **An r5 header paragraph** after r4's. It says the revision is record-only, names its sources, says why each of the five is a record, and lists what stands.
- **One "r5 (record)" note** under item 5's bullet "`evaluator::replay_run` on a corpus Run from `crates/evaluator/tests/fixtures`".
- **One "r5 (record)" block** directly after the B table, before "B0 is required". The table rows themselves are untouched.

## The five records and their sources

1. **B2's wording.** B2 compares against the session's core evaluator closure, `CommitSession::core_evaluator_closure()` (X3d r8 item 3 step 1; EC1). The owner column reads "X3d-2, binding X3d-3". B6 still names the core closure. Source: X3d r8 and EC1 (accepted, `reviews/grok-evaluator-closure-x3d-r8`); `EXIT-PLAN.md`, "X8 B2 wording owed (2026-10-02)".
2. **The corpus path.** The B cases use host's pinned `crates/host/tests/fixtures/replay-fixtures.json`. `crates/evaluator/tests/fixtures` holds no Run (product `a2c5e8b`). Source: X8c judgment call 3.
3. **The REV on B1, B2 and B4.** Any refusal that latches the gate appends one REV (X3d item 7 step 1). This adds to the table and does not contradict it. Source: X8c judgment call 4.
4. **B6 and B7 at the public boundary.** B7's drift and B6's gate latch are shown through what the public boundary exposes: the outcome, the REV and the census. X4a's private test `an_unrelated_revocation_update_continues_as_drift_without_the_fence` pins the drift itself. Source: X8c judgment call 7.
5. **B0's candidate route.** Storage's synthetic run candidate is included through `#[path]`, with a test-only shim over host's public `embedded_schema_registry()`, and a test pins that both crates use the same 48 schema files in the same order. Source: X8c judgment call 1.

Both EXIT-PLAN entries ("X8 B2 wording owed" and "X8 record notes owed after X8c") list exactly these five.

## Disclosed for your judgment

- **X8c is not yet accepted.** Records 2 to 5 come from lead decisions in the X8c request (`reviews/grok-refusal-cases-x8c-r1`, status DRAFTED). The r5 header says so: if the X8c review changes one, the matching note is corrected by a later record. Please say whether r5 should wait for X8c's acceptance, or may stand on the request.
- **B7 and X3d item 7.** X3d item 7 step 1 owes a REV if "a revocation was observed", as well as on a latched gate. B7 observes an unrelated revocation, and its census is "as B0" (no REV). r5 does not touch this. It records only that latched refusals append one REV, and it does not repeat X8c call 7's phrase "the REV that `finish` owes only for a latched gate". If you read item 7's "revocation observed" as covering an unrelated revocation, say so as a note against X8c, not against r5, unless r5's wording is itself wrong.

## Decide

- **Does r5 change any accepted outcome?** See "What is asked" for what that covers. Please answer this explicitly.
- Is each record faithful to its named source, and does it go no further?
- Is the predecessor snapshot exact, and is every accepted sentence preserved in place?
- Is anything else wrong?

Write REVIEW.md and review.json. review.json must contain:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true or false;
- "subjectSha256": the sha256 of `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`;
- the preserved snapshot's path, bytes and sha256.

Do not commit.
