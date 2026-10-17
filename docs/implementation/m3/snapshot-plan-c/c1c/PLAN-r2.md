# C1c implementation plan r2: the `node_modules` read set (M3-C r8 item 3)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 2 answers Codex `codex-c1c-plan-r1` (REQUIRED-FINDINGS: three RFs, two NBOs, rulings on Q1 to Q5). r1 (`PLAN-r1.md`) is history.

## r2 changes

| Finding | Change | Where |
| --- | --- | --- |
| **R1-RF-1** (read authorization is not the outermost classifier) | `classify_path` returns only the outermost anchor (`discovery_rule.rs`:153-180), and `cargo_roots_from_markers` deliberately excludes markers inside pruned trees (:182-199). So it can neither admit `node_modules/a/lib/x.ts` nor see a nested package or a package-local `.git` or `target`. **A new shared-rule API, `read_set_path`, sits beside `classify_path` in `discovery_rule.rs`** and owns read authorization below an authorized directory. Discovery keeps `classify_path`'s outermost semantics unchanged. The reader duplicates none of the rule's tables. `discovery_rule.rs` is a discovery-census closure file, so **C1c-0 owns the API** and its whole-file closure re-pin, and the discovery receipt's binding changes (LD-C1C-9). | §2; LD-C1C-3; LD-C1C-5; LD-C1C-9; §4; §5 |
| **R1-RF-2** (ignore and boundary exclusions) | **The read set takes the walk's own admitted `SnapshotExtent`** (`snapshot_walk.rs`:69-90: B2's `AdmittedBoundaries` and the validated Config2 `ignorePaths`), with its same-root provenance as a composition precondition. Its exclusions apply before descent, before a capture is reached or its origin changed, and before inventory admission. A layout is an exception to dependency-tree pruning only; it overrides no other exclusion. A required manifest excluded this way is never inventoried: its C2 capture stays a leftover, and sealing refuses it under item 1's rule. | LD-C1C-1; LD-C1C-12 (new); LD-C1C-6; LD-C1C-7; §4; §5 |
| **R1-RF-3** (receipt-specific freshness) | The evidence is per receipt. Each lane compares the **discovery** receipt and the **companion snapshot** receipt with their own accepted baseline and current bindings. An unchanged receipt reports an empty delta and current rows. Stale rendering is required only for a receipt whose bindings changed. A standalone C1c interval is distinguished from joining C1b's batch. Every receipt must be current at the interval's final reviewed refresh. | LD-C1C-9; §6 |
| **R1-NBO-1** (derivation inputs) | LD-C1C-8 lists the full-ledger inputs: normalized and deduplicated layout bookkeeping, `read_set_path`'s charged temporaries, root reaches, buffers, overlapping-directory traversal and per-row session work. It states the cumulative walk, session, sealing, VCS and read-set subtotal. The 100,000-row limit is **per layout**. Excess setup and non-row work is placed explicitly in the typed-refusal regime. | LD-C1C-8 |
| **R1-NBO-2** (C2b inside the interval) | If C1c-0 opens a standalone interval that refreshes only after C1c-1, C2b integrates inside it. C2b must not rely on the stale companion receipt, and every intervening census-input change, C2b's own included, is tracked before the freeze. The pre-run review reconfirms the accepted baseline and the final frozen inputs. | LD-C1C-9 |
| **Q1 to Q5 rulings** | Folded in place: Q1 into §2's order; Q2 into LD-C1C-2; Q3 into LD-C1C-5; Q4 into LD-C1C-5; Q5 into LD-C1C-8. | §7 |

**Bases:**
- product main `3d1d771` (the v221 lock): C1a1 to C1a4 integrated (the capture session, the walk, sealing, the snapshot ledger profile `2^21 / 2^24 / 2^33`); D2b-2 integrated;
- the current architecture head, with the C1b plan r3 accepted and published (`c1b/PLAN-r3.md`), and the files the subject manifest names.

