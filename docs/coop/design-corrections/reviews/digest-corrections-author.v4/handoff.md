# HANDOFF — actual Claude coauthor, v4 (post-reset-review v8: v8-S1, v8-S2)

**Standing: not accepted, not qualified, not promoted.** The v8 headline ACCEPT is not readiness and
I claim nothing from it. v8 retained two unresolved SHOULD findings against a zero-unresolved gate,
root is right to decline promotion, and **a fresh v9 review and a new fresh blind B remain
mandatory**. Nothing below is an acceptance claim, a qualification claim, or a statement that this
work has been independently reviewed.

Frozen v8, every historical report, and every prior source image are unaltered.

---

## 1. Findings closed

### v8-S1 — Plan budget equality was stated in no contract

The reviewer was exactly right: `PLAN_BUDGET_CONFIG_JOIN` was enforced in the reference and **no
sentence in any of the five contracts stated the rule**. This is a *prose* gap in an
advisory-graded join, and the remedy is prose. `identity-and-evidence.md` §3's closure list now
states that the Plan's deterministic `budget` must equal, exactly and by type, the `analysis.budget`
of the committed resolved semantic configuration the same Plan names; that a legitimate override
enters the **resolved semantic configuration first** so neither committed place silently wins; and
that this changes no identity, replay or determinism property, because both values already enter
PlanId — what it fixes is that two conforming implementations would otherwise disagree on
*admission*. The two schema `description`s (`plan.budget`,
`semantic-configuration.analysis.budget`) cross-reference the same rule.

**No new override path was invented and no enforcement changed.** The original blind **G8 finding
was retracted by its own author**, whose own `observed.planBudgetSchema` already showed the closed
`{unit, limit}` object its prose denied; that retraction stands, this is not a re-opening of G8, and
this is **not** a closed-schema fix. The v3 counterevidence check is still in the suite, unchanged.

### v8-S2 — a `file` payload's content claim was joined to nothing

Also exactly right, and closed as a **class**. Three parts, and root's own confirmed counterexample
re-run against the corrected source (§4).

**(a) The relation payload digest boundary, swept.** The closing digest law governed
identity-schemas.v2 and was extended to the native bundle; `relation-payload-schemas.v2.json` was
governed by neither. It now carries its own `x-opensip-digest-law`, and every digest-bearing and
path-bearing field in it is annotated with representation, producing preimage/codec/domain,
retention and owning authority:

| Relation | Fields |
|---|---|
| `file` | `path`, `contentSha256`, `byteLength` |
| `package` | `manifestPath` |
| `vcs-change` | `path`; `previousPath` (`retention: not-joined`, with its reason) |
| `clones` | `bodyIdentity`, `normalisationVersion` |

The law is **consumed, not counted**. `relation_annotation_closure` requires every annotated field
to be reachable from its relation's registry joins or to declare `retention: not-joined`, and every
field a join names to exist in the selector. A newly annotated field with no join refuses the Run
(`RELATION_DIGEST_LAW_RESIDUE`), and a join naming a field the selector lacks refuses
(`RELATION_JOIN_FIELD_UNKNOWN`). Both are asserted with their exact causes.

**(b) A normative per-relation snapshot-join registry, enforced in real Run closure.**
`x-opensip-relation-registry` carries `snapshotJoins`, and `close_run` applies them to **every
owning fact**, after registered-selector validation and **independently of the payload decode
memo**. Owner context is required at the consuming closure — the enclosing fact, the snapshot **that
fact names**, the retained blobs and the bound native context — because a helper holding only a
payload cannot decide snapshot truth. For `file`: the path must be inventoried, `contentSha256` must
equal that row's digest, `byteLength` must equal its length, the bytes must be **retained** under
that digest and re-hash to it, and every anchor of the fact must lie in the file the payload claims.

Interface ownership is explicit and split on purpose: `relation_annotation_closure` is a **pure
module-level function** that decides law coherence from the schema alone and takes the document as a
parameter; `relation_source_joins` and `body_identity_join` live **inside the Run closure** because
only it owns the snapshot and the retained bytes.

