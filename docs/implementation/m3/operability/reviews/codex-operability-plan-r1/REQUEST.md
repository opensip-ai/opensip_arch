Codex review: the M3 operability plan, r1. It covers logging, observability, resilience and support. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-operability-plan-r1.

**Rules:**
- Read-only. No repository edits, commits or pushes.
- Don't run product code or tests; crash-matrix lead sets are running on this machine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

**Subject:** `docs/implementation/m3/operability/PLAN.md`, 19287 bytes, sha256 `f2005ed0477f1de5690c023945a74a7534396aa2b376eef62ca71d6da65b20d5`. It is a plan, not law. The companion plan is `docs/implementation/m3/analysis-quality/PLAN.md` (r2, under separate review). Repositories:
- design: `/Users/sb/code/opensip-ai/opensip_arch`;
- product: `/Users/sb/code/opensip-ai/opensip`, main `eb0d503`;
- predecessor: `/Users/sb/code/opensip-ai/opensip-cli`, HEAD `83f705d8`. Its lessons are in §2.

**Context:** the owner will use OpenSIP daily on Rust, TypeScript and Python code at Amazon, and develops on AL2023.

## Decide

1. **Facts.** Do the plan's statements about the existing design hold, in §1 and its citations? Look for anything already specified that the plan misses or contradicts, e.g. DR-125, DR-114, DR-G20, DR-G21, the control-plane contract, the D9 outcomes, the secret-handle rule, the no-hidden-environment-input rule. Do the opensip-cli lessons in §2 match that repo's code? Spot-check them.
2. **Conflicts with accepted law.** Examples:
   - logs inside the installation's operational state;
   - the diagnostic event frame on the control plane;
   - OTLP egress;
   - the disk preflight before durable commit;
   - the panic hook versus M2 recovery.
   Is each one either compatible, or flagged in §9 as needing a successor?
3. **Method.** Is anything important missing for a daily-use tool at this quality bar? Are the proposed defaults sensible: retention, caps, the 2 s cancellation target? Are the enforcement rules sound? Is the milestone split right, especially O1's timing before the M3 protocol law?
4. **Privacy.** Are logs, crash records and support bundles safe for private source, with no excerpts and redaction at the sink?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem and fix;
- "nonBlockingObservations";
- "subjectSha256".

Do not commit.
