# Component release installation and tree custody — proposal CI r1

**Lead law proposal r1, 2026-10-17. Proposed; it needs Codex review. Not code.** The lead owns this law as DR-103's delivery owner. It answers cross-law item X-C2A-1 (`snapshot-plan-c/c2a/X-C2A-1-r1.md`, the input memo) and the assessment of that memo in `codex-c2a-plan-r2`.

**Why it exists.** M3-C r8 item 7 admits a component closure only if it "retains its manifest body and its whole tree" (`snapshot-plan-c/PROPOSAL.md`:430). NE requires the stdlib and compiler closures retained **whole**, re-admitted before any digest comparison (NE:1493-1499). Today nothing provides those bytes.
- The trust side carries metadata only: X4B's bootstrap carries the catalog and the component-manifest pairs (`m2/trust-bootstrap-x4b/PROPOSAL.md`:100-137); unit 463h retains those pairs; the ordinary reader joins a validated manifest to its catalog release, envelope and preimage (`crates/security/src/trust_ordinary_metadata.rs`:90-160).
- A verified catalog is not tree custody (`codex-c2a-plan-r1`, Q3 ruling).

This law defines the one path by which a signed component release's tree bytes enter installation custody, and the one interface by which C2a-3 reads them back.

**Nothing in it is pre-approved** (`codex-c2a-plan-r2`): the archive format, the storage authority, the installation action and every exception below are proposals, each with its rationale.

## Short names

- **SL / WS / IE / NE**: `docs/v2/contracts/product-v1/{security-and-lifecycle,workflows-and-surfaces,identity-and-evidence,native-evidence}.md`.
- **PKG**: `docs/coop/artifacts/component-packaging-contract.v14.json` (SHA-256 `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c`), standing CANDIDATE-NOT-APPLIED, register row DR-120. **PKG-AP** is its `archiveProfile` member (`opensip-archive-profile.1`, from line 1612).
- **CMS**: `docs/coop/artifacts/component-manifest-schemas.v11.json` (SHA-256 `1c0b8868…a017a005`), the delivery selector SL:30-32 names.
- **MC**: M3-C r8 (`snapshot-plan-c/PROPOSAL.md`).
- **CM**: the product's admitted manifest owner, `crates/security/src/component_manifest.rs`, and its generated shape (`generated/component_manifest_shape.rs`).
- **RC**: the product's catalog shape, `crates/security/src/trust/recovery_catalog.rs`.

## Items

**1. What is installed.**
- **Decision.**
  - **One release, one platform.** An installation installs one admitted catalog release (`opensip-catalog.1` `releases[]`, SL:36-38) for exactly one platform: the host's own S8 platform (SL:700-711). Nothing else is installed: no other platform, no dependency resolution, no second release.
  - **The tree.** What is installed is the selected manifest platform's TreeCommitment (`platforms[].tree.entries`, CMS `manifestSchema`; admitted by CM:334-382): every `type=file` row with its exact bytes, and every `type=dir` and `type=symlink` row exactly as stated. Symlink targets stay inside the tree (RJ-3; CM's `resolve`, :313-332), and a symlink is never followed when the tree is read for identity (SL:45-47).
  - **Modes.** Each row's TreeCommitment `mode` (CM `mode`, :122-124: four octal digits, 0000-0777) is recorded exactly. It is applied to the installed entry with every write bit cleared (`mode & 0o555`), because a published generation is immutable (item 5). Modes are not identity members (SL:47-48).
- **Rationale.** The identity projection SL:41-48 needs only the regular files, but D4's launch runs a component from its tree, so the dir and symlink rows must exist as stated. Clearing write bits keeps the recorded mode exact while making the installed bytes read-only.
- **Rejected:** installing all of a release's platforms; following a symlink during installation or identity reading; applying write bits.

