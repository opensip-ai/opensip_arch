"""Untrusted stand-in for prepare.py: attempts effects outside the preparation grants.

The runner substitutes __CFG__ and places this file as CODE_DIR/prepare.py, so
prepare-inputs.py loads and calls it exactly like the real one. Results are
printed to stdout, the only outbound channel the parent provides. It never
writes the three prepared files through the sink, so the entry exits nonzero.
"""
import json
import os
import sys

CFG = json.loads(__CFG__)


def attempt(action):
    try:
        return {'result': 'ALLOWED', 'detail': action()}
    except BaseException as error:
        return {'result': type(error).__name__, 'errno': getattr(error, 'errno', None)}


def read(path):
    def action():
        fd = os.open(path, os.O_RDONLY)
        try:
            return len(os.read(fd, 64))
        finally:
            os.close(fd)
    return action


def open_for_write(path, flags):
    def action():
        # Opening for write is the checked operation; zero bytes are written.
        os.close(os.open(path, os.O_WRONLY | flags, 0o644))
        return True
    return action


def waited(pid):
    os.waitpid(pid, 0)
    return pid > 0


def fork():
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    return waited(pid)


def report(results):
    print(json.dumps({CFG['mode']: results}, sort_keys=True), flush=True)


def main_probe():
    output, results = CFG['output'], {}
    results['rmdirOutputRoot'] = attempt(lambda: os.rmdir(output))
    if results['rmdirOutputRoot']['result'] == 'ALLOWED':
        os.mkdir(output)
    results['chmodOutputRoot'] = attempt(lambda: os.chmod(output, os.stat(output).st_mode & 0o7777))
    for key, path in CFG['reads'].items():
        results['read:' + key] = attempt(read(path))
    for key, path in CFG['stats'].items():
        results['stat:' + key] = attempt(lambda path=path: os.stat(path).st_size)
    for key, path in CFG['lists'].items():
        results['list:' + key] = attempt(lambda path=path: len(os.listdir(path)))
    for key, path in CFG['creates'].items():
        results['create:' + key] = attempt(open_for_write(path, os.O_CREAT | os.O_EXCL))
    for key, path in CFG['writes'].items():
        results['writeOpen:' + key] = attempt(open_for_write(path, os.O_APPEND))
    canary = CFG['reads']['canary']
    results['hardlinkCanaryIntoOutput'] = attempt(lambda: os.link(canary, os.path.join(output, 'rust-projection.json')))
    results['symlinkCanaryAsOwners'] = attempt(lambda: os.symlink(canary, os.path.join(output, 'owners.json')))
    results['readThroughSymlink'] = attempt(read(os.path.join(output, 'owners.json')))
    results['undeclaredOutput'] = attempt(open_for_write(os.path.join(output, 'targets.json'), os.O_CREAT | os.O_EXCL))
    for name in ('subprocess', 'socket', '_socket', '_ctypes', 'site', 'ssl', 'pip', 'yaml'):
        results['import:' + name] = attempt(lambda name=name: bool(__import__(name)))
    results['fork'] = attempt(fork)
    results['posixSpawnSh'] = attempt(lambda: waited(os.posix_spawn('/bin/sh', ['/bin/sh', '-c', 'exit 0'], {})))
    results['posixSpawnSelf'] = attempt(lambda: waited(os.posix_spawn(sys.executable, [sys.executable, '-I', '-S', '-c', 'pass'], {})))
    results['osSystem'] = attempt(lambda: os.system('exit 0'))
    results['info'] = {
        'environ': sorted(os.environ), 'getcwd': attempt(os.getcwd)['result'],
        'hostnameReadable': attempt(lambda: bool(os.uname().nodename))['result'],
        'usernameLookup': attempt(lambda: bool(__import__('pwd').getpwuid(os.getuid()).pw_name))['result'],
        'cpuCount': attempt(lambda: os.cpu_count() is not None)['result'],
        'openFds': attempt(lambda: sorted(os.listdir('/dev/fd')))['detail'],
        'sysPath': sys.path, 'siteLoaded': 'site' in sys.modules,
        'bytecodeWritten': attempt(lambda: sys.dont_write_bytecode)['detail']}
    report(results)


def network_probe():
    import _socket
    results = {}

    def tcp():
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect(('127.0.0.1', CFG['tcpPort']))
            return True
        finally:
            s.close()

    def udp():
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        try:
            return s.sendto(b'probe', ('127.0.0.1', CFG['udpPort']))
        finally:
            s.close()

    def listen():
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        try:
            s.bind(('127.0.0.1', 0))
            s.listen()
            return True
        finally:
            s.close()

    def syslog():
        s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_DGRAM)
        try:
            s.connect('/private/var/run/syslog')  # connect only; nothing is sent
            return True
        finally:
            s.close()
    results['tcpConnectLoopback'] = attempt(tcp)
    results['udpSendLoopback'] = attempt(udp)
    results['tcpListenLoopback'] = attempt(listen)
    results['unixConnectSyslog'] = attempt(syslog)
    report(results)


def exec_probe():
    report({'execShNext': True})
    result = attempt(lambda: os.execv('/bin/sh', ['/bin/sh', '-c', 'echo \'{"exec": {"shExecRan": true}}\'']))
    print(json.dumps({'exec': {'execSh': result}}), flush=True)
    # Python 3.14 -c imports linecache (not granted), so re-exec the entry script itself
    # with the outside canary as its raw-schemas input: stderr shows whether the
    # replacement image ran and whether it is still confined.
    argv = [sys.executable, '-I', '-B', '-S', CFG['entry'], CFG['reads']['canary'], CFG['options'], CFG['code'], CFG['output']]
    result = attempt(lambda: os.execv(sys.executable, argv))
    print(json.dumps({'exec': {'execSelf': result}}), flush=True)


def prepare(documents, options, destination):
    {'main': main_probe, 'network': network_probe, 'exec': exec_probe}[CFG['mode']]()
