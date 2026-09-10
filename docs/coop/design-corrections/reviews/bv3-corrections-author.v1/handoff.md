# bv3-corrections-author.v1 — correction pass handoff

**Standing.** Design/schema/reference correction work only. Not product
implementation, not a commit, not a publication, not readiness or product
qualification, and not an acceptance of any kind. I am the correction author; I
am not the independent reviewer and not the blind consumer, and I cannot grant
their acceptance. Root owns integration, pin refresh, sealing, the successor
freeze, and the fresh independent ACCEPT / new blind review / final application
review that follow.

- `sourceRoot`: `/tmp/opensip-design-corrections/bv3-corrections-author.v1/work`
- Baseline: frozen candidate `v12`, 2981 files. The working copy was verified
  **byte-identical, file by file**, to `/tmp/opensip-design-corrections/candidate-subject.v12`
  before any edit (0 content differences, 0 extra, 0 missing).
- Delta: **20 modified, 0 added, 0 deleted.** No pin manifest, generated report,
  validation summary, review/crosswalk/readiness/application record, historical
  artifact, security source or admission contract is touched.

## 1. Findings addressed, with actual severities preserved

The interim blind artifacts reported five defects (F1–F5). The **completed**
blind review (`blind-review.json`, sha256
`e0fa53f338acb49323a2eb9d2b5318b4833cd8b7574d850b8c3fa760bbc8fb6b`, verdict
`CHANGES_REQUIRED`) supersedes that count with **5 MUST, 3 SHOULD, 4 advisories**.
Final severities below are the blind's own; the interim F-numbers are shown only
to map the earlier report.

| Finding | Severity (final) | Interim | Status |
|---|---|---|---|
| CB3-MUST-1 relation rung ladder not carried by the named registry | MUST | F4 | corrected |
| CB3-MUST-2 `minResolution` carries two vocabularies, no mapping | MUST | F5 | corrected |
| CB3-MUST-3 `syntax-only` has no admissible universe value | MUST | — | corrected |
| CB3-MUST-4 `ScopeDocumentV1` required as a parameter, no registry row | MUST | — | corrected |
| CB3-MUST-5 partial-ownership Coverage has no publishable typed cause | MUST | — | corrected |
| CB3-SHOULD-1 mirror declares a different owning array order | SHOULD | F1, F3 | corrected |
| CB3-SHOULD-2 `import.blobs` cardinality diverges (0 **and** >4096) | SHOULD | F2 | corrected |
| CB3-SHOULD-3 `ResolvedNodeModulesLayoutV1` description self-contradicts | SHOULD | — | corrected |
| CB3-ADV-3 inventory relations have no capability row | **advisory (kept)** | — | accounted, severity unchanged |
| CB3-ADV-1 / ADV-2 / ADV-4 | advisory | — | **not converted to blockers**; see §6 |

Additionally, **three same-class mirror divergences that neither report names**
were found by resolving `$ref`s on both sides (§2.1).

## 2. Diagnosis and the exact normative rules chosen

### 2.1 Import mirror (CB3-SHOULD-1, SHOULD-2, and three unreported)

One import has one `importId` over one wrapper, admitted through **two**
documents: foundation `identity-schemas.v2.json#/$defs/import` and its declared
"exact mirror" `imported-evidence.schema.json#/$defs/ImportWrapperV2`
(likewise `scope-descriptor` / `ImportScopeDescriptor`). Both claimed exactness
while disagreeing, in **both directions**. A resolved structural differential
measured **9** divergences, not 3:

| # | Field | Foundation | Workflow mirror | Reported by |
|---|---|---|---|---|
| 1 | `omissions.x-opensip-order` | `canonical-set` | `sequence` | SHOULD-1 |
| 2–4 | scope `workspaceRoots`/`pathPrefixes`/`excludedPathPrefixes` order | `canonical-set` | `sequence` | SHOULD-1 |
| 5 | `blobs.minItems` | absent | `1` | SHOULD-2 |
| 6 | `blobs.maxItems` | `100000` | `4096` | SHOULD-2 |
| 7 | `blobs[].bytes.maximum` | `2^64-1` | `268435456` | **unreported** |
| 8 | `blobs[].path.pattern` | absent | `LogicalPath` grammar | **unreported** |
| 9 | `blobs[].path.not` (dot/dot-dot) | absent | present | **unreported** |

