# C1a4 r1: the snapshot ledger's caps, their T2 margins and the constructor (M3-C r8 item 2, as M3-C r9 amends it)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

It implements C1a4 of the C1a plan: r4 is accepted (Codex `codex-c1a-plan-r4`), amended by r5 and r6, and r6 is accepted (Codex `codex-c1a-plan-r6`). C1a4 is gated on an accepted M3-C r9 law record of item 2 (PLAN-r6:9, RF-1). That gate is met: r9 was accepted by Codex in round 2 (`codex-m3c-r9-r2`) and published (`c1a-r9/RECORD-r9.md`; `PROPOSAL.md`:5).

r9's caps are **2^21 objects, 2^24 edges and 2^33 bytes**, conditional on C1a4 landing two classification remedies, (a) and (b-prime), exactly as r9 §6 states them. This unit lands both, with:
- the `snapshot_profile` constructor;
- the census closure re-pin;
- the lead-readable companion census and its margin test.

r9's one observation, M3CR9-R2-NBO-1, is carried here. Every displaced passage, changed file, regenerated artifact and receipt is listed exhaustively under *What it displaces*.

**Base:** product main `4ece849`, as the subject manifest names: C1a1 to C1a3, D2b-1 (inventory v218) and D2b-0 (contract successor 174, inventory v219) integrated. **The lane base is `23b3871`.** Main differs from it by three commits:
- D2b-0's code, `50f64cb`: `schemas/`, identity `schema.rs` and `schema_registry.rs`, host and storage `schema_sources.rs`, and host `tests/admission_tests.rs`;
- the contract-174 lock, `2b24f31`;
- the v219 lock, `4ece849`.

None of those paths is a C1a4 file, a census-closure file or a model pin. The lane is not repeated. On `4ece849`, the model `--check`, the operability source census and verify_design were rerun and pass (`evidence/rebase-4ece849/`).

## What it changes

