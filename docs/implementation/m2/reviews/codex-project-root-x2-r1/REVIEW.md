**Verdict: REQUIRED-FINDINGS — 7 required findings.**

Law X2 r1; reviewer Codex; 2026-09-30. Subject: [docs/implementation/m2/project-root-x2/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md). SHA-256 `4750e7b0d93779c74ca5d5ef2f0fe5d59956842d692200c452d6347a7a5f668f`; 14,390 bytes. Product source checked at `fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98`.

The premise widening and conservative root placement are acceptable lead decisions. The required changes concern registry evidence, registration durability, tracking, lock exclusion, the operation handoff and one diagnostic subject. This is law review, not implementation acceptance or host qualification.

**Decisions on every requested item**

- **Item 1: Accept the explicit, closed scope widening.** 458 section 5 and 458c item 3 previously withheld this premise from projects; X2 is the requested successor decision. The same qualified no-acl-stored fact may apply to the named custody-checked user files as well as directories. User authorship alone does not require refusal. The retained descriptor must independently pass the invocation premise and same-H-volume check; all other S3 custody checks remain mandatory. Operational files, I, data-only files, off-volume objects, absent qualification and unreadable ACL evidence remain excluded. A host probe is not qualification.
- **Item 2: Accept the conservative M2 placement restriction.** Strictly below H, on its volume and outside the named OpenSIP subtree is a closed lead choice. outside-home is a usable subject on the existing root-custody row. Keep the refusal before registry content capture, including when RF-2 changes the read owner.
- **Item 3: Accept the chain/selection structure.** The stronger external-ancestor predicate below H prevents root renaming through a more permissive intermediate directory. Preserve the complete S3 predicates and explicit trust-flag semantics, discovery boundaries, retained no-follow owners and same-ledger original-owner rechecks; the abbreviated root summary is not a replacement for S3.
- **Item 4-5: Accept the classification model; RF-2 and RF-5 must close its inputs.** The full registry table, positive old-v1 absence, native qualified root identity and no read-side registration are the right boundaries. Volume/birth observations are inert data until independently qualified and joined. Eligible cannot bypass unavailable evidence or tracking.
- **Item 6: Require RF-3, RF-4 and RF-5.** The RESERVED -> complete namespace -> marker -> ACTIVE order, staged no-replace namespace, host/projects create-or-admit, independent bounded entropy, and no automatic cleanup/recovery are appropriate. The explicit sequence still needs the replacement, parent-durability and tracking corrections. The parent registry owner continues to require complete active-transition recovery and all capacity/occupancy checks before effects.
- **Item 7: Require RF-1 and RF-6.** The lease must exclude the correct modes and the fence-to-operation handoff must carry every contributing owner. N must come from the eligible ACTIVE row, never a caller value.
- **Item 8: Identity subjects are acceptable; require RF-7 for capacity.** PROJECT.ROOT_CUSTODY_REFUSED with identity-recovery-required or identity-contradiction uses an existing registered detail and free subject, preserving request-rejected/exit 2/CONFIG.INVALID. outside-home, marker-tracked and vcs-unsupported fit that same root admission route. CONFIG.CUSTODY_REFUSED and PROJECT.EXPLICIT_PATH_INVALID keep their S12 request-rejected/CONFIG.INVALID route. Busy remains operation-failed/exit 4/LEDGER.BUSY_TIMEOUT with PROJECT.BUSY; entropy/I/O/barrier failures keep the selected host-I/O row, and work exhaustion keeps its distinct host-invariant row. No new public code is needed.
- **Item 9-10: Accept the broad split after the required producer/handoff corrections.** Use one authoritative ledger for the operation, including registry/VCS validation, serialization, original-owner checks and reserved post-effect work. A 256-level S3 walk and a fail-closed 4 MiB index ceiling are conservative. X2b must own the first registry capture; X2c must own containing-VCS tracking and corrected durability; X2d needs the explicit handoff dependency. Future workspace admission remains M3.

**Required findings**

**RF-1 (P1): EXCLUSIVE must take both project locks, in S7 order**

Proposal items 7; [lines 107-114](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:107).

