"""Disposable decoder tests including parent-subject digest shape. No application, no grades."""
from __future__ import annotations

import json
import tempfile
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', type=Path, required=True)
report_path = parser.parse_args().report
assert not report_path.exists(), 'Preserve prior reports; choose a new output path'

rows = []

PARENT = 'a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb'
KIT = 'ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8'


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


try:
    d = E.decode_grok_public(grok_ok())
    record('grok-end-turn-extracts-sessionId', d['sessionId'].startswith('1111') and d['vendor'] == 'grok')
except Exception as e:
    record('grok-end-turn-extracts-sessionId', False, str(e))

try:
    E.decode_grok_public(grok_ok(stopReason='cancelled'))
    record('grok-cancelled-refuses', False, 'accepted cancelled')
except AssertionError:
    record('grok-cancelled-refuses', True)

try:
    env = grok_ok(); env.pop('stopReason')
    E.decode_grok_public(env)
    record('grok-missing-stopReason-refuses', False)
except AssertionError:
    record('grok-missing-stopReason-refuses', True)

try:
    E.decode_grok_public(grok_ok(text='   '))
    record('grok-empty-text-refuses', False)
except AssertionError:
    record('grok-empty-text-refuses', True)

try:
    d = E.decode_claude_public(claude_ok())
    record('claude-is_error-false-extracts-session_id', d['sessionId'].startswith('2222'))
except Exception as e:
    record('claude-is_error-false-extracts-session_id', False, str(e))

try:
    E.decode_claude_public(claude_ok(is_error=True))
    record('claude-is_error-true-refuses', False)
except AssertionError:
    record('claude-is_error-true-refuses', True)

try:
    env = claude_ok(); env.pop('is_error')
    E.decode_claude_public(env)
    record('claude-missing-is_error-refuses', False)
except AssertionError:
    record('claude-missing-is_error-refuses', True)

try:
    E.decode_public(claude_ok(), 'grok')
    record('claude-envelope-fails-grok-decoder', False)
except AssertionError:
    record('claude-envelope-fails-grok-decoder', True)

try:
    E.decode_public(grok_ok(), 'claude')
    record('grok-envelope-fails-claude-decoder', False)
except AssertionError:
    record('grok-envelope-fails-claude-decoder', True)

try:
    E.decode_public({'is_error': False, 'session_id': 'x'}, 'grok')
    record('name-swap-claude-fields-as-grok-refuses', False)
except AssertionError:
    record('name-swap-claude-fields-as-grok-refuses', True)

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

try:
    E.refuse_coauthor_process(
        {'standing': 'Actual Grok coauthor; isolated authorized file ownership; no source acceptance',
         'sessionId': C.KNOWN_GROK_COAUTHOR_SESSIONS[0]},
        'independent-design',
    )
    record('coauthor-standing-refuses', False)
except AssertionError:
    record('coauthor-standing-refuses', True)

try:
    E.refuse_coauthor_process(
        {'standing': 'Independent review',
         'command': ['grok', '--resume', C.KNOWN_GROK_COAUTHOR_SESSIONS[0]]},
        'independent-design',
    )
    record('resume-known-coauthor-refuses', False)
except AssertionError:
    record('resume-known-coauthor-refuses', True)

# The original environmental file later completed. Test the actual empty-file
# boundary using a disposable input, preserving the old control ID and purpose.
with tempfile.TemporaryDirectory(prefix='opensip-empty-review-') as tmp:
    empty = Path(tmp) / 'empty-public.json'
    empty.write_bytes(b'')
    try:
        E.decode_public_file(empty, 'grok')
        record('this-session-empty-raw-is-not-a-review', False, 'decoded empty input')
    except (AssertionError, json.JSONDecodeError):
        record('this-session-empty-raw-is-not-a-review', True, 'Disposable zero-byte file refused')

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

pub = E.public_view(grok_ok(thought='private'), 'grok')
record('public-view-drops-thought', 'thought' not in pub and pub.get('stopReason') == 'end_turn')

EXISTING_IDS = [r['id'] for r in rows]


def catch(ident, fn):
    try:
        fn()
        record(ident, False, 'expected refusal')
    except AssertionError:
        record(ident, True)
    except Exception as e:
        record(ident, False, type(e).__name__)


# Nested-only still admits (existing optional top-level omitted).
try:
    record(
        'nested-subject-manifest-admits',
        E.review_subject_digest({'subject': {'manifestSha256': 'a' * 64}}) == 'a' * 64,
    )
except Exception as e:
    record('nested-subject-manifest-admits', False, str(e))

