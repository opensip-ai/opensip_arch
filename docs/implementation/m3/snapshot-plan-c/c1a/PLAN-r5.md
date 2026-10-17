# C1a implementation plan r5: the sealed snapshot's capture, walk, custody, bounds and sealing (M3-C items 1, 2, 5 and 6)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

## r5 changes (a lead amendment, after building C1a1's charge model)

r4's derivation rule (C1a1, "The bound") says the byte cap is twice the maximum byte charge of any walk within the object and edge caps, and that if this exceeds 2^30 "the cap returns to the law … before any constructor lands". C1a1's model has now been built (`tools/security/snapshot_ledger_model.py`, section 2), and it gives that maximum:
- **One listed entry at the stage envelopes** (a 1023-byte name under a 15,360-byte parent path) is charged 5 objects, 2 edges and 181,992 bytes: its visit, its two converted path copies, its observation, its slot and its classification temporaries.
- **Within the caps**, 2^20 objects admit 209,715 such entries, about **35.5 GiB**, or about **71 GiB** doubled. The trigger fires.

r5 re-reads item 2 rather than inventing a cap:
- **What item 2 asks for.** Its rule is "the recipe's charge for item 5's **maximum population**, with a 2× margin", and "B2-b's T2 census margin test is extended to the snapshot ledger's object, edge **and byte** caps, with the byte census priced by C1a's recipe". That is not an adversarial supremum. It names item 5's population (100,000 rows, a 4 MiB canonical descriptor, 8 GiB), and it makes the T2 census measure the rest, as M3-B r6 did for discovery's caps.
- **The rule r5 adopts (C1a4).** The byte cap is the smallest power of two at least twice the larger of:
  - (a) the model's charge for item 5's maximum row population: 100,000 rows whose canonical inventory is at most 4 MiB, with their opens, samples, retained rows and read attempts at 8 GiB;
  - (b) the largest model charge of any T2 entry: every lead-readable repository entry and workspace, and every held-out entry through a reviewed blind refresh.
- **Item 2's objects (2^20) and edges (2^21)** are not changed. Their T2 margins are measured the same way. An entry whose admitted inventory exceeds item 5's bounds cannot seal, and is reported as over item 5 rather than given a margin.
- **A walk beyond the cap** refuses `WORK.BUDGET_EXHAUSTED`, never truncation (item 2). The ~71 GiB supremum is reported as information, not used as the cap.
- **Q5** asks whether this reading needs a law record (an M3-C r9 statement of the rule) before C1a4, or is faithful as a plan.

**The reordering this needs (sections 2 and 3):**
- `WorkLedger::snapshot_profile`, its `work_ledger.rs` change and the census closure re-pin move from C1a1 to **C1a4**. They land together with the derivation, so the constructor still never precedes its cap (r1 RF-4).
- C1a1 changes no census-closure file, so the blind receipt **stays current** until C1a4.
- C1a1, C1a2 and C1a3 test on the existing discovery-profile ledger, and no production caller exists before J2b.
- C1a4's evidence is now: the completed model (C1a2 extends it with the read, custody and row charges), the item-5 charge, the lead-readable companion census, the reviewed blind refresh, then the profile.

**What C1a1 now delivers** (built; its lane follows this review):
- `snapshot_source.rs` and `snapshot_walk.rs`;
- twelve tests, including the oracle cross-check: all 28 accepted automatic discovery walk vectors (B2-b0, contract successor 164) hand exactly the reference's regular files;
- the charge model, whose soundness control finds the native walk's charge **exactly equal** to the model's on all 32 trees (the 28 vectors and four generated worst-case shapes), so any undercount fails it.


