# B2-b3b r2 review

Verdict: **REQUIRED-FINDINGS**. Three corrections remain.

## Exact subject

Independently rehashed the 11,599-byte manifest to SHA-256 `512d8a4cebd559d9a875b042f97f8feb916a5498397463e4b0b3cf3a676b9cb4`. All 51 members match their declared bytes and hashes. All ten product-map rows match candidate worktree, staged archive and recorded parent bytes, and equal the complete worktree change set. All ten authority pins and the product-lock pin match.

Candidate HEAD is base product `f3384b59a0d6487975dc2655bca0dbab23d4f03c`; architecture HEAD is `c1690efbe14b1502b2c080f222117569064031e7`. Inventory v193 and 164 contract successors are unchanged.

## B2B3B-R2-RF-1: Preserve pruning-before-custody when a pruned prefix is not a directory

Location: discovery_walk.rs:837-850 and named_root Chain::NotDirectory judgment.

The main RF-1 gating is implemented, but named_root tests the component kind before classify_path. A file or absent component named node_modules therefore sets Chain::NotDirectory, and the function custody-judges/captures earlier chain directories. The core checks whether the complete join is inside a pruned tree before any unit custody. For a directory a, file a/node_modules, and join a/node_modules/x, the bound current reference refuses JOIN_INSIDE_PRUNED_TREE:dependency-tree:a/node_modules for both explicit and config sources; the walker first captures a unnecessarily. Capture failure/exhaustion can mask that pruning refusal.

Required correction: Determine the same crossing/pruning precedence as the core before starting custody, including non-directory or absent pruned prefixes. Preserve the reference observation population. Add both-source controls for a/node_modules/x with node_modules a file and absent, asserting the expected refusal and no ACL captures, plus a tight-budget/control that would expose an unnecessary ancestor capture.

## B2B3B-R2-RF-2: Finish the owned-storage precharge correction

Location: discovery_walk.rs:230-255, 626-639 and 750-751.

RF-3 is substantially improved, but not every allocation is charged before it occurs. subtree clones the owned name and potentially 4096-scalar relative path at line 750 before its later frame charge, and even does so for pruned children for which that later charge never happens. listed_name also calls LogicalPath::parse on an already owned relative path; parse constructs another String on success (identity/descriptors.rs), while list prices only the returned name and relative path, not this additional full-path copy. A fixed 128-byte RECORD allowance cannot cover an arbitrarily longer path copy. The new marginal-cost controls use wide sets of files and absent single-component specs, so they do not exercise the directory tuple clone or account for the validator copy.

Required correction: Borrow or move existing name/path values where possible; otherwise charge each owned copy before cloning, including copies on pruned paths. Validate without an allocating LogicalPath constructor or explicitly price its temporary full-path allocation before parsing. Extend the cost controls to long/deep directory children (ordinary and pruned), and a low remaining byte budget that refuses before the copy rather than after it. Update the stated storage model and mutation coverage.

## B2B3B-R2-RF-3: Apply the depth policy to a named subtree start

Location: discovery_walk.rs enter:649-676, subtree:722-733 and named_root:915-920.

subtree calls enter for its initial frame, and enter lists it unconditionally. The depth guard is only applied to children of an existing level. An explicit/config named root already deeper than 256 segments is therefore listed, including arbitrary files and child directories. The bound walker_population checks depth at the beginning of every subtree iteration, including a named start: above 256 it observes only the four workspace marker names and does not list. A 257-segment named root fits the 4096-scalar join grammar. In a synthetic reference population, its package.json is retained and its unlisted.txt is absent; this implementation lists and includes both. It can also refuse on an invalid arbitrary child name or spend on children the oracle never observes.

Required correction: Handle an over-depth initial named subtree with marker-only observation and no listing/descent, preserving the separate parent-first chain observations required by the reference. Add explicit-joins and config-workspace-roots vectors/native trace controls at depths 256 and 257 (and a deeper admissible named path), with marker and arbitrary children, and compare the exact population/evidence to the bound oracle.

## Prior findings and observations

Prior RF-1 is substantially corrected: the core and walker share judge_entry, metadata rejection leaves NotObserved, capture occurs on NeedsAcl, directory verdicts are memoized, rejected ancestors stop marker capture, and explicit join judgment stops at the first refusal. New mode/owner, ancestor-ACL and crossing/later-join controls exercise the principal cases. The non-directory/absent pruned-prefix case above prevents declaring it fully resolved.

