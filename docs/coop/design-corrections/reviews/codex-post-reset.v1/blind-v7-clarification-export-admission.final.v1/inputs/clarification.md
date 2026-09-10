# OpenSIP DR-011-R10 — blind consumer-B, CLARIFICATION v1

**Standing.** Post-review clarification of my own completed blind pass, after
root feedback. **Not** a new fresh blind, and **not** a design-correction
authoring pass: I edited no contract, schema or kit byte. The original review is
retained verbatim and immutable at `consumer-b.v7/output/` —
`blind-review.json` SHA-256 `520b7ddf…d466d4`, `blind-review.md` SHA-256
`ecd765f8…7a02e25`, both re-verified at the start and end of this pass. All new
work is in `consumer-b.v7-clarification.v1/output/`. Design was read only from
`consumer-b.v7/subject`. No product qualification or implementation
authorization is claimed or implied.

**Headline.** Root is right on item 1 and item 2, and I have corrected my code
and retracted the finding respectively. On item 1 my measurement differs from
root's count in one place and I report the difference rather than adopting the
number. Items 3 and 4 are corrected to measured scope.

---

## Item 1 — my closure did not admit three record families, and my grammar-tree check was wrong

### 1.1 What I reproduced, before changing anything

`probes/probe_root_claims.py` ran against the **original exported bytes** with
the **original helpers** (`probes/probe-root-claims.json`).

**Defect A — `finding.evidenceRefs` not strictly ascending by `C(item)`.**
Confirmed. `identity-schemas.v2#/$defs/finding/properties/evidenceRefs` carries
`x-opensip-order: canonical-set`; my original `build_proof` emitted
`[fact, coverage]` in construction order. Because `C` sorts object keys, the
sort key is `{"digest":…,"domain":…}` — **the digest sorts first**, so whether
the pair was ascending depended on which hex happened to be lower. That is why
it broke in some graphs and not others.

**Defect B — grammar members absent from their own declared closure tree.**
Confirmed. Native §1.2 requires "every grammar definition, the bundle manifest
and the normalizer specification **present in the retained tree**". My original
`vec_syntax` put unrelated placeholder bytes in the `kind=grammar` closure tree
and retained the real `bundleDigest`/`grammarDigest` bytes as loose CAS blobs.
Root's phrasing is exactly right: **merely retaining a blob elsewhere in CAS
does not satisfy membership.** (The normalizer specification digest happened to
be a tree member only because I had used identical bytes in both places — luck,
not law.)

**Root cause, and it is broader than either defect.** My `Closure` never walked
`finding`, `finding-fingerprint` or `execution-plan` objects at all. Those three
domains were **exported and never admitted against any schema or order
annotation**. `grep -n 'startswith("finding' graph.py` on the original returns
nothing. So my original claim that "every record is validated against its owning
normative schema" was **false as stated**, not merely incomplete.

### 1.2 My measurement differs from root's count — I report the difference

Root wrote that the unordered `evidenceRefs` are in RUN-TS, RUN-RS-A/A2 and
RUN-SYN-DATA, that five originals are refused, and that "both incomplete Rust
disclosure graphs admit".

I measure **five** graphs with unordered `evidenceRefs` and **six** distinct
graphs refused:

| graph | evidenceRefs ascending? | grammar members in tree? | corrected checker |
|---|---|---|---|
| RUN-TS | **no** | n/a | REFUSED |
| RUN-RS-A | **no** | n/a | REFUSED |
| RUN-RS-A2 | **no** | n/a | REFUSED |
| **RUN-RS-NO-OWNERSHIP-DISCLOSED** | **no** | n/a | **REFUSED** |
| RUN-RS-PARTIAL-ENUMERATION-DISCLOSED | yes | n/a | ADMITTED |
| RUN-RS-B | yes | n/a | ADMITTED |
| RUN-SYN-CODE | yes | **no** (3 members) | REFUSED |
| RUN-SYN-DATA | **no** | **no** (5 members) | REFUSED |

