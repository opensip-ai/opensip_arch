# bv5-corrections-author.v1 — correction handoff

**Role.** Correction coauthor (actual Claude). Not an independent reviewer, not an accepting
reviewer. **Technical assent: true**, to the exact bytes listed in §2 and to nothing else.
This grants no independence, no readiness, no acceptance, no product qualification and no
implementation authorization.

**Responds to.** The completed actual fresh blind consumer-B v5 review,
`docs/coop/design-corrections/reviews/consumer-b.v5/output/blind-review.{json,md}`, review hash
`a14fe6a4f7d5528ec7e6c084683fc69b6d5a6e84e09b72c6cb172638775c2e14`, verdict **CHANGES_REQUIRED**
(2 MUST, 2 SHOULD, 4 nonblocking advisories, one explicit checked-and-cleared non-issue).

**Subject.** My editable copy is `/tmp/opensip-design-corrections/bv5-corrections-author.v1/work`.
All 9 before-images equal their `candidate-subject.v15.json` digests; the whole-tree comparison
shows **9 changed of 6363 declared files**, with no additions and no deletions. Original archives,
frozen subjects and the blind-review directory were read only.

---

## 1. What was corrected, in one line each

| Finding | Disposition | Where |
|---|---|---|
| **CB5-MUST-1** ADM-DOMAIN successor selected by no contract | **CORRECTED** | identity §3 selects it by name; native §11 lists it; successor `standing` names both selectors |
| **CB5-MUST-2** enforced lib→component join with no published mapping | **CORRECTED** | native §2.4 + two schema descriptions publish fold / mapping / membership / equality / order / custody |
| **CB5-SHOULD-1** RC-1 undetermined for `unresolved-edge@observed` | **CORRECTED** | RC-1 replaced with a rule total over the registered `(relation, rung)` pairs |
| **CB5-SHOULD-2** `closedWorld` "copied from" a record it cannot hold | **CORRECTED** | repair schema + workflows §6 publish the 7→5 projection **and** the full-evidence authority prerequisite |
| **CB5-ADV-1** "four representations" are five tokens | **CLARIFIED** | identity §3: the four are *terminal*; `by-domain` is a selector |
| **CB5-ADV-2** `LogicalPath` overstates adoption | **CORRECTED** | description names the exactly two `$ref` sites; accepted path set byte-identical |
| **CB5-ADV-3** L0 payload length-prefixed twice | **CLARIFIED + byte example** | identity §3, historical `fact-identity-policy.v2` bytes untouched |
| **CB5-ADV-4** platform domain admits unselected platforms | **ACCOUNTED** | successor `PLATFORM-ID-DOMAIN-V1`, members unchanged |
| **V15-ADV-1** (already accepted, nonblocking) | **CLOSED** | native §10 sentence scoped; ordering restated as exact and cardinality-first |

Each advisory retains its original severity. `CB5-CLEARED-1` (the five-member
`DEFICIENCY-DOMAIN-V1` against nine product deficiencies) was checked and left alone: I agree with
the blind reviewer's own withdrawal, and I did not widen that domain.

---

## 2. Exact changed source — 9 files, before → after SHA-256

