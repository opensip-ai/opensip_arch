# bv4-corrections-author.v1 — handoff

**Standing.** A bounded design/schema/reference correction pass by actual Claude
against the frozen accepted v13 subject
(`8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023`, 4379 files),
answering the completed actual-Claude blind Bv4 review and root's recorded
dispositions. It is **not** product implementation, not a commit/push/publication,
not readiness promotion, and not product or platform qualification. It confers no
acceptance. Codex must read and assess this source and its discriminating tests
before integration; nothing here is alignment merely because it was requested.

`sourceRoot = /tmp/opensip-design-corrections/bv4-corrections-author.v1/work`

**Blind verdict preserved exactly.** `CHANGES_REQUIRED`, 2 MUST / 2 SHOULD / 4
advisory, the same eight ids as the interim capture, and root's account that the
totals are **126 vectors plus 8 gap records, not 126 passing tests**, with 9 of 11
law claims holding. The severities below are the blind's own and are unchanged.

---

## What the first pass found that the finding text did not

Before any edit, the two MUST findings were reproduced against the **frozen v13
bytes** through full `close_run` admission. Both were real, and both were
different from what the finding described.

**M1.** Root is right that v13 **admits** the whole-file-anchored `file` fact for
`tool/main.py`, `LICENSE`, `README.md` and `src/plain.rs` — the model's inventory
exemption precedes the grammar check at both call sites, and the blind's `REFUSE`
is its own literal reconstruction of contradictory wording, not an observed model
rejection. Nothing here claims otherwise. But the probe that establishes that also
establishes something the blind's implementation hid from it: **both spellings
admit**, with different `fact2` identities —

```
file@enumerated tool/main.py  anchored  -> fact2:5cce76d9…  ADMIT
file@enumerated tool/main.py  unanchored-> fact2:d7bb2235…  ADMIT
```

— on every path including supported ones, and the same for `vcs-change`. Three
further live gaps fell out of the same session: an unanchored `declares` /
`references` / `types` fact **closed a Run** under a TypeScript or Rust universe
(the "an unanchored code fact is not vacuously supported" rule lived only inside
the syntax-universe guard); a `package` fact claiming `package.json` **closed a
Run** while anchored into an unrelated `a.ts` (`anchorPathField` existed only on
the `file` row); and a `file@enumerated` Coverage claimed `complete` over the
inventoried subject `a.ts` with **zero facts**, making `exists file where
path=a.ts` authoritatively false over a complete result.

**M2.** The schema refusal the blind reported is real — `computed-member-access`,
`exports-open` and `compiler-inferred` are each refused as a `nativeCause`. The
larger half is that **nothing compared the pair to anything**. On frozen v13 all
of these closed a Run: `resolution-incomplete` carrying the unrelated but
schema-valid `lockfile-missing`; the same relabelled `capability-missing`;
`resolution-incomplete` over a **complete** resolution;
`external-consumers-unknown` over `exportsClosed: closed`;
`derivation-policy-unmet` over an empty `derivationKinds`;
`input-closure-incomplete` with a null cause; `budget-exhausted` with no budget
stage terminal; and a cause with no deficiency at all.

Neither blind remedy is sufficient, and both were assessed rather than accepted.

---

## The selected laws

### M1 — anchor law, published boundary, and inventory totality

Three corrections, because the finding contains three separable defects.

1. **A closed per-relation `anchorLaw`** in the relation registry, no default row,
   three classes: `source-text` (the nine code relations) **≥ 1**;
   `body-identity` (`clones`) **= 1**; `inventory` (`file`, `package`,
   `vcs-change`) **= 0**. Enforced once, in `relation_payload_rules`, before the
   snapshot joins and before the syntax guard, at the producer boundary and again
   at retained Run closure.

   Zero for the inventory class because such a fact is **not read from a source
   span**: its whole semantic input is its payload, which the relation's own
   `snapshotJoins` already bind (path in the inventory; for `file` also the
   content digest, the byte length and *custody* of the retained bytes). An anchor
   restates part of an already-joined claim on an axis nothing derives. Zero is
   also the only cardinality *every* inventoried path can satisfy — unsupported
   suffix, extensionless, data-document, and decisively a `vcs-change` on a
   `deleted` path that the registry itself places outside the snapshot and that
   can bear no anchor at all. Cardinality 1 would make that case unrepresentable
   and would newly require every package manifest's bytes to be retained.

   The `source-text` class deliberately has **no** upper bound and no canonical
   extent, and the registry says so: which spans a producer cites is a real
   statement about what it read, so differing citations are *different semantic
   descriptors* that legitimately mint different identities. **No cross-provider
   anchor identity is promised for code facts** — root's explicit caution, honoured
   in the normative text and in a control.