`RUN-RS-NO-OWNERSHIP-DISCLOSED` carries fact digest `9369…` before coverage
digest `2d5a…`, so it is unordered. Only **one** of the two incomplete Rust
disclosure graphs (PARTIAL-ENUMERATION) admits. Evidence:
`probes/corrected-checker-vs-original-exports.json`.

I am not disputing root's substance — both defects are real and mine. I am
recording that the affected set is six graphs, not five, because the corrected
report has to state the measured scope.

### 1.3 What I corrected

**`graph.py` — a generic admission pass so no domain can escape again.** Rather
than hand-adding the three missing joins, I added a closed
`FOUNDATION_SELECTOR` map plus `native_selector()` (read from the kit's own
`x-opensip-digest-domains.domainSets`), and `admit_every_retained_object()`,
which runs schema **and** declared-order admission over **every** retained typed
object and reports its coverage. A domain with no row is itself a refusal
(`RETAINED_OBJECT_DOMAIN_UNREGISTERED`). Measured coverage for RUN-TS: 16
domains, 45 objects, **zero uncovered**.

**`graph.py` — new joins** for the families that previously escaped: finding →
fingerprint identity, detector-kind rule closure, `finding-parameters` preimage
with `messageCode` equality, evidence citations confined to an evaluated view /
Plan-selected imports / retained blobs, `proof.findingIds == evidence.findingIds`;
and execution-plan → contiguous ordinals, retained `stage-spec` per stage with
Plan/producer/outputDomains/outputSchema joins and the "a stage takes no hidden
input" subset check against the Plan's analysis spec.

**`graph.py` — tree MEMBERSHIP** for the grammar bundle: `bundleDigest`, every
`grammarDigest` and the normalizer `specificationDigest` must be members of the
declared `kind=grammar` closure tree, with three distinct refusals.

**`build.py`** — `evidenceRefs` is now sorted by `C(item)`.
**`vec_syntax.py`** — the closure tree is now **built from** the exact bytes the
bundle declares (`bundle/manifest.json`, `grammars/<lang>.grammar`,
`spec/normalizer.txt`).

Before-images: `before/{graph,build,vec_syntax,vec_ts,verify,run_all}.py.before`.

### 1.4 Discriminating negatives added (6)

| negative | first refusal |
|---|---|
| `finding-evidence-refs-unordered` | `ORDER[finding]: ORDER_NOT_ASCENDING:#/$defs/finding/evidenceRefs` |
| `finding-cites-a-fact-outside-the-evaluated-view` | `FINDING_FACT_CITATION_OUTSIDE_AN_EVALUATED_VIEW` |
| `finding-parameter-message-code-mismatch` | `FINDING_PARAMETER_MESSAGE_CODE_MISMATCH` |
| `grammar-definition-outside-the-closure-tree` | `SYNTAX_GRAMMAR_DEFINITION_NOT_IN_CLOSURE_TREE` |
| `grammar-bundle-manifest-outside-the-closure-tree` | `SYNTAX_GRAMMAR_BUNDLE_NOT_IN_CLOSURE_TREE` |
| `normalizer-spec-outside-the-closure-tree` | `SYNTAX_NORMALIZER_SPEC_NOT_IN_CLOSURE_TREE` |

In each the bytes remain retained in the CAS — so each is precisely a
membership test, not a retention test.

### 1.5 Rebuilt, exported, reloaded

| graph | objects | blobs | checks | result |
|---|---|---|---|---|
| RUN-TS | 46 | 120 | 379 | ADMITTED |
| RUN-RS-A | 41 | 114 | 328 | ADMITTED |
| RUN-RS-A2 | 41 | 114 | 328 | ADMITTED |
| RUN-RS-B | 40 | 110 | 319 | ADMITTED |
| RUN-RS-PARTIAL-ENUMERATION-DISCLOSED | 37 | 99 | 292 | ADMITTED |
| RUN-RS-NO-OWNERSHIP-DISCLOSED | 37 | 99 | 290 | ADMITTED |
| RUN-SYN-CODE | 31 | 77 | 207 | ADMITTED |
| RUN-SYN-DATA | 28 | 73 | 188 | ADMITTED |
| **RUN-TS-MUST1-PROBE** | 48 | 123 | 394 | ADMITTED |

