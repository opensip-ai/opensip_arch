# TSR-1-E1 r4: the synthesized profile's program roots, and who discloses its limits

2026-11-11. Design author (Claude Opus 5.5, R2-DEEP, medium; preflight ROUTE-OK), under the lead's rulings on
JS-SYNTH-PROFILE-1 Q1-Q7 (`LC/js-synth-profile-1/QUESTIONS.md`; groundwork `SCOPE-r1.md`). **Status: PROPOSED, r4.**
Q1, Q2 and Q4 are adopted AT RISK as the readings the host code is written against. **r2** applies the independent
review (`LC/js-synth-profile-1/review-opus/VERDICT.md`, F1-F4, A1-A2) under the lead's rulings on it. F1: E1.3 is R-4.2's
candidate rule, and O1 is closed by the texts. F2: E1.2 states the monorepo effect, and O3 goes to the owner. F3: E1.4a
lists the matcher behaviours that do not apply. F4: E1.7 (b) is OPEN for the owner. A1/A2: E1.8a covers the reference
model and the pinned vectors. **r3** applies the r2 review's advisories (`review-opus/VERDICT-r2.md`, ACCEPT):
AD-1 (the user-ignored-path silence in E1.3, and a tsconfig-branch finding under Consequences), AD-2 (O3), AD-3 (one
control row). **r4** records the lead's decision of O3 (LD-DEC-8 items 5-8) and corrects O3's opt-out sentence: a
configuration file is not an opt-out that keeps the unit synthesized. A second r4 commit applies the independent
review of that change (`LC/errata-1113/review-opus/VERDICT.md` RF-6, A-6, A-7): the `allowJs` split, "roots", and the
`workspaceRoots` route. r1 to r3 are in this branch's history. The record still needs the cross-vendor review and the
lead's adoption in a receipt that pins this file's sha256. It binds nothing and edits no file.

**Short names.** Base: architecture main `fa6fa0fba`. **TSR** = `TSR-1-r4.md` beside this directory (sha256 `be654c41…`,
`ADOPTION-TSR-1.md`). **NE** = `docs/v2/contracts/product-v1/native-evidence.md`. **NS** / **NM** / **NCM** =
`docs/coop/design-corrections/native/` `native-evidence.schemas.v2.json` / `native_evidence_model.v2.py` /
`native-capability-matrix.v2.json`. **ENC** = `docs/coop/design-corrections/foundation/enumeration-contract.v1.md`.
**NSSF1** = `docs/implementation/m3/native-successors-fa/nss-f1/NSS-F1-r2.md`. **P** = `opensip-f2min` @ `e526e873`,
`providers/typescript/src/`. **B** = `opensip-c4ats-b` @ `e4e764e6`. `LC` = `.opensip-implementation-cache/lead-2026-10-25`.
Marks: **SETTLED-BY-TEXT** (the texts decide it; this record only states it), **PROPOSED** (new law, needs review), **OPEN** (a named owner decides).

**What it amends (additive).** TSR R-1.10 (TSR:306-314), which completes `SynthesizedCompilerOptionsV1` but leaves its
roots to NE:1426-1427: "roots = every `.ts/.tsx/.js/.mjs/.cjs/.jsx` file under the unit excluding `node_modules`, `.git`
and host ignore conventions". It adds a paragraph **R-1.10a** with E1.1-E1.6 below (E1.4a
included). E1.7 and E1.8 state ownership and add no profile law. The selectors NE:175 ("Plan-bound with `DEFAULTED` provenance, disclosed in output") and NE:607
("each is disclosed in Coverage, never hidden") keep their bytes. E1.7 states what can and cannot meet them today.

## Clauses