**(c) `clones` — the inherited body recipe, reused and not restated.** `normalisationVersion` is the
raw SHA-256 of the exact **retained canonical level-specification bytes**, re-hashed at closure;
`bodyIdentity` is `sha256:` + SHA-256 of the **fully framed domain-separated preimage** of
`fact-identity-policy.v2#/canonicalisationSchema`, with `levelVersion` carried as the **raw 32
digest bytes and never hex text**, and the L0 payload as `u32be raw_byte_len ‖ span` with
tokenisation forbidden. The frame is retained, fetched, re-hashed and **parsed**, and each component
is joined: domain tag to the policy, `levelId` to the payload's own level, `levelVersion` to the
retained specification, `languageId`/`languageVersion` to the fact's own semantic universe through
that universe domain's new `languageVersionBinding`. At **L0** the payload is **recomputed** from
the enclosing fact's own single anchor — a real source join. At **L1–L3** it is a trusted provider
output no host can recompute, so the requirement is exact retained custody plus well-formed stream
framing. **FACT-ID-V1 and `bodyIdentity` are never equated**, by type or by domain.

This is design-reference evidence about custody and framing. **It qualifies no parser, grades no
tokenisation and certifies no normalizer.**

### The reviewer's blocked file Run — resolved under the existing Coverage contract

v8 could not seal a `file` Run because its fixture Coverage for `file@enumerated` was refused by
**RC-1**. That refusal was correct. **RC-1 is untouched and no native rung was invented.** The
fixture was wrong: `enumerated` is not in `RESOLVED_RUNGS`, so its `ResolutionCompletenessV2` must
be `not-applicable` with `unresolvedEdgeCount: 0`, while the separate examined-partition claim
`entry.coverage` may still be `complete`. `coverage_result` now derives that by calling the native
producer's own `completeness_from_stage` instead of asserting a resolution claim — exactly as root's
note predicted — and the file Run seals, replays and commits on that basis.

---

## 2. Owned files changed, with exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `869e45313bdd4ccebb688c0ad8b3783b368b6ab8e93ef047658ad724e8712a1b` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `7507216b4f72bcae3cc8a28c1ea4f8f7d993f9d656ed31c513e8c45d44ee5b8e` |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `a9ca1ec675ef0eab5e1a16d986d6906e94f6583e41800b96402c32a72d264865` |
| `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `a77d359b4b17393e3e6d7aa769ff7aab0b9e6d0416c945e8542ffd6d3a9e1418` |
| `docs/coop/design-corrections/foundation/identity-model.py` | `8d704d59c751ca1b3c2e289d5a973ebe81c0ca768748f8dd906201a7d983d249` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `5da8d125c2afa0da348fd99a98e19b1a5cf24905b3dbb99d7846b4d282bd45ad` |

Nothing else in the tree was written by me. `canonical.py`, all workflow and security files, all
integration files, `public-detail-registry`, pin manifests, generated reports, governance and README
are untouched; root's final v8 custom-entry, repeated-extends and prose changes and every earlier
correction survive, and I re-ran every suite to show it. **One correction to that statement, stated
plainly rather than buried:** running `native/check_native_evidence.v2.py` in-tree **overwrote**
`native/native-evidence-report.v2.json` with a `PIN-MISMATCH` report, because that checker writes
its report before it checks pins. I restored the file byte-identically from the frozen v8 image
(`164b5c2241f5dd9fb61c129778f04f330a9276a1b250a4c4f01ec8e7fd1b2b74`, identical in both frozen
copies) and re-ran native and security in an out-of-tree sandbox instead. Please re-verify that hash
before your capture.

## 3. New normative inputs — blind-kit inclusion

No new normative **file** was created. The registry, the digest law and the join tables live inside
`foundation/relation-payload-schemas.v2.json`, already on the kit list since v3.

The clone body recipe adds a **retained normative dependency** that the kit must carry, named by
exact path and selector in `identity-and-evidence.md` §3 and in the relation registry itself:

```
docs/coop/artifacts/fact-identity-policy.v2.json   #/canonicalisationSchema
                                                   #/normalisationLadder
                                                   #/factRecordIdentityBoundaryV1
