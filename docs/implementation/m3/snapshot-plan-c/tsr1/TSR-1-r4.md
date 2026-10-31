# TSR-1: the TypeScript resolution profile (native successor for item 10 / NE §2.2–2.4), r4

**Standing.** Draft r4, PROPOSED, not accepted. Law text only. Authored by the TSR-1 author (R3-FRONTIER, Claude
`claude-opus-5-5`/high) under plan `lead-2026-10-25/tsr1/PLAN.md` and lead decision LD-Q-3. It is reviewed by Codex
`gpt-6-astra`/high and adopted by the coordinator under OD-AUTO-1. C2b-1b binds it; at that binding, this text and its
adoption receipt are copied unchanged into the architecture repository.

**What it decides.** The six public identity choices X-C2B1-1 to X-C2B1-6 (`../c2b1/ESCALATION-X-C2B1-r1.md`) and the
related findings X-TSR1-A to X-TSR1-E (`VERIFY-r2.md`). Each value it fixes enters `TypeScriptNativeContextV2` or the
`typescript-v2` universe, and so `nativeContextId`, the universe identity and `PlanId`. Its purpose is that two
conforming hosts mint the same context and universe for one repository when their admitted closures, platform and
other non-resolution identity inputs are equal.

**Its parts.**
- **Part P (the profile)**: §§0–9, the resolution law.
- **Part R (refusal termination)**: §10. New internal keys, their aliases, and one remedy rewrite. This is a successor
  of S10/S10b's registered text, in S10b's form.
- **Part S (schema)**: §11, **NSS-TSR1-S1**. One narrow native-schema successor: a spelling for the project root.

**Short names.** NE = `docs/v2/contracts/product-v1/native-evidence.md`. MB14a = M3-B item 14a
(`config-discovery-b/PROPOSAL.md`:605-700, r10). MC10 = M3-C item 10 (`snapshot-plan-c/PROPOSAL.md`:556-575).
NS = product `schemas/sources/native-v2.schema.json`. NM = `native_evidence_model.v2.py`. TS = TypeScript 6.0.3 (§0).
`fold` = NE §2.4's fold (full, non-tailored default lowercase, UCD 15.0.0).

A **path** is project-relative and canonical (no leading `/`; no `.`, `..` or empty segment); `""` is the project
root. `D(N)` is the directory of graph node `N`, and `E` is the entry node. "Written" means present as a member of a
node's JSON object, whatever its value. "Evidence" means the files under `work/evidence/` (interpretation evidence
only: TypeScript 6.0.3's own code run in memory on synthetic inputs; never a product run, release qualification or
runtime control).

## r4 changes (round 3: `REVIEW-r3.md`, REQUIRED-FINDINGS; all round-2 findings resolved)

| Finding | r4 change |
|---|---|
| R3-RF-1 | R-1.9: the rebased-path length limit moves from the every-write group to the **winning materialized** values. §7: a phase-3c length row follows the winning-`paths` containment row, and precedes the collection counts. The every-write element and pattern limits (phase 3a) are unchanged. Control TSR1-C29 gains the four requested cases. |
| R3-NB-1 | R-3.6's table ends at its third cell. The default-exclusion sentence is its own paragraph, and the Controls line names TSR1-C31. |

## r3 changes (round 2: `REVIEW-r2.md`, REQUIRED-FINDINGS; all round-1 findings resolved)

| Finding | r3 change |
|---|---|
| R2-RF-1 | R-4.7: one visited-directory set is shared by every base, keyed by canonical snapshot directory (`_tsc.js`:18533-18542). Witness `r2rf1_visited`. |
| R2-RF-2 | R-4.4: every extension predicate, and R-4.8's `change`, operates on the rooted subject `/` + path. Witnesses `r2rf2_*`. |
| R2-RF-3 | R-3.6: "four S rows". Stripping suppresses only the output-to-input remap; ordinary resolution, extension substitution included, continues. Witness `measured-output-remap-r3-6.0.3.json`, and control TSR1-C31. |
| R2-RF-4 | R-1.8 separates grammar (empty strings: `option-malformed`) from length. R-1.9 enumerates the per-write length limits and the winning-collection counts. §7 adds ordered phase-3a/3c rows. Control TSR1-C29. |
| R2-RF-5 | R-10.3's clause adds non-empty `types`/`customConditions` elements of at most 4,096 characters, non-empty `paths` patterns, and a `package.json` object root. Control TSR1-C30. |
| R2-NB-1 | The reference's JSONC removes trailing commas only outside strings and comments. Witness `r2nb1_comma_in_string`. |
| R2-NB-2 | `diff/compare.py` asserts: identical case sets, no unexpected refusal, and exactly one declared difference. Exit 1 otherwise. The reference states its coverage. |
| R2 §2 scope note | R-3.2: "never read" is TSR-1's selected behaviour (TypeScript parses referenced configurations before its guard). A no-root array's contents are ignored, not validated. |

The differential is now **39 cases** (`diff/cases.json`, including every round-1 and round-2 witness).
`diff/compare.py oracle-ts-6.0.3.json ref-tsr1-r3.json` prints `PASS: 39 cases, 18 fields, 1 declared difference`.

## r2 changes (round 1: `REVIEW-r1.md`, Codex `codex-tsr1-r1`, REQUIRED-FINDINGS)

| Finding | r2 change |
|---|---|
| RF-1 | `moduleDetection`, `isolatedModules` and `verbatimModuleSyntax` move from S to **P** (R-3.1). Each changes program membership through the synthetic-import guard (`_tsc.js`:124077-124092, :17973-17992). |
| RF-2 | Top-level `references` is **P**, not S (R-3.2). It is admitted absent, as `[]`, or as any array when there are no roots. The evidence is `_tsc.js`:122785-122812 (`if (rootNames.length)`) and `measured-references-r2-6.0.3.json`. |
| RF-3 | R-1.5 has two separate branches, a template branch and an ordinary branch, with exact results for the measured inputs. |
| RF-4 | R-4.8–R-4.9 replace the symmetric priority rule with TypeScript's ordered-map algorithm over its include-grouped stream. |
| RF-5 | R-4.3: an empty `include`/`exclude` string is dropped before rebasing. R-4.6: the matcher runs over UTF-16 code units. R-4.8: JSON roots keep the stream's include grouping. |
| RF-6 | The lib-expansion evidence is re-measured with a non-empty root and a confined host, recording the file lists (`measured-lib-expansion-r2-6.0.3.json`). TSR1-C11 checks the assertions. The vacuous r1 file is withdrawn. |
| RF-7 | R-3.3: the name grammar is 1–256 characters. The empty name refuses. |
| RF-8 | §7 is a total refusal table, with attribution for aggregates and ties. R-10.3 gives one exact remedy string naming every new limit. |
| RF-9 | R-11.6 names the exact-source admission pins (`crates/identity/src/schema_registry.rs`, `schemas/registry.json`, `schemas/source-map.json`, `tools/contracts/generator-closure.json`). |
| RF-10 | R-11.1–R-11.3 pin the actual selected parent (`native-owner-patterns-source-r1/sources/native-v2.schema.json`, `7179d52e…`). The model's older copy gets a separately pinned local delta. |
| NB-1 | R-1.6: a winning `es3` write masks an inherited `target`. |
| NB-2 | §15 lists every restriction. R-4.2 separates pruning from read-set membership. The identity promise is qualified. |
| NB-3 | R-5.2 drops the release-history claim. |
| NB-4 | P-0.1 cites `_tsc.js`:18175-18180 (expression :18178), NE:527-546 and :548-565, and narrows the `extends` sentence. |
| Coordinator conditions | Folded in: P-0.1 (NE unchanged, with 6.0.3 parity) and §11 (Part S identity, scope, widening, encoding, obligations). |

r2 also added a **differential reference** (r3 extends it to 39 cases): `work/evidence/diff/tsr1_ref.py` implements §§1, 2 and 4 over a reduced
graph, and `diff/ts_oracle.cjs` runs TypeScript 6.0.3 in memory over the same 33 cases. They agree on every compared
field in all 33. The one difference is R-2.2's intended de-duplication of a repeated `lib` name, in case
`node16lib` (`diff/compare.py`).

---

## 0. The profile, its key and its custody

**P-0.1 One pinned compiler.** Profile **`tsr1.v1`** has exactly one row, for TypeScript **6.0.3**. That is the
compiler the product's TypeScript provider selects (`providers/typescript/package.json`:13). Its interpretation
evidence is the npm archive `typescript-6.0.3.tgz`, sha256
`33cd0ee1beaa8c9e9d15a9da836c62ddea4c34a42d7c2d349dbc80d94165d22a`, whose `lib/_tsc.js` has sha256
`1c59e77a54b186ec43fa7f3e0d3c4bb15ca5eb5ba43e96b1d3a267139eddd3e3` and whose `lib/typescript.js` has sha256
`569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39`. Citations `_tsc.js:N` are to that file.

- **The rules below are the law.** The pinned source is the evidence they were taken from and measured against. If a
  disagreement between them is later found, it is a TSR-1 defect, corrected by a successor; neither side silently
  wins.
- **TSR-1 does not change NE:527-546 or NE:548-565.** Effective `allowJs` and `checkJs`, the jsconfig-supplied
  `allowJs`, the two universe flags, the explicit-`false` rule and "this law introduces no compiler-option diagnostic
  refusal" all stand as published. TSR-1 applies them.
  - NE:545 cites TypeScript v5.6.3's computed option `allowJs`: an unwritten `allowJs` is `!!checkJs`, and a written
    value wins, including `false`. TypeScript 6.0.3 computes it identically, at `_tsc.js`:18175-18180, with the
    expression at :18178:
    `compilerOptions.allowJs === void 0 ? !!compilerOptions.checkJs : compilerOptions.allowJs`.
  - NE's jsconfig supply is 6.0.3's `getDefaultCompilerOptions` (`_tsc.js`:39507-39510), applied to every file whose
    basename is exactly `jsconfig.json`. Inheritance (own options beat bases; a later `extends` entry beats an earlier
    one) is the `assign` order at `_tsc.js`:39274-39330.
  - Measured (evidence `diff/`, cases `jsc`, `ts_extends_jsconfig`, `jsconfig_base_allowjs_false`, and the reviewer's
    five discriminators in `REVIEW-r1.md` §9.1): no difference was found.
  - **What TSR-1 adds beside these rules, not to them:**
    - R-1.4: the same jsconfig mechanism supplies four other values.
    - R-1.2: `null` refuses. For `allowJs`/`checkJs` that is MB14a's existing rule.
- **MB14a is unchanged.** Its selected graph grammar and candidate resolution remain as published. The
  own-options/later-base inheritance used by that graph agrees with TypeScript 6.0.3 at the cited `assign` sites. This
  does not claim that MB14a implements every upstream `extends` resolution behaviour; MB14a omits `package.json`
  `exports` and `tsconfig` evaluation by design.

**P-0.2 The key, and refusal outside it.** The profile row is selected by the admitted compiler closure's
`semanticVersion`, the same value as `toolchain.compilerVersion` (NE:1481).
- The row requires `compilerVersion = "6.0.3"`, and an admitted `kind=stdlib` closure whose `semanticVersion` is also
  `"6.0.3"`.
- Any other compiler version refuses `native.typescript-profile-compiler-unsupported:<compilerVersion>`.
- A stdlib closure of another version refuses `native.typescript-profile-stdlib-version-mismatch:<semanticVersion>`.
- Both refusals happen before PlanId. Nothing is guessed from a nearby version.

**P-0.3 Custody.** Every table in TSR-1 is **source-pinned host data**: product source, keyed by the profile row, under
the same discipline as the basename table (`x-opensip-config-node-kind-law`). Each table is generated from the pinned
archive by the evidence scripts in `work/evidence/`, and checked against them by C2b-1b's controls.
- No table is read from a compiler, a toolchain tree, the environment or a worker. MC10's "pinned data taken from the
  selected compiler closure, so the resolver reads no compiler at run time" is met this way: the data is taken from the
  pinned compiler release, and is keyed by the version of the admitted closure that carries it.
- No new signed tree member, manifest field or release-format change is needed.
- A row is immutable once bound. A correction is a new successor, and it is a disclosed identity change, as a
  synthesizer change is (NE:1428).

