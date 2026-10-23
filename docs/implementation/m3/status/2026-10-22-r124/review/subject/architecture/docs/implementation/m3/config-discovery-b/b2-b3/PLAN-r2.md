# B2-b3 implementation plan r2 (M3-B unit B2-b, sub-unit B2-b3: the walker)

**Lead plan record, 2026-10-15; r2. Not law, not code.** It refines section 1.3 of the accepted B2-b plan r4 (`config-discovery-b/b2-b/PLAN-r4.md`; Codex `codex-b2b-plan-r4`). Research at product `f51769f` showed thirteen design gaps that section 1.3 does not settle. They are decided here before any walker code.

B2-b3's dependencies:
- B2-b1 is bound: the discovery ledger profile and `observe_child`.
- B2-b2, the pure core, is bound (product `a725a68`; Codex `codex-b2b2-r2`).

## r2 changes (Codex `codex-b2b3-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
|---|---|
| **B2B3PLAN-1:** name handling | **LD-B2B3-2 is rewritten.** Every returned OS name is charged; exactly `.` and `..` are then discarded, before any validation or observation. Each remaining name forms a root-relative path, validated as a whole `LogicalPath`: each segment at most 255 scalars, and the complete path at most 4096 scalars (MC:274; `LogicalPath::parse`). An overlong path refuses with the same code and detail as an unrepresentable segment. New controls: an ordinary listing succeeds; segments at 255 and 256 scalars; complete paths at 4096 and 4097 scalars. |
| **B2B3PLAN-2:** metadata-only rejection | **LD-B2B3-3 and LD-B2B3-6 are rewritten.** The core gains a metadata-only early rejection in the reference's own order: kind, owner, mode. Only then does an ACL-dependent check need the ACL. `NotObserved` faults only when judgment actually reaches that check. A non-regular marker is never opened and keeps an honest `NotObserved`; its reason (`SYMLINK`, `NOT_A_REGULAR_FILE`) comes from its kind alone. Section 3 now says that every object whose judgment **reaches the ACL** is opened. New tests: FIFO, socket and symlink markers, alone and beside a valid marker, against the oracle, with no-open traces. |
| **B2B3PLAN-3:** seam order | **LD-B2B3-12 is rewritten.** The order is: phase 1; resolution and admission on the captured carriers, with CLI provenance (`installation_read.rs:245-253`); phase 2; the equivalent release; then the walk. New control: a resolution or admission failure never reaches phase 2 or any downward observation. |
| **B2B3PLAN-4:** pin the configuration module now | **LD-B2B3-11.** The FW-01 pin covers the existing `crates/host/src/configuration.rs` and its production-reachable includes now, with planted spawn, socket and write negatives. Only the nonexistent `discovery.rs` waits for its owning unit (B2-c). |
| **B2B3PLAN-5:** cross-check evidence and records | **Section 3's oracle cross-check is rewritten.** It compares the native population's evidence, and it runs native captures through the core, comparing them with the bound reference over the same tree description. Details are in section 3. |
| NBO-1, NBO-2 | LD-B2B3-4 states the peak descriptor count. LD-B2B3-7 keeps budget exhaustion and identity changes as whole-operation refusals. |

**Authority.**
- MB (M3-B r5): items 12, 13 and 15 (FW-01); the B2-b row; the test owners.
- B2-b plan r4: section 1.3; LD-B2B-2, LD-B2B-5, LD-B2B-6, LD-B2B-7, LD-B2B-8 and LD-B2B-9.
- The B2-b0 reference's `walker_population` (contract successor 164), which is the walker's exact observation oracle.
- SL S3 (SL:105-332).
- X2 r9: item 1, item 3a, and the handoff (X2:231-248, item 7a).
- M3-C item 2's walk rules (MC:268-296), for names and entry types, so that the two walks agree.
- COV:5288 and COV:5388.

## 0. What exists (product `f51769f`, plus B2-b2 as bound at `a725a68`)

- **Post-fence holdings.**
  - **Write path:** `ProjectOperation` (`operation_handoff.rs:331-347`, built by `begin`) holds the subject, and so the `ProjectChain` with its retained root (`project_chain.rs:230`). It does not lend the receipt's qualification, which carries the ACL omission premise and the H-filesystem check (`installation_admission.rs:54-60`).
  - **Read path:** `ReadSession` (`installation_read.rs:36-51`) has no release. Dropping it drops the fence lock and the receipt, and the receipt owns the premise. `InstallationObservation::release` exists (`installation_session.rs:164-169`) but is not exposed.
