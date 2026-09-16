# OpenSIP consolidated product design — fresh independent review

**Verdict: CHANGES_REQUIRED** — 1 new MUST, 3 new SHOULDs, 3 advisories.

**Subject manifest** `c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2`.
**verifiedManifest = true**, by measurement: I recomputed the manifest digest, then
recomputed SHA-256 and byte length for all **12,892** files under
`/tmp/opensip-design-corrections/candidate-subject.v26` and walked the tree for files
the manifest omits. Result: 736,277,340 bytes, **0 missing, 0 hash mismatches,
0 length mismatches, 0 extra files**. The snapshot was re-measured as byte-unchanged
after every checker run.

This origin authored none of these bytes, resumed no author session, and wrote only
under `claude-independent-design.v26`. No grade, activation, application or
implementation authorization follows from it.

---

## 1. What I read, and how

**37 documents read end to end (21,365 lines)** through the file-reading tool in
120–180 line chunks with preserved path/offset coverage — never grep excerpts.
Exact paths and SHA-256 are in `review.json#/contractsReadCompletely`. They are:

- the five consolidated contracts and the README index — identity-and-evidence
  (1,729 lines), native-evidence (3,693), security-and-lifecycle (1,519),
  workflows-and-surfaces (1,287), admission-and-qualification (349), README (60);
- the incorporated evaluator3 contracts — enumeration v1, atom v1, execution-inputs v1,
  composition v3 **including §9 in full**, fault v3;
- the incorporated projections — query-projection v3 and workflow-projection v3;
- the current selected provider-return schemas — TargetAttributionV2 (476 lines),
  `fact-batch.schema.v3.json`, `occupancy-companion.schema.v1.json`,
  `dispatch-binding.schema.v1.json`;
- `hydradb-dispositions.proposed.md`;
- the planning layer — chapter 14 (732), implementation-boundaries-and-build-plan
  (1,128), prototype-report-inventory (237), planning sources, normative inputs;
- the incorporated companions — store-instance lineage, report-asset binding,
  attempt custody, read-only recovery v3, carrier format/dispatch/migration/high-water
  and the carrier DDL;
- the frozen disposition maps — crosswalk, inherited residuals, current-source map,
  evaluation residuals, qualification gates.

Seven large machine-readable files (identity-schemas.v3, relation-payload-schemas.v2,
capability-manifest-domains.v2, command-inventory.v3, repository-file-inventory,
implementation-coverage, commit-recovery-plan) were traversed **record by record
programmatically**, which is listed separately and is a stronger coverage claim than
eyeballing 8,925 lines of JSON.

**Pinned execution.** Everything ran under
`/tmp/opensip-architecture-review-env/bin/python -I -B` (3.12.13, jsonschema 4.25.1).
Report-writing checkers were run only inside a **disposable copy whose every one of
1,350 bytes-files I verified against the frozen manifest first**, and the frozen
snapshot was re-measured unchanged afterwards. **No pin gate was bypassed, disabled or
rewritten.** Where a gate refused because pinned inputs were absent from my copy, I
supplied those frozen bytes after verifying each against the manifest and re-ran — the
gate's refusal was correct and I satisfied it rather than editing it.

---

## 2. The current source-pinned evaluator3 launcher

`foundation/run-evaluator3-checks.py` (`c68a9ce9…`), ledger
`evaluator3-source-pins.v1.json` (`931e3803…`): **1,242 pins valid, 0 changed or
missing, 16 of 16 checks exit 0** in 239 s. Receipt:
`receipts/evaluator3-launcher/report.json`.

Sixteen further reference checkers also pass, including `check-identity` (1,596),
`check_workflows` (1,803), `check-integration` (412), native (375 cases / 66 cells),
security-lifecycle (464), `check-carrier-v3` (87/87), and both planning checkers
(198 unique paths; 320 mappings, 54 planned cases) in `--check` mode.

**Reference controls are not self-authentication.** Every one of these is design
evidence over synthetic trusted inputs. None qualifies a compiler, provider, host,
filesystem, OS or platform, and I award no readiness from any of them.

