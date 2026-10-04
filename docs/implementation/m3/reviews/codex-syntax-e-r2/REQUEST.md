Codex review: **M3-E1 r2**, the syntax crate and grammar registry law. Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review, round 2. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-syntax-e-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds, cargo or test runs: a timing-sensitive crash-matrix run is using this machine. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, counts or schedules, use read-only scratch scripts under your review directory.
- Read-only crates.io and GitHub API calls are allowed. Do not download or build upstream sources.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r2. It is the subject of `subjectSha256`. It is untracked in arch until acceptance.
- **The previous revision:** `docs/implementation/m3/syntax-e/PROPOSAL-r1.md`. It is byte-identical to your r1 subject (`90175f28…`, 69,559 bytes). Your r1 review is in `/tmp/opensip-implementation/reviews/codex-syntax-e-r1/`.
- **Pins:** `hashes.txt` pins both revisions, this request, and the context files. That includes the execution-input and enumeration owners r2 now cites, and the accepted M3-PLAN **r6**.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only.

## What r2 changes

The "r2 changes and review responses" table at the top of PROPOSAL.md maps each finding to its change.

1. **E-R1, the candidate-only result: new items 14a and 14b.**
   - **Item 14a.** A syntax-only `clones-near` binding's executed result is exactly one retained `CandidateProducerResultV1`, bound through the existing execution-input owner (EXC §6; EXM:1465-1555). It gives a case-by-case table:
     - an explicit empty census;
     - a successful empty result;
     - groups found;
     - syntax-error files (`input-closure-incomplete` / `source-parse-error`);
     - each truncation bound and each group bound (`budget-exhausted`; over-size groups withheld whole);
     - unsupported census paths (`language-tier-unsupported` / `capability-missing`);
     - a backend fault, which yields **no envelope**.

     It also covers precedence, the absence of `unavailable`, required-cell handling, the body-id recipe and `sourceBodies` custody. It distinguishes the enumeration-local `source-syntax-invalid`.
   - **Item 14b, the producer.** Every syntax-universe record names the **core provider closure**: C item 9's core import-producer projection, the same identity. There is one execution-plan stage per syntax universe.
   - **Obligations on C.** This needs two new cross-law items:
     - **X-C1:** C item 9 and C2-T13 admit the core provider closure for syntax-universe producer fields, and as a `semanticClosures` member exactly when a syntax universe is selected;
     - **X-C2:** C4a's `clones-near` census.
   - **SYN-1F,** a joined foundation successor, mirrors `source-parse-error` into every foundation `NativeCause` copy: EXS:201-218 (which EXM:851 holds equal to NES), IDS:3491, the subject-inventory and enumeration-plan schemas, and the evaluator projection registry. SYN-1 (f) covers the native-owned provider-startup copies.
   - **New unit E2s** applies both to the product's schema sources, evaluator registries and generated carriers.
   - **Controls:** E3-T8 to E3-T14.
2. **E-R2, the admission chain (item 5).** An ordered chain, A1 to A12:
   - fixed paths, size bounds, canonical bytes and digests;
   - descriptor to manifest;
   - **definition to manifest row**, for all five repeated fields;
   - the member closure and a single runtime pin;
   - `executionModel` against module presence;
   - engine and limit compatibility;
   - static module validation under the host's fixed configuration;
   - zero imports;
   - **closed exports with exact types**;
   - the shim ABI;
   - a **recomputed canonical `SymbolTableV1` digest**;
   - normalizer kinds and registry completeness.

   The T-native equivalent binds the ABI, the symbol table and the runtime to the linked `Language` and the compiled-in table. Every static failure is a named pre-Plan key on NE:3530's route; execution faults stay `operational-failed`. Item 4 gains size bounds and a closed tree. Controls: E2-T24 to E2-T32.
3. **E-R3, the H join (item 20).**
   - **The edge.** E3 is built against the **accepted H law's interface** (M3P:261, before day 0). Its integration edges are E2c, C1a, B2-c and E2s, so it finishes on **day 14** with **14 days of slack**, matching M3P r6 (M3P:303, M3P:342).
   - **The second-integrator rule.** Final wiring and its end-to-end controls go to whichever unit integrates second, inside that unit's acceptance scope. Under r6 that is:
     - **H** (day 22) for the fact and Coverage join;
     - **C4a** (day 19) for X-C1's and X-C2's Plan legs;
     - **J2** (day 25) for the capture of the stage receipt and the envelope.
   - **Preserved:** M3P r6's 33-day chain, K2 by day 28, O2_selected by day 31, and the lead set by day 22.
4. **Non-blocking observations E-N1 to E-N4** are adopted:
   - the M3P citations now point to r6, and r4 only for the historical lean;
   - dependency counts are estimates, with a minimal `wasmi` feature set;
   - P3 says "ten dialect selectors";
   - DR-G21 is described as an E extension, and the same-user-child properties are distinguished;
   - exposure scope replaces "no untrusted input", and the isolation claim is conditional on the TCB.

## Decide

1. **E-R1.** Is item 14a's table complete and lawful against EXS:833-1058, EXC §2 and §6, EXM:321-337, :540-565 and :1465-1555, and ENC:49?
   - In particular: the withheld-group rule; "no envelope" after a backend fault; never `unavailable`; and the census rule (X-C2).
   - Is SYN-1F's mirror list complete? Is E2s's product list complete?
   - Is item 14b's producer decision (X-C1) sound against IDS:4726-4803, ENS:265 and C item 9? Is routing it as an obligation on C's next revision acceptable for this law?
2. **E-R2.** Does A1 to A12 close every edge from the manifest to the definition to the executable?
   - Does it answer your r1 counterexample (E2-T24) and the correctly hashed incompatible module (E2-T28, E2-T29)?
   - Is `SymbolTableV1` an adequate canonical form, and is the T-native binding equivalent?
   - Are the static and execution routes cleanly separated?
3. **E-R3.** Is the interface-first edge with the second-integrator rule consistent with M3P r6's table and figures (M3P:284-342)? Is the assignment of legs to H, C4a and J2 sound?
4. **Regressions.** Did any r2 edit contradict r1 decisions you assessed as sound? Those are the backend and E0, the closure, the registry, the languages and routing, outcomes, the eleven cells, DR-G25 and security.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. SYN-1, SYN-1F and SYN-NS need `ACCEPT-DESIGN-UNIT` reviews of their own. X-C1 and X-C2 are reviewed in C's next revision. E2a, E2s, E2b, E2c and E3 are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.
