GROK2 review: the M3 analysis-quality plan, r1, **fact validation**. Claude Opus 5.5 leads. A separate reviewer, CODEX2, reviews method and soundness in parallel. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-analysis-quality-plan-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- Don't run product code or tests; another unit's timing-sensitive crash-matrix runs are in progress on this machine. Reading files, git read-only and grep are fine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

**Subject:** `docs/implementation/m3/analysis-quality/PLAN.md`, 28038 bytes, sha256 `4e1c090112ec7480753425605de052c77d2e36e6981bea493e437a3fe7145203`. It is a plan, not law: it changes no contract and claims no measurement. Its §1 summarizes what the design already decides. Its §11 lists the decisions it asks for. The product contracts are in `docs/v2/contracts/product-v1/`, the register is `docs/v2/architecture/08-decision-and-readiness-register.md`, and the qualification gates are in `docs/coop/design-corrections/qualification-gates.applied.v1.json`.

**Context:** the owner will use OpenSIP daily on a Rust, TypeScript and Python team at Amazon, and cares most about the quality of the analysis. M3 is the native analysis milestone (build plan line 887).

## Your focus: is every factual statement about the existing design true?

1. **Citations.** Check every citation in §1, §2, §4, §5 and §8. Does the cited file and line say what the plan claims? Examples:
   - AQC:127-130's exact equality;
   - AQ:273-287's median of 7 with ×1.20/×1.25;
   - NE:584-616's 57/6/3 cells and limitations;
   - NE:304-306 on Python;
   - IE:188-213 on fingerprints;
   - WS:352-358 delta classes;
   - QG items[12]'s p95 text (O9);
   - register:402 on condition 5.
2. **"Open or absent" claims O1–O9.** Is each gap real? Look for anything in the repository that already settles it, such as an existing rule catalog, incremental obligation, explanation requirement, Python decision or exploratory-measurement rule.
3. **"Decided" claims.** Is anything stated as decided that is actually open, superseded or contradicted?
4. **§10 items 9 and 10.** Is the record-hygiene list accurate? Are there other stale contradictions a quality plan should know about?
5. **Conflicts with accepted law.** Does any proposal conflict with an accepted contract or gate in a way the plan fails to flag as needing a successor? Examples: rule placement, explanation fields, the exploratory class, the T2 harness fetching repositories, cross-tool differentials (D-007; BP:716-717).

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, claim, evidence (file:line) and fix;
- "nonBlockingObservations";
- "subjectSha256".

Do not commit.
