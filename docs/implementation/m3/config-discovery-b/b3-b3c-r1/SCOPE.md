# B3-b3c r1: the D15 workspace margins (M3-B unit B3-b, sub-unit B3-b3c)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

It implements B3-b3c of the B3-b plan r2, §4.3 (unchanged by amendments A1 to A5):

> Each T2 workspace row's full-ledger cost is its walker cost (members entered) plus the reader term plus the member term at its member count. Each must hold the 2× margin under the r7 caps. If any row fails, the caps return to the law, as item 12 requires; nothing is truncated. Held-out workspace rows go only through the blind mode.

**Base:**
- product main `fb63a93`: B3-b3b bound, with the held-out margin holding on the full ledger; inventory v208, 170 contract successors;
- architecture `f6b561d75`.

**No product source change.** The census tool, the member model, the T2 link controls, both census records and the blind receipt are byte-identical to the base.

## What it delivers

### A companion record, `discovery_workspace_ledger.json`

**`tools/security/discovery_workspace_ledger.py` is new.** It imports the bound census tool and member model and adds no charge of its own. For each lead-readable T2 workspace, it:
1. **verifies the members and the overlay** through the census's own `verified_tree` and `verified_workspace`: integrity, the overlay record's digest, its archived copy, and its mounts;
2. **builds the D15 shape:** the workspace as D15 discovers it, per control (b) of plan §3:
   - the verified overlay root, with the members mounted;
   - each member a conventional Git repository: a `.git` directory, which the walker prunes and item 6b charges at its ceilings whatever it holds;
   - W in no repository;
   - the reader carrier rendered from the overlay's link map, by `t2_link_controls.carrier`:
     - for Cargo it must equal the cache's FETCH-SPEC §6 file byte for byte;
     - for npm it is law item 20's `package.json`, and the overlay must not hold one already;
     - Python has no D15 reader at M3, so no carrier;
3. **composes it under both declaration branches,** through the census's `d15_terms` with every source at its envelope (`ENVIRONMENT_ENVELOPE`, the system sources at their cap):
   - **`automatic` (branch B):** the members the carrier's entries place, links before the walk;
   - **`configWorkspaceRoots` (branch A):** every member mount as a configured root, so item 6b is paid at the workspace's whole member count. The tool refuses unless all are admitted. Links come after the walk;
