# Bounded diagnosis — blind19 ACCEPT vs root exact-replay REFUSE on frozen32

**Standing.** Bounded READ-ONLY diagnosis by the actual source-coauthor origin
(`919c766d-…`). **Not** independent design, blind or application acceptance. Reading the
completed blind19 outputs and root diagnostics was explicitly authorized for this task.
**Nothing was sent to or resumed at the blind origin.** Everything written lives in this
runtime; no live, frozen, consumer or earlier-runtime file was touched. No product
implementation, commit or push.

I did **not** presume the validator correct or the consumer incorrect. Two of the four
execution-input differences resolve **against the frozen reference**.

---

## 0. Verification and limits

| Check | Result |
|---|---|
| `candidate-subject.v32.json` | sha `3897e8d1…10bf2` — **matches**, 12 898 files |
| five exact exports | all five recomputed sha **match** `summary.json` |
| every owner file read | hash **equals** its manifest row |
| probes | 17, all exit 0, full stdout/stderr receipts in `probes/receipts/` |

**Limits.** I did not re-run the consumer's engine, did not re-execute the full reference
suites, and did not replay `admit_execution_inputs` end-to-end; I recomputed the specific
derivations at issue by importing the frozen owner module and calling its own functions
(`derived_applicability`, `_matrix_pairs`, `expected_source_census`,
`_summarize_coverage_records`, `derive_outcome`, `_carrier`, `_matrix_cause`) on the exact
export bytes. Root's two traces cover `syntax-code` and `syntax-data` only; I recomputed all
five. I did not assess the charter, requirement coverage, or anything outside the four
execution-input differences and the query/mutation scope.

**One correction to my own working note:** an early stub of mine suggested `clones-fact`
derives `complete`. That was wrong — it fed a hand-made account summary. The frozen owner
*does* implement the expected-subject census, and the real derivation is in §1.4. Root's
preliminary reading of that fault was right and mine was not.

---

## 1. The execution-input disagreement

Three fault keys across five runs reduce to **four** root differences. I recomputed every
owed account in all five runs (`probes/p2-accounts.json`).

### 1.1 F1 — `inapplicable-vcs` account `sourceUniverse` — **missing normative law**

**Observed, all five runs.** Applicability *agrees* (`inapplicable-vcs` both sides). Only the
universe differs: consumer `null`, owner wants the binding U.

```
syntax-code  c1/p0 vcs-change@vcs-reported  consumer=inapplicable-vcs owner=inapplicable-vcs  U null -> 3db6e722
typescript   c2/p0 …                                                                          U null -> cce6fac8
rust         c1/p0 …                                                                          U null -> 848013fe
rust-partial c1/p0 …                                                                          U null -> 79a251c4
syntax-data  c2/p0 …                                                                          U null -> fec7886f
```

**Owner selector.** `execution_inputs_model.v1.py:1140`
— `want_u = None if want_app in ("unavailable-unselected", "unavailable-null-universe") else uni`,
faulting at `:1142`.

**What the published owners say.** Nothing.
* `execution-inputs-contract.v1.md:81` — the `inapplicable-vcs` row of the §5 table governs
  **Envelopes** only: "none; admitted VCS observation `kind=none` is the basis".
* `execution-inputs.schema.v1.json#/$defs/NativeCoverageAccountV1` — `sourceUniverse` is
  **required and nullable**, and the only conditional is `coverageIds: maxItems 0` for the
  four non-`supported-available` applicabilities. **No conditional ties `sourceUniverse` to
  `applicability`.**
* The §5 per-universe attribution clause (lines 88–112) constrains **resolved Coverage**
  envelopes and payloads, and named scopes — not an account that has no Coverage.
* A corpus search for any published tie returned **0 hits**
  (`probes/p3-normative.json`, search `A3`).

The rule exists in exactly two places, both reference implementation:
`execution_inputs_model.v1.py:1140` and `execution_inputs_fixture.v3.py:273`. They agree with
each other, so the reference is self-consistent — but that is agreement between two reference
files, not published law.

**Consumer's rule is self-consistent too** (`probes/p5-outcomes.json`): `sourceUniverse` is
null exactly when the account carries no Coverage — `inapplicable-vcs` and
`unavailable-unselected` null, `supported-available` set. Both readings satisfy the schema and
the contract.

**Classification: genuinely missing normative law.** This difference alone refuses all five
runs. **Correction belongs in the contract and schema**, whichever value root picks.

### 1.2 F2 — UNSUPPORTED-TYPED **and** unselected: which token? — **ambiguous law, with a consumer-side disclosure question**

