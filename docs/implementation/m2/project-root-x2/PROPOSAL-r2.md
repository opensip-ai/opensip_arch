# Project-root custody, project admission and first registration — proposal X2 r2

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X2 of EXIT-PLAN.md, under owner.md §1b, §5, §7 and §8; the selected project registry owner (`project-registry-owner-selection-v2/owner.md`); the security contract S3 (discovery and custody), S7 (locks and leases) and S12; identity-and-evidence §2 and §5; and laws 458 (§3 and §5), 458b, 462, 465 item 4, 468 r5, 458c r6, 461 r3 (item 9, which requires this law) and X1. Every choice here is a lead decision, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each is dated and names the alternative it rejects. r2 answers Codex X2 r1 RF-1 to RF-7 against product f7acb6d (X1a integrated). r1 bytes are preserved in PROPOSAL-r1.md. Not code. Library only: CLI enablement is X11.

## Problem

Under 461, an omitted ACL is unreadable at `check_descriptor_observation`. S3's directory custody requires that "the ACL was readable", so every ordinary project refuses.

Probes on this host (2026-09-30, read-only `ls -led` and `stat`):
- `/Users/sb/code`, `/Users/sb/code/opensip-ai`, `/Users/sb/code/opensip-ai/opensip` and its `.git` all omit the ACL.
- All four are on the same volume as H (`disk3s5`, the APFS data volume).
- The other mounted volumes (`/Volumes/Claude` and `/Volumes/Install ChatGPT`) are read-only HFS disk images mounted `noowners`.

Without the premise, no project root can be admitted. Without an admitted root, no ProjectId and namespace can be registered. Without a registered namespace, X3a's store binding (owner §8) and every project writer cannot exist. The product holds only the pure registry syntax (`identity::project_registry`) and the namespace lease carriers (`lifecycle::leases`). It has no native discovery, root admission, registration or lease acquisition.

## Decisions

1. **The evidence for project custody is the same omission premise, with a new, closed scope.**
   - **The fact is the same.** 458 item 3's Evidence B says that on a filesystem whose qualified row signs `installAclOmission: "no-acl-stored"`, an omitted ACL means no ACL is stored. That holds for every object on that filesystem. 458 §5 and 458c item 3 withheld it from projects by scope, not because the fact differs. This law widens the scope; it does not create new evidence.
   - **The premise.** It is the `AclOmissionPremise` of this invocation's receipt: the read receipt (458c-a) or the write receipt (X1), from the one producer.
   - **How it applies.** It applies only through `AclOmissionPremise::admits` on the retained descriptor being judged. That is the premise's own `fstatfs`: local, not union, type qualified.
   - **In addition, every object it admits must pass `is_home_filesystem`.** The premise covers only H's own volume.
   - **Objects it covers:**
     - the directories from H, exclusive, down to the project root;
     - the project root;
     - the directories S3's walk examines from the launch directory up to the selected root;
     - `.opensip/` when it exists, as a project directory;
     - the project's custody-checked files: the S3 config file and, when unit discovery lands, the workspace marker files.
   - **Objects it never covers:**
     - OpenSIP's own operational files in the project, such as `.opensip/project-id.v1`;
     - the installation and its private descendants;
     - files read only as data, such as source and manifests read after custody;
     - anything off H's volume.
   - **Without a premise,** on a BASELINE-ATTESTED host, a V1 profile or a row without the member, every omitted ACL in scope refuses, as today.
   - **Alternative rejected:** a separate project-only profile member. The fact is per filesystem, and 458 item 6 already qualifies it per row; a second member would duplicate the qualification without adding evidence.
   - **Alternative rejected:** applying the premise to any qualified volume. External APFS volumes are commonly mounted ignoring ownership, and the qualification is by type name, so it cannot see that. A later law may widen this with an explicit `MNT_IGNORE_OWNERSHIP` refusal.

2. **Where a project root may be.** In M2 the selected project root must:
   - be strictly below H, on H's volume (`is_home_filesystem`);
   - not be inside `H/Library/Application Support/OpenSIP`;
   - not be H or any ancestor of H. Each of those contains the installation, or is shared by every project.

   A root elsewhere refuses on `PROJECT.ROOT_CUSTODY_REFUSED` with subject `outside-home`, before any registry read.

   Alternative rejected: arbitrary roots with a root-to-project walk outside H. Ancestors outside H, such as `/opt` or `/Volumes`, have no qualified custody profile, and this host has no case that needs them.

