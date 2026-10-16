# C1a implementation plan r1: the sealed snapshot's capture, walk, custody, bounds and sealing (M3-C items 1, 2, 5 and 6)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product `808ad64`: inventory v212, 173 contract successors;
- architecture `43402bbc`: shared status r104.

**What precedes it.** C1a is the next unit on the M3 critical path: "B1-a → B1-b → B2-b → B2-c → C1a → C3a → C3b → C4a → H → J2b → J3d → M3-M → M3-X" (M3-PLAN-r10.md:566).

Its unit row is "`snapshot.rs`: the capture session, walk, reads into custody, sealing, bounds (items 1, 2, 5, 6)", depending on "B2; S-B for the public projection only" (snapshot-plan-c/PROPOSAL.md, the units table). Every dependency is met:
- **B2-a to B2-d** are bound, and so is B2-c2b;
- **SX-1** (the `.opensip/` anchor) is bound with B-S1;
- **X3a-2** is integrated;
- **S-B, X9-6, P0 and M3-L** are met, and M3-L has been in effect since 2026-10-14.

**Authority:**
- law M3-C r8 (`snapshot-plan-c/PROPOSAL.md`), section A:
  - item 1, the one read and the capture session, with the carrier join;
  - item 2, the walk: extent, custody, entry types, names and the snapshot ledger;
  - item 5, the bounds;
  - item 6, sealing;
- M3-J1 r7 item 5.4(a) and (b): both modes capture into the invocation's private temporary custody, and the walk runs under the lease and never under the fence;
- M3-B r10 item 12, the discovery rule, which C1a reuses: the shared rule in `custody/discovery_rule.rs` and B2's admitted boundaries;
- the identity contract: `$defs/snapshot`, `source-inventory` and `vcs-observation` in identity-v3, and `IdentityDomain::Snapshot` (`crates/identity/src/descriptors.rs:538`);
- the bound B2-b4 plan r6 section 2.5, the blind held-out census and its receipt; amendment A1's planned-staleness precedent (B3-b plan r2).

## 0. What C1a delivers, and what it does not

**Delivers,** library only, with no caller (J2b and J2c compose it):
- **the snapshot walk:** item 2's extent, custody, entry types and names, charged to one snapshot ledger;
- **candidate blob custody:** the invocation's private temporary custody, written once per digest and verified;
- **the capture session:** item 1's one read, retained captures, re-observation, the change refusal, the leftover-capture refusal and the operational side record;
- **sealing:** item 6's order, with item 1's carrier join, item 5's bounds, `sourceInventoryDigest` and `snapshot2`;
- **the snapshot ledger's caps:** objects 2^20 and edges 2^21, with the byte cap derived from C1a's pricing recipe (item 2). Their T2 margins are on the full population, through a companion census and a reviewed blind held-out refresh (section 5).

