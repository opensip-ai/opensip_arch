# HANDOFF — actual Claude coauthor, v6 (selected compilation unit; unit-key recipe; partial-Coverage bypass)

**Standing: not accepted, not qualified, not promoted, nothing closed.** After a corrected freeze:
an actual fresh independent review with **zero unresolved MUST/SHOULD**, then a new blind, then the
complete independent application review and readiness reconciliation. I make no acceptance or
readiness claim and I do not claim all gaps are closed.

**Notes actually READ, by byte hash, content inspected rather than hashed:**

| When | File | Bytes | SHA-256 |
|---|---|---|---|
| before this batch | `digest-corrections-author.v5/CODEX-PUBLIC-NOTE.md` | 8547 | `37c3d306ba6dae482395c4085597a314982ae12ad6bf94e6e204e97072cc5baf` |
| mid-batch and again at finalisation | `digest-corrections-author.v6/CODEX-PUBLIC-NOTE.md` | 4460 | `50c0e7282f18ded8053ce2df3e981d9b4bd77a9fd1b3f7f11212278258ff58fc` |

The v5 note included the section *"Required final representation decision: shared path with distinct
target editions"*, which my v5 handoff never assessed. The v6 note grew from 2855 to 4460 bytes
during this session; I read both states, and the section added later — the executed partial-Coverage
counterexample — is closed below.

---

## 1. The remaining gap, and my v5 §10 was wrong

v5 §10 called the shared-path/two-edition case "a FACT-IDENTITY change, not one I can make here",
because the inherited clone payload field set is fixed. **The inherited field set was never an
authorization blocker, and it did not even need to change.** The selection belongs in the *retained
native ownership input*, not in the payload. Withdrawn.

## 2. Selection, committed where it makes a distinct universe

`SourceUnitOwnershipV1` now holds three things:

```
{ schemaVersion, enumeration: complete|partial,
  units:           [ {unitId, markerPath, crateName, targetKind, targetName, targetEdition} ],
  selectedUnitIds: [ unitId, … ]  (minItems 1),
  ownership:       [ {path, unitId} ] }
```

`sourceUnitOwnershipId` is `H(native.source-unit-ownership.v1, record)`, so **the selection is
inside the identity**: a different selection is a different record, a different id and therefore a
different `sourceUniverse`. The same physical `src/lib.rs`, compiled by a 2021 `lib` target and a
2015 `bin` target of the same package, is validly analysed **under each selection**, each with its
own dialect and its own `bodyIdentity`, and **no relation payload changed**.

Decision order is fixed and every step has its own cause: no committed ownership
(`BODY_LANGUAGE_OWNERSHIP_REQUIRED`) → `partial` enumeration, **before any row is read**
(`BODY_LANGUAGE_OWNER_UNENUMERATED`) → exact path equality, no row
(`BODY_LANGUAGE_OWNER_NOT_COMPILED`) → restriction to `selectedUnitIds`, none selected
(`BODY_LANGUAGE_OWNER_NOT_SELECTED`) → selected owners disagree
(`BODY_LANGUAGE_OWNER_AMBIGUOUS`). Selected owners that **agree** are admissible.

**Selected scope is not incomplete enumeration**, and the closure enforces the difference. A
selection says the named targets *are* the analysis — an owner outside them is out of scope, and
because the selection is in the identity it is visible to every consumer. `partial` says the
producer did not finish — an owner *inside* the scope may exist, unlisted, that could contradict a
listed one — so no dialect is admissible at all, checked first, so partial discovery can never act
as an implicit edition selection. Silently omitting a conflicting owner is not a selection either:
an omission leaves no trace, and the suite shows the two records have different identities.

## 3. Root's unit-key refinement — accepted, my recipe withdrawn

Root is right: `markerPath#targetKind:targetName` was injective **only** by excluding `#` from
`markerPath`, and a `#` in a repository directory is admissible under the canonical repository-path
contract. Narrowing admitted paths to make a delimiter work is the wrong trade. Withdrawn.

```
unitId = H(native.compilation-unit.v1,
           UnitIdentityV1{schemaVersion: 1, markerPath, targetKind, targetName})
```

