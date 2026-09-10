# HANDOFF — actual Claude coauthor, v5 (root's CRITICAL concerns 1 and 2, and the mixed-edition decision)

**Standing: not accepted, not qualified, not promoted, nothing closed.** A corrected v9 freeze, a
fresh independent review with **zero unresolved MUST/SHOULD**, a new blind, and the full application
review all remain required. I make no acceptance or readiness claim, and I do not claim that all
gaps are closed.

I read the **final** text of `digest-corrections-author.v4/CODEX-PUBLIC-NOTE.md` — including
paragraphs 9 and 11, which my v4 handoff had not seen and therefore did not assess — and the v5
`CODEX-PUBLIC-NOTE.md`. **Re-reading the v5 note immediately before finalising found it had grown
by two further sections after my first read** (the Cargo target-edition refinement and the
body-versus-provider language distinction). Both are correct, both were unaddressed at that point,
and both are now closed; they are §§3a and 4a below. I do not claim agreement with any text I had
not read at the time I acted on it.

---

## 1. Concern 1 — compiler identity was never missing. Root is right; my v4 text was wrong.

Verified against the current schemas and fixtures rather than asserted:

- `NativeContextV2.toolchain` → `ToolchainIdentityV1`: `rustcVersion`, `rustCommitHash`.
- `TypeScriptNativeContextV2.toolchain` → `TypeScriptToolchainIdentityV1`: `compilerName`,
  `compilerVersion`, `compilerPackageDigest`.
- Both reachable from the universe through its own `nativeContextId`, a reference `close_run`
  **already** requires to be Plan-selected (`UNIVERSE_CONTEXT_NOT_SELECTED`).
- Stronger than I had credited: `admit_native_context` already refuses
  `native.native-context-compiler-version-not-from-manifest` unless the context's compiler version
  equals the admitted tool closure's `semanticVersion`, **for both languages**. Binding to it
  inherits a real chain — closure manifest → admitted context → body frame — not a copied string.

**My v4 sentence "Rust's `ResolvedInputs` carries no rustc toolchain identity today" was false and
is withdrawn, not defended.** The TypeScript choice of `languageMode` + `synthesizerVersion`
described option synthesis, not the language, and is withdrawn too. No new universe field was
needed for the compiler half, and none was added for it.

## 2. Concern 2 — the recipe was not representable. Also right.

`edition` is a map from crate **name** to year, so `C({edition: map})` grows with the workspace.
Root's retained vector — 21 entries, **723 bytes** — exceeds the inherited frame's `u8` component
maximum of **255**. The suite now reproduces that exact number as a check
(`root-vector-raw-edition-map-would-exceed-the-inherited-u8-component`). Beyond the bound, the map
was also semantically wrong: it made one body's identity depend on unrelated crates.

**Replacement:** `languageVersion` is the **raw 32 bytes of
`SHA-256(C(body-language-version))`** — the same fixed-width treatment the inherited grammar already
gives `levelVersion`, so the inherited frame bytes and field grammar are unchanged and the component
is bounded for every valid input. Measured: 32 bytes for both languages, all five components ≤ 255.

`body-language-version` is a new closed record in `foundation/identity-schemas.v2.json`, retention
**`derived`** (existing vocabulary, not a new one). No field is a free input; every field is copied
from a named path in a record the Run already retains and the owning contract already admitted; the
closure **recomputes** it.

| Field | TypeScript | Rust |
|---|---|---|
| `compilerName` | context `toolchain.compilerName` | `"rustc"` (declared const) |
| `compilerVersion` | context `toolchain.compilerVersion` | context `toolchain.rustcVersion` |
| `compilerBuild` | context `toolchain.compilerPackageDigest` | context `toolchain.rustCommitHash` |
| `dialect` | `{sourceVariant}` from the body's own suffix | `{edition}` effective for the owning target |
| `languageId` | derived from the variant: `typescript` or `javascript` | `rust` |

Every excluded field is listed **in the registry with its reason**: `targetTriple`, `hostTriple`,
`sysrootDigest`, `rustcDevLlvmDigest`, `standardLibraryComponentDigests`,
`typescriptStdlibMerkleRoot`, `libSelection`, `cargoVersion`, `resolverVersion`, `crateRootPaths`,
`packageModuleType`, `languageMode`, `synthesizerVersion`, the edition map's keys and the anchor
path. The line is *what identifies the component that interprets the body span*, not what the
program resolves against, not where it ran, and not how it was assembled.