- **B1-b's analysis admission** (`project_admission.rs:1306-1328`) runs with the fence held and returns `ProjectRootAdmission` (chain, root, `Selected`, carriers). `CarrierAdmission` has no `chain()`.
- **`select`** (`:335-427`) records only the mode, the stop and whether a config was found:
  - no walk rows;
  - no custody reason;
  - no candidate state;
  - no VCS kind (`.git`/`.hg`/`.svn`/`.jj` are presence-only, through `observe_child_absent_accounted`);
  - in config and explicit modes, no VCS observation at all.
- **The waiver is applied nowhere upward or in the chain walk.** `judge_root` and its recheck use the unwaived judge.
- **`visit_entry_names`** (`directory_entries.rs:81-92`) yields raw name bytes, including non-UTF-8. It has hard ceilings of 131,072 entries per directory and 256 MiB of names, refuses union mounts, and has no cost function. `component()` refuses `\`, NUL, more than 1023 bytes, `.`/`..` and `.opensip-stage-*`.
- **B2-b2's `ObservedEntry`** requires an `acl` for every entry. B2-b2's scope keys and the B2-a rule are `&str`.
- **No FW-01 structural pin exists.** `tools/tests/test_environment_exceptions.py` is the model.
- **The scenario seam.** `ScenarioHome::compose_analysis_carriers` (`scenario.rs:206-246`) runs phase 1 then phase 2 on a writer's gate, with no explicit path, no waiver and no release. `crates/host/tests/discovery_tests.rs` does not exist. COV:5288 and COV:5388 name it as the verification owner of `--project` and `--workspace-root`.

## 1. Split: three sub-units

| Sub-unit | Content |
|---|---|
| **B2-b3a: selection provenance and lending** (`project_admission.rs`, `project_chain.rs`, `installation_read.rs`, `operation_handoff.rs`) | Upward walk rows and VCS evidence on the analysis path, with the legacy path unchanged; the waiver through selection and the chain walk; `DiscoveryRoot`, the one lending type a walker uses, with its two constructors |
| **B2-b3b: the walker** (`custody/discovery_walk.rs`, new; the FW-01 pin, new) | Sections 1.3 and 3 of this plan |
| **B2-b3c: the host seam and the flag rows** (`scenario.rs`; `crates/host/tests/discovery_tests.rs`, a planned path) | COV:5288 and COV:5388 through the test-only seam |

Each sub-unit gets its own review, record and inventory. B2-b3 is complete only when all three are.

## 2. Decisions

**LD-B2B3-1 (D1). The walk runs on a `DiscoveryRoot` that only two constructors make.**
- `DiscoveryRoot<'a>` lends three things and nothing else:
  - the retained root (`&RetainedDirectory`);
  - the ACL omission premise (`Option<&AclOmissionPremise>`);
  - the H-filesystem check.
- **On the write path,** `ProjectOperation::discovery_root(&self)` builds it after X2's handoff released the fence. It lends the root through the subject's chain and the premise through the receipt's qualification.
- **On the read path,** the read session's equivalent release (MB item 12): `ReadSession::release(self) -> ReleasedRead`. It releases the fence through `InstallationObservation::release` and keeps the `ReadPremiseReceipt`. `ReleasedRead::discovery_root(&self, admission: &ProjectRootAdmission)` then builds the view from the admission's chain.
- No ledger is lent. The walker charges its own discovery ledger, created once (B2-b1).
- `CarrierAdmission` gains no lending; the admission returned by phase 2 is what the view borrows.
- **Rejected:**
  - re-producing a receipt, which is impossible because there is one attempt per process (`initial_installation.rs:101-105`);
  - walking under the fence (MB item 12);
  - lending the attempt ledger.

