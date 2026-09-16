"""Explicit bounded history selection; host custody precedes lookup."""
import copy
import re
import types
from pathlib import Path
HERE=Path(__file__).resolve().parent
QUERY=types.ModuleType("typed_history_query")
exec(compile((HERE/"query_history.py").read_bytes(),str(HERE/"query_history.py"),"exec"),QUERY.__dict__)

SUBJECT=types.ModuleType("report_subject_run")
exec(compile((HERE/"subject_run.py").read_bytes(),str(HERE/"subject_run.py"),"exec"),SUBJECT.__dict__)
current_run_from_envelope=SUBJECT.subject_run

MAX_RUNS = 4
RUN_ID = re.compile(r'run3:[0-9a-f]{64}')
REMEDY = 'Use one to four distinct full Run IDs with --format html.'


class HistoryRefusal(ValueError):
    def __init__(self, detail='REPORT.HISTORY_SELECTION_INVALID', code='REQUEST.UNSATISFIABLE'):
        self.route = {'class':'request-rejected','code':code,'exitCode':2,'detail':detail}
        super().__init__(detail)


class HistorySourceRefusal(ValueError):
    """Internal projection/source mismatch, never a user request rejection."""
    def __init__(self):
        super().__init__('REPORT-HISTORY.SOURCE-MISMATCH')


def valid_run_id(value):
    return type(value) is str and RUN_ID.fullmatch(value) is not None


def admit_request(run_ids, output_format):
    # Applicability precedes token parsing. Tokens never appear in public routes.
    if output_format != 'html':
        raise HistoryRefusal('OUTPUT.FORMAT_NOT_APPLICABLE', 'REQUEST.UNKNOWN_OPTION')
    if (type(run_ids) is not list or not run_ids or any(not valid_run_id(r) for r in run_ids)
            or len(set(run_ids)) != len(run_ids)):
        raise HistoryRefusal()
    if len(run_ids) > MAX_RUNS:
        raise HistoryRefusal('EVALUATION.SELECTION_LIMIT')
    return {'mode': 'explicit', 'runIds': list(run_ids)}


def plan_selection(request, current_run_id):
    if type(request) is not dict or set(request) != {'mode', 'runIds'} or request['mode'] != 'explicit':
        raise HistoryRefusal()
    admitted = admit_request(request['runIds'], 'html')
    if current_run_id is not None and not valid_run_id(current_run_id):
        raise HistorySourceRefusal()
    return {'policy': 'explicit-run-ids.1', 'requestedRunIds': admitted['runIds'],
            'currentRunId': current_run_id,
            'slots': [{'runId': rid, 'source': 'current-run' if rid == current_run_id else 'exact-retained-lookup'}
                      for rid in admitted['runIds']]}


def resolve_slots(selection, project_id, exact_lookup, validate_query, validate_history_row):
    """One typed run.show + history projection per non-current requested slot.

    exact_lookup is bound by the host to one namespace read snapshot acquired
    after this invocation's completed data commits and before any slot lookup.
    Validators are the selected contract validators, never caller-selected schemas.
    """
    if type(project_id) is not str or re.fullmatch(r'prj1-[0-9a-f]{64}',project_id) is None:
        raise HistorySourceRefusal()
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
        if type(value) is not dict or set(value) != {'query','history'}:
            raise HistorySourceRefusal()
        try:
            item=QUERY.admit_response(value['query'],project_id,slot['runId'],validate_query)
        except QUERY.QueryHistorySourceRefusal as error:
            raise HistorySourceRefusal() from error
        row=value['history']
        if type(row) is not dict or row.get('runId')!=slot['runId']:
            raise HistorySourceRefusal()
        if item is None:
            if row.get('state')!='unavailable' or row.get('availability')!=value['query']['context']['availability']:
                raise HistorySourceRefusal()
        elif row.get('state')!='present' or row.get('run')!=item['result']:
            raise HistorySourceRefusal()
        validate_history_row(row)
        if row['state']=='present':
            projection=row['findingsProjection']
            if len(row['findings'])+projection['omitted']!=projection['total']:
                raise HistorySourceRefusal()
            if (projection['omitted']==0)!=(projection['omissionCause']=='none'):
                raise HistorySourceRefusal()
        results.append(copy.deepcopy(row))
    return results


def resolve_in_snapshot(request,current_run_id,project_id,acquire_snapshot,typed_lookup,validate_query,validate_history_row):
    """Host calls only after non-render steps settle and their data commits finish.

    One read lease is used for the entire explicit list, including Runs committed
    by earlier pivot steps in this invocation. The lease is released on failure.
    This orchestrates a supplied host read lease; it is not storage implementation.
    """
    selection=plan_selection(request,current_run_id)
    with acquire_snapshot() as snapshot:
        rows=resolve_slots(selection,project_id,lambda rid:typed_lookup(snapshot,rid),validate_query,validate_history_row)
    return selection,rows


def validate_panel(panel,current_run_id,validate_shape):
    validate_shape(panel)
    selection=panel['selection']
    expected=plan_selection({'mode':'explicit','runIds':selection['requestedRunIds']},current_run_id)
    if selection!=expected or [row['runId'] for row in panel['runs']]!=expected['requestedRunIds']:
        raise HistorySourceRefusal()
    for row in panel['runs']:
        if (row['state']=='current-run')!=(row['runId']==current_run_id):
            raise HistorySourceRefusal()
        if row['state']=='present':
            p=row['findingsProjection']
            if row['run']['runId']!=row['runId'] or len(row['findings'])+p['omitted']!=p['total'] or ((p['omitted']==0)!=(p['omissionCause']=='none')):
                raise HistorySourceRefusal()
    return panel