7–9 are invisible without resolving `$ref`s: the foundation record inlines its
own primitives while the mirror `$ref`s `common#/$defs/{Blob,LogicalPath}`.

**Chosen law.** The foundation record is the **authority**; the mirror restates
it field-for-field and both must admit and refuse exactly the same bytes.

- Order and path grammar resolve to the **foundation** values (1–4, 8, 9): the
  foundation record owns the digest preimage, and identity §3 already states both
  the `canonical-set` annotation and the logical-path grammar. Foundation gained
  a `LogicalPath` `$def` (byte-identical in constraint to the workflow one) used
  by `Blob.path`; the grammar was previously prose-only and enforced imperatively
  for `scope-descriptor` alone. Measured impact first: **82 blob rows across the
  live corpora, 0 would newly refuse.**
- Cardinality and byte bound resolve to the **import unit's own published
  hostile-input bounds** ("at most 4096 blobs", "artifact at most 268435456
  bytes"), carried as a distinct foundation `import-blob` record so the bound
  applies to imports and is **not** silently imposed on `source-inventory` or
  closure `tree` rows.
- `minItems: 1` is decided from **required payload/closure semantics**, not from
  whichever schema was stricter, as instructed. `blobs` is the closed inventory
  of retained artifact members (an archive member outside it is never read), and
  `adapterClosure` asserts an adapter ran over the artifact bytes the custody
  record's `sourcePath` names. A zero-blob import therefore claims a payload
  whose input bytes were never retained and whose `payloadDigest` can never be
  re-derived. The registered preimages remain a separate, fully joined set
  (`retainedPreimages`), unchanged.

**Intentional admissibility change, stated explicitly:** the foundation harness
`graph_with_import()` built imports with `blobs=[]`. That was not intentional
admissibility — it was this very divergence in the candidate's own corpus (the
same wrapper would have been refused by the mirror). It now names the artifact
it read.

**Semantic, not descriptive, proof.** `check_workflows.v1.py` gains a
differential that validates the *same instance* against *both* documents and
requires identical admit/refuse verdicts — 21 instances, each on a boundary the
two documents once disagreed about, plus a discriminating-negative floor so it
cannot pass by both documents being permissive. On frozen bytes it fails **24**
checks; on corrected bytes 21/21 agree.

### 2.2 Relation rung ladder (CB3-MUST-1)

`x-opensip-relation-registry` had **no `ladder` key**. Its `rungs` member is a
per-rung required/forbidden **field-rule** table, legitimately `{}` for the eight
single-rung relations. Both readings are wrong: strictly, those eight admit no
resolution at all; leniently — as `identity-model` did via `... and row['rungs']`
— the ladder check is skipped for them entirely.

**Functionally demonstrated on frozen bytes** (probe `p2b`, with a *passing*
positive control): a `declares` fact carrying `resolved-callee`, `checked`,
`resolved-binding`, `resolved-target` or `normalized-body-hash` — all rungs of
*other* relations — **closes a Run**. Root cause: `Rung` is a flat 15-member
global enum with no relation binding, so those values are well-formed;
**schema vocabulary is not relation membership.**

*(My first probe was non-discriminating — it mutated only the fact, so every
case including the control died at `FACT_SCOPE_JOIN`. Retained at
`logs/p2-FAILED-ATTEMPT-nondiscriminating.json`.)*

**Chosen law.**
- Each row carries an explicit ordered **`ladder`**, weakest-first, inherited
  verbatim from `fact-plane.v1 relationRegistry.relations[].ladder` plus
  `[observed]` for `unresolved-edge`. **No ladder value is authored by me.**
- `rungs` keeps its real meaning; the registry now says so, and says that an
  empty field-rule table is never an absent ladder.