---

## 3. My own discriminating probes

### 3.1 The reminted false-result graph (required)

I took a real admitted Run and applied three independent semantic mutations — verdict
flipped, one retained predicate-proof value flipped, one execution deficiency dropped —
then **reminted proof-bundle → semantic-evidence → evaluation-seal → run** so every
enclosing identity was recomputed and the graph was internally hash-consistent.

| Mutation | new RunId | `open_run_closure` | `close_run` | `execute_graph_query` |
|---|---|---|---|---|
| verdict flipped | differs | **ADMIT** | **REFUSE** `EVALUATOR_COMPLETE_PROOF_REPLAY` | REFUSE operational-failed / HOST.IO_FAILURE / evidence.corrupt |
| predicate value flipped | differs | **ADMIT** | **REFUSE** same | REFUSE same |
| execution deficiency dropped | differs | **ADMIT** | **REFUSE** same | REFUSE same |

The structural owner primitive is not semantic authority, and the public graph entry is
not the structural API. Separately, `admit_cache_entry` calls `close_run` **first** and
only then resolves the key's references through the Run's own closure, while
`cache_key` construction reads no bytes — so there is no cached-payload bypass.

### 3.2 Cross-unit claim: the ladder authority and the digest law

Re-derived independently: 13 relations, each with a non-empty `ladder` and an
`anchorLaw`. `native_evidence_model.v2.LADDERS` is **derived** from the single authority
(so it cannot drift) and equals it in order; `RELATION-LADDER-DOMAIN-V2` equals it in
order. The alphabetised-ladder defect the contract describes is genuinely closed.
Representations closed at four terminals plus the `by-domain` selector carried only by
`Ref`/`ProofInputRef`/`FindingEvidenceRef`; 40 `byDomain` rows, none resolving to
`by-domain`; every `domain` enum member registered. `anchorLaw` classes are exactly
inventory = {file, package, vcs-change}, body-identity = {clones}, source-text = the
other nine; `coverageTotality` is carried by `file` alone. → **S-1** below.

### 3.3 Current target/proof boundary

Constructed six discriminating instances and validated each against **both** selected
schemas, then read the actual atom guard and host projection. The two explicit MUSTs
(`occupancy=first-party`, `kind=package`) refuse correctly. The `ONLY … kind is file or
symbol` clause is enforced **nowhere**. → **M-1** below.

### 3.4 Newly specified retained graph-query boundary

Driven through the public `execute_graph_query` on a real admitted Run:

- availability `purged`/`expired`/`corrupt`/`unavailable` → operational-failed /
  `HOST.IO_FAILURE` / `evidence.{purged,expired,corrupt,missing}`, exactly the
  graph-specific selector identity §5 and query §7 own; `retained` and `partial` answer,
  with `partial` backstopped by `close_run`. An availability observation can refuse but
  never grant.
- endpoint outside the vertex domain → `QUERY.ENDPOINT_UNKNOWN`; an **admitted** vertex
  with no incident projected fact returns `items=0`, `traversalCoverage=complete`, **with**
  `{incoming-search-incomplete, resolution-not-attempted}` disclosed — evidence
  sufficiency and traversal completion stay separate and zero rows is not absence.
- a cursor minted for a different Run → `QUERY.CURSOR_MISMATCH`.
- visited-node law **at the cap**: zero-hop at `maxVisitedNodes=1` is exactly-at-cap
  `complete` (visited 1, `countBasis=exact`); one-edge at the same cap does not enter the
  target (`truncated-bound`), and under `completeness=required` carries top-level
  `{class: indeterminate, reasonCodes: [QUERY.COMPLETENESS_UNMET], runId}` — under
  best-effort, none.