**9 graphs, 2725 closure checks, 0 failures** on a from-scratch reload
(`verify.py`), against 8 graphs / 1974 checks originally. **36 negatives, all
refused** (was 29).

The MUST-1 probe is now exported as a complete inspectable graph
(`vectors/RUN-TS-MUST1-PROBE.*`), with the unrelated helper errors removed.

### 1.6 Corrected admission claim

I withdraw the original phrasing "every record is validated against its owning
normative schema". The corrected, measured claim is: **every retained typed
object of all 16 domains is admitted against its owning schema and its declared
`x-opensip-order`, with zero uncovered domains**, plus the named canonical-record
preimages the closure fetches. It remains true that this is my own checker
written from prose, and that a defect in it is mine — as this pass demonstrates
twice.

---

## Item 2 — CB7-SHOULD-1 is **RETRACTED**

Root's challenge is correct and the kit settles it.

**My error.** I imposed an equation the kit never states:
`unmetPreconditions[].code == the deficiency token`. Workflows §6 says the exact
cause is carried into the requirement's unmet precondition **so that two
different causes are two different REMEDIES**. `DomainDetail` is
`{code, remedy, subject?}` with `remedy` a required `BoundedText`.

**Three things in the kit I did not weigh.**

1. `native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary`
   names the carrier explicitly: the consumer record is
   `repair.schema.json#/$defs/EvidenceRequirement`, the field is `deficiency`,
   "REQUIRED exactly when satisfied is false" — and its own standing says this
   block "adds no D9 class, code, exit or **public detail code**". The outcome
   was never meant to become a `DomainDetailCode`.
2. `imported-evidence.schema.json#/x-opensip-imported-requirement-law` gives
   every outcome a `groundedIn` naming an existing published condition, and
   distinguishes two of them in exactly root's terms: *"Named separately from
   evidence-kind-unavailable **because the remedies differ**: import the
   evidence versus widen the capture."*
3. `RepairPlanDescriptor.applicable`'s own description — "true only when every
   evidenceRequirement is satisfied **and** unmetPreconditions is empty" — is a
   conjunction, so `applicable:false` follows from the first conjunct alone.
   An unsatisfied requirement with an **empty** `unmetPreconditions` is
   consistent with the published description. Measured: schema-admitted.

**Measured expressibility.** In the field the law actually names, **16 of 16**
producible outcomes (9 native + 7 imported) are expressible. My original
"5 of 16" counted membership of a *different* vocabulary
(`DomainDetailCode`) in a *different* field.

**`REPAIR.EVIDENCE_RUN_UNAVAILABLE`, as root asked.** Registered, but **not
applicable**: workflows §6 binds it to an evidence Run "whose availability is
retained and whose sealed assurance is replayable". An unsatisfied evidence
requirement is a different condition — the Run is available and replayable and
its evidence is insufficient at the demanded rung. Borrowing it would misname
the condition, which is the same objection I raised against borrowing
`REPAIR.CLOSED_WORLD_NOT_ESTABLISHED`. It is also **not needed**.

**The demonstration** (`vec_repair_clarify.py`, two complete
`RepairPlanV1` records, both schema- **and** order-admitted, zero new codes):

| | native cause | imported cause |
|---|---|---|
| `evidenceRequirements[].relation@minResolution` | `references@resolved-binding` | `history-change@observed` |
| `evidenceRequirements[].deficiency` (retained) | `required-relation-missing` | `history-range-insufficient` |
| `unmetPreconditions[].code` (registered) | `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` | `IMPORT.ABSENT_FOR_PREDICATE` |
| `remedy` | "native plane, relation references at rung resolved-binding: required-relation-missing — … re-analyse with the references capability requested for this unit" | "imported plane, relation history-change at rung observed: history-range-insufficient — … widen the collected revision range and re-import" |
| `applicable` | false | false |

