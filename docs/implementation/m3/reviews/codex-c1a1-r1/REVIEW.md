# C1a1 r1 review

**Verdict: REQUIRED-FINDINGS.** Four required findings and three non-blocking observations.

## Subject and review boundary

Manifest `docs/implementation/m3/snapshot-plan-c/c1a1-r1-subject.json`: 8,269 bytes, SHA-256 `914cc1bf7d6402f15c71e6aefda8759a84cad94d638cadb603cc91332d0b02e0`, 36 members. Every member was rehashed successfully. All six product-map rows match candidate and archived bytes; the existing lib.rs parent also matches. Main is clean at `808ad6476fb848f84e732ee233a47229370081f4`, candidate HEAD is the same base, and the candidate has only the six declared changed/new paths.

The review applies M3-C r8 items 1–2 and accepted C1a plan r4 as amended by r6. Under r6 this is preparatory library/model work, with no production caller, snapshot_profile, cap acceptance, closure transition or completed-snapshot claim. Findings below are source-analysis findings; no prohibited test or executable reproduction was run.

Only the two permitted checks were executed in the candidate: the snapshot model --check passed, and operability source returned passed=true, zero findings, 114 rows. No Cargo, rustc, build, lane, network, other-pane access, delegation, private fixture, installation, signing-key, held-tree or T2-cache/store access was performed. T2 census results below are archived evidence only.

## Required findings

### C1A1-R1-RF-1 (P2): The walk stats the forbidden .opensip anchor before pruning it

`crates/security/src/snapshot_walk.rs:332-346,214-216`

enter observes every converted child name with observe_child_accounted before walk_snapshot calls classify_path. Thus a root or admitted D15 member entry named .opensip is fstatat-ed on every walk, including CI. M3-C r8 item 1 explicitly says CI never stats, opens or lists that anchor. Pruning before open is insufficient. A disappearing or unstatable excluded anchor can also refuse the walk before pruning. The extent test checks that its contents are absent, not that the anchor was never observed.

**Required:** Use the shared rule to exclude the exact OpenSIP custody-state anchors before any child observation, preserving ordinary nested .opensip directories and name validation. Update the slot/observation handling and model to the resulting charges. Add an observation-level control for the project root and a D15 member in CI, including an excluded anchor that changes or cannot be observed.

### C1A1-R1-RF-2 (P2): An admitted boundary is enforced only when its current entry is a directory

`crates/security/src/snapshot_walk.rs:227-265; tools/security/snapshot_ledger_model.py:196-199`

is_boundary is called only in the Directory branch. If a nested-repository, nested-project, directory-custody or depth boundary admitted by B2 is replaced by a regular file before this walk lists it, the File branch opens and hands that exact excluded path to the visitor. The law excludes everything at or below an admitted boundary, independently of its current type. The model duplicates this omission, and the existing oracle cases keep boundary entries as directories.

**Required:** Apply admitted non-marker boundary exclusion independently of the observed entry kind, using the existing shared boundary API and preserving marker-custody exclusions as marker-specific. Update the model and add controls for a directory boundary replaced by a regular file, with equivalent excluded symlink/special-file handling.

### C1A1-R1-RF-3 (P2): The pre-walk opener does not judge the retained root directory

`crates/security/src/snapshot_source.rs:366-408`

SnapshotRoot::open judges only directories in dirs, after opening them. It never samples or judges self.retained(). For a root-level capture, dirs is empty and no directory custody is checked at all. If the admitted root becomes mode 0777, gains an unauthorized write ACL, or otherwise fails S3 after lending, this opener still returns the source descriptor; walk_snapshot, by contrast, samples and judges the root before listing. The accepted pre-walk opening rule requires a custody-judged directory chain before capture, not a later walk refusal after the source has already been read.

**Required:** Charge, sample and judge the retained root under the same S3 directory policy before any pre-walk traversal/open, or provide an equivalent current, enforced custody proof. Retain terminal refusal and directory-only waiver semantics. Cover root-level and nested captures after root mode/ACL custody changes between admission/lending and open.

### C1A1-R1-RF-4 (P2): Native path and boundary copies are outside the charge recipe

`crates/security/src/snapshot_walk.rs:169,204-214,229,257-260; crates/security/src/discovery_export.rs:218-241; tools/security/snapshot_ledger_model.py:175-201`

The new walk allocates parent_rel via top.rel.clone() and name via to_owned() for each entry before any charge for those copies, and creates root_abs without a charge. The listing conversion explicitly prices only its own path and validator copies; classify_cost describes the shared classifier's temporaries, not these additional strings. Further, the invoked AdmittedBoundaries::boundary_hit calls custody(), which allocates and clones every custody row on each lookup, without a corresponding row-dependent charge. The model mirrors the explicit ledger calls, so native <= model cannot expose these shared omissions. Item 2 and the accepted pricing recipe require every copy to be charged before it happens.

**Required:** Eliminate avoidable copies with borrowed path/name views and a non-copying shared boundary lookup, or charge their full owned records and byte volumes before allocation and mirror those charges in the model. Account for root spelling as well. Add controls involving deep/long paths and multiple custody-boundary rows; verify that accounting is justified independently of equality between two counters that omit the same work.

