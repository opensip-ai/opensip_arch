import datetime, json, os, pathlib, subprocess, tempfile, time
worktree = pathlib.Path('/Users/sb/code/opensip-ai/opensip-g2-prepared-inputs')
evidence = pathlib.Path('/tmp/opensip-implementation/g2-prepared-inputs-authoring')
evidence.mkdir(parents=True, exist_ok=True)
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
    scratch = pathlib.Path(tempfile.mkdtemp(prefix='opensip-g2-snapshot-', dir=darwin))
    scratch.chmod(0o700)
    env = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(scratch), RUSTFLAGS='-C linker=/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-path'], text=True).strip())
    env.pop('RUSTC_BOOTSTRAP', None)
    rows = []
    def run(label, command):
        result = subprocess.run(['/usr/bin/nice', '-n', '10', *map(str, command)], cwd=worktree / 'providers/rust', env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (evidence / (label + '.log')).write_text(result.stdout)
        rows.append({'label': label, 'command': list(map(str, command)), 'exitCode': result.returncode})
        print(json.dumps(rows[-1]), flush=True)
        assert result.returncode == 0, result.stdout
    run('format', ['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', 'src/prepared_inputs.rs'])
    run('unit-tests', ['cargo', 'test', '--locked', '--offline', '--lib'])
    run('clippy', ['cargo', 'clippy', '--locked', '--offline', '--lib', '--tests', '--', '-D', 'warnings'])
    assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
    report = {'standing': 'G2 DECLARED INERT PREPARED-BYTE/BINDING AUTHORING COMPONENT ONLY', 'commands': rows, 'completedAt': datetime.datetime.now(datetime.UTC).isoformat(), 'scratch': str(scratch), 'laneOwned': True, 'nice': 10, 'T1ProducerRan': False, 'providerLaunched': False, 'repositoryCodeExecuted': False, 'fullSnapshotAdmission': False, 'contextAdmitted': False, 'productQualification': False}
    (evidence / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
finally:
    if owned:
        lock.rmdir()
