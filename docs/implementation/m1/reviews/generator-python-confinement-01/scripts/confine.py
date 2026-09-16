"""Shared host constants, profile rendering and confined-run recording for this trial.

Parent-side tooling only. Writes only below the trial directory.
"""
import hashlib, json, re, subprocess, time
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
WORK = TRIAL / 'work'
ENTRY = WORK / 'entry/prepare-inputs.py'
CODE = WORK / 'code'
INPUTS = WORK / 'inputs'
RUNS = TRIAL / 'runs'
LOGS = TRIAL / 'logs'
GRANTS = LOGS / 'python-grants.json'
SANDBOX_EXEC = '/usr/bin/sandbox-exec'

# Explicit trusted host profile: Homebrew python@3.14 3.14.6 framework build.
# bin/python3.14 is only a launcher that posix_spawns Python.app, so the child
# executes the Python.app binary directly and no second exec is granted.
FRAMEWORK = Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14')
EXECUTABLE = FRAMEWORK / 'Resources/Python.app/Contents/MacOS/Python'
LIBRARY = FRAMEWORK / 'Python'
STDLIB = FRAMEWORK / 'lib/python3.14'
HOST_PINS = {str(EXECUTABLE): '0c9a985712bb1235d8fe474a6a99810dc118bcae0dfb429a237aac0c907fa3af',
             str(LIBRARY): '696ffa2cf9562522c387f7c2b3a990ef67e574df2d921822fe310ea35587cce0'}
FLAGS = ['-I', '-B', '-S']
EMITTED = ('owners.json', 'rust-projection.json', 'ts-projection.json')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def quote(path):
    return json.dumps(str(path))


def verify_host():
    for path, expected in HOST_PINS.items():
        if Path(path).is_symlink() or sha(path) != expected:
            raise SystemExit('host interpreter pin mismatch: ' + path)


def load_grants():
    verify_host()
    grants = json.loads(GRANTS.read_text())
    for row in grants['sources'] + grants['extensions']:
        path = Path(row['path'])
        if path.is_symlink() or not path.is_file() or sha(path) != row['sha256']:
            raise SystemExit('stdlib grant pin mismatch: ' + row['path'])
    for directory in grants['directories']:
        if Path(directory).is_symlink() or not Path(directory).is_dir():
            raise SystemExit('stdlib directory grant changed: ' + directory)
    return grants


def child_reads(code=CODE, runtime=True):
    reads = [ENTRY, INPUTS / 'raw-schemas.json', INPUTS / 'options.json', code / 'prepare.py']
    return reads + ([code / 'runtime/schema.ts'] if runtime else [])


def profile(grants, *, reads, output, discovery=False, extra_extensions=(), map_executable=True):
    """Deny-default preparation child profile. Apple's system.sb supplies the trusted
    dyld/libSystem/CoreFoundation runtime rules; every other grant is explicit."""
    if discovery:
        interpreter = [f'(subpath {quote(STDLIB)})']
        native = [f'(subpath {quote(STDLIB / "lib-dynload")})']
        ancestors = [STDLIB]
    else:
        files = [row['path'] for row in grants['sources'] + grants['extensions']] + [str(p) for p in extra_extensions]
        interpreter = [f'(literal {quote(p)})' for p in files + grants['directories']]
        native = [f'(literal {quote(row["path"])})' for row in grants['extensions']] + \
                 [f'(literal {quote(p)})' for p in extra_extensions]
        ancestors = files + grants['directories']
    lines = ['(version 1)', '(deny default)', '(import "system.sb")',
             ';; system.sb exposes these account files; preparation never needs them',
             '(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))',
             '(deny file-write* (subpath "/cores"))',
             f'(allow process-exec (literal {quote(EXECUTABLE)}))',
             ';; trusted host interpreter: pinned Python.app binary, framework dylib and the exact imported stdlib',
             ';; (no site-packages, no __pycache__: -B plus denied .pyc reads force source loading)',
             f'(allow file-read* (literal {quote(EXECUTABLE)}) (literal {quote(LIBRARY)}) ' + ' '.join(interpreter) + ')']
    if map_executable:
        lines += [';; scope for non-system native code; observed NOT enforced on 25G83 (ablation), read grants gate loading',
                  f'(allow file-map-executable (literal {quote(LIBRARY)}) ' + ' '.join(native) + ')']
    lines += [';; parent-designated read-only entry, inputs and code (only the selected runtime vocabulary)',
              '(allow file-read* ' + ' '.join(f'(literal {quote(p)})' for p in reads) + ')',
              ';; empty output root: its contents, never the root entry itself (no rmdir/replace/chmod)',
              f'(allow file-read* (subpath {quote(output)}))',
              f'(allow file-write* (require-all (subpath {quote(output)}) (require-not (literal {quote(output)}))))',
              ';; getpath prefix landmark (stat only; os itself is frozen in the dylib)',
              f'(allow file-read-metadata (literal {quote(STDLIB / "os.py")}))',
              ';; realpath/getpath lstat ancestor directories (metadata only, no siblings)',
              '(allow file-read-metadata ' + ' '.join(f'(path-ancestors {quote(p)})'
                                                     for p in [EXECUTABLE, LIBRARY, *ancestors, *reads, output]) + ')']
    return '\n'.join(lines) + '\n'


def denials(pid, start, end):
    """Kernel sandbox violation reports for one child pid (sandbox-exec execs in place).
    Reports can be deduplicated or rate limited; absence is not proof of no attempt."""
    time.sleep(1.5)
    fmt = '%Y-%m-%d %H:%M:%S'
    text = subprocess.run(['/usr/bin/log', 'show', '--style', 'compact', '--start', time.strftime(fmt, time.localtime(start - 1)),
                           '--end', time.strftime(fmt, time.localtime(end + 2)), '--predicate', 'sender == "Sandbox"'],
                          capture_output=True, text=True, timeout=180).stdout
    marker = f'({pid}) deny('
    return sorted({re.sub(r'^.*?\) (deny\(\d+\) )', r'\1', line) for line in text.splitlines() if marker in line})


def run(label, argv, *, text=None, cwd=None, env=None, timeout=180, logs=True):
    """Run argv (confined when a profile text is given) with pipes, stdin=/dev/null, empty env."""
    directory = RUNS / label
    directory.mkdir(parents=True, exist_ok=True)
    command = list(map(str, argv))
    if text is not None:
        (directory / 'profile.sb').write_text(text)
        command = [SANDBOX_EXEC, '-f', str(directory / 'profile.sb'), *command]
    cwd = cwd or directory / 'cwd'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    start = time.time()
    process = subprocess.Popen(command, cwd=cwd, env={} if env is None else env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
    end = time.time()
    record = {'label': label, 'confined': text is not None, 'argv': command, 'cwd': str(cwd),
              'exitCode': process.returncode, 'stdout': stdout.decode('utf-8', 'replace')[-20000:],
              'stderr': stderr.decode('utf-8', 'replace')[-4000:]}
    if text is not None and logs:
        record['sandboxDenials'] = denials(process.pid, start, end)
    (directory / 'record.json').write_text(json.dumps(record, indent=1) + '\n')
    return record


def tree(root):
    root = Path(root)
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
