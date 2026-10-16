# B3-b0 r4: the members-and-readers reference (D15 over B2-b0)

## r4 round 2 (Codex `codex-b3b0-reference-r4`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B0REF-R4-RF-1:** the gitlink validator related elements before validating them all | **Two passes (`_member_gitlinks`).**<br>- **The table:** one that is not a mapping with string keys refuses as `MEMBER_GITLINKS_INCONSISTENT`, with no directory.<br>- **Each key's entry, alone:** the key must be a directory of the tree, the value a list, and every element a string with the entry grammar. Otherwise it refuses as `MEMBER_GITLINKS_INCONSISTENT:<dir>`.<br>- **Only then are validated strings related:** no repeat, and none at or below another.<br>So the rejection never depends on element order, and no incidental Python exception escapes. **Nine new controls:**<br>- a non-string element after a valid one, and before it;<br>- a malformed path after a valid one;<br>- a string, null and object value;<br>- a list table, a string table and a non-string key.<br>**The checker's `raises` path now asserts:**<br>- the exact type, `ValueError`;<br>- the diagnostic;<br>- that no reader lookup, item-6b consultation or walk happened first.<br>An incidental exception is a failure. **Two new negative-control mutants:**<br>- round 1's validator, which fails `non-string-after`;<br>- the container check removed, which fails the three table cases. |
| **NBO-1:** no-member equality is regression coverage | **Agreed.** The 64-case equality is stated as regression coverage of SLM's discovery cases, not a proof for every no-member input. The global grammar priority changes some no-member inputs by design (`["missing", "../bad"]`); the D15 cases bind those. |

**Checks (r4 round 2).** 64 of 64 no-member cases are equal to B2-b0 (regression coverage, NBO-1), and 124 of 124 D15 cases pass. All eight negative-control mutants fail.

## r4 changes (B3-b plan r2 amendment A4; Codex `codex-b3b-plan-a4-r2`, ACCEPT)

r4 is a successor of B3-b0 r3 (contract successor 168), whose bytes in `../b3-b-reference/` are unchanged. It is to be bound as **contract successor 169** before product use (A4-3). It changes two things.

| Change | What r4 does |
| --- | --- |
| **Item 6b's index gitlinks** (law M3-B r9 items 21 and 22; Codex B3B2B2B-R2-RF-1) | **A fourth side table, `memberGitlinks`:** for each candidate, the member-relative gitlink paths item 6b reports with its admission (default none). Like `memberObservations`, it is an input, not a Git model. **It is consulted only when item 6b admits that candidate.** **Each admitted member's gitlink that is a directory is a nested repository in pass two:**<br>- the walk never enters it;<br>- it is recorded in `nestedRepositories`;<br>- an exact root at or below it refuses `JOIN_CROSSES_NESTED_REPOSITORY`.<br>It is given SLM's one boundary representation (`vcs`) in pass two's input only. The result records only its path, never VCS evidence. A gitlink with no directory there bounds nothing. **The link stage** treats an entry whose directory is at or below a gitlink as inside that nested repository: `entry-not-in-a-member`, and nothing in it is read (LD-B3B0-7). **An inconsistent table** (a key that is not a directory, or a path that is not canonical, repeated, or at or below another gitlink of the same member) refuses before discovery, as `MEMBER_GITLINKS_INCONSISTENT:<dir>`. |
| **Branch A's order** (A4-2; it replaces LD-B3B0-6) | **Members are decided before any walk,** so the gitlinks bound every descent:<br>1. **The array gate.** It is pure: no observation, no walk and no member decided. It returns SLM's own records for SLM's first two array checks (`_explicit_units`). More than 4,096 roots (`MAX_EXPLICIT_JOINS`) refuses `PROJECT.EXPLICIT_PATH_INVALID` with a null path and `TOO_MANY_JOINS` or `TOO_MANY_WORKSPACE_ROOTS`. Otherwise, the first root in array order that fails the shared rule's grammar refuses `PROJECT.EXPLICIT_PATH_INVALID` with `JOIN_PATH_GRAMMAR`; its path is the raw text, or null when it is not a string. Both carry SLM's D9 for the code. The provenance is that of the discovery without members (LD-B3B0-5); that walk supplies only the provenance, never the verdict.<br>2. **The member decisions, in path order,** each stopping at the first refusal: placement and other volumes (row 2), the cap (row 5), then directory custody and item 6b per candidate (row 2).<br>3. **The walk, once,** with the admitted members entered and their gitlinks as nested repositories. Its refusal is the result, with no members and the declaration rows as they stand. Otherwise the record is the accepted pass two, with the final rows and links. |

