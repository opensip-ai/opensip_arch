# B2-b3b r3 review

Verdict: **ACCEPT-UNIT**. The prior required findings and observations are addressed. No required findings or non-blocking observations remain.

## Exact subject

Independently verified the 12,297-byte subject manifest SHA-256 `0a85b70b3985e346ba984b37857cb6d7fb2ed65501a79985ef9466769c78e9d2` and all 54 members. Every member matches its declared length and hash. The ten product-map paths match the staged archive, candidate worktree and parent bytes, and equal the complete worktree change set. All ten source authority pins and the product-lock pin match.

Candidate HEAD is product base `f3384b59a0d6487975dc2655bca0dbab23d4f03c`; architecture HEAD is `c1690efbe14b1502b2c080f222117569064031e7`. The unchanged lock selects inventory v193 and 164 contract successors. Relative to r2, only the walker, its tests, its vectors and their generator changed.

## Round-2 findings

**B2B3B-R2-RF-1 is resolved.** named_root classifies the complete join before starting custody, even when its observed chain ended at a non-directory or absent component. The classification uses the chain's known Cargo roots. Crossing/pruning refusals therefore precede custody as in the core. Four new vectors cover a/node_modules/x with the prefix a file or absent through both explicit sources. Their oracle controls assert no captures on a join refused before custody, and pruned-join-custody-judged is caught.

**B2B3B-R2-RF-2 is resolved.** A visited child's owned name and relative path move out of the level with mem::take rather than being cloned, including on the pruning branch. The listing precharge prices the returned name, relative path and LogicalPath validator's additional path copy. classify_cost precharges the shared rule's segment/prefix/anchor temporaries. Root spelling copies are charged before cloning, and the unnecessary named-root marker spelling clone is removed. The RECORD allowance remains a conservative storage allowance rather than an allocator/RSS measurement. The explicitly documented terminal refusal-record allocation does not permit continuing uncharged traversal or replace the original refusal with an error-reporting budget failure.

The revised marginal-cost controls cover long prefixes with ordinary files, ordinary directory children and pruned directory children, plus explicit specs. They distinguish the validator/classifier costs and caught mutations remove the relevant charges. Combined with source inspection of the moved ownership and charge ordering, these address the previous missing-copy cases.

**B2B3B-R2-RF-3 is resolved.** subtree checks its initial frame's relative depth before enter/list. Above 256 it observes only the four workspace marker names and returns; the separate parent-first chain observations remain intact. New oracle vectors cover explicit depth 256, 257 and 260, and config depth 257, with markers and arbitrary children. The focused native trace control checks both sources at 257 and excludes the arbitrary child. named-start-listed is caught.

## Round-1 resolutions and implementation

The earlier corrections remain intact. Core and walker share judge_entry with Passed, Refused and NeedsAcl results. Metadata-only refusal requires no ACL capture; directory verdicts are memoized, chain custody stops at its first refusal, and markers are judged/captured only after a passing chain. Nonregular or metadata-rejected markers are not opened. Explicit joins are judged in order, with later population observation kept separate from stopped custody judgment.

Repeated observations must retain the stored device/inode/kind and remain present; otherwise Changed refuses. The shared-prefix replacement controls cover both explicit joins and config roots, preserving the r1 identity correction. Opened directories and markers are compared with their observations; no retry path is added. Captured ACLs normalize readable entries, premise-admitted omission and unreadable state. NotObserved remains an honest state, with an ACL-dependent core judgment yielding UnobservedAcl through discover_observed; discover keeps its accepted signature for fully captured input.

The level stack preserves the reference's parent-first observations and depth-first child order without recursive stack dependence. Cargo roots are inserted and removed with their level. Source selection precedes traversal, exact explicit/config populations stay restricted to named chains/subtrees, pruning precedes boundary entry, ordinary nested boundaries are probed and never listed, and automatic depth-257 directories receive marker-only observations. Name handling charges OS names, discards exactly dot and dot-dot, enforces platform components and complete LogicalPath limits, and preserves the NAME_UNREPRESENTABLE refusal/detail.

Listing syscall/name costs and owned storage use the caller's original ledger; hard listing ceilings refuse as a bound, streams close before descent, and exhaustion returns no partial scope. Descriptor accounting separates bounded subtree levels from potentially longer named chains, which are dropped before their subtree starts. EMFILE remains host I/O. The six lead decisions remain sound within accepted plan r2.

All prior observations are addressed: the r3 count is 52, with historical r2 count corrections clearly retained as history; VCS helpers now trace their individual observations/open/capture/read through test-only trace_child; and named-chain descriptor accounting is separate. Both gitdir full-metadata race controls and their comparison-removal mutations remain present.

FW-01 covers configuration.rs, the shared rule, core, walker and grants plus production include closure. Its negatives exercise process, socket, filesystem write and platform publication names. Test scope remains excluded. The native tree cross-check preserves the explicit uncaptured-ACL projection and directory/file/FIFO mode comparisons. The description adapter takes gitdir custody from the bound model, and native materialization preserves modes, ACL grants, hard links, FIFO/socket/symlink kinds and foreign uid/group relationships.

## Verification and evidence

Independently ran only the six permitted offline checks:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- FW-01 structural pin: 7 tests passed.
- Walk, scan and upward vector --check: all passed. The walker output contains 52 vectors at the bound reference bytes.

Inspected the pinned lane-r4 evidence and checked its consistency:

- Security has identical 14 named baseline/candidate failures; passes increase from 1098 to 1117. Host has identical 8 failures and 336 passes. Equal baseline failure sets do not mean wholly green suites.
- All five legacy admission spend/outcome lines match exactly.
- Locked/offline all-targets Clippy for opensip-host and opensip-security with -D warnings reports exit 0 and a completion log.
- Rustfmt passes on five base-clean/new Rust paths; project_admission.rs and project_chain.rs remain explicitly base-dirty/candidate-dirty and excluded.
- Configuration-table, census and verify_design evidence report success. The design evidence selects v193 and claims no qualification.
- All 23 mutation logs contain failing-test summaries and the test names listed in controls.json. The new pruning-order, initial-depth and classification-charge controls are caught alongside retained identity/custody/race controls.

Cargo, rustc, Rust tests, builds, Clippy, rustfmt, verify_design and the lane were not executed during this review. Those results are inspected submitted evidence, distinct from the six expressly permitted checks rerun above.

## Scope and limits

The exact diff adds the internal walker, its tests/vectors/tool and FW-01 pin, the shared custody observation support and specified test-only hooks/signature adaptations. It adds no production caller, host discovery seam/flag rows, environment read or export. Discovery refusal mapping remains limited to NAME_UNREPRESENTABLE. Acceptance does not complete B2-b3c, the inventory successor, B2-b4/T2 margin gate, later readers/members or qualification.

Only REVIEW.md and review.json were written. Neither repository, worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed. No binding, integration, push, product qualification or entire-plan completion is claimed.
