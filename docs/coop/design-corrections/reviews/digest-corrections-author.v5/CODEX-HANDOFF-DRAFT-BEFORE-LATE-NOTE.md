# HANDOFF — actual Claude coauthor, v5 (root's CRITICAL concerns 1 and 2, and the mixed-edition decision)

**Standing: not accepted, not qualified, not promoted, nothing closed.** A corrected v9 freeze, a
fresh independent review with **zero unresolved MUST/SHOULD**, a new blind, and the full application
review all remain required. I make no acceptance or readiness claim, and I do not claim that all
gaps are closed.

I read the **final** text of `digest-corrections-author.v4/CODEX-PUBLIC-NOTE.md` — including
paragraphs 9 and 11, which my v4 handoff had not seen and therefore did not assess — and the v5
`CODEX-PUBLIC-NOTE.md`, again immediately before writing this.

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
| `dialect` | `{sourceVariant}` from the body's own suffix | `{edition}` of the owning unit |

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
                        ownership: [ {path, unitId, crateName} ] }
```

Minimal by construction: it is a **relation, not an inference**, and it carries **no edition of its
own** — the year comes from the universe's already-committed `edition` map keyed by `crateName`, so
the record can never contradict it. `unitId` distinguishes several compilation contexts of one
crate. `enumeration` makes the *absence* of a row a stated claim rather than a silence.

**Selection is exact and total.** Rows whose `path` **equals** the enclosing fact's anchor path —
never a prefix, never a nearest directory, never a first match. Several owners that **agree** are
admissible (the ordinary shared-file and lib-plus-test-target case). Everything else refuses with
its own cause: `BODY_LANGUAGE_OWNER_AMBIGUOUS` (owners disagree, or name a crate the universe has no
edition for), `BODY_LANGUAGE_OWNER_NOT_COMPILED` (no row, `complete`),
`BODY_LANGUAGE_OWNER_UNENUMERATED` (no row, `partial`), `BODY_LANGUAGE_OWNERSHIP_REQUIRED` (mixed
editions, no ownership committed), `BODY_LANGUAGE_DIALECT_ABSENT` (empty map). `bind_rust_universe`
independently requires every owned `path` to be a source of the same snapshot and every `crateName`
to be a key of the same `edition` map.

**The requirement root actually set is met:** an ordinary mixed-edition workspace has a
representable valid form. The suite builds one and closes, replays and **commits** a clone Run for a
body at edition **2021** and another at **2015** *in the same universe*, with different body
identities. Only a path genuinely compiled under two different editions refuses — a real ambiguity
in the input, not a gap in the law. No compiler is admitted, no build is measured, no enumerator is
qualified: the record states what a producer claims it enumerated.

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

## 5. Owned files changed, exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `1ce2236e27537b14b24ad11f11d2a8497c0c78e70f23f4aa104e74678e8d113c` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `9048f9c25ec5ed657031c9c12ec4d5480ab11e14784f7554efd3156d7f5a0a68` |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `bd89c4a36d6eab11ef48093c913ba3f0b5f86186ed7d86fc82d1b0a682a162ff` |
| `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `7b3dcd0671d6352106a8d513f5d0cffed2f513e3f037c35739d572f1e3395b20` |
| `docs/coop/design-corrections/foundation/identity-model.py` | `798a6ead734d5c5255bd973b7a387c6d3b5cdd656658f9c1ae1fd1ef9f19af92` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `ef121880536661ce599d408b58bb042216d9e0641d7b1e9c85a0427e3a7d1c0e` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `bf657d62ab2c8e087230caa29a2123ffd6a2aafc10a81800725cf7040780f328` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `67bedaba1896317ff60c2a09acfdfb4931e73b6761257a1772c4ed75e5d2d0d9` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `81f5e296ea61f40c37d2307f7ab18f71bc6f8f9519fc14369e572f49c06fff4d` |

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
| `foundation/check-identity.py` | **540 / 540**, 0 failed (515 before the ownership work, 481 at v4 release) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, **151 / 151** cases (one new), 60 matrix cells, 0 open objects, 0 uncovered feedback — out-of-tree sandbox, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same sandbox |
| `check-integration.py` | **FAILS in tree** (§6); **363 / 363** with the one-line fix, verified out of tree |

Discriminating checks added, all with controls: both languages' complete clone Runs through
closure/replay/commit; component is 32 raw bytes and every component ≤ 255; an independent
restatement reproduces the component byte for byte; a changed `compilerVersion`, `compilerBuild`,
`compilerName` or dialect each invalidates a stale body identity; renaming crates, adding a cfg set
and a 21-crate workspace each leave the body identity **byte-identical**; raw `C` ≠ raw SHA-256 ≠
`H`, and raw digest bytes ≠ hex text; mixed-edition bodies at 2021 and 2015 both commit and differ;
withdrawn, partial, disagreeing, unknown-crate and uninventoried owner rows each refuse with their
own cause; every listed TypeScript variant is distinguished and an unlisted one refuses; the model
and the independent fixture agree on every listed variant.

Probes in `probes/`, every executed attempt retained with a truthful in-file label:

- `probe-language-version-joins-are-load-bearing.v2.py` — neutralises the two rules *separately*,
  because one stub cannot measure both. Load-bearing: all six stale-version cases, plus
  `mixed-edition-no-ownership` and `owners-disagree`. Positives that must close all close.
- **Honest negative result:** `empty-edition-absent` is **not measurable by Run-level
  neutralisation**, and I am reporting that rather than a status I did not establish. Any permissive
  fallback must *invent* a dialect, and an invented value never matches an already-minted frame. It
  is measured at the boundary where the rule lives — the pure projection function — which shows a
  guessing implementation silently choosing `2015` for an empty map and `2021` for a mixed one.
- `…v1-PARTIAL.py` and `…v2-STALE-STUB-SIGNATURE.json` — retained, superseded, labelled. The first
  neutralised the projection wholesale and so could not measure the dialect rule; the second ran
  after the function gained parameters its stubs had not, so every neutralised case died with a
  `TypeError` and `loadBearing` came out empty. Neither is evidence about the shipped negatives.

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