**Observed, `syntax-code` only.** `unresolved-edge@observed`, syntax-only, matrix
`UNSUPPORTED-TYPED`, enumerator `unselected`, `universe=null`: consumer
`unavailable-unselected`, owner `unsupported-typed`. `want_u` is `None` **both ways**, so only
the token differs.

**Owner selector.** `derived_applicability` (`:406–415`) tests the matrix at `:409` **before**
`uni is None` at `:411` and `en_status == "unselected"` at `:413`.

**Published law is about the *pair*, not the token, and the consumer already satisfies it.**
`native-capability-matrix.v2.json#/capabilityIdLaw/releaseDeclarationRegistry/absenceProjectionAndPrecedence`
says a capability "can be undeclared AND unservable … at the same time", that the syntax
prerequisite "DERIVES `language-tier-unsupported` / `capability-missing` … and refuses anything
else", and that §10 precedence "ranks `language-tier-unsupported` ahead of
`provider-unavailable`, so the more specific one wins". The consumer's binding carries exactly
`language-tier-unsupported` / `capability-missing`, so its derived pair **is** the mandated one
either way. **No published text orders the applicability enum.**

**But there is a separate, real consumer-side question.** Native says an UNSUPPORTED-TYPED cell
"**is** requestable and is answered with `unknown` plus its own named deficiency and cause,
never refused" (`native-evidence.md:830`), that such cells are "answered by disclosure rather
than **omitted**" (`admission-and-qualification.md:79`), and that "the Run closes and the
Coverage carries `unknown` with the deficiency" (`native-evidence.md:3183`). The consumer
instead left the cell **unselected** with `universe=null` and an `unavailable` inventory —
lawful under `enumeration-contract.v1.md:30`, but it is the *omitted* shape rather than the
*answered* one.

**Classification: ambiguous** on the token; **arguably a consumer defect** on choosing
omission over disclosure. Note the consumer is **internally inconsistent**: `syntax-data`
answers its UNSUPPORTED-TYPED cell with Coverage (§1.3) while `syntax-code` omits its
UNSUPPORTED-TYPED cell here.

### 1.3 F3 — UNSUPPORTED-TYPED, selected, with lawfully minted Coverage — **consumer defect in the token; documentation gap behind it**

**Observed, `syntax-data` only.** `imports@resolved-target` under syntax-only, matrix
`UNSUPPORTED-TYPED` with deficiency `language-tier-unsupported`: consumer declared
`supported-available` **with one real coverageId**; owner wants `unsupported-typed`.

**The consumer's native evidence is exactly right.** Its Coverage
`coverage2:35347f62…` carries `coverage: unknown`, `deficiency: language-tier-unsupported`,
`nativeCause: capability-missing`, `resolutionCompleteness.state: not-attempted` — precisely
what `native-evidence.md:3183` and the matrix row (`native-evidence.md:534`,
`imports@resolved-target` under `syntax-only` = ✗ `language-tier-unsupported`) prescribe.

**Its execution-inputs account is not.** `supported-available` contradicts the matrix. A
conforming shape **does** exist and I confirmed it executably
(`probes/p13-corrective-route.json`): `applicability: unsupported-typed`, `coverageIds: []`,
`sourceUniverse: <binding U>`, and the cell outcome then derives `state: complete` with a
`(None, None)` pair.

**The documentation gap.** Under that conforming shape the lawfully minted
`unknown`/`language-tier-unsupported` Coverage is referenced by **no** account, and the cell
outcome discloses **no** carrier. Nothing published says that is intended, and it sits
awkwardly beside `native-evidence.md:905` — "Omitting it would leave a consumer with no record
that the capability exists and was not served." The disclosure survives only as the
`unsupported-typed` token itself.

**F3a.** `syntax-data`'s extra `EXECUTION_INPUTS_CAUSE_CARRIER` is **derivative**: with the
account read as `unsupported-typed`, the cell derives `complete`, and `:1415–1417` then faults
the row's non-null pair. Not an independent difference.

**Classification: consumer defect** (account token), **plus a documentation gap** root should
close either way.

### 1.4 F4 — `clones-fact` carrier under census-driven incompleteness — **reference defect**

**Observed in four cells** (`syntax-code` c0, `typescript` c0, `rust` c0/p0 and c0/p1), and
**not** in `rust-partial` or `syntax-data`. That asymmetry is the discriminator.

I computed the owner's own expected-subject census (`probes/p17-clones-census.json`):