carried as `sha256:<64 hex>`, retention **`derived`** — nothing separate is retained because the
preimage *is* the row, and admission re-derives and compares. **Not an opaque digest:** the preimage
record, its domain, its codec and its selector are all published in the native schema and named in
the contract. `markerPath` is back to the ordinary canonical repository path with no added
restriction. Verified in the suite: the identity is fixed width for a 4000-character marker path and
a 250-character target name; a marker under `crates/c#interop/` validates, derives, **and closes a
complete Run**; and two markers differing only inside that `#` directory still differ.

## 4. Root's stability point — measured, and my wording corrected

My v6 interface note said "every Rust `bodyIdentity` changes again". **That was an assumption and it
was wrong.** The projection excludes unit ids, names, paths, the selection and the ownership id, so
moving the same effective edition into a units table must not move it. Measured across the two
actual source images — the retained v5 image overlaid on a current tree, and the current tree —
in `probes/probe-body-identity-stability-across-v5-and-v6.v1.py`:

- **unchanged:** `bodyIdentity`, the language-version component, the projection's canonical bytes,
  `normalisationVersion`, the anchor path.
- **changed:** `sourceUnitOwnershipId`, `sourceUniverse`.

An in-suite invariant asserts the same thing directly, and a companion check confirms that changing
the actual **selected edition** still moves the body identity.

## 5. Root's executed partial-Coverage counterexample — a real bypass, now closed

Root's evidence was exact: with the same partial ownership and the same empty view, `resolved=False`
gave the honest `unknown`/indeterminate Run, while `resolved=True` gave `coverage: complete`, no
deficiency and a determinate `fail` seal — and **that also closed, replayed and committed**. My
`EMPTY_CLONE` example only showed the honest case; it never forced the host to refuse the opposite.
Root is also right about where the join must live: `body_language_version` is never reached on an
empty view, so payload-only validation cannot see this. The Run can.

New `coverage_dialect_prerequisite`, applied in `close_run`'s Coverage loop **after** the native
producer admission, for any scope whose relation has a `bodyIdentityJoin`: if the scope's universe
can produce **no** dialect for any body — no committed ownership, or `enumeration != complete` —
then `coverage: complete` refuses (`COVERAGE_DIALECT_PREREQUISITE`) and an undisclosed entry
refuses (`COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED`). It sits in the closure loop, outside the
payload decode memo entirely.

The prerequisite is **universe level by design**, and that boundary is stated rather than stretched:
a *per-body* refusal — an unowned path, an owner outside the selection — is perfectly compatible
with `complete`, because the host examined that subject and correctly produced no fact for it. A
check asserts exactly that, so the rule cannot quietly grow into refusing honest empty findings.

**Root's own construction, re-run against this source**
(`probes/probe-root-partial-coverage-rerun.v1.py`): the honest control still closes, replays and
**commits** with an indeterminate seal; the contradictory claim now refuses with
`COVERAGE_DIALECT_PREREQUISITE:clones:enumeration-partial`. The absent-ownership variant refuses
with `:no-committed-ownership`, and both disclosed variants remain admissible.