4. **records, per branch,** the admitted members, the walker with them entered, the three terms and the full ledger (`d15_row`, the census's). A workspace holds only when both branches hold. `failingWorkspaces` and `caps` follow item 12.

The record also carries the census's manifest pin, closure, sizes, limits and root lengths, and pins the four tools.

### The classification

`every_t2_workspace_full_ledger_is_classified_against_the_profile_limits` (in `discovery_census_tests.rs`) classifies the record again. It checks:
- that it is the census's companion: the same manifest, closure, sizes, limits and root lengths, and the same workspaces with the same members in the same order;
- branch A's admitted members equal the workspace's members, and branch B's are a subset;
- per branch, the full ledger is the walker plus the three terms, classified at 2× at the widest root length;
- each row's verdict, `failingWorkspaces` and `caps`;
- the full claim: no workspace fails, and the census's `caps` is `recorded-margin-holds`.

## The result

| Workspace | Members | B: admitted, margins ‰ (objects / edges / bytes at 4,096) | A: admitted, margins ‰ |
| --- | ---: | --- | --- |
| mr-rs-medium-serde-json | 2 | 1: 1,362,229 / 5,899 / 42,683 | 2: 1,086,888 / 5,904 / 23,090 |
| mr-rs-large-aws-lambda-tokio | 8 | 7: 210,314 / 5,326 / 6,770 | 8: 161,462 / 5,568 / 5,972 |
| mr-ts-large-smithy-powertools | 2 | 1: 187,849 / 5,399 / 33,847 | 2: 126,008 / 5,633 / 19,877 |
| mr-ts-very-large-smithy-sdk | 2 | 2: 10,867 / **2,630** / 6,546 | 2: 11,172 / 3,842 / 7,484 |
| mr-py-medium-boto | 2 | 0: (no carrier) | 2: 57,371 / 5,351 / 17,138 |

**Every workspace holds 2× on the full ledger under both branches, so the caps stay recorded.**
- The tightest is mr-ts-very-large-smithy-sdk's branch B edges, at 2,630‰. Its walker alone, in the D15 shape, is about 439,500 edges. Item 6b's session adds about 357,000: mostly the environment envelope, `ARG_MAX / 3` entries, one edge each, paid once per session.
- The tightest bytes are mr-rs-large-aws-lambda-tokio's branch A, at 5,972‰: eight members with their indexes read and decoded at 4 MiB.

## Lead decisions

- **LD-B3B3C-1. A companion record, not a census change.** The blind held-out receipt binds the census tool's bytes (B2-b4 plan r6 §2.5). Editing `discovery_census.py` would make the B3-b3b receipt stale on main, and a fresh blind run would be needed. Amendment A1 rejects that: one gated refresh, over the final closure. So the workspace full ledgers are computed by a new tool over the census's own model and written to their own record. The receipt stays current, and the census `--check` keeps `heldOutMargin: holds (blind census)`.

  **Consequence:** the census record's workspace rows keep their walker-only fields and their now-superseded string `fullLedgerMargin: outstanding: walker only until the B3-b member-observation bound`. The companion record carries the full ledger, and the Rust classification ties the two together: same inputs, same workspaces and members, and the joint caps claim. The string is corrected the next time the census tool changes for other reasons, together with a gated blind run.

  **Rejected:**
  - changing the census tool now, which would cost another blind run;
  - changing the receipt's bindings, which would weaken B2-b4c's staleness rule.
- **LD-B3B3C-2. Both declaration branches, the verdict on both.** §4.3 says "the member term at its member count". Branch B admits only the members that the carrier's entries place, which are the providers: 1 of 2 for serde-json, and none for Python, which has no reader. Branch A, with every mount configured, admits all. The two branches walk differently: branch B probes markers for the automatic population. Each is a way D15 composes the workspace, so each is reported, and the row holds only if both do.

  **Rejected:** branch A alone. It is the whole member count, but branch B's walker is dearer in edges on the tightest workspace (439,526 against 188,061 for smithy-sdk).
- **LD-B3B3C-3. The D15 shape is the corpus's workspace with conventional members.** The T2 workspaces are `vcs: none` compositions, and D15 admits only repositories. Plan §3's control (b), accepted in B3-b2b2c, gives each member a synthetic conventional `.git`; this shape does the same.
  - Item 6b's cost does not depend on the repository's content: it is charged at its ceilings (LD-B3B3A1-3).
  - The walker prunes `.git`.
  - The carrier is the overlay's rendering, as the link controls use it.

  B3-b3a1's measured-against-model control covers the model on Git members created by `git init`. This unit adds no native measurement of the T2 workspaces themselves.

## What changes

| Path | Change |
| --- | --- |
| `tools/security/discovery_workspace_ledger.py` | **New.** The D15 workspace margins. |
| `crates/security/src/custody/discovery_workspace_ledger.json` | **New.** Generated. |
| `tools/tests/test_discovery_workspace_ledger.py` | **New.** Ten hermetic controls. |
| `crates/security/src/custody/discovery_census_tests.rs` | The record's classification (one new test). |

**The ten controls** use synthetic stores, overlays and rule, with the real census model, member model and carrier rendering:
- **the D15 shape:**
  - Cargo, npm and Python;
  - branch B admitting only the providers;
  - branch A admitting every member;
  - item 6b paid per admitted member;
  - the full-ledger sums;
- **refusals:**
  - a Cargo carrier differing from its rendering;
  - an npm overlay already holding a carrier;
  - a member store holding `.git`;
  - branch A failing to admit a member;
- **the record:**
  - its inputs;
  - a failing branch failing the workspace and returning the caps (Python's branch B, with no session, still holds);
  - a held-out workspace recorded as outstanding and never read.

## Checks

Lane r1, `evidence/b3b3c-checks-r1/`:
- **the security suite** at base and candidate, with equal failure sets and one new test;
- **byte-identical to the base:** the census tool, the member model, the link controls, both census records and the receipt;
- **rustfmt and Clippy** (with and without `scenario-fixtures`);
- **every census test;**
- **the T2 checks:** the workspace ledger's `--check` over the T2 cache, the census `--check` (the receipt current, held-out margin holds), and the T2 link reconstructions;
- **the census, blind-receipt and workspace-ledger controls;**
- **environment, operability and verify_design;**
- **four mutations:**
  - `members-not-repositories`: no `.git`;
  - `branch-a-dropped`;
  - `carrier-not-rendered`;
  - `record-member-term-dropped`: a branch-A member term zeroed in the record, which the Rust classification must refuse.

## Not claimed

- No held-out workspace exists in the bound manifest, so none is read or measured.
- No native measurement of the T2 workspaces.
- No change to the census record's workspace rows (LD-B3B3C-1).
- No qualification.
- No completion of B3-b, B2-b or M3-B. The inventory successor and status r102 follow.

## Inventory

New paths for the inventory after acceptance:
- `tools/security/discovery_workspace_ledger.py`;
- `crates/security/src/custody/discovery_workspace_ledger.json`;
- `tools/tests/test_discovery_workspace_ledger.py`.
