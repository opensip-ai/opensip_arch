# GROK2 review: B-S1 r1, contract successor S3 with SX-1

**Verdict: ACCEPT-DESIGN-UNIT.**

Subject manifest: `docs/implementation/m3/config-discovery-b/b-s1-subject.json`, 1948 bytes, sha256 `f94f5c1d4861759737fc4ef11f7b05c6ba2467e32c20669849d79310eb169899`. Successor: `docs/implementation/m3/config-discovery-b/b-s1/successor.json`, 26832 bytes, sha256 `8faa376e543493a14e4db9b5cb0aa799b71a0759192f7866f4f21b1ddee266c3`. Single reviewer. Design-unit review. No cargo, tests, or crash-matrix binary. All pins in `hashes.txt` matched, including M3-C r6 at arch `3590205a9` (155209 bytes, sha256 `a2f16b7bcf401f3c13f90915b0d48514cfaa7ab91f83decd3434e656bde8bab6`). `~/Library/Application Support/OpenSIP` was absent.

The record has 25 passage overrides and no supersession. S9 is absent from this unit. No native-model file is a parent or a candidate.

## Evidence

`build_b_s1.py` was run twice in a private scratch tree, with `python3.14 -I -B` at `nice -n 19`. The two runs matched, and the generated successor, subject manifest, `PASSAGES.md`, and both schema additions matched the subject bytes.

`check_b_s1.py` passed: 25 overrides whose `before` text is the parent line, no supersession, V3 deltas exact, 36 `#/` references resolved in the merged bundles, positive and negative samples passed, and the registry ids and unresolved reasons equal the schema enums.

`verify_scratch.py --rev e093e90` passed. The lock goes from 77 to 78 contract successors. B-S1 is selected, with 25 overrides, no supersession, and 8 candidates. The selected inventory and the inheritance projection are unchanged, and no bound successor overrides any of these lines. On the checkout the same script passed with 40 generation sources verified and no generator executed (see NBO-1).

## Faithfulness

The overrides state M3-B items 19, 20, 22, and 24, and they state item 23's flag reach in the new S3 paragraph, which is the reach the request names. The shape is W1–W3 and M1–M5, at most 64 members, with X2 r9 item 6b admitting only `M/.git`, `M/.git/config`, and `M/.git/index`. A member is neither a nested repository nor a boundary. Its `opensip.json` is `memberConfigs` and is never read as configuration. Discovery with an admitted `discovery.workspaceRoots` array, from the project layer, the interactive local layer, or `--workspace-root`, stays exactly those roots. The readers then declare no member. Without the array, only `cargo-config-patch@1` and `npm-workspaces-members@1` declare members, by placement, and a glob declares none.

That keeps RF-1. It is in the new paragraph, in SL:180, in the Config2 paragraph after NE:931, and in the registry's branch A. The forbidden substitutes at MB:885–898 stay intact: no new public code, no truncation, no reader-added member and no widened discovery while an array is present, no glob membership, no write, and no link honoured before S5 or S6.

SX-1 is the exact anchor `.opensip` at the selected root and at each admitted member root, reason `opensip-custody-state`, recorded in `prunedTrees` when observed as a directory, never entered, never source, and never inventoried. A directory of that name anywhere else stays ordinary source. The overrides are SL:195, SL:205, SL:274, NE:714, NE:939, and IE:552, which is the set MC:218 and MC:1047 name. Observation is from the parent's listing only, so CI does not open or list `.opensip`.

## Rulings

**R2, LD-6.** Item 22 and item 24 row 1 govern. A crossing into a repository that cannot become a member, including any crossing when W fails W2, keeps `PROJECT.EXPLICIT_PATH_INVALID` / `JOIN_CROSSES_NESTED_REPOSITORY` (SL:168 and the new paragraph). Projects that never opt into D15 keep today's refusal. `workspace-root-inside-repository` is the disclosure subject for a reader entry inside a nested repository when W is itself in a repository. That is item 24 row 6, an exclusion rather than a refusal, and it is the use X2 r9 leaves to item 24 (X2:89). Row 3 is not applied to an explicit or config member.

**R3, LD-3 and LD-4.** The anchor is always a conventional excluded prefix, and it is a `prunedTrees` row when observed as a directory. NE:938 already treats `.git` as a conventional anchor and as an observed pruned tree. Putting `.opensip` in both places keeps `scopeDigest` independent of whether the directory exists, and it matches MC's "enters `excludedPathPrefixes`, as the other anchors do." The path is exact: the conventional set names the project root and each admitted member root, which is the depth limit MC states. Version 3 is the current discovery record for every project, because the new reason enters closed enums and SX-1 applies at every selected root. Version-1 and version-2 records keep their bytes. `memberRepositories` and `memberConfigs` are empty when there is no member. `UnitMembershipV1` and `membershipDigest` are untouched. The VCS-observation version stays S4's, in B-S2.

