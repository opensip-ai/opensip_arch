# B2-C2-r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest SHA-256: `583eca29bfe0e390560995c8f6d838f4959d6d925ab94d1e86d9a67948593a3e` (11,289 bytes, 49 members).

All 49 member sizes and hashes match. All source.json authority pins and the product lock pin match. All ten product-map rows match their archived bytes and candidate worktree bytes; their parent pins or new-file absence match the product base. Architecture HEAD is `a35987d7092ba921a0459ae7e8f9660c3f676186`. Both product checkouts are at `1f70dba4d18d9db7b11253b9202846d2ca2bc50e`; main is clean. The candidate change set matches the map.

## Required findings

### B2C2-R1-RF-1 (P2): Empty-document acceptance needs an accepted law change

Location: `crates/host/src/typescript_config.rs:197`.

LD-B2C2-2(a) admits an empty or comment-only document as an empty object. Item 14a defines JSONC as JSON with comments and trailing commas, and requires non-JSONC files to refuse. Removing comments from these inputs leaves no JSON value. TypeScript compatibility is supporting evidence, not authority to add another grammar extension in this implementation unit. The two success vectors and the empty-document-refused mutation currently enforce the extension rather than the pinned law.

Evidence:

- SCOPE.md LD-B2C2-2(a) explicitly acknowledges going beyond JSON.
- read_fields returns Some(file) when document.root() is None.
- Permitted reference probes of an empty byte string and a comment-only document both returned success.

Required change: Either refuse empty/comment-only files as native.typescript-config-malformed and update the reference, expectations and controls, or obtain and pin an accepted M3-B law amendment explicitly admitting them before claiming implementation fidelity. Align the shared parser contract, scope record and evidence with that decision.

### B2C2-R1-RF-2 (P2): The Python oracle conflates JSON null with a missing document

Location: `tools/host/typescript_config_vectors.py:253`.

parse_jsonc returns Python None for both a JSON null value and an empty document. fields converts either to {}, accepting a null configuration. Rust produces Some(Node::Null) and rejects it at read_fields’ object check. Thus the independent oracle disagrees with Rust and with LD-B2C2-2(h), which requires an object root. The existing top-level malformed cases omit null.

Evidence:

- effective("tsconfig.json", source returning b"null") returned allowJs=False, checkJs=False and a graph.
- The same success occurred for b"null /* comment */".
- An entry extending base.json whose bytes are b"null" succeeded and included both nodes.
- Rust typescript_config.rs:200-201 rejects every non-object root.

Required change: Distinguish an absent document from a parsed null value, or reject both if empty documents are removed under RF-1. Add hand-written malformed expectations for null at the entry and at an extended base, including comments around null; regenerate vectors and demonstrate reference/Rust agreement.

### B2C2-R1-RF-3 (P1): Repeated edges cause exponential inheritance work within all bounds

Location: `crates/host/src/typescript_config.rs:482`.

Walk::inherited recursively evaluates each edge without caching a node’s inherited options. Graph discovery deduplicates nodes, but option evaluation expands every path through the DAG. Python effective.inherited has the same defect. A valid eight-node chain with 64 repeated edges to the next node at each level requires 4,467,856,773,185 inherited calls by the source recurrence. The entire input is 5,021 bytes, the largest file is 717 bytes, and each node has at most 64 edges, so neither item 14a’s bounds nor O-1 explains or prevents the work. This can effectively hang pre-Plan discovery on small admitted input.

Evidence:

- Permitted Python profiling measured 255, 4,095 and 65,535 inherited calls for chains of 8, 12 and 16 nodes respectively, with two repeated edges per level.
- The 16-node input totaled 569 bytes and needed only 31 source reads.
- The larger 64-edge example was constructed and its recurrence calculated, not executed.
- Rust lines 485-486 and Python lines 396-397 recursively evaluate every repeated edge without a node cache.

Required change: Compute inherited options once per canonical node, using memoization or postorder evaluation in both Rust and the reference. Preserve repeated edges in the graph and declaration-order precedence. Add a regression with repeated/shared bases that checks the result and verifies bounded evaluation work without depending on a long wall-clock timeout; refresh the affected evidence.

## Other requested decisions

