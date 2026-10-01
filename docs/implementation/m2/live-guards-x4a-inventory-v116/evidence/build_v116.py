"""Build inventory116 by adding exactly the eight X4a rows (law X4 r7 items 2
to 8 and 11: the live security guards; law X8 r3 item 3 group D's three
unnameable cases) to the inventory the real product lock selects, and write
its successor record. The parent follows the lock: inventory117 (unit X8a,
selected at product c2352ae; first built on inventory114, unit X9-0, at
daa7b01, before any review). It projects the sixteen rows inherited
through the parent. Run with python3 -I -B from any
directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It writes only its own two paths, refuses to write over any path git
already tracks, and refuses while a lock selects inventory116."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v116.json'
RECORD = M + 'live-guards-x4a-inventory-v116/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v114.json': (M + 'crash-matrix-x90-inventory-v114/successor.json', 'inventory114', 'X9-0'),
    M + 'repository-file-inventory.v117.json': (M + 'refusal-suite-x8a-inventory-v117/successor.json', 'inventory117', 'X8a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory116 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/host/tests/refusal/cases/security_admission_permit_unnameable.rs', 'opensip-host', 'fixture',
        "Compile-fail case for law X8 r3 (unit X4a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with exactly one error, E0603, module commit_authority is private; group D's unnameable row for AdmissionPermit, the operation's one commit permit, crate-private per X3d r6 item 4 step 3.9 and X4 r7 item 3. Synthetic; no compiler qualification."),
    row('crates/host/tests/refusal/cases/security_final_gate_unnameable.rs', 'opensip-host', 'fixture',
        "Compile-fail case for law X8 r3 (unit X4a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with exactly one error, E0603, module commit_authority is private; group D's unnameable row for FinalGate, the operation's one gate, crate-private per X4 r7 items 2 and 3. Synthetic; no compiler qualification."),
    row('crates/host/tests/refusal/cases/security_operation_guard_unnameable.rs', 'opensip-host', 'fixture',
        "Compile-fail case for law X8 r3 (unit X4a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with exactly one error, E0603, module custody is private; group D's unnameable row for OperationGuard, the operation's live guard, crate-private per X4 r7 item 6. Synthetic; no compiler qualification."),
    row('crates/security/src/custody/operation_guard.rs', 'opensip-security', 'composition',
        "The live security guards of one ProjectOperation (law X4 r7 items 2 to 8; unit X4a), custody.rs's macOS module beside X2e's operation_handoff. LeaseFree creates the operation's one FinalGate (commit_authority's OperationGate, never reset) and its FreshnessMonitor first, at X2e's lease-free point under the held fence and before any lease, and runs the monitor's first read with the counter receiving that read's own opening sample (X4B r5 item 1). OperationGuard is built inside the handoff from that gate, monitor and admitted view with the trust store's retained handles, and moves into ProjectOperation, which starts its one observer thread: every 5 s (in tests, only on request) it performs one observation through the shared monitor, whose one history sits behind one mutex shared with every checkpoint so their reads serialize and a waiting read's wait is inside its bound; the observer never takes the fence, appends nothing, and charges only its own per-observation ledger; it stops when the guard is dropped. A revoking observation latches the gate with trust-revoked or policy; an unrelated update or a policy change keeping every required grant (none for any M2 writer) is recorded as drift; any other failure is a fail-stop. Checkpoint, lent by ProjectOperation::journal inside the write receipt's attempt-ledger charge and requiring a JournalAppendHeld borrow of the operation's own append lock (level 4), runs item 3's steps inside the x4.checkpoint scope: item 4's mandatory guard rechecks on the attempt ledger (the write receipt's actor, core and platform; the held lease by name binding and by a fresh nonblocking EXCLUSIVE probe on a new descriptor, a lost lock being S7's busy row; the original project root, .opensip and marker; the namespace; the store marker and lineage nodes by full sample; and the operation joins N, S, G, K and the append lock's N), the final monitored observation and S6's predicate against the immutable start epoch, the latch check, and the admission-boundary check (one clock sample, no I/O, boot unchanged, within 10 s of the final read's earliest instant), with the monitor held from the observation through admission; then FinalGate::admit binds the prepared value and mints the one AdmissionPermit (handing the value back on a refusal), or the effect's own intent append follows. Every failure latches the gate and records the first stop cause (revoked, fail-stop with its reason, or a stale guard with that guard's own row). trust_termination maps X4T r9 item 10's fenced admission rows onto new InstallationTermination variants on existing details. It places law X9 r1's points x4.observer.tick (a gate replacing the observer's timed wait when armed), x4.observer.after-observation and x4.checkpoint.before-observation, .after-observation and .before-admit. cfg(test) only: a scripted monotonic clock, a manual cadence and observer ticks on request. Library only."),
    row('crates/security/src/custody/operation_guard_tests.rs', 'opensip-security', 'test',
        "Check X4a's guard pieces with scripted clocks only: every fenced admission row's termination (including each root chain detail); each stop's row; the gate and monitor created first, the first read's opening sample, a counter refusal latching, and a first read longer than the bound stalling; the admission boundary admitting exactly 10 s and refusing 10 s plus 1 ns, a boot change, a sample before the read's end and a boundary with no read, each latching; one gate minting one permit, a second admission handing the prepared value back, and a late latch keeping the admitted result; the production observer period ticking on its timeout and stopping on its signal with no sleep; and a source pin of the x4 crash points' names."),
    row('crates/security/src/custody/operation_live_tests.rs', 'opensip-security', 'test',
        "Check X4a through X2e's real handoff on scratch homes (a creator-published P0 whose trust store is replaced by X4T-0's signed accepted store for the same S and K, ordinary writers over 462's signed test trees, a scripted monitor clock, observer ticks on request, other holders as flocks on separate descriptors; no real home or installation): the first read admitting the start view at the lease-free point and the write-ahead publication completing the handoff, then a tick with no drift; a P0 installation refusing TRUST.NO_ADMITTED_TIME_CONTEXT before any lease with nothing written; an effect checkpoint then its RA, the commit admission's one permit, a revoking tick after admission taking the gate from 1 to 3 without relabelling the admitted result, and a second admission refused; a pause beyond the bound after the first read fail-stopping before any effect and closing the attempt ledger; ticks and checkpoints sharing one history; a pause after the final observation failing the admission boundary; a boot change; another operation's level 4 refused as a broken caller; an unrelated revocation update continuing as drift while another holder keeps the fence; a revoking update latching through the observer and through the checkpoint's own observation; a newer view whose revocation body is missing failing unreadable, and a pointer back below the start view's counters failing as a rollback; a state.v1 replacement during the first attempt absorbed inside one monitored read and a second one failing as mixed; the stale guards (a lost lease lock on the busy row, a replaced lease file, a substituted marker, a replaced or missing store marker, a namespace no longer private, a substituted project root), each refusing before any effect on its own row; an unrelated registration not invalidating the operation; a repeated checkpoint after journal work latching on a guard gone stale; a read waiting on the shared monitor counting its wait; and the end path stopping the observer and releasing everything."),
    row('crates/security/src/trust/live_observation.rs', 'opensip-security', 'service',
        "The operation's trust side (law X4 r7 items 2, 4 and 5 over law X4T r9 items 7 to 9; unit X4a), as a macOS child of the current-trust admission. fenced_operation_read is the lease-free point's fenced first read: X4T-b's retained state.v1 owner bound to the write gate's one read (its bytes and sample, no new content read), X4T-b's fenced_first_read with its write-ahead and the S4 observation the caller projects from the monitor's opening sample, returning the view and any confirmed publication for the gate's advance_current; TrustInvocation is the floor publication's invocation identity (req1_ and exec1_ with 32 lowercase hex, a step id). RetainedTrustHandles retains trust/stores/S, its events, and objects, records and publications, each bound no-follow by exact name to its retained parent and judged private and on H's filesystem under the fence. LiveObservation is one unfenced observation through those handles only, on a fresh per-observation ledger of two views at TRUST_VIEW_COST (256 objects, 4096 edges, 224 MiB): state.v1 opened by name through the store handle, X4T-a's reread over the closure with every file opened by name through its collection's retained handle (the native readers' own locator), state.v1 reopened and its identity and full sample compared, and all of it once more if they differ; a second change is mixed. A reread refusal naming a revoked closure component is the revoking observation; any other refusal, an unreadable record, a budget overrun or a view below the start view's floors or counters (never reaching the predicate) is a fail-stop with its reason. Then S6's observe_revocation runs against the immutable start epoch and closure subjects (X4T item 4's components, from the start view), with empty required permission pairs. It never takes the fence, writes nothing and grants nothing. Library only."),
    row('crates/security/src/trust/live_observation_tests.rs', 'opensip-security', 'test',
        "Check X4a's trust side on scratch installations under the ACL test scratch with X4T-0's signed accepted store (no real home): the invocation identity grammar; the per-observation ledger at two views inside the owner's 256 MiB cap; a reread refusal classified as a revocation only for a revoked closure component, every other row a fail-stop with its reason; the retained handles judged when retained (a filesystem that is not H's, and a missing collection never created, are incomplete); and an observation through the handles with the fence released, admitted twice on fresh ledgers, then unreadable once a closure record is gone."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive live security guard layout (law X4 r7, unit X4a, with law X8 r3 group D); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive live security guard layout (law X4 r7, unit X4a, with law X8 r3 group D); independent review and lead assent required',
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