Both remedies carry the exact plane, relation, rung and deficiency token; the
remedies differ; the deficiency is retained; `applicable` is false in both; and
`repairPlanId` differs between them. **Discriminating control:** collapsing both
onto one remedy string makes the remedies identical — which is precisely what
the purpose clause forbids, and it is the control that makes the positive
meaningful.

**Expressible ≠ authorized.** A schema-admitted `RepairPlanV1` carrying an
unsatisfied requirement is a **disclosure**. Apply additionally requires
`applicable == true`, a `RepairApplyAuthorizationV1` bound to the **exact**
`repairPlanId`, base snapshot and project, and re-checked live recipe trust.
Measured: the authorization naming the native-cause plan does not name the
imported-cause plan.

**Residue: none requiring source clarification.** What remains is implementation
latitude the law's purpose clause leaves open — whether a host *also* emits an
`unmetPreconditions` entry per unsatisfied requirement, and which registered
condition code it uses when it does. That is a choice among lawful renderings of
a disclosure whose mandated carrier is named, closed and total. It is not a
missing public or semantic contract, and I do not carry a reduced finding
forward.

**Disposition: CB7-SHOULD-1 RETRACTED IN FULL.** The original text stands
unaltered in the immutable original report as historical evidence of the error.

---

## Item 3 — CB7-MUST-1 and CB7-SHOULD-2 reassessed

### CB7-MUST-1 — **STANDS**, on the corrected build

Re-measured on the corrected helpers, exported as a complete graph
(`RUN-TS-MUST1-PROBE`, 48 objects, 123 blobs, **394 checks, 0 refusals**,
reloaded from scratch):

* the probe scope is `clones@normalized-body-hash` over the inventoried path
  `package.json` under the TypeScript universe;
* its Coverage is `coverage: complete`, `deficiency: null`, `nativeCause: null`;
* clones facts anchored on that path: **0**;
* the body-dialect selector for that path refuses
  `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`.

So the graph asserts a complete examination of a subject for which no body
identity is representable, and nothing in the published laws decides whether a
disclosure is owed. Correcting the two helper defects did not touch this: it is
not an artifact of the ordering or grammar-tree bugs. Scope is unchanged and
precise — TypeScript/JavaScript universes only; the syntax universe is closed by
the grammar-capability guard and Rust by the ownership law, both measured.

### CB7-SHOULD-2 — **STANDS, with two corrections to my own wording**

**Correction (a): the reachability is now measured, not argued.**
`vec_bounds_clarify.py` mints **129 real, distinct `TypeScriptNativeContextV2`
records** — one per real unit, each with its own inventoried `tsconfig.json` and
its own retained config graph — not 129 synthetic hex strings. Measured:

| | at 128 units | at 129 units |
|---|---|---|
| distinct real contexts minted | 128 | 129 |
| every context H frame retained | yes | yes |
| every context identity recomputes | yes | yes |
| analysis-spec rows (bound 1024) | admitted | 129, **admitted** |
| scope-descriptor roots (bound 1024) | admitted | 129, **admitted** |
| `plan.nativeContextDigests` (bound 128) | admitted | **refused** |
| Plan mints | **yes** | **no** |

An explicit single-capability `analysis.capabilities` override keeps both
published bounds satisfied while the Plan bound is exceeded. That is the finding,
now demonstrated rather than inferred.

**Correction (b): "names no field" was overbroad.** Root is right. The refusal
**does** prefix the field name (`nativeContextDigests: [...]`). Re-measured
precisely: the message is **8806 characters**, restates the entire 129-element
array, ends `"... is too long"`, and contains **no standalone count**, **no
limit** and **no remedy** (tested with a standalone-token match, after an earlier
heuristic of mine gave a false positive by matching `128`/`129` inside 64-hex
strings). The corrected claim is therefore: *no typed `PROJECT.SCOPE_LIMIT`-style
refusal with a bounded subject `field:count>limit` and a remedy is published for
the `plan` record family*. The same holds for `plan.importIds` at 257 (19555
characters, field named, no count/limit/remedy) while the resolved semantic
configuration admits up to 1024 import IDs.

