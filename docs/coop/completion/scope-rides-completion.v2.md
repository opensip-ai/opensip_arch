# Scoped sub-obligation deferrals within the existing preview

Author: Codex lead. PROPOSED for independent Claude review under D-368.
This unit changes no row status and removes no row from the affected set.

## Decision and exact amendment

Under D-367's delegated product authority, extend D-056 **Eligibility item 2**
with this narrowly bounded limb: a member of an affected row may ride an
already-adopted scope disposition if the integrated application identifies
(1) its exact obligation, (2) the governing excluded product surface and
adopted scope decision, (3) the positive work deferred, (4) its re-entry trigger
and owner, and (5) the current refusal/preservation evidence that remains due.
The independent per-row review must find that no admitted preview behavior
needs the deferred member. An implementation label, difficulty, undecided
number, or future gate name alone never meets this limb.

This is the scoped successor that D-314 **Adopted text item 11, Q7** allows in
“a future reviewed successor may change the measurement, but the label does
not.” That sentence's rejection of label-only closure stands. D-056's literal
“Every remaining acceptance-evidence member is only harness execution,
fixture execution, or qualification measurement” applies to the active
preview members after the explicit dispositions below; it is amended only to
permit these reviewed scope rides. D-056's ban on treating unauthored active
schemas/fixtures/numbers as execution remains unchanged. D-002's row-level
scope and D-134's added DR-131/DR-133 remain unchanged: 23 rows require
SATISFIED and nine have separate adopted row-level deferrals.

The limb is the five-condition property above. This table is its measured
application at this cycle; a later ride must meet the same property in its own
reviewed act, and nothing here admits a ride by name. Each row may become SATISFIED only after all
its other active members meet D-056 gates 1–3 and D-368's independent review
and exact recording rules. Product implementation/qualification is subsequent
work; condition 5 is still a separate authorization.

## Rides over measured leftoverDesign members

| ID | Affected row and obligation | Existing scope and deferred positive work | Re-entry trigger and owner | Work still active now |
|---|---|---|---|---|
| SD-1 | DR-127 OBL-AL3-CORE-ROLLBACK | D-002 excludes self-update/repair; DR-110 is on its adopted deferral limb. Defer core release byte rollback contract/positive fixture only. This expressly supersedes anti-lockstep-leftover-join.v6's “or remains this row until that contract exists” for this excluded branch. | Before DR-110 enters any slice: Update/repair + release + security supply and review the owning rollback contract and AL-3 fixtures. | Independent component/core releases and generation rollback under DR-107/G18; no generation rollback presented as core byte rollback. |
| SD-2 | DR-105/DR-114 OBL-BLK-1, CA-2 customer-tool execution | D-002's explicitly trusted first-party preview and the accepted host-effect v25 CA-2 UNEXERCISABLE boundary exclude customer-tool execution. Defer positive authorization/execution design, not its refusal. | Before any CA-2 execution is admitted: DR-119 Product + Security + platform jointly adopt the product/authorization successor named by v25. | Refuse every CA-2 request, disclose the unavailable operation, preserve actor distinction and no-silent-downgrade; G12/G21/G32 negatives remain required. |
| SD-3 | DR-105/DR-114 OBL-BLK-2, CA-3 KEYCHAIN branch | D-002 defers DR-108 credential/keychain operations. Defer positive keychain action and credential-store API. | Before DR-108 enters a slice: Credential/security + platform define the action, custody, consent and fixtures. | KEYCHAIN remains not admitted; denied/unexercisable report and actor-join fixtures remain required. Other CA-3 subtypes receive separate explicit decisions in the security unit. |
| SD-4 | DR-124 OBL-INHERIT-BLOCKED, SC-EVIDENCE/SC-ANALYSIS positive lifecycle | D-077/D-078 preserve the DR-006/007 preview identity and authoritative result dispositions; D-002 scopes DR-124 to touched classes. Defer authoritative Run/evidence persistence, replay and identity-bound retention recipes. | Before authoritative evidence/analysis persistence enters a slice: Semantic architecture + state lifecycle + Security supply the DR-002–008 dependency contracts and state fixtures. | SC-CACHE/SC-OPS/SC-TRUST placement, backup/restore, revocation floors and no-silent-promotion remain active. Five total classes are retained. |
| SD-5 | DR-122 FC-OUTFAIL.committed-run-preserved, valid sealed-Run instantiation | D-077 leaves the governing RunId recipe unbound; D-002/D-077 exclude a sealed authoritative Run. Defer proving preservation of a schema-valid authoritative Run instance only. | Before sealed Run output or SARIF applies to an authoritative Run: Output/operability + Semantic architecture bind the governing recipe and execute the valid-Run G17 golden. | The independently reviewed opaque-object non-mutation golden is required now; no object decoding or assertion that it is a valid Run. Current required-output failure remains G26/G28; no new D9 code. |
## Prospective rides over reserved binding points