## 6. Owned files changed, exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `49f24fb5ec5d229708f27e2588314828c6d2aa1cbdfbeba892924429b32029ef` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `0f5c034b4044f8c4d04dc2b1aad2eae7952e315142bcd6e70143bcc615b8244e` |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `0929731d1d62cd6ba5a4d1328ef6d3919c1b21f2c90fde48a3623020cb62ddc4` |
| `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `7b3dcd0671d6352106a8d513f5d0cffed2f513e3f037c35739d572f1e3395b20` (unchanged this session) |
| `docs/coop/design-corrections/foundation/identity-model.py` | `1a563aa17186fee697b48489dd14837a5f50aa87f00ec2495895f44f984838c9` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `d07cfe7f1a425e69b2386173e1f35d37ff17886b0775bb2b976ff22e994af25f` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `394cf4ff8688d8466cac789bed774842f00a511c0b2e3976a7250fc0749df7ce` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `327b0c06b82a5c32d133f611761d3a04136f6ed169a96d11b3322ace64a50c82` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `ed06144f4413b601d8ddaf678c5ccf06c80680e81523fa6de93aae1143075b71` |

No workflow, security, `canonical.py`, integration, pin, generated in-tree report or governance file
was written. `native-evidence-report.v2.json` remains byte-identical to the frozen v8 image
(`164b5c2241f5dd9fb61c129778f04f330a9276a1b250a4c4f01ec8e7fd1b2b74`); native and security were run
out of tree.

**One honest process note.** Mid-session a slice with an inverted boundary made `s.replace("", …)`
insert text between every character of `check-identity.py` (it grew to 624 MB). I restored the file
byte-identically from the retained v5 image
(`a2d409d8a9cdc733b43c0b6f4bb0c47068d60ef868d13eac38de52a1d3b05406`, matching that session's
handoff) and replayed the v6 edits in three verified stages. Nothing was lost and no other file was
touched, but it is recorded rather than quietly repaired.

## 7. Complete minimal shared-builder declaration set

Root has 44 and a prepared 48. The **actual transitive closure** of `build`, `native_inputs`,
`rust_inputs`, `relation_fixture`, `replay`, the re-key/resync helpers and `graph_with_import` is
**54 declarations**, in dependency order, machine-computed and retained at
`runs/shared-builder-declarations.json`:

```
H, spec, M, C, load, W, N, NATIVE_FIXTURES, ATOM, rule_for, policy_for, WAIVERS,
compiled_program, DELIVERY, CAPABILITY_RECIPE, INHERITED_MANIFEST_BYTES,
current_capability_manifest, CURRENT_CAPABILITY_MANIFEST_BYTES, RELATION_DOCUMENT,
RELATION_DOCUMENT_BYTES, NATIVE_DOCUMENT, NATIVE_DOCUMENT_BYTES, STAGE_OUTPUT_SCHEMA,
TS_SOURCES, TS_NODE_MODULES, RUST_TARGET, RUST_DEP_KEY, RUST_DEP_FILE,
RUST_PROJECTED_CONFIG, RUST_SOURCES, RUST_PREPARED_DIRECTIVES, REFERENCES_PAYLOAD,
FILTER_FIELD_OF, coverage_result, rust_inputs, native_inputs, LANGUAGE_FIXTURE,
LEVEL_SPECIFICATION, framed_body_preimage, body_language_version, unit, UID,
relation_fixture, build, replay, sort_canonical_sets, rekey, put_blob,
resync_stage_spec, resync_coverage, resync_witness, resync_proof_refs, rekey_plan,
graph_with_import
```

Not needed by the builder, and deliberately excluded: `results`, `check`, `rejects`,
`not_admitted`, `rejects_because`, `RULE`, `POLICY`, `FACT_IDENTITY_POLICY`,
`RELATION_DOCUMENT_DIGEST`, `NATIVE_DOCUMENT_DIGEST`, `RELATION_REGISTRY`.

New since your prepared 48: `unit(marker, kind, name, crate, edition=None)` and
`UID(marker, kind, name)` — the two helpers that mint a derived unit identity; everything else is a
signature change. Exact signatures (also in `runs/builder-signatures.json`):

```
build(resolved=True, has_match=False, source_path=None, with_finding=False,
      stdlib_body=b'declare const es2022: unknown;\n', universe_language='typescript',
      prepared=None, grant_operations=None, relation='references', workspace=None)
native_inputs(objects, blobs, add, blob, stdlib_body=…, prepared=None, ts_inventory=(),
              ts_source_path='a.ts', workspace=None)
rust_inputs(objects, blobs, add, blob, tree, dep_body=RUST_DEP_FILE, prepared=None, workspace=None)
relation_fixture(relation, source_path, source_body, source, universe_record, universe_domain,
                 blob, context_record=None, ownership=None)