Item 7 gives EXCLUSIVE only readers.lease LOCK_EX|LOCK_NB. An APPEND-WRITE operation holds only writer.lease, so these operations can coexist in either acquisition order. Releasing the installation fence between admissions makes this a normal interleaving. EXCLUSIVE would therefore permit a writer during GC, purge, migration or repair, contrary to S7's requirement that nothing else be held.

**Required change.** Specify EXCLUSIVE as writer.lease LOCK_EX|LOCK_NB followed by readers.lease LOCK_EX|LOCK_NB, both under the same held installation fence. Preserve APPEND-WRITE's writer-only and SHARED-READ's reader-only modes. On partial acquisition failure, release every acquired project lock before releasing the fence; any retry is outside the fence under the existing S7 policy. Existing lifecycle carriers already implement the two-lock mode and should be the starting point, not the one-lock description in this proposal.

**Validation expected from the implementing units.** Require APPEND-WRITE versus EXCLUSIVE exclusion in both orders, SHARED-READ versus EXCLUSIVE exclusion, partial second-lock failure cleanup, and unrelated-namespace independence.

Evidence: [architecture:docs/v2/contracts/product-v1/security-and-lifecycle.md:588](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/security-and-lifecycle.md:588); [product:crates/lifecycle/src/leases.rs:62](/Users/sb/code/opensip-ai/opensip/crates/lifecycle/src/leases.rs:62).

**RF-2 (P1): Own the first registry capture; the claimed retained capture does not exist**

Proposal items 4, 5, 9, 10; [lines 82-86](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:82).

Item 5 says 458c-b1 and 468b already read and decode project-registry.v2 and that X2 only decodes their retained capture. At the reviewed product HEAD, both paths judge the registry with cap=None: they check custody but do not read its bytes. RequiredFile holds only a relative path and (device, inode), not registry bytes, a decoded document, or its retained file descriptor. X3a r1 adds retention for the pair, endpoint marker and nodes; it does not supply a registry capture. X2b consequently has no specified producer for the very document from which it derives registration authority.

**Required change.** Assign X2 an explicit first bounded, charged capture of the complete registry from retained I under the same fence, retaining the original file/parent and the full metadata needed to recheck the decoded evidence. Validate canonical encoding, all rows and global uniqueness before classification, and retain/recheck positive v1 absence. Preserve item 2's ordering: reject an inadmissible root before this registry read. Missing, unreadable or malformed registry evidence must remain unavailable, never empty. Update X2b's unit inventory and budget to include this work. A one-read rule may apply after this producer exists; it cannot substitute for adding it.

**Validation expected from the implementing units.** Pin one registry content capture per admission, fail on malformed later rows and whole-document duplicates despite an early matching row, detect in-place changes to the original evidence, and refuse missing registry or occupied/unavailable v1. An outside-home root must cause no registry content read.

Evidence: [product:crates/security/src/custody/installation_admission.rs:337](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/installation_admission.rs:337); [product:crates/security/src/custody/installation_admission.rs:962](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/installation_admission.rs:962); [product:crates/security/src/custody/installation_session.rs:587](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/installation_session.rs:587); [architecture:docs/implementation/m2/store-admission-x3a/PROPOSAL-r1.md:27](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/store-admission-x3a/PROPOSAL-r1.md:27); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:33](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:33).

**RF-3 (P1): RESERVED is an atomic registry replacement, with the file barrier before publication**

Proposal items 6, 9; [lines 88-98](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:88).

Step 3 prescribes an exclusive rename and only then file and parent barriers. An established installation, including P0, already has project-registry.v2. A no-replace/exclusive rename to that name fails even for the first registration. Independently, publishing the temporary file before its file barrier exposes an incompletely durable registry replacement at the authoritative name. No-replace is the initial empty-registry publication rule, not the rule for adding RESERVED to an existing document.

**Required change.** State the replacement primitive explicitly: retain and independently reconfirm the exact predecessor file and parent; construct, validate and file-barrier the complete canonical temporary replacement before atomically replacing the registry name; then confirm the containing-directory barrier. Apply this to both the RESERVED and ACTIVE replacements. If 'exclusive' meant only that the fence is held, replace that ambiguous term. Keep no-replace for genuinely new namespace/marker names. Preserve the registry owner's completed-transition-recovery gate, prohibition on any active slot including terminal-but-unretired slots, and all pre-RESERVED collision/path-occupancy and envelope checks. Reserve necessary post-effect confirmation work before each effect; uncertainty stops before later registration steps.

