# Explicit report history selection proposal

Root owner proposal for RP-DO-12 and report disposition R14. Not accepted or
integrated. This adds an explicit selection mode to the existing bounded report
history feature. It does not replace the command's current evidence selection,
baseline, comparison, verdict or authority.

For every command that supports HTML, `--history-run RUN_ID` may be repeated one
to four times with `--format html`. Each occurrence takes exactly one full RunId;
comma splitting, prefix matching and `latest` are not supported. The parser
preserves argument order and refuses duplicate IDs or more than four IDs. With
no occurrence, the existing baseline-source-then-prior-commit-sequence policy
continues unchanged. With any occurrence, the explicit list replaces automatic
history selection completely. No baseline or recent Run is silently appended,
substituted or used to fill an unavailable slot.

The four-slot limit is the existing report maxHistoryRuns value. It is not the
prototype's recent-window limit, and it imposes no age or commit-distance cutoff.
An explicit Run can be older or newer than the report's current evidence Run,
provided it is visible in the exact admitted project namespace at the host's
retained read snapshot. It must not be described as necessarily a prior Run.
Current evidence selection and the optional comparison baseline remain visible
in their own panels even when the explicit history list does not include them.

The request is a presentation input and does not change PlanId, RunId, assessment,
grants or required capability selection. The host validates its lexical shape,
count, uniqueness and HTML applicability before planning useful work. A requested
ID can equal the Run later produced by this invocation: deterministic analysis
can reproduce an existing RunId. In that case its slot explicitly says
`current-run`, points to the already displayed current result, and consumes one
of the four requested slots. It does not cause a post-commit request refusal,
duplicate the current findings or silently discard the request.

Every other requested ID is looked up exactly once against the admitted project
namespace and the same retained read snapshot. The host supplies an admitted
authoritative Run handle, or the existing explicit unavailable state (expired,
purged, corrupt or unavailable). A Run inaccessible in this namespace is
unavailable; the report must not reveal that it exists elsewhere. Historical
bytes are not rebuilt from the current checkout or a replacement analysis. A
requested baseline source uses the same exact ID and retained evidence rules;
its presence in this panel grants no baseline comparison authority.

The carrier keeps requestedRunIds in argument order. Each slot names that exact
ID and is either `current-run` or a historical Run projection with its existing
availability and bounded findings. Missing bytes never change the requested
list or consult run.list for a fallback. Byte budgeting can omit findings or the
optional history panel under the existing explicit omission law, but the
document's history request disclosure remains visible so that omission cannot
be mistaken for a successful empty selection. A minimal selection disclosure is
fixed overhead that must be included in the report budget derivation.

The reference selection model produces a closed request/disclosure record and
exact lookup slots. Its injected lookup callback represents already-admitted
host custody, not permission for arbitrary file or cross-project access. The
reference does not implement store recovery or verify a Run's authority.
The actual report integration must bind each returned handle/result to its
requested RunId and project and retain that source association.

Proposed public refusal: request-rejected / REQUEST.UNSATISFIABLE / exit 2,
with new detail `REPORT.HISTORY_SELECTION_INVALID` and remedy
`Use one to four distinct full Run IDs with --format html.` The selected common
DomainDetailCode enum, public route table, command grammar/flags and all renderer
goldens must add this route together. No raw rejected token is included in the
public detail. The reference's local refusal is not a selected D9 route yet.
This explicit proposal avoids silently borrowing a detail with a different
meaning. Unsupported commands retain their existing unknown-option handling.

Required integration: append the same flag record to the eight HTML command
rows; select one new history mode and retain automatic mode; extend the history
slot union with current-run; make provenance mode-specific; remove the R14
feature placeholder only after carrying this data; update request binding,
byte bounds, source selection, CLI grammar, help and browser controls; test the
actual final HTML and exact history hydration. An in-browser selector changes
the view of embedded slots only. It cannot execute a new query or claim that
unembedded history was searched.
