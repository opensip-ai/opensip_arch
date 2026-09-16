# Independent design review — source43 (whole-design successor)

**Reviewer:** Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7, continuing after the completed source42 review; source43 charter; authored none of the reviewed bytes)  
**Standing:** Source43 whole-design successor review. Not fresh-origin independence, blind reconstruction, final application acceptance, implementation authorization or product qualification.

## Verdict: ACCEPT

No MUST, no SHOULD, no blocker. Availability: source43 corrects a source42 under-disclosure. A successful graph response now reports an observed partial or retained state in context.availability exactly, as identity-and-evidence ("A query reports both") and the query parity field require. Independently discriminated on one lawful closed Run with each tree's own modules: partial reports retained on source42 and partial on source43, with identical items and context. The same holds through the reference adapter record path, a trusted-latest join, a cursor continuation, and parity/renderers. A host observation grants nothing: every refusing state, precondition, public route, missing-byte and corrupt-byte case is unchanged and identical on both trees. Path orientation: section 4 selects the walk representation for a previously unspecified field and preserves the model behaviour, with byte-identical responses across trees and goldens for tie, order, depth and zero-hop. The cursor stays an opaque host token with same-host continuation, cache-loss and bound laws confirmed. Limitation and diagnostic prose obey schema, parity and route laws without canonical wording. No new public identity, error code or schema major exists, and RunIds are unchanged. ADV42-01 is retained as a non-blocking advisory; its root routing as a crates/host/src/analysis.rs implementation verification obligation is correctly scoped and is not a containment proof. S40-01 and ADV40-01 remain resolved. Also completed on verified copies: subject, archive, all members, parent42, the 9/0/0 delta, all pins, six pinned groups, 17 children, planning and inventory, package v20, the scope-preservation probes and final copy re-verification. Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.

## Subject

| Item | Value |
|---|---|
| subjectManifestSha256 | `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d` |
| liveManifestSha256Measured | `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d` |
| verifiedManifest | `True` |
| subjectFileCount | `12913` |
| subjectTotalBytes | `737769489` |
| subjectArchiveSha256 | `d1ff8312d6a5540a977e54cfe8e24dd4865f8b09e6c432e42fd0d651387b66fa` |
| archiveSha256Measured | `d1ff8312d6a5540a977e54cfe8e24dd4865f8b09e6c432e42fd0d651387b66fa` |
| parent42 | `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307` declared by 43: True; snapshot verified: True (12913 members); archive `2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6` |
| delta 42to43 | 9 changed, 0 added, 0 removed |
| owned source pins | all match: True; changed pins: `foundation/source-pins.v1.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json`, `workflows/check-query-projection.v3.py`, `workflows/query-projection-contract.v3.md`, `workflows/query_projection_model.v3.py`, `workflows/source-pins.v1.json` |
| planning input layer v11 | `75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de` (31 inputs, retained: unchanged inputs) |

Changed files: `docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json`, `docs/coop/design-corrections/foundation/source-pins.v1.json`, `docs/coop/design-corrections/native/source-pins.v2.json`, `docs/coop/design-corrections/security/source-pins.v1.json`, `docs/coop/design-corrections/workflows/check-query-projection.v3.py`, `docs/coop/design-corrections/workflows/query-projection-contract.v3.md`, `docs/coop/design-corrections/workflows/query_projection_model.v3.py`, `docs/coop/design-corrections/workflows/source-pins.v1.json`, `docs/coop/design-corrections/workflows/workflows-report.v1.json`

## Issues

No MUST issue. No SHOULD issue. No new advisory.

### ADV42-01 (ADVISORY, source42 review (retained; not new in source43)): Execution-inputs admission neither states nor checks that a complete receipt's view outputRefs carry that receipt's producerClosure, and raises the section 3 PLAN_JOIN only for candidate views whose producer matches some row; Run closure is the backstop

**Current standing.** RETAINED ADVISORY, NON-BLOCKING. Root routing as an implementation verification obligation for crates/host/src/analysis.rs is assessed as correctly scoped; it is not a containment proof and no control was executed for it.

**Standing assessment.** Every selector owner is byte-identical 42->43 ({"execution-inputs-contract.v1.md": true, "execution_inputs_model.v1.py": true, "execution_inputs_fixture.v3.py": true, "identity-model.v3.py": true, "identity-schemas.v3.json": true}), and the ported measurement re-observes the four source42 values on source43: J1 refuses EXECUTION_INPUTS_PLAN_JOIN; J2 and J3 admit, and close_run refuses them with CLOSURE_FIELD_KIND:view.producerClosure:provider. The source-only note keeps the advisory with a verification obligation for crates/host/src/analysis.rs. Repository layout 14 (:475, search output) names that module as the service composing provider work, admission, evaluation and complete replay, which makes it the planned host capture. Execution-inputs section 8 (:299, source42 read on byte-identical bytes) already binds the builder to place each explicit returned view on the view stage whose producerClosure it carries. A product verification that analysis.rs never lists a view on another producer's complete receipt therefore tests existing law and invents none. This routing is carried by the root note, not by a source43 byte: the planning inputs and coverage are unchanged. Final application must carry it explicitly. Scope limits: no two-stage two-provider Plan was minted by this review or by the note, so the unexercised shape stays argued from source. Execution-inputs admission still does not re-check receipt/view producer equality or apply PLAN_JOIN before the row filter, and those contract-level options stay optional owner improvements. Nothing warrants reopening the advisory for wording: no measured world admits a contradictory Run, the refusal chain is closed by the Run owner, and TCB-SCOPE-01 is unchanged.

- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12 (section 1: receipts rooted in producer obligations; outputRefs constrained by domain only)
- execution-inputs-contract.v1.md:51 and :53 (section 3: stage-spec producerClosure and view planId checks; "a candidate view whose planId is not the Plan's refuses EXECUTION_INPUTS_PLAN_JOIN")
- execution-inputs-contract.v1.md:299 (section 8: the builder places each explicit returned view on the view stage whose producerClosure it carries)
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1057-1093 (receipt checks compare receipt and stage spec, never an outputRef view producer)
- execution_inputs_model.v1.py:1132-1139 (the per-row producer filter precedes the planId check)
- execution_inputs_model.v1.py:1626-1640 (an attributed view is compared with the producer of its ROW's receipt, not of the receipt that lists it)
- docs/coop/design-corrections/foundation/identity-model.v3.py:1842-1851 and identity-schemas.v3.json byField view.producerClosure=provider (Run closure: VIEW_PLAN_JOIN, UNSELECTED_PRODUCER, closure kind)

**Detail (source42, unchanged bytes).** A captured, unattributed view whose producerClosure is not the receipt's producer admits at execution-inputs admission on source40, source41 and source42, even with a foreign planId, and the complete Run refuses it only at closure (CLOSURE_FIELD_KIND:view.producerClosure:provider). A foreign-planId view from the stage's own provider refuses EXECUTION_INPUTS_PLAN_JOIN as section 3 says, because it passes a row's producer filter first. By reading, the model never compares a complete receipt's outputRef views with that receipt's producerClosure, and it checks attributed views against their own row's receipt. In a Plan with two view stages of two Plan-selected providers, a view of provider P2 listed on P1's complete receipt would therefore pass admission and the closure checks measured here. No maintained multi-provider graph exists, so that shape was not exercised.

**Consequence.** No Run closes with the measured shapes; for them the contract's named refusal and the refusing owner differ. The unexercised multi-provider shape would be a self-contradictory stage-return record, a detectable host capture error rather than an omission. It is not attribution nondeterminism for one captured observation, and it is pre-existing since source40.

**Disposition.** ADVISORY, non-blocking; retained with owner routing (foundation execution-inputs owner for the optional contract clarifications; crates/host/src/analysis.rs implementation verification obligation at final application / implementation).

**Measured on source43**

```json
{
 "sameProviderForeignPlanId": {
  "admission": {
   "result": "REFUSE",
   "refusals": [
    "EXECUTION_INPUTS_PLAN_JOIN"
   ]
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:REFERENCE_PLAN_JOIN"
  },
  "onRows": []
 },
 "foreignProducerSamePlan": {
  "admission": {
   "result": "ADMIT",
   "refusals": []
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
  },
  "onRows": []
 },
 "foreignProducerForeignPlan": {
  "admission": {
   "result": "ADMIT",
   "refusals": []
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
  },
  "onRows": []
 },
 "observedEqualToSource42Receipt": true
}
```

## Observations (not defects)

- **OBS43-01** Omitted reference observation. Contract section 7 (:162) says an omitted observation neither refuses nor grants ("not a grant and not a purge"), and it pins what an observed retained or partial state reports. The value a successful response reports for an omitted observation is not stated in contract prose. It is stated by the model docstring (query_projection_model.v3.py:1483-1485: retained once close_run has admitted the closure) and pinned by the checker control host-availability-retained-and-omitted-report-retained. Measured: omitted reports retained on both trees for neighbors, path and reach. A product adapter always supplies an observation, the admitted state of the retained record (:164, :166), so omission is a reference-harness case with no product surface. Not a defect; a one-clause prose pin is optional. (receipts/probes/query43-x.json)
- **OBS43-02** Current availability is not part of the cursor binding. selection_hash binds project, Run, fact-views, operation and effective params, and never availability (model :334-342). A continuation issued under one observation and presented under partial is admitted with the same page, and source43 discloses partial on that page. This is consistent with availability being a current monotonic-generation record (identity :1722-1725) rather than a selection input. A refusing state still refuses. (receipts/probes/query43-x.json)
- **OBS43-03** Path rows carry no stored-orientation flag. Under incoming or both, a consumer recovers a hop's stored orientation only by its factId, for example from the neighbors row that keeps the projected fact's source->target. This is the representation section 4 (:100) selects. GraphPathEdge (schema :817-836) has no orientation description, and GraphPathRow (:847) describes only zero-hop and the tie-break. It is not a defect. (receipts/probes/query43-x.json)
- **OBS43-04** Against root-source43-final-reference.v1 and codex final-reference.v43: all six group stdouts are byte-equal (True); 15 of 17 child stdouts are byte-equal to root; enumeration and execution-inputs differ only in ownedHashes[].path/receiptPath (equal after removing only those fields, also against this origin's source42 receipts); query-projection is byte-equal to root and differs from this origin's source42 receipt only by 204 -> 209 checks (added ['path-incoming-edges-are-traversed-hops', 'path-both-edges-are-traversed-hops', 'host-availability-partial-reported-in-response', 'host-availability-partial-changes-only-availability', 'host-availability-retained-and-omitted-report-retained']; none removed). The codex runner-original equals the root reference-checks (True); codex adds the formal subject binding (changed top-level keys ['currentProfilePinsSha256', 'standing', 'subjectManifestSha256']). (receipts/reference-comparison.json; receipts/reference-children-stripped.json)
- **OBS43-05** The root reference and root planning verification were executed from a pre-freeze working tree (['/private/tmp/opensip-design-corrections/source42-query-successor.v1/source']), not from the frozen archive. Their recorded script shas equal the frozen source43 bytes. Their stdouts equal this review's own executions on verified archive copies: all six group stdouts are byte-equal, and the planning stdout sha is equal (True). This review's own executions are the acceptance input. (receipts/reference-comparison.json; receipts/planning-checks.json)
- **OBS43-06** Re-observed on source43 by the ten ported scope probes, every observed value identical to this origin's source42 receipts: policy 26 rows, native 39 rows, runterm 24 rows, query 98 rows, carrier 108 rows, comparison 28 rows, repair2 16 rows, term7 24 rows, custody 20 rows, capture-joins 4 rows. The source42 observation contents of OBS42-08 therefore stand on unchanged owner bytes. (receipts/probes (ported43_*))
- **OBS43-07** The model delta is three hunks (query_projection_model.v3.py diff): an observe_availability docstring, return avail replacing return "retained", and execute_graph_query passing that value to finish_operation in place of the literal "retained". Refusal routes, observation order, cursor, traversal and every other context field are byte-identical in behaviour (P43-QUERY-X: omitted/retained responses and all orientation, route, cursor and bound responses are byte-identical across trees). (receipts/delta-diffs-42to43/docs__coop__design-corrections__workflows__query_projection_model.v3.py.diff; receipts/probes/query43-x.json)

## Current dispositions of prior findings, advisories and observations

| id | current disposition | basis |
|---|---|---|
| S40-01 | REMAINS RESOLVED ON SOURCE43 | unchanged-42 basis plus current corroboration. The execution-inputs contract, schema, model and fixture and the enumeration contract/model are byte-identical 42->43 ({"execution-inputs-contract.v1.md": true, "execution-inputs.schema.v1.json": true, "execution_inputs_model.v1.py": true, "execution_inputs_fixture.v3.py": true, "enumeration-contract.v1.md": true, "enumeration_model.v1.py": true}), so the section 3 attribution predicate and section 8 capture exactness assessed in CH42-ATTRIBUTION-LAW and CH42-CAPTURE stand. Current: the execution-inputs child runs 95 cases and the enumeration child 54, each equal to root and to this origin's source42 receipts after removing only path fields, and the capture-join measurement is identical. |
| ADV40-01 | REMAINS RESOLVED ON SOURCE43 | implementation-planning-sources.v1.json and every docs/v2/architecture file (38 files) are byte-identical 42->43. The standing selects v11 (75ea60653d8c...) as current, v8 stays a superseded intermediate (bytes 99c8f8760c0e..., unchanged), and the prior-layer history digests match their bytes (True). No historical layer was mutated. |
| ADV42-01 | RETAINED ADVISORY (see advisories) | RETAINED ADVISORY, NON-BLOCKING. Root routing as an implementation verification obligation for crates/host/src/analysis.rs is assessed as correctly scoped; it is not a containment proof and no control was executed for it. |
| OBS42-01 | RETAINED OBSERVATION | execution_inputs_fixture.v3.py and execution_inputs_model.v1.py byte-identical 42->43 (True, True); the reference builder's single-producer attribution limitation is unchanged. |
| OBS42-02 | RETAINED OBSERVATION | enumeration-contract.v1.md and native_evidence_model.v2.py byte-identical 42->43 (True, True); the binder shorthand remains disambiguated within the same section. |
| OBS42-03 | RETAINED OBSERVATION (not re-probed) | Capture owner bytes unchanged; the refs-only capture consequence measured by the source42 three-tree probe stands; the execution-inputs child cases are equal modulo paths. |
| OBS42-04 | RETAINED OBSERVATION (not re-probed) | The same-scope re-encoding is a source40->42 identity change; source43 changes no execution-inputs byte, so no further re-encoding occurs. |
| OBS42-05 | RETAINED OBSERVATION | enumeration_model.v1.py byte-identical 42->43 (True); the explicit js-synthesized refusal stands; enumeration cases equal modulo paths. |
| OBS42-06 | RETAINED OBSERVATION | Enumeration bytes unchanged; unavailable-binding programEntry freedom stands, with no canonical encoding stated. |
| OBS42-07 | SUPERSEDED BY OBS43-04 (historical comparison not relabelled) | The source42 reference comparison stays historical; the source43 comparison is OBS43-04. |
| OBS42-08 | RETAINED (OBS43-06) | Ported probes re-observe every value on source43. |
| OBS40-01 | RETAINED-OBSERVATION (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION. On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-02 | RETAINED-OBSERVATION (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION. On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-03 | RETAINED-OBSERVATION (OBS42-08) (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION (OBS42-08). On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-04 | RETAINED-OBSERVATION (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION. On source43 the owning probe P43-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-05 | RETAINED-OBSERVATION (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION. On source43 the owning probe P43-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-06 | RETAINED-OBSERVATION (unchanged on source43) | Source42 disposition RETAINED-OBSERVATION. On source43 the owning probe P43-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-07 | CLOSED (unchanged on source43) | Source42 disposition CLOSED. The removed no-op continue stays removed (execution_inputs_model.v1.py byte-identical 42->43: True). |
| OBS40-08 | SUPERSEDED (historical comparison not relabelled) (unchanged on source43) | Source42 disposition SUPERSEDED. The historical comparisons stay historical; the source43 comparison is OBS43-04. |
| OBS40-09 | RETAINED (OBS42-08) (unchanged on source43) | Source42 disposition RETAINED (OBS42-08). On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-10 | HISTORICAL CORRECTION STANDS (unchanged on source43) | Source42 disposition HISTORICAL CORRECTION STANDS. The mapping population is 322 on source42 and source43 with 0 rows changed (measured). |
| S39-01 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| S39-02 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. On source43 the owning probe P43-PORTED-POLICY re-observes every row identically (26 rows). |
| ADV39-01 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. On source43 the owning probe P43-PORTED-RUNTERM re-observes every row identically (24 rows). |
| ADV38-01 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. On source43 the owning probe P43-PORTED-TERM7 re-observes every row identically (24 rows). |
| ADV38-02 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. On source43 the owning probe P43-PORTED-CARRIER re-observes every row identically (108 rows). |
| ADV38-03 | REMAINS CLOSED (unchanged on source43) | Source42 disposition REMAINS CLOSED. commit-recovery-readonly.v3.md is byte-identical 42->43 (True). |

## Item dispositions

### CH43-AVAILABILITY-REPORTING: SUFFICIENT AND CONSISTENT; CORRECTS A SOURCE42 UNDER-DISCLOSURE

Identity-and-evidence (:1715-1725) makes current availability a separate monotonic-generation record (retained, partial, expired, purged, corrupt, unavailable) and says a query reports both it and sealed assurance. Its section 5 selector (:1753-1767) hands graph availability to query contract section 7. GraphOperationResponseContext requires availability over exactly that enum. Workflows-and-surfaces (:1190, :1228-1229) makes availability a required query parity field projected from /queryResponse/context/availability, and query_surface_projection.v3.py (:47-53, :187-194, unchanged) copies ctx["availability"] verbatim. Source42 passed the literal "retained" to finish_operation, so an admitted partial observation was reported as retained: the response under-disclosed current availability, contrary to "a query reports both". Source43 section 7 (:162) requires reporting an observed retained or partial state exactly and never upgrading partial; the model returns the observed state. Independently discriminated on one lawful closed Run with each tree's own modules. For neighbors, path and reach, omitted and retained report retained on both trees, and partial reports retained on source42 and partial on source43. Items, termination and every other context field are identical across trees and observations. Omitted/retained responses are byte-identical across trees. The trusted-latest join and a cursor continuation under partial also disclose partial on source43. Through the reference adapter path, an admitted retained record with state partial reaches the response as partial on source43 (retained on source42); failing records are evidence.corrupt before any query. Parity: the graph-query-response parity field is partial on source43, and human/json/agent renderings recover it with parity holding. Omitted-observation behaviour is OBS43-01. The non-graph operations are unchanged (section 7: "It does not change the other seventeen operations").

### CH43-OBSERVATION-GRANTS-NOTHING: CONFIRMED (every refusal and precondition path)

The observation is consumed before close_run (model :1563) but only refuses or selects the reported state. close_run remains the positive admission (:1583), and view join, selection, projection and traversal follow unchanged. Measured identically on both trees: purged, expired, corrupt, unavailable and missing refuse HOST.IO_FAILURE with evidence.purged, expired, corrupt, missing and missing, operational-failed, exit 4, no run. A refusing observation routes before replay, even with missing bytes (evidence.purged). Null, unknown and non-string values raise ReferenceCallPrecondition host.availability. Corrupt and missing retained bytes refuse evidence.corrupt and evidence.missing under omitted, retained and partial observations, and through the record path a partial record with corrupt or missing bytes and a retained record with missing bytes refuse the same way.With a partial observation present, every public refusal keeps its route: schema major, malformed, project mismatch, relation, runId mismatch, missing latest, ambiguous snapshot, unavailable view, unknown endpoint and no retained Run. Adapter law: an out-of-vocabulary observation projects SYSTEM.OUTCOME.ILLEGAL_STATE / HOST.INVARIANT_VIOLATED / host-invariant / exit 4 with subject host.availability, no run and no runId. Without a RequestId it stays a precondition, and a RequestId precondition is never projected. Failing retained records (unparseable, unknown state, other Run, missing reason) are evidence.corrupt. No new public code is involved.

### CH43-PATH-EDGE-ORIENTATION: REPRESENTATION SELECTED FOR A PREVIOUSLY UNSPECIFIED FIELD; MODEL BEHAVIOUR PRESERVED; CONSISTENT

Source42 specified GraphPathEdge {factId, source, target} without an orientation (schema :817-836; GraphPathRow :847 fixes only zero-hop and the canonical fact2-id-sequence tie-break). Either reading of source/target was therefore open, and the earlier stored-orientation reading was not a defect under that law. Section 4 (:100) now selects the walk representation: edges[i] is the hop nodes[i]->nodes[i+1] under outgoing, incoming and both; factId still names the stored fact; neighbors rows keep the projected fact's source->target. path_unit already emitted traversal-oriented hops, and every orientation response is byte-identical across trees. On the real Run, the incoming and both paths bar->foo emit one hop bar->foo, the reverse of the stored fact, with the stored factId, while incoming neighbors of bar keep source foo/target bar. Incoming from the fact source finds no path. Zero-hop has nodes [start], edges [] and hopCount 0. Goldens: both s->t yields the shortest two-hop path with the lex-least fact2 sequence (1,3) and hops against both stored facts; incoming t->s yields (4,2) with hops t->y, y->s; outgoing uses stored directions (2,4); depth 1 finds no path; all goldens are identical across trees. hopCount equals len(edges) and nodes has hopCount+1 members within schema bounds (nodes 1-65, edges <=64). Order (:86) and bounds (section 5) are unchanged. No other owner consumes path edge orientation: identity :1754 and workflows :1151 hand graph law to the query contract, and the historical non-evaluator3 schema only names the operation (search output). Consequence: OBS43-03.

### CH43-CURSOR-BOUNDS-AND-PROSE: CONSISTENT; OPAQUE TOKEN FREEDOM RESPECTED

Section 5 (:138) and schema Page.cursor (:274-278) make the cursor an opaque host token of at most 256 characters, with a reference form, that grants no authority. This review claims no cross-host portability and requires no new canonical preimage; it checks only the same-host laws. Measured identically on both trees on the lawful Run: a two-row reach page issues the same token, and continuation returns the same second page. Cache loss ({}) and cache poison change nothing. Re-resolving latest, another runId, changed params, a position past the produced prefix and a malformed token each refuse QUERY.CURSOR_MISMATCH (request-rejected, exit 2). Historical selection by runId is the only continuation view. Bound admission: testBounds above a public cap refuses QUERY.PARAMS_MALFORMED, and a lowered visited cap under best-effort truncates with truncated-bound and lower-bound disclosure, identically. Prose law (source43 probe): a limitation note is any BoundedText (<=1024). Rewording it keeps GraphQueryResponseV1 admission and renderer parity, the note travels verbatim inside query-response parity, and an over-long note is refused. A success StepTermination admits no errorCode/reasonCodes/signal/faultCause. Refusal diagnostic prose is private: envelopes are identical for different diagnostics. Remedy wording changes only domainDetail.remedy, never class, errorCode, faultCause, detail or exit. Section 7 (:158) keeps refusal messages diagnostic while the table selects every route. No canonical wording is required or invented.

### CH43-NO-NEW-PUBLIC-SURFACE: CONFIRMED

The 42->43 delta is exactly nine files: the query contract, model and checker, the five source-pin ledgers and the workflows report. No schema, public-detail registry, identity, native, command inventory, surface projection or envelope byte changed ({"query_surface_projection.v3.py": true, "graph-query.schema.json": true, "common.schema.json": true, "command-envelope.schema.json": true, "command-inventory.v3.json": true, "identity-model.v3.py": true, "identity-schemas.v3.json": true, "native-evidence.schemas.v2.json": true, "public-detail-registry.v1.json": true}). No new public identity, error code or schema major exists: graph-query:3 is unchanged, and the adapter and refusal routes reuse existing codes. The same lawful Run closes to the same RunId on both trees, and package export stores are byte-equal to package19, so byte-derived identities are unchanged and nothing was reminted.

### CH43-PINS-AND-REPORT: CONFIRMED

Every entry of the five ledgers matches the formal manifest (foundation 1247, evaluator3 1251, native 1247, security 1247, workflows 1247; none added or removed). The four sibling ledgers repin exactly the three query owner files. The evaluator3 ledger additionally repins the four sibling ledgers. The workflows report updates only the checker, model and workflows source-pins digests. The evaluator3 pins sha equals the root and codex currentProfilePinsSha256 (True).

### CH43-PLANNING-V11: CONFIRMED (population measured; layer retained, not relabelled)

v11 (75ea60653d8c...) binds 31 inputs with no mismatch; none of them and none of the 31 coverage sources is among the nine changed files. Layers v8-v11 and all 38 docs/v2/architecture files are byte-identical to source42, so no layer12 is required and none is claimed. The planning checker reports 322 source-bound mappings and 54 planned failure cases (stdout sha equals the root verification: True); the inventory checker reports 198 unique paths in 20 packages. There are 0 mapping rows changed versus source42, 24 report features, M0-M6, and 54 recovery cases, none executed.

### CH43-PACKAGE20: VERIFIED AS AUTHOR EVIDENCE

See packageAssessment.

### CH43-CURRENT-REFERENCE: OWN EXECUTION PASSES; ROOT RECEIPTS CONSISTENT

This review's six groups and 17 children pass on its own verified copy, which is unchanged before and after every group. Query-projection runs 209 checks with 0 failed, execution-inputs 95 cases and enumeration 54. The comparison with root and codex is OBS43-04 and OBS43-05. The historical source42 receipts of this origin are preserved and not relabelled.

### CH43-SCOPE-PRESERVATION: SOURCE42 SCOPE RETAINED; NAMED BASIS

Each retained scope names its current source43 execution and, where applicable, its individually named unchanged-42 basis. Passing suites are corroboration, not assessment. Query changes reach the read-only response, availability and parity owners, which are assessed in CH43-AVAILABILITY-REPORTING although their bytes are unchanged.

| scope | basis | current source43 evidence | unchanged-42 basis |
|---|---|---|---|
| five product contracts and incorporated schemas | unchanged-42-basis + current execution | identity, security, native, workflows and admission contracts and the README index byte-identical ({"identity-and-evidence.md": true, "security-and-lifecycle.md": true, "native-evidence.md": true, "workflows-and-surfaces.md": true, "admission-and-qualification.md": true, "README.md": true}); the incorporated query contract changed and was fully read; all six groups pass | source42 AR-01..AR-16 row assessments and inheritedUnchanged42Read whole-file reads |
| architecture, tool, layout and report decisions | unchanged-42-basis + current execution | all 38 docs/v2/architecture files byte-identical; planning and inventory checks pass | CH42-PLANNING-V11 |
| 198 files in 20 packages; 322 mappings; M0-M6; 24 report features; 54 recovery cases | current execution | measured: 198 paths, 20 packages, 322 mappings (0 changed), M0-M6, 24 report features, 54 recovery cases not executed | - |
| native discovery, config, unitKind, allowJs, nested Cargo, clone normalization, custody | unchanged-42-basis + current execution | native group stdout equal root and own source42; native-consumer24-corrections and native-replay children {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True} / {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}; ported native (39 rows) and custody (20 rows) identical to source42; nine native-v2 membership probes content-equal to root | native bytes unchanged (native_evidence_model.v2.py True); source42 AR-07/AR-13 and OBS42-02 |
| enumeration default-vs-explicit binding, attribution and capture | unchanged-42-basis + current execution | enumeration (54) and execution-inputs (95) children equal to root and own source42 after removing path fields only; capture-join measurement identical; package binding-controls content-equal to root | CH42-ATTRIBUTION-LAW, CH42-CAPTURE, CH42-PROGRAM-ENTRY-CLARIFICATION, CH42-PROGRAM-ENTRY-ENFORCEMENT, CH42-HISTORICAL-POPULATIONS on byte-identical owners; the source42 three-tree view-attribution and program-entry probes were not re-run |
| policy.test known-hit, universe and import | unchanged-42-basis + current execution | ported policy probe 26 rows identical; policy-derivation child {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True} | policy_test_model.v3.py unchanged (True); S39-01/S39-02 closed |
| comparison counterfactuals, knowledge and identities | unchanged-42-basis + current execution | ported comparison probe 28 rows identical; comparison-knowledge child {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True} | source42 AR-10/AR-11 |
| nine command carriers and twenty operations | current execution | ported query carriers 98 rows identical; query-projection checker twenty-operation-names passes; command-inventory unchanged (True) | - |
| repair2 | unchanged-42-basis + current execution | ported repair:2 probe 16 rows identical | repair_closed_world_selection.v1.py unchanged (True) |
| security, discovery, commit, recovery and read-only carrier boundaries | unchanged-42-basis + current execution | security group stdout equal root and own source42; ported read-only carrier 108 rows and run-termination/commit-inventory 24 rows identical | carrier-dispatch.v3.json (True) and commit-recovery-readonly.v3.md (True) unchanged; ADV38-02/ADV38-03 |
| evaluator, import and termination bridges | unchanged-42-basis + current execution | children full-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, execution-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, candidate-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, composition {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, analysis-seal {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, provider-attribution-return {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, faults {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}, atoms {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine42': True}; ported section 7 termination 24 rows identical; query checker imports@resolved-target controls pass inside the 209 checks | CH42-COMPOSITION7-AND-POLICY-DERIVATION3 and CH42-IDENTITY-DIGEST-SCOPE on byte-identical owners (composition True, replay True, identity model True) |

Unchanged-42 items standing on byte-identical owners: CH42-ATTRIBUTION-LAW (SUFFICIENT AND CONSISTENT), CH42-CAPTURE (SUFFICIENT AND CONSISTENT), CH42-HISTORICAL-POPULATIONS (ACCOUNTED), CH42-PROGRAM-ENTRY-CLARIFICATION (CONSISTENT; NO SEMANTIC CHANGE), CH42-PROGRAM-ENTRY-ENFORCEMENT (CONFIRMED), CH42-IDENTITY-DIGEST-SCOPE (SUFFICIENTLY EXPLICIT; NO CLARIFICATION REQUIRED), CH42-COMPOSITION7-AND-POLICY-DERIVATION3 (SOURCE40 NO-GAP FINDINGS PRESERVED)

| ported probe | rows | same case set as source42 | observations differing from source42 |
|---|---|---|---|
| P43-PORTED-POLICY | 26 | True | 0 |
| P43-PORTED-NATIVE | 39 | True | 0 |
| P43-PORTED-RUNTERM | 24 | True | 0 |
| P43-PORTED-QUERY | 98 | True | 0 |
| P43-PORTED-CARRIER | 108 | True | 0 |
| P43-PORTED-COMPARISON | 28 | True | 0 |
| P43-PORTED-REPAIR2 | 16 | True | 0 |
| P43-PORTED-TERM7 | 24 | True | 0 |
| P43-PORTED-CUSTODY | 20 | True | 0 |
| P43-PORTED-CAPTURE-JOINS | 4 | True | 0 |

## Package v20

Package v20 verified as author evidence. All 387 files match artifact manifest 803d1e16...; the formal43 manifest db43ee76... and the files-only projection d7f43243... are different objects with equal file members, and the package copy of the formal manifest equals the live one. The rebuild base is package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15); packages 16, 17, 18 and 19 remain unchanged history. Every current export store is byte-equal to package19 at the same path, so the byte-derived RunIds are unchanged and nothing was reminted; the root formal binding records all 17 source42 comparisons as same RunId and same export bytes. This review re-executed verify-package.py and probe-native-v2.py on its own verified source43 copy: groups checkpoint3 1 (passed True, exit 0), normalized-examples6 4 (passed True, exit 0), rust-selection-examples1 2 (passed True, exit 0), semantic-controls1 3 (passed True, exit 1), binding-controls 3 (passed True, exit 1), normalization-map-controls1 4 (passed True, exit 1), query 7 (passed True, exit None); 17 exports and 7 queries; the verification and every compared output file are content-equal to the root final43 verification, and the 9 membership comparisons are content-equal to the root rebuild probe.

- Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.
- Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.
- The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.
- No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.

| control | owner admission | semantic admission | reason |
|---|---|---|---|
| ts-map-absent | REFUSE | NOT-REACHED | BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json |
| ts-map-level-unmapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim |
| ts-map-level-swapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim |
| ts-spec-outside-closure | REFUSE | NOT-REACHED | BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim |

## Commands and probes

| group | exit | seconds | stdout sha256 | equal root | equal codex | equal own source42 |
|---|---|---|---|---|---|---|
| evaluator3 | 0 | 487.6 | `2ddf8f99c46365462636ae191ff71c1800424e00c460fc335bc47f9a3659ef1b` | True | True | True |
| foundation | 0 | 127.8 | `2a7cd6d84cf029f12d43c4a34c7a91b4817167f8d88e07dc1721c87f78ef3ded` | True | True | True |
| integration | 0 | 16.6 | `3fccd9e3a400774d6f411e530a22848ec38eae5a30e737f4c66bf75254d20112` | True | True | True |
| native | 0 | 3.0 | `49fca461221535d2306dfe19a99cec49a26e6bc78ed3c9f777473073b65a1406` | True | True | True |
| security | 0 | 1.0 | `60d498d317776373a82f941db5a82a78b5eca33ba6d8f57eeb387a9a081ca746` | True | True | True |
| workflows | 0 | 9.6 | `954ebf2eedafc242f2998bcfb9f4ff4c18bd80063ad9b0edce34b7beebd14e51` | True | True | True |

evaluator3 children: 17, all exit 0: True; query-projection checks 209 (failed 0); execution-inputs cases 95; enumeration cases 54. Planning: {'check_implementation_planning': 'PASS: 322 source-bound mappings, 54 planned failure cases, private schema, owners and generated plan', 'check_repository_file_inventory': 'PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches'}. Planning counts ok: True.

| probe | rows | failed | run receipt | earlier attempts |
|---|---|---|---|---|
| P43-SUBJECT | (command receipt) | - | receipts/subject-verification.json, receipts/manifest43-index.json | - |
| P43-ARCHIVE | (command receipt) | - | receipts/archive-verification.source43.json, receipts/archive-verification.source43-pkg.json, receipts/archive-verification.base42.json | - |
| P43-DELTA | (command receipt) | - | receipts/delta-diff-summary.json | - |
| P43-GROUPS | (command receipt) | - | receipts/reference/groups-report.all.json, receipts/reference/evaluator3.stdout, receipts/reference/foundation.json | - |
| P43-REFERENCE-COMPARE | - | 0 | receipts/runs/reference-comparison-v43.run.json | 0 |
| P43-REFERENCE-CHILDREN | - | 0 | receipts/runs/reference-children-stripped.run.json | 0 |
| P43-PINS | - | 0 | receipts/runs/source-pins43.attempt2.run.json | 1 |
| P43-PLANNING | - | 0 | receipts/runs/planning-checks-v43.run.json | 0 |
| P43-QUERY-X | 66 | 0 | receipts/runs/query43-x.run.json | 0 |
| P43-QUERY-ADAPTER-X | 22 | 0 | receipts/runs/query-adapter43-x.attempt2.run.json | 1 |
| P43-QUERY-PROSE | 8 | 0 | receipts/runs/query-prose43.run.json | 0 |
| P43-PORT | (command receipt) | - | receipts/probe-port43.json | - |
| P43-PORTED-POLICY | 26 | 0 | receipts/runs/ported-policy.run.json | 0 |
| P43-PORTED-NATIVE | 39 | 0 | receipts/runs/ported-native.run.json | 0 |
| P43-PORTED-RUNTERM | 24 | 0 | receipts/runs/ported-runterm-adv.run.json | 0 |
| P43-PORTED-QUERY | 98 | 0 | receipts/runs/query-carriers.run.json | 0 |
| P43-PORTED-CARRIER | 108 | 0 | receipts/runs/carrier-readonly.run.json | 0 |
| P43-PORTED-COMPARISON | 28 | 0 | receipts/runs/comparison-knowledge.run.json | 0 |
| P43-PORTED-REPAIR2 | 16 | 0 | receipts/runs/repair2.run.json | 0 |
| P43-PORTED-TERM7 | 24 | 0 | receipts/runs/run-termination-s7.run.json | 0 |
| P43-PORTED-CUSTODY | 20 | 0 | receipts/runs/native-custody-fallback.run.json | 0 |
| P43-PORTED-CAPTURE-JOINS | 4 | 0 | receipts/runs/capture-joins-on43.run.json | 0 |
| P43-PACKAGE20 | 28 | 0 | receipts/runs/package-v20-evidence.run.json | 0 |
| P43-COPIES-FINAL | - | 0 | receipts/runs/copies-final.run.json | 0 |

## Read coverage

Whole-file claims only for fresh43Read (every line read this charter) and inheritedUnchanged42Read (counted as completely read by this origin's completed source42 review and byte-identical now; not re-read). complete42ReadPlusComplete43Diff is a complete predecessor read plus the exact diff. Delta reads, range reads, evidence reads and search-only sightings are not whole-file reads of source43 bytes. Hashes recomputed at build time.

```json
{
 "fresh43Read": 1,
 "fresh43RangeRead": 9,
 "deltaReads": 9,
 "complete42ReadPlusComplete43Diff": 0,
 "inheritedUnchanged42Read": 54,
 "changedPriorReadNotReread": 0,
 "evidenceReads": 19,
 "searchOnlySightings": 13
}
```

Delta files without a read entry: none.

Fresh whole-file reads:

- docs/coop/design-corrections/workflows/query-projection-contract.v3.md (209 lines, sha256 `47ccc81ccc33263520affe0340946aba5178bcac33131de88e6be638a1718d5f`)

Range reads:

- docs/coop/design-corrections/foundation/identity-schemas.v3.json: 1641-1701, 79-148 (sha256 `a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21`)
- docs/coop/design-corrections/workflows/check-query-projection.v3.py: 1-200,380-469,488-779, 41-48,713-761,1181-1214 (sha256 `466d6abb2a9ccdb2be7e6a0b655e9e33cef94fc64d5facdfb478bc6b58a531f9`)
- docs/coop/design-corrections/workflows/command-inventory.v3.json: 331-361 (sha256 `d303cc640154ff2b4473452c52f6578b5ffa3f20d6ed03c3976e0ddd397a4e66`)
- docs/coop/design-corrections/workflows/query_projection_model.v3.py: 1-127,260-370,565-712,1112-1663 (sha256 `9a8f9c09c70cf56aff8f353b7592fb5ce0eb2a58ad101a08a1ce56f006568b7c`)
- docs/coop/design-corrections/workflows/query_surface_projection.v3.py: 25-273,540-609 (sha256 `26106f4e523d6defa986f435de10606c60056ed6ca967baa411be0c6293a07b2`)
- docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json: 132-135,743-837 (sha256 `ce45b9ff712fa0ea4302fbdaf04cb84dfd8a3cf734f4f9677c4547672af30a8b`)
- docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json: 820-1149, 817-865 (sha256 `33a43bd86ec7bcb18e5d4ac3d65f5543f57b7d22168a004edd4f1dad285febe9`)
- docs/v2/contracts/product-v1/identity-and-evidence.md: 1700-1774, 1710-1727 (sha256 `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f`)
- docs/v2/contracts/product-v1/workflows-and-surfaces.md: 1180-1239, 312-325,682-693 (sha256 `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed`)

Complete diff reads:

- docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json (delta42to43Read; diff `4be7910fcb015aa8661d611e419dd79cb2972920aaf6cd471ab915981683bd4f`)
- docs/coop/design-corrections/foundation/source-pins.v1.json (delta42to43Read; diff `46d36200d6a2f9c5394433dcb11e164f748fcf5279323f5c0e3e6bbe255eac8c`)
- docs/coop/design-corrections/native/source-pins.v2.json (delta42to43Read; diff `308535c662e269b4585bc659a374e46c80b437b2ec18bc8244b1f4a25557d71e`)
- docs/coop/design-corrections/security/source-pins.v1.json (delta42to43Read; diff `e0f0ea63bbb6b6101300d55db894a311d06eae5408b6a5067ecd26425830541b`)
- docs/coop/design-corrections/workflows/check-query-projection.v3.py (delta42to43Read; diff `7e74a068135fb3d6fe2688251eb95deb2f0a7f04514b32835e78167ea1d5d772`)
- docs/coop/design-corrections/workflows/query-projection-contract.v3.md (delta42to43Read; diff `3f0fe7e48aade319a2ff71b0595899bd2088cb25b69f8839030a628a56c61f13`)
- docs/coop/design-corrections/workflows/query_projection_model.v3.py (delta42to43Read; diff `48ecb9f0a3bb0cb89ebde0ce7c65b6ed932750ba6a5a69c994aa79bf0d200aa5`)
- docs/coop/design-corrections/workflows/source-pins.v1.json (delta42to43Read; diff `eeaa09200d87d6afb8c022f1251798020230c073c4b660086b9362404119ee77`)
- docs/coop/design-corrections/workflows/workflows-report.v1.json (delta42to43Read; diff `5bd785c9b61c4c4377543abc00248390024217f05b7669e4e5e16dae5c3a4d15`)

Evidence reads:

- /Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v43/reference-checks.json: 1-154
- /tmp/opensip-design-corrections/author-package-final43-verification.v1/verification.json: 1-60
- /tmp/opensip-design-corrections/claude-author-package-successor.v20/artifact-manifest.json: 1-30
- /tmp/opensip-design-corrections/claude-author-package-successor.v20/source-binding.v43.json: 1-14
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/build_review42.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/build_review42_emit.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/build_review42_findings.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/build_review42_rows.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/compare_enumeration_receipts.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/compare_reference_v42.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/port_v40_probes.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/probe_package_v19.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/run_planning_checks42.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/probes/verify_base_copies.py: complete
- /tmp/opensip-design-corrections/claude-independent-design.v42/review.json: 1221-1484
- /tmp/opensip-design-corrections/root-author-package-final43-rebuild.v1/rebuild-report.json: 1-80
- /tmp/opensip-design-corrections/root-author-package-formal43-binding.v1/binding.json: 1-157
- /tmp/opensip-design-corrections/root-query43-independent-note.v1/note.json: complete
- /tmp/opensip-design-corrections/root-source43-planning-verification.v1/verification.json: 1-33

Search-only sightings (not reads):

- docs/coop/design-corrections/workflows/query_projection_model.v3.py: top-level def/class lines 128-259, 371-564, 713-1111 (function map in search output) — signatures seen in search output only, outside the ledgered ranges
- docs/coop/design-corrections/workflows/query_surface_projection.v3.py: 507, 572, 742, 903 (availability search output) and 431-454, 595-751 renderer call sites — seen in search output only, outside the ledgered ranges
- docs/coop/design-corrections/workflows/check-query-projection.v3.py: 223-227, 869 (graph.path search output) — seen in search output only
- docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json: 90-111, 160-261, 262-280, 293, 311, 355-391, 429, 470, 495-510, 754-779, 797-803, 871, 960-961, 1120, 1133 (search output) — seen in search output only, outside the ledgered ranges
- docs/coop/design-corrections/workflows/schemas/graph-query.schema.json: 78 (operation name in search output) — historical non-evaluator3 schema; one line seen in search output
- docs/v2/contracts/product-v1/identity-and-evidence.md: 878, 1184, 1465, 1473, 1483, 1524, 1672 (search output) — seen in search output only
- docs/v2/contracts/product-v1/workflows-and-surfaces.md: 408, 446-447, 706, 925, 1273, 1302-1303, 1325, 1637 (search output) — seen in search output only, outside the ledgered ranges
- docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py: 287, 300, 510-517, 598, 606, 613, 800-801 (search output) — fixture keys seen in search output only
- docs/coop/design-corrections/workflows/command-inventory.v3.json: 2-5, 368, 1634, 1678, 1745 (search output) — seen in search output only
- docs/coop/design-corrections/workflows/schemas/evaluator3/{command-inventory,comparison-result,invocation-record,repair,review,sarif-adapter}.schema.json: note/remedy property lines (search output) — seen in search output only
- docs/v2/architecture/{implementation-boundaries-and-build-plan.md,14-repository-and-module-layout.md,implementation-coverage.v1.json}: crates/host/src/analysis.rs and graph.path occurrences (search output) — seen in search output only
- docs/coop/hydradb-review/hydradb-opensip-fit-gap.md: 31 (graph.path search output, line omitted as too long) — non-normative review note; file name only
- docs/coop/design-corrections/reviews/** inside the frozen snapshot (including consumer-b.v1-v8 subject copies and tool-calls, bv3-bv6 corrections-author copies, grok-* query reviews, query-successor-root-review.v1-v3, v20-advisory-assessment, hydradb-proposal-assessment): file names and single matching lines surfaced by two broad content searches over docs/ before the searches were restricted with !**/reviews/** — UNINTENDED search-output sightings of snapshot-internal historical review copies; no such file was opened or read and nothing from them is used; all later searches excluded reviews/**

Inherited unchanged source42 whole-file reads (not re-read): 54 files; complete source42 read plus complete 42->43 diff: 0; listed in review.json.

## TCB-SCOPE-01 (assessed once)

**Assumption.** Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.

**Consequence.** Rejecting or changing the assumption reopens the thirteen dependent rows jointly, not as thirteen independent proofs. It repairs no historical attack and qualifies no containment. All thirteen author grades stay PENDING.

**Dependent rows (13).** RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c

**Current assessment.** NOT REJECTED: coherent as a scope selection on source43 and unqualified; the source43 changes add response disclosure, not trust.

- Coherent as a scope selection on source43: admission section 5 (byte-identical 42->43: True) and prototype-report-inventory (byte-identical: True) still admit no untrusted native/WASM, imperative contributions or executable report hooks.
- The source43 changes add typed response disclosure and a representation pin, not trust. Availability observations and retained records can only refuse or select the disclosed state, and close_run remains the positive admission on every graph read.
- Host observations stay TCB inputs. A product adapter's out-of-vocabulary observation is a host-invariant fault, not evidence. Capture remains a host observation: ADV42-01 is retained as an implementation verification obligation, not a trust-boundary violation.
- Providers stay untrusted: view producer closures must be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND re-measured on source43).
- Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries, and all 32 gates are unperformed (qualified=true 0).

**Position:** NOT REJECTED. **Standing:** ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE43; final application adjudication not granted. **Adjudication owner:** separate final application review, by a NEW different actual Claude origin (not this origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7 and not any author, design or blind origin)

## Disposition rows (107)

All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned; scoped owner rows are routing only.

**Basis rule.** unchanged-42-basis: the governing owner bytes are byte-identical 42->43, and the conclusion rests on that identity plus this origin's named source42 row assessment, quoted in unchanged42Basis. Re-executed suites and ported probes are corroboration only. new-43: the conclusion rests on a source43 read, diff, probe or measurement newly performed under this charter, including rows whose bytes are unchanged but whose read-only response, availability or parity owner is affected by the query change. Every row carries its own current text, current owner and consequence. No row is carried forward in bulk, and no grade is assigned. Counts: {"new-43": 33, "unchanged-42-basis": 74}.

| id | prior42 | disposition | basis | current assessment | owner | consequence |
|---|---|---|---|---|---|---|
| F-01 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-01: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-02 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-02: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-03 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-03: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-04 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-04: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-05 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-05: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-06 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-06: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-07 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-07: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-08 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-08: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-09 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-09: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-10 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-10: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-11 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-11: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-12 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-12: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-13 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-13: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| F-14 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-42-basis | F-14: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source43 change; remains carried without regrade and is not source43 acceptance. |
| RES-EP13-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Plan and derivation joins stay inside complete replay on byte-identical owners (evaluator_replay_model True, identity-model True); the full-replay child equals root and this origin's source42 receipt, and the lawful query Run closes to the same RunId on both trees. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; residual retained. |
| RES-EP13-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. Capture and current availability are both trusted host observations. The ported capture-join measurement on source43 still admits a non-provider-producer view and refuses it only at closure (ADV42-01), and an availability observation or record only refuses or selects the disclosed state, never admission (CH43-OBSERVATION-GRANTS-NOTHING). No answer-provenance claim against the host is made. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Admission contract (True) and residual ledger (True) byte-identical 42->43; the finite historical measurement is unchanged. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; finite historical measurement unchanged. |
| RES-EP13-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. Closed input admission is unchanged, and the query adds no open input. The availability observation is a closed vocabulary: null or unknown values are a reference precondition and, in a product adapter, a host-invariant fault; retained availability records failing identity admission are evidence.corrupt (P43-QUERY-X, P43-QUERY-ADAPTER-X). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | The frozen subject was verified outside every author instrument: formal43 manifest db43ee76..., archive d1ff8312..., all 12,913 members by hash and length, parent42 f602fc7e... (12,913 members), the declared chain, the exact 9/0/0 delta and every entry of the five pin ledgers. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | canonical.py stays outside the delta (True). The ported run-termination probe recomputes the commit-inventory digest over a closed source43 Run with the reviewer's own C()/H(), with every row identical to source42. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Seal and replay owners byte-identical 42->43; the analysis-seal child equals root and this origin's source42 receipt. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-08 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | A bounded historical measurement. Source43 adds a response-disclosure correction and a representation pin and claims no proof over all PlanIntents. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-09 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Provenance stays distinct from correctness on source43: package v20 semantic-controls1 keeps owner ADMIT with semantic REFUSE, content-equal to the root final43 verification, and a partial availability disclosure never turns a failing closure into an answer. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-10 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Author self-counters did not decide this review. The five added checker controls (204 -> 209) are reference self-consistency; the decisive evidence is the reviewer's own old-versus-new discrimination with each tree's own modules (P43-QUERY-X, P43-QUERY-ADAPTER-X). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-11 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Failures stay recorded by cause. This review preserves its first query-probe launch (the parent failed after a child could not write into a not-yet-created receipts/probes directory), the pin checker attempt 1 (a ledger key assumption) and the adapter probe attempt 1 (four rows built with an inadmissible missingRefs record). The root planning verification keeps its exit-2 prior attempt. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-12 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. No sole Python guard enters product authority: close_run remains the positive admission for every graph read, and SELECTED_COVER still detects internal capture inconsistency, never malicious omission. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-13 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. The discrimination probes ran each tree (base42, source43) in its own process on verified copies, which were re-verified unchanged afterwards (copy-verification-final.json). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-14 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | The differential census is not used as an oracle; the source43 delta touches no census owner. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-15 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | The C-2 v4 self-census is not elevated. Enumeration owners are byte-identical 42->43, and their 54 checker cases equal the source42 receipt after removing path fields only. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-16 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: row-attribution re-derivation and exact VIEW_TOTALITY sit in byte-identical execution-inputs owners (True), and the 95 cases are unchanged. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-17 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Text-only disclosures remain text-only. Source43's two contract sentences are not text-only: each is paired with model behaviour and checker controls and was independently discriminated. Limitation notes stay bounded free text carried by parity (P43-QUERY-PROSE). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-18 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Depends on TCB-SCOPE-01. Native discovery and custody bytes are unchanged and marker observations stay trusted; ported native (39 rows) and custody (20 rows) observations are identical to source42. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-19 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Substantive review on source43: old-versus-new discrimination on a lawful closed Run, the adapter path and the prose law. The retained advisory's standing was assessed rather than carried, and all pinned groups pass. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. Every source43 probe ran in-process with owner modules (the query and adapter probes in one process per tree); containment is not claimed. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | No name scan decides a query route: close_retained_run routes by the typed identity outcome, the availability observation by a closed vocabulary, and section 7 forbids selection by filename, exception prefix or caller-supplied fault origin. The checker control close-retained-run-routes-without-message-parsing passes. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process. Host availability, latest and snapshot observations are trusted host context, which is why each can only refuse or select, never admit. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01; one TCB account, assessed once on source43, covers all thirteen rows. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Contradictory prose still needed substantive review. Source42 identity law said a query reports current availability, while the graph model reported retained for an admitted partial observation; source43 aligns contract section 7 and the model, and the alignment was discriminated on both trees. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Historical attacker cost preserved as history; no source43 file addresses it. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | The original environment is preserved; this review names its interpreter (/tmp/opensip-architecture-review-env/bin/python -I -B) and verifies every pin. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| AX6 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. None of the nine source43 delta files claims same-process route-region protection (all nine diffs read). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AX9 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. The source43 additions (disclosed availability state, hop representation) are typed response data under a trusted evaluator, not a protection mechanism. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| MD5 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-43 | Depends on TCB-SCOPE-01. Source43 adds no Python-containment mechanism (delta read). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RX2c | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-42-basis | Depends on TCB-SCOPE-01. Complete replay and full-Run closure on the same manifest remain reproducibility evidence, not containment, and the replay owners are byte-identical 42->43. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AR-01 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Admission section 1 byte-identical 42->43; ported query carriers (98 rows) identical. | docs/v2/contracts/product-v1/admission-and-qualification.md (§1) | No change required. |
| AR-02 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Admission sections 2-4 and the qualification gate ledger byte-identical 42->43: 32 gates, none qualified (qualified=true 0); no delta file is a gate owner. | docs/v2/contracts/product-v1/admission-and-qualification.md (§§2–4) | All gates stay unperformed. |
| AR-03 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Security discovery text byte-identical; ported custody rows identical. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Discovery) | No change required. |
| AR-04 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Security trust time byte-identical; security group stdout equals root. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Trust time) | No change required. |
| AR-05 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Security root chain and revocation byte-identical; no delta file touches them. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Root chain and revocation) | No change required. |
| AR-06 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Platform admission and carrier DDL byte-identical; ported read-only carrier rows (108) identical. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Platform admission) | No change required. |
| AR-07 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Native sections 3/5/9 byte-identical; native group stdout equals root and source42. | docs/v2/contracts/product-v1/native-evidence.md (§§3/5/9) | No change required. |
| AR-08 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Invocation and repair text byte-identical; ported repair:2 rows identical. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Invocation and repair) | No change required. |
| AR-09 | NO-NEW-ISSUE (ADVISORY ADV42-01) | NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED) | new-43 | identity-and-evidence is byte-identical, and graph responses now honour its current-availability law (:1718-1725, "A query reports both"): source43 section 7 reports an observed partial state instead of retained (CH43-AVAILABILITY-REPORTING). Section 5 (:1753-1767) still routes refusing states through query section 7. S40-01 remains resolved; ADV42-01 is retained. | docs/v2/contracts/product-v1/identity-and-evidence.md (§§1–6) | No change required; the advisory is optional. |
| AR-10 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Baseline and comparison text byte-identical; ported comparison knowledge rows identical. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Baseline and comparison) | No change required. |
| AR-11 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Comparison and import text byte-identical; the execution-inputs child equals root after removing path fields only. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Comparison and import) | No change required. |
| AR-12 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Native section 4 and atoms byte-identical; atoms child equals root and source42. | docs/v2/contracts/product-v1/native-evidence.md (§4) | No change required. |
| AR-13 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Native sections 1/2/6/8 and discovery byte-identical; enumeration cases equal source42 after removing path fields only. | docs/v2/contracts/product-v1/native-evidence.md (§§1/2/6/8 plus workflow output/security discovery) | No change required. |
| AR-14 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Stage transition and lease bytes unchanged; no delta file is a lifecycle owner. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Stage transition and lease model) | No change required. |
| AR-15 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-42-basis | Contract index README byte-identical; the query contract stays incorporated through workflows-and-surfaces section 8. | docs/v2/contracts/product-v1/README.md (Entire contract index and D-372 application) | No change required. |
| AR-16 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-43 | workflows-and-surfaces is byte-identical, but the query change reaches its query command outcomes and parity: the availability parity field (:1190, :1228-1229) now carries partial exactly, every graph refusal route and exit is unchanged, and no D9 code is added. The D9 successor stays carried. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (D9 and command outcomes plus native/security guidance) | No change required. |
| FW-01 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | discovery.rs binding construction obligation unchanged; enumeration owners byte-identical. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/discovery.rs (M3) | Not executed. |
| FW-02 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | review.rs review-brief carriers unchanged; ported carriers identical. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-03 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-43 | analysis.rs composes provider work, admission, evaluation and complete replay (layout 14 :475, search output). Beyond the source42 capture obligation it now carries the ADV42-01 implementation verification obligation: never list a returned view on another producer's complete receipt. The root note routes it there, and this review assesses the routing as correctly scoped but not executed. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/analysis.rs (M3) | Implementation verification obligation retained; not executed. |
| FW-04 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | imports.rs unchanged; typed-null targetUniverse account stands. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/imports.rs (M5) | Not executed. |
| FW-05 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | comparison.rs presence knowledge unchanged; ported comparison rows identical. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-06 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | finalization.rs delivery laws unchanged; commit-inventory recipe re-derived identically on source43. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/finalization.rs (M5) | Not executed. |
| FW-07 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | invocation.rs argvDigest unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/invocation.rs (M5) | Not executed. |
| FW-08 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-43 | outcomes.rs detail allowlist is unchanged and sufficient for source43: the adapter's invalid availability observation uses the existing HOST.INVARIANT_VIOLATED detail, and every availability refusal uses an existing evidence.* detail (P43-QUERY-ADAPTER-X). No detail is added. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/outcomes.rs (M3) | Not executed. |
| FW-09 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | review.rs candidates/inspect carriers unchanged; their non-graph context keeps availability=retained (workflows :687-689). Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-10 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | repair.rs repair:2 constructor unchanged; ported repair rows identical. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/repair.rs (M5) | Not executed. |
| FW-11 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | comparison.rs baseline.show unchanged; pivot-closure availability is a separate non-graph surface. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-12 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | review.rs produce-brief host-only unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-13 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | configuration.rs policy-test admission routes unchanged; ported policy rows identical. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/configuration.rs (M3) | Not executed. |
| FW-14 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | discovery.rs recommend units unchanged; the same binding construction rule applies. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/discovery.rs (M3) | Not executed. |
| FW-15 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-42-basis | policy.rs show/test unchanged; the policy-derivation child equals source42. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: True). | crates/host/src/policy.rs (M5) | Not executed. |
| DR-001 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | current-source-map and residual ledgers byte-identical 42->43. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-002 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | ExecutionInputsV1 view attribution and exact selection remain published on byte-identical owners; S40-01 remains resolved. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-003 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Read-only carrier routes unchanged; the graph query remains a read that mints no Run; 54 recovery cases unexecuted. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained; release demonstration still required. |
| DR-004 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Native binding construction consumed by enumeration unchanged; the explicit TS/JS null refusal stands. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-005 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Custody reference groups pass unchanged; native carrier qualification still required. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-006 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Descriptor graph unchanged; the full-replay child equals root and source42. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-007 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | The D9 published successor artifact remains a carried implementation-unit obligation; source43 adds no D9 code. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation; not a new blocker. |
| DR-008 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | The applied retention posture is unchanged. Its current-availability consequence is now disclosed by graph responses exactly (partial is never upgraded), and refusing states still refuse. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-009 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | The host capture stays outside the sealed Run on byte-identical owners; census exclusion unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-010 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Bounded first-party composition unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | The blind implementer litmus follows final integration and is not closed by this review. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011-R01 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Fact-plane successor schemas unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R02 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Imperative plugins stay outside D-371. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R03 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | plan2 EnumerationPlanV1 binding joins unchanged; explicit TS/JS null entries still refuse. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R04 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | carrierFormat mapping unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R05 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Rust protocol major 3 unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R06 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Typed close_run outcomes were re-exercised through the graph query on source43: EvidenceUnavailable -> evidence.missing and AdmissionError -> evidence.corrupt under every observation, identical to source42. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R07 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Query retained-availability routes are unchanged on source43 (purged, expired, corrupt, unavailable and missing refuse with exit 4), while a successful read now reports the observed partial state; measured on both trees. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R08 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | D9 successor remains carried (DR-007). Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation. |
| DR-011-R09 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Semantic identity still excludes attempt identity and current availability: the same lawful Run closes to the same RunId on both trees, availability sits outside the cursor binding, and package export stores are byte-equal to package19. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R10 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | OPEN: this nonblind review cannot close the fresh blind implementer litmus. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained open. |
| DR-011-R11 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | Real platform durability unmeasured; 54 cases not executed. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R12 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Depends on TCB-SCOPE-01, assessed once on source43. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained; reopens with TCB-SCOPE-01 only. |
| DR-011-R13 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Source43 changes a response value (availability disclosure) and pins a representation without a schema major or identity record change; graph-query:3 bytes are unchanged, consistent with the composition profile. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R14 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | CFG-6/TM unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R15 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-43 | Trusted request context stays host-only: requestId, availability, latestRunId and runsForSnapshot are host observations that the reference takes as call arguments and a product adapter supplies; none is request-authored. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R16 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-42-basis | No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: True) is consistent with source43. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-201 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-43 | Semantic-correctness owner row: the source43 availability disclosure correction, the path hop representation and the retained ADV42-01 fall in its area. Register 08 byte-identical 42->43 (True). | register 08 condition-3 review owner row DR-201 | Input to the integrated review; routing only, not applied. |
| DR-202 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-42-basis | Delivery/operations owner row: recovery, repair and loader TCB unchanged. Register 08 byte-identical 42->43 (True). | register 08 condition-3 review owner row DR-202 | Input to the integrated review; routing only, not applied. |
| DR-203 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-42-basis | Prototype-lessons owner row (PARTIAL-SCOPED): no delta file is the prototype reference. Register 08 byte-identical 42->43 (True). | register 08 condition-3 review owner row DR-203 | Input to the integrated review; routing only, not applied. |
| DR-204 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-43 | V1/coop invariant owner row: every pin of the five ledgers verified against the formal manifest; the ledgers repin only the three query owner files and the sibling ledgers; layer v11 retained with unchanged inputs. Register 08 byte-identical 42->43 (True). | register 08 condition-3 review owner row DR-204 | Input to the integrated review; routing only, not applied. |
| DR-205 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-43 | Small-core/components owner row: TCB-SCOPE-01 remains coherent on source43. Register 08 byte-identical 42->43 (True). | register 08 condition-3 review owner row DR-205 | Input to the integrated review; routing only, not applied. |

The quoted source42 basis of every unchanged-42-basis row is in review.json (`unchanged42Basis`).

## Retained obligations

```json
{
 "residuals": 30,
 "authorGradesPending": 30,
 "condition2Obligations": 28,
 "condition2Source": "docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 42->43: True)",
 "productQualificationGates": {
  "count": 32,
  "qualifiedTrue": 0,
  "standing": "UNPERFORMED"
 },
 "plannedRecoveryCases": {
  "count": 54,
  "notExecuted": 54,
  "standing": "UNPERFORMED"
 },
 "condition5": "NOT MET (not a design defect)",
 "d9PublishedSuccessor": "Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.",
 "adv4201ImplementationVerification": "crates/host/src/analysis.rs verification that no returned view is listed on another producer's complete receipt (root note routing; not executed).",
 "gradeAndConditionOwner": "All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.",
 "finalApplication": "Requires a NEW different actual Claude origin, not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin.",
 "acceptanceStanding": "Source-level acceptance only; distinct from final application, readiness and product qualification."
}
```

## Authority

```json
{
 "gradeGranted": false,
 "activationGranted": false,
 "implementationAuthorized": false,
 "blindReconstructionClaimed": false,
 "freshOriginIndependenceClaimed": false,
 "source42ReviewConclusionInherited": false,
 "frozenInputsModified": false,
 "applicationOrReadinessGranted": false,
 "productQualificationGranted": false,
 "blindConsumerArtifactsOrOutcomesAccessed": false,
 "queryAuthorRuntimeOrReportsRead": false,
 "historicalExportsRelabelled": false,
 "runIdsReminted": false,
 "productCommitPushOrActivation": false,
 "subagentsWebOrPrivateLogsUsed": false
}
```

## Limitations

- Nonblind successor review by the same origin that completed the source40 and source42 reviews; not fresh-origin independence. The source-only note, root reference/planning/package records and codex receipts were read as evidence. The query-author runtime and reports were not read, and no blind consumer artifact, export, helper, review or root blind outcome was read.
- Two broad content searches over docs/ surfaced file names and single matching lines from snapshot-internal historical review directories (including consumer-b.* and bv*-corrections-author copies) before the searches were restricted with !**/reviews/**. None of those files was opened or read, and nothing from them is used (readScope.searchOnlySightings).
- Reference Python models over synthetic inputs; no product code. No compiler, provider, host adapter, evidence store, OS durability, process isolation or cryptography is qualified. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).
- Whole-file claims are limited to fresh43Read and inheritedUnchanged42Read. The query contract was freshly read completely. The model and checker were read in named ranges plus their complete 42->43 diffs, and the other changed files as complete diffs. Range reads and search-only sightings are listed separately and are not whole-file reads.
- Closed-run discrimination used one lawful TypeScript semantic fixture Run plus algorithm goldens over projected edges; the adapter path exercised the reference adapter laws, not a product adapter. No multi-provider, multi-stage Plan was minted, so the ADV42-01 multi-provider shape stays argued from source.
- The source42 three-tree view-attribution and program-entry probes and the case-population comparisons were not re-run. Their conclusions stand on byte-identical owners and are named as unchanged-42 basis, corroborated by the equal enumeration and execution-inputs child receipts.
- Failed attempts preserved and not counted: the first query-probe launch (a child could not write before receipts/probes existed; the parent then failed with KeyError; no receipt), source-pins43 attempt 1 (KeyError on a ledger key assumption; receipt kept), and query-adapter43-x attempt 1 (four rows used a missingRefs entry, a bare fact id, that fails identity availability admission, so those rows stopped at the record stage; its run receipt and stdout are kept, and its probe JSON was superseded by attempt 2, which is the result).
- Ported source42 probes keep their original labels ("source40"/"source42") as historical text; only runtime paths changed, and the current side is the verified source43 copy.
- The package verifier and native probe are author tools re-executed on this review's copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative is unexercised; the partial and/or/not helper is unexercised; count/all are unimplemented; two-binding qualification is incomplete.
- Cursor assessment covers same-host continuation only; the cursor is an opaque host token, and no cross-host portability or canonical preimage is assessed or required.
- Byte-identical owners outside the query change (composition section 7, policy-derivation3, attribution/capture, programEntry, identity digest scope) rely on this origin's named source42 assessments and were not re-read this charter.
- No grade, activation, application, readiness, implementation authorization or product qualification is granted.

## Build gaps

none
