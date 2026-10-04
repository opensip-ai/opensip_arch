# B-S1 — contract successor S3 (D15 discovery), with SX-1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-B r2** (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, GROK2, `92e65825…`) names its contract successors in item 25 (MB:770-787) and its design units in "Units after the law" (MB:839-842). This unit is **B-S1**:
- **S3** (MB:774): the security S3 and native §1.4 passages for D15 multi-repository workspaces (U-8, with U-9 unchanged, and the Config2 join), the security V3 discovery records, and the declaration-reader registry. Its content is MB items 19, 20, 22 and 24.
- **SX-1** of law **M3-C** (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, MC:218, MC:1047): `.opensip/` at the project root and at each admitted member root is never source. The accepted M3 plan lands it here (`M3-PLAN.md:211`, `:272`).

B2-a and C1a need SX-1, and B3-b needs S3 (MB:843-850; MC:1069).

**S9 is split out (lead decision, 2026-10-04).** M3-B's units table puts S9's remedy text in B-S1 (MB:841). By the lead's decision it is now its own design unit, **B-S9** (`docs/implementation/m3/config-discovery-b/b-s9/`), so that SX-1 and D15 do not wait on S9's binding form. B1-a's dependency "B-S1 (S9 text)" (MB:843) becomes "B-S9". This unit carries no S9 content and no passage supersession.

**Product.** Main at `e093e90` (F8b's binding, 77 contract successors), read only. The record is built and checked against it.

## Short names

MB is M3-B r2 and MC is M3-C r6, accepted by CODEX2 (`8274bca1…`); the live file is cited, and r6 left r5's SX-1 text unchanged. X2 is `docs/implementation/m2/project-root-x2/PROPOSAL.md` (r9 accepted). X12-0 is `docs/implementation/m2/config-remedy-x12-0/`. X2:NNN cites the live r9 file, whose header moves r8's lines.

The parents, all accepted base inputs of the lock at `e093e90`:
- **SL** `docs/v2/contracts/product-v1/security-and-lifecycle.md` (119,915 bytes, `a319da39…`);
- **NE** `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes, `83b99783…`);
- **IE** `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes, `c82404f3…`).

