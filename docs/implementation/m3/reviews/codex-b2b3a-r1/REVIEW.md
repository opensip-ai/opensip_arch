# B2-b3a r1 review

Verdict: **REQUIRED-FINDINGS**. One correction is required before acceptance.

## Subject and boundaries

Independently verified the 11,083-byte manifest SHA-256 `1b53ae1a963d42b4c0c9864e8329d4f3a5f51be448574f89123cc0e37522229b` and all 48 members. All member lengths and hashes match. All 14 product-map rows match the candidate worktree, staged archive and recorded parent bytes; the complete worktree change set has no extra or missing paths. The worktree HEAD matches product base `3b3ab6e0e354c8f81e4ac030ed3102757be43085`; architecture HEAD matches `363303dc906030edd4e522ad5061fce87b42a3ca`. All nine source.json authority pins and the product design-lock pin match. The lock remains at inventory v192 and 164 contract successors, unchanged from base.

## B2B3A-R1-RF-1: Apply the accepted S3 file-custody rule before reading a gitdir target

Location: crates/security/src/custody/project_admission.rs:526-573; tools/security/discovery_upward_vectors.py:160-200; SCOPE.md LD-B2B3A-3.

gitdir_target checks no-follow identity, one link and size, but receives neither invoking uid nor ProjectChainPolicy and never checks owner, write mode or ACL. It therefore reads and records targets from files that fail S3 configuration-file custody. This is an explicit deviation from accepted PLAN-r2 LD-B2B3-7, which requires the gitdir value to be read under S3 file custody and gives an unavailable target null when custody cannot yield a target. S3:121-130 defines file custody as the directory ownership/mode/readable-ACL rules plus regular/one-link/4-MiB restrictions; the parenthetical bounds do not replace those rules. SCOPE LD-B2B3A-3 unilaterally removes those checks because the target is data, which is insufficient to implement the accepted plan.

The shipped vcs-git-file-foreign-acl-still-read vector has uid:1001 in aclWrite and still expects target /elsewhere. The generator constructs fs[directory].vcs.target with its own gitdir_target helper before calling the bound model. SLM _vcs_info trusts that supplied target and performs no native gitdir-file custody judgment. Regeneration succeeds, but cannot independently justify this adapter decision.

Required correction: Thread the invoking identity, authorized groups and receipt-backed custody policy into the VCS target capture. Apply the accepted S3 file-custody judgment on the retained no-follow descriptor before reading target bytes, with no project-owner waiver on the .git file. Preserve boundary presence and a null target when custody cannot yield a target, while keeping identity changes and budget exhaustion as whole-operation refusals. Update the description adapter, vector expectations and SCOPE, and add native controls for foreign owner, other/group write, untrusted ACL write and unreadable/unadmitted ACL, alongside admissible/authorized controls. If the intended behavior is instead to remove custody, obtain acceptance of that plan change before claiming this unit implements plan r2.

## Other review results

**Selection rows and refusal projection.** The recorded branches preserve the reference's candidate and custody rows, candidate-before-boundary precedence, explicit/config/VCS/home/root outcomes and mount back-patching onto the child. Config custody records REFUSED and names the config file; launch/explicit/depth refusals preserve their object path. Config custody maps to CONFIG.CUSTODY_REFUSED with CONFIG.INVALID D9. Host I/O, budget and unrelated admission variants retain their own outcomes. See the non-blocking note on the mapping helper's stage precondition.

**VCS and decisions.** Four-marker order is .git, .hg, .svn, .jj, stopping at the first present entry. Presence costs match the legacy absence probe. Directory and non-directory evidence is never followed. The opened regular .git descriptor is compared with ChildObservation::matches; changed/gone/wrong-kind entries refuse, and read/allocation exhaustion propagates as budget, rather than becoming a null target. LD-B2B3A-1/2/4/5/6/7 are reasonable refinements: four-marker evidence also applies at explicit/config roots; non-directory non-Git markers yield no target; the mount check precedes the next level's depth on the analysis path; X2 retains stricter no-link spelling; and retained-path bounds precede walk depth. The mount/depth branch has source/reference inspection but no native mount control, as disclosed. LD-B2B3A-3 requires the correction above.

