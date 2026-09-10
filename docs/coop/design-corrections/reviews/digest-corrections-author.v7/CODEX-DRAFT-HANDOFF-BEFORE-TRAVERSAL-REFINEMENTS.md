# HANDOFF — actual Claude coauthor, v7 (v9-S1: the residue rule's unannotated-field limb)

**Standing: not accepted, not qualified, not promoted.** A new freeze, a fresh independent review at
zero unresolved MUST/SHOULD, a NEW fresh blind, and the complete independent application/readiness
reconciliation all remain required. I make no acceptance or readiness claim.

**Read, by byte count and hash, content inspected:**

| File | Bytes | SHA-256 |
|---|---|---|
| `post-reset-review.v9/review.json` | — | `13b4a4719799485139d01596eaceff93854d45d4af6d8fd689c42ff28ac9844e` (matches the stated value) |
| `post-reset-review.v9/review.md`, `probes/p03_residue_enforcement.py`, `probes/p04_third_limb.py` | — | read in full |
| `reviews/codex-post-reset.v1/technical-review.v9.md` | 8102 | read in full |
| `digest-corrections-author.v7/CODEX-PUBLIC-NOTE.md` | **1438** | **`0a06a5c404076b6d1218b017b8306dc771629beb7c1249ece5729f56e517204c`** — absent when I began, read before the checker batch and again immediately before this handoff |

The working tree matched the frozen v9 subject byte for byte for both owned files before I edited
them (`1a563aa1…`, `d07cfe7f…`).

---

## 1. v9-S1 — the finding is correct and the check that carried the name is mine

`relation_annotation_closure` iterated only fields that already carry `x-opensip-digest`, so an
**unannotated** governed field was invisible *by construction*. The reviewer injected one into all
13 selectors × 3 governed forms and **all 39 were admitted**, and reproduced my own check
`every-relation-payload-digest-and-path-field-is-annotated-and-joined` verbatim against a document
carrying an unannotated `CanonicalPath`: it still returned `True`. A test name is not enforcement,
and mine asserted a property it never tested. **I dispute nothing in v9-S1.**

I took remedy **(a)**: implement the missing limb, consume it, and make the check test its claim.
Remedy (b) — demoting the limb to an authoring aspiration — would weaken the guard that keeps the
v8-S2 class closed.

## 2. What changed, in the two files I own

**No contract, schema, registry or document edit.** `relation-payload-schemas.v2.json` is
byte-identical to frozen v9, so `x-opensip-digest-law`, the domain/custody/rung/universe laws, the
`previousPath` `not-joined` exemption and every join row are untouched. The law already declared all
three limbs; the defect was that one had no consumer.

`foundation/identity-model.py`:

- `GOVERNED_RELATION_FORMS = ('DigestHex','Sha256Text','CanonicalPath')` — the document's three
  governed scalar forms.
- `relation_digest_annotation_coverage(document=None) -> {total, annotated, unannotated,
  governedForms, byRelation}` — the relation counterpart of `native_digest_annotation_coverage`.
- `relation_annotation_closure` gains limb 3 **first**, scoped to its own relation's selector, so it
  is consumed in Run closure through `registry_row` on every owning fact — the same place limbs 1
  and 2 already fire, not only in a test.

**Traversal, stated as what I actually support** (root asked for this precisely):

| Aspect | Supported |
|---|---|
| Detection | `$ref` to a governed `$def`, **resolved transitively** through `$defs`, **and** an inline `pattern` equal to a governed form's own |
| Descent | `properties`, `items`, `additionalProperties`, `oneOf`, `anyOf`, `allOf` |
| Coverage | an `x-opensip-digest` **anywhere on the path** to a governed leaf covers it |

That last rule is required by both shipped documents: this one annotates the **parent** property
carrying the `$ref`, while the native bundle annotates the **branch** inside a nullable `oneOf`.

**New cause, in the exact form root's final verification needs:**

```
RELATION_DIGEST_UNANNOTATED:<relation>:<relation>.<fieldPath>:<governedForm>
```

for example `RELATION_DIGEST_UNANNOTATED:file:file.strayGoverned:DigestHex` and
`RELATION_DIGEST_UNANNOTATED:clones:clones.bodyIdentity:Sha256Text`. Nested paths append `.field`
and array/`additionalProperties` descent appends `[]`. Limb order is **unannotated → retention →
residue → join-unknown**, so each of the four causes stays reachable in isolation.

## 3. Evidence that it is enforcement and not decoration

**Neutralisation** (`probes/probe-third-limb-is-load-bearing.v2.py`) — the point of v9-S1 is that a
check can carry a name it does not test, so this does not merely re-run the suite:

| | injections admitted | suite assertion on a stray document |
|---|---|---|
| with enforcement | **0 / 39** | **False** |
| enforcement neutralised | **39 / 39** | **True** |

The pre-v7 assertion *shape* returns `True` on that same document when enforcement is neutralised —
the reviewer's finding reproduced on demand — and now raises under enforcement.

**The reviewer's own probes, re-run against the corrected source** (their construction, only the
`SUB` path adapted; originals untouched in the review directory):

- `p04`: all **39/39** limb-3 injections refuse; limb 2 in isolation still reaches
  `RELATION_JOIN_FIELD_UNKNOWN`; the shipped document is coherent for all 13 relations; the suite
  check now **raises** on a stray document instead of returning `True`.
- `p03`, run unmodified against **frozen v9** and against the corrected source side by side
  (`result-p03-frozen-vs-corrected.v1.json`): two cases flip from **admitted** to refused —
  `UNANNOTATED-digest-field-added` and `clones-bodyIdentity-annotation-removed`.

