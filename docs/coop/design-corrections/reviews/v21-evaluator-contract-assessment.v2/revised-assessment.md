# v21 evaluator contract — revised assessment (v2)

**Standing.** Bounded correction-*proposal* refinement. No source edit, no product
implementation, no acceptance. Source21 read-only. Blind9 not read or contacted.
v1 preserved verbatim at `../v21-evaluator-contract-assessment.v1`.

**New evidence in v2.** Every example record below was **executed** against the
frozen v21 schemas using the frozen `foundation/canonical.py` `ExactValidator`
(so `x-opensip-order`, exact `const`/`enum` and the typed-integer rule apply as the
contract requires). Script and transcript: `validate-examples.py`,
`validation-transcript.txt`. Nothing below is called schema-admitted unless it
actually validated.

**Newly read to settle these points:** `imported-evidence.schema.json#/x-opensip-imported-requirement-law`
and `#/$defs/{ImportWrapperV2,ImportObservationV1,ImportScopeDescriptor,SourceMappingV1,StalenessRule,PayloadBinding}`;
`native-evidence.schemas.v2.json#/$defs/{ResolutionCompletenessV2,ResolutionCompletenessState,ClosedWorldV2,ExaminedUniverseV1,UnresolvedEdgeKindV1,DeficiencyV2}`;
`identity-schemas.v2.json#/$defs/{plan,semantic-evidence}` and `#/x-opensip-payload-registry`;
`relation-payload-schemas.v2.json#/$defs/{ControlFlow,Literal,Reachability,VcsChange,Types,Package,UnresolvedEdge}PayloadV1`;
`common.schema.json#/$defs/{D9Deficiency,ImportedRequirementDeficiency,NativeSufficiencyDeficiency}`;
`invocation-record.schema.json` `Verdict` usage sites; and `IMPLEMENTER-BLUEPRINT.md` /
`IMPLEMENTATION-FREEZE.md` / `COORDINATOR-DECISIONS.md` / `current-source-map.proposed.md`
searched for a `gateSeverityAtLeast` or advisory-verdict selector (**0 occurrences in all four**).

---

## 1. What was wrong in v1

**W1 — C6 identity claim was factually wrong.** I wrote "toggling a rule must not
change `ruleProgramDigest`". Toggling `enabled` changes `PolicyDocumentV1` canonical
bytes → `policyDigest` → `plan.policyDigest` → **PlanId**, and
`RuleProgramV1.policyDigest` → `ruleProgramDigest` → `program-predicate.ruleProgramDigest`
→ every `witnessDigest` → `proof2` → `seal2` → `run2`. Withdrawn. What is actually
true is narrower and still worth stating: the `rules` **array** is unchanged by the
toggle, so the projection law is untouched, and a different policy legitimately being
a different Plan is correct behaviour, not a defect.

**W2 — "C5 is the only identity-breaking item" was wrong.** `fact.payloadSchemaDigest`
is the raw SHA-256 of the *exact full bytes* of `relation-payload-schemas.v2.json`.
Adding `subjectField`/`targetProjection` rows to that document therefore changes
**every `fact2` value in the world**, transitively `view2`, every witness, `proof2`,
`evidence2`, `seal2`, `run2`. C8's typed additions are identity-affecting too. §2
below gives the exact table. I conflated "shape/algorithm unchanged" with "values
unchanged"; they are different claims and I now separate them everywhere.

**W3 — G3's 100-file example was invalid.** `file@enumerated` carries the
`coverageTotality` row, so under `coverage: complete` every inventoried subject
*must* have a fact (`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`). With all 100 facts
present both readings give 100 true findings. Replaced with a validated `references`
example (§3) — a relation with **no** `coverageTotality` row.

**W4 — G1's example was invalid, and the choice is now settled.** `U_ts` and `U_syn`
are different **domain classes**, so they discriminate nothing about a single-domain
selector. Replaced with two universes of the *same* domain. More importantly, the
open v1 choice (union vs per-universe) is **settled by the published order key**:
`proof-bundle.predicateProofs` carries `x-opensip-order: "predicate"`, whose
vocabulary requires **strict ascending, unique** `ruleId,subjectId,predicateId`
tuples. Per-universe evaluation would emit two proofs with an identical tuple.
Probe result — `REFUSED: array order predicate: strict unique order required`.
Union is not a preference; the alternative is schema-refused.

**W5 — C5 was too broad and is withdrawn.** "None/count-at-most/all-covered could
never be true over imports" is wrong. `ImportWrapperV2` carries `completeness` and
`omissions`; `ImportObservationV1` carries `window`, `population` and
`selection.completenessEstablished`; `HistoryPayloadV1.collectionScope` exists,
per the law, "precisely so that an absent path can be distinguished from an
unexamined one"; and `x-opensip-imported-requirement-law` already defines
`import-absent-for-requirement` as "in scope and consumable, but no row reaches
that target". Bounded observational completeness **is** established by retained
fields. Codex is right: I removed functionality the contract already supports. All
four operators are preserved in the revised proposal, with the no-static-negative
boundary stated as a *labelling* law rather than by deleting operators.

