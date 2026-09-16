"""Run generator child steps under a per-step deny-default macOS sandbox profile.

Positive: three real child steps, confined and unconfined, byte-compared.
Negative: probe.cjs and generator misuse under the same profiles.
Writes only below this trial directory.
"""
import hashlib, json, shutil, socket, subprocess, sys, threading
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
WORK = TRIAL / 'work'
SNAPSHOT, INPUTS, BIN = WORK / 'snapshot', WORK / 'inputs', WORK / 'bin'
RUNS = TRIAL / 'runs'
SANDBOX_EXEC = '/usr/bin/sandbox-exec'
CONTRACTS = SNAPSHOT / 'tools/contracts'


def quote(path):
    return json.dumps(str(path))


def profile(executable, reads, writes, extra=''):
    """Deny-default child profile. Apple's system.sb supplies the trusted
    dyld/libSystem runtime rules; everything else is explicit."""
    lines = ['(version 1)', '(deny default)', '(import "system.sb")',
             ';; system.sb exposes these account/system files; generation never needs them',
             '(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))',
             '(deny file-write* (subpath "/cores"))',
             '(allow process-exec (literal ' + quote(executable) + '))',
             '(allow file-read* (literal ' + quote(executable) + ')' + ''.join(' (subpath ' + quote(p) + ')' for p in reads + writes) + ')',
             ';; realpath(3)/Node module resolution lstat each ancestor directory (metadata only, no siblings)',
             '(allow file-read-metadata' + ''.join(' (path-ancestors ' + quote(p) + ')' for p in [executable, *reads, *writes]) + ')']
    if writes:
        lines.append('(allow file-write* ' + ' '.join('(subpath ' + quote(p) + ')' for p in writes) + ')')
    return '\n'.join(lines) + ('\n' + extra if extra else '') + '\n'


def env_for(scratch):
    return {'PATH': '/usr/bin:/bin', 'HOME': str(scratch / 'home'), 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}


def run(label, argv, *, executable, reads, writes, cwd, confined=True, extra=''):
    directory = RUNS / label
    directory.mkdir(parents=True, exist_ok=True)
    command = list(argv)
    if confined:
        text = profile(executable, reads, writes, extra)
        (directory / 'profile.sb').write_text(text)
        command = [SANDBOX_EXEC, '-f', str(directory / 'profile.sb'), *argv]
    process = subprocess.run(command, cwd=cwd, env=env_for(cwd), stdin=subprocess.DEVNULL,
                             capture_output=True, timeout=300)
    record = {'label': label, 'confined': confined, 'argv': argv, 'cwd': str(cwd), 'exitCode': process.returncode,
              'stdout': process.stdout.decode('utf-8', 'replace')[-4000:],
              'stderr': process.stderr.decode('utf-8', 'replace')[-4000:]}
    (directory / 'record.json').write_text(json.dumps(record, indent=1) + '\n')
    return record


def tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def fresh(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    (path / 'home').mkdir() if path.name == 'scratch' else None
    return path


def generation(mode):
    confined = mode == 'confined'
    base = RUNS / mode
    scratch, output = fresh(base / 'scratch'), fresh(base / 'output')
    node, generator = BIN / 'node', BIN / 'format-generator'
    # NA5: validation compiles its runtime into a scratch copy, never the inputs.
    validate_inputs = scratch / 'validate-inputs'
    validate_inputs.mkdir()
    for name in ('options.json', 'raw-schemas.json'):
        shutil.copyfile(INPUTS / name, validate_inputs / name)
    steps = [
        run(mode + '-1-validate', [str(node), str(CONTRACTS / 'validate-schemas.cjs'), str(validate_inputs)],
            executable=node, reads=[CONTRACTS], writes=[scratch], cwd=scratch, confined=confined),
        run(mode + '-2-rust', [str(generator), str(INPUTS), str(output)],
            executable=generator, reads=[INPUTS], writes=[output], cwd=scratch, confined=confined),
        run(mode + '-3-typescript', [str(node), str(CONTRACTS / 'generate-ts.cjs'), str(INPUTS), str(output)],
            executable=node, reads=[CONTRACTS, INPUTS], writes=[output], cwd=scratch, confined=confined),
    ]
    return steps, tree(output)


def negatives():
    base = RUNS / 'negative'
    scratch, output = fresh(base / 'scratch'), fresh(base / 'output')
    canary = fresh(TRIAL / 'canary') / 'secret.txt'
    canary.write_text('outside secret\n')
    node, generator = BIN / 'node', BIN / 'format-generator'
    # The probe is untrusted input code: place it where a real generator script lives.
    probe_dir = fresh(base / 'probe-snapshot')
    shutil.copyfile(TRIAL / 'scripts/probe.cjs', probe_dir / 'probe.cjs')
    tcp = socket.socket(); tcp.bind(('127.0.0.1', 0)); tcp.listen(); tcp.settimeout(6)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); udp.bind(('127.0.0.1', 0)); udp.settimeout(6)
    seen = {}
    def accept():
        try: tcp.accept()[0].close(); seen['tcp'] = True
        except OSError: seen['tcp'] = False
    def receive():
        try: udp.recvfrom(64); seen['udp'] = True
        except OSError: seen['udp'] = False
    threads = [threading.Thread(target=accept), threading.Thread(target=receive)]
    for t in threads: t.start()
    cfg = {'scratch': str(scratch), 'output': str(output), 'input': str(INPUTS / 'options.json'),
           'tcpPort': tcp.getsockname()[1], 'udpPort': udp.getsockname()[1],
           'outsideReads': {'canary': str(canary),
                            'candidateSource': '/private/tmp/opensip-implementation/m1-generator-integration-candidate-03/schemas/registry.json',
                            'snapshotUnselected': str(SNAPSHOT / 'tools/generate_contracts.py'),
                            'nodeHomeSibling': '/Users/sb/.nvm/versions/node/v24.16.0/include/node/node.h'},
           'outsideStats': {'canary': str(canary), 'nodeHomeSibling': '/Users/sb/.nvm/versions/node/v24.16.0/include/node/node.h'},
           'outsideLists': {'trial': str(TRIAL), 'snapshotParent': str(WORK)},
           'outsideWrites': {'trialRoot': str(TRIAL / 'canary/written.txt'), 'tmp': '/private/tmp/opensip-confinement-forbidden',
                             'inputs': str(INPUTS / 'injected.json'), 'snapshot': str(CONTRACTS / 'injected.cjs'),
                             'userTmpdir': '/private/var/tmp/opensip-confinement-forbidden'}}
    records = {}
    records['probe'] = run('negative-probe', [str(node), str(probe_dir / 'probe.cjs'), json.dumps(cfg)],
                           executable=node, reads=[probe_dir, INPUTS], writes=[scratch, output], cwd=scratch)
    for t in threads: t.join()
    tcp.close(); udp.close()
    records['listenerObserved'] = seen
    # Attribute link artifacts to the confined probe before any control runs.
    records['confinedScratchEntries'] = {p.name: {'symlink': p.is_symlink(), 'links': p.lstat().st_nlink,
        'sameInodeAsCanary': p.lstat().st_ino == canary.stat().st_ino} for p in sorted(scratch.iterdir())}
    records['canaryUnchanged'] = canary.read_text() == 'outside secret\n' and not (TRIAL / 'canary/written.txt').exists()
    records['forbiddenTmpAbsent'] = not Path('/private/tmp/opensip-confinement-forbidden').exists() and not Path('/private/var/tmp/opensip-confinement-forbidden').exists()
    records['inputsUntouched'] = not (INPUTS / 'injected.json').exists() and not (CONTRACTS / 'injected.cjs').exists()
    # Rust generator (in-process prettyplease) pointed outside its grants.
    outside_input = fresh(TRIAL / 'canary/outside-inputs')
    for name in ('owners.json', 'rust-projection.json'):
        shutil.copyfile(INPUTS / name, outside_input / name)
    records['generatorOutsideRead'] = run('negative-generator-outside-read', [str(generator), str(outside_input), str(output / 'g1')],
                                          executable=generator, reads=[INPUTS], writes=[output], cwd=scratch)
    records['generatorOutsideWrite'] = run('negative-generator-outside-write', [str(generator), str(INPUTS), str(TRIAL / 'canary/g2')],
                                           executable=generator, reads=[INPUTS], writes=[output], cwd=scratch)
    records['generatorOutsideWriteCreated'] = (TRIAL / 'canary/g2').exists()
    # Undeclared executable: exec itself is refused before any code runs.
    records['undeclaredExec'] = run('negative-undeclared-exec', ['/bin/sh', '-c', 'echo ran'],
                                    executable=node, reads=[INPUTS], writes=[output], cwd=scratch)
    # Control: identical probe without the sandbox, proving each negative is a real effect.
    control_scratch, control_output = fresh(RUNS / 'control' / 'scratch'), fresh(RUNS / 'control' / 'output')
    records['probeUnconfinedControl'] = run('control-probe-unconfined', [str(node), str(probe_dir / 'probe.cjs'),
        json.dumps({**cfg, 'scratch': str(control_scratch), 'output': str(control_output), 'tcpPort': 9, 'udpPort': 9,
                    'outsideWrites': {'trialRoot': str(TRIAL / 'canary/control-written.txt')}})],
        executable=node, reads=[], writes=[], cwd=control_scratch, confined=False)
    return records


def main():
    if len(sys.argv) != 1:
        raise SystemExit('no arguments')
    before = tree(WORK)
    confined_steps, confined_tree = generation('confined')
    plain_steps, plain_tree = generation('unconfined')
    result = {
        'standing': 'macOS development-trusted-host confinement trial; not hermetic, not product admission',
        'host': subprocess.run(['/usr/bin/sw_vers'], capture_output=True, text=True).stdout,
        'positive': {'confined': confined_steps, 'unconfined': plain_steps,
                     'confinedOutputs': confined_tree, 'byteParity': confined_tree == plain_tree and len(confined_tree) > 0},
        'negative': negatives(),
        'snapshotUnchanged': tree(WORK) == before,
    }
    (TRIAL / 'logs/results.json').write_text(json.dumps(result, indent=1) + '\n')
    summary = {'steps': [(s['label'], s['exitCode']) for s in confined_steps + plain_steps],
               'byteParity': result['positive']['byteParity'], 'outputs': len(confined_tree),
               'snapshotUnchanged': result['snapshotUnchanged']}
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