No leftoverDesign member measures SD-6–SD-8 today; these are recorded so
re-entry has a home. Their exact source selectors follow the table, and no
measured-member closure credit is inferred from them.

| ID | Affected row and obligation | Existing scope and deferred positive work | Re-entry trigger and owner | Work still active now |
|---|---|---|---|---|
| SD-6 | DR-112 repair trust/material and DR-120 packaging updateData/stateMigration positive repair branches | D-002 defers DR-106/DR-109/DR-110. Defer TR-REPAIR keys/positive repair payload, repair-media/update execution, and the reserved persistent-state migration binding. | Before the respective DR-106/DR-109/DR-110 surface enters a slice: State lifecycle + Update/repair + Security + release define the owning contract, roles, schemas and gates. | Typed absence, refusal of unsupported repair material, ordinary signed installation/replacement and current trust checks remain required. |
| SD-7 | DR-121 SL-5/SL-6 authoritative identity/replay/evidence CI branches | D-077/D-078 and D-002 defer sealed identity/evidence replay. Defer positive authoritative replay fixture instantiations only. | Before the corresponding authoritative branch enters a slice: CI + Semantic architecture supply valid identity/evidence inputs and the original SL assertions. | Preview offline installation/analyze, deterministic selected metadata, trusted fixture-domain ownership and all other SL slots remain required; do not label preview output replay an authoritative Run replay. |
| SD-8 | DR-124 SC-CACHE-REGENERATION-KEY for durable analysis results | D-077 preserves DR-006 recipe deferral; distribution completion explicitly chooses no durable analysis-result reuse in preview. Defer that consumer's key and equal-recompute contract. | Before durable analysis-result reuse is enabled: Semantic host + Lifecycle + Security review the recipe and equal-recompute evidence. | Cache class remains active; disposable cache cannot influence semantic results, and cached downloads undergo current digest/signature/trust admission. |

CA-1 IN_PROCESS, CA-3 LOCAL_SOCKET_OR_PIPE/PRIVILEGED_PLATFORM_FACILITY and
CA-4 PATH-INDEX-REACH/PATH-DECLARED-EXTERNAL-SERVICE are **not additional scope
rides**. The security contract makes explicit current product admission
choices and supplies negative fixtures; those choices close the current
admission question. Admitting a new operation later requires a reviewed
successor. They cannot be used to omit an admitted preview operation's design.

## Exact source selectors

All paths below are relative to `docs/coop/artifacts/`. Full hashes are
retained in `scope-rides-freeze.v2.json`; selectors are JSON Pointers.

- SD-1: `anti-lockstep-leftover-join.v6.json` `/obligations/5` (OBL-AL3-CORE-ROLLBACK).
- SD-2: `permission-leftover-join.v12.json` `/obligations/14` (OBL-BLK-1); `doctor-actor-leftover-join.v12.json` `/obligations/19` (OBL-BLK-1).
- SD-3: `permission-leftover-join.v12.json` `/obligations/15` (OBL-BLK-2); `doctor-actor-leftover-join.v12.json` `/obligations/20` (OBL-BLK-2).
- SD-4: `state-class-leftover-join.v5.json` `/obligations/6` (OBL-INHERIT-BLOCKED).
- SD-5: `sarif-leftover-join.v14.json` `/obligations/7` (OBL-FC-OUTFAIL-FX).
- SD-6: `signed-index-trust-contract.v14.json` `/roles/4` (TR-REPAIR); `component-manifest-schemas.v11.json` `/manifestSchema/fields/17` (stateMigration); `component-manifest-schemas.v11.json` `/manifestSchema/fields/18` (updateData).
- SD-7: `monorepo-ci-contract.v16.json` `/sharedLanes/4` (SL-5); `monorepo-ci-contract.v16.json` `/sharedLanes/5` (SL-6).
- SD-8: `state-class-contract.v11.json` `/classes/2/previewStanding` (SC-CACHE regeneration-key producing rule).

## Recording, re-entry and reversibility

The integrated application manifest records SD-1–SD-5 against their measured
join obligations and SD-6–SD-8 against their reserved binding-point selectors and retains this unit's exact digest and independent
verdict. Re-entry reopens the affected row's corresponding member before
activation; the previous SATISFIED applies only to its recorded preview scope.
No positive deferred operation inherits qualification, permission or authority
from a negative fixture. Overturning this act restores D-056's unsplit
remainder rule for these members and reopens every dependent row still relying
on a ride. Historical decisions and source artifacts stay byte-identical.