**Not delivered:**
- **The VCS observation for Git (item 4)** is C1b. C1a seals only `kind: none` (LD-C1A-5).
- **The `node_modules` read set (item 3)** is C1c. C1a seals an empty read set (LD-C1A-6).
- **The public projection of `SnapshotBound`** (S-B's row) is J1's, in J2's outcome matrix. C1a returns the internal refusal with its field, observed value and limit.
- **No caller, command or Plan.** C4a mints the Plan; J2b and J2c call C1a.
- **No qualification.**

## 1. Where the code lives (LD-C1A-1)

Item 1 and control C1-T2 say `crates/host/src/snapshot.rs` holds the **only source-read site**. But the custody machinery the walk must use is crate-private to `opensip_security`:
- S3's directory judgment (`custody/discovery_scan.rs:379`, `judge_entry`);
- the shared rule (`custody/discovery_rule.rs`);
- the retained root (`DiscoveryRoot`, `custody/project_chain.rs:330`), lent only by `ProjectOperation::discovery_root` (`operation_handoff.rs:380`).

Several of those files are pinned whole by the T2 census closure (`tools/security/discovery_census.py`, `CLOSURE`). A byte change to any of them makes the blind held-out receipt stale.

**The split:**
- **`crates/security/src/snapshot_walk.rs` (new),** declared in `lib.rs` beside `discovery_export.rs`. It changes no census-closure file. It walks from the operation's retained root, and it does all the custody and extent work: enumeration, S3 directory custody, the marker config-file custody, entry typing, names, and the extent (the shared rule's pruned trees, B2's admitted boundaries, Config2 `ignorePaths`, the `.opensip/` anchors). For each regular file in the extent, it opens the file `O_NOFOLLOW` relative to its parent's retained descriptor. It rechecks `st_dev`/`st_ino` against the `fstatat(AT_SYMLINK_NOFOLLOW)` observation, and hands the **open descriptor** and that observation to a caller-supplied visitor. **It reads no content.**
- **`crates/host/src/snapshot.rs` (new)** is the visitor and everything after it. It reads each handed descriptor once, streams the bytes into custody, compares the during and after metadata samples, and runs the capture session and sealing. It is the only module that reads source bytes, so C1-T2's source pin is over `snapshot.rs` and `snapshot_walk.rs` together.
- **`crates/host/src/candidate_custody.rs` (new)** is the blob custody.

**Rejected:**
- **Extending `discovery_walk.rs`.** It is a census-closure file, and discovery's walk reads no content. Mixing the two walks would also merge the discovery ledger with the snapshot ledger, against item 2.
- **Making the security internals `pub`.** That widens the security boundary for one consumer. A new module with a narrow public entry point is the existing pattern (`discovery_export.rs`).
- **Doing the custody work in host.** Host cannot reach `judge_entry` or `DiscoveryRoot`, and re-implementing S3's judgment there would be a second custody rule.

## 2. The steps

### C1a1: the snapshot walk and the snapshot ledger (security, platform)

- **`snapshot_walk.rs`:**
  - `pub fn walk_snapshot(operation: &ProjectOperation, extent: &SnapshotExtent, visit: &mut dyn FnMut(SnapshotFile<'_>) -> Result<(), SnapshotVisitError>, work: &mut WorkScope) -> Result<SnapshotWalkReport, SnapshotWalkRefusal>`.
  - `SnapshotExtent` is built only from B2's accepted outputs: `discovery_export::AdmittedBoundaries`, the pruned-tree rows, the admitted D15 member roots for the `.opensip/` anchors, and the resolved `ignorePaths`. A caller cannot hand the walk an ignore list in place of admitted boundaries (the `discovery_export.rs` rule).
  - Order: depth-first in byte order of names. A directory is entered only after S3 custody passes. A refusal is typed (`Custody`, `Changed`, `Name`, `MarkerCustody`, `Budget`), never retried, and never a silent skip.
  - `SnapshotFile` carries the logical path, the open `File`, the pre-open observation and whether the path is a marker. Markers pass config-file custody first: regular, link count 1, at most 4 MiB.
  - Symlinks and special files are never opened. They are counted in `SnapshotWalkReport`, the operational walk report, with their paths for S-OP-2's P2.
  - **Names:** `LogicalPath` (IE:161-163). An unrepresentable name refuses with its parent path and the escaped name bytes (C1-T7).
- **The snapshot ledger:** `WorkLedger::snapshot_profile()` in `crates/platform/src/work_ledger.rs`. Objects are 2^20 and edges 2^21, as item 2 fixes them, and bytes are the derived cap (section 5). `with_limits` cannot raise past the global caps (`work_ledger.rs:231-240`), so a constructor is needed, as discovery's was.
  - **This changes a census-closure file.** The census pins `work_ledger.rs` whole (`discovery_census.py:85`) and refuses on any drift, so C1a1 also does what B3-b2a did (`58d450c`, "the census closure re-pin"):
    - it re-pins that one closure row;
    - it regenerates `discovery_census.json`, whose held-out rows then read `outstanding: held-out (blind receipt stale)`, because the receipt binds the tool's bytes and the closure pins.
  - The discovery caps are unchanged. The anchored `DISCOVERY_*` constants read the same, and every lead-readable row is reproduced unchanged.
  - The receipt stays stale from C1a1 until C1a4's reviewed refresh. That is amendment A1's planned staleness (B3-b2a, then B3-b3b), and the status board says so for that interval.
- **Vectors:** `tools/security/snapshot_walk_vectors.py` (new). For every accepted walk vector tree of `discovery_walk_vectors.py`, plus new trees for `ignorePaths`, `.opensip/` anchors, symlinks, special files, unrepresentable names and marker custody, it gives the expected inventory paths and refusals. The extent is the bound B2-b0 discovery reference's (contract successor 164), with `ignorePaths` and the anchors applied as item 2 states. The reference is unchanged, and the extent rule is not copied (LD-C1A-2).
- **Controls:** C1-T4 (a swap or change refuses, with no retry), T5 (symlinks are not inventoried), T6 (a FIFO is not opened), T7 (names), T8 (marker custody), T9 (`target/` is pruned only beside `Cargo.toml`), T10 (boundaries), T11 (pruned contents do not move `snapshot2`; with C1a3) and T25's walk half (`.opensip/` never stat'ed in CI). A FIFO and a planted swap use the existing test hooks (`set_before_open` pattern) in a test-only module.

