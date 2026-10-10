"""Experimental compiler-information queries; no Cargo or native admission.

Caller pins, target lists, cwd and output directories are supplied experiment
data. They are not authenticated capabilities. There is no cache or retry.
No output is interpreted as a signed toolchain table or semantic version.
"""
from dataclasses import asdict, dataclass
import hashlib
import os
from pathlib import Path
import re
import stat

from root_observation import observe_root
from selected_projection import rustflags_projection


HEAD = ('-', '--crate-name', '___', '--print=file-names')
TAIL = ('--crate-type', 'bin', '--crate-type', 'rlib', '--crate-type',
        'dylib', '--crate-type', 'cdylib', '--crate-type', 'staticlib',
        '--crate-type', 'proc-macro', '--print=sysroot',
        '--print=split-debuginfo', '--print=crate-name', '--print=cfg',
        '-Wwarnings')


@dataclass(frozen=True)
class Query:
    kind: str
    target: str | None = None
    original_flags: tuple = ()
    snapshot_paths: tuple = ()
    closure_paths: tuple = ()

    def arguments(self, experimental_targets):
        if self.kind == 'version':
            if self.target is not None or self.original_flags or self.snapshot_paths or self.closure_paths:
                raise ValueError('VERSION_HAS_EXTRA_INPUTS')
            return ('-vV',), None
        if self.kind not in ('host-info', 'target-info'):
            raise ValueError('QUERY_KIND_UNSUPPORTED')
        if not all(type(v) is str and '\0' not in v for v in self.original_flags):
            raise ValueError('FLAG_DATA_INVALID')
        projection = rustflags_projection(list(self.original_flags),
                                         set(self.snapshot_paths),
                                         set(self.closure_paths))
        if self.kind == 'host-info':
            if self.target is not None:
                raise ValueError('HOST_HAS_TARGET')
            target_args = ()
        else:
            # This narrower prototype supports explicitly listed built-in
            # triples only. It publishes no native target admission rule.
            if type(self.target) is not str or not re.fullmatch(r'[A-Za-z0-9_-]+', self.target) or self.target not in experimental_targets:
                raise ValueError('EXPERIMENTAL_TARGET_UNSUPPORTED')
            target_args = ('--target', self.target)
        return HEAD + tuple(projection['honored']) + target_args + TAIL, projection


def file_pin(path):
    """Stream a regular, final-component non-symlink file and retain a stamp.

    Pre/post descriptor and path stamps catch observed mutation. They do not
    seal ancestors, remove races or authenticate a runtime closure.
    """
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('PIN_NOT_REGULAR')
        h = hashlib.sha256()
        size = 0
        while chunk := os.read(fd, 1024 * 1024):
            size += len(chunk)
            h.update(chunk)
        after = os.fstat(fd)
        stamp = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if stamp(before) != stamp(after) or stamp(after) != stamp(path.lstat()) or size != after.st_size:
            raise ValueError('PIN_OBSERVATION_CHANGED')
        return {'path': str(path), 'bytes': size, 'sha256': h.hexdigest(),
                'observedStamp': list(stamp(after))}
    finally:
        os.close(fd)


def run_query(query, *, executable, expected_pin, attempt_label, cwd,
              output_directory, ordinal, experimental_targets, timeout_nanos):
    """One exact information query through the accepted Darwin root helper.

    Real env={}, EOF stdin, close_fds; only fresh exclusive collector files.
    Caller supplies the deadline. Files remain retained even on failure.
    Output byte totals are observations, not hard output or scratch bounds.
    Root-only wait4 is not descendant settlement or workload-tree RSS.
    """
    executable = Path(executable)
    if not executable.is_absolute() or type(attempt_label) is not str or not attempt_label:
        raise ValueError('EXPERIMENT_ASSOCIATION_INVALID')
    if type(ordinal) is not int or ordinal < 0:
        raise ValueError('ORDINAL_INVALID')
    if type(timeout_nanos) is not int or timeout_nanos <= 0:
        raise ValueError('DEADLINE_INVALID')
    args, projection = query.arguments(experimental_targets)
    before = file_pin(executable)
    if (before['bytes'], before['sha256']) != (expected_pin['bytes'], expected_pin['sha256']):
        raise ValueError('EXECUTABLE_PIN_MISMATCH')
    cwd = Path(cwd)
    output_directory = Path(output_directory)
    for p in (cwd, output_directory):
        if not p.is_absolute() or p.is_symlink() or not p.is_dir():
            raise ValueError('EXPERIMENT_DIRECTORY_INVALID')
    paths = [output_directory / f'query-{ordinal}.{stream}' for stream in ('stdout', 'stderr')]
    descriptors = []
    try:
        for p in paths:
            descriptors.append(os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600))
        observed = observe_root((str(executable),) + args, cwd=cwd,
                                environment={}, stdout_fd=descriptors[0],
                                stderr_fd=descriptors[1], timeout_nanos=timeout_nanos)
    finally:
        for fd in descriptors:
            os.close(fd)
    after = file_pin(executable)
    if before != after:
        raise ValueError('EXECUTABLE_OBSERVATION_CHANGED')
    return {'attemptLabel': attempt_label, 'query': asdict(query),
            'argv': [str(executable), *args], 'environment': {}, 'cwd': str(cwd),
            'executableObservation': before, 'projection': projection,
            'rootObservation': asdict(observed),
            'stdout': file_pin(paths[0]), 'stderr': file_pin(paths[1]),
            'cacheReuse': False, 'retry': False, 'nativeAdmission': False,
            'fullQueryPopulation': False, 'SMComplete': False}