**E1.1 Order. PROPOSED (lead Q1).** Under `js-synthesized`, `programRootFiles` is strictly ascending by the UTF-8 bytes
of the path, and `jsRootFiles` is its subsequence (R-4.10, TSR:843), so it has the same order. TSR's own order rule,
R-4.9 (`L ++ W ++ J`, TSR:840), is a rule over tsconfig specs and does not apply here.
- **What fixes order today.** NS types both lists `x-opensip-order: "sequence"` with `uniqueItems` (NS:3385-3409,
  `TypeScriptUniverseV2ResolvedInputs`). `sequence` "preserves order" and "the canonical encoder never sorts" (NE:1243-1250).
  So the schema says the producer's order is kept and is identity. It does not say what that order is. The only text
  that does is NM, which sorts (`sorted(...)`, NM:2223). Python `str` order is code-point order, which equals UTF-8
  byte order. NM is a reference model, not law.
- **Identity.** Both lists are universe members that reach `PlanId` (TSR P-0.4, TSR:131-138). Any other order is a
  different Plan.

**E1.2 "Under the unit". PROPOSED (lead Q2).** A path `p` is under a unit with root `r` iff `r = ""`, or `p` begins
with `r + "/"`. This is NM's `_under_unit` (NM:2211). The unit's `FileMembershipRowV1` rows do not decide it.
- **Nested units.** The subtree includes the directories of nested `tsjs` units. A file under a nested unit `N` (marker
  `N/package.json` or `N/tsconfig.json`) inside a `js-synthesized` unit `O` is a root of `O`'s program, under `O`'s
  synthesized options. It is also a root of `N`'s own program when `N`'s rules select it. Membership is unchanged:
  the file stays a member of `N` only, the deepest unit (U-3, NE:686-692).
