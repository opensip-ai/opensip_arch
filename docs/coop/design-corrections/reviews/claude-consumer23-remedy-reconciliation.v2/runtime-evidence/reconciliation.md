# Remedy reconciliation: consumer23 author remedy, three bounded issues

**Standing.** This is remedy assistance by origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`.
It is **not independent acceptance and not successor acceptance**, and it carries no blind-consumer standing.
- **Purpose.** It helps the author before a new fresh source acceptance and a new fresh blind consumer, each
  run under its own new origin.
- **Grants nothing.** No application outcome, readiness, activation or implementation authority.

**Inputs.**
- The captured author report (`author-report.md` `d6bf9f4d…`, `author-report.json` `de5f2fd2…`) from author
  origin `823bf66b…`.
- `after-manifest.json` (`a86847ff…`).
- The seven captured after-images under `observed-author-source/`. Each was verified against the
  after-manifest, and the native schema image equals frozen36.
- Frozen36 for the owning contracts, read-only.

**Not read:** the live source assembly, original blind artifacts, and root consumer diagnostics.

**Evidence.** One targeted probe (`receipts/p01-targeted.json`) over a disposable frozen36 overlay carrying the
author images. It checks the wrapper, the helpers and the native route, and runs no suites. My earlier
gap-assessment records stay historical and unedited.

| Issue | Verdict | Recommended change |
|---|---|---|
| 1. S1 schema-first remedy | **Coherent** | One precision sentence in query §2 step 2 |
| 2. Native schema annotation | **Keep exact registered bytes** | Explicit supersession note in native §10 |
| 3. Native §10 primary-deficiency wording | **Real scope conflation** | Boundary paragraph in §10, one fault-law sentence, one model docstring; no behaviour change |

All recommended edits anchor exactly once in the author's images. They were applied only to disposable copies,
and the edited model still compiles. The full reviewable diff is `recommended-edits.diff`.

---

## 1. S1: the author's schema-first remedy is coherent

**What the author did.** The author took the lawful alternative my gap assessment recorded:
- closed-schema admission decides;
- a `package` endpoint without a non-empty `packageManifestPath` is `QUERY.PARAMS_MALFORMED`;
- `graph-query.schema.json` is unchanged;
- query §2, the §7 rows and `parse_endpoint_syntax` agree.

**Measured on the author's images:**

| Request | Public wrapper, no Run | Wrapper, purged observation | Wrapper, dummy Run + purged | Helper |
|---|---|---|---|---|
| package, coordinate absent | `REQUEST.PRECONDITION_FAILED` / `QUERY.PARAMS_MALFORMED` | same | same | same |
| package, coordinate `""` | same | same | same | same |
| package with coordinate | `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN` | same | `HOST.IO_FAILURE` / `evidence.purged` | not refused |

**What that shows.**
- **Schema first.** The malformed refusal really is decided before Run presence, view and availability.
- **Ambiguity is helper-only.** `QUERY.ENDPOINT_AMBIGUOUS` is produced only when `admit_vertices` is handed a
  pre-marked key.
- **Nothing else changed.** The schema bytes are unchanged, and no model issue remains.
- **My earlier preference is withdrawn for this successor.** I had suggested preserving the old §2
  distinction with a request-side schema. The author's choice needs no schema or planning-input change for S1,
  and it satisfies both conditions I attached to the alternative: §2 step 2 and the §7 row are rewritten.

**One precision.** §2 defines an endpoint, and therefore a vertex, by its complete tuple (line 36). So a
complete tuple cannot name two vertices under the *contract*, not just under the reference. The author's
closing clause, "the detail remains the lawful answer for a vertex domain that could", implies a lawful domain
the contract does not admit.

**Recommended replacement** in `workflows/query-projection-contract.v3.md` §2 step 2. Replace:

> The reference vertex domain is keyed by the complete tuple, so one retained Run cannot yield two distinct
> vertices for one tuple and this step is not reachable through `execute_graph_query`; the detail remains the
> lawful answer for a vertex domain that could.

with:

> Because this section defines an endpoint, and so a vertex, by its complete tuple, a complete tuple names at
> most one vertex of an admitted domain: this step is not reachable through `execute_graph_query` and is kept
> only as a closed refusal. An implementation that nevertheless observes two distinct vertex records for one
> complete tuple must refuse with `QUERY.ENDPOINT_AMBIGUOUS` and must never choose one.

**Owners:**
- query-projection-contract.v3.md §2 (line 36 tuple identity; fault precedence), §7 rows, §8 step 1;
- `graph-query.schema.json#/$defs/GraphEndpoint` (unchanged);
- query model `_validate_request`, `parse_endpoint_syntax`, `inventory_vertices`, `admit_vertices`.

