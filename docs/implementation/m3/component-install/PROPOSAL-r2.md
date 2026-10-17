# Component release installation and tree custody — proposal CI r2

**Lead law proposal r2, 2026-10-17. Proposed; it needs Codex review. Not code.** Round 2 answers `codex-component-install-r1` (REQUIRED-FINDINGS: CI-R1-RF-1 to RF-6 and NBO-1, with rulings Q1 to Q7). r1 (`PROPOSAL-r1.md`) is history.

The lead owns this law as DR-103's delivery owner (`codex-component-install-r1`: "The lead may propose this missing delivery law"). It answers cross-law item X-C2A-1 (`snapshot-plan-c/c2a/X-C2A-1-r1.md`, the input memo, which is not law). **Nothing in it is pre-approved:** each choice is proposed with its rationale.

## r2 changes

| Finding | Change | Where |
| --- | --- | --- |
| **RF-1** (the whole committed tree) | The read capability carries the **authenticated selected-platform TreeCommitment**, not just the identity Blobs. It enumerates the installed tree completely, bounded and no-follow, and checks every entry: exact path set, type, symlink text, installed-mode policy, and file length and digest. Extras and missing entries refuse. `generation.json` is never authority. The manifest, candidate and generation-record association is checked explicitly. New typed failures: `Extra`, `Absent`, `Type`, `Mode`, `LinkTarget`, `Association`. | items 5, 6; CI-T9, CI-T10, CI-T17 |
| **RF-2** (usable modes) | An explicit **installed-mode policy by entry type**, separate from the authenticated archive mode (LD-CI-10). Files are `0400`, or `0500` exactly when the authenticated mode has an execute bit. Directories in the tree are `0500`; the store and generation directories are `0700`. Symlinks get no mode operation. Staging uses `0700` directories and `0600` files, and finalization runs **bottom-up after verification**. No execution is granted that the authenticated mode lacks, and no admitted mode is unmaterializable. | items 1, 4, 5; CI-T18 |
| **RF-3** (durable publication) | A **durable sequence** on the platform's own primitives: a file barrier per payload and for the record, then directory barriers bottom-up, then law 467's exclusive publication, then the parent's barrier. Outcomes for every failure point follow law 467 item 7's route classes. Restart recovery is defined: no automatic replacement or retry, surviving stages are inert, and an uncertain publication is resolved only by the full read verification. Crash-prefix controls run through the post-rename barrier. | item 4; CI-T7, CI-T19 |
| **RF-4** (byte transfer and pins) | **A pin is a shared `flock` on the generation's `pin.lock`**, acquired under the fence at R10a's read and held to operation end. GC needs the exclusive lock, so busy means retain. The `RetainedTree` capability is **pinned** and offers a **bounded verified-byte transfer** (`transfer`) into the owning retention path's sink. A Run releases the origin only after its own retention holds every preimage. Replay uses the Run's own retained preimages, with its evidence-missing and corrupt semantics; WS pivot resolution is a separate operation. | items 6, 7; CI-T20, CI-T21 |
| **RF-5** (the not-installed gates) | `NotInstalled` is a **typed input** to the availability, selection and composition owners (C2a, C4a, J2). The durable detail is qualified by RTC's committed-Run authority. **X-8 is carried as a gate** before required-cell end-to-end composition. No placeholder closure or context is minted, no cell is dropped, and no ephemeral detail is added. | item 8 |
| **RF-6** (installer work) | Installer work is accounted (LD-CI-11). Every read and write attempt, allocation, creation, mode change, barrier, rename and cleanup step is priced, and charged before it runs. The read discipline is the snapshot session's: 64 KiB chunks, the read-attempt envelope, and one write attempt never retried. **The exact cost of a release is computed from its signed tree before any acquisition**, and refused before any acquisition (`install-budget`, `EXTENSION.ADMISSION_REJECTED`) if it exceeds the installation ledger. The ledger is `WorkLedger::snapshot_profile()`, an interim reuse of a sourced bound, with cross-law item X-CI-1. Exhaustion during installation publishes nothing and takes law 468's existing budget route (`installation_termination.rs`:389-396). | items 3, 4; CI-T22 |
| **NBO-1** | CI-T1 uses PKG-AP's exact 15 cases. Codec and metadata-capacity controls are labelled separately from feasible signed-installation controls. An existing-generation no-op now runs the full read verification before reporting installed (LD-CI-6). | item 4; item 9 |
| **Q rulings** | Q1: no total-byte constant, with RF-6's accounting. Q2: the lookup is accepted, and the alias never becomes an admitted id. Q3: accepted. Q4: no Run pin once its own retention holds, as in RF-4. Q5: no new public code. Q6: accepted as an explicit new selection; DR-120's standing is unchanged. Q7: replaced by LD-CI-10. | throughout |

