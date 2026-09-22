"""Conditional reference assembly, not a native observer or product renderer.

The caller supplies an already admitted complete-root observation and already
admitted DomainDetail values. Input schemas and source pins are checked by the
companion checker. No filesystem, trust, custody or native capability is inferred.
"""
from copy import deepcopy

INFO = 'INSTALLATION.DURABILITY_NOT_CHECKED'
NOTICE = {
    'code': INFO,
    'remedy': 'The complete installation is visible; root durability was not checked by this read-only command.',
}


class ReportUnavailable(Exception):
    pass


class DoctorSession:
    """A conditional report session with an explicit failure latch."""

    def __init__(self, workflow):
        self.workflow = workflow
        self.failed = False

    def assemble(self, complete_root, actual_details, *, report_producible=True):
        if self.failed:
            raise ReportUnavailable('report session already failed')
        limit = 255 if complete_root else 256
        if (not report_producible or len(actual_details) > limit
                or any(detail['code'] == INFO for detail in actual_details)):
            self.failed = True
            raise ReportUnavailable('bounded report unavailable')
        details = deepcopy(actual_details)
        if complete_root:
            details.append(deepcopy(NOTICE))
        return self.workflow['doctor'](True, details)

    def unavailable_projection(self):
        if not self.failed:
            raise ValueError('no failed report session')
        return self.workflow['doctor'](False, [])


def project_doctor(workflow, command, result, termination, request_id, offline_window):
    """Use the selected render reference and explicit existing parity fields.

offline_window is an admitted security projection supplied by the caller. This
adapter performs no security observation. Outputs are reference projections;
they are not bytes emitted by the product's currently metadata-only renderer.
"""
    envelope = {
        'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 7,
        'kind': 'doctor', 'requestId': request_id,
        'termination': termination, 'exitCode': workflow['exit_code'](termination),
        'doctor': result,
    }
    parity = {
        'report-produced': result['reportProduced'], 'outcome': termination,
        'defects-found': result['defectsFound'], 'defects': result['defects'],
        'offline-window': offline_window, 'termination-class': termination['class'],
    }
    projections = [workflow['render']({'envelope': envelope, 'parity': parity}, fmt, command)
                   for fmt in command['formats']]
    for projection in projections:
        if projection['format'] == 'human':
            for detail in result['defects']:
                if detail['code'] == INFO:
                    projection['lines'].append('Informational: durability not checked')
    return envelope, projections
