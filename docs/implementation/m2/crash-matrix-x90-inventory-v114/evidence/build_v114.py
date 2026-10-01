"""Build inventory114 by adding exactly the seven X9-0 rows (law X9 r1 items 1
to 5, 7 and 12: the crash-matrix mechanism) to the inventory the real
product lock selects, and write its successor record. The parent follows the
lock: inventory111 (units X2e and X3b-3, selected at product abf2a48). It
projects the sixteen rows inherited through the parent. Run with python3 -I
-B from any directory. Deterministic for a given lock: rerunning reproduces
the same bytes. It refuses to write over any path git already tracks, and
while a lock selects inventory114. It was first built on inventory108 at
97f630a (accepted at r1), then rebuilt on inventory111 with the same seven
rows; PRIOR maps inventory106, inventory108 and inventory111."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v114.json'
RECORD = M + 'crash-matrix-x90-inventory-v114/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v106.json': (M + 'trust-floor-x4tb-inventory-v106/successor.json', 'inventory106', 'X4T-b'),
    M + 'repository-file-inventory.v108.json': (M + 'journal-rollover-x3b4-inventory-v108/successor.json', 'inventory108', 'X3b-4'),
    M + 'repository-file-inventory.v111.json': (M + 'operation-handoff-x2e-inventory-v111/successor.json', 'inventory111', 'X2e'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory114 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/platform/src/crash_macros.rs', 'opensip-platform', 'public-api',
        "Define crash_barrier! and crash_scope! (law X9 r1 items 1 and 2; unit X9-0) in every build, so that protocol and primitive call sites compile with or without the test-only crash-matrix feature. Without the feature a point expands to an empty block, a wrapped point to its effect expression, a gate to its timed wait, a draw to its draw and a scope to its block: no call, no string and no branch remains. With the feature (macOS and Linux) they call opensip_platform::crash_barrier. Forms: primitive points (step, fallible, write) inside this crate's native primitives; protocol points of kind step, fallible (with the caller's fault-to-error mapping), gate and draw under the current or a named scope. Confers no authority."),
    row('crates/platform/src/crash_barrier.rs', 'opensip-platform', 'service',
        "The crash barrier module of law X9 r1 items 1 to 5 (unit X9-0), compiled only under the test-only crash-matrix feature, which no manifest enables and which src/lib.rs refuses without debug assertions. It holds the scope registry fixed by item 5 (with a read-only flag for x4.observer and x6.recover, and two x9.selftest scopes only in this crate's test build), the point grammar <scope>[.segments][/<primitive-step>.<before|after>] with per-name 1-based occurrences, the kinds step, fallible, write, gate and draw and the actions each admits, and the OPENSIP_X9_ARMS parser (<full name>#<k|*>=hold|fail-before|fail-after|torn|inject-id:exec1_..., inject-id only at x3d.session.execution-draw). Without OPENSIP_X9_ARMS every point is one OnceLock read and a return. In a matrix child (OPENSIP_X9_CHILD set) every reached point writes one tagged stderr record X9|pid|thread|n|name#k|event|payload in a single write(2) of at most 512 bytes, numbered under one lock; hold registers the point, writes held and blocks on a stdin read until resume (bare when exactly one thread holds) or resume <name>#<k>, one held thread reading for all and handing lines to their targets by condvar; fail-before and fail-after return EIO from a primitive or the caller's error at a protocol site without or after the effect; torn writes the first half of the bytes with the same write, then holds, and a resumed torn write fails with EIO; a gate's armed rendezvous replaces the product's timed wait; the draw records its payload or returns an injected ExecutionId. An unadmitted action, a primitive outside any scope, an unknown scope or a malformed arming is a harness-error record and exit status 86. It never sleeps, polls or waits on a timer. Test-only; confers no authority, qualification or production seam."),
    row('crates/platform/src/crash_barrier/driver.rs', 'opensip-platform', 'service',
        "The parent driver of law X9 r1 item 3 and item 5's census (unit X9-0), under the test-only crash-matrix feature. MatrixChild re-executes the current test binary as current_exe() --exact <entry> --nocapture --test-threads=1 with a cleared environment holding only OPENSIP_X9_CHILD, OPENSIP_X9_INPUT, OPENSIP_X9_ARMS (absent for an untraced child) and TMPDIR, validates the arming before spawning, reads the child's stderr records on a reader thread and drains stdout, awaits a held or other event by blocking reads, writes addressed resumes on stdin, and kills with SIGKILL; dropping an unfinished child kills it. The per-run watchdog (300 s; shorter only in this crate's tests) is the one timed wait: it kills the child and the run can only be a HARNESS-ERROR. Exit verifies a finished child (exit 0, the entry ran, no harness-error, every arm reached) and item 3's death at a point (signal 9, the holding thread's last record is that held, and no later record names a durability point), and gives the outcome and the trace without the process id. Census takes a traced child with nothing armed into points with contiguous occurrences and durability, and derives the kill set: each durability point at #1 and, when repeated, at (n + 1) / 2 and n. Test-only; confers no authority."),
    row('crates/platform/src/crash_barrier/self_tests.rs', 'opensip-platform', 'test',
        "X9-0's self-tests (law X9 r1 item 12), compiled only for this crate's tests with the crash-matrix feature. A matrix_child test entry returns at once in the parent's own run; each test re-executes it as a child over a /tmp scratch root and drives it: a kill at replace's rename.after with the new bytes visible, at write.before leaving the empty staging file no destructor removed, and at lock.after with the flock busy until the death, each verified by SIGKILL and the trace; hold then resume to the lawful outcome and tree, with the bare resume when one thread holds; fail-before and fail-after at rename, file-barrier and directory-barrier returning EIO on the primitive's own stage and visibility, with the state each leaves, and at an accounted barrier; torn writes leaving half the bytes, killed or resumed into a failed write; an untraced child writing no record and matching the featureless outcome and tree, a traced unarmed child doing the same and recording the pinned 42-point census and 44-point kill set with a reproducible trace; armed but unreached points and actions a point's kind does not admit as harness errors; a primitive outside any scope; addressed resumes across two held threads, read-only points of another thread admitted after a kill point and a durability point refused; the watchdog ending a never-resumed child as a harness error; gate, protocol fallible and draw points with inject-id; and the arming grammar, point names, durability and kill-set derivation."),
    row('crates/platform/src/crash_matrix_tests.rs', 'opensip-platform', 'test',
        "Pins for law X9 r1 items 2 and 3 (unit X9-0) that run in every platform test build, with or without the crash-matrix feature: every Cargo.toml and Cargo configuration file in the repository names crash-matrix only as a crate's own [features] definition forwarding to dependencies' crash-matrix, or as a [[test]] target's required-features, never default or in any dependency table, and every crate declaring it carries the compile guard; the pin's refusals; a source pin that the barrier module, driver, self-tests and macros admit no sleep, timed wait, nonblocking or polling call except the driver's one watchdog receive; without the feature, points leave only their effect and literals; and the self-test workload (each instrumented platform primitive once in x9.selftest scopes), whose pinned outcome and tree the feature's unarmed child must reproduce. Compiled only for tests; confers no qualification."),
    row('tools/check_crash_matrix.py', 'tooling', 'validator',
        "Check an X9 crash-matrix run set (law X9 r1 item 7) and scan a release binary (item 2, guard 4); read-only, standard library only. check refuses unless both lead run sets list exactly the reviewed required-runs.v1.json rows, each run and matrix.json is canonical JSON of the opensip.x9 v1 shapes, every verdict is PASS with labels, units, script and expected values equal to the required row, the reviewed clean commit and dev crash-matrix profile, synthetic-signed-v2 and BASELINE-ATTESTED host labels, process-death exactly when the script kills with a signal-9 child held there, a census of registered scopes with the right durability whose derived kill set equals the recorded one and is fully killed, a passed release absence, limits L1 to L10, and agreement of the two repetitions on normalizedSha256, trace digests and census. release-absence reports whether OPENSIP_X9_ or any scope name from the barrier's registry block occurs in a binary. It runs no matrix and qualifies nothing."),
    row('tools/tests/test_check_crash_matrix.py', 'tooling', 'test',
        "Exercise tools/check_crash_matrix.py on a disposable synthetic run pair against the repository's real scope registry: the registry read, kill-set derivation and point grammar; a complete agreeing pair passing; missing and extra runs; each run-field corruption (verdicts, labels, expected, script, commit, dirty worktree, profile, fixture labels, unverified kills, keys, postState); a claimed process death; noncanonical bytes, floats and duplicate keys; matrix corruptions (run bytes, kill set, durability, unregistered census point, release absence, limits, product); an uncovered new durability point; disagreeing repetitions; and the release-absence scan."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive crash-matrix mechanism layout (law X9 r1, unit X9-0); test-only; no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive crash-matrix mechanism layout (law X9 r1, unit X9-0); independent review and lead assent required',
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
