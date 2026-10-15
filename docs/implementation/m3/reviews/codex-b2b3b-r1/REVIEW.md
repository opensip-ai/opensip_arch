# B2-b3b r1 review

Verdict: **REQUIRED-FINDINGS**. Three corrections are required.

## Subject identity

The subject manifest is 10,192 bytes with SHA-256 `1501f8a3eb6838434aa1ea73055e891fe555f6ad56cf51a6b57acdb42b7c0afd`. All 45 members independently match their lengths and hashes. The nine product-map paths match the staged archive, worktree and recorded parent bytes, and equal the complete worktree change set. All ten authority pins and the product-lock pin match.

Candidate HEAD is product base `f3384b59a0d6487975dc2655bca0dbab23d4f03c`; architecture HEAD is `c1690efbe14b1502b2c080f222117569064031e7`. The unchanged lock selects inventory v193 and 164 contract successors. No closed predecessor implementation is reopened here except the specified walker changes and gitdir race controls.

## B2B3B-R1-RF-1: Gate ACL capture by the judgment actually reached

Location: discovery_walk.rs:335-384, 571-578, 718-745 and explicit-root capture in walk.

capture unconditionally calls capture_descriptor_acl_accounted for any NotObserved entry. Automatic candidates capture every ancestor and every regular marker even when an earlier directory fails custody; named chains likewise capture metadata-rejected directories and boundary directories before returning. There is no kind/owner/mode early-rejection gate in capture and no custody-result gate before capturing later chain entries or markers. Thus a 0777 unit directory still gets an ACL capture and its marker gets opened/captured even though the core stops at DIRECTORY_CUSTODY. This contradicts LD-B2B3-3/6 and the claimed only-where-judgment-reaches-ACL behavior. Unnecessary capture can exhaust the ledger or fail host I/O before the core returns its otherwise available exclusion/crossing refusal.

Required correction: Share the reference-order metadata-only gate with the walker, preserve NotObserved for early rejection, and memoize chain custody outcomes so later ACL/marker captures occur only if the core would reach them. Preserve the reference population and required non-custody boundary observations. Add trace and tight-budget controls for mode/owner rejection, ACL rejection on an ancestor, and a crossing that must not trigger unrelated custody capture.

## B2B3B-R1-RF-2: Reject identity changes when overlapping named roots revisit a path

Location: discovery_walk.rs:276-291, 335-343 and 678-747.

observe performs a fresh status read but or_insert_with silently retains any earlier scope entry. named_root starts a new descriptor chain for each distinct requested root, so shared prefixes are reopened. open_directory matches only the new observation; capture then returns immediately if that path already has a captured ACL. For roots a/u and a/v, replacing a between walks can therefore open the replacement while retaining the original a metadata/ACL in the core scope. A new mode/owner on the replacement can be hidden by cached custody. The before-open hook can replace a and move its existing children into the new directory while preserving child inode identities; the current one-root swap controls do not exercise this window.

Required correction: Keep retained shared-prefix descriptors/observations for the invocation or compare every repeated observation/open against the original admitted identity before reusing cached custody. Refuse a previously present path becoming absent or changing identity; never mix a new descriptor with an old captured entry. Add both explicit-joins and config-workspace-roots controls with shared/overlapping roots and a same-kind prefix replacement between visits, asserting Changed and no accepted mixed scope.

## B2B3B-R1-RF-3: Account for owned paths and collection storage before allocation

Location: discovery_walk.rs listed_name, observe, list, subtree, named_root and walk.

The listing charges one copy of each raw name, but subsequently allocates name strings, full relative paths, LogicalPath copies, absolute paths, BTreeMap keys, observed vectors and listed/seen/cargo/frame collections without corresponding owned-storage charges. observe allocates abs.to_owned and inserts an ObservedEntry after only the platform status-read charge; list retains the raw bytes while building additional path copies. The fixed 1024 listing allowance does not bound this storage. Deep parents with many short child names amplify full-path storage far beyond the charged raw-name bytes. This undermines the claimed one-ledger precharge and the byte/object bounds; the current one-short tests merely measure the same incomplete cost model.

Required correction: Define conservative costs for the actual owned records, path copies and collection growth, and charge the original discovery ledger before allocating them, or restructure ownership to eliminate copies with an explicit bounded storage allowance. Keep listing syscall/name costs separate from retained-scope costs. Include tight-byte/object-budget controls for wide directories under long/deep prefixes and explicit-root collections, demonstrating refusal before the uncharged allocation would occur. Update the scope/census cost description accordingly.

## Other review results