- Membership is against `ladder`, **always, with no empty-ladder fallback**; a
  relation with no ladder is a registry defect and refuses.
- Order is the index within one relation's ladder. No global rank; a
  cross-relation comparison is an admission refusal, not a boolean.

**One authority, no fourth source.** Per Codex's steering, `LADDERS` in
`native_evidence_model.v2.py` is now **read from** the authority instead of
restated, and `check_native_evidence.v2.py` drift-checks every mirror
**exactly and in order**.

> **Finding neither report names.** `RELATION-LADDER-DOMAIN-V2.ladders` declared
> `fact-plane…[].ladder` as its source while being **alphabetised**, reversing
> `calls`, `imports` and `references`. It was harmless only because that registry
> is consulted for membership alone — anything reading it as an *order* would
> have let a syntactic fact satisfy a demand for a resolved rung. Reordered to
> weakest-first; membership unchanged; the drift check catches re-alphabetisation
> (3 failures when reverted).

### 2.3 Policy/native/repair resolution order (CB3-MUST-2)

Assessed substantively as instructed, across the **full** policy/native/repair
interfaces rather than one `eval_pred` line:

- `policy-document#/$defs/Resolution` = `{syntax, resolved, type, external}`,
  reached from `Atom.minResolution` **and reused by** repair's
  `EvidenceRequirement.minResolution` and `policy-test`.
- Native `RequirementV2.minResolution` and `CoverageKeyV2`/`ViewEntryV3.resolution`
  use the 15 actual rungs. **Zero shared members.** No mapping published.
- `workflows_model.RES_ORDER = {syntax:0, resolved:1, type:2, external:1}` is a
  **single global rank** over the abstract words — precisely what the inherited
  C-1 law forbids (`forbiddenGlobalFields: [quality, tier, degraded, rank]`), with
  an arbitrary `external`/`resolved` tie.
- The workflow fixtures' `relation` values include `runtime-observation` and
  `history-change`, which are **not** native fact relations, and `Atom.relation`
  had no admission at all.

**Both options were weighed.** Preserving abstract syntax requires a
**per-relation** mapping — `resolved` names a different rung in each of
`imports`/`references`/`calls`/`reachability`, `type` names a rung only for
`types`, `external` names no native rung — so it is a partial, lossy renaming
with no expressive power, it does not preserve one-word-one-meaning, and it
cannot survive C-1 (`syntax < resolved < type` *is* a global ladder; making it
relation-relative dissolves it into the rung names). It would also **add** a
mostly-empty normative table while `RES_ORDER` had to die either way.

**Chosen law (smallest coherent correction): name the rung directly.**
`Atom.minResolution` and `EvidenceRequirement.minResolution` are rung names; the
abstract `Resolution` enum and the global `RES_ORDER` rank are **withdrawn**;
satisfaction is ladder-index comparison inside one relation.

**Admission, in two conditions.** The schema constrains `minResolution` to the
flat vocabulary — exactly the union of the authority's ladders, drift-checked —
which is **necessary only**. Ladder membership is **sufficient** and is enforced
at admission: in `resolve_policy`, in `repair_preview`, and — per Codex's
steering — **at the Run closure** (`open_run_closure`) over both the Plan's
`PolicyDocumentV1` and the proof's compiled `RuleProgramV1`, so a sealed Run
cannot assert a predicate that was never admissible.

**Closed relation namespace.** An atom names a native fact relation or one of the
imported-evidence relations closed by a new
`imported-evidence#/x-opensip-evidence-relation-registry`
(`runtime-observation`, `history-change`), each with the one-rung ladder
`[observed]` — **no new rung token is introduced**; `observed` is already the
registered rung of `unresolved-edge`. An evidence relation must declare its
`evidence` kind; a native fact relation must not carry one. These are
deliberately **not** added to the 13-relation native registry: they mint no
`fact2` and carry no universes.

