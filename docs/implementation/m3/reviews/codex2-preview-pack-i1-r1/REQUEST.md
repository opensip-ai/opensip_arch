CODEX2 review: M3-I1 r1, the X12c preview policy pack. This is a **law and contract-soundness** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-preview-pack-i1-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix review is using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. Both subject files are untracked in arch until acceptance.
- `docs/implementation/m3/preview-pack-i1/PROPOSAL.md`, the law. It is the subject of `subjectSha256`.
- `docs/implementation/m3/preview-pack-i1/UNITS.md`, the code-unit breakdown.

**The unit.** M3-I1 is a row of the accepted M3 plan (`docs/implementation/m3/M3-PLAN.md:166`). The row asks for three things:
- the frozen preview rule IR;
- the contract successor for `opensip.preview.typescript.pack:1`, meaning its bundled bytes, registry row and self-checks;
- the conditional policy-language successor of X12:191.

**The governing law.** X12 r3 is accepted (`docs/implementation/m2/policy-admission-x12/PROPOSAL.md`). The reviewed bytes are `PROPOSAL-r3.md`, sha256 `11628912…`. Its forbidden substitutes are at X12:196-222.

**The rule.** It is stated in AQC §2 (`docs/coop/completion/analysis-quality-completion.v2.md:51-82`). That section is pinned by the application manifest's `QUALITY.RULE` target, and DR-131 is SATISFIED under D-369.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `2967905`, read-only. X12a was integrated at `b642c45`, and X12b at `6dd7363`.

## What the law decides

**No product change before X9-6.** The law makes none. Its code units start only after X9-6 is integrated.

1. **A successor is needed (item 1).** The four predicate ops are per subject, emission is unary, and an `imports` importer is a symbol. So the rule cannot be written in today's DSL.
2. **One root-only graph atom (item 2).** I1 adds `cycle-representative` over `imports@resolved-target` on `file` subjects. Its truth table:
   - true at the least-path member of each admitted cyclic SCC;
   - false at the SCC's other members;
   - otherwise false only under complete graph Coverage, else indeterminate.

   The atom reuses the existing `declarative-subject-v1` emission, so there is one finding per component, on its representative. Item 2 also defines graph completeness at the universe extent, the uncertain-edge causes, the witness sets and the budget argument.
3. **Widen in place (item 3).** The successor widens the `PolicyDocumentV2`, proof3 and program-predicate `operation` enums without a new major. The law states its tension with IE:213-214.
4. **The successor's passages (item 4).** These are the WS, PDS, IDS and COMP overrides, plus a new ATOM §4a.
5. **The pack contract (item 5).** This covers:
   - the canonical document bytes, the registry row and the digest rules;
   - the digests, which are provisional and computed by the drafter;
   - the self-checks S1 to S10.
6. **Outcome (items 6 and 7).** The thresholds and outcome are in item 6. Item 7 is a scoped amendment to X12 r3 items 4 and 10.
7. **Feeds and open points (items 8 and 9).** Item 8 covers how I1 feeds C4, H, J and I2. Item 9 lists LD-1 to LD-12.

## Decide

1. **Consistency with X12 r3.**
   - Does the pack contract keep items 2 to 7 and 9, and every forbidden substitute?
   - Is item 7's amendment limited to the M2 registry state and the item 10 tests?
2. **Consistency with AQC §2 and DR-131 (PAC).** Do items 2.4 and 6 give these four results?
   - one finding per cyclic component;
   - external vertices dropped only by the host's partition;
   - unknown never treated as a pass or a guessed edge;
   - fail on one or more components, and pass only with sufficient Coverage.

   Is LD-4 a sound reading of AQC:65-69 against WS:600-604 and COMP:56? LD-4 says a known cycle under incomplete Coverage fails, with its deficiencies retained.
3. **Soundness of the IR against the product-v1 contracts.** Check:
   - the strong-Kleene value table;
   - universe-extent completeness (RPS:15);
   - the fixed forbid/forbid requirement, and the reading that sufficiency step 7 tests nothing here (LD-6, NE:2271);
   - the rule that every indeterminate answer carries a blocking native cause (COMP:56);
   - the use of `population-unknown` and `target-kind-unknown`;
   - the rule that edges entering V from outside are not read;
   - the witness sets;
   - the budget bound against COMP:38.
4. **LD-3.** Is widening the proof3 and program-predicate `operation` enums in place lawful under IE:213-214 and COMP:7, or does it need new identifier majors?
5. **The pack bytes and digest rules (item 5).**
   - Are they consistent with WS §5, COMMON's `ContributionId` and the X12a registry key law (`policy.rs:953-965`)?
   - Recompute the three provisional digests if you can, using only a read-only scratch script.
6. **Feeds.** Are the C4, J and I2 feeds and LD-10's detector-closure recommendation consistent with IE:1508-1512, COMP:9 and WS:277-281?
7. **Units.** Is UNITS.md's order sound, including LD-11, and does it respect the X9-6 gate?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The later contract-successor units (I1-L, I1-P) will need `ACCEPT-DESIGN-UNIT` reviews of their own. Do not commit.
