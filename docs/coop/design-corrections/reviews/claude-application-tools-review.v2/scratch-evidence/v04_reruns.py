"""V04: re-run the v1 discriminating probes (P01 bind, P02 retain, P03/P04 whitelist+digest)
against the CORRECTED v2 inputs, with expectations updated where root declared a new selection.
"""
import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INPUTS))
import fixture as F  # noqa: E402
import coverage_contract as C  # noqa: E402
import retain_public as P  # noqa: E402
import review_envelope as E  # noqa: E402

REF = '/tmp/opensip-architecture-review-env/bin/python'
BIND = INPUTS / 'bind-review-receipts.v1.py'
out = {}

# ============================ P01: bind ============================
p01 = []


def bcase(ident, expect, **kw):
    with tempfile.TemporaryDirectory(prefix='opensip-bind-') as td:
        rp, o, _ = F.build(td, **kw)
        r = subprocess.run([REF, '-I', '-B', str(BIND), '--receipt', str(rp), '--out', str(o)],
                           capture_output=True, text=True, cwd=str(HERE))
        acc = r.returncode == 0 and o.exists()
        p01.append({'id': ident, 'expected': expect, 'observed': 'ACCEPT' if acc else 'REFUSE',
                    'asExpected': acc is (expect == 'ACCEPT'),
                    'detail': (r.stderr.strip().splitlines() or [''])[-1][:140]})


bcase('control-fresh-sessions-bind', 'ACCEPT')
for i, s in enumerate(C.KNOWN_CLAUDE_COAUTHOR_SESSIONS, 1):
    bcase(f'bind-refuses-claude-author-origin-{i}-as-design', 'REFUSE', design_session=s)
    bcase(f'bind-refuses-claude-author-origin-{i}-as-blind', 'REFUSE', blind_session=s)
for i, s in enumerate(C.KNOWN_GROK_COAUTHOR_SESSIONS, 1):
    bcase(f'bind-refuses-grok-coauthor-origin-{i}-as-design', 'REFUSE', vendor='grok', design_session=s)
bcase('bind-refuses-historical-excluded-claude-session', 'REFUSE',
      design_session=C.HISTORICAL_CLAUDE_EXCLUDED_SESSION)
bcase('bind-refuses-blind-reusing-design-session', 'REFUSE', blind_session=F.FRESH_DESIGN_SESSION)
bcase('bind-refuses-blind-kit-naming-other-parent', 'REFUSE', blind_parent='e' * 64)
bcase('bind-refuses-assent-naming-other-subject', 'REFUSE', assent_subject='e' * 64)
bcase('bind-refuses-assent-naming-other-reviewer-session', 'REFUSE',
      assent_session='cccccccc-0000-4000-8000-000000000003')
bcase('bind-refuses-missing-root-design-assent', 'REFUSE', drop_assent=True)
bcase('bind-refuses-coauthor-process-standing', 'REFUSE',
      design_process={'standing': 'Actual Claude coauthor; no source acceptance',
                      'sessionId': F.FRESH_DESIGN_SESSION})
bcase('bind-refuses-process-resuming-claude-author-origin', 'REFUSE',
      design_process={'standing': 'Independent review', 'sessionId': F.FRESH_DESIGN_SESSION,
                      'command': ['claude', '--resume', C.KNOWN_CLAUDE_COAUTHOR_SESSIONS[0]]})
bcase('bind-refuses-process-session-not-matching-envelope', 'REFUSE',
      design_process={'standing': 'Independent review', 'sessionId': 'dddddddd-0000-4000-8000-000000000004'})
bcase('bind-refuses-shape-only-receipt', 'REFUSE',
      receipt_overrides={'standing': 'SHAPE ONLY. Not a bound receipt.'})
bcase('bind-refuses-receipt-preclaiming-readyForAssembly', 'REFUSE',
      receipt_overrides={'readyForAssembly': True})
bcase('bind-refuses-non-accept-design-verdict-requirement', 'REFUSE',
      design_spec_overrides={'requiredVerdict': 'CHANGES_REQUIRED'})
out['P01'] = p01