**Compatibility and scope.** This is a dialect change to `PolicyDocumentV1`,
`RuleProgramV1`, `PolicyTestSuiteV1` and repair's `EvidenceRequirement`. It is
design-stage: every instance lives in this kit, and all 28 were rewritten by an
explicit **per-relation** table that refuses to guess (any unmapped
(relation, tier) pair aborts rather than defaulting). Each rewrite preserves the
instance's ladder position, so **no expected policy verdict changes**; the
workflow suite re-verifies that independently. Any policy document outside this
kit would need the same per-relation migration — there is no compatible global
rewrite, which is itself the evidence that the abstract tier was never
well-defined.

**Independent confirmation of the root regression.** Reverting only the subject
bytes under the corrected fixtures reproduces
`RES_ORDER[f['resolution']] → KeyError: 'resolved-target'` — the exact failure
root's own probe reports on frozen v12.

**Negative/closed-world semantics are untouched.** Strong-Kleene evaluation,
`all-covered`, coverage-sufficiency and the universal-negative requirements are
unchanged; no global boolean replaces Coverage sufficiency, and the small
fixture interpreter is still not a production evaluator (its existing limitation
text stands).

### 2.4 Syntax-only universe (CB3-MUST-3)

`fact2` and `subject-scope` both **require** a `native-semantic-universe`
h-identity; that set held exactly the TypeScript and Rust universes; §1.2 gave
`syntax-only` the universe "none". So the mode's own advertised cells
(`declares`/`literal`/`control-flow@syntactic`, `clones@normalized-body-hash`)
and **every `file`/`package`/`vcs-change` fact in a repository with no
TypeScript or Rust unit** could mint no fact and no scope.

**Chosen shape:** a third registered universe `native.semantic-universe.syntax.v2`
over a third context `native.context.syntax.v2`. Nullable universe fields were
rejected — that deletes the invariant that every fact states what produced it and
leaves "which grammar read this body" unanswerable. Narrowing the matrix was
forbidden and would have removed advertised capability.

- **Context** carries one thing: `SyntaxGrammarBundleV1`, pinned the way a
  toolchain is — an admitted **`kind=grammar`** closure, `parserVersion` that
  must equal that closure manifest's `semanticVersion`, and every grammar
  definition, bundle manifest and normalizer spec present in the retained tree.
  No toolchain, stdlib, lockfile, node_modules or config graph. Per Codex: a
  **signed/bound grammar/normalizer closure owns the syntactic version
  information**; no static constant and no fabricated TS compiler.
- **Universe** commits the context plus the **selected** grammar set (a different
  selection is a different universe, not an invisible default) and the constant
  `resolutionAttempted=false`.
- **Dialect axis:** `body-language-version.dialect` gains a `{grammarVariant}`
  branch. A grammar-only analysis has no compilation unit, so it has no edition;
  claiming one for a `.rs` body read without Cargo would fabricate compiler
  semantics. Because it is a distinct branch, **a grammar-parsed body never mints
  the same identity as a compiler-parsed one** — required, since equating them
  would be a false clone claim.
- **The existing `languageId` join is respected**, as Codex required: bundled
  grammars are held **equal** to the closed `{typescript, javascript, rust}` enum
  by an executed drift check, so advertised grammar coverage cannot outrun what a
  clone identity can express.
- **Capability is not widened**: only inventory, `syntactic` and clones rungs;
  semantic rungs stay `language-tier-unsupported`, `unresolved-edge` stays
  unavailable, and universal negatives still require their own complete Coverage.
- `body_language_version` needed **no code change** — it is table-driven from the
  registry row.

Also, per Codex, **CB3-ADV-3 is accounted for here while keeping its advisory
severity**: the matrix gains an `inventory` capability naming the three inventory
relations and the component that produces them (host discovery/enumeration, in
every mode), with a note that their universe in a compiler-free repository is the
syntax universe.

### 2.5 `ScopeDocumentV1` parameter row (CB3-MUST-4)

The comparison contract requires `EvaluationContext.scopeDigest` to be bound as
an analysis-spec parameter; the `parameter` class was closed to one document and
a key with no row refuses — so the binding refused at Plan admission and the
comparison scope axis was unimplementable. Registered the exact owning
document + selector (`workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1`),
kept distinct from the foundation `scope-descriptor` (repository extent vs policy
glob selection; both may appear in one Plan). No arbitrary `registeredSchemas`
fallback and no permissive unregistered parameter: those still refuse.

