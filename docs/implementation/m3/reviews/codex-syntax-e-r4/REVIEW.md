# M3-E1 r4 review

**Verdict: ACCEPT.** No required findings and no new non-blocking observations. The revision records accepted outcomes and successor items, keeps SYN-NS proposals conditional, and preserves the accepted r3 rules outside its declared changes.

Subject: `docs/implementation/m3/syntax-e/PROPOSAL.md`, **133,352 bytes**, sha256 `ed4f1fec5a7e11293f48724e349afc0ca8bf9b7b2e46e761efac25a4f7d8764c`.

Diff base: `docs/implementation/m3/syntax-e/PROPOSAL-r3.md`, **117,273 bytes**, sha256 `d71031ff1aee01ba20b471e9db1891f4a0e976751741ffa10a783585eedd7c46`. Line references below use the pinned r4 subject unless another file is named.

## Pins and review boundary

Twenty-nine of the 31 request pins match their live files. The two moved sources were handled without substituting new authority:

- **SYN-NS:** the live README is now an r2 draft. The retained r1 README at `/tmp/opensip-implementation/reviews/codex2-syn-ns-r1/reviewed-subject/docs/implementation/m3/syntax-e/syn-ns/README.md` matches the requested **25,369 bytes** and full sha256 `5e0cb9394db15f15c369bfc96df509aa9fb948428965b5d98cde45fab2e36b1f`. Its exact bytes were copied to this review directory and used for the conditional record items.
- **Overnight log:** its live size and digest have moved, and its first 64,551 bytes do not reproduce the old digest. The request explicitly allows this live log to grow and directs checking the cited entries by title. All nine relevant entries were read and retained with their live coordinates and text digests. They corroborate the separately pinned E0 report, reviews and successor READMEs.

Product main is `218465fb71fd62ca01856d40d26ec822f45233be`, with **91 contract successors**. Read-only inspection of the lock and Git history confirms CRC-1 at `392499e` (83), CR-1 at `3fe7eb5` (89), SYN-1 at `682991f` (90), and SYN-1F at `218465f` (91). The record, subject-manifest, review and assent pins of those four bound units match current arch bytes; their reviews say ACCEPT-DESIGN-UNIT. This validates their recorded status, without treating design binding as product implementation.

## Requested decisions

**1. E0 — faithful.** Item 3 at line 192 records the report's actual gate: P5a's median per-file throughput is 0.818 MiB/s against the 1.0 floor, so P5 fails; P1–P4 and P6 pass. This selects T-native under r3's already accepted “any criterion fails” rule. The manifest uses `native-linked-v1`, and item 18's fallback posture applies. The non-product diagnostic does not select a different branch. The glance table, item 2, placement annotation, item 18, unit row and owner notes consistently record this result.

The inactivity rule is confined to provisions that apply **only to T-wasm**, and expressly identifies the governing T-native paragraphs in items 5, 11 and 18. It leaves native linked-Language and compiled-table admission, whole-closure retention, normalizer joins, tree validation, whole-file outcomes, operation budgets, size/node/depth bounds, the dedicated parse thread and fixed stack intact. A cross-branch check such as A7's refusal of a module under `native-linked-v1` remains applicable; it is not a T-wasm-only control. Parser crashes and allocation failures remain declared native residual risks, not guaranteed typed returns. No confinement claim or M4 entry condition is relaxed.

The runtime-source annotation at line 216 correctly records the omitted wasm headers and wasm-stdlib members as inactive. Eager compilation at line 263 and E2b's row remains a T-wasm obligation, with the report's allowed engine-identity/configuration alternatives. The eighth minimal-host crate is correctly identified as `bitflags` through `wasmparser`. The four full commits, release tags, generated ABIs, runtime ABI range and wasi-sdk archive digest at line 324 agree with E0's pinned Inputs and Substitutions sections. Fuel constants 190,000 / 420,000 and the 20,896-page ceiling remain relevant only if T-wasm returns. These are records of accepted probe evidence, not a rerun or qualification claim.

**2. ERROR — faithful and correctly attributed.** A11 at line 283 excludes 65535 (0xFFFF) from the contiguous `SymbolTableV1` rows. Item 10 at line 423 states the corresponding exception to an out-of-table symbol and routes a valid ERROR node to `syntax-error`, not `backend-fault`. This is E0's recorded exception. The stronger symbol/error-flag equivalence is attributed to bound SYN-1 LD-2, rather than represented as an E0-only ruling.

The bound SYN-1 NE:306 override confirms the exact law: ERROR is lawful exactly when the error flag is set; the table never lists it; ERROR_REPEAT 65534 is not lawful among visible nodes; and a malformed tree still yields `backend-fault`. E2b's obligation at line 742 includes that decoded validation law. The probe's byte layout is not adopted as normative.

**3. SYN items — faithful, with the acceptance boundary preserved.** The additions agree with the accepted SYN-1 r2 README, its bound record, and CODEX2's accepting review:

- A12 at line 284 covers kinds, fields and anonymous tokens named by a mapped level specification (E-7). The specific level bytes remain SYN-NS's pending work.
- The item-19 key checklist includes `-normalization-map-mismatch` (E-5), resolving E-R3-NB-02.
- Item 5, E3-T1 and the checklist use the **bare** `native.syntax-grammar-closure-absent` key (LD-4/LD-13, E-6). This keeps absence distinct from a named but unretained, malformed, misidentified or wrongly kinded closure.
- The SYN-1 row correctly records that no NEM change is needed (LD-6, E-4); the model continues to read the schema's cause registry.
- The unit-status cells report SYN-1 and SYN-1F as accepted and bound without claiming their E2s/E2b implementation complete.
- E2s's I1-a prerequisite or combined identity-source change at line 741 matches both READMEs and NB-SYN1F-1. It prevents materializing SYN-1F from a source that drops I1-L's carried member.

The SYN-NS-dependent changes are explicitly **pending SYN-NS acceptance**: item 6's selection time at line 324 (E-10), item 13's specification ownership at line 500 (E-11), and item 14's per-level placement at line 519 (E-9). The retained r1 LD-NS1/2/3 passages support those proposals. The revision's introductory rule says they bind only after acceptance and may change in that review. The A12 acceptance already settled by SYN-1 does not accept any particular SYN-NS table. E2c still waits for accepted SYN-NS before freezing its fixtures.

**4. X-C1 and X-C2 — faithful.** The named C r7 passages are the accepted bytes:

- **C:431–443, item 9:** the same core provider identity has its existing import use plus syntax-universe producer use, and belongs to `semanticClosures` exactly when a syntax universe is selected. The adapter remains import-only.
- **C:470–471 and the continuation of C2-T13a:** C2-T13 now tests conditional membership, and C2-T13a tests the allowed syntax fields and forbidden non-syntax uses.
- **C:905 and its following bullets, item 16 step 12:** C4a builds the Plan-selected `clones-near` census.
- **C:954, C4-T21:** the fixture checks code-path census, explicit scope additions, an explicit empty census, and the syntax producer/stage.

These agree with the annotations at lines 79, 614–615 and item 19. C5:409–411 and C5:435 resolve to the former import-only restriction and unconditional core-provider membership refusal in the accepted r5 snapshot. They are correctly used for the historical conflict that X-C1 amended. C r7's effective-with-L gate remains stated; binding CRC-1/CR-1 does not by itself declare all C code ready.

**5. Re-pins — sound.** Read-only Git extraction of the three named historical arch commits reproduces the live files r3 cited. Removing their two-line acceptance insertion reproduces the pinned M3P r6, M3P r4 and B r2 snapshots exactly. Every old M3P/B line range checked therefore retains its bytes at −2, including M3P 214→212, 303→301, 322–332→320–330, M3P-r4 299→297, and B 411→409, 480–481→478–479, 674→672. The reviewed history tables retain their coordinates and have an explicit wrapper-offset explanation.

The substantive C r3→r7 mappings checked are byte-identical: 93→138, 114→176, 282–302→360–380, 318→396, 320→398, 403→501, and the C2a unit row 933→1086. The item-9 basis now correctly uses r7 414–443, which contains the accepted X-C1 expansion, while historical restrictions use C5. The correction from C item 8 to **item 10** identifies the same syntax-context assignment; it changes no owner.

L r1:132 is item 2's “No in-process fallback” bullet, retained in r5 at line 378. L r1:494–506 is item 17's launch-rule ownership and gates, retained with the accepted D-state update in r5 at lines 898 onward. Item-based references preserve the provisions E relies on and follow L X10.

**6. Scope — no undeclared change found.** All **76 diff blocks** were inspected, including character-level differences in long rows. They map to the nine r4 change-table rows: revision metadata, E0's outcome/record items/pins, accepted or conditional SYN items, X-C1/X-C2 status, L item references, and snapshot citation repairs. The 20 decisions, code-unit sizes/durations, second-integrator rule, candidate retention limits, admission ownership, outcome routes and remaining controls retain r3's behavior except for the explicitly sourced record changes.

The product citations remain explicitly based on `3e64266`. Among the existing implementation/registry/schema files cited as evidence, read-only Git comparison confirms only Cargo.toml and Cargo.lock differ at the named main. The revision does not silently rebase those citations onto P0. E3's day-14 schedule and the conditional host-chain figures remain r6 planning coordinates, not a new schedule decision.

## Prior observation and acceptance scope

E-R3-NB-02 and E-R3-NB-03 are addressed. **E-R3-NB-01 remains open**, exactly as the request declares: E3-T9's “add one member to any group” wording does not isolate the union cap when a full 4,096-member group is grown. r4 leaves that control unchanged; its accepted operative retention rule remains intact. This review does not close that prior observation or require an unrelated control edit in a record revision.

Acceptance covers only this pinned M3-E1 r4 law/contract record revision. SYN-NS retains its separate ACCEPT-DESIGN-UNIT review, and code/inventory units retain their own acceptance gates. No inventoryCandidateAssessment is supplied.

Evidence is retained in the pin checks, exact subject/base copies, diff and change blocks, recovered SYN-NS snapshot, citation/shift assessments, source-review and binding assessments, product history, and title-selected overnight entries. All computation was static read-only inspection using scratch Python scripts at nice -n 19 with -I -B. No product or owner code was executed. No Cargo command, product build, test, verifier lane, network access, delegation, repository edit, commit, push, real OpenSIP-home access or 413-fixture access occurred. All new files are confined to this review directory.

