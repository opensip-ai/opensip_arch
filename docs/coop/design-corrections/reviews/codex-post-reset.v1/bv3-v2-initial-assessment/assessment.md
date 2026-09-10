# bv3-corrections-author.v2 — assessment of Codex rechecks, written BEFORE editing

**Standing.** This is my substantive assessment of each point root raised, made
after reading `current-codex-note.md` and every report under
`root-input/codex-rechecks` in full, and after independently reproducing the
disputed results against my own released v1 source. It is not an acceptance of
anything and confers no review status. Where I agree, I say why on evidence;
where I disagree I say so and cite the source.

**Reproduction basis.** `v2/work` is byte-identical to my released `v1/work`
(2981 files, 0 differences) and differs from frozen v12 in exactly my 20 v1
changes. I re-ran Codex's own probe scripts against a disposable copy of my
source plus root's adapted `integration-fixtures.py`
(sha256 `9ea48d52…`, matching root's recorded hash exactly).

---

## 0. Manifest SHA — resolved, and my earlier limit was self-inflicted

`fc124cc7d487f7f6fcc97665255574273b03fe1f09e6b70c3246feedf1678beb` is the **raw
SHA-256 of the file** `root-input/candidate-subject.v12.json` (668000 bytes).
Verified: computed hash equals the declared value exactly.

I then verified the frozen subject against that manifest's 2981 rows:
**0 missing, 0 hash mismatches, 0 byte-length mismatches, 0 extra files on disk.**

My v1 handoff recorded this as an unreproducible "aggregation algorithm" and
tried seven aggregation variants. That was my error of assumption, not a gap in
root's records — I assumed the value summarised a tree when it identified a
file. The v1 statement stays as written; this is the additive correction.

## 1. M3 — bundled grammars. **Codex is right. Not complete in v1.**

**Reproduced on my own source.** Running root's `probe-grammar-domain.py`
against my v2 copy gives the same result as root's report: `typescript`,
`javascript`, `rust` admit; **`json`, `toml`, `markdown`, `yaml` — all already in
`BUNDLED_GRAMMARS` — are REFUSED** by
`SyntaxGrammarBundleV1.grammars.items.properties.languageId`; `python` (correctly
unsupported) refuses. `BUNDLED_GRAMMARS` at `native_evidence_model.v2.py:2732-2734`
contains 14 suffixes over **seven** language ids.

My v1 handoff §2.4 called the three-member equality a positive drift check. As a
*coverage* claim that was wrong: it proved the enum matched itself, not that the
bundle was representable. `assign_membership` (line 2944) routes exactly those
suffixes to `membership: syntax-only, reason: grammar-only`, so the four data
grammars are live today and my descriptor could not express them.

**The exact distinction root asked me to identify does exist, and it is not the
one my v1 implied.** Searching the whole kit:

- §6.3 defines body spans as *"function, method, closure/lambda, `impl` item and
  block bodies"*, gives L2/L3 normalisation tables **only** for TypeScript/JavaScript
  and Rust, and states *"Fact identity is same-language: `languageId ∈
  {typescript, javascript, rust}` is in the preimage"*. That closure is a
  reasoned law about clone body identity, not an oversight.
- U-4 gives grammar-only files exactly one published role: membership
  (`grammar-only` = "bundled grammar, no program"), i.e. honestly accounted,
  **not** `unsupported-file`.
- There is **no** published tokenisation, normalisation, `literalKind` mapping or
  capability statement anywhere in the kit for JSON/TOML/Markdown/YAML as
  analysed languages. They appear only in `BUNDLED_GRAMMARS` and as config files
  Cargo/TypeScript read.

So the real distinction is **membership/inventory capability (any bundled
grammar) versus body-identity/code-construct capability (the three code
languages, by §6.3)**. `declares`/`literal`/`control-flow` payloads are
code-construct shaped (`declarationKind ∈ {module…parameter}`,
`edgeKind ∈ {fallthrough…exception}`), and producing them for a data format
would require a tokenisation law the kit does not publish. Asserting that
capability would be exactly the fabricated-semantics failure M3 exists to
prevent.

**Planned correction.** Make all seven representable by giving each grammar row
an explicit capability class; keep clone body identity at the three code
languages on the §6.3 basis and say so; change the drift check from "all bundled
grammars == body-language enum" to "the **body-identity-capable** grammars ==
body-language enum", which accounts for all seven instead of ignoring four. Data
grammars stay `grammar-only` members bearing inventory evidence — **not**
relabelled unsupported. Then a complete Run over a non-TS/JS/Rust bundled
grammar exercising its promised capability, plus a control that such a grammar
cannot mint a clone body identity, plus an unknown-grammar (`.py`) negative.

**One thing I will flag rather than invent:** if the product does want
`literal@syntactic` for JSON/YAML/TOML, that needs a published tokenisation and
`literalKind` law. I am not writing one; I will record it as a bounded future
capability so the matrix does not over-promise.

## 2. M5 — clone ownership disclosure. **Codex is right. Not closed in v1.**

**Reproduced exactly** with root's `probe-bv3-ownership-cause.py` on my source:

| case | entry | my released v1 |
|---|---|---|
| `producer-control` | `resolution-incomplete` / `null` | **ADMITS** |
| `missing-cause-on-input-closure` | `input-closure-incomplete` / `null` | **ADMITS** |
| `unrelated-budget-deficiency` | `budget-exhausted` / `null` | **ADMITS** |
| `false-complete-claim` | `complete` / `null` | refuses `COVERAGE_DIALECT_PREREQUISITE:clones:enumeration-partial` |

The concrete bypass is exactly where root points. `identity-model.py:816-820`:

```
if entry['coverage']=='complete':          raise ...PREREQUISITE
if entry.get('deficiency') is None:        raise ...PREREQUISITE_UNDISCLOSED
```

That is the whole check. It never asks whether the deficiency is the *right*
one, and never looks at `nativeCause` at all — so an unrelated
`budget-exhausted` with a null cause satisfies it under partial ownership.

My v1 added the three `NativeCause` members and the §10 mapping row. Those are
**necessary but not sufficient**: they supply the vocabulary the enforcement
needs and nothing enforces it. Calling M5 "corrected" in my v1 handoff was
wrong, and I withdraw it.

**Planned correction.** Derive the expected `(deficiency, nativeCause)` pair from
the committed ownership state and the selected scope, and enforce that exact pair
at the producer and again at retained-Run admission; legal pair admits;
null/wrong-cause/wrong-deficiency/false-complete refuse with distinct causes.
Cover absent, partial and ambiguous **selected** ownership, plus healthy and
deliberately-excluded selections, keeping those two genuinely distinct.
Make `examinedExhaustive` versus `resolutionCompleteness.state` explicit.
Preserve empty-view indeterminacy and mint no fabricated body identity.

I will also fix the stale `sourceUnitOwnershipId.description`, which still says
null is admissible *"only while the edition map has a single distinct value,
where every body has the same dialect"*. The retained `selectionLaw` says the
opposite — there is **no** package-default fast path because `targetEdition`
overrides exist — and `body_language_version` refuses on missing ownership
unconditionally. The description is stale prose; the nullable form stays, because
retaining an unavailable/partial universe with an indeterminate empty clone view
is intended behaviour.

## 3. Import minimum — **Codex is right and my v1 reasoning was wrong. I adopt 0..4096.**

This is the one point where I made a substantive error of inference, so I want to
be precise about it.

My v1 justified `minItems: 1` by: *"adapterClosure asserts that an adapter ran
over the artifact bytes named by the custody record's sourcePath, so a zero-blob
import claims a payload whose input bytes were never retained."* Checking the
actual definitions:

- `common.schema.json#/$defs/UserInputPath` — the type of
  `ImportedEvidenceRecordV1.sourcePath` — says in its own description:
  *"never enters any content identity; recorded in operational records only."*
  My argument rested on a field the contract explicitly excludes from identity.
- There is **no** join anywhere from `sourcePath` to `wrapper.blobs`. The only
  `sourcePath` joins in `workflows_model.v1.py` (765, 775) belong to
  `SourceMappingV1`, which binds `sourceSha256` to the **snapshot inventory**,
  not to import blobs.
- Payload custody is independent of `blobs`: `registered_payload` retains and
  re-hashes the canonical payload bytes and requires the exact registered schema
  **document** bytes. Those obligations hold identically at zero blobs, so
  "the payload cannot be re-derived" does not follow.
- The archive-member rule I cited is *"an archive member outside the wrapper's
  `blobs` is never read"*. That is a **restriction on reading**, satisfied
  vacuously by an empty list. It does not mandate a member. My citation also
  pointed at §6 (clones); it is **§3 PO-4**, lines 916-935. Root is right on both.

So the correct reading is root's: `blobs` is the **auxiliary asset** inventory; a
self-contained normalized payload may legitimately have zero. Requiring one
arbitrary blob proves nothing about adapter-input custody and adds a restriction
no existing law supports.

**I adopt 0..4096.** The maximum keeps its authority — the workflow
`imported-evidence` description explicitly publishes 4096 blobs and a 256 MiB
artifact bound — and the compatibility change (foundation's 100000 → 4096) will
be stated.

I also accept the narrower methodological point: in v1 I treated *mirror
agreement* as if it justified the minimum. It does not. Agreement is a property
of the two documents; it says nothing about which admissible set is correct. The
13-case mirror parity result stands and is preserved; only the minimum moves, and
zero-asset and 4097 boundary controls will be same-instance tested on both
documents.

## 4. M4 — comparison scope binding. **Codex is right that a hash assignment is not a join.**

Verified in source: `adopt_baseline` (`workflows_model.v1.py:643-657`) sets
`ctx['scopeDigest'] = doc_digest(scope)` from its **passed** document, and its
`plan` argument is used only as `'planId': plan` — a PlanId string. The function
therefore cannot verify that the document was the Run's selected analysis-spec
parameter. The same is true of `ctx['policyDigest']`, whose comment already
claims `= plan.policyDigest`.

The registry half of M4 is genuinely done and root's `scope.json` confirms it
independently: base Run and a legal `ScopeDocumentV1` parameter ADMIT; missing
`include` and wrong selector refuse `PAYLOAD_RECORD:#/$defs/ScopeDocumentV1`;
unknown schema refuses `PAYLOAD_PARAMETER_UNREGISTERED`. That correction is
preserved.

**Planned correction.** Do both things root offers rather than one: name the
producing/admission precondition normatively and honestly (a pure projection
over documents the caller must already have admitted), *and* add a bounded
composition that, when the retained Plan and analysis-spec are available,
verifies the scope document is a member of the selected parameters — with
mismatched-digest and non-member controls. I will not describe the existing
assignment as proof of a join, and I will not build a product host. The
repository `scope-descriptor` versus operator glob `ScopeDocumentV1` distinction
stays.

## 5. Evidence and timing clarification — **root is right about the scope of my claim.**

My v1 `inputsConsumed` entry recorded `CODEX-PUBLIC-NOTE.md` with the standing
"read in full before the substantial edit batches and before handoff". The
accurate scope is narrower: my only full public Read of that file was at 06:02.
Root added further notes afterwards; my later tool call on that path **computed
its hash only** and did not re-read its contents, so the material added after
06:02 — the concrete cardinality reasoning, the retained-Run M5 counterexamples
and the M3/`BUNDLED_GRAMMARS` contradiction — was **not** reflected in my v1
handoff. A hash is not substantive reading, and the "before handoff" half of that
claim overstated what I did.

The v1 handoff and custody stay byte-identical; this is the additive correction,
and it is recorded here and in the v2 handoff rather than by rewriting history.

I also accept the framing that root's probes and the earlier independent/blind
judgments are **literal evidence, not new acceptance**. Nothing here confers
review status on my own work.

---

## Summary of positions

| # | Point | My position |
|---|---|---|
| 0 | Manifest is a raw file hash | **Agree** — verified; my v1 assumption was the error |
| 1 | M3 incomplete for 4 already-bundled grammars | **Agree** — reproduced; distinction identified in §6.3/U-4 |
| 2 | M5 not closed by enum additions | **Agree** — reproduced; v1 claim withdrawn |
| 3 | Import minimum should be 0..4096 | **Agree — my v1 reasoning was wrong**; adopting 0..4096 |
| 4 | `adopt_baseline` hash ≠ selected-parameter join | **Agree**; registry half preserved |
| 5 | Note-consumption claim overstated | **Agree**; corrected additively |

I have **no substantive disagreement** with root's five points. Every one is
supported by source I re-read and by results I reproduced independently on my own
released bytes. Two of them (3 and 5) are corrections of my own errors rather
than gaps I merely failed to fill, and I have said so plainly rather than
presenting them as refinements.

The work I will preserve unchanged, because root's own rechecks confirm it:
M1/M2 ladder authority and rung vocabulary (16/16 policy cases pass), the closed
relation namespace, mirror **order** agreement and the duplicate/reversed
controls (13 cases, 0 mismatches), the `ScopeDocumentV1` registry row, and the
`node_modules` description fix.