- **No text forbids this.** Roots are not membership: "Roots may lie outside the unit's directory … Membership (U-3) is
  unchanged" (TSR:734-735). A root `tsconfig.json` with the default `include` `["**/*"]` (R-4.3) already makes nested
  units' files its roots. NE:175 ("they do not themselves make a unit") is about units, not roots. ENC has no rule
  that a root may appear in only one program (ENC:81: the host does not re-derive program semantics).
- **What it does to a JavaScript monorepo.** Take a root `package.json` with no config and nested packages
  `packages/*/package.json`. Each nested package's files are roots of the root unit's synthesized program and of the
  package's own program. So they are analysed in two universes, possibly under different options. They sit in two
  symbol extents (ENC:172, "Symbol extent is owner-admitted `programRootFiles`"), and their facts appear twice, under
  two `sourceUniverse` values. No occupancy conflict refuses this, because the conflict key includes `targetUniverse`
  (`docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md:50`). A rule that counts across universes
  counts these files twice.
- **This is already the unit model's behaviour.** A root `tsconfig.json` with no `files` or `include` gets
  `include = ["**/*"]` (R-4.3, TSR:750). Its roots therefore include nested `tsconfig` units' files, except under
  `node_modules`, `bower_components`, `jspm_packages` and dot-directories (R-4.6). The nested units are still distinct
  units (U-3, NE:690-692). NM's `_under_unit` does the same for every mode (NM:2211, :2223). The overlap is therefore not
  new to the unit model, but its cause is. Under a tsconfig it follows from the user's own spec, which `include` or
  `exclude` can change, and a `ts-tsconfig` root takes no nested `.js` file. Under `js-synthesized` the host imposes it
  unconditionally (O3, decided: it stands and is disclosed).
- **Fixtures.** `js-small-body-parser` has one marker, the root `package.json` (25 paths), and no nested unit.
  `ts-small-constructs` has no `js-synthesized` unit (root `tsconfig.json`, `projenrc/` and `test/` tsconfig units).
  Its overlap, if any, comes from R-4.3 and not from this record. Neither fixture is affected.

**E1.3 Candidates. SETTLED-BY-TEXT (corrects lead Q3's five-segment reading; review F1).** The synthesized roots are
drawn from TSR R-4.2's candidates: "the snapshot inventory paths that are regular files and whose membership row is not
inside a pruned tree (U-4a) and not `outside-project-boundary`" (TSR:729-730). E1.2 and E1.4 then filter them. The texts:
- NE:1427's "host ignore conventions" are U-4a's, stated "once, normatively" (NE:703-704). U-4a prunes by **exact path
  segment** (`node_modules`; `.git`, `.hg`, `.svn`, `.jj`) **and** "a `target` segment whose parent directory holds
  `Cargo.toml`, an actual Cargo root known from the units" (NE:710-714). A co-located `Cargo.toml` and `package.json`
  root is lawful and keeps both units (NE:671-673). Host membership classifies with those Cargo roots (B
  `discovery.rs:769`, :795).
- ENC:172: the symbol extent is `programRootFiles`, and "every extent path must be a first-party scoped snapshot
  member". An `outside-project-boundary` row (a nested repository, U-8) is not one.
- Concordant: R-6.1 already applies "R-4.2's candidate rule" under `js-synthesized` (TSR:894-897; there it selects the
  `package.json`). NSSF1 LD-N7 rests on "R-4.2's candidates exclude `outside-project-boundary` rows" (NSSF1:294-295).
- NM:2223 classifies with `()` as the Cargo roots. Its comment "a tsjs unit has no Cargo root" is false for the
  co-located case. NM is the defect (A1, E1.8a).

**A silence shared with R-4.2: user-ignored paths. PROPOSED (review AD-1).** ENC:172 says "every extent path must be a
first-party scoped snapshot member". The Plan scope's `excludedPathPrefixes` are "Config2 `ignorePaths` ∪ the anchors of
the pruned trees … ∪ the admitted boundary anchors" (NE:935-940). R-4.2 (TSR:729-730) names pruned trees and boundary
rows, but not `ignorePaths`. For the synthesized root list this record follows ENC:172: a path under an
`ignorePaths` prefix is not a root. The reason is that such a root would sit in the symbol extent (ENC:172) without being
a scoped member, and the extent rule would refuse it. So excluding it is the only lawful value. If ignored paths never
reach the snapshot inventory, the rule is moot. Whether R-4.2 itself should name them is for the lead, outside this
erratum.

A unit root never lies in a pruned tree (U-4b item 1, NE:747-749). **Host consequence:** B-21 today passes every
snapshot row as a candidate (B `plan.rs:2100-2106`). Commit 1's function must take the unit membership rows, or classify
with the units' Cargo roots and the boundary rows itself, and drop `host-ignore-convention` rows,
`outside-project-boundary` rows, non-regular rows and rows under a Config2 `ignorePaths` prefix.

**E1.4 Declaration files. PROPOSED (lead Q4).** The six extensions are tested with TSR R-4.4's predicate: "A path `p`
**has** extension `e` when its rooted subject `/` + `p` is longer than `e` and ends with it" (TSR:761-762). So `x.d.ts` is
a root: it has `.ts`, which NE:1426 lists. `x.d.mts` and `x.d.cts` are not roots: they have `.mts` and `.cts`, which
NE:1426 omits and TSR keeps out of synthesized roots (TSR:1117). They do not have `.ts`. `.mts`, `.cts` and `.json`
are not roots. Weakest point: R-4.4 does not group `.d.ts` with `.ts` for this profile. That grouping comes only from
the predicate applied to NE's list. NM agrees on `.d.ts` but disagrees on the rest: its `TS_EXT` (NM:2210) adds `.mts`
and `.cts`, so it admits `.mts`, `.cts`, `.d.mts` and `.d.cts`. This record follows TSR:1117, the adopted row: "NE:1426
… is the published law and is unchanged", and its model change "synthesized roots follow NE:1426". The reference fix
is owed (E1.8a).

**E1.4a TypeScript's file matching does not apply. PROPOSED (review F3).** NE:1426 says "every" such file. So none of
TSR R-4.6-R-4.8's matcher behaviours applies to synthesized roots. Each value below enters Plan identity (TSR:131-138).
NM and P agree with this clause today: NM filters by suffix and sorts, and P passes the list as given (`program.ts:68-70`).
B's tsconfig `program_roots` implements the matcher, so commit 1 must not reuse it. These behaviours do not apply:
- **No priority displacement.** `a.ts` and `a.js` are both roots (R-4.8 step 3 would drop `a.js`), and `a.d.ts` and
  `a.js` are both roots (R-4.8 step 4 drops `a.js` when `a.js` precedes `a.d.ts` in the stream, TSR:836).
- **No dot-file or dot-directory exclusion** (R-4.6's `[^./]` and `[^/.]`). `.config/x.js` and `.eslintrc.js` are roots.
- **No `.min.js` exclusion** (R-4.6 `(?!min\.js$)`). `x.min.js` is a root.
- **No `bower_components` or `jspm_packages` exclusion** (R-4.6 item 4). Only U-4a's trees are excluded (E1.3).
- **UTF-8 byte order, not R-4.7's UTF-16 code-unit order.** `B.js` precedes `a.js` (case is significant; P
  `program/host.ts:213`). `\u{FF21}.js` precedes `\u{1F600}.js`, which UTF-16 order reverses.

**E1.5 A JavaScript-only unit has a default program. SETTLED-BY-TEXT (lead Q5, reading A).** A `tsjs` unit whose U-1
marker is `package.json` (NE:663-667) has a `js-synthesized` default program, minted under R-1.10:
- NE:180-184: "For the five rows that name a **compilation** universe — `ts-tsconfig`, `js-allowjs`, `js-synthesized`,
  … the cell is read **after** §1.4 U-1 has yielded a unit …, because those modes describe a program and a program
  needs one."
- NE:175 (universe `typescript-v2`, `configOrigin=synthesized`); NE:196, "no `js-synthesized` program is minted for
  them" (bare `.js` directories), which assumes such a program is minted for a marked unit.
- ENC:21 ("`provenance=default-unit` … the `tsjs` or `rust` unit U-1 yields by marker precedence") and ENC:31's row
  "TS/JS `default-unit`, marker `package.json` (`js-synthesized`)": `programEntry` null, `entryConfigPath` null, `nodes` `[]`.
- NE:593-595 and the NCM `js-synthesized` rows (`imports` SUPPORTED-DESIGN with L-JS1, NCM:438-450; `references`, `calls`).
"The default program per TS unit" is PLAN-r5's phrase (`LC/c4ats/PLAN-r5.md:496`, citing ENC:21-24), not law. By
these texts its "TS unit" means a `tsjs` unit. The default binding exists only for a cell requested at that unit's mode
and root (ENC:17, :21), as for every mode. **Reading B** would need these selectors amended: NE:175, :180-184, :196, ENC:31,
the NCM rows, and NE:593-595's `js-synthesized` column. That would be a law change.

**E1.6 The profile entry. PROPOSED (lead Q6 (a)).** Under `js-synthesized` the host ignores the `ProfileIn.entry` it is
handed (the marker). It does not read it, validate it or copy it into any record. No text reads an entry here:
`entryConfigPath` is null with no nodes (ENC:31), the marker is never copied into `programEntry` (ENC:26), and the
`package.json` the profile reads is the one R-6.1's walk selects, which "under `js-synthesized` … is the unit's marker"
(TSR:894-897).

**E1.7 Disclosure. (a) PROPOSED; (b) OPEN, owner (lead Q7; review F4). The texts name no owner or member.**
- **The texts.** No record has a member for either disclosure. `WorkspaceUnitV2.provenance` cannot be `DEFAULTED` for this
  unit: it is `DISCOVERED` or `EXPLICIT`, and only U-9 is `DEFAULTED` (U-4b item 2, NE:774-776). The only `DEFAULTED`
  enums in NS are the unit records' (NS `WorkspaceUnitV1`, `WorkspaceUnitV2`). `ViewEntryV3` and `CoverageResultV3` are
  closed and have no limitation member (NE:2017-2031; NS:1250-1263, :1383-1390). The one `limitations` member is
  `TypeDerivationV1`'s, and its enum is `["L-JS3"]` (NS:1235-1247; NE:2350-2354). So no producer can write "L-JS1" into
  Coverage without a schema successor.
- **(a) `DEFAULTED` provenance: the host, in the Plan (the lead's interim reading).** The disclosure is the retained universe members
  `configOrigin = "synthesized"`, `synthesizerVersion = 1` and `synthesizedOptions` non-null (NE:175, :1386-1391), with
  the context's empty `configGraphPaths` (NE:1489). JS-SYNTH-PROFILE-1 (commit 2) produces them. They are Plan identity
  and are retained with the sealed Run. No other member is added.
- **(b) L-JS1. OPEN (owner); the lead's recommendation is disclosure by the Coverage key, with no new member.** Every Coverage record names its `sourceUniverse`
  in its key (NE:2016-2017; NS `CoverageKeyV2`, :1334-1337). A `coverage2` record of `imports@resolved-target`,
  `references@resolved-binding` or `calls@resolved-callee` whose source universe has `configOrigin = "synthesized"`
  is under L-JS1, by the law's table (NE:593-595; NCM:438-481 is its copy, status PROPOSED, NCM:4). A specifier that L-JS1 makes unresolvable
  appears in that entry as `unresolved-module-specifier` in `unresolvedEdgeClasses` (NE:609, :2026). The provider adds nothing and is not changed. No output
  member names a matrix limitation. `InspectionBundle.limitations` names correspondence reasons, an incomplete rule
  enumeration and truncation (`workflows-and-surfaces.md:681-683`), so it would need a successor. A reader holding the
  Run alone cannot see L-JS1. Whether a disclosure readable only from the Plan and the Coverage key meets NE:175
  ("disclosed in output") and NE:607 ("disclosed in Coverage, never hidden") is the owner's decision (O2).
- **Interim (normative for TS1).** A body-parser milestone record states both disclosures in its own text and states
  that this Run does not meet those two sentences of the native-evidence law as written. The two disclosures are these.
  First, the program at unit `""` is `js-synthesized` (`configOrigin=synthesized`, `synthesizerVersion` 1), so its
  options are host-defaulted (NE:175). Second, its `imports` Coverage is under L-JS1 (NE:609): a specifier resolvable
  only through `paths`, `baseUrl`, `rootDirs` or custom `types` is `unresolved-module-specifier`. The two law sentences
  are NE:175 and NE:607; the product meets them by join only.
- **Weakest point.** (b) is disclosure by join, not by a named member. A reader must know the matrix to see L-JS1, and
  nothing tells L-JS1's `unresolved-module-specifier` edges apart from other ones.

**E1.8 What nothing checks. SETTLED-BY-TEXT.** The provider recomputes the R-1.10 options (P `context/tsr1/options.ts:542-551`)
and checks them against the context (P `context/carrier.ts:119-137`, `program/adapter.ts:134-148`). It takes the roots as
given and builds over them (P `options.ts:350-352`, `program/program.ts:68-70`). NSSF1 LD-N7 makes the roots Plan
authority and rejects re-deriving them (NSSF1:289-300, alternative A6 :414). NC-10 accepts a changed root list when the
context is equal (NSSF1:576). The host's closure does not re-derive program semantics (ENC:81). **So only host tests
catch a host root error.** This record adds no provider or evaluator check. **Control owed (JS-SYNTH-PROFILE-1 commit 1,
control 1(c)), one table:**

| Case | Expected | Clause |
|---|---|---|
| `.js` `.jsx` `.mjs` `.cjs` `.ts` `.tsx` `.d.ts` | in | E1.4 |
| `.mts` `.cts` `.d.mts` `.d.cts` `.json` | out | E1.4 |
| each of `node_modules` `.git` `.hg` `.svn` `.jj` as a nested segment; `node_modules_x/a.js` | out; in | E1.3 |
| `target/x.js` beside a co-located root `Cargo.toml`; `src/target/x.js` | out; in | E1.3 |
| an `outside-project-boundary` row; a non-regular row | out | E1.3 |
| a file outside the unit root; a nested unit's file | out; in | E1.2 |
| `a.ts` + `a.js`; `a.d.ts` + `a.js` | all in | E1.4a |
| `.config/x.js`, `.eslintrc.js`, `x.min.js`, `bower_components/x.js`, `jspm_packages/x.js` | in | E1.4a |
| `jsRootFiles` content: exactly the `.js` `.jsx` `.mjs` `.cjs` members of `programRootFiles`, same order, no `.ts` `.tsx` `.d.ts` | subsequence | E1.1 (R-4.10) |
| `B.js` before `a.js`; `\u{FF21}.js` before `\u{1F600}.js`; `eslint.config.mjs` at index 0 | order | E1.1, E1.4a |

**E1.8a Second derivation and pinned vectors. PROPOSED (review A1, A2).** The table above alone is too little for new
identity values. Commit 1 also owes a differential: the host's `programRootFiles` and `jsRootFiles` over that tree equal
a reference derivation of E1.1-E1.4a. The reference is NM's `typescript_mode` after its two fixes (synthesized roots
without `.mts`/`.cts`, per TSR:1117's model-change row; classification with the units' Cargo roots and boundary rows,
per E1.3). The fixes are owed by the reference model's owner (TSR §12, C2b-1b's model change), or by a test-local
derivation if those fixes are not yet made. **Pinned root lists that must not change:** the NC-1 vectors
`js-synthesized-null` and `js-synthesized-layout` (B `typescript_nss_f1_vectors_tests.rs:135-142`; product fixtures
`crates/components/src/provider_protocol/fixtures/ts2-worker/nss-f1/*.bin`). Also P's embedded copies, `NC1_VECTORS`,
generated by `providers/typescript/scripts/gen-context-fixtures.mjs:170-188` into `src/test/fixtures/context-vectors.ts`.
Their trees hold `src/a.js` and `src/view.jsx` only, so E1 leaves them byte-identical. If one moves, its generator
regenerates it, never a hand edit.

## Open points

- **O1. Closed by text (E1.3).** The Cargo arm and boundary rows are R-4.2's and U-4a's (NE:703-714; ENC:172). They
  have no body-parser effect.
- **O2 (project owner).** First, whether disclosure by join (E1.7 (a) and (b)) meets NE:175 and NE:607. Second, if not,
  which carrier to add: a `ViewEntryV3` successor or a reporting rule. This covers every matrix limitation that has no
  carrier: L-JS1, L-JS2 (also on `ts-tsconfig` and `js-allowjs` `references`/`calls`), L-RS1-L-RS4 and L-FW1 (NE:593-597).
  Only L-JS3 has one (`TypeDerivationV1`).
- **O3. Decided by the lead (LD-DEC-8 items 5-8, under OD-DECIDE-1; r4).** Nested packages under a synthesized root
  (E1.2). Under a `tsconfig` the overlap with nested units is the user's own configuration. Under `js-synthesized` the
  host imposes it, and there is no opt-out that keeps the outer unit synthesized and the nested packages analysed:
  - a root `jsconfig.json`, or a root `tsconfig.json` with `allowJs`, alone changes the outer unit's mode to `js-allowjs`
    (NE:664-670), and its default `include` `["**/*"]` (R-4.3, TSR:750) takes the nested files as roots again. A plain
    root `tsconfig.json` selects `ts-tsconfig` (an omitted `allowJs` is false for it, NE:668-670), which takes no `.js`
    root at all (R-4.4; E1.2 above): nested `.js` files leave the outer program's roots, and so do the outer unit's own;
    nested `.ts` files are still taken;
  - such a file that also writes `exclude` (or a narrower `include`) does leave them out of the outer program's roots (the
    outer program can still reach them through imports, as non-root members), and the nested units are still
    analysed; but the outer unit is then no longer `js-synthesized`: another mode, other options, another universe;
  - `ignorePaths` drops the packages from analysis altogether: they leave the Plan scope (NE:936), not only the outer
    program (E1.3's ignored-path rule);
  - `opensip.json` `discovery.workspaceRoots`, listed explicitly without `.`, restricts discovery to the listed roots
    (NE:909-920; LD-DEC-8 panel A, `PANEL-A-texts.md:55`): it drops the outer unit instead, which suits only an outer
    unit with no source of its own.

  **Decision:** E1.2 stands (option (i)). A file that is a root of two programs yields two findings, as the identity law
  says for different universes (IE:1521-1523). No de-duplication is built. Disclosed wherever findings are counted:
  counts may double for nested packages under a synthesized unit, and one waiver covers both copies (LD-DEC-8 item 6;
  LD-DEC-8 panel A: "would plausibly match both. I did not trace the waiver-matching law for universe"). Revisit trigger:
  before the first release that admits a synthesized JavaScript unit for a user, or the baseline surfaces, whichever comes
  first; a de-duplication then is an identity-law amendment. Option (ii) (exclude nested `tsjs` subtrees from synthesized
  roots: a law line beside NE:1426 and TSR R-1.10a, a change to NM's `_under_unit` use and the control table, a divergence
  from R-4.3) is not taken. Neither fixture is affected. The cross-vendor reviewer may still read the identity law
  differently for two programs over one file (LD-DEC-8, "What would reverse this").

## Consequences

- **JS-SYNTH-PROFILE-1:** commit 1 implements E1.1-E1.4a over E1.3's candidates (not B-21's every-row set), with control
  1(c) and E1.8a's differential. Commit 2 implements E1.5, E1.6 and E1.7 (a). Its control CP-G-TS2-STANDIN expects 14
  roots. The NC-1 vectors and P's copies stay unchanged (E1.8a).