# ============================ P02: retain ============================
spec = importlib.util.spec_from_file_location(
    'retain_app', INPUTS / 'retain-application-review.successor.v1.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

DESIGN_S = 'aaaaaaaa-0000-4000-8000-000000000001'
BLIND_S = 'bbbbbbbb-0000-4000-8000-000000000002'
FRESH_S = 'ffffffff-0000-4000-8000-00000000000f'
SENTINEL = 'SYNTHETIC-INVENTED-PRIVATE-MARKER-DO-NOT-RETAIN'
CLAUDE_LOG = '\n'.join(json.dumps(x) for x in [
    {'uuid': 'u1', 'timestamp': 't1', 'message': {'content': [
        {'type': 'thinking', 'thinking': SENTINEL + '-in-session-log'},
        {'type': 'text', 'text': 'public narration'},
        {'type': 'tool_use', 'id': 'tu1', 'name': 'Read', 'input': {'file_path': '/x'}}]}},
    {'uuid': 'u2', 'timestamp': 't2', 'message': {'content': [
        {'type': 'tool_result', 'tool_use_id': 'tu1', 'content': 'public tool output'}]}},
])
p02 = []


def rbuild(base, *, session=FRESH_S, verdict='ACCEPT', subject_ok=True,
           process=None, envelope_extra=None):
    base = Path(base)
    root, stage, src = base / 'root', base / 'stage', base / 'src'
    (stage / 'files/docs').mkdir(parents=True)
    (stage / 'files/docs/x.md').write_text('synthetic staged doc\n')
    src.mkdir(parents=True)
    sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest = {'standing': 'SYNTHETIC FIXTURE ONLY',
                'retainedManifestPath': 'docs/coop/design-corrections/reviews/application-subject.v3.json',
                'files': [{'path': 'docs/x.md', 'sha256': sh(stage / 'files/docs/x.md'),
                           'bytes': (stage / 'files/docs/x.md').stat().st_size}],
                'beforeImages': [], 'support': []}
    mp = stage / 'application-subject.v3.json'
    mp.write_text(json.dumps(manifest, indent=2) + '\n')
    digest = sh(mp)
    ret = root / manifest['retainedManifestPath']
    ret.parent.mkdir(parents=True, exist_ok=True)
    ret.write_bytes(mp.read_bytes())
    (src / 'review.json').write_text(json.dumps({
        'standing': 'SYNTHETIC FIXTURE ONLY.', 'verdict': verdict,
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


def rcase(ident, expect, scope, **kw):
    with tempfile.TemporaryDirectory(prefix='opensip-retain-') as td:
        root, stage, src, dest, bound = rbuild(td, **kw)
        err = ''
        try:
            R.run_retain(root=root, stage=stage, version='v3', bound=bound,
                         dest=dest, src=src, claude_log_text=CLAUDE_LOG)
            acc = True
        except Exception as e:  # noqa: BLE001
            acc, err = False, f'{type(e).__name__}: {e}'[:140]
        leak, retained = None, None
        if dest.exists():
            leak = [str(q.relative_to(dest)) for q in dest.rglob('*')
                    if q.is_file() and SENTINEL.encode() in q.read_bytes()]
            retained = sorted(str(q.relative_to(dest)) for q in dest.rglob('*') if q.is_file())
        p02.append({'id': ident, 'scope': scope, 'expected': expect,
                    'observed': 'RETAINED' if acc else 'REFUSED',
                    'asExpected': acc is (expect == 'RETAINED'),
                    'sentinelInRetainedCopy': leak, 'retainedFiles': retained, 'detail': err})


rcase('control-fresh-session-retains', 'RETAINED', 'control')
for i, s in enumerate(C.KNOWN_CLAUDE_COAUTHOR_SESSIONS, 1):
    rcase(f'retain-claude-author-origin-{i}', 'REFUSED', 'author-origin-exclusion', session=s)
for i, s in enumerate(C.KNOWN_GROK_COAUTHOR_SESSIONS, 1):
    rcase(f'retain-grok-coauthor-origin-{i}', 'REFUSED', 'author-origin-exclusion', session=s)
rcase('retain-historical-excluded-claude-session', 'REFUSED', 'author-origin-exclusion',
      session=C.HISTORICAL_CLAUDE_EXCLUDED_SESSION)
rcase('retain-reuses-design-session', 'REFUSED', 'distinct-origin', session=DESIGN_S)
rcase('retain-reuses-blind-session', 'REFUSED', 'distinct-origin', session=BLIND_S)
rcase('retain-coauthor-process-standing', 'REFUSED', 'coauthor-process',
      process={'standing': 'Actual Claude coauthor; no source acceptance', 'sessionId': FRESH_S})
rcase('retain-process-resuming-claude-author-origin', 'REFUSED', 'coauthor-process',
      process={'standing': 'Independent review', 'sessionId': FRESH_S,
               'command': ['claude', '--resume', C.KNOWN_CLAUDE_COAUTHOR_SESSIONS[0]]})
rcase('retain-cross-subject-review', 'REFUSED', 'subject-custody', subject_ok=False)
rcase('retain-accepts-changes-required-verdict', 'RETAINED', 'verdict-passthrough',
      verdict='CHANGES_REQUIRED')
rcase('retain-claude-envelope-with-private-key', 'RETAINED', 'public-only-retention',
      envelope_extra={'thinking': SENTINEL + '-in-cli-envelope'})
rcase('retain-claude-envelope-with-unknown-extra-key', 'RETAINED', 'public-only-retention',
      envelope_extra={'internalScratchpad': SENTINEL + '-nonwhitelisted-key'})
out['P02'] = p02

# ============================ P03/P04 ============================
p03 = []


def rec(probe, ident, passed, detail=''):
    p03.append({'probe': probe, 'id': ident, 'passed': bool(passed), 'detail': str(detail)[:180]})


MATRIX = [
    ('response.raw.json', 'response.raw.json', True, 'default CLI stdout'),
    ('chat_history.jsonl', 'response.raw.json', True, 'raw transcript'),
    ('updates.jsonl', 'response.raw.json', True, 'authenticated update source'),
    ('events.jsonl', 'response.raw.json', True, 'private events'),
    ('system_prompt.txt', 'response.raw.json', True, 'private prompt state'),
    ('compaction/summary.json', 'response.raw.json', True, 'top-level compaction dir'),
    ('terminal/out.txt', 'response.raw.json', True, 'top-level terminal dir'),
    ('nested/custom-name.json', 'nested/custom-name.json', True, 'custom stdoutName, nested'),
    ('review.json', 'response.raw.json', False, 'authored review must be retained'),
    ('prompt.txt', 'response.raw.json', False, 'orchestration prompt retained'),
    ('work/probe.py', 'response.raw.json', False, 'disposable probe delta retained'),
    # NEW SELECTION declared by root: nested private dirs are now excluded.
    ('work/compaction/summary-note.txt', 'response.raw.json', True,
     'NEW EXPECTATION (v1 informational gap F10 now closed)'),
    ('a/b/terminal/x.txt', 'response.raw.json', True, 'deeply nested terminal dir'),
]
for rel, sn, expected, note in MATRIX:
    got = P.grok_source_is_private(rel, sn)
    rec('P03a', f'private({rel})=={expected}', got == expected, f'{note}; got={got}')

SENT = 'SYNTHETIC-INVENTED-THOUGHT-MARKER'
SID, PROMPT = 'grok-session-0001', 'synthetic launch prompt'


def upd(kind, **u):
    u['sessionUpdate'] = kind
    return json.dumps({'params': {'sessionId': SID, 'update': u, '_meta': {'eventId': 'e'}}})


lines = [
    upd('user_message_chunk', content={'type': 'text', 'text': PROMPT}),
    upd('agent_thought_chunk', content={'type': 'text', 'text': SENT + '-thought'}),
    upd('thought_delta', content={'type': 'text', 'text': SENT + '-delta'}),
    upd('agent_message_chunk', content={'type': 'text', 'text': 'public narration'}),
    upd('tool_call', toolCallId='t1', title='Read', rawInput={'path': '/x'},
        rawOutput={'secret': SENT + '-rawOutput'}),
    upd('auto_compact_completed', summary=SENT + '-compaction-summary'),
    upd('tool_call_update', toolCallId='t1', status='completed',
        content=[{'type': 'content', 'content': {'type': 'text', 'text': 'public tool output'}}]),
]
blocks, account = P.public_grok_update_blocks('\n'.join(lines), SID, PROMPT)
blob = json.dumps(blocks)
for ident, cond in [('thought-chunks-excluded', SENT + '-thought' not in blob),
                    ('thought-delta-excluded', SENT + '-delta' not in blob),
                    ('rawOutput-excluded', SENT + '-rawOutput' not in blob),
                    ('compaction-summary-excluded', SENT + '-compaction-summary' not in blob),
                    ('public-narration-retained', 'public narration' in blob),
                    ('public-tool-output-retained', 'public tool output' in blob),
                    ('compaction-observed-accounted', account['compactionsObserved'] == 1),
                    ('privateFieldsRetained-false', account['privateFieldsRetained'] is False)]:
    rec('P03b', ident, cond)
for ident, mutate in [
    ('foreign-session-refuses', lambda ls: [ls[0].replace(SID, 'other-session')] + ls[1:]),
    ('extra-user-message-refuses', lambda ls: ls + [upd('user_message_chunk',
                                                        content={'type': 'text', 'text': 'second turn'})]),
    ('undelivered-tool-call-refuses', lambda ls: ls[:-1]),
    ('malformed-line-refuses', lambda ls: ls + ['{not json']),
]:
    try:
        P.public_grok_update_blocks('\n'.join(mutate(list(lines))), SID, PROMPT)
        rec('P03b', ident, False, 'accepted')
    except AssertionError as e:
        rec('P03b', ident, True, e)

src = (INPUTS / 'verify-applied.py').read_text()
fn = next(n for n in ast.parse(src).body
          if isinstance(n, ast.FunctionDef) and n.name == 'review_subject_digest')
ns = {}
sys.path.insert(0, str(INPUTS))
exec(compile(ast.Module(body=[fn], type_ignores=[]), 'verify-applied.py', 'exec'), ns)
VA = ns['review_subject_digest']
PARENT, KIT = 'a' * 64, 'b' * 64
CASES = [
    ('top-level-only', {'subjectManifestSha256': PARENT}),
    ('nested-only', {'subject': {'manifestSha256': PARENT}}),
    ('inputKit-parentSubject-only', {'inputKit': {'parentSubjectSha256': PARENT, 'manifestSha256': KIT}}),
    ('declared-null-beside-valid', {'subjectManifestSha256': None,
                                    'inputKit': {'parentSubjectSha256': PARENT}}),
    ('uppercase-digest', {'subjectManifestSha256': PARENT.upper()}),
    ('wrong-length-digest', {'subjectManifestSha256': 'aa'}),
    ('nonobject-inputKit', {'inputKit': None, 'subjectManifestSha256': PARENT}),
    ('kit-digest-only', {'inputKit': {'manifestSha256': KIT}}),
]


def outcome(f, r):
    try:
        return 'admit:' + str(f(r))[:12]
    except Exception as e:  # noqa: BLE001
        return 'refuse:' + type(e).__name__


div = []
for ident, r in CASES:
    a, b = outcome(E.review_subject_digest, r), outcome(VA, r)
    if a != b:
        div.append(ident)
    rec('P04', 'selector-agrees:' + ident, a == b, f'shared={a} verify-applied={b}')
out['P03_P04'] = p03
out['P04_divergences'] = div

(HERE / 'v04_reruns.result.json').write_text(json.dumps(out, indent=2) + '\n')
for key, rowset in [('P01', p01), ('P02', p02)]:
    bad = [r['id'] for r in rowset if not r['asExpected']]
    print(f'{key}: {len(rowset)} cases, {len(rowset) - len(bad)} as expected, unexpected={bad}')
leaks = [r['id'] for r in p02 if r['sentinelInRetainedCopy']]
print('P02 sentinel leaks:', leaks)
bad3 = [r['probe'] + '/' + r['id'] for r in p03 if not r['passed']]
print(f'P03+P04: {len(p03)} checks, {len(p03) - len(bad3)} passed, failed={bad3}')
print('P04 selector divergences:', div)
ctrl = next(r for r in p02 if r['id'] == 'control-fresh-session-retains')
print('control retained files:', ctrl['retainedFiles'])
priv = next(r for r in p02 if r['id'] == 'retain-claude-envelope-with-private-key')
print('private-key case retained files:', priv['retainedFiles'], '| leak:', priv['sentinelInRetainedCopy'])
