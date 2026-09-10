# bv4-corrections-author.v2 — handoff

Focused second pass answering the seven CX-BV4 items and the four precision
points in this session's `CODEX-PUBLIC-NOTE.md`. **Not** independent acceptance,
**not** blind acceptance, **not** final-source assent, **not** product or platform
qualification, **not** readiness. No source integrated, no successor frozen.

`sourceRoot = /tmp/opensip-design-corrections/bv4-corrections-author.v2/work`
v1 is untouched — its `identity-model.py` still hashes `1f48f0b65c04e9e2…`, the
exact SHA root's diagnostics cite.

A pre-edit `assessment.md` / `assessment.json` answering all seven items was
written **before** any edit. I agreed with all seven; none was contested.

---

## Input consumption — the correction, additively

Root's record is right and I do not contest it. `CODEX-PUBLIC-NOTE.md` was read in
full **once**, at 11:09:04.258, before the first edit batch. At 12:30:05 I ran
`shasum` on it and treated an unchanged hash as evidence that re-reading was
unnecessary. It was not: the note had been **extended**, and the six later
sections are exactly the feedback missing from v1.

v1's `inputsReadInFull` says the note was "read in full before the first edit
batch **and again before handoff**". The first clause is true; the second is not —
what happened before handoff was a hash comparison, and **hashing is not reading**.
The correction is additive: v1's bytes stay as they are, because rewriting its
claim would be a worse offence than the original error.

This turn every supplied input was read in full before any edit — the complete
60-line note, `codex-assessment.json`, and all three diagnostic trees including
both retained failed attempts. The `CODEX-PUBLIC-NOTE.md` that appeared mid-pass
was **read**, not hashed, and its four points were acted on before the final suite.

Also corrected: v1's "every other script unchanged" describes *results*. The
13-file aggregate delta governs and it includes `check_native_evidence.v2.py`.

---

## The seven items, by source and result

**1 · TOTALITY — corrected.** Reproduced first: `probes/p1_totality.py` on the v1
bytes returned root's attempt-3 run ids exactly — `3f32e8c1…` ADMIT, `92e44a44…`
ADMIT (the counterexample), `0d63a184…` ADMIT (the valid control). The helper
filtered relation and rung where `CoverageKeyV2` has five coordinates, and the
view-level fact/scope join is **existential**, so a TypeScript fact lawfully sat
beside a syntax scope and paid its obligation. The filter now reads `matchOn`
from the registry — `[snapshotId, relation, resolution, sourceUniverse,
targetUniverse]` — with `matchLaw` in the registry and the reason in native §1.2
and identity §6. After: the counterexample **REFUSES**, both valid controls still
ADMIT. Four full-Run regressions retained. `snapshotId` is already forced
transitively (control: `REFERENCE_SOURCE_JOIN`) and is listed anyway, because this
law reads one scope's obligation out of a *shared* view. Root's attempts 1 and 2
are recorded as harness error and proper unrelated refusal — not defects.

**2 · DERIVATION — corrected.** Reproduced first: `references` ADMIT *and*
`declares` ADMIT on the v1 bytes. §4.7 / `sufficiency_v2` gate `derivationPolicy`
on `rel == "types"`. The registry row gains `relations: ["types"]` and a generic
relation condition in `deficiency_cause_faults`. **My v1 positive was the
counterexample**: it used `references`, so it moved to `types` and `references`
became the discriminating negative. The requirement boundary is preserved and
tested — `compiler-inferred` under `derivationPolicy=any` stays valid, RC-3 stays
lawful, and one control calls `sufficiency_v2` directly to show `declared-only`
yields the deficiency while `any` is satisfied.

**3 · DEFAULT — corrected.** My v1 sentence granted an unqualified *subset*
permission; written about membership, it read as permission about scope, and the
default was driven **from** the registry. New `required_default_capabilities(mode)`
derives the obligation from the **matrix** — every cell not `NOT-SELECTED`, with
`UNSUPPORTED-TYPED` included deliberately so it is disclosed rather than omitted.
The registry now states *availability*, never scope. For the corpus units the
default is 21 rows whatever the release declares; the new staged-subset case
discloses 17 absences. Availability is not qualification; explicit configuration
overrides the *request* with its own provenance; the host input boundary is stated
honestly. No preview exception.

