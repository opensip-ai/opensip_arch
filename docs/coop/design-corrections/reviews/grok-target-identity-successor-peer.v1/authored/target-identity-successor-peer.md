# Target-identity successor — coauthor peer

**Verdict: CHANGES_REQUIRED.** Three required corrections remain. ACCEPT_SCOPED is not available.

This is a bounded coauthor peer of the isolated successor at
`/tmp/opensip-design-corrections/target-identity-successor.v1` against frozen
`candidate-subject.v24`. It is not blind-consumer reconstruction, not whole-design
acceptance, not pin reseal, and not product qualification.

Reviewer: actual Grok, fresh session. No source edits, no pin writes, no freezes,
no subagents, no web.

## Subject custody

Task input manifest SHA-256 `e0d0522eb1f70465bd37792eff6aaa1cf9d69893ce128948b4a2d6224f415f93`
(18 files, standing “Exact target author COMPLETE63 source before root
integration; NOT accepted”).

Every listed path is byte-identical across the task input copy, the successor
tree, and the manifest row (hash and length). Non-review successor vs frozen
delta is exactly those 18 paths: 17 modified, 1 new
(`foundation/target-attribution.schema.v2.json`). No other non-review file
changed size or appeared/disappeared.

Frozen source-pin ledgers are **not resealed**. `run-evaluator3-checks.py`
refused before any suite job: `sourcePinsValid=false`, 17 drifted pinned paths,
new V2 schema unpinned. Focused checkers below were run directly against
successor bytes and are **pre-seal measurements**, not a global profile pass.

## What this successor gets right

Ordinary first-party file/package occupancy is now a mapped `evaluationNativeId`
on TargetAttributionV2, not a payload-vs-N compare. Opaque `SubjectIdV1` payload
IDs remain on `targetNativeId`. Schema refuses V1 sidecars, null first-party
`evaluationNativeId`, and missing first-party/external package `packageManifestPath`.
Same-provider first-party occupancy conflicts refuse;
cross-provider equal opaque strings are not aliases. Symbol exact-id without a
sidecar still occupies at the atom owner. Owner `close_run` of the imports-file
fixture fails with one finding (`run3:655602a89dfa346614c59f57a7f63550f7ca5eb7a244d97c0cdc4e8119ddd95d`),
and `execute_graph_query` incoming on inventory `a.ts` returns that occupancy
vertex while `file:a.ts` is `QUERY.ENDPOINT_UNKNOWN`.

Those positives do not close the three root concerns.

## Root concern 1 — provider return transport

**Finding: downstream custody is specified; worker→host delivery is not.**

Native-evidence now says a Plan-selected fact-producing provider “returns
TargetAttributionV2 records as typed companions of its resolved binary-id facts”
and the host captures admitted bytes into `hostCapture.hostDerivedRefs`
(`domain=target-attribution`). It also says protocol3 phases and frames are
unchanged.

Measured owner fields:

| Channel | TargetAttributionV2 field? |
|---|---|
| protocol3-transitions.v1.json frames | no attribution frame; `FactBatch` present |
| rust-provider-protocol.v2.json `FactBatchV2` | required `analysisOrdinal, stageId, batchIndex, candidates`; `optional: []` |
| fact-plane FactCandidateV1 | closed, `additionalProperties: false`, `optional: []`; payload is relation CBOR only |
| native-evidence.schemas.v2.json | no `TargetAttribution` / `target-attribution` token |
| execution-inputs.schema.v1.json `InputRefV1.domain` | `target-attribution` already present in frozen24 |
| identity-schemas.v3 `byDomain` | pointer switched to `target-attribution.schema.v2.json` |
| execution_inputs_model join | schemaVersion=2, `sourceFactId` in selected views, `producerClosure` and `planId` match |

`hostDerivedRefs` is custody of a canonical-record blob the host already holds.
Inventories have cell-outcome digest names. IncomingSearch is also host-derived
and also has no protocol3 frame, but it is not claimed as a per-fact companion
of `FactBatch`. The successor’s new claim is that the **fact-producing**
provider emits a typed companion of the source fact. The only worker→host fact
return is closed `FactBatch`/`FactCandidate`. No owner schema field on that
return names the companion.

Existing channels therefore do **not** suffice: the demonstrated fields are
admission/custody after capture, not provider delivery. A later protocol
extension is exactly what the author charter forbade as an incomplete design.

**MUST M1.** Name the worker→host return. Either a closed field on
`FactBatch`/`FactCandidate` (digest or inline record) whose bytes admit as
TargetAttributionV2, or a published non-frame typed return schema that the
analyze-stage host is required to receive, with exact owner selectors. Keep
`hostDerivedRefs` as custody after join. Do not treat “not a protocol3 frame”
as a completed return path.

