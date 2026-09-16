"""Reference timing semantics over already admitted, host-owned attempts.

These pure helpers establish no RequestId/ExecutionId custody and do not read
clocks or write a journal. Production measurement must remain inside the host.
"""
import re

U64_MAX = 18446744073709551615
OUTCOMES = frozenset(('completed', 'rejected', 'failed', 'cancelled', 'abandoned'))
CLOCK_REASONS = frozenset(('clock-unavailable', 'clock-regressed', 'duration-overflow'))


class TimingRefusal(ValueError):
    pass


def unavailable(reason):
    return {'state': 'unavailable', 'reason': reason}


def admit_duration(outcome, value):
    if type(outcome) is not str or outcome not in OUTCOMES or type(value) is not dict:
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
    if type(outcome) is not str or outcome not in OUTCOMES:
        raise TimingRefusal('invalid outcome')
    for sample in (start_ns, end_ns):
        if sample is not None and type(sample) is not int:
            raise TimingRefusal('clock samples must be exact integer nanoseconds')
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


def source_support(source_major):
    if type(source_major) is not int or source_major < 1:
        raise TimingRefusal('malformed invocation source major')
    if source_major not in (3, 4):
        return {'state': 'incompatible', 'reason': 'retained-schema-major-unsupported'}
    return {'state': 'supported', 'sourceSchemaMajor': source_major}


def project_attempt(source_major, attempt):
    """Map a terminal attempt already admitted under its original schema.

    No cross-major schema admission or current clock lookup occurs here.
    Caller binds the exact retained InvocationRecord, StepId and ExecutionId.
    """
    if type(attempt) is not dict or not valid_execution_id(attempt.get('executionId')) or type(attempt.get('outcome')) is not str or attempt['outcome'] not in OUTCOMES:
        raise TimingRefusal('malformed admitted attempt projection source')
    if source_support(source_major)['state'] != 'supported':
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
            'outcome': attempt['outcome'], 'duration': dict(value)}


def valid_execution_id(value):
    return type(value) is str and re.fullmatch(r'exec1_[0-9a-f]{32}', value) is not None


def admit_projection(value):
    if type(value) is not dict or set(value) != {'executionId', 'sourceSchemaMajor', 'outcome', 'duration'} or not valid_execution_id(value['executionId']):
        raise TimingRefusal('invalid timing projection shape')
    major, outcome, duration = value['sourceSchemaMajor'], value['outcome'], value['duration']
    if type(major) is not int or major not in (3, 4) or type(outcome) is not str or outcome not in OUTCOMES:
        raise TimingRefusal('invalid timing projection source')
    if major == 3:
        if type(duration) is not dict or duration != unavailable('not-retained'):
            raise TimingRefusal('invalid legacy duration')
    else:
        admit_duration(outcome, duration)


def summarize_attempts(projections):
    """Sum terminal-attempt service observations, NEVER step wall time.

    No attempts means no observation, not a measured zero. Partial history and
    an in-progress current attempt remain separately disclosed by the ledger.
    """
    if type(projections) is not list:
        raise TimingRefusal('attempt projections must be an array')
    if len(projections) > 3:
        raise TimingRefusal('attempt budget exceeded')
    seen = set()
    for projection in projections:
        pass
        if projection['executionId'] in seen:
            raise TimingRefusal('duplicate ExecutionId')
        seen.add(projection['executionId'])
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
