"""Retain an actual completed independent application review. Never apply.

Vendor envelope decode is required. Grok tool history is chat_history.jsonl
(assistant.tool_calls + tool_result). Claude tool history remains
~/.claude/projects JSONL. Do not walk Claude logs for a Grok session.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E

p = argparse.ArgumentParser()
for name in ('root', 'stage'):
    p.add_argument('--' + name, type=Path, required=True)
p.add_argument('--version', required=True)
p.add_argument('--bound-receipt', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve()
stage = a.stage.resolve()
bound = json.loads(a.bound_receipt.read_text())
vendor = bound['vendor']
dc = root / 'docs/coop/design-corrections'
src = stage.parent / ('application-review.' + a.version)
dest = dc / 'reviews' / src.name
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
mp = stage / ('application-subject.' + a.version + '.json')
manifest = json.loads(mp.read_text())
digest = sha(mp)
assert sha(root / manifest['retainedManifestPath']) == digest
launch = bound.get('launch') or {}
if vendor == 'grok':
    public_name = 'response.public.json'
    raw_name = launch.get('stdoutName', 'response.raw.json')
    public_path = src / public_name
    raw_path = src / raw_name
    if public_path.is_file():
        envelope_path = public_path
    else:
        envelope_path = raw_path
else:
    envelope_path = src / launch.get('stdoutName', 'response.json')
response = json.loads(envelope_path.read_text())
decoded = E.decode_public(response, vendor)
if vendor == 'grok' and not (src / 'response.public.json').is_file():
    (src / 'response.public.json').write_text(
        json.dumps(E.public_view(response, 'grok'), indent=2) + '\n'
    )
review = json.loads((src / 'review.json').read_text())
assert review['subjectManifestSha256'] == digest
assert review['verdict'] in ('ACCEPT', 'CHANGES_REQUIRED', 'BLOCKED')
if review['verdict'] == 'ACCEPT':
    E.require_findings_none(review, 'application')
app = json.loads((stage / 'files/docs/coop/design-corrections/application.v1.json').read_text())
session = decoded['sessionId']
prior = [
    bound['independentDesignReview']['sessionId'],
    bound['freshBlindConsumerReview']['sessionId'],
]
assert session not in prior
assert session not in C.KNOWN_GROK_COAUTHOR_SESSIONS
if vendor == 'claude':
    assert session != C.HISTORICAL_CLAUDE_EXCLUDED_SESSION


def verify():
    for field, base in [('files', stage / 'files'), ('beforeImages', stage / 'before'), ('support', stage)]:
        for row in manifest[field]:
            rel = Path(row['path'])
            assert not rel.is_absolute() and '..' not in rel.parts
            q = base / rel
            assert q.is_file() and sha(q) == row['sha256'] and q.stat().st_size == row['bytes'], str(q)


verify()
assert not dest.exists()
blocks = []
if vendor == 'grok':
    transcript = bound.get('applicationSessionTranscriptPath')
    if not transcript:
        # Independent application session transcript must be named; do not guess
        # ~/.grok/sessions from cwd encoding.
        raise AssertionError('Grok retain requires applicationSessionTranscriptPath on the bound receipt')
    log = Path(transcript)
    assert log.is_file(), 'Missing Grok chat_history.jsonl'
    for line in log.read_text().split('\n'):
        if not line:
            continue
        d = json.loads(line)
        if d.get('type') == 'assistant':
            for call in d.get('tool_calls') or []:
                if isinstance(call, dict):
                    blocks.append({'type': 'tool_call', 'block': call})
        elif d.get('type') == 'tool_result':
            blocks.append(
                {
                    'type': 'tool_result',
                    'tool_call_id': d.get('tool_call_id'),
                    'contentChars': len(str(d.get('content') or '')),
                }
            )
    assert blocks, 'Grok transcript has no tool_call/tool_result blocks'
    origin_review = 'Verbatim actual Grok independent application review output'
else:
    logs = list(Path('/Users/sb/.claude/projects').glob('*/' + session + '.jsonl'))
    assert len(logs) == 1
    for line in logs[0].read_text().split('\n'):
        if not line:
            continue
        d = json.loads(line)
        content = d.get('message', {}).get('content', [])
        for b in content if isinstance(content, list) else []:
            if isinstance(b, dict) and b.get('type') in ('tool_use', 'tool_result'):
                blocks.append({'timestamp': d.get('timestamp'), 'messageUuid': d.get('uuid'), 'block': b})
    assert blocks
    origin_review = 'Verbatim actual Claude independent application review output'
dest.mkdir()
rows = []
excluded = []
deltas = []
for q in sorted(src.rglob('*')):
    if not q.is_file() or '__pycache__' in q.parts:
        continue
    rel = q.relative_to(src)
    if rel.parts[0] in ('work', 'scratch', 'verify'):
        sub = Path(*rel.parts[1:])
        matches = [base / sub for base in (stage, root)]
        if any(x.is_file() and sha(x) == sha(q) for x in matches):
            excluded.append(str(rel))
            continue
        deltas.append(str(rel))
    t = dest / rel
    t.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(q, t)
    origin = (
        'Codex orchestration metadata'
        if q.name in ('prompt.txt', 'process.json')
        else origin_review
    )
    rows.append({'path': str(rel), 'sha256': sha(t), 'bytes': t.stat().st_size, 'origin': origin})
t = dest / 'tool-calls.json'
t.write_text(json.dumps(blocks, indent=2) + '\n')
verify()
retention_name = 'codex-retention-custody.json' if (dest / 'custody.json').exists() else 'custody.json'
(dest / retention_name).write_text(
    json.dumps(
        {
            'standing': (
                'Actual fresh independent application review; only its substantive exact-subject '
                'verdict grants scope. Retention does not apply documentation. Private thought is not retained.'
            ),
            'vendor': vendor,
            'sessionId': session,
            'differentFromDesignAndBlindSessions': prior,
            'manifestSha256': digest,
            'packageRoot': str(stage),
            'packageBeforeAndAfterRetentionVerified': True,
            'files': rows,
            'toolBlocks': {
                'path': 'tool-calls.json',
                'sha256': sha(t),
                'count': len(blocks),
                'selection': (
                    'Grok: assistant.tool_calls + tool_result from named chat_history.jsonl; '
                    'Claude: tool_use/tool_result from session JSONL. No private thinking retained.'
                ),
            },
            'excludedExactDisposableCopies': excluded,
            'retainedDisposableDeltas': deltas,
            'implementationAuthorized': False,
            'qualificationClaimed': False,
        },
        indent=2,
    )
    + '\n'
)
print(session, review['verdict'], len(rows), 'outputs', len(blocks), 'tool blocks', vendor)