**Authority:**
- **The law:** M3-C r8 item 3 (`PROPOSAL.md`:302-321), with item 1's capture-session rules (:207-226), item 2's descriptor discipline, entry types and names (:271-279), item 5's bounds (:349-353) and item 6's order (:377-383). The r9 law record's caps (`c1a-r9/RECORD-r9.md`; the note at `PROPOSAL.md`:5).
- **The contracts it cites:** IE "What `sourceInventory` contains" (`docs/v2/contracts/product-v1/identity-and-evidence.md`:548-593); SL "Pruned trees and the read set (A-5)" (`security-and-lifecycle.md`:266-279); NE's `ResolvedNodeModulesLayoutV1` (`native-evidence.md`:1399-1419) and its schema (`schemas/sources/native-v2.schema.json`:6971-7015: `entries` at most 100,000, `installPath` and `realPath` `CanonicalPath`s, `contentSha256` the manifest's raw SHA-256); NE:2948-2953 (the provider's `node-modules-outside-read-set`).
- **The accepted unit plans it builds on:** the C1a plan r4 as amended by r6 (LD-C1A-6: the read set is empty until C1c, `c1a/PLAN-r6.md`:263); the C1b plan r3 (LD-C1B-7, the census batch and its stale-receipt rules; LD-C1B-9, the shared sealing file).
- **The Run-closure join it must agree with:** the evaluator's `pruned_fault` (`crates/evaluator/src/plan_native.rs`:262-292, :297-345), which refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.

## 1. What C1c delivers

The second part of `sourceInventory` (IE:548-557): the files that a Plan-selected TypeScript context commits to its read set, read once into custody through the capture session, under item 2's descriptor discipline, before sealing.
- **Which files.** For each admitted `ResolvedNodeModulesLayoutV1` row, the regular files below its `realPath` whose path below that directory has no further exact `node_modules` segment, and whose name ends in one of item 3's nine suffixes (`.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.json`; :306).
- **Not read:** everything else in a package; a nested installed package without its own row; and VCS trees or Cargo build output at any depth (:308; SL:272-274).
- **The side record.** Each row read this way carries `CaptureOrigin::ReadSet` (`snapshot.rs`:96-101), outside identity (C1-T25; :220).
- **Without a layout,** the read set stays empty, exactly as C1a seals it today (:311).

C1c does not compute the layout. That is C2b's TypeScript resolver (item 10; the law's units table, `PROPOSAL.md`:1182).

## 2. The split

| Sub-unit | Scope | Controls | Integration edge |
|---|---|---|---|
| **C1c-0** | **The pruned-tree opener** (security, a new module `crates/security/src/snapshot_read_set.rs`), `CaptureSession::capture_pruned` (host, `snapshot.rs`), which C2b's layout reads use (LD-C1C-2), and **(r2) the shared rule's `read_set_path`** in `custody/discovery_rule.rs` (LD-C1C-5), with its whole-file closure re-pin (LD-C1C-9):<br>- a path below a pruned anchor is reached from the retained root by no-follow opens. Directories above the anchor are judged under S3 directory custody, as `SnapshotRoot::open` judges them (`snapshot_source.rs`:495-584). Directories at and below the anchor get descriptor discipline only (SL:266);<br>- the final regular file is opened `O_NOFOLLOW` and compared with its observation;<br>- every step is charged to the caller's ledger. | the pruned-tree reach; a symlinked component refused; an inode swap refused; first-party custody kept above the anchor; no custody judgment below it; the session's no-second-read and change rules; **(r2)** `read_set_path`'s positive and negative cases (§4), and `classify_path`'s outputs unchanged on discovery's vectors | C1a (integrated). **Lands before C2b**, which needs it (LD-C1C-2; Q1 ruling). |
| **C1c-1** | **The read set** (security reader in `snapshot_read_set.rs`; host `CaptureSession::read_set`; sealing step 2 in `snapshot_seal.rs`):<br>- the layouts' package directories, deduplicated by `realPath` (LD-C1C-4);<br>- **(r2)** the walk's own `SnapshotExtent` applied first (LD-C1C-12);<br>- a bounded, iterative walk below each, authorized by `read_set_path` (LD-C1C-5);<br>- the suffix filter;<br>- each read through the session's one read, with origin `ReadSet`;<br>- sealing's step 2 re-check (LD-C1C-7);<br>- **the read-set term** in `snapshot_ledger_model.py`, its vectors and its cap derivation (LD-C1C-8). | C1-T12, C1-T13, C1-T14; the suffix, nested-package, VCS and Cargo exclusions; symlinks and special files; the manifest digest join; the leftover rule; the charge exactness; the model `--check` and the cap evidence | C1c-0, **and C2b's layout** (`PROPOSAL.md`:1182) |