## r4 changes (Codex `codex-c1a-plan-r3`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **C1APLAN-R3-RF-1:** the name cost used a 255-byte limit the law does not impose | **The byte envelopes are the stages' actual limits** (C1a1, "Charge types"):<br>• **raw listed names:** up to 1023 bytes, the walker's `MAX_COMPONENT_BYTES` (`discovery_walk.rs:76`), within macOS's 1024-byte `d_name`. A longer raw name is captured at that envelope, then refused as `Name` with its escaped bytes (at most four bytes per raw byte), and one refusal ends the walk;<br>• **a valid segment:** at most 255 scalars, so at most 1020 bytes of UTF-8;<br>• **a retained row's path:** at most 4096 scalars, so at most 16,384 bytes;<br>• **classification temporaries:** priced at the parent path's envelope plus the name's.<br>Each copy is priced at its stage's envelope.<br>**New model controls:** a 255-scalar name of four-byte scalars (1020 bytes), a 1023-byte raw name, a 1024-byte raw name (refused as `Name`), and a 4096-scalar multibyte path. **New mutant:** the 255-byte name assumption restored, which must fail the soundness control.<br>The corrected envelopes feed the exact solver before any cap is accepted. |
| **RF-2:** the payload guard changes walk-phase observations and needs a law decision | **LD-C1A-10 is withdrawn**, with the guard. The walk and read keep the authorized semantics. Every inventoried file is read once, to EOF, into custody, as item 1 says, so every read failure and change during a read is observed in item 6's order, and step 5 refuses `SnapshotBound {totalBytes}` over 8 GiB.<br>**Size drift is bounded by the reads themselves.** A file that grows, or whose `size` is stale, either exhausts its attempt envelope (`ReadAttemptsExhausted`) or ends at a length unequal to its samples (`ChangedDuringRead`), so no partial capture can seal.<br>**Temporary custody's disk capacity** is not this law's bound: J1's S-OP-8 capacity preflight owns it (M3-J1, "Once their successors are accepted"), and C1a claims nothing about it.<br>**Controls:** C1A-T6 is replaced by mixed-error controls on an over-8-GiB synthetic tree (sparse files):<br>• a later read I/O failure refuses with the read's error first;<br>• a later change during a read refuses `ChangedDuringRead` first;<br>• a later custody or open failure refuses with that failure first;<br>• with none of those, `totalBytes` refuses at step 5. |

