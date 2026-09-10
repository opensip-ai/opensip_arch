"""Decode actual public reviewer envelopes. Not a vendor rename and not acceptance.

Grok public JSON (observed completed --output-format json sessions):
  stopReason == "end_turn", sessionId, nonempty text.
  Optional requestId/usage/num_turns/modelUsage. thought is not a gate and is
  not review evidence.

Claude public JSON (existing assembly gate, retained for a future credits path):
  is_error is False (key present and boolean false), session_id nonempty.
  stop_reason is not Grok stopReason.

Missing keys fail. Cross-vendor decode fails. Coauthor standing fails.
"""
from __future__ import annotations

import json
from pathlib import Path

PUBLIC_GROK_KEYS = (
    'text', 'stopReason', 'sessionId', 'requestId', 'usage', 'num_turns',
    'total_cost_usd', 'modelUsage',
)


def load_json(path):
    p = Path(path)
    assert p.is_file(), 'Missing public envelope: ' + str(p)
    data = json.loads(p.read_text())
    assert isinstance(data, dict), 'Public envelope must be a JSON object: ' + str(p)
    return data


def public_view(envelope, vendor):
    """Strip private thought. Used when only response.raw.json exists."""
    if vendor == 'grok':
        return {k: envelope[k] for k in PUBLIC_GROK_KEYS if k in envelope}
    if vendor == 'claude':
        out = dict(envelope)
        out.pop('thinking', None)
        return out
    raise AssertionError('Unknown vendor: ' + repr(vendor))


def decode_grok_public(envelope):
    assert envelope.get('stopReason') == 'end_turn', (
        'Grok public envelope requires stopReason=end_turn, not '
        + repr(envelope.get('stopReason'))
    )
    session = envelope.get('sessionId')
    assert isinstance(session, str) and session.strip(), 'Grok sessionId missing'
    text = envelope.get('text')
    assert isinstance(text, str) and text.strip(), 'Grok public text missing'
    assert 'is_error' not in envelope or envelope.get('is_error') is not True
    return {
        'vendor': 'grok',
        'sessionId': session,
        'stopReason': 'end_turn',
        'publicTextChars': len(text),
    }


def decode_claude_public(envelope):
    assert 'is_error' in envelope, 'Claude public envelope requires is_error'
    assert envelope.get('is_error') is False, 'Claude is_error must be false'
    session = envelope.get('session_id')
    assert isinstance(session, str) and session.strip(), 'Claude session_id missing'
    return {
        'vendor': 'claude',
        'sessionId': session,
        'is_error': False,
    }


def decode_public(envelope, vendor):
    if vendor == 'grok':
        return decode_grok_public(envelope)
    if vendor == 'claude':
        return decode_claude_public(envelope)
    raise AssertionError('Unknown vendor: ' + repr(vendor))


def decode_public_file(path, vendor):
    return decode_public(load_json(path), vendor)


def refuse_coauthor_process(process, role):
    if process is None:
        return
    assert isinstance(process, dict)
    standing = process.get('standing')
    if isinstance(standing, str):
        lowered = standing.lower()
        if 'no source acceptance' in lowered or 'coauthor' in lowered:
            raise AssertionError(
                'Process standing is coauthor/non-accepting; cannot bind as '
                + role + ': ' + standing
            )
    command = process.get('command')
    if isinstance(command, list) and '--resume' in command:
        # Resume of a coauthor session is not a fresh independent session by itself.
        # Allowed only when standing already passed and role is not independent-*.
        if role.startswith('independent-'):
            idx = command.index('--resume')
            resumed = command[idx + 1] if idx + 1 < len(command) else ''
            from coverage_contract import KNOWN_GROK_COAUTHOR_SESSIONS
            if resumed in KNOWN_GROK_COAUTHOR_SESSIONS:
                raise AssertionError(
                    'Independent role must not resume a known coauthor session: '
                    + resumed
                )


def review_subject_digest(record):
    values = [record.get('subjectManifestSha256')]
    if isinstance(record.get('subject'), dict):
        values.append(record['subject'].get('manifestSha256'))
    values = [v for v in values if v is not None]
    assert values and all(type(v) is str and v == values[0] for v in values), (
        'Absent or conflicting review subject digests'
    )
    return values[0]


def require_findings_none(record, label):
    from coverage_contract import REQUIRED_FINDING_KEYS
    for key in REQUIRED_FINDING_KEYS:
        value = record.get(key)
        assert isinstance(value, list), (
            label + ' must explicitly account ' + key + ' as a list'
        )
        assert not value, (
            label + ' unresolved required findings in ' + key
        )


def require_verdict(record, expected, label):
    verdict = record.get('verdict', record.get('overallVerdict'))
    assert verdict == expected, (
        label + ' verdict ' + repr(verdict) + ' != ' + repr(expected)
    )