## 2. Native schema annotation: keep the bytes, supersede the text in §10

**What the author did.** The author correctly restored `native-evidence.schemas.v2.json` to exact frozen36
bytes. The stale annotation was then recorded only in the author report.

**Why §10 needs a note.** At
`#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination`
the annotation still lists three codes and says `errorCode`. Against the corrected §10 table, that public text
is incomplete and misleading, so the owning contract must say which governs.

**The bytes must not change here.**
- `coverage2` is minted from `payloadSchemaDigest`, the raw SHA-256 of the exact registered schema document
  (native §4.1a, lines 1759–1760; identity-schemas `payloadSchemaDigest`).
- In my earlier rehearsal, changing those bytes failed check-identity
  `v20-native-view-fixture-declares-current-registered-schemas`.
- It also made every positive retained package13 Run refuse `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`.
  These results are retained in my gap-assessment completion runtime (`receipts/p05-successor-rehearsal2.json`,
  `receipts/s04-retained-schema-digests.json`).

This recommendation includes no registration or remint.

**Recommended insertion** in `native-evidence.md` §10, directly after the author's paragraph ending "agrees
with it. No D9 class, code, exit or vocabulary changes.":

> **Superseded schema annotation (registered bytes kept).** The annotation
> `native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination`
> still reads "the class/exit/errorCode of the Run or step that carries the requirement - unchanged, still the
> section 10 table columns (indeterminate (3) with VERDICT.INDETERMINATE, COVERAGE.PROVIDER_UNAVAILABLE or
> COVERAGE.BUDGET_EXHAUSTED)". Its reference to the section 10 class and code columns stands. Its parenthetical
> three-code list and its word `errorCode` are superseded by this section: an `indeterminate` termination carries
> `reasonCodes`, and the codes are the complete route in the table above, including
> `COVERAGE.LANGUAGE_TIER_UNSUPPORTED`, `COVERAGE.CONFIDENCE_FLOOR_UNMET` and `COVERAGE.REQUIRED_RELATION_MISSING`.
> Where the annotation and this section differ, this section governs. The annotation's bytes are deliberately
> unchanged: that document is a registered payload schema whose raw SHA-256 is the `payloadSchemaDigest` from
> which every `coverage2` minted against it is identified (§4.1a), so editing the annotation is a schema-document
> successor with its own re-registration, not a text correction.

## 3. Native §10 scope: the author's wording conflates stage selection with Run termination

**Author text:**

> The **primary** deficiency is chosen by the precedence above over every deficiency the Run's admitted Coverage
> entries declare and the one a clean typed stage terminal implies …

**Why this conflates scopes.** That describes exactly the native helper's input,
`run_termination(stage, coverage_entries)`, but calls the result the *Run's* primary deficiency. The owners put
the Run's termination above native:
- **Host finalizer only.** Only the host finalizer constructs the termination (D9 `invariant-one-mapper`;
  native line 70: "D9 class assignment is host-owned"; workflows-and-surfaces 1386–1388).
- **Host-ordered reduction.** The host reduces concurrent conditions: fault cause, else rejection cause, else
  deficiencies. The primary is `deficiencies[0]` of *its* ordered set, and the rest become
  `secondaryDeficiencies` (D9 `concurrentConditionReducer`; `causeModel.precedence`, `theOneException`,
  `codeDerivation`; X1, X4, X10).
- **Requirement-relative deficiencies.** `required-relation-missing` and `confidence-floor-unmet` have **no
  entry carrier**; the cause registry marks them `none-in-entry`. The confidence floor lives in `RequirementV2`,
  and a missing relation has no entry (native §4.6). Their D9 goldens (`analysis-required-coverage-missing`,
  `analysis-confidence-floor-unmet`) are requirement scenarios.
- **Verdict composition.** Required execution deficiencies and gating-rule indeterminacy make the sealed verdict
  indeterminate (evaluator-composition-contract §5, lines 56 and 58, and line 315).

**Measured on the author's model:**
- The helper produces `COVERAGE.REQUIRED_RELATION_MISSING` or `COVERAGE.CONFIDENCE_FLOOR_UNMET` only when an
  entry declares them. A clean stage with no entries is `success`.
- A stage-implied primary can differ from the typed-detail deficiency:
  - `BudgetExhausted` stage + `resolution-incomplete` entry → `COVERAGE.BUDGET_EXHAUSTED`, detail
    `resolution-incomplete`;
  - `Unavailable` stage + `budget-exhausted` entry → `COVERAGE.PROVIDER_UNAVAILABLE`, detail `budget-exhausted`.
