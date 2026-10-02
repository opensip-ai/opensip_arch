"""Build inventory126 by adding exactly the eight X6b rows (law X6 r3 items
1 to 6, 8 and 12's X6b list: security's read-only recovery admission and the
recovery-side carrier location, storage's recover and RecoveredCommit with
its read-only ledger snapshot and object reads, and the host's read-entry
route, with law X9 r1 item 5's x6.recover after-lease and
after-ledger-snapshot points) to the inventory the real product lock
selects, and write its successor record. The parent follows the lock:
inventory125 (unit X7a, selected at product f097c5b, with D1's thirty-nine
overrides and D2's four supersessions already folded into its projection).
It projects the fifty-five rows inherited through the parent. Run with
python3 -I -B from any directory. Deterministic for a given lock: rerunning
reproduces the same bytes. It writes only its own two paths, refuses to
write over any path git already tracks, and refuses while a lock selects
inventory126."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v126.json'
RECORD = M + 'recovery-admission-x6b-inventory-v126/successor.json'
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v125.json': (M + 'finalization-x7a-inventory-v125/successor.json', 'inventory125', 'X7a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory126 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/recovery_admission.rs', 'opensip-security', 'composition',
        "Read-only recovery's admission (law X6 r3 items 1 to 3 with law X2 r8 item 7's r6 exception; unit X6b), custody.rs's macOS module: the custody half that storage's recover consumes. RequestedBinding (storeGenerationDigest, namespaceId, journalCarrierDigest, operationRef, each in its closed grammar; inert) and RecoveryRequest (plain: an ExecutionId and the namespace that selects N; for_binding: an ExecutionId and F34's requested binding) are public values. RecoveryAdmission::admit is one of X1 item 7's read entries: it produces the process's one read receipt (458c-a) and then, on recovery's own failure-latching ledger at the owner's caps (one per process; a second allocation is the invariant row), runs 458c's charged retained walk from the root to I without its fence step (the fence is neither opened nor waited on), reads through the retained I the registry (X2b's single bounded capture) and X3a's endpoint members (pair, marker, state.v1 and node chain) by installation_session's member reads without the fence member, admits the endpoint against the receipt's selected core, and takes N only from the one ACTIVE registry row the request's namespace selects (no row, another state or several rows is NamespaceUnregistered, before any lease) and S, G and K only from the endpoint. It confirms I/stores/S against the endpoint's admitted marker and I/trust, then takes N's readers.lease LOCK_SH|LOCK_NB without the fence through recovery_shared_lease, built from X2d's own carrier, lock and recheck primitives (writer.lease is never opened; an EXCLUSIVE holder is UnavailableBusy), places law X9 r1's x6.recover after-lease point, and rechecks every captured sample and N's spelling once: any change is UnavailableBusy, never a conclusion. Other refusals take their 458c, 468c item 6 or X2 item 8 rows, the budget its row. The admission lends recovery's ledger (charge, and charge_store with the admitted I/stores/S, its spelling and the user) and X6a's capture at the recovered location (capture_carrier, through CarrierLocation::recovered from its RecoveryPlace), returning the public CarrierObservation. Not Clone; dropping it releases the lease. It writes, upgrades, allocates and waits on nothing. Library only."),
    row('crates/security/src/custody/recovery_admission_tests.rs', 'opensip-security', 'test',
        "Check X6b's admission (law X6 r3 items 2 and 3, X2 r8 item 7's exception), included as recovery_admission.rs's cfg(test) module, on scratch homes with a P0 published by the real creator, X4T-0's accepted trust, and a project registered by an ordinary writer that then released its fence: the request's and the binding's closed grammars; one recovery ledger per process; N from the ACTIVE row, S, G, K, the carrier digest SHA-256(N) and I/stores/S's spelling admitted while another holder keeps the installation fence for the whole admission, readers.lease held shared and writer.lease untouched at after-lease, the lease released on drop and every file under I byte- and time-identical; an unregistered namespace refused before any lease; an EXCLUSIVE holder unavailable-busy while an APPEND-WRITE holder (F29) admits beside it; a changed registry, selection pair or store marker sample at after-lease unavailable-busy; an absent I not initialized; a short ledger on the budget row; the carrier captured at the recovered location (another carrier refused with no capture, a registered N without a carrier unknown custody from one capture, a query outside its representation refused) with nothing written; and source pins that the module holds no fence, wait, writer lease, exclusive lock, creation, publication, rename, sleep or SQL write, places after-lease once, and that the shared lease and the fence-free member read are as stated."),
    row('crates/security/src/journal_store/recovery_location.rs', 'opensip-security', 'adapter',
        "The recovery side of X6a's carrier capture (law X6 r3 items 1 and 12; unit X6b), carrier_floor.rs's macOS child module recovery_location: CarrierLocation::recovered, the recovery-side location constructor, built only from the RecoveryPlace a recovery admission confirmed (I/trust, N, N's spelling and id, the user), and CarrierObservation with CarrierKind, the public inert view of the capture's standing for storage's recover: its kind, anchor class, would-write diagnosis, typed unknown or quarantine reason (operational record only, never a public detail), the offending digest, the interior-bodies-not-authenticated limitation of a confirmation, and the capture count. Private fields; only the admission returns one. It reads, writes and locks nothing."),
    row('crates/storage/src/recover.rs', 'opensip-storage', 'service',
        "Storage's recover and RecoveredCommit (law X6 r3 items 2, 4, 5, 6 and 8; unit X6b), lib.rs's macOS module. RecoveredCommit is exactly section 1's standings, each variant non_exhaustive so only storage constructs one: committed-historically (RunId, pendingSettlement, legacyCustodyUnknown, the anchor class and any would-write diagnosis), committed-availability-degraded (the same with each unavailable committed object's raw SHA-256 name and evidence.missing, evidence.corrupt, evidence.purged or evidence.expired), terminal-not-committed, unknown-attempt-open, unknown-attempt-unobserved, unknown-custody with its typed reason, unknown-quarantine-condition, unavailable-busy, binding-unusable with its typed subject and unknown-carrier-incompatible; standing gives the owner's spelling and limitation interior-bodies-not-authenticated on a confirmation. recover consumes a RecoveryAdmission and, on recovery's ledger: one coherent ledger snapshot at the admitted digest of (N, S, G, K), N, SHA-256(N) and the ExecutionId (read_recovery_ledger), with law X9 r1's x6.recover after-ledger-snapshot point after it; a missing, refused or unreadable ledger is unknown custody and a busy one unavailable-busy, never absence; F34's requested binding compared member by member with the admitted binding and the snapshot's attempt row (store-generation, namespace, carrier, operation; no attempt row is operation); the settlement matrix by join_ledger in that snapshot; a joined receipt without its Run material row is unknown custody; then X6a's capture through the admission, each carrier standing mapped to its own; then, for a confirmation, every committed object (the inventory's H digests and raw blob digests) read and hashed, a missing one evidence.missing (evidence.purged or evidence.expired under a purged or expired availability record), any other failure evidence.corrupt. A budget refusal is RecoveryFailure on the budget row, never a standing. It writes, settles, locks, waits and repairs nothing. Library only."),
    row('crates/storage/src/recover_tests.rs', 'opensip-storage', 'test',
        "Check X6b's storage half without an admission (storage cannot build security's RecoveryAdmission; X9 composes the two in fresh processes), included as commit_tests.rs's child module so that it runs recover_from over scratch I/stores/S stores that X3d-2's own storage steps committed into, with a scripted carrier verdict, checking every time that recovery leaves the ledger bytes unchanged: a confirmed commit committed-historically with pending settlement disclosed, then without it once settled committed, and the carrier asked exactly the association's carrier half; the settlement matrix (admitted with no receipt unknown-attempt-open and no row unknown-attempt-unobserved, both without asking the carrier; settled refused with both absent the only negative; settled committed without a receipt and settled refused beside one unknown custody); each carrier verdict its own standing, a budget refusal RecoveryFailure; F34's requested binding equal giving the standing and differing in operation, store generation, namespace or carrier, or with no attempt row, binding-unusable before the carrier is asked; no projects directory, a missing ledger file, a non-database and a drifted schema unknown custody; a deleted and a flipped committed object evidence.missing and evidence.corrupt in committed-availability-degraded, and evidence.purged under a purged availability generation; a short ledger the budget row; ExistingAttempt's requested binding equal to the plan's and refused on operation against another attempt; and source pins that recover.rs and recovery_read.rs hold no SQL write, transaction, creation, barrier, publication, settlement or sleep and place after-ledger-snapshot once, after the snapshot."),
    row('crates/storage/src/ledger_store/recovery_read.rs', 'opensip-storage', 'store',
        "Read-only recovery's ledger and object reads (law X6 r3 items 4 and 5; unit X6b), project_ledger.rs's child module recovery_read, under a recovery admission's custody of I/stores/S and on recovery's ledger. read_recovery_ledger admits projects and N only if present (security's admit_existing_store_directory: no creation, no barrier), observes the ledger's name, opens it as a judged private file, and charges one fixed snapshot cost before opening exactly one ReadSnapshot (read-only, busy handler off) that must name the same file and hold exactly the selected schema, then reads the receipt, association, attempt row, Run material, availability and pins together through the existing recovery_pins capture, returning values: the join_ledger standing, the attempt's operationRef, the association's carrier half and Run, the committed object and blob digests, and the stored availability state. A positively absent directory or ledger is Missing, an unreadable or drifted ledger Unreadable, a busy one Busy, and a refused directory or file ReadRefused, which closed the ledger; none is absence. check_objects reads each committed digest under objects/sha256 no-follow, requiring one regular file with one link whose bytes hash to its name, its length charged before its bytes. Nothing here writes."),
    row('crates/host/src/recovery_route.rs', 'opensip-host', 'composition',
        "The host's read-entry route for read-only recovery (law X6 r3 items 6 and 8; unit X6b), lib.rs's macOS module: route_recovery admits a RecoveryRequest through security's read entry, calls storage's recover once and projects the RecoveredCommit on item 8's rows with no new code: committed-historically and terminal-not-committed success; committed-availability-degraded success for history with each unavailable object's evidence detail disclosed, and required_object as the second projection for a selected operation that needs one (operational-failed, HOST.IO_FAILURE, host-io, that detail); unknown-attempt-open and unavailable-busy the busy row; unknown-attempt-unobserved, unknown-custody and unknown-carrier-incompatible the host I/O row; unknown-quarantine-condition LEDGER.CORRUPT with no detail; binding-unusable and an unregistered namespace request-rejected EXTENSION.ADMISSION_REJECTED RECOVERY.REFUSED with the subject; admission refusals and the budget their own rows. The match from RecoveredCommit has no wildcard. It is never called in a writer's invocation (X6 r3 item 6), and MIGRATION.CORRUPT is on no row. Library only: no CLI command calls it before X11."),
    row('crates/host/src/recovery_route_tests.rs', 'opensip-host', 'test',
        "Check X6b's host route (law X6 r3 item 8), included as recovery_route.rs's cfg(test) module: every standing's exact row (success, busy, host I/O, LEDGER.CORRUPT with no detail, RECOVERY.REFUSED with its subject); committed-availability-degraded success for history with its details, and the second projection for each of evidence.missing, corrupt, purged and expired, none for an available object; admission refusals on their rows, the unregistered namespace on RECOVERY.REFUSED and unavailable-busy on the busy row; and a source pin that the route makes one read entry and one recover, matches RecoveredCommit's ten variants with no wildcard, and names no MIGRATION.CORRUPT, commit facade or writer admission."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive read-only recovery admission, recover and route layout (law X6 r3, unit X6b); library only, nothing recovers from a command; no release, custody, profile, boot or creator qualification'
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
# The lock's inheritance rows bind exactly the prior record's projection to
# the parent; each is carried by stable file path to its new index.
bound = {json.dumps(o['selector'], sort_keys=True): o for o in lock['inventoryPassageInheritance']}
assert len(bound) == len(prior['descriptionOverrideProjection']) == 55
projection = []
for p in prior['descriptionOverrideProjection']:
    o = bound[json.dumps(p['candidateSelector'], sort_keys=True)]
    assert o['parent'] == parent and o['before'] == p['before'] and o['after'] == p['effectiveDescription'], p['filePath']
    i = int(p['candidateSelector']['jsonPointer'].split('/')[2])
    assert inherited['files'][i]['path'] == p['filePath'] and inherited['files'][i]['description'] == p['before'], p['filePath']
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
# Passage supersessions the lock binds on the parent (law VD1 item 3; D2's
# README, "After selection"): each ends the meaning its row's one inheritance
# entry carries. Fold each into that entry: the raw before stays, and the
# supersession's after becomes the effective description. The count stays 55.
# D2's four are on inventory122; X5a folded them, and the lock binds them to
# inventory125 as plain inheritance rows, so none is left to fold on that
# parent and D2's after text is checked instead.
by_selector = {json.dumps(p['parentSelector'], sort_keys=True): p for p in projection}
folded = 0
for binding in lock['contractSuccessors']:
    for s in json.loads((A / binding['record']['path']).read_bytes()).get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        p = by_selector[json.dumps(s['selector'], sort_keys=True)]
        assert s['before'] == p['effectiveDescription'], p['filePath']
        p['effectiveDescription'] = s['after']
        folded += 1
d2 = json.loads((A / M / 'description-batch-d2/successor.json').read_bytes())['passageSupersessions']
assert folded == (4 if parent == d2[0]['parent'] else 0), folded
effective = {p['filePath']: p['effectiveDescription'] for p in projection}
d2_rows = json.loads((A / d2[0]['parent']['path']).read_bytes())['files']
for s in d2:
    path = d2_rows[int(s['selector']['jsonPointer'].split('/')[2])]['path']
    assert effective[path] == s['after'], f'D2 must stay folded: {path}'
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 55
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive read-only recovery admission, recover and route layout (law X6 r3, unit X6b); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, all bound to {parent_name} by the lock, with contract successor D2\'s four passage supersessions folded in (their after text is the effective description). Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
