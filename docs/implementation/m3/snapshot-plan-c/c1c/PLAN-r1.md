# C1c implementation plan r1: the `node_modules` read set (M3-C r8 item 3)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 1.

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
| **C1c-0** | **The pruned-tree opener** (security, a new module `crates/security/src/snapshot_read_set.rs`), and `CaptureSession::capture_pruned` (host, `snapshot.rs`), which C2b's layout reads use (LD-C1C-2):<br>- a path below a pruned anchor is reached from the retained root by no-follow opens. Directories above the anchor are judged under S3 directory custody, as `SnapshotRoot::open` judges them (`snapshot_source.rs`:495-584). Directories at and below the anchor get descriptor discipline only (SL:266);<br>- the final regular file is opened `O_NOFOLLOW` and compared with its observation;<br>- every step is charged to the caller's ledger. | the pruned-tree reach; a symlinked component refused; an inode swap refused; first-party custody kept above the anchor; no custody judgment below it; the session's no-second-read and change rules | C1a (integrated). **Lands before C2b**, which needs it (LD-C1C-2; Q1). |
| **C1c-1** | **The read set** (security reader in `snapshot_read_set.rs`; host `CaptureSession::read_set`; sealing step 2 in `snapshot_seal.rs`):<br>- the layouts' package directories, deduplicated by `realPath` (LD-C1C-4);<br>- a bounded, iterative walk below each, by the shared rule's segments (LD-C1C-5);<br>- the suffix filter;<br>- each read through the session's one read, with origin `ReadSet`;<br>- sealing's step 2 re-check (LD-C1C-7);<br>- **the read-set term** in `snapshot_ledger_model.py`, its vectors and its cap derivation (LD-C1C-8). | C1-T12, C1-T13, C1-T14; the suffix, nested-package, VCS and Cargo exclusions; symlinks and special files; the manifest digest join; the leftover rule; the charge exactness; the model `--check` and the cap evidence | C1c-0, **and C2b's layout** (`PROPOSAL.md`:1182) |

**Order:** C1c-0, then C2b (which consumes it), then C1c-1. C1c-1 may be **authored** now against the layout record's registered schema, with test layouts admitted through it. It **integrates** only after C2b's layout, as the law's integration edge requires (`PROPOSAL.md`:1194).

## 3. Lead decisions

- **LD-C1C-1. The read set takes admitted layouts, not paths.** C1c-1's input is the set of `ResolvedNodeModulesLayoutV1` values that C2b's resolver produced, each admitted against the native-v2 schema's `$defs/ResolvedNodeModulesLayoutV1` (`native-v2.schema.json`:6971). It is never a caller's list of directories. That the layouts are the Plan-selected contexts' own is a **composition precondition**, which C4a and J2 bind: the snapshot precedes the Plan, and the host fixes the read set before any compiler runs (:304). This is the same shape as C1b's same-root join (C1b plan r3, NBO-1). The precondition is stated, not claimed as a type proof.
- **LD-C1C-2. One pruned-tree opener, for C2's reads and the read set.** Item 1 sends C2's installed-package manifest reads through the session (:209). But `SnapshotRoot::open` judges S3 directory custody, and config-file custody for a marker, on every component (`snapshot_source.rs`:495-584). Inside a pruned tree that contradicts SL:266 ("A pruned tree is never custody-walked"). It would also refuse ordinary installed trees on custody grounds that the law does not apply there.
  - So C1c-0 adds one opener for paths that lie in a pruned tree. Above the pruned anchor it judges S3 custody, as the walk and `open` do. At and below the anchor it applies item 2's descriptor discipline only: `fstatat(AT_SYMLINK_NOFOLLOW)`, `O_NOFOLLOW` opens, the inode recheck, and the before and after samples, never retried (:309; :271).
  - `package.json` below the anchor is not judged under config-file custody either, for the same reason (Q2).
  - `SnapshotRoot::open` itself is unchanged and stays the opener for first-party captures.
  - C2b's layout reads use `CaptureSession::capture_pruned`. That is why C1c-0 lands before C2b.
