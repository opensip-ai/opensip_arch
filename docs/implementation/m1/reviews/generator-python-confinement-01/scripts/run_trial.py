"""Confined Python preparation child: positive parity and negative probes.

Positive: the real entry + prepare.py confined twice under the exact pinned
profile, collected with candidate-03's lstat/O_NOFOLLOW collector, and compared
byte-for-byte with an unconfined run of the same entry and with a direct
in-process prepare.prepare reference (test oracle only, never a fallback).
Negative: probe_prepare.py loaded as prepare.py under the same profile shape,
each probe also run unconfined as a control; plus profile/flag ablations.
Writes only below this trial directory (probe targets outside it are attempted
only by confined runs and checked absent afterwards).
"""
import hashlib, json, shutil, socket, subprocess, sys, threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confine as C

CANDIDATE = Path('/private/tmp/opensip-implementation/m1-generator-integration-candidate-03/tools/generate_contracts.py')
TRIAL01_INPUTS = Path('/private/tmp/opensip-implementation/m1-generator-confinement-trial-01/work/inputs')
SOCKET_EXTENSION = C.STDLIB / 'lib-dynload/_socket.cpython-314-darwin.so'
SOCKET_EXTENSION_SHA256 = '3a7a8008ad91202e06d2ce6a5963963c89b78ffb64d7e6b5e9bcd75a56b9c89b'
CANARY = C.TRIAL / 'canary/secret.txt'
FORBIDDEN_OUTSIDE = ['/private/tmp/opensip-python-confinement-forbidden', '/private/var/tmp/opensip-python-confinement-forbidden',
                     str(C.STDLIB / 'opensip-python-confinement-forbidden.py'),
                     str(C.STDLIB / 'json/__pycache__/opensip-python-confinement-forbidden.pyc')]


def load_collector():
    """candidate-03's parent collector, executed from the exact bytes recorded here."""
    raw = CANDIDATE.read_bytes()
    module = type(sys)('candidate03_generate')
    module.__file__ = str(CANDIDATE)
    exec(compile(raw, str(CANDIDATE), 'exec'), module.__dict__)
    return module, hashlib.sha256(raw).hexdigest()


def fresh(path):
    if path.exists() or path.is_symlink():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def entry_argv(output, flags=C.FLAGS, code=C.CODE):
    return [C.EXECUTABLE, *flags, C.ENTRY, C.INPUTS / 'raw-schemas.json', C.INPUTS / 'options.json', code, output]


def collect(collector, output):
    try:
        files = collector.collect_outputs(output, set(C.EMITTED))
        return {'ok': True, 'sha256': {k: hashlib.sha256(v).hexdigest() for k, v in sorted(files.items())}}, files
    except Exception as error:
        return {'ok': False, 'error': type(error).__name__ + ': ' + str(error)}, None


def reference_direct():
    """Oracle: unconfined in-process prepare.prepare into a real directory (writes 4 files)."""
    output = fresh(C.RUNS / 'reference-direct/output')
    path = C.CODE / 'prepare.py'
    module = type(sys)('reference_prepare')
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    documents = {}
    for text in json.loads((C.INPUTS / 'raw-schemas.json').read_text()):
        document = json.loads(text)
        documents[document['$id']] = document
    module.prepare(documents, json.loads((C.INPUTS / 'options.json').read_text()), output)
    return C.tree(output)


def positive(grants, collector):
    result = {}
    for label in ('confined-1', 'confined-2'):
        output = fresh(C.RUNS / label / 'output')
        record = C.run(label, entry_argv(output), text=C.profile(grants, reads=C.child_reads(), output=output))
        record['collection'], _ = collect(collector, output)
        result[label] = record
    output = fresh(C.RUNS / 'unconfined-entry/output')
    record = C.run('unconfined-entry', entry_argv(output))
    record['collection'], _ = collect(collector, output)
    result['unconfined-entry'] = record
    reference = reference_direct()
    result['referenceDirect'] = reference
    trial01 = {name: C.sha(TRIAL01_INPUTS / name) for name in C.EMITTED}
    shas = [result[k]['collection'].get('sha256') for k in ('confined-1', 'confined-2', 'unconfined-entry')]
    result['parity'] = {
        'confinedRunsIdentical': shas[0] is not None and shas[0] == shas[1],
        'confinedEqualsUnconfinedEntry': shas[0] is not None and shas[0] == shas[2],
        'confinedEqualsDirectPrepareReference': shas[0] == {k: reference[k] for k in C.EMITTED},
        'directReferenceAlsoWroteTargetsJson': 'targets.json' in reference,
        'confinedEqualsTrial01PreparedInputs': shas[0] == trial01,
        'trial01PreparedInputsNote': 'trial-01 work/inputs came from candidate-03 prepare.py of that moment; informational'}
    # Parent-side merge demo: collected child bytes + the parent's own options/raw schemas, never child-written copies.
    merged = fresh(C.RUNS / 'merged-inputs')
    _, files = collect(collector, C.RUNS / 'confined-1/output')
    if files:
        for name, raw in files.items():
            (merged / name).write_bytes(raw)
        for name in ('options.json', 'raw-schemas.json'):
            shutil.copyfile(C.INPUTS / name, merged / name)
    result['mergedInputs'] = C.tree(merged)
    return result


