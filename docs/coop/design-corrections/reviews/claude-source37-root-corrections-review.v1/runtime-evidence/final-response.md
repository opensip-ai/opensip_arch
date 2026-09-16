Root's overlay fixes most of what I raised, but not all. S37-02, S37-03, R1 and R2 are substantively corrected, A37-05 and A37-07 are addressed with advisories, and A37-06 is not closed (a new SHOULD, RC37-01). Nothing here accepts the final design, application, readiness or any grade, and my original source37 review stays unchanged at CHANGES_REQUIRED.

**How it was checked.**
- **Overlay verified:** the overlay manifest (`db9b7b3f…`) matches dispatch. All 12 overlay files match their hashes, and each source37 base file equals its before-hash.
- **Disposable copy:** I built a verified copy of source37 (manifest `245ef613…`, 12,900 files) and applied the overlay.
- **What I ran:** probes plus only the three changed checkers and the two planning checkers, each individually. No suite was run and no pins were regenerated. None of those runs changed a file in the copy, and `subject/` is byte-unchanged.

**Dispositions**

| Item | Outcome | Basis |
|---|---|---|
| S37-02 | Closed by the text (rebind still needed) | R02 and R24 now allow host-approved data projections only and state that executable report hooks are not admitted. The only remaining "hook" wording is those two negations. |
| S37-03 | Closed for schema and controls | The new `else` branch makes schema admission match "advisory is true for exactly four operations" across all 20 operations. The base failed this for 13. No consumer's admission changes, and the query checker passed 162/162. |
| A37-05 | Addressed, with advisory RC37-A1 | See below. |
| A37-06 | **Not closed — RC37-01** | See below. |
| A37-07 | Wording closed | The build plan now names the v5 normative-input binding and keeps the historical receipts. |
| A37-08 | Unchanged, as intended | The registered native schema bytes are untouched. |
| R1 / R2 | Accepted as schema law | See below. |

**RC37-01 (A37-06).** The new query route sends a replay mismatch to `HOST.IO_FAILURE` / `evidence.corrupt`. The evaluator-fault contract (line 15) and its route registry already define a different public outcome for exactly this condition:
- a retained-data mismatch goes to `evidence.regeneration-mismatch`;
- a live host defect goes to host-invariant.

In practice the probe results show the problem:
- A structural refusal, all four reminted false-result mutants and a simulated host bug inside `close_run` all produce the identical class, code and detail. They differ only in the subject text, which is the exception-text selection both contracts forbid.
- The query still fails closed (exit 4, no items, no Run), which is why this is SHOULD rather than MUST.
- My original A37-06 remedy said `evidence.corrupt` was acceptable "if chosen deliberately". I had missed that fault-contract row, and I've corrected that in this review.

**RC37-A1 (A37-05).** Treating a null, wrong-type or unknown availability value as a reference-call precondition is honest for the reference harness. All 17 probe variants behave as specified: omitted is still allowed, and request-schema refusal comes first. It doesn't hide a needed new public code. The analogy with a malformed RequestId is only partial, though:
- A missing RequestId makes a failure envelope impossible to build.
- With a valid RequestId, a real host can still report its own bad observation publicly. The existing host-invariant route (`SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`) validates, and the contract should cite it.

**R1/R2.**
- **Exhaustive check:** I checked all 3,120 combinations of class, `faultCause`, `reasonCodes` and `errorCode`. The base schema admitted 990 and the overlay admits 34, adding none. None of the 956 removed combinations is lawful under D9, and none of the 34 admitted is unlawful.
- **Request-rejected:** it keeps all 19 error codes, so no legitimate route is excluded (RC37-A3 notes fault-family codes are still admitted there, by design).
- **Fault pairs:** operational-failed now requires exactly the 11 fault/error pairs of the host fault map, including host-invariant.
- **Successor versus union:** limiting `faultCause` to operational-failed follows the successor field closure (workflows-and-surfaces §0 and §9); the superseded D9 union never had that field.
- **Producers:** every evaluator fault route and native public route validates identically before and after.
- **Fixtures:** only the 12 new reject vectors change admission.
- **Controls:** `check_workflows` passed 1816/1816 and `check-workflow-projection` passed 493/493. The `check_workflows` report gives only counts, so its new fault-pair control is confirmed by reading the code plus zero failures.

**Identity consequence:** none. No registered payload document is changed by the overlay, and none references the changed definitions. Four closed Runs rebuilt on the overlay copy have the same RunIds as my earlier receipts, so no retained identity needs reminting.

**RC37-A2 (integration).** The planning checker fails on the overlay copy with "Planning source changed: query". I've kept that failure as recorded. It stops at the first stale binding; the full list shows that v5, the coverage sources, the planning sources, the five source-pins files and the workflows report all still hold pre-overlay hashes. That's a rebind needed at integration, not a defect in the correction text.

**Outside this overlay.** S37-01 and A37-01..04 are not closed here. All 30 grades stay PENDING, the 32 gates stay unperformed and the 54 recovery cases stay not executed.

All child commands have finished. Files are in `/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1`:
- review.md
- review.json
- probes/
- receipts/