```

Per root's note this is already selected in the blind kit and **no foundation-owned successor
extract is wanted**; my default was to cite the pinned inherited artifact and that is what shipped.

New normative machinery inside already-listed documents, which blind B must be able to find:

- `relation-payload-schemas.v2.json#/x-opensip-digest-law` — representations, retention vocabulary
  (including `not-joined`), the enforcement statement and the residue rule.
- `relation-payload-schemas.v2.json#/x-opensip-relation-registry/snapshotJoinLaw` and each
  relation's `snapshotJoins`; `.../relations/clones/bodyIdentityJoin`.
- `identity-schemas.v2.json#/x-opensip-digest-domains/languageVersionBindingLaw` and the
  `languageVersionBinding` on each `native-semantic-universe` domain row.

## 4. Development checks actually run (all green)

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **481 / 481**, 0 failed (was 445 at session start; +36) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, 150 / 150 cases, 60 matrix cells, 0 open objects, 0 uncovered feedback — **run in an out-of-tree sandbox with regenerated pins**, because in-tree it stops at your pins (which you refresh after this handoff) |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same sandbox, same reason |
| `check-integration.py` | 363 / 363, in-tree, unchanged |

Probes, with every executed attempt retained and truthfully labelled, in
`/tmp/opensip-design-corrections/digest-corrections-author.v4/probes/`:

- **`probe-joins-are-load-bearing.v2.py`** — removes the new enforcement and re-runs all eleven
  negatives. Every one closes without it and refuses with its exact cause with it:
  `notLoadBearing: []`. No negative is counted as coverage of a join it does not reach.
- **`probe-joins-are-load-bearing.v1-STALE-MUTATION.py`** — retained, superseded, labelled. It
  carried its own stale copy of a mutation that also moved the fact's anchor, so its two
  `notLoadBearing` rows measured a different graph. Its first execution also ran against a module
  left poisoned by an earlier version of the residue test, which mutated module globals and restored
  them incompletely; that test now asks its question of a deep-copied hypothetical document and
  mutates nothing.
- **`probe-root-counterexample-rerun.v2.py`** — **your** confirmed counterexample construction,
  re-run against the corrected tree. Control closes, replays and **commits**; all three contradictory
  payloads now refuse, with distinct exact causes: `RELATION_FILE_CONTENT_JOIN:a.ts`,
  `RELATION_FILE_LENGTH_JOIN:a.ts`, `RELATION_PATH_NOT_INVENTORIED:file:absent.ts`.
- **`probe-root-counterexample-rerun.v1.py`** — retained, superseded, labelled. Its three refusal
  rows are valid; its control row is not, because your frozen-source construction reset the
  module-level `ATOM` before `build()`, and the current `build()` takes the atom as a parameter, so
  the control's policy stayed references-shaped while its fact became file-shaped and replay
  correctly disagreed. A probe-adaptation defect, not a finding.

The evidence for the fix is **yours**, from
`reviews/codex-post-reset.v1/file-payload-counterexample.v9/attempt2/`, and is not rewritten,
relabelled or absorbed.

## 5. New and changed APIs

`identity-model.py` (module level, pure):

- `parse_body_frame(raw) -> [domainTag, levelId, levelVersion, languageId, languageVersion, payload]`
  — the inherited `domainSeparatedPreimage`; refuses truncation and trailing bytes.
- `parse_token_stream(raw) -> [(kind, value)]` — the inherited `framedTokenStream`; proves custody
  and framing of an L1–L3 payload and judges no tokenisation.
- `relation_annotation_closure(name, document=None)` — the residue/coherence rule; `document` is a
  parameter so a caller can ask about a hypothetical document without mutating the module.

`identity-model.py` (inside `open_run_closure`, owner context required):

- `relation_source_joins(value, row, fact)` — the `snapshotJoins` table over the fact's own snapshot.
- `body_identity_join(value, join, fact)` — the framed body-identity join.
- `relation_payload_rules(value, row, fact)` now calls `relation_source_joins`.