## Root concern 2 — independent exact-id vs sidecar first-party identity

**Finding: lawful portable IDs allow the operand, and independent-known-fact
priority is violated.**

Atom contract and V2 join-law both say unknown sidecar fields cannot override
known ephemeral fields, and `occupancy=external` while ephemeral is first-party
refuses `TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY`. Exact-id
ephemeral first-party is existing source authority (symbols; accidental
colon-path files whose inventory `nativeSubjectId` equals the payload string).

`_join_sidecar` first-party inventory join is on `evaluationNativeId`, not on
the ephemeral identity. Same-kind disagreement of those two identities is not
refused. `_reconcile_attribution` then overwrites ephemeral `nativeId` with
sidecar `evaluationNativeId` when both are first-party (`source=sidecar+ephemeral`).

Discriminating operand (ATOM-JOIN-HELPER + ATOM-EVALUATION):

- payload `resolvedTarget = file:src/a.ts`
- inventory contains file `file:src/a.ts` (exact-id) **and** file `src/a.ts`
- sidecar `occupancy=first-party`, `kind=file`, `evaluationNativeId=src/a.ts`

Results:

- ephemeral: occupancy first-party, `nativeId=file:src/a.ts`
- join admitted
- reconcile `nativeId=src/a.ts`, source `sidecar+ephemeral`
- `exists` on `src/a.ts` = true; on `file:src/a.ts` = false
- **same maps with sidecar removed:** `exists` on `file:src/a.ts` = true; on `src/a.ts` = false

So an independently known first-party occupancy identity is relocated to a
different identity of the same kind. That is stronger than the refused
external-vs-first-party case. Symbols cannot do this (`evaluationNativeId` must
byte-equal `targetNativeId`). Files/packages can, including the colon-path
exact-id the V2 schema itself names as existing authority.

Same-provider two-sidecar occupancy conflict does **not** cover this: this is
one sidecar versus independently known inventory exact-id, not two sidecars.

**MUST M2.** When ephemeral occupancy is first-party, a sidecar first-party
identity of the same kind MUST equal the ephemeral identity
`(kind, nativeSubjectId, packageManifestPath or empty)` or refuse (kind
disagreement already exists; add an occupancy-identity disagreement or reuse a
named key). `_reconcile_attribution` MUST NOT overwrite independently known
ephemeral `nativeId`. Sidecar first-party mapping remains the occupancy identity
only where ephemeral occupancy is not independently first-party.

## Root concern 3 — query projects raw sidecar, not reconciled occupancy

**Owning law:** atom-evaluation-contract occupancy compare and identity-and-evidence
§4 (“occupancy-identity target vertices”). Query-projection-contract table law
currently names raw TargetAttributionV2, including “without V2 or occupancy=unknown
the fact is unprojectable.” That query sentence conflicts with atom precedence
(“prefer independently known ephemeral fields”) on the same occupancy identity.

`query_projection_model.project_fact` reads `target_attr` occupancy/`kind`/
`evaluationNativeId` and never calls `_reconcile_attribution` / `_ephemeral_target`.
`execute_graph_query` feeds `retained_attributions(proof)` into that function.

Discriminating results:

| Operand | Atom (`evaluate_atom`) | Query |
|---|---|---|
| imports target = unique symbol inventory id, **no sidecar** | exists **true** (ATOM-EVALUATION) | `project_fact` unprojectable: “imports target kind requires admitted TargetAttributionV2” (QUERY-PROJECT-HELPER). Not a full Run false. |
| same, sidecar `kind=symbol` `occupancy=unknown` | exists **true**, reconcile occupancy first-party source=ephemeral | unprojectable: “unknown occupancy is not a graph endpoint” |
| owner imports-file Run with V2 sidecar | close_run ADMIT, verdict fail, 1 finding | `execute_graph_query` incoming `a.ts` returns 1 row (QUERY-OWNER-WRAPPER) |
| same owner facts, empty attribution map to `collect_projected_edges` | n/a | 0 projected, unprojectable-fact limitation (QUERY-PROJECT-HELPER; does not claim Run false) |

Unknown sidecar occupancy is not an unknown field in the “fill remaining unknown”
sense once ephemeral first-party is known. Query treating raw `occupancy=unknown`
as unprojectable **overrides** independently known occupancy and omits an edge
the atom resolved. Missing V2 on multi-kind imports does the same when exact-id
already uniquely identifies kind and identity.

The query contract still says “imports without TargetAttributionV1” (fact law)
and “Project from … retained TargetAttributionV1” (wrapper step 4), while the
table and model selected V2.

