# B2-B3D-r2 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Subject manifest: `docs/implementation/m3/config-discovery-b/b2-b3d-r2-subject.json`, 9,745 bytes, SHA-256 `bb15540fb68d72f5eeeb2368e7ebb0034669d5bfca0f0ee2fcc99c27aa4978a5`. Independently rehashed all 43 members. All ten product-map rows match the archived and candidate worktree bytes; parent pins match product base `84caf3f58d8379c9386fda42a41e5513ac81ebbb`. Exactly nine existing paths and one new path are changed. Product main remains clean at that base; architecture matches `a1f14786e4ecb0c780d25b093c438821e6a5c3d8`. All nine source-authority pins match committed architecture bytes. The design lock is unchanged.

## Round-1 resolution

**B2B3D-R1-RF-1 resolved.** `Walk::enter` charges `owned(paths.len().saturating_mul(size_of::<ChildObservation>()))` before `Vec::with_capacity(paths.len())`. Failure propagates before reservation. The old per-slot charge is removed, so the array is charged once, with one collection-record allowance. The listing ceiling of 131,072 names and pinned 88-byte element size bound the payload to 11,534,336 bytes; multiplication cannot overflow the supported native usize. WorkScope::charge checks remaining ledger capacity before the allocation.

The census now charges that same array once immediately after listing and before observations. Its whole-file walker pin and SLOT anchor match the revised source; the native size inventory remains closed and consistent. The tight-budget native control verifies refusal after listing and before child observations, with the threshold covering the full payload. The structural check verifies charge/reservation order and its planted reversal is caught. These controls complement each other: allocation order is established by source inspection and the structural check, rather than inferred from final ledger totals alone.

**B2B3D-R1-NBO-1 addressed.** SCOPE now says the per-entry root term is removed while one per-walk root term remains. Census module documentation correctly describes the old probe cross-check as retired and the replacement probe as separately archived supporting evidence.

## Implementation assessment

Compared the complete r2 product-map contents with the reviewed r1 archive and inspected the changed charge/model/test/check sites. Core relative-key handling, scan adapters, native size assertions, listing conversion and the remaining walker redesign are unchanged from r1; the production delta for this round is the observation-array precharge. The previously assessed mechanisms remain sound:

- Core custody, markers, chains and enumeration read root-relative keys, with the empty key representing the selected root. Common-prefix removal preserves order. Resolved record paths and UnobservedAcl paths retain absolute construction, including root `/`; raw rejected specifications and absent paths retain their original construction. Behavioral vector files and expected records are unchanged.
- Frames, listed/verdict keys and retained scope keys carry no per-entry absolute spelling. One root spelling is retained in production. Child names are borrowed from one relative path; observations remain aligned in a parallel vector, and directory paths move on descent. Keys, validator temporaries, owned scope records, captures, caches and the observation array are charged before their allocations under the stated accounting model.
- ListingConversion keeps the bounded, precharged first invalid name, converts nothing after it, continues visits, and gives listing failures priority before constructing the terminal absolute refusal. Partial listings never drive observations. Traces/hooks remain absolute only under cfg(test); production stubs do not call spelling closures. Terminal refusal details retain their exemption. Descriptor-relative observations, custody ordering, identity comparisons and gitdir evidence are preserved.
- Existing test adaptations are limited to storage keys, population mapping and exact charge-count arithmetic. Behavioral expectations, traces and records are retained. New listing, tight-budget and structural controls exercise the changed mechanisms. The structural check is a concrete regression guard, not a general proof about arbitrary Rust code.

The census mirrors the revised charge sites, including the single array record instead of one record per observation. Closure pins, anchors and native sizes match. Dearer-branch capture costs, the explicit uninterrupted-read envelope, integrity verification, reference population and composed-workspace treatment remain intact. Its perRootByte is 1 for every censused lead-readable row; edges are unchanged from r1. The regenerated figures are consistent with the changed accounting.

The new supporting probe was rerun against r2. Its archived diff raises only throwaway limits and adds the ignored probe; all four successful measurements exactly equal the regenerated census's objects, edges and bytes at the measured 134-byte root. No stale probe dependency is retained.

The walker-only maxima are 1,476,438 objects, 1,007,224 edges and 358,480,897 bytes at R=4,096. Applying the smallest-power-of-two-at-least-2× rule gives 2^22 objects, 2^21 edges and 2^30 bytes, as stated arithmetic only. The sole failing entry against current provisional caps is `rs-very-large-aws-sdk-rust`, on objects. No overall, held-out or workspace full-ledger margin is claimed. No cap, law, production caller or environment read changes. Inventory remains 197 with 157 inventory successors; contract successors remain 164. B2-b and the entire plan remain incomplete; qualification is not granted.

## Verification

Independently ran only the expressly permitted checks in the candidate worktree:

- Operability source census: 114 rows, no findings.
- Environment exceptions: 10 tests passed.
- FW-01: 7 tests passed.
- Census controls: 18 tests passed.
- Walker storage checks: 5 tests passed, including the planted reservation-order reversal.
- Full census `--check`: both generated records verified. Held-out entries are skipped before store/overlay resolution.

Assessed supplied Rust/lane evidence without executing Rust or the lane. All 17 recorded check rows pass. The current Clippy command covers host, security and platform, all targets, with warnings denied; its log completes successfully. All five edited Rust files have base-clean and candidate-clean formatting classifications. The recorded earlier int_plus_one failure is disclosed and superseded by the successful current evidence.

Security preserves the identical 14 failures, with 1,124→1,128 passing tests; host preserves the identical eight failures and 343 passes. These are matching baseline failure sets, not whole-suite passes. The focused census log contains 56 native comparisons bounded in all three dimensions, 46 exact. Platform size controls pass. Each of the eight mutation logs matches its listed runtime test failures and contains no Rust compilation error; all five model mutations regenerated predictions. Existing scan, upward and walk vector-check logs verify the bound reference bytes. Candidate product-map pins remain exact after the permitted checks.

## Boundaries

No Cargo, rustc, Rust tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out store/overlay was accessed. Neither repository, candidate worktree, stage nor control files was edited. Only `REVIEW.md` and `review.json` in the requested directory were written. Lead assent/publication, product commit, inventory successor and subsequent cap recording/implementation remain separate actions.