**Correction (c): bounds re-measured.** `plan.nativeContextDigests` **128**,
`plan.semanticClosures` **128**, `plan.importIds` **256**. The original report
already stated 128 for `semanticClosures`; re-measured and confirmed, not changed.

I note that any source fix would require a newly frozen candidate and a fresh
independent blind; this clarification accepts no future change and grades nothing.

---

## Item 4 — reporting scope corrected, by measurement

Each of root's eight points is confirmed and now recorded as a measurement
(`vec_scope_audit.py`, `vector-results.json#/clarificationV1/item4_reportingScopeAudit`).

1. **Failure envelopes** are literal composed `CommandEnvelope` objects
   validated against the envelope schema and the `StepTermination`/`DomainDetail`
   branch contract. They are **not** raised-and-caught internal failures routed
   through a host termination projection. 7 envelopes.
2. **Authorization vectors** measure schema validity, effect-value equality
   against the pinned truth table in the `child-process` mode, the canonical
   empty owner-array digest, and the display-alias enum refusal. The CI-consent
   refusal, the over-claimed `ENFORCED-PLATFORM` refusal and the repair-plan edit
   boundary are **literal assertions in the vector**, not outputs of an executed
   security admission or authorization engine.
3. **Comparison cases** are schema-valid `ComparisonDescriptor` records with
   conceptual classifications — **not** a closed baseline/Run comparison engine;
   no pivot was evaluated and no finding set was diffed. The two ScopeDocument
   Plans **are** real constructed Plans with real distinct PlanIds, but they are
   **not** two fully compared Runs.
4. **`minResolutionPredicates`** are ladder-index comparison helpers plus
   cross-relation refusal — **not** full `sufficiency_v2` over every Coverage and
   evidence boundary (no confidence floor, derivation policy, closed-world or
   `dependsOn` recursion).
5. **Relation digest-law traversal** covers **7 top-level selector
   occurrences**, not arbitrary schema inheritance: nested members, array
   elements, map values, intermediate `$defs` aliases, inline equal patterns and
   `oneOf`/`anyOf`/`allOf` branch inheritance are outside what I walked, though
   the document's own law governs them.
6. **"Single-field mutation" was not generally accurate.** Measured: **4 of 33**
   distinct negative mutations change strictly one field
   (`compiler-version-not-from-manifest`, `grammar-version-not-from-manifest`,
   `lockfile-outside-snapshot`, `plan-budget-contradicts-config`). The rest
   change a whole record, a retained blob, a closure tree or a selection, and
   most recompute downstream identities. What holds for all of them is that each
   **isolates one law** and leaves the rest of the graph otherwise complete.
7. **`nativeHPreimages.canonicalPayloadBytes`** are 400-character **truncated
   heads for 4 of 6** records (425/722/1884/2163 canonical bytes). Full bytes do
   exist in the per-run blob exports keyed by digest.
8. **ADV-1 counts** compared 10 inherited fault-**map** entries against 12
   successor **enum** members including the `none` sentinel. The like-for-like
   comparison is **11 → 12**; the delta is the same single member
   (`host-invariant`) either way.

---

## Retained evidence

| artifact | content |
|---|---|
| `probes/probe_root_claims.py`, `probe-root-claims.json` | pre-fix reproduction on the original bytes |
| `probes/verify_originals_with_corrected_checker.py`, `corrected-checker-vs-original-exports.json` | corrected checker refusing 6 of my 8 originals |
| `before/*.before` | exact before-images of every edited module |
| `work/*.py` | corrected helpers plus 3 new clarification modules |
| `vectors/` | all 9 exported graphs (objects + blobs) |
| `vector-results.json`, `verify-report.json` | raw measured results |
| `blind-review.{json,md}` | full corrected report with dispositions |

Original outputs and the 45-file kit are byte-identical, re-verified at finish.