| File | Change |
| --- | --- |
| `crates/security/src/snapshot_walk.rs` | **Remedy (a): the anchor scan's `.opensip` classification is reused.**<br>• `custody_state_anchor` becomes `opensip_name`, which returns `OpensipName {Other, Anchor, Classified {pruned}}`. It keeps its one charge, `classify_cost(path)`, asked only of a `.opensip` name.<br>• `enter` records a kept `.opensip`'s classification in a new `Level` field, `opensip: Option<(usize, bool)>`: its index, and whether a pruned tree holds it. A listing holds at most one `.opensip`, so an anchor removal and a recorded index never occur together.<br>• The walk loop, at the recorded index, neither charges `classify_cost` nor calls `rule::classify_path`, and uses the recorded result.<br>• The reuse is exact. Between the scan and the loop, `known` gains at most this directory's own Cargo root (the push follows the scan). `classify_path` tests a Cargo prefix only in front of a `target` segment, and every such prefix of `x/.opensip` is a strict ancestor of `x`. The member roots are fixed.<br>**Remedy (b-prime)'s charge:** `classify_cost(rel)` drops its member terms (`lists`, `member_segments`) and its `members` parameter; its doc comment says why. |
| `crates/security/src/custody/discovery_rule.rs` | **Remedy (b-prime):** `custody_state` compares each member root's segments with the path's in place (`parts[..k].iter().copied().eq(base.split('/'))`, k from a non-allocating count) and collects nothing. `classify_path`'s signature and results are unchanged for every caller: the snapshot walk, `discovery_walk.rs`, `discovery_scan.rs`, `workspace_declarations.rs`, `discovery_export.rs` and `host/src/discovery.rs`. This also corrects r9 §7's finding for discovery, whose `classify_cost` charges no member term, with no change to discovery's charges. |
| `crates/security/src/custody/discovery_rule_tests.rs` | Two tests: a multi-segment member root anchors only its own `.opensip` (not `a/bc/.opensip` or `ab/.opensip` for `a/b`); and `custody_state`'s source names no allocating conversion. |
| `crates/platform/src/work_ledger.rs` | **`WorkLedger::snapshot_profile()`**, beside `discovery_profile`, with `SNAPSHOT_OBJECT_LIMIT = 1 << 21`, `SNAPSHOT_EDGE_LIMIT = 1 << 24` and `SNAPSHOT_BYTE_LIMIT = 1 << 33`, citing r9. Like every ledger it has no `Default` and no `Clone`. **C1-T27:** at exactly the three caps it admits; one unit over in any dimension refuses as budget exhaustion, charges nothing and closes the ledger; and a ledger at its caps refuses the next unit. The test states r9's values literally. |
| `crates/host/src/snapshot_tests.rs` | The payload controls charge on the snapshot profile (C1-T27's second half): a stream is charged its buffer and its read attempts, and the 4 GiB probe (an ignored lane probe, run in the lane) is charged only those, at the final caps. |
| `tools/security/snapshot_ledger_model.py` | **The model terms that move:**<br>• `SNAPSHOT_ANCHORS`: `CLASSIFY` has no member fold; `ANCHOR_CLASSIFY` is re-matched against `opensip_name`; the new `ANCHOR_RECORDED` and `ANCHOR_REUSED` pin the reuse; `KIND_FREE_BOUNDARY` is re-anchored on the one-line exclusion.<br>• `SnapshotModel`: `classify` drops the member terms; `custody_anchor` records a kept `.opensip`; `walk` skips that name's second classification.<br>• The r8 constants `SNAPSHOT_OBJECTS` and `SNAPSHOT_EDGES` are gone: the caps are the profile's, read by anchor (`snapshot_caps`, which also pins the constructor's use of all three). The docstring says so. |
| `crates/security/src/snapshot_ledger_vectors.json` | Regenerated. **Only `opensip-anchors-root-and-member`'s prediction moves**, by −12 objects, 0 edges and −1,726 bytes, as r9 §6 predicted (`option3_r2.output.json`). The lane asserts this. The other 34 cases, the openers and every `exact` flag are unchanged; the pins change. `crates/host/src/snapshot_session_vectors.json` is byte-equal to the base. |
| `tools/security/snapshot_ledger_census.py` (new) | **The lead-readable companion census** (PLAN-r6 C1a4). It writes or checks `crates/security/src/snapshot_ledger_census.json`.<br>**Inputs:** it imports `discovery_census.py` and `snapshot_ledger_model.py` unchanged, and adds no store access of its own: every store is reached through `discovery_census.store_path`, held-out entries are never opened, and the blind mode is neither called nor changed. Item 5's bounds and sealing's charge sites are read by anchor from `snapshot_seal.rs` and the identity crate; the caps from the profile.<br>**Pricing** is r9's conservative pricing: no boundary, every blob new, sealing at its 4 MiB envelope, and the admitted D15 members (none).<br>**Eligibility:** over-item-5 is decided on the admitted extent's lower bound (r9 RF-3).<br>A `--report` mode prints the record with further cap sets, for evidence. |
| `crates/security/src/snapshot_ledger_census.json` (new) | The census record: 39 measured entries and workspaces, and 5 over item 5 (the same five as r9 §8, with the same evidence). The full-ledger maxima are 529,529 objects, 1,488,056 edges and 220,027,344 bytes (`poly-large-rspack`), equal to r9's. Every measured entry passes 2× at the profile's caps. Ids and counts only. |
| `crates/security/src/snapshot_walk_tests.rs` | **The margin test** (item 2: "B2-b's T2 census margin test is extended to the snapshot ledger's object, edge and byte caps"). Each lead-readable row is classified again against the compiled `snapshot_profile()`, on its full ledger at 2×:<br>• every measured entry must pass, and a failure returns the caps to the law;<br>• an over-item-5 entry claims no margin;<br>• the record's caps are the profile's own;<br>• the record covers discovery's manifest. |
| `tools/security/discovery_census.py` | The census closure re-pinned: the `CLOSURE` rows for `work_ledger.rs` and `discovery_rule.rs`. No charge or code path changes. |
| `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json`, `discovery_workspace_ledger.json` | Regenerated over the lead-readable cache through the tools' own `--write`. The diffs are:<br>• the two closure rows;<br>• for the census record, its 10 held-out rows, now `outstanding: held-out (blind receipt stale)`, and `heldOutMargin: outstanding`;<br>• for the workspace ledger, the census tool's pin.<br>No lead-readable charge or margin changes. |

## Lead decisions

- **LD-C1A4-1. (a) records only whether a pruned tree holds the name.** The walk loop needs only `is_some()` of the classification, so the `Level` keeps a `bool`, not the `PrunedAnchor`, and retains nothing uncharged.
- **LD-C1A4-2. (b-prime) changes `discovery_rule.rs`, an M3-B file in the census closure,** as r9 §6 decided.
  - Its behaviour is unchanged; the rule's reference vectors and cross-checks still pass, and the new tests pin the in-place comparison.
  - **The lead, as M3-B's law owner, accepts the edit through this unit's review.**
  - **It resolves r9 §7's finding for M3-B.** Discovery's `classify_cost` charged no member term, while `custody_state` allocated a segment list per member root on every classification. The allocation is now gone, so discovery's charge is exact with no change to its charges, vectors or caps.
- **LD-C1A4-3. The companion census record is a product file, with its own margin test,** as `discovery_census.json` is: ids and counts only, generated and checked by its tool, and classified again by a Rust test against the compiled profile.
  - The plan's "companion census's tool bytes" (PLAN-r6:11 step 2) are pinned in the record's `pins` (with the model, `discovery_census.py`, the member model, `snapshot_seal.rs` and `work_ledger.rs`).
  - The companion snapshot receipt, written by the blind validation unit, binds them in turn. They are not added to `discovery_census.py`'s `CLOSURE`.
  - **This is the lead's reading of PLAN-r6's phrase, for the reviewer to judge.** Either reading makes the discovery receipt stale here.
- **LD-C1A4-4. The blind receipt goes stale here, on purpose (LD-C1A-7; PLAN-r6:11 step 2).**
  - `discovery_rule.rs` and `work_ledger.rs` are closure files, and the receipt binds the closure and `discovery_census.py`'s own pin (`receipt_bindings`).
  - The receipt file itself is unchanged, and the regenerated census record shows every held-out row stale.
  - **The reviewed blind validation run follows as a separate unit** (PLAN-r6:11 step 3; B2-b4 plan r6 section 2.5): a pre-run Codex review of the companion blind mode, the lead's blind run, then a post-run Codex review. It refreshes the discovery receipt against the final pins and writes the companion snapshot receipt in the closed format. A held-out failure within item 5 returns the caps to the law (step 4).
  - This unit does not attempt it.
- **LD-C1A4-5. The payload controls move to the snapshot profile,** so C1-T27's second half ("a 4 GiB payload file is charged only its buffer and metadata") is shown on the final caps. The walk's other tests keep the discovery profile, which they use only as a test ledger.

## What it displaces (M3CR9-R2-NBO-1, exhaustively)

**Law (`snapshot-plan-c/PROPOSAL.md`, as r9 amends it; r9's note at :5):**
- item 2 "Ledger": objects 2^20 (:252), edges 2^21 (:253), and the byte cap's derivation (:254-259) are superseded by r9's caps;
- :261 (`WORK.BUDGET_EXHAUSTED`, and the census margin test extended to all three caps) stands, and is implemented here;
- C1-T27 (:300) stands, at r9's caps.

`PROPOSAL-r8.md`'s copies are history.

**Plan (`c1a/PLAN-r6.md`):**
- **Superseded:**
  - :10 (RF-2's cap-bounded term (a), departed from by r9 §5);
  - :17 (r5's adversarial figures within 2^20);
  - :20-22 (r5's rule and its item-5 recipe);
  - :24 ("Item 2's objects (2^20) and edges (2^21) are not changed");
  - :97 (the caps as 2^20 and 2^21, with a derived byte cap);
  - :165-166 (the byte cap as twice a linear program's maximum within 2^20 objects and 2^21 edges).
- **Stands:** :167's last sentence ("The census then measures the actual margins of all three (C1a4)"), which is this unit's census.
- **History:** the changes table at :51 (C1APLAN-R2-RF-1's linear bound) repeats the old formula. It is a round's history row and is left unchanged.

**Product code changed here:**
- `crates/platform/src/work_ledger.rs`: the `SNAPSHOT_*_LIMIT` constants and `snapshot_profile()` (new);
- `crates/security/src/snapshot_walk.rs`: (a), and `classify_cost`;
- `crates/security/src/custody/discovery_rule.rs`: (b-prime);
- `tools/security/snapshot_ledger_model.py`: the model terms above, with the r8 cap constants at its old :133-135 removed;
- `tools/security/discovery_census.py`: two `CLOSURE` rows;
- `tools/security/snapshot_ledger_census.py`: new;
- the tests: `work_ledger.rs`, `discovery_rule_tests.rs`, `snapshot_walk_tests.rs` and `host/src/snapshot_tests.rs`.

**Regenerated artifacts:**
- `crates/security/src/snapshot_ledger_vectors.json` (one prediction moves);
- `crates/security/src/custody/discovery_census.json` (closure rows; held-out rows stale);
- `crates/security/src/custody/discovery_census_vectors.json` and `crates/security/src/custody/discovery_workspace_ledger.json` (closure rows and tool pin);
- `crates/security/src/snapshot_ledger_census.json` (new).
- `crates/host/src/snapshot_session_vectors.json` is not regenerated: byte-equal.

**Receipts:**
- `crates/security/src/custody/discovery_census_held_out.json` is unchanged in bytes and stale from this commit.
- It and the new companion snapshot receipt are written by the blind validation unit.

**History, left unchanged:** r9's record and evidence (`c1a-r9/`), including its §9; C1a1 to C1a3's packages; the archived model copies.

## Checks

Lane r1, `evidence/c1a4-checks-r1/` (the lane of record, attempt 2), on main `23b3871` (the lane asserts the base checkout's HEAD equals the worktree's, and the base is clean), passed every check (`allPassed`, 24 rows):
- **the suites,** at base and candidate, with equal failure sets and no differing test:
  - host: 8 failures each side, 407 passed each, no new tests;
  - security: 14 failures each side, and 3 new passing tests (1,184 to 1,187);
  - platform: 0 failures, and 1 new passing test (321 to 322), run serially on both sides. That suite races under parallel test threads at base: D1a's lane of record and B2-b1 r2 run it serially for the same reason (`supervisor-d/d1a-r1/evidence/base-platform-flakiness.md`). **Attempt 1** (`evidence/c1a4-checks-r1-attempt1/`, history) ran it in parallel, and its candidate run hit the recorded `IO Safety violation` abort, so the comparison row failed. Every other attempt-1 check passed, and all eight mutations were caught;
- **a candidate-build preflight;** **rustfmt** on all six edited Rust files, each base-clean; and warning-denied all-targets **Clippy** on host, security and platform;
- **the focused tests:** the walk and its source, the rule, the discovery census tests (the closure as compiled), the ledger, and the session, custody and sealing tests. Also **the 4 GiB payload probe** on the snapshot profile (1 passed, 123 s);
- **the model's `--check`,** and **the vector moves:** only `opensip-anchors-root-and-member`, by −12 objects, 0 edges and −1,726 bytes, exactly r9's figure. The case list, the openers and every `exact` flag are unchanged, and the session vectors are byte-equal to the base;
- **the discovery census, workspace ledger and snapshot census `--check`s,** over the lead-readable cache only;
- **the census closure:** of its 19 files, exactly `work_ledger.rs` and `discovery_rule.rs` changed, **as expected**, and recorded as a pass. **The held-out receipt** is byte-equal to the base, and all 10 held-out rows of the regenerated census record are `outstanding: held-out (blind receipt stale)`, also as expected;
- **repository checks:** FW-01, the environment exceptions, the operability source census and its mint audit, and verify_design;
- **eight mutations,** each failing its focused tests:
  - (a): the recorded `.opensip` classified twice; the reuse misread; the classification recorded for the wrong child. Each is caught by the native-versus-model soundness control, and the misread also by the anchor control;
  - (b-prime): the member segments collected again, caught by the allocation pin; only the first segment compared, caught by the multi-segment control;
  - the profile: edges doubled, bytes halved, a discovery cap borrowed. Each is caught by C1-T27.

**The base, after the lane.** The lane ran on `23b3871`. The worktree and the subject are on `4ece849`, which adds only D2b-0's code and two lock commits, all disjoint from C1a4 (see *Base* above); the model, operability and verify_design checks pass there too.

## Not delivered

- **The reviewed blind validation run** and the two receipts (LD-C1A4-4): a separate unit, next.
- **A production caller:** `snapshot_profile` has none until J2b and J2c compose the walk, the session and sealing on it.
- **The inventory successor** for the two new paths: its own unit, after acceptance.

## Not claimed

- No caller, command, Plan or Run.
- No held-out margin. The held-out rows are stale until the blind run.
- No Linux claim: every test runs on this host's macOS family.
- No qualification. C1a's completion is not claimed: C1a4's blind validation, C1b and C1c follow.

## Inventory

New paths: `tools/security/snapshot_ledger_census.py` and `crates/security/src/snapshot_ledger_census.json`.
