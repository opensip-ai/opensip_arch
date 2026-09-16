"""Disposable retainer/launch public-copy tests. No live application retain. No real CLI logs.

Preserves the v1 40 behavioral assertions against adapted fixtures whose public
Grok event stream is updates.jsonl. Adds compaction/private/source refusals.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREPARED = HERE / 'prepared'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PREPARED))
import coverage_contract as C
import retain_public as P
import review_envelope as E

SENTINEL = 'SYNTHETIC_PRIVATE_SENTINEL_THOUGHT_NOT_FOR_RETENTION'
PUBLIC_TEXT = 'PUBLIC_REVIEW_TEXT_ACCEPT'
PUBLIC_TOOL = 'PUBLIC_TOOL_RESULT_BODY'
PRE_COMPACTION_TEXT = 'PRE_COMPACTION_PUBLIC_ASSISTANT'
PRE_COMPACTION_TOOL = 'PRE_COMPACTION_TOOL_RESULT'
POST_COMPACTION_TEXT = 'POST_COMPACTION_PUBLIC_ASSISTANT'
POST_COMPACTION_TOOL = 'POST_COMPACTION_TOOL_RESULT'
PROMPT = 'synthetic prompt names absolute stage'
rows = []


def record(ident, passed, detail=''):
    rows.append({'id': ident, 'passed': bool(passed), 'detail': detail})


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = load_mod('retain_app_v2', HERE / 'retain-application-review.successor.v1.py')
R1 = load_mod(
    'retain_app_v1',
    HERE / 'public-custody-before-compaction.v1' / 'retain-application-review.successor.v1.py',
)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def grok_ok(**extra):
    env = {
        'text': PUBLIC_TEXT,
        'stopReason': 'end_turn',
        'sessionId': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'requestId': 'req-1',
    }
    env.update(extra)
    return env


def claude_ok(**extra):
    env = {
        'is_error': False,
        'session_id': 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        'stop_reason': 'end_turn',
        'result': 'Independent review complete.',
    }
    env.update(extra)
    return env


def update_row(session, kind, **update):
    u = {'sessionUpdate': kind}
    u.update(update)
    return {
        'params': {
            'sessionId': session,
            'update': u,
            '_meta': {'eventId': 'evt-' + kind},
        }
    }


def updates_text(session, items):
    return ''.join(json.dumps(item, ensure_ascii=False) + '\n' for item in items)


def default_public_updates(session, prompt=PROMPT):
    return [
        update_row(session, 'user_message_chunk', content={'type': 'text', 'text': prompt}),
        update_row(
            session,
            'agent_thought_chunk',
            content={'type': 'text', 'text': SENTINEL},
        ),
        update_row(
            session,
            'agent_message_chunk',
            content={'type': 'text', 'text': 'PUBLIC_ASSISTANT_TEXT'},
        ),
        update_row(
            session,
            'tool_call',
            toolCallId='c1',
            title='read_file',
            rawInput={'target_file': 'review.json'},
            **{'_meta': {'x.ai/tool': {'name': 'read_file'}}},
        ),
        update_row(
            session,
            'tool_call_update',
            toolCallId='c1',
            status='completed',
            content=[{'type': 'content', 'content': {'type': 'text', 'text': PUBLIC_TOOL}}],
            rawOutput={'private': SENTINEL},
        ),
    ]


def compaction_updates(session, prompt=PROMPT):
    return [
        update_row(session, 'user_message_chunk', content={'type': 'text', 'text': prompt}),
        update_row(
            session,
            'agent_message_chunk',
            content={'type': 'text', 'text': PRE_COMPACTION_TEXT},
        ),
        update_row(
            session,
            'tool_call',
            toolCallId='pre1',
            title='read_file',
            rawInput={'target_file': 'before.json'},
            **{'_meta': {'x.ai/tool': {'name': 'read_file'}}},
        ),
        update_row(
            session,
            'tool_call_update',
            toolCallId='pre1',
            status='completed',
            content=[{'type': 'content', 'content': {'type': 'text', 'text': PRE_COMPACTION_TOOL}}],
            rawOutput={'private': SENTINEL},
        ),
        update_row(session, 'auto_compact_completed', message=SENTINEL, summary=SENTINEL),
        update_row(
            session,
            'agent_thought_chunk',
            content={'type': 'text', 'text': SENTINEL},
        ),
        update_row(
            session,
            'agent_message_chunk',
            content={'type': 'text', 'text': POST_COMPACTION_TEXT},
        ),
        update_row(
            session,
            'tool_call',
            toolCallId='post1',
            title='read_file',
            rawInput={'target_file': 'after.json'},
            **{'_meta': {'x.ai/tool': {'name': 'read_file'}}},
        ),
        update_row(
            session,
            'tool_call_update',
            toolCallId='post1',
            status='completed',
            content=[{'type': 'content', 'content': {'type': 'text', 'text': POST_COMPACTION_TOOL}}],
            rawOutput={'private': SENTINEL},
        ),
    ]


def envelope_v1_checks():
    try:
        d = E.decode_grok_public(grok_ok(text='Independent review complete. Verdict ACCEPT.'))
        record('v1-grok-end-turn-extracts-sessionId', d['sessionId'].startswith('aaaa') and d['vendor'] == 'grok')
    except Exception as e:
        record('v1-grok-end-turn-extracts-sessionId', False, type(e).__name__)
    try:
        E.decode_grok_public(grok_ok(stopReason='cancelled', text='Independent review complete. Verdict ACCEPT.'))
        record('v1-grok-cancelled-refuses', False, 'accepted cancelled')
    except AssertionError:
        record('v1-grok-cancelled-refuses', True)
    try:
        env = grok_ok(text='Independent review complete. Verdict ACCEPT.')
        env.pop('stopReason')
        E.decode_grok_public(env)
        record('v1-grok-missing-stopReason-refuses', False)
    except AssertionError:
        record('v1-grok-missing-stopReason-refuses', True)
    try:
        E.decode_grok_public(grok_ok(text='   '))
        record('v1-grok-empty-text-refuses', False)
    except AssertionError:
        record('v1-grok-empty-text-refuses', True)
    try:
        d = E.decode_claude_public(claude_ok())
        record('v1-claude-is_error-false-extracts-session_id', d['sessionId'].startswith('bbbb'))
    except Exception:
        record('v1-claude-is_error-false-extracts-session_id', False)
    try:
        E.decode_claude_public(claude_ok(is_error=True))
        record('v1-claude-is_error-true-refuses', False)
    except AssertionError:
        record('v1-claude-is_error-true-refuses', True)
    try:
        env = claude_ok()
        env.pop('is_error')
        E.decode_claude_public(env)
        record('v1-claude-missing-is_error-refuses', False)
    except AssertionError:
        record('v1-claude-missing-is_error-refuses', True)
    try:
        E.decode_public(claude_ok(), 'grok')
        record('v1-claude-envelope-fails-grok-decoder', False)
    except AssertionError:
        record('v1-claude-envelope-fails-grok-decoder', True)
    try:
        E.decode_public(grok_ok(text='Independent review complete. Verdict ACCEPT.'), 'claude')
        record('v1-grok-envelope-fails-claude-decoder', False)
    except AssertionError:
        record('v1-grok-envelope-fails-claude-decoder', True)
    try:
        E.decode_public({'is_error': False, 'session_id': 'x'}, 'grok')
        record('v1-name-swap-claude-fields-as-grok-refuses', False)
    except AssertionError:
        record('v1-name-swap-claude-fields-as-grok-refuses', True)
    ok_review = {
        'verdict': 'ACCEPT',
        'subjectManifestSha256': 'a' * 64,
        'newMustIssues': [],
        'newShouldIssues': [],
    }
    try:
        E.require_verdict(ok_review, 'ACCEPT', 'design')
        E.require_findings_none(ok_review, 'design')
        record('v1-accept-empty-findings-lists', E.review_subject_digest(ok_review) == 'a' * 64)
    except Exception:
        record('v1-accept-empty-findings-lists', False)
    try:
        E.require_findings_none({**ok_review, 'newMustIssues': [{'id': 'x'}]}, 'design')
        record('v1-accept-with-must-refuses', False)
    except AssertionError:
        record('v1-accept-with-must-refuses', True)
    try:
        bad = dict(ok_review)
        bad.pop('newShouldIssues')
        E.require_findings_none(bad, 'design')
        record('v1-accept-unaccounted-should-refuses', False)
    except AssertionError:
        record('v1-accept-unaccounted-should-refuses', True)
    try:
        E.require_verdict({**ok_review, 'verdict': 'CHANGES_REQUIRED'}, 'ACCEPT', 'design')
        record('v1-changes-required-is-not-accept', False)
    except AssertionError:
        record('v1-changes-required-is-not-accept', True)
    try:
        E.refuse_coauthor_process(
            {
                'standing': 'Actual Grok coauthor; isolated authorized file ownership; no source acceptance',
                'sessionId': C.KNOWN_GROK_COAUTHOR_SESSIONS[0],
            },
            'independent-design',
        )
        record('v1-coauthor-standing-refuses', False)
    except AssertionError:
        record('v1-coauthor-standing-refuses', True)
    try:
        E.refuse_coauthor_process(
            {
                'standing': 'Independent review',
                'command': ['grok', '--resume', C.KNOWN_GROK_COAUTHOR_SESSIONS[0]],
            },
            'independent-design',
        )
        record('v1-resume-known-coauthor-refuses', False)
    except AssertionError:
        record('v1-resume-known-coauthor-refuses', True)
    pub = E.public_view(grok_ok(text='Independent review complete. Verdict ACCEPT.', thought=SENTINEL), 'grok')
    record('v1-public-view-drops-thought', 'thought' not in pub and pub.get('stopReason') == 'end_turn')
    record(
        'v1-historical-v21-subject-constant-preserved',
        C.HISTORICAL_V21_SUBJECT_SHA256 == '360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1',
    )
    record(
        'v1-coverage-counts',
        all(
            [
                len(C.AR_IDS) == 16,
                len(C.FW_IDS) == 15,
                len(C.INHERITED_IDS) == 27,
                len(C.CONDITION2_IDS) == 28,
                len(C.GATE_IDS) == 32,
                C.EVALUATION_RESIDUAL_COUNT == 30,
                C.D9_CARRIED_ROWS == ('DR-007', 'DR-011-R08'),
            ]
        ),
    )


def write(p, obj=None, text=None):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if obj is not None:
        p.write_text(json.dumps(obj, indent=2) + '\n')
    else:
        p.write_text(text)


def make_fixture(
    td,
    stdout_name='cli-envelope.json',
    session='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    *,
    update_items=None,
    session_chat=None,
    write_updates=True,
    prompt_text=PROMPT + '\n',
):
    td = Path(td)
    root = td / 'root'
    stage = td / 'pkg' / 'stage'
    src = td / 'pkg' / 'application-review.t1'
    dest = td / 'retained'
    sessions = td / 'sessions'
    cwd = src
    review_bytes = json.dumps(
        {
            'verdict': 'ACCEPT',
            'subjectManifestSha256': None,
            'newMustIssues': [],
            'newShouldIssues': [],
        },
        indent=2,
    )
    md = '# synthetic application review\nPUBLIC_REVIEW_MARKDOWN\n'
    probe = {'id': 'probe-1', 'result': 'PUBLIC_PROBE'}
    write(src / 'review.md', text=md)
    write(src / 'probes/probe.json', obj=probe)
    write(src / stdout_name, obj=grok_ok(sessionId=session, thought=SENTINEL))
    write(src / 'chat_history.jsonl', text=json.dumps({'type': 'reasoning', 'encrypted_content': SENTINEL}) + '\n')
    write(src / 'events.jsonl', text=json.dumps({'type': 'phase_changed', 'note': SENTINEL}) + '\n')
    write(src / 'updates.jsonl', text=json.dumps({'private': SENTINEL, 'sessionUpdate': 'agent_thought_chunk'}) + '\n')
    write(
        src / 'process.json',
        obj={
            'command': ['/Users/sb/.grok/bin/grok', '--cwd', str(cwd), '--permission-mode', 'acceptEdits'],
            'cwd': str(cwd),
            'standing': 'Independent application review launch metadata; not a verdict.',
            'stdoutName': stdout_name,
        },
    )
    write(src / 'prompt.txt', text=prompt_text)
    transcript = P.grok_transcript_path(str(cwd), session, sessions_root=sessions)
    if session_chat is None:
        session_chat = json.dumps({'type': 'assistant', 'content': 'POST_COMPACTION_CHAT_FRAGMENT'}) + '\n'
    write(transcript, text=session_chat)
    if write_updates:
        items = update_items if update_items is not None else default_public_updates(session, prompt_text.strip())
        write(P.grok_updates_path(str(cwd), session, sessions_root=sessions), text=updates_text(session, items) if isinstance(items[0], dict) else ''.join(items))
    manifest = {
        'retainedManifestPath': 'docs/coop/design-corrections/reviews/application-subject.t1.json',
        'files': [],
        'beforeImages': [],
        'support': [],
        'implementationAuthorized': False,
    }
    man_path = stage / 'application-subject.t1.json'
    write(man_path, obj=manifest)
    digest = sha(man_path)
    review_obj = json.loads(review_bytes)
    review_obj['subjectManifestSha256'] = digest
    write(src / 'review.json', obj=review_obj)
    write(root / manifest['retainedManifestPath'], obj=manifest)
    write(
        stage / 'files/docs/coop/design-corrections/application.v1.json',
        obj={'implementationAuthorized': False},
    )
    bound = {
        'vendor': 'grok',
        'readyForAssembly': True,
        'implementationAuthorized': False,
        'independentDesignReview': {'sessionId': 'design-session'},
        'freshBlindConsumerReview': {'sessionId': 'blind-session'},
        'launch': {'stdoutName': stdout_name, 'permissionMode': 'acceptEdits'},
        'applicationSessionTranscriptPath': str(transcript),
    }
    return {
        'root': root,
        'stage': stage,
        'src': src,
        'dest': dest,
        'sessions': sessions,
        'bound': bound,
        'digest': digest,
        'review_sha': sha(src / 'review.json'),
        'md_sha': sha(src / 'review.md'),
        'probe_sha': sha(src / 'probes/probe.json'),
        'session': session,
        'stdout_name': stdout_name,
        'cwd': cwd,
        'transcript': transcript,
    }


def write_update_items(fx, items):
    path = P.grok_updates_path(str(fx['cwd']), fx['session'], sessions_root=fx['sessions'])
    if items is None:
        if path.exists():
            path.unlink()
        return
    if isinstance(items, str):
        write(path, text=items)
        return
    write(path, text=updates_text(fx['session'], items))


def catch(ident, fn):
    try:
        fn()
        record(ident, False, 'expected refusal')
    except AssertionError:
        record(ident, True)
    except Exception as e:
        record(ident, False, type(e).__name__)


def retain(fx, retainer=None):
    retainer = retainer or R
    return retainer.run_retain(
        root=fx['root'],
        stage=fx['stage'],
        version='t1',
        bound=fx['bound'],
        dest=fx['dest'],
        sessions_root=fx['sessions'],
        src=fx['src'],
    )


envelope_v1_checks()

# Launch spec: acceptEdits, cwd=output dir, no resume
out = Path('/tmp/synthetic-application-review.t1')
spec = P.grok_application_launch_spec(out, {})
record(
    'launch-default-acceptEdits-cwd-output-no-resume',
    spec['permissionMode'] == 'acceptEdits'
    and spec['cwd'] == str(out)
    and spec['args'][spec['args'].index('--cwd') + 1] == str(out)
    and '--resume' not in spec['args']
    and spec['stdoutName'] == 'response.raw.json',
)
spec2 = P.grok_application_launch_spec(out, {'stdoutName': 'cli-envelope.json', 'permissionMode': 'acceptEdits'})
record('launch-stdoutName-parameterized', spec2['stdoutName'] == 'cli-envelope.json')

# Transcript path derivation uses URL-quoted resolved cwd
with tempfile.TemporaryDirectory(prefix='opensip-retain-path-') as td:
    cwd = Path(td) / 'app-review'
    cwd.mkdir()
    sessions = Path(td) / 'sessions'
    session = 'cccccccc-cccc-cccc-cccc-cccccccccccc'
    expected = P.grok_transcript_path(str(cwd), session, sessions_root=sessions)
    from urllib.parse import quote

    record(
        'transcript-path-quoted-resolved-cwd',
        expected.parent.parent.name == quote(str(cwd.resolve()), safe='') and expected.name == 'chat_history.jsonl',
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-ok-') as td:
    fx = make_fixture(td)
    result = retain(fx)
    dest = Path(fx['dest'])
    names = {p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file()}
    leak = P.dest_contains_sentinel(dest, SENTINEL)
    record('raw-custom-stdoutName-not-copied', fx['stdout_name'] not in names and leak is None)
    record('raw-chat_history-not-copied', 'chat_history.jsonl' not in names)
    record('private-events-not-copied', 'events.jsonl' not in names)
    pub = json.loads((dest / 'response.public.json').read_text())
    record(
        'public-text-retained-thought-absent',
        pub.get('text') == PUBLIC_TEXT and 'thought' not in pub and SENTINEL not in json.dumps(pub),
    )
    blocks = json.loads((dest / 'tool-calls.json').read_text())
    contents = json.dumps(blocks)
    record(
        'public-tool-result-body-retained',
        PUBLIC_TOOL in contents and 'PUBLIC_ASSISTANT_TEXT' in contents and 'read_file' in contents,
    )
    record('reasoning-rows-not-retained', all(b.get('type') != 'reasoning' for b in blocks) and 'encrypted_content' not in contents)
    record(
        'authored-review-bytes-unchanged',
        sha(dest / 'review.json') == fx['review_sha']
        and sha(dest / 'review.md') == fx['md_sha']
        and sha(dest / 'probes/probe.json') == fx['probe_sha'],
    )
    custody = json.loads((dest / 'custody.json').read_text())
    record(
        'custody-records-excluded-private',
        fx['stdout_name'] in custody.get('excludedPrivateSources', [])
        and 'chat_history.jsonl' in custody.get('excludedPrivateSources', []),
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-rawname-') as td:
    fx = make_fixture(td, stdout_name='response.raw.json')
    retain(fx)
    names = {p.name for p in fx['dest'].rglob('*') if p.is_file()}
    record(
        'default-response.raw.json-not-copied',
        'response.raw.json' not in names and P.dest_contains_sentinel(fx['dest'], SENTINEL) is None,
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-derived-') as td:
    fx = make_fixture(td)
    fx['bound'].pop('applicationSessionTranscriptPath')
    before_bound = json.dumps(fx['bound'], sort_keys=True)
    result = retain(fx)
    record(
        'session-derived-after-launch-without-rebinding',
        result['sessionId'] == fx['session']
        and json.dumps(fx['bound'], sort_keys=True) == before_bound
        and P.dest_contains_sentinel(fx['dest'], SENTINEL) is None,
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-wrong-') as td:
    fx = make_fixture(td)
    other = Path(td) / 'sessions' / 'other' / fx['session'] / 'chat_history.jsonl'
    write(other, text=json.dumps({'type': 'assistant', 'content': 'nope'}) + '\n')
    fx['bound']['applicationSessionTranscriptPath'] = str(other)

    def wrong():
        retain(fx)

    catch('wrong-session-path-refuses', wrong)
    record('wrong-session-path-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-cancel-') as td:
    fx = make_fixture(td)
    write(fx['src'] / fx['stdout_name'], obj=grok_ok(stopReason='cancelled', thought=SENTINEL))

    def cancelled():
        retain(fx)

    catch('cancelled-envelope-refuses', cancelled)
    record('cancelled-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-coauthor-') as td:
    fx = make_fixture(td)
    proc = json.loads((fx['src'] / 'process.json').read_text())
    proc['standing'] = 'Actual Grok coauthor; no source acceptance'
    write(fx['src'] / 'process.json', obj=proc)

    def coauthor():
        retain(fx)

    catch('coauthor-process-refuses', coauthor)
    record('coauthor-writes-nothing', not fx['dest'].exists())

# Claude selector is not widened
claude_jsonl = '\n'.join(
    [
        json.dumps(
            {
                'timestamp': 't0',
                'uuid': 'u0',
                'message': {
                    'content': [
                        {'type': 'thinking', 'thinking': SENTINEL},
                        {'type': 'tool_use', 'id': '1', 'name': 'Read', 'input': {'path': 'review.json'}},
                    ]
                },
            }
        ),
        json.dumps(
            {
                'timestamp': 't1',
                'uuid': 'u1',
                'message': {'content': [{'type': 'tool_result', 'tool_use_id': '1', 'content': PUBLIC_TOOL}]},
            }
        ),
    ]
)
cblocks = P.claude_selected_tool_blocks(claude_jsonl)
record(
    'claude-selector-tool_use-result-only',
    [b['block']['type'] for b in cblocks] == ['tool_use', 'tool_result']
    and all(b['block'].get('type') != 'thinking' for b in cblocks)
    and SENTINEL not in json.dumps(cblocks),
)

# v1 rglob defect still present on immutable prepared retainer (honest standing)
prepared_retain = (
    Path('/tmp/opensip-design-corrections/grok-application-successor-preparation.v2/prepared')
    / 'retain-application-review.successor.v1.py'
).read_text()
record(
    'v1-prepared-retainer-still-rglob-copies-raw',
    'for q in sorted(src.rglob' in prepared_retain
    and 'excludedPrivateSources' not in prepared_retain
    and "public_name = 'response.public.json'" in prepared_retain,
)

EXISTING_IDS = [r['id'] for r in rows]

# --- new discriminating checks ---

with tempfile.TemporaryDirectory(prefix='opensip-retain-compact-') as td:
    fx = make_fixture(
        td,
        update_items=compaction_updates('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
        session_chat=json.dumps({'type': 'assistant', 'content': POST_COMPACTION_TEXT})
        + '\n'
        + json.dumps({'type': 'tool_result', 'tool_call_id': 'post1', 'content': POST_COMPACTION_TOOL})
        + '\n',
    )
    retain(fx)
    blocks = json.loads((fx['dest'] / 'tool-calls.json').read_text())
    contents = json.dumps(blocks)
    chat = fx['transcript'].read_text()
    record(
        'compaction-pre-and-post-public-retained',
        PRE_COMPACTION_TEXT in contents
        and PRE_COMPACTION_TOOL in contents
        and POST_COMPACTION_TEXT in contents
        and POST_COMPACTION_TOOL in contents,
    )
    record(
        'compaction-chat-fragment-not-complete',
        PRE_COMPACTION_TOOL not in chat and PRE_COMPACTION_TOOL in contents,
    )
    record(
        'private-agent-thought-not-retained',
        P.dest_contains_sentinel(fx['dest'], SENTINEL) is None and 'agent_thought_chunk' not in contents,
    )
    record(
        'compaction-summary-not-retained',
        'auto_compact_completed' not in contents and SENTINEL not in contents,
    )
    record('rawOutput-not-retained', 'rawOutput' not in contents and 'private' not in contents)
    names = {p.name for p in fx['dest'].rglob('*') if p.is_file()}
    record('updates-source-not-copied', 'updates.jsonl' not in names)
    custody = json.loads((fx['dest'] / 'custody.json').read_text())
    record(
        'compaction-account-observes-compact-and-updates-source',
        custody.get('publicEventAccount', {}).get('compactionsObserved') == 1
        and custody.get('publicEventAccount', {}).get('publicEventSource')
        == 'authenticated session updates.jsonl',
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-origfail-') as td:
    fx = make_fixture(
        td,
        update_items=compaction_updates('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
        session_chat=json.dumps({'type': 'assistant', 'content': POST_COMPACTION_TEXT})
        + '\n'
        + json.dumps({'type': 'tool_result', 'tool_call_id': 'post1', 'content': POST_COMPACTION_TOOL})
        + '\n',
    )
    retain(fx, retainer=R1)
    blocks = json.loads((fx['dest'] / 'tool-calls.json').read_text())
    contents = json.dumps(blocks)
    record(
        'original-v1-retainer-keeps-only-chat-fragment',
        POST_COMPACTION_TEXT in contents
        and POST_COMPACTION_TOOL in contents
        and PRE_COMPACTION_TOOL not in contents
        and PRE_COMPACTION_TEXT not in contents,
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-wrongupd-') as td:
    fx = make_fixture(td)
    items = default_public_updates(fx['session'])
    items[0]['params']['sessionId'] = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
    write_update_items(fx, items)

    def wrong_upd():
        retain(fx)

    catch('wrong-updates-session-refuses', wrong_upd)
    record('wrong-updates-session-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-noupdates-') as td:
    fx = make_fixture(td, write_updates=False)
    # chat_history has public tools; updates absent. Must not fall back.
    write(
        fx['transcript'],
        text='\n'.join(
            [
                json.dumps({'type': 'assistant', 'content': 'PUBLIC_ASSISTANT_TEXT', 'tool_calls': [{'id': 'c1', 'name': 'read_file', 'arguments': '{}'}]}),
                json.dumps({'type': 'tool_result', 'tool_call_id': 'c1', 'content': PUBLIC_TOOL}),
            ]
        )
        + '\n',
    )

    def missing_upd():
        retain(fx)

    catch('missing-updates-refuses', missing_upd)
    record('missing-updates-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-noprompt-') as td:
    fx = make_fixture(td)
    items = default_public_updates(fx['session'])
    items = [x for x in items if x['params']['update']['sessionUpdate'] != 'user_message_chunk']
    write_update_items(fx, items)

    def missing_prompt():
        retain(fx)

    catch('missing-prompt-refuses', missing_prompt)
    record('missing-prompt-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-duporigin-') as td:
    fx = make_fixture(td)
    items = default_public_updates(fx['session'])
    items.insert(0, update_row(fx['session'], 'user_message_chunk', content={'type': 'text', 'text': PROMPT}))
    write_update_items(fx, items)

    def dup_origin():
        retain(fx)

    catch('duplicate-origin-refuses', dup_origin)
    record('duplicate-origin-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-dupcall-') as td:
    fx = make_fixture(td)
    items = default_public_updates(fx['session'])
    dup = update_row(
        fx['session'],
        'tool_call',
        toolCallId='c1',
        title='read_file',
        rawInput={'target_file': 'other.json'},
        **{'_meta': {'x.ai/tool': {'name': 'read_file'}}},
    )
    items.insert(-1, dup)
    write_update_items(fx, items)

    def dup_call():
        retain(fx)

    catch('duplicate-tool-call-refuses', dup_call)
    record('duplicate-tool-call-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-malformed-') as td:
    fx = make_fixture(td)
    write_update_items(fx, '{"params":{"sessionId":"' + fx['session'] + '"}\n')

    def malformed():
        retain(fx)

    catch('malformed-updates-refuses', malformed)
    record('malformed-updates-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-delivery-') as td:
    session = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    items = [
        update_row(session, 'user_message_chunk', content={'type': 'text', 'text': PROMPT}),
        update_row(
            session,
            'tool_call',
            toolCallId='ok1',
            title='read_file',
            rawInput={'target_file': 'ok.json'},
            **{'_meta': {'x.ai/tool': {'name': 'read_file'}}},
        ),
        update_row(
            session,
            'tool_call_update',
            toolCallId='ok1',
            status='completed',
            content=[{'type': 'content', 'content': {'type': 'text', 'text': 'DELIVERY_OK'}}],
        ),
        update_row(
            session,
            'tool_call',
            toolCallId='fail1',
            title='grep',
            rawInput={'pattern': 'x'},
            **{'_meta': {'x.ai/tool': {'name': 'grep'}}},
        ),
        update_row(
            session,
            'tool_call_update',
            toolCallId='fail1',
            status='failed',
            content=[{'type': 'content', 'content': {'type': 'text', 'text': 'DELIVERY_FAIL'}}],
        ),
    ]
    fx = make_fixture(td, update_items=items)
    retain(fx)
    blocks = json.loads((fx['dest'] / 'tool-calls.json').read_text())
    statuses = {b.get('tool_call_id'): b.get('publicStatus') for b in blocks if b.get('type') == 'tool_result'}
    contents = json.dumps(blocks)
    record(
        'delivery-completed-and-failed-status-retained',
        statuses.get('ok1') == 'completed'
        and statuses.get('fail1') == 'failed'
        and 'DELIVERY_OK' in contents
        and 'DELIVERY_FAIL' in contents,
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-resume-') as td:
    fx = make_fixture(td)
    proc = json.loads((fx['src'] / 'process.json').read_text())
    proc['command'] = list(proc['command']) + ['--resume', 'dddddddd-dddd-dddd-dddd-dddddddddddd']
    write(fx['src'] / 'process.json', obj=proc)

    def resumed():
        retain(fx)

    catch('resume-process-refuses', resumed)
    record('resume-process-writes-nothing', not fx['dest'].exists())

# Root discriminating controls: one fresh user origin and all tool deliveries.
for variant in ('foreign-user-before', 'foreign-user-after', 'missing-terminal-delivery'):
    with tempfile.TemporaryDirectory(prefix='opensip-retain-root-stream-') as td:
        fx = make_fixture(td)
        items = default_public_updates(fx['session'])
        if variant == 'missing-terminal-delivery':
            items = items[:-1]
        else:
            foreign = update_row(fx['session'], 'user_message_chunk', content={'type':'text','text':'An additional user message outside the original prompt'})
            items.insert(0 if variant == 'foreign-user-before' else len(items), foreign)
        write_update_items(fx, items)
        catch(variant+'-refuses', lambda: retain(fx))
        record(variant+'-writes-nothing', not fx['dest'].exists())

failed = [r for r in rows if not r['passed']]
existing_failed = [r for r in rows if r['id'] in EXISTING_IDS and not r['passed']]
report = {
    'standing': (
        'Disposable retainer/public-copy tests only. Synthetic sentinel is not actual CLI thought. '
        'v1 40 behavioral assertions re-run against updates.jsonl fixtures. Additional compaction '
        'and public-source refusals are included. No application performed.'
    ),
    'passed': sum(r['passed'] for r in rows),
    'failed': [r['id'] for r in rows if not r['passed']],
    'existing40Passed': sum(1 for r in rows if r['id'] in EXISTING_IDS and r['passed']),
    'existing40Failed': [r['id'] for r in existing_failed],
    'existing40Count': len(EXISTING_IDS),
    'checks': rows,
    'actualApplicationPerformed': False,
    'testedRealPrivateCliContents': False,
}
(HERE / 'check-retain-public.v2.report.json').write_text(json.dumps(report, indent=2) + '\n')
env_ids = [r for r in rows if r['id'].startswith('v1-')]
env_report = {
    'standing': 'v1 public envelope decoder checks re-run in v2. They do not cover retainer copy.',
    'passed': sum(r['passed'] for r in env_ids),
    'failed': [r['id'] for r in env_ids if not r['passed']],
    'checks': env_ids,
    'actualApplicationPerformed': False,
}
(HERE / 'check-review-envelope.report.json').write_text(json.dumps(env_report, indent=2) + '\n')
print(
    json.dumps(
        {
            'retainAndEnvelopePassed': report['passed'],
            'failed': report['failed'],
            'existing40Passed': report['existing40Passed'],
            'existing40Count': report['existing40Count'],
            'envelopePassed': env_report['passed'],
        }
    )
)
raise SystemExit(bool(failed))
