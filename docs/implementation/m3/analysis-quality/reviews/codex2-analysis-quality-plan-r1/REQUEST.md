CODEX2 review: the M3 analysis-quality plan, r1, **method and soundness**. Claude Opus 5.5 leads. A separate reviewer, GROK2, validates the plan's facts and citations in parallel. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-analysis-quality-plan-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- Don't run product code or tests; another unit's timing-sensitive crash-matrix runs are in progress on this machine. Reading files, git read-only and grep are fine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

**Subject:** `docs/implementation/m3/analysis-quality/PLAN.md`, 28038 bytes, sha256 `4e1c090112ec7480753425605de052c77d2e36e6981bea493e437a3fe7145203`. It is a plan, not law: it changes no contract and claims no measurement. Its §1 summarizes what the design already decides. Its §11 lists the decisions it asks for. The product contracts are in `docs/v2/contracts/product-v1/`, the register is `docs/v2/architecture/08-decision-and-readiness-register.md`, and the qualification gates are in `docs/coop/design-corrections/qualification-gates.applied.v1.json`.

**Context:** the owner will use OpenSIP daily on a Rust, TypeScript and Python team at Amazon, and cares most about the quality of the analysis. M3 is the native analysis milestone (build plan line 887).

## Your focus: will this plan make OpenSIP's analysis excellent, and is its method sound?

1. **Dimensions Q1–Q8.**
   - Are they the right ones for a heavy daily user?
   - Is anything important missing? Examples: false-positive cost per finding type, noise per thousand lines, time-to-first-useful-finding, determinism across machines, memory under very large monorepos, behaviour under broken or partial builds.
2. **Targets.** Are the proposed numbers sensible, measurable and not self-defeating? In particular:
   - precision ≥ 0.99 for gating rules, and zero false-clean results;
   - the §5.2 budgets, including the Rust build-output caveat;
   - incremental ≤ 2 s.
3. **Ground-truth method** (§4.3–4.5):
   - adjudication: bias, label drift, and agents as adjudicators;
   - seeded defects: realism, and whether seeds land in unresolved regions;
   - the cross-tool differential: tool-specific semantics, and versions;
   - the refactor suite.
   Can these be gamed, or give false confidence? What would make them robust?
4. **The rule catalog** (§3). Is the initial set right for Rust and TypeScript teams? Is anything high-value missing? Example: Rust workspace-level `pub` analysis versus rustc lints. Are any rules likely to be noisy?
5. **Incremental and resident host** (§5.3). Is the recommendation (c) sound? Is "decide before the M3 provider protocol is fixed" the right timing? What are the risks to authority, replay and Coverage honesty?
6. **Python and the onboarding kit** (§8). Are the third-language concerns complete?
7. **§10, what's missing.** Are the priorities right? What else is missing from the project and the product?
8. **Internal consistency.** Does the milestone mapping (§9) hang together with the build plan? Are the decisions in §11 owned correctly between owner and lead?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem and recommended fix;
- "nonBlockingObservations";
- "subjectSha256".

Do not commit.