| Path | before SHA-256 | after SHA-256 | after bytes |
|---|---|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `751de4d460aabcd5bb7f7b163d9286a40d6605e0ab53060a19cc9d7eb1a12407` | `64a2a019d6aa94177f59ca0b2cbd380f7e89f3aa3682707b82f50166c72fb8b3` | 102837 |
| `docs/v2/contracts/product-v1/native-evidence.md` | `706b7e0fc94bb1467e33c9f75d5406046e32ab9859f57f08a1f6642dfbdc7d46` | `db1d427e146613132f4d045731617af19efa2cb03a853c663ff3d4c7b06005f0` | 223017 |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `80dcc7474d7202b631194be9c4dc07828c5d507a5c9fd1e961a76f9dcfbc2abc` | `1545b36e65c1e1d6a103c3f82659b7f44a34fec9fe653f536de0eef6639c14fa` | 70355 |
| `docs/coop/design-corrections/native/capability-manifest-domains.v2.json` | `939626cf8533c53cdebfa6421ceb89b9ca6128e3deb841b8a1f6070e0f8e4582` | `088e2fd256681d238502d84092b48b67b89cb5fed0d7dc16d43223a30680b866` | 16051 |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `9ef09ab70c280d63d390fcafef1254d74504fa12d3839823518a1cf111099602` | `7738c372ec7e3d5dbf3766340839d2352f03e0b086d52b2056796dcc24e04508` | 203245 |
| `docs/coop/design-corrections/workflows/schemas/repair.schema.json` | `9188163012b57421b13ff0155c51270250f2f19c782da0875711db75a30137ef` | `797f06565223363c0c2b29bb89e9f9eed49e8c8d5ac1ececb090bb1c2172d456` | 25757 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `f127fb117c3f3526fa6fad62a63e203a75e510fc7950f8e3dfd5b736d614e287` | `4e06e1869f0702f720a960e93390be38363fd2a622475fcd08cac1d6f8284a9d` | 131091 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `3619accb0b190586cabd9fdcca41c9f4db981862d13ff2dd7953f5bf65a6566d` | `9ad4e2682fbc8294666ec9984ded5651ea46718a4b1d352dcba720785fd1e439` | 251852 |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `4b4dc9ed823674273ba3285a6bfcc56fc4499ad3b821cd0446c4ebcf137d8106` | `3b302d7d63b8976cb9dec448db20ec24f8c60f18ac7364d0d278fca6a22adfe5` | 111970 |

The same values, with a per-file account of every edit, are in
`handoff.json#/changedSource`. A unified diff of all nine files is `changed-source.diff`, and the
pre-edit bytes are retained under `before-images/` (each verified equal to its v15 manifest digest).

The two `.py` files changed **docstrings and one comment only**. No expression, statement or
constant was modified. The two schema files changed **`description` text only**: no type, enum,
`required`, pattern, bound, order or const keyword was touched.

---

## 3. The four required findings

### CB5-MUST-1 — the value-domain successor is now selected, by name, in both owning contracts

The blind reviewer was right, and the defect is load-bearing. I checked the superseded domain
myself rather than taking the review's word: `delivery.v4.json`'s
`capabilityManifestIdentity.valueDomains.registries` keys it as
`"fact-plane.v1#relationRegistry.relations"` — 12 members, equal to the live `fact-plane.v1`
relation registry read from its own bytes, with no `unresolved-edge`.

What I found that the review could not: **the reference host admission already read the
successor.** `native_evidence_model.v2.admit_capability_manifest` loads
`capability-manifest-domains.v2.json` directly. So the gap was never in the code — it was that no
contract sentence selected that document, while the sentence that did select one pointed at the
superseded artifact. That is precisely the kind of gap a blind reconstruction catches and a
model-driven check cannot.

The correction:

* **identity §3** now says the host validates the committed CVE1 artifact under *the effective
  value-domain registry*, and then names it: `native/capability-manifest-domains.v2.json`,
  superseding `delivery.v4.json`'s `valueDomains` **within its own declared scope and nowhere
  else**, with the scope spelled out (the two relation registries) and everything inherited
  spelled out too — the CVE1 encoder and its `resolved-inputs.v2` selector, the identity recipe
  and its domain, and ADM-TYPE / ADM-CLOSED / ADM-DOMAIN / ADM-ORDER in the inherited order.
* **native §11** lists it, states it adds **no** native `H` domain (the same statement §11
  already makes for `subjectScopeCommitment`), and names the two registries and the mirror
  relationship to the single ladder authority.
* The successor's own `standing` now names the two exact selectors instead of asserting a naming
  that did not exist. It makes **no** claim that the selection was previously present.

**Not done, deliberately:** no unrelated domain was widened. `PLATFORM-ID-DOMAIN-V1`,
`DEFICIENCY-DOMAIN-V1`, `COVERAGE-STATE-DOMAIN-V1` and every declared-OPEN position keep exactly
the membership they had. Inherited bytes are unchanged.

