# D2B-2-r1 review

**Verdict: REQUIRED-FINDINGS.** Two closed-loading corrections are required. No nonblocking observations.

## Exact subject

Verified the 8,480-byte manifest SHA-256 `4aa010746720f0ba83ea1fba326b844d0d3e6fc4370544c17fb7058878a65b4c` and all 37 members. All seven candidate product-map files and archived copies match their recorded sizes and hashes; the existing parent provider_protocol.rs matches the base. The candidate is detached at `23b3871269c6553c96097084dd412b3aa95dec68`, with exactly the mapped changes (six new paths). Authority and design-lock pins in source.json match.

Both vendored tables are byte-identical to their architecture authorities and match the carriers' own p3 and ts2order size/SHA-256 pins. Vector reference-source hashes also match. No table pin is restated in engine code.

## Required findings

### D2B2-R1-RF-1 — Validate the stage-dependent law value, not only its key

`crates/components/src/provider_protocol/table.rs:233`

load_from verifies that stageDependentTransitions has exactly the ANALYZING_OR_READY_COMPLETE key, but never reads or compares its value. Both published tables put the actual increment-and-resolve law in that value. Keeping the key and changing its value to arbitrary prose, a different increment rule, or even null still passes this check once the carrier-owned table pin is updated; Run::step continues to execute its hard-coded increment-and-resolve behavior. This contradicts the request and SCOPE claim that the stage-dependent next is pinned exactly and that an unimplemented prose law refuses Law. The existing unknown-law control mutates a state update, so it does not catch this omission. Current pinned-table traces are not shown to diverge; the defect is the required closed-loading guard.

**Required correction:** Compare the complete stageDependentTransitions mapping, including the protocol-specific prose value, against the exact law implemented by the engine. Refuse unsupported values with TableRefusal::Law. Add loading controls for both protocols that change the value while preserving the key and update the carriers pin/length so content validation, rather than Pin refusal, is exercised.

### D2B2-R1-RF-2 — Require TS2 to declare the supported no-overlay descriptor

`crates/components/src/provider_protocol/table.rs:338`

The TS2 branch checks only that an overlay key exists and guardAdditions does not. It never validates the overlay value, the TS2 base pin/rule count, or other transition members. Replacing the current none declaration with an unsupported overlay string or null is accepted. Adding stateAdditions or stateUpdateAdditions is also silently accepted and ignored, provided guardAdditions is absent. Thus the loader can report success while disregarding a declared TS2 transition overlay, contrary to the requested no-overlay check and closed-loading behavior. The Rust unknown-overlay-member test does not exercise this branch.

**Required correction:** Validate the TS2 base descriptor and require the exact supported no-overlay declaration (or an equally explicit closed representation of none), with a closed set of supported transition members. Reject a non-none declaration and unsupported executable overlay members instead of ignoring them. Add controls for altered overlay values, unexpected update/state members, and incorrect base metadata; preserve the current payload-selection/contextual-admission boundary.

## Implementation and differential assessment

Apart from the loading gaps above, no mismatch was identified for the currently pinned tables. The engine checks pre-match and no-match prose exactly and maps supported state-update sets strings to implemented operations. It reads initial assignments, rows and guards, wildcard phases and process frames from data. The Rust overlay's current state additions, update additions and P3-25 outputSeen guard are applied; hostMaySendInStart=false preserves P3-29's exclusion of START. Unknown Rust top-level overlay members refuse. These checks do not substitute for the missing stage-law and TS2 overlay validation.

Run::step follows the reference pre-match order: FAULT absorption, post-terminal frame refusal, then process-fault catch-all. Ordinary matching preserves first-row order, exact frame and phase/set-wildcard membership, with state guards and only declared TS2 event-observation overrides. No match takes the total fallback. Matched updates precede overlay additions, stage-dependent next increments both counters, terminalKind is set when declared, and the resulting phase and trace id are returned. The current parent and overlay updates are compatible with the reference's assignment order.

Event's inputs are the codec-derived negotiation result, derived dependency/prepared modes, invocation stage count and TS2 unavailablePayload observation. They are not parsed here from wire booleans. LD-D2B-15 contextual admission and LD-D2B-18 exact token-array validation remain D2b-3/-4 obligations; the reference engine's token-presence boolean does not authorize accepting a bad HelloAck. Process events remain D3's responsibility. No caller currently composes these APIs.

The vector builder extracts the named reference functions and their actual global constant assignments in source order with ast, supplies their required json/copy/Path/HERE globals, and avoids unrelated module imports. The interpreter bodies are retained. The added postponed annotations do not change the executed transition logic. OpenUniverse defaults in native-case inputs are explicitly aligned between the base and overlay runners, as documented, rather than treating their differing absent-mode defaults as equivalent.

The breadth-first exploration covers representative reachable live states for stage counts one and two, then extends each by every row-named frame, process observation and Unknown. Observation variants cover negotiation, all Rust mode combinations and both TS2 Unavailable payload variants. The hidden key preserves token/mode/output/coverage distinctions needed by current guards; fallback-then-event probes check absorption. The exploration is a finite differential over the current tables, not a proof over arbitrary future table languages or arbitrary stage-count inputs.

The two prefix-tree files contain 18,367 Rust3 nodes and 2,810 TS2 nodes. Rust phase/terminal/trace expectations come from overlay_run; source/stage/identity expectations come from the base reference where shared. Native cases assert their original base expectations and replay six overlay traces. Rust base/overlay differences are retained as annotations. Replay tests check every declared row id, including both catch-alls; the separate disjointness test checks overlapping phase/frame guards. The focused overlay control covers Unavailable before/after output and the different START Cancel table behavior. Closed-loading tests currently cover a bad pin, an unsupported update law and a new Rust overlay key; they need the controls requested above.

## Lane and independently executed checks

The recorded lane reports and logs agree:

- Components: **35 base / 41 candidate passing tests**, equal empty failure sets and six new passing tests.
- All **six focused table tests** pass.
- Warning-denied all-targets Clippy and rustfmt pass; no base-dirty formatting exclusion is recorded.
- Vectors regenerate, and vendored-table equality passes.
- Package edges remain contracts and identity, both normal. Environment-exception tests (10), operability, closure-unchanged and verify_design pass.
- All **eight mutants** compile and produce actual test failures: omitted row, non-total fallback, dropped overlay guard, lost FAULT absorption, missing post-terminal check, process events matched as frames, stage resolution without increment, and ignored negotiation. The runner restores original bytes; the rehashed candidate matches the package.

After inspecting the builder's nonwriting --check path, independently ran exactly its permitted lane invocation:

`python3 -I -B <package>/evidence/build_table_vectors.py <architecture> <candidate> crates/components/tests/data --check`

Result: **current []**, both vector files reproduced byte for byte.

Also ran `python3 -I -B tools/check_operability.py source --repository .` in the candidate: **passed, 114 rows, no findings**. Rust builds/tests, Clippy and the lane were not rerun. The two required findings are source-derived loading counterexamples, not claimed executed Rust tests.

## Rules and inventory

The mapped source adds no mint-census call, environment read or let-underscore discard. The seven changed paths intersect none of the 19 census-closure files. provider_protocol.rs only adds the table module declaration; accepted D2b-1 mechanics remain outside the code changes.

The six new inventory paths are table.rs, table_tests.rs, the two vendored table JSON files and the two table-vector fixtures. No codec, contextual admission, process supervision, production caller, completed D2b or qualification is claimed.

Only REVIEW.md and review.json in the requested directory were written. Neither repository, worktree nor control files were edited. No Cargo, rustc, build, lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key, held tree, T2 store or T2 cache was read.