- A crashed stage keeps `PROVIDER.PROTOCOL_VIOLATION`.
- The route is total over the nine deficiencies, drift-free, and refuses non-members.

**Preserved by the recommendation:**
- the total native-to-D9 route;
- native stage and entry precedence, and `nativeCause`s;
- the fault and cancellation law;
- the host's responsibility for `secondaryDeficiencies`.

**Deliberately not added:**
- a per-requirement D9 code;
- any recipe ordering requirement, proof-cause, import or verdict outcomes.

**Recommended replacement** in `native-evidence.md` §10 of the author paragraph beginning "The **primary**
deficiency is chosen…" (through "…is **not** produced by that helper."):

> **Native stage selection, and where it stops.** Within one native stage, the precedence above selects that
> stage's **native primary deficiency** over the deficiencies its admitted Coverage entries declare and the one a
> clean typed stage terminal implies (`BudgetExhausted` → `budget-exhausted`, `Unavailable` →
> `provider-unavailable`). A faulted or cancelled stage mints nothing and keeps its own operational-failed or
> interrupted termination, so no deficiency accompanies it. The typed detail names the most specific deficiency an
> entry actually carries and every `nativeCause` those entries carry; it can differ from a stage-implied primary.
> The reference `run_termination` implements exactly this stage selection and returns its one code.
>
> That selection is the native contribution, not the Run's termination. Only the host finalizer constructs the
> Run's termination (`d9-exit-contract.v1.14.json` `invariant-one-mapper`). It reduces every concurrent condition
> the Run exhibits under `causeModel`: a fault cause, else a rejection cause, else deficiencies, whose primary and
> ordered `secondaryDeficiencies` come from that reduction (`concurrentConditionReducer`, `codeDerivation`). Besides
> native stage selections, those conditions include requirement sufficiency over `RequirementV2` (§4.6;
> `required-relation-missing` and `confidence-floor-unmet` have no entry carrier and are requirement-relative),
> required execution and imported-evidence obligations, and verdict composition
> (`evaluator-composition-contract.v3.md` §5). Whatever `DeficiencyV2` member that reduction names takes its class
> and code from the total route above. This section does not define how requirement, proof-cause, import or
> verdict outcomes are ordered in that reduction.

**Recommended replacement** of the author's fault-law sentence ("The termination code is the whole-Run route of
the Run's primary deficiency…"):

> The stage's native termination code is the route above applied to its native primary deficiency:
> `VERDICT.INDETERMINATE` for the incomplete-input deficiencies named here, and `COVERAGE.BUDGET_EXHAUSTED` /
> `COVERAGE.PROVIDER_UNAVAILABLE` for those two terminals unless an entry declares a more specific deficiency
> (`run-termination-code-is-the-primary-deficiency-route`). The Run's termination is the host's D9 reduction over
> all its conditions (section 10, native stage selection).

**Model issue (docstring only, no behaviour change).** `native_evidence_model.v2.py` `run_termination` says
"Otherwise the Run's PRIMARY deficiency is…". Replace it with the stage-scoped wording in
`recommended-edits.diff`:
- "Otherwise the STAGE's native primary deficiency is …";
- "the stage's native termination is `native_deficiency_d9` of it";
- "NATIVE CONTRIBUTION ONLY: the Run's HostTermination is the host finalizer's D9 reduction over every concurrent
  condition (native stages, requirement sufficiency, execution and import obligations, verdict), which this
  helper does not see."

**Advisory.** A stage-implied primary produces a code that differs from the typed-detail deficiency. How a host
pairs a `coverageId` with such a termination belongs to host and D9 and is not decided here.

## Limits

- **Targeted probe only.** No global suite, pin, planning or generated-report run.
- **The author applies the edits.** The recommended texts were rehearsed only on disposable copies.
- **The reduction's ordering stays undefined.** The scope boundary names the host reduction but deliberately
  does not define how requirement, proof-cause, import or verdict outcomes are ordered in it.
- **Not read:** the author assembly and its receipts, beyond the captured report, manifest and images.
- **Carried unchanged:**
  - TCB-SCOPE-01 as one shared assumption over 13 dependent rows;
  - 32 product gates with 0 performed and condition 5 NOT MET;
  - 54 planned recovery cases with 0 executed;
  - source36 acceptance reopened;
  - no final application or readiness authority.

**Probe error kept.** The probe's predicate "helper inputs are only stage and entries" came out False only
because the model uses postponed annotations, so the recorded signature is
`(stage: 'dict', coverage_entries: 'list[dict]') -> 'dict'`. The helper's inputs are exactly its stage and entries.
