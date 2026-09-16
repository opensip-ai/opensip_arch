## Verdict: CHANGES_REQUIRED

Nothing on my side of the reconstruction is failing. The verdict is held by three SHOULD-level design issues in the kit that I can't resolve by choosing a reading. There are no MUST issues, no claimed-positive audit failures and no open helper failures.

## Final verification
- **Command:** a fresh-process `verify_all.py` ran after the last edit: 54 stages, all exited 0.
- **Reconciliation:** afterwards all 145 artifact digests in the report matched the bytes on disk, and the per-command receipt matches `verify-all.json`.
- **Counts:**
  - Requirement status: 131 executed, 3 future qualification.
  - Claimed-positive audit: 126 PASS, plus the 5 phase-11 rows, which the status stage marks executed after the report is written.
  - The md and json reports state the same verdict, and the measured read graph passes.
- **Earlier attempt:** one earlier full command (attempt A) also passed but wasn't final: a stage label still said "generation 22" and two report details were then corrected. It is retained in `notes/v23-command-attempts.json`.

## Atom-contract reconciliation (three kit files changed)
- **Runtime polarity (V23-D1):** an unfiltered runtime `exists` now matches both observed-hit and observable-unhit rows, which withdraws my gen-22 reading. TypeScript findings went from 3 to 5.
- **Absent dependency (V23-D2):** it now answers `required-relation-missing`, with the same-kind totality check. Rust findings went from 8 to 7.
- **Scope pairing (V23-D3):** scopes with a missing or null enumerator closure are now refused, and there is no mapped-scope fallback.
- **Result:** all five Runs were rebuilt, closed, replayed and controlled. The independent atom-law instrument admits all five and refuses the gen-22 and gen-20 predecessors.

## Claimed positives that were wrong and are now corrected
These passed schema admission but their semantic fields weren't derived from their premises. Each failing gen-22 artifact is kept under `predecessors.v22`.
- **Comparisons (V23-D6):** four scenarios said `pass` although the current Run carries required-execution deficiencies. They are now derived from premises and independently re-derived (6/6).
- **Graph query (V23-D7, D8):**
  - External targets were dropped, row order and cursor were wrong, and a full page was marked truncated.
  - The visited-node count, the path walk and the deficiency citations were also wrong.
  - `finding.list` listed a waived finding while claiming to exclude suppressed ones.
  - The executor's 46 outcomes are now recomputed by separate code with 0 disagreements, and 10 of 10 re-injected gen-22 defects are detected.
- **Purge/replay/output failures (V23-D9):** missing replay bytes were exit 3 instead of HOST.IO_FAILURE exit 4. A format-not-applicable error used the wrong error code.
- **Single- and multi-step envelopes (V23-D10):** these reported success, exit 0, "coverage satisfied" for Runs sealed indeterminate. They are now derived from each proof: exit 3, `required-relation-missing`, with the cited coverage id.
- **Public termination examples (V23-D11):** they asserted pass/fail verdicts for the real TypeScript Run and paired unrelated codes. Each is now rebuilt from the kit golden it cites.

## Open design issues
- **V23-S1:** a package graph endpoint without its manifest path. §2 of the query projection contract says `ENDPOINT_AMBIGUOUS`, but the schema requires the field and §8 admits against the schema first, which gives `PARAMS_MALFORMED`.
- **V23-S2:** native-evidence §10 gives `VERDICT.INDETERMINATE` for three deficiencies, while the D9 exit contract gives specific `COVERAGE.*` reason codes for the same Runs.
- **V23-S3:** the graph-query availability state `unavailable` must refuse with an `evidence.*` detail, but no such detail code is registered.
- **Advisory V23-A1:** no single envelope kind is stated for an invocation interrupted before any Run commits.

Each issue records the reading I applied and the smallest fix.

## Limits
- **Measured layer:** 16 positives are graded "schema-admitted-record". Their records are re-admitted and their joins recomputed, which is accepted for their kind, but their other fields were surveyed, not independently re-derived. The report says this.
- **Synthetic inputs:** comparison sides and termination-example Run ids that no retained Run can supply are labelled synthetic. All host observations are synthetic trusted inputs.
- **Unexercised branches:** some query disclosure branches aren't reached by any retained Run.
- **No qualification:** nothing here qualifies a product or a host.

The report is in `output/blind-review.md` and `output/blind-review.json`.