2. **Published boundary (2) now carries the inventory exemption**, alongside
   boundary (3), with the reason: the exemption belongs to the *relation*, not to
   the boundary, because an inventory fact is not read by a grammar at all. The
   two laws are independent and agree — an inventory fact also names no anchor
   path for boundary (2) to test — and the exemption is from **grammar ownership
   only**: snapshot joins, own-scope attribution and the anchor law all still
   bind, and no code fact becomes admissible because some other anchor in the Run
   sits on a supported path.

3. **`coverageTotality`**, a new registry row on `file` **only**: a `complete`
   `file@enumerated` Coverage must carry an admitted fact for every subject the
   snapshot inventory contains, derived at Run closure from the retained view's
   own facts and the retained inventory. A subject the snapshot does *not* contain
   is owed nothing — that is the one case a universal negative over inventory
   exists to serve — and an `unknown` result with its disclosed deficiency is owed
   nothing either. `package` and `vcs-change` are not total and get no row.

### M2 — a closed cause-carrier registry, and no new enum members

`x-opensip-deficiency-cause-registry` covers **every** `DeficiencyV2` member with
no default row, naming which retained field carries each cause and what that field
must say. **No enum changes anywhere** — not `NativeCause`, not `DeficiencyV2`,
not `UnresolvedEdgeKindV1`, not the public `DomainDetailCode` registry, no D9
class, code or exit. Every carrier already existed and was already closed.

New members were rejected **on the merits**: `resolution-incomplete` has a
genuinely set-valued cause — up to all sixteen `UnresolvedEdgeKindV1` classes at
once — so a scalar could only lose information or force an arbitrary pick, which
is the multi-cause defect itself. The three named rows get their real carriers:

| deficiency | carrier | `nativeCause` |
|---|---|---|
| `resolution-incomplete` | `resolutionCompleteness` — `state` ∈ {incomplete, partial, not-attempted}; `unresolvedEdgeClasses` holds **all** classes at once | `null` |
| `external-consumers-unknown` | `closedWorld.exportsClosed` ∈ {open, unknown} | `null` |
| `derivation-policy-unmet` | `derivationKinds` contains `compiler-inferred` | `null` |

Those nulls are no longer an escape: admission refuses unless the named field
actually carries the cause. The other rows are named too — `input-closure-incomplete`
**requires** one of the twelve, `language-tier-unsupported` requires exactly
`capability-missing`, `budget-exhausted` requires its stage terminal, and
`confidence-floor-unmet` / `required-relation-missing` are requirement-relative
with **no** entry carrier, stated as a limit rather than given an invented
predicate.

**Multi-cause and precedence.** An entry carries one deficiency and *every*
carrier simultaneously; the carriers are structurally independent, so the scalar
loses nothing. Which member is declared when several apply is the published §10
precedence, applied by the sufficiency evaluation against a **Requirement**.

**What was deliberately not done.** The law is one-directional: a *declared*
deficiency must be *supported* by the entry's own committed evidence. It does not
derive an obligation to declare one, because RC-3 makes `coverage: complete` with
`state: incomplete` and no deficiency a valid honest entry — the v13 corpus
fixture `coverageIncompletePayload` is exactly that — and because
external-consumer state and the confidence floor are requirement-relative. The
registry publishes that limit instead of papering over it.

**Retained vs public routes** are stated separately and both named: the entry
lives in the committed `coverage2` record; the *deficiency* is already a public
`DomainDetailCode` for all three rows, and the *cause* travels as typed detail in
the `coverage2` record the termination names by `coverageId`. No public code added.

### S1 — `languageIdSource` names the body selector

The registry key now names the same selector over the same single anchor that
identity §3 and each domain row's `bodyLanguageLaw` always named:
`bodyLanguageByVariant[<variant the dialect suffix table selects, longest match>]`
for a `closed-suffix-table` dialect, `bodyLanguage` otherwise. A second key
records the refuted engine reading, so it cannot be re-derived from silence.
Verified by **full Runs**, not assertions: a compiler-free clones Run over a `.rs`
body under the syntax universe closes with frame `languageId: rust`, and a
TS-hosted `.js` clones Run closes with `javascript`. The grammar parse and the
compiler parse of one language still mint different identities.

### S2 — the capability vocabulary authority