## Other requested assessments

- **Extent and custody:** the walk calls discovery_rule::classify_path, uses AdmittedBoundaries, validates ignorePaths, and reuses unchanged ListingConversion. It maintains Cargo roots from regular Cargo.toml observations and removes them when leaving their frame. Marker-custody rows exclude the matching marker through the existing boundary API. Every entered child directory and every reached marker uses judge_entry with metadata-first refusal, descriptor ACL capture and omission-premise handling; a failure refuses rather than silently skipping. The directory waiver does not reach markers. Symlinks and special files are reported and not opened. No retry loop was introduced. RF-1 and RF-2 qualify exclusion fidelity; RF-3 qualifies the pre-walk custody chain.
- **Enumeration binding:** each frame owns its retained directory. Child observations and opens use that same retained parent; directory matches and regular-file same_object checks compare device/inode/kind. Ancestor path replacement after entry cannot redirect the retained traversal. SourceFile carries the enumeration-time full metadata for the later capture-session comparison. The pre-walk swap tests establish the opener/walk identity distinction; C1a2 still owns the full observation comparison and one-read control.
- **Roots and reads:** production SnapshotRoot construction is limited to ProjectOperation and the crate-internal ReleasedRead/admission route; for_tests and the swap hook are test-only. Borrowed roots retain the lawful lending lifetime. The two new non-test security modules open/observe descriptors and capture metadata/ACLs but never read source content. The visitor read exists only in the separate test module. This leaves the planned C1a2 source pin and sole host read site possible, without claiming they already exist.
- **Model:** it imports discovery_census.py unchanged, obtains the reference rule/vector interpretation and anchored cost/size closure there, and pins both new snapshot modules whole plus their own charge shapes. The abstract charge sequence matches the explicit native calls for the current cases; its ACL dearer-branch capture bounds either native branch. RF-4 concerns omitted native charges, and RF-1/RF-2 require model updates with their code fixes. The three regenerated undercount mutants genuinely fail the native upper-bound control. Thirty-two finite controls do not prove soundness for every tree or catch costs omitted on both sides.
- **Recorded lane:** base and candidate have identical sets of 14 security test failures, no differing failures, and the same two suites. Total passes are 1,167 versus 1,179: 12 additional tests. The lib suites each have seven ignored tests. This is an equal-failure-set result, not an all-green security suite. The focused snapshot suite has 12 passes. Its oracle asserts 28 exact matches and zero custody refusals; its model test checks all 32 trees.
- **Other archived checks:** warning-denied all-targets Clippy passes; the three new Rust files are rustfmt-clean, while existing lib.rs is classified dirty at both base and candidate and excluded under the recorded policy. Model --check, T2 discovery census --check, operability, closure-unchanged and verify_design all record success. verify_design selects inventory v212 and 173 contract successors. All eight walk mutation logs contain actual failed tests without compilation errors; all three model mutation logs show the over-the-model assertion after vector regeneration.
- **Closure and rules:** independently rehashed all 19 census-closure files and compared each with Git base; none changed. The census tool itself also matches base, so this candidate does not stale the blind receipt through a closure change. No new forbidden from/into/pid/line/issue call or environment read was found in non-test Rust. Test-only environment use remains separate. No Linux build or qualification is claimed.
- **Inventory:** the five new paths are snapshot_source.rs, snapshot_walk.rs, snapshot_walk_tests.rs and snapshot_ledger_vectors.json under crates/security/src, plus tools/security/snapshot_ledger_model.py. Existing crates/security/src/lib.rs is the sixth product-map row. An inventory successor remains subsequent work.

## Non-blocking observations

### C1A1-R1-NBO-1: Route controls may move to C1a2 with an explicit remaining obligation

The C1A-T2/T3 deferral is acceptable for this r6 preparatory unit: the constructors are thin wrappers over the existing lawful lendings, the released-read constructor remains crate-internal, and no production caller or snapshot profile is added. C1a2 must retain both the same-tree durable/released-read inventory comparison and the no-lease/no-fence released-read control, with its scenario helper, before production use. Current for_tests roots do not discharge those controls.

### C1A1-R1-NBO-2: The soundness test establishes an upper bound, not an asserted exact equality

The 32-case native test asserts used <= predicted componentwise; it neither asserts equality nor prints the 32 native/predicted triples in the normal lane log. The dearer-branch formula is conservatively sound for ACL captures (CAP plus componentwise max of the bounded ACL-entry copy and filesystem-premise costs). Exact agreement on the present APFS branches may follow from those formulas, but the blanket statement that any undercount fails is stronger than this test guarantees. Preserve the upper-bound assertion for conservative branches; explicitly assert or record equality on designated exact controls and describe the three mutants as evidence for the terms they remove.

### C1A1-R1-NBO-3: Scope and source metadata need a status refresh

SCOPE.md still calls plan r6 in review, although the request identifies it as accepted and published. source.json says publicApiAdded=false despite two new public modules and public types/functions. The runner also retains a serial-platform/attempt-3 comment although its security command has no serial argument. These stale descriptions do not change the pinned bytes or the actual checks reviewed here.