## 3. Mixed-edition ownership — decided by root, designed here, exercised end to end

Root's v5 note authorised this and required it not be left as a categorical gap. Root also correctly
rejected the obvious shortcut: a crate-name-to-root map cannot identify arbitrary module paths,
because `#[path]`, files shared by several targets, and several compilation contexts of one crate
all defeat a directory rule.

**New: `native.source-unit-ownership.v1` / `SourceUnitOwnershipV1`**, referenced by a new
`RustUniverseV2ResolvedInputs.sourceUnitOwnershipId` — **required and nullable**, exactly the shape
`preparedOutputSetId` already has, so it follows an existing precedent rather than inventing one.

```
SourceUnitOwnershipV1 { schemaVersion, enumeration: complete|partial,
                        ownership: [ {path, unitId, crateName, targetEdition} ] }
```

Minimal by construction: it is a **relation, not an inference**. `unitId` distinguishes several
compilation contexts of one crate. `enumeration` makes the *absence* of a row a stated claim rather
than a silence. `targetEdition` is `null` for a target that takes its package default and so
**defers** to the universe's `edition` map — see §3a, which is why that column exists at all.

**Selection is exact and total.** Rows whose `path` **equals** the enclosing fact's anchor path —
never a prefix, never a nearest directory, never a first match. Several owners that **agree** are
admissible (the ordinary shared-file and lib-plus-test-target case). Everything else refuses with
its own cause: `BODY_LANGUAGE_OWNER_AMBIGUOUS` (owners disagree, or a deferring row names a crate
the universe has no edition for), `BODY_LANGUAGE_OWNER_NOT_COMPILED` (no row, `complete`),
`BODY_LANGUAGE_OWNER_UNENUMERATED` (no row, `partial`), `BODY_LANGUAGE_OWNERSHIP_REQUIRED` (no
ownership committed at all), `BODY_LANGUAGE_DIALECT_ABSENT` (empty map). `bind_rust_universe`
independently requires every owned `path` to be a source of the same snapshot and every `crateName`
to be a key of the same `edition` map.

**The requirement root actually set is met:** an ordinary mixed-edition workspace has a
representable valid form. The suite builds one and closes, replays and **commits** a clone Run for a
body at edition **2021** and another at **2015** *in the same universe*, with different body
identities. Only a path genuinely compiled under two different editions refuses — a real ambiguity
in the input, not a gap in the law. No compiler is admitted, no build is measured, no enumerator is
qualified: the record states what a producer claims it enumerated.

## 3a. Target edition, not package default — root's primary-source refinement

Root checked Cargo's current documentation and is right: a **target** may set its own `edition`,
defaulting to `package.edition` when absent (`cargo metadata` lists `targets[].edition` and states
the package value is a default individual targets may differ from; the `[[bin]]`/`[lib]` field is
deprecated but still documented). So *source → package → package edition* misses a supported
override.

Root also found a real soundness bug in my in-progress code: `if len(distinct)==1: selected=...`
skipped the ownership relation whenever the package defaults agreed. **That is unsound once target
overrides exist, and it is gone.** There is now **no fast path at all**: a `clones` fact over a Rust
universe requires the committed ownership relation whatever the package map looks like, and a null
`sourceUnitOwnershipId` admits no clone (`BODY_LANGUAGE_OWNERSHIP_REQUIRED`).

Each ownership row gained `targetEdition`: the target's own edition when it sets one, `null` when it
takes the package default. `null` **defers** to the map, so the two committed places cannot
contradict — an override is explicit and visible, and so is its absence. The effective edition is
`targetEdition ?? edition[crateName]`.

The discriminating vector root asked for is in the suite: **one package, two targets, two
editions**, where `len(set(package_map.values())) == 1` and the package map therefore could not
distinguish the two bodies. Both close, replay and commit; their body identities differ; withdrawing
the override invalidates the previously valid body identity; and a second target claiming a third
edition for the same path refuses. No Cargo, build script or repository read is executed — the rows
are retained native observations.

## 4. TypeScript — root asked me to inspect it, and the null boundary was not safe