The bundles that the additions extend (not parents, because they are not overridden):
- **SLS** `docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json`;
- **NES** `docs/coop/design-corrections/native/native-evidence.schemas.v2.json`.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: every override, with the exact `before` and candidate `after` |
| `successor.json` | the contract successor record (25 passage overrides, no supersession) |
| `schemas/security-lifecycle.schemas.v1.b-s1-additions.json` | generated: SLS additions (`DiscoveryProvenanceV3`, `DiscoveryResultV3`, `AdmittedBoundaryInventoryV3` and six `$defs`) |
| `schemas/native-evidence.schemas.v2.b-s1-additions.json` | generated: NES additions (`PrunedTreeV3`, `AdmittedBoundaryInventoryV3`, `UnitBoundariesV2`, `UnitDiscoveryV3`) |
| `registry/workspace-declaration-readers.v1.json` | the closed reader registry (FW-13 row, MB:251) |
| `evidence/build_b_s1.py` | builds the generated files, the record and the subject manifest deterministically |
| `evidence/check_b_s1.py` | read-only content checks |
| `evidence/verify_scratch.py` | runs the real verify_design with a synthetic review and assent |
| `../b-s1-subject.json` | the subject manifest (generated) |
| `../b-s1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What it changes

### 1. SX-1: OpenSIP custody state is never source

`.opensip` at the selected root and at each admitted D15 member root joins the shared discovery rule's anchors (SL:190-195; NE:711-714; IE:551-552). It is an **exact anchor**: a directory named `.opensip` anywhere else is ordinary source. Whatever its entry type, the path is never entered, never source and never inventoried. It is observed only as an entry of its parent directory, never opened or listed, so CI never probes `local.json` (MB item 3; MC item 1). When it is observed as a directory, it is recorded once in `prunedTrees` with the new reason `opensip-custody-state`. It is always a conventional excluded prefix in the scope descriptor (NE:939; LD-3). It is never a read (SL:274). This settles MB finding F10, which MC item 1 also settles.

### 2. D15 in security S3

A new paragraph after SL:185, "Multi-repository workspaces", states MB items 19, 20, 22 and 24 as contract text:
- **Shape.** W1 to W3 and M1 to M5. At most 64 members.
- **Declaration.** The two branches of MB item 20 (RF-1): with an admitted `discovery.workspaceRoots` array, from any layer or `--workspace-root`, the array alone decides membership and discovery stays exactly those roots; without it, the two closed readers declare members.
- **Membership.** A member is neither a nested repository nor a boundary, and inside it repositories and projects stay boundaries.
- **A member's `opensip.json`** is `memberConfigs`, never read.
- **Selection, not authorization.** MB item 23's flag reach is stated.
- **Refusal and disclosure rows.**
- **The V3 records.**

Edits to existing lines make the rest consistent:
- SL:166 and SL:168: nested repositories, with the member exception and LD-6's crossing rule;
- SL:180: an explicit source also suppresses reader membership;
- SL:262: a workspace is one project and its readers are not configuration carriers;
- SL:286 and SL:298: the V3 boundary export, whose members are not boundaries;
- SL:1323: the member cap, with its remedy (LD-17).

### 3. D15 in native §1.4

- **U-4a** gains the SX-1 anchor (NE:714) and names the V3 rows (NE:719, NE:730-731).
- **U-8** consumes `AdmittedBoundaryInventoryV3` (NE:822, NE:824) and gains a D15 paragraph after NE:863. A member is not a boundary. The subset test is unchanged over boundaries. A `vcs-tree` anchor whose directory is outside every boundary must be a member (LD-13). `UnitBoundariesV2` carries the members.
- **U-9 and U-6 are stated unchanged** in that paragraph; U-9's own lines are not overridden (LD-12).
- **The Config2 join** gains a D15 paragraph after NE:931. It keeps "exactly those roots, never widened". Its only addition is that an exact root may lie inside a member, and a present array suppresses reader membership.
- **The scope descriptor** adds `.opensip` to the conventional anchors and states that members add no prefix (NE:939-940).
- **H-8** (NE:4135) names the V3 inventory, which also fixes MB finding F9 there.

### 4. Identity §3

The source-inventory extent (IE:552) excludes `.opensip` at the root and at each member root.

### 5. The V3 records

These are additions to their bundles, never edits (LD-5). Each V3 record is its V2 record plus exactly the delta below. `check_b_s1.py` proves this structurally.

| Record | Delta from version 2 |
|---|---|
| SLS `PrunedTreeRowV3`, NES `PrunedTreeV3` | reason enum + `opensip-custody-state` |
| SLS `DiscoveryProvenanceV3` | `schemaVersion` 3. `prunedTrees` rows V3. Added: `memberRepositories` (≤ 64, `path` order, each with `declaredBy`); `workspaceDeclarations` (exactly one row per reader, `readerId` order); `memberConfigs` (≤ 64, `utf8` order) |
| SLS `DiscoveryResultV3` | V3 provenance; refusal enum + `PROJECT.SCOPE_LIMIT`; D9 branch `DiscoveryD9V1` (LD-15) |
| SLS and NES `AdmittedBoundaryInventoryV3` | `schemaVersion` 3; `prunedTrees` rows V3; + `memberRepositories` (relative, ≤ 64, `utf8` order) |
| NES `UnitBoundariesV2` | + `memberRepositories` |
| NES `UnitDiscoveryV3` | `prunedTrees` rows V3; `boundaries` is `UnitBoundariesV2` |
| SLS `$defs` (new) | `MemberDeclarationV1` (law field names `source`, `readerId`, `readerVersion`, `path`, `contentSha256`), `MemberRepositoryV1`, `WorkspaceDeclarationV1` (`absent`, `read` or `refused`), `UnresolvedDeclarationEntryV1` (closed reasons), `DiscoveryD9V1` |

Version-1 and version-2 records keep their bytes and are read under their own versions. No product producer has emitted a V2 discovery record: `discovery.rs` is absent (MB:44). `UnitMembershipV1` and `membershipDigest` do not change shape. Units inside members are ordinary `WorkspaceUnitV2` rows.

### 6. The reader registry

`registry/workspace-declaration-readers.v1.json` is the closed FW-13 registry. An unknown reader is a host invariant fault. It fixes, for `cargo-config-patch@1` and `npm-workspaces-members@1`:
- carriers, parsers and custody;
- entry grammar, placement and dispositions;
- the member cap's count;
- link derivation and the closed `unresolved` reasons.

`pnpm-workspace.yaml`, Python files and any tool-specific manifest are not readers (MB item 20; OQ-1).

### 7. S9 is not here

S9, the `CONFIG.INVALID` remedy text, is unit B-S9. B-S1 touches no native-model file.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects.

**LD-1 and LD-2: moved to B-S9.** S9's form and text are B-S9's decisions (`b-s9/README.md`). The numbers are kept so that the other decisions keep theirs.

**LD-3. `.opensip` is always a conventional excluded prefix, and a `prunedTrees` row when observed.**
- The same checkout gives the same `scopeDigest` whether or not `.opensip/` exists, which depends on the installation's registration state, not on the source.
- That matches IE:556-557's two-hosts rule for the inventory. MC's "enters `excludedPathPrefixes`, as the other anchors do" is kept: `.git` is likewise both conventional and observed.
- **Rejected:**
  - **Observed-only.** The scope would differ between a registered and an unregistered copy of one checkout.
  - **A segment matched at any depth.** It would hide ordinary source named `.opensip`, which MC forbids.

**LD-4. SX-1 makes version 3 the current discovery record for every project, not only D15 projects.**
- The new reason enters closed enums, so the version moves.
- Nothing retained changes. No product producer of a V2 record exists, and `UnitMembershipV1`, `membershipDigest`, `snapshot2` and `scopeDigest` keep their shapes.
- **Rejected:**
  - **Recording the anchor in a new field.** That needs version 3 anyway.
  - **Not recording it in `prunedTrees`.** That contradicts MC's SX-1 text.

**LD-5. The records are additions to the SLS and NES bundles, never edits.**
- Each fragment pins its base bundle. It adds keys under the bundle's own names and resolves `#/` references in the merged bundle. The product units materialize them into the product schema sources.
- **Rejected:**
  - **Editing the frozen bundles.** They are frozen.
  - **Standalone copies of shared definitions.** They would drift.