## Short names

- **SL / WS / IE / NE / RTC**: `docs/v2/contracts/product-v1/{security-and-lifecycle,workflows-and-surfaces,identity-and-evidence,native-evidence}.md` and the run-termination contract §7.4–7.5.
- **PKG**: `docs/coop/artifacts/component-packaging-contract.v14.json` (SHA-256 `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c`), standing CANDIDATE-NOT-APPLIED, register row DR-120. **PKG-AP** is its `archiveProfile` member (`opensip-archive-profile.1`, from line 1612).
- **CMS**: `docs/coop/artifacts/component-manifest-schemas.v11.json` (SHA-256 `1c0b8868…a017a005`).
- **MC**: M3-C r8 (`snapshot-plan-c/PROPOSAL.md`).
- **CM**: `crates/security/src/component_manifest.rs` and `generated/component_manifest_shape.rs`.
- **RC**: `crates/security/src/trust/recovery_catalog.rs`.
- **FS**: the platform filesystem primitives:
  - `crates/platform/src/filesystem.rs`;
  - `filesystem/directory_publication.rs`, private staging and exclusive publication under law 467 item 7;
  - `filesystem/file_effects.rs`;
  - `filesystem/directory_effects.rs`.
- **SNAP**: the snapshot session's read discipline, `crates/host/src/snapshot.rs`:33-70: the 64 KiB `READ_CHUNK`, one charged edge per read attempt, and the envelope `2·⌈size/64 KiB⌉ + 2` (C1a plan r3).

## Items

**1. What is installed.**
- **One release, one platform.** An installation installs one admitted catalog release (`opensip-catalog.1` `releases[]`, SL:36-38) for exactly one platform: the host's own S8 platform (SL:700-711). Nothing else is installed: no other platform, no dependency resolution, no second release.
- **The tree.** What is installed is the selected manifest platform's TreeCommitment (`platforms[].tree.entries`, CMS; admitted by CM:334-382):
  - every `type=file` row, with its exact bytes;
  - every `type=dir` row, as a directory;
  - every `type=symlink` row, with its exact target text. Targets stay inside the tree (RJ-3; CM `resolve`, :313-332), and no symlink is followed when the tree is read (SL:45-47).
- **Modes (LD-CI-10, r2).** The authenticated `mode` (CM `mode`, :122-124: four octal digits, `0000`–`0777`) is retained exactly in the generation record and verified against the archive header (item 3). It is **not** copied onto the filesystem. The installed mode is a function of entry type and the authenticated mode:
  - **file:** `0500` if the authenticated mode has any execute bit (`mode & 0o111 ≠ 0`), else `0400`;
  - **dir** (inside `tree/`): `0500`;
  - **symlink:** no mode operation (`lchmod` is not portable across S8's four platforms, and a symlink's mode is not used for access on them). Its target text is the only checked attribute.
  - **Rationale.** Owner read and traverse are always required for installer verification, D4's launch and the retained reader. Group and other get nothing, matching the private store (item 5). No write bit is set, because a published generation is immutable. Execute appears only where the signed mode grants it, so nothing is silently made executable. Every admitted mode maps to a usable installed mode, so no mode is unmaterializable and no new refusal is needed. The authenticated mode stays exact and checked (Q7 ruling).
