"""Explicit bounded history selection; host custody precedes lookup."""
import copy
import re

MAX_RUNS = 4
RUN_ID = re.compile(r'run3:[0-9a-f]{64}')
REMEDY = 'Use one to four distinct full Run IDs with --format html.'


class HistoryRefusal(ValueError):
    def __init__(self):
        super().__init__('REPORT.HISTORY_SELECTION_INVALID')


class HistorySourceRefusal(ValueError):
    """Internal projection/source mismatch, never a user request rejection."""
    def __init__(self):
        super().__init__('REPORT-HISTORY.SOURCE-MISMATCH')


def valid_run_id(value):
    return type(value) is str and RUN_ID.fullmatch(value) is not None


def admit_request(run_ids, output_format):
    if (output_format != 'html' or type(run_ids) is not list or not 1 <= len(run_ids) <= MAX_RUNS
            or any(not valid_run_id(r) for r in run_ids) or len(set(run_ids)) != len(run_ids)):
        raise HistoryRefusal()
    return {'mode': 'explicit', 'runIds': list(run_ids)}


def plan_selection(request, current_run_id):
    if type(request) is not dict or set(request) != {'mode', 'runIds'} or request['mode'] != 'explicit':
        raise HistoryRefusal()
    admitted = admit_request(request['runIds'], 'html')
    if current_run_id is not None and not valid_run_id(current_run_id):
        raise HistoryRefusal()
    return {'policy': 'explicit-run-ids.1', 'requestedRunIds': admitted['runIds'],
            'currentRunId': current_run_id,
            'slots': [{'runId': rid, 'source': 'current-run' if rid == current_run_id else 'exact-retained-lookup'}
                      for rid in admitted['runIds']]}


def resolve_slots(selection, exact_lookup):
    try:
        expected = plan_selection({'mode': 'explicit', 'runIds': selection['requestedRunIds']}, selection['currentRunId'])
    except (KeyError, TypeError, HistoryRefusal) as error:
        raise HistorySourceRefusal() from error
    if selection != expected:
        raise HistorySourceRefusal()
    results = []
    for slot in expected['slots']:
        if slot['source'] == 'current-run':
            results.append({'state': 'current-run', 'runId': slot['runId']})
            continue
        value = exact_lookup(slot['runId'])
        if (type(value) is not dict or value.get('runId') != slot['runId'] or
                value.get('state') not in ('present', 'unavailable')):
            raise HistorySourceRefusal()
        if value['state'] == 'unavailable' and value.get('availability') not in ('expired', 'purged', 'corrupt', 'unavailable'):
            raise HistorySourceRefusal()
        results.append(copy.deepcopy(value))
    return results
