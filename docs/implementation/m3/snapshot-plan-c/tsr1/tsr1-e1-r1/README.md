# TSR-1-E1 r1: the synthesized profile's program roots, and who discloses its limits

2026-11-11. Design author (Claude Opus 5.5, R2-DEEP, medium; preflight ROUTE-OK), under the lead's rulings on
JS-SYNTH-PROFILE-1 Q1-Q7 (`LC/js-synth-profile-1/QUESTIONS.md`; groundwork `SCOPE-r1.md`). **Status: PROPOSED, r1.**
Q1-Q4 are adopted AT RISK as the readings the host code is written against. It needs one independent review and the
cross-vendor review, then the lead's adoption in a receipt that pins this file's sha256. It binds nothing and edits no file.

**Short names.** Base: architecture main `fa6fa0fba`. **TSR** = `TSR-1-r4.md` beside this directory (sha256 `be654c41…`,
`ADOPTION-TSR-1.md`). **NE** = `docs/v2/contracts/product-v1/native-evidence.md`. **NS** / **NM** / **NCM** =
`docs/coop/design-corrections/native/` `native-evidence.schemas.v2.json` / `native_evidence_model.v2.py` /
`native-capability-matrix.v2.json`. **ENC** = `docs/coop/design-corrections/foundation/enumeration-contract.v1.md`.
**NSSF1** = `docs/implementation/m3/native-successors-fa/nss-f1/NSS-F1-r2.md`. **P** = `opensip-f2min` @ `e526e873`,
`providers/typescript/src/`. `LC` = `.opensip-implementation-cache/lead-2026-10-25`. Marks: **SETTLED-BY-TEXT** (the texts
decide it; this record only states it), **PROPOSED** (new law, needs review).

**What it amends (additive).** TSR R-1.10 (TSR:306-314), which completes `SynthesizedCompilerOptionsV1` but leaves its
roots to NE:1426-1427: "roots = every `.ts/.tsx/.js/.mjs/.cjs/.jsx` file under the unit excluding `node_modules`, `.git`
and host ignore conventions". It adds a paragraph **R-1.10a** with E1.1-E1.6 below. E1.7 and E1.8 state ownership and
add no profile law. The selectors NE:175 ("Plan-bound with `DEFAULTED` provenance, disclosed in output") and NE:607
("each is disclosed in Coverage, never hidden") keep their bytes. E1.7 states how they are met.

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

**E1.3 Exclusions. SETTLED-BY-TEXT for the five segments (lead Q3).** NE:1427's "`node_modules`, `.git` and host ignore
conventions" reads as U-4a, which states the host ignore conventions "once, normatively" (NE:703-710). Its pruned trees
are matched "by **exact path segment** (never substring)": `node_modules`, `.git`, `.hg`, `.svn`, `.jj` (NE:710-712;
the reference `discovery-defaults.py:58-59`, `_segment_prune` :139-147). A path with any such segment is not a root.
A unit root never contains one (U-4b item 1, NE:747-749), so the result is the same whether segments are counted from
the project root or from the unit root. U-4a's third arm (a Cargo `target` segment under a Cargo root, NE:712-716) and
boundary rows are left open (O1).

**E1.4 Declaration files. PROPOSED (lead Q4).** The six extensions are tested with TSR R-4.4's predicate: "A path `p`
**has** extension `e` when its rooted subject `/` + `p` is longer than `e` and ends with it" (TSR:761-762). So `x.d.ts` is
a root: it has `.ts`, which NE:1426 lists. `x.d.mts` and `x.d.cts` are not roots: they have `.mts` and `.cts`, which
NE:1426 omits and TSR keeps out of synthesized roots (TSR:1117). They do not have `.ts`. `.mts`, `.cts` and `.json`
are not roots. Weakest point: R-4.4 does not group `.d.ts` with `.ts` for this profile. That grouping comes only from
the predicate applied to NE's list (NM agrees by `endswith`).

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

**E1.7 Disclosure. PROPOSED (lead Q7; the texts name no owner or member).**
- **The texts.** No record has a member for either disclosure. `WorkspaceUnitV2.provenance` cannot be `DEFAULTED` for this
  unit: it is `DISCOVERED` or `EXPLICIT`, and only U-9 is `DEFAULTED` (U-4b item 2, NE:774-776). The only `DEFAULTED`
  enums in NS are the unit records' (NS `WorkspaceUnitV1`, `WorkspaceUnitV2`). `ViewEntryV3` and `CoverageResultV3` are
  closed and have no limitation member (NE:2017-2031; NS:1250-1263, :1383-1390). The one `limitations` member is
  `TypeDerivationV1`'s, and its enum is `["L-JS3"]` (NS:1235-1247; NE:2350-2354). So no producer can write "L-JS1" into
  Coverage without a schema successor.