**Control** (`probes/probe_capability_manifest_domain_selection.py`, 23/23, through
`admit_capability_manifest`): a committed manifest declaring `unresolved-edge: observed` admits
and carries the thirteenth relation; the superseded 12-member domain provably cannot express it;
an unknown relation key refuses `capability.adm-domain:relation:no-such-relation`; a cross-relation
rung refuses `capability.adm-domain:rung:unresolved-edge@resolved-binding`; the inherited committed
bytes still admit and still reproduce the golden id
`508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b`; and ADM-TYPE, ADM-CLOSED and
ADM-ORDER each still fire (the ADM-ORDER control is paired with an ascending-order positive so it
is the *order* rule, not membership, that is shown).

### CB5-MUST-2 — the `libSelection` → component join is published

Confirmed, and the evidence is stronger than the kit could show. The accepted reference fixture
`tsNativeContext` selects `["DOM", "ES2022"]` while its retained components are
`lib.dom.d.ts` / `lib.es2022.d.ts`. **The accepted positive graph already depended on the
unpublished fold-and-map.** Publishing it records an existing dependency; it does not choose a
new algorithm.

Published in native §2.4 and mirrored in the two schema descriptions:

* **fold** — `fold(n)` is the Unicode simple lowercase mapping of the name's code points. It is
  the *same* fold the `honoredOptions.lib` agreement already uses, and this section defines no
  other: no NFC/NFKC step, no trimming, no alias table, no prefix or suffix matching.
* **mapping** — `component(n) = "lib." + fold(n) + ".d.ts"`, total, deterministic and
  **one-directional**.
* **membership** — `component(n)` must be in the declared `component` set, else
  `native.native-context-lib-not-retained:<n>`, the §10 `request-rejected` (2) /
  `REQUEST.PRECONDITION_FAILED` route, before PlanId.
* **equality** — the folded `libSelection` set must equal the folded `honoredOptions.lib` set.
  That list is `required` and non-empty in the closed resolved context, so the agreement always
  applies and is **not** weakened by the mapping.
* **order** — `libSelection` by the raw UTF-8 bytes of the *retained, unfolded* names;
  components by `component` bytes. Folding is a comparison, never a rewrite of retained bytes.
* **custody** — `libSelection` is the configuration-facing record; the component rows are the
  tree-facing **complete** `.d.ts` inventory. Selection never narrows the inventory, the
  inventory never adds a selected name, and the join reads no other input.

**Control** (`probes/probe_ts_lib_component_mapping.py`, 16/16, through `admit_native_context`
plus a positive `bind_typescript_universe`): the accepted context admits and binds a universe;
every selected name maps into the retained component set; the rows really are the complete tree
inventory and strictly larger than the selection; a lower-case re-spelling admits against the
upper-case honored list **and moves `nativeContextId`**, which is what "comparison, not rewrite"
means; `es2023` selected with the honored list widened in step refuses **only**
`native.native-context-lib-not-retained:es2023`; a folded-set disagreement, a fold-duplicate and
an unsorted selection each still refuse; and the two existing accepted custody refusals
(incomplete inventory, ambiguous basename) still reproduce.

### CB5-SHOULD-1 — RC-1 is now total over the registered pairs

The contract gap is real: RC-1 named seven one-rung relations and "syntactic rungs", which leaves
`unresolved-edge@observed` **and** `types@annotated` undetermined, while `resolutionCompleteness`
is a required member of `ViewEntryV3`.

I checked the reference host rather than assuming: `completeness_from_stage` and
`coverage_bijection` decide applicability by membership in the five resolved rungs
(`RESOLVED_RUNGS`), so the model already implemented the corrected rule. **The divergence the
blind review measured is between two readings of the prose, not between the prose and the
model.** That does not dissolve the finding — a contract that two conforming readers read
differently is the defect — but it does bound its blast radius, and I have said so rather than
inflating it.

RC-1 now states:

* applicability is decided by membership of the **rung** in the closed five-member resolved set,
  **never** by ladder length;
