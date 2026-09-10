# Query occupancy reconciliation — coauthor peer

**Verdict: `ACCEPT_SCOPED`**

Fresh independent coauthor peer of the bounded query occupancy correction. Not a blind consumer, not a final whole-design review, not pin reseal, not product qualification. Provider-return (M1) and C15 sidecar-overwrite (M2) are separately authored and are **not** accepted or reopened here.

No MUST blocker was actually reached on public `execute_graph_query` after complete `close_run`. Helper-only failures are preserved as helper-only and are not whole-Run proof.

## Standing and custody

- Only source: `/tmp/opensip-design-corrections/grok-query-reconciliation-correction-peer.v1/inputs/source`
- Additional inputs read: `author.md`, `author.patch`, `root.patch`
- Writes: this output directory only. Inputs were not mutated.
- Source manifest SHA-256 `75e9e648dd216c25c498de72c8cd0e6dd11e122871aa0537de5eb1240646d082` (255900 bytes). **1318/1318 files** matched SHA-256 and size. Missing 0, mismatches 0, extra 0.
- Manifest standing: exact root integration source copy before provider-return merge; pins stale; cannot claim global pin pass.
- Source already contains the author overlay plus `root.patch` on the query contract. Author-claimed contract hash `a7c64284…` / 20762 bytes is the pre-root wording. Integrated contract is `629ec5f8b097c74a95b2a981deddc6ea010339390a3570e25985779575d97f4d` / 21128 bytes.

| Input | SHA-256 |
|---|---|
| `source-manifest.json` | `75e9e648dd216c25c498de72c8cd0e6dd11e122871aa0537de5eb1240646d082` |
| `author.md` | `86832d1b637efb90dd0bd2e10175b50d95d17192de55cf6e21ee7c3f567c2992` |
| `author.patch` | `3f76e1562f05c26d609e7d7b467898400d9eb1220452f63a5cc523873375068a` |
| `root.patch` | `1f05ec1ad7b6d32c17a6339baaab0d51f77bf75731f5f04999b7b0437e32c6a1` |

Reviewed source bytes:

| Path | SHA-256 | bytes |
|---|---|---|
| `workflows/query_projection_model.v3.py` | `4c9c91215fb70653ae75b563f6ba38788e410eb4004c4e9765e3bc08e8259e0a` | 58283 |
| `workflows/query-projection-contract.v3.md` | `629ec5f8b097c74a95b2a981deddc6ea010339390a3570e25985779575d97f4d` | 21128 |
| `workflows/check-query-projection.v3.py` | `f90f100142bcbeaab546aa270365c82b5f9b28f972da152e29cbc3787230054c` | 52470 |
| `foundation/evaluator_semantic_fixture.v3.py` | `87aed7412091f67103c815f35c8ce9714037348d4d71f3771fda88119a76ae5e` | 40539 |
| `foundation/atom_model.v1.py` (not this proposal) | `99d9d79fe5ace3c22595791924b89fad7a2cdbc38835425c605db8779703e6c4` | 90962 |
| `foundation/atom-evaluation-contract.v1.md` | `030e9e9cea54ec93667be86e4e59b68f6a307e7847d2115621b71f77b704f7b3` | 22290 |
| `foundation/target-attribution.schema.v2.json` | `1ec8c07ae18558671de8d8a9f703767eae67ce18f27500a6a534fd29a7bc67a2` | 19173 |

Root wording in the integrated contract is the occupancy law used here: selected occupancy is TargetAttributionV2; a selected `schemaVersion=1` sidecar causes retained Run admission to refuse; it cannot reach public edge projection and is not downgraded to an omitted edge; occupancy identity follows atom evaluation §2 and the selected V2 join law; the reference helper is an implementation of those laws, not an additional normative input.

## Occupancy identity (public path)

Intended query projection uses the same reconciled occupancy identity as atom matching: ephemeral exact-id first-party when payload native id uniquely equals one inventory native id; known ephemeral fields override unknown sidecar attestation; otherwise V2 sidecar mapping; missing mapping and no unique exact-id is unprojectable on multi-kind `imports@resolved-target`; unknown attestation must not erase a known occupancy identity. Inputs are the admitted Run’s selected `evaluationInputRefs` (`subject-inventory`, `target-attribution`), the plan enumeration binding, and named producer closures. Host cache / standing / `targetAttributions` / census are not authority. No SubjectIdV1 `namespace:opaque` parse. No extra graph kinds or aliases.

Public `execute_graph_query` always calls `close_run` first, then `occupancy_inputs_from_retained`, then `atom_model._reconcile_attribution`. Independent probes after complete `close_run` observed:

| Mode | Atom matching evidence | Public query |
|---|---|---|
| Ordinary mapped file | `a.ts` exists = true; matchingFactIds `[fact2:40400803…]` | incoming `file/a.ts` one edge, target native id `a.ts` (not `file:a.ts`), same factId, same universe |
| Exact-id symbol, no sidecar | `symbol:foo` exists = true; matchingFactIds `[fact2:5d039783…]`; no selected target-attribution | incoming foo from bar, target kind symbol, same factId |
| Unknown sidecar + unique inventory | `symbol:foo` still true; same matchingFactIds; forged `host.targetAttributions` / cache / standing | still one incoming edge to foo; host objects do not grant occupancy |
| Actual absent mapping | `a.ts` exists = **indeterminate**; matchingFactIds empty; uncertainFactIds `[fact2:40400803…]` | outgoing unprojectable-fact “missing occupancy mapping with no unique exact-id identity”; incoming `a.ts` empty success — **not** native none |
| Single-kind references, no sidecar | foo exists = true; matchingFactIds `[fact2:65225291…]` | outgoing still projects payload native id; same factId |
| Isolated package vertex | n/a | empty neighbors, success, not absence; missing `packageManifestPath` is `QUERY.PARAMS_MALFORMED` |

Five binary rungs only: `calls@resolved-callee`, `references@resolved-binding`, `imports@resolved-target`, `control-flow@syntactic`, `reachability@from-resolved-calls`.

## V1 sidecar: helper vs full Run

Root law: V1 is global admission refusal, not an omitted edge.

| Path | Actual result | Standing |
|---|---|---|
| Helper `collect_projected_edges` with occupancy_inputs mutated to `schemaVersion=1` | `unprojectable-fact` note `occupancy admission TARGET_ATTRIBUTION_SCHEMA_VERSION`; zero projected edges | **Helper-only.** Preserved. Not whole-Run proof. |
| Seed-time selected V1 through `close_positive` / `close_run` | `AdmissionError: REGISTERED_RECORD:#` (current registered TargetAttributionV2 `schemaVersion` const 2). No Run is produced. | Full retained admission. Public query never starts. |
| Sealed proof rewritten to a new V1 digest without reminting identities, then `execute_graph_query` | `QueryRefusal` `HOST.IO_FAILURE` / `evidence.corrupt`; termination class `operational-failed`; `close_run` `REFERENCE_IDENTITY` | Public path. Not an omitted-edge success body. |

A malformed/current-wrong V1 sidecar (`schemaVersion=1` with leftover `evaluationNativeId`) also refuses at seed-time `REGISTERED_RECORD:#` and, if hand-fed to the helper after a good close, is still caught as unprojectable. The catch lives inside the public call chain **after** `close_run`, so it is not reachable on a complete successor Run. That is L1 below, not a public occupancy identity blocker.

## Checks actually run

Disposable copy: `output/disposable/work` from `inputs/source`. Python `/tmp/opensip-architecture-review-env/bin/python -I -B`. **Pin-gated global suite not run.** `run-evaluator3-checks.py` not invoked and not claimed.

| Command | Exit | Result | Receipt SHA-256 |
|---|---|---|---|
| `check-query-projection.v3.py --report output/receipts/query-projection.receipt.json` | 0 | **123/123**, 0 failed | `9465ea7ff956191b936bc82b9a72c1b5e58163969d407012ecfa5c5bd3d53423` |
| `check-semantic-replay.v3.py --output output/receipts/semantic-replay` | 0 | **passed 18**, blocked [] | `4d02a93009eededc6afdcb9516135db9a2941095cb52a7afdffe46cd957f1f19` |
| `output/probes/independent_occupancy_probes.py` | 0 | **42/42** public `execute_graph_query` + `close_run` + helper distinction | `a4ddd5f6593217630b99f8f72d88c60660298ec6e763728d6edba74a4cf550d8` |
| `output/probes/v1_close_run_admission_probe.py` | 0 | **8/8** seed-time V1 vs helper | `1f4baf2b04cb2589b6819a5ef0b623757c89dda42252220a921f4296447f11aa` |
| `output/probes/unmapped_verdict_dump.py` | 0 | unmapped exists: 7/7 predicates indeterminate, verdict pass, findingCount 0 | `b46a11670a4b1475ea1757779f7d941b79a94e0c20287683bf328f77cac9ec66` |

Semantic 18 includes two default mapped-file imports cases (`imports-file-first-party-exists` fail/1; `imports-file-none-false-on-mapped-target` fail/6) plus non-imports positives and four finding mutants. That count pass is not census-parity and is not matchingFactId occupancy agreement.

First helper V1 failure is the catch in `collect_projected_edges`. It is recorded as helper-only (L1). It is not claimed as complete `close_run` behavior.

## Substantive findings

No MUST blockers. Three scoped observations that must not be inflated into whole-Run or whole-design defects:

### Q-PEER-L1 — LIMITATION, not blocker

