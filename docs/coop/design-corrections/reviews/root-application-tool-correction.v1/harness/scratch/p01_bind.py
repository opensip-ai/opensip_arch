"""P01: discriminating bind-review-receipts.v1.py boundary probes.

Author-session rejection, cross-subject refusal, missing/mismatched root design
assent, coauthor process standing/resume. All fixtures synthetic and disposable.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import fixture as F  # noqa: E402
import coverage_contract as C  # noqa: E402

BIND = INPUTS / 'bind-review-receipts.v1.py'
REF = '/tmp/opensip-architecture-review-env/bin/python'

rows = []


def run_bind(receipt, out):
    r = subprocess.run([REF, '-I', '-B', str(BIND), '--receipt', str(receipt), '--out', str(out)],
                       capture_output=True, text=True, cwd=str(HERE))
    return r


def case(ident, expect, **kw):
    with tempfile.TemporaryDirectory(prefix='opensip-bind-probe-') as td:
        rp, out, subject = F.build(td, **kw)
        r = run_bind(rp, out)
        bound_written = out.exists()
        accepted = r.returncode == 0 and bound_written
        ok = (accepted is (expect == 'ACCEPT'))
        tail = (r.stderr.strip().splitlines() or [''])[-1][:160]
        rows.append({'id': ident, 'expected': expect,
                     'observed': 'ACCEPT' if accepted else 'REFUSE',
                     'asExpected': ok, 'boundReceiptWritten': bound_written,
                     'detail': tail})


# --- control: a well-formed synthetic receipt binds ---
case('control-fresh-sessions-bind', 'ACCEPT')

# --- independent reviewer-origin exclusion: the four Claude author origins ---
for i, s in enumerate(C.KNOWN_CLAUDE_COAUTHOR_SESSIONS, 1):
    case(f'bind-refuses-claude-author-origin-{i}-as-design', 'REFUSE', design_session=s)
    case(f'bind-refuses-claude-author-origin-{i}-as-blind', 'REFUSE', blind_session=s,
         receipt_overrides=None)
for i, s in enumerate(C.KNOWN_GROK_COAUTHOR_SESSIONS, 1):
    case(f'bind-refuses-grok-coauthor-origin-{i}-as-design', 'REFUSE', vendor='grok', design_session=s)
case('bind-refuses-historical-excluded-claude-session', 'REFUSE',
     design_session=C.HISTORICAL_CLAUDE_EXCLUDED_SESSION)

# --- blind must be a distinct fresh session ---
case('bind-refuses-blind-reusing-design-session', 'REFUSE',
     blind_session=F.FRESH_DESIGN_SESSION)

# --- cross-subject refusals ---
case('bind-refuses-blind-kit-naming-other-parent', 'REFUSE', blind_parent='e' * 64)
case('bind-refuses-assent-naming-other-subject', 'REFUSE', assent_subject='e' * 64)
case('bind-refuses-assent-naming-other-reviewer-session', 'REFUSE',
     assent_session='cccccccc-0000-4000-8000-000000000003')
case('bind-refuses-missing-root-design-assent', 'REFUSE', drop_assent=True)

# --- coauthor process standing / resume ---
case('bind-refuses-coauthor-process-standing', 'REFUSE',
     design_process={'standing': 'Actual Claude coauthor; no source acceptance',
                     'sessionId': F.FRESH_DESIGN_SESSION})
case('bind-refuses-process-resuming-claude-author-origin', 'REFUSE',
     design_process={'standing': 'Independent review',
                     'sessionId': F.FRESH_DESIGN_SESSION,
                     'command': ['claude', '--resume', C.KNOWN_CLAUDE_COAUTHOR_SESSIONS[0]]})
case('bind-refuses-process-session-not-matching-envelope', 'REFUSE',
     design_process={'standing': 'Independent review', 'sessionId': 'dddddddd-0000-4000-8000-000000000004'})

# --- receipt hygiene ---
case('bind-refuses-shape-only-receipt', 'REFUSE',
     receipt_overrides={'standing': 'SHAPE ONLY. Not a bound receipt.'})
case('bind-refuses-receipt-preclaiming-readyForAssembly', 'REFUSE',
     receipt_overrides={'readyForAssembly': True})
case('bind-refuses-non-accept-design-verdict-requirement', 'REFUSE',
     design_spec_overrides={'requiredVerdict': 'CHANGES_REQUIRED'})

# --- historical source21 subject must not be bound by a non-v21 successor ---
# (cannot be forged here: manifestSha256 is the real digest of the fixture manifest;
#  recorded as an unperformed sub-case rather than a fabricated pass.)

failed = [r['id'] for r in rows if not r['asExpected']]
print(json.dumps({'probe': 'P01-bind', 'cases': len(rows), 'asExpected': len(rows) - len(failed),
                  'unexpected': failed}, indent=2))
(HERE / 'p01_bind.result.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    print(('ok  ' if r['asExpected'] else 'DIFF'), r['id'], '->', r['observed'], '|', r['detail'])
