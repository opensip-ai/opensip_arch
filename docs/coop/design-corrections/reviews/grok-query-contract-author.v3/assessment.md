I'll start from root's v3 retained probes and the current query successor, then apply only the remaining required corrections on the owned isolated files.I have the remaining defects. Next I’ll patch the model, schema, and contract, then add discriminating controls that use admitted Runs.I'll verify the isolated successor tree, v3 reports, and remaining required corrections against disk before touching any owned files.v3 reports and a newer root `retained-probes.v4` are already on disk. I'll compare those against the isolated successor sources next.v3 reports claim 101/101, but root already has `retained-probes.v4`. I'll verify live source hashes and whether those new probes still fail.Root ran `retained-probes.v4` against the v3 model after those reports. I'll read those results and check the implementation against the seven required items.Root v4 still shows `lim=None` on the no-selected-views probe. I'll inspect that result and the model’s limitation path next.Item 5 lands in `resolutionLimitations`; the explicit-unrelated-view probe still returns an empty list. I'll audit the model against all seven required items.`parameter_row_of` keys match `ENUM_PLAN_ROW`. I'll confirm enumeration-plan selection on an admitted Run, then apply the remaining item-5 fix.Enumeration-plan digest selection is correct on the admitted Run. Next I’ll fix native-evidence-unavailable for explicit unrelated views and add the missing controls.Checker is 108/108 and the first failing run is still preserved. I'll write the v3 reports with exact hashes and remaining limits.Query successor v3 is a coauthor correction of the isolated tree, not independent acceptance.

Required items 1–7, EnumerationPlan digest selection, and availability refuse-not-grant are corrected. Focused checker is **108/108 PASS**. The first failing run is preserved. No ACCEPT.

Root `retained-probes.v4` against the first v3 model (`10cd224f…`) still had empty `resolutionLimitations` when explicit unrelated `factViewDigests` were selected for `calls@resolved-callee`. That remaining item-5 gap is closed: `native-evidence-unavailable` now fires when **no selected view** matches the requested relation@rung.

### Dispositions
1. **RequestId** — reserved `host.requestId` only (`req1_`+32 hex). Never a content hash. Missing host id is `ReferenceCallPrecondition`, not a public refusal. Malformed `projectId` omitted from the failure envelope.
2. **Validate-before-Run** — malformed request without a Run is `QUERY.PARAMS_MALFORMED`. `runId` mismatch is `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN`.
3. **Snapshot uniqueness** — explicit complete `host.runsForSnapshot` observation required (missing/empty UNKNOWN, >1 AMBIGUOUS, unique other-run UNKNOWN).
4. **`resolutionState`** — native token `incomplete`; kind stays `resolution-incomplete`.
5. **`native-evidence-unavailable`** — empty auto-selection **or** explicit unrelated views; matching selected views do not emit it.
6. **Canonical BFS** — `fact2` adjacency order; first reach is shortest+tie witness then stop; cap before target claims no path.
7. **Unknown tuple** — fully specified unknown is `ENDPOINT_UNKNOWN`; package missing-path stays AMBIGUOUS.

**EnumerationPlan** uses registered `schemaDigest` via `parameter_row_of`, not duck-typed `cells`. **Availability** is a trusted host observation owned by foundation `EvidenceStore`: purged/expired refuse; they cannot grant retained authority.

### Authored (isolated successor)
| Path | SHA-256 |
|---|---|
| `graph-query.schema.json` | `e14ea2f9d4d03ef23182cab6a7279c846ee552ebbdd7fc3082184660cd7354c1` |
| `query-projection-contract.v3.md` | `2a8f6d44615591df33955dee53d04b25bc8fcf6dab159041f2ad47916f62551b` |
| `query_projection_model.v3.py` | `8da16bea35af5f8ecb2518973ce6b668a94fa0d14c860d89c37173a9f99c28e1` |
| `check-query-projection.v3.py` | `19de09307e0e8287fb0a33f5f71b7c8966cd788beafcea54fa5bff74a3e834de` |

Command inventory, surface projection, profile checker, foundation pins, frozen23, and live normative design were not edited.

### Controls
- First failing run kept: `original-failures.json` `a4d4931b…` — 101 checks, 1 FAIL `path-stops-at-first-canonical-bfs-target`
- Final: `final-results.json` `e63d7ff7…` — **108/108 PASS**
- Reports: `/tmp/opensip-design-corrections/grok-query-contract-author.v3/{review.md,review.json,authored-hashes.json}`

### Remaining limits (honest)
- Native `incomplete` Coverage is mapped from `completeness_from_stage`; the owner semantic fixture unresolved path is still `not-attempted`.
- `imports@resolved-target` multi-kind is not an owner-admitted TS positive.
- Independent successor review, new blind, and application review are still required.