Root asked whether the `null` dialect left `.tsx`/`.js`/`.ts` reproducibly specified. **It did not.**
Two identical spans in `a.ts` and `a.tsx` would have received the same `bodyIdentity` — a silent
false equation, which is the one direction this evidence must never fail in.

The TypeScript dialect is now `{sourceVariant}`, selected from the body's own file suffix by a
**closed longest-suffix table** (`.d.ts` never read as `.ts`), covering `.ts .tsx .mts .cts .d.ts
.js .jsx .mjs .cjs`. An unlisted suffix **refuses** (`BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`) rather
than being folded into a neighbour, so no normal variant is silently mis-assigned and a new one must
be registered deliberately. Distinct suffixes stay distinct even where a parser would treat two
alike: **this can fail to equate two equivalent bodies and can never equate two the language reads
differently.** Collapsing variants is a claim about a parser and belongs to the level specification.

**This changes every TypeScript `bodyIdentity` value.** There is now **no `null` dialect branch** at
all: every language declares its axis and its selection law, so there is no unexamined default left.

**Version identity versus equivalence, stated in the contract:** two bodies sharing a `bodyIdentity`
is evidence that their *normalized bodies agree under one language version at one level*. It is not
semantic equivalence, not a cross-language or cross-variant claim, and not a statement about any
normalizer's correctness.

## 4a. Body language is not provider language — native §6.3/§6.4

Root checked native §6.3 and is right again. It closes the normalized-body `languageId` to
`{typescript, javascript, rust}` precisely so a `.ts` and a `.js` body never group even with
identical bytes, and §6.4 keeps `cross-tsjs` a **candidate-only** projection. My code checked the
frame's `languageId` against `universe_row['language']` — always `typescript` for that engine — and
my TypeScript binding fixed `languageId: 'typescript'`. **A JavaScript body could not carry the
declared `javascript` identifier.** That is now fixed:

- `languageId` is **derived from the selected source variant** by a registry-carried selector
  (`bodyLanguageByVariant`): `js/jsx/mjs/cjs → javascript`, `ts/tsx/mts/cts/ts-declaration →
  typescript`, Rust → `rust`. The record's enum is `{typescript, javascript, rust}`.
- The frame's `languageId` and the record's come from **one derivation over one anchor**, so they
  cannot disagree; the frame's must also be a language the universe's binding declares that engine
  produces (`bodyLanguages`), so a `rust` frame under a TypeScript universe refuses.
- The provider stays the provider: the same TypeScript **engine** universe reads both. No JavaScript
  body is rewritten as TypeScript, and the `cross-tsjs` design is untouched.

Exercised, not asserted: a **real JavaScript clone Run through the TypeScript engine universe**
prepares, replays and **commits**; its frame carries `javascript`; and a `.js` body with **byte
identical** source to the `.ts` body has a **different** `bodyIdentity`. Negatives: a frame naming
`rust` under that universe, and a frame naming `javascript` over a TypeScript body, each refuse at
`BODY_IDENTITY_LANGUAGE_JOIN`.