**Validation expected from the implementing units.** Specify the durable prefixes for replacement of an existing empty registry and a nonempty registry, plus failures before/after temporary-file durability, rename and parent confirmation. No uncertain RESERVED publication may proceed to namespace publication, and no uncertain final replacement may claim ACTIVE.

Evidence: [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:54](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:54); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:68](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:68); [architecture:docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:73](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:73).

**RF-4 (P1): Confirm publication of .opensip itself before publishing a durable marker**

Proposal items 6; [lines 94-98](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:94).

For an absent .opensip, the listed sequence creates the directory, creates the marker, barriers the marker and its parent, then activates the row. The marker's parent is .opensip. That confirms the marker entry but does not confirm the .opensip entry in the project root. The sequence can claim ACTIVE without the containing-root barrier that makes the new directory name durable, leaving an ACTIVE row with a missing marker path after a crash.

**Required change.** Give .opensip the same explicit create-or-admit directory-publication treatment used for host/projects: retain and admit its exact name/custody, apply its own directory barrier and the containing project-root barrier before using it as a durable parent, then perform the marker's file and parent barriers. Cover reused .opensip as well; mere existence is not a durability receipt. State the retained-parent/recheck obligations and reserve their post-effect work. These confirmations belong only to the registration writer, not plain read admission.

**Validation expected from the implementing units.** Cover newly created and reused .opensip, failure of its containing-root barrier, and a crash between directory publication and marker publication. A failed or uncertain directory confirmation must not proceed to marker creation or ACTIVE.

Evidence: [architecture:docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:71](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:71); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60).

**RF-5 (P1): Check tracking in the containing repository and during eligible reuse**

Proposal items 4, 6; [lines 102-105](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:102).

The check runs only when the selected root itself holds .git, and its refusal applies only to registration. S3 deliberately permits a nested config to select H/repo/subproject while the containing repository is H/repo/.git. If that index contains subproject/.opensip/project-id.v1, even with the worktree file currently absent, the proposed check sees no .git at the selected root and permits registration at a tracked path. The same gap exists for explicit nested roots and enclosing unsupported VCS markers. Separately, an initially untracked marker can be added to version control after registration; item 4's Eligible classification and item 7 then have no tracking check. The registry owner requires the selected marker to be untracked, not merely untracked on its creation day.

**Required change.** Define a bounded, charged, custody-checked containing-VCS/tracking observation independent of where S3's project-selection walk stops. Check the marker's exact repository-relative path. Unsupported or unreadable containing VCS/index evidence must refuse rather than mean untracked; supporting indirection or other VCS implementations is not required for M2. Apply the observation to eligible reuse and first use, with first-use tracking/absence preconditions completed before RESERVED. Specify original-evidence retention and rechecks. A root with no local VCS marker alone is not evidence that its marker is untracked.

**Validation expected from the implementing units.** Include a nested-config root and an explicit nested root whose marker path is indexed in an ancestor repository, an indexed path whose worktree file is absent, enclosing unsupported VCS, and a registered marker that becomes tracked before a later admission. None may acquire a project lease or create a reservation under the proposed untracked policy.

Evidence: [architecture:docs/v2/contracts/product-v1/security-and-lifecycle.md:132](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/security-and-lifecycle.md:132); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60).

**RF-6 (P1): Define the joint owner handoff before releasing the installation fence**

Proposal items 7, 10; [lines 107-114](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:107).

X2 unconditionally releases the fence and returns NamespaceAdmission containing N, ProjectId, lease and root admission, then says this is the source for a binding formed after X2d. X3a r1's SelectedStoreEndpoint is borrowed from one held session. There is no defined joint transfer of the endpoint/store/lineage owners into the operation that survives X2's fence release. The current DurableInstallation::release consumes the gate and closes its retained chain. A copied (N,S,G,K) or continued use of a provisional borrowed reader cannot fill this gap; reopening a session while holding the project lease reverses the required lock order.