**Order (Q1 ruling: the preparatory split is accepted):** C1c-0, then C2b (which consumes it), then C1c-1. C1c-1 may be **authored** now against the layout record's registered schema, with test layouts admitted through it. It **integrates** only after C2b's layout, as the law's integration edge requires (`PROPOSAL.md`:1194).

## 3. Lead decisions

- **LD-C1C-1. The read set takes admitted layouts, not paths.** C1c-1's input is the set of `ResolvedNodeModulesLayoutV1` values that C2b's resolver produced, each admitted against the native-v2 schema's `$defs/ResolvedNodeModulesLayoutV1` (`native-v2.schema.json`:6971). It is never a caller's list of directories. That the layouts are the Plan-selected contexts' own is a **composition precondition**, which C4a and J2 bind: the snapshot precedes the Plan, and the host fixes the read set before any compiler runs (:304). This is the same shape as C1b's same-root join (C1b plan r3, NBO-1). The precondition is stated, not claimed as a type proof. **(r2)** C1c-1 also takes the walk's own `SnapshotExtent` (LD-C1C-12).
- **LD-C1C-2. One pruned-tree opener, for C2's reads and the read set.** Item 1 sends C2's installed-package manifest reads through the session (:209). But `SnapshotRoot::open` judges S3 directory custody, and config-file custody for a marker, on every component (`snapshot_source.rs`:495-584). Inside a pruned tree that contradicts SL:266 ("A pruned tree is never custody-walked"). It would also refuse ordinary installed trees on custody grounds that the law does not apply there.
  - So C1c-0 adds one opener for paths that lie in a pruned tree. Above the pruned anchor it judges S3 custody, as the walk and `open` do. At and below the anchor it applies item 2's descriptor discipline only: `fstatat(AT_SYMLINK_NOFOLLOW)`, `O_NOFOLLOW` opens, the inode recheck, and the before and after samples, never retried (:309; :271).
  - `package.json` below the anchor is not judged under config-file custody, nor its 4 MiB marker ceiling (Q2 ruling). C2b accounts separately for its own parsing, retention and read bounds; no new unsourced per-manifest cap is introduced.
  - `SnapshotRoot::open` itself is unchanged and stays the opener for first-party captures.
  - C2b's layout reads use `CaptureSession::capture_pruned`. That is why C1c-0 lands before C2b.
- **LD-C1C-3. A path is a read-set path only inside a pruned tree.** A file below a listed `realPath` that lies outside every pruned tree stays with the first-party walk, even though the directory contains it (IE:548-593: "A row outside every pruned tree stays with the first-party custody walk even when a listed `realPath` contains it").
  - So the reader never reads, and never adds, a path that the shared rule does not classify as pruned. This covers a workspace link's `realPath` into a first-party package: its files are walk rows or excluded, never read-set rows.
  - **(r2)** The reader decides this, and everything below the authorized directory, by calling the shared rule's `read_set_path` (LD-C1C-5). It never copies the rule's segments (`discovery_rule.rs`:22-24 keeps them private).
- **LD-C1C-4. Package directories: `realPath`, once each.** Each layout row names a read location, `realPath` (:306; the law rejects reading through `installPath` symlinks, "Rejected").
  - Rows are deduplicated by `realPath` across all the given layouts, so a directory is walked once.
  - A `realPath` must be a `LogicalPath` after at most one trailing slash is removed (`CanonicalPath` admits a trailing slash and an interior empty segment, `native-v2.schema.json`:981-986). Any other spelling refuses `ReadSetRefusal::Layout`. Read-set rows are inventory `Blob` paths, which are `LogicalPath`s (IDS:2737-2745).
  - The evaluator's join also trims a trailing slash (`plan_native.rs`:279-281).