**P-0.4 Effect on PlanId (applies to every section).** TSR-1 adds no field, record, domain or digest. Every value it
fixes is a value of an existing field:
- in the context: `configProjection.honoredOptions`, `configProjection.strippedOptions`, `toolchain.libSelection`,
  `toolchain.compilerPackageDigest`, `toolClosure.compiler`, `toolClosure.runtime`, `packageModuleType`,
  `lockfileIdentity`;
- in the universe: `programRootFiles`, `jsRootFiles`, `lockfileKind`.

So each enters `nativeContextId` or the universe identity, and reaches `PlanId` through `plan.nativeContextDigests` and
the universe. A different value is a different identity, never a tolerated difference.

**P-0.5 When it runs.** The host resolved-inputs adapter applies TSR-1 before PlanId (MC10). It runs after MB14a's
graph has been read and admitted, over the same function's retained graph. MB14a's discovery refusals, reading,
bounds and graph are unchanged. TSR-1 reads more members of the same retained files. The worker's independent
recomputation (NE:1618-1620) applies TSR-1 too, so a host that departs from it is caught as
`Unavailable(native-context-mismatch)`.

---

## 1. X-C2B1-1 — the effective honored options

**R-1.1 What is read.** From every node of the admitted graph:
- every member of `compilerOptions`;
- the top-level members `files`, `include`, `exclude`, `references`, `typeAcquisition`, `watchOptions` and
  `compileOnSave`.

Other top-level members are not compiler configuration. TypeScript 6.0.3 ignores them, and TSR-1 neither reads nor
lists them. MB14a's JSONC grammar applies, including "a duplicate key keeps its last value". `compilerOptions` member
names are matched **exactly and case-sensitively**, as TypeScript's tsconfig option map does (`_tsc.js`:38380-38382).
For example, `AllowJs` is an unknown name (§3).

**R-1.2 Types and `null`.** Each H (honored) and P (pinned) member, wherever it is written, must have the JSON type of
its row below.
- `null` is not admitted for any H or P member.
- A wrong type or a `null` refuses `native.typescript-profile-option-malformed`.
- This follows MB14a, which already refuses a wrong-typed or `null` `allowJs`/`checkJs`. It is a stated departure from
  TypeScript, which treats `null` as "unset the inherited value" (measured case `nulls`).
- An S (stripped) member's value is never inspected (§3).

**R-1.3 Inheritance.** Each option's effective value is the value of its **winning write**. Winning follows NE:527-546's
inheritance rule, which is TypeScript's `assign` order (`_tsc.js`:39274-39330):
- `eff(N)` starts empty;
- for each entry of `N.extendsResolved`, in order, repetitions included, every option of `eff(base)` overwrites;
- then every option `N` writes overwrites.

The value at `E` is the effective configuration. Each write keeps its declaring node, so path values are rebased by the
node that wrote them (R-1.5).

**R-1.4 What a jsconfig node supplies (X-TSR1-B).** A node whose `kind` is `jsconfig` (the basename law) supplies these
five values as if written in that node, unless the node writes them itself:
- `allowJs: true` (NE:527-546, unchanged);
- `allowSyntheticDefaultImports: true`;
- `skipLibCheck: true`;
- `noEmit: true`;
- `maxNodeModuleJsDepth: 2`.

This is TypeScript's `getDefaultCompilerOptions` (the function before `_tsc.js`:39511; measured case `jsc`). A
supplied value is never "written" for §3's presence rule.

**R-1.5 Path rebasing.** One rule applies to every path-valued string TSR-1 reads: `baseUrl`, each `rootDirs` element,
each `paths` substitution, each `files`/`include`/`exclude` entry (with R-4.3's treatment of empty specs), and §4's
use of `outDir`/`declarationDir`. Let `v` be the written string and `N` its declaring node.

1. **Grammar.** `v` must not contain NUL, a backslash, or a character below U+0020. A violation refuses
   `native.typescript-profile-option-malformed` (for a spec entry, `native.typescript-profile-spec-malformed`).
2. **Template branch.** If `v` begins with exactly `${configDir}`:
   - replace that prefix with `./`, as TypeScript does (`_tsc.js`:39217-39219);
   - join the result to `D(E)`, the **entry's** directory, whichever node wrote `v`;
   - normalize (step 4).

   Steps 3's rootedness test and base selection are not applied. In particular a `paths` substitution in this branch
   ignores `baseUrl`, because TypeScript makes it absolute before resolution. If `v` begins with a string that equals
   `${configDir}` only case-insensitively, it refuses as malformed: TypeScript detects the prefix case-insensitively
   (`_tsc.js`:39209-39216) but replaces it case-sensitively, and TSR-1 does not reproduce that.
3. **Ordinary branch** (every other `v`).
   - **Rooted.** If `v` is rooted, it refuses `native.typescript-profile-path-outside-project`. Rooted means: `v`
     begins with `/`, or matches `^[A-Za-z]:` or `^[A-Za-z][A-Za-z0-9+.-]*://`.
   - **The base `B`.** For a `paths` substitution: the effective `baseUrl` when it is non-null, otherwise `D` of the node
     whose `paths` write won (`pathsBasePath`, `_tsc.js`:16595-16599, :39280-39283). For everything else: `D(N)`, so an
     inherited `files`/`include`/`exclude` entry is relative to the base that wrote it (`_tsc.js`:39306-39314).
   - Join `v` to `B`. An empty `v` denotes `B` itself.
4. **Normalization.** Split on `/`; drop empty and `.` segments; `..` removes the preceding segment. A `..` that rises
   above the project root refuses `native.typescript-profile-path-outside-project`. The result is a path, or `""` for
   the root (Part S). `*` and `?` are ordinary characters here; only §4 gives them meaning.

**Exact results** (measured case `cfgdir_rf3`, where `app/tsconfig.json` extends `cfg/base.json`):

| Written in `cfg/base.json` | Result |
|---|---|
| `baseUrl: "${configDir}/src"` | `app/src` |
| `rootDirs: ["${configDir}/gen", "${configDir}"]` | `["app/gen", "app"]` |
| `paths: {"@/*": ["${configDir}/src/*"]}` (with a `baseUrl` in effect) | `app/src/*` (the base is not applied) |
| `include: ["${configDir}/src"]` | the spec `app/src` |
| `"${configDir}"`, with a root entry `tsconfig.json` | `""` |
| `"${configDir}/../.."`, from `app/tsconfig.json` | refuses `path-outside-project` |
| `"${CONFIGDIR}/src"` | refuses `option-malformed` |

**R-1.6 The value tables.** An enumerated value matches by `fold` of the written string, as TypeScript's
`toLowerCase` lookup does (`_tsc.js`:39593-39602), with no trimming. It is recorded as the canonical spelling below. A
string outside the table refuses `native.typescript-profile-option-value-unsupported`; a non-string refuses
`native.typescript-profile-option-malformed`.

| Option | Admitted folded values → canonical | Source |
|---|---|---|
| `target` | `es3` (see below); `es5`; `es6`→`es2015`; `es2015` … `es2025` (each to itself); `esnext` | `_tsc.js`:36819-36849 |
| `module` | `none` `commonjs` `amd` `system` `umd`; `es6`→`es2015`; `es2015` `es2020` `es2022` `esnext` `node16` `node18` `node20` `nodenext` `preserve` | `_tsc.js`:36850-36880 |
| `moduleResolution` | `node`→`node10`; `node10` `classic` `node16` `nodenext` `bundler` | `_tsc.js`:37337-37355 |
| `jsx` | `preserve` `react-native` `react-jsx` `react-jsxdev` `react` | `_tsc.js`:36983 |

**`es3`.** A winning `es3` write is an ordinary winning write: it masks any inherited `target`. Only the post-merge
computation then treats the target as absent, because TypeScript computes `ES3` as `undefined`
(`_tsc.js`:18011-18016). So `es3` over a base writing `es5` gives effective `target` `es2025` (measured case
`nb1_es3_masks`).

**Deprecated values** (`target: es5`; `module: none/amd/system/umd`; `moduleResolution: node10/classic`) are admitted
with their meaning. TypeScript 6.0.3 reports them as deprecation errors but still applies them
(`_tsc.js`:125170-125240), and TSR-1 introduces no refusal for a compiler diagnostic, in the sense of NE:557-565.

**R-1.7 The defaulting chain (unwritten values), in order** (`_tsc.js`:18004-18265; measured):

| Option | Effective value when unwritten (or computed) |
|---|---|
| `target` | `es2025` |
| `module` | from the effective `target`: `esnext`→`esnext`; `es2022`–`es2025`→`es2022`; `es2020`, `es2021`→`es2020`; `es2015`–`es2019`→`es2015`; `es5`→`commonjs` |
| `moduleResolution` | from the effective `module`: `none` `amd` `umd` `system`→`classic`; `nodenext`→`nodenext`; `node16` `node18` `node20`→`node16`; otherwise (`commonjs` `es2015` `es2020` `es2022` `esnext` `preserve`)→`bundler` |
| `esModuleInterop` | `true` |
| `allowSyntheticDefaultImports` | `true` |
| `strict` | `true`: effective `strict` is `false` exactly when its winning write is `false` |
| `skipLibCheck` | `false`, or `true` when supplied by R-1.4 |
| `resolveJsonModule` | `true` when the effective `module` is `node20` or `nodenext`; otherwise `true` exactly when the effective `moduleResolution` is `bundler`; otherwise `false` |
| `checkJs` | `false` |
| `allowJs` | NE:527-546 (R-1.4 supplies `true` from a jsconfig node; otherwise the effective `checkJs`) |
| `types` | `[]` (`_tsc.js`:40294-40297) |
| `lib` | §2's T-DEF row for the effective `target` |
| `baseUrl` | `null` |
| `paths`, `rootDirs`, `customConditions` | `[]` |
| `jsx` | `null` |
| `noEmit` | `true`, always (NS: `const true`) |

**R-1.8 Materializing each honored field.** `honoredOptions` is exactly these 18 fields:
- **Booleans** (`allowJs`, `checkJs`, `strict`, `skipLibCheck`, `resolveJsonModule`, `allowSyntheticDefaultImports`,
  `esModuleInterop`): a write must be a JSON boolean. The effective value is per R-1.3, R-1.4 and R-1.7.
- **`noEmit`**: a write must be a boolean. The honored value is always `true`. A winning write of `false` is disclosed
  in `strippedOptions` as `{noEmit, emits-output}`, because the analysis never emits.
- **`target`, `module`, `moduleResolution`, `jsx`**: a write must be a string. Values follow R-1.6, and unwritten
  values R-1.7. `moduleResolutionMode` equals `moduleResolution` (NE:1600-1601).
- **`lib`**: §2.
- **`types`, `customConditions`**: a write must be an array of non-empty strings (R-1.9 limits their length). They
  are kept as written: no fold and no rebasing. A repeated element keeps its first occurrence. `types` may contain
  `"*"`, which is retained literally; TypeScript expands it at analysis time over the retained layout.
- **`baseUrl`**: a write must be a string. It is rebased per R-1.5; an empty string denotes `D(N)`. Otherwise `null`.
- **`rootDirs`**: a write must be an array of strings. Each element is rebased per R-1.5. A repeated result keeps its
  first occurrence.
- **`paths`**: a write must be an object.
  - Each member name is a pattern: non-empty, with at most one `*` (R-1.9 limits its length).
  - Each member value is a non-empty array of strings, each with at most one `*`.
  - Each substitution is rebased per R-1.5.
  - The `paths` array lists the members in ECMAScript own-property order of the parsed object, which is what
    TypeScript iterates: array-index names (`0`…`4294967294` in canonical decimal) ascending numerically first, then the
    other names in first-occurrence order. A duplicate name keeps its first position and its last value.
  - The whole object of the winning write is used. Objects from different nodes are never merged by member.
  - Any departure from this shape refuses `native.typescript-profile-option-malformed`. A length limit of R-1.9 is not
    shape.

**R-1.9 Bounds.** The schema bounds are refusals, never truncations. Each refuses `native.typescript-profile-bound`,
with §7's attribution. Lengths count characters as Unicode scalar values (JSON Schema string length).
- **Per-write length limits** apply to **every** write, overridden or not:
  - a `types` or `customConditions` element: at most 4,096 characters;
  - a `paths` pattern: at most 1,024 characters.
- **Winning path lengths** apply to the materialized honored value only, after its containment is established. An
  overridden write's paths are never rebased for length. Each of these is at most 4,096 characters, checked in this
  order: `baseUrl`; each `rootDirs` element; each `paths` substitution (entries in order, substitutions in order).
- **Winning-collection counts** apply to the materialized honored value: `lib` ≤ 64; `types` ≤ 1,024;
  `customConditions` ≤ 64; `rootDirs` ≤ 1,024; `paths` ≤ 4,096 entries, each with at most 64 substitutions. A `paths`
  entry with no substitution is shape, not a count.

**R-1.10 The synthesized profile completed.** Under `js-synthesized` (NE:1422-1428), `SynthesizedCompilerOptionsV1` is
unchanged. The honored fields it omits are computed by R-1.7 from its values, as if they were written:
- `lib` = T-DEF[`es2022`];
- `baseUrl` = `null`; `paths` = `rootDirs` = `customConditions` = `[]`;
- `resolveJsonModule` = `false` (`module=node16`, `moduleResolution=node16`);
- `allowSyntheticDefaultImports` = `esModuleInterop` = `true`;
- `jsx` = `null` unless the synthesizer set `preserve`.

`strippedOptions` is `[]` and `configGraphPaths` is `[]`.

**Controls (§1):** TSR1-C1 to TSR1-C8 (§13).

---

## 2. X-C2B1-2 — the `lib` canonicalization table, the target-default table, and materialization (LD-Q-4(b))

**R-2.1 Why canonicalize (X-TSR1-E).** NE's join is `component(n) = "lib." + fold(n) + ".d.ts"`. TypeScript maps a
written name through its `libMap` (`_tsc.js`:36426-36542), and for 12 names that map is not `lib.<name>.d.ts`. A name
therefore enters `honoredOptions.lib` only in **canonical** form: the stem of the file TypeScript would load. NE's join
then selects exactly TypeScript's file, and NE's join and admission are unchanged.

**R-2.2 Materializing `honoredOptions.lib`** (the value C2b-1b hands to C2b-1a):
1. **Written** (the winning write is an array of strings): map each element `x` to `T-LIB[fold(x)]`.
   - A key absent from T-LIB refuses `native.typescript-profile-option-value-unsupported` (for example `es2025.full`,
     which is a file, not a written name).
   - A repeated canonical name keeps its first occurrence, because `lib` is `uniqueItems`. TypeScript keeps the
     repeat but loads the file once (case `node16lib`), so the effective library is the same.
   - The sequence is kept in written order.
   - An empty array refuses `native.typescript-profile-option-value-unsupported`. TypeScript would load no library at
     all, and the closed record requires a non-empty list (NE:1606).
   - A non-array, or a non-string element, refuses `native.typescript-profile-option-malformed`.
2. **Unwritten:** the T-DEF row for the effective `target`, in the row's order.
3. **`toolchain.libSelection`** is the same set of names, sorted by UTF-8 bytes (NE:1600-1608). Canonical names are
   lower-case ASCII, so `fold` is the identity on them and NE's agreement holds by construction.

**R-2.3 Why the default is a list (X-TSR1-D).** TypeScript's default is one aggregator file (`getDefaultLibFileName`,
`_tsc.js`:11255-11274). Every aggregator in the 6.0.3 tree holds only `/// <reference lib>` directives, and their
targets are already canonical names. T-DEF records those directives in file order.
- A 6.0.3 program given T-DEF's list loads exactly the declaration files that the omitted-`lib` default loads, minus
  the declaration-free aggregator itself. This was measured for all 13 targets with a non-empty root and a confined
  host, file lists recorded and in order (`work/evidence/measured-lib-expansion-r2-6.0.3.json`; TSR1-C11).