**2. The source of the bytes, and what each digest hashes.**
- **Decision.**
  - **The artifact.** The installer's only source of tree bytes is the catalog release's artifact row for the host's platform: `artifacts[{platform, archiveProfileId, archiveDigest, sha256}]`, which RC admits (:67-80) and whose catalog is signed TR-INDEX (SL:36-38).
  - **The archive profile.** `archiveProfileId` must equal `opensip-archive-profile.1` (item 3). Any other value refuses: no other profile is defined.
  - **What `archiveDigest` hashes.** It is the raw SHA-256 of the exact archive bytes the profile's byte algorithm produces (PKG `outputContract` OC-2: "archiveDigest = sha256 of those exact archive bytes"; PKG-AP `treeRelation`). This is sourced.
  - **What `sha256` hashes (a lead decision, LD-CI-1).** No source defines the catalog row's separate `sha256` member: SL:38 and the security completion's catalog section (`coop/completion/security-completion.v2.md`:303-304) name it without semantics. Profile 1 is uncompressed, and its artifact file **is** the archive (PKG-AP `compression`: "none"). So under profile 1 the artifact's bytes and the archive's bytes are the same octets, and `sha256` is the raw SHA-256 of the artifact file as delivered. **A profile-1 row whose `sha256` differs from its `archiveDigest` is self-contradictory and refuses** (`artifact-digest-split`). A later profile with a compressed or wrapped artifact would give `sha256` a different subject; this law defines none.
  - **The platform token (LD-CI-2).** RC admits four artifact `platform` tokens: `macos-arm64`, `macos-x86_64`, `linux-arm64`, `linux-x86_64` (:75-77; `security-schemas.v8/catalog.schema.json`). These are S8's **Display alias** spellings, not its machine Platform ids (SL:704-709). The installer maps the host's machine Platform id to the artifact token through S8's closed four-row table, used only as a lookup and never as an admitted platform id. A host whose platform has no row refuses (`platform-unsupported`). See Q2.
- **Trust.** The catalog release, manifest body, envelope and preimage are verified by the trust owner's ordinary reader at the host's trust instant (SL S1, :21-28; `trust_ordinary_metadata.rs`:90-160). This law adds no signature check and re-verifies nothing the reader verified. It consumes the reader's evidence through a narrow interface, and selects the platform's TreeCommitment from the validated manifest (CM).
- **Rejected:** a digest asserted by the operator; installing from an unsigned or unverified catalog; treating `sha256` as a hash of the tree or of the manifest.

**3. The archive profile: exactly one, closed.**
- **Decision.** The one profile is **`opensip-archive-profile.1`, adopted exactly as PKG-AP defines it**: uncompressed POSIX ustar headers with the stated field rules, members sorted by NFC code point, `mtime`/`uid`/`gid` 0, empty `uname`/`gname`/`prefix`, the three permitted typeflags (`0x30` file, `0x35` dir, `0x32` symlink), a checksum under the all-spaces mask, exactly two zero blocks, and nothing after them. Adoption is by reference to PKG at its pinned SHA-256, and covers PKG-AP **only**: this law does not apply PKG's other members, and does not close DR-120.
- **Admission is PKG-AP's `admissionChecks`, run as hostile-input parsing.**
  - Every header is recomputed from the TreeCommitment row and compared octet for octet.
  - The member set is in bijection with the TreeCommitment entries (`bijection`): an extra member, a missing member, a type or mode disagreement, a body length or digest disagreement, a non-NUL pad, or any byte after the trailer refuses.
  - The archive's length must equal PKG-AP's `archiveLength` formula over the TreeCommitment (`512·N + Σ512·⌈len/512⌉ + 1024`). The installer computes it **before reading** and reads at most that many bytes plus one, to detect excess, so the read is bounded by signed data.
  - Nothing in the archive is executed, interpreted or decompressed. No member name is used as a path until it has matched its TreeCommitment row exactly.
- **Its limits, and where each comes from:**

  | Limit | Value | Source |
  |---|---|---|
  | Entries per tree | 1 to 100,000 | **sourced**: the admitted manifest shape, `component_manifest_shape.rs`:231-234 |
  | Path length | ≤ 1,024 bytes, NFC, relative, no `.`/`..`/empty segments | **sourced**: CM `path_ok`, :153-176 |
  | Path in a header | ≤ 100 UTF-8 bytes, else `PATH-EXCEEDS-USTAR-NAME` | **sourced**: PKG-AP `pathBytes` |
  | Symlink target | ≤ 100 UTF-8 bytes, else `LINKTARGET-EXCEEDS-USTAR-LINKNAME` | **sourced**: PKG-AP `linkTargetBytes` |
  | File length | ≤ 8,589,934,591 bytes, else `SIZE-EXCEEDS-USTAR-FIELD` | **sourced**: PKG-AP `numericCapacity.size` |
  | Mode | ≤ 2,097,151 (CM bounds it to 0777) | **sourced**: PKG-AP `numericCapacity.mode`; CM `mode` |
  | Archive length | exactly PKG-AP's `archiveLength` over the tree | **sourced**: PKG-AP `archiveLength` |

  **This law defines no new numeric constant.** The total size is bounded by signed data (entries × file length), not by a law cap. Exhausting the disk is an I/O failure (item 8). Q1 asks whether a law-defined total cap is wanted.