- **LD-C1C-5. The walk below a package directory: bounded, iterative, by the shared rule.**
  - **(r2, R1-RF-1) The authorization API.** `classify_path` (`discovery_rule.rs`:153-180) answers "which outermost pruned tree holds this path", and discovery keeps that answer, unchanged. Read authorization is a different question, so C1c-0 adds **`read_set_path(authorized, relative, package_cargo_roots) -> ReadSetPath`** to `discovery_rule.rs`, beside it and over the same private tables (`DEPENDENCY_TREE_SEGMENT`, `VCS_TREE_SEGMENTS`, `CARGO_BUILD_OUTPUT_SEGMENT`, :22-24). It decides:
    - **the authorized directory's own ancestry:** `authorized` must lie inside a dependency tree (an exact `node_modules` segment), and no segment of it may be a VCS segment. Otherwise it refuses `ReadSetPath::Forbidden`;
    - **ordinary descendants are admitted:** `node_modules/a/lib/x.ts` below `node_modules/a`;
    - **a further exact `node_modules` segment below `authorized` stops** the descent: a nested package needs its own row (:306-308; IE "Nested packages have explicit custody");
    - **VCS segments are excluded throughout the whole path,** above, at and below `authorized` (SL:272-274; IE: "the VCS exclusion uses exact segments at every depth");
    - **package-local Cargo output is excluded:** a `target` directory is excluded when its parent directory below `authorized` holds `Cargo.toml`. Package-local Cargo roots are found by a package-local marker derivation, parent first, in the rule as `cargo_roots_from_markers` derives first-party roots (:182-199). The reader supplies the markers it has listed, not a root set of its own.

    The API allocates only charged temporaries, and their costs are published beside it. Discovery's callers of `classify_path` and `cargo_roots_from_markers` are unchanged, and their vectors are re-checked byte for byte.
  - **Descent.** A directory below `realPath` is descended exactly when `read_set_path` admits it as a directory. This is stricter than the evaluator's join, which faults Cargo output only under first-party Cargo roots (`plan_native.rs`:312-344). Not reading is always within the join, and the evaluator cross-check alone does not validate the stricter exclusion, so the read-set controls test it directly.
  - **Entries.** A regular file whose name ends in one of the nine suffixes is read. Other regular files are counted in the operational report and not read. Symlinks are never followed and never inventoried. FIFOs, sockets and devices are never opened. Every one of these is counted in the report, as the walk counts them (item 2, "Entry types", :272-275).
  - **The suffix test** is an exact, case-sensitive byte suffix over the raw name bytes, against item 3's nine suffixes (Q3 ruling). Declaration files are included by their `.ts`, `.mts` or `.cts` ending. There is no extra suffix, no case folding and no compiler-driven late read. The table stays C2's and F's.
  - **Names (Q4 ruling).** Every candidate row, and every directory actually descended, must form a `LogicalPath` (:276). A malformed one refuses the snapshot with the parent and the escaped name bytes. A regular-file name without a matching suffix is outside item 3's read set: it is filtered on its raw bytes before any `LogicalPath` admission, so a non-UTF-8 name is handled safely, then counted and disclosed, never read. This is the read set's suffix exclusion. It does not weaken the first-party walk's name rule.
  - **No listing is collected whole.** The reader descends iteratively under held descriptors and charges every step first. It follows the bounded-walk shape of C1a1's walk (`snapshot_walk.rs`) and D3a-0's scratch walks.
  - **Custody:** descriptor discipline only below the pruned anchor (LD-C1C-2).
- **LD-C1C-6. The session's rules hold for the read set.** The read set reads through `CaptureSession`. A file captured earlier, in particular a package manifest that C2's resolver captured through `capture_pruned`, is never read again. Its observation through the read set's enumerating parent is compared with the capture's, and a difference refuses `ChangedSinceCapture` (`snapshot.rs`:237-246; :216; C1-T24). Reaching a capture sets its origin to `ReadSet`.
  - **The leftover rule** therefore covers C2's captures as well: a manifest that C2 captured but that no read-set row reaches stays a leftover, and sealing refuses it (:219).
  - **The manifest join, per row.** For each layout row, the `package.json` capture at its `realPath` must have the SHA-256 that the row's `contentSha256` records. A mismatch refuses `ReadSetRefusal::ManifestDigest` (NE:1399-1419: `contentSha256` is "the raw SHA-256 of that package's manifest file bytes"). The join is kept **per layout row** even when several rows share one `realPath`, so conflicting digests refuse rather than vanish in deduplication.
  - **(r2) A first-party workspace-link manifest** may already be a `Walk` capture. Its digest join reads that capture, and does not convert it into a `ReadSet` row (LD-C1C-3).
  - **(r2) An excluded manifest** (LD-C1C-12) is never reached by the read set. Its C2 capture keeps no origin, and sealing refuses it as a leftover (:219).