## r3 changes (Codex `codex-c1a-plan-r2`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **C1APLAN-R2-RF-1:** the cap derivation does not bound the specified operations | **A complete charge model and a linear bound** (C1a1, "The pricing recipe and the cap derivation").<br>**The model.** Every operation the walk, the capture, the read and custody perform is a charge type with its `(objects, edges, bytes)` read from the code, and every type that carries bytes also carries an object or an edge. The types cover:<br>• each directory opened, with its ACL;<br>• each listed entry, whether excluded, pruned, a symlink, special or regular;<br>• each name copy and the shared rule's per-entry temporaries;<br>• each file opened, with its samples;<br>• each read attempt;<br>• each retained row;<br>• the reused buffer;<br>• custody's per-blob temporaries.<br>**The bound.** The byte cap is twice the **maximum** byte charge of any multiset of those operations within the object cap 2^20 and the edge cap 2^21: a linear program over the charge types, solved exactly, whose optimum lies on a vertex. It is a true upper bound on any walk the other caps admit, not an estimate of a typical one.<br>**Reads** have a finite attempt envelope per file: `2·⌈size / 64 KiB⌉ + 2` attempts, which covers short reads, `Interrupted` and EOF. Each attempt is charged as an edge before it is made. Exhausting the envelope is the terminal, typed `ReadAttemptsExhausted`, with no retry.<br>**Custody** no longer re-reads during the walk: duplicate digests are resolved against the invocation's own in-memory digest set (LD-C1A-9).<br>**Controls:** worst-envelope model controls (vector trees built to maximize each charge type), and undercount mutants (a charge type dropped from the model, an attempt envelope shortened), each of which must fail the soundness control. |
| **RF-2:** the opener is not bound to the walk's enumeration parent | **The walk opens from its enumerating parent** (section 1, `snapshot_walk.rs`):<br>• it holds each directory's retained descriptor as it descends, exactly as the discovery walk does;<br>• it examines each entry with `fstatat(AT_SYMLINK_NOFOLLOW)` relative to that descriptor, and opens it `O_NOFOLLOW` relative to the same descriptor;<br>• it compares `st_dev`/`st_ino`/type with the listing-time observation, and the same for each child directory before entering it.<br>**Pre-walk captures** keep `SnapshotRoot`'s root-relative traversal. When the walk reaches a captured path, it re-observes it **through the enumerating parent** and compares with the capture's observation, so the capture is bound to the enumerated entry. An ancestor replaced after the capture changes the observation and refuses.<br>**New control C1A-T5:** an ancestor directory replaced after its parent is listed refuses `Changed`. The same replacement made after a pre-walk capture, under the reaching walk, refuses too. |
| **RF-3:** LD-C1A-8 does not preserve the descriptor bound or the refusal order | **LD-C1A-8 is withdrawn.** The law's bounds are checked only at sealing step 5, in item 6's order, over the **full canonical snapshot descriptor** (`IdentityCandidate::from_json`, whose canonical encoding enforces 4 MiB over the whole envelope, separators and escaping included). Boundary controls cover an inventory that fits while the descriptor does not.<br>**Resource accounting** is the snapshot ledger alone, which bounds retention during the walk (RF-1's model).<br>**The payload guard (LD-C1A-10)** follows item 2's "payload volume itself is bounded by item 5's 8 GiB total": once the summed sizes would pass 8 GiB, no further content is read into custody. Enumeration, custody, names, opens and the before and after metadata samples continue for every remaining file, so every walk-phase refusal still occurs in the law's order, and step 5 then refuses `SnapshotBound {totalBytes}`. Q4 asks whether item 2's sentence authorizes this, or whether a law clarification is needed. |

## r2 changes (Codex `codex-c1a-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **C1APLAN-R1-RF-1:** the single source-read boundary is not established, and pre-walk captures have no custody-judged opener | **Two services, one read site** (section 1, C1a1 and C1a2).<br>**Opening.** Security's new `SnapshotRoot` opens and re-observes a logical path relative to the retained root, judging S3 directory custody on every component. Both the extent walk and the pre-walk captures use it, so there is one opening rule and no host path-string open.<br>**Reading.** Candidate custody takes **chunks** (`PendingBlob::write(&[u8])`, then `commit`), never a reader. The only loop that calls `read` on a handed source descriptor is in `snapshot.rs`.<br>**The source pin** covers `snapshot.rs` (the only source read), `snapshot_source.rs` and `snapshot_walk.rs` (opens and observations, no content read) and `candidate_custody.rs` (no source read). New control C1A-T1: a path captured before the walk and reached by the walk is read once, a read-count spy shows it, and a change between the two refuses (C1-T24). |
| **RF-2:** the walk accepts only the durable writer handoff | **`SnapshotRoot` has one constructor per lawful lending** (section 1):<br>• `from_operation(&ProjectOperation)`: durable, the writer handoff after the fence is released, under the lease;<br>• `from_released_read(&ReleasedRead, &ProjectRootAdmission)`: ephemeral with I complete, the read session's equivalent release (`installation_read.rs:56-74`, `DiscoveryRoot::lend_read`), with no lease and no fence.<br>Neither changes a census-closure file: both call existing `pub(crate)` lendings from a new module. The `ReleasedRead` constructor is crate-internal until J2c exposes the read entry.<br>**I positively absent** has no `ProjectRootAdmission`. Its root is join E-1 (M3-J1 item 6), owed by M3-B and X2 through successor S7b, and not yet written. C1a adds its constructor when E-1 lands, and J2c waits on E-1 anyway.<br>New controls C1A-T2 (each route walks the same tree to the same inventory) and C1A-T3 (the ephemeral route takes no lease and runs under no fence). |
| **RF-3:** the interim VCS gate must cover D15 Git members | **`SnapshotVcsPending` covers every input C1b observes** (LD-C1A-5): an enclosing Git repository, **or any admitted D15 member** (members are Git repositories by M3-B item 22). C1a seals `kind: none` only for an authenticated `NoRepository` tracking observation with no admitted member. New control C1A-T4: a NoRepository root with one admitted Git member refuses `SnapshotVcsPending`. |
| **RF-4:** the constructor precedes its cap's derivation | **The recipe and the cap derivation move into C1a1** (section 2), before the constructor lands. The derivation accounts for every charge the walk and the read make:<br>• every listing, status sample, ACL capture and retained record;<br>• every read attempt, as one edge per `read` call, EOF included;<br>• the one reused chunk buffer.<br>The retained inventory is bounded during the walk, not after it: the descriptor bound (item 5) is enforced incrementally (LD-C1A-8), so retained rows never exceed 4 MiB canonical. The cap is not inferred from final path bytes alone.<br>C1a4 keeps only the corpus margins and the blind refresh. Every later change to the cap or the closure, and every receipt transition, is named in section 2's "Transitions". |

**Bases (r5):** product `808ad64`; architecture `92eaf1d5` (the accepted r4); r1 to r4 at `PLAN-r1.md` to `PLAN-r4.md`.


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
- **the snapshot ledger's caps:** objects 2^20 and edges 2^21, with the byte cap derived from C1a1's pricing recipe (item 2). Their T2 margins are on the full population, through a companion census and a reviewed blind held-out refresh (C1a4).

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

**The split (r2):**
- **`crates/security/src/snapshot_source.rs` (new), `SnapshotRoot`:** the lawful root, and the one opening rule.
  - **Constructors:** `from_operation(&ProjectOperation)` (durable) and `from_released_read(&ReleasedRead, &ProjectRootAdmission)` (ephemeral, I complete; crate-internal until J2c). Each wraps the existing `DiscoveryRoot` lending (`operation_handoff.rs:380`; `installation_read.rs:68`).
  - **`open(path, work) -> SourceFile {file, observation}`**, for **pre-walk captures only** (r3): it walks `path`'s components from the retained root with `fstatat(AT_SYMLINK_NOFOLLOW)` and `O_NOFOLLOW` opens. It judges S3 directory custody on each directory with the existing judge, applies marker config-file custody to a marker, and rechecks `st_dev`/`st_ino` between the observation and the open. The extent walk does not use it.
  - **Charging:** both charge the ledger they are given. B2's and C2's pre-walk captures use the discovery ledger (item 1); the walk uses the snapshot ledger.
  - **No content read.**
- **`crates/security/src/snapshot_walk.rs` (new):** the extent walk over a `SnapshotRoot` (r3, RF-2).
  - It descends holding each directory's retained descriptor, and enters a child directory only after comparing its open with the listing-time `fstatat` observation.
  - It examines each entry relative to its enumerating parent, and opens each regular file `O_NOFOLLOW` relative to that **same** descriptor, rechecking `st_dev`/`st_ino`/type. The shared custody judgments are used for directories and markers.
  - It covers entry typing, names and the extent (the shared rule's pruned trees, B2's admitted boundaries, `ignorePaths`, the `.opensip/` anchors).
  - It hands each `SourceFile` to the visitor, and **re-observes a pre-walk capture through the enumerating parent** for the visitor's comparison.
  - **No content read.** Both files are declared in `lib.rs` beside `discovery_export.rs`, and neither is a census-closure file.
- **`crates/host/src/snapshot.rs` (new):** the only source-read site. Its one loop reads each handed `SourceFile` to EOF through one reused buffer and writes the chunks to custody. It runs the capture session, the extent visitor and sealing.
- **`crates/host/src/candidate_custody.rs` (new):** blob custody. Its writer takes chunks, so it never holds a source descriptor.
- **The source pin (C1-T2):**
  - only `snapshot.rs` calls `read`, or any `Read` method, on a `SourceFile`'s descriptor;
  - the security modules call none;
  - `candidate_custody.rs` reads only its own custody files, at open, to verify them.

**Rejected:**
- **Extending `discovery_walk.rs`.** It is a census-closure file, and discovery's walk reads no content. Mixing the two walks would also merge the discovery ledger with the snapshot ledger, against item 2.
- **Making the security internals `pub`.** That widens the security boundary for one consumer. A new module with a narrow public entry point is the existing pattern (`discovery_export.rs`).
- **Doing the custody work in host.** Host cannot reach `judge_entry` or `DiscoveryRoot`, and re-implementing S3's judgment there would be a second custody rule.

## 2. The steps

### C1a1: the snapshot walk and the snapshot ledger (security, platform)

- **`snapshot_walk.rs`:**
  - `pub fn walk_snapshot(root: &SnapshotRoot, extent: &SnapshotExtent, visit: &mut dyn FnMut(SourceFile) -> Result<(), SnapshotVisitError>, work: &mut WorkScope) -> Result<SnapshotWalkReport, SnapshotWalkRefusal>`, with `SnapshotRoot`, `SourceFile` and the opening rule in `snapshot_source.rs`.
  - `SnapshotExtent` is built only from B2's accepted outputs: `discovery_export::AdmittedBoundaries`, the pruned-tree rows, the admitted D15 member roots for the `.opensip/` anchors, and the resolved `ignorePaths`. A caller cannot hand the walk an ignore list in place of admitted boundaries (the `discovery_export.rs` rule).
  - Order: depth-first in byte order of names. A directory is entered only after S3 custody passes. A refusal is typed (`Custody`, `Changed`, `Name`, `MarkerCustody`, `Budget`), never retried, and never a silent skip.
  - `SourceFile` carries the logical path, the open `File`, the pre-open observation and whether the path is a marker. Markers pass config-file custody first: regular, link count 1, at most 4 MiB.
  - Symlinks and special files are never opened. They are counted in `SnapshotWalkReport`, the operational walk report, with their paths for S-OP-2's P2.
  - **Names:** `LogicalPath` (IE:161-163). An unrepresentable name refuses with its parent path and the escaped name bytes (C1-T7).
- **The pricing recipe and the cap derivation (r3, RF-1).** C1a1's evidence comes before `snapshot_profile` exists. It is a model, a solver and controls, with every constant read from the code by anchor, as the census reads its own.
  - **Charge types.** Each is one operation the code charges before it happens, as `(objects, edges, bytes)`:
    - *per directory entered:* the open with its status sample, the listing (`LISTING`), the ACL capture at its owner's pricing (`descriptor_acl_capture.rs:134`), and the retained descriptor's record;
    - *per listed entry*, whatever it turns out to be:
      - its `fstatat` sample (`STATUS`);
      - its name copy, `owned(name bytes)` at the raw envelope of 1023 bytes (r4, RF-1: `discovery_walk.rs:76`);
      - the shared rule's classification temporaries (`classify_cost`'s form), at the parent path's envelope (16,384 bytes) plus the name's;
      - for the one name a walk can refuse, its escaped copy (at most 4 × 1023 bytes);
    - *per regular file in the extent:* the open, the before and after samples, and the retained row (`owned(path + digest)`), with the path at its envelope of 4096 scalars, at most 16,384 bytes (r4);
    - *per read attempt:* one edge;
    - *per custody blob:* the temporary entry's name and its digest record;
    - *once per walk:* the 64 KiB chunk buffer, charged by the reader's growth rule (`work_reader.rs:24`).

    Every type that carries bytes also carries an object or an edge. The evidence checks this for each type, because a type with bytes and neither would make the bound infinite.
  - **The read-attempt envelope.** A file of `size` bytes gets at most `2·⌈size / 64 KiB⌉ + 2` `read` calls, which covers short reads, `Interrupted` and the EOF read. Each is charged as an edge before it is made. A file that needs more refuses `ReadAttemptsExhausted {path}`, terminal and typed, with no retry. **(r4)** The edge cap bounds the total attempts, and so the payload read before any refusal; step 5's `totalBytes` bound applies to what was read.
  - **The bound.** The byte cap is twice the maximum of `Σ nₖ·bytesₖ` subject to `Σ nₖ·objectsₖ ≤ 2^20` and `Σ nₖ·edgesₖ ≤ 2^21`, with each `nₖ ≥ 0`. The read attempts are counted in the edge constraint like every other edge (r4).
    - This is a two-constraint linear program over the charge types, so its optimum lies on a vertex with at most two types non-zero. The evidence enumerates the vertices exactly, in integers.
    - The result bounds every walk the object and edge caps admit, so no walk within those caps can exhaust the byte cap. The census then measures the actual margins of all three (C1a4).
    - If the doubled maximum exceeds 2^30, the cap returns to the law (item 2; item 12's procedure) before any constructor lands.
  - **Controls:**
    - **worst-envelope model controls:** vector trees built to maximize each charge type, at the vertex types (deep directories, wide listings of long excluded names, many small files, short-read readers), for which the native walk and read must use no more than the model predicts;
    - **undercount mutants,** each of which must make the soundness control fail:
      - a charge type dropped from the model;
      - an envelope shortened by one attempt;
      - the ACL charge omitted;
      - name copies priced at zero;
      - **(r4)** names priced at 255 bytes.
    - **(r4) envelope model controls:** a 255-scalar name of four-byte scalars (1020 bytes); a 1023-byte raw name; a 1024-byte raw name, refused as `Name` with its escaped bytes; a 4096-scalar multibyte path.
- **(r5) The snapshot ledger constructor, the census re-pin and the transitions move to C1a4.** C1a1 changes no census-closure file. The walk takes the caller's `WorkScope`; its tests use the existing discovery profile.
- **(r5) The charge model:** `tools/security/snapshot_ledger_model.py` and `crates/security/src/snapshot_ledger_vectors.json`. The model imports `discovery_census.py` unchanged (its anchored costs, size inventory, tree reading and reference rule), pins `snapshot_walk.rs` and `snapshot_source.rs` whole and by anchor, and mirrors the walk charge for charge, with ACL captures at their dearer branch. The soundness control, `the_native_walk_never_charges_more_than_the_model_predicts`, walks each of the 32 trees natively and asserts used ≤ predicted. Here they are equal.
- **Vectors:** `tools/security/snapshot_walk_vectors.py` (new). For every accepted walk vector tree of `discovery_walk_vectors.py`, plus new trees for `ignorePaths`, `.opensip/` anchors, symlinks, special files, unrepresentable names and marker custody, it gives the expected inventory paths and refusals. The extent is the bound B2-b0 discovery reference's (contract successor 164), with `ignorePaths` and the anchors applied as item 2 states. The reference is unchanged, and the extent rule is not copied (LD-C1A-2).
- **Controls:** **C1A-T5 (r3):** an ancestor directory replaced after its parent is listed refuses `Changed`; replaced after a pre-walk capture, it refuses at the reaching walk. **C1A-T2 (r2):** the durable and the ephemeral (released-read) routes walk one tree to the same inventory. **C1A-T3 (r2):** the ephemeral route holds no lease and runs under no fence. C1-T4 (a swap or change refuses, with no retry), T5 (symlinks are not inventoried), T6 (a FIFO is not opened), T7 (names), T8 (marker custody), T9 (`target/` is pruned only beside `Cargo.toml`), T10 (boundaries), T11 (pruned contents do not move `snapshot2`; with C1a3) and T25's walk half (`.opensip/` never stat'ed in CI). A FIFO and a planted swap use the existing test hooks (`set_before_open` pattern) in a test-only module.

