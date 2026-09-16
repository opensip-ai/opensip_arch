**Verdict: changes required.** This isn't yet an adequate complete report owner. It's a sound partial shape contract, but it doesn't close AUDIT-G10 as it claims. Both files are written to `m1-report-projection-review-01/`, and every required finding cites exact owner lines.

**Checks:** the manifest hash, all 6 files and all 15 parent pins were byte-exact before and after the review. The subject's `check.py` passes on a copy (79 cases, exit 0). All external schema references resolve through the hash-pinned loader: 18 documents, none unresolved.

**Required findings:**
1. **fit HTML (RP-OBL-1, blocking).** fit requires `candidates` and `evidence-levels`, but the command envelope has nowhere to carry them, for any output format. Even so, the subject's own positive fit case is admitted, and the schema's fixed fit views leave no room for a later fix. This needs to be a scoped correction and a registered gap, not something treated as covered.
2. **Envelope joins aren't checked (blocking).** A positive fixture uses a `latest` view with `advisory:false` for candidates, which the workflow rules forbid. Miscounted evidence levels and an inspect result pointing at a different Run are also admitted.
3. **The symbol join does exist (blocking).** subject3 is computed from exactly the same fields a graph endpoint carries, and the evaluator models build it that way. So "no subject3↔endpoint join exists" is false. The missing piece is a bounded, host-computed `{endpoint, subjectId}` index that admission recomputes.
4. **Features vanish under "no owner" (blocking).** Metrics and test reachability, descriptions, recipe parameters, the step ledger and declared configuration are simply "not shown". The inventory requires a visible unknown or unavailable state, and none of them is registered as an obligation.
5. **Panels overstate their sources.** A substituted empty capability registry, a history with an unrelated baseline and a history row holding the current Run's findings are all admitted.
6. **The larger codec overrides owner limits.** A policy rule its owner refuses for depth (nesting 28) is accepted inside the report. The report codec also never checks raw bytes, even though the chapter-14 override says it runs before shape validation.
7. **Budgets use typical sizes, not worst cases.** These are owner-valid maximums, validated against the schemas:
   - A finding can be 49,889 bytes, so only 1,681 fit under the 80 MiB envelope cap.
   - A 1000-row graph page can be 66 MB.
   - A single 64-hop path can be 6.4 MB, which alone exceeds the 4 MiB exploration cap.
   - When bytes overflow, whole panels have to be dropped, because lists can't be shortened for bytes.
8. **The standing overstates completion.** Measured product qualification (RP-OBL-2) is correctly kept separate, and I didn't assess it.

Five advisories are also in the files, including:
- Browser failure states are underspecified.
- The multi-run history deferral isn't registered.
- The report inventory is itself still an unreviewed author proposal. I treated its R01–R24 rows as the selected scope, since chapter 14 and M4 bind to them.

**Limits:**
- No browser or product code was run.
- The subject3 recipe is confirmed from the schema, the contract text and the evaluator models, not from a pinned test vector.
- I didn't build worst-case sizes for coverage results or comparisons.
