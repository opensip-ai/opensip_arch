# OpenSIP — fresh independent architecture/design/reference review, v17

**Verdict: ACCEPT** — for **source and design only**, bound to the exact frozen bytes
`subjectManifestSha256 = 8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c`.

**Zero unresolved MUST issues. Zero unresolved SHOULD issues.** I raise two new findings and
both are nonblocking advisories. Under the standing rule that *any* unresolved MUST or SHOULD
forces `CHANGES_REQUIRED` regardless of headline verdict or check count, there is none here.

I am actual Claude in a fresh independent session. I authored none of these bytes and am not
correction coauthor `4b48ccdd-92fb-4f92-9db2-ac8942f796d6`, blind
`15922f81-214f-4262-9201-227218b75e99`, or the earlier independent
`543080e2-18a0-42f2-bfd7-29858aaed6bb`. I ran no agents, spawned no subagents, made no fix, no
product implementation change, no commit and no push, and edited no subject byte. Everything I
wrote lives under `/tmp/opensip-design-corrections/post-reset-review.v17`, including both
disposable full copies, every probe, every failed attempt and every report.

**The v16 ACCEPT did not survive blind reconstruction.** I have treated that as the governing fact
of this review: an ACCEPT here is not a prediction that a new blind reconstruction will succeed,
and it cannot substitute for one.

---

## 1. Custody, before and after

The manifest hashes to the declared value. All **7671** declared files verify by digest *and* by
length: **0** missing, **0** hash mismatches, **0** length mismatches, **0** undeclared files on
disk, **0** symlinks, and the observed byte total equals the declared **531,154,521** exactly. I
ran the identical check again after finishing — identical result — so the frozen subject is
unchanged by this review.

Two named disposable full copies, each verified byte-exact against the manifest before use:

| Copy | Purpose | Byte-exact before | In-tree delta after all execution |
|---|---|---|---|
| `copy-A-reference-run` | the six recorded reference-check commands | 7671/7671 | 0 modified, 0 added, 0 removed |
| `copy-B-probes` | my own probes, plus a second determinism run | 7671/7671 | 0 modified, 0 added, 0 removed |

A third directory, `copies/v16-extract`, holds **13** files extracted from the repository's own
`candidate-source.v16.tar.gz` as the before-image for structural diffs. It is a *partial*
extraction, not a copy and not a subject, and it is recorded as such. Its extracted bytes match
the `beforeSha256` values declared in the source assessment, which is how I know the before-image
is authentic.

The native checker writes its report in-tree and also carries a `--regenerate-pins` mode. It was
run **only** inside the disposable copies, and `--regenerate-pins` was **never** invoked.

## 2. Source pins, verified before anything executed

| Pin registry | Entries | Valid |
|---|---|---|
| `foundation/source-pins.v1.json` | 1099 | 1099 |
| `native/source-pins.v2.json` | 71 | 71 |
| `security/source-pins.v1.json` | 73 | 73 |
| `workflows/source-pins.v1.json` | 65 | 65 |
| **total** | **1308** | **1308** |

All six reference-check command sources match their declared `sourceSha256` **and** their manifest
entry. **No pin was rewritten under any circumstance** — a pin failure would have been a finding,
never something to repair. After all recording I re-sealed all 1308 pins in the frozen subject and
in both copies: **3924 pin checks, 0 mismatches.**

*(A correction of mine: my first pin parser matched `primaryReferences` before `pins` in the native
registry and reported 0 entries. Re-run against the `pins` key it is 71/71. The figure above is the
corrected one.)*

## 3. The exact v16 → v17 delta

Predecessor chain verified: the v17 manifest's declared predecessor equals the actual SHA-256 of
`candidate-subject.v16.json`.

**31 files changed, 832 added, 0 removed.** Outside review scaffolding that is **30 changed and 2
added**. The assessment declares a 17-file source delta, and it is exactly consistent: for all 17,
`beforeSha256` equals the v16 manifest entry, `afterSha256` equals both the v17 manifest entry and
the actual frozen bytes, and `coauthorSha256` equals `afterSha256`.

