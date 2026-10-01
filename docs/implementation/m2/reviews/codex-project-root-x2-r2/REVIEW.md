**Verdict: REQUIRED-FINDINGS — 4 required findings.**

Law X2 r2; Codex; 2026-09-30. Subject: [docs/implementation/m2/project-root-x2/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md). SHA-256 `445d30286948bc60524b5adc60a941f97e5f042a42627b73d94cba83e9bf0771`; 24,117 bytes. Product source checked at `f7acb6d7f8acadcbc0bf81d141f39077d817f043`.

The replacement ordering, two-lock EXCLUSIVE mode, first registry capture, .opensip durability, and X2e ownership handoff address the corresponding r1 problems. The nearest-repository decision is unsound. Tracking also needs a closed custody/layout policy, and first registration must advance its retained evidence after its own publications.

**Disposition of the r1 findings**

| r1 finding | Disposition | Reason |
| --- | --- | --- |
| RF-1 | CLOSED | Item 7 now gives EXCLUSIVE both locks in writer-then-readers order, with reverse partial cleanup before fence release. |
| RF-2 | CLOSED for the initial capture | Item 5 correctly owns the first complete charged capture, full metadata and original descriptors, v1 absence, whole-document validation and placement-before-read order. New r2 RF-2 addresses advancing that capture across this writer's own publications. |
| RF-3 | CLOSED for replacement ordering | The temporary file is validated and made durable before replacing the existing registry name, followed by the parent barrier. The recovery gate and pre-effect checks are explicit. New r2 RF-2 addresses the current predecessor between the two replacements. |
| RF-4 | CLOSED | Both new and reused .opensip receive their own and containing-root barriers before marker publication. |
| RF-5 | NOT CLOSED | Both first-use and eligible-reuse now check tracking, and ancestor discovery is added, but the nearest-repository assumption still misses tracked markers. New r2 RF-1, RF-3 and RF-4 address tracking completeness, custody scope and layout interpretation. |
| RF-6 | CLOSED at the law/ownership level | X2d retains the fence. X2e joins same-session owners, moves them into a distinct ProjectOperation before unlocking and demotes mutable global captures to provenance. The lease remains part of the moved FencedNamespace. See OBS-1 for a contradictory dependency sentence. |
| RF-7 | CLOSED | The scope-limit class, exit, REQUEST.UNSATISFIABLE code, absent fault cause, attempted count/limit subjects and retention-compatible remedy are now explicit. Actual work exhaustion remains separate. |

The unchanged conditional premise widening to named user custody objects and the conservative H-volume/root placement remain acceptable. The new tracking requirement needs the explicit scope completion in RF-3. X2e's combined same-fence transfer is sound as a law-level design; RF-2 must first provide the confirmed ACTIVE owner that a newly registered operation joins.

**Required findings**

**RF-1 (P1): A nearer Git repository does not exclude tracking by an outer index**

[Proposal lines 140-143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:140).

The nearest-repository rule is unsound. Consider H/outer/.git whose index already contains inner/.opensip/project-id.v1, then an independently initialized H/outer/inner/.git with no index. Initializing the inner repository does not remove the outer index entry. Selecting inner makes item 6a report no tracked paths from the nearer repository even though the outer index tracks the marker. The worktree marker can also be absent while that outer index entry remains, so this affects first registration as well as reuse. Git's ordinary treatment of newly added embedded repositories is not an invariant over existing index entries.

**Required change.** Inspect every enclosing supported repository's index for the corresponding repository-relative marker path, or conservatively refuse multiple enclosing repositories. Do not stop the evidence check at the nearest .git. Retain and recheck all contributing index/name observations within the same ledger. An outer gitlink can be distinguished from an actual indexed marker path; neither the presence of an inner .git nor a gitlink assumption proves the outer index is clear.

**Implementing-unit validation.** Require a nested repository with an empty/absent inner index and an outer index containing the marker path, both with the marker present and with it absent. Both must refuse before a lease or RESERVED publication. Also cover a normal submodule/gitlink case according to the explicitly chosen M2 support boundary.