**LD-6. A crossing into a repository that cannot become a member keeps `JOIN_CROSSES_NESTED_REPOSITORY`, including when W is in a repository.**
- MB is internally inconsistent here. Item 22 (MB:672) and item 24 row 1 (MB:753) give `JOIN_CROSSES_NESTED_REPOSITORY` for "any crossing when W fails W2". Item 24 row 3 (MB:755) gives `PROJECT.ROOT_CUSTODY_REFUSED` / `workspace-root-inside-repository` for "an explicit or config member when W is inside a repository". Both describe the same event.
- B-S1 follows item 22 and row 1, so every project that is not a D15 workspace keeps S3's existing refusal byte for byte.
- X2 r9's subject `workspace-root-inside-repository` is used where item 24 row 6 sends reader failures: as the disclosed reason for a reader entry inside a nested repository when W is itself in a repository. X2 r9 defers "when each applies" to MB item 24 (X2:89).
- **Rejected:** following row 3. It changes the public detail of an existing S3 refusal for projects that never opted into D15.
- **Reviewer to rule** (R2 in "Points for the reviewer").

**LD-7. The member cap counts candidates after placement and before any Git read, and never truncates.**
- n is the number of distinct repositories that the active branch's declarations name after M1 to M3. It is counted before X2 r9 item 6b reads any configuration or index, which is what bounds the ~260 MiB (MB:554).
- n > 64 refuses in **both** branches, which settles how MB item 24 row 5 relates to row 6.
- **Rejected:**
  - **Dropping the excess reader-declared members.** That is truncation (MB item 12; U-7).
  - **Counting after item 6b.** Up to every declared candidate's index would be read before the bound applies.

**LD-8. Membership is by an entry's placement alone. Link failures leave the member declared.**
- Reading a provider manifest to decide membership would make boundaries depend on units: the fixpoint MB item 20 rejects.
- **Rejected:** dropping the member on a name mismatch, an ambiguity or an unusable version.

**LD-9. Reader grammar is strict and ambiguity is disclosed.**
- An entry path is exactly U-0's canonical relative directory, never normalized.
- `W/.cargo/config` and `W/.cargo/config.toml` both present: nothing is declared, and the carrier is `carrier-ambiguous`. Cargo's own preference is not imitated (MB item 17: narrower scope, disclosed).
- npm's object form `{packages: […]}` is `workspaces-shape-unsupported`.
- A glob is `workspace-glob-crosses-repository` when its literal prefix reaches a nested repository. Globs are never evaluated.
- **Rejected:**
  - **Normalizing `./x` or `x/`.** A second spelling of one entry.
  - **Picking one Cargo carrier.** A silent choice.
  - **Expanding globs against the filesystem.** That is the glob program SL:184 forbids.

