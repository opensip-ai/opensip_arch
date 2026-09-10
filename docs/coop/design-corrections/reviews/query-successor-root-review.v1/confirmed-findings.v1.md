# Root query review — first written model, author still working

The root read the whole 1099-line query model and first complete contract/schema.
`retained-probes.v1.py/json` reproduce below using the existing semantic reference
fixture builder followed by actual M3 `open_run_closure`, evaluator derive,
seal, and `close_run`. The fixture and model are NOT an independent blind
reconstruction. M3 admits the retained Run. The query model SHA256 is
2a9d2c0dc4bd2e2b82dff35f3493c2ef6095151248c70c5fc9eeb83254cb7ce3; its exact bytes are preserved in `first-read-query-model.py`.

Required corrections before freeze:

QROOT-1 — Derived cache is treated as authoritative projection data. On the SAME
owner-admitted Run/request, clean canonical projection returns one outgoing
reference. After cache edges are replaced by [], execute_graph_query returns
zero with traversalCoverage=complete/countBasis=exact. close_run authenticates
the base evidence, not the cached projection's completeness. Remove the optional
cache from this reference strong path, or reconstruct and compare the complete
projected payload before use. A projection hash stored beside caller-modifiable
cache content does not independently authenticate completeness. Preserve GX exact
fallback law. Need poisoned omission/addition/provenance and cache-deletion cases
on actual admitted Runs, not synthetic graph labels alone.

QROOT-2 — Unknown endpoint is a fabricated graph member. On that actual Run,
start==target={universe:e*64,kind:symbol,nativeSubjectId:missing} produces one
zero-hop path. The universe is not retained and the symbol is absent. Define
vertex membership via admitted subject inventories and/or actual projected
fact endpoints; no persisted evaluation-subject object need exist. Unknown
identity must receive typed refusal; known isolated vertices remain usable.
Exercise false universe, absent subject and known empty-incidence symbol.

QROOT-3 — Advertised strong entry point has a no-closure escape. Supplying only
host.standing=synthetic-admitted-fact-graph and an empty invented graph returns
a retained complete response without a Run/objects/blobs. Internal graph-only
algorithm tests are fine, but must use a separate internal helper. The public
execute_graph_query must always require complete retained owner admission;
unknown extra host observation flags must not bypass that boundary.

QROOT-4 — host.targetAttributions and host.evaluationDeficiencies currently
replace retained attribution/deficiency data. Derive them from the actual
admitted proof inputRefs/retained blobs and proof/native records. Imports target
kind must join actual TargetAttributionV1, not a host-authored kind. Deficiency
citations must retain exact reference/selectors and supported typed source/cause,
not coerce unknown source values to execution and silently drop inputRefs.
coverage_limitations reads nonexistent unresolvedCount (actual unresolvedEdgeCount),
handles incomplete but drops partial/not-attempted states. Preserve actual
Coverage entry fields/state and citations so caller resolution limits are explicit.
The executed incomplete-incoming example returns zero/complete traversal and
coverage-unknown citations, but loses the actual partial resolution state.
Further actual Run controls are required; this item combines static inspection
with the retained coveragePayloads/result evidence in the root probe.

QROOT-5 — Public work accounting is not a completed node-budget law. Projection
counts scanned fact IDs as visited nodes, traversal resets a separate full cap,
then reports max(scan,walk). Walk increments before refusal and can report cap+1.
These are not a single globally bounded endpoint visit count. Specify the canonical
logical query work/count model and enforce it consistently independent of index
access. Do not use cache presence to change count/completeness. Exactly-at-cap
and first owed extra work need actual controls. This is static inspection pending
completed author checker; do not claim an executed budget counterexample yet.

Additional normative joins to settle: endpoint malformed vs ambiguity fault
precedence; explicit unsupported request refusal vs individual unprojectable
fact omission; exact endpoint tuple order and default handling; deterministic
unprojectable/incoming limitations from all relevant retained records; explicit
vertex universe for zero-hop/includeStart; exact schema-admitted full failure
carrier (StepTermination is not by itself CommandEnvelope).

The separate schema probes v2 pass 27 shape-level controls against the recorded
query schema, including 17 unchanged non-graph parameter bags and rejecting
unresolved latest/advisory true/missing disclosures on graph responses. v1 had
an incorrect ROOT fixture ProjectId prefix; its failures are preserved. v2 uses
the exact published prj1- grammar; all negative first boundaries were inspected
and are now the intended fields. Neither schema result validates traversal.

Root integration outside W ownership: product workflow §8; current-source map;
Hydra proposal dispositions; current invocation Operation/Page schema refs→query3;
current workflow profile checker selected query3; three historical closed-detail
guards explicitly retain 289 substrate + 13 evaluator additions + six query
additions. W should not edit those root-owned files.


Follow-up root retained-probes.v2 now executes QROOT-5's cap counterexample:
with testBounds.maxVisitedNodes=1, an actual retained one-edge path reports
visitedNodes=2. The normal outgoing neighbor positive still returns one edge.
The same cache omission, unknown-zero-hop and no-closure strong-wrapper
counterexamples reproduce. Exact second model bytes are in
second-read-query-model.py; report names their SHA256.

QROOT-6 — Snapshot resolver result is not joined to the admitted Run snapshot.
An explicit request for a different fake snapshot2, with a stale/mismatched
host.runsForSnapshot row pointing to the actual Run, returns that other Run's
complete query result. The strong owner must compare request snapshot selection
to admitted run.snapshotId before traversing. A derived resolver/index is not
permission to answer the wrong historical selection. Exact probe is
wrong-snapshot-index-result in retained-probes.v2.json. Latest selection may
remain a separately documented trusted host index observation; do not invent
ordering from static Run bytes.