| run | expected | covered | missing | owner account pair | consumer row pair |
|---|---|---|---|---|---|
| syntax-code c0/p0 | 5 | 2 | LICENSE, README.md, package.json | **provider-unavailable**, null | null, null |
| typescript c0/p0 | 7 | 3 | package-lock.json, package.json, tsconfig*.json | **provider-unavailable**, null | null, null |
| rust c0/p0 | 9 | 4 | Cargo.lock, Cargo.toml, … | **provider-unavailable**, null | null, null |
| rust c0/p1 | 9 | 1 | … 8 paths | **provider-unavailable**, null | null, null |
| rust-partial c0/p0 | 9 | 4 | … | input-closure-incomplete / body-language-owner-unenumerated | **same** |
| syntax-data c0/p0 | 6 | 6 | — | language-tier-unsupported / capability-missing | **same** |

The **state** agrees (`partial`); only the **carrier** differs. Where the Coverage record
carries a real pair the two sides agree exactly; where it carries none, the owner
`_summarize_coverage_records:614` takes `coverage_records[0].get("deficiency") or
"provider-unavailable"` and **invents** a carrier.

**That invention is what the contract forbids.** `execution-inputs-contract.v1.md:68`: the
row's pair "**must actually occur on a source record** — … and **not a rewrite of inventory
`budget-exhausted` as generic `provider-unavailable`**." And §5 (line 83): "do not manufacture
a carrier." The only source record here is a Coverage whose pair is `(null, null)`. The
consumer's `(None, None)` is the pair that actually occurs; the owner's
`provider-unavailable` occurs on nothing.

The consumer reached this deliberately and documented it: `output/helper-corrections.json`
V18-D7/V18-D8 records that its clones-fact FILE extent had dropped `package.json`, lockfiles
and tsconfigs, cites the clause token
`EXECUTION_INPUTS_COVERAGE_DERIVE:MISSING_EXPECTED_SOURCE_SUBJECTS_MAKE_THE_ACCOUNT_INCOMPLETE`,
and says "the consequence is reported rather than engineered away".

**Classification: reference defect.** The frozen owner manufactures a carrier for
census-driven incompleteness, which its own contract prohibits, and then refuses the host that
declines to manufacture one. **Census-driven incompleteness currently has no defined carrier.**

---

## 2. Query artifact and mutation scope — root's four preliminary items

Assessed against final19 bytes (`output/query/graph-query-reconstruction.json`,
`output/vectors/mutation-keys.json`), not historical18.

**Q1 `truncated=true` — CONFIRMED (consumer defect).** `query-projection-contract.v3.md` §5:
"**Page fullness** is `truncated-page`, `truncated=false`. It is **not** operation truncation."
The artifact sets `truncated: true` on operations 1 (page size 1, plainly page fullness), 5 and
6. *Limit:* I compared against the contract sentence; I did not validate the reconstruction
document against a response wire schema, as it is a reconstruction narrative.

**Q2 cursor `ord:1` — CONFIRMED (substantive).** `graph-query.schema.json#/$defs/Page.cursor`:
"Opaque host token **bound to** projectId+runId+factViewDigests+operation+effective
params/order+page position. Reference form `q3.<runId-64hex>.<selectionHash64>.<position>`."
Contract §5 adds "Continuation requires request `view.{runId}` equal to the bound Run" and
routes a bind mismatch to `QUERY.CURSOR_MISMATCH`. `ord:1` carries a position and nothing else,
so the published continuation check and that route are unimplementable against it. It is
**schema-valid** (opaque, 1–256 chars), so this is a contract-level defect, not a schema
violation.

**Q3 external-import omission — CONFIRMED.** The `typescript` Run holds a genuine external
resolved import target: `{"importer":"ts:src/index.ts#main","resolvedTarget":
"ts:node_modules/left-pad/index.d.ts","specifier":"left-pad"}`. The contract requires that "an
external resolved target that is not first-party inventory remains a lawful vertex". The
artifact's `endpointMembership.admittedMembers` lists 11 members and includes no `left-pad`
endpoint. *Limit:* I compared the artifact's own declared membership list against the Run's
import facts; I did not re-derive the projection.

**Q4 invalid request/step IDs — REFUTED in the query artifact, CONFIRMED in the mutation
scope.**
* Query artifact `requestId` is `req1_abababababababababababababababab`, which **matches** the
  published `RequestId` pattern `^req1_[0-9a-f]{32}(?![\s\S])`. No `stepId` appears at all.
  Root's concern does not land here.