3. **The project chain walk.** Project admission walks with charged, retained, no-follow handles:
   - from `/` to H, exactly as 468 r5 step 0 does, under 465 item 4's scope;
   - then from H down to the selected root.

   **Each directory strictly between H and the root** must pass the external-ancestor predicate (458 item 1: no principal other than the invoking user or root holds a right beyond list, search and read). Item 1's premise applies to it.

   **The root** must pass S3's directory custody: owner is the invoking user or root; no other-write; no group-write unless the gid is in the explicit `--trust-group` set; no ACL write grant to others; ACL readable, or omitted under the premise.

   **Selection stays S3's.** The S3 discovery walk (launch directory upward, at most 256 levels, with the boundaries in precedence) selects the root. A custody failure at an ancestor stays a discovery boundary, as S3 says. The chain walk above runs after selection, over the selected root's chain. The selection walk is charged on the same ledger.

   **Recheck.** The chain is rechecked under the held fence as in 468 item 3's recheck set, with the project chain added.

   Alternative rejected: no ancestor check below H. A writable ancestor could rename the root during the operation. The registry incarnation key detects that only after the fact.

4. **What a project root admission is.** A private, non-Clone `ProjectRootAdmission`, produced only under a held installation fence: the 458c read session, or the 468 write gate for X1 writers. It holds:
   - the retained chain and root descriptor;
   - the canonical path bytes;
   - the root identity sampled from the retained root descriptor: device, inode, native birth, and the APFS volume UUID (`DirectoryVolumeObservation`);
   - the marker observation at `.opensip/project-id.v1`;
   - the complete registry classification from the registry owner's table:
     - **Eligible(N, ProjectId):** exactly one matching ACTIVE row;
     - **FirstUseCandidate:** marker positively absent, and no live binding to this locator or incarnation;
     - **RecoveryNeeded:** a matching RESERVED row;
     - **OneSided;**
     - **Contradiction.**

   It grants:
   - **Eligible:** namespace admission (item 7);
   - **FirstUseCandidate:** item 6's registration, under the write gate only;
   - **RecoveryNeeded, OneSided, Contradiction:** nothing.

   It is never a write capability on its own. Read commands get only the classification and Eligible's namespace for read leases.

   **The native birth sampler.** It is the existing `RetainedDirectory::observe_birth` (`crates/platform/src/filesystem/directory_birth.rs`). X2 adds only its charged admission use: it is charged before it runs, and an unsupported or unreliable birth refuses, with no mtime or ctime substitute, as the registry owner says. There is no second native sampler. The sample is inert data until joined with the qualified premise and the root admission above.

   **Tracking.** Every classification that grants anything (Eligible, and FirstUseCandidate) also requires item 6a's tracking observation to show the marker path untracked. Otherwise the admission refuses on item 8's tracking row and grants nothing.

5. **The registry read: X2 owns the first capture.** At f7acb6d, the write gate and the read session judge `project-registry.v2`'s custody without reading its bytes (`judge("project-registry.v2", None, …)`), and the retained `RequiredFile` keeps only a path and (device, inode). There is no retained capture to reuse, so X2 adds the producer:
   - **Order.** Item 2's placement check runs first. An outside-home or otherwise inadmissible root refuses before any registry content read.
   - **One capture.** Under the held fence, X2 makes one bounded, charged read of the complete registry: at most 4 MiB, through the retained I, no-follow, by the registry file whose custody the session or gate already judged. It retains the original file descriptor, its parent (I), and the file's full metadata sample: device, inode, size, mode, link count, owner, modified and changed times. It also retains the exact bytes and the decoded document.
   - **Validation.** The whole document is validated before any classification: canonical encoding, every row, ordering, and global uniqueness of live ProjectId, locator, incarnation and namespace. There is no early match. A malformed later row, or a whole-document duplicate, refuses even when an earlier row matches.
   - **The old name.** X2 requires positive no-follow absence of `project-registry.v1` under the retained I, and retains that observation.
   - **Rechecks.** Both the registry's full metadata sample and the v1 absence join item 3's recheck set, so an in-place rewrite of the registry fails the recheck.
   - **Unavailable, never empty.** A missing, unreadable, oversized or malformed registry, or a present or unreadable v1, is unavailable on the host I/O row or the incomplete row, never an empty registry.
   - **One read per admission.** Later consumers in the same admission (classification, item 6, item 7 and the item 7a handoff) use this capture and never read the registry again.
   - **Owner.** X2b owns this producer and its budget.