- The single-file spelling was rejected. `es5`'s default, `lib.d.ts`, has no `lib.<name>.d.ts` name, and
  `es2025.full` is not a name TypeScript accepts in `lib`, so a worker could not pass it back to the compiler.
- Two repositories, one omitting `lib` and one writing the same list, mint one context, because their effective
  library is one.

**R-2.4 The tables.** T-LIB has 107 rows; T-DEF has 13 (`es3` computes as unwritten and `es6` is canonical `es2015`,
so neither has a row).

<!-- generated by work/evidence/lib_tables.py from TypeScript 6.0.3 libMap, targetToLibMap and lib files -->
**T-LIB (lib name canonicalization).** Key = `fold(written)`; value = canonical name `c` (so `component(c)` is TypeScript's own file).

| Written name (folded) | Canonical name |
|---|---|
| `es5` | `es5` |
| `es6` | `es2015` |
| `es2015` | `es2015` |
| `es7` | `es2016` |
| `es2016` | `es2016` |
| `es2017` | `es2017` |
| `es2018` | `es2018` |
| `es2019` | `es2019` |
| `es2020` | `es2020` |
| `es2021` | `es2021` |
| `es2022` | `es2022` |
| `es2023` | `es2023` |
| `es2024` | `es2024` |
| `es2025` | `es2025` |
| `esnext` | `esnext` |
| `dom` | `dom` |
| `dom.iterable` | `dom.iterable` |
| `dom.asynciterable` | `dom.asynciterable` |
| `webworker` | `webworker` |
| `webworker.importscripts` | `webworker.importscripts` |
| `webworker.iterable` | `webworker.iterable` |
| `webworker.asynciterable` | `webworker.asynciterable` |
| `scripthost` | `scripthost` |
| `es2015.core` | `es2015.core` |
| `es2015.collection` | `es2015.collection` |
| `es2015.generator` | `es2015.generator` |
| `es2015.iterable` | `es2015.iterable` |
| `es2015.promise` | `es2015.promise` |
| `es2015.proxy` | `es2015.proxy` |
| `es2015.reflect` | `es2015.reflect` |
| `es2015.symbol` | `es2015.symbol` |
| `es2015.symbol.wellknown` | `es2015.symbol.wellknown` |
| `es2016.array.include` | `es2016.array.include` |
| `es2016.intl` | `es2016.intl` |
| `es2017.arraybuffer` | `es2017.arraybuffer` |
| `es2017.date` | `es2017.date` |
| `es2017.object` | `es2017.object` |
| `es2017.sharedmemory` | `es2017.sharedmemory` |
| `es2017.string` | `es2017.string` |
| `es2017.intl` | `es2017.intl` |
| `es2017.typedarrays` | `es2017.typedarrays` |
| `es2018.asyncgenerator` | `es2018.asyncgenerator` |
| `es2018.asynciterable` | `es2018.asynciterable` |
| `es2018.intl` | `es2018.intl` |
| `es2018.promise` | `es2018.promise` |
| `es2018.regexp` | `es2018.regexp` |
| `es2019.array` | `es2019.array` |
| `es2019.object` | `es2019.object` |
| `es2019.string` | `es2019.string` |
| `es2019.symbol` | `es2019.symbol` |
| `es2019.intl` | `es2019.intl` |
| `es2020.bigint` | `es2020.bigint` |
| `es2020.date` | `es2020.date` |
| `es2020.promise` | `es2020.promise` |
| `es2020.sharedmemory` | `es2020.sharedmemory` |
| `es2020.string` | `es2020.string` |
| `es2020.symbol.wellknown` | `es2020.symbol.wellknown` |
| `es2020.intl` | `es2020.intl` |
| `es2020.number` | `es2020.number` |
| `es2021.promise` | `es2021.promise` |
| `es2021.string` | `es2021.string` |
| `es2021.weakref` | `es2021.weakref` |
| `es2021.intl` | `es2021.intl` |
| `es2022.array` | `es2022.array` |
| `es2022.error` | `es2022.error` |
| `es2022.intl` | `es2022.intl` |
| `es2022.object` | `es2022.object` |
| `es2022.string` | `es2022.string` |
| `es2022.regexp` | `es2022.regexp` |
| `es2023.array` | `es2023.array` |
| `es2023.collection` | `es2023.collection` |
| `es2023.intl` | `es2023.intl` |
| `es2024.arraybuffer` | `es2024.arraybuffer` |
| `es2024.collection` | `es2024.collection` |
| `es2024.object` | `es2024.object` |
| `es2024.promise` | `es2024.promise` |
| `es2024.regexp` | `es2024.regexp` |
| `es2024.sharedmemory` | `es2024.sharedmemory` |
| `es2024.string` | `es2024.string` |
| `es2025.collection` | `es2025.collection` |
| `es2025.float16` | `es2025.float16` |
| `es2025.intl` | `es2025.intl` |
| `es2025.iterator` | `es2025.iterator` |
| `es2025.promise` | `es2025.promise` |
| `es2025.regexp` | `es2025.regexp` |
| `esnext.asynciterable` | `es2018.asynciterable` |
| `esnext.symbol` | `es2019.symbol` |
| `esnext.bigint` | `es2020.bigint` |
| `esnext.weakref` | `es2021.weakref` |
| `esnext.object` | `es2024.object` |
| `esnext.regexp` | `es2024.regexp` |
| `esnext.string` | `es2024.string` |
| `esnext.float16` | `es2025.float16` |
| `esnext.iterator` | `es2025.iterator` |
| `esnext.promise` | `es2025.promise` |
| `esnext.array` | `esnext.array` |
| `esnext.collection` | `esnext.collection` |
| `esnext.date` | `esnext.date` |
| `esnext.decorators` | `esnext.decorators` |
| `esnext.disposable` | `esnext.disposable` |
| `esnext.error` | `esnext.error` |
| `esnext.intl` | `esnext.intl` |
| `esnext.sharedmemory` | `esnext.sharedmemory` |
| `esnext.temporal` | `esnext.temporal` |
| `esnext.typedarrays` | `esnext.typedarrays` |
| `decorators` | `decorators` |
| `decorators.legacy` | `decorators.legacy` |

**T-DEF (target-default lib list).** Key = effective canonical `target`; value = the `lib` list, in order.

| Effective `target` | TypeScript default file | Materialized `honoredOptions.lib` |
|---|---|---|
| `es5` | `lib.d.ts` | `["es5", "dom", "webworker.importscripts", "scripthost"]` |
| `es2015` | `lib.es6.d.ts` | `["es2015", "dom", "dom.iterable", "webworker.importscripts", "scripthost"]` |
| `es2016` | `lib.es2016.full.d.ts` | `["es2016", "dom", "webworker.importscripts", "scripthost", "dom.iterable"]` |
| `es2017` | `lib.es2017.full.d.ts` | `["es2017", "dom", "webworker.importscripts", "scripthost", "dom.iterable"]` |
| `es2018` | `lib.es2018.full.d.ts` | `["es2018", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2019` | `lib.es2019.full.d.ts` | `["es2019", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2020` | `lib.es2020.full.d.ts` | `["es2020", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2021` | `lib.es2021.full.d.ts` | `["es2021", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2022` | `lib.es2022.full.d.ts` | `["es2022", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2023` | `lib.es2023.full.d.ts` | `["es2023", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2024` | `lib.es2024.full.d.ts` | `["es2024", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `es2025` | `lib.es2025.full.d.ts` | `["es2025", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |
| `esnext` | `lib.esnext.full.d.ts` | `["esnext", "dom", "webworker.importscripts", "scripthost", "dom.iterable", "dom.asynciterable"]` |

**Custody and effect.** P-0.3 and P-0.4. A name T-LIB admits whose component the admitted stdlib tree lacks still
refuses through NE's existing `native.native-context-lib-not-retained:<n>`.

**Controls:** TSR1-C9 to TSR1-C11.

---

## 3. X-C2B1-3 — the closed option classification and `strippedOptions`

**R-3.1 Three classes, one table.** Every `compilerOptions` member name TypeScript 6.0.3 declares (128 names, evidence
`ts-6.0.3-option-declarations.json`) is in exactly one class.

- **H — honored**: the 18 `honoredOptions` fields (§1).
- **P — pinned**: an option that changes module resolution or program membership in 6.0.3, has no honored field, and
  has no strip reason that describes it truthfully.
  - The option may be unwritten, or written only with a value its row admits.
  - Any other written value, wherever written, refuses `native.typescript-profile-option-unsupported:<option>`.
  - An admitted P write is neither honored nor stripped. Its effect equals the unwritten effect, which is the effect
    the analysis applies. So in every admitted context, resolution and membership are determined by the honored
    options, R-3.6's stated consequences apart.
  - There are 14 P options. The three r2 additions, `isolatedModules`, `verbatimModuleSyntax` and `moduleDetection`,
    change membership through the synthetic-import guard: a non-declaration script file receives the implicit JSX
    runtime import (and the `tslib` import) only when it is a module or `getIsolatedModules` holds
    (`_tsc.js`:124077-124092), and `moduleDetection` decides which files are modules (`_tsc.js`:17973-17992).
    Measured in `REVIEW-r1.md` RF-1: each adds `node_modules/react/jsx-runtime.d.ts` to a one-script program.
- **S — stripped**: the option is removed and disclosed with the reason in its row. The reason is a true description
  of the option, decided by its name alone; the value is never inspected, except as R-4.3 reads `outDir` and
  `declarationDir`.

**Unknown names.** Names TypeScript 6.0.3 does not declare (typos, options of other versions, any case variant) are S
with `not-a-resolution-or-membership-option`. That is true of the pinned compiler, which ignores them; refusing them
would be a refusal on TypeScript diagnostic 5023.

**R-3.2 Top-level members.**

| Member | Class and rule |
|---|---|
| `files`, `include`, `exclude` | read by §4; never listed |
| `references` | **P.** Admitted: unwritten; `[]`; or any JSON array when `programRootFiles` (§4) is empty, as in a solution configuration such as `{"files": [], "references": [...]}`. A non-array refuses `option-malformed:references`; any other array refuses `option-unsupported:references`. Under TSR-1 the reference graph is never read, and a no-root array's contents are ignored, not validated. That is TSR-1's selected behaviour; TypeScript itself parses referenced configurations before its guard (`_tsc.js`:122788-122792), and the evidence shows equal source membership, not equal read sets or diagnostics. Evidence: `_tsc.js`:122785-122812 adds referenced outputs or sources only `if (rootNames.length)`. Measured (`measured-references-r2-6.0.3.json`): with a root, a `module: none` reference with `outFile` adds `dist/ref.d.ts`; with no roots it adds nothing. |
| `compileOnSave` | S, `emits-output` |
| `typeAcquisition` | S, `acquires-types-from-the-network` (NE's `typeAcquisitionEnabled` is `false`) |
| `watchOptions` | S, `not-a-resolution-or-membership-option` |

Other top-level members are not compiler configuration. TypeScript ignores them, and TSR-1 neither reads nor lists
them.

**R-3.3 `strippedOptions`.**
- **Presence.** One row for each S name written in at least one graph node, whatever its value and whichever node
  wrote it (an overridden write still counts). Plus R-1.8's `noEmit` row.
- **Never listed.** An option no node writes, and a jsconfig-supplied value.
- **Name grammar.** A name that becomes a row must be 1 to 256 characters, counted as Unicode scalar values (JSON
  Schema string length; NS `TypeScriptStrippedOptionV1.option`).
  - The empty name (`{"compilerOptions": {"": true}}`) refuses `native.typescript-profile-option-malformed`, with
    member `""`.
  - A longer name refuses `native.typescript-profile-bound:strippedOptions`.
  - No unrepresentable name is dropped silently.
- **Order.** Rows are unique by `(option, reason)` and sorted by UTF-8 bytes of `option`, then of `reason`.
- **Count.** More than 256 rows refuses `native.typescript-profile-bound:strippedOptions`.
- **Synthesized.** Under `js-synthesized`, `strippedOptions = []`.

**R-3.4 Reasons not used at v1.** `reads-the-environment` names no 6.0.3 option. It remains available to a later row.

**R-3.5 The table** (`compilerOptions` members):

<!-- generated by work/evidence/classify_options.py from TypeScript 6.0.3 declarations; 128 names -->
| `compilerOptions` member | Class | Rule |
|---|---|---|
| `all` | S | `not-a-resolution-or-membership-option` |
| `allowArbitraryExtensions` | P | pinned; admitted written values: `false` |
| `allowImportingTsExtensions` | S | `not-a-resolution-or-membership-option` |
| `allowJs` | H | honored (TSR-1 §1) |
| `allowSyntheticDefaultImports` | H | honored (TSR-1 §1) |
| `allowUmdGlobalAccess` | S | `not-a-resolution-or-membership-option` |
| `allowUnreachableCode` | S | `not-a-resolution-or-membership-option` |
| `allowUnusedLabels` | S | `not-a-resolution-or-membership-option` |
| `alwaysStrict` | S | `not-a-resolution-or-membership-option` |
| `assumeChangesOnlyAffectDirectDependencies` | S | `not-a-resolution-or-membership-option` |
| `baseUrl` | H | honored (TSR-1 §1) |
| `charset` | S | `not-a-resolution-or-membership-option` |
| `checkJs` | H | honored (TSR-1 §1) |
| `composite` | S | `emits-output` |
| `customConditions` | H | honored (TSR-1 §1) |
| `declaration` | S | `emits-output` |
| `declarationDir` | S | `emits-output` |
| `declarationMap` | S | `emits-output` |
| `diagnostics` | S | `not-a-resolution-or-membership-option` |
| `disableReferencedProjectLoad` | S | `not-a-resolution-or-membership-option` |
| `disableSizeLimit` | S | `not-a-resolution-or-membership-option` |
| `disableSolutionSearching` | S | `not-a-resolution-or-membership-option` |
| `disableSourceOfProjectReferenceRedirect` | S | `not-a-resolution-or-membership-option` |
| `downlevelIteration` | S | `emits-output` |
| `emitBOM` | S | `emits-output` |
| `emitDeclarationOnly` | S | `emits-output` |
| `emitDecoratorMetadata` | S | `not-a-resolution-or-membership-option` |
| `erasableSyntaxOnly` | S | `not-a-resolution-or-membership-option` |
| `esModuleInterop` | H | honored (TSR-1 §1) |
| `exactOptionalPropertyTypes` | S | `not-a-resolution-or-membership-option` |
| `experimentalDecorators` | S | `not-a-resolution-or-membership-option` |
| `explainFiles` | S | `not-a-resolution-or-membership-option` |
| `extendedDiagnostics` | S | `not-a-resolution-or-membership-option` |
| `forceConsistentCasingInFileNames` | S | `not-a-resolution-or-membership-option` |
| `generateCpuProfile` | S | `emits-output` |
| `generateTrace` | S | `emits-output` |
| `help` | S | `not-a-resolution-or-membership-option` |
| `ignoreConfig` | S | `not-a-resolution-or-membership-option` |
| `ignoreDeprecations` | S | `not-a-resolution-or-membership-option` |
| `importHelpers` | S | `emits-output` |
| `importsNotUsedAsValues` | S | `not-a-resolution-or-membership-option` |
| `incremental` | S | `emits-output` |
| `init` | S | `not-a-resolution-or-membership-option` |
| `inlineSourceMap` | S | `emits-output` |
| `inlineSources` | S | `emits-output` |
| `isolatedDeclarations` | S | `not-a-resolution-or-membership-option` |
| `isolatedModules` | P | pinned; admitted written values: `false` |
| `jsx` | H | honored (TSR-1 §1) |
| `jsxFactory` | S | `not-a-resolution-or-membership-option` |
| `jsxFragmentFactory` | S | `not-a-resolution-or-membership-option` |
| `jsxImportSource` | P | pinned; admitted written values: `"react"`, only when effective `jsx` is `react-jsx` or `react-jsxdev` |
| `keyofStringsOnly` | S | `not-a-resolution-or-membership-option` |
| `lib` | H | honored (TSR-1 §1) |
| `libReplacement` | P | pinned; admitted written values: `false` |
| `listEmittedFiles` | S | `not-a-resolution-or-membership-option` |
| `listFiles` | S | `not-a-resolution-or-membership-option` |
| `listFilesOnly` | S | `not-a-resolution-or-membership-option` |
| `locale` | S | `not-a-resolution-or-membership-option` |
| `mapRoot` | S | `emits-output` |
| `maxNodeModuleJsDepth` | P | pinned; admitted written values: the unwritten value: `2` when the graph has a `jsconfig` node, else `0` |
| `module` | H | honored (TSR-1 §1) |
| `moduleDetection` | P | pinned; admitted written values: the computed default only, matched by `fold`: `force` when effective `module` is `node16`, `node18`, `node20` or `nodenext`, otherwise `auto` |
| `moduleResolution` | H | honored (TSR-1 §1) |
| `moduleSuffixes` | P | pinned; admitted written values: `[""]` |
| `newLine` | S | `emits-output` |
| `noCheck` | S | `not-a-resolution-or-membership-option` |
| `noEmit` | H | honored (TSR-1 §1) |
| `noEmitHelpers` | S | `emits-output` |
| `noEmitOnError` | S | `emits-output` |
| `noErrorTruncation` | S | `not-a-resolution-or-membership-option` |
| `noFallthroughCasesInSwitch` | S | `not-a-resolution-or-membership-option` |
| `noImplicitAny` | S | `not-a-resolution-or-membership-option` |
| `noImplicitOverride` | S | `not-a-resolution-or-membership-option` |
| `noImplicitReturns` | S | `not-a-resolution-or-membership-option` |
| `noImplicitThis` | S | `not-a-resolution-or-membership-option` |
| `noImplicitUseStrict` | S | `not-a-resolution-or-membership-option` |
| `noLib` | P | pinned; admitted written values: `false` |
| `noPropertyAccessFromIndexSignature` | S | `not-a-resolution-or-membership-option` |
| `noResolve` | P | pinned; admitted written values: `false` |
| `noStrictGenericChecks` | S | `not-a-resolution-or-membership-option` |
| `noUncheckedIndexedAccess` | S | `not-a-resolution-or-membership-option` |
| `noUncheckedSideEffectImports` | S | `not-a-resolution-or-membership-option` |
| `noUnusedLocals` | S | `not-a-resolution-or-membership-option` |
| `noUnusedParameters` | S | `not-a-resolution-or-membership-option` |
| `out` | S | `not-a-resolution-or-membership-option` |
| `outDir` | S | `emits-output` |
| `outFile` | S | `emits-output` |
| `paths` | H | honored (TSR-1 §1) |
| `plugins` | S | `selects-an-executable` |
| `preserveConstEnums` | S | `emits-output` |
| `preserveSymlinks` | P | pinned; admitted written values: `false` |
| `preserveValueImports` | S | `not-a-resolution-or-membership-option` |
| `preserveWatchOutput` | S | `not-a-resolution-or-membership-option` |
| `pretty` | S | `not-a-resolution-or-membership-option` |
| `project` | S | `not-a-resolution-or-membership-option` |
| `reactNamespace` | S | `not-a-resolution-or-membership-option` |
| `removeComments` | S | `emits-output` |
| `resolveJsonModule` | H | honored (TSR-1 §1) |
| `resolvePackageJsonExports` | P | pinned; admitted written values: any boolean when effective `moduleResolution` is `node10` or `classic` (the compiler forces `false`); otherwise `true` |
| `resolvePackageJsonImports` | P | pinned; admitted written values: any boolean when effective `moduleResolution` is `node10` or `classic` (the compiler forces `false`); otherwise `true` |
| `rewriteRelativeImportExtensions` | S | `not-a-resolution-or-membership-option` |
| `rootDir` | S | `emits-output` |
| `rootDirs` | H | honored (TSR-1 §1) |
| `showConfig` | S | `not-a-resolution-or-membership-option` |
| `skipDefaultLibCheck` | S | `not-a-resolution-or-membership-option` |
| `skipLibCheck` | H | honored (TSR-1 §1) |
| `sourceMap` | S | `emits-output` |
| `sourceRoot` | S | `emits-output` |
| `stableTypeOrdering` | S | `not-a-resolution-or-membership-option` |
| `strict` | H | honored (TSR-1 §1) |
| `strictBindCallApply` | S | `not-a-resolution-or-membership-option` |
| `strictBuiltinIteratorReturn` | S | `not-a-resolution-or-membership-option` |
| `strictFunctionTypes` | S | `not-a-resolution-or-membership-option` |
| `strictNullChecks` | S | `not-a-resolution-or-membership-option` |
| `strictPropertyInitialization` | S | `not-a-resolution-or-membership-option` |
| `stripInternal` | S | `emits-output` |
| `suppressExcessPropertyErrors` | S | `not-a-resolution-or-membership-option` |
| `suppressImplicitAnyIndexErrors` | S | `not-a-resolution-or-membership-option` |
| `target` | H | honored (TSR-1 §1) |
| `traceResolution` | S | `not-a-resolution-or-membership-option` |
| `tsBuildInfoFile` | S | `emits-output` |
| `typeRoots` | P | pinned; admitted written values: none |
| `types` | H | honored (TSR-1 §1) |
| `useDefineForClassFields` | S | `not-a-resolution-or-membership-option` |
| `useUnknownInCatchVariables` | S | `not-a-resolution-or-membership-option` |
| `verbatimModuleSyntax` | P | pinned; admitted written values: `false` |
| `version` | S | `not-a-resolution-or-membership-option` |
| `watch` | S | `not-a-resolution-or-membership-option` |

The classifier is generated by `work/evidence/classify_options.py`, which checks completeness against the dumped
declarations. Completeness is not truth. The truth of each row rests on the source citations here and on R-3.6, and it
is reviewed.
- `emits-output`: TypeScript's "Emit" category, plus `rootDir`, `composite`, `incremental`, `tsBuildInfoFile`,
  `generateCpuProfile` and `generateTrace`, which write files.
- `selects-an-executable`: `plugins` (language-service plugin modules).
- Every other S option is `not-a-resolution-or-membership-option`.
- Options TypeScript flags `affectsModuleResolution` that change only diagnostics stay S, with their evidence:
  - `forceConsistentCasingInFileNames`: a casing diagnostic after the file is located (`_tsc.js`:124297-124315);
  - `disableSizeLimit`: no compiler-program use;
  - `allowImportingTsExtensions`: the checker reports after resolution (`_tsc.js`:49490-49518); the other uses choose
    generated specifier spellings.

**R-3.6 Stated consequences of S options that touch resolution or membership.** Four S rows have a true reason
(`emits-output`), but in 6.0.3 each also has one bounded effect on resolution or membership. The analysis does not
reproduce that effect. TSR-1 discloses the consequence instead of pinning these options, because pinning would refuse
the ordinary configuration (almost every project writes `outDir`):
- **`importHelpers`.** TypeScript adds a synthetic `tslib` import to each module file (`_tsc.js`:124085-124087). The
  analysis does not, so `tslib` is not a program member through that import.
- **`outDir`, `declarationDir`, `rootDir`.** TypeScript maps a package `exports`/`imports` target inside the project's
  own output directory back to its input source (`tryLoadInputFileForPath`, `_tsc.js`:41808-41880). The analysis does
  not. The analysis suppresses only that remap, and continues ordinary TypeScript resolution at the package target,
  extension substitution included. The edge is unresolved only when that ordinary lookup fails (NE §4.4). Measured
  (`measured-output-remap-r3-6.0.3.json`, `exports` `./dist/index.js`, `bundler`):

  | Candidates present | With `outDir`/`rootDir` | Stripped (the analysis) |
  |---|---|---|
  | input and output declaration | `src/index.ts` | `dist/index.d.ts` |
  | input only | `src/index.ts` | unresolved |
  | output declaration only | `dist/index.d.ts` | `dist/index.d.ts` |
  | neither | unresolved | unresolved |

  `outDir` and `declarationDir` still supply R-4.3's default exclusion.

**Controls:** TSR1-C12 to TSR1-C15, TSR1-C28, TSR1-C31.

---

## 4. X-C2B1-4 — program roots under a tsconfig/jsconfig

**R-4.1 Decision.** `programRootFiles` is TypeScript 6.0.3's `files`/`include`/`exclude` result
(`getFileNamesFromConfigSpecs`, `_tsc.js`:39608-39654; matcher `_tsc.js`:18399-18600; extensions
`_tsc.js`:18621-18651; extension changes `_tsc.js`:18748-18772 and :5323-5430). It is evaluated over the snapshot
instead of a filesystem, with case-sensitive matching over UTF-16 code units on every host. The rules below restate
that procedure exactly. The differential reference implements them, and agrees with TypeScript on every root list of
the 33 cases.

**R-4.2 Candidates.** The candidates are the snapshot inventory paths that are regular files and whose membership row
is not inside a pruned tree (U-4a) and not `outside-project-boundary`.
- **A profile choice, not a pruning rule.** TypeScript can honor an explicit `files` entry inside `node_modules`, and
  U-4a's pruning governs discovery only; a pruned-tree file can be a retained read-set row (NE:735-741). TSR-1
  nevertheless makes roots first-party: a retained read-set row is never a root.
- **Outside the unit.** Roots may lie outside the unit's directory where the specs name them, as TypeScript allows.
  Membership (U-3) is unchanged.

**R-4.3 The specs.**
- **Which node.** Each of `files`, `include` and `exclude` is taken from the nearest node that writes it: `E` if it
  writes it, otherwise the last `extends` entry (in order, recursively) whose effective spec defines it
  (`_tsc.js`:39306-39314). A written `[]` is defined; it is not absent.
- **Shape.** A written spec must be an array of strings. Anything else, `null` included, refuses
  `native.typescript-profile-spec-malformed:<member>`.
- **Empty strings.** An empty string in `include` or `exclude` contributes no pattern and no base: it is dropped before
  rebasing, and it is not `.` (`_tsc.js`:18444-18449). Measured: `include: [""]` gives no roots; `include: ["."]`
  gives `a.ts`; `exclude: [""]` excludes nothing. An empty string in `files` names a directory, not a file, and
  refuses as R-4.5 says.
- **Rebasing.** Every other entry is rebased per R-1.5 against its declaring node.
- **Malformed entries.** An `include` entry matching `(^|/)\*\*/?$`, and any entry with a `..` segment after a `**`
  segment, refuse `spec-malformed` (`_tsc.js`:39711-39720).
- **Default include.** If neither `files` nor `include` is defined, `include` is `["**/*"]`, declared at `E`.
- **Default exclude.** If `exclude` is undefined, it is the effective `outDir` and `declarationDir`, where each is a
  string, rebased per R-1.5 (`_tsc.js`:39060-39066). An ill-formed or outside-project value excludes nothing. Both
  remain S.

**R-4.4 The supported extensions `X`**, as TypeScript's priority groups:
- without effective `allowJs`: `[.ts .tsx .d.ts]`, `[.cts .d.cts]`, `[.mts .d.mts]`;
- with it: `[.ts .tsx .d.ts .js .jsx]`, `[.cts .d.cts .cjs]`, `[.mts .d.mts .mjs]`.

`flat(X)` is their concatenation, plus `.json` when effective `resolveJsonModule` is true.

A path `p` **has** extension `e` when its rooted subject `/` + `p` is longer than `e` and ends with it
(`fileExtensionIs`, `_tsc.js`:5323-5325, which TypeScript applies to directory-prefixed paths). Every R-4 extension
test uses this predicate: literal validation, stream filtering, the priority group and the priority tests. So a root
file named `.ts` has extension `.ts` (measured cases `r2rf2_files_dot_ts`, `r2rf2_include_dot_ts` and
`r2rf2_root_ext_only_prio`). Retained values stay project-relative.

**R-4.5 Literal roots (`files`).** Each entry, rebased, must be a candidate that has an extension in `flat(X)`.
Otherwise it refuses `native.typescript-profile-root-unsupported:<entry>`, which is TypeScript's "not found" or
"unsupported extension" for a root file. It is a configuration error, refused as MB14a refuses an unresolved `extends`.
`L` is the literal roots in `files` order, keeping the first occurrence of a repeat.

**R-4.6 The matcher** (`getSubPatternFromSpec`, `_tsc.js`:18457-18509). Each rebased spec `p` gives a pattern
`P(p, usage)`, for usage `files` (include) or `exclude`.

1. **Components.** `K = ["", s1, …, sn]`: an empty first component, then `p`'s segments (`[""]` for `p = ""`).
2. **Trailing `**`.** For `files` usage, a last component `**` gives no pattern (R-4.3 already refuses it).
3. **Implicit glob.** If the last component contains none of `.`, `*` and `?`, append `**` and `*`.
4. **The fragments.**
   - `files`: `S = (?:[^./]|(?:\.(?!min\.js$))?)*` and
     `DS = (?:/(?!(?:node_modules|bower_components|jspm_packages)(?:/|$))[^/.][^/]*)*?`;
   - `exclude`: `S = [^/]*` and `DS = (?:/.+?)?`.
5. **Building the pattern.** Walk `K`. A `**` component appends `DS`. Any other component first appends `/` if a
   component was already written, then:
   - for `files`: a leading `*` becomes `(?:[^./]S)?` and a leading `?` becomes `[^./]`. In the rest, `*` becomes `S`,
     `?` becomes `[^/]`, any character other than ASCII letters, digits, `_`, whitespace or `/` becomes `\` followed by
     the character, and the remaining characters stand for themselves. If the component contained `*` or `?`, the
     whole component pattern is prefixed with `(?!(?:node_modules|bower_components|jspm_packages)(?:/|$))`.
   - for `exclude`: the same character mapping, with no leading-character case and no prefix.
6. **The regular expressions.**
   - Include: `^` + `P(p, files)` + `$`, one per non-empty include entry, in order. JSON include: the same, for the
     entries whose written text ends in `.json`.
   - Exclude: `^(?:(?:P1)|(?:P2)|…)(?:$|/)`, over the non-empty exclude entries.
7. **The subject.** A candidate's subject is `/` + its path. Matching is ECMAScript regular-expression semantics
   **without** the Unicode flag, over the UTF-16 code units of the subject and the pattern. So `?`, `[^/]` and `[^./]`
   each consume one code unit, and a supplementary character needs `??`. Measured: `include: ["?.ts"]` over `x.ts` and
   `😀.ts` gives `x.ts`; `["??.ts"]` gives `😀.ts`.

**R-4.7 The visit stream** (`matchFiles`, `_tsc.js`:18525-18596).
- **Bases.** `D(E)` first. Then each non-empty include entry's base directory: the rebased spec up to the last `/`
  before its first `*` or `?`; or, for a spec with neither, the spec itself when its last component has no `.`, else
  its directory. Bases are sorted by UTF-16 code units, and one is kept only when it is not equal to or below an
  earlier base.
- **The walk.** Each base in order, depth-first. In each directory, its files come before its subdirectories, each set
  sorted by the UTF-16 code units of the name.
- **One visited set.** A single set of visited directories is shared by every base, keyed by the canonical snapshot
  directory path (`""` for the root). Before a directory is walked: if it is in the set, it is skipped with everything
  below it; otherwise it is added, then walked (`_tsc.js`:18533-18542). No ambient `realpath` is consulted. So an
  ancestor base, such as `include: ["../**/*"]` from `app/`, never revisits `app/`. Measured case `r2rf1_visited`:
  `app/a.cts app/a.d.cts app/z.ts`; a repeated walk would give `app/a.cts app/z.ts app/a.d.cts`.
- **Membership of the stream.** Each visited candidate whose path has an extension in `flat(X)` and whose subject
  matches no exclude regex is placed in bucket `i`, where `i` is the index of the first include regex its subject
  matches. Candidates matching none are dropped.
- **The stream** is bucket 0, then bucket 1, and so on, each in visit order.

**R-4.8 Selecting wildcard roots: TypeScript's ordered-map algorithm** (`_tsc.js`:39620-39654, :39783-39815).
`W` (wildcard roots) and `J` (JSON roots) are insertion-ordered lists; deleting from `W` removes the entry from its
position. For each path `f` of the stream, in order:
1. **JSON.** If `f` has extension `.json`: when `f`'s subject matches a JSON include regex and `f` is in neither `L` nor
   `J`, append `f` to `J`. In every case, continue with the next `f`.
2. **The group.** `G` is the first priority group of R-4.4 that holds an extension `f` has. Without one, go to step 5.
3. **Higher priority.** For each `e` of `G`, in order:
   - if `f` has `e`, and not (`e = .ts` and `f` has `.d.ts`), stop this step: `f` is not displaced;
   - otherwise let `h = change(f, e)`. If `h` is in `L` or `W`: when `e = .d.ts` and `f` has `.js` or `.jsx`, continue
     with the next `e`; otherwise `f` is displaced, so skip it and go to the next `f`.
4. **Lower priority.** For each `e` of `G`, from the last backward: if `f` has `e`, stop. Otherwise delete
   `change(f, e)` from `W`.
5. **Insert.** If `f` is in neither `L` nor `W`, append `f` to `W`.

`change(f, e)` operates on the rooted subject `/` + `f`, and drops the leading `/` from the result. It removes the first
extension of
`[.d.ts, .d.mts, .d.cts, .mjs, .mts, .cjs, .cts, .ts, .js, .tsx, .jsx, .json]` that the subject ends with, preceded by a
`.`, and appends `e` (`changeExtension`, `_tsc.js`:18748-18772). The `.d.ts` exception is asymmetric, and it does not apply
to `.d.cts` or `.d.mts`.

Measured witnesses (all agree with the reference):
- `include: ["b.js", "b.d.ts"]` gives `b.d.ts`, while `["b.d.ts", "b.js"]` gives `b.d.ts b.js`;
- `include: ["*"]` with `allowJs` over `a.cts a.d.cts a.cjs b.mts b.d.mts b.mjs` gives `a.cts a.d.cts b.mts`;
- case `prio` gives `a.ts b.d.ts b.js c.mts y.ts z/q.ts`.

**R-4.9 Order (`x-opensip-order: sequence`).** `programRootFiles = L ++ W ++ J`. The JSON roots keep the stream's
include grouping: `include: ["b/*.json", "a/*.json"]` gives `b/x.json a/x.json`.

**R-4.10 `jsRootFiles`** is the subsequence of `programRootFiles` ending in `.js`, `.jsx`, `.mjs` or `.cjs`. It is
empty when effective `allowJs` is false. NE:548-551's flags are unchanged.

**R-4.11 No refusal for emptiness.** An empty result is admitted. TypeScript reports diagnostics 18002 and 18003 for
it, and TSR-1 does not refuse on a diagnostic.

**R-4.12 Bounds.** More than 100,000 roots refuses `native.typescript-profile-bound:programRootFiles`.

**R-4.13 Disclosed divergence.** TypeScript on a case-insensitive host (macOS, Windows) matches specs
case-insensitively; TSR-1 never does, because resolution semantics are platform-invariant by design (NE §1.1).
Synthesized roots are NE:1424-1427's, unchanged.

**Controls:** TSR1-C16 to TSR1-C20, TSR1-C27.

---

## 5. X-C2B1-5 — toolchain member selection

**R-5.1 A role table over the tree, not a manifest field.** The profile row fixes three paths in the admitted
`kind=toolchain` closure tree named by `toolClosure.closureId`:

| Field | Tree member path | What it is |
|---|---|---|
| `toolClosure.runtime` | `bin/node` | the bundled JavaScript runtime |
| `toolClosure.compiler` | `lib/typescript.js` | the compiler module the provider loads (the 6.0.3 package's `main`) |
| `toolchain.compilerPackageDigest` | `package.json` | the compiler package manifest (`name: typescript`, `version: 6.0.3`) |

The tree root is the `typescript` package root, with the runtime at `bin/node`. Each field is that member's digest. A
missing member refuses `native.typescript-profile-toolchain-member-missing:<field>` before PlanId.

**R-5.2 Why this needs no release-format change.** The component manifest and CR-1 are unchanged: one `entrypoint` per
platform (`component_manifest.rs`:365-377), no new field and no new role. R-5.1 is a requirement on the **content**
of a TypeScript toolchain release for profile row 6.0.3, which the release builder must meet. It selects content for this
profile's toolchain releases; actual release qualification stays separately gated.
- The manifest's `entrypoint` is not read by TSR-1. CR-1 requires it to be a regular file, and `bin/node` is the
  natural choice.
- `inspect_native_context` keeps its membership-only check (`native_context.rs`:163-183). TSR-1 fixes how a host
  **mints**; the worker's recomputation, not admission, catches a host that mints another member.

**R-5.3 Fixtures.** The C2a/C2b fixtures use `lib/tsc.js` as the compiler, give `compilerPackageDigest` the compiler's
digest, and carry `5.6.3`. They are synthetic and need not follow R-5.1 for admission tests. Any TSR-1 mint control
uses a tree with R-5.1's members and version `6.0.3`.

**C2b-1a interface:** these are the `ToolchainMembers` paths. C2b-1a joins the digests.

**Controls:** TSR1-C21, TSR1-C22.

---

## 6. X-C2B1-6 — `packageModuleType` and `lockfileIdentity`

**R-6.1 `packageModuleType` comes from the nearest `package.json`.** This is Node's and TypeScript's scope rule.
- **Which file.** Walk from the unit's root directory up to the project root. The first directory holding a candidate
  file named exactly `package.json` (R-4.2's candidate rule) supplies it. Under `js-synthesized` this is the unit's
  marker.
- **Reading.** The file is read as strict JSON (RFC 8259, not JSONC), at most 1 MiB, with a root object. A duplicate
  key keeps its last value.
- **`type`.** `"module"`→`module`; `"commonjs"`→`commonjs` (exact, case-sensitive); member absent→`absent`.
- **Refusals.** Any other value, a non-object root, or unparseable JSON refuses
  `native.typescript-profile-package-json-malformed:<path>`. More than 1 MiB refuses
  `native.typescript-profile-bound:package.json`.
- **No file.** If no directory up to the project root holds one, the value is `absent`.

**R-6.2 `lockfileIdentity` comes from the nearest lockfile directory.**
- **Which directory.** Walk from the unit's root directory up to the project root. The first directory holding at
  least one candidate file with one of these names supplies it.
- **Precedence** within that directory (NM:2246-2249, now published): `package-lock.json`→`package-lock`, then
  `pnpm-lock.yaml`→`pnpm-lock`, then `yarn.lock`→`yarn-lock`, then `bun.lock`→`bun-lock`, then `bun.lockb`→`bun-lock`.
- **The value.** `lockfileIdentity = {kind, path, contentSha256}`, where `contentSha256` is the inventoried snapshot
  digest. Lockfile contents are not parsed.
- **None.** If no directory holds one, the value is `null` and `lockfileKind = none`.
- **The reason for the ancestor walk.** It finds the workspace-root lockfile of an npm, pnpm, yarn or bun workspace,
  which is where a nested package's install is recorded.
- **Disclosed limits.** `npm-shrinkwrap.json` is not a lockfile under `tsr1.v1`, because the schema has no kind for
  it. A lower-precedence lockfile in the chosen directory, or any lockfile further up, is not recorded.

**C2b-1a interface:** `LockfileSelection {kind, path}` and `PackageModuleType`.

**Controls:** TSR1-C23, TSR1-C24.

---

## 7. Order of evaluation and the total refusal table

TSR-1 runs after MB14a has admitted the graph. The phases run in order, and the first fault found is the refusal.
Within a phase, the order is as stated. The subject is `<key>:<path>`, followed by `:<member>` where the table gives
one. The member is the option, the spec name, the field or the entry, written verbatim (so the empty name gives a
trailing `:`). The subject is bounded by the inherited termination rule, as for MB14a.

| Phase and order | Check | Key | `<path>` (attribution) | `<member>` |
|---|---|---|---|---|
| 1 | compiler version (P-0.2) | `compiler-unsupported` | the compiler `semanticVersion` | — |
| 1 | stdlib version (P-0.2) | `stdlib-version-mismatch` | the stdlib `semanticVersion` | — |
| 1 | members, in R-5.1 table order | `toolchain-member-missing` | the field (`toolClosure.runtime` …) | — |
| 2: nodes ascending by UTF-8 path; within a node, `compilerOptions` members ascending by UTF-8 name, then `files`, `include`, `exclude`, `references`; elements in order | empty option name | `option-malformed` | the node | `""` |
| 2 | H or P member: type, `null`, shape (`paths`, arrays, element strings, pattern `*` count, empty substitution list), and the non-empty grammar of `types`/`customConditions` elements and `paths` patterns | `option-malformed` | the node | the option |
| 2 | H member value: enum, `lib` name, `lib: []` | `option-value-unsupported` | the node | the option |
| 2 | path grammar or template case (R-1.5 step 1 or 2) | `option-malformed` / `spec-malformed` | the node | the option or spec |
| 2 | rooted, or rising above the root (R-1.5 steps 3–4), for every write except a `paths` substitution in the ordinary branch | `path-outside-project` | the node | the option or spec |
| 2 | spec shape, trailing `**`, `..` after `**` (R-4.3) | `spec-malformed` | the node | the spec |
| 3a: each write in phase-2 node, member and element order | R-1.9's per-write length limits | `bound` | the writing node | the option |
| 3b: P options in table order, each write in phase-2 node order | a P write outside its admitted values (`references` waits for phase 4) | `option-unsupported` | the writing node | the option |
| 3c | containment of the winning `paths` write's ordinary-branch substitutions, whose base is the effective `baseUrl` (R-1.5 step 3) | `path-outside-project` | the node whose `paths` write won | `paths` |
| 3c | R-1.9's winning path lengths, in R-1.9 order | `bound` | the node whose write won | the option |
| 3c | R-1.9's winning-collection counts, in R-1.9 order | `bound` | the node whose write won | the field |
| 3d | a stripped name over 256 characters, first in phase-2 order | `bound` | the writing node | `strippedOptions` |
| 3d | more than 256 stripped rows | `bound` | `E` | `strippedOptions` |
| 4 | literal roots, in `files` order (R-4.5) | `root-unsupported` | the node that wrote the winning `files` | the entry |
| 4 | `references` admission (R-3.2) | `option-unsupported` | the node that wrote it | `references` |
| 4 | more than 100,000 roots | `bound` | `E` | `programRootFiles` |
| 5 | `package.json` (R-6.1): unparseable, non-object root, `type` value | `package-json-malformed` | that `package.json` | — |
| 5 | `package.json` over 1 MiB | `bound` | that `package.json` | `package.json` |

Every key is prefixed `native.typescript-profile-`. A phase-2 fault in a node that phase 3 would also fault is
reported in phase 2. Because each phase's order is total, two hosts report the same refusal for one repository.

---

## 8. What a conforming implementation computes (the C2b-1b outputs)

| C2b-1a typed input | TSR-1 rule |
|---|---|
| `HonoredOptions` (with `lib` materialized) | §1, §2 |
| `StrippedOption` list | §3 |
| program roots and JS roots | §4 |
| `ToolchainMembers` (paths) | §5 |
| `LockfileSelection {kind, path}` | §6 |
| `PackageModuleType` | §6 |
| config graph nodes | MB14a, unchanged |

TSR-1 adds no custody input. T-LIB, T-DEF and the option and role tables are host data inside C2b-1b. The only change
to a C2b-1a input type is Part S: `baseUrl`, `rootDirs` elements and `paths` substitutions may be `""`.

---

## 9. Pricing

TSR-1 adds work: reading more members, the matcher over the candidate files, and two ancestor walks. Its pricing is
C2b-1b's, under M1a convention C1. Every pass is funded first and assigned to *T*/*L*/*N*. TSR-1 changes no cap and no
charge law.

---

## 10. Part R — refusal termination (successor of S10/S10b's registered text)

**R-10.1 Configuration-caused keys.** These are internal keys, each aliased at the host boundary to the **existing**
public `DomainDetailCode` **`native.typescript-config-unresolved`**. They take its existing D9 row (request-rejected,
exit 2, `CONFIG.INVALID`) and its "request rejection detail" carrier, exactly as MB14a's four keys do. No public code is
added. Subjects are as §7 states.
- `native.typescript-profile-option-malformed`
- `native.typescript-profile-option-value-unsupported`
- `native.typescript-profile-option-unsupported`
- `native.typescript-profile-path-outside-project`
- `native.typescript-profile-spec-malformed`
- `native.typescript-profile-root-unsupported`
- `native.typescript-profile-package-json-malformed`
- `native.typescript-profile-bound`

**R-10.2 Toolchain-caused keys.**
- `native.typescript-profile-compiler-unsupported`
- `native.typescript-profile-stdlib-version-mismatch`
- `native.typescript-profile-toolchain-member-missing`

These join NE §10's existing row for native-context closure and join failures (NE:3530): request-rejected (2),
`REQUEST.PRECONDITION_FAILED`, request detail, before PlanId, and no worker is spawned. They are carried by the existing
`NativeContextRefused` carrier (`crates/host/src/outcomes.rs`:1408-1410) as internal keys, not public codes.

**R-10.3 The remedy, exactly.** The remedy keyed by `native.typescript-config-unresolved` is replaced, under the same
key, by one exact string. That string is S10b's current text (`REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED`,
`crates/host/src/outcomes.rs`:1033), followed with no other change by the clause below. The result is copied byte for
byte to every selected carrier: the product constant and both native-model copies.

> `; or, for the options OpenSIP resolves under TypeScript 6.0.3: give every compilerOptions member a non-empty name of at most 256 characters, and every honored or pinned option its JSON type and a value TypeScript 6.0.3 accepts, never null and never an empty lib; make every types and customConditions element a non-empty string of at most 4096 characters and every paths pattern non-empty; write baseUrl, rootDirs, paths and every files, include and exclude entry inside the project, without a backslash or control character, with ${configDir} only in that exact case, with no include entry ending in ** and no .. after a **; name in files only existing project files outside node_modules with an extension the compiler accepts; leave typeRoots, moduleSuffixes, preserveSymlinks, noResolve, noLib, libReplacement, allowArbitraryExtensions, resolvePackageJsonExports, resolvePackageJsonImports, maxNodeModuleJsDepth, jsxImportSource, isolatedModules, verbatimModuleSyntax and moduleDetection unset or at their defaults, and references unset or empty unless the configuration has no root files; keep lib within 64 entries, types within 1024, customConditions within 64, rootDirs within 1024, paths within 4096 patterns of at most 1024 characters with 1 to 64 substitutions and at most one * in each pattern and substitution, every path within 4096 characters, at most 256 stripped options and at most 100000 root files; and keep the nearest package.json valid JSON of at most 1 MiB with an object root whose type, if present, is module or commonjs`

The public record, the D9 row and the detail vocabulary are unchanged. C2b-1b binds the new alias rows and the remedy.

---

## 11. Part S — the project-root spelling (NSS-TSR1-S1)

**R-11.1 Identity, parent and owner.**
- **The successor.** NSS-TSR1-S1 is the first narrow successor of the native closed schema
  `urn:opensip:product-v1:native:evidence-schemas:v2`, made under TSR-1. The schema keeps its `$id` and its major
  version 2, because the change only widens admission (R-11.4).
- **Its parent** is the **selected** native source. That is the architecture
  `docs/implementation/m3/native-publication/native-owner-patterns-source-r1/sources/native-v2.schema.json` (295,104
  bytes, sha256 `7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132`), which the product source map
  selects (`schemas/source-map.json`:154-168) and which equals the product `schemas/sources/native-v2.schema.json`
  today.
- **Its custody.** The parent stays frozen. At binding, C2b-1b publishes the successor source in a new architecture
  successor directory (for example `docs/implementation/m3/native-publication/nss-tsr1-s1/sources/native-v2.schema.json`).
  It is the parent with only R-11.3's edit, preserving every other byte of inherited content. The product source then
  becomes that successor, byte for byte.
- **Adoption and binding.** The owner is the native schema. The coordinator adopts it with TSR-1 under OD-AUTO-1, and
  C2b-1b binds it, with its inventory row, as a contract successor beside TSR-1.

**R-11.2 The defect.** `TypeScriptHonoredOptionsV1.baseUrl`, `rootDirs[]` and `paths[].substitutions[]` are
`CanonicalPath` (`minLength 1`, no `.` segment). So the project root, the effective `baseUrl` of `"baseUrl": "."` in
a root `tsconfig.json`, has no admissible spelling. The value is real (measured case `ext`: `baseUrl ""`) and common.

**R-11.3 The change, exactly, and nowhere else.**
- Add `$defs/TypeScriptProjectPathV1`:
  `{"oneOf": [{"$ref": "#/$defs/CanonicalPath"}, {"const": ""}], "description": "A project-relative path in TypeScriptHonoredOptionsV1 only. The empty string is the project root, as InternalUnitRootV1 spells it; it is never \".\"."}`.
- Change exactly three `$ref`s in `TypeScriptHonoredOptionsV1` from `#/$defs/CanonicalPath` to
  `#/$defs/TypeScriptProjectPathV1`:
  1. `properties.baseUrl.oneOf[0]`;
  2. `properties.rootDirs.items`;
  3. `properties.paths.items.properties.substitutions.items`.
- `CanonicalPath` itself and every other use of it are unchanged, including `configGraphPaths`, the config graph, the
  layout, the lockfile and `programRootFiles`. `""` becomes **newly** admissible only at these three locations. Other
  fields that already spell the root, such as `InternalUnitRootV1`, are untouched.
- `InternalUnitRootV1` is not reused, because its grammar is narrower than `CanonicalPath` (no trailing slash, no empty
  segment). Reusing it would refuse values the current schema admits, so it would not be a pure widening.

**R-11.4 It only widens.**
- `CanonicalPath` has `minLength: 1`, so the two `oneOf` branches are disjoint. Every string `CanonicalPath` admits
  matches exactly one branch, and the parent's accepted set is a subset of the successor's.
- No value is rewritten, and no record gains or loses a member. Every previously admitted record keeps its bytes, its
  `C` encoding, its raw SHA-256 and its H identity.
- So every **existing retained** context, universe, vector and Plan descriptor keeps its identity. This is not a
  promise that a fresh invocation on another host or core closure mints the same `PlanId`: Plan also binds its semantic
  closures and other inputs. Nor does Part S undo TSR-1's own disclosed choices. No re-identification or rewriting of
  a historical record is authorized.
- Checked by the reviewer, on literal fixture values: the six complete honored-option objects in
  `native-cases.v2.json` and the one in each of the three product `native-context-fixtures*.json` files all carry
  `baseUrl: null`, `rootDirs: []` and `paths: []`. Universal preservation rests on the set-inclusion proof, not on
  these nine objects alone.

**R-11.5 Canonical encoding and hashing.** `""` is an ordinary JSON string. `C` encodes it under its existing string
rule as the two bytes `0x22 0x22`, a string token inside `C` of the complete descriptor. The context's identity is
`H("native.context.typescript.v2", descriptor)` = `SHA256("opensip.product.v1" || 00 || domain || 00 ||
uint64BE(len(C(X))) || C(X))` (identity-and-evidence:121-130, :168-174), computed over those bytes unchanged. There is
no special case:
- `""` is never normalized to `null`, `"."` or an absent member;
- `baseUrl: ""` (the root) and `baseUrl: null` (unwritten) are different values, and they mint different contexts.

A resolver emits `""` only for the root. Every other value it emits is in canonical directory form (no trailing slash,
no empty segment), by R-1.5's normalization.

**R-11.6 What C2b-1b must carry for Part S.**
- **The exact-source admission chain.** The native semantic joins need no new root-specific rule. But the selected
  schema bytes are pinned in several places, and every pin moves to the successor's exact bytes under its existing
  custody rules. No pin may be bypassed or weakened:
  - `crates/identity/src/schema_registry.rs` (the `SourcePin` for `urn:opensip:product-v1:native:evidence-schemas:v2`:
    295,104 bytes and its sha256), checked by `RegisteredSchemas::from_sources`;
  - `schemas/registry.json`'s `sourceSha256`;
  - `schemas/source-map.json`'s `architectureSource` (the new successor path, bytes and hash);
  - `tools/contracts/generator-closure.json`'s pin;
  - the generated carriers, regenerated: `crates/contracts/src/generated/evidence.rs` (`base_url`, `root_dirs`,
    `PathsItem.substitutions` become the generated `TypeScriptProjectPathV1` type), and any TypeScript carrier the same
    generator emits for these fields.

  A carrier-only regeneration does not satisfy this.
- **The reference model.** NM loads `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (sha256
  `2d37b810…`). That is an older, different document with its own `CanonicalPath` pattern, and it is not the product
  source. C2b-1b applies the same additive edit (one definition, three references) to it as a separately pinned local
  delta, preserving its other bytes and standing. It is never called identical to the product source.
- **Checks C2b-1b runs:**
  - (a) the product source equals the selected successor source, byte for byte;
  - (b) the successor differs from its parent by exactly R-11.3's structural delta;
  - (c) the model copy differs from its pinned parent by exactly the same structural delta.
- **The host.** C2b-1b's resolver emits `""` per R-1.5. C2b-1a's typed input accepts it and keeps `null` and `""`
  distinct (§8).
- **Controls:** TSR1-C26.

---

## 12. The reference model: divergences, and the change C2b-1b carries

| NM today (`typescript_mode`, NM:2219-2258) | TSR-1 | Model change C2b-1b carries |
|---|---|---|
| Reads only the unit-root file's own `compilerOptions`, without `extends` | §1 over MB14a's graph | a `typescript_resolution_profile` reference implementing §§0–7 over the retained graph, the snapshot inventory, the layout and the **admitted closure inputs** (compiler and stdlib `semanticVersion`, toolchain tree member paths). `work/evidence/diff/tsr1_ref.py` is the seed for §§1, 2 and 4; no source lookup or ambient data fills an omitted input |
| `compilerOptionsSubset` holds `typeRoots` and `exactOptionalPropertyTypes` and omits 8 honored fields | the 18 honored fields, P and S classes | drop the subset; emit `honoredOptions` and `strippedOptions`; generated T-LIB, T-DEF and option tables |
| Roots: every TS (and with `allowJs`, JS) file under the unit | §4 | the §4 matcher and ordered-map algorithm over the inventory |
| `TS_EXT` adds `.mts`/`.cts` to synthesized roots | NE:1426 (`.ts/.tsx/.js/.mjs/.cjs/.jsx`) is the published law and is unchanged | synthesized roots follow NE:1426 |
| `package.json` `type`: other values become `absent`; unit-root file only | R-6.1: nearest ancestor; other values refuse | R-6.1 |
| Lockfile at the unit root only | R-6.2: nearest ancestor directory, same precedence | R-6.2 |
| The schema copy cannot spell the root | R-11.6's local delta | apply it |
| Fixtures: `5.6.3`, `lib/tsc.js` as the compiler, `compilerPackageDigest` equal to the compiler's digest | §0, §5 | mint vectors use 6.0.3 and R-5.1's members; admission fixtures may stay synthetic |

---

## 13. Controls (a conforming implementation must pass)

Expected values come from §§1–7. Where measured, they agree with the evidence. No TypeScript runs in any control. The
measured evidence is interpretation evidence; it is not product or release qualification.

- **TSR1-C1** (defaults): an empty `tsconfig.json` gives `target es2025`, `module es2022`, `moduleResolution bundler`,
  `strict`, `esModuleInterop`, `allowSyntheticDefaultImports` and `resolveJsonModule` all `true`, `types []`, and
  `lib` = T-DEF[`es2025`].
- **TSR1-C2** (the chain): `target ES5` with `module CommonJS` gives `moduleResolution bundler`,
  `resolveJsonModule true` and `lib` = T-DEF[`es5`]. `target es6` gives `es2015`/`es2015`/`bundler`. `module node16`
  gives `node16` and `resolveJsonModule false`. `es3` over a base writing `es5` gives `es2025`/`es2022` (NB-1).
- **TSR1-C3** (aliases and case): `"ES2022"`, `"Node"` and `"React-JSX"` give `es2022`, `node10` and `react-jsx`.
  `"es2022 "` refuses `option-value-unsupported`.
- **TSR1-C4** (jsconfig supply): case `jsc` gives `allowJs` and `skipLibCheck` `true`. Case
  `jsconfig_base_allowjs_false` gives `allowJs true` (NE:533-541). Case `ts_extends_jsconfig`, a `tsconfig` extending
  a `jsconfig` that writes `skipLibCheck: false`, gives `allowJs true` and `skipLibCheck false`. The pinned
  `maxNodeModuleJsDepth` is 2 under a jsconfig.
- **TSR1-C5** (inheritance and rebasing; case `ext`): `baseUrl ""` (Part S); substitution `src/*`;
  `rootDirs ["gen", "base"]`; entry `strict: false` wins.
- **TSR1-C6** (`paths` base; cases `pathsnob` and `baseurl_other_node`): with no `baseUrl`, the base is the `paths`
  node's directory; with a `baseUrl` written in another node, the base is that `baseUrl`. Case `paths_order` gives the
  ECMAScript order `2, 10, b/*, a/*`, and a repeated `b/*` keeps its first position and last value.
- **TSR1-C7** (`${configDir}`): R-1.5's table of exact results.
- **TSR1-C8** (refusals): each of these refuses with §7's key, path and member: `strict: null`; `module: 5`;
  `paths {"a": []}`; `paths {"*/*": ["x"]}`; `baseUrl "/abs"`; `rootDirs ["../../.."]` (rising above the root);
  `rootDirs ["a\\b"]`. Two faults in two nodes report the lower path.
- **TSR1-C9** (T-LIB): `["ES6", "esnext.asynciterable", "DOM", "es2015"]` gives
  `["es2015", "es2018.asynciterable", "dom"]`. TypeScript keeps the repeat; the record does not (case `node16lib`).
  `["es2025.full"]` and `[]` refuse.
- **TSR1-C10** (T-DEF and the join): for every T-DEF row, every name's component is in the 6.0.3 stdlib tree, and
  `libSelection` is the sorted set. The generated tables equal `lib_tables.py`'s output.
- **TSR1-C11** (expansion evidence): `measured-lib-expansion-r2-6.0.3.json` and its generator are pinned. For each of
  the 13 targets, the evidence check asserts:
  - the root is in both populations;
  - the exact aggregator is in the default population and not in the expanded one;
  - the expanded count is greater than 1;
  - the default list minus the aggregator equals the expanded list, in order.

  This checks evidence; it is not a runtime control.
- **TSR1-C12** (classification): the product table equals `classify_options.py`'s. The P rows' witnesses are retained
  as evidence: RF-1's membership probe, and `measured-references-r2-6.0.3.json`.
- **TSR1-C13** (P refusal and admission):
  - refuse `option-unsupported`: `typeRoots ["./types"]`; `preserveSymlinks: true`; `maxNodeModuleJsDepth: 0` under a
    jsconfig; `jsxImportSource: "preact"`; `jsxImportSource: "react"` with `jsx: preserve`; `isolatedModules: true`;
    `verbatimModuleSyntax: true`; `moduleDetection: "force"` under `module esnext`; `references [{"path": "./a"}]` with
    a non-empty root set.
  - admit: `moduleSuffixes [""]`; `resolvePackageJsonExports: false` under `moduleResolution node10`;
    `jsxImportSource: "react"` with `jsx: react-jsx`; `moduleDetection: "Force"` under `module nodenext`;
    `isolatedModules: false`; `{"files": [], "references": [{"path": "./a"}]}`.
- **TSR1-C14** (`strippedOptions`): `{outDir, sourceMap, AllowJs, plugins, compileOnSave, typeAcquisition,
  noEmit: false}` gives the rows `AllowJs/not-a-resolution-or-membership-option`, `compileOnSave/emits-output`,
  `noEmit/emits-output`, `outDir/emits-output`, `plugins/selects-an-executable`, `sourceMap/emits-output` and
  `typeAcquisition/acquires-types-from-the-network`, in UTF-8 order. An overridden write still gives a row. Supplied
  and unwritten options give none.
- **TSR1-C15** (strip bound): 256 distinct unknown names admit; 257 refuse `bound:strippedOptions` at path `E`.
- **TSR1-C16** (roots; case `empty`): `src/a.ts` only.
- **TSR1-C17** (priority, stream and order): cases `prio`, `rf4_js_first`, `rf4_dts_first` and `rf4_cts_mts`, as R-4.8
  states.
- **TSR1-C18** (inherited specs and bases): case `ext` gives `src/a.ts`. Case `outside_base` gives
  `app/src/a.ts shared/a.ts shared/z/b.ts lib/c.ts`. Case `dfs_order` gives
  `src/_x.ts src/a.ts src/z.ts src/B/d.ts src/b/c.ts`. Case `r2rf1_visited` gives `app/a.cts app/a.d.cts app/z.ts`,
  and case `r2_ancestor_and_entry` gives `pkg/src/a.ts pkg/b.ts top.ts other/c.ts`.
- **TSR1-C19** (JSON): case `json` gives `src/a.ts src/d.json`; case `rf5_json_order` gives `b/x.json a/x.json`; case
  `json_rjm_off` gives `a.ts`.
- **TSR1-C20** (literal and empty specs):
  - a missing `files` entry, `files ["a.js"]` without `allowJs`, `files [""]`, and `files ["node_modules/p/i.d.ts"]`
    each refuse `root-unsupported`;
  - `"files": []` with `references` admits with no roots;
  - cases `rf5_empty_include`, `rf5_dot_include`, `rf5_empty_exclude`, `rf5_q_one` and `rf5_q_two` give their
    measured results;
  - case `files_plus_include` keeps the excluded literal `z.ts`;
  - cases `r2rf2_files_dot_ts` and `r2rf2_include_dot_ts` give `.ts`, and `r2rf2_root_ext_only_prio` gives `.ts .cts`.
- **TSR1-C21** (members): a tree without `lib/typescript.js` refuses
  `toolchain-member-missing:toolClosure.compiler`. With all three members, the digests are those members' digests.
- **TSR1-C22** (versions): a compiler `6.0.2` refuses `compiler-unsupported:6.0.2`. A stdlib `6.0.2` with compiler
  `6.0.3` refuses `stdlib-version-mismatch:6.0.2`.
- **TSR1-C23** (`packageModuleType`): a unit `packages/web` with no `package.json`, under a root `package.json` with
  `{"type": "module"}`, gives `module`. `{"type": "Module"}` refuses. No file anywhere gives `absent`.
- **TSR1-C24** (lockfile): a root holding `yarn.lock` and `package-lock.json`, with a unit at `packages/web`, gives
  `{package-lock, package-lock.json, <digest>}`. A unit-root `pnpm-lock.yaml` wins over the root's files. With none,
  the value is `null` and the kind `none`.
- **TSR1-C25** (identity): changing any one TSR-1 output changes `nativeContextId` or the universe identity. Two
  repositories whose effective configurations are equal (for example omitted `lib` versus the written T-DEF list) mint
  one context, given equal admitted closures, platform and other non-resolution identity inputs.
- **TSR1-C26** (Part S):
  - admission is tested separately for `baseUrl ""`, `rootDirs [""]` and a `paths` substitution `""`;
  - each admits under the successor schema and refuses under the parent;
  - `""` still refuses at other `CanonicalPath` locations (`configGraphPaths`, `programRootFiles`, the layout's
    `installPath`);
  - `baseUrl ""` and `baseUrl null` give two distinct `nativeContextId`s;
  - every existing case-corpus and product TypeScript fixture admits, and round-trips its bytes and identity
    unchanged;
  - the registry is built against the successor's exact bytes, and R-11.6's checks (a)–(c) pass.
- **TSR1-C27** (differential corpus): the 39 cases of `work/evidence/diff/cases.json` give the TypeScript oracle's
  values for every compared field. The one exception is R-2.2's de-duplication in `node16lib`, which
  `diff/compare.py` declares and asserts (exit 0 only on `PASS`). The corpus is positive only. P admission and §7's
  refusal subjects are tested by their own law-expected controls (C13, C28, C29), never by comparing compiler
  diagnostics.
- **TSR1-C28** (names and attribution):
  - names of 0, 1, 256 and 257 characters give, respectively, `option-malformed` with member `""`, admit, admit, and
    `bound`;
  - a `strippedOptions` overflow assembled from three nodes reports path `E`;
  - simultaneous faults in phases 2 and 3 report the phase-2 fault;
  - the remedy bytes are identical in all three carriers.
- **TSR1-C29** (lengths, R-1.9):
  - a `types` or `customConditions` element of 0, 1, 4,096 and 4,097 characters gives, respectively,
    `option-malformed`, admit, admit and `bound`, with member the option;
  - a `paths` pattern of 0, 1, 1,024 and 1,025 characters gives the same four outcomes;
  - an overridden base write of a 4,097-character condition, under an entry writing `customConditions: []`, refuses
    `bound` at the base's path;
  - a node with both a phase-2 shape fault and a phase-3a length fault reports the phase-2 fault;
  - with `base.json` writing `paths {"x": ["../outside"]}` and the root entry extending it with `paths {}` and
    `files []`, no containment or length refusal results, because the overridden substitution is never rebased;
  - a winning ordinary `../outside` substitution refuses `path-outside-project` at its writer, in phase 3c;
  - the same configuration with `noLib: true` refuses `option-unsupported` at its writer, member `noLib`, in phase 3b;
  - a contained winning substitution whose rebased length is 4,097 characters refuses `bound` at its writer, member
    `paths`; one of 4,096 characters passes that bound.
- **TSR1-C30** (remedy coverage): the refusals for a 4,097-character condition, an empty `types` element, an empty
  `paths` pattern and a `package.json` of `[]` each carry R-10.3's exact remedy, and the remedy names each
  prerequisite.
- **TSR1-C31** (R-3.6 resolver witness; C2b-1b's resolver or program test): with `exports` `./dist/index.js`, the
  stripped analysis resolves as the "Stripped" column of R-3.6's table, in each of its four variants. The program
  membership follows the selected edge.

---

## 14. Rejected

- **Pinning 5.6.3.** It is not the shipped compiler, and its defaults differ.
- **Stripping P options with `not-a-resolution-or-membership-option`.** That would be a false disclosure (RF-1).
- **Stripping `references` as `emits-output`** (r1). Its stated rationale was false (RF-2).
- **Pinning `importHelpers`, `outDir`, `declarationDir` or `rootDir`.** Each has a true reason, and pinning would
  refuse ordinary configurations. Their bounded consequence is disclosed instead (R-3.6).
- **A new strip reason, or new honored fields.** Each is a wider native-schema change. It is listed as a follow-on.
- **Refusing unknown option names.** That would be a refusal on a compiler diagnostic.
- **`null` as reset.** MB14a's precedent is followed instead.
- **A single-file default `lib`, a signed lib-table member, or parsing aggregators at mint time** (§2).
- **A symmetric "declarative" extension-priority rule** (r1). It is not TypeScript's algorithm (RF-4).
- **NM's "every file under the unit".** It contradicts `tsc` and NE:968.
- **A manifest field for toolchain roles.** It is a release-format change, and R-5.1 needs none.
- **Unit-root-only lockfile and `package.json`.** They miss workspace roots and Node's scope rule.
- **Reusing `InternalUnitRootV1` for Part S.** It is not a pure widening.

## 15. Not claimed, and every disclosed restriction

- **No product code, schema edit, binding or test.** C2b-1b does those.
- **No equivalence with `tsc` beyond the stated rules.** Every restriction and divergence is:
  1. case-sensitive matching (R-4.13);
  2. `null` refuses for H and P options (R-1.2);
  3. a P option written away from its admitted values refuses (R-3.1). These are 14 options plus `references`, and
     they include settings common in modern templates (`isolatedModules: true`, `verbatimModuleSyntax: true`,
     `moduleDetection: "force"`);
  4. R-3.6's stated consequences of `importHelpers`, `outDir`, `declarationDir` and `rootDir`;
  5. a `${configDir}` case variant refuses (R-1.5);
  6. spec errors that TypeScript reports and drops refuse (R-4.3);
  7. literal roots are validated: a missing, unsupported or retained-read-set `files` entry refuses (R-4.2, R-4.5);
  8. stricter `package.json` parsing: strict JSON, at most 1 MiB, and a `type` value other than `module`/`commonjs`
     refuses (R-6.1);
  9. no `npm-shrinkwrap.json`, and only the nearest lockfile directory is recorded (R-6.2);
  10. a repeated `lib` name is recorded once (R-2.2).
- **No measurement of a real TypeScript toolchain release** on any platform. That remains qualification work
  (NE §12).
- **No cap, charge-law, capacity, count or route change.** Pricing is C2b-1b's (§9).
- **Follow-on (not in this plan; recommended early because of restriction 3).** A native successor (TSR-2 with a schema
  change) could widen `TypeScriptHonoredOptionsV1` to honor `isolatedModules`, `verbatimModuleSyntax`,
  `moduleDetection`, `typeRoots`, `jsxImportSource` and project `references`, and so remove their refusals.
