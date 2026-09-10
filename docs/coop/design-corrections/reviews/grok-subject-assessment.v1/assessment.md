I'll start from the two Codex coauthor assessments and the frozen v21 contracts, then settle a concrete subject-identity proposal without treating Claude's draft as authority.Codex’s two assessments are in; next I’ll read Claude’s incomplete draft and the frozen v21 identity/evidence contracts they point at.Claude’s v2 draft is incomplete and cites undelivered proposal files; I’ll pull the identity/evidence and native clauses next and treat those as the authority.The Claude draft ends without a delivered proposal; I’ll pin frozen v21 and read the identity, policy, and native subject clauses next.Manifest SHA matches frozen v21. Next I’ll read the identity, policy, and native clauses that actually define subject enumeration.Policy kinds and fingerprint keys are now in view; I’ll pull Plan-bound universe identity, closed-world completeness, and D9 deficiency next.# Subject identity and enumeration — bounded coauthor assessment

**Standing.** Actual Grok, bounded coauthor assessment for Codex. Not a blind review, not Claude agreement, not source assent, not implementation, not evaluator-contract completion. Normative pin: frozen21 at `/tmp/opensip-design-corrections/candidate-subject.v21`, manifest SHA-256 `360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1` (recomputed match). Claude `proposal.md` / `proposal.json` / `validation-transcript.txt` were never delivered; v2 examples are treated as conceptual record *shapes*, not admitted Run inputs.

**Verdict.** A coherent subject-identity design is feasible from frozen21 without inventing a second evaluation language. Bare-string union is **not** sufficient. Evaluation must use a **universe-qualified evaluation subject**. Exported-subject functionality is preservable with a small retained inventory record and existing Kleene/D9 carriers. Unknown export status is a routine evidence-deficiency choice, not a product-owner question. This does **not** settle G3–G9, disabled-rule proofs, filter projection, or verdict/waiver composition.

## Critique of Claude’s draft

v1 C1 recommended union because `predicateProofs[].subjectId` is bare text. v2 then treated union as **forced** by `x-opensip-order: "predicate"` uniqueness (`ruleId,subjectId,predicateId`). Codex v2 is right: uniqueness forbids *duplicate bare tuples*; it does not make union the only lawful redesign. A qualified key, or a proof field that includes universe, also yields unique tuples.

v2 C1 (“derive `U(rule)` from retained scopes; Plan carries no universe ids”) is a half-truth. `plan` has no universe-H array, but identity §3 already Plan-binds universes: retained universe frames must join `plan.nativeContextDigests` via `nativeContextId`, and `subject-scope.enumeratorClosure` must be a `provider` member of `plan.semanticClosures`. Deriving `U(rule)` only from scopes that happen to exist lets a missing examination silently shrink the selector.

v1 C2 withdrawal of `export` and non-path globs is rejected (Codex v1). v2 restored them via an undelivered “subject-descriptor,” then left unknown export as a user question and offered Plan-construction refusal as a live alternative. Plan construction does not yet have native export observations; refusal there would block other rules. The remaining v2 fork (“indeterminate is silently non-gating”) confuses *advisory non-gating* with *gating success*. Identity §4 and workflows §5 already say an indeterminate **gating** rule is a typed deficiency; aggregate fail ≻ indeterminate ≻ pass.

v2’s identity table (descriptor + required `predicate-witness` member, `predicate-witness` 2→3, “policy schema unchanged”) cannot be assessed as a completed proposal: the files do not exist. Adding a required witness member would churn every witness digest for a record the witness does not need to own.

Claude’s reading of `subjectKindLaw` / native-evidence §1.2 (symbol paths only answerable at coarser extent) is correct **as a host-rederivation ban**. It is not a licence to union two TypeScript configurations’ subject strings, nor to skip retained attribution.

## Exact selector citations