body_language_version(universe_record, context_record, domain_row, anchor, retained=None)
framed_body_preimage(level, level_version, language_id, language_version, payload)
coverage_result(scope_descriptor, universe, resolved)
rule_for(language, atom=None, subject_kind='symbol')
policy_for(language, atom=None, subject_kind='symbol')
replay(plan, objects, blobs, evaluation_refs)
unit(marker, kind, name, crate, edition=None)      UID(marker, kind, name)
```

`build(relation='file')` and `relation_fixture`'s positional prefix are unchanged, so your file
counterexample runner keeps working. The `workspace` descriptor is
`{edition, enumeration, units, selectedUnitIds, ownership}`.

**The single integration line is unchanged from v5** and remains the only integration edit:
`'sourceUnitOwnershipId':None` at `integration-fixtures.py:199`. Verified out of tree again: 363/363.

## 8. New normative inputs for the blind kit

```
native/native-evidence.schemas.v2.json   #/$defs/SourceUnitOwnershipV1
                                         #/$defs/UnitIdentityV1
                                         #/$defs/RustUniverseV2ResolvedInputs/properties/sourceUnitOwnershipId
foundation/identity-schemas.v2.json      #/$defs/body-language-version
                                         #/x-opensip-digest-domains/languageVersionBindingLaw
                                         #/x-opensip-digest-domains/domainSets/native-semantic-universe/*/languageVersionBinding
                                         #/x-opensip-digest-domains/domainSets/native-nested/native.source-unit-ownership.v1
```

New H domains named in native §11: `native.source-unit-ownership.v1`,
`native.compilation-unit.v1`. No new file was created in any session; all selectors are inside
documents already on the kit list.

## 9. Development checks

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **602 / 602**, 0 failed (597 before the Coverage join; 589 before the unit-key change) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, 151 / 151, 72 / 72 annotated digest sites — out of tree, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — out of tree |
| `check-integration.py` | fails in tree on the stale builder; **363 / 363** with the one line, out of tree |

Preserved vectors re-run green on this source: the JS body through the TypeScript engine, the
target override with identical package defaults, the 723-byte predecessor input now a 32-byte
component, root's three file-claim refusals with the control committing, and the budget-equality
join.

Probes, every executed attempt retained and labelled:

- `probe-selected-unit-joins-are-load-bearing.v2.py` — **all ten** negatives load-bearing, every
  positive closes.
- `probe-selected-unit-joins-are-load-bearing.v1.py` / `…v1-STALE-LITERAL-UNIT-IDS.json` —
  superseded, labelled: it ran after `unitId` became an H identity while still carrying the
  withdrawn literal ids, so three rows measured a schema refusal rather than a selection rule.
- `probe-body-identity-stability-across-v5-and-v6.v1.py` — the stability measurement in §4.
- `probe-root-partial-coverage-rerun.v1.py` — root's construction in §5.

## 10. Limitations

- A single selection cannot represent a body at two editions **at once**; that is the point, and the
  ambiguous unselected request refuses. Two editions need two Runs over two selections.
- `enumeration` and every ownership row record what a producer **claims**. Nothing here verifies the
  claim against a real repository, executes Cargo or a build script, or qualifies an enumerator,
  compiler or OS. Schema validity is not a completeness claim about reality, and the contract now
  says so.
- The Coverage prerequisite is universe level. A host that enumerates one path incorrectly inside a
  selected unit is not caught by it — that is producer truth and future qualification work.
- Only `L0-verbatim` is recomputed through a complete Run; L1–L3 remain retained custody plus
  framing.
- The TypeScript suffix table stays deliberately conservative: it can under-detect across variants
  and never over-detect.
- `selected-owners-disagree` was unmeasurable by neutralisation in the first probe version because
  an arbitrary-pick stub is a coin flip against an already-minted frame; it became measurable only
  incidentally when the derived ids changed the canonical order. The shipped test asserts the exact
  cause with valid positive controls, which is what root's guidance calls sufficient.
- Native and security ran out of tree with regenerated pins; the in-tree pin refresh is yours.

---

**No acceptance, no readiness, and not all gaps closed.** Corrected freeze, then an actual fresh
independent review at zero unresolved MUST/SHOULD, then a new blind, then the complete independent
application review and readiness reconciliation. Your final recheck of the saved vectors on this
source is expected and welcome.
