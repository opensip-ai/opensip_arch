"""Q0 r13 fresh own-root slot execution component, not a Q6 driver.

The caller prepares and authorizes each invocation and owns reset/cache policy,
collectors, exclusive reaping, input identity and any operational record capture.
This component executes the named slot schedule only. Darwin settlement/charged
memory remain unverified, and no operational record is captured here.
"""
from dataclasses import dataclass

from canonical import canonical
from records import require
from measurement import summarize_slots
from root_observation import observe_root


@dataclass(frozen=True)
class Invocation:
    argv: tuple
    cwd: str
    environment: dict
    stdout_fd: int
    stderr_fd: int
    timeout_nanos: int


def observe_slots(reset, prepare):
    """Execute one fresh root per slot; retain failed slots without retry.

    prepare(slot) supplies one Invocation just before that root is launched.
    Its reset/caches/instrumentation/input claims are not attested here. It must
    not return a provider process to reuse; the mechanism creates each root.
    A preparation or reaping exception aborts this operation and propagates;
    no fabricated observation or complete batch is returned for that slot.
    """
    require(type(reset) is str and reset in {"cold", "warm"}, "RESET_REQUIRED")
    require(callable(prepare), "INVOCATION_PREPARATION_REQUIRED")
    slots = ([{"kind": "priming", "index": 0}] if reset == "warm" else [])
    slots += [{"kind": "warmup", "index": i} for i in range(3)]
    slots += [{"kind": "measured", "index": i} for i in range(7)]
    observations, evidence = [], []
    for slot in slots:
        invocation = prepare(dict(slot))
        require(type(invocation) is Invocation, "INVOCATION_REQUIRED")
        observed = observe_root(invocation.argv, cwd=invocation.cwd,
                                environment=invocation.environment,
                                stdout_fd=invocation.stdout_fd,
                                stderr_fd=invocation.stderr_fd,
                                timeout_nanos=invocation.timeout_nanos)
        row = observed.slot_evidence(slot)
        row["reasons"] = sorted(set(row["reasons"]) | {"record-missing"},
                                key=canonical)
        observations.append((dict(slot), observed))
        evidence.append(row)
    return observations, summarize_slots(reset, evidence)