- **LD-C1C-3. A path is a read-set path only inside a pruned tree.** A file below a listed `realPath` that lies outside every pruned tree stays with the first-party walk, even though the directory contains it (IE:548-593: "A row outside every pruned tree stays with the first-party custody walk even when a listed `realPath` contains it").
  - So the reader never reads, and never adds, a path that the shared rule does not classify as pruned. This covers a workspace link's `realPath` into a first-party package: its files are walk rows or excluded, never read-set rows.
  - The reader decides "inside a pruned tree" by calling the shared rule (`custody/discovery_rule.rs`, `classify_path`, :156). It never copies the rule's segments (`discovery_rule.rs`:22-24 keeps them private).
- **LD-C1C-4. Package directories: `realPath`, once each.** Each layout row names a read location, `realPath` (:306; the law rejects reading through `installPath` symlinks, "Rejected").
  - Rows are deduplicated by `realPath` across all the given layouts, so a directory is walked once.
  - A `realPath` must be a `LogicalPath` after at most one trailing slash is removed (`CanonicalPath` admits a trailing slash and an interior empty segment, `native-v2.schema.json`:981-986). Any other spelling refuses `ReadSetRefusal::Layout`. Read-set rows are inventory `Blob` paths, which are `LogicalPath`s (IDS:2737-2745).
  - The evaluator's join also trims a trailing slash (`plan_native.rs`:279-281).
- **LD-C1C-5. The walk below a package directory: bounded, iterative, by the shared rule.**
  - **Descent.** A directory below `realPath` is descended unless the shared rule prunes it. That covers an exact `node_modules` segment (a nested package, which needs its own row: :306-308; IE "Nested packages have explicit custody"), a VCS segment (`.git`, `.hg`, `.svn`, `.jj`), and a Cargo `target` under a directory holding `Cargo.toml`, at any depth (SL:272-274). This is stricter than the evaluator's join, which faults Cargo output only under first-party Cargo roots (`plan_native.rs`:312-344). Not reading is always within the join.
  - **Entries.** A regular file whose name ends in one of the nine suffixes is read. Other regular files are counted in the operational report and not read. Symlinks are never followed and never inventoried. FIFOs, sockets and devices are never opened. Every one of these is counted in the report, as the walk counts them (item 2, "Entry types", :272-275).
  - **The suffix test** is an exact, case-sensitive byte suffix over the item 3 list (Q3).
  - **Names.** A name that would be read, or a directory that would be descended, must form a `LogicalPath` (:276). An unrepresentable one refuses the snapshot, with the parent and the escaped name bytes, as item 2 refuses. A non-matching file name is never read, so it is counted and not judged (Q4).
  - **No listing is collected whole.** The reader descends iteratively under held descriptors and charges every step first. It follows the bounded-walk shape of C1a1's walk (`snapshot_walk.rs`) and D3a-0's scratch walks.
  - **Custody:** descriptor discipline only below the pruned anchor (LD-C1C-2).
- **LD-C1C-6. The session's rules hold for the read set.** The read set reads through `CaptureSession`. A file captured earlier, in particular a package manifest that C2's resolver captured through `capture_pruned`, is never read again. Its observation through the read set's enumerating parent is compared with the capture's, and a difference refuses `ChangedSinceCapture` (`snapshot.rs`:237-246; :216; C1-T24). Reaching a capture sets its origin to `ReadSet`.
  - **The leftover rule** therefore covers C2's captures as well: a manifest that C2 captured but that no read-set row reaches stays a leftover, and sealing refuses it (:219).
  - **The manifest join.** For each layout row, the read set's `package.json` capture at `realPath` must have the SHA-256 that the row's `contentSha256` records. A mismatch refuses `ReadSetRefusal::ManifestDigest`. The layout must then describe the bytes the session holds (NE:1399-1419: `contentSha256` is "the raw SHA-256 of that package's manifest file bytes").
- **LD-C1C-7. Sealing's step 2 re-checks the join.** Step 2 (`snapshot_seal.rs`:273) gains the read set's structural check over the session's inventory: every `ReadSet` row lies below the `realPath` of a given layout row, with no further `node_modules` segment, and no row lies in a VCS tree. A violation is `SealError::Internal`. It cannot occur by construction, so this is defence in depth.
  - The public refusal stays the Run closure's `SNAPSHOT_PRUNED_TREE_NOT_A_READ` (IE:584; `plan_native.rs`:290).
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
  - **The bounds it uses:** at most 100,000 layout rows per layout (:6984); the read set's rows are bounded jointly with the walk's by item 5 (100,000 rows, the 4 MiB descriptor), which r9's row term already bounds by the descriptor. Listed entries that are not rows are bounded by r9's typed-refusal regime, exactly as the walk's are (RECORD-r9 §5).
  - **The gate:** C1c-1's evidence shows, by r9's own 2× rule, that r9's caps hold with the read set's row term at its dearest branch. If they do not, C1c-1 stops for a law-record revision; it never raises a cap.
  - **Rejected:** a separate read-set ledger (item 2 allows one); an uncharged read.
