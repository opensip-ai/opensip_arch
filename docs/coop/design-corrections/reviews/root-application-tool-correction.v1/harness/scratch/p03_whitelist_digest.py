"""P03: Grok retention whitelist + P04: parent-subject digest selector divergence.

Synthetic invented markers only. No real private content.
"""
import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import retain_public as P  # noqa: E402
import review_envelope as E  # noqa: E402

SENT = 'SYNTHETIC-INVENTED-THOUGHT-MARKER'
rows = []


def rec(probe, ident, passed, detail=''):
    rows.append({'probe': probe, 'id': ident, 'passed': bool(passed), 'detail': str(detail)[:200]})


# ---------- P03a: grok_source_is_private whitelist matrix ----------
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
    ('work/compaction/summary-note.txt', 'response.raw.json', False,
     'GAP CANDIDATE: compaction dir nested below a non-private first part'),
]
for rel, stdout_name, expected, note in MATRIX:
    got = P.grok_source_is_private(rel, stdout_name)
    rec('P03a', f'private({rel})=={expected}', got == expected, f'{note}; got={got}')

# ---------- P03b: public_grok_update_blocks drops private kinds ----------
SID = 'grok-session-0001'
PROMPT = 'synthetic launch prompt'


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
rec('P03b', 'thought-chunks-excluded', SENT + '-thought' not in blob)
rec('P03b', 'thought-delta-excluded', SENT + '-delta' not in blob)
rec('P03b', 'rawOutput-excluded', SENT + '-rawOutput' not in blob)
rec('P03b', 'compaction-summary-excluded', SENT + '-compaction-summary' not in blob)
rec('P03b', 'public-narration-retained', 'public narration' in blob)
rec('P03b', 'public-tool-output-retained', 'public tool output' in blob)
rec('P03b', 'compaction-observed-accounted', account['compactionsObserved'] == 1, account['compactionsObserved'])
rec('P03b', 'privateFieldsRetained-false', account['privateFieldsRetained'] is False)

for ident, mutate in [
    ('foreign-session-refuses', lambda ls: [ls[0].replace(SID, 'other-session')] + ls[1:]),
    ('extra-user-message-refuses', lambda ls: ls + [upd('user_message_chunk',
                                                        content={'type': 'text', 'text': 'second user turn'})]),
    ('undelivered-tool-call-refuses', lambda ls: ls[:-1]),
    ('malformed-line-refuses', lambda ls: ls + ['{not json']),
]:
    try:
        P.public_grok_update_blocks('\n'.join(mutate(list(lines))), SID, PROMPT)
        rec('P03b', ident, False, 'accepted')
    except AssertionError as e:
        rec('P03b', ident, True, e)

# ---------- P04: parent-subject digest selector divergence ----------
src = (INPUTS / 'verify-applied.py').read_text()
fn = next(n for n in ast.parse(src).body
          if isinstance(n, ast.FunctionDef) and n.name == 'review_subject_digest')
ns = {}
exec(compile(ast.Module(body=[fn], type_ignores=[]), 'verify-applied.py', 'exec'), ns)
VA = ns['review_subject_digest']

PARENT = 'a' * 64
KIT = 'b' * 64
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


def outcome(fn_, rec_):
    try:
        return 'admit:' + str(fn_(rec_))[:12]
    except Exception as e:  # noqa: BLE001
        return 'refuse:' + type(e).__name__


div = []
for ident, r in CASES:
    a, b = outcome(E.review_subject_digest, r), outcome(VA, r)
    same = a == b
    if not same:
        div.append(ident)
    rec('P04', 'selector-agrees:' + ident, same, f'review_envelope={a} verify-applied={b}')

failed = [r['probe'] + '/' + r['id'] for r in rows if not r['passed']]
print(json.dumps({'cases': len(rows), 'passed': len(rows) - len(failed),
                  'failed': failed, 'selectorDivergences': div}, indent=2))
(HERE / 'p03_whitelist_digest.result.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    if not r['passed']:
        print('DIFF', r['probe'], r['id'], '|', r['detail'])