The 13 changed non-scaffold files *outside* that 17 are all generated reports, the four pin
registries, the README and the correction crosswalk — no normative source hides among them. The 2
additions are the v17 preservation report and the v17 disposition record.

## 4. The six reference checks

I wrote `logs/expected-outcomes.prewritten.json` **before** executing anything, grounding each
expectation in my own pin verification rather than in the candidate's logs.

All six reproduced in **both** copies: exits matching, stdout **byte-identical** to the frozen
logs, and every in-tree report regenerated **byte-identical** to the frozen one. Zero source files
were mutated and zero files added by execution. The results are therefore deterministic across two
independent byte-exact copies.

I re-derived every headline figure from the reports **I executed**, rather than restating them:

- foundation **1694** = 231 + 1346 + 24 + 28 + 65, summed from the executed component reports; **1099** source pins
- identity **1346** passing calls over **1334** distinct ids, **12** duplicate extra instances — from exactly two ids at seven instances each (`closed-closure`, `exact-version-closure`), which reproduces the candidate's own count account, whose pinned `sourceReportSha256` I also confirmed
- security **456** cases, **10** invariant sweeps, 39 schemas validated
- native **355** cases (**74** positive, **281** negative), **66** matrix cells = 11 capabilities × 6 modes, **0** qualified cells
- workflows **1787**, over 13 schemas and 4 boundaries
- integration **392** passed, 0 failed
- **45** commands, **43** goldens

These are measured passing **calls**, **distinct IDs**, and **scoped cases and sweeps with their
recorded scope**. They are not exhaustive coverage and are never product qualification. Nothing in
them qualifies a host, compiler, provider, ledger, renderer, storage or platform.

## 5. The four blind-v6 findings

I authored every expectation from the published law before running, and treated the candidate's own
case files as construction data only, never as a verdict oracle.

### CB6-MUST-1 — per-requirement vocabulary · **corrected and verified**

The field is retyped from `D9Deficiency` to a plane-tagged `oneOf` over **two separately defined**
vocabularies. Measured on the frozen bytes:

- The native plane vocabulary is **exactly `DeficiencyV2`, same members and same order**, so every
  native sufficiency cause is preserved and all four values blind v6 named inexpressible —
  `derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete`,
  `resolution-incomplete` — are expressible.
- The imported plane has its **own** 7-member vocabulary, **disjoint** from the native one, owned by
  a separate law with per-kind applicability. The model *reads* `DeficiencyV2` and the imported law
  rather than restating them, so the two cannot drift.
- **The global D9 vocabulary did not grow.** `D9Deficiency`'s enum is byte-identical at 10 members;
  only a description was added — which the coauthor discloses, and which I measured independently
  rather than accepting.

I exercised the actual consumer against the actual owning schema over **191** cases spanning the
full cross-product of relations and vocabularies. **All 191 matched my independently authored
expectations; 0 disagreements.** Within that:

- All **10** presence-law cases **agree at both boundaries** — the exact claim CX-BV6-02 makes.
  `satisfied` must be an actual bool (`1` and `0` both refuse), and a present key with a `null`
  value refuses in **both** branches. Two positives admit.
- The **50** cases where the consumer refuses and the schema admits are *all* cross-plane or
  per-kind — precisely the registry lookup the schema explicitly delegates to admission. That is
  the documented division of authority, not a defect.
- I drove the **real producer**: `sufficiency_v2` genuinely emits each of the four formerly
  inexpressible outcomes, and each round-trips into a real `EvidenceRequirement` that admits at both
  boundaries. Lossless.
- The two specific admissions BV6-V3-IMPORT-CAUSE named (a runtime relation carrying a history-range
  outcome, and the reverse) now **refuse**.

