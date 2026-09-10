"""Disposable retainer/launch public-copy tests. No live application retain. No real CLI logs."""
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
rows = []


def record(ident, passed, detail=''):
    rows.append({'id': ident, 'passed': bool(passed), 'detail': detail})


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = load_mod('retain_app_v2', HERE / 'retain-application-review.successor.v1.py')


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


def make_fixture(td, stdout_name='cli-envelope.json', session='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'):
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
    write(
        src / 'process.json',
        obj={
            'command': ['/Users/sb/.grok/bin/grok', '--cwd', str(cwd), '--permission-mode', 'acceptEdits'],
            'cwd': str(cwd),
            'standing': 'Independent application review launch metadata; not a verdict.',
            'stdoutName': stdout_name,
        },
    )
    write(src / 'prompt.txt', text='synthetic prompt names absolute stage\n')
    transcript = P.grok_transcript_path(str(cwd), session, sessions_root=sessions)
    write(
        transcript,
        text='\n'.join(
            [
                json.dumps(
                    {
                        'type': 'assistant',
                        'content': 'PUBLIC_ASSISTANT_TEXT',
                        'tool_calls': [{'id': 'c1', 'name': 'read_file', 'arguments': '{"target_file":"review.json"}'}],
                        'model_id': 'grok-4.6-build',
                    }
                ),
                json.dumps({'type': 'tool_result', 'tool_call_id': 'c1', 'content': PUBLIC_TOOL}),
                json.dumps({'type': 'reasoning', 'encrypted_content': SENTINEL, 'summary': SENTINEL}),
            ]
        )
        + '\n',
    )
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
    }


def catch(ident, fn):
    try:
        fn()
        record(ident, False, 'expected refusal')
    except AssertionError:
        record(ident, True)
    except Exception as e:
        record(ident, False, type(e).__name__)


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
    result = R.run_retain(
        root=fx['root'],
        stage=fx['stage'],
        version='t1',
        bound=fx['bound'],
        dest=fx['dest'],
        sessions_root=fx['sessions'],
        src=fx['src'],
    )
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
    R.run_retain(
        root=fx['root'],
        stage=fx['stage'],
        version='t1',
        bound=fx['bound'],
        dest=fx['dest'],
        sessions_root=fx['sessions'],
        src=fx['src'],
    )
    names = {p.name for p in fx['dest'].rglob('*') if p.is_file()}
    record(
        'default-response.raw.json-not-copied',
        'response.raw.json' not in names and P.dest_contains_sentinel(fx['dest'], SENTINEL) is None,
    )

with tempfile.TemporaryDirectory(prefix='opensip-retain-wrong-') as td:
    fx = make_fixture(td)
    other = Path(td) / 'sessions' / 'other' / fx['session'] / 'chat_history.jsonl'
    write(other, text=json.dumps({'type': 'assistant', 'content': 'nope'}) + '\n')
    fx['bound']['applicationSessionTranscriptPath'] = str(other)

    def wrong():
        R.run_retain(
            root=fx['root'],
            stage=fx['stage'],
            version='t1',
            bound=fx['bound'],
            dest=fx['dest'],
            sessions_root=fx['sessions'],
            src=fx['src'],
        )

    catch('wrong-session-path-refuses', wrong)
    record('wrong-session-path-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-cancel-') as td:
    fx = make_fixture(td)
    write(fx['src'] / fx['stdout_name'], obj=grok_ok(stopReason='cancelled', thought=SENTINEL))

    def cancelled():
        R.run_retain(
            root=fx['root'],
            stage=fx['stage'],
            version='t1',
            bound=fx['bound'],
            dest=fx['dest'],
            sessions_root=fx['sessions'],
            src=fx['src'],
        )

    catch('cancelled-envelope-refuses', cancelled)
    record('cancelled-writes-nothing', not fx['dest'].exists())

with tempfile.TemporaryDirectory(prefix='opensip-retain-coauthor-') as td:
    fx = make_fixture(td)
    proc = json.loads((fx['src'] / 'process.json').read_text())
    proc['standing'] = 'Actual Grok coauthor; no source acceptance'
    write(fx['src'] / 'process.json', obj=proc)

    def coauthor():
        R.run_retain(
            root=fx['root'],
            stage=fx['stage'],
            version='t1',
            bound=fx['bound'],
            dest=fx['dest'],
            sessions_root=fx['sessions'],
            src=fx['src'],
        )

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
prepared_retain = (PREPARED / 'retain-application-review.successor.v1.py').read_text()
record(
    'v1-prepared-retainer-still-rglob-copies-raw',
    'for q in sorted(src.rglob' in prepared_retain
    and 'excludedPrivateSources' not in prepared_retain
    and "public_name = 'response.public.json'" in prepared_retain,
)

failed = [r for r in rows if not r['passed']]
report = {
    'standing': (
        'Disposable retainer/public-copy tests only. Synthetic sentinel is not actual CLI thought. '
        'v1 envelope 20 checks did not cover the retainer rglob leak. No application performed.'
    ),
    'passed': sum(r['passed'] for r in rows),
    'failed': [r['id'] for r in rows if not r['passed']],
    'checks': rows,
    'actualApplicationPerformed': False,
    'testedRealPrivateCliContents': False,
}
(HERE / 'check-retain-public.report.json').write_text(json.dumps(report, indent=2) + '\n')
env_ids = [r for r in rows if r['id'].startswith('v1-')]
env_report = {
    'standing': 'v1 public envelope decoder checks re-run in v2. They do not cover retainer copy.',
    'passed': sum(r['passed'] for r in env_ids),
    'failed': [r['id'] for r in env_ids if not r['passed']],
    'checks': env_ids,
    'actualApplicationPerformed': False,
}
(HERE / 'check-review-envelope.report.json').write_text(json.dumps(env_report, indent=2) + '\n')
print(json.dumps({'retainAndEnvelopePassed': report['passed'], 'failed': report['failed'], 'envelopePassed': env_report['passed']}))
raise SystemExit(bool(failed))
