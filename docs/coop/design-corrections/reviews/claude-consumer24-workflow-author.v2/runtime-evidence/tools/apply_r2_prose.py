"""R2 + query-step mapping normative prose (tables are the published law; reference Python is not)."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply  # noqa: E402

WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
QPC = 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md'
rows = []

CARRIER = '''**Public query carriers.** Every `kind=query` envelope names `querySurface`, one closed value per
query-class command, equal to that command's inventory `queryDispatch.surface`.
`graph-query-response` carries `queryResponse`, the complete owner-admitted `GraphQueryResponseV1`;
every other surface carries `queryRecord` of exactly its closed record type, whose members reuse
the owning schemas, and never `queryResponse`. Non-query envelope kinds carry none of these
members. No untyped payload member exists. The JSON rendering is that envelope, the agent
rendering is the same envelope plus `agentHints`, and the human rendering prints every parity
field; parity is read from the envelope at the inventory `queryDispatch.parityPaths` JSON pointers
and recovered identically from each rendering. The closed record or response, its cross-record
joins and the compact `QueryResult` join are admitted before any rendering. A query never commits
a Run, so a rendering that cannot deliver its carrier is `DELIVERY.REQUIRED_FAILED` with
`DELIVERY.REQUIRED_PROJECTION_FAILED` and no `runId`.

| Command | Step / operation / request | `querySurface` / carrier record | Joins beyond schema | Compact `QueryResult` |
|---|---|---|---|---|
| `query` | `query`; caller-selected member of the 20 public graph-query:3 operations; `GraphQueryRequestV1` | `graph-query-response` / `queryResponse` = `GraphQueryResponseV1` | project, termination and graph summary joins above | graph law above; the other 17 keep their owners |
| `candidates` | `query`; public `candidate.list`; `GraphQueryRequestV1` (`view`, `params.includeSuppressed`) | `candidate-list` / `CandidateListRecordV1`: `context` (`GraphQueryResponseContext`), `includeSuppressed`, `candidates` (review:2 `Candidate[]`), `evidenceLevels`, `suppressedCount` | context project equals envelope project; `advisory` true; concrete Run; every candidate names that Run; `evidenceLevels` counts listed candidates per `EvidenceLevel`; without `includeSuppressed` no listed candidate is suppressed, with it `suppressedCount` equals listed suppressed; an untruncated `totalItems` equals the listed count | `items` listed, `truncated` context, `completenessMet` coverage `complete`, `advisory` true |
| `inspect` | `query`; public `inspection.show`; `GraphQueryRequestV1` (`params.candidateId`) | `candidate-inspection` / `CandidateInspectionRecordV1`: `context`, `inspection` (review:2 `InspectionBundle`) | project; `advisory` true; concrete Run equals the bundle Run; facts unique and byte-ordered; `totalItems` equals the fact count | `items` facts, `truncated` context, `completenessMet` coverage `complete`, `advisory` true |
| `review-brief` | `query`; host `review.produce-brief`; `ReviewBriefProduceRequestV1` (`view`, `producer`) | `review-brief` / `ReviewBriefRecordV1`: `context`, `brief` (review:2 `ReviewBrief`) | project; `advisory` true; concrete Run equals the brief Run; `brief.truncated` equals context `truncated` equals (`totalItems` greater than listed) | `items` listed, `truncated` brief, `completenessMet` not truncated, `advisory` true |
| `recommend` | `query`; host `discovery.recommend`; `DiscoveryRecommendRequestV1` | `discovery-recommendation` / `DiscoveryRecommendationRecordV1`: `advisory`, `discovery` (native `UnitDiscoveryV2`), `recommendations` (`DomainDetail[]`), `config2Proposals` | every proposed root normalizes under the native explicit-root law to a discovered unit root, and `unitOrdinals` are exactly those units | `items` recommendations, `truncated` false, `completenessMet` true, `advisory` true |
| `baseline-show` | `query`; host `baseline.inspect`; `BaselineInspectRequestV1` (`path`) | `baseline-inspection` / `BaselineInspectionRecordV1`: `baseline` (baseline:2 artifact), `pivotClosureAvailability` | baseline admission (§2, including detector identity); one availability row per descriptor pivot closure, in order | `items` rows, `truncated` false, `completenessMet` every row `available`, `advisory` false |
| `policy-show` | `query`; host `policy.show`; `PolicyShowRequestV1` | `effective-policy` / `EffectivePolicyRecordV1`: `policyDigest`, `policy` (`PolicyDocumentV2`), `waiverSetDigest`, `effectiveWaivers` (`WaiverSetV1`), `waiverResolution` (`WaiverResolutionV1`) | both digests are the document digests; `effectiveCount` equals the effective waivers; no expired or rejected waiver is effective | `items` rules, `truncated` false, `completenessMet` true, `advisory` false |
| `policy-test` | `query`; host `policy.test`; `PolicyTestRequestV1` (`suitePath`) | `policy-test-result` / `PolicyTestResultRecordV1`: `result` (`PolicyTestResultV1`) | `policyTestResultId` recomputes; `summary` counts case outcomes | `items` cases, `truncated` false, `completenessMet` resolver accepted with no indeterminate or not-executable case, `advisory` false |
| `repair-preview` | its own `repair-preview` step; `RepairPreviewParams` | `repair-preview` / `RepairPreviewRecordV1`: `preview` (invocation:3 `RepairPreviewResult`), `plan` (repair:2 `RepairPlanV1`) | `repairPlanId` recomputes from the descriptor; preview plan id, snapshot, `applicable` and `unmetPreconditions` equal the descriptor; descriptor project equals envelope project | `items` edits, `truncated` false, `completenessMet` `applicable`, `advisory` false |

Parity pointers (`queryDispatch.parityPaths`); `termination-class` is `/termination/class` for all nine:
`query` resolved-view `/queryResponse/context/resolvedView`, availability
`/queryResponse/context/availability`, truncated `/queryResponse/context/truncated`, total-items
`/queryResponse/context/totalItems`, query-response `/queryResponse`; `recommend` recommendations
`/queryRecord/recommendations`, discovery-units `/queryRecord/discovery/units`, config2-proposals
`/queryRecord/config2Proposals`; `baseline-show` baseline-id `/queryRecord/baseline/baselineId`,
pivot-closure-availability `/queryRecord/pivotClosureAvailability`; `policy-show` policy-digest
`/queryRecord/policyDigest`, waiver-resolution `/queryRecord/waiverResolution`; `policy-test`
policy-test-result-id `/queryRecord/result/policyTestResultId`, summary `/queryRecord/result/summary`,
resolver-accepted `/queryRecord/result/resolverAccepted`, overrides-applied
`/queryRecord/result/overridesApplied`; `candidates` candidates `/queryRecord/candidates`,
evidence-levels `/queryRecord/evidenceLevels`, suppressed-count `/queryRecord/suppressedCount`;
`inspect` candidate-id `/queryRecord/inspection/candidateId`, facts `/queryRecord/inspection/facts`,
limitations `/queryRecord/inspection/limitations`; `review-brief` candidates
`/queryRecord/brief/candidates`, producer `/queryRecord/brief/producer`, truncated
`/queryRecord/brief/truncated`; `repair-preview` repair-plan-id `/queryRecord/preview/repairPlanId`,
snapshot-id `/queryRecord/preview/snapshotId`, applicable `/queryRecord/preview/applicable`,
unmet-preconditions `/queryRecord/preview/unmetPreconditions`.

**Query-step operations.** A `query` step's params are closed: `PublicQueryParams` for the twenty
public graph-query:3 operations, carrying the complete `GraphQueryRequestV1` whose operation,
completeness and page equal the step's; or `HostQueryParams` for the closed host-only extension
`baseline.inspect`, `discovery.recommend`, `policy.show`, `policy.test` and
`review.produce-brief`, each with its own closed request record. Host-only operations are not
public query operations and never widen graph-query:3 `Operation` or `Params`; the public
`baseline.show`, `policy.effective` and `review.brief` operations remain the API over retained
records. Dispatch owners: `candidate.list` and `inspection.show` read the review projection of the
admitted Run (§5 candidate and inspection laws); `review.produce-brief` runs the review brief
producer (`--producer model` is a model principal with its admitted `modelClosureId`,
`--producer heuristic` is `{kind: policy-rule, id: opensip.review.heuristic}`); `discovery.recommend`
joins the security discovery boundary inventory with native unit discovery; `baseline.inspect`
admits the artifact (§2) and resolves pivot closures under current trust; `policy.show` resolves the
tracked policy and waivers at the admitted trust-clock date (§5); `policy.test` runs the authoring
test (§5). `repair-preview` keeps its own step and `RepairPreviewParams`. Every query step still
yields the compact `QueryResult`.

**Query-class failures.** A refusal is a `kind=failure` envelope with its owner's detail and no
carrier: `query` per the query projection contract §7; `candidates`, `inspect` and `review-brief`
view resolution per that table, and an unknown candidate `IDENTITY.UNKNOWN` /
`REVIEW.CANDIDATE_UNKNOWN`; `recommend` the native discovery refusal and its registered detail (a
refused `UnitDiscoveryV2` is never carried); `baseline-show` the baseline admission refusals (§2);
`policy-show` the policy and waiver resolution refusals (`POLICY.UNKNOWN_RULE`,
`POLICY.DUPLICATE_WAIVER`); `policy-test` an inadmissible suite `CONFIG.INVALID` / `CONFIG.INVALID`
(resolver refusals are result data); `repair-preview` its `REPAIR.*` refusals (unmet preconditions
are plan data). A missing, revoked or incompatible pivot closure is availability data
(`BASELINE.PIVOT_DETECTOR_UNAVAILABLE`, `BASELINE.PIVOT_CLOSURE_REVOKED`,
`BASELINE.PIVOT_CLOSURE_INCOMPATIBLE`), not a baseline-show failure. The only config2 proposal is
explicit `discovery.workspaceRoots`; config2 publishes no other proposal grammar.'''

OLD_CARRIER = '''**Public query carrier.** Every `kind=query` envelope names `querySurface`. The query command,
whose inventory parity fields include `query-response`, selects `graph-query-response` and
carries that complete owner-admitted response in `CommandEnvelope.queryResponse`: the JSON
rendering is that envelope, the agent rendering is the same envelope plus `agentHints`, and
the human rendering prints every parity field; parity recovered from each rendering is
identical. `queryResponse` is required for that selector and forbidden for every other
selector and envelope kind, so a query-command envelope cannot omit it silently and no private
wrapper carries it. Every other query-class command (`recommend`, `baseline show`,
`policy show`, `policy test`, `candidates`, `inspect`, `review brief`, `repair preview`)
selects `command-owned-summary`; its compact `QueryResult` and parity fields keep their owners.
A query never commits a Run, so a query rendering that cannot deliver the carrier is
`DELIVERY.REQUIRED_FAILED` with `DELIVERY.REQUIRED_PROJECTION_FAILED` and no `runId`.'''

rows.append(apply('R2 prose workflows', WS, [
    (OLD_CARRIER, CARRIER),
    ('''returns a bounded `InspectionBundle` (≤ 4096 facts, Coverage, imports, limitations).''',
     '''returns a bounded `InspectionBundle` (≤ 4096 facts, Coverage, imports, limitations). Its `facts`,
`coverageIds` and `importIds` are the fact2, coverage2 and import2 evidence references of the
candidate's findings, unique and ordered by UTF-8 bytes; `limitations` name each unmatched
correspondence reason, an incomplete enumeration of the candidate's rule, and any bound
truncation (facts 4096; references and limitations 64). A candidate id that is not a candidate of
the admitted Run refuses `IDENTITY.UNKNOWN` / `REVIEW.CANDIDATE_UNKNOWN`. `candidates` lists
suppressed candidates only with `--include-suppressed`; `suppressedCount` always counts the Run's
suppressed candidates and `evidenceLevels` counts listed candidates per level. The non-graph
context of these Run-backed surfaces reports `coverage=complete` exactly when the admitted proof
was evaluated with no execution deficiency and every enabled rule's enumeration is complete,
otherwise `partial`, with `availability=retained`.'''),
    ('''tracked-intent write; nothing writes a waiver implicitly.''', '''tracked-intent write; nothing writes a waiver implicitly. `opensip policy show` resolves the tracked
policy and waiver documents at the admitted trust-clock date and reports the policy, its digest,
the effective waiver set, its digest and the resolution disclosure.'''),
    ('''current detector explicitly and is a mutation with its own receipt.''', '''current detector explicitly and is a mutation with its own receipt.

**Baseline show.** `opensip baseline show [PATH]` admits the tracked artifact as above and reports,
for each descriptor pivot closure in order, its current-trust state: `missing` (no admitted record
or bytes), `revoked` (trust not admitted), `incompatible` (unsupported protocol major, or a platform
that is neither the host's nor `any`), or `available` with its trust origin (retained generation,
installed signed release or signed closure bundle). These states are data, not a failure.'''),
]))

rows.append(apply('R2 prose query contract §7', QPC, [
    ('''The public success carrier is CommandEnvelope major 3 `kind=query` with `querySurface=graph-query-response` and the complete response in `queryResponse` (workflows-and-surfaces §8).''',
     '''The public success carrier is CommandEnvelope major 3 `kind=query` with `querySurface=graph-query-response` and the complete response in `queryResponse` (workflows-and-surfaces §8). The other query-class CLI commands have their own closed surfaces there; the host-only query-step operations those commands dispatch are not members of this contract's public operation set.'''),
]))
print(json.dumps(rows, indent=1))