**One p03 case does not reach its intended cause, and it is byte-identical on both images.**
`join-names-field-selector-lacks` renames an existing join role, which *un-joins* `contentSha256`,
so limb 1 fires first and reports `RELATION_DIGEST_LAW_RESIDUE:file:contentSha256`. The reviewer
documented this themselves in p03's docstring and isolated it correctly in p04 case A, which passes
here. It is a pre-existing probe ordering artifact, **not** a regression from this correction, and
the side-by-side is retained so that is checkable rather than merely claimed.

**In-suite matrix** (`check-identity.py`), each with a positive control:

- all 13 relations × 3 governed forms refuse an unannotated field; **the same injected field is
  admissible once annotated**, for all 39 — so the refusals are caused by the missing annotation and
  by nothing else about injecting a field.
- six traversal shapes each refuse unannotated and pass annotated: `ref`, `inline` (pattern copied
  rather than referenced), `nullable` (`oneOf` with `null`), `aliased` (a `$def` that refs a governed
  `$def`), `nested` (object member) and `array` (`items`).
- removing the shipped annotation from each of the seven governed fields refuses with that field's
  own cause.
- `byteLength` is annotated but refs `UInt64`: the sweep must **not** count it as governed, or the
  totals would drift and the law would appear to cover a field it does not govern. Asserted.

**No identity churn** (`probes/probe-no-identity-churn.v1.py`), measured rather than assumed, as
root asked: across the frozen v9 subject and the corrected tree, for `references`, `file`,
`clones-typescript` and `clones-rust` shapes, every `RunId`, `PlanId`, fact payload digest,
`bodyIdentity` and language-version component is **identical**. Exactly two files differ between the
images, asserted by hashing all nine previously-owned files in both.

## 4. Owned files changed, exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `f60657124060eb0078a9348498dc5f1b73f777ced8f0f99218989076ad5e44b3` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `317159f39d9f9de19872a53d106a2842362458ac2a7fda767068e37eec5fe566` |

Nothing else was written. Verified byte-identical to frozen v9 after this session:
`native-evidence-report.v2.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json` and
`integration-fixtures.py`. Native and security ran in a disposable copy with regenerated pins; **no
in-tree report or pin was regenerated.**

## 5. Development checks

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **627 / 627**, 0 failed (602 at frozen v9; +25) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, 151 / 151 — disposable copy, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same copy |
| `check-integration.py` | **363 / 363**, with the integration builder **unedited** |

## 6. Integration and blind kit

**No builder edit is needed** and I made none: no helper body, signature or dependency changed, and
the 54-declaration set is unchanged. Confirmed by running `check-integration.py` at 363/363 against
the unmodified `integration-fixtures.py`.

**One provenance line will be stale**, as root's note anticipates: `integration-fixtures.py:2` reads
`Source: foundation/check-identity.py SHA256 d07cfe7f…`, which is the frozen v9 hash. The new value
is `317159f39d9f9de19872a53d106a2842362458ac2a7fda767068e37eec5fe566`. Root owns that refresh; I did
not touch it.

**Blind kit unchanged**: no new normative file and no new selector. The new function is reference
implementation of a rule the registered document already states.

## 7. Advisories

v9-A1 through v9-A11 are root's bookkeeping and I make no unsolicited change for them. For the
record and without acting on it: my v6 handoff's 723-byte figure is the **wrapped** expression
`C({'edition': map})`, which is what v9-A1 asks be stated; the bare map is 711. v9-A2 through v9-A5
are limits I disclosed and they stand unchanged. Nullable ownership for a universe carrying no clone
facts still does not authorise a `complete` clone Coverage — that is the v6
`coverage_dialect_prerequisite`, unchanged and re-verified green here.

## 8. Limitations

- **This is a validator-consistency fix.** It closes no currently exploitable payload attack: the
  relation selectors are closed (`additionalProperties: false`) and the shipped document has zero
  unannotated governed fields, so reaching the new cause requires a reviewed design-time edit to a
  registered document. **Every injection in this session is a hypothetical schema edit, not an
  admitted Run attack**, and I claim no runtime security property and no product qualification.
- The sweep decides **law coherence from the schema alone**. It cannot decide snapshot truth, and it
  says nothing about whether an annotation's stated recipe is honoured — that remains the closure's
  source joins.
- Governance of the three forms is by name and pattern. A future governed form must be added to
  `GOVERNED_RELATION_FORMS`; a *new* scalar `$def` with a novel pattern would not be swept until it
  is declared governed. That is the same boundary the native sibling has, stated rather than hidden.
- One of my own probe results was retained with a truthful superseding label:
  `result-third-limb-is-load-bearing.v1-MISLABELLED-FLAG.json` derived a summary flag from the wrong
  state. Its measurements were correct and its conclusion stood; only the derived flag was wrong,
  and it is fixed in v2 rather than quietly overwritten.
- The reviewer's p03 `join-names-field-selector-lacks` case still does not reach
  `RELATION_JOIN_FIELD_UNKNOWN`, identically on frozen v9 and here, for the reason the reviewer
  themselves gave. I did not alter limb ordering to make someone else's probe report differently.

---

**No acceptance, no readiness, no qualification.** New freeze, fresh independent review at zero
unresolved MUST/SHOULD, NEW fresh blind, then the complete independent application/readiness
reconciliation. Root's final source-pinned six commands, the integration provenance refresh and all
records remain root's.
