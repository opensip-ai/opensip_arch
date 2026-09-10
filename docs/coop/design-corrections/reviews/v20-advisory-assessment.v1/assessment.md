# v20 advisory assessment — BLIND8 CB-ADV-1 and CB-ADV-2

Subject: frozen `candidate-subject.v19` (manifest SHA256 `312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b`).
Bounded to the two named laws. Probes ran against a copy of the subject at `probe-tree/`
(`reviews/` excluded) using a truncated fixture harness (`_probe_fixtures.py` = the first 1020
lines of `check-identity.py`, its constructors only — no suite execution, no report writing). The
frozen tree was read, never imported from and never written to. Sources and raw results are in
`probes/`.

---

## CB-ADV-1 — `view.schemaDigests`

**Disposition: PARTIALLY CONFIRMED. The union theory is refused; a different, real defect is
demonstrated. Severity: moderate (published law unenforced, with observed in-tree drift).**

### What the accepted closure actually enforces

`schemaDigests` appears **zero** times in `identity-model.py`. The field is admitted only by the
generic annotation dispatch: `identity-model.py:652`, `if representation=='raw-artifact':blob(value)`.
The entire enforced law is *retention* — the bytes must be present and re-hash to the digest.
Probes (`probes/p1_view_schema_digests.py`, run against the pristine model):

| probe | result |
|---|---|
| P1-b `schemaDigests: []` | **admits** |
| P1-c2 drop the document a member Coverage was actually admitted under | **admits** |
| P1-d add a registered document the view admitted nothing under | **admits** |
| P1-e / P1-g arbitrary retained blob as a member | **admits** |
| P1-f unretained digest | refuses `EVIDENCE_UNAVAILABLE` |

So: **not** a required union, **not** restricted to registered documents, only retained.

### Selected, not derived — and no floor is required

The set is a deliberate producer declaration, and the shipped reference producer proves it: with
`build(has_match=False)` the view carries **no relation facts** yet still names
`foundation/relation-payload-schemas.v2.json` alongside the native document. The committed set is
a strict superset of the mechanical union (`viewSetEqualsMechanicalUnion: false`). Two different
consumers selecting different sets from the same repository is therefore expected behaviour of the
contract as written, not evidence of divergent semantic inputs.

No floor is required either, and I do **not** propose one. Every fact and Coverage pins and
retains its own schema document independently through its own `payloadSchemaDigest`:
`registered_payload` (`identity-model.py:735`) resolves the closed registry row, requires
`sha256(document bytes) == payloadSchemaDigest` exactly (`PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`),
retains it via `blob(schema_digest)`, and validates by the row selector. Payload admission is
decided there. A document omitted from `view.schemaDigests` is still pinned; one added there
admits nothing. An automatic maximal union would be speculative redesign, and the existing contract
does not require it.

### The real defect

`identity-and-evidence.md:568` publishes: "`view.schemaDigests` names the registered documents a
view admitted, and each member must be one of them." The item annotation
(`identity-schemas.v2.json:733`) says "the exact complete **registered** schema document bytes".
**Nothing enforces registration**, and the drift is not hypothetical: the live tree already
contains a committed `view` record whose member matches no file in the tree at all —
`native/native-cases.v2.json` → `fixtures.coverageView.schemaDigests[0]` =
`5665e5dd92cd022040142a63d8e183cc258f678baf8f0674f8da9ebe0302a7a4`, exhaustively confirmed absent.
It reaches the native `coverage_view_use` boundary, which does not read `schemaDigests` at all, so
nothing catches it.

The identical published word appears at a second site: `x-opensip-digest-domains.schema`
(`identity-schemas.v2.json:2887-2890`), `raw-artifact`, "the exact complete registered schema
document bytes", reachable as a `ProofInputRef` domain. Probe P4-b: an arbitrary retained blob is
admitted as a `schema` evaluation input of a Run. Same defect, same fix.

### Proposed correction (executable, verified)

Annotation-driven, matching the contract's own stated discipline ("dispatches on the
`x-opensip-digest` annotation of the field it is walking, never on that field's name"). Exact
diffs: `probes/cb-adv-1.identity-model.diff` (+24/-1) and `probes/cb-adv-1.identity-schemas.diff`
(+4/-2). A new `artifactClass: "registered-schema-document"` on both annotations; one cached
helper `registered_schema_documents()` derived from the single `x-opensip-payload-registry` (no
second list to drift); one branch in `digest_field` raising
`SCHEMA_DOCUMENT_UNREGISTERED:<digest>`. Neither name collides in the subject (0 files each).

**Proposed prose, replacing `identity-and-evidence.md:568-569`:**

> `view.schemaDigests` is the producer's own **declaration** of the schema documents its view was
> produced under. Each member is the raw SHA-256 of the exact full bytes of a document on the
> closed registry above; a member naming anything else refuses (`SCHEMA_DOCUMENT_UNREGISTERED`).
> The set is **selected, not derived**: it is neither required to name every document a member fact
> or Coverage was admitted under, nor forbidden from naming a registered document this view
> admitted nothing under. It carries no admission authority of its own — every fact and Coverage
> pins its own document through its own `payloadSchemaDigest`, whose exact bytes are re-hashed and
> retained on every reference, so a document omitted here is still pinned there and a document
> added here admits nothing. The same rule holds wherever the `registered-schema-document` artifact
> class appears, including the `schema` proof-input-ref domain.