`check-identity.py`: `rule_for(language, atom=None, subject_kind='symbol')`,
`policy_for(language, atom=None, subject_kind='symbol')`,
`build(..., relation='references')`, new `relation_fixture(...)`, `framed_body_preimage(...)`,
`LEVEL_SPECIFICATION`; `FILTER_FIELD_OF` is now **relation-keyed**; `coverage_result` derives
`resolutionCompleteness` from the rung via `N.completeness_from_stage`.

## 6. Copied-builder declaration (integration fixture)

`design-corrections/integration-fixtures.py` copies `ATOM, FILTER_FIELD_OF, POLICY, RULE,
coverage_result, policy_for, rule_for, build` among others. **All eight of those have drifted** and
the copy is now stale, though `check-integration.py` still passes 363/363 because it exercises only
the references path. The refresh you hold needs: relation-keyed `FILTER_FIELD_OF`; rung-derived
`coverage_result`; `rule_for`/`policy_for` atom+subject-kind parameters; `build(relation=...)` with
`relation_fixture`; `framed_body_preimage`; `LEVEL_SPECIFICATION`; and `TS_SOURCES` gaining an
inventoried workspace `package.json` (needed because `node_modules/**` is correctly pruned from the
snapshot, so no package manifest was inventoried before).

## 7. Advisories and dispositions

- **v8-A1 (pin truncation undetectable)** — acknowledged, **not mine to close**; it is a property of
  your pin manifest format, and I changed no pin.
- **v8-A2 (Rust component inventory asymmetry)** — acknowledged, native-owned, untouched.
- **V7-ADV1, per your note** — closed in the digest-law section. The annotation is what closes a
  field; a bare 64-hex string, a `sha256:` prefix and a typed `plan2:`-style prefix are *spellings*
  and never imply an annotation. I explicitly do **not** claim every prefixed identity carries the
  same annotation. `plan.nativeContextDigests` is stated as a **set that may hold several contexts
  of one language**, with the fact's `sourceUniverse` selecting the corresponding context through
  the universe record's own `nativeContextId` — verified against the enforcement at
  `identity-model.py` `UNIVERSE_CONTEXT_NOT_SELECTED` — and no arbitrary scalar display anywhere.
- **Your VCS request** — honoured and exercised positively, not just declared: `deleted` is exempt
  from the path join, `previousPath` is `retention: not-joined` as a **historical observation**
  distinct from a current source claim, and both a deleted-path Run and a renamed-path Run close.
- **Workflow §8/§12 clarifications** — yours; I did not overlap.

## 8. Limitations, stated plainly

- `LEVEL_SPECIFICATION` in the fixture is a **stand-in** for the retained canonical level
  specification. Its *content* is FACT-IDENTITY's to write; what this bundle demonstrates is that the
  bytes are retained and that `normalisationVersion` is their raw SHA-256 rather than a label or an
  opaque caller hash.
- Only `L0-verbatim` is exercised through a complete Run. L1–L3 are enforced as **custody plus
  framing** (retained frame, parsed token stream) and are deliberately not recomputed; no normalizer
  is qualified and no tokenisation is graded.
- **Rust `languageVersionBinding` is `edition` alone**, because `RustUniverseV2ResolvedInputs`
  carries no rustc toolchain identity. The tokenisation rules are pinned by the level specification,
  so this is coherent, but if a later decision wants toolchain identity inside the body frame it is a
  native `ResolvedInputs` change and therefore a universe-identity change. Flagged, not silently
  absorbed.
- The `file` anchor rule (`anchorPathField`) requires every anchor of a `file` fact to be in the
  claimed file. That is what refuses the borrowed-anchor second owner; if a future relation needs a
  file fact anchored elsewhere, it needs a different join row, not an exception.
- The native and security suites were run in an out-of-tree sandbox with regenerated pins; the pin
  refresh in-tree is yours.
- All of this is design/reference evidence over synthetic fixtures. No compiler, Cargo, OS or
  repository code was executed; no platform, parser, normalizer or product behaviour is qualified.

---

**Fresh v9 review and a new fresh blind B remain mandatory. I make no acceptance, readiness or
qualification claim.** Your source capture should precede your integration changes, as agreed.