### C1a2: candidate blob custody and the capture session (host)

- **`candidate_custody.rs`:** `CandidateCustody` over a caller-supplied retained parent directory. J1 chooses the parent (M3-J1 item 5.4(a)); tests supply a private 0700 temporary directory.
  - **`put(&mut self, source: &mut dyn Read, expected_len: u64, work) -> Result<Custodied {sha256, bytes}, CustodyError>`** streams through one fixed, reused 64 KiB buffer, hashing with `RawSha256`. It writes a create-exclusive, no-follow temporary entry, then verifies the length and digest, and links it into place under its digest hex. An existing entry with that digest is re-verified and kept, never overwritten.
  - **`open(&self, sha256) -> Result<File, CustodyError>`** re-checks length and digest at open. Custody files are mode 0600 in a 0700 directory and are never source.
- **`snapshot.rs`, the session:**
  - `CaptureSession` is keyed by logical path. Each capture keeps its custody digest, length and descriptor observation (`st_dev`, `st_ino`, size, `mtime`, `ctime`).
  - **The read:** the handed descriptor is read to end. The after sample must equal the before sample, and the length must equal `size`, else `ChangedDuringRead` (no retry).
  - **Reuse:** a later request for a captured path re-observes with `fstatat(AT_SYMLINK_NOFOLLOW)` and reuses the bytes. A difference refuses (C1-T24).
  - **Leftover captures:** a capture the walk's extent never reached refuses sealing if any resolved input depends on it (item 1).
  - **The side record:** each inventory path's origin (`walk` or `read-set`). It is operational and outside identity (C1-T25).
  - **The source interface B2 and C2 read through:** `CaptureSession::read(path)`. B2's marker reads and C2's layout reads use it, so they see the bytes the inventory holds (C1-T24's source pin). C1a2 ships the interface; J2b wires B2's callers.
- **Controls:** C1-T1 (delivered, retained and hashed bytes are equal; a recording sink), T3 (a rewrite after sealing changes nothing), T24, and the custody controls: an existing digest is kept, a corrupted custody file is refused at open, a length mismatch refuses, and a 4 GiB stream is charged only the buffer.

### C1a3: sealing (host)

- **The order (item 6):**
  1. the walk;
  2. the read set (empty until C1c);
  3. sort by path bytes and check uniqueness;
  4. the VCS observation (`kind: none` until C1b);
  5. the bounds;
  6. `snapshot2` through `IdentityCandidate::from_json(.., IdentityDomain::Snapshot, ..)`, which admits against identity-v3's `$defs/snapshot` and checks the order.
- **Bounds (item 5):** more than 100,000 rows; a canonical descriptor over 4 MiB (`canonical.rs:5`); more than 8 GiB of total bytes. Each refuses as the internal `SnapshotBound {field, observed, limit}`, with no truncation and no Plan or Run minted.
- **The carrier join (item 1, rule 2):** the input is `ProjectCarrierObservation {Absent | Present {sha256}}`, built from the B1 resolver input's project carrier: the captured `opensip.json` bytes X2 judged, hashed. The table's seven rows give `SnapshotCarrierChanged {digest | present-absent | absent-present | type | excluded}`, with no retry (C1-T26).
- **Bound inputs:**
  - `projectId` comes from the caller. The fresh ephemeral draw is J2c's.
  - `resolvedConfigDigest` is B1's.
  - `scopeDigest` comes from B2's `unit_scope_descriptor`.
  - No operational value enters a snapshot field (C1-T23's source pin).
- **`sourceInventoryDigest`** is the raw SHA-256 of the canonical inventory. The inventory is retained as a custody blob (item 4).
- **Controls:** C1-T17 (the inventory digest), T18 to T21 (the bounds: at, and one past, each), T22's snapshot half, T23, T26, and T11 with C1a1.

### C1a4: the snapshot ledger's byte cap and its T2 margins

- **The pricing recipe (item 2, r4):**
  - the fixed 64 KiB chunk buffer, charged once per walk by the reader's growth rule (`work_reader.rs:24`);
  - every listing, status sample, ACL capture and path record charged under its existing owner's pricing (`discovery_walk.rs` `LISTING`, `STATUS`, `owned`, and the platform owners);
  - payload volume bounded by item 5's 8 GiB, not by the ledger.
- **The cap derivation.** The cap is the recipe's charge for item 5's maximum population, with a 2× margin. That population has 100,000 rows, and their canonical inventory is at most 4 MiB, which bounds the total path bytes. Directories are bounded by the walk's object cap. The derivation is part of C1a4's evidence. If the derived cap exceeds 2^30, the lead returns it to the law, as item 12 does for discovery.
- **Lead-readable margins:** `tools/security/snapshot_ledger_census.py` (new), a companion tool. It imports `discovery_census.py` unchanged (its integrity-verified stores, overlays and walker model) and adds the snapshot walk's charges, which mirror `snapshot_walk.rs` charge for charge. Its constants are read from the code by anchor, and its files are pinned whole. Each lead-readable T2 repository entry and workspace is classified against the snapshot ledger at the 2× margin. The security tests classify the record again (the B3-b3c pattern).
- **Held-out margins:** the census tool's blind mode is not edited. A companion blind mode measures the snapshot terms, and the existing blind mode refreshes the discovery receipt that C1a1 made stale. Both run under B2-b4 plan r6 section 2.5's procedure: Codex reviews the code before the run, the lead runs it blind, and Codex reviews again after. The owner's standing answer of 2026-10-16 ("mechanical blind run") applies.
- **Soundness control:** the native snapshot walk on the vector trees uses no more than the model predicts (the `discovery_census_tests.rs` pattern), and C1-T27 runs at the exact caps and one over.

## 3. Lead decisions

- **LD-C1A-1. The split** (section 1): security walks and opens; host reads, custodies and seals.
- **LD-C1A-2. The extent is the shared rule's, never a copy.** `snapshot_walk.rs` calls `discovery_rule` and `AdmittedBoundaries`. Its only additions are the ones item 2 names: `ignorePaths`, the `.opensip/` anchors, and every regular file. The vectors derive the expected extent from the bound B2-b0 reference.
- **LD-C1A-3. The read is one pass through one reused buffer.** There is no memory-only copy (item 1 rejects it) and no second read for retention. The during-read check is the before and after descriptor samples, plus the length equal to `size`. A file that grows or shrinks refuses.
- **LD-C1A-4. Custody location is the caller's.** C1a takes a retained parent directory. J1 decides it (item 5.4(a)) and owns removing it at the end of the invocation. Tests use private 0700 temporary directories, and production reads no `TMPDIR`.
- **LD-C1A-5. VCS at C1a is `kind: none` only.** C1b adds Git (item 4, VCS-1). A Git-tracked project's snapshot cannot be sealed until C1b, and C1a refuses it as `SnapshotVcsPending`, internal, with no public route. Nothing calls C1a before J2b.
- **LD-C1A-6. The read set is empty at C1a.** C1c fills it. The sort and uniqueness check already cover both parts.
- **LD-C1A-7. The receipt goes stale on purpose, and is refreshed by review.** This is the A1 precedent. The alternative, not adding a snapshot ledger constructor, would put the walk on a ledger with the wrong caps, against item 2.

## 4. Questions for the reviewer

- **Q1.** Is LD-C1A-1's split a faithful reading of item 1 and C1-T2 ("`snapshot.rs` holds the only source-read site")? The security walk opens descriptors but reads no content, and the source pin covers both modules.
- **Q2.** Is the planned receipt staleness (LD-C1A-7), with its reviewed refresh in C1a4, acceptable?
- **Q3.** Is LD-C1A-5's `SnapshotVcsPending` the right interim for Git-tracked projects, given that C1b follows directly and nothing calls C1a before J2b?

## 5. Checks (each step's lane)

- **Suites:** the security and host suites at base and candidate, with equal failure sets (security 14, host 8 at base);
- **Formatting and lints:** rustfmt on new and base-clean files; warning-denied all-targets Clippy on the touched crates;
- **Vector checks:**
  - the step's own vectors;
  - the census `--check` on the re-pinned record, with the held-out rows stale from C1a1 until C1a4;
  - the companion census, from C1a4;
- **Repository checks:** FW-01 (the host modules are pure apart from the descriptors they are handed), the environment exceptions, the operability source census and verify_design;
- **Mutations:** for each step, mutations that each weaken one rule (for example: a retry after `Changed`, a skipped `ignorePaths`, a followed symlink, a digest not re-verified, a bound off by one, a carrier row merged), each of which must fail the step's tests.

## 6. Not claimed

- No caller, command, Plan or Run.
- No Git VCS observation (C1b) and no `node_modules` read set (C1c).
- No public projection (J2).
- No Linux claim: every test runs on this host's macOS family, and Linux rows are "not run".
- No qualification.
- C1's completion is not claimed; C1b and C1c follow.