* the five resolved pairs are enumerated and may never claim `not-applicable`;
* **every other registered rung is `not-applicable`**, minted with `attempted=false`,
  `unresolvedEdgeCount=0`, `unresolvedEdgeClasses=[]` — the seven one-rung relations, the four
  weaker rungs of multi-rung relations including `types@annotated`, and
  **`unresolved-edge@observed`**, with its reason: `observed` records the edges resolution did
  *not* close, so it makes no resolution claim of its own;
* **`reachability@from-resolved-calls`** is called out as the one-rung relation whose single rung
  *is* resolved — the case a generic one-rung rule would get wrong;
* an unregistered relation or rung refuses, and `not-applicable` is never a fallback for it;
* the host recheck and the `not-applicable` ≠ `complete` statement are retained, and the entry's
  `coverage` keeps its own independent value over the examined partition (RC-2, RC-3 unchanged).

**Control** (`probes/probe_rc1_all_registered_pairs.py`, through the producer boundary
`admit_coverage_result_v3`): all **17** registered `(relation, rung)` pairs are enumerated from
the ladder authority itself, so the sweep cannot miss a relation the registry adds. For each pair
the contract state admits and the RC-1-forbidden state refuses. Plus six named controls:
`unresolved-edge@observed` present in the sweep; `reachability` one-rung-and-resolved;
`reachability@from-resolved-calls` with `not-applicable` **refuses** (a generic one-rung rule
would have admitted it); unknown relation and unknown rung refuse; RC-2 preserved (a `complete`
claim over a `budget-exhausted` stage still refuses); RC-3 preserved (`coverage: complete` with
`state: incomplete` still admits).

**On the cited evidence.** The retained blind vector `rc1-unresolved-edge-state-gap.json` holds
two payload digests and two admitted flags. The two admissible records it compares necessarily
differ in `attempted` and `stageTerminal` as well as in `state` — `complete` requires
`attempted=true` / `stageTerminal=complete`, `not-attempted` requires `attempted=false` — so
"the same observation" is stronger than what the vector exhibits. I record that without using it
to dismiss the finding: the question RC-1 failed to answer is which state it *determines*, and
that is what the correction answers.

### CB5-SHOULD-2 — the projection and, more importantly, where the authority lives

I read the code, the schema and the workflow prose rather than reasoning from the copied boolean.
`repair_preview` consumes the evidence Run's native `ClosedWorldV2`, reads
`deadCodeRepairEligible` **and** `reasons` from it, decides eligibility for unsafe edits, and
*then* projects exactly five fields into `RepairPlanDescriptor`, preserving `evidenceRunId`.

The published correction therefore has two halves, and the second is the one that matters:

1. `repair.schema.json` replaces "Copied from" with the exact five-field projection, states that
   `ClosedWorldV2` is closed at seven and that a literal copy is refused here, and names the two
   dropped members.
2. Both the schema description and workflows §6 publish the **authority prerequisite**: the gate
   is decided against the evidence Run's full record **before any descriptor exists**; the
   descriptor is a projection carried for display and for the `repairplan2` identity, never the
   gate's input; and deleting or editing a field of it cannot bypass the gate, because the whole
   descriptor is the preimage of `repairPlanId` and apply requires a security authorization bound
   to that exact id, base snapshot and project.

**Not done:** the repair record was not widened to seven members.

**Control** (`probes/probe_repair_closed_world_projection.py`, 18/18, through `repair_preview`,
`repair_apply` and the workflow schema closure): a full seven-member eligible record yields an
applicable plan whose `closedWorld` is exactly the five projected members with the Run's own
values, `evidenceRunId` preserved, validating against `RepairPlanV1`; a literal seven-member copy
is refused naming `dynamicDispatch` / `reasons`; a **denying** full record makes the plan
inapplicable with `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` whose remedy **carries the native
`reasons`** — a field the projection does not keep, which is the direct demonstration that the
gate read more than the five; an `imported-prepared-declared` origin denies even with the flag
true; a create-only plan is applicable under the same denying record, so the gate is correctly
scoped to `delete`/`replace`; and both forged-descriptor apply attempts refuse — on the unmet
precondition, and on `REPAIR.CONSENT_NOT_BOUND` once `applicable` is also forged, because forging
moves `repairPlanId` away from the authorization.

