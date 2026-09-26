"""macOS 27 negative matrix for the generator child Seatbelt profile (confinement-reprobe-01).

Adapted from opensip_arch/docs/implementation/m1/reviews/generator-confinement-01/scripts/run_confined.py.
Changes vs the macOS 26 script:
  * The profile is rendered by the CURRENT scratch product renderer
    (tools/contracts/admission.py child_profile), not the trial's own renderer, and
    children are launched with the product's confine.capture_child (pipes, stdin
    /dev/null, new session, close_fds) plus the pipeline's env/cwd shape.
  * Old /private/tmp candidate paths are replaced by the current layout: executables
    are copied like pipeline.py does (tool-node, tool-generator), inputs are the
    'prepared' directory and snapshot from a completed positive run, and the rebuilt
    Rust generator (argv: <prepared> <out>) replaces the format-trial binary.
  * The unconfined control uses real loopback listeners (the macOS 26 control used
    port 9) and control-specific write targets, and also runs the generator and
    /bin/sh controls.
  * Two extra probe rows (writeRootRename, syslogUnixConnect) exercise the current
    profile's require-not write-root rule and syslog deny.
Writes only under /Users/sb/opensip-deps/confinement-reprobe-01/negative-<run> plus
/private/tmp|/private/var/tmp control canaries that are removed afterwards.
"""
from pathlib import Path
import hashlib, importlib.util, json, shutil, socket, subprocess, sys, threading

BASE = Path('/Users/sb/opensip-deps/confinement-reprobe-01')
PRODUCT = BASE / 'product'
NODE = Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node')
GENERATOR = Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01/opensip-contract-generator')
SANDBOX_EXEC = '/usr/bin/sandbox-exec'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


admission = load(PRODUCT / 'tools/contracts/admission.py', 'scratch_admission')
confine = load(PRODUCT / 'tools/contracts/confine.py', 'scratch_confine')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}