# Alternate parent: inputKit.parentSubjectSha256. Kit digest present and different; must not win.
b11_shape = {
    'standing': 'PARSER-SHAPE ONLY. Refused consumer-b.v11 layout. Not acceptance.',
    'verdict': 'ACCEPT-RECONSTRUCTABLE',
    'inputKit': {
        'manifestSha256': KIT,
        'parentSubjectSha256': PARENT,
        'hashVerification': 'PASS',
    },
    'newMustIssues': [],
    'newShouldIssues': [],
}
got = None
try:
    got = E.review_subject_digest(b11_shape)
    record('alternate-parent-inputKit-parentSubject-admits', got == PARENT and got != KIT)
except Exception as e:
    record('alternate-parent-inputKit-parentSubject-admits', False, str(e))
record(
    'b11-shape-is-not-acceptance',
    got == PARENT
    and b11_shape['standing'].startswith('PARSER-SHAPE')
    and 'Not acceptance' in b11_shape['standing'],
)

catch(
    'kit-only-manifestSha256-refuses',
    lambda: E.review_subject_digest({'inputKit': {'manifestSha256': KIT, 'hashVerification': 'PASS'}}),
)

catch(
    'conflicting-parent-top-vs-inputKit-refuses',
    lambda: E.review_subject_digest(
        {
            'subjectManifestSha256': 'b' * 64,
            'inputKit': {'parentSubjectSha256': PARENT, 'manifestSha256': KIT},
        }
    ),
)

catch(
    'conflicting-parent-nested-vs-inputKit-refuses',
    lambda: E.review_subject_digest(
        {
            'subject': {'manifestSha256': 'c' * 64},
            'inputKit': {'parentSubjectSha256': PARENT},
        }
    ),
)

try:
    record(
        'agreeing-declared-parents-admit',
        E.review_subject_digest(
            {
                'subjectManifestSha256': PARENT,
                'subject': {'manifestSha256': PARENT},
                'inputKit': {'parentSubjectSha256': PARENT, 'manifestSha256': KIT},
            }
        )
        == PARENT,
    )
except Exception as e:
    record('agreeing-declared-parents-admit', False, str(e))

catch(
    'malformed-digest-uppercase-refuses',
    lambda: E.review_subject_digest({'inputKit': {'parentSubjectSha256': PARENT.upper()}}),
)
catch(
    'malformed-digest-wrong-length-refuses',
    lambda: E.review_subject_digest({'subjectManifestSha256': 'aa'}),
)
catch(
    'declared-null-parent-refuses',
    lambda: E.review_subject_digest({'subjectManifestSha256': None, 'inputKit': {'parentSubjectSha256': PARENT}}),
)
catch(
    'declared-wrong-type-parent-refuses',
    lambda: E.review_subject_digest({'inputKit': {'parentSubjectSha256': 1}}),
)
catch(
    'declared-nonobject-inputKit-refuses',
    lambda: E.review_subject_digest({'inputKit': None, 'subjectManifestSha256': PARENT}),
)
catch(
    'declared-nonobject-subject-refuses',
    lambda: E.review_subject_digest({'subject': None, 'subjectManifestSha256': PARENT}),
)
catch(
    'absent-parent-fields-refuses',
    lambda: E.review_subject_digest({'verdict': 'ACCEPT', 'newMustIssues': [], 'newShouldIssues': []}),
)

# Current .get() ignored missing keys; explicit null is now fail-closed when declared.
# Missing nested form beside a valid top-level remains optional.
try:
    record(
        'omitted-optional-nested-still-admits',
        E.review_subject_digest({'subjectManifestSha256': PARENT, 'subject': {}}) == PARENT,
    )
except Exception as e:
    record('omitted-optional-nested-still-admits', False, str(e))

failed = [r for r in rows if not r['passed']]
existing_failed = [r['id'] for r in rows if r['id'] in EXISTING_IDS and not r['passed']]
report = {
    'standing': (
        'Disposable envelope/decoder tests only. Alternate parent-field adapter. '
        'B11 layout is parser-shape evidence, not acceptance. No application, bind, or staging.'
    ),
    'passed': sum(r['passed'] for r in rows),
    'failed': [r['id'] for r in rows if not r['passed']],
    'existing20Passed': sum(1 for r in rows if r['id'] in EXISTING_IDS and r['passed']),
    'existing20Count': len(EXISTING_IDS),
    'existing20Failed': existing_failed,
    'checks': rows,
    'actualApplicationPerformed': False,
    'blind11Accepted': False,
}
report_path.write_text(json.dumps(report, indent=2) + '\n')
print(
    json.dumps(
        {
            'passed': report['passed'],
            'failed': report['failed'],
            'existing20Passed': report['existing20Passed'],
            'existing20Count': report['existing20Count'],
            'actualApplicationPerformed': False,
        }
    )
)
raise SystemExit(bool(failed))