---

## 4. Advisories and the accepted V15-ADV-1

* **ADV-1.** identity §3: the four are the closed set of **terminal** representations;
  `by-domain` is a **selector**, resolving through `x-opensip-digest-domains.byDomain` into
  exactly one of them. Measured: 4 terminal tokens in use, `by-domain` on exactly the three
  reference `digest` fields, all 32 `byDomain` rows resolving to a terminal representation and
  none naming `by-domain`.
* **ADV-2.** The `LogicalPath` description no longer claims universal adoption. It names the two
  `$ref` sites, says that this is a claim about **schema enforcement points and not about
  accepted paths**, records that the two join-only fields acquire the grammar by join (an anchor
  path must be an inventoried snapshot path and inventory rows *are* `Blob`), and records why the
  scope-descriptor arrays cannot reference it. `pattern`, `not`, `minLength` and `maxLength` are
  byte-identical — nothing widened, nothing narrowed.
* **ADV-3.** identity §3 now states that both length prefixes are present and meant, that
  `payload_len == raw_byte_len + 4` at `L0-verbatim`, that this is the same shape `L1`–`L3`
  already have, and gives the byte example: span `a=1\n` (`61 3d 31 0a`) → L0 payload
  `00 00 00 04 61 3d 31 0a` → frame component `00 00 00 08 00 00 00 04 61 3d 31 0a`. It says the
  alternative reading yields a different `bodyIdentity` and is not the admitted one. The
  historical `fact-identity-policy.v2.json` is **byte-unchanged**
  (`10055004…bd110`, equal to the accepted v15 manifest) and is quoted, not rewritten.