def probe_code(label, cfg):
    code = fresh(C.RUNS / label / 'code')
    template = (C.TRIAL / 'scripts/probe_prepare.py').read_text()
    (code / 'prepare.py').write_text(template.replace('json.loads(__CFG__)', 'json.loads(' + repr(json.dumps(cfg)) + ')', 1))
    (code / 'runtime').mkdir()
    shutil.copyfile(C.CODE / 'runtime/schema.ts', code / 'runtime/schema.ts')
    return code


def parse(stdout):
    merged = {}
    for line in stdout.splitlines():
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if isinstance(value, dict):
            for key, rows in value.items():
                merged.setdefault(key, {}).update(rows)
    return merged


class Listeners:
    def __init__(self):
        self.tcp = socket.socket(); self.tcp.bind(('127.0.0.1', 0)); self.tcp.listen(); self.tcp.settimeout(8)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); self.udp.bind(('127.0.0.1', 0)); self.udp.settimeout(8)
        self.seen = {}
        self.threads = [threading.Thread(target=self.accept), threading.Thread(target=self.receive)]
        for thread in self.threads:
            thread.start()

    def accept(self):
        try: self.tcp.accept()[0].close(); self.seen['tcp'] = True
        except OSError: self.seen['tcp'] = False

    def receive(self):
        try: self.udp.recvfrom(64); self.seen['udp'] = True
        except OSError: self.seen['udp'] = False

    def close(self):
        for thread in self.threads:
            thread.join()
        self.tcp.close(); self.udp.close()
        return self.seen


def probe_cfg(mode, output, targets, confined, ports=(9, 9)):
    reads = {'canary': str(CANARY),
             'trialSourceCopy': str(C.TRIAL / 'source/schemas/registry.json'),
             'candidate03Source': str(CANDIDATE),
             'unselectedRuntime': str(C.CODE / 'runtime/patterns.ts'),
             'unimportedStdlib': str(C.STDLIB / 'subprocess.py'),
             'stdlibBytecodeCache': str(C.STDLIB / 'json/__pycache__/__init__.cpython-314.pyc'),
             'sitePackages': '/opt/homebrew/lib/python3.14/site-packages/pip/__init__.py',
             'frameworkSibling': str(C.FRAMEWORK / 'include/python3.14/Python.h'),
             'bundleInfoPlist': str(C.FRAMEWORK / 'Resources/Python.app/Contents/Info.plist'),
             'etcPasswd': '/private/etc/passwd'}
    creates = {'trialRoot': str(targets / 'written.txt'), 'outputParent': str(targets / 'output-parent.txt'),
               'inputsDir': str(targets / 'inputs-injected.json'), 'codeDir': str(targets / 'code-injected.py')}
    writes = {'optionsJson': str(targets / 'options.json'), 'rawSchemasJson': str(targets / 'raw-schemas.json'),
              'preparePy': str(targets / 'prepare.py'), 'entry': str(targets / 'prepare-inputs.py')}
    if confined:
        creates.update({'inputsDir': str(C.INPUTS / 'injected.json'), 'codeDir': str(C.CODE / 'injected.py'),
                        'outputParent': str(output.parent / 'output-parent.txt'),
                        'privateTmp': FORBIDDEN_OUTSIDE[0], 'varTmp': FORBIDDEN_OUTSIDE[1],
                        'stdlibDir': FORBIDDEN_OUTSIDE[2], 'stdlibPycache': FORBIDDEN_OUTSIDE[3]})
        writes = {'optionsJson': str(C.INPUTS / 'options.json'), 'rawSchemasJson': str(C.INPUTS / 'raw-schemas.json'),
                  'preparePy': str(C.CODE / 'prepare.py'), 'entry': str(C.ENTRY)}
    return {'mode': mode, 'output': str(output), 'entry': str(C.ENTRY), 'options': str(C.INPUTS / 'options.json'),
            'code': str(C.CODE), 'tcpPort': ports[0], 'udpPort': ports[1], 'reads': reads,
            'stats': {'canary': str(CANARY), 'frameworkSibling': reads['frameworkSibling']},
            'lists': {'trial': str(C.TRIAL), 'work': str(C.WORK), 'privateTmp': '/private/tmp',
                      'outputParent': str(output.parent), 'stdlibGrantedDir': str(C.STDLIB)},
            'creates': creates, 'writes': writes}