**W6 — C2/C4's narrowing was schema-work-driven, not intent-driven.** Withdrawing
`export`, `targetKind` and all symbol/package globs saved edits at the cost of
promised product semantics. Withdrawn. The subject-descriptor record that G8
requires **anyway** re-founds all three, and `targetKind` turns out to be
genuinely supported for six of thirteen relations plus a per-fact rule for
`unresolved-edge` (whose `targetScope ∈ {external, module, universe, unknown}` is a
retained target-role field I missed in v1). Prefer the smallest **complete** design.

**W7 — "No `ProofInputRef` domain can name adapter output" was too absolute.**
`ProofInputRef.domain` admits `blob`, and §3 permits raw blob citations that are
explicit blob inputs. The real gap is narrower and still real: a bare blob is
**untyped and producer-unbound** — no schema admission, no closure join, no
snapshot join — so it cannot discharge §4's fingerprint recomputation.

**W8 — G9's "no published sentence relates the two Verdict enums" was overstated.**
The *usage* is published: `common#/$defs/Verdict` (4-valued) is referenced only by
`invocation-record.schema.json` (the reported step result) and `policy-test.schema.json`;
`proof-bundle`, `evaluation-seal` and `policy-derivation` carry their own 3-valued
enum. That the surface and the seal are different types is therefore established.
What is missing is only the **projection rule**. `gateSeverityAtLeast` genuinely has
no prose anywhere — re-verified at 0 occurrences across blueprint, freeze,
coordinator decisions and source map.

**W9 — no new deficiency vocabulary is needed.** `common#/$defs/D9Deficiency`
already carries `verdict-indeterminate`, and the per-predicate carrier is
`predicateProofs[].value = "indeterminate"`. v1 implied a new carrier; withdrawn.

**W10 — the waiver "type mismatch" was overstated.** `S_F = "ts-symbol:src/a.ts#f"`
validates as **both** `SubjectIdV1` and `LogicalPath` (executed). Almost every
`SubjectIdV1` is a syntactically valid `LogicalPath`. The real gap is not the type
but that no law says **which string** the waiver compares against.

**W11 — C7 was unsound.** "Every rung ≥ k has a complete scope" over-constrains a
weaker request to unavailable higher capability, and its existential over universes
would let one universe discharge another's absence. Replaced in §5 of the proposal.

**W12 — C4's "invents nothing" was wrong.** `targetFieldByRung` is a genuine
semantic selection, and five relations carry `rungs: {}` (an empty field-rule
table), so there is nothing mechanical to read. Marked as a design **choice** with a
complete table.

---

## 2. Exact identity and migration standing

Pre-implementation. Historical frozen subjects are immutable and are **not**
migrated; there are no produced current product Runs to silently migrate. What
changes is what *future* admission computes.

| Document / record | Shape or algorithm | Values | Major |
|---|---|---|---|
| `H(D,X)` recipe, `C` encoder, `x-opensip-order` vocabulary | **unchanged** | — | none |
| `relation-payload-schemas.v2.json` (add `subjectField`, `targetProjection`, `policySubjectKind`) | payload `$defs` shapes unchanged; registry gains keys | **document bytes change** → `fact.payloadSchemaDigest` changes → **every `fact2`**, `view2`, witness, `proof2`, `evidence2`, `seal2`, `run2` value changes | relation `schemaVersion` stays 1; `fact` stays 2 |
| `identity-schemas.v2.json` (add `subject-descriptor` `$def`, `ProofInputRef.domain` member, `byDomain` row, `predicate-witness` member) | `predicate-witness` gains a required member | witness digests change | **`predicate-witness` 2 → 3**; all other records stay 2 |
| `imported-evidence.schema.json` (correct `RuntimePayloadV1.subjects` order annotation) | payload record shape unchanged | document bytes change → `wrapper.payloadSchemaDigest` → `importId` | `ImportWrapperV2` stays 2 |
| `policy-document.schema.json` | **no change required** under the revised proposal | policy/waiver/rule-program digests for a given document are unchanged | stays 1 |
| `native-evidence.schemas.v2.json` | **no change required** | unchanged | stays 3 |

Two consequences to state plainly. First, `policy-document.schema.json` needs **no
schema edit at all** once `export` and `targetKind` are re-founded on the descriptor
rather than withdrawn — the v1 proposal's two enum narrowings are gone. Second, the
relation-document edit is the expensive one and I still recommend it, because the
alternative (a second document carrying the projection) creates the independent
second source that `ladderAuthority` exists to forbid. Cost at design time is
regenerating reference fixtures in `check-identity.py`, `native-cases.v2.json`,
`foundation-report.json` and `workflow-cases.v1.json` — not a data migration.

---

## 3. The corrected discriminating examples (all executed)