* **ADV-4.** The current successor registry's `PLATFORM-ID-DOMAIN-V1` now records that the
  inherited vocabulary is deliberately broader than the four selected platforms
  (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64` — cross-checked
  against the security S8 table), that membership admits a manifest **scalar** and is not a
  platform admission, qualification lane, supported population or support promise, and that
  `DUD-V4-9` is the accounted open item. **Members and `memberCount` are unchanged**: narrowing
  an inherited encoding domain would change the admissibility of historical committed bytes to
  close a documentation gap. Nothing here claims or enables an unsupported platform.
* **V15-ADV-1** (already accepted, nonblocking, original severity retained). native §10's
  sentence is scoped to "for every request that reaches that step", and the paragraph now states
  that the ordering is exact and cardinality-first, that an oversized-*and*-malformed spec
  refuses with the cardinality result and reports its schema fault on a later narrowed request,
  and that nothing is lost — both routes are request-rejected / exit 2, no Plan or Run is minted.
  The identical sentence in `admit_analysis_spec`'s docstring is scoped identically. The bounded
  array limit table, the four bounded fields, no-truncation and the retained-record corruption
  classification are **textually unchanged**. Measured: a 10-row malformed spec refuses at the
  schema step; the 1034-row malformed spec refuses on cardinality.

---

## 5. New findings — reported, not fixed

* **BV5A-NEW-1 (advisory).** `admit_coverage_result_v3` does **not** re-check ladder membership
  of the entry's own `(relation, rung)` pair. A cross-relation pair whose rung is registered for a
  different relation — `unresolved-edge@resolved-binding` — **admits** at the Coverage producer
  boundary when its `resolutionCompleteness` is a resolved-shaped record, and mints a `coverage2`.
  It is caught later: `sufficiency_v2` resolves no ladder index and reports
  `required-relation-missing`, and fact admission refuses such a fact. An *unregistered* relation
  or rung refuses at the boundary on the schema enum. I did not fix this — adding a membership
  check at that boundary is a behaviour change outside a minimal contract/description correction,
  and none of the four required findings depends on it. I did make the RC-1 replacement **exact**
  so it does not overclaim: it says an unregistered value refuses on the schema enum, and that a
  cross-relation rung is refused at fact admission and resolves no ladder index at use. It does
  not claim the Coverage producer boundary refuses cross-relation pairs.
* **BV5A-NEW-2 (advisory).** `workflow-cases.v1.json` `repairScenario.run.closedWorld` carries
  **six** members (`dynamicDispatch` absent), and `repair_preview` does not schema-validate the
  evidence Run's `closedWorld` against `ClosedWorldV2`. So the reference does not itself exhibit
  the seven-member evidence record the corrected prose names as the gate input. Not fixed:
  that would change reference behaviour and case data. The corrected prose states the **contract**
  obligation (native §4.5 closes the record at seven; the gate reads it before projection) and
  makes no claim about what the workflow reference model validates; my probe supplies its own full
  seven-member records on both sides of the gate.
* **BV5A-NEW-3 (corroboration, not a defect).** The accepted TypeScript fixture already depended
  on the unpublished lib mapping (§3, CB5-MUST-2).

---

## 6. Evidence, commands and preserved failures

All controls run under `/tmp/opensip-architecture-review-env/bin/python -I -B`, each against the
corrected `work` tree, each driven through a **host admission entry point** on an admitted
positive graph where one is needed. Schema-only assertions appear only where the thing being
checked *is* a published description.

| Probe | Entry point | Checks | Exit |
|---|---|---|---|
| `probe_rc1_all_registered_pairs.py` | `admit_coverage_result_v3` | 17 pairs × 2 + 6 controls | 0 |
| `probe_ts_lib_component_mapping.py` | `admit_native_context` + `bind_typescript_universe` | 16 | 0 |
| `probe_repair_closed_world_projection.py` | `repair_preview` + `repair_apply` + schema closure | 18 | 0 |
| `probe_capability_manifest_domain_selection.py` | `admit_capability_manifest` | 23 | 0 |
| `probe_advisories.py` | `admit_analysis_spec` + registry/byte measurements | 21 | 0 |

Retained results: `probes/*.result.json`.

**Original failures and attempts, preserved and classified.** Four first runs failed. All four
were **probe errors, not design findings**, and each is recorded in
`handoff.json#/referenceControlsExecuted/originalFailuresPreserved`:

1. `probe_ts_lib_component_mapping` — my first case control re-spelled `libSelection` to
   `["DOM","ES2022"]`, which is what the fixture already carries, so the identity could not move.
   Replacing it with a lower-case re-spelling both exercises the fold across the two records and
   moves the identity — and noticing why it failed produced **BV5A-NEW-3**.
2. `probe_repair_closed_world_projection` — 5 failures because the case file writes constants as
   `$NAME` placeholders and I passed `recipe.closureId` through as the literal `"$PROD"`. Added
   the same substitution the reference checker performs.
3. `probe_advisories` — I asserted an abbreviated quotation of the inherited L0 string. Replaced
   with the stronger, correct control: the whole historical file's SHA-256 against the accepted
   v15 manifest digest.
4. `probe_capability_manifest_domain_selection` — a `KeyError` because `delivery.v4` keys the
   superseded domain as `"fact-plane.v1#relationRegistry.relations"`; and separately a **vacuous**
   ADM-ORDER control, because the live provider row carries a single `platformId` so reversing it
   was a no-op. Both fixed, and the order control is now paired with an ascending-order positive.

**Disposable copies, named, with all deltas preserved.**

* `disposable/stale-pin-observation.v1` — the corrected bytes with pins untouched.
  `check_native_evidence.v2.py` exits **2** with 9 `sha256 mismatch` pin faults naming exactly the
  9 changed files. This is a **stale pin against changed source, not a product failure, and it
  cannot be called a PASS.** Only delta: the checker overwrote
  `native/native-evidence-report.v2.json` with its pin-fault report.
* `disposable/checker-run.v1` — the corrected bytes with the four `source-pins` files refreshed
  **locally only**. All five unit reference checkers pass:
  native `347/347` (matrix cells 66, open objects 0, uncovered feedback `[]`);
  foundation `passed: true` over 1099 source files; workflows `passed: true` over 65;
  security `456/456`; integration `365 passed, 0 failed`.
  Logs retained under `disposable/logs/`.
  Deltas versus the proposed tree: the four pin files, plus `workflows-report.v1.json`
  (three `sourceSha256` rows — `repair.schema.json`, `workflows_model.v1.py`, `source-pins.v1.json`
  — **no check result changed**) and `workflows-validation-report.json`'s `reportSha256` following
  it. Notably, `native-evidence-report.v2.json` regenerated **byte-identical** to the proposed
  tree's copy.

---

## 7. Preserved behaviour, and what I did not do

Preserved: no type/enum/required/pattern/bound/order/const keyword changed in any schema; no
expression, statement or constant changed in either model; the inherited historical artifacts
(`delivery.v4`, `fact-plane.v1`, `fact-identity-policy.v2`, `d9-exit-contract.v1.14`,
`permission-truth-tables.v9`) are byte-unchanged; the capability-manifest gates, CVE1 encoder,
identity recipe and golden DCM-1-core identity all still reproduce; RC-2/RC-3/RC-4/RC-5 unchanged
in substance and no pair's admitted state moved; the repair record stays closed at five members
and its gate, code and remedy are unchanged; the bounded-array limit/order/no-truncation and
retained-corruption text is unchanged.

Not done:

* **Source pins in the proposed tree were not refreshed.** They are stale by construction and are
  root/Codex's to refresh **after** all final source and records, followed by the six final checks
  and a fresh independent review.
* The six whole-subject checks were not run on the proposed tree; the unit checkers were run only
  in the named disposable copy.
* No generated report, review history record, crosswalk, readiness register, disposition file or
  source-pin manifest was edited in the proposed tree.
* No repository file, frozen subject, blind-review directory or historical archive was written to.
  Every deliverable and every piece of retained evidence is under
  `/tmp/opensip-design-corrections/bv5-corrections-author.v1`. **Disclosed:** during the run I used
  two transient scratch locations outside that directory — `/tmp/v15-extract` (two files extracted
  from `candidate-source.v15.tar.gz` to recover the two model before-images) and `/tmp/*.log`
  (checker stdout). Both were copied into `before-images/` and `disposable/logs/` and then deleted.
  Neither is inside any subject, review or repository tree.
* No product implementation, commit, push or publication.

---

## 8. Limitations, and where a reviewer may reasonably disagree

* This is a **coauthor** pass. My assent is substantive but **not independent** and confers no
  readiness or acceptance. The v15 independent review and the consumer-B v5 blind review remain
  literal historical evidence and were not edited.
* Everything observed here is over reference models and synthetic fixtures. No compiler, cargo,
  provider, repository, filesystem, ledger or renderer was executed. Where a control "refuses",
  that is a reference model applying a stated rule, not evidence about any implementation. None of
  this is product qualification.
* **BV5A-NEW-1 and BV5A-NEW-2 are left open by design.** A reviewer may reasonably judge that the
  Coverage-boundary membership check, or validating the evidence Run's `closedWorld`, belongs in
  this pass. I judged both to be behaviour changes outside a minimal contract-and-description
  correction, and I chose to keep my prose narrow enough to remain true without them rather than
  to write prose the reference does not support.
* **Placement of the MUST-1 listing.** Native §11 is titled "Identity domains authored here" and
  what I added is a *value-domain registry*, not an `H` domain. The paragraph says so explicitly.
  A reviewer may prefer §0's superseded-selector table. I chose §11 because the successor's own
  `standing` names §11 and because §11 already hosts the parallel "adds no native domain"
  statement for `subjectScopeCommitment`.
* **The two `.py` edits.** MUST-1/MUST-2/SHOULD-1 needed no model change, and I made none. I did
  correct two model **docstrings** that carried the very wording two findings are about
  (`"copied from a native ClosedWorldV2"`, and the unqualified schema-step sentence). A reviewer
  who wants zero model bytes touched can revert those two files; doing so leaves the misleading
  wording in current source and changes no behaviour either way.

**No whole-tree acceptance is claimed.** The proposed bytes are exactly the nine files in §2.