- **LD-C1C-9. Census inputs, and the stale interval.** C1c's census inputs:
  - **C1c-0** changes `snapshot_source.rs`'s module set and the host session (`snapshot.rs`). The snapshot ledger model pins `snapshot.rs` (`snapshot_ledger_model.py`:31, :39) and the snapshot walk's files (:77), and the companion snapshot receipt binds the model's recipe. So C1c-0 re-pins the model's file pins and regenerates its vectors (pins only; C1c-0 adds no snapshot-ledger charge, because C2's captures are charged to the ledger their caller passes, `snapshot_source.rs`:493-494). The new module joins the model's pinned files.
  - **C1c-1** adds the read-set term (LD-C1C-8). It changes the model, its vectors and the snapshot census's pinned `snapshot_seal.rs` (`snapshot_ledger_census.py`:48).
  - **Neither changes a discovery-census closure file** (`discovery_census.py`'s CLOSURE). C1c calls the shared rule and never edits it. If an edit to any closure file proves necessary, it becomes a closure change under the same rules, and the plan is revised first.
  - **The rules are C1b plan r3's LD-C1B-7, unchanged:**
    - after each sub-unit's re-pin and regeneration, `discovery_census.py --check` and `snapshot_ledger_census.py --check` pass (they compare regenerated bytes, `discovery_census.py`:1373-1379, `snapshot_ledger_census.py`:283-303);
    - the stale receipt is recorded separately, from public receipt fields only: the exact changed bindings, and the rendered stale rows and published status (`discovery_census.py`:1205-1218), with the companion receipt's status as C1a4's refresh unit defines it;
    - malformed receipts, bad pins, missing artifacts and output differences stay failures;
    - no lane, check or unit relies on a stale receipt.
  - **Which batch.** C1c-0 joins C1b's open batch if it integrates before that batch's pre-run review freezes its inputs. Otherwise it opens its own interval. C1c-1 integrates only after C2b's layout, so it most likely follows C1b's refresh. It then opens its own interval, carrying C1c-0's change if C1c-0 was not in C1b's batch. That interval's one reviewed blind validation and refresh (pre-run review, mechanical blind run, post-run review, as LD-C1B-7 states) follows C1c-1's integration. The starting baseline is whichever accepted refresh last made both receipts current.
- **LD-C1C-10. C1c and C1b touch disjoint steps of `snapshot_seal.rs`.** Step 2 is C1c's; step 4 is C1b's (C1b plan r3, LD-C1B-9). Whichever lands second rebases its edit onto the other.
  - C1c-1's step 2 edit adds no charge site. It keeps every anchor that the snapshot census reads from `snapshot_seal.rs` unique and unchanged (`snapshot_ledger_census.py`:52-57, :109).
  - `SealInputs` gains the layouts, as `Option<&[AdmittedLayout]>`, beside C1b-2's member record.
- **LD-C1C-11. Refusals are typed.** C1c returns `ReadSetRefusal {Layout, ManifestDigest, Name, Changed, Custody, Io}` beside the session's `ReadError`. Their public projection is J2's (as LD-C1B-8). Work exhaustion stays the ledger's `Budget` failure, distinct from refusal.

## 4. Controls

- **C1-T12 (C1c-1):** a pnpm layout (store `realPath`s under `node_modules/.pnpm/…`, with `installPath` links) and an npm layout (flat `node_modules/<name>`) both admit.
  - `node_modules/a/node_modules/b` is read only when `b` has its own row. Without the row, none of `b`'s files is read, even though `a`'s row encloses them.
- **C1-T13 (C1c-1):** a snapshot row injected outside every listed directory refuses at Run closure with `SNAPSHOT_PRUNED_TREE_NOT_A_READ` (`plan_native.rs`:290), and at sealing's re-check with `Internal`.
  - Every read set C1c seals passes `pruned_fault` for its layouts. A cross-check test runs the evaluator's join over sealed fixtures.
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
- **The manifest join:** a layout row whose `contentSha256` differs from the captured `package.json` refuses `ManifestDigest`.
- **`realPath` spellings:** a trailing slash is accepted. An interior empty segment, `.`, `..` or a backslash refuses `Layout`.
- **First-party containment (LD-C1C-3):** a layout row whose `realPath` is a first-party package (a workspace link) adds no read-set rows. Its files stay walk rows, or excluded rows, as the walk decided.
- **No layout:** the read set is empty, and `snapshot2` is byte-equal to C1a's for the same tree (LD-C1A-6).
- **The side record (C1-T25):** every read-set row's origin is `ReadSet`, and no identity row carries an origin.
- **Bounds:** item 5's three bounds count the read set's rows. A read set pushing the inventory one row, one descriptor byte or one total byte over the bound refuses with that field, and exactly at the bound admits.
- **Charge exactness (C1c-1):** the read-set walk's charge equals the price of its recorded calls, as D3a-0's walks are priced. The model `--check` passes, and the cap derivation is in the evidence.

## 5. Mutations

- **C1c-0:** custody judged below the anchor; a component followed through a symlink; the inode recheck skipped.
- **C1c-1:**
  - a nested `node_modules` descended without its own row;
  - the suffix filter dropped (README read);
  - a VCS directory inside a package descended;
  - `installPath` read instead of `realPath`;
  - a captured manifest read a second time;
  - the manifest join skipped;
  - a first-party path under a workspace-link `realPath` added as a read-set row;
  - sealing's re-check skipped;
  - a read uncharged.

## 6. Checks

Each sub-unit's lane, as C1a3's, C1a4's and D3a-0's are:
- the host and security suites at base and candidate, with equal failure sets and the new passing tests (platform's too, serially, if it is touched);
- rustfmt on new and base-clean files only;
- warning-denied all-targets Clippy;
- the operability source census, with the mint census by its own audit: no new `from(`, `into(`, `line(`, `pid(` or `issue(` calls, no `let _ =`, and no new environment read, tests included;
- FW-01;
- the census output checks after the sub-unit's own re-pin and regeneration, and the separate stale-receipt record while an interval is open (LD-C1C-9);
- for C1c-1, the evaluator's `plan_native` tests (the join cross-check);
- verify_design.

## 7. Open questions

- **Q1.** Is C1c-0, the pruned-tree opener and `capture_pruned`, rightly C1c's sub-unit landing before C2b, rather than part of C2b? The law's integration edge "C1c: C1a; C2b's layout" (`PROPOSAL.md`:1182) is read here as governing item 3's read set (C1c-1). C1c-0 serves item 1's capture session, which C2's reads already use (:209). The recommendation is C1c-0 in C1c, ahead of C2b.
- **Q2.** Below the pruned anchor, should a `package.json` that C2 captures be judged under config-file custody: regular, link count 1, at most 4 MiB (SL:126-128)? SL:266 says a pruned tree is never custody-walked, and item 3 applies only descriptor discipline (:309). The recommendation is no config-file custody there, with the session's own read bounds applying. Note that this leaves an installed manifest's size bounded only by item 5's 8 GiB total and the read envelope. A narrower per-manifest cap would need its source.
- **Q3.** Is the suffix test an exact, case-sensitive byte suffix over item 3's list? The law lists the suffixes but not their case. The recommendation is exact and case-sensitive. C2's table owner reviews the table with F (:310), and this plan adds no suffix.
- **Q4.** Inside a package, should a file name that is not a `LogicalPath`, and would not be read (no matching suffix), be counted and skipped rather than refused? Item 2 refuses every unrepresentable name the walk reaches. The read set, by contrast, reads only suffix-matching names. The recommendation is to refuse a name that would be read or descended, and to count the rest.
- **Q5.** Should the lead-readable T2 census gain a read-set population? Today's T2 trees carry no installed layouts that C2b's resolver has produced, so the evidence would be the model's dearest-branch derivation (LD-C1C-8), not a measured census. The recommendation is that the derivation suffices for C1c-1's gate, and that a measured read-set census follows when the harness's H-NM recipe (item 15) produces layouts.

## 8. Not delivered

- **The layout itself:** C2b (item 10).
- **The harness's no-layout configuration when item 5 refuses the read set:** H-NM (item 15).
- **The Plan's context selection and its binding of the layouts:** C4a and J2.
- **The VCS observation:** C1b.

## 9. Not claimed

- No code. No caller, no qualification, and no completion of C1 or M3-C.