- **Reference model (TSR §12 owner):** NM's synthesized roots drop `.mts`/`.cts`, and NM classifies with the Cargo roots
  and boundary rows (A1).
- **The confinement trial (lead, CF-1 G-TS2):** body-parser's oracle is re-derived. It has 14 roots, with
  `eslint.config.mjs` at index 0 of both lists. The stand-in's `.js`/`.jsx` filter and its `jsx` rule (from `.jsx`
  alone; NE:1424 says `.jsx`/`.tsx`) differ from E1.4 and NE. The `jsx` difference has no body-parser effect. E1.3's wider exclusion and E1.4a have none
  either (the 14 roots hold no `target`, dot-file, `.min.js` or same-stem pair).
- **The body-parser milestone record:** the E1.7 interim text.
- **Finding for the lead (not this erratum's law; review AD-1).** The host's `tsconfig` branch also passes every snapshot
  row as a candidate. In B @ `e4e764e6`, `crates/host/src/plan.rs:2097-2106` builds the set, and `:2109` hands it to
  `opts::program_roots` (the worktree's uncommitted edits move these to :2144-2156). So that branch does not apply R-4.2's
  pruned-tree and boundary exclusions either. Inputs that would show a wrong tsconfig root list:
  - a `target/x.ts` beside a co-located root `Cargo.toml` under `include: ["**/*"]`;
  - a nested repository's (boundary) files;
  - a `files` literal naming a pruned or boundary row, which R-4.5 refuses and which would be admitted;
  - a path under `ignorePaths`.

  The TypeScript fixture is not such an input. `ts-small-constructs` (47 paths) has no `node_modules`, VCS directory,
  `Cargo.toml`, `target` segment or nested repository. Its only dot-directories are `.github/` and `.projen/`, which hold
  no TS or JS file, and no `ignorePaths` is configured (TS1-HOST-VALUES V8's `opensip.json` sets only
  `analysis.capabilities`).
- **Fixture 2 (`ts-small-constructs`):** nothing. It has no `js-synthesized` unit.

## What this record does not do

It adds no field, record, schema, code or check. It does not change TSR's tsconfig rules (R-4.2-R-4.13) or NE's
bytes. It does not decide O2. O3 is decided by the lead (LD-DEC-8), not by this record. It does not make the provider or the evaluator re-derive roots.