- **Rejected:** copying authenticated modes, which could leave the tree unreadable or untraversable (r1's RF-2 cases, `0200` and `0600` dirs); granting execute where the signed mode has none; applying modes to symlinks.

**2. The source of the bytes, and what each digest hashes.**
- **The artifact.** The installer's only source of tree bytes is the catalog release's artifact row for the host's platform: `artifacts[{platform, archiveProfileId, archiveDigest, sha256}]`, which RC admits (:67-80), signed TR-INDEX (SL:36-38).
- **The archive profile.** `archiveProfileId` must equal `opensip-archive-profile.1` (item 3); any other value refuses.
- **What `archiveDigest` hashes.** The raw SHA-256 of the exact archive bytes the profile produces. This is sourced: PKG `outputContract` OC-2 and PKG-AP `treeRelation`.
- **What `sha256` hashes (LD-CI-1, kept; accepted in review).** Under profile 1 the artifact file is the uncompressed archive (PKG-AP `compression`: "none"), so `sha256` is the raw SHA-256 of the same octets. A row whose two digests differ refuses (`artifact-digest-split`). This is this law's rule for profile 1 only: it reinterprets no other profile.
- **The platform token (LD-CI-2, kept; Q2 accepted).** The host's S8 machine Platform id is mapped to RC's artifact token (`macos-arm64`, `macos-x86_64`, `linux-arm64`, `linux-x86_64`; :75-77) through S8's closed four-row table, used only to select the artifact. The alias never becomes an admitted platform, profile or grant id, and this law authorizes aliases nowhere else.
- **Trust.** The catalog release, manifest body, envelope and preimage are verified by the trust owner's ordinary reader at the host's trust instant (SL S1; `trust_ordinary_metadata.rs`:90-160). This law re-verifies nothing the reader verified. It consumes the reader's evidence, including the validated manifest's selected-platform TreeCommitment and the retained manifest body.
- **Crate edges.** The reader's evidence and C2a-1's `ClosureCandidate` belong to security, and the installer to lifecycle. The O1-a package policy lists `opensip-security` among `opensip-lifecycle`'s permitted dependencies. lifecycle's manifest currently depends only on platform and identity, so CI-2's plan adds that edge and names the bridge API. This law asserts no existing lifecycle–security API.

**3. The archive profile: exactly one, closed.**
- **The one profile** is `opensip-archive-profile.1`, adopted exactly as PKG-AP defines it, by reference to PKG at its pinned SHA-256. This is an explicit new selection here (Q6 ruling). It is not evidence that PKG or DR-120 was applied: PKG's other members, release and adapter qualification, and DR-120's standing are unchanged.
- **Admission is PKG-AP's `admissionChecks`**, run as hostile-input parsing:
  - every header is recomputed from the TreeCommitment row and compared octet for octet;
  - the members are in bijection with the entries (PKG-AP `bijection`), and every type, mode, length, digest, pad and the trailer must be exact;
  - the archive length must equal PKG-AP's `archiveLength` over the tree, computed **before reading**. At most that many bytes plus one are read.
  Nothing is executed, interpreted or decompressed, and no member name is used as a path until it has matched its row.
- **Signed capacities**, all sourced. These are distinct from work limits (item 4) and from disk exhaustion:

  | Capacity | Value | Source |
  |---|---|---|
  | Entries per tree | 1–100,000 | the admitted manifest shape, `component_manifest_shape.rs`:231-234 |
  | Path | ≤ 1,024 bytes, NFC, relative, no `.`/`..`/empty segments | CM `path_ok`, :153-176 |
  | Path in a header | ≤ 100 UTF-8 bytes, else `PATH-EXCEEDS-USTAR-NAME` | PKG-AP `pathBytes` |
  | Symlink target | ≤ 100 UTF-8 bytes, else `LINKTARGET-EXCEEDS-USTAR-LINKNAME` | PKG-AP `linkTargetBytes` |
  | File length | ≤ 8,589,934,591, else `SIZE-EXCEEDS-USTAR-FIELD` | PKG-AP `numericCapacity.size` |
  | Mode field | ≤ 2,097,151 (a codec limit only; CM admits ≤ `0777`) | PKG-AP `numericCapacity.mode`; CM `mode` |
  | Archive length | exactly PKG-AP's `archiveLength` | PKG-AP |

- **Capacity mismatch (LD-CI-3, kept).** A release whose tree has a path or target longer than 100 bytes is admissible metadata that profile 1 cannot deliver. It refuses (`archive-capacity`) before any read.
- **No new third-party dependency.** The profile is fixed-layout ustar, parsed with the product's own code and the identity crate's SHA-256.

**4. The installer: handoff, work, transaction, durability and recovery.**
- **The handoff (LD-CI-4; Q3 accepted).** The archive reaches the library as **an operator-supplied local regular file**.
  - The host opens it itself, with a no-follow regular-file open, and reads it once, streaming.
  - Its `(device, inode, size, mtime, ctime)` are sampled before and after the read; any change refuses (`archive-changed`).
  - There is no network acquisition and no URL. The CLI spelling is J1's (WS command inventory :1101).
- **When, and under which trust.**
  - An installation runs under the lifecycle fence alone (SL:658-670): a bounded wait of 5 s, then `PROJECT.BUSY` (SL:588).
  - The trust instant is read once at the start (SL S1), and the release must be admitted and unrevoked then.
  - The fence is held through the end of step 6 below.
- **Work (LD-CI-11, r2).** The installer runs on a ledger the caller supplies. **Before any acquisition** it computes the installation's exact cost from the signed tree, and refuses if that cost exceeds the ledger (`install-budget`, item 8). A signed release too costly for the ledger is deterministic from signed data, so it is an admission refusal like `archive-capacity`. It then charges every operation **before** making it, at published costs. Each of these is priced:
  - **reading the archive:** one 64 KiB buffer, charged once (SNAP's buffer rule), and one charged edge per read attempt. A read that does not complete within the archive's envelope, `2·⌈archiveLength/64 KiB⌉ + 2` (SNAP:66-70), refuses (`archive-read-attempts`);
  - **headers:** one 512-byte header per member, processed in the read buffer with no allocation;
  - **staged files:** each exclusive create (FS `create_exclusive_regular_cost`), each positioned write attempt (one per chunk, **never retried**; the C1a2 candidate-custody rule), each mode change and each file barrier;
  - **directories and links:** each directory creation, mode change and directory barrier (FS `directory_barrier_cost`), and each symlink creation, with its target text copied as an owned record;
  - **the generation record:** its canonical length, as an owned record;
  - **publication:** the private stage (FS `private_directory_stage_cost`), the exclusive publication (FS `exclusive_publication_cost`) and the parent barrier;
  - **verification:** item 6's read costs;
  - **failed-stage cleanup:** each unlink and rmdir, best-effort and charged. A shortfall during cleanup stops cleanup, and leaves an inert stage (below).

  **The ledger.** `WorkLedger::snapshot_profile()` (2^21 objects, 2^24 edges, 2^33 bytes; `crates/platform/src/work_ledger.rs`:28-30, :242; the r9 law record). It is reused as an existing sourced bound for one bounded tree operation, as D3a's LD-D3A-12 reused the discovery profile for scratch walks. This is an interim reuse, and **cross-law item X-CI-1** asks this law's owner for a sourced installation profile. It does not depend on R10a's reader profile, which is D4/J1's (`codex-c2a-plan-r2` Q5). A tree whose exact cost exceeds it refuses before any byte is read, and nothing is installed.

  Signed capacities, work and disk space are distinct. `ENOSPC` is an I/O failure (item 8), not a work limit (Q1 ruling).
- **The transaction:**
  1. **Admit.** The release, manifest, envelope and TreeCommitment come from the ordinary reader (item 2). The archive length is computed, and capacity (item 3) and cost (above) are checked.
  2. **Stage.** A private stage is created with FS `create_private_directory_stage_accounted` in `<store>/.staging/`, as a `0700` directory. Each member is verified (item 3), then created:
     - files with create-exclusive no-follow opens at `0600`, then written;
     - directories at `0700`;
     - symlinks with their exact target.
  3. **Verify.** The archive digest is compared with `archiveDigest` and `sha256` (item 2). Every staged entry is checked against the TreeCommitment through item 6's structural and byte verification, run over the stage.
  4. **Make durable.** Each file is file-barriered (FS `FileBarrierReceipt`), then its mode is set to its LD-CI-10 installed mode. `generation.json` is written, file-barriered and set to `0400`. The `pin.lock` file is created at `0600`. Then each directory inside `tree/`, deepest first, gets its directory barrier (FS `confirm_directory_barrier_accounted`) and is set to `0500`. The generation directory, which stays `0700`, gets its barrier last.
  5. **Publish.** The stage is published under `<closure2-hex>` with FS `publish_exclusive_accounted` (law 467's exclusive rename, which never replaces an entry).
  6. **Make the name durable.** The publication parent gets its barrier on `publication.parent_directory()` while the fence is held (FS `directory_publication.rs`:9-14).
- **Outcomes and recovery (LD-CI-5, r2).** Failures route by law 467 item 7's classes (FS `DirectoryRenameClass`):
  - **Before step 5:** nothing is published. The stage is removed best-effort under charge. Existing generations are never written, renamed or removed. Result: `EXTENSION.ADMISSION_REJECTED` or `EXTENSION.INSTALL_IO_FAILED` (item 8).
  - **Step 5 `LostRace`** (`EEXIST` with the stage unchanged): another entry holds the name, and this attempt published nothing. The stage is left in place, inert. The installer then runs the existing-generation path below; it never replaces the winner.
  - **Step 5 `NotPerformed`:** no rename happened. Treated as before step 5.
  - **Step 5 `Indeterminate`, or a step-6 barrier failure:** publication is uncertain. The act stops with `EXTENSION.INSTALL_IO_FAILED`. Nothing is retried, re-staged or replaced.
  - **Restart, or any later operation.** A generation name either exists or does not, and its existence is never proof of anything. Its contents were made durable at step 4, before its name could exist, so a crash leaves at most a complete tree under a possibly non-durable name. Every use passes item 6's full verification, which detects any incompleteness. An uncertain prior publication is therefore resolved only by verification: a verifying generation is usable; a non-verifying one refuses as corrupt (item 8); an absent one is not installed. No automatic re-install, repair or replacement happens on any path.
  - **Surviving stages** (after a crash or an incomplete cleanup) carry the FS stage prefix (`.opensip-stage-install-`) under `.staging/`. They are never read as generations, because generation names are exactly 64 lowercase hex digits and live only at the store's top level. Only GC's census removes them, under the fence; this law adds no other cleanup owner.
- **Re-install of a published release (LD-CI-6, r2).** If `<closure2-hex>` already exists, the installer runs item 6's full verification on it (custody, structure and every byte). If it verifies, the release is reported installed and nothing is staged. If it does not, the act refuses with the corrupt cause (item 8) and replaces nothing (LD-CI-8). Existence alone is never reported as a usable installation (NBO-1).

**5. The component store and its custody.**
- **Location (LD-CI-7, kept).** `<installRoot>/components/`, created by installation provisioning as a private `0700` directory. The lifecycle locations owner (`crates/lifecycle/src/locations.rs`) gains it. Inside:
  - `<closure2-hex>/` is one published generation, `0700`. It holds `tree/` (the committed entries, under LD-CI-10's installed modes), `generation.json` (`0400`) and `pin.lock` (`0600`);
  - `.staging/` holds FS stages, which are never generations.
- **Custody.** The store, the generation directories and the stages must pass `admit_custody_directory`'s rule (`crates/security/src/snapshot_source.rs`:444): a directory owned by the invoking user, `0700`, with no foreign ACL grant. All reads are no-follow and descriptor-relative from the retained store directory.
  - **Exactly what custody excludes:** this rule excludes other principals. It does not exclude the invoking user's own processes or root (snapshot_source.rs:440-442; review, "Authority, scope and sound portions"). Clearing write bits and private directories do not enforce exclusive installer access against those. So **every use re-verifies** (item 6), and the law relies on no claim of exclusivity.
  - The installer transaction is the only lawful writer, and it writes only stages.
- **Immutability.** A published generation is never modified by any lawful path from publish until its GC removal. Its files carry no write bit, and no code path opens one for writing.
- **The generation record** (`generation.json`, canonical JSON, closed): `{closureId, componentManifestDigest, catalogRelease: {stableId, version, manifestDigest, envelopeDigest}, platform, archiveProfileId, archiveDigest}`. It is an origin record:
  - it is **not authority** for the tree;
  - it adds no identity member;
  - `closure2` is C2a-1's;
  - item 6 checks it only for association: each member must equal the value derived from the authenticated evidence.
- **Refuse, never repair (LD-CI-8, kept).** A failed verification refuses with its cause. Nothing re-extracts, rewrites or re-reads the store to heal it. Only an explicit operator uninstall and re-install can replace the bytes.

**6. The retained-tree capability (what C2a-3 binds).**
- **Opening (r2).** One function in `opensip-lifecycle`, beside `installation.rs`:

  `open_retained_tree(store: &ComponentStore, evidence: &AdmittedRelease, candidate: &ClosureCandidate, pin: PinRequest, work: &mut WorkScope) -> Result<RetainedTree, TreeReadFailure>`
  - `AdmittedRelease` is the ordinary reader's evidence: the catalog release, the retained manifest body, and the selected-platform **TreeCommitment**. `ClosureCandidate` is C2a-1's unadmitted candidate (`closure2` and its Blobs).
  - **Association.** The function first checks that `closure2` matches the candidate and that the candidate's Blobs are exactly the TreeCommitment's file rows projected (SL:41-44). It then checks that `generation.json`'s every member equals the value derived from `evidence`. Any disagreement is `Association`.
  - **The pin.** It acquires a **shared `flock`** on `<closure2-hex>/pin.lock` (`PinRequest` says whether the caller holds the fence, item 7) before reading anything, and the lock stays with the returned capability.
  - **Structural verification.** Bounded no-follow enumeration of `tree/`. Every directory is listed in charged steps, with no listing collected whole; the total entries are bounded by the signed count. The checks:
    - the **exact path set** equals the TreeCommitment's: any extra entry is `Extra`, any missing one `Absent`;
    - each entry's **type** must match: `Type`;
    - each symlink's **target text** must match exactly, read with `readlinkat` and never followed: `LinkTarget`;
    - each file's and directory's **installed mode** must equal LD-CI-10's function of its authenticated mode: `Mode`;
    - each regular file's **length and SHA-256** must match its row, streamed with the charged 64 KiB buffer: `Length` or `Digest`;
    - the store's and generation's **custody**: `Custody`.
  - **The other typed failures:** `NotInstalled` (no `<closure2-hex>`), `Budget`, `Io{call, errno}`.
  - **The result.** `RetainedTree` is an opaque, **pinned** capability that only this function constructs. It holds the store's retained directory, the generation's retained directory, the TreeCommitment and the pin. It **never** stands for bytes present later on its own: a hash-only proof is not retained bytes (RF-4).
- **The bounded verified-byte transfer (r2).** `RetainedTree::transfer(&self, path, sink: &mut impl VerifiedSink, work) -> Result<(), TreeReadFailure>`:
  - it re-opens the file no-follow from the retained generation directory, re-checks type, mode and length, and streams the bytes in 64 KiB chunks to the sink while hashing;
  - the sink receives the expected `(sha256, length)` first, and is told only at the end whether the stream verified;
  - a sink commits nothing unless the final verification succeeds;
  - every chunk and attempt is charged; a changed file is `Length` or `Digest`, and nothing is repaired.
  - The owning retention path, which is the Run's custody under IE §5 and the native context's retained trees under NE:1493-1499, copies each Blob through `transfer`. It takes the manifest body and the closure descriptor from `AdmittedRelease` and C2a-1, never from the store. **That owner, not this law, decides what a Run retains**; this law supplies only the verified bytes.
- **The fixture path.** `ComponentStore::fixture(dir)` exists only under the joint fixture predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (MC item 8; X8 item 4b). Synthetic generations are produced **by the same installer**, from C2a-2's synthetic-signed catalog and a profile-1 archive, and are opened by the same function. No other constructor of `RetainedTree` exists.
- **Charges.** Every open, status read, listing step, `readlinkat`, read attempt, buffer and record is charged before it is made. **The work profile is the caller's:** R10a's production profile is D4's and J1's (Q5 of `codex-c2a-plan-r2`), and this law fixes only the interface and its prices.

**7. Lifetime: R10a, the operation, and Run retention (LD-CI-9, r2).**
- **Use at R10a.** C2a's admission opens the capability at its R10a/ER10a step, before the draw (`codex-c2a-plan-r2`, RF-3), under current trust. A release revoked at that instant is never admitted or executed, whatever bytes are present (WS:293-299).
- **Pin acquisition and continuity.**
  - The durable path opens the capability **while holding the lifecycle fence** (`PinRequest::UnderFence`), so no GC census, which also needs the fence, can interleave between admission and the pin.
  - The pin is a shared `flock`, so it survives the fence-to-lease handoff (SL S7: leases follow the fence). The operation holds it through R11 and every later step, until the operation ends or, for a Run, until the Run releases it.
  - `flock` locks die with the process, so a crashed operation releases its pins and no stale pin survives (SL S7's lease rule).
- **GC.** GC removes a generation only under the fence and only after acquiring an **exclusive non-blocking** `flock` on its `pin.lock`. A busy lock means retain, never refusal (SL:658-661). A generation is thus never removed while any live operation pins it.
- **A Run and its retention.** A Run that will be retained copies every preimage it must own through `transfer` into its own retention. That covers the closure descriptor, the manifest body and the file bytes, as IE:1399-1412 and NE:1493-1499 require. **The Run releases its pin only after its own retention is established**; until then, the pin holds.
- **Replay** uses the Run's own retained preimages, with its existing evidence-missing and evidence-corrupt semantics (IE §5). It never consults the component store as a substitute for retained bytes. WS:293's pivot resolution (a retained generation, an installed signed release, or a signed bundle, under current trust) is a **separate operation** with its own current-trust execution and its own unavailability results (WS:295). It is not replay, and not a fallback for missing retained bytes (Q4 ruling).
- **Ephemeral.** The ephemeral path never writes the store and never installs. When its admission has an admitted trust view (MC item 7), it may open the capability, taking the shared pin for its operation's life and releasing it at operation end. It retains no Run. With no admitted trust view it admits nothing and opens nothing (MC:431-437).
- **Excluded:** removal beyond GC's census, updates and migration (DR-110, DR-112).

**8. Refusals and routes — existing codes only (Q5).**
- **The installation command:**

  | Refusal | Class / exit | Code | Detail |
  |---|---|---|---|
  | Release not admitted, revoked or unverified; `platform-unsupported`; profile not 1; `artifact-digest-split`; `archive-capacity`; `install-budget` (before acquisition); any profile admission check (item 3); `archive-changed`; `archive-read-attempts` | request-rejected 2 | `EXTENSION.ADMISSION_REJECTED` | none, except an existing `NT-TCB-*` platform-decision detail where the platform owner supplies one (precedent `crates/host/src/installation_termination.rs`:280-340) |
  | An I/O failure while staging, verifying, making durable or publishing (`ENOSPC` included), or an uncertain publication (item 4) | operational-failed 4 | `EXTENSION.INSTALL_IO_FAILED`, fault cause `extension-install-io` | none |
  | Work exhausted during installation | operational-failed 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant` | `WORK.BUDGET_EXHAUSTED`, a registered detail (common-v4); law 468's route, precedent `installation_termination.rs`:389-396 |
  | Fence busy after 5 s | as SL:588 | `PROJECT.BUSY` | none |
  | An existing generation fails verification on re-install | operational-failed 4 | `HOST.IO_FAILURE` | `DELIVERY.CLOSURE_BYTES_CORRUPT` (WS:1375) |

  The internal subjects are typed diagnostics, not public codes. The implementation must derive full schema-valid terminations, including their carriers and remedies, from these rows, preserving provenance. A registered code is not proof of every placement, so CI-4's package exhibits each.
- **The retained-tree capability at R10a (RF-5, r2).** Its results are **typed inputs to the existing availability, selection and composition owners** (C2a's admission, C4a's enumeration, J2's termination). This law does not itself terminate an analysis:
  - **`NotInstalled`** is handed to those owners as "required closure not installed". The durable detail `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`, under indeterminate 3 with `COVERAGE.PROVIDER_UNAVAILABLE` (WS:1374), appears **only under RTC §7.5's committed-Run authority** (MC item 7:435). **X-8 is carried as a gate** (MC:436): a required non-inventory cell has no lawful unavailable binding today, so required-cell end-to-end composition waits for X-8's successor. Before the draw, the result propagates as data only:
    - no placeholder closure or context is minted;
    - no cell is dropped;
    - the ephemeral path adds no detail (MC item 7's lead ruling; RTC §7.4).
  - **`Absent`, `Length`, `Digest`, `Type`, `Mode`, `LinkTarget`, `Extra`, `Association` and `Custody`** are a promised tree's own corruption. They keep their own cause and never become "not installed" (`codex-c2a-plan-r1` Q3). Durably they route operational-failed 4, `HOST.IO_FAILURE`, with `DELIVERY.CLOSURE_BYTES_CORRUPT`, or `DELIVERY.CLOSURE_BYTES_MISSING` for `Absent` (WS:1375; `public-detail-registry.v1.json`:306). Ephemerally they route the same, with no detail.
  - **`Io`** routes operational-failed 4, `HOST.IO_FAILURE`. **`Budget`** takes the caller's existing budget route (law 468's, for an installation-owned operation).

**9. Units and controls.**
- **Units:**
  - **CI-1, the profile-1 codec:** security, pure, hostile-input. It covers item 3, plus the PKG-AP emitter for fixtures only.
  - **CI-2, the store and the installer:** `crates/lifecycle/src/installation.rs` (a planned row), with the store location in `locations.rs`. It covers items 4 and 5 and LD-CI-10/11, and adds the lifecycle–security edge (item 2).
  - **CI-3, the retained-tree capability:** lifecycle. It covers item 6 and item 7's pin. **C2a-3 binds CI-3**; C2a-4's wiring waits for it (`codex-c2a-plan-r2` Q6).
  - **CI-4, the command surface:** J1, with item 4's handoff and item 8's terminations.
  - **Gates:** X-CI-1 (a sourced installation profile) and X-8 (required-cell composition).
- **Order:** CI-1, then CI-2 and CI-3, with C2a-2's generator emitting profile-1 archives; then C2a-3; then CI-4 with J1.
- **Controls, part 1: the codec, and metadata capacity.** These are pure codec checks, not signed installations:
  - **CI-T1:** PKG-AP's exact 15 `goldenAndNegativeCases`, each as the codec's outcome. AT-ARCHIVE-SIZE-MAX's 8,589,934,591 case and the mode-field maximum are codec-capacity cases, labelled metadata-only (PKG-AP permits a synthetic, metadata-only fixture), never presented as installable signed positives.
  - **CI-T2:** an archive whose length differs from the formula refuses before any member is written, with at most the expected length plus one byte read.
  - **CI-T5:** a tree with a 101-byte path or target refuses `archive-capacity` before any read.
- **Controls, part 2: signed installation** (feasible, manifest-valid releases through the synthetic-signed path):
  - **CI-T3:** `archiveDigest` mismatch; `artifact-digest-split`; a profile id other than 1.
  - **CI-T4:** a host platform with no S8 row; and the alias never appears as an admitted id.
  - **CI-T6:** `archive-changed`; `archive-read-attempts`.
  - **CI-T7 (nothing installed):** failure injected at every step 1-4 point. Each leaves no new generation, every other generation byte-identical, and an inert surviving stage never read as a generation.
  - **CI-T8:** re-install of a verifying generation is a no-op. Re-install of a non-verifying one refuses as corrupt and replaces nothing.
  - **CI-T9 (immutability and refusal):** a published file modified, truncated, removed or replaced by a symlink refuses with its own failure, and nothing rewrites it.
  - **CI-T10 (the capability):** `NotInstalled` versus `Absent`; every typed failure; exact charges against a recorded call log; `Budget`.
  - **CI-T11 (the fixture):** a synthetic-signed release installed and opened through the same code; no synthetic `ComponentStore` in a release build (a source pin).
  - **CI-T12:** a release revoked after installation is never admitted, though its bytes verify.
  - **CI-T13:** source pins: no socket or URL API, and no process spawn, in CI-1 to CI-3.
  - **CI-T14:** a foreign ACL entry on the store or a generation refuses `Custody`.
  - **CI-T15:** the ephemeral path writes nothing.
  - **CI-T16:** every item 8 row's class, code, detail, carrier and remedy, on both paths, with X-8's gate case named and not exercised end to end.
  - **CI-T17 (RF-1, structure):**
    - an extra regular file refuses `Extra`;
    - a removed empty directory refuses `Absent`;
    - a changed symlink target refuses `LinkTarget`, including for **a symlinked analyzer entrypoint**;
    - a directory replaced by a file refuses `Type`;
    - a `generation.json` member disagreeing with the evidence refuses `Association`.
  - **CI-T18 (RF-2, modes):**
    - authenticated file `0200` installs `0400` and reads back;
    - authenticated directory `0600` installs `0500` and is traversed;
    - authenticated file `0100` installs `0500`;
    - nested staging is populated at `0700` and finalized bottom-up;
    - a symlink gets no mode call;
    - an installed mode differing from LD-CI-10 refuses `Mode`.
  - **CI-T19 (RF-3, crash prefixes):** a simulated crash after each barrier, after the rename, and before and after the parent barrier. On restart, each prefix gives absent (not installed), or present and verifying, or present and refusing as corrupt; never usable but incomplete. Nothing is automatically retried or replaced, and an `Indeterminate` publication stops the act.
  - **CI-T20 (RF-4, pins):** GC under the fence retains a generation pinned by a live operation and removes an unpinned one. A pin taken under the fence survives the handoff to the operation's lease. A crashed holder releases its pin. A Run releases only after its retention holds every preimage.
  - **CI-T21 (RF-4, transfer):** `transfer` delivers exact verified bytes; a file changed mid-transfer fails the sink commit; replay never reads the store.
  - **CI-T22 (RF-6, work):** a release whose computed cost exceeds the ledger refuses before acquisition. Exhaustion injected at every priced step publishes nothing and takes law 468's budget route. The charge for a full install equals the recorded call log's price.

## Open questions

- **Q8 (new).** LD-CI-10 grants execute only where the authenticated mode has any execute bit, and grants group and other nothing. Is owner-only access right for the installation user model at M3? The install runs as that user, and the store is private to them.
- **Q9 (new).** Is LD-CI-11's interim reuse of `snapshot_profile()` for the installer acceptable until X-CI-1? Or should the installation profile be derived and sourced (for example, from the census of first-party releases) before CI-2 is accepted?
- **Q10 (new).** Should GC's removal of inert stages, item 4's "surviving stages", be named as GC's census duty here, or left to the GC owner?

## Excluded

- multi-platform installation;
- updates and migration (DR-110, DR-112);
- removal policy beyond GC's census and pins;
- network acquisition;
- any profile other than profile 1;
- any change to MC item 7, C2PM-1, CR-1, the trust owner, RTC or X-8's resolution.

## Not claimed

No code, no binding and no qualification. No public code is added, and no accepted law text is changed.