**LD-B2B3-2 (D3; r2). Listed names: charge, discard the dot entries, validate the whole path.**
- **The order.** Every name the OS returns is charged first (LD-B2B3-5). Exactly `.` and `..` are then discarded, before any validation or observation (`visit_entry_names` yields both, `directory_entries.rs:417-418`).
- **Validation.** Each remaining name forms the root-relative path, which must be a `LogicalPath`:
  - UTF-8 scalars;
  - each segment at most 255 scalars, with no `\` or NUL;
  - the **complete path at most 4096 scalars** (IE:161-163; `LogicalPath::parse`; MC:274).

  The platform grammar must also accept the name; it refuses `.opensip-stage-*`.
- **The refusal.** Any failure refuses the whole discovery with `PROJECT.ROOT_CUSTODY_REFUSED`, the existing discovery code. The detail is `NAME_UNREPRESENTABLE:<parent>:<escaped name bytes>`, the same for an unrepresentable segment and an overlong path. The remedy is to rename.
- **Where it applies.** Names inside a pruned anchor are never listed, so they never refuse. Explicit modes list only their named roots' subtrees.
- **Rejected:**
  - dropping the name with a disclosure, which is erasure (NE:700-702; MC:282);
  - a new public code;
  - honouring `ignorePaths` in the walk, because SLM's discovery takes none.

**LD-B2B3-3 (D4; r2). `ObservedAcl::NotObserved`, and a metadata-only early rejection.**
- **Which entries.** An entry the walker never opens carries `NotObserved`, an honest uncaptured state: pruned anchors, listed-only entries, and non-regular markers. B2-b3b adds the variant to B2-b2's type.
- **The early rejection.** The core gains a metadata-only path in the reference's own order: kind (`ABSENT`, `SYMLINK`, `NOT_A_DIRECTORY`, `NOT_A_REGULAR_FILE`), owner, then mode. If that path refuses, its reason is final and no ACL is needed.
- **When `NotObserved` faults.** Only when judgment actually reaches an ACL-dependent check. That is an instrument invariant fault, never a public reason. The walker opens and captures every object whose judgment reaches the ACL.
- **The unreadable-anchor filter** ignores `NotObserved`. That is sound because production's basis is always `not-enumerated`.
- **Rejected:**
  - judging every listed directory (LD-B2B-2);
  - an invented empty ACL.

**LD-B2B3-4 (D5). A depth-first walk with the open ancestor stack.**
- The walk is depth-first. It keeps each ancestor's retained descriptor open, at most 257 retained at a time.
- A unit's chain is judged lazily from those descriptors, memoized per directory. There is no reopen and no second identity sample.
- **Peak descriptors (NBO-1).** The retained ancestors are the root plus depths 1 to 256. Opening a 257-segment directory to observe its markers adds one temporary descriptor, and the listing stream adds another, so the peak is 259. The code and the census state it.
- Running out of descriptors (`EMFILE`) refuses as `HostIo`, never truncation.
- The scope is a `BTreeMap`, so walk order changes no output. The reference's population is order-free.
- **Rejected:** breadth-first, which needs reopening and an identity comparison, or thousands of open descriptors.

**LD-B2B3-5 (D6). Listing has a cost, and its limits are typed.**
- `directory_listing_cost`, before the listing: 2 objects, 3 edges and 1,024 bytes, as in `first_registration.rs:95-99`. Then each name is charged inside the visitor before it is copied: one edge, plus its bytes.
- The platform's per-directory ceilings (`EntryLimit`, `NameByteLimit`) refuse as `WORK.BUDGET_EXHAUSTED`, a bound and never truncation. A union mount (`Unsupported`) refuses as `HostIo`.
- B2-b4's census pins these costs from the code.

**LD-B2B3-6 (D7; r2). Only an object whose judgment reaches the ACL is opened.**
- **Markers.** A marker observed as `File` is opened `O_NOFOLLOW` from its parent, compared with its observation through `matches`, and its ACL captured.
- **Non-regular markers.** A FIFO, socket, device or symlink named `Cargo.toml` is never opened. It stays `NotObserved`, and its reason (`NOT_A_REGULAR_FILE`, `SYMLINK`) comes from the metadata-only rejection (LD-B2B3-3).
- **Directories** on a unit's chain are opened after `classify_entry` says `Ordinary` and the observation says `Directory`, and they are compared the same way.

**LD-B2B3-7 (D8). Upward rows and VCS evidence, on the analysis path only.**
- `select` gains an optional row sink. `select_project_root` (legacy) passes none, so its charges and outcomes are unchanged. The base-against-head legacy probe of B1-b holds that.
- **Rows** follow SLM's walk exactly:
  - the custody reason is kept;
  - the candidate is ABSENT, PRESENT, REFUSED or NOT_EXAMINED;
  - the boundary is EXPLICIT, VCS, HOME, FS_ROOT or MOUNT, or the bare custody reason. A mount is back-patched onto the child row.
- **VCS on the analysis path.** Presence comes from `observe_child_accounted`, which costs the same as the legacy probe and returns the kind. In config and explicit modes it is one extra by-name `.git` observation.
- **The `vcs` record:**
  - a `.git`, `.hg`, `.svn` or `.jj` **directory** is `directory`;
  - a regular `.git` **file** is `indirection`. Its `gitdir:` value is read as data under S3 file custody (regular, one link, at most 4 MiB) and is never followed. A file whose custody or content does not yield a target gives target `null`. **Budget exhaustion and an identity change between observation and read still refuse the whole operation** (NBO-2), as section 3 states;
  - a `.git` of any other kind (symlink, FIFO) is still X2b's boundary, but its `vcs` record is `indirection` with target `null`. It is never read and never followed.
- **Rejected:**
  - recording rows on the legacy path, which would change accepted charges;
  - reading a symlink's target, which is a follow in all but name.

**LD-B2B3-8 (D9). Downward, a nested repository is a directory holding `.git`, `.hg`, `.svn` or `.jj` of any kind.** These are X2b's four upward markers (SL:140), observed by name when the directory is probed.

**LD-B2B3-9 (D10). The waiver reaches selection and the chain walk through new functions.**
- `--trust-project-owner` with `--project` waives the owner check on the explicit root in `select` and in `walk_project_chain`'s root judgment, **and in its recheck**. It reaches nothing else.
- New functions carry `Option<&ProjectOwnerWaiver>`. Every legacy caller is unchanged (LD-B2B-9).

**LD-B2B3-10 (D11). No downward mount rule.** SLM has none. Each judged object's ACL omission is admitted per its own filesystem by the premise (`admits`), so a mounted subtree is judged on its own terms. X2 item 1's volume rule governs the chain down to the root, not below it.

**LD-B2B3-11 (D12; r2). The FW-01 structural pin is new.**
- `tools/tests/test_discovery_fw01.py`, modeled on the environment pin (`blank`, `regions`, production reachability along `include!` edges).
- **What it covers now,** in production-reachable code:
  - `crates/host/src/configuration.rs`, which already exists, and its production includes;
  - `custody/discovery_walk.rs`, `custody/discovery_scan.rs`, `custody/discovery_rule.rs` and `grants.rs`.

  Only MB item 15's `discovery.rs`, which does not yet exist, is added by its owning unit (B2-c).
- **What it forbids:**
  - `std::process` and `Command`;
  - `TcpStream`, `UdpSocket`, `UnixStream` and `libc::socket`;
  - `OpenOptions`, `fs::write`, `fs::create*`, `fs::remove*`, `fs::rename` and `File::create`;
  - the platform's create and publish primitives.
- **Planted negatives** (spawn, socket and write) mutate a temporary copy of each covered file.

**LD-B2B3-12 (D2, D13). The flag rows go through the read path, on a new test-only seam method.**
- `ScenarioHome::discover(&self, root, request) -> Result<DiscoveryRecords, String>` runs, on the read session, **in this order (r2)**:
  1. analysis phase 1, with the explicit path and the waiver;
  2. resolution and pack admission on the captured carriers, with the CLI layer's provenance (`installation_read.rs:245-253`), which gives the winning `discovery.workspaceRoots`;
  3. phase 2;
  4. `release`, then `discovery_root`, then the walker.

  A resolution or admission failure never reaches phase 2 or any downward observation, and a control asserts it.

  It returns plain records only: the source, unit paths, the refusal code and detail, and the boundary inventory's JSON. It lends no authority.
- `crates/host/tests/discovery_tests.rs` (B2-b3c) holds the COV:5288 and COV:5388 rows. Applicability, provenance and precedence come from the source join:
  - a winning `--workspace-root` (layer 6) is `config-workspace-roots` and never falls through;
  - `--project` with `--trust-project-owner` waives exactly the owner check;
  - configuration can impersonate neither.
- `explicit-joins` has no M3 producer. Its CLI flag is M4's. The walker supports it through the request type.
- **Rejected:** the write path for tests, which needs tracking, namespace and lease state that adds nothing to these rows.

**LD-B2B3-13 (D5, traces). The test trace is a test-only thread-local log.** The `LOCAL_LOOKUPS` pattern: every observe, open and list the walker makes appends `(op, path)` under `#[cfg(test)]`. The CI and scope traces assert on it, and production carries nothing.