| Portable field | Frozen spelling | Bound identities |
|---|---|---|
| `Rule.subjectEnumeration.universe` | `CanonicalIdentifier` (`policy-document.schema.json#/$defs/Rule`) | Closed membership: the three keys of `identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/native-semantic-universe` (`native.semantic-universe.typescript.v2` / `.rust.v2` / `.syntax.v2`). Unlisted name: policy admission refusal (`CONFIG.INVALID`), not evaluation. |
| `U(rule)` | not a Plan field | Every retained universe **H** of that domain whose `nativeContextId` is `sha256:` + a member of `plan.nativeContextDigests`, admitted by the domain’s `bind_*_universe` entry point (identity §3; native §11). |
| Examined partition | `subject-scope` / `scope2` | `{snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}`; `subjects` are native spellings, unique, `canonical-set`. Coverage partition key is the same universe pair (`coveragePartitionLaw`). Totality for `file@enumerated` is discharged only by a fact of **that** universe (`coverageTotality.matchOn`). |
| Policy kinds | `file \| symbol \| export \| package` | Registry kinds are `source-path \| symbol \| package-name` (`subjectKindLaw`). `export` is a **filter** on symbol rows, not a fourteenth relation. |
| Globs / path waivers | `GlobPattern` over `LogicalPath`; waiver `(ruleId, subjectPath)` | Compare **attributed** `LogicalPath`, never `SubjectIdV1` text. |
| Finding correspondence | `finding-fingerprint.subjectKey` | `{language, kind, logicalPath, qualifiedName, discriminator}`; discriminator = raw SHA-256 of canonical JSON of declaration-signature tokens in grammar order (identity §3; native §14). |
| Proof identity | `predicateProofs` order `predicate` | Unique `ruleId,subjectId,predicateId`. Completeness is native examined partition **and** resolution **and** closed-world (identity §4; native §4.1/§4.5). |
| Truth / deficiency | Kleene 3-value; `predicateProofs[].value` | Gating indeterminate → typed deficiency; `D9Deficiency.verdict-indeterminate` / `VERDICT.INDETERMINATE`. Schema/identity faults are operational, not a fourth truth value. Missing promised bytes are retention loss (`HOST.IO_FAILURE`), not a false predicate. |

**Choice.** Do **not** union bare native strings across `U(rule)`. Mint a qualified **evaluation subject**:

`H("evaluation-subject", {schemaVersion: 2, universe: <64-hex>, nativeSubjectId})`

Carry the 64-hex suffix in `predicateProofs.subjectId` and `finding.subjectId`. Keep `subject-scope.subjects` as today’s native spelling. Do **not** put universe H into `finding-fingerprint.subjectKey` (fingerprint is logical correspondence; universe H churns with resolved inputs). Distinguishability **in evidence** is the evaluation id plus `scopeIds` / universe-keyed scopes. Consequence: a fingerprint-targeted waiver can hit the same logical subject in every selected universe; a path waiver hits each matching attributed path independently. That is correspondence vs evaluation, not a defect.

Union would let U2’s fact make `exists` true for a U1-only reading and would let one complete Coverage discharge another’s absence, contradicting `coverageTotality.matchLaw` and identity §4. Concatenating `universe+"/"+nativeSubjectId` into the existing string is also rejected: `SubjectIdV1` is already `maxLength` 4096, so qualification overflows; it would also leak configuration H into waiver/fingerprint strings.

## Minimal retained inventory (acyclic)

New record `EnumeratedSubjectInventoryV2` (new H domain `subject-inventory`, prefix e.g. `subjinv2:`). **Not** inside `subject-scope`, **not** a `scope-descriptor` (that is workspace roots / path prefixes), **not** a raw `ProofInputRef.blob`.

```
{
  schemaVersion: 2,
  snapshotId,                    // snapshot2:
  universe,                      // 64-hex native-semantic-universe H
  enumeratorClosure,             // closure2: provider ∈ plan.semanticClosures
  rows: [ /* canonical-set by nativeSubjectId */ ]
}
```

Row (minimal):

| Field | Who trusts it | Join |
|---|---|---|
| `nativeSubjectId` | spelling = `subject-scope.subjects` member | unique per inventory |
| `kind` | `file \| symbol \| package` | maps `source-path → file`, `package-name → package` |
| `language` | host | must equal the universe domain’s `language` |
| `path` | **host-checkable** `LogicalPath` | must be a snapshot inventory path. File: equals native id. Package: manifest path. Symbol: enumerator attribution, **not** parsed from the id |
| `exported` | **trusted native** tri-state `true \| false \| unknown` | required iff `kind=symbol`; forbidden otherwise |
| `qualifiedName` | trusted native | file: path; package: package name; symbol: binding name |
| `signatureTokens` | trusted native, grammar order, repeats kept | may be `[]`; discriminator = SHA-256(C(tokens)) as §3 |

Forbidden on the record: `scopeId`, Coverage, views, expected predicate values, findings, raw unbounded blobs, second copies of fact payloads.

