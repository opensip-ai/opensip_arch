Root's finding holds, and I fixed it by removing the fallback in `_select_dep_coverages`. Neither validating the scope carrier nor limiting the fallback to exact coordinates would have worked. Carrier checks alone still let a valid scope at the wrong universe, relation or rung supply the dependency. Limiting it to exact coordinates just duplicates the main path, because `_scopes_exact` already selects every such scope. This is authorship only; nothing here is acceptance or qualification.

**The defect.** On frozen35, a dependency scope whose `sourceUniverse`, `relation` or `resolution` is absent, null or different still made `all-covered` true, on both endpoints. Ten variants did this, including a rung that is valid for `calls`. With the fallback removed, a non-exact scope is simply ignored, exactly as if it had been deleted: the answer is unknown, the dependency isn't cited, and the causes are `coverage-unknown` and `required-relation-missing`. An exact scope that fails its carrier still refuses `ATOM_NATIVE_CARRIER`. I1, the three cause channels, known-fact and count-bound dominance, pairing, folds and whole-source dependencies are unchanged.

**Can a real Run reach it?** No, as far as I can tell; I did not build a closed or retained Run to prove it.
- **Native producer (measured):** `admit_coverage_result_v3` rejects all ten variants. The six absent/null cases fail schema validation, and the four different-value cases fail the coverage-key/scope coordinate check.
- **Run closure (read only):** closure requires each Coverage's scope to be in its view and re-runs that producer check. The evaluator input model copies every view scope. So on inputs rebuilt from an admitted Run, the fallback never triggers, and the fix changes no admitted result I can identify.

**Reviewer v35 finished while I worked.** It accepted frozen35, not these bytes, and recorded this same fallback as advisory A-13 ("unreachable for retained Runs"). None of A-13's seven cases produce `true` on the successor anymore. My probe and root's also found that null `relation`, null `resolution` and an off-ladder rung produce `true` on frozen35; A-13 doesn't list those, and they are also unknown now. Deciding A-13 against these bytes, and an independent review of them, are root's.

**My changes** (frozen35 → successor):

| File | Change | Lines |
|---|---|---|
| `atom_model.v1.py` `c1243ca9…` → `2c5fdabb…` | fallback removed, docstring added | +12/−12 |
| `atom-evaluation-contract.v1.md` `f6c3b375…` → `72986bd3…` | §4 now says exact selection only, no mapped fallback, non-exact scopes ignored not refused, applies at every depth; §9 cases added | +2/−2 |
| `check-atoms.v1.py` `11aa038a…` → `67d8c656…` | 6 new checks, no existing line touched | +191/−0 |

Frozen35 already carried root's edits on top of my earlier incoming-binding work: the contract refusal wording and the borrowed-scope check. The report keeps those separate from mine.

**Checks.** 95 of 95 pass, and the original 89 passed on the fixed model before I added anything. None of the 89 ever reached the fallback, so no expected outcome changed.
- **Fail on frozen35, pass on the successor:** the ten-variant check, the known-fact check, and a depth-2 check that uses a synthetic dependency graph, since the published graph is only one level deep.
- **Pass on both (non-regression pins):** exact pairing by mapping or commitment plus carrier refusal, order independence with two disjoint scopes, and clones whole-source behaviour.
- **Downstream checkers:** all seven that import the atom model exit 0 with identical output on both trees.

**Still open:**
- **Found but not fixed:** consider an incoming reachability scope over both f and g, where only f has a matching `calls` dependency scope. `all-covered` is true on frozen35 and on the successor. The contract doesn't say whether every subject needs its own dependency partition, so this needs a decision from root. It's only shown on synthetic inputs.
- **Root's to do:** reseal the 15 stale pin rows (the three files across five ledgers; no new pin needed), run the integrated groups, and get an independent review of these bytes.

Files are in `/tmp/opensip-design-corrections/claude-dependency-scope-author.v1/`:
- review.md
- review.json