- **(a) `DEFAULTED` provenance: the host, in the Plan.** The disclosure is the retained universe members
  `configOrigin = "synthesized"`, `synthesizerVersion = 1` and `synthesizedOptions` non-null (NE:175, :1386-1391), with
  the context's empty `configGraphPaths` (NE:1489). JS-SYNTH-PROFILE-1 (commit 2) produces them. They are Plan identity
  and are retained with the sealed Run. No other member is added.
- **(b) L-JS1: carried by the Coverage key, no new member.** Every Coverage record names its `sourceUniverse`
  in its key (NE:2016-2017; NS `CoverageKeyV2`, :1334-1337). A `coverage2` record of `imports@resolved-target`,
  `references@resolved-binding` or `calls@resolved-callee` whose source universe has `configOrigin = "synthesized"`
  is under L-JS1. The published matrix says so (NE:593-595; NCM:438-481). A specifier that L-JS1 makes unresolvable
  appears in that entry as `unresolved-module-specifier` in `unresolvedEdgeClasses` (NE:609, :2026). The provider adds nothing and is not changed. Rendering "L-JS1" by name
  belongs to the reporting and inspection surface (`InspectionBundle.limitations`, `workflows-and-surfaces.md:679-683`),
  which no M3 unit owns (O2).
- **Interim (normative for TS1).** Until a surface names L-JS1, a fixture-1 Run's milestone record must state, in its own
  text: the program at unit `""` is `js-synthesized` (`configOrigin=synthesized`, `synthesizerVersion` 1), so its options
  are host-defaulted, not read from the repository (NE:175). Its `imports` Coverage is under L-JS1 (NE:609), so a specifier
  resolvable only through `paths`, `baseUrl`, `rootDirs` or custom `types` is `unresolved-module-specifier`. And the
  product does not yet emit either disclosure by name.
- **Weakest point.** (b) is disclosure by join, not by a named member. A reader must know the matrix to see L-JS1, and
  nothing tells L-JS1's `unresolved-module-specifier` edges apart from other ones.

**E1.8 What nothing checks. SETTLED-BY-TEXT.** The provider recomputes the R-1.10 options (P `context/tsr1/options.ts:542-551`)
and checks them against the context (P `context/carrier.ts:119-137`, `program/adapter.ts:134-148`). It takes the roots as
given and builds over them (P `options.ts:350-352`, `program/program.ts:68-70`). NSSF1 LD-N7 makes the roots Plan
authority and rejects re-deriving them (NSSF1:289-300, alternative A6 :414). NC-10 accepts a changed root list when the
context is equal (NSSF1:576). The host's closure does not re-derive program semantics (ENC:81). **So only host tests
catch a host root error.** This record adds no provider or evaluator check. **Control owed (JS-SYNTH-PROFILE-1 commit 1,
control 1(c)):** one table over a tree with `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.d.ts` (in); `.mts`, `.cts`,
`.d.mts`, `.d.cts`, `.json` (out); each of the five segments nested under the unit (out); a substring such as
`node_modules_x/a.js` (in); a file outside the unit root (out); a nested unit's files (in, E1.2); and byte order with a
non-ASCII path and `eslint.config.mjs` at index 0.

## Open points

- **O1 (lead).** U-4a's Cargo arm: a `target` segment whose parent holds a co-located `Cargo.toml` (NE:712-716). Also
  `outside-project-boundary` rows (U-8) under the unit, which TSR R-4.2 excludes from tsconfig candidates (TSR:729-730)
  and NE:1426 does not mention. Body-parser has neither.
- **O2 (owner).** A named L-JS1 carrier: a schema successor to `ViewEntryV3`, or a reporting rule. It is not proposed here.

## Consequences

- **JS-SYNTH-PROFILE-1:** commit 1 implements E1.1-E1.4 and control 1(c) (E1.8). Commit 2 implements E1.5, E1.6 and
  E1.7 (a). Its control CP-G-TS2-STANDIN expects 14 roots.
- **The confinement trial (lead, CF-1 G-TS2):** body-parser's oracle is re-derived. It has 14 roots, with
  `eslint.config.mjs` at index 0 of both lists. The stand-in's `.js`/`.jsx` filter and its `jsx` rule (from `.jsx`
  alone; NE:1424 says `.jsx`/`.tsx`) differ from E1.4 and NE. The `jsx` difference has no body-parser effect.
- **The fixture-1 milestone record:** the E1.7 interim text.
- **Fixture 2 (`ts-small-constructs`):** nothing. It has no `js-synthesized` unit.

## What this record does not do

It adds no field, record, schema, code or check. It does not change TSR's tsconfig rules (R-4.2-R-4.13) or NE's
bytes. It does not decide O1 or O2. It does not make the provider or the evaluator re-derive roots.