- **full-response renderer parity**: `query-response` is byte-equal to the complete
  owner-admitted `GraphQueryResponseV1`; all four scalars plus `termination-class` are
  exact projections of its context; `completenessMet` is true exactly when
  `countBasis == exact`, in both directions; `advisory` is const false; and a
  response/termination pair that disagrees refuses
  (`QUERY_SURFACE_RESPONSE_TERMINATION_MISMATCH`). The inventory's declared
  `parityFields` for `query` are exactly the six §8 fields.

### 3.5 Closure-kind at each actual owner

`closureKinds` publishes 15 field→kind bindings and `closureMembership` publishes
`direct` / `equalToDirect` / `selectedThroughOtherInput` with an explicit selection law.
I swapped the declared kind of every retained closure, reminted its identity and rewrote
every reference. **Every referenced closure** (provider ×22, evaluator ×5, detector ×3)
refuses at both boundaries. The three that admitted have **zero** references in that
fixture, which the contract expressly permits. Transitive selection is not flattened.

### 3.6 Planning layer, measured

198 unique paths in 20 groups; 0 unknown dependency targets; 0 cycles; the pure-layer
direction holds with no reverse edge; storage→evaluator/security as the build plan
states and neither depends on storage; 8 generated files, all under `generated/`,
matching the registry's "all eight"; 5 renderers with json v3; 45 commands with HTML on
exactly the declared 8 and SARIF on exactly the declared 4; every SARIF command declares
all seven common parity fields; `capability-availability` is a parity field of exactly
the 5 `requestClass: analysis` commands and no others; `query` advertises human/JSON/agent
only; 24 report features R01–R24 (8 Preserve, 16 Change) matching the coverage group;
`CommitRecoveryAssociationV1` is 13 closed fields with F00–F53 contiguous, **all 54
`executionStanding: not-executed`**, `journalSeq` maximum excluding the reserved terminal
slot, and the carrier dispatch's security/storage owner split **partitions the record
exactly**, no overlap, nothing unassigned; **all 32 gates carry `qualified:false`,
`demonstrated:false`, `implementationHarnessAuthored:false`**; 28 architecture pins all
match the current v26 bytes while source25 is retained separately as inherited
provenance.

---

## 4. New MUST

### M-1 — `logicalPath` admits in a position its own normative text excludes, and the two spellings mint different `run3` identities

**Owners.** `target-attribution.schema.v2.json#/properties/logicalPath/description` and
`#/allOf`; `occupancy-companion.schema.v1.json` likewise;
`atom-evaluation-contract.v1.md` §2; `atom_model.v1.py` sidecar guard;
`provider_attribution_return_model.v2.py` `project_companion_to_v2`;
`target-attribution.schema.v2.json#/x-opensip-new-internal-faults/keys`.

**The claim.** "logicalPath is a non-authoritative hint **ONLY** when occupancy is
external or unknown **AND kind is file or symbol**. MUST be null when
occupancy=first-party. MUST be null when kind=package."

**Measured.** The two explicit MUSTs refuse. The `ONLY` clause excluding `kind=unknown`
is enforced nowhere: `kind=unknown` + `occupancy=external|unknown` + non-null
`logicalPath` **admits** in both schemas and through `admit_atom_inputs`;
`project_companion_to_v2` copies the value mechanically; the internal key list carries
only `…_ON_FIRST_PARTY` and `…_ON_PACKAGE`.

**Consequence (reproducer `probes/pB_target_boundary.py`, `pB2_model_boundary.py`).**
TargetAttributionV2's identity is raw SHA-256 of `C(record)`; the two spellings measured
to `4337e66e…` and `2acc198d…`. That digest is a `hostCapture.hostDerivedRefs` and
`ExecutionInputsV1.selectedRefs` member, so it reaches `C(ExecutionInputsV1)` →
`proof.executionInputsDigest` → **proof3/evidence3/seal3/run3**. One provider observation
with undecidable target kind therefore has two admissible encodings producing two sealed
Run identities. No query answer, finding, verdict or occupancy decision changes —
`logicalPath` is never read for identity — but the retained input's identity does.

