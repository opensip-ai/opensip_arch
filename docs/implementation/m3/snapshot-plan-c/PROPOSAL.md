# Sealed snapshot and Plan — proposal M3-C r1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-C** of the accepted M3 unit plan (`M3-PLAN.md:163`).

**Draft r1, not accepted. Not code.** No product crate is touched before X9-6 (M3P:5, M3P:272). Every code unit below also waits for P0, the M3-L law and I1's product units ("Units").

**Lead decisions.** Items 1 to 20 hold lead decisions dated 2026-10-04. They are made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each one names the alternatives it rejects. The owner may reverse any of them. Three are flagged to the owner in "Open questions"; none blocks this law.

## Short names

Lines were checked against the files named here on 2026-10-04.

- **M3P** `docs/implementation/m3/M3-PLAN.md` (r4, accepted). **L** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (M3-L r1, draft, acceptance-gated). **I1** `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` (r2, accepted). **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6, accepted). **Q0** `docs/implementation/m3/harness/DESIGN.md` (r13, accepted). **FS** `docs/implementation/m3/corpus/FETCH-SPEC.md`. **T2M** `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json`.
- **X12** `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` (r3, accepted). **EC1** `docs/implementation/m2/core-evaluator-closure-ec1/README.md`. **X8** `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`.
- **IE / NE / SL / WS / AQ** `docs/v2/contracts/product-v1/{identity-and-evidence,native-evidence,security-and-lifecycle,workflows-and-surfaces,admission-and-qualification}.md`. **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`. **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`. **COV** `docs/v2/architecture/implementation-coverage.v1.json`.
- **IDS** `docs/coop/design-corrections/foundation/identity-schemas.v3.json`. **NES** `docs/coop/design-corrections/native/native-evidence.schemas.v2.json`. **NEM** `docs/coop/design-corrections/native/native_evidence_model.v2.py`. **COMP** `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`. **RPP** `docs/coop/artifacts/rust-provider-protocol.v2.json`.
- Product paths are under `opensip/`, at main `30c5db1`.

## Acceptance gate

This law may be reviewed now. It can be accepted when:
- **M3-L is accepted, or its INC items 4 to 10 are unchanged** from L r1. This law states its consistency with them (item 20).
- **The B law's discovery interface is drafted**, so that item 2's input contract (units, boundaries, pruned trees, ignore paths, scope descriptor) matches B2's output.

O7 is **not** a gate item. This law launches nothing except the dependency-feature adapter of item 12, and that launch is gated on O7, D1's primitive and the D law, not decided here (L:494-506; M3P:310).

## Problem

**No source-byte reader exists.** At `30c5db1` M2 reads exactly one project file, the marker, and only to decide whether Git tracks it. `crates/security/src/custody/git_tracking.rs:1-6`: "M2 admits one closed, conventional Git layout and refuses every other layout as `vcs-unsupported`". There is no `snapshot.rs`, `plan.rs` or `imports.rs` in `crates/host/src` (M3P:122). The only snapshot builder is test-only and empty (`crates/host/src/schema_sources.rs:705`).

