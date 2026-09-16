# Generated exact AST extraction from pinned report08 subject_run; no semantic change.
def subject_run(env, command):
    if env['kind'] == 'run':
        return env['run']['runId'] if env['run']['authority'] == 'authoritative' else None
    if env['kind'] != 'query':
        return None
    record = env['queryRecord']
    if command == 'candidates':
        return record['context']['resolvedView'].get('runId')
    if command == 'inspect':
        return record['inspection']['runId']
    if command == 'review-brief':
        return record['brief']['runId']
    return None