The registry owner requires the selected marker to be untracked (owner.md:46). The counterexample is a static inference from Git's documented independent repository initialization and direct index-entry insertion; no Git fixture was created during this review. [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46); [Git init documentation](https://git-scm.com/docs/git-init); [Git update-index: cacheinfo and index-info](https://git-scm.com/docs/git-update-index#_using_cacheinfo_or_info_only).

**RF-2 (P1): Advance retained evidence after each authorized registry publication**

[Proposal lines 86-91](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:86).

Item 5 retains one original registry capture R0 and says registration, namespace admission and handoff all use it. Item 6 then replaces R0 with RESERVED (R1), but the next replacement reconfirms 'item 5's full sample', and ACTIVE first rechecks every original registry observation. The original named inode is no longer current. Moreover, after ACTIVE is durably published as R2, item 7 admits only an ACTIVE row in item 5's capture; a FirstUseCandidate's R0 has no such row. As written, successful self-publication either fails the unchanged original-owner checks or leaves no admissible source for the new namespace. The same distinction is needed for the originally absent marker/namespace names that this writer intentionally creates.

**Required change.** Specify a private, checked successor-owner transition under the held fence. After confirmed RESERVED replacement, retain the newly published file, its validated document and post-publication metadata/name binding as the current registry predecessor for ACTIVE. After confirmed ACTIVE replacement, make that exact published row/document the source of Eligible and the handoff. Demote replaced captures to predecessor provenance without treating arbitrary changes as authorized. Transfer positively absent names to their checked newly published owners only through the relevant successful writer step. Reuse retained temporary-file owners and validated bytes to preserve the single initial registry-content capture; do not invent ACTIVE from the candidate IDs or silently disable rechecks. An explicitly separate fresh admission is another possible design, but must be stated and cannot repair using R0 as the predecessor of the second replacement. Align the durable-prefix table with these states: before a new publication is confirmed, the predecessor remains the last guaranteed authoritative state; unconfirmed writes are not guaranteed absent from durable storage.

**Implementing-unit validation.** Trace an empty established registry through R0 -> RESERVED R1 -> ACTIVE R2 -> project lease, identifying the current file owner and decoded row at every step. Require the second replacement to reconfirm R1, not R0; reject unrelated replacement or mutation at each boundary, and refuse all uncertain publications. Require no lease from merely serialized or unconfirmed ACTIVE bytes.

The contradiction is between item 5's single retained capture/recheck rule, item 6's two replacements (lines 106-127), and item 7's ACTIVE-row source restriction (line 149). The existing gate also records required-file identities, so its registry limb must participate in the authorized successor transition rather than continue expecting R0. [architecture:docs/implementation/m2/project-root-x2/PROPOSAL.md:106](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:106); [architecture:docs/implementation/m2/project-root-x2/PROPOSAL.md:127](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:127); [architecture:docs/implementation/m2/project-root-x2/PROPOSAL.md:149](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:149); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:54](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:54); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:60); [product:crates/security/src/custody/installation_admission.rs:337](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/installation_admission.rs:337).

**RF-3 (P2): Close the omission-premise scope for the newly required Git custody checks**

[Proposal lines 137-146](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:137).

Item 6a now makes repository/index custody a prerequisite for every useful admission, but item 1's closed omission scope includes neither the child .git directory nor its index. They are not directories on the H-to-project or S3 launch walk, and the enumerated custody-checked files are the S3 config and workspace markers. Law 461 maps omitted ACLs to unreadable outside an explicitly admitted premise scope. Thus an otherwise supported ordinary Git project whose .git and index omit ACLs still refuses even under a qualified omission profile. Applying the premise implicitly would instead violate the law's closed scope. The current checkout's .git directory and index both show omitted ACLs in a read-only ls -led probe; that probe is illustrative, not qualification.

**Required change.** Select an explicit custody policy for the finite tracking-evidence objects. If ordinary omitted-ACL Git metadata is intended to work, extend item 1 deliberately to the admitted .git directory and exact index, and any configuration evidence required by RF-4, under the same retained-descriptor, qualified-premise and H-volume constraints. Cover every enclosing repository the tracking rule consults; refuse unsupported off-volume/out-of-scope evidence. Alternatively, explicitly select and disclose refusal of omitted-ACL tracking metadata as the M2 support restriction. Do not weaken custody or extend the premise to all data files by implication.