**R4, LD-7 and LD-8.** `n` counts distinct repositories the active branch's declarations name after placement and before X2 r9 item 6b reads any Git configuration or index. `n > 64` refuses `PROJECT.SCOPE_LIMIT` / `REQUEST.UNSATISFIABLE` with subject `members:<n>>64` in both branches. Members are never dropped to fit. The remedy at SL:1323 is the sentence X2 r9 leaves to S3 (X2:74, X2:88), and X2's registry-capacity remedy stays with its three subjects. An entry declares its candidate by placement alone. A name mismatch, an ambiguity, or an unusable version yields no link and leaves the member declared. That matches item 20, where those outcomes are link outcomes, and it avoids the fixpoint item 20 rejects.

**R5, LD-10.** With the array present and W2 holding, readers declare no member. Links are kept only inside members the array already admitted. Any other repository entry is `dropped-workspace-roots-present`. With the array absent and W2 holding, the readers declare members. When W2 fails, readers declare nothing and derive no link; a literal entry inside a nested repository is disclosed as `member-excluded` with subject `workspace-root-inside-repository`, and no other entry is recorded. That narrows disclosure for an ordinary repository. It adds no member and widens no discovery. The registry is the disposition table the S3 paragraph cites.

**R7, LD-13.** U-8's subset test over boundaries is unchanged. The added test is a `vcs-tree` anchor `D/<marker>`, derived or carried, with D strictly below the root and outside every admitted boundary: D must be in `memberRepositories`, or the inventory refuses `native.boundary-inventory-mismatch`. An extra admitted member is carried, which is U-8's superset direction. U-9's own lines are not overridden. The D15 paragraph states U-9 and U-6 unchanged, including that a member is never a second fallback site and that a cross-member edge stays `external-module-boundary`.

## Records and registry

Each V3 record is its version-2 record plus the declared delta. `PrunedTreeRowV3` and native `PrunedTreeV3` add only `opensip-custody-state`. `DiscoveryProvenanceV3` adds `memberRepositories` (at most 64, path order, each `declaredBy`), `workspaceDeclarations` (exactly one row per reader), and `memberConfigs` (at most 64, utf8 order). `DiscoveryResultV3` points at the V3 provenance, adds `PROJECT.SCOPE_LIMIT`, and uses `DiscoveryD9V1`, the bundle D9 plus `REQUEST.UNSATISFIABLE`, so the bundle D9 itself stays unchanged. `AdmittedBoundaryInventoryV3` in both bundles adds relative `memberRepositories`. `UnitBoundariesV2` adds the same field. `UnitDiscoveryV3` uses `PrunedTreeV3` and `UnitBoundariesV2`.

`MemberDeclarationV1` is closed. An explicit tier is `explicit-joins` or `config-workspace-roots` with `path`. A reader tier is `source: reader` with `readerId`, `readerVersion`, `path`, and `contentSha256`. Those are item 22's names; the optional marks are the two branches of one closed `oneOf`. Provenance paths are absolute. Inventory paths are relative. New objects set `additionalProperties` to false and bound their arrays.

The registry is the FW-13 row (MB:251): `cargo-config-patch@1` and `npm-workspaces-members@1`, pinned, and an unknown id or version is a host invariant. `pnpm-workspace.yaml`, Python files, and any tool-specific manifest are not readers. A reader parses its carrier as data. It runs no process, writes nothing, and evaluates no glob. While an array is present it declares no member. A glob is classified from its literal prefix and declares neither a member nor a link.

## Conflicts and form

The README's conflict list matches the accepted laws this unit touches. M3-B's row 1 and row 3, and its cap rows, are ruled above. The units table's placement of S9 inside B-S1 is the split the request states: B-S9 carries that text, and B1-a's dependency becomes B-S9. M3-C r6's SX-1 is landed, with the conventional prefix above. X2 r9's three Git objects and item 6b are cited unchanged, and the `members:<n>>64` remedy is stated here. B-S1 overrides IE:552. B-S2's record overrides IE:542 and IE:547. No X12 or native-model passage is overridden.

The successor selects. Parents are the three pinned contracts. Candidates are the subject members other than the record. Passage overrides only, so it has no inventory candidate.

## Non-blocking

**NBO-1.** README pins product main at `e093e90` with 77 contract successors, and that commit still verifies as 77 to 78. The checkout at review time is `0ceb9ad`, which adds I1-L and has 78 successors. B-S1 also selects on that lock, as successor 79, with no shared line and an unchanged inventory.