**LD-10. Readers run whenever discovery runs, and declare only under W2 with no array.**
- When W is in a repository they declare nothing and disclose only entries inside nested repositories. A normal repository with a `[patch]` git entry therefore gets no D15 noise.
- **Rejected:**
  - **Not running at all outside W2.** Item 24's `workspace-root-inside-repository` would then have no use, and a user whose workspace root sits in a repository would get no hint.
  - **Recording every entry outside W2.** Noise in ordinary repositories.

**LD-11. `memberConfigs` records paths only. The file is never read.**
- "Not consulted" (MB item 22) is taken literally. C1 still inventories the file as ordinary member source (MC r4, C3-R1).

**LD-12. U-9's lines are not overridden.**
- "U-9 unchanged" (MB:674, MB:774) is stated inside U-8's D15 paragraph, with MB item 22's sentence that a member is never a second fallback site.
- **Rejected:** appending to U-9 itself. That would read as a change to the rule.

**LD-13. The native member check is the `vcs-tree` anchor test.**
- MB item 22's "a member path in the native derivation" is made exact. A `vcs-tree` anchor `D/<marker>`, derived or carried, with D strictly below the root and outside every boundary, must have D in `memberRepositories`.
- An extra admitted member is carried through, like any additional admitted row.
- **Rejected:** a two-way equality. The native instrument cannot observe what security observed, which is U-8's superset rule.

**LD-14. `discovery-defaults.py` is not overridden here.**
- NE:708-710 makes the prose authoritative and DD the reference. A DD refresh needs its reference checkers rerun, which is a machine job this docs-only unit does not do.
- B2-a implements SX-1 natively, and DD's refresh is owed with B2-a's evidence (finding BS1-F3).

**LD-15. `DiscoveryResultV3` has its own D9 subset.**
- SLS `$defs/D9` omits `REQUEST.UNSATISFIABLE`. Yet `PROJECT.WORKSPACE_UNIT_LIMIT` carries it (SL:217-218; security model :147), as does the new member cap.
- **Rejected:** widening the bundle D9 here, which is a change to every version-1 and version-2 record (finding BS1-F2).

**LD-16. A Cargo link carries `cargoPatchSource`, the `[patch.<source>]` key.**
- S5 projects admitted links as `[patch.<source>]` entries (MB:694) and cannot do so without it.

**LD-17. `members:<n>>64` has its own remedy.**
- X2 r9 leaves this remedy to S3 (X2:74, X2:88): "This workspace declares more than 64 member repositories, the most one project admits. Name at most 64 members in discovery.workspaceRoots or --workspace-root, or select a narrower project root."
- X2's registry-capacity remedy stays those three subjects' only.

**LD-18. Locators.**
- Provenance paths are absolute locators, as V2's `selectedRoot`, `nestedRepositories` and `units` are.
- Inventory paths are relative, as V2's are.

## Points for the reviewer