**Acyclic construction** (extends native §4.1a): closures → native context → universe H → **inventory** → `scope2` (subjects ⊂ inventory native ids of the relation’s kind) → Coverage → view → evaluation. Inventory names snapshot, universe, enumerator; it does not name scope/coverage/view/proof/Run. Scopes do not name inventory. Run closure: exactly one inventory per `(snapshotId, universe, enumeratorClosure)`; every `subject-scope` of that triple has a row for every subject; `ProofInputRef.domain` gains `subject-inventory` (typed `byDomain` row, canonical-record). Fingerprint recomputation reads this input, not an unbound blob and not a producer flag.

## Enumeration algorithm

For enabled rule `R` with `subjectEnumeration = {universe: D, subjectKind: K, include?, exclude?}`:

1. Admit `D` as a native-semantic-universe domain key; else `CONFIG.INVALID`.
2. `U(R)` = Plan-bound admitted universe H identities of domain `D`. If `U(R)` is empty: gating → whole-rule indeterminate with disclosure; advisory → disclose, emit no subjects. Do **not** treat as a successful empty pass.
3. Load inventories for those universes. Missing inventory bytes: retention/operational failure, not `false`.
4. Kind-select rows: `file`/`package`/`symbol` as above; `export` ≡ `kind=symbol`.
5. Path filter: globs apply only to `row.path`. Absent `include`/`exclude`: all kind-selected rows pass the path filter. Never glob `nativeSubjectId`.
6. Export filter (only `K=export`): keep `exported=true`. `unknown` is unresolved (table below). `false` is a known non-member.
7. Each surviving row becomes one evaluation subject `H(universe, nativeSubjectId)`. Same native string in U1 and U2 → two subjects, two proofs.
8. Candidates come from **inventory**, not from facts and not from the predicate tree. A subject with no matching fact is a lawful candidate (needed for `none` / absent-fact). `file@enumerated` totality remains a Coverage/view admission law, not an enumerator substitute.
9. Atom-to-current-subject binding, `subjectField` projection, and atom/kind mismatch (`file` rule + `calls` atom) are **G3/G4**. Until those land, this algorithm must not be read as licensing a fabricated universal negative.

## Decision table

| Case | Classification | Gating (`gate: true`) | Advisory (`gate: false`) |
|---|---|---|---|
| Unknown selector token | invalid config | Plan/policy admission `CONFIG.INVALID` | same |
| Valid selector, `U(R)=∅` | well-formed unavailable | rule indeterminate; `verdict-indeterminate` | disclose; rule does not gate |
| Inventory bytes promised but missing/corrupt | missing retained bytes | operational (`HOST.IO_FAILURE`); not a predicate value | same |
| Scope subject with no row; two rows disagree on any field; `exported` not in tri-state; `path` not `LogicalPath`; `path` not in snapshot inventory; `language` ≠ universe domain | invalid metadata | Run admission refusal (provider-protocol / host-invariant). Not Kleene | same |
| `K=export`, every kind/path-selected symbol has `exported` ∈ {true,false}, none unknown | determinate | enumerate `true` only; zero trues is a real empty set | same |
| `K=export`, ≥1 otherwise-selected symbol has `exported=unknown` (including **zero known-true** + unresolved) | well-formed unavailable | **indeterminate, not pass**; disclose universe, unknown count, selector `export` | disclose; evaluate only known-`true` for advisory findings; does not mint gating deficiency |
| `include`/`exclude` present, symbol/package `path` missing | invalid here (`path` required) | refusal | refusal |
| Globs on symbols/packages with valid attributed path | host match on `path` | ordinary include/exclude | same |
| Signature-less row (`signatureTokens=[]`) | determinate discriminator | SHA-256 of canonical `[]`; identity is kind+path+qualifiedName+empty tokens | same |
| Two rows, same language/kind/path/qualifiedName/tokens in one collision class | ambiguous key | refuse correspondence (existing §3); no encounter-order suffix | same |
| Same path, two Plan-bound universes of `D` | two evaluation subjects | separate proofs/completeness; path waiver applies per subject | same |
| `K=export` on file/package-only inventories (no symbol rows) | determinate empty **if** no unknown symbols exist | empty export set; `exists` false only under complete Coverage | no findings |
| ClosedWorld `exportsClosed=unknown` with per-row `exported` still boolean | do not override rows | per-row tri-state wins for enumeration; closed-world remains native sufficiency for universal-negatives (G7/native §4.6), not this filter | same |

Indeterminate gating is not silent success. Do not refuse the Plan because export status is unknown.