6. **First registration** follows the registry owner's ordinary first-use sequence exactly, under X1's `OrdinaryWriteAdmission` (f7acb6d), or under the creator's `AdmittedInstallation` from 468c, inside the same held fence. It needs a FirstUseCandidate (item 4) with item 6a's untracked observation.

   **Preconditions before any effect.** All of these run first:
   - the registry owner's completed active-transition-recovery gate. Any active transition slot, including a terminal one not yet retired, refuses;
   - capacity: rows, bytes, and the worst legal all-registered transition wrappers, within the 4096-row profile (item 8's scope-limit row);
   - collision checks against all history;
   - occupancy of the candidate namespace path, positively absent no-follow;
   - the marker's positive absence;
   - item 6a's tracking observation.

   Each effect reserves its own post-effect confirmation work before it runs (467 item 6). Any failed or uncertain step latches, with no later registration step, no retry and no deletion.

   **The registry replacement primitive.** It is used for both RESERVED and ACTIVE, and is not a no-replace publication:
   1. Reconfirm the exact predecessor registry file (item 5's full sample) and its parent I.
   2. Construct the complete canonical replacement document, and validate it with the same decoder.
   3. Write it to a fresh same-directory temporary name, created exclusively. Barrier that file (`F_FULLFSYNC`, the receipt's policy), and confirm it by identity and exact bytes.
   4. Atomically replace `project-registry.v2` with the temporary file (`rename`, replacing the predecessor).
   5. Confirm I's directory barrier, then recheck that the name holds the new file by identity.

   No-replace stays only for names that are genuinely new: the namespace directory and the marker. "Exclusive" in r1 meant only that the fence is held; r2 drops the word. Uncertainty at any step before step 5 completes stops before the next registration step.

   **The steps:**
   1. **Allocation.** Draw at most eight ProjectId candidates and eight UUIDv4 namespace candidates, each from independent OS-CSPRNG draws.
   2. **RESERVED,** through the replacement primitive.
   3. **Namespace.** Durably publish `I/host/projects/N`, holding exactly `writer.lease` and `readers.lease`, through a staged no-replace directory publication (467's primitives).
      - P0 has no `I/host` or `I/host/projects`. The first registration creates or admits each as 465 item 3 does: exact name, private custody, and a zero-rights owner allow on creation. Each also gets its own directory barrier and its parent's barrier, whether new or reused.
   4. **`.opensip` directory.** Create or admit `.opensip` under the retained project root, as 465 item 3 does:
      - exact name and S3 directory custody (item 1's premise applies);
      - a zero-rights owner allow on creation;
      - `.opensip`'s own directory barrier, then the containing project root's barrier.

      This applies to a reused `.opensip` too: existence is not a durability receipt. The retained `.opensip` handle and the root handle join the recheck set. A failed or uncertain confirmation stops before the marker.
   5. **Marker.** Create the 92-byte marker no-replace under the retained `.opensip`, with the zero-rights owner allow. Barrier the file, then `.opensip`'s directory barrier.
   6. **ACTIVE.** Recheck every original root, `.opensip`, marker, namespace, registry, chain and tracking observation, then replace RESERVED with ACTIVE through the replacement primitive.

   **Durable prefixes.** These are for X2c's tests.
   - Before step 2's file barrier: nothing is durable.
   - After step 2's step 4 (the replace) but before step 5 (I's barrier): RESERVED may or may not survive, and the act stops.
   - After RESERVED: the namespace, `.opensip` and marker may be partially present.
   - Before ACTIVE's confirmation: RESERVED or ACTIVE may survive.

   Each leftover is the registry owner's explicit-recovery case, which X2 does not implement. Plain read admission never takes any of these barriers.

6a. **Tracking observation (both first use and eligible reuse).** This is a bounded, charged, custody-checked observation that does not depend on where S3's selection walk stopped:
   - **Finding the repository.** Walk the retained chain from the selected root upward to `/`. At each directory, look up `.git`, `.hg`, `.svn` and `.jj` no-follow.
   - **Refusals.** Any `.hg`, `.svn` or `.jj` at any level refuses, as does a `.git` that is not a directory (indirection or a worktree file). Each refuses on the `vcs-unsupported` subject: those implementations could track the path, and M2 does not read them.
   - **The nearest repository.** The nearest `.git` directory is the repository: Git does not track paths inside a nested repository.
     - **The index.** Read its `index` no-follow, under custody, charged, at most 4 MiB. It must be index version 2, 3 or 4, with no split-index (`link`) or sparse-directory extension. Otherwise it refuses as `vcs-unsupported`.
     - **No index.** A positively absent `index` in a `.git` directory means no tracked paths.
     - **The check.** Look up the marker's exact repository-relative path (`<root relative to the repository>/.opensip/project-id.v1`). The path is tracked if the index has that entry, whether or not the worktree file exists.
   - **No repository.** If no VCS marker is found up to `/`, the observation is "no repository". That is untracked only because every directory on the chain was looked up positively. A missing local `.git` alone is not evidence.
   - **Unreadable evidence.** Unreadable, oversized or malformed VCS or index evidence refuses; it is never treated as untracked.
   - **Rechecks.** The repository directory, the `index` file's full metadata sample, and every negative lookup join the recheck set.
   - **When it runs.** It runs for Eligible before any lease is taken, and for FirstUseCandidate before RESERVED. A registered marker that has since become tracked therefore refuses on the next admission, and takes no lease.

7. **Namespace admission and leases.** For `Eligible(N)`, with N taken only from the ACTIVE row in item 5's capture and never from a caller, under the same held fence:
   - Confirm the namespace directory and both lease files under custody.
   - Take the S7 lease without blocking, starting from the existing `lifecycle::leases` two-lock implementation:
     - **SHARED-READ:** `readers.lease` LOCK_SH|LOCK_NB only.
     - **APPEND-WRITE:** `writer.lease` LOCK_EX|LOCK_NB only.
     - **EXCLUSIVE:** `writer.lease` LOCK_EX|LOCK_NB, then `readers.lease` LOCK_EX|LOCK_NB, both while the fence is held.
   - **Partial failure.** If any lock fails, release every project lock already taken, in reverse order, before the fence is released. A retry happens outside the fence under S7's existing backoff.
   - **Rules.** There is no lease without the fence, no waiting for a lease, and no upgrade. A busy lease is the busy row.

   The result is a private `FencedNamespace`: the held lease, the row snapshot, and the root admission. It still borrows the held fence. **X2d does not release the fence.** Item 7a decides when the fence is released.

7a. **The checked operation handoff (a lead decision; owner: unit X2e, after X2d and X3a-1).** One combined owner builds the operation context while the same fence is held:
   1. **Join.** Join the Eligible row, root admission, marker, tracking observation and `FencedNamespace` with X3a's `SelectedStoreEndpoint` from the same session or gate.
   2. **Transfer.** Move these into a private, non-Clone `ProjectOperation`:
      - the immutable row snapshot and selected generation;
      - the original project root, `.opensip`, marker and namespace owners;
      - the store endpoint and lineage owners.

      It is built by moving owners out of the fenced session or gate, never from copied fields.
   3. **Release the fence.** Only then is the fence released, per owner §8 and S7.

   **After the release.** The mutable registry and pair captures become provenance. An unrelated registration, or a same-schema core selection, cannot invalidate the pinned operation. Same-N move, retirement or store reselection stays excluded by the lease.

   **What it never does.** It never promotes a fenced provisional reader, reopens a session while holding the project lease, or reacquires the fence backwards.

   **Without X2e.** Until X2e lands, a `FencedNamespace` can only be dropped, which releases the lease and then the fence. X3a-1's endpoint and X3b's writers depend on X2e, not on X2d alone.

   **Alternative rejected:** X2d releasing the fence and returning `NamespaceAdmission`. The endpoint and lineage owners would not survive the release, and reopening them under the lease reverses the lock order.

8. **Refusal rows.** These use 468 item 6 and the existing `PROJECT.*` details. No new code is added; the owner allows only the three of 468.
   - **Root custody, an outside-home root, a chain predicate failure, or an unsupported volume, birth or profile:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subjects `outside-home`, `acl-unreadable`, `foreign-owner`, `mode`, `volume-unsupported`, `birth-unsupported` and the like. This is request-rejected, exit 2, `CONFIG.INVALID`.
   - **Config file custody:** `CONFIG.CUSTODY_REFUSED`.
   - **An explicit-path grammar or join problem:** `PROJECT.EXPLICIT_PATH_INVALID`, as S3 says.
   - **One-sided, contradiction or recovery-needed identity:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `identity-recovery-required` or `identity-contradiction`.
     - The identity contract calls these admission refusals that require explicit recovery or adoption, and no identity detail exists.
     - Alternative rejected: a new code, which the owner's no-new-codes rule forbids.
   - **A tracked marker, or an unsupported or unreadable VCS, on first use or eligible reuse (item 6a):** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `marker-tracked` or `vcs-unsupported`.
   - **Registry capacity:** `PROJECT.SCOPE_LIMIT`, request-rejected, exit 2, `REQUEST.UNSATISFIABLE`, with no fault cause, and the S12 `field:count>limit` subject:
     - rows: `registry-rows:<n>>4096`, where n is the attempted resulting row count (4097 when the registry already has 4096 rows);
     - bytes: `registry-bytes:<n>>4194304`, where n is the canonical byte length of the resulting RESERVED or ACTIVE document, or of a worst-case later terminal spelling;
     - transition wrappers: `registry-transition-rows:<n>>4096`, where n is the namespace count of the worst legal all-registered transition wrapper.

     The remedy text is: "This installation's project registry is at its lifetime capacity. Registry entries are kept for the life of the installation and are never removed, so a new project cannot be registered here. Use a project that is already registered." It does not suggest discarding rows or compaction.

     Actual work-budget exhaustion stays the separate `WORK.BUDGET_EXHAUSTED` row.
   - **Entropy failure, I/O and barriers:** the host I/O row.
   - **A busy lease:** the busy row (`LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`).
   - **Budget:** `WORK.BUDGET_EXHAUSTED`.

   Where S12 fixes a class for a detail, S12 prevails.

9. **Budget.** Everything is charged before it runs, to one authoritative ledger for the operation (the session's or the gate's), at the owner's caps. That includes every walk, sample, the registry capture and validation, replacement serialization, the VCS lookups and index read, original-owner rechecks, and reserved post-effect work. The selection walk is at most 256 levels. The registry and the git index are each bounded by the 4 MiB per-record ceiling. A larger registry is unavailable, and a larger index refuses as `vcs-unsupported`.

10. **Units after the law.** Each unit is reviewed with an inventory successor.
    - **X2a:** the scoped premise application (a `ProjectChainPolicy` over the shared walk code), the charged use of the existing birth sampler, and the project chain walk.
    - **X2b:** S3 root selection (no unit discovery), the item 5 registry capture producer, `ProjectRootAdmission`, and the item 6a tracking observation.
    - **X2c:** first registration (item 6), with the registry replacement primitive and the create-or-admit of `I/host/projects` and `.opensip`.
    - **X2d:** namespace admission and leases (item 7), returning `FencedNamespace` with the fence still held.
    - **X2e:** the checked operation handoff (item 7a). It depends on X2d and X3a-1, and X3a's store binding and X3b depend on it.
    - **Unit discovery** (S3's workspace units, markers, pruning and the 4096 cap) belongs to M3's analysis owner. Item 1's scope already covers its custody-checked objects.

## Forbidden substitutes

- the premise on OpenSIP's operational files, the installation, data-only files, or any object off H's volume;
- a caller-built filesystem sample or premise;
- an mtime or ctime birth substitute, or a device, fsid or marker fallback for volume identity;
- a partial or early-match registry scan;
- registration under a read receipt;
- a lease without the fence, a waiting lease, or a lease upgrade;
- EXCLUSIVE without both project locks;
- releasing the fence before the item 7a handoff;
- an operation context built from copied fields or a released session;
- treating a missing local `.git` as untracked;
- a no-replace publication of the existing registry name, or a registry replacement published before its file barrier;
- first registration over a tracked or unreadable marker;
- deleting or adopting a leftover reservation, namespace or marker;
- a new public code.

## Not claimed

- CLI enablement;
- unit discovery;
- explicit recovery, adoption, move, fork and retirement;
- project roots outside H or on other volumes;
- Linux;
- any qualified measured row for this macOS 27 host. It stays BASELINE-ATTESTED, so real project admission here refuses, and tests use synthetic signed profiles.
