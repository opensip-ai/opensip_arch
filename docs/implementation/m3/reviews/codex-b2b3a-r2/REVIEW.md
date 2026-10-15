# B2-b3a r2 review

Verdict: **ACCEPT-UNIT**. The prior required finding and both non-blocking observations are addressed. No required findings remain.

## Exact subject

Independently rehashed the subject manifest: 11,548 bytes, SHA-256 `09ae5866624d25a621e919be186121a03bd4307ff28ca37905438ad887ec6af1`. All 50 members match their declared lengths and hashes. All 14 product-map rows match the staged archive, candidate worktree and recorded parent bytes. The complete candidate worktree change set equals the map, with no extra or missing paths.

The candidate HEAD is product base `3b3ab6e0e354c8f81e4ac030ed3102757be43085`; architecture HEAD is `363303dc906030edd4e522ad5061fce87b42a3ca`. All nine source.json authority pins and the product-lock pin match. The unchanged lock selects inventory v192 and contains 164 contract successors. Relative to reviewed r1, only project_admission.rs, its upward tests, the generated upward vectors and their generator changed.

## Prior review disposition

**B2B3A-R1-RF-1 is resolved.** gitdir_target now receives the invoking uid and ProjectChainPolicy. After opening the regular .git file no-follow and matching its observed identity, it calls judge_project_object_ordered with ConfigurationFile, Reference order and no owner waiver. The existing judge applies owner, other/group write and ACL policy, receipt-backed omission premise, link count and size in reference order. Ordinary custody refusals and unadmitted ACL omission preserve the VCS boundary with a null target; capture/host failures and budget failures propagate. Successful judgment must match the opened full metadata, and the same retained descriptor is read and sampled again before any target is accepted. Changed identity and oversize growth refuse rather than becoming an unavailable target.

The vector adapter now delegates file custody to the bound model's _file_custody with the invoking uid, authorized groups and waiver false. It decides only line grammar and observational representation. The former ACL-writable-target vector is inverted. New vectors cover untrusted user/group ACL grants, other/group write, an authorized writable group, owner-only mode and a foreign explicit root whose .git file is not waived. Native direct controls cover foreign ownership and omitted ACL without an admitting premise. These corrections implement accepted plan r2 LD-B2B3-7; LD-B2B3A-3 is explicitly withdrawn.

**NBO-1 is addressed.** Rust and Python strip only LF or CRLF; a bare CR remains invalid. A bare-CR vector and a caught parser mutation cover the distinction.

**NBO-2 is addressed.** The public crate-local projection is now UpwardRecord::discovery_refusal, which requires a selection-named object and returns that path with code/detail. The variant mapper is private. Successful selection clears its pre-open refusal path; later chain/carrier/marker failures therefore cannot be projected merely because they reuse a selection variant. The new control covers synthetic overlapping variants and a real post-selection OutsideHome failure; the guard-removal mutation is caught.

## Remaining review dimensions

The upward selection retains reference row order, candidates, custody boundaries, mount-on-child recording, stop reason, mode, configPath and named refusal semantics. Config custody has its proper discovery code and D9. X2's stricter refusal of symlinked spellings and retained-path bound remain explicit. Four-marker probing is ordered and charged, including config/explicit roots; directory evidence and unavailable indirections are never followed. The remaining lead decisions are within the accepted plan. Mount-before-depth has source/reference verification and no native mount control, as disclosed.

The unrecorded legacy branches remain unchanged in opens, probe order, charges and refusal order. The moved pure ordered judge retains its Shared behavior; discovery uses the Reference order. All five legacy spend/outcome lines are byte-for-byte equal at base and candidate. The corrected .git custody adds costs only on the recorded analysis path.

The owner waiver remains typed and exact-spelling-bound. It reaches the explicit root and its opensip.json, then the chain leaf and its required recheck; owner_waived gates reapplication. It reaches no ancestor, marker, local carrier, mode or ACL check, and no .git target custody judgment. Lending and read release are unchanged from r1: DiscoveryRoot exposes only the retained root, spelling, premise and H-filesystem check; its two restricted lending constructors are used by ReleasedRead and ProjectOperation. ReadSession::release consumes the session, frees the fence and installation handles, keeps only the receipt and returns no lending on latch/failure. ProjectOperation chooses the appropriate Eligible or Registered subject chain.

The 59 vectors (35 accepted, 24 refused; 17 original reference cases) reproduce exactly at the bound reference bytes. Native materialization preserves modes, ACL grants, hardlinks, FIFOs, symlinks and the relationships represented by foreign uid and authorized-group substitutions. The two other upward-only cases remain covered by grant-construction and omitted-ACL controls. The new custody adapter and controls close the r1 gap without changing the current reference.

The paths remain exactly the product map's. No walker, listing, downward seam, production caller, public row, environment read or export is added. The existing scenario seam only adapts its analysis call signatures. B2-b3b/c, T2 census, inventory succession and qualification remain separate.

## Verification and evidence

Independently ran the four permitted offline checks in the candidate worktree:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- Upward vector --check: passed.
- Discovery scan vector --check: passed.

Inspected the pinned lane-r4 evidence and checked its internal consistency:

- Security failure sets are identical: 14 named failures at both base and candidate; passing tests increase from 1086 to 1098. Host failure sets are identical: 8 named failures, with 336 passes at both. This is equal baseline failure evidence, not wholly green suites.
- All-targets, locked/offline Clippy for opensip-host and opensip-security with -D warnings reports exit 0 and a matching completion log.
- Rustfmt passes for seven base-clean/new Rust paths. Five edited paths are explicitly base-dirty and candidate-dirty and excluded from that check; no all-files formatting pass is claimed.
- Configuration-table, source census and verify_design evidence report success; verify_design selects v192 and productQualification false.
- All 17 mutation logs have failing-test summaries and include the failed test names recorded in controls.json. The new custody, bare-CR and stage-guard mutations are caught. Retiring the former separate hard-link mutation is reasonable because custody now owns that bound and the retained hard-link vector plus custody-bypass mutation exercise it.

Cargo, rustc, Rust tests, builds, lane, Clippy, rustfmt and verify_design were not executed during this review. Their results above are inspected submitted evidence; only the four expressly permitted checks were rerun.

## Non-blocking observation

**B2B3A-R2-NBO-1:** The new opened-versus-judged and post-read full-metadata comparisons are present and correct on the successful capture path. A future focused race control or mutation for each comparison would strengthen the existing different-inode and budget controls, which do not independently exercise those two comparisons.

Only REVIEW.md and review.json were written. Neither repository, the candidate worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed. This accepts the unit's exact submitted bytes; it does not bind or integrate them, push anything, qualify the product or complete the entire plan.