- **LD-C1C-7. Sealing's step 2 re-checks the join.** Step 2 (`snapshot_seal.rs`:273) gains the read set's structural check over the session's inventory: every `ReadSet` row lies below the `realPath` of a given layout row, with no further `node_modules` segment, and no row lies in a VCS tree. A violation is `SealError::Internal`. It cannot occur by construction, so this is defence in depth.
  - The public refusal stays the Run closure's `SNAPSHOT_PRUNED_TREE_NOT_A_READ` (IE:584; `plan_native.rs`:290).
  - **(r2)** The check also applies the walk's `SnapshotExtent` exclusions and `read_set_path`'s rule, so the reader and the check agree after RF-1 and RF-2.
  - It is a structural guard. It does not prove the host performed every permitted read, which IE treats as a host-TCB observation (IE:548-593).
  - Step 2 allocates nothing and adds no charge.
  - Item 5's bounds already count both parts, since `session.inventory()` yields every reached capture.
- **LD-C1C-8. The read set is charged to the snapshot ledger, and the r9 derivation gains a read-set term.**
  - Item 2 charges the walk to one snapshot ledger (:250). The read set is item 6's step 2, and is charged to the same ledger, the `WorkScope` its caller passes.
  - **The term**, owned by C1c-1 as C1b-1 owns the VCS term (C1b plan r3, LD-C1B-6). It covers:
    - each package directory's reach from the root, at most the `CanonicalPath`'s 4,096 scalars of components (`native-v2.schema.json`:984);
    - each listing, status and descent;
    - each read row's session cost, as the walk's row is priced;
    - each counted non-row entry.
    Every part is priced under its existing owner's pricing.
  - **(r2, R1-NBO-1) The full-ledger inputs**, each priced explicitly:
    - the layouts' normalized and deduplicated bookkeeping (the `realPath` set and the per-row digest joins);
    - `read_set_path`'s charged temporaries, and those of the package-local Cargo-root derivation;
    - each package directory's root reach;
    - the session's read buffer, and any reader buffers;
    - traversal of overlapping directories (a `realPath` inside another's subtree), counted once per actual descent;
    - per-row session work, as the walk's rows are priced.
  - **The bounds it uses:**
    - at most 100,000 entries **per layout** (`native-v2.schema.json`:6984). That is not a bound on the number of layouts, and no source bounds the layout count;
    - the read set's rows are bounded jointly with the walk's by item 5 (100,000 rows, the 4 MiB descriptor), which r9's row term already bounds by the descriptor. The descriptor bounds the combined inventory, not all layout-processing work.
  - **The typed-refusal regime:** listed non-row entries, layout setup beyond the rows that fit, and overlapping traversal are placed explicitly in r9's typed-refusal regime (RECORD-r9 §5), as the walk's non-row entries are.
  - **The gate (Q5 ruling):**
    - C1c-1's evidence states the full cumulative subtotal (walk, session, sealing, C1b's VCS term when accepted, and the read set), with soundness vectors;
    - it shows the full fixed-cap evidence: r9's caps hold by r9's own 2× rule;
    - a conservative derivation, with synthetic and native soundness and boundary controls, gates C1c-1 while no admitted-layout T2 population exists. The existing no-layout census is not read-set evidence. A measured installed-layout population follows when H-NM supplies it.
    - If the caps do not hold, C1c-1 stops for a law-record revision; it never raises a cap.
  - **Rejected:** a separate read-set ledger (item 2 allows one); an uncharged read.
