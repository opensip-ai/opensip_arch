"""Public-only Grok retain helpers. Not acceptance and not a live retainer.

v1 copied the CLI raw envelope (thought) via src.rglob. v2 helpers
whitelist public envelope keys and public assistant/tool records, and
exclude the raw CLI envelope wherever launch.stdoutName placed it.

This successor keeps that whitelist, and takes Grok public assistant/tool
deliveries from authenticated session updates.jsonl so a post-compaction
chat_history fragment is not treated as the complete public record.
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

GROK_PUBLIC_RESPONSE_NAME = 'response.public.json'
DEFAULT_GROK_STDOUT_NAME = 'response.raw.json'
PRIVATE_ENVELOPE_KEYS = ('thought', 'reasoning', 'encrypted_content')
GROK_PRIVATE_BASENAMES = frozenset(
    {
        DEFAULT_GROK_STDOUT_NAME,
        'chat_history.jsonl',
        'chat_history.jsonl.lock',
        'events.jsonl',
        'updates.jsonl',
        'updates.jsonl.lock',
        'rewind_points.jsonl',
        'rewind_points.jsonl.lock',
        'announcement_state.json',
        'plan.json',
        'plan_mode.json',
        'prompt_context.json',
        'resources_state.json',
        'signals.json',
        'summary.json',
        'summary.json.lock',
        'system_prompt.txt',
        'title_refresh_idx',
    }
)
GROK_PRIVATE_TOP_DIRS = frozenset({'compaction', 'compaction_checkpoints', 'terminal'})
PUBLIC_ASSISTANT_KEYS = ('type', 'content', 'tool_calls')
PUBLIC_TOOL_CALL_KEYS = ('id', 'name', 'arguments')
PUBLIC_TOOL_RESULT_KEYS = ('type', 'tool_call_id', 'content', 'publicStatus')
GROK_SKIP_UPDATE_KINDS = frozenset(
    {
        'agent_thought_chunk',
        'auto_compact_completed',
        'available_commands_update',
        'session_info_update',
        'plan_update',
        'thought_delta',
    }
)


def command_cwd(process):
    if not isinstance(process, dict):
        return None
    if isinstance(process.get('cwd'), str) and process['cwd'].strip():
        return process['cwd']
    command = process.get('command')
    if isinstance(command, list) and '--cwd' in command:
        idx = command.index('--cwd')
        if idx + 1 < len(command):
            return command[idx + 1]
    return None


def grok_session_dir(cwd, session_id, sessions_root=None):
    assert isinstance(cwd, str) and cwd.strip(), 'process cwd missing'
    assert isinstance(session_id, str) and session_id.strip(), 'sessionId missing'
    root = Path(sessions_root) if sessions_root else Path.home() / '.grok' / 'sessions'
    quoted = quote(str(Path(cwd).resolve()), safe='')
    return (root / quoted / session_id).resolve()


def grok_transcript_path(cwd, session_id, sessions_root=None):
    return grok_session_dir(cwd, session_id, sessions_root=sessions_root) / 'chat_history.jsonl'


def grok_updates_path(cwd, session_id, sessions_root=None):
    return grok_session_dir(cwd, session_id, sessions_root=sessions_root) / 'updates.jsonl'


def require_named_grok_transcript(named, cwd, session_id, sessions_root=None):
    expected = grok_transcript_path(cwd, session_id, sessions_root=sessions_root)
    actual = Path(named).resolve()
    assert actual == expected, (
        'Named Grok transcript is not the session path derived from process cwd + sessionId'
    )
    assert actual.is_file(), 'Missing Grok chat_history.jsonl at derived session path'
    return actual


def require_grok_updates(cwd, session_id, sessions_root=None):
    path = grok_updates_path(cwd, session_id, sessions_root=sessions_root)
    assert path.is_file(), 'Missing Grok updates.jsonl at derived session path'
    return path


def require_fresh_grok_process(process):
    if process is None:
        return
    assert isinstance(process, dict)
    command = process.get('command')
    if isinstance(command, list):
        assert '--resume' not in command, (
            'Independent application retain requires a fresh session; --resume is excluded'
        )
    if 'freshSession' in process:
        assert process.get('freshSession') is True, 'freshSession must be true when present'


def stdout_basename(launch):
    launch = launch or {}
    name = launch.get('stdoutName', DEFAULT_GROK_STDOUT_NAME)
    assert isinstance(name, str) and name.strip() and '..' not in Path(name).parts
    return Path(name).name


def grok_source_is_private(rel, stdout_name):
    rel = Path(rel)
    if rel.parts and rel.parts[0] in GROK_PRIVATE_TOP_DIRS:
        return True
    name = rel.name
    if name in GROK_PRIVATE_BASENAMES:
        return True
    if name == Path(stdout_name).name:
        return True
    return False


def envelope_has_private_keys(obj):
    if not isinstance(obj, dict):
        return False
    return any(k in obj for k in PRIVATE_ENVELOPE_KEYS)


def public_grok_transcript_blocks(text):
    """Keep public assistant/tool_call/tool_result only. Drop reasoning rows.

    Not the complete public source after CLI compaction. Application retain
    must use public_grok_update_blocks on authenticated updates.jsonl.
    """
    blocks = []
    for line in text.split('\n'):
        if not line.strip():
            continue
        d = json_obj(line)
        t = d.get('type')
        if t == 'assistant':
            item = {'type': 'assistant'}
            if 'content' in d:
                item['content'] = d['content']
            calls = []
            for call in d.get('tool_calls') or []:
                if isinstance(call, dict):
                    calls.append({k: call[k] for k in PUBLIC_TOOL_CALL_KEYS if k in call})
            if calls:
                item['tool_calls'] = calls
            blocks.append(item)
        elif t == 'tool_result':
            item = {'type': 'tool_result'}
            if 'tool_call_id' in d:
                item['tool_call_id'] = d['tool_call_id']
            if 'content' in d:
                item['content'] = d['content']
            blocks.append(item)
    assert blocks, 'Grok transcript has no public assistant/tool_call/tool_result blocks'
    assert all(b.get('type') != 'reasoning' for b in blocks)
    return blocks


def public_grok_update_blocks(text, session_id, prompt):
    """Public assistant/tool deliveries from authenticated updates.jsonl.

    Skips thought chunks, compaction summaries, and rawOutput. Requires the
    exact launch prompt once before any public activity. Does not treat
    chat_history as complete.
    """
    assert isinstance(session_id, str) and session_id.strip(), 'sessionId missing'
    assert isinstance(prompt, str) and prompt.strip(), 'Launch prompt missing'
    needle = prompt.strip()
    public = []
    names = collections.Counter()
    starts = []
    user_messages = 0
    calls = set()
    delivered = set()
    event_ids = []
    compactions = 0
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError('Malformed Grok updates.jsonl line ' + str(line_no)) from exc
        assert isinstance(row, dict), 'updates row must be an object at line ' + str(line_no)
        pars = row.get('params')
        assert isinstance(pars, dict), 'updates row missing params at line ' + str(line_no)
        assert pars.get('sessionId') == session_id, (
            'updates sessionId does not match authenticated session at line ' + str(line_no)
        )
        u = pars.get('update')
        assert isinstance(u, dict), 'updates row missing update at line ' + str(line_no)
        kind = u.get('sessionUpdate')
        if kind == 'auto_compact_completed':
            compactions += 1
            continue
        if kind in GROK_SKIP_UPDATE_KINDS or kind == 'user_message_chunk':
            if kind == 'user_message_chunk':
                user_messages += 1
                c = u.get('content', {})
                if isinstance(c, dict) and c.get('type') == 'text' and needle in c.get('text', ''):
                    starts.append(len(public))
            continue
        if kind == 'agent_message_chunk':
            c = u.get('content', {})
            if isinstance(c, dict) and c.get('type') == 'text':
                public.append({'type': 'assistant', 'content': c['text']})
            else:
                continue
        elif kind == 'tool_call':
            tid = u.get('toolCallId')
            assert isinstance(tid, str) and tid.strip(), 'tool_call missing toolCallId'
            assert tid not in calls, 'duplicate tool_call id: ' + tid
            calls.add(tid)
            meta = u.get('_meta') if isinstance(u.get('_meta'), dict) else {}
            tool_meta = meta.get('x.ai/tool') if isinstance(meta.get('x.ai/tool'), dict) else {}
            name = tool_meta.get('name') or u.get('title')
            assert isinstance(name, str) and name.strip(), 'tool_call missing name'
            assert 'rawInput' in u, 'tool_call missing rawInput'
            item = {
                'type': 'assistant',
                'tool_calls': [
                    {
                        'id': tid,
                        'name': name,
                        'arguments': json.dumps(u['rawInput'], ensure_ascii=False),
                    }
                ],
            }
            public.append(item)
            names[name] += 1
        elif kind == 'tool_call_update' and u.get('status') in ('completed', 'failed'):
            tid = u.get('toolCallId')
            assert isinstance(tid, str) and tid.strip(), 'tool_call_update missing toolCallId'
            assert tid in calls, 'tool_result without tool_call: ' + tid
            assert tid not in delivered, 'duplicate tool_result delivery: ' + tid
            delivered.add(tid)
            content = []
            for item in u.get('content') or []:
                if not isinstance(item, dict):
                    continue
                c = item.get('content', {})
                if item.get('type') == 'content' and isinstance(c, dict) and c.get('type') == 'text':
                    content.append(c['text'])
            public.append(
                {
                    'type': 'tool_result',
                    'tool_call_id': tid,
                    'content': '\n'.join(content),
                    'publicStatus': u['status'],
                }
            )
        else:
            continue
        event_ids.append(pars.get('_meta', {}).get('eventId') if isinstance(pars.get('_meta'), dict) else None)
    assert starts == [0], ('Fresh prompt must appear exactly once before public activity', starts)
    assert user_messages == 1, 'Fresh review has additional user messages'
    assert calls == delivered, 'Incomplete public tool deliveries: ' + str(sorted(calls - delivered))
    assert public, 'Grok updates.jsonl has no public assistant/tool deliveries'
    for block in public:
        assert isinstance(block, dict)
        assert 'rawOutput' not in block
        assert not envelope_has_private_keys(block)
        assert block.get('type') != 'reasoning'
        for call in block.get('tool_calls') or []:
            assert isinstance(call, dict)
            assert 'rawOutput' not in call
    source_bytes = text.encode('utf-8')
    return public, {
        'toolCalls': dict(names),
        'publicBlocks': len(public),
        'promptFoundExactlyOnce': True,
        'compactionsObserved': compactions,
        'eventIds': event_ids,
        'sourceBytes': len(source_bytes),
        'sourceSha256': hashlib.sha256(source_bytes).hexdigest(),
        'publicEventSource': 'authenticated session updates.jsonl',
        'privateFieldsRetained': False,
    }


def json_obj(line):
    d = json.loads(line)
    assert isinstance(d, dict)
    return d


def dest_contains_sentinel(dest, sentinel):
    dest = Path(dest)
    for q in dest.rglob('*'):
        if q.is_file() and sentinel.encode() in q.read_bytes():
            return str(q.relative_to(dest))
    return None


def claude_selected_tool_blocks(text):
    """Historical Claude selector: tool_use/tool_result only. Not a field widening."""
    blocks = []
    for line in text.split('\n'):
        if not line:
            continue
        d = json.loads(line)
        content = d.get('message', {}).get('content', [])
        for b in content if isinstance(content, list) else []:
            if isinstance(b, dict) and b.get('type') in ('tool_use', 'tool_result'):
                blocks.append(
                    {'timestamp': d.get('timestamp'), 'messageUuid': d.get('uuid'), 'block': b}
                )
    return blocks


def grok_application_launch_spec(out, launch=None):
    launch = launch or {}
    out = Path(out)
    cli = launch.get('cli', '/Users/sb/.grok/bin/grok')
    stdout_name = stdout_basename(launch)
    permission = launch.get('permissionMode', 'acceptEdits')
    max_turns = str(launch.get('maxTurns', 60))
    args = [
        cli,
        '--cwd',
        str(out),
        '--permission-mode',
        permission,
        '--no-subagents',
        '--disable-web-search',
        '--max-turns',
        max_turns,
        '--output-format',
        'json',
        '--prompt-file',
        str(out / 'prompt.txt'),
    ]
    assert '--resume' not in args
    assert permission == launch.get('permissionMode', 'acceptEdits')
    return {
        'args': args,
        'cwd': str(out),
        'stdoutName': stdout_name,
        'permissionMode': permission,
    }
