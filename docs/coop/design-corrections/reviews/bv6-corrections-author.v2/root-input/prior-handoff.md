# bv6-corrections-author.v1 — correction coauthor handoff

**Role.** Correction **coauthor** working with Codex on the fresh blind consumer-B
v6 report. Not an independent reviewer, not an accepting reviewer. No product
implementation, no agents, no commit, no push, no publication. Every write is
under `/tmp/opensip-design-corrections/bv6-corrections-author.v1`.

**Technical assent: TRUE**, to the exact bytes listed in §5 as a correct, minimal
and mutually consistent disposition of all seven listed blind v6 items plus the
three new findings in §4. It asserts nothing about independence, acceptance,
readiness, qualification, or any file outside that list.

---

## 1. Custody

| Check | Result |
|---|---|
| Blind report `blind-review.json` SHA-256 | `f4c77a7a…d200a5f2` — **verified** |
| Frozen manifest `candidate-subject.v16.json` SHA-256 | `ca5f36d4…44042ee9` — **verified** |
| Declared files | 6839 |
| Verified **before** any edit | 6839 matched, 0 missing, 0 mismatched, 0 undeclared |
| Verified **after** all edits | **14** changed, 0 missing, 0 undeclared |

The report says "2 MUST, 2 SHOULD, 2 advisory" in its heading but lists **three**
advisories (ADV-1/2/3), and the JSON carries three advisory objects. Three is the
actual content; all three are dispositioned below. The original report is
preserved unedited.

---

## 2. What I did first

I ran the six reference commands on the **unmodified** work copy and re-verified
the tree byte-identical to the manifest afterwards. Baseline: foundation 231,
identity 1331, security 456 + 10 sweeps, native 347 cases, workflows 1598,
integration 365 — all pass. Every count in §6 is a delta against that baseline.

I then read the actual producers and consumers for each item rather than the prose
alone. That is where the two disagreements in §3 and §4 came from.

---

## 3. Dispositions — all seven, with disagreement recorded

### CB6-MUST-1 (was MUST-1) — `EvidenceRequirement.deficiency` — **AGREE, CORRECTED**

Independently confirmed, against the frozen bytes:

* `DeficiencyV2` has 9 members, `D9Deficiency` 10; the difference is exactly the
  four the report names.
* `DomainDetailCode` carries a **different** five (`budget-exhausted` plus those
  four). The two vocabularies overlap in `budget-exhausted` alone, their union is
  all nine, and neither alone is. The report characterised this exactly.
* `sufficiency_v2` is **total** and its result shape is closed: `satisfied=true`
  carries no deficiency; `satisfied=false` carries exactly one `DeficiencyV2`
  member.
* `repair_preview` took the requirements as a caller input and read only
  `satisfied`. The single retained fixture was `satisfied=true` with the field
  absent, so **the field had never been exercised in any direction.**
* The other four `D9Deficiency` sites are whole-Run and comparison-step
  terminations — which is why widening it was refused.

**Chosen remedy: the report's first option, retype the field**, on the merits.
Option 2 (write the D9-mapped value) is lossy in exactly the case that matters:
all four successor members map to `verdict-indeterminate`, which cannot
distinguish `resolution-incomplete` — the §4.6 step 6 outcome a destructive
unused-code repair turns on — from three unrelated causes. Option 3 adds a second
field to an identity-bearing record to carry a value the first can now hold.

Published, consistently across schema, prose and reference:

* `common#/$defs/NativeSufficiencyDeficiency` — the nine members in the authority
  order, annotated as a **generated/drift-checked mirror** of
  `native-evidence.schemas.v2.json#/$defs/DeficiencyV2` (the workflows bundle
  takes no cross-bundle `$ref`), with cross-unit parity held in
  `check-integration.py`.
* A **presence law**: `deficiency` is REQUIRED when `satisfied` is false and
  FORBIDDEN when true — schema-enforced *and* admitted again at the boundary by
  `admit_evidence_requirement`, which **returns the exact cause, never a boolean**.
  All three previously conforming readings are now refused or impossible.
