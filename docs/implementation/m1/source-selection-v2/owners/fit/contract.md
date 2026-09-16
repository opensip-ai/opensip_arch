# Fit query binding and interrupted advisory output

Root correction01 at narrow schema-fragment/model scope. Not accepted, integrated or product-qualified.
Addresses Q-FIT-1, including the reproduced static parity crash recorded under
`docs/implementation/m1/audits/fit-interruption-parity-01`.

## Plan the query against its producing analysis step

The current query step params require a complete public query request. The
report08 interrupted-fit fixture plans a request for a fixed `run3:bbbb...`
and `prj1-aaaa...`, then commits and reports a different Run/project. Its query
result is a scripted scalar summary, not a response bound to that request.
The fixture cannot establish that fit actually queried the Run it just sealed.
The missing dynamic binding must be corrected along with advisory output.

Add a closed host-only QueryParams alternative `FitQueryFromAnalysisParams`:
`{kind:"query", operation:"candidate.list", sourceStep:StepId}`. It is an
invocation parameter form, not a new public graph query operation. Existing
PublicQueryParams and HostQueryParams remain unchanged. At invocation admission,
sourceStep must select an earlier analysis step, be an explicit dependency of
this query step, and use the completed dependency gate. The builtin fit plans
exactly this source relationship and exactly one query step. No latest selector,
fixed placeholder Run, arbitrary binding expression or mutable request rewrite
is permitted.

After the dependency completes, an authoritative AnalysisResult supplies the
exact committed RunId; the admitted invocation supplies ProjectId. The host
constructs the existing GraphQueryRequestV1 with operation candidate.list,
params includeSuppressed=false, completeness best-effort, page size100 and no
cursor. The existing query owner admits and executes it. Public request shape,
native Run admission, source custody and query projection remain their existing
owners' duties. The immutable sourceStep plan is not replaced with the resolved
request; both are retained as different records of planning and execution.

For a completed ephemeral analysis there is no authoritative query request.
The host query adapter produces the already defined unavailable-ephemeral-
analysis advisory form and an advisory QueryResult summary with items0,
truncated=false, completenessMet=false. The report parity fields remain null,
not an empty authoritative candidate list. Failed/skipped/cancelled analysis
continues to block this query through the existing dependency gate.

## Keep the completed response until required output settles

Before marking the query step completed, the host admits its complete response,
derives the QueryResult summary and retains the exact FitAdvisoryReport with a
private handle bound to the invocation RequestId, query StepId and completed
attempt ExecutionId. The summary in StepResult must equal that derivation. The
response's request/project/Run and first-page parity retain all existing fit
joins. This handle is private host custody, not a caller-controlled receipt or
a new public source of authority. Root's reference uses dictionaries as a
stand-in and does not implement private custody.

Keep this handle through required output finalization, including cancellation
of a later renderer. A completed query's full admitted advisory report is
copied exactly into the interrupted run envelope. No re-query after the signal,
current-checkout fallback, cursor expansion, reconstruction from item counts or
fabricated candidates is allowed. If the required completed response is lost,
the host reports its existing required-projection operational failure while
preserving the committed Run and original query completion. It must not present
that state as if the query were cancelled or as an empty successful result.
Durable replay of a previous invocation needs an explicitly retained response;
the private live handle does not itself make historical query data durable.

## Interrupted query before completion

On an interrupted fit run envelope whose query was cancelled, skipped, failed or rejected,
include a new FitAdvisoryReport form `unavailable-query-result`. Its parity
names the envelope's committed RunId; candidates, evidenceLevels, truncated,
totalItems and nextCursor are null; candidatesAvailability is the same explicit
state string. Add `queryOutcome` with exactly cancelled, skipped, failed or rejected, joined to
the recorded query outcome. This is an absence disclosure, not a query result.
No query response handle may accompany this state. A failed/rejected query retains that actual outcome and its existing error detail; this state does not relabel it as cancelled. The envelope's recorded
errors and invocation availability follow the existing interruption laws.

An interrupted fit without any committed Run keeps the existing failure
carrier and prohibition on advisoryReport. A completed ephemeral analysis that
was interrupted before query completion also cannot mint a Run. These cases
do not invent fit parity pointers on a failure carrier.

The unchanged static parity function can render every run carrier once its
required advisoryReport is present with total parity. Do not catch KeyError,
silently skip parity fields or use L02 capacity failure to excuse this defect.

## Required source succession and validation

Publish exact successors for invocation QueryParams, envelope fit union,
inventory fit planning/parity descriptions, workflow planning/query binding and
report construction/admission. Compose with timing's invocation successor;
do not overwrite it or mutate accepted owners. The final envelope/source major
is chosen in the joint source closure, not silently reused here.

Update report08's builders and representative params to sourceStep binding and
replace the interrupted fit's invented query summary with a real admitted
candidate-page fixture bound to the same Run/project. Exercise the actual
static parity function for every interruption golden, not a count of format
labels. Require completed-query response identity/summary joins, missing/extra
handles, wrong invocation/step/attempt/source, cancellation before query, skips,
ephemeral behavior and real required-output failure propagation.

The three schema-fragment outputs reproduce byte-identically. Thirteen focused
groups pass, including calls to the unchanged static parity function for all36
builtin interruption fixtures using the corrected fit carrier. Eleven targeted
semantic mutation controls are caught. The first broad mutant run produced
consequent errors in unrelated tests for two mutants; that run is retained. The
final controls execute each named semantic witness directly and require its
assertion failure, not a tool or parser failure.

Full invocation/page/native schema admission is delegated in this reference.
The actual unchanged candidate summary function and its helpers are AST-extracted
from the pinned query owner; other query branches and loader behavior are not
qualified. Noncompleted-outcome tests are focused synthetic join inputs, not
fully re-admitted invocation records. Private handles are dictionary stand-ins.
This is not a completed Q-FIT-1 correction until the complete owner schemas and
joint report integration exist. Actual Claude must independently review the
new planning/custody laws as well as the original parity fix.