The field annotation text is in the diff. **What an implementer must know:** (1) choose the set —
it is a declaration, with no derivation and no completeness obligation; (2) every member must be a
current registry document, exact full bytes, retained; (3) it grants nothing — never rely on it to
establish what a view admitted, and never treat omission as absence.

### Compatibility and limits

Refusal-widening only; identity is over the record, so no RunId changes. Verified: the
`p3_correction_compatibility.py` matrix (7 build variants + 2 import graphs) is **byte-identical**
across pristine and corrected trees. `check-foundation.py` 231/231 and `check-array-orders.py`
65/65 pass under the correction in the sandbox. Two matrix cells (`pure-syntax`,
`unresolved-edges`) error identically in both trees from my own harness-kwarg misuse, not model
faults; they carry no evidence either way. Mechanics: `source-pins.v1.json` rows for
`identity-model.py` and `identity-schemas.v2.json` must be re-pinned, and the
`native-cases.v2.json` `coverageView` fixture must be re-pinned to a registry document or it will
refuse if ever routed through a Run closure.

---

## CB-ADV-2 — `semantic-evidence.importIds` vs `plan.importIds`

**Disposition: CONFIRMED as the root states — a missing prose/annotation of an EXISTING enforcement
law. Severity: low (documentation). No model change required or proposed.**

The root's reading is exactly correct. `identity-model.py:1290`:
`if evidence['importIds']!=plan['importIds']:raise C.AdmissionError('IMPORT_JOIN')`. Both arrays
are `uniqueItems` with `x-opensip-order: canonical-set`, enforced by `ordered()`
(`ORDER_OR_DUPLICATE`), so list equality *is* canonical-set equality. Probes
(`probes/p2_import_join.py`, `probes/p2g_finding_import_authority.py`), each asserting its exact
refusal token:

- P2-b evidence omits a selected import → `IMPORT_JOIN`
- P2-c Plan omits an import the evidence names → `IMPORT_JOIN`
- P2-d selected but **not** evaluated → **admits** (lawful)
- P2-e the same graph with that import withheld → `EVIDENCE_UNAVAILABLE` (retention is real)
- P2-f evaluated but unselected → `UNSELECTED_EVALUATION_IMPORT` (`identity-model.py:1428`)
- P2-g1 finding cites an **evaluated** selected import → admits
- P2-g2 finding cites a **selected but unevaluated** import → `HIDDEN_FINDING_EVIDENCE`
  (`finding_evidence_roots['import']` is keyed on `evaluated_imports`, `identity-model.py:1432`)

Existing meaningful controls, all distinct and all already enforced: the equality join (1290); the
evaluated ⊆ selected join (1428); finding-citation restriction to the evaluated subset (1432-1439);
retention of **every** evidence import (1591) and per-selected-import source-correspondence
admission (1564-1589); `IMPORT_OPERATION_JOIN` (1304) requiring `read-import` in the grant; and
`CACHE_INPUT_IMPORT_NOT_SELECTED` (1664). There is no gap and no synthetic join to add — a Run is
already a complete admitted record, not a join of parts.

The published corpus states evaluated ⊆ selected (`identity-and-evidence.md:191-197`, "Every
evaluated import must belong to Plan even when no finding cites it") but the equality is stated
nowhere. The owning paragraph is `identity-and-evidence.md:505-506`, which enumerates precisely
these root equalities and stops at coverage.

**Proposed prose, appended at `identity-and-evidence.md:506`:**

> `semantic-evidence.importIds` repeats the Plan-selected import set **exactly**: the two are equal
> as canonical sets and any difference in either direction refuses (`IMPORT_JOIN`). It is a
> repetition of the Plan's selection, never a second selection — evidence can neither drop a
> selected import from the record nor add one the Plan did not select.
> `proof-bundle.evaluationInputRefs` separately names the subset actually **evaluated**, which must
> be a subset of the selected set (`UNSELECTED_EVALUATION_IMPORT`) and never grants authority to an
> unselected import. Selection is retention, not use: a selected import is resolved and admitted by
> the Run closure even when nothing evaluated it, and selection alone lets no finding cite it —
> import citations are restricted to the evaluated subset (`HIDDEN_FINDING_EVIDENCE`). A selected
> but non-evaluated import contributes no fact to any view.

**Proposed field annotation** for `identity-schemas.v2.json#/$defs/semantic-evidence/properties/importIds`
(currently undescribed), added as a sibling `description` — non-normative text only, no shape
change, no digest consequence for any payload document:

> "Exactly the Plan-selected import set of this Run's Plan, repeated: equal as a canonical set to
> `plan.importIds` (`IMPORT_JOIN`). A repetition of the selection, never a second selection. The
> evaluated SUBSET is named separately by `proof-bundle.evaluationInputRefs`; a selected import that
> nothing evaluated is still resolved and retained by the Run closure, and being selected alone
> grants it no evidence authority."

This erases nothing: non-evaluated selected imports remain retained (P2-e), and nothing implicitly
adds imported facts to a view.

---

## Assent and limits

`technicalAssent` is given to the **specified wording and semantics proposed above** and, for
CB-ADV-1, to the executable correction exactly as diffed and verified — nothing else. It is not
assent to source20, to any independent acceptance, or to a readiness position. Boundaries: this is
a bounded two-law review; the six broad suites were not rerun. Scope-parameter cardinality,
request-tuple uniqueness and coverage exhaustiveness belong to the source coauthor; stage operation
vocabulary and Plan semantic-closure membership belong to the other assessor; neither was examined
here. The `probe-tree` correction is a sandbox demonstration only — nothing in the frozen or live
tree was modified.