## 5. Owned files changed, exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `8d752cf624fb8d5007639cc94febaf5588bf829369dc449bc4074c7863fef6f1` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `3db88d625142a2b20632c37cd247dd9a2a8e24c757137f68c7f5548cecaaffd0` |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `23b78b906306e060aef8f1558566767530cdb4d4b08707eb07271e52d5a04480` |
| `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `7b3dcd0671d6352106a8d513f5d0cffed2f513e3f037c35739d572f1e3395b20` |
| `docs/coop/design-corrections/foundation/identity-model.py` | `a2184ed146348f588f7e4cdb7c5e894f90d9d985c1fa2cf5aca894c1633c1c56` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `a2d409d8a9cdc733b43c0b6f4bb0c47068d60ef868d13eac38de52a1d3b05406` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `0a4290e530c6fa1a3f25e9c9f9dff051bda5dd4d9b32c380452312986e01d43c` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `67bedaba1896317ff60c2a09acfdfb4931e73b6761257a1772c4ed75e5d2d0d9` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `687409136a677f2c097708eac7cfddb7048c41944e85bc5a9b81c6b19f08d571` |

Three native files are new to my ownership this session, used only where the join required it, under
the authorisation in your v5 note. Nothing else in the tree was written by me: no workflow, security,
`canonical.py`, integration, public registry, pin manifest, generated report, governance or README
file. `native-evidence-report.v2.json` is byte-identical to the frozen v8 image
(`164b5c2241f5dd9fb61c129778f04f330a9276a1b250a4c4f01ec8e7fd1b2b74`) — I ran the native and security
checkers **out of tree** this time precisely to avoid the v4 incident.

Everything from v4 survives and is re-verified: the file/package/vcs-change snapshot joins, the
clone frame/source/level custody, the typed array and registry laws, the body-versus-fact
distinction, the budget prose, and root's workflow changes. Root's own file counterexample re-runs
green against this source: control closes, replays and commits; `RELATION_FILE_CONTENT_JOIN`,
`RELATION_FILE_LENGTH_JOIN` and `RELATION_PATH_NOT_INVENTORIED` each still refuse.

## 6. One thing root must fix, and it is one line

`check-integration.py` **currently fails** at `H_FRAME_RECORD:native.semantic-universe.rust.v2`,
because the stale copied builder writes a Rust universe without the now-required
`sourceUnitOwnershipId`. I did not edit your file. I verified out of tree that this single addition
at `integration-fixtures.py:199` restores **363/363**:

```python
universe={'schemaVersion':2,'edition':{'fixture-root':2021},'sourceUnitOwnershipId':None,
```

I chose *required and nullable* over *optional* deliberately: `preparedOutputSetId` sets the
precedent, every other property of that record is required, and a producer should have to **say**
whether it committed ownership rather than omit it. The cost is this one line in a file you own.

## 7. Development checks

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **559 / 559**, 0 failed (481 at v4 release) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, **151 / 151** cases (one new, covering the ownership record and its target-edition column), 60 matrix cells, 0 open objects, 0 uncovered feedback — out-of-tree sandbox, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same sandbox |
| `check-integration.py` | **FAILS in tree** (§6); **363 / 363** with the one-line fix, verified out of tree |

Discriminating checks added, all with controls: a same-package two-target/two-edition pair that the
package map alone could not distinguish; a real JavaScript clone Run through the TypeScript engine
universe, with a byte-identical `.ts` body proved to have a different identity; both languages'
complete clone Runs through
closure/replay/commit; component is 32 raw bytes and every component ≤ 255; an independent
restatement reproduces the component byte for byte; a changed `compilerVersion`, `compilerBuild`,
`compilerName` or dialect each invalidates a stale body identity; renaming crates, adding a cfg set
and a 21-crate workspace each leave the body identity **byte-identical**; raw `C` ≠ raw SHA-256 ≠
`H`, and raw digest bytes ≠ hex text; mixed-edition bodies at 2021 and 2015 both commit and differ;
withdrawn, partial, disagreeing, unknown-crate and uninventoried owner rows each refuse with their
own cause; every listed TypeScript variant is distinguished and an unlisted one refuses; the model
and the independent fixture agree on every listed variant.

Probes in `probes/`, every executed attempt retained with a truthful in-file label:

- `probe-language-version-joins-are-load-bearing.v3.py` — neutralises the two rules *separately*,
  because one stub cannot measure both, and models the forbidden guess exactly (arbitrary first
  match in canonical row order). Load-bearing: all six stale-version cases plus
  `no-committed-ownership` and `owners-disagree`. Every positive vector closes, including a mixed
  **package** map whose committed ownership still resolves the body to its own edition — the package
  map is not the dialect.
- **Honest negative result:** `empty-edition-absent` is **not measurable by Run-level
  neutralisation**, and I am reporting that rather than a status I did not establish. Any permissive
  fallback must *invent* a dialect, and an invented value never matches an already-minted frame. It
  is measured at the boundary where the rule lives — the pure projection function — which shows a
  guessing implementation silently choosing `2015` for an empty map and `2021` for a mixed one.
- Three superseded runs are retained and labelled in file, and none is evidence about the shipped
  negatives: `…v1-PARTIAL` neutralised the projection wholesale and so deleted the dialect rule it
  meant to measure; `…v2-STALE-STUB-SIGNATURE` ran after the function gained parameters its stubs
  had not, so every neutralised case died with a `TypeError`; `…v3-STALE-GUESS-STUB` ran after the
  target-edition change while the stub still implemented the package-map rule. Each is the same
  class of defect — a probe lagging the source — and each is labelled as such rather than quietly
  replaced.

## 8. New normative inputs for the blind kit

Beyond `fact-identity-policy.v2`, `resolved-inputs.v2` and both registries, which you already carry:

```
native/native-evidence.schemas.v2.json     #/$defs/SourceUnitOwnershipV1
                                           #/$defs/RustUniverseV2ResolvedInputs/properties/sourceUnitOwnershipId
foundation/identity-schemas.v2.json        #/$defs/body-language-version
                                           #/x-opensip-digest-domains/languageVersionBindingLaw
                                           #/x-opensip-digest-domains/domainSets/native-semantic-universe/*/languageVersionBinding
                                           #/x-opensip-digest-domains/domainSets/native-nested/native.source-unit-ownership.v1
```

All inside documents already on the list; no new file was created.

## 9. APIs and shared-builder declarations

Model: `M.body_language_version(universe, context, row, anchor, retained=None)` (pure);
`N.SOURCE_UNIT_OWNERSHIP_DOMAIN`; `N.source_unit_ownership_identity(ownership)`;
`rust_universe_retained_input_faults` gains the ownership joins; `snapshot_joins` accepts a
`pathField` so an `inventoried-paths` row may be a record.

Fixture, all additions defaulted and backwards compatible with your file counterexample runner —
`build(relation='file')` and `relation_fixture` keep working as it uses them:
`build(..., workspace=None)`, `native_inputs(..., workspace=None)`, `rust_inputs(..., workspace=None)`,
`relation_fixture(..., context_record=None, ownership=None)`,
`file_fact_mutation(mutate, relation='file', universe_language='typescript')`,
`clone_run_with_universe(mutate_universe, language='rust', mutate_ownership=None, source_path=None, workspace=None)`,
plus new `body_language_version`, `projection_inputs`, `universe_and_context`, `clone_frame_of`,
`MIXED_WORKSPACE`, `LARGE_EDITION`, `UNIVERSE_ROW`, `BINDING`. The v4 additions stand:
`LEVEL_SPECIFICATION`, `framed_body_preimage`, `relation_fixture`, relation-aware `FILTER_FIELD_OF`,
`build`'s `relation` parameter, rung-derived `coverage_result`. `TS_SOURCES` also gained an
inventoried workspace `package.json` in v4.

## 10. Limitations, stated plainly

- **Every Rust universe carrying `clones` facts must now commit a `SourceUnitOwnershipV1`.** That is
  a real new obligation on producers, and it is the direct consequence of target-level edition
  overrides: without the relation there is no sound dialect. Rust universes carrying no clone
  evidence may still set it null.
- **A path genuinely compiled under two different editions still refuses.** That is a real ambiguity
  in the input and one body identity cannot represent it. If the product later needs such a body,
  the clone payload would have to name its owning unit, and the inherited payload field set is
  fixed — so that is a FACT-IDENTITY change, not one I can make here.
- `enumeration: complete|partial` records what a producer **claims** it enumerated. Nothing here
  verifies the claim, and nothing here qualifies an enumerator, a compiler or a build.
- Only `L0-verbatim` is recomputed through a complete Run; L1–L3 remain retained custody plus
  framing. No normalizer is qualified and no tokenisation is graded.
- The TypeScript suffix table is deliberately conservative and will **under-detect** clones across
  variants a parser would treat alike. Collapsing them is a level-specification decision.
- `compilerBuild` holds a 40-hex commit for Rust and a 64-hex digest for TypeScript, so it is not a
  64-hex field of this bundle and carries no `x-opensip-digest`. That is stated in the schema
  description rather than left as an apparent omission: it is an owner-admitted identity inside a
  derived record, joined by equality and never re-hashed here.
- `LEVEL_SPECIFICATION` remains a fixture stand-in for the retained canonical level specification;
  its content is FACT-IDENTITY's.
- Native and security suites were run out of tree with regenerated pins; the in-tree pin refresh is
  yours.
- Design/reference evidence over synthetic fixtures only. No compiler, Cargo, OS or repository code
  was executed; no platform, parser, normalizer or product behaviour is qualified.

---

**No acceptance, no readiness, and I do not claim all gaps are closed.** Corrected v9 freeze, fresh
independent review at zero unresolved MUST/SHOULD, new blind, and the full application review all
remain required. Capture these exact source images before your integration changes, as agreed.
