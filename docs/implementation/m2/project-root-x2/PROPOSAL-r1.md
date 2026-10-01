# Project-root custody, project admission and first registration — proposal X2 r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X2 of EXIT-PLAN.md, under owner.md §1b, §5, §7 and §8; the selected project registry owner (`project-registry-owner-selection-v2/owner.md`); the security contract S3 (discovery and custody), S7 (locks and leases) and S12; identity-and-evidence §2 and §5; and laws 458 (§3 and §5), 458b, 462, 465 item 4, 468 r5, 458c r6, 461 r3 (item 9, which requires this law) and X1. Every choice here is a lead decision, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each is dated and names the alternative it rejects. Not code. Library only: CLI enablement is X11.

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

   **The native birth sampler.** It is new platform work: `fgetattrlist` `ATTR_CMN_CRTIME` on the retained descriptor. It is charged, and it refuses when unsupported or unreliable, with no mtime or ctime substitute, as the registry owner says.

5. **The registry read.** It is the complete bounded capture of `project-registry.v2` under the held fence. 458c-b1 and 468b already read and decode it as a required file, so this decodes the same retained capture and adds no second read (the X3a item 2 rule).

   It also requires a positive absence of `project-registry.v1`, under the same retained I.

   It validates the whole document and global uniqueness before any match, as the registry owner requires. There is no early match.

6. **First registration** follows the registry owner's ordinary first-use sequence exactly, under X1's `OrdinaryWriteAdmission`, or under the creator's `AdmittedInstallation` from 468c, inside the same held fence. The steps:
   1. **Capacity.** Check registry capacity (4096 rows) and the bounds of every envelope before any effect.
   2. **Allocation.** Draw at most eight ProjectId candidates and eight UUIDv4 namespace candidates, rejecting collisions against all history.
   3. **RESERVED.** Durably publish the RESERVED row: a same-directory temporary file, an exclusive rename, then file and parent barriers using the write receipt's barrier policy. Each prior registry file and its parent are reconfirmed first.
   4. **Namespace.** Durably publish `I/host/projects/N`, holding exactly `writer.lease` and `readers.lease`, through a staged no-replace directory publication (467's primitives).
      - P0 has no `I/host` or `I/host/projects`. The first registration creates or admits them as 465 item 3 does: exact name, private custody, a zero-rights owner allow on creation, and the directory's own barrier and its parent's.
   5. **Marker.**
      - Create `.opensip/` with the zero-rights owner allow if it is absent.
      - Create-new the 92-byte marker with the zero-rights owner allow.
      - Barrier the file, then its parent.
   6. **ACTIVE.** Recheck every original root, marker, namespace and chain observation, then durably replace RESERVED with ACTIVE.

   Any failed or uncertain step latches, with no retry or deletion. The registry owner's explicit recovery handles the leftovers; that recovery is not in X2.

   **Tracked marker.** The marker must be untracked:
   - If the root holds a `.git` directory, X2 reads its index (versions 2 to 4) with a bounded, charged, read-only probe for the exact path `.opensip/project-id.v1`. If the path is present, registration refuses.
   - A `.git` indirection file, or any other VCS marker (`.hg`, `.svn`, `.jj`), refuses first registration as unsupported in M2.
   - Alternative rejected: skipping the check. The registry owner requires it, and a tracked marker would put one ProjectId on every clone.

7. **Namespace admission and leases.** For `Eligible(N)`, the operation:
   - confirms the namespace directory and both lease files under custody;
   - takes its S7 lease without blocking, while the fence is still held: `writer.lease` LOCK_EX|NB for APPEND-WRITE, `readers.lease` LOCK_SH|NB for SHARED-READ, or `readers.lease` LOCK_EX|NB for EXCLUSIVE;
   - then releases the fence, per owner §8 and S7.

   The result is a private `NamespaceAdmission { N, ProjectId, lease, root admission }`. It is the namespace source for X3a's five-field binding. There is no lease without the fence, no waiting for a lease, and no upgrade. A busy lease is the busy row.

   The fence is released only after the lease is held. The write gate's durable confirmation (468) stays valid for this operation's pinned generation, per owner §8.

8. **Refusal rows.** These use 468 item 6 and the existing `PROJECT.*` details. No new code is added; the owner allows only the three of 468.
   - **Root custody, an outside-home root, a chain predicate failure, or an unsupported volume, birth or profile:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subjects `outside-home`, `acl-unreadable`, `foreign-owner`, `mode`, `volume-unsupported`, `birth-unsupported` and the like. This is request-rejected, exit 2, `CONFIG.INVALID`.
   - **Config file custody:** `CONFIG.CUSTODY_REFUSED`.
   - **An explicit-path grammar or join problem:** `PROJECT.EXPLICIT_PATH_INVALID`, as S3 says.
   - **One-sided, contradiction or recovery-needed identity:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `identity-recovery-required` or `identity-contradiction`.
     - The identity contract calls these admission refusals that require explicit recovery or adoption, and no identity detail exists.
     - Alternative rejected: a new code, which the owner's no-new-codes rule forbids.
   - **A tracked marker or an unsupported VCS:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `marker-tracked` or `vcs-unsupported`.
   - **Registry capacity:** `PROJECT.SCOPE_LIMIT`, subject `registry-rows`, under the registry's own class.
   - **Entropy failure, I/O and barriers:** the host I/O row.
   - **A busy lease:** the busy row (`LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`).
   - **Budget:** `WORK.BUDGET_EXHAUSTED`.

   Where S12 fixes a class for a detail, S12 prevails.

9. **Budget.** Every walk, sample, read and git-index probe is charged before it runs, to the session's or the gate's ledger, at the owner's caps. The selection walk is at most 256 levels. The git-index probe is bounded by the 4 MiB per-record ceiling; a larger index refuses on the budget row.

10. **Units after the law.** Each unit is reviewed with an inventory successor.
    - **X2a:** the scoped premise application (a `ProjectChainPolicy` over the shared walk code), the native birth sampler, and the project chain walk.
    - **X2b:** S3 root selection (no unit discovery), `ProjectRootAdmission`, and the registry classification over the retained capture.
    - **X2c:** first registration (item 6), with the git-index probe and `I/host/projects` create-or-admit.
    - **X2d:** namespace admission and leases (item 7). After X2d, X3a's binding can be formed.
    - **Unit discovery** (S3's workspace units, markers, pruning and the 4096 cap) belongs to M3's analysis owner. Item 1's scope already covers its custody-checked objects.

## Forbidden substitutes

- the premise on OpenSIP's operational files, the installation, data-only files, or any object off H's volume;
- a caller-built filesystem sample or premise;
- an mtime or ctime birth substitute, or a device, fsid or marker fallback for volume identity;
- a partial or early-match registry scan;
- registration under a read receipt;
- a lease without the fence, a waiting lease, or a lease upgrade;
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