Prior RF-2 is resolved. Repeated present observations are compared with the stored device/inode/kind, and disappearance refuses. The revised shared-prefix control swaps between visits rather than at the second open, for both explicit and config sources; revisit-identity-unchecked is caught. New descriptors cannot silently reuse custody from a different inode in the reviewed path.

Prior RF-3 is substantially corrected by owned record/path charges, the RECORD allowance, scope/observed/frame/verdict/spec/ACL accounting and removal of per-directory Cargo-set copies. The remaining allocations identified above prevent full resolution. The exact marginal-cost tests catch the charged-copy mutations, but do not independently establish complete preallocation pricing.

All three prior NBOs are addressed: the count is corrected to 44; VCS helpers trace individual by-name observations, gitdir open/capture/read through test-only trace_child; and descriptor accounting distinguishes named chains from subtree descent. The trace control asserts that an external gitdir target is not followed. Named-chain descriptors are dropped before descending its subtree.

The iterative level stack preserves ordinary depth-first name order, parent-first Cargo-root knowledge, and Cargo-root insertion/removal on level entry/exit. It removes recursive stack dependence. Its initial-level depth omission needs the third correction above; therefore the conversion is not yet faithful for every admitted named root.

## Other implementation review

The stable-tree vectors exercise pruning, nested VCS/project boundaries, automatic depth handling, explicit/config populations, custody inputs and downward result/inventory comparison. The adapter continues to delegate gitdir custody to the bound model. Name validation and refusal escaping remain correct, and returned OS names are charged before copying, with exactly dot and dot-dot discarded. Listing streams close before child traversal, and listing ceilings propagate as a bound rather than truncation. Complete owned-storage accounting is still outstanding.

Shared judge_entry preserves reference refusal order and the NeedsAcl instrument distinction. discover_observed returns UnobservedAcl when the core reaches an uncaptured ACL; discover keeps its accepted signature. Nonregular markers and markers rejected by metadata are not opened. Captures preserve premise-applied normalization and identity comparison. The two gitdir full-metadata race controls and their mutations remain present. Boundary probing does not list the boundary's interior. The six lead decisions remain reasonable; the required findings concern their implementation and control completeness.

FW-01 covers configuration.rs, discovery rule/core/walker and grants with production include closure, excluding test-only code, and catches process/socket/write/publication negatives. Production trace_child builds no path outside tests. The new shared walker request waiver and existing tests' VCS helper argument adaptations add no production caller, host discovery seam, environment read or export. Discovery refusal mapping remains limited to NAME_UNREPRESENTABLE.

## Independently run checks and inspected evidence

Only the expressly permitted checks were run:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- FW-01 structural pin: 7 tests passed.
- Walk, scan and upward vector --check: all passed; the walker output contains 44 vectors.

Also imported only the bound reference read-only over synthetic inputs. For both explicit sources it confirms that the non-directory node_modules join refuses as JOIN_INSIDE_PRUNED_TREE before unit custody, and a 257-segment named subtree retains a workspace marker while excluding an arbitrary child. No native filesystem fixtures or Rust execution were used for these additional checks; implementation behavior was established by source inspection.

The hash-pinned lane-r3 evidence is internally consistent:

- Security has the same 14 named failures at base and candidate, with passes 1098 to 1115. Host has the same 8 failures and 336 passes. These are equal baseline failure sets, not wholly green suites.
- Five legacy admission spend/outcome lines match exactly.
- Locked/offline all-targets Clippy for opensip-host and opensip-security with -D warnings reports exit 0 and a matching completion log.
- Rustfmt passes for five base-clean/new Rust paths; project_admission.rs and project_chain.rs remain explicitly base-dirty/candidate-dirty and excluded.
- Configuration tables, census and verify_design evidence report success; the design record selects v193 and claims no qualification.
- All 20 mutation logs have failing-test summaries containing the tests named by controls.json. Lane-r2's unsuccessful mutation attempts are disclosed as historical; the current lane-r3 catches all 20.

Cargo, rustc, Rust tests, builds, Clippy, rustfmt, the lane and verify_design were not executed by this review. Those results are inspected evidence, separate from the six permitted checks rerun above.

Only REVIEW.md and review.json were written. Neither repository, worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed. No binding, integration, push, product qualification or entire-plan completion is claimed. B2-b3c, inventory succession, B2-b4/T2 margin and later owning units remain outstanding.