## Schema / identifier-major consequences

- **New** `subject-inventory` and `evaluation-subject` H domains; `ProofInputRef.domain` / `byDomain` gain `subject-inventory`. Identity-schema document bytes change. Do **not** add a required `predicate-witness` member.
- `predicateProofs.subjectId` / `finding.subjectId` **meaning** changes from native spelling to evaluation-H suffix. Shape can stay a 1–4096 string. Strict identifier-major discipline: `proof-bundle` and `finding` 2→3. This correction series has also mutated v2 in place; the identity owner must pick one and not pretend the field still *is* `SubjectIdV1` or `LogicalPath`.
- Fingerprint schema can stay v2 if universe H is kept out. Path-form waivers then join `row.path`, which is the G8 gap this record actually fills.
- `policy-document.schema.json`: **keep** `export` and globs. No enum narrowing. Universe closed by admission against `domainSets` keys (do not duplicate that set as a second schema enum).
- Relation payload document need not grow export fields; export is inventory, not `DeclaresPayloadV1`. Avoiding a relation-document edit avoids the `fact.payloadSchemaDigest` world-change Claude correctly described for *other* G4 rows — those rows are not this task.
- Historical frozen subjects are not migrated. No product Runs exist to convert. Future admission only.
- Exact annotation/Ref registry diffs remain unassessed until a real schema patch exists. This is not that patch.

## Three conceptual examples (not executed)

**E1 — two TypeScript configurations, same native id.** Plan binds `U1` and `U2`, both `native.semantic-universe.typescript.v2`. Both inventories contain `ts-symbol:src/a.ts#f`. Only `U2` has a matching `references` fact. Rule selector `native.semantic-universe.typescript.v2`, `subjectKind: symbol`, gating `exists`. Qualified evaluation: two subjects; U1 complete-absent → `false`; U2 match → `true`; two proofs; distinct `subjectId`s so `predicate` uniqueness holds. Union: one subject, `exists` true from U2, U1 completeness never asked. Selector `native.semantic-universe.syntax.v2` would not see these universes.

**E2 — export rule, zero known exported, unresolved remainder.** One TS universe, 10 symbols, all `exported=unknown`, globs match all. Gating `subjectKind: export`. Outcome: predicate/rule **indeterminate**, deficiency `verdict-indeterminate`, disclosure of 10 unresolved / 0 known-true. Not pass, not Plan refusal. Same data, `gate: false`: no findings, same disclosure, advisory rule does not force Run indeterminate by itself (G9 projection still open).

**E3 — glob vs conflict.** Symbol `ts-symbol:src/a.ts#f` attributed to `src/a.ts`; include `src/**` includes it. A second row for the same native id with `exported` differing: inventory **refused**, not indeterminate. A well-formed inventory with no row for a scope subject: same refusal. Missing inventory blob listed in `evaluationInputRefs`: retention loss, not `none=true`.

## Dependencies on other evaluator work

This proposal **needs** G3 (current-subject binding / `subjectField`) before anyone can claim `none` is sound over these candidates. It **needs** G4 (`targetKind` / filter projection) for atom/kind agreement. G7 (per-subject Coverage aggregation, no cross-universe completeness substitution) must use the same qualified subject and the same `U(rule)`. G8’s remaining pieces — optional `messageCode`, `finding-parameters`, adapter qualification of **token projection** (native §14 still names that a qualification task) — are not discharged by retaining tokens; we only retain what reconstruction hashes. G5 imported witnesses, G6 disabled rules, G9 `gateSeverityAtLeast` / 3- vs 4-valued verdict / whether waived findings stay in `findingIds` are untouched. `FieldFilter.universe` is still a CanonicalIdentifier vs 64-hex mismatch; do not silently treat it as settled by the selector law above.

**Assumptions.** `path` can be required on every inventory row (symbol attribution is trusted but must name a snapshot path). Fingerprint `kind` for export-selected subjects stays `symbol`. One inventory per `(snapshot, universe, enumerator)`. Token projection quality is a native qualification, not a host parse.

**Unsettled (honest).** Whether identity-owner bumps `proof-bundle`/`finding` majors or redefines subjectId in-place; whether a later portable selector finer than domain (one of two tsconfigs) is wanted — current `CanonicalIdentifier` cannot name a 64-hex H, and pinning H would be non-portable; whether fingerprint-targeted waivers *should* span configurations (I keep that, and would not hide it). No source assent. No complete replay. Stop.