**Hardening found while doing it:** the class is keyed by the cited **document**
digest, so two rows selecting different records out of one document would be
indistinguishable and the first listed would silently win. That is the arbitrary
selection the registry law forbids, so an ambiguous key now refuses.

### 2.6 Clone ownership causes (CB3-MUST-5)

`NativeCause` could not name any of the three ownership states the
`languageVersionBinding` selection law refuses on, so the disclosure §11 mandates
had no expressible value — and `nativeCause: null` records that a disclosure was
*owed and not made*, it does not fulfil it. Added
`body-language-ownership-missing`, `body-language-owner-unenumerated`,
`body-language-owner-ambiguous`, mapped in the §10 `input-closure-incomplete`
row. The other selection-law refusals get **no** cause, explicitly justified:
`OWNER_NOT_COMPILED`/`OWNER_NOT_SELECTED` are per-body refusals §11 states are
compatible with `coverage: complete`, and `DIALECT_ABSENT`/`DIALECT_AMBIGUOUS`
refuse before a Coverage entry exists. Body refusal and indeterminate empty-clones
Coverage are unchanged.

### 2.7 `ResolvedNodeModulesLayoutV1` description (CB3-SHOULD-3)

Description corrected to match §2.2 and the `blobJoin` annotation (retained
outside the inventory, joined by digest). **Behaviour unchanged** — this was a
machine-readable prose fix only, as the finding asks.

## 3. Checks actually run, and their results

All commands used `/tmp/opensip-architecture-review-env/bin/python -I -B`.

Whole-suite runs used a **further disposable copy** (`probes/devtest.sh`) with an
**explicit measured pin refresh**, because existing pins are intentionally stale
in a development source copy. **Those refreshed pins exist only in the disposable
copy and are not candidate bytes; they are not evidence that the candidate's pins
are correct.** Root owns the final pin refresh and seal.

| Checker | Baseline (frozen v12) | Final (corrected) |
|---|---|---|
| `foundation/check-foundation.py` | 231/231 | **231/231** |
| `foundation/check-identity.py` | 767/767 | **823/823** |
| `foundation/check-product-quality.py` | 24/24 | **24/24** |
| `foundation/check-product-configuration.py` | 28/28 | **28/28** |
| `foundation/check-array-orders.py` | 65/65 | **65/65** |
| `workflows/check_workflows.v1.py` | 1290/1290 | **1590/1590** |
| `native/check_native_evidence.v2.py` | 151/151 cases, 60 cells | **346/346 cases, 66 cells** |

Every unit exits 0. Net new: +56 identity checks, +300 workflow checks,
+195 native cases, +6 matrix cells.

**Probes** (`probes/`, outputs in `logs/`):

| Probe | Purpose | Result |
|---|---|---|
| `p1_mirror_diff.py` | resolved structural mirror differential | 9 divergences before, **0** after |
| `p2_rung_exploit.py` | first F4 attempt | **retained failure**: non-discriminating |
| `p2b_rung_exploit.py` | F4 with a passing positive control | `DEFECT-PRESENT` before, `CLOSED` after |
| `p3_blob_path_impact.py` | impact of the path tightening | 82 rows, **0** would newly refuse |
| `p4_preserved_guards.py` | guards that must survive | **all present and passing** |
| `p5_regression_matrix.sh` | corrected checkers vs frozen subject bytes | fails, incl. the `RES_ORDER` `KeyError` |
| targeted mirror regression | frozen schemas, corrected checker | **24 failures** |
| targeted ladder regression | frozen capability registry | **3 order failures** |

## 4. Preserved identities and intended descriptor changes

**Preserved unchanged in meaning** (verified by `p4`, 1042 check ids, all
matched guards passing): typed annotation conflict / alias / cycle / missingness
guards; all three digest-law limbs; clone version, dialect and source-inventory
joins; early annotation comparisons; universe rules; Coverage sufficiency.