This is precisely the independent-replay-across-machines property this contract set
closed three times on the same reasoning: `FACT_ANCHOR_CARDINALITY`, the `capabilityId`
spelling vocabulary, and the `TypeScriptConfigGraphV1` node-kind law. Each was recorded
as a defect, not tolerated.

**Required minimal remedy** — make the description and the admission agree, and say
which was chosen:

- **(a)** enforce the stated `ONLY`: one `allOf` branch in each schema requiring
  `logicalPath: null` when `kind` is `unknown`, plus one internal key (e.g.
  `TARGET_ATTRIBUTION_LOGICAL_PATH_ON_UNKNOWN_KIND`) beside the two existing ones, routed
  on the existing `input-join-invalid` / `provider-return` / `EVALUATION.INPUT_REFUSED`
  route — no new `DomainDetailCode`, no new D9 code; **or**
- **(b)** withdraw the word `ONLY` and state that a `kind=unknown` record may carry the
  hint, accepting that differing hints are different descriptors exactly as the
  `source-text` `anchorLaw` already says for `fact.anchors`.

Either is bounded. Leaving the field's own description and its enforcement disagreeing is
not.

---

## 5. New SHOULDs

**S-1 — the closing digest law states a universal quantifier that is false of the bundle
it annotates.** `identity-and-evidence.md` §3 and
`identity-schemas.v3.json#/x-opensip-digest-domains/standing` both say every 64-hex field
carries `x-opensip-digest` and a field without one is inadmissible. Measured: **64 bare-hex
occurrences, 0 unannotated** — the law holds in its narrow reading — but **63 typed-prefix
identity occurrences carry no annotation**, and `byDomain` publishes no prefix→domain key,
so the resolution exists only in prose. The reference enforcement
(`check-identity.py`, case `digest-law-covers-every-64-hex-field`) uses the narrow
predicate. A consumer implementing the stated law literally refuses every conforming Run.
**Remedy:** narrow the quantifier in both places and add one machine-readable scope key to
`x-opensip-digest-domains` naming which fields the law governs and how a typed prefix
resolves. *(One finding in my first pass here was my own probe defect, recorded in
`review.json#/limitations`, not a design gap.)*

**S-2 — `CarrierMigrationIntentV1` has no satisfiable value on the selected fresh-install
and act-C-resume path.** `carrier-migration.v1.md` §2 and
`carrier-dispatch.v3.json#/migration/intentIsNotPersisted` both say it is validated
**before any act**; the intent's `observedFormat` is `1|2` and `firstGeneration` is
`i64 >= 2`. But `openDispatch` step 8 and the integrated fresh-install boundary select a
path with **acts B and C only**, `first_generation 1`, `migrated_from null` — and the DDL
itself admits `first_generation >= 1`. Acts B and C are durable acts. **Remedy:** one
sentence scoping the precondition to the migration path (acts A–B–C from an inherited
carrier), or widen `observedFormat` and lower `firstGeneration` to `>= 1`.

**S-3 — `report-asset-binding.v1.json` declares two different anchors under one id `B11`,
and cites that id with both meanings** (`#/failureBehavior/cases[2]/basis` uses it for the
aggregate-termination rule; `#/anchorSelection/…/installTimeProvenance` and `#/limits[2]`
use "(B11/B12)" for the TR-CORE signed inventory). This is the ambiguous-selector defect
the programme itself records against `security-completion.v8`'s duplicate headings, where
`current-source-map.proposed.md` requires exact selectors. **Remedy:** renumber the second
occurrence and update the two citations.

---

## 6. Advisories (not blockers)

- **A-1** `witnessMalformed` is a reportable quarantine condition with no durable
  representation in `carrier_quarantine.reason` (`uncertainTailLoss`,
  `witnesslessRestore`). Consistent with the selected design — read-only recovery may not
  write a marker and the side tables are preserved byte-identically — but worth stating.
- **A-2** security §S13 states 456 cases / ten sweeps; the pinned checker reports 464 and
  eleven. The same hand-maintained-counter problem native §1.1 argues against.