**No copied boolean alone proves authorization.** `admit_evidence_requirement` returns
`(plane, None)` and grants nothing; the closed-world gate reads the evidence Run's own
`deadCodeRepairEligible` **before any descriptor exists**, `applicable` is false whenever any
requirement is unsatisfied, and apply still requires an authorization bound to the exact
`repairPlanId`. The imported law states outright that no imported outcome changes
`deadCodeRepairEligible`. These are **trusted admitted model inputs**, not production measurement,
and I do not claim otherwise.

### CB6-MUST-2 — TypeScript config node `kind` · **corrected and verified**

A closed, normative path→`kind` law is published beside the field and **read** by the model rather
than restated. It is the **exact, case-sensitive basename** over a two-member table, total, applying
to **every** node including non-entry ones.

- **22/22** discriminating paths agree with my independent expectation: no prefix inference
  (`tsconfig.build.json`, `tsconfig.base.json`, `tsconfig.jsonc`, `jsconfig.build.json` are all
  `other`), no case folding (`TSConfig.json`, `TSCONFIG.JSON`, `Tsconfig.json` all `other`), no stem
  or suffix matching, and the final path segment decides even when a *parent directory* is named
  `tsconfig.json`.
- The law's own **7** published examples agree with the model.
- **The prose in §2.2 agrees clause by clause.** The law's `driftScope` explicitly declines to claim
  prose agreement and calls it a review obligation. I discharged it, and it holds.
- **Valid retained contexts remain usable**: 6 positive controls admit, including the load-bearing
  one — an explicitly selected **custom-named entry** whose kind is `other`, which still derives
  `configOrigin=tsconfig`. `other` is not a refusal.
- **A wrong kind refuses**: 7 negative controls, including a relabelled entry, a relabelled
  **non-entry base**, the prefix-convention reading, and case folding.
- The identity consequence is real and measured: the two readings of one repository mint two
  different `tsconfigGraphHash` values (`4ff62816…` vs `0817c006…`), and only the exact reading
  admits — so the ambiguity is removed *at admission*, not merely described.

One point worth stating precisely, because it is easy to get wrong. The v16 model already contained
an inline restatement of this rule. I compared the removed inline rule against the newly published
table over 25 paths including edge cases: **0 disagreements.** So **publishing the authority moved
no derived value.** The fixture identities that move do so because the schema *document* digest
changed, not because any `kind` changed — and I do not describe any changed schema document as an
unchanged exact preimage.

### CB6-SHOULD-1 — command → operation map · **corrected and verified**

One owned closed map, publishing four things it keeps apart by name. I recomputed rather than
restated:

- **45** commands, **24** operations.
- The **20** generic rows are **exactly** the commands carrying a `mutation` step, recomputed from
  the command inventory. Every row names a real command and a registered operation, and every row's
  `requestClass` matches the inventory's own value (0 mismatches).
- **Every operation is accounted**: 0 unaccounted, 0 over-accounted. I independently recomputed the
  set of operations bound by no command and no step kind and got exactly `["config-write"]` —
  matching the disclosure precisely.
- **Specialized versus generic is enforced, not asserted.** At the *actual field schema*, both
  generic fields (`MutationParams.mutationClass` and `MutationReplayScopeV1.operation`) admit all
  **23** admissible tokens and refuse **exactly** `repair-apply`. So the dedicated repair apply
  cannot be promoted into a generic mutation. And no implicit config write is invented:
  `config-write` has no command row, no step-kind binding, and no command bears that name.
- **Replay preimage law**: `MutationReceiptV1` requires **both** `operation` and `idempotencyKey`;
  `ImportResult` and `NativePreparationResult` both require `receiptId`; the preimage fields match
  the declared recipe, and the key I recomputed is deterministic and moves with both the operation
  and the requestId.
- **Authority separation** is explicit — the map states it is not a request grammar and grants
  nothing — and injectivity is correctly *not* assumed: `import` really is shared by the `analyze`
  and `import` commands, which I confirmed from the inventory's own step lists.