- **Capacity mismatch (LD-CI-3).** CM admits paths up to 1,024 bytes, but profile 1 carries only 100. A release whose tree has a longer path or target is admissible metadata that **profile 1 cannot deliver**. Its installation refuses (`archive-capacity`) before any byte is read, and no other profile is invented to carry it.
- **Implementation without a new dependency.** The profile is fixed-layout ustar, which the product parses with its own code and the identity crate's SHA-256. No third-party archive crate is added, so the package policy is unchanged.
- **Rejected:** zip, gzip or xz; PAX or GNU long names; an archive library that accepts the ustar family loosely; extracting first and comparing afterwards.

**4. The offline handoff, and the installer transaction.**
- **The handoff (LD-CI-4).** The archive reaches the installer as **a local regular file the operator supplies**. The host opens it itself, with a no-follow regular-file open, and reads it once, streaming, under item 3's bound. Its `(device, inode, size, mtime, ctime)` are sampled before and after the read, and any change refuses (`archive-changed`), as the snapshot's capture reads do. **There is no network acquisition.** The installer opens no socket and fetches no URL: network acquisition is excluded (the memo's exclusions). How the operator names the file belongs to the command's owner (J1, WS command inventory :1101); see Q3.
- **When, and under which trust.** An installation runs under the lifecycle fence alone, as SL S7 places `install` (SL:658-670, the "none (fence only)" lease row). The fence is a bounded wait of 5 s, then `PROJECT.BUSY` (SL:588). The trust instant is the host's, read once at the start (SL S1). The release must be admitted and unrevoked at that instant.
- **The transaction:**
  1. **Admit.** The release, manifest, envelope and platform TreeCommitment come from the ordinary reader (item 2). The archive length is computed, and capacity is checked (item 3).
  2. **Stage.** A fresh staging directory is created under the component store (item 5), `0700`, private, and verified with security's `admit_custody_directory` rules (`crates/security/src/snapshot_source.rs`:444). Each archive member is verified (item 3) and written as its TreeCommitment row: files by create-exclusive no-follow writes, then the write bits cleared; dirs created; symlinks created with their exact stated target. The generation record (item 5) is written last.
  3. **Verify.** The archive digest is compared with `archiveDigest` and `sha256` (item 2). Every staged file's length and SHA-256 are compared with its row, by reading the staged file through the item 6 reader.
  4. **Publish.** The staging directory is renamed into place under the generation's name with an exclusive rename, which never replaces an entry. The name becomes visible only by that rename.
- **Nothing installed on failure (LD-CI-5).** A failure at any step before publish leaves:
  - **no new generation.** The staging directory is never visible under a generation name, and is removed best-effort. A staging directory that survives a crash is never read as a generation: generations are named only by item 5's grammar, and staging names never match it;
  - **every existing published generation untouched.** The installer never writes, renames or removes a published generation, including one of the same component at another version;
  - **no partial staging that counts as installed.** A crash between publish and the end of the step is safe: what is published is complete, because it was verified before the rename.
- **Re-installing a release whose generation is already published** is a no-op. The installer reports it as installed, and neither stages anything nor replaces the generation (LD-CI-6).
- **Rejected:** installing in place; publishing by moving files one at a time; letting a repair or re-read heal a failed install; trusting a staging directory left by an earlier run.

**5. The component store and its custody.**
- **Location (LD-CI-7).** `<installRoot>/components/`, created by installation provisioning as a private `0700` directory. No layout owner defines a component store yet; the lifecycle locations owner (`crates/lifecycle/src/locations.rs`) gains it. Inside it:
  - `<closure2-hex>/` is one published generation per `closure2`, named by the 64 lowercase hex digits of the closure's identity hash (C2a-1's candidate). It contains `tree/` (item 1's entries) and `generation.json` (below);
  - `.staging/<random>/` holds staging directories, never read as generations.
- **Custody.** The store, each generation and each staging directory are private to the installation user and must pass `admit_custody_directory`'s ACL rule: no other principal is granted any right. All reads are no-follow and descriptor-relative from the retained store directory. **The installer transaction is the only writer**, and it writes only staging directories.
- **Immutability.** A published generation is never modified: its files' write bits are cleared, and no code path opens a generation file for writing. The generation's `closure2` names exactly one tree.
- **The generation record** (`generation.json`, canonical JSON, written inside staging before publish) is closed:
  - `{closureId, componentManifestDigest, catalogRelease: {stableId, version, manifestDigest, envelopeDigest}, platform, archiveProfileId, archiveDigest, entries}`;
  - `entries` is the TreeCommitment's file rows as `{path, sha256, bytes}` (the identity Blobs, SL:41-44), plus dir and symlink rows as stated.
  - It is an origin record, not an identity input: it adds no identity member, and `closure2` is computed by C2a-1, never read from it.
- **Retention by raw SHA-256 and `BLOB_LENGTH`.** The retained file for a Blob is the one at its `tree/` path. C2a-3 verifies its bytes against the Blob's `sha256` and `bytes` on every read (item 6). It never accepts a path's existence, a cached digest or `generation.json`'s claim as proof.
- **A later observed change refuses and is never repaired (LD-CI-8).** If a read finds a file missing, a different length, a different digest, a non-regular entry, or an extra or missing directory entry, the read refuses with that cause. The store is never rewritten, re-extracted or re-downloaded to heal it. Only an explicit operator action can replace the bytes, by uninstalling and re-installing, and nothing infers one.
- **Rejected:** a content-addressed blob store beside a materialized tree, because it would double the bytes and give two sources of truth; mutable generations; a shared system location.

**6. The retained-tree read interface (what C2a-3 binds).**
- **Decision.** One function in the lifecycle crate, beside `installation.rs`, which the inventory plans: `catalog.rs`/`installation.rs`, crate `opensip-lifecycle`.

  `retained_tree(store: &ComponentStore, closure: &ClosureCandidate, work: &mut WorkScope) -> Result<RetainedTree, TreeReadFailure>`
  - `ComponentStore` is the retained, custody-admitted store directory (item 5). It is obtained only from the installation's provisioning, or from the fixture constructor below.
  - `ClosureCandidate` is C2a-1's unadmitted candidate: `closure2` and its identity Blob list.
  - It opens `<closure2-hex>/tree/` no-follow. For each Blob in the candidate's order it opens the path no-follow, descriptor-relative, segment by segment; it requires a regular file, and streams its bytes into a SHA-256 with a charged read buffer. It returns `RetainedTree`, an opaque proof listing each Blob as verified, which only this function constructs.
  - **Typed failures:**
    - `NotInstalled`: there is no generation for this `closure2`;
    - `Missing{path}`: the generation exists but the file does not;
    - `Length{path, expected, observed}`;
    - `Digest{path}`;
    - `NotRegular{path}`;
    - `Custody(..)`: the store or generation fails custody;
    - `Budget`: the caller's work is exhausted;
    - `Io{call, errno}`.
  - **Bounds and charging.** Every open, status read, read call and buffer is charged to the caller's `WorkScope` before it is made, at published costs, as the snapshot's capture reads are. The total read is bounded by the candidate's Blob lengths, which are signed. **The work profile the caller passes is the caller's choice.** Which production profile R10a uses is D4's and J1's to select (`codex-c2a-plan-r2`, Q5); this law fixes only the interface and its charges.
- **The fixture path.** `ComponentStore::fixture(dir)` exists only under the joint fixture predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (MC item 8; X8 item 4b). It admits a test-owned private directory as a store. Synthetic generations are produced **by the same installer** from a synthetic-signed catalog and a profile-1 archive that C2a-2's generator writes, so the fixture path runs the same verifier and the same installer (`codex-c2a-plan-r1`, RF-2). There is no constructor of `RetainedTree` outside `retained_tree`.
- **Rejected:** returning paths for the caller to open; verifying once at installation and trusting it afterwards; a fixture store that skips the installer.

**7. The lifecycle minimum.**
- **Installation** is item 4's transaction, durable path only.
- **Use at R10a.** C2a's admission reads through item 6 at its R10a/ER10a step, before the draw (`codex-c2a-plan-r2`, RF-3), **under current trust**. A release revoked at that instant is never admitted or executed, whatever bytes are present (WS:293-299, "a revoked closure is never executed, whatever bytes are present").
- **Pinning across an operation and Run retention (LD-CI-9).**
  - **During an operation.** Removal is a GC census only, and never removes a generation a live operation pins (SL:658-661). An operation pins every generation it read through item 6 from that read until its lease ends.
  - **After it.** A retained Run does not rely on the component store for its evidence: its replay closure is the Run's own retention under IE §5 and IE:1399-1411. **This law adds no Run-retention pin.** The store is an origin of bytes, not a retention record (memo item 4). GC removal of an installed generation that a retained Run names is a removal of an origin. That Run's replay then resolves its closure through WS:293's other origins, or reports it unavailable (`pivot-detector-unavailable`, WS:295), never a silent substitute. See Q4.
  - **Immutability lifetime.** A generation is immutable from publish until its removal by GC. Nothing modifies it in between.
- **Removal** beyond GC's census, and updates and migration (DR-110, DR-112), are excluded (the memo's exclusions).
- **Durable versus ephemeral.**
  - The **durable** path installs, reads and pins.
  - The **ephemeral** path never writes the store and never installs. It may read a published generation through item 6, when its own admission has an admitted trust view (MC item 7).
  - With **no admitted trust view**, the ephemeral path admits nothing, so it reads nothing (MC:431-437).

