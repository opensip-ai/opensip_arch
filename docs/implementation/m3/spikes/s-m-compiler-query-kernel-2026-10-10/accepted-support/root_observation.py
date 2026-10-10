"""Q0 r13 Darwin root observations, never workload-tree settlement.

The harness caller owns and authorizes the command, cwd, environment and output
collectors. This is not a provider launcher, closure admission, cold/warm reset,
operational-record admission, descendant reaper or Q6 measurement mechanism.
Only this call's fresh root is waited for and, on deadline, killed. Darwin's
required unavailable-platform reasons remain present even on a successful root.
"""
from dataclasses import dataclass
import os
import subprocess
import signal
import sys
import time

from canonical import canonical
from records import require
from measurement import _slot


@dataclass(frozen=True)
class RootObservation:
    pid: int | None
    returncode: int | None
    root_reaped_elapsed_nanos: int | None
    rss_native: int | None
    launch_errno: int | None
    timed_out: bool

    def slot_evidence(self, slot):
        """Supply only existing QD-27 accounting fields, not a full envelope."""
        kind, _ = _slot(slot)
        reasons = {'settlement-unverified-platform',
                   'memory-peak-unavailable-platform'}
        if self.pid is None or self.returncode != 0:
            reasons.add('run-failed')
        if self.timed_out:
            reasons.add('timeout')
        row = {'slot': dict(slot), 'reasons': sorted(reasons, key=canonical)}
        if kind == 'measured':
            row.update(elapsedNanos=None, cgroupMemoryPeakBytes=None,
                       rootReapedElapsedNanos=self.root_reaped_elapsed_nanos)
        return row


def observe_root(argv, *, cwd, environment, stdout_fd, stderr_fd,
                 timeout_nanos):
    """Execute one caller-authorized root with EOF stdin and closed extra fds.

    The caller must exclusively own this root's reaping; an external wait or
    SIGCHLD reaper cannot be combined with this operation.
    The deadline is supplied by the owning harness, not a new safety constant.
    wait4's native macOS ru_maxrss is informational bytes. A root that was
    created and reaped retains its actual elapsed time even on failure/timeout.
    Launch errors retain only errno; arbitrary exception/stderr text is not
    copied into this observation. Output collection stays with the caller.
    """
    require(sys.platform == 'darwin', 'DARWIN_ROOT_OBSERVATION_REQUIRED')
    require(type(argv) in (list, tuple) and len(argv) > 0 and
            all(type(arg) is str and '\x00' not in arg for arg in argv) and
            os.path.isabs(argv[0]), 'ABSOLUTE_COMMAND_REQUIRED')
    require(type(environment) is dict and all(
        type(k) is str and type(v) is str and k and '=' not in k and
        '\x00' not in k and '\x00' not in v for k, v in environment.items()),
        'EXPLICIT_ENVIRONMENT_REQUIRED')
    require(type(timeout_nanos) is int and timeout_nanos > 0,
            'POSITIVE_DEADLINE_REQUIRED')
    require(all(type(fd) is int and fd >= 0 for fd in (stdout_fd, stderr_fd)),
            'OUTPUT_COLLECTOR_FDS_REQUIRED')
    start = time.monotonic_ns()
    try:
        child = subprocess.Popen(argv, cwd=cwd, env=environment,
                                 stdin=subprocess.DEVNULL,
                                 stdout=stdout_fd, stderr=stderr_fd,
                                 close_fds=True, start_new_session=True)
    except OSError as exc:
        return RootObservation(None, None, None, None, exc.errno, False)
    timed_out = False
    try:
        while True:
            try:
                pid, status, usage = os.wait4(child.pid, os.WNOHANG)
            except InterruptedError:
                continue
            if pid:
                break
            remaining = timeout_nanos - (time.monotonic_ns() - start)
            if remaining <= 0:
                timed_out = True
                # This unreaped root still owns its pid; do not signal another
                # process or claim that killing the root settles descendants.
                os.kill(child.pid, signal.SIGKILL)
                while True:
                    try:
                        pid, status, usage = os.wait4(child.pid, 0)
                        break
                    except InterruptedError:
                        continue
                break
            time.sleep(min(remaining / 1_000_000_000, 0.005))
    except ChildProcessError:
        # Reaping ownership was lost. Do not signal a possibly reused pid.
        raise
    except BaseException:
        # Reap only the process created here before propagating interruption.
        os.kill(child.pid, signal.SIGKILL)
        while True:
            try:
                _, status, _ = os.wait4(child.pid, 0)
                child.returncode = os.waitstatus_to_exitcode(status)
                break
            except InterruptedError:
                continue
        raise
    finish = time.monotonic_ns()
    child.returncode = os.waitstatus_to_exitcode(status)
    require(pid == child.pid and 1 <= finish - start <= 2**64 - 1,
            'ROOT_REAP_OBSERVATION_INVALID')
    rss = usage.ru_maxrss
    require(type(rss) is int and 0 <= rss <= 2**64 - 1,
            'NATIVE_RSS_OBSERVATION_INVALID')
    return RootObservation(child.pid, child.returncode, finish - start,
                           rss, None, timed_out)