## 3. B2-b3b: the walker

`walk(root: DiscoveryRoot, selection: &Selected + rows, request, ledger) -> ObservedScope`, then the B2-b2 core:
- **The source is chosen first** (LD-B2B-8).
  - **Automatic mode** walks the root depth-first.
  - **Explicit and config modes** walk each named root's chain parent-first, observing `Cargo.toml`, `.git` (and the other three) and `opensip.json` by name at each level, then that root's subtree.
- **Each listed directory** goes through these steps:
  1. charge, then list (LD-B2B3-5);
  2. discard `.` and `..`, then refuse unrepresentable names and overlong paths (LD-B2B3-2);
  3. `observe_child` on each name;
  4. `classify_entry`, so a pruned anchor is its own entry only and never opened;
  5. directories of at most 256 segments are listed; at 257, only the four marker names are observed;
  6. a directory holding a VCS marker or `opensip.json` is a boundary: it is probed and never listed.
- **Unit chains and markers are judged lazily**, through the premise-applied capture normalized to `ObservedAcl`.
- **Every object whose judgment reaches the ACL** is opened from its parent and compared with its observation through `matches`. A change or absence refuses and never retries. Non-regular markers are rejected from metadata alone and never opened (LD-B2B3-3, LD-B2B3-6).
- **Exhaustion** is `WORK.BUDGET_EXHAUSTED`.

