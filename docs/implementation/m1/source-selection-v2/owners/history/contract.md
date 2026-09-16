# Explicit report history correction02

Root correction after actual-Claude presentation review01, covering RP-DO-12.
Unreviewed and unselected. Historical subject01 and its incorrect route remain
under prior/candidate01. No product source or accepted architecture byte changes.

The candidate adds explicit history selection to the existing report. It does
not change current evidence selection, baseline comparison, grants, verdict,
PlanId or RunId. No-flag automatic history selection remains byte/behavior
unchanged. Root pins report08, including its unchanged subject_run selector;
report08 itself still needs joint independent acceptance.

## Request and exact command records

`--history-run RUN_ID` is repeatable one through four times, in argument order.
Every value is one full lowercase run3 identity. Empty selection, malformed
values, duplicates, commas, prefixes and latest are refused. There is no implicit
baseline insertion, recent-history fill or fallback. A Run may be older or newer
than the report's current evidence Run. The fixed four-slot bound is not an age
or commit-distance limit.

history-command-flags.json freezes the exact `{flag, owner, class, join}` record
for all eight HTML commands: default, analyze, fit, audit, candidates, inspect,
review-brief and repair-preview. The join fixes grammar, repeatability, format
coupling and help text. The final inventory/CLI source successor must append
these exact records; this candidate does not claim to implement the parser.

Admission precedes useful planning and retained-history lookup. Precedence is:
unknown option on commands without this flag; then HTML applicability; then
lexical shape/nonempty/uniqueness; then the bound on a well-formed list.

- Non-HTML: REQUEST.UNKNOWN_OPTION / OUTPUT.FORMAT_NOT_APPLICABLE / exit2.
- More than four otherwise valid distinct IDs: REQUEST.UNSATISFIABLE /
  EVALUATION.SELECTION_LIMIT / exit2.
- Empty, malformed or duplicate IDs: REQUEST.UNSATISFIABLE /
  REPORT.HISTORY_SELECTION_INVALID / exit2.

Only the third detail is new. common.history-candidate.schema.json and
public-detail-registry.history-candidate.json add that one member. The other
routes are inherited. No rejected token is copied into a public diagnostic.
history-route-goldens.json records route tuples; full command-envelope and D9
renderer goldens remain a joint integration duty, not a claim of these tuples.

A malformed host currentRunId is an internal source failure, never a user
request refusal. The current Run is derived by the unchanged report08
subject_run function, extracted into subject_run.py and AST-compared with its
pinned source. Authoritative run carriers and the candidates/inspect/brief
query subjects preserve their existing mappings. Ephemeral, failure, invocation
and repair-preview carriers have no current Run under that selector. Merely
mentioning a Run in an error, repair prerequisite or earlier invocation step
does not make it an already displayed current result.

## Read snapshot and same-invocation Runs

After all non-render steps have reached their terminal state and their data
commits have completed, and before the first historical lookup, acquire one
retained read lease in the admitted project namespace. Use it for the entire
list and release it even if lookup/projection fails. The reference's
resolve_in_snapshot explicitly performs one acquisition around every slot.
It models a supplied host lease, not a datastore transaction implementation.

The snapshot includes authoritative primary and pivot Runs committed earlier
by this invocation. A requested pivot therefore uses ordinary exact lookup in
this same snapshot; it is not absent merely because a snapshot was taken before
this invocation began. If a requested ID equals the already displayed current
Run, emit current-run without lookup and consume a slot. Other IDs receive
exactly one typed run.show lookup each, in order. Later unrelated commits or
purges do not retarget the lease. A promised byte that is nevertheless unavailable
still receives the exact owner's unavailable result; no replacement analysis,
current checkout, latest resolver or other namespace is consulted.

An admitted project namespace is required for any lookup. If the request never
obtained one, preserve its selection disclosure and use the existing
unavailable/no-admitted-result panel state without probing any namespace.
Having no current Run does not by itself forbid explicit history when an
admitted project namespace exists. Final report applicability must support
explicit history on all eight commands while preserving automatic-mode rules.

## Typed run.show owner and admission

The selected parent generic query schema left run.show items untyped. The root
owner audit demonstrated that an arbitrary object passed shape validation.
This correction does not claim an existing typed run.show adapter was invoked.
graph-query.history-candidate.schema.json adds RunShowItemV1 and its response
constraint. It retains all 20 operation names and all other 19 operations' laws.
Source selection and compatibility of this stricter response contract require
independent review before integration.

run.show resolves one concrete Run. Its retained response has exactly one item:
`{runId, projectId, sealedRun, result}`. sealedRun is the existing identity:v3
Run record; result is the existing authoritative AnalysisResult. Context names
that exact ProjectId/RunId, totalItems1, coverage complete, availability retained,
truncated false and advisory false, with no cursor. Here coverage describes
complete metadata projection, not native semantic sufficiency; the result keeps
its own requiredCoverage, deficiency and verdict.

