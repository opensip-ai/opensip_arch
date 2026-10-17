# C1a4-blind r1: the pre-run gate, the companion blind mode and the blind validation run (C1a plan r6 RF-3, steps 2 to 4)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1. Nothing held out has been opened.**

It implements the blind validation C1a4 owes (C1a plan r6, RF-3).
- **Step 2 is done.** C1a4 landed the constructor with r9's caps, re-pinned the census closure and made the discovery receipt stale (product `57e5c48`; `c1a4-r1`, Codex ACCEPT-UNIT).
- **This gate is step 3's pre-run review.** One gated blind validation run, under B2-b4 plan r6 §2.5's procedure, measures every held-out entry against the frozen caps. It writes:
  - the discovery receipt, refreshed against the final pins;
  - a companion snapshot receipt, in the same closed format.
- **Step 4** is the outcome rule: a held-out failure within item 5 returns the caps to the law.

Following the B3-b3a2 precedent (and B2-b4c3's before it), this one gate reviews the tool and the run:
- the companion's new blind mode and its controls;
- the run plan (`RUN-PLAN.md`);
- the run script (`evidence/run_c1a4_blind.py`).

The run follows only after Codex accepts these exact bytes with `runAuthorized`. It carries both of C1a4's observations:
- **C1A4-R1-NBO-1:** the companion receipt binds the complete snapshot cost-source closure;
- **C1A4-R1-NBO-2:** the margin test checks row identity sets.

**Base:** product main `b753854` (C1a4 integrated, inventory v221 bound; D2b-0b integrated, 175 contract successors); architecture as the subject manifest names. **The gate freezes on it:** nothing else integrates before the run. C1b-0, which changes the generator closure again, is sequenced after the run (`RUN-PLAN.md`, precondition 4).

**Discovery's census tool is unchanged.** Discovery's blind mode runs as accepted (B2-b4c, B3-b3a2). Its receipt only needs refreshing, because C1a4 changed two closure files.

## What it changes

| File | Change |
| --- | --- |
| `tools/security/snapshot_ledger_census.py` | **The companion blind mode,** with the tool restructured around one `Census` class whose `measure` prices a tree for both the lead-readable and the blind rows (LD-C1A4B-1). New:<br>• **`--held-out-blind`**, which reaches each held-out store only through `discovery_census.held_out_store_path`, the one held-out join, with discovery's blind token;<br>• **its only effects:** the receipt `crates/security/src/snapshot_ledger_census_held_out.json`, and one line of counts on stdout;<br>• **every failure reduced to a class** (`INTEGRITY`, `POPULATION`, `MODEL`, `IO`) and discarded unprinted. A failing blind command line prints one generic line;<br>• **the closed rows** (LD-C1A4B-2): measured `{id, status, integrity, population, marginPermille, passes2x}`, over item 5 `{id, status, integrity, population}`, and error `{id, status, errorClass}`;<br>• **the receipt state:** `holds`, `fails` or `incomplete`, derived and validated;<br>• **the bindings** (NBO-1; LD-C1A4B-3): discovery's own receipt bindings in full; the four tools; **every product source the snapshot cost reads**, namely the snapshot modules the model pins, every file its walk and session anchors read, the session files, the ledger, sealing, the identity bound and encoding sources, and the depth bound; and the caps, item 5's bounds, the depth bound and the sealing bound;<br>• **`compose_held_out`:** the ordinary record composes the held-out rows from the receipt only while every binding equals the current inputs; any drift is `stale`;<br>• the record gains `heldOutEntries`, `heldOutMargin` and `capsStatus` (LD-C1A4B-4). A failing blind row is added to `failing2x` and returns the caps;<br>• **the population check:** the discovery walk model's scope must equal the reference population for every row, as discovery's own census requires (LD-C1A4B-1). |
| `crates/security/src/snapshot_ledger_census.json` | Regenerated over the lead-readable cache. The equality projection: added `heldOutEntries`, `heldOutMargin` and `capsStatus`; changed `counts.heldOut`, the tool's own pin and the standing text. **Every lead-readable and workspace row is byte-equal.** The ten held-out rows read `outstanding: held-out`, since no companion receipt exists yet. |
| `crates/security/src/snapshot_walk_tests.rs` | **The margin test, extended** (NBO-2):<br>• the record's lead-readable ids must be unique and equal discovery's compiled lead-readable repository rows and workspaces, in order;<br>• its held-out ids must equal discovery's held-out rows, in order, not merely the record's own counts;<br>• the composed held-out rows are classified in their closed formats, with the record's state the receipt's derived state and `capsStatus` consistent with `failing2x`. |
| `tools/tests/test_snapshot_ledger_census_blind.py` (new) | **21 hermetic controls,** modelled on discovery's B2-b4c ones:<br>• a canary in held-out names and content never reaching the receipt, stdout or stderr;<br>• each error class, and an over-item-5 entry's closed row;<br>• a held-out member as `MODEL`;<br>• the blind margins equal to the lead-readable measure;<br>• the command line's generic failure line, and abbreviated options refused;<br>• invalid receipts refusing;<br>• the lifecycle: survives regeneration; a failure returns the caps; incomplete; outstanding; and **drift in each of the seven bindings stale**, by value and by real bytes in a bound source, the tool and the member model;<br>• access: the ordinary mode touches no held-out store, and the join refuses outside the mode;<br>• **completeness (NBO-1):** the fixture's product holds only the bound sources and the census builds and runs there, and every product path the tool and the model name is bound. |

**Unchanged:** `discovery_census.py`, the member model, the snapshot model, the workspace ledger and every native file. So no census-closure file changes, and the discovery receipt's expected binding changes stay exactly C1a4's (`RUN-PLAN.md`).

## Lead decisions

- **LD-C1A4B-1. The companion's blind mode lives in the companion tool, and reuses discovery's join.**
  - It reaches held-out stores only through `discovery_census.held_out_store_path` with discovery's `_BLIND` token, verifies them with `verified_tree`, and checks the population with `reference_population`. It adds no store access of its own.
  - One `measure` prices a tree for both the lead-readable and the blind rows, and the lane's blind equivalence shows the two agree.
  - **Rejected:** a second blind mode inside `discovery_census.py`. That would change the tool discovery's receipt binds, adding `tool` drift beyond C1a4's, and put snapshot pricing into the discovery census.
  - **Accepted by the lead:** `discovery_census.py` stays byte-unchanged.
- **LD-C1A4B-2. An over-item-5 held-out entry is its own closed row** `{id, status: "over-item-5", integrity, population}`.
  - r9 classifies an entry over item 5 only on its admitted extent's lower bound. Such an entry cannot seal and claims no margin, so it is neither a pass nor a fail.
  - **The lead's ruling:** the owner's allowlist is "pass/fail and per-mille margins… no paths, names or counts". So the row may carry only `id`, the status `over-item-5` and `integrity`, and keep `population` only if it is a closed label, never a number or size.
  - **The result:** `population` is kept. It is the population check's boolean verdict, the literal `true` that a measured row carries too; `validated_receipt` admits nothing else in that row. The row carries no field, count, bound or size.
  - **Rejected:** reporting it as measured with conservative margins, which r9 forbids; and as an error, which would leave the gate open on a valid classification.
- **LD-C1A4B-3. The complete cost-source closure is bound directly** (NBO-1). The companion receipt's `snapshotSources` is computed from the model's own constants and this tool's anchors, not listed by hand, and a control shows the census reads nothing else. It is distinct from the record's six tool `pins`, which identify the tool bytes.
- **LD-C1A4B-4. The held-out rows are a separate `heldOutEntries` list** in the companion record, with `heldOutMargin` and `capsStatus`, so the lead-readable rows stay byte-stable. Discovery interleaves them in `entries`; the companion record has no held-out rows to keep in place.
- **LD-C1A4B-5. Inventory.** The gate adds one path (the controls) and the run adds one (the companion receipt). **Accepted by the lead:** one inventory successor after the run's bind, covering both.

## Checks

Lane r1, `evidence/c1a4b-checks-r1/` (the lane of record), on the frozen main `b753854` (the lane asserts that the base checkout's HEAD equals the worktree's and that the base is clean), passed every check (`allPassed`, 18 rows). **No held-out store was opened.**

**The earlier lanes,** on `3d1d771` before D2b-0b integrated, are history (`evidence/history-3d1d771/`). The first failed only Clippy's `explicit_auto_deref` on two `*row` dereferences, since removed; the second passed. No candidate byte changed between that second lane and this one.

This lane's results:
- **the security suite** at base and candidate: 14 failures each side, with no differing test. No new test (1,187 passed each side); the margin test is extended;
- **a candidate-build preflight,** rustfmt on the edited base-clean Rust file, and warning-denied all-targets Clippy on security;
- **the focused tests:** the snapshot census margin test and the discovery census tests (8 passed);
- **the controls:** the companion's 21 and discovery's 25 blind controls, and discovery's census controls;
- **the equality projection:** the companion record changes exactly as SCOPE states, and every lead-readable and workspace row is equal;
- **the discovery census, the workspace ledger and the companion `--check`s,** over the lead-readable cache only;
- **the blind equivalence:** the companion's `blind_row` over every lead-readable repository store (39), each presented as held out, equals the record's row, 35 measured and 4 over item 5. The program opens only lead-readable stores. Workspaces are not blind rows; no held-out workspace exists;
- **the census closure unchanged** (19 files, none hit);
- **the environment exceptions, the operability source census and verify_design;**
- **eight mutations,** each failing its focused tests:
  - **the receipt:** a bound source class unbound (the completeness and drift controls); freshness unchecked (drift);
  - **the blind mode:** the margins taken over the walk only (equivalence); the population unchecked (the error classes and incomplete); an over-item-5 entry measured (its closed row); the failure text printed on the command line (the generic line);
  - **NBO-2:** a consistently truncated record, and a duplicated id, each failing the margin test's identity sets.

## The run, after this gate is accepted

See `RUN-PLAN.md`. The run script pins the companion tool's bytes to this gate's `product-map.json` and the four unchanged tools to main's. It runs once, only after this unit's code commit is on main. It names every binding expected to change in both receipts.

## Not claimed

- **No held-out store has been opened.**
- No receipt, and no held-out margin.
- No product source change beyond the companion tool, its record, its controls and the margin test.
- No qualification.