**4 · PUBLIC-ROUTE — corrected.** The public detail registry's own `aliasRule`
already governs this and has three precedents, so the fix **reuses** it and adds
no public code: a new `x-opensip-public-route-registry` routes all 14 internal
keys to codes already in the closed set, and native §10 carries the rows.
`public-detail-registry.v1.json#/internalAliases` is a **records** artifact and is
deliberately not edited — the exact pairs are published so root's edit is
mechanical, and a control asserts it was not performed here. `UNSUPPORTED-TYPED`
stays a disclosed answer, demonstrated by a compiler-free `references`/`syntax-only`
full Run matching root's `run2:e3947278…`. v1's p5 limitation stays recorded
unchanged, and root's three sibling relation rows are not cited as bijection
evidence.

**5 · PRECISION — corrected, all three.** *(a)* Every live statement now says "no
**additional relation-specific** maximum … beyond the common schema bounds",
naming `maxItems: 100000` and `uniqueItems`. *(b)* This was substantively wrong,
not a wording slip: the claim held for `unresolvedEdgeClasses` (a genuine set) and
was false for `input-closure-incomplete` (a single scalar while several inputs can
be missing). The text is now **per carrier**, with a new
`selectedScalarCauseLimitation` naming the selection's provenance and directing a
consumer needing the complete set to the retained records. **No multi-cause format
was invented.** *(c)* The five-column event rows have their own header again under
a new heading, rows untouched; controls parse §10 into contiguous headed blocks
and check each against its own header.

**6 · CONTROLS — corrected, and tested rather than asserted.** The prediction was
that at zero anchors the `ANCHOR_*` loop never runs for an inventory fact while
the `inventoried-file` join still does. `probes/p3_rawbytes.py` tested it: empty,
non-UTF8 binary and extensionless-path facts **ADMIT**; wrong digest, wrong
length, uninventoried path and wrong empty-length all **REFUSE** with their exact
join reasons; and the *same* non-UTF8 bytes still **REFUSE** as a source-text
anchor (`ANCHOR_UTF8`) — the discriminating pair. For location: nothing reads
`fact.anchors` as a finding location, so **no new flexibility was added**. A
finding locates through `finding-fingerprint.subjectKey.logicalPath`, an inventory
claim through its payload `path` joined to the inventory, and no
finding/fingerprint/proof/witness record carries an anchor field. Ten controls
retained.

**7 · NOTE-CONSUMPTION — accepted and corrected additively.** Above.

## This session's note, by point

1. **Originating boundary** — three boundaries named separately per admission §1's
   actor/layer law: external Config2/CLI → `CONFIG.INVALID`; a **host-generated**
   `analysis-spec` → `REQUEST.PRECONDITION_FAILED` as a **host invariant fault**,
   explicitly not a user configuration error; host-supplied release registry →
   `REQUEST.PRECONDITION_FAILED`. The `NOT-SELECTED` row is marked
   **origin-independent** (`REQUEST.UNSATISFIABLE`) — nothing is malformed. The
   pure helpers are passed rows and no provenance and never infer an origin.
2. **Absence versus the syntax guard** — the blanket pair is gone.
   `UNDECLARED_CAPABILITY_ACCOUNT` is deliberately **not** Coverage-shaped
   (`declared` / `candidateDeficiency` / `subjectToPrecedence`, never
   `coverage`/`deficiency`/`nativeCause`). Where a capability is both undeclared
   and unservable, `language-tier-unsupported` wins on the published precedence
   and the existing derivation governs; five controls hold it, including one that
   shows the existing guard still refuses a substituted pair.
3. **Candidate-only capabilities** — each absence row carries an explicit
   `projection`: `coverage-entry` with exact `relation@rung` coordinates, or
   `selection-account-only` with empty relations for `clones-near` and
   `clones-cross-tsjs`, which mint no fact and have no Coverage entry to carry
   anything. An availability account may be shared; it is automatically a Coverage
   result for none of them.
