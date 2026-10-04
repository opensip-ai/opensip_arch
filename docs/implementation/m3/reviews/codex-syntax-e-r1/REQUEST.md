Codex review: **M3-E1 r1**, the syntax crate and grammar registry law. Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review, round 1. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-syntax-e-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds, cargo or test runs: a timing-sensitive crash-matrix run is using this machine. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, counts or schedules, use read-only scratch scripts under your review directory.
- You may make read-only crates.io or GitHub API calls to check the law's **[U]** upstream facts. Do not download or build upstream sources.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r1. It is the subject of `subjectSha256`. It is untracked in arch until acceptance.
- **Pins:** `hashes.txt` pins the subject, this request and the context files.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only. `crates/syntax` is not a workspace member yet (P0, M3-PLAN:161).

## What the law decides

The "Decisions at a glance" table maps items to decisions. In brief:
1. **The backend (items 1 to 3; CH14:614).** tree-sitter grammars, executed **in the host inside a fuel-metered WebAssembly memory boundary** (one module per code grammar row, built from pinned sources, zero imports, run by the pure-Rust `wasmi` interpreter, with a fresh instance per file). This is "T-wasm". Natively linked tree-sitter ("T-native", BP:680-682) is the predeclared fallback. **E0**, a lead-run probe with six fixed pass criteria, chooses between them. The rejected alternatives are pure-Rust parsers, hand-written parsers, a confined syntax component, and tree-sitter's own wasmtime store.
2. **The closure (items 4 to 7; BP:684-688).** Fixed closure paths, definition records, a bundle manifest carrying identity-bearing limits and the engine identity, the descriptor join, the pins, and **one grammar registry file owned by `opensip-identity`** (moved from `crates/evaluator/src/native-context-registry.json`). It is drift-checked against `schemas/sources/native-v2.schema.json` and `identity-v3.schema.json`.
3. **Languages, outcomes and limits (items 8 to 11; NE:260-306).** Seven languages, **eight rows** (TypeScript has `typescript` and `tsx`), fourteen suffixes. **The four data-document rows are format definitions, with no parser pinned or run.** Per-file outcomes: any ERROR or MISSING node makes the whole file a parse error, with a **new `NativeCause` `source-parse-error` under `input-closure-incomplete`** (successor SYN-1). Size, fuel, memory, node and depth bounds give `budget-exhausted`. A backend fault fails the step and is never Coverage.
4. **The syntax-only mode (items 12 to 16).** Its eleven cells; syntax facts and NE:7 clones; every bundle row selected; DR-G25's no-fallback guarantee, from five structural reasons.
5. **Security (items 17 and 18).** In the host, not a component. The WebAssembly boundary is defence-in-depth memory isolation and **not a sandbox claim** (AQ:344). It has no O7 dependency. Residual risk and the T-native posture are stated, with an M4 re-decision before untrusted input arrives.
6. **Successors and units (items 19 and 20).** SYN-1 (native contract), SYN-NS (normalizer specification), SYN-REG, SYN-DEP and SYN-LANE, plus C's CR-1 and an LP-1 licence recommendation. The units are E0, E2a, E2b, E2c and E3. The DAG claim is that the conditional host chain does not move.

## Decide

1. **Backend.** Is the criteria comparison in item 1 accurate and complete against the brief's criteria: determinism, the self-contained closure (DR-119, DR-G14), licences, supply chain and dependency policy, the unsafe and C footprint, pinning, performance, and Python readiness?
   - Is T-wasm a lawful reading of BP:676-688 and CH14:375 (the law's R-1)?
   - Are E0's criteria sufficient, and is the predeclared fallback lawful without a law revision?
   - Check the [U] facts you can.
2. **Closure.**
   - Do items 4 to 6 meet BP:685-688 and NE:223-232 exactly?
   - Is the descriptor-to-manifest join complete?
   - Is it sound that the limits and the engine identity are identity-bearing through `bundleDigest` (IDS:4533-4555)?
   - Is the T-native compiled-in table check adequate?
3. **Registry.**
   - Is moving the registry to `opensip-identity` consistent with BP:676-677 and the evaluator's existing owner (`native_context.rs:276-361`)?
   - Is the completeness rule ("a product bundle is the whole registry") lawful against NES:2257's `minItems: 1`?
4. **The table and routing.**
   - Does item 8's table match NES:536-646, NEM:3788-3790, NE:788-796 and IDS:4556-4610 exactly?
   - Is the data-document "format definition, no parse" decision consistent with NE:260-267 (R-2)?
5. **Outcomes.**
   - Is `source-parse-error` under `input-closure-incomplete` the right carrier, against NES:31-50 and NE:3317-3374 (R-3)?
   - Is the precedence handling, the per-file all-or-nothing rule and the `backend-fault` route sound?
   - Is anything left untyped?
6. **The syntax-only mode and DR-G25.** Are the eleven cells (NCM; COV) answered exactly? Is item 16 a complete structural guarantee against REG:370 and AQP:114-115?
7. **Security.**
   - Is the in-host placement, with its "not a sandbox" wording, consistent with AQ:344, SL:497, SL:1113, NE:2554, REG:317 and REG:366?
   - Is the C-worker rejection sound given M3-PLAN:308-319 and CH14:614?
   - Is the residual-risk statement honest?
8. **Successors and units.**
   - Is SYN-1's scope complete? Note the claimed record gap: the existing `native.syntax-grammar-*` keys are absent from NE:3530's route row.
   - Are the review kinds right?
   - Do the unit dependencies and the DAG claim hold against M3-PLAN:197-233 and C r3's recomputation (C:955-1009)?
9. **Consistency.** Does anything conflict with AQP r6, B r2, C r3, L r1 or M3-PLAN r4?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The successors SYN-1 and SYN-NS need `ACCEPT-DESIGN-UNIT` reviews of their own. E2a, E2b, E2c and E3 are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.