**8. Refusals and routes — onto existing codes only.**
- **The installation command:**

  | Refusal | Class / exit | Code | Detail |
  |---|---|---|---|
  | Release not admitted, revoked or unverified; platform unsupported; profile not 1; `artifact-digest-split`; `archive-capacity`; any profile admission check fails (item 3); `archive-changed` | request-rejected 2 | `EXTENSION.ADMISSION_REJECTED` | none, except an existing `NT-TCB-*` platform-decision detail where the platform owner supplies one (the precedent is `crates/host/src/installation_termination.rs`:280-340) |
  | An I/O failure while staging, verifying or publishing (ENOSPC included) | operational-failed 4 | `EXTENSION.INSTALL_IO_FAILED`, fault cause `extension-install-io` | none |
  | Fence busy after 5 s | as SL:588 | `PROJECT.BUSY` | none |

  The internal subjects named above (`artifact-digest-split`, `archive-capacity`, `archive-changed`, `platform-unsupported`, and the profile's own `PATH-EXCEEDS-USTAR-NAME` and the rest) are typed internal refusals for diagnostics. **None is a new public code** (Q5).
- **Retained reads at R10a** (item 6), routed by WS:1374-1375:

  | Read result | Durable | Ephemeral |
  |---|---|---|
  | `NotInstalled` for a required closure | indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`, detail `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` (WS:1374) | indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`, **no detail** (MC item 7 lead ruling; RTC §7.4) |
  | `Missing` in a published generation | operational-failed 4, `HOST.IO_FAILURE`, detail `DELIVERY.CLOSURE_BYTES_MISSING` (registered, `public-detail-registry.v1.json`:306) | operational-failed 4, `HOST.IO_FAILURE`, no detail |
  | `Length`, `Digest`, `NotRegular`, or `Custody` of a generation | operational-failed 4, `HOST.IO_FAILURE`, detail `DELIVERY.CLOSURE_BYTES_CORRUPT` (WS:1375) | the same, no detail |
  | `Io` | operational-failed 4, `HOST.IO_FAILURE` | the same |
  | `Budget` | the caller's existing budget route (`WORK.BUDGET_EXHAUSTED`) | the same |

  A corrupted promised tree keeps its own cause and never becomes "not installed" (`codex-c2a-plan-r1`, Q3 ruling; C2a plan r2 LD-C2A-5).

**9. Units and controls.**
- **Units:**
  - **CI-1, the profile-1 codec** (security, pure, hostile-input). It implements admission per item 3, and the PKG-AP byte algorithm emitter for fixtures only. It has PKG-AP's golden and negative cases.
  - **CI-2, the component store and the installer transaction** (`crates/lifecycle/src/installation.rs`, a planned row; store location in `locations.rs`). It covers items 4 and 5.
  - **CI-3, the retained-tree reader** (lifecycle). It covers item 6, with the fixture constructor. **C2a-3 binds CI-3**, and C2a-4's wiring waits for it (`codex-c2a-plan-r2`, Q6).
  - **CI-4, the command surface:** J1 exposes `install` with item 4's handoff, under WS's command inventory, after Q3.
- **Order:** CI-1, then CI-2 and CI-3, with C2a-2's generator emitting profile-1 archives; then C2a-3; CI-4 with J1.
- **Controls:**
  - **CI-T1 (the profile):** PKG-AP's 17 golden and negative cases (`goldenAndNegativeCases`), each as the codec's admission outcome. These include AT-ARCHIVE-IDENTITY's two-emitter byte identity, the 100- and 101-byte name and link, the size and mode field maxima, NUL typeflag, the NUL-in-mask checksum, a non-zero uid, extra and missing members, and body and target mismatches.
  - **CI-T2:** an archive whose length differs from the formula refuses before any member is written. The installer reads at most the expected length plus one byte.
  - **CI-T3:** `archiveDigest` mismatch refuses; `sha256` ≠ `archiveDigest` refuses (`artifact-digest-split`); `archiveProfileId` other than profile 1 refuses.
  - **CI-T4:** a host platform with no S8 row refuses; the catalog token is mapped through S8's table, and an alias is never admitted as a platform id.
  - **CI-T5:** a tree with a 101-byte path is refused `archive-capacity` before any read.
  - **CI-T6:** the archive file changed during the read refuses `archive-changed`.
  - **CI-T7 (nothing installed):** failures injected at each stage step, and a crash between staging and publish, leave no new generation. Every other generation's bytes and metadata are unchanged, and a surviving staging directory is never read as a generation.
  - **CI-T8:** re-installing the same release is a no-op that replaces nothing.
  - **CI-T9 (immutability):** a published file's write bits are clear. A file modified, truncated, removed or replaced by a symlink after publish refuses with `Digest`, `Length`, `Missing` or `NotRegular`, and nothing rewrites it.
  - **CI-T10 (the reader):** `NotInstalled` versus `Missing`; every typed failure; exact charges against a recorded call log; `Budget` exhaustion.
  - **CI-T11 (the fixture):** a synthetic-signed release installed by the same installer into a fixture store reads back through the same reader. A synthetic `ComponentStore` cannot be constructed in a release build (a source pin, as MC item 8's C2-T7).
  - **CI-T12 (revocation):** a release revoked after installation is never admitted, though its generation's bytes verify.
  - **CI-T13 (no network, no execution):** source pins showing the installer and codec name no socket or URL API and spawn no process.
  - **CI-T14 (custody):** a store or generation with a foreign ACL entry refuses `Custody`.
  - **CI-T15 (ephemeral):** the ephemeral path writes nothing to the store.
  - **CI-T16 (routes):** each item 8 row's class, code and detail, on both paths.

## Open questions

- **Q1.** Is a law-defined cap on a tree's total bytes wanted, beyond the signed per-file and entry bounds and disk exhaustion as an I/O failure? I recommend none at M3.
- **Q2.** The catalog's artifact `platform` tokens are S8's display aliases (RC :75-77). Is LD-CI-2's lookup through S8's table compatible with S8's MUST-2 one-vocabulary rule, or does the catalog schema need a successor to carry machine ids?
- **Q3.** How the operator names the archive file (an argument of `install`, or a release-bundle directory) is J1's. Should this law fix the library input as "an operator-supplied regular file", as item 4 does, and leave the spelling to J1?
- **Q4.** Should a retained Run pin the installed generations it used (LD-CI-9 says no), or is the store an origin only, with replay resolving through WS:293's origins?
- **Q5.** Do the install-time refusals need a public detail beyond `EXTENSION.ADMISSION_REJECTED`'s, or are internal subjects enough at M3?
- **Q6.** Does adopting PKG-AP alone by pinned reference, without applying the rest of PKG or closing DR-120, satisfy the archive-profile ownership PKG-AP claims ("THIS ARTIFACT OWNS archive determinism")?
- **Q7.** Is clearing write bits (item 1) the right reconciliation of "modes applied from the TreeCommitment" with immutability?

## Excluded

- multi-platform installation;
- updates and migration (DR-110, DR-112);
- removal policy beyond GC's census and live-operation pinning;
- network acquisition;
- any profile other than profile 1;
- any change to item 7, C2PM-1, CR-1 or the trust owner.

## Not claimed

No code, no plan for C2a-3's binding beyond item 6's interface, no binding, and no qualification. No public code is added, and no accepted law text is changed.