- The renamed rows are **4**, not 3, including the execution-class `native-prepare` — the map's own
  CB6-NEW-1 correction, which my recomputation confirms.

### CB6-SHOULD-2 — coverage partition · **corrected and verified, at full Run closure**

The two halves are separated and the disjointness half is **enforced at retained-Run closure**, not
merely reconciled in text. The identity model **reads** the published five-field `partitionKey`
from the registry rather than restating it.

My controls here are **full admitted Run graphs**, because this change affects closure:

| Control | Outcome |
|---|---|
| baseline fixture **(positive)** | **ADMIT** — `run2:5e215948…` |
| same partition tuple, shared subject | **REFUSE** — `SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:foo` |
| same tuple, disjoint subjects **(positive)** | **ADMIT** — `run2:67765bf2…` |
| different rung, shared subject **(positive)** | **ADMIT** — `run2:575c3ec2…` |
| **two scopes that BOTH lack a Coverage entry, overlapping** | **REFUSE** — `…:zzz/shared.ts` |
| the same two-scope shape, disjoint **(positive)** | **ADMIT** — `run2:93e4bcf9…` |
| empty subjects array **(positive)** | **ADMIT** — `run2:24060945…` |

The fifth row is the load-bearing one: **both** overlapping scopes lack a Coverage entry, which the
per-Coverage producer guard structurally cannot see because it admits one scope at a time. Only the
per-view closure boundary can decide it, and it does. Five positives close complete Runs with real
distinct `run2:` identities; the refusals carry the exact published refusal shape.

**Totality is owed only as the registry declares.** Of **13** relations, exactly one — `file` —
carries a `coverageTotality` row, so the nine symbol relations owe none. **Symbol-to-file
attribution remains trusted where the contract says so.** I did not reconstruct it and I make no
claim to have.

## 6. The three advisories, on the actual chosen wording

**CB6-ADV-1 — js-synthesized vs U-1.** The table now says outright that it *selects a mode and
discovers no unit*. The unit prerequisite is scoped to exactly the **five rows naming a compilation
universe**, which the text enumerates; `syntax-only` explicitly carries no such prerequisite and is
named as the compiler-free path for a repository where U-1 yields no TS or Rust unit. The
bare-`.js`-directory case is decided explicitly — not a unit, `syntax-only` with reason
`no-program-unit-for-language`, `unitOrdinal: null` under U-4 — and the unreachable disjunct, plus
*why* it was unreachable, is preserved as history rather than deleted. Severity retained.

**CB6-ADV-2 — the confidence clause.** I assessed the **actual chosen wording, not the blind
reviewer's inferred types-only reading**, as required. The design deliberately selects the *wider*
global provider-emission law and explains that narrowing it to `types@checked` would be a
**weakening** that readmits fabricated percentages for other relations. I verified the structural
claims the distinction rests on: `TypeDerivationV1` pins `confidenceMillionths` as a schema `const`
1000000 with `confidenceMethod` `const native.confidence.v1`, while `ViewEntryV3` carries the full
0…1000000 domain and **no** `confidenceMethod`. The blind reviewer's counterexample is correctly
re-classified rather than adopted: the named regression case is a hand-built **evaluator input** —
not a `ViewEntryV3`, not provider emission — so it is no counterexample to the emission law, and the
wider domain is what keeps §4.6 step 3 reachable for a defective provider. The imported example is
removed *with a reason* (imported evidence mints no `ViewEntryV3` at all) rather than silently.
**I agree with the selected law.** This is a design selection, correctly distinguished from a
defensive fixture, and the severity is retained.

