"""Public-only Grok retain helpers. Not acceptance and not a live retainer.

v1 copied the CLI raw envelope (thought) via src.rglob. These helpers
whitelist public envelope keys and public assistant/tool records, and
exclude the raw CLI envelope wherever launch.stdoutName placed it.
"""
from __future__ import annotations

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
PUBLIC_TOOL_RESULT_KEYS = ('type', 'tool_call_id', 'content')


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


def grok_transcript_path(cwd, session_id, sessions_root=None):
    assert isinstance(cwd, str) and cwd.strip(), 'process cwd missing'
    assert isinstance(session_id, str) and session_id.strip(), 'sessionId missing'
    root = Path(sessions_root) if sessions_root else Path.home() / '.grok' / 'sessions'
    quoted = quote(str(Path(cwd).resolve()), safe='')
    return (root / quoted / session_id / 'chat_history.jsonl').resolve()


def require_named_grok_transcript(named, cwd, session_id, sessions_root=None):
    expected = grok_transcript_path(cwd, session_id, sessions_root=sessions_root)
    actual = Path(named).resolve()
    assert actual == expected, (
        'Named Grok transcript is not the session path derived from process cwd + sessionId'
    )
    assert actual.is_file(), 'Missing Grok chat_history.jsonl at derived session path'
    return actual


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
    """Keep public assistant/tool_call/tool_result only. Drop reasoning rows."""
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


def json_obj(line):
    import json

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
    import json

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