A fourth signal settled the choice the blind left open:
`product-configuration.analysis.capabilities` already constrains its items to
`^[a-z][a-z0-9._:-]*$`, which contains **no `@`** — so `relation@rung` was never
admissible at the configuration layer. The authority is therefore
`native-capability-matrix.v2.json#/capabilities[].id`, published with its exact
selector, its law at `#/capabilityIdLaw`, and the analysis-spec schema annotated
to point at it.

A capability id and a `relation@rung` are declared **different concepts** and are
not equated — one is a requestable unit of work covering several relations
(`inventory` covers three) or none (`clones-near`, `clones-cross-tsjs`), the other
is a fact/Coverage coordinate — with `capabilities[].relations` as the published
bridge both ways. Mode applicability is closed: the cell must exist and must not
be `NOT-SELECTED` ("no promise", unsatisfiable), while an `UNSUPPORTED-TYPED` cell
stays requestable and is **disclosed**, never refused. The release declaration
registry keeps release-specific *content* as an authenticated input, but its
schema (`ReleaseCapabilityRegistryV1`), membership authority, canonical spelling
and Plan binding are normative. It is closed at **admission** — over the retained
`analysis-spec` at Run closure — not only in the default helper.

### Advisories

- **ADV-1** — the prose carries **no** cell count at all; it states the cells array
  *is* the complete product, and the checker enforces that in both directions
  (missing, extra, duplicate, `len == product`) plus a vocabulary drift check. A
  maintained invariant, not a second counter that would go stale again. Root's
  `validation-summary.v1.json` stale 60 is **not** touched.
- **ADV-2** — both prose enumerations now name all three universe and all three
  context domains, and identity §3 records that the machine registry always
  carried three.
- **ADV-3** — the effect→token table is published in native §5.2 and mirrored in
  security S10, with three scope facts that must not be dropped: the values are
  **per execution mode** (in v9's `in-host-process` mode every token including
  `PT-ENV-READ` is `DISCLOSURE-ONLY`); `PT-FS-WRITE-HOST-STATE` names the **host's
  own state store** and confers no repository filesystem authority, its
  `DISCLOSURE-ONLY` value saying precisely that the code holds ambient user
  authority throughout; and `PT-HOST-EFFECT-BROKERED`, the one
  `ENFORCED-AT-HOST-BROKER` token, is deliberately projected by no effect name.
  Controls read the **pinned v9 table**, not the prose.
- **ADV-4** — the key stays the document digest and the ambiguity refusal stays.
  Only the accounting is added, including why re-keying by `(document, selector)`
  is deliberately *not* done, and a real Plan-admission control shows the
  forbidden future case refusing rather than choosing.

---

## Evidence

Every case below is a full retained Run through `close_run`.

**M1 (17 cases, `logs/p3-before.json` / `p3-after.json`)** — the two spellings of
one inventory claim now collapse to one (`A` refuses, `B` admits); the borrowed
anchor refuses for `file`, `package` **and** `vcs-change`; unanchored code facts
refuse under TypeScript *and* Rust; a code fact anchored at both a supported and
an unsupported path still refuses; `LICENSE`, `docs/extra.md` and `tool/main.py`
inventory facts all close a Run; and the complete-empty `file` Coverage now
refuses.

**M2 (17 cases, `logs/p4-before.json` / `p4-after.json`)** — every deliberately
wrong pair moved ADMIT → REFUSE; the honest RC entry, the open-exports entry, the
`compiler-inferred` entry and the budget entry all still ADMIT; the three §10
causes remain unrepresentable as `nativeCause`, which is the finding, now answered
by naming carriers.

**S1/S2 (`logs/p5-before.json` / `p5-after.json`)** — the engine reading is shown
unrepresentable under the syntax universe and wrong for `.js` under TypeScript,
against the derived values and the actual Run frames; the three wrong capability
spellings moved ADMIT → REFUSE while both matrix ids still ADMIT.

**Full suite on the released bytes**, run in a separate disposable copy with an
explicit measured temporary repin (log retained; 23 manifest entries over exactly
the 13 changed files) — **these repinned bytes are a development instrument and
are not accepted pin evidence**. The two copies were diffed afterwards and differ
in exactly three files: the two repinned manifests, and
`native-evidence-report.v2.json`, which the native checker regenerated *inside the
disposable copy* while the released copy keeps the frozen v13 bytes. No source,
schema, model, corpus or contract byte differs, so the result below is a result
about the released bytes:

