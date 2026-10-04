CODEX2 review: F8b, the generator-closure and TypeScript-lane-registry contract successor, **proposal r1**. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** (proposal) or **REQUIRED-FINDINGS**. The unit's ACCEPT-DESIGN-UNIT review comes later, on the frozen subject manifest, after the observed rebuild.

Write only under /tmp/opensip-implementation/reviews/codex2-generator-closure-f8b-r1.

**Rules:**
- Read-only. Run no cargo, Node or generator; a crash-matrix evidence run is active on this machine.
- Never touch the real home. Never read the 413 fixture. Do not commit.

**Subject:** `docs/implementation/m2/generator-closure-f8b/PROPOSAL.md`, 16874 bytes, sha256 `f3162181aa65aeb63266df162147d6e6e366862a76c011610becf9126fba9833`.

**Product:** `/Users/sb/code/opensip-ai/opensip`, main `30c5db1`.

**Context:**
- L1's review request, `docs/implementation/m2/reviews/codex-licence-l1-r1/REQUEST.md`, judgment call 1: three tooling manifests were excluded from the licence change because their bytes are pinned.
- The precedent successor: `existing-root-diagnostics-468a` (see `docs/implementation/m2/` and its review).
- The companion F8a is in Codex's review, `docs/implementation/m2/reviews/codex-policy-refresh-f8a-r1/`.

## What it proposes

It re-pins two design-selected registries that still pin the `verify_design.py` from before VD1:
- `tools/contracts/generator-closure.json`, together with its build receipt from an observed offline generator rebuild, and `toolchain.json`;
- `tools/typescript-lanes.json`.

It also updates `schemas/registry.json`'s `generatorClosureSha256` and `apps/report/src/generated/report.ts`'s header. It adds `license = "Apache-2.0"` to the three tooling manifests.

**Lead decisions to examine:**
- rebuilding the generator, rather than hand-editing a receipt;
- leaving the lockfiles unchanged;
- a process rule: a unit that changes a file these registries pin must carry the re-pin.

## Decide

1. Is the scope complete and minimal? Is every file these registries pin accounted for?
2. Is a successor of 468a's shape the right vehicle? Is anything here an identity or contract change in disguise?
3. Are the lead decisions sound?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
