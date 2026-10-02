"""Build inventory127 by adding exactly the six X6c rows (law X6 r3 item 7
and item 12's X6c list, under commit-recovery-readonly.v3.md section 4 and
F53: security's custody half of the authorized settlement sweep, storage's
sweep step and its one settle write in ledger_store, and the host's store-gc
per-namespace step's tests, with law X9 r2 item 5's x6.sweep after-exclusive,
after-snapshot and settle.commit points) to the inventory the real product
lock selects, and write its successor record. The host step itself is the
already planned crates/host/src/maintenance.rs row, which this successor
keeps by value. The parent follows the lock: inventory126 (unit X6b,
selected at product f880145, with D1's thirty-nine overrides and D2's four
supersessions already folded into its projection). It projects the
fifty-five rows inherited through the parent. Run with python3 -I -B from
any directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It writes only its own two paths, refuses to write over any path git
already tracks, and refuses while a lock selects inventory127."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v127.json'
RECORD = M + 'settlement-sweep-x6c-inventory-v127/successor.json'
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v126.json': (M + 'recovery-admission-x6b-inventory-v126/successor.json', 'inventory126', 'X6b'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory127 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/settlement_sweep.rs', 'opensip-security', 'composition',
        "The custody half of the authorized settlement sweep (law X6 r3 items 1 and 7 under commit-recovery-readonly.v3.md section 4 and F53; unit X6c), custody.rs's macOS module, consumed by storage's settle step and the host's store-gc step. SettlementSweep::admit is X1's admit_ordinary_writer (the process's one write receipt and the 468 gate, which holds the installation fence), then, on the gate's ledger with the gate's and the receipt's rechecks under the held fence: X3a's selected endpoint joined from the gate's one read (S, G and K), I/stores/S confirmed against the endpoint's admitted marker, and the registry's one bounded capture (X2b), from which every namespace held by exactly one row, that row ACTIVE, is listed, sorted. It takes no trust admission, X4 guard, operation, session, grant or ExecutionId (X1 item 4; X9 r2 gap G5's narrowest reading). lease takes X2 item 7's EXCLUSIVE for one listed N under the held fence as one fenced step built from X2d's own primitives (I/host, projects and N confirmed private, both carriers judged, then writer.lease and readers.lease each LOCK_EX|LOCK_NB with their bindings and the directories rechecked, as one reserved effect), and places law X9's x6.sweep after-exclusive point. A held lock is SweepLeaseRefusal::Busy with no lock left held and nothing latched (skip and retain, never refuse); an unlisted N is the invariant row; any other refusal is its X2 item 8 row and spends the gate. SweepLease lends the admitted N, S, G, K and SHA-256(N), I/stores/S and its own failure-latching ledger at the owner's caps (charge_store), so a refusal inside one namespace never closes the sweep; it borrows the sweep mutably, so one namespace is leased at a time, and dropping it releases readers.lease then writer.lease. release unlocks the fence last. It reads and writes no ledger, journal, witness, floor or trust record. Library only."),
    row('crates/security/src/custody/settlement_sweep_tests.rs', 'opensip-security', 'test',
        "Check X6c's custody half (law X6 r3 item 7), included as settlement_sweep.rs's cfg(test) module, on scratch homes with a P0 published by the real creator and projects registered by ordinary writers that then released their fence: the sweep holds the installation fence throughout, lists the ACTIVE namespaces sorted, admits the endpoint's S and I/stores/S, leases each N EXCLUSIVE (both carriers held against shared and exclusive takers) with a fresh empty ledger, releases each lease before the next and the fence last, and writes nothing under I; an APPEND-WRITE or SHARED-READ holder makes N busy with no lock left held while the next namespace still leases; an unlisted N is the invariant row and a missing lease file X2's incomplete row, after which the spent gate refuses every later lease while the fence is still released last; an installation without projects lists nothing; a held fence refuses on the gate's busy row; an accepted view revoking the running core's own closure does not refuse the sweep (gap G5); and source pins that the module takes no trust admission, guard, operation, session, grant, ExecutionId, wait, shared lock or write, calls admit_ordinary_writer once, locks writer.lease before readers.lease, both exclusive, and places after-exclusive once after the fenced lease."),
    row('crates/storage/src/sweep.rs', 'opensip-storage', 'service',
        "Storage's step of the authorized settlement sweep for one namespace (law X6 r3 item 7, owner section 4.2 and 4.3, F53; unit X6c), lib.rs's macOS module, over security's SweepLease (the installation fence and N's EXCLUSIVE lease held) and on its ledger. sweep_namespace takes one coherent ledger snapshot of the admitted binding's (the digest of N, S, G and K) admitted attempts with read_sweep_ledger, places law X9's x6.sweep after-snapshot point, and then settles each decided attempt in ExecutionId order in its own single-statement transaction (settle_attempt): refused when neither receipt nor association is present (crashed, an orphan SEAL, durability uncertainty), committed when both are present and joined, and nothing for a one-sided, contradictory, foreign-binding or impossible standing, each reported by ExecutionId and reason. The first settle that finds the ledger busy, unreadable or undetermined, or a ledger budget refusal, ends the namespace's writes and is reported. NamespaceSweep is the closed outcome: NoLedger (projects, N or the ledger positively absent: no row to settle), Unreadable (host I/O), Busy (skip and retain), Budget, or Swept with settled, left, more and stopped. It writes nothing but the settle transition, reuses no dead attempt's authority, obtains no grant and never retries a commit. Library only."),
    row('crates/storage/src/sweep_tests.rs', 'opensip-storage', 'test',
        "Check X6c's storage step without a lease (storage cannot build security's SweepLease; X9 composes the two in fresh processes), included as commit_tests.rs's child module so that sweep_from runs over scratch I/stores/S stores that X3d-2's own storage steps committed into, read back by recovery's recover_from: a committed-but-unsettled attempt settled committed and a crashed one settled refused, with no receipt, association or object written, the reader moving from committed-historically with pending settlement and unknown-attempt-open to committed-historically without it and terminal-not-committed, and a second sweep listing and writing nothing; a one-sided ledger (receipt or association removed behind its reinstalled trigger, X9's F23 mutation) reported one-sided and left admitted while the crashed attempt beside it settles; a missing projects directory or ledger file no ledger, a non-database, a drifted schema and a non-private ledger file unreadable with nothing written; a foreign holder of the ledger's write lock stopping the namespace busy with every row left admitted until the next sweep settles each once; an admitted row under another binding never listed; a short ledger the budget row with nothing written; and source pins that the sweep's only write is the one settle UPDATE in ledger_store, guarded on admitted and never undetermined, called only from sweep_settle.rs, and that sweep.rs and sweep_settle.rs hold no other SQL write, staging, publication, creation, barrier, SEAL, witness, sleep or retry and place after-snapshot once between the snapshot and the first settle and settle.commit once after the settle statement."),
    row('crates/storage/src/ledger_store/sweep_settle.rs', 'opensip-storage', 'store',
        "The authorized settlement sweep's ledger work for one namespace (law X6 r3 item 7, owner section 4.3 steps 2 and 4; unit X6c), project_ledger.rs's child module sweep_settle, under security's SweepLease and on its ledger. read_sweep_ledger admits projects and N only if present (no creation, no barrier), observes the ledger's name, opens it as a judged private file and charges the snapshot before opening exactly one ReadSnapshot (read-only, busy handler off) that must name the same file and hold exactly the selected schema; inside it, it lists the admitted binding's admitted attempt rows in ExecutionId order (at most 4096, observing more) and for each reads the receipt, the association and the attempt row together, its bodies charged as read, deciding owner section 4.2 through join_ledger: committed for a joined pair, refused for neither, and no write for one-sided, contradiction, binding-unusable or invariant. A positively absent directory or ledger is Missing, a busy one Busy and anything else unreadable; none is settled. settle_attempt, for one decided attempt, rechecks the file's identity, opens the existing writer and verifies the selected schema, then runs one BEGIN IMMEDIATE transaction holding exactly one statement, ledger_store's settle_admitted_attempt, and commits it under the ledger's own durability at law X9's fallible x6.sweep settle.commit point: settled, unchanged (rolled back), busy, unreadable, or undetermined (a failed COMMIT, never retried). It writes nothing else."),
    row('crates/host/src/maintenance_tests.rs', 'opensip-host', 'test',
        "Check X6c's store-gc settlement step (law X6 r3 items 7 and 8), included as maintenance.rs's cfg(test) module, over a scripted sweep that logs its calls (the host cannot build security's sweep; X9-5 runs F53's store-gc step in fresh processes): every listed namespace in order, a busy lease skipped and retained and an unreadable ledger reported host I/O while the sweep continues, the fence released last; a lease refusal ending the sweep on its row with the fence still released, and a failed release the host I/O row unless a row already ended the sweep; item 8's per-namespace rows exhaustively (no row for skipped, no ledger, busy or a clean sweep; host I/O for unreadable; the budget row; DURABILITY.COMMIT_FAILED for an undetermined settle); and a source pin that the step admits once, holds each lease only inside its storage step and drops it before the next, releases after the loop, and names no recovery, commit facade, direct writer admission, MIGRATION.CORRUPT, sleep or retry."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive authorized settlement sweep layout (law X6 r3 item 7, unit X6c); library only, no command sweeps; no release, custody, profile, boot or creator qualification'
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
# inventory126 as plain inheritance rows, so none is left to fold on that
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
    'standing': 'PROPOSED additive authorized settlement sweep layout (law X6 r3 item 7, unit X6c); independent review and lead assent required',
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