**Precedence, as a public priority (A4-2):**
1. the array's size;
2. grammar, for the whole array;
3. the member rules, in path order;
4. the walk's refusals.

**Two documented changes from r3:**
- **Grammar is global.** `["missing", "../bad"]` was `ABSENT` at `missing`; it is now `JOIN_PATH_GRAMMAR` at `../bad`.
- **A member rule comes before a walk refusal.** Two r3 cases are revised:
  - `rf2-*-absent-before-layout` (`["missing", "a"]`, `a` a `.git` file) was `ABSENT`. It is now `PROJECT.ROOT_CUSTODY_REFUSED`, `member-vcs-unsupported:git-not-directory`, at `a`.
  - `rf2-*-crossing-before-layout` (`["f", "a/inner"]`) was the crossing at `a/inner`. It is now the layout refusal of `f`.

  The other `rf2-*` cases keep their results: both grammar cases (now also asserting the path and that item 6b is never consulted), `member-then-absent` and `member-decisions-in-path-order`.

**New controls (42), under both array sources where branch A applies:**
- **The gate:**
  - malformed grammar after an earlier root that would otherwise refuse: a conventional repository whose item-6b verdict refuses, a crossing into a member's nested repository, an absent root, a member-directory custody failure and a chain custody failure;
  - a non-string root (null path);
  - 4,096 roots with a malformed one (the grammar refusal);
  - 4,097 roots (the size refusal).

  Each asserts the exact record and that no item-6b verdict or gitlink is consulted.
- **Gitlinks in branch A:**
  - a join through a gitlink whose descendant fails custody: the crossing, and the walk never holds the descendant. A paired control without the gitlink gives the custody refusal;
  - a selected member whose gitlink subtree holds a nested project, a world-writable directory and a unit: none of it is walked. A paired control without the gitlink walks it;
  - the mixed case, in both path orders: the other member's item-6b refusal, before the crossing;
  - a device change below a gitlink, found by a placement lookup: a member rule (LD-B3B0-16);
  - links at and below a gitlink.
- **Gitlinks in branch B:**
  - a member's gitlink: never walked, no unit or project below it, its entry links nothing and its manifest is never read; a paired control without the gitlink;
  - a gitlink that is absent or a regular file;
  - the gitlinks of a candidate item 6b refuses, never consulted;
  - a glob beside a gitlink (LD-B3B0-15);
  - five inconsistent tables.

**New spies:**
- **A walk spy** wraps B2-b0's `walker_population` and records every path any pass-two population of the discovery holds. `notWalked` asserts the gitlink interior is never entered or probed.
- **A 6b spy** records every item-6b verdict and gitlink lookup. `no6b` asserts none was made.

