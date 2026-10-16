# B3-b3a1 r1: the D15 terms of the T2 census (M3-B unit B3-b, sub-unit B3-b3a1)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

It implements B3-b3a1 of the B3-b plan r2 as amendment A5 states it (`../b3-b/PLAN-r2-A5.md`; Codex `codex-b3b-plan-a5-r1`, ACCEPT), under §4.1 and §4.2 and law M3-B r9 item 12. That is the bound, before B3-b3a2's gate.

**Base:**
- product main `e367d7f`: B3-b2 complete, inventory v207, 170 contract successors;
- architecture `ea65b4d5c`.

**No product source changes.** The unit changes the census tool, adds its model module, its generated records and their tests.

## What it delivers

### The closure and the anchors

- **The census's cost closure** gains the D15 member producer, readers, native observation and composition: `git_tracking.rs`, `workspace_declarations.rs`, `workspace_observation.rs` and `workspace_discovery.rs`. The platform helpers they call are already in it. Any change to any of them refuses the census, as for the walker's files.
- **Every constant the terms use is read by an anchor** that must match exactly once:
  - the carrier, config and index caps;
  - item 6b's status and its config-parse and decode charges, whose shapes are checked;
  - the system sources;
  - the identity list and records;
  - the native observation's bind, observe, kept-read and copy records, and the walker's bind;
  - the fixed-path open;
  - the core's member cap and depth.
- **The size inventory** gains `DescriptorMetadata` (80) and `(Vec<u8>, DescriptorMetadata)` (104). The census size test asserts both against the build.

### The terms

`tools/security/discovery_member_model.py` is new. Each charge is assigned to exactly one term (A2-3 step 4):
- **`Native`** mirrors `NativeObservation` charge by charge:
  - the reused directory stack;
  - one owned record per new binding in the shared table;
  - the per-phase memo of entries and custody entries;
  - the custody capture;
  - the bounded read with its post-read status and capture;
  - each kept-read copy.
- **`Member`** mirrors item 6b at its ceilings:
  - the session's environment check, global sources, system sources and W's status;
  - each member's reserved identity list;
  - each member's segments (open, status, record, four marker lookups);
  - each member's layout (`.git`, the two linked-worktree probes, the config and the index, each judged and read at its cap), the config parse, the decode and the identity records.
- **`decide`** mirrors the decision core's request sequence: carriers, placement, the visible-repository listing, candidate checks, member custody, item 6b and the links, in branch A's order (A4-2) and branch B's.
- **The three terms:**
  - **the reader term,** at n = 0: the carriers' lookups, custody and reads;
  - **the member term:** placement and listing, paid at n = 0 over the declaring entries and the listed population, then item 6b and the provider manifests;
  - **member descent:** the walker with its admitted members and gitlinks (the walker model gains both), plus the composition walk's binding records for every observed path the decision did not bind.
- **Each binding record is charged once,** to whichever step binds the path first, in the composition's order:
  - branch B: the decision with its links, then the walk;
  - branch A: the decision, the walk, then the links on a fresh observation.

### The repository rows

Each lead-readable repository entry's row gains `d15`: its three terms and its full ledger (the walker plus the terms, with per-mille margins and the 2× verdict at R = 4,096). A full-ledger failure fails the entry and returns the caps.

**Over the T2 corpus no entry fails.** The tightest is `rs-very-large-aws-sdk-rust`: 2,400‰ objects, 2,080‰ edges, 2,488‰ bytes. Its walker alone is 2,840‰ objects and 2,082‰ edges.

Its descent term is large: about 271,000 objects and 73 MB. That is the composition's binding table, one record per observed path (B3-b2b2b's design).

Workspace rows stay walker-only until B3-b3c. The held-out rows stay `outstanding: held-out (blind receipt stale)`; B3-b3a2 is the gate.

### The equality projection

Both census records equal B2-b4b3's in every field except an explicit allowlist:
- the closure;
- the two new sizes;
- each row's `d15`;
- the vectors' new composition keys.

The lane checks the allowlist (`evidence/b3b3a1-checks-r1/equality-projection.json`).

### The validation

`workspace_census_tests.rs` (new) holds `the_census_bounds_the_composed_discovery_at_every_root_length`. It builds every accepted composition vector, and three worst cases, as scratch trees with real Git members. It composes each natively at synthetic root spellings of 134, 1,024 and 4,096 bytes; `DiscoveryRoot` takes its spelling apart from the opened directory, so the walk observes the real tree. It measures the discovery's own charges, with item 6a in one ledger scope and the discovery in the next. Measured objects, edges and bytes must not exceed the prediction.

**The worst cases reach the caps natively:**
- a 4 MiB carrier;
- a 64 KiB member config;
- a valid index of exactly 4 MiB, built to size and sealed with its SHA-1, so the read and the decode reach the model's dearest branch;
- an oversize index;
- H's global sources and five system sources at 64 KiB;
- a descent-heavy tree.

**Tightness:**
- `worst-config-workspace-roots` is exact in objects and edges (272 / 2,528) and within 5 KB of 40 MB in bytes;
- `worst-descent` is exact in all three;
- `w-in-repository` and `b-carrier-oversize` are exact.

