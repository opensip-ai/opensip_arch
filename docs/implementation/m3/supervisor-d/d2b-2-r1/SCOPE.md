# D2b-2 r1: the transition tables as data, and their engine (M3-D r5 item 10; D2b plan, sub-unit D2b-2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements sub-unit D2b-2 of the D2b plan (`../d2b/PLAN-r3.md`; LD-D2B-1, LD-D2B-4): the table engine over the vendored P3T, the carriers' Rust overlay and T2O. It is library only, with no caller. The per-frame contextual admission that runs before the table (LD-D2B-15) is D2b-3's and D2b-4's; this engine gives them the event input.

**Base:** product main with D2b-1 integrated, as the subject manifest names.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/provider_protocol/table.rs` (new) | **`Table::load(Protocol)`.** The base table (P3T for `Rust3`, T2O for `Ts2`) is a byte copy embedded with `include_bytes!` and checked against the carriers' own `sourcePins` entry (`p3`, `ts2order`) by SHA-256 and length, so no pin is restated in code. Its rows, initial state, set wildcard (`*PRE_COMPLETE`, `*PRE_TERMINAL`), process-observation frames and catch-all rows are read from it. **The prose laws are pinned:** the pre-match law, the no-match law and every state update's `sets` text must equal, exactly, a law the engine implements, and the stage-dependent next must be the one it implements, or loading refuses (`TableRefusal::Law`). **The Rust overlay** is the carriers' `protocols.rust-semantic.transitions` (published as `p3-guard-successor.v1.json`): its state additions, its update additions (applied after the parent's), its guard additions (P3-25's `outputSeen: false`), and its Cancel position (`hostMaySendInStart: false`). An unknown overlay member refuses. T2O's carrier entry must state no overlay.<br>**`Run::step(&Event)`,** the references' interpreter: the pre-match law in its order (FAULT absorbing; a post-terminal frame in WAIT_ZERO_EXIT, WAIT_EOF or DONE; a process observation, to the table's own catch-all row), then first match on phase or set wildcard, frame and guard (guards see the state and, for T2O, the derived event observations the table lists), the total fallback to the other catch-all row, and on a match the frame's updates, the overlay's additions, the resolved next (`ANALYZING_OR_READY_COMPLETE`), the terminal and the trace entry.<br>**`Event`** carries the frame and the host-derived observations the updates and guards read: `identityNegotiated` on HelloAck, the two modes on OpenUniverse, the stage count on Analyze, and TS2's `unavailablePayload`. None is a wire member; the codecs derive them (LD-D2B-15, LD-D2B-18). |
| `crates/components/src/provider_protocol/table_tests.rs` (new) | 6 tests (below). |
| `crates/components/src/provider_protocol.rs` | `pub mod table`. |
| `crates/components/data/protocol3-transitions.v1.json`, `typescript-protocol2-order.v1.json` (new) | Byte copies of the architecture's P3T and T2O (`docs/coop/design-corrections/native/`), pinned by the carriers. |
| `crates/components/tests/data/table-vectors.rust3.v1.json`, `table-vectors.ts2.v1.json` (new) | The reference's outcomes (D2b-T1), built by `evidence/build_table_vectors.py`: 18,367 Rust3 and 2,810 TS2 nodes of a prefix tree, and native-cases.v2's six `protocol3_run` cases. |

## The vectors

`evidence/build_table_vectors.py` runs the reference interpreters unchanged: trial 07's `tools/admission_ref.py` `overlay_run` (P3T with the carriers' overlay, the production major-3 table), `native_evidence_model.v2.protocol3_run` (the base P3T) and `provider_startup_model.v1.typescript_protocol2_run` (T2O). Each function and the module constants it reads are extracted from the module's source with `ast` and executed alone: the startup model imports `referencing` at module level, which its interpreter does not use and this environment does not have.

The traces are a breadth-first exploration of each table's reachable live states (the shortest path to each), each extended by every event of the alphabet (every frame a row names, the four process observations, `zero-exit`, `eof` and one unknown frame), under the observation variants the tables read: HelloAck negotiated or not, OpenUniverse's four mode combinations, Analyze under one and two stages, and TS2's Unavailable payload before and after Analyze. One fallback-then-event probe per state checks absorption. Trial 07's scripted transition traces are added as nodes. Each node records the reference's trace entry for its last event and its state after it. Where the base table and the overlay differ (P3-25 after output, 16 nodes), the node records the base table's outcome too.

## The tests

- **D2b-T1, Rust3:** all 18,367 nodes step to the overlay runner's trace entry, phase and terminal, and to the base runner's `sourceBytesSent`, `stagesCompleted` and `identityNegotiated`; every one of the 34 row ids is reached, both catch-alls included.
- **D2b-T1, TS2:** all 2,810 nodes, likewise, with `cancelPhase`; all 23 row ids are reached.
- **The native cases:** native-cases.v2's six `protocol3_run` cases, whose own expectations the builder asserts for the base table, replay under the overlay to the overlay runner's traces.
- **The overlay:** Unavailable after output faults (P3-34) under the production table, before output it is P3-25; Cancel in START is P3-34 under major 3 and T2-18 under TS2.
- **Disjointness:** rows sharing a phase (or set wildcard) and a frame have mutually exclusive guards, so first match resolves no ambiguity (both tables' match law).
- **Closed loading:** a base table that is not the carriers' pin refuses (`Pin`); a prose law the engine does not implement refuses (`Law`), with the pin re-pointed so the content is what is judged; an unknown overlay member refuses.

## Checks

Lane r1, `evidence/d2b-2-checks-r1/`, on main `23b3871` (D2b-1 integrated, inventory v218 bound), passed every check (`allPassed`):
- **the components suite** at base and candidate: 0 failures each side, 35 → 41 passing (6 new);
- **rustfmt** on the new files, and warning-denied all-targets Clippy on `opensip-components`;
- **the table tests;**
- **the vectors regenerated** byte for byte from the references (`build_table_vectors.py --check`);
- **the vendored tables** equal to the architecture's bytes;
- **the package edges** under the O1-a package policy (unchanged: `opensip-contracts` and `opensip-identity`);
- **repository checks:** the environment exceptions, the operability source census, the census-closure check (no closure file changed) and verify_design;
- **mutations,** each failing the table tests:
  - a row skipped at load;
  - the fallback not total (an unmatched event left in its phase);
  - the overlay's guard additions dropped;
  - FAULT not absorbing;
  - the post-terminal law dropped;
  - process observations matched as frames;
  - the stage-dependent next resolved without its increment;
  - the HelloAck negotiation ignored (every HelloAck taken as negotiated).

## Not claimed

- No caller, no codec, no contextual admission (D2b-3, D2b-4).
- No process supervision: `zero-exit`, `eof` and the process observations are D3a's to feed (LD-D2B-6).
- No qualification; D2b's completion is not claimed.

## Inventory

New paths: `crates/components/src/provider_protocol/table.rs`, `table_tests.rs`, the two vendored tables under `crates/components/data/`, and the two vector files under `crates/components/tests/data/`.