* `mutation-keys.json` `genericMutation.preimage` uses `requestId: "req-7f3a1c"` and
  `stepId: "step-2"`. `MutationReplayScopeV1`
  (`workflows/schemas/invocation-record.schema.json#/$defs/MutationReplayScopeV1`) `$ref`s
  `common#/$defs/RequestId` (that pattern) and `common#/$defs/StepId` (**integer** 0–63).
  Validated against the frozen schema: **invalid** —
  `'req-7f3a1c' does not match '^req1_[0-9a-f]{32}(?![\s\S])'`; the same record with a
  conforming `requestId` and integer `stepId` validates. The declared idempotency key
  `20cbbcc1695dd79f…` is therefore `H("workflow.mutation-intent", …)` over a **preimage that
  cannot be admitted**, so the demonstrated key is not reproducible from an admitted record.

---

## 3. Does frozen32 source acceptance require reopening?

**Yes, at bounded scope — for F1 and F4.** Both are defects in frozen32 *owners*, not in the
consumer:

* **F1** — the account `sourceUniverse` law is enforced by the reference and published by
  nothing. Either the contract §5 table and `NativeCoverageAccountV1` gain the rule, or the
  reference stops enforcing it. Until then two conforming hosts disagree and one is refused.
* **F4** — the reference manufactures `provider-unavailable` for census-driven incompleteness,
  which `execution-inputs-contract.v1.md:68` and §5 both forbid. Either the contract defines a
  carrier for that case, or `_summarize_coverage_records` must stop inventing one.

**F3 does not require reopening** the source's *rules* — the consumer's account token is wrong
and a conforming shape exists — but the **documentation gap** (what becomes of the lawfully
minted Coverage, and of the disclosure, for an UNSUPPORTED-TYPED cell) should be closed in the
same pass.

**F2 needs a decision, not necessarily a change**: publish the applicability precedence, and
state whether an UNSUPPORTED-TYPED cell may be left unselected or must be answered.

**The blind19 ACCEPT-RECONSTRUCTABLE claim and root's REFUSE are both partly right.** Root's
replay is correct that the exports do not satisfy the frozen owner. The consumer is correct on
F4 and on the native half of F3, and is enforcing a contract clause the reference does not.

---

## 4. Proposed correction route (for root to decide; nothing authored)

1. **F1, smallest coherent fix:** add the `sourceUniverse` rule to the §5 table and to
   `NativeCoverageAccountV1` as a conditional, stating explicitly which of "binding U always"
   or "null when no Coverage" is normative. If binding U is chosen, the schema conditional can
   mirror the existing `coverageIds` one. No identity or enum change.
2. **F4:** define the carrier for census-driven incompleteness. Either (a) a named deficiency
   for "expected subjects not in any returned partition", or (b) explicitly allow a
   `(null, null)` pair for that case and delete the `or "provider-unavailable"` fallback at
   `_summarize_coverage_records:614`. (b) is smaller and matches the contract's existing "must
   actually occur on a source record".
3. **F3:** state in §5 what happens to Coverage lawfully minted for an UNSUPPORTED-TYPED pair —
   that it is retained but unaccounted, and that the token is the disclosure.
4. **F2:** publish the applicability precedence in the §5 table, and reconcile
   `enumeration-contract.v1.md:30`'s `unselected` allowance with native's "answered by
   disclosure rather than omitted".
5. **Q1–Q4:** consumer-side corrections; Q4's mutation-key vector additionally invalidates the
   demonstrated key and should be regenerated from an admissible preimage.

---

## 5. Unresolved questions

1. **F1 direction.** Which value is normative? I found no basis in the published text to prefer
   either, and the consumer's rule is defensible.
2. **F2 precedence.** Is the applicability enum ordered, and does "answered by disclosure rather
   than omitted" forbid leaving an UNSUPPORTED-TYPED cell unselected? The consumer's own two
   runs answer this differently.
3. **F4 semantics.** Should census-driven incompleteness carry a deficiency at all? If yes, it
   needs a new named one; the existing vocabulary has no member that "actually occurs on a
   source record" for this case.
4. **Scope beyond these five runs.** I diagnosed only the differences reachable in the five
   exported positives. Whether other capability/mode combinations hit F1/F2/F3 shapes was not
   surveyed.
5. **Q3 breadth.** I confirmed one omitted external vertex in one Run; I did not survey the
   other four Runs or re-derive the full projection.
6. **Root's other hypotheses.** Scope enumerator / foreign-U filtering were **not** supported by
   anything I traced, consistent with root's instruction not to treat them as demonstrated. I
   found no evidence for them and make no claim either way.