**G3 — subject binding.** Relation `references` (subjects are `symbol`; ladder
`[syntactic-name-match, resolved-binding]`; **no** `coverageTotality` row).
One TypeScript universe `U1`. Scope `S1` over subjects
`{ts-symbol:src/a.ts#f, ts-symbol:src/a.ts#g}` at `syntactic-name-match`, Coverage
`complete` with `resolutionCompleteness.state = not-applicable` (correct: that rung
is not in the closed five-member resolved set). One fact `F1` whose payload is
`{referrer: "ts-symbol:src/a.ts#f", name: "helper"}`. Rule `r1`: `subjectKind: symbol`,
`emitWhen {exists, references, syntactic-name-match, filters: []}`, `gate: true`,
`severity: error`, `gateSeverityAtLeast: warning`. One waiver `w1` targeting
`(r1, "ts-symbol:src/a.ts#f")`.

- **With implicit subject binding:** `#f` → match `{F1}` → true → one finding,
  waived. `#g` → no match, Coverage complete → **false**. No unwaived gating
  finding → verdict **pass**.
- **Without implicit binding:** both subjects see `{F1}` → both true → two findings,
  one waived, one not → verdict **fail**.

Same admitted inputs, differing per-subject predicate values *and* differing verdict.
All seven records validated.

**G1 — universe binding.** Two universes `U1`, `U2` of the **same** domain
`native.semantic-universe.typescript.v2` (different resolved inputs, e.g. two
`cfgSets`/tsconfig graphs). `S1` under `U1` contains `#f`; `S2` under `U2` contains
`#f`; `F2` under `U2` is the only fact for `#f`. Reading (a-union) → `exists` true.
Reading (b-digest-in-policy naming `U1`) → false. Different `matchingFactIds`,
different `witnessDigest`, different `proof2`, different findings. Both scopes and
both facts validated. Per-universe evaluation is separately **refused** by the
`predicate` order key, so union is the only admissible reading.

---

## 4. Disposition of every v1 item

| Item | Disposition |
|---|---|
| **G1** universe binding | **STANDS**, example corrected; the union/per-universe choice is now **settled** by the `predicate` order key |
| **G2** subject selection / kind / export / globs | **STANDS**; remedy replaced — descriptor re-founds `export` and non-path globs instead of refusing them |
| **G3** current-subject binding | **STANDS**, example corrected and executed |
| **G4** filter projection | **STANDS**; `targetKind` is **partly supportable** (6/13 + per-fact `unresolved-edge`), so v1's "unsupportable" is corrected |
| **G5** import witness | **STANDS**; scope widened — occurrence addressing, duplicate counting and observability/mapping selection all needed, operators preserved |
| **G6** disabled rules | **STANDS** as a gap; v1's identity claim withdrawn (W1) |
| **G7** completeness selection | **STANDS**; v1's rule was unsound (W11) and is replaced |
| **G8** finding identity | **STANDS**; v1 overstated the `ProofInputRef` claim (W7); ownership now **settled** as current-contract, not deferred |
| **G9** verdict / waiver join | **STANDS**; v1 overstated the enum claim (W8) and the waiver type claim (W10) |
| **E1** §4 misnames the artifact | **STANDS**; correction now explicitly preserves the exact projection law |
| **C1** universe | revised: derive `U(rule)` from retained scopes, not from Plan (Plan carries no universe ids); union settled |
| **C2** subjects | **substantially rewritten** (descriptor-founded; no enum narrowing) |
| **C3** subject binding | retained; `subjectField` table completed for all 13 relations |
| **C4** filters | **rewritten**; complete `targetProjection` table, marked as choices; existing `FieldFilter` `allOf` typing preserved verbatim |
| **C5** imports | **withdrawn and replaced**; all four operators preserved |
| **C6** disabled rules | law retained, **identity claim withdrawn** |
| **C7** completeness | **withdrawn and replaced** (§5 of proposal) |
| **C8** finding identity | **expanded**; circularity avoided; ownership settled |
| **C9** verdict | retained with an added omission/deficiency-carrier clause and an explicit "no change to sealed 3-value or D9 precedence" |

Full normative text, tables and records: **`proposal.md`** / **`proposal.json`**.

---

## 5. Remaining decision I cannot settle

One, and it needs product-owner input rather than more reading. Under the revised
C2, `subjectKind: export` selects subjects whose descriptor carries
`exported == true`. If a universe's enumerator populates `exported: null` for every
subject (it did not determine export status), the rule can either be
**INDETERMINATE with disclosure** — honest, zero-config safe, but silently
non-gating for a whole rule class — or **refuse at Plan construction**, which is
loud but blocks otherwise-useful analysis on a capability the universe may never
have. I recommend indeterminate-with-disclosure, reusing
`D9Deficiency.verdict-indeterminate`, but I am flagging it rather than deciding it.

Everything else in the proposal is total over admitted shapes; §7 of `proposal.md`
carries the totality argument branch by branch.