Expired/purged/corrupt/unavailable responses have no items, totalItems0 and query
coverage unavailable. A partial retained-evidence closure is not an authoritative
Run item. No second page or inferred zero-findings assertion exists.

query_history.run_show invokes the selected existing identity-model.v3 close_run,
including complete replay, before returning a retained item. It checks project,
requested identity, receipt RunId/PlanId and receipt verdict against the admitted
seal. Declared missing-evidence outcomes map to unavailable; declared corruption
or replay disagreement maps to corrupt. Unexpected host exceptions propagate as
operational defects and are never relabelled as retained corruption. Expired and
purged observations come from the same namespace read lease. Inaccessible IDs
produce unavailable and reveal no other namespace. A wrongly joined source
returned by the host is an internal source failure.

The terminal receipt's operational fields remain an admitted-host custody
precondition; sealed semantic evidence does not recreate a durability receipt.
The reference accepts an identity-model object to exercise the actual pinned
owner in isolation. Product construction must supply its selected private owner
and validated receipt handles; it must not expose caller-selected callbacks or
source dictionaries as authority.

The producer's source admission and the consumer's joins are separate mandatory
steps. history.resolve_slots requires a typed query result paired with the
bounded HistoryRun projection. It checks requested Run/project against the
query item, exact AnalysisResult equality, unavailable-state equality, and
finding count/omission arithmetic. It never accepts the old untyped callback.
The latter remains only in historical subject01 evidence.

## Panel, provenance and limits

explicit-history-panel.schema.json owns the explicit mode: exact selection,
ordered slots, and mode-specific provenance. Slots are current-run or the
existing present/unavailable HistoryRunV1. The reference admits the schema and
checks row order, current-run equality, per-row Run identity and item arithmetic.
It does not claim the automatic mode's not-current-run, prior-commit ordering or
baseline-source relationships for explicit selection.

The document can verify its own identities, order and counts. The binding to the
admitted typed query, retained namespace lease, terminal receipt and findings
source remains host-asserted because those admission proofs are not embedded.
The producer checks them through the typed adapter; provenance does not pretend
the offline browser replays close_run. In-browser controls select embedded slots
only and cannot launch queries or claim to search unembedded history.

Unavailable slots may retain the existing optional DomainDetail, restricted to
the read result: evidence.expired, evidence.purged, evidence.corrupt, or
QUERY.VIEW_UNKNOWN respectively. A writer's evidence.pinned purge inventory is
not a history read detail. No arbitrary detail is substituted to fit a budget.

The exact codec derivation in budget-result.json gives:

- maximal mandatory selection record: 896 bytes;
- four minimal unavailable rows: 533 bytes;
- maximal unavailable row including optional detail: 12,484 bytes;
- four maximal unavailable rows including details: 49,941 bytes;
- whole explicit unavailable panel with selection/provenance: 51,243 bytes.

The maximum includes both 1,024-scalar BoundedText fields at six canonical bytes
per scalar, longest code/state spellings and all optional subject members.
Reserve selection plus its enclosing member syntax before optional exploration.
Present findings and the final panel must fit the actual remaining whole-document
budget. Never drop requested IDs or individual unavailable slots to fit. If the
panel cannot fit, retain the mandatory selection and disclose the existing
exploration-budget-exceeded omission. L02 global required-output delivery capacity
remains a separate unresolved owner obligation.

## Evidence and remaining integration

Root selection/schema tests, actual close_run query checks, mutation controls,
and exact byte derivations are separate receipts. The actual close_run tests
use an unchanged, pinned predecessor evaluator3 fixture/replay closure, without
the feature02 parameter transforms. The source loader compiles verified copied
owner bytes and does not consume adjacent owner bytecode. Python dependencies
remain the declared reference environment. This is not general confinement.

All evidence uses synthetic native inputs and operational receipts. No compiler,
signed release, live product store, CLI, report construction or browser behavior
is qualified. Final work must select and compose the query/common/registry/flag/
report successors; retain the exact namespace and receipt handles; integrate the
selected source/generator inventory; and test real commands, failure envelopes,
rendered HTML, omission disclosure and browser controls. Actual Claude review and
root acceptance are required. No feature placeholder is removed by this unit.

## Query compatibility selection

The proposed run.show response refinement reuses the parent query schema URI/major. That versioning choice is not yet accepted. An older untyped cached item cannot become a typed admitted RunShowItem merely by relabeling it. A host with retained authority may project a new typed response from that exact retained Run and its evidence; it must not reanalyze the current checkout or substitute the latest Run. Unavailable authority keeps its explicit unavailable state. Independent review must confirm the versioning and selection mechanism before product integration.
