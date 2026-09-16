All three items (R1, R2 with the query-step mapping, and the /tmp read replacement) are done in the v2 runtime, and every command has finished. Every focused check passes on the final tree except the security owner launcher: it stops at its source-pin gate and runs no cases. The same security checks pass 464/464 only when run with that gate bypassed.

**R1: absence needs correspondence knowledge**
- An unmatched occurrence now blocks proof that a fingerprint is absent. The exceptions: its rule differs, both paths are known and differ, or both subject identities are known and differ. Baseline unmatched rows always block on same rule and same path.
- This applies the same way to B and E0–E4. Known hits stay true, and policy/scope non-selection stays false. An unrelated unknown never erases a separately proven hit or CODE-NET-NEW. Unmatched occurrences never get a fingerprint, and baseline `absenceKnowledge` is kept as recorded.
- The published reason order uses only existing values:
  1. `pivot-reevaluation-unavailable`
  2. evidence reasons
  3. the detector disposition's reason
  4. `baseline-absence-unknown`
  5. `current-absence-unknown`
- The contradictory §12 example and its check are replaced with `baseline-absence-unknown`. The pivot-only fingerprint and the baseline gating obligation stay. I added a genuine complete empty-baseline example that is CODE-NET-NEW and later policy-hidden.
- The controls run through close_run/compare_admitted: collision in both gating modes, known hit, unrelated unknown, pivot collision, and the baseline barrier.

**R2: carriers and parity for all nine query commands**
- `querySurface` now has nine closed values, one per command. `query` keeps `queryResponse`; the other eight each carry one typed `queryRecord` built from the owners' schemas. `command-owned-summary` is removed.
- The inventory's `queryDispatch` gives the JSON path of every existing parity field; none were removed. Record admission and cross-record checks run before rendering.
- Query steps accept either a public request (the 20 operations, unchanged) or one of five host-only operations: `baseline.inspect`, `discovery.recommend`, `policy.show`, `policy.test`, `review.produce-brief`. `repair-preview` keeps its own step.
- Each of the eight non-graph commands has positive envelopes from real owner records. Each also has controls for parity recovery from human/json/agent output, missing carrier, cross-command record, wrong surface, untyped member, mutated parity, and a join mutant refused before rendering. That is 156 checks in the workflow checker; the graph `query` command is covered in the query checker.
- I closed two gaps myself: `recommendations` now carry zero rows, because no recommendation detail is registered, and I corrected the policy-test refusal wording.
- **/tmp reads:** both historical reads in check-workflow-projection now read current source. The only `/tmp` strings left are docstrings and an output-path guard.

**Checks on the final tree**

| Checker | Result |
|---|---|
| workflow-projection | 766/766 |
| query-projection | 204/204 |
| current-profile | 38 |
| comparison-knowledge | 1 |
| workflows-v1 | 1816 passed |
| integration | 412 passed |
| composition | 30 |
| semantic-replay | 30 |
| evaluator-faults | 41 |
| replay | 73 |
| security owner launcher | exit 1: pins no longer match (22 changed pinned files), 0 cases run |
| security checks, pin gate bypassed | 464/464 cases, 11/11 sweeps |

One earlier run failed and is kept (`r2-2-wp`): my policy-test fixture passed the suite without resolving its `$` references. I fixed it by reusing the owner checker's substitution.

**Custody and diffs**
- The parent tree and v1 are unchanged, and the v1 final receipt still hashes to 27e3c03a….
- v2 has 12904 files, no new files and no unexpected changes; every change is covered by an edit receipt.
- Full diff against source38: 22 files (`diffs/source38-to-v2.diff`, f5fdab1d…). Incremental v1→v2 diff: 15 files (`diffs/v1-to-v2.diff`, be055eb7…). The per-file hashes are in `receipts/final-custody-and-diff.json`.

**Breaking draft effects**
- **Envelope schema:** old selector removed and typed `queryRecord` now required, with no compatibility coercion.
- **Invocation schema:** public query steps now require the full request.
- **Inventory schema:** `queryDispatch` is required for query commands.
- **comparisonResultId:** it changes wherever the new barrier applies.
- **Unchanged:** baselineId and graph-query:3.
- **Additive:** `REVIEW.CANDIDATE_UNKNOWN`.
- **Nothing new:** no new files, child commands or normative/reference files.

**Integration needs for you**
- **native823v2:** the recommend record points at native UnitDiscoveryV2, so native changes flow through it.
- **ce3v2:** termination and carrier are read-only for it; the delivery-failure rule is unchanged.
- **Shared paragraphs:** workflows-and-surfaces §8, §5 and §2, and query-projection-contract §7.
- **Repair owner:** the reference constructor still emits a major-1 plan. The control relabels it as repair:2 and remints the id, and says so.
- **config2 and recommendations:** config2 has no published schema, so proposals are limited to `discovery.workspaceRoots`. Real recommendations need registered details and a successor record.
- **Suite admission detail:** the policy-test suite admission refusal uses `CONFIG.INVALID`, whose registry owner is security; please confirm it covers workflow suite admission.
- **Not modelled:** HTML renderings.
- **Synthetic inputs:** trust origins, waivers, a disposition receipt id, and a copied security fixture.
- **Pins:** not updated; you need to rebind them and run the owner launcher after integration.

No acceptance or readiness is claimed.

Files are in `/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2`:
- review.md (sha 609011cd…)
- review.json (sha 6dbde41b…)