For a stable supplied tree, the traversal and population projection agree with the bound walker_population design: source chosen first, depth-first ordinary traversal, Cargo roots discovered before classifying children, pruning before boundary probing, boundaries probed and not listed, and depth 257 restricted to four workspace marker names. Explicit/config chains run parent-first and restrict listing to the named subtrees. populationMatchesReference describes that stable-tree population behavior; it does not excuse the repeated-identity flaw above.

Name handling charges returned OS names, discards exactly dot and dot-dot, checks the platform component grammar and complete root-relative LogicalPath, and refuses with the existing discovery code and escaped name detail. The byte-copy accounting after that first charge needs RF-3's correction. The listing syscall allowance and per-name charge are present, hard ceilings produce ListingBound, native errors remain HostIo, and streams close before descent. Exhaustion propagates rather than returning a partial scope, but its current storage price is incomplete.

The new core NotObserved branch performs metadata-only early rejection in reference order. An ACL-dependent judgment records UnobservedAcl, and discover_observed returns the instrument fault rather than a public result; discover retains its old signature for fully captured vectors. Normalized captures preserve readable ACL entries, premise-admitted omission and unreadable state. Nonregular markers are never opened by the marker-capture loop. The walker must still gate regular-marker and chain captures as RF-1 requires.

The FW-01 structural pin covers configuration.rs, the rule, core, walker and grants plus their production include closure. It excludes test scope and detects planted process, socket, write and platform-publication names. Its seven checks pass. This is a lexical structural pin, not transitive Rust call-graph verification.

Both gitdir full-metadata comparison follow-ups are implemented with test-only hooks at Opened and Judged. Their native race controls mutate the same file, and separate comparison-removal mutations are caught. The remaining lead decisions—listed-name disappearance refusal, identity comparison with capture metadata standing, listed-root VCS evidence, no automatic-root capture, escaping and test-only seams—are reasonable within plan r2. Their implementation remains subject to the required fixes.

## Vectors, controls and evidence

All three vector tools reproduce their checked-in bytes at the bound reference pins. The walker file actually contains **44** vectors; see NBO-1. Its adapter takes gitdir custody from the bound model's _file_custody without waiver. Native materialization handles modes, chmod +a grants, hard links, FIFOs, sockets, symlinks and foreign uid/group relationships. The population/evidence and downward-record comparisons use an explicit uncaptured-ACL projection, with directory/file/FIFO mode comparisons. Those static comparisons do not establish capture minimality, repeated-path identity stability or complete allocation accounting.

Independently ran only the permitted offline checks:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- FW-01 structural pin: 7 tests passed.
- Walk, scan and upward vector --check: all passed.

Inspected the pinned lane evidence:

- Security: identical 14 named baseline/candidate failures; passes 1098 to 1109. Host: identical 8 failures and 336 passes. Neither suite is wholly green.
- Five legacy admission spend/outcome lines match exactly.
- Locked/offline all-targets Clippy for opensip-host and opensip-security with -D warnings reports exit 0 and a matching completion log.
- Rustfmt passes on the four base-clean/new Rust paths. project_admission.rs and project_chain.rs are explicitly base-dirty and candidate-dirty and excluded.
- Configuration tables, census and verify_design report success; the design evidence selects v193 and claims no qualification.
- All 15 mutation logs contain failing-test summaries and the failed test names listed in controls.json. Their reported catches are consistent.

Cargo, rustc, Rust tests, builds, Clippy, rustfmt, verify_design and the lane were not executed during this review. Those results are submitted evidence, distinct from the six permitted checks independently rerun above.

## Non-blocking observations

- **B2B3B-R1-NBO-1**: The pinned JSON and successful generator check contain 44 vectors, not the 46 claimed by REQUEST.md and SCOPE.md. Correct the publication count (or add and review the two intended cases); the native test only asserts at least 40. This review reports the actual 44.
- **B2B3B-R1-NBO-2**: The trace records probe(directory) but vcs_evidence/gitdir_target perform their by-name observations, file open and custody/read internally without walker observe/open/capture trace events. Expand the trace at those primitive call sites before relying on it as an exhaustive access log; the current no-open assertions cannot establish the absence of operations hidden by these helper calls.
- **B2B3B-R1-NBO-3**: The root-plus-depths-1-to-256 descriptor description applies to automatic subtree descent. named_root can retain a longer explicit chain allowed by the 4096-scalar grammar. State that distinction in descriptor accounting; EMFILE must remain a refusal.

The diff adds no production caller, downward host seam/flag rows, environment input or export. Public discovery refusal mapping is limited to NAME_UNREPRESENTABLE; remaining row integration stays with B2-b3c. Inventory succession, B2-b3c, B2-b4/T2 margin, readers/members and qualification remain outstanding.

Only REVIEW.md and review.json were written. Neither repository, worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed. No binding, integration, push, product qualification or entire-plan completion is claimed.