def probe_run(grants, mode, confined, extra_extensions=(), map_executable=True, suffix=''):
    label = ('negative-' if confined else 'control-') + 'probe-' + mode + suffix
    base = fresh(C.RUNS / label)
    output = fresh(base / 'output')
    targets = fresh(base / 'targets')
    if not confined:
        for name, src in (('options.json', C.INPUTS / 'options.json'), ('raw-schemas.json', C.INPUTS / 'raw-schemas.json'),
                          ('prepare.py', C.CODE / 'prepare.py'), ('prepare-inputs.py', C.ENTRY)):
            shutil.copyfile(src, targets / name)
    listeners = Listeners() if mode == 'network' else None
    ports = (listeners.tcp.getsockname()[1], listeners.udp.getsockname()[1]) if listeners else (9, 9)
    code = probe_code(label, probe_cfg(mode, output, targets, confined, ports))
    text = C.profile(grants, reads=C.child_reads(code), output=output, extra_extensions=extra_extensions,
                     map_executable=map_executable) if confined else None
    record = C.run(label, entry_argv(output, code=code), text=text)
    record['listenerObserved'] = listeners.close() if listeners else None
    record['probe'] = parse(record['stdout'])
    record['outputEntries'] = {p.name: {'symlink': p.is_symlink(), 'nlink': p.lstat().st_nlink,
                                        'sameInodeAsCanary': p.lstat().st_ino == CANARY.stat().st_ino}
                               for p in sorted(output.iterdir())} if output.is_dir() else None
    return record


def negatives(grants, collector):
    results = {}
    fresh(CANARY.parent)
    CANARY.write_text('outside secret\n')
    for mode in ('main', 'exec'):
        results['probe-' + mode] = probe_run(grants, mode, True)
        results['control-probe-' + mode] = probe_run(grants, mode, False)
    if C.sha(SOCKET_EXTENSION) != SOCKET_EXTENSION_SHA256:
        raise SystemExit('_socket pin mismatch')
    # Widened by exactly the _socket extension so the kernel rules, not import absence, are tested.
    results['probe-network-widened'] = probe_run(grants, 'network', True, extra_extensions=[SOCKET_EXTENSION])
    results['control-probe-network'] = probe_run(grants, 'network', False)
    # Is file-map-executable enforced for dlopen of a readable non-system extension on this host?
    results['probe-network-widened-without-map'] = probe_run(grants, 'network', True, extra_extensions=[SOCKET_EXTENSION],
                                                             map_executable=False, suffix='-without-map')
    results['collectionAfterProbe'], _ = collect(collector, C.RUNS / 'negative-probe-main/output')

    def ablation(label, flags=C.FLAGS, reads=None, map_executable=True, prefill=False, exe=None):
        output = fresh(C.RUNS / label / 'output')
        if prefill:
            (output / 'stale.json').write_text('{}\n')
        text = C.profile(grants, reads=reads or C.child_reads(), output=output, map_executable=map_executable)
        argv = entry_argv(output, flags=flags) if exe is None else exe
        record = C.run(label, argv, text=text)
        record['outputEntries'] = sorted(p.name for p in output.iterdir())
        return record
    results['withoutIsolatedFlag'] = ablation('negative-without-I', flags=['-B', '-S'])
    results['withoutNoSiteFlag'] = ablation('negative-without-S', flags=['-I', '-B'])
    results['withoutBytecodeFlag'] = ablation('negative-without-B', flags=['-I', '-S'])
    results['withoutMapExecutable'] = ablation('negative-without-map-executable', map_executable=False)
    results['withoutRuntimeVocabularyGrant'] = ablation('negative-without-runtime-grant', reads=C.child_reads(runtime=False))
    results['nonEmptyOutputRoot'] = ablation('negative-nonempty-output', prefill=True)
    results['undeclaredExec'] = ablation('negative-undeclared-exec', exe=['/bin/sh', '-c', 'echo ran'])
    results['launcherStubExec'] = ablation('negative-launcher-stub',
                                           exe=[C.FRAMEWORK / 'bin/python3.14', *C.FLAGS, '-c', 'print("ran")'])
    results['canaryUnchanged'] = CANARY.read_text() == 'outside secret\n'
    results['forbiddenOutsideAbsent'] = {p: not Path(p).exists() for p in FORBIDDEN_OUTSIDE}
    return results


def main():
    if len(sys.argv) != 1 or not sys.flags.isolated:
        raise SystemExit('usage: python3 -I -B scripts/run_trial.py')
    grants = C.load_grants()
    collector, collector_sha = load_collector()
    before = C.tree(C.WORK)
    result = {'standing': 'macOS development-trusted-host Python preparation confinement author/probe trial; '
                          'not approval, not hermetic, not product integration',
              'host': subprocess.run(['/usr/bin/sw_vers'], capture_output=True, text=True).stdout,
              'collector': {'path': str(CANDIDATE), 'sha256': collector_sha},
              'positive': positive(grants, collector),
              'negative': negatives(grants, collector)}
    result['workTreeUnchanged'] = C.tree(C.WORK) == before
    result['grantsStillPinned'] = bool(C.load_grants())
    (C.LOGS / 'results.json').write_text(json.dumps(result, indent=1) + '\n')
    p = result['positive']
    print(json.dumps({'positiveExit': {k: p[k]['exitCode'] for k in ('confined-1', 'confined-2', 'unconfined-entry')},
                      'positiveDenials': {k: p[k].get('sandboxDenials') for k in ('confined-1', 'confined-2')},
                      'parity': p['parity'], 'workTreeUnchanged': result['workTreeUnchanged']}, indent=1))


if __name__ == '__main__':
    main()