**CB6-ADV-3 — the D9 extension.** The inherited `d9-exit-contract.v1.14.json` is **byte-untouched**
(`8dd33038…`). The successor adds one `faultCause` (`host-invariant`) mapped to
`SYSTEM.OUTCOME.ILLEGAL_STATE`, which is **already** a member of the inherited **19**-member closed
error-code vocabulary; the cause has no preimage in either inherited map; the successor map stays
injective and adds **no new error code**. So it is a vocabulary extension over an immutable
historical artifact, disclosed as a future integration obligation that **remains unperformed**.

*(A correction of mine: my first measurement checked only the values of `faultCauseToErrorCode` and
concluded the error code was absent. It is present at `codeVocabulary.errorCodes[18]`. The corrected
measurement is the one relied on, and the blind reviewer's original claim was right.)*

## 7. All nineteen additional source findings

Each is individually accounted in `review.json`. The ones carrying independent measurement here:
CX-BV6-01 (verified by the full-Run partition controls), CX-BV6-02 (the ten agreeing presence-law
cases), CX-BV6-03 and BV6-V3-IMPORT-CAUSE/BINDING/SEMANTICS (the per-kind and projection results
above), CX-BV6-04 and BV6-V3-RECEIPT (the recomputed map and required receipt fields), CX-BV6-05
(§1.2/§1.4), CX-BV6-06 (the projection law), CX-BV6-07 and CX-BV6-08 (the four precision items and
the disclosed v1 evidence corrections), CB6-NEW-1..4, and BV6-V3-PRECISION / BV6-V4-CR-1 /
BV6-V5-CR-1.

On the last three, the retired false rationale — *"the schema cannot decide them because `relation`
is a CanonicalIdentifier, not an enum"* — I scanned all **140** non-review documents under the two
owning trees. The retired causal claim occurs **zero** times in any normative document, and the
affirmative replacement (*"deliberately leaves the authoritative registry lookup to admission"*) is
present in all four named carriers. Its 7 remaining occurrences are quotations inside `finding`
fields of the disposition record — preserved history, which is correct. The deliberately retained
neighbouring check id `repair.the-schema-alone-cannot-decide-the-plane` is present and is accurate
of that schema as written.

## 8. What the delta did to admission

I diffed structurally rather than reading summaries.

**Across all six changed schema/registry documents: zero structural pointers changed and zero
widening-key pointers changed.** Every structural delta is an *addition*. There is exactly **one**
structural removal in the entire delta —
`repair.schema.json#/$defs/EvidenceRequirement/properties/deficiency/$ref → D9Deficiency` — and that
removal **is** the CB6-MUST-1 correction. `D9Deficiency` and `DeficiencyV2` enums are unchanged; two
new `$defs` were added and none removed; relation-registry membership is untouched.

**Executable lines, comments and docstrings stripped by tokenizing:**

| File | +/− executable | refusal-bearing removed |
|---|---|---|
| `workflows_model.v1.py` | +180 / −1 | **0** |
| `native_evidence_model.v2.py` | +5 / −2 | **0** |
| `identity-model.py` | +15 / −0 | **0** |
| `check-identity.py` | +91 / −0 | **0** |
| `check_workflows.v1.py` | +401 / −2 | 1 (harness) |
| `check-integration.py` | +140 / −0 | **0** |

**Not one refusal-bearing line was removed from any model.** I read all three removals:

1. The native model's removal is the **inline restatement** of the kind rule, replaced by a read of
   the published table — and I measured that both derive identical values over 25 paths.
2. The workflows model's single removal is an unmet-precondition append that now has a **new
   admission gate ahead of it** (`admit_evidence_requirement`, which runs for satisfied requirements
   too) and carries the rung, plane and exact cause. Strictly stronger.
3. The checker's two are harness lines replaced by **stricter** versions that additionally assert
   `errorCode` equality and an expected remedy substring.

**No grammar, no authority and no admission was widened.**

## 9. Preserved prior corrections

All **14** corrections I am required to keep in view have live anchors in the frozen bytes:
capability/default/availability composition; the Unicode 15 lib-name conversion assumption
(including the `ReferenceEnvironmentError` that keeps an environment fault from being laundered into
a typed refusal); body-language and compiler-dialect ownership; anchor cardinality and file
totality; registered payload and digest annotations; typed canonical equality; imported observations
and ScopeDocument binding; static/runtime evidence distinctions; cache admission; repair
projection/replay; purge disclosure; output failure after a committed Run; the new coverage
partition law; and the closed-world gate before any descriptor exists.

This is **preservation** evidence — a live anchor plus a governing suite that executed and passed on
those exact bytes, combined with zero structural schema change, unchanged registry membership and a
refusal-only executable delta. It is **not** a first-principles re-derivation of each correction.

*(Two of my anchor patterns were initially wrong — one case-sensitive, one naming a relation the
model reads from the schema registry rather than spelling literally. Both anchors are in fact
present; the corrected patterns confirm 14/14.)*

## 10. Two new findings — both advisory

### V17-ADV-1 — a prose `rule` string sits as a pseudo-row inside a relation-keyed map

`imported-evidence.schema.json#/x-opensip-imported-requirement-law/perKindApplicability` is a map
keyed by imported relation name whose values are outcome arrays. It carries a **third key**, `rule`,
whose value is a prose string. That map is cited **by name** as the per-kind authority in the repair
schema's `x-opensip-vocabulary`, at two sites in `workflows_model`, and in the checker — so a reader
deriving *"which kinds have applicability rows"* from the published authority gets three kinds, one
of which is not a relation and whose value is not an outcome list.

This is inconsistent with the contract set's own convention, which everywhere else places a prose
`rule` as a **sibling** of the data it describes: `x-opensip-config-node-kind-law` has `rule` beside
`basenames`, `RELATION-LADDER-DOMAIN-V2` has `rule` beside its registry, and **this very law block
has `precedenceRule` beside `precedence`.**

*Not a MUST or SHOULD.* No admission outcome is wrong today: every actual reader indexes by an
explicit relation key, and at the model site the relation is already known to be one of the two
imported relations because the plane test precedes it, so `rule` is never reached as a row. I found
**zero** readers that iterate the map generically. Both real rows are precise, and the prose value
is transparently not an outcome list, so no conforming implementation is misled about either real
relation. The cost is verification friction — a conformance check asserting "every imported relation
has a row and every row names an imported relation" fails on these bytes. *Repair:* move the string
to a sibling `perKindApplicabilityRule`, matching `precedenceRule` directly above it.

### V17-ADV-2 — the V16-ADV-1 provenance defect recurs on the sibling item it was compared against

`advisory-application-account.v17.proposed.json#/items/44` (V14-ADV-2) pins
`foundation/relation-payload-schemas.v2.json` at `ef0c244e…`, the **v16** digest. That file is one of
the 17 changed source files in this candidate — it gained `coveragePartitionLaw` under CX-BV6-01 —
so the frozen v17 digest is `53380a24…` and the pin no longer resolves. Unlike its sibling, item 44
carries no `sourceCorrectionContext`, no historical label and no current-source binding.

**V16-ADV-1 was properly discharged for item 43.** That item now carries an explicit as-of-v15
label (*"Historical as-of-v15 correction pin; preserved without retrospective repinning"*), an
as-of-v16 pointer, and a `currentSource` binding which I verified equals the frozen bytes exactly.
That is the better of the two remedies the v16 review offered, because it preserves history. But the
same remedy was not extended to the sibling — and the v16 review had explicitly noted that item 44's
pin *"resolves only because its file happened not to change."* That contingency has now expired.

*Not a MUST or SHOULD.* Nothing normative is affected and no admission changes. The substance of
V14-ADV-2 survives in the current bytes: I confirmed `relation_payload_rules` is still invoked inside
`open_run_closure`. This is provenance friction — the same defect the v16 review and the candidate
both graded advisory, so I grade it the same way. *Repair:* apply the item-43 pattern to item 44. No
historical byte need be rewritten.

Across the whole governance corpus I resolved **522** current pins and **22** explicit as-of
historical pins; item 44 is the **only** unresolved pin not marked historical.

## 11. Registers — preservation, not grades

Every owning register document is **byte-identical to its v16 manifest entry**, which is the
cleanest available preservation evidence.

- **16 AR rows** — CARRIED-UNCHANGED (`architecture-depth-review/REVIEW.md` and the crosswalk byte-identical).
- **15 FW rows** — CARRIED-UNCHANGED (`current-source-map.proposed.md` byte-identical and absent from the changed-path set).
- **27 inherited residuals** — CARRIED-UNCHANGED: DR-001…DR-011 (11) plus the DR-011 subledger R01…R16 (16). *DR-012 appears only in the document's header prose as an explicitly excluded item — "DR-012 remains release qualification" — and is not a table row.* DR-011-R10 states outright that it cannot be closed by that table and needs an actual fresh blind implementer litmus, which this review does not supply.
- **30 evaluation subresiduals** — CARRIED-UNCHANGED; owning file byte-identical.
- **5 scoped review owners (DR-201…205)** — ROUTING-ASSESSED-ONLY-NOT-APPLIED.
- **32 qualification gates** — all `demonstrated: false`, `qualified: false`. Unperformed, and this review performs none.
- **Carried advisory account 50 → 55**: five added (CB6-ADV-1/2/3, V16-ADV-1, V16-ADV-2), **zero removed, zero severities changed**. My own V17-ADV-1 and V17-ADV-2 are **not** in that account and any future application must account for them separately.

**On the five owner rows, explicitly: `appliedByThisReview = false` and
`finalApplicationOutcomeGranted = false`. The precise scope is that five owner routing assessments
do not grant a final application outcome and are not a grade.** CARRIED-UNCHANGED and ROUTING-ONLY
are likewise neither new grades nor final application outcomes. **No grade is granted anywhere by
inference.**

## 12. Evidence honesty

I distinguish what each result is:

- **Schema-level**: the vocabulary joins, the presence law, the generic field domain, the required
  receipt fields, and every structural diff.
- **Helper-level**: `config_node_kind`, `typescript_config_graph_faults`,
  `admit_evidence_requirement`, `sufficiency_v2`, `mutation_replay_key` and the target projection
  are reference *model* functions over synthetic in-memory inputs — trusted admitted inputs, not
  production measurement, and no host, compiler, Cargo, provider, repository, renderer, ledger or
  operating system executed. Python file IO and `hashlib` SHA-256 did execute, here as there.
- **Full Run closure**: only the CB6-SHOULD-2 controls are complete admitted Run graphs. Where a
  change affects closure I used full Runs; **schema fragments are nowhere claimed to prove full
  Runs.**
- **Executed expectation**: all six reference commands, with pre-written expectations, in two
  byte-exact copies.
- **Narrative**: statements of intent, rationale and history — including the candidate's own
  dispositions — are narrative and are reported as such, never as measurement.

**First actual refusal boundary**, stated precisely because it differs per finding. For the imported
per-requirement plane it is `workflows_model.admit_evidence_requirement` raising `CONFIG.INVALID`;
the owning schema deliberately does **not** refuse a cross-plane value, and I measured exactly 50
cases where the consumer refuses and the schema admits. For the config-node kind it is
`typescript_config_graph_faults` reporting `native.config-graph-kind-contradicts-path`, ahead of
universe admission — and the law correctly states that a candidate digest *may already have been
computed*; what never happens is admission. For the coverage partition it is `close_run` raising
`SUBJECT_SCOPE_PARTITION_OVERLAP`, and **not** the per-Coverage producer, which structurally cannot
see a second scope.

**On blind v6**, I preserve the root qualifications as written: it constructed 355 CAS objects, but
its four claimed complete Run graphs refuse `close_run` for missing retained schema bytes, and
separate policy/waiver schema checks fail; its 83 negative-labelled controls include 3
positive/hash-distinction controls; some assertions are narrative. Its original report remains
literal historical evidence. **Those helper limits do not erase the normative gaps it identified**,
and they do not turn precise existing text into a design omission — which is why all four of its
findings are dispositioned on their merits above.

No blanket coverage claim is made. Every count above is tied to a specific executed output.

## 13. Failed attempts — all mine, all preserved

Four probe failures are preserved with their corrected successors, plus four scanner/measurement
corrections:

1. **Wrong fixture shape** — I used `entry` instead of the schema's `entryConfigPath`.
2. **Unsorted `nodes` array** — the record carries `x-opensip-order {by:[path]}` and the digest path
   correctly refused it. Worth noting: the *fault checker* does not validate order; the *digest* path
   does.
3. **Wrong ladder authority** — I read `RELATION_LADDERS` from the identity model; ladders live in
   the relation registry, which is the single published ladder authority.
4. **A degenerate control** — my first overlap control built a second subject-scope byte-identical to
   the first. Subject-scopes are content-addressed, so it collapsed onto the same id and added
   nothing; the Run admitted **with the baseline's own run id**, which is how I caught it. Corrected
   by giving the second scope an extra subject so it is a distinct record that still shares one
   subject and the full partition tuple — it then refused, as the law requires.

Plus: the native pin-registry parser (`primaryReferences` before `pins`); the cross-reference
resolver (record-relative custody paths, and `subjectManifestSha256` mis-paired as a file digest,
which produced 304 false positives before correction); two anchor regexes; and the too-narrow D9
error-code lookup. **Not one was a design failure**, and in every case the correctly constructed
controls in the same run already agreed.

One honest limit of my evidence: `historical-preservation-report.v17.json` names **31** files, of
which only **10** lie inside the frozen subject slice. Those 10 match their `currentSha256` exactly.
The other **21** are outside the subject, so I **cannot** verify them from the frozen bytes. I state
that as a limit of my evidence, not as a finding against the candidate.

## 14. What this does not claim

Source and design acceptance coexists with a **pending**, independently reviewed application. This
review invents no grade authority. **D-372 is unapplied, condition 5 is NOT MET, the readiness
register is unchanged, and no implementation is authorized** — the register itself still reads
*"Implementation remains forbidden until condition 5"* and *"Condition 5 remains last and
unauthorized."*

I claim **no blind reconstructability**. A **new independent blind consumer reconstruction** over
these accepted normative bytes is a separate act, still required, and this review cannot supply it —
a point made sharper by the fact that the v16 ACCEPT did not survive exactly that step.

No product, platform, compiler, storage or cryptographic qualification is claimed or implied. All
32 qualification gates remain unperformed. The intended product remains **one complete design
implemented in stages**, over native TypeScript/JavaScript/Rust plus bounded bundled grammar modes
and four selected macOS/Linux machine ids; no provider, OS, compiler, crypto or storage
qualification is invented here.

## 15. Required next acts

1. A **new independent blind consumer reconstruction** over these accepted normative bytes.
2. A complete, **independently reviewed application and readiness reconciliation**.
3. Optionally, the two nonblocking clarifications **V17-ADV-1** and **V17-ADV-2**, at their stated
   advisory severity.

---

**Verdict, bound to the exact frozen bytes.** Against
`8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c`, whose 7671 files I verified by
digest and length before and after, all four blind-v6 findings and all nineteen additional source
findings are corrected **in the admission**, not merely in prose — and I reproduced each refusal at
its own real boundary while every positive control still admits, using complete Run graphs wherever
closure is affected. The delta widens no grammar, no authority and no admission: zero structural
schema pointers changed, registry membership is untouched, no refusal-bearing line was removed from
any model, and publishing the config-kind authority moved no derived value. The two findings I raise
are advisory and change nothing at admission. **ACCEPT**, for source and design only, with blind
reconstruction, application and readiness all still open.
