"""Build inventory124 by adding exactly the two X6a rows (law X6 r2 items 1,
4, 10, 11 and 12's X6a list: security's read-only carrier recovery capture,
journal_store::recovery_capture, with law X9 r1 item 5's x6.recover bracket
points) to the inventory the real product lock selects, and write its
successor record. The parent follows the lock: inventory123 (unit X5a,
selected at product 54e6166, with D1's thirty-nine overrides and D2's four
supersessions already folded into its projection; inventory122 remains
admissible, and on it D2 is folded here). It projects the fifty-five rows
inherited through the parent. Run with python3 -I -B from any directory.
Deterministic for a given lock: rerunning reproduces the same bytes. It
writes only its own two paths, refuses to write over any path git already
tracks, and refuses while a lock selects inventory124."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v124.json'
RECORD = M + 'recovery-capture-x6a-inventory-v124/successor.json'
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v122.json': (M + 'commit-facade-x3d2-inventory-v122/successor.json', 'inventory122', 'X3d-2'),
    M + 'repository-file-inventory.v123.json': (M + 'replay-join-x5a-inventory-v123/successor.json', 'inventory123', 'X5a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory124 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/journal_store/recovery_capture.rs', 'opensip-security', 'validator',
        "Read-only carrier recovery capture (law X6 r2 items 1 and 4, commit-recovery-readonly.v3 steps 3 and 4 and its section 1 carrier precedence, adapted to X3b r10's generation succession; unit X6a), as carrier_floor.rs's macOS child module recovery_capture. recover_carrier takes the retained CarrierLocation, the association's carrier half (RecoveryQuery: journalCarrierDigest, grantGeneration, journalSeq, journalBodySha256, operationRef, runId, each in its closed representation) and the recovery's own WorkScope. An association naming another carrier than SHA-256(N) is BindingUnusable before any read. Otherwise each capture performs exactly W1 H1 J W2 H2: the witness, the floor under trust/carrier-floors (a present floors directory passing the private-directory check), one read-only journal snapshot (names-first dispatch, the format row and binding, the newest tail with the writers' predecessor check, the requested generation's count, tail and closure chain, the SEAL row) retained until the floor positions are read in it, then the witness and the floor; each read is charged before it runs and a budget failure is returned, never absence; X9's read-only x6.recover points after-w1, after-h1, after-j, after-w2, after-h2 and after-fresh-capture are placed between them. At most one fresh capture follows, so at most two journal snapshots and four witness and four floor reads. Precedence: a missing, emptied or fresh-install carrier is unknown custody and an unmigrated one is unknown-carrier-incompatible, from the names alone; an unlawful format-3 footprint, a violated boundary, a foreign format row, witness or floor, or a broken succession is a quarantine candidate, and the unpublished complete set over an inherited carrier is busy; an association below first_generation is incompatible; then shape (malformed witness or floor, a lost floor), the floor against item 4a's copy tail with the open-successor exception and floorOk at its own position, a generation pruned below a newer one (F28) as unknown custody, contiguity and a closed chain below the newest generation (every generation from the requested one up to the newest present, each ending in a TERMINAL on its highest-seq row), the F43 hazard (the F22 condition only for a floor in the requested generation at or above the requested sequence, carrying that floor's digest), and the full SEAL join (type, schema, stored and recomputed domain-framed digest, operationRef, body coordinates and run3 Run). The anchor follows item 4a's reconciliation of the newest tail: OK is witness-committed-tail, ADVANCE witness-pending-at-tail with witnessWouldAdvance, OPEN either with witnessWouldOpen, REVERT sc-trust-floor with witnessWouldRevert when the floor covers the requested record and its bracket is stable, otherwise the C-prime unknown, never invalidated; A and B need a stable witness bracket. Step 4: a quarantine condition (typed by X3b's kinds, binding, footprint or contiguity, with the offending bytes' digest) or the F22 hazard is reported only with stable witness and floor brackets and two agreeing journal tails, otherwise unavailable-busy. Every confirmation carries interior-bodies-not-authenticated. It writes nothing: no witness INIT, REVERT, ADVANCE or OPEN, no floor copy, no marker, no lock, no wait. The cfg(test) hook observes the named points only. X6b composes it with admission and the ledger snapshot; library only."),
    row('crates/security/src/journal_store/recovery_capture_tests.rs', 'opensip-security', 'test',
        "Check X6a (law X6 r2 item 11's carrier rows) on scratch installations with X3b's production creation, start and append paths, planting later generations, gaps and prunes with the lifted-and-reinstalled triggers: the query's closed representation; an association naming another carrier refused with no read and no charge; anchor A at several tails, B (F45) with witnessWouldAdvance, C with witnessWouldRevert, and C-prime (F44) with the floor below the record or INIT; every SEAL join member (Run, operationRef, digest, an RA row at k, a body that no longer hashes to its stored digest); the adverse witness rows (beyond the tail, equal sequence with another hash, non-adjacent PENDING, malformed (F20), a lower generation, missing (F21)) and floor rows (above the tail and equal sequence with another hash (F22), floorOk, malformed, lost, a missing floors directory), and a foreign witness or floor, each a quarantine only after two stable captures with the offending digest; unstable witness or floor brackets and disagreeing journal tails busy, never a quarantine; a lawful append between any two bracket reads (F49) confirming after the fresh capture, and an in-flight PENDING giving C or C-prime, never a quarantine, with nothing reverted; the F43 hazard busy, the F22 condition when the floor covers k, busy for a sequence above a closed generation's tail under the open-successor floor (G+1, 0, null), and the reconciling retry confirming; section 1's precedence (missing, emptied and fresh-install carriers as unknown custody and format 1 or 2 as incompatible whatever the witness, the {A, B} prefix busy, a partial or unpublished fresh footprint and a foreign format row as stable quarantines, busy when unstable, a migrated carrier's association below first_generation incompatible before a malformed witness and after a foreign one); X3b r10's succession (a SEAL in a closed generation anchored by the open successor with the floor at (G+1, 0, null) or still in G, case 1's REVERT, COMMITTED (G+1, n) as uncertainTailLoss, would-OPEN under OK and ADVANCE, a PENDING after a TERMINAL and a floor at (G+1, 0) against a witness naming G as quarantines, a later open generation anchoring an earlier SEAL, a witness naming a superseded generation); a broken succession, a generation gap, an intermediate generation holding a TERMINAL and then a later non-terminal row (a protocol violation, and a confirmation once that generation ends in its TERMINAL), and a sequence gap; F28's pruned-record fixture; an unreadable floor busy and a non-database carrier unknown custody; the budget returned on a short ledger; and source pins that the module holds no write statement, open, lock, rename or sleep, calls the capture exactly twice and places each x6.recover point once. Every recovery leaves the carrier, its WAL frames, the witness and the floor byte-identical (SQLite's shared-memory index excluded) and reaches the points in bracket order."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive read-only carrier recovery capture layout (law X6 r2, unit X6a); library only, nothing recovers from a command; no release, custody, profile, boot or creator qualification'
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
# D2's four are on inventory122: on that parent they fold here; on
# inventory123 X5a already folded them, and the lock binds them to it as
# plain inheritance rows, so none is left to fold and D2's after text is
# checked instead.
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
    'standing': 'PROPOSED additive read-only carrier recovery capture layout (law X6 r2, unit X6a); independent review and lead assent required',
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
