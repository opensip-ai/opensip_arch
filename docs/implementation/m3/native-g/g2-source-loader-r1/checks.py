import datetime, json, os, pathlib, subprocess, tempfile, time

worktree = pathlib.Path('/Users/sb/code/opensip-ai/opensip-g2a')
evidence = pathlib.Path('/tmp/opensip-implementation/g2-authoring')
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
    scratch = pathlib.Path(tempfile.mkdtemp(prefix='opensip-g2-source-', dir=darwin))
    scratch.chmod(0o700)
    env = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(scratch), RUSTFLAGS='-C linker=/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-path'], text=True).strip())
    env.pop('RUSTC_BOOTSTRAP', None)
    rows = []
    def run(label, command, child=env, cwd=worktree / 'providers/rust'):
        result = subprocess.run(['/usr/bin/nice', '-n', '10', *map(str, command)], cwd=cwd, env=child, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (evidence / (label + '.log')).write_text(result.stdout)
        rows.append({'label': label, 'command': list(map(str, command)), 'exitCode': result.returncode})
        print(json.dumps(rows[-1]), flush=True)
        return result
    for file in ['sealed_vfs.rs', 'compiler_adapter.rs', 'lib.rs']:
        r = run('format-' + file, ['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', 'src/' + file])
        assert r.returncode == 0, r.stdout
    r = run('unit-tests', ['cargo', 'test', '--locked', '--offline', '--lib'])
    assert r.returncode == 0, r.stdout
    r = run('clippy', ['cargo', 'clippy', '--locked', '--offline', '--lib', '--tests', '--', '-D', 'warnings'])
    assert r.returncode == 0, r.stdout
    compiler_env = dict(env, DYLD_LIBRARY_PATH=str(sysroot / 'lib') + ':' + str(sysroot / 'lib/rustlib/aarch64-apple-darwin/lib'))
    build_env = dict(compiler_env, RUSTC_BOOTSTRAP='1', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-path'], text=True).strip())
    binary = scratch / 'owned-driver'
    r = run('driver-build', [sysroot / 'bin/rustc', '--edition', '2024', '--sysroot', sysroot, '-C', 'prefer-dynamic', '-C', 'rpath', '-C', 'linker=/usr/bin/cc', evidence / 'driver.rs', '-o', binary], build_env)
    assert r.returncode == 0, r.stdout
    namespace = scratch / 'namespace'
    namespace.mkdir()
    (namespace / 'forbidden.rs').write_text('compile_error!("AMBIENT_FALLBACK_EXECUTED"); pub fn value() -> u8 { 99 }')
    (namespace / 'forbidden.bin').write_bytes(b'AMBIENT_FALLBACK_EXECUTED')
    assert not (namespace / 'lib.rs').exists()
    for mode in ['positive', 'missing-module', 'missing-binary', 'invalid-text']:
        r = run('driver-' + mode, [binary, namespace, sysroot, mode], compiler_env)
        if mode == 'positive':
            assert r.returncode == 0 and 'SEALED_AFTER_ANALYSIS' in r.stdout, r.stdout
        else:
            assert r.returncode != 0 and 'SEALED_AFTER_ANALYSIS' not in r.stdout and 'AMBIENT_FALLBACK_EXECUTED' not in r.stdout, r.stdout
        assert not list(namespace.glob('*.rmeta')), 'analysis must stop before emitting metadata'
    assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
    report = {'standing': 'G2 SOURCE-LOADER AUTHORING COMPONENT ONLY', 'commands': rows, 'completedAt': datetime.datetime.now(datetime.UTC).isoformat(), 'scratch': str(scratch), 'laneOwned': True, 'nice': 10, 'T1ProducerRan': False, 'providerLaunched': False, 'repositoryCodeExecuted': False, 'confinementClaimed': False, 'productionToolchainSelected': False}
    (evidence / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
finally:
    if owned:
        lock.rmdir()
