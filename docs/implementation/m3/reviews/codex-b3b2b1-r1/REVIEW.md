# B3-B2B1 r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 12,714 bytes, SHA-256 `b1475d5d046ac5deeb40d0bfb01db47109c13b10a33ad4a649e074f4386565b6`. All 53 members rehash correctly. All product-map parent, candidate and archive pins match, as do the source-authority and candidate design-lock pins. Product main is clean at `03876532b54d8327db96091fababb1fd994a83d2`; the detached candidate is at that base. Architecture HEAD matches `6666ae1abc8f17d01168c715a1d3b4999170ae7f`.

## Required findings

### B3B2B1-R1-RF-1 — P1: Cargo key order changes the winning declaration

The Cargo carrier loop at workspace_declarations.rs:458–468 constructs `patch.<source>.<name>`, then phase_one deduplicates by that string. This encoding is not injective. LD-B3B2B1-3's argument that order cannot affect dispositions overlooks collisions between different source/name pairs.

For example, put these tables in this document order:

```toml
[patch."s.t"]
x = { path = "repos/a" }
[patch.s]
"t.x" = { path = "repos/b" }
```

Both entries are named `patch.s.t.x`. The reference's tomllib traversal encounters source s.t first and retains repos/a. Key-ordered traversal encounters source s first and retains repos/b. With ordinary valid repository placements at both paths, this changes membership even if neither provider manifest exists: package metadata does not decide membership. The registry does not impose an additional Cargo package-key grammar that removes quoted dotted keys from the reader's input domain.

This is a source-derived counterexample, not a probe executed by this reviewer. Preserve the reference's first-wins selection where flattened identifiers collide, add a reference-derived control, and correct LD-3. Sorting output rows does not repair a different member selected earlier. npm array order and branch-A first other-volume path are preserved independently of this defect.

### B3B2B1-R1-RF-2 — P1: Branch-A batching changes short-circuit observation semantics

phase_two at lines 952–966 judges directory custody for the entire candidate prefix and calls member_verdicts over it before deciding the first returned 6b refusal. B3-b0 instead performs directory custody and 6b together per candidate and returns immediately on branch A's first failure.

For a and b in ascending order, let a's 6b verdict be an ordinary unsupported-member refusal. In the reference b is never observed by 6b. The proposed native observation behind the batch can encounter host I/O or budget exhaustion at b and return O::Error, losing a's prior refusal. A fallible custody lookup for b can similarly escape before a's 6b is even consulted. Even without an error, the batch spends work on members after the terminal branch-A decision. The adapter uses Infallible and supplied verdicts, so current byte comparisons cannot establish LD-5's equivalence claim for the accepted fallible interface.

Provide a branch-A observation protocol that short-circuits directory custody and 6b in candidate order while checking pass-level environment/global sources once. Add a recording, fallible control where a refuses and b would error/exhaust; b must not be reached. This does not prohibit branch B from continuing past an excluded member. Returning the first semantic refusal after eagerly observing later candidates is insufficient.

### B3B2B1-R1-RF-3 — P2: Directory listings bypass the access assertions

Synthetic::children at workspace_declarations_tests.rs:203–210 enumerates keys and returns child names without recording the call or path. consulted records entry and marker access; read records bytes. Neither includes listings. A discarded children call below an anchor or boundary therefore passes the final-output, subset and forbidden-path assertions.

A2 explicitly requires recording every entry, markers, children and bytes call. Add a listing observation record and validate its allowed scope/forbidden paths. Include an output-preserving forbidden-listing mutation. The existing mutation of obs.entry before anchor classification is meaningful, but covers a different interface method.

### B3B2B1-R1-RF-4 — P2: JSON controls omit the byte boundary

parser_controls generates 26 JSON controls: carrier/provider pairs for depth, integer range, numeric forms, surrogate escapes and duplicate keys. None tests bytes at or beyond 4 MiB, although A2 r2 explicitly requires that alignment. The TooLarge and custody/read/parser boundary are consequently absent from these controls.

Add carrier and provider JSON fixtures at and beyond the byte limit, with accurate metadata and contents. Assert the reference/product dispositions, preserving custody-before-read precedence when metadata already refuses and testing a bounded read's TooLarge result where applicable. Compact parts encoding can avoid embedding giant literals. Refresh counts, generated artifacts and evidence.

## Other requested assessments

The phase boundary correctly leaves branch-A grammar, absence, disallowed crossing and pruned-tree priority with the trial walk. A refused trial returns TrialRefused rather than running terminal member decisions. Placement, candidate depth, cap-before-6b, root-in-repository, ordinary link failures and ambiguity generally follow the reference. The fixes above are needed before claiming complete order fidelity.

WorkspaceObservation otherwise provides the intended narrow access families. The core checks custody before requesting carrier/provider bytes; LD-4's reduced read set is appropriate. Uncaptured ACLs fail rather than pass. Literal and glob traversal apply pruning before descendant metadata queries, and links are suppressed for inner-boundary/pruned targets. The batch protocol and missing listing instrumentation are the outstanding interface issues.

The vector recorder wraps _finish and _refuse without editing the reference and extracts trial status, provisional members and final decision projections. The 116 baseline cases, 20 rootless cases and one input-consistency exclusion are consistent with running all discovery cases and D15 cases through that partition. Rootless selection has no W/core call and remains a composition obligation. These counts establish baseline enumeration, not coverage of the collision or fallible batching cases above.

The four TOML controls are a sound implementation of A2's labelled divergence: compare the real input's reference outcome, derive the product parse disposition by substituting syntactically unusable bytes, and restore the carrier digest to the original bytes. Product tests separately assert actual RecursionLimit/NodeLimit. Thus the expected parse failure is not silently treated as reference equality. The JSON controls present are meaningful, but the byte-bound pair is missing.

The identity change adds only read-only TomlTableView len/is_empty/iter views; it does not change the parser's grammar or bounds. The local toml.rs source pin is updated to the candidate bytes. The archived identity dependency logs show the same source-census failure at base and candidate, with their repository paths differing as expected. Treating that as a disclosed existing gate failure is appropriate; it is not a repaired dependency policy or an all-green dependency gate. The separate policy refresh remains outstanding.

An independent structural comparison confirms that both census JSON files change only closure/6's bytes and SHA-256, and all candidate closure pins match the sources. custody.rs adds only the module declaration block. No cost constants/model steps change; held-out rows remain outstanding. A1's full-ledger and blind-run gates remain later work.

## Evidence and limits

The two permitted checks were rerun successfully: operability source check (114 rows, no findings), and workspace_member_vectors.py --check against the bound reference bytes. No other executable check was run.

Archived security logs have the same 14 failing test names at base/candidate and three additional candidate passes (aggregate 1,141 to 1,144 across two suites). Identity has 72 passing tests on both. These are equal failure sets, not a fully green security suite. The package records successful Clippy, formatting, vector checks, FW-01, census, environment, operability and design verification; the identity dependency failure is separately disclosed. I inspected the archived evidence rather than rerunning those commands.

All eleven archived mutation logs compile and fail behavioral workspace-declaration tests. They cover the named cap, metadata-access, glob, shape, inner-link, ambiguity, declarer, root-in-repository, trial, waiver and depth changes. They do not cover the four findings above. No non-blocking observations are added.

No Cargo, rustc, tests, builds, lane, census tool or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. No panes or delegation were used. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