**Negative controls** (`evidence/negative-control-r4.json`): the checker against six mutants of r4 (eight in round 2). Each fails the controls named there:
- gitlinks not made boundaries;
- links allowed below gitlinks;
- grammar checked per root (r3's order);
- the size not gated;
- r3's trial walk, with the provisional members entered before item 6b;
- the table not validated.

**Checks (r4).** 64 of 64 no-member cases are equal to B2-b0, and 115 of 115 D15 cases pass.

## r3 changes (Codex `codex-b3b0-reference-r2`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B0REF-R2-RF-1:** glob classification still consulted repository evidence below pruned anchors | **Globs see only the lawfully visible repositories** (`_visible_repositories`). This is a downward walk from W, parent-first to 256 segments, that never enters a pruned anchor (the shared rule over the Cargo roots seen so far, with SX-1 at W). It records a directory holding a VCS marker as a boundary without entering it, and it does not enter a nested `opensip.json` project. A glob crosses only when its literal prefix is at or below a visible repository, or a visible repository lies at or below the prefix. **Every reader metadata lookup now goes through one helper (`_entry`),** so the checker records exactly which paths the readers consulted. SLM and B2-b0 keep their own access, as before. **New controls with an observation spy:** paired fixtures that differ only by a repository hidden below `W/.opensip` and below `node_modules` (the hidden one changes nothing and is never consulted); a crossing proved by a visible enclosing repository, without consulting its interior; a repository inside a nested project, not visible; and the RF-1 cases' anchors, now also asserted never consulted. **Negative control** (`evidence/negative-control-r3.json`): the checker against a mutant with r2's raw-tree scan fails all four new glob controls. |

**Checks (r3).** 64 of 64 no-member cases are equal to B2-b0, and 73 of 73 D15 cases pass.

## r2 changes (Codex `codex-b3b0-reference-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B0REF-R1-RF-1:** the link reader crossed a member's custody-state and VCS anchors | **The placement walk never enters a pruned anchor.** At each step it classifies the next prefix with the shared rule, over the Cargo roots seen so far and with SX-1 at W and at the candidate found so far. On an anchor (`.opensip`, `.git` or another VCS tree, `node_modules`, a Cargo `target`) it stops: nothing below is looked up, and no provider there is read. The entry still declares its candidate by placement when one was found before the anchor, but it yields no link and is disclosed `entry-not-in-a-member` (LD-B3B0-7, extended). This is an existing reason; no new one is coined. **New controls**, with a read spy proving that the hidden manifest is never consulted: npm entries `a/.opensip/p`, `a/.git` and `a/node_modules/dep`, and Cargo entries under `a/.opensip` and `a/target`. **Changed:** an entry under `W/.opensip` is now `entry-not-in-a-member`, because the repository below the anchor is never seen. It was `member-excluded` in r1. |
| **B3B0REF-R1-RF-2:** branch A skipped earlier grammar and absence failures | **SLM decides first in branch A.** Pass two runs with every provisional member withheld: each array candidate that is not a crossing into a repository that cannot become a member. So the array's grammar, crossings, pruned trees, absence and directory custody refuse in SLM's own array order (rows 1 and 4). Only an accepted pass reaches the member decisions: placement and other volumes (row 2), then the cap (row 5), then 6b (row 2), each in path order. **New controls**, for config roots and for `--workspace-root`: grammar before and after a layout failure; absence before a layout failure; a member root and then an absent root inside it; a crossing before a layout failure; and member decisions in path order. |
| **B3B0REF-R1-RF-3:** side-table VCS evidence was not carried into selection and boundaries | **One VCS representation (`_project_vcs`).** Every directory the side table lists with markers is given SLM's `vcs` evidence before pass one. Only admitted members have it withheld in pass two. So the positive observation that excludes a candidate also keeps it a nested repository. An inconsistent table (a listed marker with no tree entry, an empty list, an unknown marker) refuses before discovery, as `VCS_SIDE_TABLE_INCONSISTENT:<dir>`. **New controls:** side-table-only `.hg`, `.svn` and `.jj` (excluded, a boundary, not a unit); a side-table `.git` file; a side-table repository nested in a member (a boundary); a side-table marker at an ancestor of W (W2 fails); and an inconsistent table. |
| **B3B0REF-R1-RF-4:** the depth bound was applied to the declaring entry | **M1's 256-segment bound now applies to the candidate only.** It is a placement failure with S3's existing depth subject, `DEPTH`: excluded in branch B, refused `PROJECT.ROOT_CUSTODY_REFUSED` in branch A. The entry directory has no depth limit. **New controls:** a depth-1 member declared by entries at depths 256 and 257 (admitted and linked), and a candidate at depth 257 in branch B (excluded) and in branch A (refused). |

**Checks (r2).** 64 of 64 no-member cases are equal to B2-b0, and 67 of 67 D15 cases pass.

**Design unit, reference only, r4, under the accepted B3-b plan r2 as amended by A1 to A4** (`../b3-b/PLAN-r2.md` section 1 and `../b3-b/PLAN-r2-A4.md`; Codex `codex-b3b-plan-r2` and `codex-b3b-plan-a4-r2`). **PROPOSED; it needs Codex's ACCEPT-DESIGN-UNIT.** It is to be bound as contract successor 169, succeeding r3 (successor 168). It is the executable oracle for B3-b2's readers, membership and V3 records.

**Authority:**
- law M3-B r9, items 19 to 24;
- design unit B-S1: S3's multi-repository passage, the V3 schema additions and the closed reader registry `../b-s1/registry/workspace-declaration-readers.v1.json`;
- B2-b0, the current discovery reference (contract successor 164);
- B3-b0 r3 (contract successor 168), which r4 succeeds.

## What it is

`reference/member_reader_reference.py` (new). It edits no byte of B2-b0, SLM, the B2-a rule or B-S1.

| Function | What it does |
| --- | --- |
| `Context(arch)` | Loads B2-b0 (with SLM and the B2-a rule), the foundation's exact JSON parser (`canonical.parse`), and the registry. |
| `discover(ctx, inp)` | The current discovery with D15. It returns a complete `DiscoveryResultV3`, with `memberRepositories`, `memberConfigs` and `workspaceDeclarations` filled, plus the link rows. |
| `boundary_inventory_v3(ctx, result)` | `AdmittedBoundaryInventoryV3` through the B2-a converter, which already carries `memberRepositories`. |

**The input** is SLM's synthetic observation plus four side tables, removed before SLM sees it:
- **`contents`:** the bytes of carriers and provider manifests.
- **`vcsMarkers`:** which VCS markers a directory holds, when SLM's single `vcs` flag does not say. By default, `vcs: true` is `.git` as a directory, and an `indirection` is `.git` as a file.
- **`memberObservations`:** item 6b's verdict per candidate, `admitted` or an X2 r9 subject.
- **(r4) `memberGitlinks`:** the member-relative index gitlinks item 6b reports with an admission.

**The flow:**
1. **Pass one** is SLM over the unchanged input: selection, the upward walk and the unit source, exactly B2-b0's pass one.
2. **The readers** read their carriers at W, as data, under S3 custody.
3. **Membership is decided:**
   - **with an admitted `workspaceRoots` array, or `--workspace-root` (branch A),** from the array;
   - **without one (branch B),** from the reader entries;
   - **when W is in a repository,** not at all.

   Placement, the member cap, the 6b verdicts and directory custody are applied in law item 24's order; in branch A (r4) the array gate comes first and the walk last (A4-2). Then come the links.
4. **Pass two** is B2-b0's downward population and SLM's `finish`. Every admitted member's VCS evidence and its own root `opensip.json` are withheld from SLM, so the member is entered as an ordinary directory, and the shared rule is bound to the member roots (SX-1 at each member root). Nested repositories and projects inside a member keep their evidence and stay boundaries. (r4) So does each admitted member's index gitlink that is a directory.

## Lead decisions

- **LD-B3B0-1. A wrapper with side tables.** SLM's `fs` model has no file bytes and a single VCS flag per directory, and SLM refuses unknown input keys. So the three D15 facts travel beside it and are removed before every SLM call. **Rejected:** editing SLM or its case schema.
- **LD-B3B0-2. Item 6b's verdict is supplied, not modelled** (plan r2 LD-B3B-2). Law item 21 says 6b is item 6a's admitted layout, unchanged. B3-b1's product tests own the Git decisions, with real fixtures.
- **LD-B3B0-3. The placement vocabulary.** The registry names the subjects as "X2 r9 or S3". This reference uses 6a's own reasons and S3's crossing details:

  | Condition | Branch B (member-excluded subject) | Branch A (refusal) |
  | --- | --- | --- |
  | `.git` a file | `member-vcs-unsupported:git-not-directory` | `PROJECT.ROOT_CUSTODY_REFUSED`, same subject (row 2) |
  | another VCS marker at the candidate | `member-vcs-unsupported:vcs-other` | same (row 2) |
  | a device change on the path | `member-outside-volume` | same (row 2) |
  | `opensip.json` strictly between W and the candidate | `JOIN_CROSSES_NESTED_PROJECT` | not a member; SLM's crossing refusal (row 1) |
  | the candidate at or below `W/.opensip` | (r2) never seen: the placement walk does not enter the anchor, so the entry is `entry-not-in-a-member` | SLM's pruned-tree refusal (row 1) |
  | member directory custody | `DIRECTORY_CUSTODY:<code>` | `PROJECT.ROOT_CUSTODY_REFUSED`, with the failing path and the code, S3's existing form (row 4) |
  | a 6b verdict | the verdict's subject | `PROJECT.ROOT_CUSTODY_REFUSED`, same subject (row 2) |
  | (r2) a candidate deeper than 256 segments (M1) | `DEPTH` | `PROJECT.ROOT_CUSTODY_REFUSED`, `DEPTH` (row 2) |

- **LD-B3B0-4. A selection refusal records each reader as `absent`.** Before a root is selected there is no W, so no carrier is observed at W. Every refusal after selection carries the readers' real rows.
- **LD-B3B0-5. A refusal decided by the member rules** (the cap, a branch-A placement or 6b failure) carries the provenance of the same discovery without members: what the walker observed, plus the readers' rows.
- **LD-B3B0-6 (r4, replacing r2's SLM-first order; plan amendment A4-2). The order in branch A.**
  1. The array gate: the size, then the first malformed root (SLM's records and D9, with the provenance of the discovery without members).
  2. Then placement failures and other volumes, in path order (row 2).
  3. Then the cap, counted after placement (row 5).
  4. Then directory custody and 6b per candidate, in path order (row 2).
  5. Then one walk, with the admitted members and their gitlinks, which decides absence, crossings, pruned trees and chain custody in SLM's array order (rows 1 and 4).

  **Branch B** excludes instead of refusing. The cap refuses in both branches, and a placement failure is never counted.
- **LD-B3B0-7 (r2, extended). An entry whose directory is outside every member's analyzed tree** is `entry-not-in-a-member`. Its directory may lie at or below a boundary inside its member (a nested repository or a nested `opensip.json` project), or (r2) at or below a pruned anchor, which is never entered. It still declares the member it found by placement, but it yields no link, and nothing below an anchor is consulted. The registry names this reason for W's own tree and is silent on these cases. The reason's sense, a directory that is neither a member's tree nor a link target, is the one used. **Rejected:** coining a new reason.
- **LD-B3B0-13 (r2). One VCS representation** (`_project_vcs`, RF-3), with the input contract above.
- **LD-B3B0-8. The member cap's D9** is request-rejected, exit 2, `REQUEST.UNSATISFIABLE` (B-S1 `DiscoveryD9V1`; item 24 row 5). SLM's D9 map predates it.
- **LD-B3B0-9. The owner waiver** (`--trust-project-owner` with an explicit `--project W`) applies to member directories and carrier directories only. It never applies to carrier files, provider manifests or member Git evidence; that last is item 23, and 6b's verdict carries it.
- **LD-B3B0-10. Cargo TOML** is parsed with Python's `tomllib` (TOML 1.0). The product uses the pinned Rust `toml` crate through the identity crate. B3-b2's vectors compare the two on the carriers they share.
- **LD-B3B0-11. Layers are resolved upstream.** A project-layer and a local-layer array both arrive as `configWorkspaceRoots` (source `config-workspace-roots`). `--workspace-root` arrives as `explicitJoins` (source `explicit-joins`). B3-b2's product controls exercise the three sources through the configuration resolver.
- **LD-B3B0-12. Links are typed rows, not a published record** (plan r2 LD-B3B-3).
- **LD-B3B0-14 (r4). A gitlink is supplied with item 6b's admission and bounds the member's analyzed tree.** It is a nested repository wherever pass two would meet it, through SLM's single boundary representation, and its path is all the result records. An entry at or below it declares its member by placement, as an entry inside a physical nested repository does (LD-B3B0-7), and yields no link. **Rejected:** stating a gitlink as a physical VCS marker (r3's only representation). The marker was visible before item 6b, so the order could not show the index-only boundary the product meets.
- **LD-B3B0-15 (r4). Globs are unchanged by gitlinks.** Glob classification is a placement observation, made before item 6b, over the lawfully visible repositories. A gitlink lies inside an admitted member, and every admitted member is itself a visible repository. Its candidate is reached from W without a pruned anchor or a nested project, at a depth within M1. So any glob whose literal prefix is at, above or below a gitlink is already at, above or below that member, and it crosses. Control: `r4-b-glob-beside-gitlink-crosses-its-member`.
- **LD-B3B0-16 (r4). Placement lookups may pass a gitlink's directory.** Forming and counting branch A's candidates looks up each directory on the path from W to a root by name (A4-2 step 2; Codex B3BA4-R1-NBO-2). Nothing is listed, judged for custody or read there before admission, and the walk never enters the gitlink. A device change found by those lookups below a gitlink is a member rule (row 2), and so comes before the walk's crossing, by A4-2's priority. Control: `r4-*-offvolume-below-gitlink-is-a-member-rule`.

## Checks (`evidence/check.py`, `evidence/checks.json`)

- **No-member equality.** All 64 discovery cases of `discovery-cases.v1.json` give the same status, refusal, path, detail and every provenance field other than the three D15 fields as B2-b0. None admits a member or yields a link.
- **124 D15 cases (r4 round 2; 115 in r4's first round, 73 in r3, 67 in r2, 42 in r1),** each with its outcome written in the checker by hand from the law and the registry, the r1 cases below plus the r2 controls in the table above:
  - **Branch B:** Cargo with two members, the legacy carrier, two carriers (ambiguous); npm literal members, globs (crossing and own-tree), a root glob, the object form, no `workspaces`, parse failures (a float, a duplicate key, TOML syntax, a non-table `patch`); carrier and carrier-directory custody.
  - **Every entry disposition:** grammar, outside the root, absent, not in a member, not a path patch, name mismatch, version unusable, manifest unusable (absent, parse, name absent, custody), ambiguous provider.
  - **Excluded candidates,** each with its subject: a `.git` file, `.hg`, a 6b verdict, another volume, directory custody, a nested project between, `.opensip`.
  - **Member contents:** its own `opensip.json` (`memberConfigs`, not a nested project), a nested repository inside it (a boundary), SX-1 at its root, its `.git` as a `vcs-tree` row, and an entry inside its nested repository (LD-B3B0-7).
  - **The cap:** 64 admits, 65 refuses with `members:65>64`, and a placement failure is not counted.
  - **W in a repository.**
  - **Branch A:** config roots and `--workspace-root`; links kept, other repositories dropped, own-tree entries dropped; two roots in one member; exact roots inside a member; layout, 6b, custody and other-volume refusals; root in a repository; a root inside a member's nested repository; a nested project between; the cap.
  - **Selection:** a launch inside a member selects that member alone; a selection refusal.
  - **The owner waiver:** it admits an other-owned member directory, and the member's Git evidence is still refused.
- **Validation.** Every result validates as `DiscoveryResultV3`, and every accepted result's inventory validates as `AdmittedBoundaryInventoryV3`, in the SLS bundle merged with B-S1's additions. Any exception fails the checker.

## Not claimed

- No product code: B3-b1 and B3-b2.
- No Git modelling (6b's verdicts and gitlinks are inputs).
- No link honouring (S5, S6).
- No snapshot (C1).
- No qualification.