**Finding.** `collect_projected_edges` catches `AtomAdmissionError` and records `unprojectable-fact`. A helper-fed `schemaVersion=1` sidecar is therefore omitted. Public `execute_graph_query` after complete `close_run` never gets there: selected V1 is refused by retained admission.

**Consequence.** Using the helper catch as V1 public law would contradict root: V1 is not an omitted edge. The public path matches root.

**Owner.** `query_projection_model.v3.py` `collect_projected_edges` / `_reconcile_fact_occupancy`.

**Reproducer.** `output/probes/independent_occupancy_probes.py` (`helper-collect-projected-edges-downgrades-v1-to-unprojectable` vs `fullrun-v1-cannot-reach-omitted-edge`); `output/probes/v1_close_run_admission_probe.py`.

**Minimal remedy.** Keep public law as `close_run` refusal. If later tightened, do not convert occupancy admission errors into omitted edges. Not required to accept this scoped correction.

### Q-PEER-L2 — ADEQUACY, not blocker

**Finding.** Author said the default mapped-file fixture is unchanged. Mapped-file payload/sidecar still occupy `a.ts`. Independently, imports subject-scope subjects are `{symbol:foo, symbol:bar}` for every imports occupancy mode, including mapped-file. Semantic 18 does not inspect that census.

**Consequence.** Broad replay parity from 18 counts is not census-parity. The extra `bar` source subject does not change mapped-file occupancy identity (query still projects `a.ts`; atom matchingFactIds still agree). It is fixture coupling for exact-id/unknown-sidecar, not host census authority and not a new graph kind.

**Owner.** `evaluator_semantic_fixture.v3.py` `subjects=E.cset([foo, bar])` on the imports scope.

**Reproducer.** Independent probe `census-default-imports-scope-includes-foo-and-bar`; author.patch hunk vs previous `[foo]`.

**Minimal remedy.** If later split, keep mapped-file source census as that mode’s importer set. Not required for occupancy identity acceptance.

### Q-PEER-L3 — ADEQUACY, not blocker

**Finding.** Author `*-atom-run-agrees` checks use `verdict` / `findingCount` only. Peer compared query `factId` to predicate witness `matchingFactIds` on public `execute_graph_query` after `close_run` and they agree for mapped-file, exact-id, unknown-sidecar, and single-kind references. Unmapped exists-target is **not** a known miss: all seven file predicates are indeterminate, `findingCount` 0, Run verdict `pass` because composition treats indeterminate without blocking deficiencies as non-gating. Query omits the fact and returns empty incoming success. Zero neighbors is not native `none`.

**Consequence.** Author `findingCount == 0` cannot be read as atom/query known-miss agreement. Occupancy agreement for this review is the matching-fact identity and the unprojectable limitation, not verdict.

**Owner.** `check-query-projection.v3.py` owner-imports atom-run-agrees controls.

**Reproducer.** `output/receipts/independent-probes.json`; `output/receipts/unmapped-verdict-dump.json` `unmapped-exists-file`.

**Minimal remedy.** If later tightened, assert predicate value and matchingFactIds identity, and state unmapped `findingCount` 0 / verdict pass as non-blocking unknown. Not a MUST occupancy defect.

## Coordination (M1 / M2)

Independently inspected:

- `atom_model._reconcile_attribution(fact, spec, inputs)`
- `atom_model._ephemeral_target(fact, spec, inputs)`
- `AtomAdmissionError.key` (sample `TARGET_ATTRIBUTION_SCHEMA_VERSION`)

Query does not overwrite `atom_model`. M1 provider-return and M2 C15 overwrite are **not in these source bytes** and are not accepted here. If M2 later wants a public adapter, add it instead of a second occupancy implementation. If M2 renames the private helper without a shim, the first occupancy call in this overlay fails. That is a coordination limitation, not a new query occupancy defect.

## Boundary limitations

- Not a full independent design review and not NEW-blind.
- Pins stale; no global evaluator3 pin ledger pass.
- No compiler / host / platform qualification.
- No new graph kinds, aliases, or per-language Runs.
- External package occupancy projection is in contract/code; no new imports-package fixture mode was exercised as a full Run.
- Query still imports the private atom helper; contract (post-root) cites §2 / V2 join law.
- `close_retained_run` maps non-missing `close_run` failures to `HOST.IO_FAILURE` / `evidence.corrupt`; that wrapping is existing public query admission, not a new occupancy rule.

## Verdict

**`ACCEPT_SCOPED`.** Public query projection on an admitted Run uses the same reconciled occupancy identity as atom matching for ordinary file mapping, exact-id symbol without sidecar, unknown sidecar that must not erase known inventory identity, honest unmapped omission, single-kind payload projection, and package endpoint coordinates. V1 cannot reach public edge projection. Helper-only V1 omission, fixture census expansion, and verdict/count-only author agrees are recorded as non-blocking limitations. Full design independent review and NEW-blind remain later.
