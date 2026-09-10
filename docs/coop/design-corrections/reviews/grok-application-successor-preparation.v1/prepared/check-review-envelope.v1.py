"""Disposable decoder tests. No application, no live writes, no grades."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E

rows = []


def record(ident, passed, detail=''):
    rows.append({'id': ident, 'passed': bool(passed), 'detail': detail})


def grok_ok(**extra):
    env = {
        'text': 'Independent review complete. Verdict ACCEPT.',
        'stopReason': 'end_turn',
        'sessionId': '11111111-1111-1111-1111-111111111111',
        'requestId': 'req-1',
    }
    env.update(extra)
    return env


def claude_ok(**extra):
    env = {
        'is_error': False,
        'session_id': '22222222-2222-2222-2222-222222222222',
        'stop_reason': 'end_turn',
        'result': 'Independent review complete.',
    }
    env.update(extra)
    return env


# Positive Grok
try:
    d = E.decode_grok_public(grok_ok())
    record('grok-end-turn-extracts-sessionId', d['sessionId'].startswith('1111') and d['vendor'] == 'grok')
except Exception as e:
    record('grok-end-turn-extracts-sessionId', False, str(e))

# Grok cancelled
try:
    E.decode_grok_public(grok_ok(stopReason='cancelled'))
    record('grok-cancelled-refuses', False, 'accepted cancelled')
except AssertionError:
    record('grok-cancelled-refuses', True)

# Missing stopReason
try:
    env = grok_ok(); env.pop('stopReason')
    E.decode_grok_public(env)
    record('grok-missing-stopReason-refuses', False)
except AssertionError:
    record('grok-missing-stopReason-refuses', True)

# Empty text
try:
    E.decode_grok_public(grok_ok(text='   '))
    record('grok-empty-text-refuses', False)
except AssertionError:
    record('grok-empty-text-refuses', True)

# Claude positive
try:
    d = E.decode_claude_public(claude_ok())
    record('claude-is_error-false-extracts-session_id', d['sessionId'].startswith('2222'))
except Exception as e:
    record('claude-is_error-false-extracts-session_id', False, str(e))

# Claude is_error true
try:
    E.decode_claude_public(claude_ok(is_error=True))
    record('claude-is_error-true-refuses', False)
except AssertionError:
    record('claude-is_error-true-refuses', True)

# Missing is_error is not success (old .get is False would fail None is False)
try:
    env = claude_ok(); env.pop('is_error')
    E.decode_claude_public(env)
    record('claude-missing-is_error-refuses', False)
except AssertionError:
    record('claude-missing-is_error-refuses', True)

# Cross-vendor: Claude envelope is not a Grok envelope
try:
    E.decode_public(claude_ok(), 'grok')
    record('claude-envelope-fails-grok-decoder', False)
except AssertionError:
    record('claude-envelope-fails-grok-decoder', True)

# Cross-vendor: Grok envelope is not a Claude envelope
try:
    E.decode_public(grok_ok(), 'claude')
    record('grok-envelope-fails-claude-decoder', False)
except AssertionError:
    record('grok-envelope-fails-claude-decoder', True)

# Name-swap refusal: vendor grok with only session_id/is_error
try:
    E.decode_public({'is_error': False, 'session_id': 'x'}, 'grok')
    record('name-swap-claude-fields-as-grok-refuses', False)
except AssertionError:
    record('name-swap-claude-fields-as-grok-refuses', True)

# Findings none
ok_review = {
    'verdict': 'ACCEPT',
    'subjectManifestSha256': 'a' * 64,
    'newMustIssues': [],
    'newShouldIssues': [],
}
try:
    E.require_verdict(ok_review, 'ACCEPT', 'design')
    E.require_findings_none(ok_review, 'design')
    record('accept-empty-findings-lists', E.review_subject_digest(ok_review) == 'a' * 64)
except Exception as e:
    record('accept-empty-findings-lists', False, str(e))

try:
    E.require_findings_none({**ok_review, 'newMustIssues': [{'id': 'x'}]}, 'design')
    record('accept-with-must-refuses', False)
except AssertionError:
    record('accept-with-must-refuses', True)

try:
    bad = dict(ok_review); bad.pop('newShouldIssues')
    E.require_findings_none(bad, 'design')
    record('accept-unaccounted-should-refuses', False)
except AssertionError:
    record('accept-unaccounted-should-refuses', True)

try:
    E.require_verdict({**ok_review, 'verdict': 'CHANGES_REQUIRED'}, 'ACCEPT', 'design')
    record('changes-required-is-not-accept', False)
except AssertionError:
    record('changes-required-is-not-accept', True)

# Coauthor process standing
try:
    E.refuse_coauthor_process(
        {'standing': 'Actual Grok coauthor; isolated authorized file ownership; no source acceptance',
         'sessionId': C.KNOWN_GROK_COAUTHOR_SESSIONS[0]},
        'independent-design',
    )
    record('coauthor-standing-refuses', False)
except AssertionError:
    record('coauthor-standing-refuses', True)

# Resume of known coauthor session
try:
    E.refuse_coauthor_process(
        {'standing': 'Independent review',
         'command': ['grok', '--resume', C.KNOWN_GROK_COAUTHOR_SESSIONS[0]]},
        'independent-design',
    )
    record('resume-known-coauthor-refuses', False)
except AssertionError:
    record('resume-known-coauthor-refuses', True)

# This preparation session public file is empty or missing stopReason
prep = Path('/tmp/opensip-design-corrections/grok-application-successor-preparation.v1/response.raw.json')
if prep.is_file():
    raw = prep.read_text().strip()
    if not raw:
        record('this-session-empty-raw-is-not-a-review', True)
    else:
        try:
            E.decode_public(json.loads(raw), 'grok')
            record('this-session-empty-raw-is-not-a-review', False, 'decoded as success')
        except Exception:
            record('this-session-empty-raw-is-not-a-review', True)
else:
    record('this-session-empty-raw-is-not-a-review', True, 'missing file')

# Historical v21 subject is not evaluator3 unless explicitly v21 application of source21
record(
    'historical-v21-subject-constant-preserved',
    C.HISTORICAL_V21_SUBJECT_SHA256 == '360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1',
)
record('coverage-counts', all([
    len(C.AR_IDS) == 16,
    len(C.FW_IDS) == 15,
    len(C.INHERITED_IDS) == 27,
    len(C.CONDITION2_IDS) == 28,
    len(C.GATE_IDS) == 32,
    C.EVALUATION_RESIDUAL_COUNT == 30,
    C.D9_CARRIED_ROWS == ('DR-007', 'DR-011-R08'),
    C.HISTORICAL_V13_ADVISORY_IDS == ('CLAUDE-V13-ADV-1', 'CLAUDE-V13-ADV-2'),
]))

# Public view drops thought
pub = E.public_view(grok_ok(thought='private'), 'grok')
record('public-view-drops-thought', 'thought' not in pub and pub.get('stopReason') == 'end_turn')

failed = [r for r in rows if not r['passed']]
report = {
    'standing': 'Disposable envelope/decoder tests only. Not review evidence. No application.',
    'passed': sum(r['passed'] for r in rows),
    'failed': [r['id'] for r in rows if not r['passed']],
    'checks': rows,
    'actualApplicationPerformed': False,
}
out = HERE / 'check-review-envelope.report.json'
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ('passed', 'failed', 'actualApplicationPerformed')}))
raise SystemExit(bool(failed))