- **R2 (LD-6).** Rule on MB item 22 and item 24 row 1 against item 24 row 3.
- **R3 (LD-3, LD-4).** Is SX-1's anchor, recorded in `prunedTrees` and always a conventional excluded prefix, right? Is moving every discovery record to version 3 acceptable?
- **R4 (LD-7, LD-8).** The cap's count and its branch reading; membership by placement only.
- **R5 (LD-10, registry).** Do the readers' dispositions match MB item 20's two branches exactly, with nothing widened (MB's forbidden substitutes, MB:885)?
- R1 and R6 moved to B-S9.
- **R7 (LD-13).** Is the `vcs-tree` anchor test a faithful reading of MB item 22's native mismatch sentence?

## Conflicts and reconciliations with accepted laws

- **M3-B r2:**
  - Items 22 and 24 rows 1 and 3 conflict on one event (LD-6).
  - Item 24 rows 5 and 6 leave the cap's branch reading open (LD-7).
  - The units table puts S9 in B-S1 (MB:841, MB:843). S9 is split into B-S9 by the lead's decision, a unit-plan change and not a change of content.
- **M3-C r6 (accepted):** SX-1 is landed as MC states it, plus LD-3's conventional prefix, which is stronger and consistent. MC's C1 rule "In CI, C1 never stats, opens or lists `.opensip/`" is matched: discovery observes the entry from its parent's listing only.
- **X2 r9:**
  - `workspace-root-inside-repository` is used as a disclosure reason (LD-6), under X2's deferral to MB item 24.
  - The `members:<n>>64` remedy is stated here, as X2 r9 asks.
  - Item 6b and the three Git objects are cited unchanged.
- **X12 r4 and X12-0:** none. B-S1 touches no native-model file.
- **B-S2 and VCS-1:** none here. B-S1 overrides IE:552 only; B-S2 overrides IE:542 and IE:547.

No owner question is raised. OQ-1, the shape of the owner's team workspace, stays open. The admitted shape is kept: a non-repository root with 1 to 64 disjoint conventional Git members, declared by explicit roots or by the Cargo patch and npm `workspaces` readers. Nothing widens it.

## Findings for other owners

- **BS1-F1: withdrawn.** With S9 split into B-S9, B-S1 needs no verify_design successor.
- **BS1-F2 (record hygiene).** SLS `$defs/D9` lacks `REQUEST.UNSATISFIABLE`, which `DiscoveryResultV1` and `V2`'s `PROJECT.WORKSPACE_UNIT_LIMIT` refusal carries. The reference checker asserts it (`check-security-lifecycle.v1.py:514`).
- **BS1-F3 (B2-a).** `discovery-defaults.py` lacks SX-1's anchor and D15's `memberRepositories` in `boundary_inventory_from_provenance`, so a reference refresh is owed (LD-14).
- **BS1-F4 (M4).** WS:1221's `recommend` record carries native `UnitDiscoveryV2`. When M4 wires `recommend`, its record must move to `UnitDiscoveryV3` through a workflow successor. M3 wires no command (MB item 18).
- **BS1-F5 (security reference seam).** SL:111-119's disposable instrument keys have no reader observation. The reference model is not updated here. The product instrument is native.

## Binding

B-S1 has passage overrides only, so it binds on the verify_design at main `e093e90` with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok2-b-s1-r1/review.json`;
- complete `b-s1-unit.json` (`ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`);
- append to the product lock `{record, subjectManifest, review, assent}` pinning `b-s1/successor.json`, `b-s1-subject.json`, the review and `b-s1-unit.json`;
- run plain verify_design.

Until review, `verify_scratch.py` serves `SCRATCH-B-S1/` placeholders in memory only.

**Evidence runs** (`python3.14 -I -B` at `nice -n 19`, read-only):
- `build_b_s1.py` twice: identical bytes.
- `check_b_s1.py`: pass.
- `verify_scratch.py` on the main checkout at `e093e90`, and with `--rev e093e90`: it binds. There are 25 overrides and no supersession. No bound successor overrides any of the same lines, and the candidates cover the subject. The selected inventory and inheritance are unchanged, and the lock goes from 77 to 78 contract successors. On the checkout, 40 generation sources are verified.

## Controls owed by the implementing units

- **B2-a:** the SX-1 anchor at the root and at a member root; `.opensip` elsewhere is source; a `.opensip` file or symlink is not inventoried; the CI trace shows no open or listing of `.opensip`.
- **B2-b and B3-b, Branch A from each source** (project layer, local layer, `--workspace-root`):
  - reader membership is suppressed;
  - a link into an admitted member is kept;
  - an entry naming another repository is `dropped-workspace-roots-present`, and its paths stay `outside-project-boundary`;
  - discovery inside a member visits exactly the named roots.
- **Branch B:** the four T2 workspaces give their overlay link maps. Disclosure fixtures:
  - glob-crossing, ambiguous-provider and name-mismatch;
  - `.cargo/config` with `config.toml`;
  - npm object form;
  - W in a repository (disclosure only);
  - a reader-declared member failing item 6b (excluded, disclosed).
- **The cap:** 64 and 65 members in each branch; 65 refuses before any index read.
- **LD-6:** an explicit root into a nested repository in a repository-rooted project keeps `JOIN_CROSSES_NESTED_REPOSITORY`.
- **U-8:** a `vcs-tree` anchor outside every boundary whose directory is not a member refuses `native.boundary-inventory-mismatch`. U-9's fallback is at `""` only.

## Not claimed

- No product code, test, build or corpus run was made. Only the three evidence scripts ran, read-only.
- No S9 content: see B-S9.
- No law is amended. No public code, class, exit, flag or command is added.
- No Linux claim.
- The member cap and the discovery ledger caps stay provisional (MB:907).
- D15's analysis value at M3 is bounded by MB findings F2 to F4. Links are not honoured before S5 and S6.
