# Interrupted fit loses advisory parity

Confirmed required correction against frozen report08. Run `python -I -B
probe.py` from this directory; output is retained in `result.json`.

The unmodified fixture `fit/primary/signal-before-required-render` has a
committed Run and a completed candidate query. Its interruption envelope omits
`advisoryReport`. Report08 `admit_envelope` explicitly permits that omission
under Q-FIT-1, while inventory5's fit parity pointers and the unchanged
`static_parity_text` require the member. Passing the exact fixture to that
function raises `KeyError('advisoryReport')`.

Report08 `interruption_controls` verifies carrier/ledger joins and counts the
four names in `golden.formats`; it does not call the static renderer there.
Consequently, 144 declared renderer rows are not 144 successful renderings.
The narrower schema/owner checks remain evidence for what they execute, but
they do not establish this path's delivery. Original fixtures/results remain
unchanged historical evidence. This audit does not prove a live HTML/browser
failure; it directly proves the reference parity function cannot render that
accepted-by-its-checker carrier.

The successor must define total interrupted-fit parity and align envelope shape,
command inventory, ledger/query-result source custody, envelope construction,
admission and all renderer paths. Distinguish a completed query whose admitted
response is retained from a cancelled/skipped query and from a completed query
whose response is unavailable. Do not fabricate a completed query, use empty
candidates to mean unavailable, rerun the query after cancellation, or erase a
committed Run. QueryResult currently stores a summary rather than the full
candidate page; it is not enough to reconstruct or authenticate that page.
Any required retained response must have an explicit host owner and join.

Add real parity execution for every interruption golden and positive/negative
cases for cancellation before/after query completion, including the actual
completed-query fixture here. Merely changing the golden's status or catching
KeyError in the renderer is insufficient. Actual review and final report
integration remain required. The L02 operational output-failure policy cannot
be used to waive this deterministic missing-member defect.
