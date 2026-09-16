"""Reference timing semantics over already admitted, host-owned attempts.

These pure helpers establish no RequestId/ExecutionId custody and do not read
clocks or write a journal. Production measurement must remain inside the host.
"""
U64_MAX = 18446744073709551615
OUTCOMES = frozenset(('completed', 'rejected', 'failed', 'cancelled', 'abandoned'))
CLOCK_REASONS = frozenset(('clock-unavailable', 'clock-regressed', 'duration-overflow'))


class TimingRefusal(ValueError):
    pass


def unavailable(reason):
    return {'state': 'unavailable', 'reason': reason}


def admit_duration(outcome, value):
    if outcome not in OUTCOMES or type(value) is not dict:
        raise TimingRefusal('invalid duration input')
    if value.get('state') == 'measured':
        if set(value) != {'state', 'milliseconds'} or type(value['milliseconds']) is not int or not 0 <= value['milliseconds'] <= U64_MAX or outcome == 'abandoned':
            raise TimingRefusal('invalid measured duration')
    elif value.get('state') == 'unavailable':
        allowed = {'supervisor-lost'} if outcome == 'abandoned' else CLOCK_REASONS
        if set(value) != {'state', 'reason'} or type(value.get('reason')) is not str or value['reason'] not in allowed:
            raise TimingRefusal('invalid unavailability reason for attempt')
    else:
        raise TimingRefusal('unknown duration state')


def observe_terminal(outcome, start_ns, end_ns):
    """Consume private observations from the SAME host monotonic clock lifetime.

    None represents a missing/failed clock sample. Origin values are not stored.
    Recovery never subtracts its clock from the dead supervisor's clock.
    """
    if outcome not in OUTCOMES:
        raise TimingRefusal('invalid outcome')
    if outcome == 'abandoned':
        return unavailable('supervisor-lost')
    if start_ns is None or end_ns is None:
        return unavailable('clock-unavailable')
    if type(start_ns) is not int or type(end_ns) is not int:
        raise TimingRefusal('clock samples must be exact integer nanoseconds')
    if end_ns < start_ns:
        return unavailable('clock-regressed')
    milliseconds = (end_ns - start_ns) // 1_000_000
    if milliseconds > U64_MAX:
        return unavailable('duration-overflow')
    return {'state': 'measured', 'milliseconds': milliseconds}


def project_attempt(source_major, attempt):
    """Map a terminal attempt already admitted under its original schema.

    No cross-major schema admission or current clock lookup occurs here.
    Caller binds the exact retained InvocationRecord, StepId and ExecutionId.
    """
    if type(source_major) is not int or source_major not in (3, 4):
        raise TimingRefusal('unsupported invocation source major')
    if source_major == 3:
        if 'observedDuration' in attempt:
            raise TimingRefusal('v3 does not own a duration field')
        value = unavailable('not-retained')
    else:
        if 'observedDuration' not in attempt:
            raise TimingRefusal('v4 missing observed duration')
        value = attempt['observedDuration']
        admit_duration(attempt['outcome'], value)
    return {'executionId': attempt['executionId'], 'sourceSchemaMajor': source_major,
            'duration': dict(value)}


def summarize_attempts(projections):
    """Sum terminal-attempt service observations, NEVER step wall time.

    No attempts means no observation, not a measured zero. Partial history and
    an in-progress current attempt remain separately disclosed by the ledger.
    """
    if len(projections) > 3:
        raise TimingRefusal('attempt budget exceeded')
    if not projections:
        return {'state': 'no-attempts', 'attemptCount': 0}
    missing = sum(p['duration']['state'] == 'unavailable' for p in projections)
    if missing:
        return {'state': 'unavailable', 'attemptCount': len(projections),
                'unavailableAttemptCount': missing, 'reason': 'incomplete-observations'}
    total = sum(p['duration']['milliseconds'] for p in projections)
    if total > U64_MAX:
        return {'state': 'unavailable', 'attemptCount': len(projections),
                'unavailableAttemptCount': 0, 'reason': 'duration-overflow'}
    return {'state': 'measured', 'attemptCount': len(projections), 'milliseconds': total}