### C1a2: candidate blob custody and the capture session (host)

- **`candidate_custody.rs`:** `CandidateCustody` over a caller-supplied retained parent directory. J1 chooses the parent (M3-J1 item 5.4(a)); tests supply a private 0700 temporary directory.
  - **The writer takes chunks (r2, RF-1).** `begin(expected_len) -> PendingBlob`; `PendingBlob::write(&[u8])` hashes with `RawSha256` and writes to a create-exclusive, no-follow temporary entry; `commit() -> Custodied {sha256, bytes}` verifies the length and digest and links the entry into place under its digest hex. The writer never holds or reads a source descriptor.
  - **Duplicates (r3, LD-C1A-9):** custody is per invocation and starts empty, so this invocation wrote every entry in it. A digest already committed is found in the invocation's in-memory digest set; the new temporary is discarded and nothing is re-read. Verification by reading is `open`'s, for later consumers, on their own ledgers.
  - **`open(&self, sha256) -> Result<File, CustodyError>`** re-checks length and digest at open.
  - Custody files are mode 0600 in a 0700 directory and are never source.
- **`snapshot.rs`, the session:**
  - `CaptureSession` is keyed by logical path. Each capture keeps its custody digest, length and descriptor observation (`st_dev`, `st_ino`, size, `mtime`, `ctime`).
  - **The read** is `snapshot.rs`'s one loop. It reads a `SourceFile` to EOF through the one reused 64 KiB buffer, and each chunk goes to the pending blob. The after sample (`fstat`) must equal the before sample and the length must equal `size`, else `ChangedDuringRead`, with no retry. Each `read` call is one attempt, charged as an edge before it is made, within the file's attempt envelope (C1a1); exhausting the envelope refuses `ReadAttemptsExhausted`.
  - **(r4)** There is no payload guard: every file in the extent is read once, to EOF, into custody (item 1). A file that grows or whose `size` is stale ends in `ReadAttemptsExhausted` or `ChangedDuringRead`, never in a partial capture.
  - **Pre-walk captures (r2, RF-1):** `CaptureSession::capture(path, &SnapshotRoot, work)` opens through `SnapshotRoot::open` and reads through the same loop. B2's marker and manifest reads and C2's layout reads use it, on the discovery ledger.
  - **Reuse (r3, RF-2):** when the walk reaches a captured path, it re-observes the entry through its enumerating parent and hands that observation to the visitor. The visitor compares it with the capture's observation (`st_dev`, `st_ino`, size, `mtime`, `ctime`) and reuses the bytes. It never reads again, and a difference refuses (C1-T24). The walk binds the capture to the enumerated entry.
  - **Leftover captures:** a capture the walk's extent never reached refuses sealing if any resolved input depends on it (item 1).
  - **The side record:** each inventory path's origin (`walk` or `read-set`). It is operational and outside identity (C1-T25).