**Implementing-unit validation.** Under synthetic qualified profiles, pin the chosen result for omitted ACLs on .git and index separately, with all other checks passing. Preserve refusal without the premise, for off-volume evidence, and for OpenSIP operational files. Show that the native tracking implementation uses the selected scope rather than a generic omitted-ACL exemption.

Proposal item 1 lists the admitted objects and excludes data-only files. S3 requires readable ACL evidence, and the current descriptor-custody choke point retains the law-461 omitted-to-unreadable conversion. [architecture:docs/implementation/m2/project-root-x2/PROPOSAL.md:23](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:23); [architecture:docs/v2/contracts/product-v1/security-and-lifecycle.md:121](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/security-and-lifecycle.md:121); [product:crates/security/src/custody.rs:326](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody.rs:326).

**RF-4 (P1): Prove the worktree root used to interpret index paths**

[Proposal lines 140-143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md:140).

A .git directory does not prove that its containing directory is the index's worktree root. Git honors core.worktree even in a conventional .git/config. For example H/repo/.git/config can select H/repo/subproject as the worktree, and its index can track .opensip/project-id.v1 there. If X2 selects subproject, the stated relative-path rule looks for subproject/.opensip/project-id.v1 and misses the tracked marker. This case uses a .git directory, not an already-refused gitdir indirection file.

**Required change.** Define and admit the supported Git layout before interpreting an index path. A conservative M2 profile may reject configured worktree relocation and other unsupported layout indirection on vcs-unsupported; it need not implement them. Read enough bounded, custody-checked repository configuration/layout evidence to establish the conventional worktree mapping, and retain/recheck that evidence. Do not infer the mapping from directory spelling. Likewise pin the supported index object-hash format or reject unsupported formats explicitly; index version 2/3/4 alone does not select SHA-1 versus SHA-256 field widths.

**Implementing-unit validation.** Add the core.worktree=subproject counterexample with an index entry at .opensip/project-id.v1. It must either be recognized as tracked or refuse as unsupported before registration/lease. Cover changed configuration and each selected index hash-format boundary without treating parse uncertainty as untracked.

Git documents that core.worktree can override the worktree root even when the configuration is in a .git subdirectory. Its index-format documentation separately defines hash-dependent object/checksum widths. The concrete lookup mismatch above is inferred from those documented rules and the proposal's path calculation. [Git configuration: core.worktree](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreworktree); [Git index format](https://git-scm.com/docs/index-format); [architecture:docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-registry-owner-selection-v2/owner.md:46).

**Nonblocking wording correction**

Line 174 says X3a-1's endpoint depends on X2e, while lines 160 and 207 put X2e after X3a-1. The substantive handoff is sound; the intended acyclic graph is X3a-1 endpoint plus X2d -> X2e -> N-bound binding/project writers. Change line 174 to refer to the N-bound binding or operation use, not production of X3a-1's endpoint. X3a also serves fenced observation readers before any project operation exists.

**Verification and limits**

- Read the r2 request and ran the requested unified diff against PROPOSAL-r1.md. Verified r1 against the prior reviewed hash and r2 against the request pin (24,117 bytes).
- Read the prior review, the registry and initial-root owners, S3/S7/S12 context, and the relevant product custody/admission code. The birth-sampler correction is retained.
- Product HEAD at final check: f7acb6d7f8acadcbc0bf81d141f39077d817f043. Product worktree status: clean.
- Read primary Git documentation for repository initialization, index insertion, configured worktree roots and index formats. The Git and self-publication counterexamples are static traces, not executed filesystem fixtures.
- A read-only ls -led probe showed omitted ACLs on the current checkout's .git, index and config. This is not a platform qualification claim.
- No Cargo, Git fixture creation, repository edits, commits, pushes or delegation. Only REVIEW.md and review.json were written in the requested output directory.
- This is law re-review. No implementation acceptance, successful native registration, crash-test result or real-host qualification is claimed.