**Tests (scratch trees under the APFS test premise):**
- **Cross-check against the oracle (r2).** One tree description drives both sides:
  - **The reference.** The vector tool turns each description into SLM's `fs` and runs the bound B2-b0 reference.
  - **The native side.** The test materializes the same description as a scratch tree, walks it and runs the core.

  **What must be equal:**
  - the observed population: paths and kinds;
  - the evidence: VCS presence, kind and target on exactly the probed directories, and its absence on pruned anchors and 257-segment directories that hide a `.git`;
  - the judged objects' custody inputs: kind, owner, mode, links, size, and the normalized ACL for objects whose judgment reaches it;
  - the core's output from the native capture: every partial-provenance field except `workspaceDeclarations`, the complete boundary inventory, and the refusal and its detail.

  **The projection.** Equality is claimed for ACLs only where the walker captured one. A `NotObserved` entry is compared by kind, owner and mode only. A scratch tree cannot have a foreign owner, so owner cases stay with the pure-core vectors.

  **Descriptions include:**
  - pruned anchors (all four reasons) and 257-segment directories hiding a `.git` directory;
  - ordinary nested VCS and project boundaries;
  - explicit and config chains, including a Cargo `target` join;
  - metadata-only marker rejection (FIFO, socket, symlink);
  - mode and ACL failures set on the tree with `chmod`.
- **The CI trace (LD-B2A-5).** `.opensip/` at the root: the only operation touching it is the parent's by-name observation. `.opensip` as a file or symlink is never source and has no row.
- **The scope trace.** An explicit root beside a large sibling: the sibling never appears in the trace. A ledger sized to the named root succeeds, where automatic mode exhausts.
- **Swaps.** A same-kind swap of a chain directory and of a marker between observation and open refuses.
- **Names (r2).** An ordinary listing succeeds, with `.` and `..` discarded. These refuse with the detail: a non-UTF-8 name, a backslash name, a `.opensip-stage-x` name, a 256-scalar segment (255 is admitted), and a complete path of 4097 scalars (4096 is admitted). The scratch filesystem cannot hold a 256-byte name, so the 256-scalar case runs on the walker's name validator directly. The 255 case and both complete-path cases are native trees, opened relative to their parents.
- **Boundaries.** A nested `.git` file is never followed.
- **Non-regular markers (r2).** FIFO, socket and symlink markers, alone and beside a valid marker, give their kind reasons with no open in the trace.
- **Waiver controls (plan r4).**
- **FW-01.** A read-only (0555/0444) tree gives byte-identical records, a canary is never touched, and the structural pin runs with its negatives.
- **Exhaustion** at the cap.

## 4. Sequence

1. This plan (r2), reviewed by Codex.
2. B2-b3a: code, review, records, inventory.
3. B2-b3b: code, review, records, inventory.
4. B2-b3c: code, review, records, inventory.

Status rounds follow as they bind. B2-b4, the census, needs B2-b3b's cost model.

## 5. Not claimed

- No native unit instrument and no export (B2-c).
- No readers or members (B3-b).
- No production caller (J1).
- No CLI flag for joins (M4).
- No T2 census (B2-b4).
- No qualification.
- No law change.