- **Controls:**
  - C1-T1: delivered, retained and hashed bytes are equal (a recording sink);
  - T3: a rewrite after sealing changes nothing;
  - T24;
  - **C1A-T1 (r2):** a path is captured before the walk and reached by the walk; a read-count spy in `snapshot.rs`'s loop shows exactly one read pass, and a rewrite between capture and walk refuses;
  - the custody controls:
    - an existing digest is kept;
    - a corrupted custody file is refused at open;
    - a duplicate digest is resolved without a re-read (LD-C1A-9);
    - a length mismatch refuses;
    - a 4 GiB stream is charged only the buffer and its read attempts.

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
- **Controls:**
  - C1-T17 (the inventory digest);
  - T18 to T21 (the bounds, at and one past each, all at step 5); **(r3)** an inventory that fits 4 MiB inside a descriptor that does not, which refuses `descriptor`; and mixed-error trees, where an over-bound tree with a later changed file, and another with a later custody-refusing file, give the walk's refusal first, in item 6's order;
  - T22's snapshot half, T23, T26, and T11 with C1a1;
  - **C1A-T4 (r2):** a NoRepository root with one admitted Git member refuses `SnapshotVcsPending` (LD-C1A-5);
  - **C1A-T6 (r4):** on an over-8-GiB synthetic tree of sparse files:
    - a later read I/O failure refuses with that error first;
    - a later change during a read refuses `ChangedDuringRead` first;
    - a later custody or open failure refuses with that failure first;
    - otherwise `totalBytes` refuses at step 5.

