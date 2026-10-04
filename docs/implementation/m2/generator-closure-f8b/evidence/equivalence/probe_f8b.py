"""F8b step 6: executable-equivalence probe. COMPARISON EVIDENCE, NOT ADMITTED F8b DRIFT.

Runs rebuild-01 and rebuild-02, each on its own, on identical prepared inputs, for both
generator invocations the pipeline issues:
- ordinary, as pipeline.py:132: <tool> PREPARED OUTPUT_ROOT;
- format, as pipeline.py:160: <tool> --format-rust INPUT OUTPUT.

It compares exit status, stdout, stderr, the exact output file set and every output byte.
It also checks determinism against step 5's own run. Ordinary outputs are compared with
step 5's base tree, where protocol.rs is the pre-assembly intermediate. The formatted
protocol.rs is compared with step 5's final assembled output (proposal r2 step 6; CODEX2
F8B-NBO-2). It selects and admits nothing. It never calls generate_contracts.py,
pipeline.run or the receipt validator. It reads no product file except the two
closure-pinned helpers it imports (admission.py and confine.py). The confinement profile
value is loaded from step 5's closure-authenticated snapshot, and its closure pin is asserted
(CODEX2 F8B-NBO-3). It writes only inside the fresh probe directory.

Usage: probe_f8b.py GEN_CANDIDATE WORKTREE PROBE_DIR REBUILD01_DIR REBUILD02_DIR
Exits nonzero on any difference, refusal or failed child; any difference stops the unit."""
import hashlib, importlib.util, io, json, os, shutil, sys, tarfile
from pathlib import Path

GEN, WORKTREE, PROBE, R01, R02 = (Path(a) for a in sys.argv[1:6])
EXE = 'opensip-contract-generator'
PREPARED = ['options.json', 'owners.json', 'provenance.json', 'raw-schemas.json', 'rust-projection.json', 'ts-projection.json']
RUST = {f'crates/contracts/src/generated/{n}.rs' for n in ('evidence', 'identity', 'invocation', 'output', 'protocol', 'mod')}
ENV_KEYS = ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TZ')


