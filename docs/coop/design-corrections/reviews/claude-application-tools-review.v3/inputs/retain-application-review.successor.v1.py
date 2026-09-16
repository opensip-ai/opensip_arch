"""Retain an actual completed independent application review. Never apply.

Grok: copy authored review/probes/reports/custody; write whitelisted public
envelope and public assistant/tool records from authenticated updates.jsonl.
Do not copy the CLI raw envelope (wherever launch.stdoutName placed it),
raw chat_history, updates.jsonl, thought chunks, compaction summaries, or
rawOutput. Post-compaction chat_history is not a complete public record.
Claude: unchanged explicit tool_use/tool_result selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREPARED = HERE / 'prepared'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PREPARED))
import coverage_contract as C
import retain_public as P
import review_envelope as E


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def run_retain(
    *,
    root,
    stage,
    version,
    bound,
    dest=None,
    sessions_root=None,
    src=None,
    claude_log_text=None,
):
    root = Path(root).resolve()
    stage = Path(stage).resolve()
    vendor = bound['vendor']
    dc = root / 'docs/coop/design-corrections'
    src = Path(src).resolve() if src is not None else (stage.parent / ('application-review.' + version)).resolve()
    dest = Path(dest).resolve() if dest is not None else (dc / 'reviews' / src.name)
    mp = stage / ('application-subject.' + version + '.json')
    manifest = load(mp)
    digest = sha(mp)
    assert sha(root / manifest['retainedManifestPath']) == digest
    launch = bound.get('launch') or {}
    process = load(src / 'process.json') if (src / 'process.json').is_file() else None
    E.refuse_coauthor_process(process, 'independent-application')
    if vendor == 'grok':
        P.require_fresh_grok_process(process)
        stdout_name = P.stdout_basename(launch)
        public_path = src / P.GROK_PUBLIC_RESPONSE_NAME
        raw_path = src / stdout_name
        if public_path.is_file() and not P.envelope_has_private_keys(load(public_path)):
            envelope = load(public_path)
        else:
            assert raw_path.is_file(), 'Missing Grok CLI envelope: ' + stdout_name
            envelope = load(raw_path)
        decoded = E.decode_public(envelope, 'grok')
    else:
        stdout_name = launch.get('stdoutName', 'response.json')
        envelope_path = src / Path(stdout_name).name
        envelope = load(envelope_path)
        decoded = E.decode_public(envelope, 'claude')
    review = load(src / 'review.json')
    assert review['subjectManifestSha256'] == digest
    assert review['verdict'] in ('ACCEPT', 'CHANGES_REQUIRED', 'BLOCKED')
    if review['verdict'] == 'ACCEPT':
        E.require_findings_none(review, 'application')
    session = decoded['sessionId']
    prior = [
        bound['independentDesignReview']['sessionId'],
        bound['freshBlindConsumerReview']['sessionId'],
    ]
    assert session not in prior
    assert session not in C.KNOWN_COAUTHOR_SESSIONS
    if vendor == 'claude':
        assert session != C.HISTORICAL_CLAUDE_EXCLUDED_SESSION

    def verify():
        for field, base in [('files', stage / 'files'), ('beforeImages', stage / 'before'), ('support', stage)]:
            for row in manifest.get(field) or []:
                rel = Path(row['path'])
                assert not rel.is_absolute() and '..' not in rel.parts
                q = base / rel
                assert q.is_file() and sha(q) == row['sha256'] and q.stat().st_size == row['bytes'], str(q)

    verify()
    assert not dest.exists()
    blocks = []
    excluded_private = []
    update_account = None
    if vendor == 'grok':
        cwd = P.command_cwd(process)
        transcript = bound.get('applicationSessionTranscriptPath')
        if not transcript:
            transcript = str(P.grok_transcript_path(cwd, session, sessions_root=sessions_root))
        P.require_named_grok_transcript(transcript, cwd, session, sessions_root=sessions_root)
        updates = P.require_grok_updates(cwd, session, sessions_root=sessions_root)
        prompt_path = src / 'prompt.txt'
        assert prompt_path.is_file(), 'Missing launch prompt.txt'
        blocks, update_account = P.public_grok_update_blocks(
            updates.read_text(), session, prompt_path.read_text()
        )
        origin_review = 'Verbatim actual Grok independent application review output'
    else:
        if claude_log_text is None:
            logs = list(Path('/Users/sb/.claude/projects').glob('*/' + session + '.jsonl'))
            assert len(logs) == 1
            claude_log_text = logs[0].read_text()
        blocks = P.claude_selected_tool_blocks(claude_log_text)
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
        if P.grok_source_is_private(rel, stdout_name, vendor):
            excluded_private.append(str(rel))
            continue
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
    if vendor == 'grok':
        public_body = E.public_view(envelope, 'grok')
        assert not P.envelope_has_private_keys(public_body)
        tpub = dest / P.GROK_PUBLIC_RESPONSE_NAME
        tpub.write_text(json.dumps(public_body, indent=2) + '\n')
        rows = [r for r in rows if r['path'] != P.GROK_PUBLIC_RESPONSE_NAME]
        rows.append(
            {
                'path': P.GROK_PUBLIC_RESPONSE_NAME,
                'sha256': sha(tpub),
                'bytes': tpub.stat().st_size,
                'origin': 'Whitelisted Grok public envelope; CLI raw stdout excluded',
            }
        )
    if vendor == 'claude':
        # Never copy CLI stdout wholesale. Preserve its expected retained name,
        # but write only the explicitly selected public result members.
        public_body = E.public_view(envelope, 'claude')
        assert not P.envelope_has_private_keys(public_body)
        tpub = dest / Path(stdout_name).name
        tpub.write_text(json.dumps(public_body, indent=2) + '\n')
        rows = [r for r in rows if r['path'] != tpub.name]
        rows.append({'path': tpub.name, 'sha256': sha(tpub),
                     'bytes': tpub.stat().st_size,
                     'origin': 'Whitelisted Claude public envelope; raw stdout excluded'})
    t = dest / 'tool-calls.json'
    t.write_text(json.dumps(blocks, indent=2) + '\n')
    verify()
    if vendor == 'grok':
        for row in rows:
            rel = Path(row['path'])
            if rel.name == P.GROK_PUBLIC_RESPONSE_NAME:
                continue
            assert not P.grok_source_is_private(rel, stdout_name, vendor), row['path']
    retention_name = 'codex-retention-custody.json' if (dest / 'custody.json').exists() else 'custody.json'
    tool_selection = (
        'Grok: public assistant content, tool_calls id/name/arguments, and tool_result content '
        'from authenticated session updates.jsonl derived from process cwd + sessionId. '
        'Post-compaction chat_history is authenticated by path only and is not the complete '
        'public record. Claude: tool_use/tool_result from session JSONL. '
        'Thought chunks, compaction summaries, rawOutput, and reasoning are not retained.'
    )
    custody = {
        'standing': (
            'Actual fresh independent application review; only its substantive exact-subject '
            'verdict grants scope. Retention does not apply documentation. Grok public '
            'assistant/tool deliveries are taken from authenticated session updates.jsonl '
            'across compaction. Private thought chunks, compaction summaries, rawOutput, '
            'CLI raw envelope, raw chat_history, and updates.jsonl were excluded from '
            'retained copies. Post-compaction chat_history is not treated as complete.'
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
            'selection': tool_selection,
        },
        'excludedExactDisposableCopies': excluded,
        'excludedPrivateSources': excluded_private,
        'retainedDisposableDeltas': deltas,
        'implementationAuthorized': False,
        'qualificationClaimed': False,
    }
    if update_account:
        custody['publicEventAccount'] = update_account
    (dest / retention_name).write_text(json.dumps(custody, indent=2) + '\n')
    return {
        'sessionId': session,
        'verdict': review['verdict'],
        'outputs': len(rows),
        'toolBlocks': len(blocks),
        'vendor': vendor,
        'dest': str(dest),
        'excludedPrivateSources': excluded_private,
    }


def main():
    p = argparse.ArgumentParser()
    for name in ('root', 'stage'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--version', required=True)
    p.add_argument('--bound-receipt', type=Path, required=True)
    a = p.parse_args()
    bound = load(a.bound_receipt)
    result = run_retain(root=a.root, stage=a.stage, version=a.version, bound=bound)
    print(
        result['sessionId'],
        result['verdict'],
        result['outputs'],
        'outputs',
        result['toolBlocks'],
        'tool blocks',
        result['vendor'],
    )


if __name__ == '__main__':
    main()