**The control found one under-count while the unit was built:** `MemberSession::begin` samples W's status for the session's device, one edge and 512 bytes, which the model had missed. The model now carries it, and the `member-session-device-dropped` mutation pins it.

## What changes

| Path | Change |
| --- | --- |
| `tools/security/discovery_member_model.py` | **New.** The D15 terms. |
| `tools/security/discovery_census.py` | The closure, the anchors, the sizes, the walker model with members and gitlinks, the terms' composition, the repository rows' `d15`, the composition predictions and worst cases, and the docstring. |
| `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json` | Regenerated. |
| `crates/security/src/custody/workspace_census_tests.rs` | **New.** The measured-against-model control, with its pads and its valid-index builder. |
| `crates/security/src/custody/workspace_discovery_tests.rs` | `run_with` is split into `built`, the tree, and `discover_at`. `discover_with` adds the spelling, the system sources and the measurement. It includes the new control. |
| `crates/security/src/custody/discovery_census_tests.rs` | The closure list (19 files), the size inventory, and the margin control's full-ledger classification. |
| `tools/tests/test_discovery_census_blind.py` | The fixture copies the model module, and the access control stubs the terms as it stubs the walker model. |

## Lead decisions

- **LD-B3B3A1-1. The bound is the ledger's** (A5-3). The decision core's parses are not charged, so no term has a parse component. Item 6b's config parse and index decode are charged, and the member term carries them.
- **LD-B3B3A1-2. The D15 terms' read-retry envelope is POSIX regular-file reads, uninterrupted.** Each attempt fills the buffer's free space or reaches end of file. Interrupted retries are excluded, as the B2-b4 census excludes them. Every D15 read is of a regular file opened no-follow, which custody requires.

  So a read's attempts are its buffer growths plus, below the ceiling, the end-of-file attempt. The B2-b4 walker envelope (one byte per attempt) stays for the walker's own reads, keeping the equality projection.

  **Rejected:** applying the one-byte envelope to the D15 reads. A 4 MiB index alone would then cost about 4.2 million edges, over the whole edge cap (2^21). The caps would return to law for any workspace with one member, on reads that natively take about a dozen attempts.
- **LD-B3B3A1-3. Item 6b at its ceilings:**
  - every candidate admitted with `.git`;
  - its config read at 64 KiB + 1 and parsed at 64 KiB;
  - its index read at 4 MiB + 1 and decoded at 4 MiB;
  - H's global sources present at their caps;
  - each system source read at its cap.

  **The process environment** is bounded by macOS's `ARG_MAX` (1 MiB for arguments and environment together): at most `ARG_MAX / 3` entries and `ARG_MAX` bytes. No T2 repository row starts a session, so this envelope first matters in B3-b3c.
- **LD-B3B3A1-4. The other unknowns take their dearer branch:**
  - custody passes and its ACL is captured, at the larger of the ACL record and the premise check;
  - no gitlink bounds the walk.
- **LD-B3B3A1-5. Member descent** is the walker with its members (the walker model's `members` and `gitlinks`), plus the composition walk's binding records. Each record is charged to the step that binds its path first.
- **LD-B3B3A1-6. The measurement:**
  - **Item 6a runs in its own ledger scope,** so the measured cost is the discovery's alone.
  - **The root lengths are synthetic spellings.** The terms keep no root spelling, so R affects only the walker's per-root byte.
- **LD-B3B3A1-7. The control's own include.** The control is included from `workspace_discovery_tests.rs`, not from the closure file `workspace_discovery.rs`, so a test addition does not re-pin the closure.

## Checks

Lane r1, `evidence/b3b3a1-checks-r1/`. A first attempt (`b3b3a1-checks-r1-attempt1/`) failed on a Clippy lint (`manual_is_multiple_of` in the index builder) and on rustfmt of the two test files. Its mutations were already all caught and its projection was clean. The second attempt is the lane of record:
- the security suite at base and candidate, with equal failure sets and one new test;
- the equality projection;
- rustfmt;
- Clippy, with and without `scenario-fixtures`;
- the measured-against-model control and every census, discovery, workspace and Git-tracking test;
- every vector check;
- FW-01, walk storage, and the census tool's and blind receipt's controls;
- the census `--check` over the T2 cache;
- environment, operability and verify_design.

**Mutations (five, one per term and one per new mechanism).** Each patches the model, regenerates the vectors only, and the control must fail with a measured charge over the prediction. The vectors are restored.
- `reader-carrier-read-dropped`;
- `member-index-read-dropped`;
- `member-session-device-dropped`;
- `descent-dropped`;
- `walker-members-ignored`.

## Not claimed

- **No held-out store is opened.** The blind mode's extension to the terms, the receipt's binding over the extended closure, and its controls are B3-b3a2, the pre-run gate.
- No workspace margin (B3-b3c).
- No product code change.
- No qualification.

## Inventory

New paths for the inventory after acceptance:
- `tools/security/discovery_member_model.py`;
- `crates/security/src/custody/workspace_census_tests.rs`.