- **Item 14a fidelity:** apart from the findings above, the source implements the closed specifier classification order, lexical normalization before reads, path and nearest-package candidate orders, canonical node identity, cycle checks, 32-node/64-KiB boundary comparisons, four refusal keys and NE's inheritance precedence. The exact `jsconfig.json` basename supplies the node's own default true; written false remains distinct from absence. Graph nodes sort by path and retain every edge. The node/file bounds constrain discovery but do not fix RF-3's subsequent evaluation cost.
- **LD-B2C2-2:** (a) needs a law amendment or removal, as RF-1 explicitly rules. Decisions (b)-(h) are otherwise reasonable implementation decisions: initial BOM handling, CR/LF comment termination, scalar-valid string escapes, strict literals/numbers/UTF-8, one trailing comma, iterative nesting without another depth refusal, and object/boolean/extends type checks. RF-2 violates (h) in the reference.
- **LD-B2C2-3 through -5:** immediate link refusal follows the pre-C1 link rule even if a later candidate exists. Per-spelling normalization, skipping the project-directory candidate, literal package candidate lists and non-files are sound. Depth-first declaration order and deterministic edge-owner versus file subjects do not introduce new refusal classes. Invalid/missing inventory entries appropriately remain composition faults; links retain the specified refusal.
- **LD-B2C2-6 and -9:** two-pass composition is sound for this scope: surviving unit/marker selection precedes option reading, and effective allowJs changes the mode. Refused discovery reads nothing; pruned markers are excluded. The seven units cases reproduce B2-c0's trusted observations. Keeping only the duplicate's last value and first position is consistent with the later item 14a law and the closed output; no duplicate disclosure field is invented.
- **Row 59:** the new Observation projects to request-rejected/2, CONFIG.INVALID, absent fault cause, S10's public detail and exact remedy, with bounded internal-key/path subject and no runId/executionId or operational key. The alias table equals the four S10 registry rows. The commit-evidence match correctly returns None. The matrix test adds row 59 and explicitly excludes the already-unimplemented row 58; it does not remove existing coverage.
- **Oracle and controls:** the file contains 113 hand-written cases, 67 refusals, plus seven units cases. The permitted vector check reproduces the checked-in bytes and validates its successful case graphs through S10. The named resolution, grammar, bounds, identity, inheritance, alias and FW-01 controls are represented. This establishes coverage of those cases, not oracle correctness for omitted inputs: null is missing, empty-document success is outside the current grammar, and repeated-edge cost is untested.
- **Purity/parser:** inspection finds configuration reads only through ConfigSource. Rust's parser uses explicit frames and arena indices; parsing and dropping nested values do not recurse through owned children. The graph walk's depth is bounded by canonical node count. The extended lexical FW-01 gate and its planted negatives are useful checks of the current pure implementation; they are not a general proof against every possible Rust spelling of I/O.
- **O-1:** deferral is acceptable for this unit's boolean discovery result because it emits no graph record or C2 projection and adds no unsupported edge refusal. More than 64 retained edges cannot be claimed as an admissible TypeScriptConfigGraphV1. The lead must resolve the law/contract mismatch before C2 emits such graphs, through the appropriate accepted authority change. RF-3 uses at most 64 edges per node and is independent of O-1. O-2/O-3 correctly remain custody/composition work.

## Verification and evidence

Reviewer reruns, all passing:

- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b2c2`: 114 rows, no findings.
- `python3 -I -B tools/tests/test_discovery_fw01.py`: eight passing tests, including planted negatives on copies.
- The expressly permitted Python 3.14 TypeScript vector `--check` with the requested architecture/packages roots: checked-in bytes verified.

Additional read-only imports exercised empty/comment-only documents, null entry/base files and other root types, normalization/package candidates, and profiled small repeated-edge graphs. Rust behavior for those additional inputs was established by source inspection; no Rust execution was performed.

The recorded host logs support 349 to 357 passes with the same eight pre-existing failures, across three suites. Focused TypeScript/outcome logs report 10 and 18 passing tests. Rustfmt classifications report all seven edited/new Rust files clean, and the recorded all-targets warning-denied Clippy completed successfully. The recorded verify_design check passes; it was not rerun. All 20 mutation logs show the intended gate failing without compilation errors: 17 host assertion failures, the unchecked-cycle mutation's stack-overflow abort, and two vector-generation failures. These are meaningful sensitivity checks, except that the empty-document mutation currently protects the unapproved extension described in RF-1. They do not address RF-2 or RF-3.

Only REVIEW.md and review.json were written in the requested directory. Neither repository nor the candidate worktree was edited. No Cargo, rustc, build, unpermitted test/lane, network, installation, private fixture, signing key, held tree or T2 held-out access was used. No delegation or other panes were used. Acceptance and qualification are not claimed.