**Legacy and shared custody order.** The unrecorded selection branches preserve legacy opens, positive-absence probes, judgment order and refusal behavior. The moved ordered judge retains the Shared branch unchanged, while the Reference branch preserves ACL-before-link/size behavior for discovery. The five archived B1B-LEGACY spend/outcome lines match exactly between base and candidate. Analysis-path extra evidence/record costs are explicitly separate.

**Waiver and lending.** applicable_waiver compares exact raw OsStr spellings. Selection applies it only to the explicit directory and opensip.json; the chain applies it to the leaf and records owner_waived. Recheck reapplies it only when originally admitted for that exact spelling. Ancestors, modes, ACLs, marker and local carrier remain unwaived. DiscoveryRoot exposes the retained root, spelling, premise and H-filesystem check; its private fields and two parent-visible lending constructors have only the specified production call sites. ProjectOperation selects the proper chain for Eligible and Registered subjects. ReadSession::release consumes the session, invokes InstallationObservation::release, drops other retained state and keeps only the receipt; latched/failed sessions cannot return ReleasedRead. The source and submitted release/lending controls support these properties.

**Vectors and materialization.** All 52 vectors regenerate exactly at the bound reference bytes; 17 identify original upward-only reference cases. The remaining two upward-only cases are accounted for by grant-construction and omitted-ACL controls. Native tests materialize mode bits, chmod +a grants, hard links, FIFOs and symlinks; uid/gid substitutions preserve foreign-owner and group-authorization relationships. Accepted selections compare their upward fields and roots; refusals compare rows, code, detail and path. This establishes reproducibility for the supplied observation adapter, not independent authority for its gitdir policy; that limitation is the required finding.

**Scope.** The diff contains selection/provenance, waiver/order plumbing, lending, test/vector support and existing caller signature adaptations. It adds no walker, listing, downward seam, production caller, public observation row, environment input or export. B2-b3b/c, the census and qualification remain outstanding.

## Checks and evidence

Independently ran only the permitted offline checks:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- Upward and scan vector --check commands: both passed at the accepted reference bytes.

The submitted, hash-pinned evidence reports:

- Security: the same 14 named failures at base and candidate, passing count 1086 to 1097. Host: the same 8 named failures, passing count 336 unchanged. The failure sets were compared directly; neither suite is wholly green.
- All-targets Clippy for opensip-host and opensip-security, locked/offline with -D warnings: exit 0, consistent with its completion log.
- Rustfmt: seven base-clean/new Rust paths pass. Five paths are classified dirty at both base and candidate and excluded; this is not an all-files formatting pass.
- Configuration-table check, verify_design and census: submitted exit-0 evidence. verify_design reports passed and selects v192; it was not rerun here.
- All 15 mutation logs contain failed-test summaries and the test names recorded by controls.json. Each mutation is caught in the submitted evidence. The lane-r1 extractor issue is explained and the lane-r2 five-line legacy comparison is consistent.

Rust tests, Cargo, rustc, Clippy, rustfmt, the lane and verify_design were not executed during this review. Those results are inspected evidence, distinct from the four checks independently rerun above.

## Non-blocking observations

- **B2B3A-R1-NBO-1**: gitdir_value strips a trailing CR even without a preceding LF; b"gitdir: /a\r" therefore yields /a. SCOPE specifies optional LF or CRLF. Align that description and parser policy and add a bare-CR vector; the Python adapter currently duplicates the same behavior.
- **B2B3A-R1-NBO-2**: discovery_refusal is safe only under its documented selection-refusal precondition. The same Chain(PathInvalid(NotFound/NotADirectory)) and Chain(Symlink) variants can also arise in the later chain walk, and the helper alone cannot distinguish them. Document and test the caller-stage guard (for example the selection record's refusal path), or carry explicit selection context before the future seam projects errors from the whole admission.

Only REVIEW.md and review.json were written. Neither repository, the candidate worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or held-out entries were accessed. No binding, integration, push, product qualification or completion of the entire plan is claimed.
