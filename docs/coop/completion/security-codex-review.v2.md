# Security completion v2 — independent Codex review

OBJECT: 5 MUST-FIX, 0 SHOULD-FIX. Frozen subject fca2a4b615a3261f61e2e2d7a685b1b747678dedc54f9f87d7adcd643ffd3b78 at HEAD 867175a. Reviewer authored none of the unit. Independent replay: 82/82 pass. No register edit.

## SEC2-M1 — Resolve stock Linux platform support against the stated threat model

security-completion.v2.md §8.4/8.6, v48 successor boundary

The proposed product now requires an OpenSIP-built kexec-absent kernel. §1 incorporates a threat model expressly excluding compromised OS and distribution signing chain. This requirement creates a new customer OS replacement prerequisite without establishing a needed security claim within that threat model.

Required repair: Adopt an explicit scoped OS-ABI successor with an honest assumed OS TCB and stock signed supported Ubuntu baseline, or independently justify the custom-kernel requirement against a concrete in-scope attack not already excluded. Preserve component loader and dependency exact-byte protections. This is a challenged design choice, not a claim that existing v48 already permits stock kernels.

## SEC2-M2 — Define a race-free lifecycle-to-operation lock handoff and witness reconciliation

§5.4; paired lifecycle-carrier v2

Security releases the fence before acquiring the operation lease; lifecycle v2 requires lease publication under the fence. End/start high-water copies claim no lease held yet read a carrier another writer may change. COMMITTED n with matching seq but differing hash has no specified branch; project rollback after last start floor can evade the blanket claim.

Required repair: Acquire project lease nonblocking under fence, compare/publish trust and lifecycle observations before releasing fence; never wait for fence under operation lease. Define a race-free end handoff/re-read or skip protocol. Reconcile every witness state including zero/genesis, malformed/missing, equal-seq unequal-hash, ahead/behind, generation mismatches. Author executable crash/restore/overlap cases and honest bounds of detection.

## SEC2-M3 — Make rollback claims consistent with the explicit detection boundary

§1 and §5.5

§1 says rollback yields denial, not stale authority, while §5.5 acknowledges undetectable coherent offline rollback with a suppressed marker. The former is not guaranteed under the latter, and copied project floors only cover observed operation boundaries.

Required repair: Bound fail-closed claims to detected/declared restores and observed floors. State explicitly that coherent unmarked rollback may reuse formerly valid authority until a trusted refresh/expiry observation. Do not claim an origin check happens before offline operations unless actually required.

## SEC2-M4 — Enforce semantic root admission before signature thresholds are consumed

root.schema.json and security_unit_lib_v2.py verify_envelope/root_keys_for_role

Independent probe changes roles.TR-COMPONENT.threshold to 1. The root schema admits it; with one retained signature verify_envelope returns VERIFIED, valid=1 threshold=1, contrary to chosen 2-of-3. No root semantic admission checker enforces exact role membership, keyId/publicKey consistency, references, distinct/disjoint keys, role activity or threshold selection. previousRootVersion is also uint53 while rootVersion is i64, preventing a valid high-version chain.

Required repair: Implement explicit root semantic validation and call it before using root authority; retain negative cases for weak thresholds, missing/duplicate/reused keys, keyId mismatch, active-role typed absence, and chaining bounds. Fix previousRootVersion to the chosen common range. The checker may be design evidence; do not equate mere JSON shape with trusted root admission.

## SEC2-M5 — Align cross-unit canonical and epoch field names

§2.1 domain table, §4.5 registry views, §5.1 trustEpoch

Registry-view digest uses opensip.metadata.registry-view.1 but the closed prose registry omits it (the helper contains it). trustEpoch uses catalogSnapshotVersion while lifecycle v2 uses indexSnapshotVersion.

Required repair: Add the registry-view domain to the normative closed table; align trustEpoch exact schema member with lifecycle, retaining an explicit catalog-snapshot meaning. Update numeric text to distinguish journal uint53 seq from metadata i64.

All exact subject pins are retained in the companion JSON. Passing the retained examples does not settle these cross-contract or adversarial cases. G22 fixture union and remaining doctor/permission product-output joins require separate evidence before row application.
