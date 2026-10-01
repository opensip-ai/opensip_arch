"""Build inventory119 by adding exactly the fifty-two X3d-1 rows (law X3d r6
items 1 to 4, 7, 8 and 13: the security side of the commit facade; law X8 r3
item 3's owner rows for the session types) to the inventory the real product
lock selects, and write its successor record. The parent follows the lock:
inventory113 (unit X4B-a, selected at product 0fc8ea2). It projects the
sixteen rows inherited through the parent. Run with python3 -I -B from any
directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It writes only its own two paths, refuses to write over any path git
already tracks, and refuses while a lock selects inventory119. It was first
written on inventory116 at a34dc6b, then rebased onto 0fc8ea2 (inventory113)
before any review; PRIOR maps both parents."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v119.json'
RECORD = M + 'commit-session-x3d1-inventory-v119/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v116.json': (M + 'live-guards-x4a-inventory-v116/successor.json', 'inventory116', 'X4a'),
    M + 'repository-file-inventory.v113.json': (M + 'trust-bootstrap-x4ba-inventory-v113/successor.json', 'inventory113', 'X4B-a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory119 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
# Law X8 r3 item 3's owner rows for unit X3d-1: (file, group, what the case
# pins, the expected code or none, rustc 1.95.0's message fragment).
CASES = [
    ["security_commit_session_literal.rs", "D", "CommitSession cannot be forged as a struct literal", "none", "cannot construct `CommitSession` with struct literal syntax due to private fields"],
    ["security_commit_session_default.rs", "D", "CommitSession has no Default", "E0277", "the trait bound `CommitSession: Default` is not satisfied"],
    ["security_commit_session_deserialize.rs", "D", "CommitSession cannot be deserialized", "E0277", "the trait bound `CommitSession: serde::Deserialize<'de>` is not satisfied"],
    ["security_commit_session_clone.rs", "E", "CommitSession cannot be cloned", "E0277", "the trait bound `CommitSession: Clone` is not satisfied"],
    ["security_commit_session_serialize.rs", "G", "CommitSession cannot be serialized", "E0277", "the trait bound `CommitSession: serde::Serialize` is not satisfied"],
    ["security_journal_write_txn_literal.rs", "D", "JournalWriteTxn cannot be forged as a struct literal", "none", "cannot construct `JournalWriteTxn` with struct literal syntax due to private fields"],
    ["security_journal_write_txn_default.rs", "D", "JournalWriteTxn has no Default", "E0277", "the trait bound `JournalWriteTxn: Default` is not satisfied"],
    ["security_journal_write_txn_deserialize.rs", "D", "JournalWriteTxn cannot be deserialized", "E0277", "the trait bound `JournalWriteTxn: serde::Deserialize<'de>` is not satisfied"],
    ["security_journal_write_txn_clone.rs", "E", "JournalWriteTxn cannot be cloned", "E0277", "the trait bound `JournalWriteTxn: Clone` is not satisfied"],
    ["security_journal_write_txn_serialize.rs", "G", "JournalWriteTxn cannot be serialized", "E0277", "the trait bound `JournalWriteTxn: serde::Serialize` is not satisfied"],
    ["security_journal_seal_binding_literal.rs", "D", "JournalSealBinding cannot be forged as a struct literal", "none", "cannot construct `JournalSealBinding` with struct literal syntax due to private fields"],
    ["security_journal_seal_binding_default.rs", "D", "JournalSealBinding has no Default", "E0277", "the trait bound `JournalSealBinding: Default` is not satisfied"],
    ["security_journal_seal_binding_deserialize.rs", "D", "JournalSealBinding cannot be deserialized", "E0277", "the trait bound `JournalSealBinding: serde::Deserialize<'de>` is not satisfied"],
    ["security_journal_seal_binding_clone.rs", "E", "JournalSealBinding cannot be cloned", "E0277", "the trait bound `JournalSealBinding: Clone` is not satisfied"],
    ["security_journal_seal_binding_serialize.rs", "G", "JournalSealBinding cannot be serialized", "E0277", "the trait bound `JournalSealBinding: serde::Serialize` is not satisfied"],
    ["security_stopped_session_literal.rs", "D", "StoppedSession cannot be forged as a struct literal", "none", "cannot construct `StoppedSession` with struct literal syntax due to private fields"],
    ["security_stopped_session_default.rs", "D", "StoppedSession has no Default", "E0277", "the trait bound `StoppedSession: Default` is not satisfied"],
    ["security_stopped_session_deserialize.rs", "D", "StoppedSession cannot be deserialized", "E0277", "the trait bound `StoppedSession: serde::Deserialize<'de>` is not satisfied"],
    ["security_stopped_session_clone.rs", "E", "StoppedSession cannot be cloned", "E0277", "the trait bound `StoppedSession: Clone` is not satisfied"],
    ["security_stopped_session_serialize.rs", "G", "StoppedSession cannot be serialized", "E0277", "the trait bound `StoppedSession: serde::Serialize` is not satisfied"],
    ["security_project_operation_literal.rs", "D", "ProjectOperation cannot be forged as a struct literal", "none", "cannot construct `ProjectOperation` with struct literal syntax due to private fields"],
    ["security_project_operation_default.rs", "D", "ProjectOperation has no Default", "E0277", "the trait bound `ProjectOperation: Default` is not satisfied"],
    ["security_project_operation_deserialize.rs", "D", "ProjectOperation cannot be deserialized", "E0277", "the trait bound `ProjectOperation: serde::Deserialize<'de>` is not satisfied"],
    ["security_project_operation_clone.rs", "E", "ProjectOperation cannot be cloned", "E0277", "the trait bound `ProjectOperation: Clone` is not satisfied"],
    ["security_project_operation_serialize.rs", "G", "ProjectOperation cannot be serialized", "E0277", "the trait bound `ProjectOperation: serde::Serialize` is not satisfied"],
    ["security_project_operation_open_twice.rs", "E", "one ProjectOperation opens one CommitSession (open consumes it)", "E0382", "use of moved value: `operation`"],
    ["security_commit_session_reused.rs", "E", "a CommitSession consumed by begin_journal_txn cannot be reused", "E0382", "use of moved value: `session`"],
    ["security_journal_write_txn_reused.rs", "E", "JournalWriteTxn's consuming abort runs once", "E0382", "use of moved value: `txn`"],
    ["security_stopped_session_finish_twice.rs", "E", "StoppedSession::finish consumes it, so the end path runs once", "E0382", "use of moved value: `stopped`"],
    ["security_commit_session_open_arity.rs", "F", "no caller-chosen ExecutionId: CommitSession::open takes the operation alone", "E0061", "this function takes 1 argument but 2 arguments were supplied"],
    ["security_ordinary_writer_unnameable.rs", "F", "the cfg(test) begin_operation_with that returns a ProjectOperation lives on the unnameable OrdinaryWriteAdmission", "E0603", "module `custody` is private"],
    ["security_project_operation_binding_private.rs", "F", "ProjectOperation's non-public binding is unreachable outside security (item 3a's census)", "E0624", "method `binding` is private"],
    ["security_project_operation_row_private.rs", "F", "ProjectOperation's non-public row is unreachable outside security (item 3a's census)", "E0624", "method `row` is private"],
    ["security_project_operation_mode_private.rs", "F", "ProjectOperation's non-public mode is unreachable outside security (item 3a's census)", "E0624", "method `mode` is private"],
    ["security_project_operation_subject_private.rs", "F", "ProjectOperation's non-public subject is unreachable outside security (item 3a's census)", "E0624", "method `subject` is private"],
    ["security_project_operation_endpoint_private.rs", "F", "ProjectOperation's non-public endpoint is unreachable outside security (item 3a's census)", "E0624", "method `endpoint` is private"],
    ["security_project_operation_required_private.rs", "F", "ProjectOperation's non-public required is unreachable outside security (item 3a's census)", "E0624", "method `required` is private"],
    ["security_project_operation_selected_core_private.rs", "F", "ProjectOperation's non-public selected_core is unreachable outside security (item 3a's census)", "E0624", "method `selected_core` is private"],
    ["security_project_operation_carrier_private.rs", "F", "ProjectOperation's non-public carrier is unreachable outside security (item 3a's census)", "E0624", "method `carrier` is private"],
    ["security_project_operation_guard_private.rs", "F", "ProjectOperation's non-public guard is unreachable outside security (item 3a's census)", "E0624", "method `guard` is private"],
    ["security_project_operation_attempt_closed_private.rs", "F", "ProjectOperation's non-public attempt_closed is unreachable outside security (item 3a's census)", "E0624", "method `attempt_closed` is private"],
    ["security_project_operation_charge_private.rs", "F", "ProjectOperation's non-public charge is unreachable outside security (item 3a's census)", "E0624", "method `charge` is private"],
    ["security_project_operation_reserve_end_path_settlement_private.rs", "F", "ProjectOperation's non-public reserve_end_path_settlement is unreachable outside security (item 3a's census)", "E0624", "method `reserve_end_path_settlement` is private"],
    ["security_project_operation_settle_end_path_private.rs", "F", "ProjectOperation's non-public settle_end_path is unreachable outside security (item 3a's census)", "E0624", "method `settle_end_path` is private"],
    ["security_project_operation_journal_private.rs", "F", "ProjectOperation's non-public journal is unreachable outside security (item 3a's census)", "E0624", "method `journal` is private"],
    ["security_project_operation_end_private.rs", "F", "ProjectOperation's non-public end is unreachable outside security (item 3a's census)", "E0624", "method `end` is private"],
    ["security_project_operation_end_with_private.rs", "F", "ProjectOperation's non-public end_with is unreachable outside security (item 3a's census)", "E0624", "method `end_with` is private"],
    ["security_project_operation_lease_mut_private.rs", "F", "ProjectOperation's non-public lease_mut is unreachable outside security (item 3a's census)", "E0599", "no method named `lease_mut` found for struct `ProjectOperation`"],
    ["security_project_operation_carrier_mut_private.rs", "F", "ProjectOperation's non-public carrier_mut is unreachable outside security (item 3a's census)", "E0599", "no method named `carrier_mut` found for struct `ProjectOperation`"],
    ["security_project_operation_attempt_used_private.rs", "F", "ProjectOperation's non-public attempt_used is unreachable outside security (item 3a's census)", "E0599", "no method named `attempt_used` found for struct `ProjectOperation`"]
]
def case_row(file, group, what, code, fragment):
    reason = f'exactly one error without a code, {fragment}' if code == 'none' else f'exactly one error, {code}, {fragment}'
    return row('crates/host/tests/refusal/cases/' + file, 'opensip-host', 'fixture',
        f"Compile-fail case for law X8 r3 (unit X3d-1), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with {reason}; group {group}: {what}. Synthetic; no compiler qualification.")
ADDED = [
    row('crates/security/src/custody/commit_session.rs', 'opensip-security', 'composition',
        "The security side of the CommitSession storage facade (law X3d r6 items 1 to 4, 7, 8 and 9; unit X3d-1, with X4c's end path merged), custody.rs's macOS module beside X2e's operation_handoff and X4a's operation_guard. CommitSession::open consumes one ProjectOperation, draws the ExecutionId (exec1_) and the operationRef (op-) from 16 host-CSPRNG bytes each on the write receipt's attempt ledger (law X9 r1's x3d.session.execution-draw draw point), and binds N, (S, G, K), the carrier digest SHA-256(N) and the receipt's selected core closure, with a read-only execution_id. reserve_end_path is item 3 step 0: the attempt ledger's one settlement reserve (X3d-0), taken through the attempt, write receipt and operation (one production caller each, source-pinned), sized exactly at one REV and one CLN append at their bounded maximum bodies by X3b-2's own cost functions (writer open, witness read and append cost at the largest generation and the last ordinary sequence, with no literal), held only in a private end-path value. capacity is item 3 step 3 over seal_fits on the tail the start proved. begin_journal_txn takes the journal's level 3 (refusing a session without the reserve) and JournalWriteTxn keeps it detached across storage's evidence-ledger BEGIN IMMEDIATE, with a consuming abort. seal_under_append_lock runs item 4 step 3 with the security-owned two-phase adapter traits (CommitAdapter staging, StagedCommit COMMIT, EvidenceCommit) inside one attempt-ledger charge: level 4, X4's checkpoint, the SEAL built and bound to the caller's ReplayedRun through PreparedJournalSeal, its witnessed append, the repeated checkpoint, staging, the final checkpoint ending in FinalGate::admit, the evidence COMMIT only through the one AdmissionPermit, level 4's release; a certain stop rolls the evidence transaction back, then releases level 4 and any journal level 3, appends nothing and latches the gate; JournalSealBinding is read-only evidence of the SEAL. Every certain refusal before admission latches the operation's one gate (0 to 2). An uncertain journal commit or barrier, an undetermined attempt-admission COMMIT and an undetermined evidence COMMIT forfeit the reserve where classified. StoppedSession::finish owes a REV for a durable SEAL without its evidence commit, a latched gate or an observed revocation (reason from a closed set: trust-revoked, policy, observer-fail-stop, stale-guard, operation-stopped; no trustEpochObserved) and a CLN for F38's fixed residual pair, appends them in one settle of the reserve as fresh level-3-then-level-4 appends with no checkpoint, each refused on the invariant row before any effect if its draft exceeds its kind's body bound, stopping at the first failure (no CLN after a failed REV), then releases the lease and runs X3b's end step unless an outcome was uncertain or the attempt ledger is closed. SessionRefusal projects every composition row through InstallationTermination. It places law X9 r1's x3d.session, x3d.publish (after-staging, before-final-checkpoint, commit-returned) and x3d.finish (settle.before, settle.after) points. Library only: no command commits."),
    row('crates/security/src/custody/commit_session_tests.rs', 'opensip-security', 'test',
        "Check X3d-1 through X2e's real handoff on scratch homes (a creator-published P0 with X4T-0's signed accepted store, ordinary writers over 462's signed test trees, a scripted monitor clock, observer ticks on request, a test adapter standing in for storage's staging and COMMIT; no real home or installation), included under operation_handoff_tests.rs's cfg(test) module: open's ids, grammar and binding; a lawful commit appending one SEAL, no REV or CLN, and the end step copying the floor; after each certain refusal that closes the attempt ledger (a publication-reserve overrun, busy at the evidence ledger's BEGIN IMMEDIATE with the consuming abort, a staging I/O error, a failed final checkpoint on a stall), the REV (and the CLN after a durable SEAL) appended from the settlement with its closed reason and the end step taking no fence; a busy carrier failing the REV, with no CLN and the busy row disclosed; a refused step 0 holding no reserve and appending nothing; an unfunded journal transaction and a second reserve on the invariant row; nothing appended and no end step after an uncertain SEAL commit, an undetermined evidence COMMIT and an undetermined attempt admission; an exhausted generation returned with the ledger open and rolled over; the reserve equal to one bounded REV and one bounded CLN, the closed reasons, and a draft one byte over its bound refused; a real REV and CLN at the last two ordinary slots charging exactly the cost function; the settlement chain's single production caller per link; and the x3d crash points' names."),
] + [case_row(*c) for c in CASES]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive commit-session security layout (law X3d r6, unit X3d-1, with law X8 r3 item 3 owner rows); library only, nothing commits; no release, custody, profile, boot or creator qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + len(ADDED)
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / prior_path).read_bytes())
assert prior['candidate'] == parent, f'{parent_name} is not the selected {parent_unit} candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive commit-session security layout (law X3d r6, unit X3d-1, with law X8 r3 item 3 owner rows); independent review and lead assent required',
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