def fresh(path):
    if path.exists() or path.is_symlink():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def main():
    run_id = sys.argv[1]
    positive = Path(sys.argv[2])  # completed positive run: its prepared/ and snapshot/
    trial = fresh(BASE / ('negative-' + run_id))
    runs = trial / 'runs'
    work = trial / 'work'
    bin_dir = work / 'bin'; bin_dir.mkdir(parents=True)
    node, generator = bin_dir / 'tool-node', bin_dir / 'tool-generator'
    for src, dst in ((NODE, node), (GENERATOR, generator)):
        dst.write_bytes(src.read_bytes()); dst.chmod(0o700)
    inputs = work / 'inputs'; shutil.copytree(positive / 'prepared', inputs)
    snapshot = work / 'snapshot'; shutil.copytree(positive / 'snapshot/tools/contracts', snapshot / 'tools/contracts')
    shutil.copyfile(positive / 'snapshot/tools/generate_contracts.py', snapshot / 'tools/generate_contracts.py')
    contracts = snapshot / 'tools/contracts'
    before = tree(work)

    records = {}

    def run(label, argv, *, executable, reads, writes, cwd, home, confined=True):
        d = runs / label; d.mkdir(parents=True, exist_ok=True)
        command = [str(x) for x in argv]
        profile_text = None
        if confined:
            profile_text = admission.child_profile(executable, reads, writes)
            (d / 'profile.sb').write_text(profile_text)
            command = [SANDBOX_EXEC, '-f', str(d / 'profile.sb'), *command]
        status, out, err, failure = confine.capture_child(command, cwd=cwd, env={
            'PATH': '/usr/bin:/bin', 'HOME': str(home), 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}, timeout=120)
        rec = {'label': label, 'confined': confined, 'argv': command, 'cwd': str(cwd), 'exitCode': status,
               'failure': failure, 'stdout': out.decode('utf-8', 'replace')[-6000:], 'stderr': err.decode('utf-8', 'replace')[-3000:],
               'profileSha256': hashlib.sha256(profile_text.encode()).hexdigest() if profile_text else None}
        (d / 'record.json').write_text(json.dumps(rec, indent=1) + '\n')
        return rec

    def listeners():
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
        def finish():
            for t in threads: t.join()
            tcp.close(); udp.close(); return seen
        return tcp.getsockname()[1], udp.getsockname()[1], finish

    # ---------------- confined ----------------
    base = runs / 'negative'
    scratch, output, home = fresh(base / 'scratch'), fresh(base / 'output'), fresh(base / 'home')
    canary_dir = fresh(trial / 'canary'); canary = canary_dir / 'secret.txt'; canary.write_text('outside secret\n')
    probe_dir = fresh(base / 'probe-snapshot'); shutil.copyfile(BASE / 'scripts/probe.cjs', probe_dir / 'probe.cjs')
    forbidden_tmp = Path('/private/tmp/opensip-confinement-forbidden')
    forbidden_vartmp = Path('/private/var/tmp/opensip-confinement-forbidden')
    assert not forbidden_tmp.exists() and not forbidden_vartmp.exists()
    tcp_port, udp_port, finish = listeners()
    cfg = {'scratch': str(scratch), 'output': str(output), 'input': str(inputs / 'options.json'),
           'tcpPort': tcp_port, 'udpPort': udp_port,
           'outsideReads': {'canary': str(canary),
                            'candidateSource': '/Users/sb/code/opensip-ai/opensip/schemas/registry.json',
                            'snapshotUnselected': str(snapshot / 'tools/generate_contracts.py'),
                            'nodeHomeSibling': '/Users/sb/.nvm/versions/node/v24.16.0/include/node/node.h'},
           'outsideStats': {'canary': str(canary), 'nodeHomeSibling': '/Users/sb/.nvm/versions/node/v24.16.0/include/node/node.h'},
           'outsideLists': {'trial': str(trial), 'snapshotParent': str(work)},
           'outsideWrites': {'trialRoot': str(canary_dir / 'written.txt'), 'tmp': str(forbidden_tmp),
                             'inputs': str(inputs / 'injected.json'), 'snapshot': str(contracts / 'injected.cjs'),
                             'userTmpdir': str(forbidden_vartmp)}}
    records['probe'] = run('negative-probe', [node, probe_dir / 'probe.cjs', json.dumps(cfg)],
                           executable=node, reads=[probe_dir, inputs], writes=[scratch, output], cwd=scratch, home=home)
    records['listenerObserved'] = finish()
    records['confinedScratchEntries'] = {p.name: {'symlink': p.is_symlink(), 'links': p.lstat().st_nlink,
        'sameInodeAsCanary': p.lstat().st_ino == canary.stat().st_ino} for p in sorted(scratch.iterdir())}
    records['outputRootStillPresent'] = output.is_dir() and not Path(str(output) + '-renamed').exists()
    records['canaryUnchanged'] = canary.read_text() == 'outside secret\n' and not (canary_dir / 'written.txt').exists()
    records['forbiddenTmpAbsent'] = not forbidden_tmp.exists() and not forbidden_vartmp.exists()
    records['inputsUntouched'] = not (inputs / 'injected.json').exists() and not (contracts / 'injected.cjs').exists()
    outside_input = fresh(canary_dir / 'outside-inputs')
    for p in inputs.iterdir():
        shutil.copyfile(p, outside_input / p.name)
    gout = fresh(base / 'gen-output')
    records['generatorOutsideRead'] = run('negative-generator-outside-read', [generator, outside_input, gout / 'g1'],
                                          executable=generator, reads=[inputs], writes=[gout], cwd=scratch, home=home)
    records['generatorOutsideReadCreated'] = (gout / 'g1').exists()
    records['generatorOutsideWrite'] = run('negative-generator-outside-write', [generator, inputs, canary_dir / 'g2'],
                                           executable=generator, reads=[inputs], writes=[gout], cwd=scratch, home=home)
    records['generatorOutsideWriteCreated'] = (canary_dir / 'g2').exists()
    # Positive control inside the same generator profile shape: granted in/out works.
    records['generatorGranted'] = run('positive-generator-granted', [generator, inputs, gout / 'g0'],
                                      executable=generator, reads=[inputs], writes=[gout], cwd=scratch, home=home)
    records['generatorGrantedFiles'] = sorted(p.name for p in (gout / 'g0').iterdir()) if (gout / 'g0').is_dir() else None
    records['undeclaredExec'] = run('negative-undeclared-exec', ['/bin/sh', '-c', 'echo ran'],
                                    executable=node, reads=[inputs], writes=[output], cwd=scratch, home=home)

    # ---------------- unconfined control ----------------
    cbase = runs / 'control'
    cscratch, coutput, chome = fresh(cbase / 'scratch'), fresh(cbase / 'output'), fresh(cbase / 'home')
    ctmp, cvartmp = Path(str(forbidden_tmp) + '-control'), Path(str(forbidden_vartmp) + '-control')
    cinputs = fresh(cbase / 'inputs-copy'); ccontracts = fresh(cbase / 'contracts-copy')
    tcp_port, udp_port, finish = listeners()
    ccfg = {**cfg, 'scratch': str(cscratch), 'output': str(coutput), 'tcpPort': tcp_port, 'udpPort': udp_port,
            'outsideWrites': {'trialRoot': str(canary_dir / 'control-written.txt'), 'tmp': str(ctmp),
                              'inputs': str(cinputs / 'injected.json'), 'snapshot': str(ccontracts / 'injected.cjs'),
                              'userTmpdir': str(cvartmp)}}
    records['probeUnconfinedControl'] = run('control-probe-unconfined', [node, probe_dir / 'probe.cjs', json.dumps(ccfg)],
        executable=node, reads=[], writes=[], cwd=cscratch, home=chome, confined=False)
    records['controlListenerObserved'] = finish()
    records['controlScratchEntries'] = {p.name: {'symlink': p.is_symlink(), 'links': p.lstat().st_nlink} for p in sorted(cscratch.iterdir())}
    records['controlWritesCreated'] = {k: Path(v).exists() for k, v in ccfg['outsideWrites'].items()}
    for p in (ctmp, cvartmp):
        if p.exists(): p.unlink()
    cg = fresh(cbase / 'gen-output')
    records['generatorOutsideReadControl'] = run('control-generator-outside-read', [generator, outside_input, cg / 'g1'],
        executable=generator, reads=[], writes=[], cwd=cscratch, home=chome, confined=False)
    records['generatorOutsideWriteControl'] = run('control-generator-outside-write', [generator, inputs, canary_dir / 'g2-control'],
        executable=generator, reads=[], writes=[], cwd=cscratch, home=chome, confined=False)
    records['generatorOutsideWriteControlCreated'] = (canary_dir / 'g2-control').exists()
    records['undeclaredExecControl'] = run('control-sh-unconfined', ['/bin/sh', '-c', 'echo ran'],
        executable=node, reads=[], writes=[], cwd=cscratch, home=chome, confined=False)

    result = {'standing': 'macOS 27 reprobe of the generator child Seatbelt profile; development-trusted host, not release qualification',
              'host': subprocess.run(['/usr/bin/sw_vers'], capture_output=True, text=True).stdout,
              'renderer': {'path': str(PRODUCT / 'tools/contracts/admission.py'), 'sha256': sha(PRODUCT / 'tools/contracts/admission.py')},
              'probe': {'path': str(BASE / 'scripts/probe.cjs'), 'sha256': sha(BASE / 'scripts/probe.cjs')},
              'executables': {'node': sha(node), 'generator': sha(generator), 'sandboxExec': sha(SANDBOX_EXEC),
                              'systemSb': sha('/System/Library/Sandbox/Profiles/system.sb'),
                              'dyldSupportSb': sha('/System/Library/Sandbox/Profiles/dyld-support.sb')},
              'negative': records, 'workUnchanged': tree(work) == before}
    (trial / 'results.json').write_text(json.dumps(result, indent=1) + '\n')
    probe = json.loads(records['probe']['stdout'])
    print(json.dumps({'probeExit': records['probe']['exitCode'], 'probe': probe,
                      'genRead': records['generatorOutsideRead']['exitCode'], 'genWrite': records['generatorOutsideWrite']['exitCode'],
                      'genGranted': records['generatorGranted']['exitCode'], 'undeclared': records['undeclaredExec']['exitCode'],
                      'workUnchanged': result['workUnchanged']}, indent=1))


if __name__ == '__main__':
    main()
