All eleven native findings are dispositioned in `output/review.md` and `review.json`. M1, M2, M3, S1, S2, S3, S4, A1, A2 and A4 are corrected; A5 is merged and finished. On the final source every focused check passes except the security checker, which stops at its source-pin gate. No check processes are still running.

**Continuation and custody**
- v1's full check run never finished: query-projection has no exit record, and the checkers after it never ran. I reran everything here.
- The v1 source matched root's partial capture exactly (12,905 files, `14f29c96…`). I copied it as regular files into this runtime's `source/`. v1 itself was not modified.
- I didn't re-hash the whole source38 tree. The diff tool refuses unless every changed file's source38 bytes match the source38 manifest, and it passed.

**The two scope resolutions**
- **A4 schema:** the registered `ResolvedNodeModulesLayoutV1` description now matches the read-set law.
  - A layout row describes a package directory; it is not an inventory row.
  - Files actually read inside a listed package are snapshot inventory rows, checked at Run closure (`SNAPSHOT_PRUNED_TREE_NOT_A_READ`).
  - Compiler, standard-library and Rust dependency inputs from outside the project stay in their own closures and are never snapshot paths. Identity §3 says the same.
- **A5 merge:**
  - Root's diff and ce3's `proposed-amendment.r2.diff` were merged section by section (each hunk had to match exactly once), with no whole-file overwrite. The merged text is byte-identical to root's model change and ce3's amended prose and cases.
  - The stale F11 case is renamed, the three new cases are in, and the README F11 row is updated.
  - I added a statement that the flags law introduces no compiler-option diagnostic refusal (5052 included) and names no owner that routes one.
  - The in-tree native report was regenerated with the checker's own `main()` (PASS, 380/380). Only its pin gate was bypassed, and the report records the 21 real pin faults.

**Registered schema consequences.** Two registered documents change bytes; the other six don't.

| Document | source38 | now |
|---|---|---|
| `foundation/enumeration-plan.schema.v1.json` | `62ff499e…` | `10627cb6…` |
| `native/native-evidence.schemas.v2.json` | `3e37c7b7…` | `2d37b810…` |

These changes flow into Plan and Coverage identities, and from there into Run ids. The S1 closure-tree, S4 account-value and A5 mode changes move the same chains for the fixtures they touch. Historical v2 files and exports are unchanged.

**Goldens.** All 16 pinned Run and Coverage ids were remapped by what each Coverage is about. The rewrite only succeeds if each new expectation equals what the corrected Run actually derives. Under the final identities no carrier-role swap was needed; v1's single swap is superseded. Semantic-replay passes with all 8 goldens. The current ids are in `review.json#/goldens`. The new checker command to add is `python -I -B docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py`.

**Checks run** (24 jobs, receipts `*-v2-final`)

| Check | Result |
|---|---|
| New corrections checker | 159/159 (M1 23, M2 20, M3 21, S1 23, S2 17, S3 12, S4 8, A1 17, A2 6, A4 12), including real Run passes and refusals |
| Native checker `main()`, pin gate bypassed | 380/380 plus all static sweeps clean |
| Security lifecycle, pin gate bypassed | 464 cases, 11/11 sweeps |
| Identity (v2 lane) | 1596/1596 |
| Workflows | 1816/1816 |
| Integration (v2 lane) | 412 passed |
| Enumeration, execution-inputs | 0 mismatches |
| The other replay and projection checkers | exit 0 |
| **Security checker** | **exit 1: stops at its source-pin gate, no cases run** |

v1's failed attempts are kept as receipts and listed in the review.

**What root still needs to do**
- Regenerate the five source-pin files and the planning registries.
- Run the six global groups.
- Merge the proposed security S3 "Pruned trees and the read set" paragraph (text is in the review).
- Record that security's discovery unit list doesn't include the S3 fallback unit.
- Merge these goldens with other authors' additions.
- Rebuild the author package; any other evaluator3 stage-spec fixture must register its output schema in its producer closure.

**Limits**
- The S2 map law has real Run controls only for the syntax universe; no current v3 fixture builds TypeScript or Rust clone bodies.
- The A4 read set is recorded per package directory, not per file.
- The TypeScript compiler wasn't rerun; A5 relies on the 52 retained observations (root's 32, ce3's 20) as supporting evidence, not a product pin.
- No acceptance or readiness is claimed.

Files are in `output/`:
- review.md
- review.json
- source38-to-corrected.diff
- changed-files.v1.json
- v1-to-v2.diff
- v1-to-v2.changed-files.json
- evidence-index.json
