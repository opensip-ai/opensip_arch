# v21 evaluator contract assessment — does the published join fully define replay?

**Assessor:** actual Claude, bounded design-coauthor assessor. **Source:** frozen
`/tmp/opensip-design-corrections/candidate-subject.v21` (manifest SHA
`360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`). Read scope is
listed in `assessment.json#readScope`. I did not read prior reviews, review
directories, or author responses before deriving the answer below; the one author
reference model I opened (`workflows/workflows_model.v1.py`) is cited **only** as
implementation evidence in §7 and carries no normative weight.

## 1. Verdict

**No.** The join is *substantially* built but **not closed**. Nine named public
semantics are absent, four of them at the centre of the question. An independent
implementer given only the published contract cannot reconstruct the same subject
set, the same matching facts, the same completeness value, the same findings or
the same verdict without inventing public semantics. This is not a case of a
deficient implementation proving a gap: in each case below I can name **two
conforming readings that produce different retained `proof2` bytes** from one
Plan, which is exactly the standard identity-and-evidence §3 lines 754–777 already
applied when it withdrew the abstract `Resolution` tier ("two conforming
implementations emitted different findings from the same Plan").

Crucially, the missing items are **selection laws, not retention gaps**. Every
datum needed for seven of the nine is already retained and Plan-joined. Two
require unavoidable typed schema change.

## 2. What is already answered (do not re-open)

These are genuinely closed and any correction must preserve them verbatim:

- **Rung satisfaction.** `policy-document.schema.json#/$defs/Atom/properties/minResolution`
  plus `relation-payload-schemas.v2.json#/x-opensip-relation-registry/{ladderAuthority,membershipRule}`:
  ladder-index comparison **within one relation**, `≥` the atom's rung, membership
  enforced at policy resolution *and* Run closure. No global rank.
- **Relation closure.** An atom names one of thirteen native relations or
  `runtime-observation`/`history-change`
  (`imported-evidence.schema.json#/x-opensip-evidence-relation-registry`), with the
  `evidenceDeclarationRule` separating the two planes at admission.
- **Fact↔scope join key.** `(snapshotId, relation, resolution, sourceUniverse,
  targetUniverse)` — `relations.file.coverageTotality.matchOn`, `coveragePartitionLaw.partitionKey`,
  native-evidence.md 309–328. Cross-universe leakage is already refused.
- **Kleene table, predicate node addressing, witness contents.**
  identity-and-evidence.md 1354–1360, 1140–1147; `identity-schemas.v2.json#/$defs/program-predicate`
  fixes `p`, `p.i`, `p.0` addressing exactly.
- **Rule-program projection.** identity-and-evidence.md 526–529: `RuleProgramV1` is
  *exactly* `{schemaVersion:1, policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]}`
  in policy `ruleId` order.
- **Waiver resolution.** Expiry/duplicates at Plan construction; `plan.waiverDigest`
  is the *resolved* set (workflows §5, 489–495).
- **Canonical order and identity recipes** throughout §3.

## 3. The four central gaps

### G1 — `subjectEnumeration.universe` has no binding recipe (MUST)

`Rule.subjectEnumeration.universe` is `common#/$defs/CanonicalIdentifier`
(`^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$`). Every retained universe reference is a
bare 64-hex H-identity (`identity-schemas.v2.json#/$defs/fact/properties/sourceUniverse`,
`#/$defs/subject-scope/properties/sourceUniverse`,
`native-evidence.schemas.v2.json#/$defs/CoverageKeyV2`). **No document binds one to
the other.** The only two plausible readings:

- **(a) domain-set member name** — one of `native.semantic-universe.typescript.v2`
  / `.rust.v2` / `.syntax.v2`
  (`identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/native-semantic-universe`),
  denoting the *set* of Plan-bound universes of that domain;
- **(b) the 64-hex digest itself.**

(b) is very likely wrong — the `CanonicalIdentifier` pattern requires a leading
`[a-z]`, so roughly ten of sixteen possible digests are unrepresentable, and a
policy naming a per-Run digest is not portable across snapshots. But "very likely
wrong" is not a published law, and (a) still leaves the **multi-universe**
question open, which native-evidence.md 314–323 states is not hypothetical.

**Discriminating example.** A Run binds a TypeScript universe `U_ts` and a syntax
universe `U_syn`, each with its own complete `file@enumerated` scope over `a.ts`.
Under (a)-with-union the rule sees one subject `a.ts`; under (a)-per-universe it
sees two evaluations; under (b) it sees whichever digest was pasted. Three
different `predicateProofs` arrays, three different `proof2`.

### G2 — subject selection, `subjectKind` mapping, and glob applicability (MUST)

`subjectEnumeration` names `universe`, `subjectKind ∈ {file,symbol,export,package}`
and optional `LogicalPath` globs. Nothing says **which retained inventory** the
subjects come from. The only retained subject inventory is
`subject-scope.subjects`, keyed by `(snapshot, universes, relation, resolution)` —
coordinates the DSL never mentions. Two plausible readings: union over *all*
scopes of the matching kind, or only over scopes whose relation appears in the
rule's atoms. The second makes enumeration depend on the predicate tree; the
first enumerates subjects that bear no fact at all. Both are defensible; only the
first answers the "absent facts" case, and neither is published.

Three sub-defects compound this:

- **Kind vocabulary mismatch.** The registry's `subjectKind` vocabulary is
  `source-path | symbol | package-name`
  (`x-opensip-relation-registry/subjectKindLaw`). The DSL's is
  `file | symbol | export | package`. No mapping is published, and **`export`
  names nothing at all** — no relation, no scope, no retained field. Today a rule
  with `subjectKind: export` is schema-valid and silently selects the empty set,
  i.e. a vacuous pass.
- **Globs over non-paths.** `subjectKindLaw` states, deliberately, that `symbol`
  subjects are opaque `SubjectIdV1` and that symbol-to-file attribution "is NOT
  re-derivable from the retained Run" (repeated at native-evidence.md 447–455).
  A `LogicalPath` glob over an opaque identity therefore has no defined meaning:
  match-as-text and always-false are both conforming, and they differ in subject
  count.
- **No atom/kind agreement rule.** Nothing stops `subjectKind: file` with an atom
  over `calls` (whose subjects are `symbol`). Under any subject-binding law that
  atom can never match — so `none` over complete Coverage returns **true**, a
  fabricated universal negative. This is the exact failure class §3's rung
  correction exists to prevent.

### G3 — an atom has no published way to bind the current subject (MUST)

This is the sharpest gap. `FieldFilter` compares a projected field to a **literal**
`value` (string / integer ≤ 1e6 / string array). There is no `$subject`
placeholder, no `eq-subject` comparator, and no prose anywhere saying an atom is
implicitly restricted to the enumerated subject. Yet
`proof-bundle.predicateProofs[]` is keyed by `(ruleId, subjectId, predicateId)`
and ordered by that tuple (`x-opensip-order: predicate`), which only makes sense
if predicate values vary per subject.

**Discriminating example.** Rule `r1`: `subjectKind: file`, `emitWhen: {op: exists,
relation: file, minResolution: enumerated, filters: []}` over a 100-file snapshot.
Under implicit binding: 100 proofs, values determined per file, findings only where
a file fact exists. Under no implicit binding: 100 proofs all `true`, 100 findings.
Both satisfy every published sentence. `verdict` differs.

Even granting implicit binding, `subjectOf(fact)` is undefined: a `fact2` descriptor
carries no subject, and the retained payload's subject-role field is **never
published**. The registry publishes `subjectKind` (what the subject *is*) and, for
`file` only, `coverageTotality.pathField: "path"` — introduced for the totality law,
not for evaluation. `declares` carries both `container` and `declared` as
`SubjectIdV1`; nothing says which is the subject.

### G4 — `FieldFilter` projection over heterogeneous payloads is undefined (MUST)

The eight filter fields confront thirteen closed payload shapes
(`relation-payload-schemas.v2.json#/$defs/*PayloadV1`). Status per field:

| Filter field | Retained support | Status |
|---|---|---|
| `resolution` | `fact.resolution` | defined |
| `confidenceMillionths` | `fact.confidenceMillionths` | defined |
| `subject` | payload subject-role field | **no published projection** (G3) |
| `target` | rung-dependent (`calleeText` vs `resolvedCallee`, `specifier` vs `resolvedTarget`, `name` vs `resolvedBinding`, `typeText` vs `checkedType`); **absent** for `file`, `package`, `clones` | undefined + ambiguous |
| `universe` | `fact.sourceUniverse` **or** `targetUniverse`; and type mismatch per G1 | undefined |
| `subjectKind` | constant per relation via the registry; needs the G2 mapping | undefined |
| `targetKind` | **nothing.** No fact or payload field declares a target kind, and the DSL enum adds `external` | **unsupportable by any retained field** |
| `observability` | only `RuntimeSubject.observability`; no native fact carries it | undefined on native atoms |

Also unpublished: whether multiple filters conjoin; whether a filter on a field the
rung *forbids* (e.g. `resolvedCallee` at `syntactic-callee-name`) is **false** or
**indeterminate** — which flips every `none` outcome; and whether `glob`/`prefix`
on a non-path `SubjectIdV1` is a match, a non-match, or a refusal.

## 4. Adjacent obligations that the narrow mapping does not reach

I will not claim the four gaps above close full replay. These remain open:

- **G5 — imported-evidence atoms cannot be witnessed.** `predicate-witness` is
  closed with `matchingFactIds` (`fact2` pattern only) and no import member; the
  evidence registry states these relations "mint no fact2". §4's "witness facts
  must be exactly those selected" and "counts count distinct selected fact IDs"
  are therefore **unsatisfiable** for an `exists`/`count-at-most` over
  `runtime-observation`. This needs a typed change.
- **G6 — disabled rules.** `enabled` exists only in `PolicyDocumentV1`; the
  projection law puts *every* rule in `RuleProgramV1`. Skip-entirely and
  evaluate-then-suppress produce different `predicateProofs` sets and different
  `proof2`. Unpublished.
- **G7 — completeness scope selection.** §4 grounds `all-covered` in "the requested
  universe/rung", but an atom has no universe, and the atom's rung is a **lower
  bound** while a scope carries **one** rung. Complete-at-exactly-`k` vs
  complete-at-every-rung-`≥ k` give different `none` results on any two-rung
  relation. Unpublished.
- **G8 — finding identity.** `finding-fingerprint.subjectKey` requires
  `{language, kind, logicalPath, qualifiedName, discriminator}`. From a retained
  subject string only `logicalPath` is derivable, and only for `source-path`
  subjects. §3 179–183 assigns these to a native subject adapter whose token
  projection native-evidence.md 3400–3401 openly calls "a named native
  qualification task". **No retained record holds adapter output and no
  `ProofInputRef` domain can name one**, so §4's "recomputes finding fingerprints"
  is currently not discharge-able from the closure. Separately: `Rule.messageCode`
  is optional but `finding.messageCode` is required, and the DSL has no parameter
  construct while `finding-parameters.parameters` is required.
- **G9 — verdict and waiver join.** `gateSeverityAtLeast` has **no prose anywhere
  in the contract set** — its interaction with `Rule.gate` is unstated. Whether a
  waived finding stays in `proof.findingIds` is unstated (it changes `proof2`).
  `common#/$defs/Verdict` is four-valued (`pass|advisory|fail|indeterminate`) while
  `proof-bundle.verdict` and `policy-derivation.verdict` are three-valued; the
  relationship is unstated. And a waiver targeting `(ruleId, subjectPath)` is typed
  `LogicalPath` while `finding.subjectId` is opaque `Text`, so symbol findings have
  no path-form waiver.

## 5. Correction proposal

Design intent throughout: **use already-retained data; refuse rather than fabricate;
keep the zero-config path (globs, filters, `evidenceUse` are all optional).**

**C1 (law, no schema change) — universe.** `subjectEnumeration.universe` and
`FieldFilter{field:"universe"}.value` are **domain-set member names** from
`identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/native-semantic-universe`;
an unlisted name refuses at policy admission (`POLICY.UNKNOWN_UNIVERSE`). The name
denotes `U(rule)` = every Plan-bound universe H-identity of that domain. A fact
matches on `sourceUniverse ∈ U(rule)`. **Unresolved choice, my recommendation:**
union subjects across `U` by byte equality rather than evaluating per universe,
because `predicateProofs[].subjectId` is bare `Text` and cannot carry a universe
discriminator without inventing an encoding that would also propagate into
waivers and fingerprints. State the consequence explicitly: a two-universe rule
sees the coarser union extent, which is exactly what native-evidence.md 447–455
already says is the only answerable question.

**C2 (registry rows + law; one enum narrowing) — subjects.** Add to each
`x-opensip-relation-registry.relations[*]` a `policySubjectKind`
(`source-path→file`, `package-name→package`, `symbol→symbol`) and a `subjectField`
(`calls→caller`, `control-flow→from`, `declares→container`, `imports→importer`,
`literal→owner`, `reachability→origin`, `references→referrer`, `types→subject`,
`unresolved-edge→referrer`, `file→path`, `package→packageName`, `vcs-change→path`,
`clones→` the single anchor's `path`, which `anchorLaw.body-identity` already fixes
at cardinality 1). Subject set = union of `subjects` over every subject-scope
reachable from the Plan-selected views whose `sourceUniverse ∈ U(rule)` and whose
relation's `policySubjectKind` equals `subjectEnumeration.subjectKind`, then
include/exclude. **Withdraw `export`** from the `subjectKind` enum (typed change);
it turns today's silent vacuous pass into `POLICY.UNKNOWN_SUBJECT_KIND` at
admission. Globs are admissible **only** for `subjectKind: file`; on `symbol` or
`package` a present `include`/`exclude` refuses (`POLICY.SUBJECT_GLOB_NOT_APPLICABLE`)
rather than being matched against an opaque identity. An atom whose relation's
`policySubjectKind` differs from the rule's refuses at admission
(`POLICY.ATOM_SUBJECT_KIND_MISMATCH`) — same shape as the existing cross-relation
rung refusal, and it removes the fabricated universal negative of G2.

**C3 (law, no schema change) — subject binding.** Every atom is **implicitly
restricted to the current enumerated subject**: fact `f` is in the match set for
subject `s` iff `payload(f)[subjectField(relation(f))] == s`, *and* relation, rung
(`≥`), universe and all filters hold. `FieldFilter{field:"subject"}` is an
additional constraint on that same projected value, never the binding.

**C4 (registry rows + law; one enum narrowing) — filters.** Add
`targetFieldByRung` per relation, defined as **exactly the field that rung's
existing `rungs.required` entry names** (`calls`: `syntactic-callee-name→calleeText`,
`resolved-callee→resolvedCallee`; `imports`: `→specifier`/`→resolvedTarget`;
`references`: `→name`/`→resolvedBinding`; `types`: `→typeText`/`→checkedType`;
single-rung: `declares→declared`, `control-flow→to`, `reachability→reachable`,
`unresolved-edge→targetModule`; `file`/`package`/`vcs-change`/`literal`/`clones` →
`null`). Deriving it from the published `rungs` table invents nothing. A `target`
filter on a `null`-target relation refuses at admission. `universe` binds
`fact.sourceUniverse`. `subjectKind` resolves through `policySubjectKind` (decidable,
constant per relation). **Withdraw `targetKind`** (typed change) — no retained field
supports it. `observability` is admissible only on an atom over `runtime-observation`.
Filters **conjoin** in admitted order. A field the rung forbids projects **absent →
filter FALSE**, never indeterminate, because `rungs.forbidden` makes the absence a
published certainty and leaves closed-world reasoning owned by Coverage.
`glob`/`prefix` require a path-shaped projected value and refuse on `SubjectIdV1`.

**C5 (typed change, unavoidable) — import atoms.** Refuse `none`, `count-at-most`
and `all-covered` over evidence relations at policy admission: §4 already holds that
"runtime unhit observations never supply universal static completeness", so those
three could never be true and today are undecidable rather than refused. For the
surviving `exists`, add a required `matchingImportSubjects` member to
`predicate-witness` — items `{importId (import2), subjectIndex}`, `x-opensip-order:
canonical-set` — since `RuntimePayloadV1.subjects` is an ordered array with a
declared sort, an index is a stable deterministic address into retained bytes and
needs no new identity domain. Bind an import atom's subject to
`RuntimeSubject.path`/`HistorySubject.path`, admissible only under
`subjectKind: file`; do **not** map `RuntimeSubject.symbol` to `SubjectIdV1`.
**Cost:** `predicate-witness` schemaVersion 2→3 changes every witness digest and
therefore every `proof2`/`seal2`/`run2`. §3 already requires exactly this
("Schema/domain changes require a new identifier major and reviewed migration").

**C6 (law) — disabled rules.** `enabled=false` ⇒ no subject enumerated, no
predicate proof, no finding; the rule **stays** in `RuleProgramV1` (the projection
law forbids dropping it) and stays ladder-checked. Toggling a rule must not change
`ruleProgramDigest`.

**C7 (law) — completeness.** An atom over relation `R` at rung `k` for subject `s`
is COMPLETE iff, for **every** rung of `R`'s ladder with index `≥ k`, some
subject-scope reachable from this predicate's `inputRefs` carries that rung, a
universe in `U(rule)`, contains `s`, and its Coverage entry has
`coverage == complete` **and** the §4-required resolution/closed-world
completeness. An empty set is INDETERMINATE, never complete. Those scopes are
exactly `predicateProofs[].scopeIds`; those Coverage ids exactly
`predicate-witness.coverageIds` — so the whole computation replays from retained
bytes. "Every rung `≥ k`" rather than "exactly `k`" is required because the match
set spans those rungs; the weaker reading would assert a negative over unexamined
rungs.

**C8 (law + one typed record) — finding identity.** Law part: an omitted
`Rule.messageCode` yields `messageCode = ruleId`; DSL v1 emits
`finding-parameters.parameters = {}`, fixing `parameterDigest`; a
`(ruleId, subjectPath)` waiver matches only `source-path` subjects, and a symbol
finding is waivable only by fingerprint. Typed part: register a `subject-descriptor`
record (`{schemaVersion:2, scopeId, subject, language, kind, logicalPath,
qualifiedName, signatureTokens[]}`) produced by the same enumerator closure that
mints `subject-scope`, plus a `subject-descriptor` member on `ProofInputRef.domain`.
Without it §4's fingerprint-replay obligation cannot be discharged from the
closure at all. I flag this as the item most likely to belong to the native
contract's already-named token-projection task rather than to this correction; a
correction author should confirm ownership before writing it.

**C9 (law) — verdict.** A finding is *gating* iff `rule.gate` **and**
`rank(rule.severity) ≥ rank(policy.gateSeverityAtLeast)` over `note<warning<error`.
`fail` if any gating finding is unwaived; else `indeterminate` if any gating rule
carried an indeterminate required predicate; else `pass`. Waived findings **remain**
in `proof.findingIds` (they are evidence) and are excluded only from gating.
`proof-bundle`/`evaluation-seal`/`policy-derivation` verdicts stay three-valued;
`common#/$defs/Verdict.advisory` is a **surface** projection of a `pass` carrying
unwaived non-gating findings and is never sealed. State this, because two published
enums disagree today.

**Editorial MUST.** identity-and-evidence.md 1330–1332 says "The declarative rule
program defines the exact subject enumeration…". `RuleProgramV1` contains no
`subjectEnumeration`, `severity`, `gate`, `evidenceUse` or `messageCode`. The
sentence must be corrected to name `PolicyDocumentV1` (already a legal
`ProofInputRef.domain`) as the source of those, or an implementer will look for
them in the wrong artifact.

## 6. Compatibility and test consequences

C1, C3, C4 (projection), C6, C7, C9 are **pure law**: no schema byte changes, no
identity changes, and they make previously-underdetermined behaviour determined.
C2 and C4's two enum narrowings (`export`, `targetKind`) and C5's admission
refusals reject policy documents that are valid today but were already vacuous or
undecidable; each needs a public detail code added to
`public-detail-registry.v1.json`. C5's witness change is the only identity-breaking
item and requires the reviewed migration §3 already mandates. Test consequences:
`workflow-cases.v1.json` needs per-relation projection cases (both rungs of each
two-rung relation), a two-universe enumeration case, a symbol-subject glob refusal,
an `export`/`targetKind` refusal, a disabled-rule proof-shape case, and a
`≥ k` completeness case; `foundation/check-identity.py` needs witness cases for
`matchingImportSubjects`.

## 7. Implementation evidence (non-normative) and limits

`workflows/workflows_model.v1.py` — the fixture verifier, **not** a published
projection — corroborates rather than supplies these laws. Its `eval_pred` binds
`f['subject'] == subject` (C3's shape) and its `_filter_ok` treats a missing field
as false (C4's shape), but both work only because `policy-test.schema.json#/$defs/FactRecordCandidate`
is a **flat test-input record** carrying literal `subject`/`target`/`universe`/
`subjectKind`/`targetKind`/`observability` fields that no retained `fact2` has. Its
`evaluate()` never reads `subjectEnumeration.universe` or `subjectKind` at all —
so even the reference implementation does not exercise the two fields G1 and G2
concern. It emits an `advisory` verdict the seal cannot hold. None of this is
normative authority for a production evaluator.

**Limits.** I read the sections named in `assessment.json#readScope`, not the whole
258 KB native-evidence contract, `IMPLEMENTATION-FREEZE.md`, or
`IMPLEMENTER-BLUEPRINT.md`; a binding law for G1 or G4 could in principle sit in an
unread region, though I searched every occurrence of `subjectEnumeration`,
`gateSeverityAtLeast` and the filter vocabulary across the non-review tree and
found none. Unresolved design choices I did **not** settle: per-universe vs union
enumeration (C1), and ownership of the subject-descriptor record (C8).
