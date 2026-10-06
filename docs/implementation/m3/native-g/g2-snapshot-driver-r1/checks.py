import datetime, hashlib, json, os, pathlib, shutil, subprocess, tempfile, time
worktree = pathlib.Path('/Users/sb/code/opensip-ai/opensip-g2-source-snapshot')
evidence = pathlib.Path('/tmp/opensip-implementation/g2-snapshot-driver-authoring')
evidence.mkdir(parents=True, exist_ok=True)
shutil.copyfile('/tmp/opensip-implementation/g2-authoring/snapshot-driver.rs', evidence / 'snapshot-driver.rs')
sysroot = pathlib.Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot')
darwin = pathlib.Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR'], text=True).strip())
lock = darwin / 'opensip-lanes.lock'
owned = False
while not owned:
    try:
        lock.mkdir()
        owned = True
    except FileExistsError:
        print('Waiting for the build lane.', flush=True)
        time.sleep(15)
try:
    active = [line for line in subprocess.check_output(['/bin/ps', '-Ao', 'pid=,comm='], text=True).splitlines() if line.split() and pathlib.Path(line.split()[-1]).name == 'cargo']
    assert not active, active
    scratch = pathlib.Path(tempfile.mkdtemp(prefix='opensip-g2-composition-', dir=darwin))
    scratch.chmod(0o700)
    env = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(scratch), RUSTFLAGS='-C linker=/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-path'], text=True).strip(), DYLD_LIBRARY_PATH=str(sysroot / 'lib') + ':' + str(sysroot / 'lib/rustlib/aarch64-apple-darwin/lib'))
    env.pop('RUSTC_BOOTSTRAP', None)
    rows = []
    def run(label, command, child=env):
        result = subprocess.run(['/usr/bin/nice', '-n', '10', *map(str, command)], cwd=worktree, env=child, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (evidence / (label + '.log')).write_text(result.stdout)
        rows.append({'label': label, 'command': list(map(str, command)), 'exitCode': result.returncode})
        print(json.dumps(rows[-1]), flush=True)
        assert result.returncode == 0, result.stdout
        return result
    target = scratch / 'official-build'
    run('identity-build', ['cargo', 'build', '-p', 'opensip-identity', '--locked', '--offline', '--target-dir', target], dict(env, RUSTC=str(sysroot / 'bin/rustc')))
    dependencies = target / 'debug/deps'
    libraries = list(dependencies.glob('libopensip_identity-*.rlib'))
    assert len(libraries) == 1, libraries
    driver = scratch / 'snapshot-driver'
    run('wrapper-build', [sysroot / 'bin/rustc', '--edition', '2024', '--sysroot', sysroot, '-D', 'warnings', '-C', 'prefer-dynamic', '-C', 'rpath', '-C', 'linker=/usr/bin/cc', '--extern', 'opensip_identity=' + str(libraries[0]), '-L', 'dependency=' + str(dependencies), evidence / 'snapshot-driver.rs', '-o', driver], dict(env, RUSTC_BOOTSTRAP='1'))
    namespace = scratch / 'namespace'
    namespace.mkdir()
    for mode in ['positive', 'tampered', 'missing', 'wrong-length', 'snapshot-mismatch', 'collision']:
        result = run(mode, [driver, namespace, sysroot, mode, worktree])
        expected = 'VERIFIED_SNAPSHOT_AFTER_ANALYSIS\n' if mode == 'positive' else 'REFUSED_BEFORE_COMPILER:' + mode + '\n'
        assert result.stdout == expected, result.stdout
        assert not list(namespace.iterdir()), 'no analysis/codegen outputs permitted'
    source_pins = []
    source_paths = ['providers/rust/src/sealed_vfs.rs', 'providers/rust/src/compiler_adapter.rs', 'providers/rust/src/source_snapshot.rs', 'crates/identity/Cargo.toml', 'Cargo.toml', 'Cargo.lock'] + [str(path.relative_to(worktree)) for path in sorted((worktree / 'crates/identity/src').rglob('*.rs'))]
    for relative in source_paths:
        raw = (worktree / relative).read_bytes()
        source_pins.append({'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
    artifacts = []
    for path in [driver, libraries[0], sysroot / 'bin/rustc']:
        raw = path.read_bytes()
        artifacts.append({'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    report = {'standing': 'G2 DECLARED SNAPSHOT/SOURCE-LOADER/REAL-DRIVER COMPOSITION, OWNED AUTHORING FIXTURES ONLY', 'commands': rows, 'completedAt': datetime.datetime.now(datetime.UTC).isoformat(), 'scratch': str(scratch), 'laneOwned': True, 'nice': 10, 'sourcePins': source_pins, 'artifactPins': artifacts, 'coherentIdentityLibraryCompiler': str(sysroot / 'bin/rustc'), 'bootstrapForWrapperBuildOnly': True, 'T1ProducerRan': False, 'providerLaunched': False, 'analyzedRepositoryCodeExecuted': False, 'fullSnapshotAdmission': False, 'nativeContextAdmitted': False, 'confinementClaimed': False, 'productionToolchainSelected': False, 'productQualification': False}
    (evidence / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
finally:
    if owned:
        lock.rmdir()
