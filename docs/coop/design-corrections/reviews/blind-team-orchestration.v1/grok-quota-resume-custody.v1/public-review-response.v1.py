"""Public review response envelope; only the observed exact402 format is a partial error.
It is never relabelled end_turn/cancelled or substantive acceptance.
"""
import json
PUBLIC_KEYS=('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage')
ERROR_TEXT='API error (status 402 Payment Required): Grok Build usage balance exhausted'
def observed_response(raw,session_id):
    assert isinstance(raw,dict)
    if raw.get('type')=='error':
        assert 'stopReason' not in raw and 'sessionId' not in raw
        message=raw.get('message');assert isinstance(message,str) and message.startswith('Internal error: ')
        detail=json.loads(message[len('Internal error: '):])
        assert detail.get('http_status')==402 and detail.get('message')==ERROR_TEXT
        assert type(raw.get('num_turns')) is int and raw['num_turns']>=0
        return {'type':'error','httpStatus':402,'message':ERROR_TEXT,'num_turns':raw['num_turns'],'sessionIdFromProcess':session_id,'sessionIdAuthority':'Authenticated launch process and exact public update stream; provider error response contains no sessionId.','completed':False},'usage-balance-exhausted'
    assert raw.get('sessionId')==session_id
    assert raw.get('stopReason') in ('end_turn','cancelled')
    return {k:raw[k] for k in PUBLIC_KEYS if k in raw},raw['stopReason']