**Intended descriptor/vocabulary changes** (each with its reason above):
`body-language-version.dialect` gains a `{grammarVariant}` branch; closure `kind`
gains `grammar`; `NativeContextLanguageV1` and the admission `domain` enum gain
`syntax`; `NativeCause` gains three ownership causes; `languageModes.map.syntax-only`
`null → "syntax"`; `PolicyDocumentV1` `Resolution → Rung`; a new
`x-opensip-mirror` annotation on `import.blobs` and a new
`x-opensip-evidence-relation-registry`; the `parameter` registry gains one row;
the matrix gains an `inventory` capability and 6 cells.

**Pinned constant deliberately updated, law unchanged:** the native digest-law
case moved 72 → 76 sites. `total == annotated` still holds and an unannotated
64-hex field would still fail — only the count moved, and the case note records
exactly which four sites and why.

## 5. Verification of the delta

- Working copy vs frozen v12 at start: **byte-identical** (2981 files).
- Final delta: **20 modified, 0 added, 0 deleted** — every path listed with
  before/after sha256 in `output/changed-files.json` and `handoff.json`.
- Explicitly verified **0 changes** in: source-pin manifests (12 candidates),
  generated reports (69), review/history records (1775), security sources (35),
  admission contract (3), validation summaries (10), crosswalk/readiness/
  application records (22), inherited artifacts (27), completion records (1061).
- `native-evidence-report.v2.json` was modified once by an early in-tree checker
  run and was **restored to frozen bytes**; verified identical. All later native
  runs were confined to the disposable copy.
- New probe files live under `probes/`, never in the candidate.
- Exact BEFORE images of every changed source: `output/before-images/`.

## 6. Remaining limits and open items

1. **No acceptance is conferred.** Not readiness, not product qualification, not
   an independent review. Codex must substantively review this source, these
   probes and this prose before any released bytes are integrated.
2. **Pins are intentionally stale in the candidate delta** and I did not touch
   them. The suite results above come from a disposable copy with measured pins;
   they are development evidence, not accepted-candidate pin proof. Root refreshes
   pins **after** all recording edits, then runs the six commands and seals.
3. **I could not reproduce root's manifest aggregation** `fc124cc7…`; seven
   plausible algorithms were tried and none matched. I verified the stronger
   direct property instead — file-by-file byte identity with
   `candidate-subject.v12`. Root should confirm against its own algorithm.
4. **`p4` covers the foundation checkers' check ids**; the workflows report
   publishes aggregate counts only, so workflow-side guards are evidenced by the
   suite's own pass/fail rather than by id matching.
5. **`bind_syntax_universe` accepts `retained`/`snapshot_inventory` for signature
   parity and does not consult them** — the syntax universe names no retained
   nested record and no snapshot path. Stated in the docstring so it is not
   mistaken for a weakened join.
6. **Advisories were not converted into blockers**, per instruction. ADV-1
   (pin-inventory completeness) and ADV-2 (confinement claim is a host join) are
   valid scope limits and I did **not** weaken the host obligations they rest on.
   ADV-4 (the 723-byte example) needs no algorithm change; I did not alter the
   number or the example — the naming-dependence point is noted here rather than
   asserted as one number for all 21-crate maps. ADV-3 is accounted for in §2.4
   at unchanged advisory severity.
7. **Cross-unit dependency root must fix on integration:** the native unit now
   consumes `foundation/relation-payload-schemas.v2.json` (the ladder authority)
   and reads `docs/coop/artifacts/fact-plane.v1.json` for the drift check. The
   first is added to `CONSUMED_SOURCES`, so **the native pin manifest will need
   that new row** when root refreshes pins. I did not edit the manifest myself.
   The fact-plane artifact is read with plain `json` (not `C`) because it carries
   float lexemes elsewhere that `C` correctly refuses; only its ladder arrays are
   read, and only as exact string arrays.
8. **Not attempted:** no host product implementation, no compiler/provider
   execution, no changes to the security unit or the admission contract, and no
   re-derivation of any report.