**What exists to build on:**
- the `snapshot2` and `plan2` identity domains (`crates/identity/src/descriptors.rs:538`, `:541`), the H frame (`digests.rs:52-68`), and the 4 MiB canonical cap (`canonical.rs:5`);
- the descriptor read discipline: `DescriptorObservationError::ChangedDuringRead` when the before, during and after samples differ (`crates/platform/src/filesystem.rs:1840`, `:1899`);
- the project custody root: `ProjectChain` (`crates/security/src/custody/project_chain.rs:201-206`) and `ProjectRootAdmission`, which "grants nothing in this unit: every grant also requires item 6a's tracking observation" (`custody/project_admission.rs:722-727`);
- the core evaluator closure of EC1 (`crates/security/src/trust/core_inventory.rs:420-430`; `initial_core.rs:238`; storage's check at `crates/storage/src/commit.rs:258`);
- the evaluator's Run-closure inspectors for contexts and nested native records (`crates/evaluator/src/native_context.rs:368`; `native_universe.rs:521`, `:555`);
- `check_plan_pack`, provided and deliberately unwired (`crates/evaluator/src/policy.rs:1358-1367`), pinned unwired by `crates/host/src/fact_admission_tests.rs:661-668`;
- a TOML 1.0 parser (`crates/identity/src/toml.rs:1-2`, `:51`).

**What the contracts leave open, and this law must close:**
- how the snapshot walk treats symlinks, special files and unrepresentable names (no contract text; item 2);
- which `node_modules` files a TypeScript context "read" before any compiler has run (IE:548-561; item 3);
- what `vcs-observation.dirty` means when the host has no Git object reader (IE:542-546; item 4);
- that the 4 MiB descriptor cap (IE:117) bounds `snapshot2` far below the protocols' 200,000 entries (item 5);
- how a `closure2` kind follows from a component manifest whose only role is `analyzer` (item 7);
- the detector closure of a bundled pack (I1 LD-10, I1:428; item 9);
- what `acquisition.descriptorId` and `preparation.importId` name, since a payload cannot name its own import (item 13);
- which closures stand as an M3 import's producer and adapter (item 13);
- how an import can correspond to the snapshot that its own configuration would bind (item 13).

## Decisions

### A. C1 — the sealed snapshot

**1. What the snapshot is: one read, and the bytes hashed are the bytes retained and analyzed.**
- **Decision.**
  - **The record.** `snapshot2` is `H("snapshot", {schemaVersion: 2, projectId, sourceInventory, resolvedConfigDigest, scopeDigest, vcsDigest})` (IE:179; IDS:197-215). `sourceInventory` is the registered `source-inventory` record: an array of `Blob {path, sha256, bytes}`, strictly ascending by path bytes, unique, at most 100,000 rows (IDS:2737-2745; IE:148-152).
  - **One read.** `crates/host/src/snapshot.rs` (CH14:495) reads every inventoried file exactly once. While reading, it writes the bytes into the invocation's candidate blob custody under their raw SHA-256, and verifies digest and length there. That custody is the storage-owned CAS the commit publishes from (`crates/storage/src/commit.rs:247-266`) for a durable request, or the temporary custody of an ephemeral one (IE:1639-1641). J1 chooses which.
  - **No second read.** After sealing, nothing reads a source file from the project again. Provider transfer, context minting, dependency import (Cargo.lock), Run retention and replay all take bytes from custody. The bytes that were hashed are the bytes every consumer sees.
  - **Sealed means closed.** A file found missing later (a context names it, a provider asks for it) is absent. It is never read late.
- **Basis:** CH14:495 ("Capture exact admitted source/read-set bytes through the selected custody boundary"); IE:1399-1415 (a replayable Run retains every source-inventory preimage); NE:2992-2995 (every child receives the sealed snapshot); SL:313-315.
- **Rejected:**
  - **Hash first, re-read for transfer or retention.** It opens a window between the hashed bytes and the analyzed bytes, which the descriptor discipline (SL:313-315) exists to close.
  - **Memory-only bytes.** A very large repository would exhaust memory, and durable retention would need a second read anyway.
- **Forbidden substitutes:** any read of project bytes after sealing; a provider or adapter reading the project filesystem; a "digest only" row whose bytes are not in custody.
- **Controls:**
  - C1-T1: bytes delivered to a recording provider sink, and the bytes retained, equal the hashed bytes, row by row.
  - C1-T2: a source pin shows that `snapshot.rs` holds the only project-file read site, and that the read precedes sealing.
  - C1-T3: a file rewritten after sealing changes nothing downstream.

**2. The walk: its extent, custody, entry types and names (relation to M2 custody).**
- **Decision.**
  - **Preconditions.** The walk starts from the retained project-root directory descriptor of the request's admitted `ProjectRootAdmission`, and only after the tracking observation has admitted it (X2 item 6a; `custody/project_admission.rs:722-727`; `git_tracking.rs:697`). It runs after X12's pack admission (X12 item 8) and B's discovery. For a durable request it runs inside the lifecycle lease that J1 orders (IE:1657-1658). The walk takes no lock itself.
  - **Extent.** It covers what the one shared discovery rule reaches (IE:548-551):
    - every regular file under the project root;
    - except pruned trees, matched by exact segment: `node_modules`, `.git`, `.hg`, `.svn`, `.jj`, and a Cargo `target` whose parent holds `Cargo.toml` (NE:711-716; SL:190-195);
    - except what lies at or below an admitted boundary: nested repositories, nested projects, and custody- or depth-excluded directories (NE:816-841; SL:281-303);
    - except Config2 `ignorePaths` (NE:928-929).

    It never descends into an excluded tree. `workspaceRoots` and `pathPrefixes` do **not** narrow the walk. They narrow the Plan's analysis (L:153), while contexts must still find configuration ancestors and lockfiles outside a narrowed root in the inventory (IE:341-351).
  - **Custody.** Every directory entered passes S3 directory custody: real directory, owner, mode and readable ACL (SL:121-126). Every marker (`Cargo.toml`, `package.json`, `tsconfig.json`, `jsconfig.json`) also passes config-file custody: regular, link count 1, at most 4 MiB (SL:126-128, SL:182). A custody failure refuses the snapshot. It never silently skips.
  - **Reads.** Each entry is examined with `fstatat(AT_SYMLINK_NOFOLLOW)` relative to its parent's descriptor, and each regular file is opened `O_NOFOLLOW` relative to that same descriptor. `st_dev`/`st_ino` are rechecked between the lstat and the open, and the before, during and after metadata samples are compared (`filesystem.rs:1899`). Any difference refuses the snapshot. It is **never retried** (SL:313-315). M2's test-only settle loops (`crates/security/src/lib.rs:130-150`) never enter product code.
  - **Entry types:**
    - **Regular file:** inventoried, whatever its content (binary, generated or vendored). U-4 forbids erasure (NE:693-702).
    - **Symlink:** never followed and never inventoried. It is recorded in the operational walk report: a count, plus paths at P2 under S-OP-2. A context or universe that names a symlinked path then refuses, because the path is not inventoried (IE:341-351).
    - **FIFO, socket or device:** never opened, so the walk cannot block. Recorded the same way.
  - **Names.** A path must be a `LogicalPath`: UTF-8 scalars, at most 4096 scalars and at most 255 per segment, no `\`, NUL, empty, `.` or `..` segment (IE:161-163; `crates/identity/src/descriptors.rs:14`, `:31`). An unrepresentable name refuses the snapshot. The refusal names the parent path and the escaped name bytes. The remedy is to rename the file, or to add its directory to `ignorePaths`. No Unicode normalization is applied (IE:122-123).
  - **`.gitignore` is not a rule.** Ignored and untracked files the walk reaches are inventoried. The only exclusions are the discovery rule's (U-4a) and `ignorePaths`.
- **Basis:** SL:105-135, SL:180-222, SL:313-315; NE:686-760, NE:816-863; IE:548-593.
- **Rejected:**
  - **Following in-root symlinks** and inventorying the target under the link's path. It breaks the `O_NOFOLLOW` discipline (SL:107), and a path can then name bytes that custody never walked.
  - **Refusing the snapshot on any symlink.** Many repositories carry symlinks in fixtures. Refusal adds nothing over non-inventory plus disclosure, since nothing reads the link.
  - **Scope-narrowed walks.** A narrowed root would refuse its own context (IE:341-351).
  - **Honouring `.gitignore`.** It is a second discovery rule (MUST-3; SL:187-190), and global excludes (`core.excludesFile`) are ambient input.
  - **Dropping an unrepresentable name** with a disclosure. U-4 has no erasure row (NE:700-702).
  - **Retrying a changed file.** SL:315: "a refusal, not a retry".
- **Forbidden substitutes:** a path-string walk (`open(path)` rather than `openat` from the retained descriptor); following a symlink; opening a non-regular file; a retry after `ChangedDuringRead`; a second exclusion rule in `snapshot.rs`; an inventoried file outside the reach of the discovery rule.
- **Controls:**
  - C1-T4: an inode swap between lstat and open refuses; a change during read refuses; neither retries.
  - C1-T5: in-root and escaping symlinks are not inventoried, and a context naming one refuses.
  - C1-T6: a FIFO in the tree neither blocks nor is opened.
  - C1-T7: non-UTF-8, backslash and 256-scalar segments refuse with the escaped bytes.
  - C1-T8: a marker with link count 2, or over 4 MiB, refuses.
  - C1-T9: `packages/target/x.ts` is inventoried; `target/` under a Cargo root is not.
  - C1-T10: a nested repository's files are not read (the boundary inventory).
  - C1-T11: two copies of one tree, differing only in `target/`, `.git/` contents or unread `node_modules` files, mint the same `snapshot2` (IE:555-557).

**3. The read set beyond the walk: installed TypeScript dependencies.**
- **Decision.**
  - **Which bytes.** The second part of `sourceInventory` holds the `node_modules` bytes that a Plan-selected TypeScript context commits to its read set (IE:552-557; SL:266-271). The host fixes that set **before** any compiler runs, deterministically, at package-directory granularity, which is the granularity replay decides (IE:584-592):
    1. C2's TypeScript resolver computes `ResolvedNodeModulesLayoutV1` (NE:1399-1420). It reads only installed package manifests, and it observes links with `readlinkat` without following them.
    2. For each layout row, C1 reads the regular files below `realPath` whose path below that directory has no further exact `node_modules` segment (IE:572-577). A file is read only when its name ends in one of `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs`, `.cjs` or `.json`. This suffix set covers `.d.ts`, `.d.mts`, `.d.cts` and `package.json`.
    3. The rows are `host-ignore-convention` members (NE:731-736).
  - **Not read:** anything else in a package (README, native `.node` binaries, maps); nested installed packages without their own row; and VCS trees or Cargo build output at any depth (SL:272-274).
  - **Custody.** A pruned tree is never custody-walked (SL:266). Its files are read under the same descriptor discipline as item 2 (`O_NOFOLLOW`, inode recheck, no retry). So the bytes analyzed are exact, while who could write them is not established. That is the host-TCB limit SL:276-278 already states.
  - **The table's owner.** The suffix table is part of C2's TypeScript resolution semantics and is reviewed with F. The provider's own refusal `node-modules-outside-read-set` (NE:2953) is the control: a read outside this set is a provider fault, never a late host read.
  - **Without a layout,** `nodeModulesInReadSet=false`, and bare specifiers are `unresolved-module-specifier` (NE:1392-1393, NE:1417-1419). The harness uses that configuration whenever item 5's bound refuses the read set (item 15, H-NM).
- **Basis:** IE:548-593; SL:266-279; NE:1399-1420, NE:2948-2953.
- **Rejected:**
  - **Every file of every listed package.** It inflates the inventory against item 5's bound with bytes no resolver reads.
  - **A compiler-traced read set.** It runs the compiler before PlanId, and before O7 permits any launch. And the trace would be a worker claim (NE:1475-1477).
  - **Reading through `installPath` symlinks.** That follows links. The layout's `realPath` is the read location.
- **Forbidden substitutes:** an implicit install; a `node_modules` read outside a layout row; a nested package authorized by an enclosing row; a host read after sealing to satisfy a provider.
- **Controls:**
  - C1-T12: pnpm and npm layouts admit, and a nested `node_modules/a/node_modules/b` needs its own row.
  - C1-T13: an injected snapshot row outside every listed directory refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ` at Run closure (IE:584).
  - C1-T14: an unread `README.md` in a package does not change `snapshot2`.

**4. The VCS observation.**
- **Decision.** `vcsDigest` hashes `{schemaVersion: 2, kind, commitId, dirty, sourceInventoryDigest}` (IE:542-546; IDS `vcs-observation`). At M3:
  - **Kind and commit.** The kind comes from X2's tracking observation. `NoRepository` gives `kind: none`, `commitId: null` and `dirty: false`. One enclosing Git repository of the closed layout gives `kind: git`. Every other layout is already refused as `vcs-unsupported` (`git_tracking.rs:1-6`). With several enclosing repositories, the innermost is used.
  - **Resolving HEAD.** `commitId` is HEAD resolved through `HEAD`, the loose ref and `packed-refs` only, read under the same descriptor discipline. Detached HEAD gives the hash. An unborn HEAD refuses as `vcs-unsupported:unborn-head`. No object is read.
  - **`dirty` means "cleanliness not established".** M3 has no Git object reader, so it cannot compare the working tree with HEAD's tree. For `kind: git` it therefore records `dirty: true`. This fails closed: a `vcs-revision` correspondence requires a clean commit (NE:2722-2728), so nothing can map through an M3 observation. At M3 nothing consumes one (imports of runtime, test and history evidence are M5).
  - **The inventory digest.** `sourceInventoryDigest` is the raw SHA-256 of the canonical inventory, retained as a blob (IE:544-545, IE:639-641).
- **Basis:** IE:542-546 ("This is source provenance; it alone never authenticates imported runtime-to-source correspondence").
- **Rejected:**
  - **A Git object reader** (zlib, pack indexes, deltas) to compute an exact `dirty`. It adds a large hostile-input parser to the TCB for provenance nothing consumes at M3.
  - **`kind: none` for a Git checkout.** That is a false statement.
  - **`dirty: false` from index stat data.** Staged changes would be invisible, so it could claim clean when the tree is not.
- **Successor:** VCS-1 (a passage making this meaning of `dirty` explicit).
- **Forbidden substitutes:** an invented commit id; `dirty: false` without proof; any environment, `$HOME` or global Git configuration read.
- **Controls:**
  - C1-T15: no repository; HEAD through a loose ref; HEAD through `packed-refs`; detached HEAD; unborn HEAD refusing; the innermost of nested repositories.
  - C1-T16: `dirty` is `true` for every Git case.
  - C1-T17: `sourceInventoryDigest` equals the inventory's canonical SHA-256.

**5. Bounds and refusals, and the size finding.**
- **Decision.** The snapshot refuses, typed and without truncation (IE:119-120), when any of these is exceeded:
  - **rows:** more than 100,000 inventory rows (IDS:2739);
  - **descriptor:** a canonical descriptor over 4 MiB (IE:117; `crates/identity/src/canonical.rs:5`);
  - **total bytes:** more than 8 GiB, which is Rust3's retained `maxSnapshotTotalFileBytes` (RPP:100; NE:2934). The snapshot is shared by every universe, so the smallest applicable bound governs. TS2 has no total.

  The library's refusal is the internal `SnapshotBound {field, observed, limit}`. Its public projection is J1's. The recommendation is S-B: make the snapshot inventory an eighth field of NE:4276's bounded family (`REQUEST.UNSATISFIABLE`, `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`), with the remedy "add `ignorePaths` or select a narrower project root". Until then no CLI reaches the refusal (M3 has none).
- **The size finding (estimate, not measurement).** A canonical inventory row is about 105 bytes plus its path. At a 50-byte mean path, 4 MiB holds about 27,000 rows. That is far below the 100,000-row schema bound and the protocols' 200,000 entries (NE:2963; RPP:99). By T2M's `treeDigest.blobEntries`, `rs-very-large-aws-sdk-rust` (245,250 entries) exceeds even the row bound. `ts-very-large-aws-cdk` (29,375), `ts-very-large-aws-sdk-js-v3` (51,178) and `py-very-large-home-assistant` (28,573) exceed the descriptor bound. A medium TypeScript repository **with** its `node_modules` read set is likely to exceed it too. S-M's SM-5 and SM-6 measure this (L:281-282).
- **Consequence.** S-R, a `snapshot2` successor that names the inventory by reference rather than inline, is **likely required** before very large T2 repositories, or `node_modules`-bearing TypeScript read sets, can be analyzed. It is conditional on SM-6. It is an identity-owner successor, and it changes no INC obligation: it re-spells one Plan input and never removes one from identity.
- **Basis:** IE:117-120; IDS:2737-2745; NE:4276.
- **Rejected:**
  - **Truncating, or dropping unread classes,** to fit. IE:119-120 forbids it.
  - **Splitting one project into several snapshots.** NE:4280 forbids sharding.
  - **Raising the 4 MiB cap in product code.** It is a contract bound.
- **Forbidden substitutes:** a partial inventory under a complete-looking identity; a refusal that mints a Plan or Run.
- **Controls:**
  - C1-T18: 100,001 rows refuse.
  - C1-T19: a 4 MiB + 1 descriptor refuses.
  - C1-T20: exactly at each bound admits.
  - C1-T21: no Plan or Run is minted on refusal, and the refusal carries field, observed value and limit.

**6. Sealing order, and what is included and excluded.**
- **Decision.**
  - **Order:**
    1. the walk (item 2);
    2. the layout and read set (item 3);
    3. sort, and the uniqueness check (IE:150-152);
    4. the VCS observation (item 4);
    5. the bounds (item 5);
    6. `H("snapshot", …)`.
  - **Bound inputs.** `projectId` comes from X2. `resolvedConfigDigest` comes from B1's resolution, which never names native-input imports (item 13). `scopeDigest` is B2's scope descriptor (NE:933-944). Snapshot and Plan carry the same configuration and scope digests (IE:1416).
  - **Included:** every regular file the walk reaches, including in-snapshot `.cargo/config(.toml)` originals (NE:1739-1741), lockfiles, markers and in-repository vendored trees; and item 3's read set.
  - **Excluded:**
    - pruned trees outside the read set, boundaries, `ignorePaths`, symlinks and special files;
    - compiler, runtime and standard-library bytes, which stay in their closures (IE:558-561);
    - Rust dependency sources, which stay in `DependencySourceSetV1` (IE:560-561);
    - prepared outputs, which are inert rows of `PreparedOutputSetV3` (NE:1803-1873);
    - OpenSIP's store and installation, which lie outside the project root;
    - every operational value: RequestId, ExecutionId, pids, wall clock and host paths (IE:104-107; L:373-394).
- **Basis:** IE:179, IE:548-593, IE:1416.
- **Rejected:** including the dependency, closure or prepared bytes in the inventory. IE:558-561 keeps each with its own owner and join.
- **Forbidden substitutes:** an operational value in any snapshot field; a context or universe minted before sealing.
- **Controls:**
  - C1-T22: the snapshot and Plan disagreeing on config or scope refuses at Run closure.
  - C1-T23: a RequestId appears in no snapshot byte (a source pin over the descriptor builder).

### B. C2 — closure admission and native contexts

**7. Closure admission: one path, from a signed manifest to a `closure2` kind.**
- **Decision.**
  - **The one path.** A `closure2` descriptor `{kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}` (IE:180; IDS `closure`) is admitted only through the signed path that SL:21-60 and BP:701-709 state:
    - the component-manifest body, under `opensip-signature-envelope.2` and a TR-INDEX catalog entry, both verified by the M2 trust owner (`crates/security/src/trust.rs`; `component_manifest.rs:395`);
    - the selected platform's TreeCommitment, projected onto regular files with exact path, sha256 and length (SL:41-48);
    - `manifestDigest` equal to the raw SHA-256 of the manifest body, envelope excluded (IE:272-276).

    A manifest for another tree, platform or component refuses (IE:276).
  - **The kind** is fixed by a closed host table keyed by the manifest's `role`. The manifest's role vocabulary is "host-owned … vocabulary extension is a host decision" (`component-manifest-schemas.v11.json`, the `role` field). M2's manifest owner admits only `analyzer`. This law fixes the table:

    | role | closure2 kind |
    |---|---|
    | `analyzer` | `provider` |
    | `toolchain` | `toolchain` |
    | `stdlib` | `stdlib` |
    | `rust-dev-llvm` | `rust-dev-llvm` |
    | `grammar` | `grammar` |

    `evaluator`, `detector` and `adapter` are never manifest roles at M3. They are reached only by the core-role rule of item 9.

    Widening the role enum is successor **CR-1**, owned by security and DR-103, and joined with D4's `components/manifest.rs` (DR-G29, BP:1033). A closure whose role maps to a kind other than the one its selecting field requires (IDS `closureKinds.byField`, IDS:4726) refuses.
  - **Retention.** Every admitted closure retains its manifest body and its whole tree (IE:1493-1499; IE:1399-1411).
- **Basis:** IE:180, IE:272-285; SL:21-60; BP:699-720; IDS:4726-4794.
- **Rejected:**
  - **A kind field asserted by the caller,** or a kind inferred from a path or file name. Either is a claim, not an admission (IE:174-175).
  - **Everything as `analyzer`/`provider`.** It breaks `closureKinds` for the toolchain, stdlib and grammar joins (IE:327-339).
- **Forbidden substitutes:**
  - a closure from a PATH lookup or system runtime (BP:715-717);
  - a semantic version standing in for a closure (IE:278);
  - a tree that includes symlink or directory rows (SL:45-47);
  - an unsigned closure in a release build.
- **Controls:**
  - C2-T1: a tree projection mismatch refuses; a manifest for another platform refuses.
  - C2-T2: a role/kind mismatch per field refuses.
  - C2-T3: a bad envelope signature refuses.
  - C2-T4: a symlink row is never followed into the tree.
  - C2-T5: the same tree under a changed version is a new `closure2`.

**8. Synthetic signed closures for tests.**
- **Decision.**
  - **The generator.** Tests build closures through one generator in security's fixture module. It sits on the joint fixture predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (X8 item 4b; X8:189-210). It writes a real component-manifest body for a supplied tree, signs the envelope and the catalog with the public deterministic fixture keys under the synthetic root (the precedent is `sign_synthetic_profile`, `crates/security/src/trust/native_census.rs:651`), and returns the signed bytes.
  - **Same admission as production.** Admission then runs the **production** path of item 7. There is no constructor that skips verification.
  - **The core.** The synthetic installation (`crates/security/src/crash_matrix_support.rs:51`, `FIXTURE = "synthetic-signed-v2"`) supplies the synthetic core. Its evaluator, detector and adapter closures follow item 9.
  - **Labels.** Every synthetic artifact carries the existing `synthetic` label (`crates/security/src/scenario.rs:51`). Harness runs that use synthetic closures over real tool bytes are labelled synthetic-trust, are never authoritative, and are never Q6 or qualification evidence (M3P:370; AQP:481).
- **Basis:** M3P:163 ("Tests use synthetic signed closures"), M3P:370; X8 item 4b.
- **Rejected:**
  - **Unsigned test closures** (`crates/host/src/schema_sources.rs:463` builds unsigned descriptors for identity tests). They bypass item 7, so the admission path would be untested.
  - **A harness-only trust root** reachable through a new feature. It is a second seam on trust admission.
- **Forbidden substitutes:** a synthetic root or key reachable in a release build; a test-only admission shortcut; a synthetic closure presented as a release closure.
- **Controls:**
  - C2-T6: synthetic closures admit through the production path.
  - C2-T7: the release build has no synthetic root (a source pin, as X8 item 4f).
  - C2-T8: a synthetic-labelled Run is refused by any authoritative surface.

**9. The detector closure for the bundled preview pack (I1 LD-10), and the other in-core role closures.**
- **Decision (the detector).** A bundled pack's detector closure is the **core detector closure**:

  > `closure2:` + H("closure", D″), where D″ is the authenticated core inventory's selected-platform descriptor, the one security already projects for the core closure (`core_inventory.rs:385-415`), with `kind` set to `"detector"` and every other member unchanged. `manifestDigest` is the raw SHA-256 of the TR-CORE-signed inventory body, envelope excluded, exactly as for EC1's evaluator closure.

  - **How it relates to the evaluator closure.** It differs from EC1's core evaluator closure **only by `kind`** (EC1 "The rule"). Security derives both from the one authenticated inventory it already holds. No new signed data, release format or trust change is needed.
  - **Where it is used.** In the `EvaluatorEmissionPlanV1` row of every rule whose policy came from a `RELEASE_PACKS` row of that core (`policy.rs:716-721`), `detectorClosure` is this closure. So is `finding.ruleClosure` for those rules' findings (IDS `closureKinds.byField`). It is a `plan.semanticClosures` member (IDS `closureMembership.direct`).
  - **The join (Run closure; wired by X12d, item 19).** For a Plan whose analysis-spec names a bundled pack:
    - every emission row of that pack names a retained `kind: detector` closure whose descriptor equals the seal's evaluator-closure descriptor except for `kind`;
    - its `contributionId` is a member of the pack row's `contributions` (I1:328).

    So the detector and the evaluator are one core release, and an evaluator or provider closure cannot stand in (COMP:9).
  - **The I1 LD-10 obligations, discharged:**
    - **signed-core provenance:** the TR-CORE signature over the inventory body;
    - **component and role joins:** TR-CORE's role over that body (IE:274-276), as EC1;
    - **retained bytes and descriptor:** the inventory body and the platform tree, retained once per store by raw SHA-256 (EC1 "Consequences");
    - **selection in the Plan:** the emission row and `semanticClosures`.
- **Decision (the in-core import roles).** Item 13 needs an `import.producerClosure` of kind `provider` and an `import.adapterClosure` of kind `adapter` (IDS:4726) for the in-core importer. These are the **core adapter closure** and the **core import-producer closure**: the same D with `kind` set to `"adapter"` and `"provider"` respectively.
  - Each is admissible **only** in that one field, of an import whose `kind` is `dependency` or `prepared`.
  - Neither is ever a `plan.semanticClosures` member, so neither can produce a view, scope, fact, stage or cache entry (IDS `closureMembership.direct`; L:206-210).
- **Successor CRC-1** (the core role closures; identity owner; the EC1 pattern). It carries:
  - the three projections;
  - the `manifestDigest` artifact text for those kinds;
  - the field restrictions and the detector join;
  - a test vector built on EC1's `baseline-macos` fixture.

  It is flagged to the owner like EC1: every core release becomes a new detector closure.
- **Consequence, disclosed.** A new core release is a new detector, so two-way baseline comparison across releases needs the core tree's `.opensip/detector-compatibility.json` listing (WS:300-316; IE:282-285) or an E0 pivot. That is M5 work. Findings' fingerprints are unaffected: `finding-key2` names no closure (IE:188).
- **Basis:** COMP:9 ("Its detectorClosure is a selected closure of kind detector. A provider or evaluator closure cannot stand in for it"); IE:1508-1512; WS:277-287; EC1; I1:392-396, I1:428.
- **Rejected:**
  - **I1 LD-10's literal form: a `closure2` whose tree is the one bundled document and whose `semanticVersion` is the pack version.** No admitted manifest describes a one-document tree, so `manifestDigest` would name a manifest of a different tree (IE:276; SL:27-32). The alternative, a signed per-pack component manifest, changes the signed release format (EC1 rejected the same thing for the evaluator). Worse, the document alone does not implement the detector. The `cycle-representative` semantics live in the core evaluator (I1 item 2). A pack-only identity would therefore stay unchanged when the code that implements the rule changes, which defeats WS:300-303's `identical-closure` law.
  - **The evaluator closure itself.** COMP:9 forbids it.
  - **A separately shipped detector component.** It contradicts X12 item 2 ("Bundled") and I1 LD-10.
  - **For the import roles:**
    - the consuming Rust provider's closure as producer: false, since the provider did not produce the record;
    - a placeholder closure: not admissible;
    - a new closure kind: `closureKinds` is closed (IDS:4726).
- **Forbidden substitutes:** a detector closure from any core other than the seal's evaluator's; a core role projection outside its one field; `kind: core` anywhere in identity (EC1 "Rejected").
- **Controls:**
  - C2-T9: the vector. D″ equals D′ except `kind`, the ids differ, and `manifestDigest` is the body's SHA-256.
  - C2-T10: an emission row naming the evaluator closure refuses.
  - C2-T11: an emission row naming another core's detector refuses.
  - C2-T12: a core adapter projection as a view producer refuses.
  - C2-T13: a core provider projection in `semanticClosures` refuses.

**10. Native contexts and universes.**
- **Decision.**
  - **Who computes.** The host resolved-inputs adapter computes every context and universe **before PlanId**, from admitted retained bytes only: snapshot rows, closure trees, imports. Nothing comes from a worker claim, a version string or the environment (NE:1460-1462, NE:1475-1477).
  - **One admission, two call sites.** The adapter admits what it minted by calling the **same** functions that Run closure re-runs over retained bytes (IE:310-325): the evaluator's `inspect_native_context` (`native_context.rs:368`) and the universe binders. Mint-time admission and Run-closure admission therefore cannot diverge.
  - **Scope.** C2 covers NE §2 entirely: the contexts (NE:1430-1645) and the universes and their binders (NE:1255-1429). M3P's C2 row cites only NE:1430-1645, but the universe binding is the same adapter (a record correction, below).
  - **TypeScript (C2b):**
    - the config graph `TypeScriptConfigGraphV1` (NE:1330-1353), with kinds from the closed basename table (NE:1355-1386);
    - the honored and stripped options (NE:1487-1488);
    - `libSelection` and the stdlib inventory join (NE:1501-1519);
    - the layout (item 3);
    - `bind_typescript_universe` (NE:1583-1598).

    The resolver is a Rust implementation of the closed resolution these sections publish. The target-default `lib` table is pinned data taken from the selected compiler closure, so the resolver reads no compiler at run time. The worker's independent recomputation is the cross-check: `Unavailable(native-context-mismatch)` before Analyze (NE:1618-1620; NE:3003-3007).
  - **Rust (C2c):**
    - `CargoConfigProjectionV2` from the in-snapshot configs: honored and stripped keys (NE:1743-1753), the two distinct digests (NE:1755-1763), and the rustflags allowlist (NE:1765-1781);
    - `ToolClosureV1` (NE:1450-1458);
    - `baseCfg`;
    - `bind_rust_universe` (NE:1279-1311).

    **`baseCfg` is pinned data:** a per-target cfg table shipped in the signed toolchain closure, never a `rustc --print cfg` run. Nothing in NE specifies its source. A data member keeps the context "from admitted, retained bytes" with no launch before PlanId.

    The Rust context also names `dependencySourceSetId`, `unifiedFeaturesId` and `preparedOutputSetId`. So it is minted only after C3 (items 12 to 14).
  - **Syntax.** `native.context.syntax.v2` over the grammar bundle is E's (M3P:165). C2 supplies the generic admission it uses.
  - **The count is checked when contexts are produced.** Contexts are deduplicated by identical descriptor, and more than 128 distinct contexts refuse at that producer boundary, before any prospective Plan exists (NE:4276).
- **Basis:** NE §2; IE:265-285, IE:297-374; BP:711-717.
- **Rejected:**
  - **Contexts computed by the provider** and accepted from its echo. Workers never mint host identities (NE:1475-1477; L:382).
  - **Running the pinned compiler or `rustc` before PlanId** to read option defaults or cfgs. That is a launch before Plan, before O7 permits any, and a tool output standing in for retained data.
  - **A context-free universe admission** path (NE:1286-1289, NE:1583-1591).
- **Forbidden substitutes:** an ambient Node, TypeScript, `rustc` or `cargo`; a field read from the environment; a stripped option read from anywhere else (NE:1488); a universe naming an uninventoried path.
- **Controls:**
  - C2-T14: NE:1622-1638's seventeen TypeScript cases as host tests.
  - C2-T15: NE:1289-1307's Rust refusals.
  - C2-T16: 129 distinct contexts refuse with `nativeContextDigests:129>128`, and identical ones collapse.
  - C2-T17: a mint-time admission and a Run-closure admission over the same bytes agree.

### C. C3 — dependency sources and prepared outputs

**11. The M3 importer: a library function, driven by the harness, with no command.**
- **Decision.**
  - **Where it lives.** `crates/host/src/imports.rs` (CH14:484) is built at M3 as a **library-only** module. It admits exactly two import kinds, `dependency` and `prepared` (NE:2671-2672), from a source path the caller names explicitly (DS-5, NE:1688-1692).
  - **What M3 leaves out.** There is no CLI, no persistent import registry and no mutation receipt. The `import` command stays at M5 (BP:957; COV:8966). This is a module built early, as D1 builds `platform/process.rs` (M3P:164). No delivery row moves.
  - **Scope of an import.** An M3 import is invocation-scoped. It is admitted in the request that consumes it and retained only through that request's Run closure. A later request imports again. Identical inputs give the identical ImportId, and the store deduplicates the bytes.
  - **Pure admission sits beside the inspectors.** The DS-1..DS-6 and PO-0..PO-4 decisions are functions over supplied observations, placed beside the evaluator's retained-input inspectors (`native_universe.rs:521`, `:555`). Admission and Run closure therefore run one implementation (IE:629-631). `imports.rs` does only the I/O.
  - **Who calls it.** At M3 only the harness (Q0) and tests call it.
- **Basis:** M3P:300 ("a library-level import of user-named sources … driven by the harness. The `import` command stays at M5"); M3P:375; NE:1688-1692.
- **Rejected:**
  - **A separate M3 module beside a later `imports.rs`.** That would be two owners of one record law (IE:629-631).
  - **Wiring `import` early.** BP:957.
  - **No import at M3.** Every T2 registry dependency would then be `input-closure-incomplete` (NE:1693-1698; M3P:300).
- **Forbidden substitutes:**
  - an implicit or ambient source (`$CARGO_HOME`, `~/.cargo`, `vendor/` outside the snapshot) not named by the caller (DS-5);
  - any network fetch in product code (NE:1691-1692);
  - an import admitted outside `imports.rs`.
- **Controls:**
  - C3-T1: a populated `CARGO_HOME` that is not named is never read (a source pin shows no environment read, plus a test).
  - C3-T2: a fetch URL, or an acquisition mode outside the closed set, refuses DS-5.
  - C3-T3: no CLI token reaches `imports.rs`.

**12. DS-1..DS-6 at M3, and the dependency-feature launch gate.**
- **Decision.** The source of truth is the Cargo.lock bytes **from the sealed snapshot** (item 1), parsed with `crates/identity/src/toml.rs:51`. Lock versions 3 and 4 only (`LockfileIdentityV1`, NES). The caller names one directory, laid out as Cargo itself lays out its sources:
  - **DS-2 (registry tarball):** `<name>-<version>.crate`, the layout of `$CARGO_HOME/registry/cache` (the native case `acquisitionSourcePath`, `native-cases.v2.json:8285`).
    - The tarball's raw SHA-256 must equal `lockChecksum`, giving `tarball-matched` and `registry-authenticated`. Any other digest is `mismatch` and refuses the whole set (NE:1666, NE:1681-1684).
    - The host extracts the tarball deterministically into custody and computes the file manifest itself. Extraction is gzip plus ustar. Only regular-file members are allowed. Every path is under the exact `<name>-<version>/` prefix and is a strict logical path. Duplicates refuse. Symlink, hardlink and device members refuse.
    - Decompressed bytes are counted as they are produced, against ProtocolLimitsV3's dependency bounds (NE:2931-2932). Exceeding them refuses; nothing is truncated.
  - **DS-1 (vendored tree):** `<name>-<version>/` with `.cargo-checksum.json`, the `cargo vendor` layout. Internal consistency only, giving `self-consistent` and `declared` (NE:1671-1680).
  - **DS-3 (git):** the tree at the locked revision, in the same layout. It is `not-applicable` and `declared`, and the file manifest is the binding (NE:1685-1686). M3 has no object reader to verify the revision.
  - **DS-4 (path):** in the snapshot; nothing is imported (NE:1687). An in-snapshot `vendor/` tree with source replacement is DS-1 with `in-snapshot-vendored` (NE:1665, NE:1745).
  - **User-named paths** get the user-input custody of NE:4207-4208. Here that means item 2's descriptor discipline and S3 directory custody over the named tree. A custody failure refuses the import.
  - **DS-6, and the launch gate.** Completeness is over the packages that `UnifiedFeaturesV1` activates (NE:1693-1697). Unified features are computed **only** by the bundled `cargo metadata --offline --frozen --locked --format-version 1 --filter-platform <target>`, through `opensip-cargo-adapter` and the CC-1..CC-5 carrier (NE:1724-1741, NE:1785-1791). So the steps are:
    1. materialize every supplied package read-only in private scratch;
    2. run the adapter;
    3. admit the set over the activated packages, as the reference does (`NEM:1820-1883`).

    A Cargo failure from a missing package is `completeness.incomplete` (NE:1789-1791), and dependent crates are `input-closure-incomplete` with cause `missing-dependency-source` (NE:1795-1801).

    **Lead decision: this adapter child is a tool launch, not a provider launch.** It runs before PlanId by contract (NE:2499-2500). L item 2's cardinality rule, which applies to provider children after Plan binding (L:129), does not govern it. The D law's launch rules do (L:494-506). Until O7 is decided and D1's primitive exists, the adapter is **unavailable**. Rust contexts can then be minted only in tests, from synthetic `UnifiedFeaturesV1` records.

    `cargo metadata` runs no build script and no proc macro (NE:1788-1789). So this is no repository-code execution.
- **Basis:** NE:1646-1801; NEM:1820-1883; M3P:355.
- **Rejected:**
  - **A Rust reimplementation of feature unification.** NE:1785 names bundled Cargo, so a reimplementation would be a substitute recipe.
  - **Activation guessed from the lockfile alone.** It over-claims completeness for platform- and feature-gated packages.
  - **Running the adapter under L item 2** as if it were a provider. It is not a provider, and L defers launch to the D law.
  - **Using the `tar` crate's extractor** with its own entry-type and path laws. The entry and path law must be this law's. A first-party ustar reader with a pure-Rust inflater is a P0 dependency-policy row.
- **Forbidden substitutes:**
  - a lockfile update or `cargo generate-lockfile` (NE:1264);
  - a system `cargo`;
  - the adapter run outside the D1 primitive;
  - a partially extracted package admitted;
  - activation from a worker claim.
- **Controls:**
  - C3-T4: the DS-1 mutation `ds1-mutation-preserving-package-checksum-stays-declared` stays declared.
  - C3-T5: the DS-2 match authenticates; a mismatch refuses the set.
  - C3-T6: extraction refusals: traversal, a symlink member, a duplicate, the wrong prefix, the decompression bound.
  - C3-T7: DS-6 with a missing package gives an incomplete set and typed Coverage, and syntax analysis is unaffected.
  - C3-T8: the adapter is refused as unavailable before D1 and O7.
  - C3-T9: CC-1, an ancestor `.cargo/config.toml`, refuses `native.ambient-cargo-config`.

**13. The import wrapper and its join to the Plan.**
- **Decision.**
  - **The wrapper.** Each admitted set becomes one `import2` (NE:2650-2657; NEM:376-415):
    - `kind` is `dependency` or `prepared`;
    - the payload is `DependencySourcePayloadV1 {set, acquisitionSourcePath, tarballDigests}` or `PreparedOutputPayloadV1 {set}` (NE:2671-2672);
    - `sourceCorrespondence` is `{kind: exact-snapshot, snapshotId}` of the analysis snapshot (NE:2722);
    - `scopeDigest` is the analysis scope descriptor (NE:2707);
    - `buildDigest` is `{schemaVersion: 1, buildIdentity: null}`;
    - `observation` has every member null;
    - `completeness` is `complete`, or `partial` with one `missing:<name> <version> <sourceId>` omission per missing package;
    - `producerClosure` and `adapterClosure` are item 9's core import-producer and core adapter closures.
  - **No self-reference.** A payload cannot name its own ImportId, because ImportId hashes the payload (IE:181; NE:2655). So in every M3 record:
    - `acquisition.descriptorId` is `null` (NES `AcquisitionV1`);
    - `preparation.importId` is `null` (NES `PreparationV3`).
  - **The join is by identity.** It has three parts:
    - a Rust context whose set has any `imported-descriptor` row joins exactly one Plan-selected `dependency` import whose `payload.set` has H identity equal to `dependencySourceSetId`;
    - an imported prepared set joins exactly one Plan-selected `prepared` import in the same way, through `preparedOutputSetId`;
    - zero or two matching imports refuse at Run closure.
  - **The configuration never names these imports.** Native-input imports enter `plan.importIds` **through that join**, not through configuration `evidence.importIds` (AQ:51). So `plan.importIds` is B1's resolved `evidence.importIds` together with the imports the Plan's contexts join. Naming them in the configuration would be circular: `snapshot2` binds `resolvedConfigDigest` (IE:179), the configuration would bind the ImportId, and the ImportId binds `snapshot2` through its correspondence.
  - **Identity reuse.** `dependencySourceSetId` contains no snapshot id, so it stays equal across source edits that leave Cargo.lock and the sources unchanged. Only the wrapper's ImportId moves. That keeps INC-3's dependency class separately addressable for a later INC-1 key (L:214-230).
  - **`acquisitionSourcePath` is kept as named.** It is a closed, required payload member (NES `DependencySourcePayloadV1`), so the ImportId, and through `plan.importIds` the PlanId, depend on the host path. That contradicts WS:1539-1541, where a user input path "never enters any content identity". At M3 the harness names its sources under a fixed per-runner root, and cross-runner Plan equality for Rust dependency imports is not claimed. The recommended fix goes to the native owner in NIJ-1.
- **Successor NIJ-1** (the native import join; native owner) covers:
  - null self-references;
  - the identity join and its Run-closure refusal;
  - native-input imports entering `plan.importIds` through the context join;
  - the producer and adapter projections (with CRC-1);
  - the `acquisitionSourcePath` disposition.
- **Basis:** NE:1665, NE:1806-1807, NE:2650-2732; IE:181, IE:220-221, IE:1370-1373; NEM:1875 (the reference copies `descriptorId` from its input with no rule); NES.
- **Rejected:**
  - **Self-referencing ids.** Impossible.
  - **A second "admitted" set record with the ids filled in.** That gives two identities for one set, and a projection no contract defines.
  - **One import per package.** 4096 packages exceed `importIds` 256 (NE:4276; IDS:538).
  - **Naming the imports in configuration.** Circular, as above.
  - **A shadow pre-configuration snapshot** as the correspondence target. It is a second `snapshot2` for bytes that are never analyzed.
  - **`vcs-revision` correspondence.** It needs a clean commit and a SourceMappingV1 (NE:2723-2728), and item 4 never proves clean.
- **Forbidden substitutes:**
  - a non-null `descriptorId` or `importId` in an M3 record;
  - a context joined to an import that is not Plan-selected;
  - a key match treated as admission (IE:1614-1615);
  - a native-input import named in configuration.
- **Controls:**
  - C3-T10: the wrapper digests match NEM's recipes (`import2-raw-digest-differs-from-semantic-identity`).
  - C3-T11: the join admits exactly one import, and zero or two refuse.
  - C3-T12: an unselected retained import is never consumed.
  - C3-T13: a body-only source edit keeps `dependencySourceSetId` and changes the ImportId.
  - C3-T14: the evaluator admits Plan-selected `dependency` and `prepared` imports as evaluation inputs with no observations (IE:1517-1518).

**14. Prepared outputs at M3: `imported-descriptor` only, explicit mode only.**
- **Decision.** M3 admits `PreparedOutputSetV3` only with `preparation.kind: imported-descriptor` and `producer.id: "external"` (NE:1806-1808; NE:2535-2537). `authorized-execution` sets are M5 (BP:992; M3P:301). The admission rules:
  - **PO-0:** exactly three row kinds, by kind and consumption channel, whatever the media type. `proc-macro-dylib` and `build-script-binary` rows, and media types outside a kind's set, refuse `native.prepared-output-not-inert`, exit 2 (NE:1815-1832).
  - **PO-4:** strict `logicalPath`s and `GeneratedInputBoundsV1` (4,096 files per owner, 64 MiB per file, 1 GiB in total, 1,024-byte paths; NE:1845-1852; NES). An archive member outside `blobs[]` is never read.
  - **PO-1:** prepared mode at M3 is only ever **explicit**. A prepared set exists only when the caller imports one and requests a `rust-cargo-prepared` cell. So the explicit branch always applies: any stale row refuses before Plan, `REQUEST.PRECONDITION_FAILED` / `native.stale-prepared-output`, listing the differing fields (NE:1853-1858). `inputBinding` must equal the current owner manifest, `dependencySourceSetId`, `toolchainDigest` (raw SHA-256 of `C(ToolchainIdentityV1)`) and `cfgSetId`.
  - **PO-2:** a `failed` row is retained, and its owner is analyzed non-prepared (NE:1859-1861).
  - **PO-3:** `declared` provenance, disclosed with the import identity and producer (NE:1862-1865).
  - **Universe and grant.** `preparedResolution` is `imported-inert` (NE:1272-1274). The semantic grant gets `read-import` and never `prepare-code` (IE:396-403; NEM:2080-2086).
  - **The owner-manifest recipe.** The owner file-manifest digest is computed with security's S10 owner-manifest recipe (SL:1076-1082) by one library function, which the harness recipe also calls. Open question R3 asks security to confirm the recipe for snapshot-member and dependency-closure-member owners.
- **Basis:** NE:1803-1873, NE:2497-2558; M3P:301, M3P:355.
- **Rejected:**
  - **The defaulted branch of PO-1** (ignore stale rows and fall back). Nothing defaults prepared mode at M3, so the branch is unreachable, and an explicit request that silently falls back would hide a stale set.
  - **`authorized-execution` sets at M3.** They need `prepare-code`, a grant and an execution. That is M5 and M5-EX (M3P:347-352).
- **Forbidden substitutes:**
  - a prepared artifact loaded, linked or executed;
  - a stale blob used;
  - a dylib row admitted under any label;
  - an expansion matched by anything but its exact site key;
  - a host-path fallback for `OUT_DIR` (NE:1840-1844).
- **Controls:**
  - C3-T15: a relabelled dylib refuses.
  - C3-T16: a media type outside its kind's set refuses.
  - C3-T17: an escaping `logicalPath` refuses.
  - C3-T18: each of the four `inputBinding` fields stale refuses, naming that field.
  - C3-T19: a failed row gives non-prepared analysis for its owner only.
  - C3-T20: `read-import` is in the grant and `prepare-code` is absent.
  - C3-T21: a retained but unselected prepared set refuses (NE:1302-1304).

**15. The harness recipes: produce, pin and regenerate. No repository code runs.**
- **Decision.** Three recipes. They are harness units (the K lane), not product code, and each is bound by Q0's M3 rule (Q0:688-692). The product side of each is the importer (items 11 to 14) or C1's read set (item 3).
  - **H-DEP (Rust dependency sources).**
    - **Produce.** The corpus fetch remains the only networked step (Q0:1121, Q0:1135). For each Rust entry, the harness reads the entry's Cargo.lock. For each registry package with a checksum, it fetches the `.crate` into the store under its SHA-256, and verifies that digest against the lock's checksum. Git packages are fetched at their locked revision, like repositories (Q0 §10). Any other source kind is recorded as unavailable and becomes a DS-6 `missing` row, never a fetch at run time.
    - **Pin.** A per-entry dependency pin `{packageKey, sha256, bytes}`, sorted, enters the T2 manifest by its canonical digest (successor T2-DEP).
    - **Regenerate.** A new repository pin re-derives its dependency pin in the same fetch.
    - **Run.** The harness lays out the pinned `.crate` files read-only in the per-workload directory `deps/<entry>/` and names that directory to the importer. `CARGO_HOME` is per-run scratch (Q0:1134).
  - **H-NM (TypeScript installed dependencies).**
    - **Produce.** The fetch pins the package tarballs named by the entry's lockfile (by integrity digest).
    - **Materialize.** Workload preparation installs into a copy-on-write working copy of the store tree (FS §6 item 1). It uses the pinned package manager, offline, from the pinned cache, with lifecycle scripts disabled. The install mode is accepted only after Q0's non-execution canary passes for it (Q0:689). The working copy is then made read-only.
    - **Fallbacks.** A repository without a lockfile, or using Plug'n'Play, runs with `nodeModulesInReadSet=false`, disclosed. So does a read set that item 5's bound refuses.
  - **H-PREP (prepared sets): declarative only.** No execution source can produce a faithful expansion or `OUT_DIR` without running the build script or proc macro (NE:2511-2517), and M3 runs neither (M3P:355; Q0:688). So:
    - **Produce.** The recipe compiles a harness-authored **declarative fixture spec** into a `PreparedOutputSetV3` (`imported-descriptor`, producer `{id: "external", version: "opensip-harness-prepared/<n>"}`). For each owner and cfg set, the spec states the directive text, the expansion text per exact site, and the generated files with their logical paths. The `inputBinding` comes from the same product library functions the importer uses, not from a second implementation.
    - **Pin.** The set's identity and import identity enter the harness freeze per fixture.
    - **Regenerate.** Any change to an `inputBinding` component (the fixture, toolchain, dependency set or cfg set) regenerates the set. PO-1's explicit refusal is the staleness detector, and regeneration is deterministic.
    - **Scope.** Prepared sets exist only for T1 fixtures and synthetic controls, including Q0:794's stale-prepared control.
- **The consequence, decided.** At M3, T2 Rust runs in `rust-cargo` (non-prepared) mode with L-RS3's disclosures (NE:614). T2 measurement of the `rust-cargo-prepared` cells waits for M5's authorized `native-prepare` and M5-EX (M3P:347-352; Q0:691). It is flagged to the owner (O-1).
- **Basis:** M3P:163, M3P:301, M3P:355; Q0:688-692, Q0:732, Q0:1119-1135; AQP:381; FS:120-125.
- **Rejected:**
  - **Preparing T2 by running build scripts** in a disposable container at M3. That executes repository code (M3P:355; Q0:691 "Deferred, not conditional").
  - **`cargo vendor` at run time.** It is a networked tool outside the fetch step.
  - **A second binding implementation in the harness.** Staleness would then be judged twice.
  - **An npm install that runs scripts.** Repository code would run.
- **Forbidden substitutes:**
  - a prepared row whose content was produced by executing repository code;
  - a network access outside `corpus fetch`;
  - a harness-installed tree written into the store;
  - a prepared set presented as `authorized-execution`.
- **Controls:**
  - H-T1: an unpinned or changed `.crate` fails the fetch.
  - H-T2: the H-NM canary for the install mode.
  - H-T3: a fixture edit changes the prepared set's identity, and the old set refuses as stale.
  - H-T4: regeneration is byte-identical on identical inputs.

### D. C4 — the Plan

**16. `plan2` and the pre-Plan order.**
- **Decision.** `crates/host/src/plan.rs` (CH14:489) mints `plan2 = H("plan", …)` over the fourteen required members (IE:182; IDS:456-470), each from one owner:

  | Member | Source |
  |---|---|
  | `snapshotId` | C1 |
  | `capabilityManifestId`, `capabilityManifestBytesDigest` | the committed CVE1 artifact and its recipe (IE:224-235) |
  | `semanticClosures` | the selected provider closures, the core evaluator closure (EC1) and the core detector closure (item 9). These are exactly the direct members (IDS:4794), and nothing a context or import already selects. |
  | `analysisSpecDigest` | the analysis-spec: B's requested capabilities; `policyPackIds` from the `AdmittedPack` (item 18); the `EnumerationPlanV1` and `EvaluatorEmissionPlanV1` parameters (COMP:9); B2's membership record (NE:745) |
  | `resolvedConfigDigest`, `scopeDigest` | B1 and B2, equal to the snapshot's (IE:1416) |
  | `nativeContextDigests` | C2, as a bare-hex canonical set (IE:297-302, IE:498-506) |
  | `importIds` | item 13's union |
  | `policyDigest` | `AdmittedPack` (X12:134) |
  | `waiverDigest` | B1's effective `WaiverSetV1`, which is empty at M3 because waiver admission is M5 (X12:229) |
  | `budget` | equal, exactly and by type, to the configuration's `analysis.budget` (IE:1417-1425) |
  | `semanticGrantDigest` | see the semantic grant below |

  **The semantic grant.** Each selected provider closure is a first-party principal with a null owner source. The operations are `read-source` and `native-analysis`, plus `read-import` exactly when `importIds` is non-empty, and never `prepare-code` at M3 (IE:525-540). An absent required permission refuses before Plan (IE:539).

  **The order** (a lead decision; each step consumes only what is already admitted):
  1. X12 pack admission, which is pure and comes first (X12 item 8);
  2. X2 project admission;
  3. B1 configuration, then B2 discovery;
  4. analysis-spec assembly and its admission (item 17);
  5. closure admission (items 7 and 9);
  6. the TypeScript layout and C1 sealing;
  7. C3 dependency import, unified features and prepared import;
  8. C2 context and universe minting and binding, with the context count checked as they are produced;
  9. the prospective Plan and its bounds (item 17);
  10. `plan2`;
  11. the host `check_plan_pack` over the just-built Plan, where a mismatch is X12 row 4 (X12:144);
  12. stage specs and `exec-plan2`.

  **Stage specs and `exec-plan2`.** Each stage spec is `{planId, producerClosure, operation, parameters, outputDomains, outputSchemaDigest}`. Its operation token comes from the selected producer's interface. Its output schema must be registered at `opensip-interface/stage-output/<operation>.schema.json` in that closure. Every parameter row must also be an analysis-spec row (IE:1288-1346).

  C4 mints no `cache2` and no `regen2` (L item 3).
- **Basis:** IE:182, IE:1360-1377, IE:1416-1425, IE:1508-1515; IDS `plan`, `closureMembership`; X12 items 8 and 9.
- **Rejected:**
  - **Pack admission inside Plan construction.** X12:138.
  - **Contexts minted after PlanId.** NE:1460-1462.
  - **A stage parameter outside the analysis-spec.** It is a hidden input (IE:1296-1298).
  - **Flattening context-selected closures into `semanticClosures`.** It is lawful (IE:1374-1376) but adds identity churn for nothing. The required minimum is selected.
- **Forbidden substitutes:**
  - `policyPackIds` or `policyDigest` from anything but an `AdmittedPack` (X12:214);
  - a budget given in two disagreeing places;
  - a Plan input supplied by a worker;
  - any operational value in the Plan;
  - a cache or regeneration key at M3.
- **Controls:**
  - C4-T1: a recomputed `plan2` vector.
  - C4-T2: a budget disagreement refuses before evaluation.
  - C4-T3: a stage parameter outside the spec refuses.
  - C4-T4: an unregistered output schema refuses `STAGE_OUTPUT_SCHEMA_UNREGISTERED`.
  - C4-T5: `read-import` appears iff imports are selected.
  - C4-T6: the host's `check_plan_pack` mismatch is row 4.

**17. The prospective-Plan bounds (NE:4276) and the analysis-spec order (NE:4278).**
- **Decision.** C4 implements NE:4276-4280 exactly:
  - **When.** `semanticClosures` (128), `nativeContextDigests` (128) and `importIds` (256) are counted on the **prospective** Plan, assembled from already-admitted inputs, **before** `plan2` is minted.
  - **The refusal.** It is `request-rejected` (2), `REQUEST.UNSATISFIABLE`, public detail `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`. No Plan and no Run are minted for the step.
  - **More than one overflow.** The subject is the first in `$defs/plan` declaration order: `semanticClosures`, `nativeContextDigests`, `importIds`.
  - **The producer boundary.** `nativeContextDigests` is also counted earlier, at item 10's producer boundary, which fires first.
  - **The analysis-spec order.** Cardinality first, conditional on the field actually being a JSON array (`requestedCapabilities`, 1024); then schema; then the closed capability vocabulary. A host-generated invalid spec is `operational-failed` (4), `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant` (NE:4278).
  - **A retained Plan over its bound** is a corrupt record. It keeps its schema-first refusal at Run closure. It is never re-projected as a request remedy (NE:4276).
- **Basis:** NE:4276-4280; the reference cases (`foundation/check-identity.py:4090-4115`).
- **Rejected:**
  - **Truncating, sharding or raising a bound** (NE:4280).
  - **Counting on the retained Plan.** It misroutes corruption (NE:4276).
- **Forbidden substitutes:** a generic schema exception for an oversized array; two subjects for one request; a Plan minted and then refused.
- **Controls:**
  - C4-T7: 129 closures, 129 contexts and 257 imports each refuse, with the exact subject.
  - C4-T8: two overflows report the first in declaration order.
  - C4-T9: a 1025-character string in `requestedCapabilities` reaches the schema step.
  - C4-T10: exactly at each bound admits and closes a Run (the pattern of `check-identity.py:4110-4115`).

**18. How the Plan cites I1's pack.**
- **Decision.** When the selection admits `Named("opensip.preview.typescript.pack:1")` (I1:405), C4:
  - writes `analysis-spec.policyPackIds = ["opensip.preview.typescript.pack:1"]` and `plan.policyDigest = 96675a5e…` (I1:317-321; X12:134);
  - commits the bundled policy bytes and the compiled `RuleProgramV2` (`e796f817…`), whose `policyDigest` equals the Plan's (IE:634-638);
  - commits an `EnumerationPlanV1` covering:
    - the `typescript` file population of the rule (COMP:26);
    - **the `imports`-cell symbol inventories of every TypeScript universe**, which item 2.5(b)'s source census reads (I1:155-167);
  - commits an `EvaluatorEmissionPlanV1` row `{ruleId: module-import-cycle, contributionId: opensip.preview.typescript, ruleStableId: module-import-cycle, semanticsMajor: 1, detectorClosure: <core detector closure>}` (I1:299; item 9);
  - requests `typescript.imports` whenever the pack is selected (I1:395).

  The provisional digests are I1's. A disagreement with I1-P's accepted record blocks C4a. It is resolved in the encoder, never in the document (I1:323).
- **Basis:** I1 item 8 (I1:390-396), item 5; X12 items 8 and 9; IE:1508-1515; COMP:9.
- **Rejected:**
  - **An emission row naming the evaluator closure** (COMP:9).
  - **An enumeration plan without the symbol inventories.** Every subject would then be indeterminate through `population-unknown`, by construction (I1:160).
- **Forbidden substitutes:** more than one pack; a merged policy; the policy read from a file or the configuration (X12:199, X12:215).
- **Controls:**
  - C4-T11: the Plan's pack fields equal I1-P's pins.
  - C4-T12: the emission row joins the core detector closure (C2-T10 and C2-T11).
  - C4-T13: a Plan without `typescript.imports` is lawful and evaluates only to indeterminate.

**19. X12d: the Run-closure pack join, and the corpus.**
- **Decision.** X12d is C4's inventory successor (X12:192). It has six parts:
  1. **The pack join.** `replay_run` (`crates/evaluator/src/replay.rs:163`) calls `check_plan_pack` after reading the Plan and before `derive_evaluation`. A refusal is X5 item 5's structural row, `EVALUATION.INPUT_REFUSED` (X12:144).
  2. **The detector join.** Item 9's join is wired at the same point, with the same row.
  3. **The unwired-pins are amended, not deleted.** `crates/host/src/fact_admission_tests.rs:661-668` and `configuration_tests.rs:449-450` pin `check_plan_pack` unwired. They become pins that it is wired exactly once, in replay.
  4. **The corpus is regenerated onto the release preview pack.** The synthetic replay corpus (`crates/storage/src/crash_matrix_support/run_candidate.rs:1-20` and its fixtures) moves onto `opensip.preview.typescript.pack:1`, with an empty `typescript` file population, so the rule evaluates nothing (I1:219). X12:192 said "onto the bundled test pack". **That cannot work:** `check_plan_pack` always uses `RELEASE_PACKS` (`policy.rs:1361-1367`), and the test registry is `cfg(test)`-private to the evaluator crate (`policy.rs:1412`). So storage, host and crash-matrix builds never see it. This is a record amendment to X12 r3's X12d text.
  5. **Dependencies.** X12d depends on I1-c (the row) and I1-b2 (the op).
  6. **The X9 rerun.** The replay change reaches the crash matrix, so X12d's evidence includes a full X9 matrix lead set on X12d's commit (`matrixPass: true`). It is serialized with every other lead run set (M3P:270).

  X12d runs **beside H**, after C4a. H depends on C4 (M3P:169), not on X12d, and J2 depends on X12d. So X12d is off the host critical chain.
- **Basis:** X12 items 9 and 10, X12:191-192; I1:396; M3P:163, M3P:170.
- **Rejected:**
  - **A feature-gated test registry reachable from downstream builds.** It is a new cfg seam on admission, and needs an X8 and X9 site-list amendment (X8:189-210).
  - **Leaving replay unwired until J.** X12:148: "it must land before any analysis producer can reach X5".
  - **Wiring only the host-side check.** A retained candidate would then bypass it.
- **Forbidden substitutes:**
  - a corpus Plan naming `"fixture"` after X12d;
  - a replay path without the join;
  - deleting the pin tests rather than amending them;
  - X9 evidence from an earlier commit offered for X12d.
- **Controls:**
  - C4-T14: replay refuses an unbundled pack, a wrong digest, and a detector from another core.
  - C4-T15: the regenerated corpus replays.
  - C4-T16: the X9 matrix passes on the X12d commit.

### E. Consistency with M3-L and the identity contract

**20. C contradicts no INC item.**
- **Plan binding (INC-1, INC-2; L items 4 and 5).** Every C record is minted under the current snapshot and Plan. C mints no cache or regeneration key, and no Plan-independent key (L:149-158, L:175-196). Equal content digests are never admission (IE:1614-1615).
- **Invalidation classes (INC-3; L item 6).** C keeps each class separately identified:
  - enumeration: the inventory;
  - configuration and native context: `resolvedConfigDigest` and the contexts;
  - tool and rule closures: closure ids and the detector;
  - dependency sources: `dependencySourceSetId`, which is snapshot-independent (item 13);
  - prepared outputs: `preparedOutputSetId`.

  A later INC-1 successor key can therefore cover every class.
- **Disclosure (INC-8; L item 10).** Operational records stay outside identity: the walk report (item 2) and import provenance. No reuse provenance enters any C record.
- **Identities and phase (L item 13).** No RequestId or RunId appears in any C record. C's only child process is item 12's adapter, under the D law.
- **The protocols (INC-5; L item 1).** C changes no protocol. Item 5's bound and the prepared-entry question (cross-law finding X-3) are recorded for L and G1b. Neither is resolved by host behaviour.
- **Changed scope (L item 3).** No changed-scope path exists. An explicit narrower scope is a different Plan (L:153), and item 2 keeps the walk independent of it.

## Successors

| ID | Kind and owner | Content | Needed before |
|---|---|---|---|
| **X12d** | inventory successor (C4b); lead | Item 19 | J2; any producer reaching X5 |
| **CRC-1** | identity contract successor; identity owner (EC1 pattern) | Item 9: the core detector, adapter and import-producer closures; the `manifestDigest` text; field restrictions; the detector join; a vector | C2a |
| **CR-1** | security / DR-103 host vocabulary successor; security owner with D4 | Item 7's role-to-kind table; widening the manifest `role` enum | C2a; F4 and G2 closure manifests |
| **NIJ-1** | native passage successor; native owner | Item 13: null self-references, the identity join, native-input imports in `plan.importIds`, the producer and adapter, the `acquisitionSourcePath` disposition | C3a |
| **VCS-1** | identity passage successor (IE:542-546) | Item 4's meaning of `dirty` | C1b |
| **S-B** | native passage successor (NE:4276) | Item 5: the snapshot inventory as the eighth bounded field | J1's public projection |
| **S-R** | identity successor, **conditional** on SM-5/SM-6 | Item 5: the inventory named by reference | T2 TypeScript with `node_modules`; very large T2 |
| **T2-DEP** | corpus manifest and FETCH-SPEC successor; Q0 §10 amendment | Item 15: dependency pins and the H-DEP and H-NM recipes | H-DEP, H-NM |
| **X12-A** | record amendment to X12 r3 | X12d's corpus target (item 19) | X12d |
| **M3P-C** | record corrections for M3P's next revision | C2 covers NE:1255-1429 too; the C3b → D1 and O7 edge; C2 is sized as three sub-units; X12d runs beside H; SM-6 compares with identity bounds (X-1) | — |

## Units

All code units wait for **X9-6** (M3P:5), **P0** (the scaffolds and dependency-policy rows, including the inflater of item 12), **M3-L's acceptance** (INC fixed), and **I1** (I1-c for C4a; I1-c and I1-b2 for X12d). Each is an inventory successor on the linear chain, numbered at launch (workflow lesson, 2026-09-30).

| Unit | Scope | Depends on | Size |
|---|---|---|---|
| **C1a** | `snapshot.rs`: walk, reads into custody, sealing, bounds (items 1, 2, 5, 6) | B2's interface; S-B for the public projection only | M |
| **C1b** | the VCS observation (item 4) | C1a; VCS-1 | S |
| **C1c** | the `node_modules` read set (item 3) | C1a; C2b's layout | S |
| **C2a** | closure admission, synthetic signed closures, core role closures (items 7 to 9) | CRC-1; CR-1 | M |
| **C2b** | TypeScript context and universe resolver, and the layout (item 10) | C2a | L |
| **C2c** | Rust context and universe: pure projection and binding (item 10) | C2a; minting after C3a and C3b | M |
| **C3a** | `imports.rs` and the DS-1..DS-6 admission, extraction and wrapper (items 11 to 13) | C1a; NIJ-1; P0's inflater row | L |
| **C3b** | the unified-features adapter invocation (item 12) | C3a; **D1's primitive, O7 and the D law** for any real launch | S |
| **C3c** | prepared import and PO-0..PO-4 (item 14) | C3a; R3 | M |
| **C4a** | `plan.rs`: Plan, bounds, grant, pack citation, stage specs (items 16 to 18) | C1, C2, C3; B1; I1-c | L |
| **C4b = X12d** | item 19 | C4a; I1-b2; X12-A; one X9 lead run set | M |
| **H-DEP, H-NM, H-PREP** | harness recipes (item 15), on the K lane | T2-DEP; C3a (H-DEP); C1c (H-NM); C3c (H-PREP) | S each |

**Order:**
- C2a → (C2b ∥ C2c);
- B2 → C1a → C1b;
- C2b → C1c;
- C1a → C3a → (C3b, C3c);
- C1, C2, C3, B1, I1-c → C4a → C4b, beside H.

**Critical path.** M3P gives C2 three days from day 0, but C2b is L-sized. Run C2b and C2c in parallel after C2a (2 + 5 days): C2 finishes by day 7, and C4 starts at day 10 at the earliest (M3P:205-208). So the host chain is unchanged, provided X12d runs beside H. C3b's real launch needs D1, which finishes on day 2 (M3P:210), so it adds no delay.

## Cross-law findings

- **X-1 (for L).** SM-6 compares the TypeScript read set with TS2's `maxSnapshotEntries` of 200,000 (L:282, L:592). The binding bounds are `snapshot2`'s 100,000 rows and its 4 MiB descriptor, about 27,000 rows (item 5). SM-5 and SM-6 should report the descriptor bytes as well.
- **X-2 (for NE, WS and the native owner).** `DependencySourcePayloadV1.acquisitionSourcePath` puts a host path into ImportId and PlanId, while WS:1539-1541 keeps user input paths out of content identity (item 13; NIJ-1).
- **X-3 (for L and G1b).** Rust3 retains v2's `maxPreparedOutputEntries` of 256 for the prepared manifest's entries (RPP:102, RPP:385; NE:2934), beside `maxExpansionRows` and `maxGeneratedFileRows` of 1,000,000 (NE:2933). If an entry is a row, an admitted set over 256 rows cannot be transferred. C3c admits by NE §3.6's bounds. The Rust protocol owner should confirm which bound governs transport (R4).
- **X-4 (for B3 and D15).** FS:120 renders multi-repository Cargo links as config-level `[patch.crates-io]` in `ws/<id>/.cargo/config.toml`. CC-5 replaces that file with the projection, and config-level `patch` is stripped (NE:1748-1751). So the links have no effect on OpenSIP's Rust analysis, and linked crates resolve as registry dependencies. B3's successor must choose a carrier that the projection honours (`[patch]` in `Cargo.toml`, NE:1746) or record the limit.
- **X-5 (for B2).** Whether the project marker directory `.opensip/` is a discovery exclusion. U-4a does not prune it, so the walk inventories `project-id.v1` (item 2). That is harmless, but it is B2's rule to state.
- **X-6 (for the native owner).** `baseCfg` has no producing recipe in NE (NE:1438, NE:1268). Item 10 decides that it is closure-shipped data. A passage could state this.

## Forbidden substitutes

In addition to each item's list:
- any project-byte read after sealing, or by a provider or adapter;
- following a symlink, opening a special file, or retrying a changed read;
- any execution of repository code: build scripts, proc macros, package scripts, or prepared content produced by execution;
- any network access in product code, or outside `corpus fetch` in the harness;
- a closure admitted other than through item 7's signed path;
- a detector closure that is not the seal's core with `kind: detector`;
- a self-referencing or non-null `descriptorId` or `importId` in an M3 record, or a native-input import named in configuration;
- a stale, dylib or out-of-bounds prepared row admitted;
- a Plan minted before its bounds are counted, or refused after minting;
- policy fields not from an `AdmittedPack`;
- a cache or regeneration key at M3;
- an operational value in any identity;
- edits to frozen contract text (successors only).

## Open questions

**For the owner.** None blocks this law. Three lead decisions are flagged, and the owner may reverse any of them:
- **O-1.** T2 measurement of the five `rust-cargo-prepared` cells waits for M5's authorized preparation (item 15). It is possible earlier only by executing repository code, which M3 forbids.
- **O-2.** Every core release becomes a new detector closure, as EC1 did for the evaluator (item 9). Cross-release baseline comparison will need compatibility listings at M5.
- **O-3.** Until S-R lands, large T2 repositories, and TypeScript repositories analyzed with `node_modules`, may refuse at item 5's bound, and the harness then falls back to `nodeModulesInReadSet=false` (item 15). Expect S-R to be needed after S-M.

**For other owners:**
- **R1. Identity owner (CRC-1).** Are three core-role projections acceptable, in particular the provider projection confined to `import.producerClosure`? Or should a native-import producer kind be added to `closureKinds`?
- **R2. Security and DR-103 owner (CR-1).** The role-to-kind table of item 7.
- **R3. Security owner.** Confirm the S10 owner file-manifest recipe used for `inputBinding.ownerFileManifestSha256` for snapshot-member and dependency-closure-member owners (SL:1076-1082). The field is `owner-retained` by security (NES).
- **R4. Rust protocol owner.** X-3.
- **R5. Native owner (NIJ-1).** Item 13's identity join, and X-2.

**For the reviewer:**
- **V1.** Is item 9's reading of COMP:9 sound? "An evaluator closure cannot stand in" is taken to refer to the closure, not to the core release, so a distinct `kind: detector` projection of the same core is lawful.
- **V2.** Is item 4's `dirty: true` ("cleanliness not established") an acceptable M3 meaning, given VCS-1?
- **V3.** Does item 13's union for `plan.importIds` conflict with any closure rule that requires `plan.importIds` to equal the configuration's `evidence.importIds`? The drafter found none: NE:4276 calls the configuration field "the selecting field" for overflow purposes only.

## Not claimed

- **Nothing was run.** No product code, cargo command, test, fetch or lead run set was run for this law. Product facts come from reading main `30c5db1`.
- **Item 5's sizes are estimates.** They come from T2M's entry counts at an assumed mean row size. S-M measures them.
- **No contract, schema, gate, threshold, register row or pinned file is changed.** The successors listed are proposals.
- **No launch rule is stated** (the D law's), and no O7 outcome is assumed.
- **Not claimed for M3:** confinement; repository-code execution; `authorized-execution` prepared sets; the `import` and `native-prepare` commands; changed-scope or cache reuse; a public projection of item 5's refusal before S-B and J1; Git object reading; T2 prepared-mode measurement.
