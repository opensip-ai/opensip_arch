# J2a inventory137

Adds exactly two sources to inventory136 (unit X3a-2, selected at product cca4fe4 and still at d2c00a9, where no later unit has an inventory successor):
- crates/host/src/invocation_tests.rs
- crates/host/src/outcomes_tests.rs

It keeps all 971 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 973 planned files. No crate or dependency is added; both rows are in the existing `opensip-host` package. The rows belong to unit J2a of the accepted host-pipeline law M3-J1 r5 (`m3/host-pipeline-j/PROPOSAL-r5.md`, item 14): the pure invocation model and the M3 outcome matrix.

- **invocation_tests.rs (test)** is `invocation.rs`'s cfg(test) module: the three M3 requests and their step lists, WS section 1's step-list rules on the WFC refusal cases, the join chains, the cancel phases (with lead decision LD-r5-1), the cancellation source, 8.3's precedence rules, the final output section and settlement, on the WFC cases M3's step lists express.
- **outcomes_tests.rs (test)** is `outcomes.rs`'s cfg(test) module: item 10's rows, each validated against the selected common-v4 `StepTermination`; rows 56 and 57 (contract successors SD-5 and SD-7); NE section 10's deficiency bridge and public route registry, restated; the subject bound; and the D9 v1.14 goldens of the analysis path.

**Order.** This successor's parent is the inventory the real product lock selects: inventory136 at d2c00a9. `evidence/build_v137.py` reads the parent from the lock, checks every meaning the lock binds to it, writes only its two paths, refuses tracked paths, and refuses while a lock selects inventory137. Reruns reproduce the same bytes.

**Changes to existing rows.** The unit's production files are planned rows; no row is added for them:
- `crates/host/src/invocation.rs` is new bytes for a row planned since the original inventory ("Execute the bounded step/attempt DAG and apply dependency, retry and cancellation rules."). J2a writes its pure model: the typed request (R1), the step lists, the join chain, the cancellation source and phase recording, and settlement. J2c and J3d drive it.
- `crates/host/src/outcomes.rs` keeps the metadata ingress and gains item 10's total projection, the deficiency bridge, the route and origin tables, and the aggregate of WS:233-240. Its planned row ("… map typed host boundary observations and aggregate step outcomes under their existing owners …") describes that.
- `crates/host/src/lib.rs` declares `invocation` and keeps both modules crate-private (`#[allow(dead_code)]`, library only). Nothing new is public.

No description successor accompanies this inventory: each changed row still describes its file.

**Projection: one hundred and three rows.** Once inventory137 is selected, inventory136 becomes an ancestor, and every description meaning the lock binds to it is inherited by stable file path:
- the one hundred inheritance rows inventory136 projected (inventory135's one hundred, re-parented at X3a-2's integration: the sixteen carried unchanged from inventory81 onward, D1's thirty-nine overrides with D2's four supersessions folded, and D3's forty-five overrides with its seventeen supersessions folded);
- the three direct overrides of the bound description successor `read-endpoint-x3a2-descriptions` on inventory136 (installation_records.rs, installation_selection.rs, native_marker.rs).

No bound contract successor has a passage supersession on inventory136. Of the projected rows sorted after the inserted paths, one moves by one and eighty-seven by two.

- `verify_projection.py` is inventory136's helper with the row count and its comment updated for this parent. It runs against the real lock at d2c00a9: PASS, 103 rows, 518 corruptions refused.
- `evidence/stage_lock_j2a.py` stages the lock change in the J2a worktree, as P0 staged inventory135: HEAD's `design-lock.json` plus the inventory137 entry, with the one hundred and three inheritance rows re-parented to inventory137. The parent, candidate and record pins are real. The review and assent pins are `SCRATCH-J2A/` placeholders, which integration replaces with the accepted review and the completed unit record.
- `evidence/verify_scratch.py` checks the staged lock (or, on an unstaged worktree, applies the same change in memory). It requires the staged lock to equal HEAD's plus exactly that change, serves a synthetic review and assent for the two placeholders, and runs the worktree's real `verify_design` (VD2-a's) on the lock without J2a and with inventory137. It requires verify_design's own projected inheritance to equal the record's, and the contract successors and both supersession counts to be unchanged. It also checks that plain `verify_design` refuses the staged lock at `SCRATCH-J2A/review.json`, as it must until integration.

**Parallel units.** Unit E2a's inventory successor is to be built on this one, as inventory138. This file set is final: a change to it would change this candidate's bytes and every pin built on them.
