Status update, since this is a long run.

**Done so far:** all ten items are implemented in the working copy, and each new control section passes: M1 23/23, M2 20/20, M3/S3 33/33, S1 23/23, S2 17/17, A4 11/11. S4, A1 and A2 passed in an earlier combined run (74 controls, whose only two failures were M1 expectations since fixed). Items whose checks needed real Runs have positive and negative Run controls. Without their pin gates, the native checker's full `main` passes as on the parent (377/377), and the security cases and sweeps pass (464 cases, 11/11 sweeps).

**Suite still running.** The all-checkers run on the corrected source is at query-projection. So far every checker exits 0 except semantic-replay, which fails only because 8 pinned golden Run/Coverage ids are stale. Still to come: comparison-knowledge, workflows, analysis-seal, security (expected to stop at its pin gate), integration, native-cases and corrections.

**Next, once the suite finishes:**
- Apply the goldens id rewrite. Its dry run is clean: 16 ids, plus one carrier-role exchange that the termination contract's "canonically least carrier" rule makes lawful.
- Rerun semantic-replay.
- Produce the changed-file manifest and full diff against source38, then write review.md/json.
- Finish with a single check that the frozen parent is unchanged.

**Already clear for the review:**
- Only one registered schema document changes bytes (`enumeration-plan.schema.v1.json`, `62ff499e…` → `10627cb6…`).
- 18 pinned files differ; that is root's pin work.
- The registered native schema's `ResolvedNodeModulesLayoutV1` description contradicts the A4 read-set decision. I left those bytes alone and am flagging it as a cross-owner item.