**MUST M3.** Graph projection MUST consume the same reconciled occupancy
projection as atom matching. Unknown sidecar occupancy MUST NOT unproject a fact
whose ephemeral exact-id occupancy is first-party. Missing V2 on
`imports@resolved-target` MUST still project when ephemeral uniquely identifies
`(kind, nativeSubjectId, packageManifestPath or empty)`. Update
query-projection-contract.v3.md so table, fact law, and wrapper step 4 name
reconciled occupancy, not raw sidecar, and drop the leftover V1 tokens.

Do not invent new graph kinds or multihop semantics. This is the existing
occupancy-identity vertex.

## Other required / recommended items

**SHOULD S1.** Same contract leftover V1 tokens (fact law; wrapper step 4).
Covered in substance by M3; still a producer conflict if those sentences survive
a projection fix.

**SHOULD S2.** `target-attribution.schema.v2.json` is absent from
`array-order-report.json`. New closed schema should enter the array-order owner.

**SHOULD S3.** V2 adds many `TARGET_ATTRIBUTION_*` keys marked “NEW/internal
pending root public-detail / D9 route-registry integration.” Same standing as
V1’s pending list, now larger. Root must route them before qualification; not
a reason to pretend they are published DomainDetailCode members.

**Advisory A1.** Focused `imports-file-none-false-on-mapped-target` reaches
`close_run` ADMIT with **Run verdict indeterminate**, findingCount 0. Subject-local
`none=false` on `a.ts` is asserted by the checker; that is not a whole-Run false.
The exists positive *is* a whole-Run fail (1 finding). Do not treat the none
fixture as a complete logical-negative Run.

**Advisory A2.** `execution_inputs_model` join checks schemaVersion / fact
presence / producerClosure / planId only. Occupancy identity remains atom
admission. Split is acceptable if every selected sidecar is later atom-admitted;
it is not a second occupancy owner.

**Advisory A3.** `atom_model` loads `TARGET_ATTRIBUTION_V1_SCHEMA` and never uses
it. Evaluator-projection-registry notes on types/unresolved-edge still say
“No TargetAttributionV1.”

## Focused reference measurements (pre-seal)

| Control | Boundary | Result |
|---|---|---|
| `run-evaluator3-checks.py` | PRE-SEAL-PIN-LEDGER | refuse; 17 drifted pins; V2 schema unpinned; no jobs run |
| `check-atoms.v1.py` | ATOM unit maps | 66/66 pass (includes new file/package/malformed/V1/conflict cases; does **not** include M2 overwrite operand) |
| `check-execution-inputs.v1.py` | execution-inputs join | ADMIT (`--receipt`) |
| `check-semantic-replay.v3.py` | identity `close_run` | passed 18; imports-file exists = fail/1 finding; imports none-false = indeterminate/0 |
| `check-query-projection.v3.py` | query schema + owner wrapper | 114/114 pass, including five `owner-imports-*` rows |
| Independent C1–C3 probes | labeled above | all recorded in `_peer_controls/independent-probes.json` |

These unit/replay passes do not imply M1–M3 are closed. Author checkers never
construct the overwrite operand or the unknown-sidecar-vs-ephemeral query split.

## Proposed remedy (source not mutated)

1. **Return:** add a closed worker→host field or typed analyze-stage return schema
   for TargetAttributionV2; keep protocol3 phase/terminal set unless that field
   needs a new frame. Point native-evidence at that field, not only
   `hostDerivedRefs`.
2. **Join:** refuse sidecar first-party identity ≠ ephemeral first-party identity
   of the same kind; stop overwrite in `_reconcile_attribution`.
3. **Query:** `project_fact` takes reconciled occupancy (shared with atom);
   contract table/fact-law/wrapper step 4 updated; leftover V1 removed.
4. Root pin reseal, array-order, and D9/public-detail remain root integration
   after those normative bytes exist.

## Limitations

- Review tree under `docs/coop/design-corrections/reviews/` was not hashed as
  part of the change-set (user barred unrelated review histories). Non-review
  trees were compared.
- C3 missing-sidecar symbol case is ATOM-EVALUATION vs QUERY-PROJECT-HELPER, not
  `execute_graph_query` on a second sealed Run without sidecar. Owner wrapper
  was executed on the V2-sidecar imports-file Run. Empty-attribution
  `collect_projected_edges` used that Run’s facts as a helper, labeled as such.
- No compiler, host, or platform qualification.
- No claim that frozen24 V1 Runs are accepted under this successor.

**ACCEPT_SCOPED is refused** until M1, M2, and M3 are corrected in successor
bytes and independently rechecked.
