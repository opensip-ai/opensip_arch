"""Build inventory117 by adding exactly the 31 X8a fixture rows (law X8 r3
items 1 and 3, groups I, K and L, and the item 1e self-test; unit X8a) to the
inventory the real product lock selects, and write its successor record.
crates/host/tests/admission_tests.rs, the driver, already has its planned row
and keeps it by value. The parent follows the lock: inventory114 (unit X9-0,
selected at product daa7b01) when first built. The successor record bound to
the parent is the one the lock pins beside it, so a later parent (X4a's
inventory116, say) needs no edit here. It projects the sixteen rows inherited
through the parent. Run with python3 -I -B from any directory. Deterministic
for a given lock: rerunning reproduces the same bytes. It writes only its own
two paths, refuses to write over any path git already tracks, and refuses
while a lock selects inventory117."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v117.json'
RECORD = M + 'refusal-suite-x8a-inventory-v117/successor.json'
LOCK = Path('/Users/sb/code/opensip-ai/opensip/design-lock.json')
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory117 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
H = 'crates/host/tests/refusal/'
def fixture(name, description):
    return {'path': H + name, 'package': 'opensip-host', 'role': 'fixture', 'description': description, 'generated': False, 'standing': 'proposed'}
CASE = ("Compile-fail case for law X8 r3 (unit X8a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 "
        "against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and "
        "the misuse fails with exactly one error, ")
SELF = ("Must-reject driver self-test for law X8 r3 item 1e (unit X8a), compiled only by admission_tests.rs's driver, never a Cargo "
        "target. The driver fails if it passes, or if it is rejected for any reason other than ")
def case(name, pins):
    return fixture('cases/' + name, CASE + pins + '. Synthetic; no compiler qualification.')
def selftest(name, shape, reason):
    return fixture('selftest/' + name, SELF + reason + ': ' + shape + '.')
ADDED = [
    case('evaluator_admitted_pack_literal.rs', "E0451 naming AdmittedPack's four private fields on the literal's first field line; group L, ported from the AdmittedPack compile_fail doctest in crates/evaluator/src/policy.rs"),
    case('evaluator_capability_manifest_literal.rs', "E0451 naming CapabilityManifest's three private fields on the literal's first field line; group L, ported from the compile_fail doctest in crates/evaluator/src/capabilities.rs"),
    case('evaluator_replayed_bool.rs', 'E0308 mismatched types: a boolean verified (true) in place of ReplayedRun; group K, boolean verified'),
    case('evaluator_replayed_deserialize.rs', 'E0277, the trait bound ReplayedRun: serde::Deserialize is not satisfied, on serde_json::from_str::<ReplayedRun>; group K, serialized previous session'),
    case('evaluator_replayed_empty_literal.rs', 'no code, cannot construct ReplayedRun with struct literal syntax due to private fields, on an empty literal returned as a ReplayedRun; group K, forged receipt'),
    case('evaluator_replayed_literal.rs', 'no code, cannot construct ReplayedRun with struct literal syntax due to private fields, on the let-bound empty literal; group L, ported from the ReplayedRun compile_fail doctest in crates/evaluator/src/replay.rs'),
    case('evaluator_replayed_raw_json.rs', 'E0308 mismatched types: an opensip_identity::JsonValue in place of ReplayedRun; group K, raw DTO'),
    case('evaluator_replayed_retained_inputs.rs', "E0308 mismatched types: the inert RetainedInputs that replay_run reads, in place of ReplayedRun; group K, structural-only input"),
    case('platform_scope_replace.rs', "E0308 mismatched types: a helper's WorkScope replaced by a fresh WorkLedger; group L, ported from WorkLedger::scope's first compile_fail doctest in crates/platform/src/work_ledger.rs"),
    case('platform_scope_swap.rs', "E0521, borrowed data escapes outside of closure, as a second ledger's scope is donated out of its nested borrow; group L, ported from WorkLedger::scope's second compile_fail doctest, whose core::mem::swap yields two E0521 errors on 1.95.0, so the port keeps the one direction (the first of those errors)"),
    case('platform_settlement_clone.rs', 'E0599, no method named clone found for struct SettlementReserve; group L, ported from the SettlementReserve compile_fail doctests in crates/platform/src/work_ledger.rs'),
    case('platform_settlement_default.rs', 'E0599, no function or associated item named default found for struct SettlementReserve; group L, ported from the SettlementReserve doctests'),
    case('platform_settlement_literal.rs', "E0451 naming SettlementReserve's two private fields; group L, ported from the SettlementReserve doctests"),
    case('platform_settlement_reserve_in_postchecks.rs', 'E0599, no method named reserve_settlement on &mut ReservedPostchecks; group L, ported from the SettlementReserve doctests'),
    case('platform_settlement_reserve_in_scope.rs', 'E0599, no method named reserve_settlement on &mut WorkScope; group L, ported from the SettlementReserve doctests'),
    case('platform_settlement_settle_in_postchecks.rs', 'E0599, no method named settle on &mut ReservedPostchecks; group L, ported from the SettlementReserve doctests'),
    case('platform_settlement_settle_in_scope.rs', 'E0599, no method named settle on &mut WorkScope; group L, ported from the SettlementReserve doctests'),
    case('platform_settlement_settle_twice.rs', 'E0382, use of moved value: reserve, on a second settle; group L, ported from the SettlementReserve doctests'),
    case('security_fence_capture_after_drop.rs', "E0505, cannot move out of fence because it is borrowed, on dropping the InstallationReadFence before its capture's use; group L, ported from the compile_fail,E0505 doctest in crates/security/src/installation_observation.rs"),
    case('security_fence_capture_escape.rs', "E0515, cannot return value referencing function parameter fence, on a ProvisionalHeldFile<'static>; group L, ported from the compile_fail,E0515 doctest in crates/security/src/installation_observation.rs"),
    case('security_trust_session_after_drop.rs', 'E0505, cannot move out of fence because it is borrowed, on dropping the fence before NativeTrustReadSession::raw_current; group L, ported from the compile_fail,E0505 doctest in crates/security/src/trust/native_read_session.rs'),
    case('security_trust_session_escape.rs', "E0515, cannot return value referencing function parameter fence, on a NativeTrustReadSession<'static>; group L, ported from the compile_fail,E0515 doctest in crates/security/src/trust/native_read_session.rs"),
    case('storage_ledger_store_private.rs', "E0603, module ledger_store is private (storage's SQL connection, transaction handle and stage_recovery_pair); group I"),
    selftest('wrong_broken_control.rs', 'the lawful twin calls a ReplayedRun constructor that does not exist', 'a control that does not compile'),
    selftest('wrong_extra_error.rs', 'the intended private-field literal error together with an unrelated E0308', 'an error count other than one'),
    selftest('wrong_fragment.rs', "the right E0308 on the right line with a fragment naming another type", 'the wrong code or fragment'),
    selftest('wrong_line.rs', 'the intended error one line above the annotation', 'the wrong line'),
    selftest('wrong_none_for_coded.rs', 'none annotated where rustc emits E0308', 'the wrong code or fragment'),
    selftest('wrong_reason_typo.rs', 'a path typo failing with E0422 instead of the annotated private-field literal error', 'the wrong code or fragment'),
    selftest('wrong_two_annotations.rs', 'two annotations in one case', 'a malformed annotation'),
    selftest('wrong_vacuous_reference_clone.rs', '.clone() on &ReplayedRun, which compiles because shared references are Clone', 'an error count other than one'),
]
lock_row = lock['inventorySuccessors'][-1]
selected, prior_pin = lock_row['candidate'], lock_row['record']
parent = pin(selected['path'])
assert parent == selected, 'the selected inventory bytes differ from the lock'
assert pin(prior_pin['path']) == prior_pin, 'the selected successor record bytes differ from the lock'
prior = json.loads((A / prior_pin['path']).read_bytes())
assert prior['candidate'] == parent, 'the lock pins a record for another candidate'
parent_name = 'inventory' + Path(parent['path']).name.split('.v')[1].split('.')[0]
inherited = json.loads((A / parent['path']).read_bytes())
assert any(r['path'] == 'crates/host/tests/admission_tests.rs' for r in inherited['files']), 'the driver row must be inherited'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive opaque API refusal fixture layout (law X8 r3, unit X8a); test-only; no release, custody, profile, boot, creator or compiler qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + len(ADDED)
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive opaque API refusal fixture layout (law X8 r3, unit X8a); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all sixteen effective descriptions by stable file path from the rows bound to {parent_name}, which carries them unchanged from inventory81 onward. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