### C1a4: the snapshot ledger's caps, their T2 margins and the constructor (r5)

- **The completed model.** C1a1's model, extended by C1a2 with the read, custody and row charges, is evaluated three ways:
  - **(a)** item 5's maximum row population;
  - **(b)** every lead-readable T2 repository entry and workspace, through `tools/security/snapshot_ledger_census.py`, a companion tool that imports `discovery_census.py` unchanged (its integrity-verified stores and overlays) and adds no store access of its own;
  - **(c)** every held-out entry, in a companion blind mode. The census tool's own blind mode is not edited. The run follows B2-b4 plan r6 section 2.5: Codex reviews the code before it, the lead runs it blind, and Codex reviews it after. The owner's standing answer of 2026-10-16 ("mechanical blind run") applies.
- **The byte cap** (r5's rule) is the smallest power of two at least twice the larger of (a) and (b, c). **The objects and edges caps** are item 2's (2^20 and 2^21), with their margins classified on (b, c). An entry over item 5's bounds is reported as such and needs no margin. A margin that fails for an entry within item 5 returns the caps to the law.
- **Then the constructor:** `WorkLedger::snapshot_profile()` in `crates/platform/src/work_ledger.rs`, with those three caps. `with_limits` cannot raise past the global caps (`work_ledger.rs:231-240`).
  - **This changes a census-closure file.** The census pins `work_ledger.rs` whole (`discovery_census.py:85`), so C1a4 re-pins that one closure row and regenerates `discovery_census.json`, with the discovery caps and every lead-readable row unchanged, as B3-b2a did (`58d450c`).
  - **The receipt.** The discovery receipt then binds stale pins. C1a4's reviewed blind run refreshes it in the same gated run as (c), so it is current again when C1a4 lands.
- **Soundness, on the final caps:** C1-T27 at the exact caps admits and one unit over refuses `WORK.BUDGET_EXHAUSTED`. A 4 GiB payload file is charged only its buffer and its read attempts.
- **Transitions (r5):** no closure change before C1a4. C1a4 makes one `work_ledger.rs` change, one re-pin and one gated blind run. A later cap revision would repeat that sequence. Nothing is raised by hand.

## 3. Lead decisions

- **LD-C1A-1. The split** (section 1): security walks and opens; host reads, custodies and seals.
- **LD-C1A-2. The extent is the shared rule's, never a copy.** `snapshot_walk.rs` calls `discovery_rule` and `AdmittedBoundaries`. Its only additions are the ones item 2 names: `ignorePaths`, the `.opensip/` anchors, and every regular file. The vectors derive the expected extent from the bound B2-b0 reference.
- **LD-C1A-3. The read is one pass through one reused buffer.** There is no memory-only copy (item 1 rejects it) and no second read for retention. The during-read check is the before and after descriptor samples, plus the length equal to `size`. A file that grows or shrinks refuses.
- **LD-C1A-4. Custody location is the caller's.** C1a takes a retained parent directory. J1 decides it (item 5.4(a)) and owns removing it at the end of the invocation. Tests use private 0700 temporary directories, and production reads no `TMPDIR`.
- **LD-C1A-5 (r2). VCS at C1a is `kind: none` only.** C1b adds Git (item 4, VCS-1) and D15 members (M3-B successor S4). C1a refuses as `SnapshotVcsPending`, internal, with no public route, whenever any input needs C1b's observation: the X2 tracking observation is a Git repository, **or** the project has at least one admitted D15 member, since every member is a Git repository (M3-B item 22). C1a seals schema-2 `kind: none` only for an authenticated `NoRepository` observation with no admitted member. Nothing calls C1a before J2b.
- **LD-C1A-6. The read set is empty at C1a.** C1c fills it. The sort and uniqueness check already cover both parts.
- **LD-C1A-8 (r2) is withdrawn (r3, RF-3).** The law's bounds are checked only at sealing, step 5 of item 6, over the full canonical snapshot descriptor. The snapshot ledger alone bounds resource use during the walk.
- **LD-C1A-9 (r3). Custody is per invocation; duplicates are resolved in memory.** Nothing else writes the custody directory, so a digest this invocation already committed needs no re-read. Consumers verify by reading at `open`.
- **LD-C1A-10 (r3) is withdrawn (r4, RF-2).** The walk and read keep item 1's semantics. Temporary custody's disk capacity is J1's S-OP-8 capacity preflight's, not this law's.
- **LD-C1A-7. The receipt goes stale on purpose, and is refreshed by review.** This is the A1 precedent. The alternative, not adding a snapshot ledger constructor, would put the walk on a ledger with the wrong caps, against item 2.

## 4. Questions for the reviewer

- **Q4 (r3) is withdrawn with LD-C1A-10 (r4).**
- **Q5 (r5).** Is r5's reading of item 2 faithful, with the byte cap derived from item 5's maximum row population and the T2 census and the adversarial supremum reported only? Or must an M3-C r9 law record state that rule before C1a4?

- **Q1.** Is LD-C1A-1's split a faithful reading of item 1 and C1-T2 ("`snapshot.rs` holds the only source-read site")? The security walk opens descriptors but reads no content, and the source pin covers both modules.
- **Q2.** Is the planned receipt staleness (LD-C1A-7), with its reviewed refresh in C1a4 and the named transitions, acceptable?
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