def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def tree_pins(root):
    return {p.relative_to(root).as_posix(): pin(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


if not sys.flags.isolated or sys.flags.optimize:
    raise SystemExit('run with python -I and no optimization')
GEN, WORKTREE = GEN.resolve(strict=True), WORKTREE.resolve(strict=True)
PROBE.mkdir(mode=0o700)
PROBE = PROBE.resolve(strict=True)

# Closure-authenticated pins from step 5's own snapshot (pipeline.py:128 input-closure.json).
closure_rows = {r['path']: r for r in json.loads((GEN / 'input-closure.json').read_bytes())['files']}
executables = json.loads((GEN / 'input-closure.json').read_bytes())['executables']
helpers = {}
for name in ('admission.py', 'confine.py'):
    rel = 'tools/contracts/' + name
    raw = (WORKTREE / rel).read_bytes()
    assert pin(raw) == {k: closure_rows[rel][k] for k in ('bytes', 'sha256')}, rel
    assert raw == (GEN / 'snapshot' / rel).read_bytes(), rel
    helpers[rel] = pin(raw)
admission = module(WORKTREE / 'tools/contracts/admission.py', 'probe_admission')
confine = module(WORKTREE / 'tools/contracts/confine.py', 'probe_confine')
profile_rel = 'tools/contracts/confinement-profile.json'
profile_raw = (GEN / 'snapshot' / profile_rel).read_bytes()
assert pin(profile_raw) == {k: closure_rows[profile_rel][k] for k in ('bytes', 'sha256')}, profile_rel
confinement = json.loads(profile_raw)
admission.verify_confinement(confinement)

# Binaries: rebuild-01 is the base selected pin; rebuild-02 is the pin step 5 ran (and its receipt's).
binaries = {
    '01': (R01 / EXE, {'bytes': 7202304, 'sha256': '4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959'}),
    '02': (R02 / EXE, {k: executables['generator'][k] for k in ('bytes', 'sha256')}),
}
assert json.loads((R02 / 'receipt.json').read_bytes())['executable'] == executables['generator']
tools, binary_pins = {}, {}
for label, (path, expected) in binaries.items():
    raw = path.read_bytes()
    assert pin(raw) == expected, 'rebuild-' + label
    copy = PROBE / ('tool-generator-' + label)
    copy.write_bytes(raw); copy.chmod(0o700)
    tools[label] = copy
    binary_pins[label] = {'path': str(path), 'before': pin(raw)}

# Inputs: copied once from step 5's run; both binaries read these same bytes.
inputs = PROBE / 'inputs'; (inputs / 'prepared').mkdir(parents=True)
assert sorted(p.name for p in (GEN / 'prepared').iterdir()) == PREPARED, 'unexpected prepared membership'
for name in PREPARED:
    shutil.copyfile(GEN / 'prepared' / name, inputs / 'prepared' / name)
shutil.copyfile(GEN / 'protocol-unformatted.rs', inputs / 'protocol-unformatted.rs')
inputs_before = tree_pins(inputs)
assert inputs_before['protocol-unformatted.rs'] == pin((GEN / 'protocol-unformatted.rs').read_bytes())

logs = PROBE / 'logs'; logs.mkdir()
runs = {}
for label in ('01', '02'):
    for inv in ('ordinary', 'format'):
        out = PROBE / f'out-{label}' / ('rust' if inv == 'ordinary' else 'format'); out.mkdir(parents=True)
        home = PROBE / 'private' / f'{label}-{inv}' / 'home'; home.mkdir(parents=True)
        cwd = PROBE / 'private' / f'{label}-{inv}' / 'cwd'; cwd.mkdir()
        if inv == 'ordinary':
            argv = [tools[label], inputs / 'prepared', out]; reads = [inputs / 'prepared']; expected = RUST
        else:
            argv = [tools[label], '--format-rust', inputs / 'protocol-unformatted.rs', out / 'protocol.rs']
            reads = [inputs / 'protocol-unformatted.rs']; expected = {'protocol.rs'}
        # Profile from the pipeline's own helper, after the output root exists (pipeline.py:85-95).
        policy = admission.child_profile(tools[label], reads, [out])
        policy_path = logs / f'{label}-{inv}-profile.sb'; policy_path.write_text(policy)
        env = {'PATH': '/usr/bin:/bin', 'HOME': str(home), 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}
        admission.verify_confinement(confinement)
        status, stdout, stderr, failure = confine.capture_child(
            ['/usr/bin/sandbox-exec', '-f', str(policy_path), *[str(x) for x in argv]], cwd=cwd, env=env)
        admission.verify_confinement(confinement)
        (logs / f'{label}-{inv}.stdout').write_bytes(stdout); (logs / f'{label}-{inv}.stderr').write_bytes(stderr)
        run = {'argvShape': ['<tool>'] + [str(Path(a).relative_to(PROBE)) if isinstance(a, Path) else a for a in argv[1:]],
               'reads': [str(p.relative_to(PROBE)) for p in reads], 'writes': [str(out.relative_to(PROBE))],
               'environmentKeys': list(ENV_KEYS), 'status': status, 'failure': failure,
               'stdout': pin(stdout), 'stderr': pin(stderr)}
        if failure or status != 0:
            runs[f'{label}/{inv}'] = run
            (PROBE / 'probe-partial.json').write_text(json.dumps(runs, indent=2) + '\n')
            raise SystemExit(f'rebuild-{label} {inv}: child refused or failed (status {status}, failure {failure})')
        outputs = admission.collect_outputs(out, expected)
        run['outputs'] = {name: pin(raw) for name, raw in sorted(outputs.items())}
        run['_bytes'] = outputs
        assert not any(home.iterdir()) and not any(cwd.iterdir()), 'child wrote outside its output root'
        runs[f'{label}/{inv}'] = run

comparison, determinism = {}, {}
for inv in ('ordinary', 'format'):
    a, b = runs[f'01/{inv}'], runs[f'02/{inv}']
    comparison[inv] = {
        'statusEqual': a['status'] == b['status'] == 0,
        'stdoutEqual': (logs / f'01-{inv}.stdout').read_bytes() == (logs / f'02-{inv}.stdout').read_bytes(),
        'stderrEqual': (logs / f'01-{inv}.stderr').read_bytes() == (logs / f'02-{inv}.stderr').read_bytes(),
        'outputSetEqual': set(a['_bytes']) == set(b['_bytes']),
        'outputBytesEqual': a['_bytes'] == b['_bytes'],
    }
    comparison[inv]['equal'] = all(comparison[inv].values())
# Determinism against step 5: ordinary joins the base tree; format joins the final output.
base = {name: (GEN / 'base' / name).read_bytes() for name in sorted(RUST)}
determinism['ordinaryVsStep5Base'] = {'reference': 'gen-candidate/base/crates/contracts/src/generated/*.rs (pre-assembly intermediate protocol.rs)',
                                      'equal': runs['02/ordinary']['_bytes'] == base}
final = (GEN / 'assembly/output/crates/contracts/src/generated/protocol.rs').read_bytes()
determinism['formatVsStep5Final'] = {'reference': 'gen-candidate/assembly/output/crates/contracts/src/generated/protocol.rs (final assembled output)',
                                     'equal': runs['02/format']['_bytes']['protocol.rs'] == final, 'reference_pin': pin(final)}

# After: binaries (originals and copies) and inputs unchanged.
for label, (path, expected) in binaries.items():
    assert pin(path.read_bytes()) == expected and pin(tools[label].read_bytes()) == expected, 'rebuild-' + label + ' changed'
    binary_pins[label]['after'] = pin(path.read_bytes())
inputs_after = tree_pins(inputs)
assert inputs_after == inputs_before, 'probe inputs changed'
for run in runs.values():
    run.pop('_bytes')

# Archive: inputs, both output trees, logs and profiles. Deterministic members; binaries excluded.
members = []
for top in ('inputs', 'out-01', 'out-02', 'logs'):
    members += [p for p in sorted((PROBE / top).rglob('*')) if p.is_file()]
manifest = {'schemaVersion': 1, 'standing': 'Members of probe.tar.xz (F8b step 6 comparison evidence; not admitted drift).',
            'members': [{'path': p.relative_to(PROBE).as_posix(), **pin(p.read_bytes())} for p in members]}
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode='w:xz', format=tarfile.PAX_FORMAT) as archive:
    for p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(p.relative_to(PROBE).as_posix())
        info.size, info.mtime, info.mode, info.uid, info.gid, info.uname, info.gname = len(raw), 0, 0o644, 0, 0, '', ''
        archive.addfile(info, io.BytesIO(raw))
archive_raw = buffer.getvalue()
(PROBE / 'probe.tar.xz').write_bytes(archive_raw)
manifest_raw = (json.dumps(manifest, indent=2) + '\n').encode()
(PROBE / 'probe-manifest.json').write_bytes(manifest_raw)
equal = all(c['equal'] for c in comparison.values()) and all(d['equal'] for d in determinism.values())
result = {
    'schemaVersion': 1,
    'standing': 'comparison evidence: rebuild-01 versus rebuild-02 on identical prepared inputs; not admitted F8b drift; no selection; no reproducible-build claim',
    'equal': equal,
    'binaries': {'rebuild-' + k: v for k, v in binary_pins.items()},
    'helpers': helpers, 'confinementProfile': {'path': 'gen-candidate/snapshot/' + profile_rel, **pin(profile_raw)},
    'inputs': {'before': inputs_before, 'after': inputs_after},
    'runs': {f'rebuild-{k.split("/")[0]}/{k.split("/")[1]}': v for k, v in runs.items()},
    'comparison': comparison, 'determinism': determinism,
    'archive': pin(archive_raw), 'manifest': pin(manifest_raw), 'archiveMembers': len(members),
}
(PROBE / 'probe-result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'equal': equal, 'comparison': comparison, 'determinism': {k: v['equal'] for k, v in determinism.items()},
                  'archive': result['archive'], 'archiveMembers': len(members)}, indent=2))
sys.exit(0 if equal else 1)