- **A-3** the carrier correction's executed controls C1–C18 are cited by `scratch/out/…`
  paths that are **not** subject members. `check-carrier-v3.py` is nonetheless runnable
  from frozen bytes once its expected runtime layout is reconstructed, which I did — it
  passed 87/87. The *validator* reproduces; the original *measurements* do not.

---

## 7. What I checked and found sound

Discovery, zero-config and installed availability; typed configuration, admission and
authority ordering; the acyclic source/Plan/native/evaluator/proof/evidence/Run graph;
complete enumeration and negative knowledge; atom witnesses, target attribution and
incoming completeness; host-captured execution inputs and candidate-only paths;
three-valued composition, waivers and budgets; stable correspondence with unmatched
findings retained as findings; the source-bound portable baseline and the E0–E4
counterfactuals with non-substituted evidence binding; the optional tree-bound detector
compatibility listing kept distinct from the component manifest; import/test/runtime/history
evidence; invocation and repair authority; SEAL full replay and the three distinct SEAL
boundaries; output and common fault routes; capability, platform and qualification
boundaries. Composition §9's proof/witness/finding/evidence field derivation, canonical
ordering and dedup, and originating-cause retention are reconstructible from the normative
documents alone — I rebuilt the ordering and `Cset` laws from §9.2–§9.7 without reading the
models. `hydradb-dispositions.proposed.md` accounts all eight proposals without selecting a
graph database or claiming measured performance. The twenty query operation names are
unchanged and major 3 strengthens only the three graph operations.

---

## 8. Dispositions

Complete maps keyed by id are in `review.json`:
`arDispositions` (AR-01…AR-16, **16**), `fwDispositions` (FW-01…FW-15, **15**),
`inheritedResidualDispositions` (DR-001…DR-011 and DR-011-R01…R16, **27**),
`scopedReviewOwnerDispositions` (DR-201…DR-205, **5**). Each row names the actual owning
contract section I read, a substantive basis and an explicit scope — not a generic
carry-forward.

**Every row: `appliedByThisReview = false`, `finalApplicationOutcomeGranted = false`,
no grade.** The five owner rows DR-201…DR-205 carry
`ROUTING-ASSESSED-ONLY-NOT-APPLIED`; DR-011-R10 (blind consumer-B) likewise, because it is
closable only by the separate blind session that follows.

Retained in the cross-unit assessment and closed by nothing here: the **30** evaluation
residuals (RES-EP13-01…19, IR-EP13-NB-01…07, AX6, AX9, MD5, RX2c), the **28** condition-2
obligations (DR-101–107, DR-109–115, DR-117–127, DR-130/131/133), and **all 32** product
qualification gates, measured unperformed.

---

## 9. Limitations

Full list in `review.json#/limitations`. The load-bearing ones: this qualifies no product,
compiler, provider, host, filesystem, OS or platform; every checker operates on synthetic
trusted inputs and synthetic TCB observations are assumptions, not proof of enforcement;
all 54 commit-recovery cases and all 32 gates are unperformed; **I did not perform and do
not claim a blind consumer reconstruction** — a separate NEW blind session follows under
the original charter; the 718 MB historical `reviews/` tree was hash-verified but not read;
the 44 prototype pins name a separate repository and are not verifiable from these bytes;
and two of my own probes initially produced false positives, both corrected, re-run and
recorded rather than hidden.

D9's later published successor artifact carrying the `host-invariant` faultCause is a
carried implementation obligation of the D9 unit, consistent with the contract's own
disclosure — I do not treat it as a design-level blocker.

---

## 10. Standing

**CHANGES_REQUIRED.** ACCEPT requires every review action complete **and** no unresolved
MUST or SHOULD; M-1, S-1, S-2 and S-3 are unresolved. All required review actions were
completed and are itemised in `review.json#/requiredReviewActions`.

No grade, activation or implementation authorization is granted. Nothing is applied.
Final application and readiness remain a later, separately reviewed boundary, and root
independently assesses this review.