**Required change.** Split namespace validation/lease acquisition from final handoff, or specify a combined checked handoff owner. While the same fence is held, join the eligible row/root/marker/namespace and X3a endpoint, acquire the required lease, and transfer the immutable row/generation plus original project, namespace, store and lineage owners to a distinct operation context before unlocking. The mutable registry/pair captures then become provenance as owner section 8 requires. State which unit owns this bridge, and adjust the X2d/X3a/X3b dependency wording; it may be a later unit, but X2d must not mandate releasing the needed session before that unit can act. No automatic promotion of fenced provisional readers or backwards fence reacquisition.

**Validation expected from the implementing units.** Require that the operation cannot be constructed from copied fields or a released observation session, that relevant original owners survive under the lease, and that unrelated registry/core-pair replacement does not invalidate the pinned operation while same-N mutation/store reselection remains excluded.

Evidence: [architecture:docs/implementation/m2/store-admission-x3a/PROPOSAL-r1.md:17](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/store-admission-x3a/PROPOSAL-r1.md:17); [architecture:docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:138](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:138); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:104](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:104); [product:crates/security/src/custody/installation_admission.rs:381](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/installation_admission.rs:381).

**RF-7 (P2): Pin the scope-limit class and count/limit subject**

Proposal items 8; [lines 124-129](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:124).

The proposed subject registry-rows omits the count and limit prescribed by the existing PROJECT.SCOPE_LIMIT projection. 'Under the registry's own class' is also too indirect for the requested row decision. The registered code's selected mapping is request-rejected, exit 2, REQUEST.UNSATISFIABLE, with a field:count>limit subject; it is not CONFIG.INVALID or the WORK.BUDGET_EXHAUSTED host-invariant row. A generic schema accepts both subjects because subject is a string, so schema success does not establish this semantic mapping.

**Required change.** Write the full row explicitly. For example, refusing an insertion into a 4096-row registry can report subject registry-rows:4097>4096, with 4097 explicitly the attempted resulting count, request-rejected/exit 2/REQUEST.UNSATISFIABLE and no faultCause. Define equally precise bounds for any byte or transition-wrapper capacity case assigned this detail. Give the registry-capacity use a remedy consistent with lifetime history retention; do not direct users to discard rows or invoke nonexistent automatic compaction. Preserve the separate budget row for actual work-budget exhaustion.

**Validation expected from the implementing units.** Pin the refusal at the full-registry boundary, including exact D9 class/code/exit, count/limit subject and applicable remedy. Keep schema validation separate from semantic route checks.

Evidence: [architecture:docs/v2/contracts/product-v1/security-and-lifecycle.md:1323](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/security-and-lifecycle.md:1323); [architecture:docs/coop/design-corrections/native/native_evidence_model.v2.py:3608](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py:3608); [architecture:docs/coop/design-corrections/native/native_evidence_model.v2.py:4050](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py:4050); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:56](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:56).

**Nonblocking source correction**

Item 4 and X2a call fgetattrlist/ATTR_CMN_CRTIME sampling new platform work. The product already exports observe_directory_birth and RetainedDirectory::observe_birth in crates/platform/src/filesystem/directory_birth.rs (lines 27-35), exported from filesystem.rs:2357. Reuse that sampler and add the charged admission/qualification integration; do not create a second native sampler. Its existence does not itself supply a qualified root capability.

**Verification and limits**

- Verified the subject SHA-256 and 14,390-byte length against hashes.txt, including immediately before writing this review.
- Read the requested law/contract context and inspected current product source at fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98. Product git status was clean at the final source check.
- Used X3a r1 as requested. During review it was preserved as store-admission-x3a/PROPOSAL-r1.md while the live PROPOSAL.md advanced to r2; the r1 borrowed-session/retention boundary is the context reviewed here.
- Checked the mentioned public detail names in the selected detail registry and traced S12/native-model projections. In an in-memory TypeScript command-envelope:7 schema probe, six representative failure envelopes validated: outside-home, identity-contradiction, identity-recovery-required, marker-tracked, and both scope subjects (registry-rows and registry-rows:4097>4096). This checks shape only, not route/remedy correctness.
- Analyzed lock interleavings, nested-project tracking and durability prefixes against the selected owners. These are static counterexamples, not executed native crash or filesystem qualification tests.
- No product Cargo, repository edits, commits, pushes or delegation. Only REVIEW.md and review.json were written in the requested output directory. No real-host project-admission success is claimed; the proposal explicitly leaves this host BASELINE-ATTESTED.
