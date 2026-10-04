Codex review: **S-OP-2 r1**, the safe event vocabulary and sink law. It is a contract-successor proposal for the DR-125 owners, named by the accepted operability plan (`docs/implementation/m3/operability/PLAN.md:408`). Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review, round 1. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- This is a law review, so run no product builds, cargo or tests. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

`docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, r1. Its sha256 and bytes are in `hashes.txt`, which also pins the context files below.

The product is `/Users/sb/code/opensip-ai/opensip` at main `3d2d5b5` (X9-6 integrated), read-only.

## What it builds on

- **The accepted operability plan** (`docs/implementation/m3/operability/PLAN.md`, r3; reviewed bytes `PLAN-r3.md`):
  - §3.1, phase-lawful identities (lines 145-162);
  - §3.2, the vocabulary and privacy (164-183);
  - §3.3, the bounds (185-207);
  - §3.4 and §3.6;
  - §5.3, the crash-ring allowlist (178, 302-313);
  - §6, the bundle (351-359);
  - §7, enforcement (363-372);
  - §9's S-OP-2 row (408);
  - §10, the controls (422-437).
- **Your own operability-plan reviews** (`docs/implementation/m3/operability/reviews/codex-operability-plan-r{1,2,3}/`). Three findings bear on this subject:
  - OP-R1-03 and OP-R1-08;
  - OP-R2-NB-01, digest provenance;
  - OP-R3-NB-02, write admission and the queue under suppression.
- **The draft law M3-L r1** (`docs/implementation/m3/provider-protocol-l/PROPOSAL.md`; not accepted):
  - item 12, the S-OP-4 record join (lines 345-371);
  - item 13, the identities (373-394);
  - item 14, the events it needs from S-OP-2 (396-425);
  - its gate item G7 (line 24).
- **The M3 plan** (`docs/implementation/m3/M3-PLAN.md`, r4): lines 89, 92, 160 and 174.
- **The joined contracts:**
  - DR-125: REG:314 and REG:434; APP:620-630 (D.SDK) and APP:3860-3869 (the DR-125 row); DRC §8 (`distribution-runtime-completion.v2.md:513-601`); SDK4 `component-sdk-contract.v4.json:78-82, 99-105`; F02:179-197.
  - DR-114: DC4 `doctor-contract.v4.json:1005-1086`.
  - The secret rule: F03:45-50, F03:56-59 and F03:65-67.
  - No hidden environment input: CH13:59-62.
  - Common control: `control-completion.contract.v5.md:9-65`.
  - The protocols: RPP:117 and RPP:441-445; DLV:857 and DLV:1133; NE:2025, NE:2967 and NE:3160-3164.
  - The gates: QG:403-441; SLJ:481.
  - Historical: OPV10:65-110, 163-175, 191 and 257.

## What it decides

1. **Registry (items 1-3).**
   - It is one host-owned registry in Rust source, with generated Markdown and JSON documentation that is drift-checked.
   - Names follow `domain.component.action`. OPP's two-segment working names are mapped to it.
   - It defines which changes are ordinary registrations and which need a successor.
2. **Privacy classes and kinds (items 4-7).**
   - P0–P3 are defined by what may determine a value's bits. P3 has no kind.
   - There are fifteen closed `SafeField` kinds, K1–K15, each with its class, constructors, bound and no-source argument.
   - Paths are `ProjectPath` (P2), or `PathRef` (P1): an anchor plus a 64-bit HMAC tag under a per-process key that is never written.
3. **Enforcement (items 8-11).**
   - `SafeField` is sealed. `CodeEnum` text tables are associated `const`s. P1 and P2 constructors are restricted by provenance. Record bounds are static assertions.
   - Phase-lawful identities are enforced by scope marker traits.
   - Foreign `tracing` and `log` callsites never get interest.
   - The sink scrubber is a tripwire that must fire zero times.
4. **Sinks (items 12-13).** Each sink has a class ceiling, and its encoder projects fields by their static class. Item 13 adds sink-specific rules, including control and bidi escaping, and the bundle re-projecting by the registry.
5. **Bounds (items 14-17).** OPP §3.3's values, plus:
   - two new provisional mechanisms: `warn`/`error` headroom in the queue, and a per-name, per-request budget;
   - eight loss reasons;
   - a non-recursive marker in a preallocated slot;
   - a sink gate, read immediately before each write syscall. It is the mechanism behind OP-R3-NB-02. The policy for closing it is S-OP-1's and S-OP-7's.
6. **Joins (items 18-22).**
   - DC4's two tiers carry over. Error text is stricter than DC4: kind and errno only.
   - DR-125: what "bounded structured diagnostics" and "unstructured host logs" mean for the host.
   - The secret rule and DR-108; CH13.
   - The provider-value dispositions. Two go beyond M3-L: `refusal` detail is reduced, and nonces are never recorded. `detailCode` gets an empty registered table.
7. **Initial registry (item 23).** 26 events. **Recording (item 24):** two insert-only overrides, deferred to M3-O's first code unit.

## Decide

1. **Scope.** Does the subject deliver the whole OPP:408 row: registry, `SafeField` set, privacy classes, per-sink allowlists, §3.3 bounds and loss marker? Does it stay out of S-OP-1, -5, -6, -7, -9, -10 and -12, O4, O7 and O9?
2. **Successor standing.** Does it lawfully give content to DR-125's SF-2 (SDK4:81), F02:186 and F02:193-195, and DRC:574-579, without narrowing or contradicting any accepted sentence? Is citing SDK4, whose own header says `CANDIDATE-NOT-APPLIED` but which APP:3860-3865 inherits, sound?
3. **Classes.** Are the P0–P3 definitions sound and consistent with OPP:169 and OP-R2-NB-01? Rule on open question R5 (`RuleId` P2).
4. **Kinds.** For each of K1–K15:
   - Is the class right?
   - Is the constructor set closed?
   - Is the "cannot carry source or secrets" argument sound?

   Look hardest at:
   - K3 `RegisteredCode`;
   - K6 `CodeLocation`: the product has no path remapping, so dependency `Location::file()` values are absolute;
   - K7 `Reduced`, which keeps no digest;
   - K9 `IdentityDigest`, which has no file-content digest;
   - K10 `PathRef`: is the keyed ephemeral tag sound, and is the rejection of an unkeyed hash right?
   - K12 `ProjectPath`, built only from admitted path types.
5. **Enforcement.** Does item 8 really make free text fail to compile into an event of any class? Look for a hole:
   - a `CodeEnum` impl;
   - a blanket or `From` impl;
   - misuse of a mint;
   - generic code;
   - the macro itself.

   Is item 9's scope-typed enforcement equivalent to OPP:151-160, including CommitUndetermined's ExecutionId, no candidate RunId, and the emergency case?
6. **Sinks.**
   - Are item 12's ceilings exactly OPP:174-180? Is any sink missing?
   - Is static projection, rather than whole-event refusal, the right rule?
   - Item 13: are the escaping rules sound? Is it right that the bundle builder re-projects by the running registry?
7. **Bounds.** Check items 14-17 against OPP:185-207 and OPP:431:
   - Static record bounds, and `refused` as a defensive zero.
   - The admission order.
   - The two new mechanisms: headroom and the per-name budget.
   - The marker's non-recursion.
   - The sink gate as the answer to OP-R3-NB-02, without deciding S-OP-7's policy.
8. **Joins.** Is any statement in items 18-22 wrong, or does any of them change the joined text? Look at:
   - the DC4 mapping table and the stricter error rule (R2);
   - the DR-125 reading (R1);
   - DR-108 handles;
   - CH13 and the environment list;
   - the provider table against M3L:345-371, especially `refusal` detail, nonces and the empty `detailCode` table.
9. **Registry r1** (item 23).
   - Do the names follow item 2's grammar?
   - Is every M3L:412-419 need covered?
   - Are the kinds, classes and required identities right?
   - Are export candidates limited to P0 fields?
10. **Recording** (item 24). Are the two insert-only overrides correct and sufficient? Is deferring them to M3-O right?
11. **Controls C-1 to C-12.** Can each one falsify the claim it names? What is missing?
12. **Citations.** Spot-check them. "Citations checked" notes that the secret rule is at F03:45-50, not 44-50.
13. **Anything else** wrong or missing.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on acceptance. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: a single string, PROPOSAL.md's sha256 as pinned in `hashes.txt`.

r1 has no verify_design subject manifest, because item 24 defers recording, so this verdict is on the successor text. The later recording unit (`successor.json` plus a subject manifest over these bytes) will need its own `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. This is not an inventory unit, so give no `inventoryCandidateAssessment`.

Do not commit.