| script | exit | result |
|---|---|---|
| `foundation/check-foundation.py` | 0 | 231/231 |
| `foundation/check-identity.py` | 0 | **1133 passed, 0 failed** (977 on v13; +156) |
| `foundation/check-product-quality.py` | 0 | 24/24 |
| `foundation/check-product-configuration.py` | 0 | 28/28 |
| `foundation/check-array-orders.py` | 0 | 65/65 |
| `workflows/check_workflows.v1.py` | 0 | 1598/1598 |
| `native/check_native_evidence.v2.py` | 0 | 346/346 cases; 66 cells; 0 open objects |

---

## Diff account against frozen v13

**13 files changed, 0 added, 0 deleted** (4379 → 4379). Exact
`beforeSha256`/`afterSha256` for each are in `handoff.json`; the pre-edit bytes are
in `before-images/`.

```
docs/coop/design-corrections/foundation/check-identity.py
docs/coop/design-corrections/foundation/identity-model.py
docs/coop/design-corrections/foundation/identity-schemas.v2.json
docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json
docs/coop/design-corrections/native/check_native_evidence.v2.py
docs/coop/design-corrections/native/native-capability-matrix.v2.json
docs/coop/design-corrections/native/native-cases.v2.json
docs/coop/design-corrections/native/native-evidence.schemas.v2.json
docs/coop/design-corrections/native/native_evidence_model.v2.py
docs/v2/contracts/product-v1/admission-and-qualification.md
docs/v2/contracts/product-v1/identity-and-evidence.md
docs/v2/contracts/product-v1/native-evidence.md
docs/v2/contracts/product-v1/security-and-lifecycle.md
```

No source-pin manifest, generated report, validation/provenance summary,
review/crosswalk/readiness/application record, historical artifact or security
reference model is changed. `security-and-lifecycle.md` is touched only for the
ADV-3 effect mapping clarification, the single use the launch prompt permits.
Pins in the released copy are intentionally stale.

---

## Failed development attempts, retained

Nine are recorded in full in `handoff.json`. The three that mattered:

- The first M2 enforcement pass **broke every unknown-Coverage fixture**, because
  it had found a real defect in the reference fixture: `coverage_result` emitted
  `resolution-incomplete` for every unknown entry regardless of rung, including
  rungs whose RC state RC-1 forces to `not-applicable` — an entry contradicting
  its own record, unnoticed because nothing had ever compared the pair.
- The first multi-class control **asserted** three unresolved classes with zero
  admitted edge facts; RC-2 correctly refused it. The fixture was rebuilt to
  construct real `unresolved-edge` facts with their own scope and Coverage, so the
  classes are committed evidence rather than a claim.
- An early native check run against the released copy while its pins were stale
  **dirtied a generated report**, because `check_native_evidence` writes its
  `PIN-MISMATCH` report to the in-tree path regardless of `--report`. Restored
  byte-exact from the frozen snapshot and confirmed by the diff account; every
  later native run was confined to a disposable repinned copy. Root should know
  about that write path.

## Honest limits

- No product exists to measure and none was assumed. Every compiler, cargo,
  grammar bundle, provider enumeration, VCS observation and permission value is a
  **synthetic trusted input**, never native or platform enforcement proof.
- `SYNTAX_CAPABILITY_CAUSE_MISMATCH` is no longer reachable by an internally
  coherent entry, because the cause registry closes `language-tier-unsupported` to
  exactly `capability-missing`, so no coherent wrong cause exists there. The
  scope-derivation guard is still reachable and still exercised through
  `SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH` with a coherent wrong deficiency. This
  is a strengthening; it is recorded rather than hidden.
- The p5 S2 probe cannot discriminate the `UNSUPPORTED-TYPED` cell case (changing
  the mode also changes which universe the Plan requested, so both trees refuse
  with `UNIVERSE_LANGUAGE_NOT_REQUESTED`); the direct control is the instrument
  for that branch. The `NOT-SELECTED` case *is* discriminating.
- The `file@enumerated` totality law binds the **claim**, not the observation.

## Next, and whose

Codex owns: assessment of this source and its tests; the two substantive choices
stated explicitly (inventory cardinality **zero** over a canonical whole-file
anchor, which cannot represent a deleted `vcs-change`; **named carriers** over new
`NativeCause` members, because a scalar cannot hold a set-valued cause); reference
fixture integration; recording edits **before** final pins; the commands; the pin
seal and freeze. Then a fresh independent review, a **new** blind reconstruction
and a complete application review. Any implementer or future blind kit needs
`native-capability-matrix.v2.json#/capabilityIdLaw` and
`native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityRegistryV1` to be
reachable — both sit inside documents already in the 45-file kit, so no new file
is required, but the release declaration registry was named by two contracts and
supplied by none, and that should be confirmed.

No readiness promotion and no product qualification here.