- **LD-C1C-9 (r2, R1-RF-3, R1-NBO-2). Census inputs, per receipt.**
  - **The two receipts and what each binds:**
    - **the discovery receipt** binds its tool, its CLOSURE, the member model, the sizes, the caps, the root lengths and the reference inputs (`receipt_bindings`, `discovery_census.py`:1086-1095). It does not bind `snapshot.rs`, `snapshot_source.rs`, `snapshot_seal.rs`, the snapshot model or the new read-set module;
    - **the companion snapshot receipt**, as C1a4's refresh unit defines it, binds the snapshot cost-source closure and recipe (C1A4-R1-NBO-1).
  - **What each sub-unit changes:**
    - **C1c-0** changes `discovery_rule.rs`, a CLOSURE file (r2, R1-RF-1), so it re-pins it whole and regenerates the discovery census's records. **This changes the discovery receipt's bindings.** It also changes `snapshot_source.rs`'s module set and the host session (`snapshot.rs`). The snapshot model pins both (`snapshot_ledger_model.py`:31, :39, :77), so it re-pins them and regenerates the model's vectors (pins only; C1c-0 adds no snapshot-ledger charge, because C2's captures are charged to the ledger their caller passes, `snapshot_source.rs`:493-494). The new module joins the model's pinned files. **This changes the companion receipt's bindings.**
    - **C1c-1** adds the read-set term (LD-C1C-8), changing the model, its vectors and the snapshot census's pinned `snapshot_seal.rs` (`snapshot_ledger_census.py`:48). **This changes the companion receipt's bindings, not the discovery receipt's.**
  - **The evidence is receipt-specific.** Each lane compares each receipt with its own accepted baseline and its current bindings:
    - a receipt whose bindings did not change reports an empty delta, and its rendered rows stay current (for example, the discovery receipt in C1c-1's lane, if no closure input changed since its last refresh);
    - stale rendering is required only for a receipt whose bindings changed, naming the exact changed bindings: the rendered `outstanding: held-out (blind receipt stale)` rows and the published `heldOutMargin: outstanding` (`discovery_census.py`:1205-1218), or the companion receipt's published status;
    - no fabricated staleness is required as evidence;
    - the generated-output checks, `discovery_census.py --check` and `snapshot_ledger_census.py --check`, pass after each sub-unit's own re-pin and regeneration (they compare regenerated bytes, `discovery_census.py`:1373-1379, `snapshot_ledger_census.py`:283-303);
    - malformed receipts, bad pins, missing artifacts and output differences stay failures;
    - no lane, check or unit relies on a stale receipt.
  - **Two cases, distinguished:**
    - **Joining C1b's batch.** If C1c-0 integrates while C1b's batch is open and before its pre-run review freezes the inputs, C1c-0's changes join that batch. Both receipts are already stale from C1b-0's integration. C1c-0's lane names its own changed bindings in addition to C1b's, and the batch's one refresh covers it.
    - **A standalone C1c interval.** Otherwise, C1c-0 opens its own interval at its integration, with both receipts stale for its own bindings only. The interval's refresh follows C1c-1, unless C2b requires current evidence first, in which case C1c-0 refreshes separately.
  - **(R1-NBO-2) C2b inside a standalone interval.** If the interval spans C2b's integration:
    - C2b must not rely on the stale companion receipt or the stale discovery receipt;
    - every intervening census-input change, C2b's included, is tracked as the batch's input before the freeze;
    - the pre-run review reconfirms the exact accepted baseline and the final frozen inputs.
  - **The refresh.** Each interval's one reviewed blind validation and refresh (pre-run review, the mechanical blind run, post-run review; C1b plan r3 LD-C1B-7) makes **every** receipt current for the final inputs, and both freshness checks pass. The starting baseline is whichever accepted refresh last made each receipt current.
- **LD-C1C-10. C1c and C1b touch disjoint steps of `snapshot_seal.rs`.** Step 2 is C1c's; step 4 is C1b's (C1b plan r3, LD-C1B-9). Whichever lands second rebases its edit onto the other.
  - C1c-1's step 2 edit adds no charge site. It keeps every anchor that the snapshot census reads from `snapshot_seal.rs` unique and unchanged (`snapshot_ledger_census.py`:52-57, :109).
  - `SealInputs` gains the layouts, as `Option<&[AdmittedLayout]>`, beside C1b-2's member record.
- **LD-C1C-12 (r2, R1-RF-2). The admitted extent binds the read set.** A layout is an exception to dependency-tree pruning only. It is not authority to override any other exclusion that item 6 keeps: boundaries and `ignorePaths` (:393).
  - **The input.** C1c-1 takes the walk's own `SnapshotExtent` (`snapshot_walk.rs`:69-90): B2's `AdmittedBoundaries` and the validated Config2 `ignorePaths`. It is the same value the walk used, and its same-root provenance (`AdmittedBoundaries`' selected root) is a composition precondition, as LD-C1C-1's is.
  - **Where it applies:** before any descent, before a capture is reached or its origin changed, and before inventory admission. An excluded `realPath`, or an excluded path below it, is never read and never inventoried.
  - **A required manifest excluded this way:** its C2 capture stays a leftover, and sealing refuses it under item 1's rule (:219). It is never silently inventoried.
  - **The workspace-link behaviour** (LD-C1C-3) is unchanged.
- **LD-C1C-11. Refusals are typed.** C1c returns `ReadSetRefusal {Layout, ManifestDigest, Name, Changed, Custody, Io}` beside the session's `ReadError`. Their public projection is J2's (as LD-C1B-8). Work exhaustion stays the ledger's `Budget` failure, distinct from refusal.

## 4. Controls

- **C1-T12 (C1c-1):** a pnpm layout (store `realPath`s under `node_modules/.pnpm/…`, with `installPath` links) and an npm layout (flat `node_modules/<name>`) both admit.
  - `node_modules/a/node_modules/b` is read only when `b` has its own row. Without the row, none of `b`'s files is read, even though `a`'s row encloses them.
- **C1-T13 (C1c-1):** a snapshot row injected outside every listed directory refuses at Run closure with `SNAPSHOT_PRUNED_TREE_NOT_A_READ` (`plan_native.rs`:290), and at sealing's re-check with `Internal`.
  - Every read set C1c seals passes `pruned_fault` for its layouts. A cross-check test runs the evaluator's join over sealed fixtures.
- **(r2, R1-RF-1) `read_set_path`:**
  - `node_modules/a/lib/x.ts` below `node_modules/a` is admitted;
  - a pnpm store path (`node_modules/.pnpm/a@1/node_modules/a/index.js` below its `realPath`) is admitted;
  - `node_modules/a/node_modules/b/x.ts` is refused below `node_modules/a`, and admitted below `b`'s own row;
  - a VCS segment above, at and below `realPath` is refused in each position (`.git/node_modules/a`, `node_modules/.git`, `node_modules/a/.git/x.js`);
  - package-local Cargo output (`node_modules/a/target/x.js` beside `node_modules/a/Cargo.toml`) is excluded, while `node_modules/a/target/x.js` with no `Cargo.toml` is read;
  - a `realPath` outside every dependency tree is `Forbidden`;
  - `classify_path` and `cargo_roots_from_markers` are byte-unchanged on discovery's vectors.
- **(r2, R1-RF-2) The extent:**
  - a layout row whose `realPath` is under an `ignorePaths` entry adds no row, and its C2-captured manifest refuses as a leftover;
  - a `realPath` below an admitted boundary adds no row;
  - an `ignorePaths` entry inside a package excludes just that subtree;
  - the workspace-link control is kept.
- **C1-T14 (C1c-1):** an unread `README.md`, a `.map` file and a `.node` binary in a package do not change `snapshot2`.
- **The suffix filter:** each of the nine suffixes is read, including `.d.ts`, `.d.mts` and `.d.cts` as `.ts`, `.mts` and `.cts`. `X.TS`, `x.ts.bak` and `x.json5` are not read (Q3).
- **The exclusions at depth:** a `.git` directory, and a `target` beside a `Cargo.toml`, inside a package are never read. A `target` with no `Cargo.toml` beside it is read normally.
- **Links and special files:** a symlink inside a package is not followed or inventoried. A FIFO is not opened and does not block. Both are counted.
- **Descriptor discipline (C1c-0, C1c-1):** an inode swap between status and open refuses, and a change during the read refuses. Neither is retried. A symlinked component on the way to `realPath` refuses rather than being followed.
- **Custody above and below the anchor (C1c-0):** a first-party directory that fails S3 custody above the anchor refuses. A group-writable directory below the anchor is read: no custody judgment applies there (SL:266).
- **The session (C1c-1):**
  - a manifest captured by `capture_pruned` and reached by the read set is not read twice (the C1A-T1 spy), and its origin becomes `ReadSet`;
  - a manifest rewritten between its capture and the read set refuses `ChangedSinceCapture`;
  - a captured manifest that no row reaches refuses as a leftover.
- **The manifest join:** a layout row whose `contentSha256` differs from the captured `package.json` refuses `ManifestDigest`. Two rows sharing one `realPath` with different digests refuse. A workspace-link row's join reads the `Walk` capture and leaves its origin `Walk`.
- **`realPath` spellings:** a trailing slash is accepted. An interior empty segment, `.`, `..` or a backslash refuses `Layout`.
- **First-party containment (LD-C1C-3):** a layout row whose `realPath` is a first-party package (a workspace link) adds no read-set rows. Its files stay walk rows, or excluded rows, as the walk decided.
- **No layout:** the read set is empty, and `snapshot2` is byte-equal to C1a's for the same tree (LD-C1A-6).
- **The side record (C1-T25):** every read-set row's origin is `ReadSet`, and no identity row carries an origin.
- **Bounds:** item 5's three bounds count the read set's rows. A read set pushing the inventory one row, one descriptor byte or one total byte over the bound refuses with that field, and exactly at the bound admits.
- **Charge exactness (C1c-1):** the read-set walk's charge equals the price of its recorded calls, as D3a-0's walks are priced. The model `--check` passes, and the cap derivation is in the evidence.

## 5. Mutations

- **C1c-0:**
  - custody judged below the anchor; a component followed through a symlink; the inode recheck skipped;
  - **(r2)** `read_set_path` stopping at the outer `node_modules` (ordinary descendants refused), passing a nested `node_modules`, checking VCS segments only below `realPath`, or ignoring package-local Cargo roots.
- **C1c-1:**
  - a nested `node_modules` descended without its own row;
  - the suffix filter dropped (README read);
  - a VCS directory inside a package descended;
  - `installPath` read instead of `realPath`;
  - a captured manifest read a second time;
  - the manifest join skipped;
  - a first-party path under a workspace-link `realPath` added as a read-set row;
  - sealing's re-check skipped;
  - a read uncharged;
  - **(r2)** `ignorePaths` not applied to the read set; a boundary not applied; an excluded manifest inventoried.

## 6. Checks

Each sub-unit's lane, as C1a3's, C1a4's and D3a-0's are:
- the host and security suites at base and candidate, with equal failure sets and the new passing tests (platform's too, serially, if it is touched);
- rustfmt on new and base-clean files only;
- warning-denied all-targets Clippy;
- the operability source census, with the mint census by its own audit: no new `from(`, `into(`, `line(`, `pid(` or `issue(` calls, no `let _ =`, and no new environment read, tests included;
- FW-01;
- **(r2)** for C1c-0, discovery's own vectors re-checked byte for byte, and the discovery census's records regenerated after the CLOSURE re-pin;
- the census output checks after the sub-unit's own re-pin and regeneration, and the receipt-specific freshness record, per receipt, while an interval is open (LD-C1C-9);
- for C1c-1, the evaluator's `plan_native` tests (the join cross-check);
- verify_design.

## 7. Open questions

r1's Q1 to Q5 are ruled (`codex-c1c-plan-r1`) and folded in place:
- **Q1:** §2's order;
- **Q2:** LD-C1C-2;
- **Q3** and **Q4:** LD-C1C-5;
- **Q5:** LD-C1C-8.

No question is open in r2.

## 8. Not delivered

- **The layout itself:** C2b (item 10).
- **The harness's no-layout configuration when item 5 refuses the read set:** H-NM (item 15).
- **The Plan's context selection and its binding of the layouts:** C4a and J2.
- **The VCS observation:** C1b.

## 9. Not claimed

- No code. No caller, no qualification, and no completion of C1 or M3-C.
