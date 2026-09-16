"""P02: retain-application-review.successor.v1.py boundary probes (vendor=claude).

Author-origin exclusion for the FINAL application review, coauthor-process refusal,
cross-subject refusal, and public-only retention of the CLI envelope.
Synthetic invented sentinels only; no real private content is used anywhere.
"""
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import coverage_contract as C  # noqa: E402

spec = importlib.util.spec_from_file_location(
    'retain_app', INPUTS / 'retain-application-review.successor.v1.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

DESIGN_S = 'aaaaaaaa-0000-4000-8000-000000000001'
BLIND_S = 'bbbbbbbb-0000-4000-8000-000000000002'
FRESH_S = 'ffffffff-0000-4000-8000-00000000000f'
# Synthetic invented marker. NOT real private reasoning of any kind.
SENTINEL = 'SYNTHETIC-INVENTED-PRIVATE-MARKER-DO-NOT-RETAIN'

CLAUDE_LOG = '\n'.join(json.dumps(x) for x in [
    {'uuid': 'u1', 'timestamp': 't1', 'message': {'content': [
        {'type': 'thinking', 'thinking': SENTINEL + '-in-session-log'},
        {'type': 'text', 'text': 'public narration'},
        {'type': 'tool_use', 'id': 'tu1', 'name': 'Read', 'input': {'file_path': '/x'}}]}},
    {'uuid': 'u2', 'timestamp': 't2', 'message': {'content': [
        {'type': 'tool_result', 'tool_use_id': 'tu1', 'content': 'public tool output'}]}},
])

rows = []


def build(base, *, session=FRESH_S, verdict='ACCEPT', subject_ok=True,
          process=None, envelope_extra=None):
    base = Path(base)
    root, stage, src = base / 'root', base / 'stage', base / 'src'
    (stage / 'files/docs').mkdir(parents=True)
    (stage / 'files/docs/x.md').write_text('synthetic staged doc\n')
    src.mkdir(parents=True)
    sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest = {
        'standing': 'SYNTHETIC FIXTURE ONLY',
        'retainedManifestPath': 'docs/coop/design-corrections/reviews/application-subject.v3.json',
        'files': [{'path': 'docs/x.md', 'sha256': sh(stage / 'files/docs/x.md'),
                   'bytes': (stage / 'files/docs/x.md').stat().st_size}],
        'beforeImages': [], 'support': [],
    }
    mp = stage / 'application-subject.v3.json'
    mp.write_text(json.dumps(manifest, indent=2) + '\n')
    digest = sh(mp)
    ret = root / manifest['retainedManifestPath']
    ret.parent.mkdir(parents=True, exist_ok=True)
    ret.write_bytes(mp.read_bytes())

    (src / 'review.json').write_text(json.dumps({
        'standing': 'SYNTHETIC FIXTURE ONLY. Not actual review evidence.',
        'verdict': verdict,
        'subjectManifestSha256': digest if subject_ok else 'e' * 64,
        'newMustIssues': [], 'newShouldIssues': []}, indent=2))
    env = {'is_error': False, 'session_id': session, 'result': 'synthetic public result'}
    if envelope_extra:
        env.update(envelope_extra)
    (src / 'response.json').write_text(json.dumps(env, indent=2))
    (src / 'prompt.txt').write_text('synthetic prompt\n')
    if process is not None:
        (src / 'process.json').write_text(json.dumps(process, indent=2))
    bound = {'vendor': 'claude', 'launch': {'stdoutName': 'response.json'},
             'independentDesignReview': {'sessionId': DESIGN_S},
             'freshBlindConsumerReview': {'sessionId': BLIND_S}}
    return root, stage, src, base / 'dest', bound


def case(ident, expect, scope, **kw):
    with tempfile.TemporaryDirectory(prefix='opensip-retain-probe-') as td:
        root, stage, src, dest, bound = build(td, **kw)
        err = ''
        try:
            R.run_retain(root=root, stage=stage, version='v3', bound=bound,
                         dest=dest, src=src, claude_log_text=CLAUDE_LOG)
            accepted = True
        except Exception as e:  # noqa: BLE001
            accepted, err = False, f'{type(e).__name__}: {e}'[:160]
        leaked = None
        if dest.exists():
            hits = [str(q.relative_to(dest)) for q in dest.rglob('*')
                    if q.is_file() and SENTINEL.encode() in q.read_bytes()]
            leaked = hits
        rows.append({'id': ident, 'scope': scope, 'expected': expect,
                     'observed': 'RETAINED' if accepted else 'REFUSED',
                     'asExpected': accepted is (expect == 'RETAINED'),
                     'sentinelInRetainedCopy': leaked, 'detail': err})


case('control-fresh-session-retains', 'RETAINED', 'control')

# Independent reviewer-origin exclusion for the FINAL application review.
for i, s in enumerate(C.KNOWN_CLAUDE_COAUTHOR_SESSIONS, 1):
    case(f'retain-claude-author-origin-{i}', 'REFUSED', 'author-origin-exclusion', session=s)
for i, s in enumerate(C.KNOWN_GROK_COAUTHOR_SESSIONS, 1):
    case(f'retain-grok-coauthor-origin-{i}', 'REFUSED', 'author-origin-exclusion', session=s)
case('retain-historical-excluded-claude-session', 'REFUSED', 'author-origin-exclusion',
     session=C.HISTORICAL_CLAUDE_EXCLUDED_SESSION)
case('retain-reuses-design-session', 'REFUSED', 'distinct-origin', session=DESIGN_S)
case('retain-reuses-blind-session', 'REFUSED', 'distinct-origin', session=BLIND_S)

# Coauthor process standing / resume, claude vendor.
case('retain-coauthor-process-standing', 'REFUSED', 'coauthor-process',
     process={'standing': 'Actual Claude coauthor; no source acceptance', 'sessionId': FRESH_S})
case('retain-process-resuming-claude-author-origin', 'REFUSED', 'coauthor-process',
     process={'standing': 'Independent review', 'sessionId': FRESH_S,
              'command': ['claude', '--resume', C.KNOWN_CLAUDE_COAUTHOR_SESSIONS[0]]})

# Exact subject custody.
case('retain-cross-subject-review', 'REFUSED', 'subject-custody', subject_ok=False)
case('retain-accepts-changes-required-verdict', 'RETAINED', 'verdict-passthrough',
     verdict='CHANGES_REQUIRED')

# Public-only retention: synthetic private key in the Claude CLI envelope.
case('retain-claude-envelope-with-private-key', 'RETAINED', 'public-only-retention',
     envelope_extra={'thinking': SENTINEL + '-in-cli-envelope'})

failed = [r['id'] for r in rows if not r['asExpected']]
leaks = [r['id'] for r in rows if r['sentinelInRetainedCopy']]
print(json.dumps({'probe': 'P02-retain', 'cases': len(rows),
                  'asExpected': len(rows) - len(failed), 'unexpected': failed,
                  'sentinelLeaks': leaks}, indent=2))
(HERE / 'p02_retain.result.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    print(('ok  ' if r['asExpected'] else 'DIFF'), r['id'], '->', r['observed'],
          '| leak:', r['sentinelInRetainedCopy'], '|', r['detail'])