4. **`bindingToPlan`** — rewritten to the matrix-driven recipe, recording that the
   `(registry row, unit)` recipe is the one `requiredDefault` replaces. One
   normative recipe stands.

---

## Delta

**Aggregate vs frozen v13 — 13 files, 0 added, 0 deleted** (the complete set for
eventual direct integration; per-file `beforeSha256`/`afterSha256` in
`handoff.json`). **This turn vs v1 — 10 files**, `v1Sha256`/`finalSha256` in
`handoff.json`; before-images for all ten are in `before-images/` and each equals
the v1 released byte. The three aggregate-changed files *not* touched this turn
are `identity-schemas.v2.json`, `check_native_evidence.v2.py` and
`security-and-lifecycle.md`.

Released work contains no source-pin change, no generated report, no validation
summary, no review/crosswalk/readiness/application record and no security
reference model.

## Final checks — once, on the final source

Disposable copy, explicit measured temporary repin (23 entries over exactly the 13
aggregate-changed files). **These repinned bytes are a development instrument and
are not accepted pin evidence.** The released and suite copies were diffed
afterwards and differ in exactly three files: the two repinned manifests and
`native-evidence-report.v2.json`, regenerated *inside* the disposable copy.

| script | exit | result |
|---|---|---|
| `check-foundation.py` | 0 | 231/231 |
| `check-identity.py` | 0 | **1203 passed, 0 failed** (1133 in v1) |
| `check-product-quality.py` | 0 | 24/24 |
| `check-product-configuration.py` | 0 | 28/28 |
| `check-array-orders.py` | 0 | 65/65 |
| `check_workflows.v1.py` | 0 | 1598/1598 |
| `check_native_evidence.v2.py` | 0 | **347/347** cases; 66 cells; 0 open objects |

Efficiency: discriminating work ran through `probes/bounded_loader.py`, which
extracts the same fixed 54-definition fixture set root's instrument uses and
executes it in a disposable copy (~0.5 s per probe against ~75 s for the full
checker), recording the source hashes it read. It writes nothing into the released
tree and is an instrument, not accepted source. The full checker was run only to
confirm named controls in situ and once at the end.

## Development limits

No product exists to measure and none was assumed; every compiler, grammar,
provider, permission value and release declaration is a **synthetic** trusted
input. Passing-call totals are development evidence produced with temporary pin
changes — not final frozen-source acceptance, not distinct-case or qualification
counts. The absence account is a selection-boundary record: whether a real host
emits the corresponding Coverage, and what a real release ships, stay unmeasured.
The location controls say nothing about renderer or repair-tool behaviour.
`check_native_evidence` writes its `PIN-MISMATCH` report to the **in-tree** path
regardless of `--report`, so it was run only inside disposable repinned copies.

Four failed development attempts are retained with their logs in `handoff.json` —
including one that mattered: among the six control failures after the note points,
five were my controls being too narrow, but **one was a real data slip** (I had
given the origin-independent `NOT-SELECTED` row a `byOriginatingBoundary` it should
not have), now corrected with `originIndependent` stating why.

## Standing

Original Bv4 findings are unchanged: **2 MUST / 2 SHOULD / 4 advisory**, the same
eight ids, the blind's own severities. Root's same-scope follow-ups do not rewrite
them, and the 43 historical advisories remain root's successor records.

Root owns final reference/fixture integration, records **before** pins, the
`internalAliases` materialisation (pairs published here), the six final pinned
commands, the pin seal and freeze, and the fresh independent, blind and
application reviews. The four judgement calls for Codex to confirm are: the
five-coordinate totality match including the redundant `snapshotId`; the
matrix-fixed default with the release as availability only; the absence account
deliberately not being Coverage-shaped, with its precedence and candidate-only
projection; and the originating-boundary routing that keeps a host-generated spec
fault off `CONFIG.INVALID`.