* `perRequirementConsumerBoundary` in the native deficiency-cause registry, naming
  the producer, the consumer record, the ownership and the drift rule.

Held apart, as required: the **native outcome**; the **public D9 termination**
(unchanged, still §10's class/code columns); the **retained cause carrier**
(unchanged); and the **satisfied state**. `D9Deficiency` is byte-unchanged, its
four other uses are untouched, and `evidenceOrigin` and the
`imported-prepared-declared` unsafe-repair refusal are unchanged, so import
semantics are preserved.

**Not an authorization.** `applicable` is still false whenever any requirement is
unsatisfied; authority remains the sealed Run named by `evidenceRunId`; apply
still needs an authorization bound to the exact `repairPlanId`, and every edit to
the value mints a different one.

**Meaningful positive and failing requirements exist now.** The retained satisfied
requirement is byte-unchanged; two admitted **failing** requirements
(`resolution-incomplete`, `external-consumers-unknown`) each produce a schema-valid
not-applicable plan whose unmet precondition carries that exact cause — and a
control fails if the two remedies become indistinguishable.

### CB6-MUST-2 (was MUST-2) — config node `kind` — **AGREE, CORRECTED**

The rule existed only as an inline literal in `typescript_config_graph_faults` and
was stated in no schema and no prose. It is already total over every node,
case-sensitive and exact — so the reviewer's exact-basename guess matched the
model and did not distort the reconstruction, but it was still a guess.
`configOrigin` reads only the entry's kind and both `other` and `tsconfig` derive
`tsconfig`, so nothing pinned it.

The identity consequence is real and is now **computed**, not asserted: the two
readings of one repository mint `tsconfigGraphHash` `c5a10868…` (exact) versus
`76108059…` (prefix).

Published by the CB4-SHOULD-2 pattern: `x-opensip-config-node-kind-law` as a
top-level authority, an `x-opensip-vocabulary` annotation on the field naming it
and the identity path it moves, the rule in §2.2 prose — and the **model now reads
the table** instead of restating it, so the three cannot drift. Coverage includes
non-entry nodes (the discriminating control), `tsconfig.build.json`,
`tsconfig.base.json`, case variants, `.tsconfig.json`, `tsconfig.jsonc`,
`jsconfig.build.json` and a custom-named selected entry. No enum member, no field
and no derived value changed; every existing fixture and refusal is byte-identical.

### CB6-SHOULD-1 (was SHOULD-1) — command → operation map — **AGREE, CORRECTED (count refined)**

All three named mismatches confirmed. 45 commands, 24 operations, 20 with a
generic `mutation` step, three more with a dedicated mutating step.

Published as **one owned machine-readable map** beside the enum
(`x-opensip-mutation-operation-map`), keyed both ways, each row carrying
`mintedByStepKind` and `requestClass` so inventory request classes and generic
operations stay distinguished. The report's other option — add `mutationClass` to
the Command record — would widen the closed 45-row record and force a per-row
answer for the 22 commands that mint nothing.

**`repair-apply` was not accidentally enabled.** It was already excluded from both
`MutationParams.mutationClass` and `MutationReplayScopeV1.operation` by an explicit
`not`; both are untouched, and a control proves it still refuses in both positions
while all 20 generic classes admit. Nothing was widened: still 24 operations, 45
commands, no new request class, step kind or replay authority.

### CB6-SHOULD-2 (was SHOULD-2) — the partition clause — **AGREE, CORRECTED as text in both documents**

Confirmed: `coverageTotality` has exactly one row (`file@enumerated`) and
`identity-model` reads it rather than hardcoding; the nine source-text (symbol)
relations have none; the full owning tuple is the registry's own `matchOn`.

Written into **both** contracts so a reader arriving at either is not left to
reconcile them: disjointness is the general rule over the full
`(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` tuple;
omission is owed only where the registry has a row; symbol relations are a
**stated trust boundary**, not an omission. Completeness is explicitly **not**
vacuous — RC-0/1/2, `examinedUniverse` counts and the partial/not-attempted/unknown
states still decide it, and the snapshot/ownership joins are unchanged. I did not
claim symbol attribution is re-derived, and I did not claim disjointness is
enforced at closure — see CB6-NEW-3.

### CB6-ADV-1 — `js-synthesized` vs U-1 — **AGREE, CLARIFIED**

`discover_units` is marker-driven; `discover_units(markers={})` returns no units,
and `typescript_mode` is only ever reached for an already-discovered unit. The
recognition cell now reads as **mode selection inside a U-1 unit**, with a new
paragraph stating the table discovers no units, plus a negative case (bare `.js`,
no unit) and a positive one (same files under a `package.json` marker). No implicit
compilation unit is created and U-1 is unchanged.

*One correction to both the report's wording and my own first draft:* the model
classifies a marker-less `.js` file as `syntax-only` with reason
`no-program-unit-for-language`, not `grammar-only`. The prose now uses the model's
spelling.

### CB6-ADV-2 — the confidence clause — **PARTIAL: agree it needed scoping, DISAGREE with the reviewer's resolution**

I did **not** adopt the types-scoped reading. What the artifacts actually show:

* `native.confidence.v1` appears in exactly one record —
  `TypeDerivationV1.confidenceMethod`, a `const`, whose `confidenceMillionths` is
  the `const` 1000000.
* `ViewEntryV3.confidenceMillionths` is an integer 0…1000000 in a **different
  record** and carries **no** `confidenceMethod` at all.
* The named 100000 regression case passes a **hand-built dict** straight to
  `sufficiency_v2`. It is not a `ViewEntryV3` and **fails** `ViewEntryV3` admission
  (`'closedWorld' is a required property`). No provider emitted it.
* No producer in the model emits below 1000000; both retained coverage fixtures
  carry 1000000.

Scoping the emission clause to `types@checked` would **weaken** it — it would
permit a native `clones` or `references` provider to emit a fabricated percentage,
which is exactly what §4.8 removed. The published scope is therefore the stronger
one: a **declared-exact native provider emission law across the bundle**, with
step 3 reachable because it compares the deliberately wider `ViewEntryV3` field, so
an imported, non-native or defective contribution is still judged. The 100000
fixture is published as a **defensive evaluator fixture outside provider
emission**, and the contract now says so; no claim is made that the product emits
such a value.

### CB6-ADV-3 — the successor D9 artifact — **AGREE, CARRIED FORWARD as mandatory**

Confirmed: the inherited enum has 11 faultCause members without `host-invariant`;
`faultCauseToErrorCode` has 10 rows and no preimage for it;
`SYSTEM.OUTCOME.ILLEGAL_STATE` was already in the inherited closed 19-member
errorCode vocabulary, so the successor adds no code and the map stays injective;
the selected `D9FaultCause` is exactly the inherited set plus one.

Added `successorArtifactObligation` to the public route registry — standing
**MANDATORY / LIVE / CROSS-UNIT** — and a §10 paragraph distinguishing the
**current selected extension** (complete and self-sufficient as the law the product
source carries) from the **future integration and qualification** owed by the D9
unit. `d9-exit-contract.v1.14.json` is byte-unchanged
(`8dd33038…cdf7da31`) and is not in the changed-source list; repinning it is
explicitly refused in the published text and held by a control.

---

## 4. New findings

**CB6-NEW-1 — the name mismatch is four rows, not three.** The report's three are
correct for the ten *mutation-class* commands. The execution-class `native-prepare`
also does not share its operation's name (`native-preparation`). Counting only the
mutation-class commands would leave one command's operation still underivable —
the exact defect the map exists to close. My own first draft reproduced the
report's three; **the totality control I wrote caught it.** `renamedRows` now
carries four and is held *equal* to the derived set, so a later rename cannot enter
the vocabulary without appearing there.

**CB6-NEW-2 — `config-write` is an operation no command mints.** Across the whole
live tree it occurs in exactly one place: the `MutationOperation` enum. Published
as `operationsWithNoCommand` with a disclosure rather than removed (a vocabulary
change this correction does not own) or given an invented command.

**CB6-NEW-3 — Coverage-scope disjointness is stated, not enforced.** §3 asserts
scopes partition "without overlaps or omissions". The **omission** half is enforced
for `file@enumerated` by `coverage_inventory_totality`. The **overlap** half is
enforced **nowhere** — there is no pairwise disjointness check over scope subjects,
although it is decidable from the retained scopes. That is the same class of defect
this contract set has corrected before. **I deliberately did not add the refusal:**
a new admission could refuse Runs lawful under the frozen bytes, and SHOULD-2 asked
for a text reconciliation. My wording therefore states disjointness as a producer
obligation and claims no closure enforcement. Recommended for the next pass or for
the successor blind review.

---

## 5. Changed source — 14 files, complete, with before/after SHA-256

All relative to the proposed source copy
`/tmp/opensip-design-corrections/bv6-corrections-author.v1/work`. Per-file edit
summaries are in `handoff.json#/changedSource[].edits`.

| Path | before → after |
|---|---|
| `docs/coop/design-corrections/check-integration.py` | `df9fbb2e…66be071f` → `cabb75b3…0719d01c` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `2724276f…ad33ab48` → `c32dc28d…db87d0f3` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `5740aed5…9f00dfce` → `07d990e2…60507225` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `2a5fc493…8092cc0f` → `f85e3950…6fe4ad85` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `8301e8e3…17447b18` → `01b517d3…cca9d86c` |
| `docs/coop/design-corrections/workflows/check_workflows.v1.py` | `0af791d5…eea8fbaf` → `d10faaf3…d79896c9` |
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | `3f84dff2…abe17a8a` → `89774dff…1ff39401` |
| `docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json` | `3b89b739…082a4814` → `cf3f7543…a7a0b089` |
| `docs/coop/design-corrections/workflows/schemas/repair.schema.json` | `b8fe3464…a8f8dc3d` → `aefc4c47…25a47501` |
| `docs/coop/design-corrections/workflows/workflow-cases.v1.json` | `688506e6…bb0ec93a` → `3f4bcb99…f0f73dc6` |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `8d45d115…5a99793b` → `4c4754d4…51926e97` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `64a2a019…c72fb8b3` → `83ae8f12…86521914` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `b50c814c…acbd3fea` → `7c925f57…1af15063` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `4a5f0c4e…2e263742` → `48bdbfdb…d8ea6e01` |

Digests are abbreviated to first and last eight hex characters for reading; the full
untruncated values are in `handoff.json#/changedSource` and are the authoritative ones.

**Not touched:** the blind report and its output directory; anything under
`docs/coop/design-corrections/reviews/`; every generated report; all four
source-pins manifests in the proposed copy; the correction crosswalk, historical
preservation reports, post-reset dispositions, qualification gates and validation
summary; `d9-exit-contract.v1.14.json` and every other inherited artifact; and the
live repository, which was read-only throughout.

One accidental write, corrected and disclosed: an early exploratory run of
`check_native_evidence.v2.py` inside `work/` overwrote the generated
`native-evidence-report.v2.json` with a short stale-pin failure report. It was
restored byte-exactly from the frozen snapshot and is not in the changed-source
list; the final manifest comparison confirms 14 changed files with no generated
report among them.

---

## 6. Executed commands and results

Run in a **separate disposable repinned copy**,
`disposable/checker-run.v1`. The proposed copy was **never** repinned — its four
source-pins files are byte-unchanged and therefore stale, which is expected and is
neither a product failure nor a PASS. Root refreshes pins after the final source
and records, then runs the six and freezes the successor.

**Disposable-copy deltas, disclosed in full:** it excludes
`docs/coop/design-corrections/reviews/` except the three author-feedback files the
pin manifests name (copied in individually); `repin.py` refreshed **50** pin rows
across the four manifests; and the six checkers rewrite their own report files
there. All of that exists only in the disposable copy.

| # | Command | Result | Δ vs baseline |
|---|---|---|---|
| 1 | `foundation/check-foundation.py` | PASS 231/231 | 0 |
| 2 | `foundation/check-identity.py` | 1338 passed, 0 failed | +7 |
| 3 | `security/check-security-lifecycle.v1.py` | 456/456, 10 sweeps true | 0 |
| 4 | `native/check_native_evidence.v2.py` | PASS 355/355 cases, uncovered feedback `[]` | +8 cases |
| 5 | `workflows/run-reference-checks.py` | pins valid, 1672/1672 | +74 |
| 6 | `check-integration.py` | 378 passed, `failed: []` | +13 |

**Intermediate failures, retained rather than smoothed over.** The
`renamedRows` totality control failed on its first run and exposed CB6-NEW-1; the
map and prose were corrected and **the control was not weakened**. The ADV-3
disclosure control failed because the obligation lived only in `common.schema.json`
and prose, not in the native route registry — so `successorArtifactObligation` was
added there, which is what ADV-3 asks for. Two `expectError` strings and one
wrap-sensitive prose assertion were my own errors, corrected against the actual
messages; no product behaviour was involved.

**What these controls are, and are not.** *Schema-level*: jsonschema validation of
the new presence law and vocabularies, of `MutationReplayScopeV1`/`MutationParams`
admission and refusal, and of `TypeDerivationV1`/`ViewEntryV3` shape.
*Helper-level*: direct calls into the reference models. *Full retained Run*: only
the CB6-SHOULD-2 controls, which call `close_run` over a built Run graph.
*Host enforcement*: **none** — nothing here executes a provider, compiler,
renderer, ledger or filesystem, and no control shows that a host obeys any of it.

**Count honesty.** These are check rows and case rows, not distinct properties and
not exhaustive coverage. The workflows +74 is inflated relative to distinct
assertions because nine rows are one per vocabulary member and twenty are one per
generic mutation class; they are enumerated individually so a reader can see which
boundary each covers. No control asserts the model equals a second copy of itself:
the parity controls compare a mirror against the **native authority document**, and
the config-node-kind controls compare model output against the **published table
the model reads** — which is the correction, not a tautology, because before this
pass no published table existed to compare with.

---

## 7. On the blind v6 report's own evidence

The report is substantive and its four normative findings are real; root confirmed
them and I confirmed them independently above. These reservations concern the
strength of its **positive reconstruction** and its headline counts, and they
reduce no finding. The report is preserved unedited.

* The four "complete positive Run graphs" do not validate against all owning
  schemas — its policy and waiver records use `schemaVersion` where the owning
  schemas require `schemaFamily`/`schemaMajor`, and its `ruleProgramRef` carries
  different fields.
* The same CAP-1 manifest — one TypeScript provider, Rust row absent — is reused
  for the Rust and both syntax runs, so those runs do not exercise their own
  provider rows.
* The "83 discriminating negative controls" are mixed: at least one is a Rust
  positive ownership assertion (N4) and two are hash-distinction positives. It is
  not 83 typed refusals. Several others are narrative or boolean rather than
  executed refusals.
* Its canonical decoder does not demonstrate the lexical `-0` and duplicate-key
  admission it describes; its RC2 helper is incomplete; its graph-closure claims
  are asserted rather than proven by the retained code.

None of this was used to dismiss a finding. Where the report's code was limited I
re-derived the fact from the frozen source instead — which is how CB6-NEW-1 and the
CB6-ADV-2 disagreement were found.

---

## 8. Standing and limitations

* Design-reference correction over synthetic trusted inputs. **No** product
  qualification, implementation authorization or readiness grade. Passing controls
  is not qualification.
* This is **correction coauthor assent**, not independent acceptance and not blind-
  review acceptance. A fresh, genuinely independent review and a fresh blind
  consumer pass on the accepted successor bytes remain required.
* `admit_evidence_requirement` is a reference-model admission at the repair-preview
  boundary; producer conformance in a real host remains an implementation
  obligation, as the relation registry already says for the anchor law.
* Disjointness is stated, not enforced — CB6-NEW-3.
* I did not re-derive the blind review's positive reconstruction, its 78 vector
  groups or its 355 retained objects, and I make no claim about them beyond §7.
* No commit, push, publication, agent or product implementation was performed or
  authorized.
