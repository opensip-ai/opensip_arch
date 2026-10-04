"""Build contract successor SD-5 (law M3-D r3 successor SD-5, its ExcludedForm half; law M3-J1 r4 successor
S20): the public route of a manifest-class excluded form refused at pre-draw component admission (R10a, and
ER10a on the ephemeral path).

Writes, deterministically:
- sd-5/PASSAGES.md, a readable rendering of the override and of the effective route-table rows;
- sd-5/successor.json and ../sd-5-subject.json;
- ../sd-5-unit.json, the lead's DRAFT-PENDING-REVIEW assent record (not part of the subject).
Hand-written inputs it pins but never writes: README.md and the three evidence scripts.

Usage: build_sd5.py [--check]
--check builds everything in memory and compares it with the files on disk; it writes nothing.

Run with python3 -I -B from any directory; a rerun reproduces the same bytes. It reads the architecture
repository and, read-only through `git show`, the product lock at LOCK_REV. The lock is used only for
assertions; no output byte depends on it."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = 'cd5958b'
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-5/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
HAND = [D + 'README.md', D + 'evidence/build_sd5.py', D + 'evidence/check_sd5.py', D + 'evidence/verify_scratch.py']
DRAFTS = ['docs/implementation/m3/native-successors-fa/fa-1/successor.json',
          'docs/implementation/m3/native-successors-fa/fa-2/successor.json',
          'docs/implementation/m3/native-successors-fa/rust3-lim/successor.json',
          'docs/implementation/m3/syntax-e/syn-1/successor.json']
CHECK = '--check' in sys.argv[1:]
LINE = 3540


def raw(p):
    return (A / p).read_bytes()


def pin_bytes(p, b):
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, raw(p))


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


# ---- the passage: one row after the authenticated release declaration row ----------------------
REMEDY = ('This installed component is a form OpenSIP never admits. Only first-party or explicitly trusted '
          'components are admitted, and none may claim policy, persistence, rendering, termination or '
          'host-lifecycle authority, run untrusted native or WASM code, or declare a project hook, root command or '
          'probe. Remove the component, or install its first-party release.')
CONDITION = (
    '**component manifest that is an excluded form** (contract successor SD-5 of law M3-D r3, item 24): an '
    'authenticated component manifest (security S1: its signature envelope and signed catalog association) that '
    'current trust admits and that the analysis step can select, refused at component admission before any '
    'analysis attempt\'s `ExecutionId` is drawn or reserved, on the durable and the ephemeral path, as '
    '`ExcludedForm {class, subject}`, because it represents one of DR-117\'s manifest-class excluded forms: '
    '`EE-1`, a publisher neither first-party nor explicitly trusted; `EE-3b`, a claim of policy, persistence, '
    'rendering, termination or host-lifecycle authority (a `commands` entry for role `analyzer`, or a capability '
    'outside the native capability matrix\'s provider capabilities); `EE-4`, untrusted native or WASM code; '
    '`EE-5a`, a project hook, root command or contribution-granted probe. No Plan, Coverage, Run or closure '
    'selection follows, so the refusal is never a `provider-unavailable` deficiency and never the not-installed '
    'golden of workflows §9. A required closure that is not installed, or that current trust does not admit '
    '(an ephemeral request with no trust view included), is never an excluded form and keeps that golden: '
    '`indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. A '
    'condition the authenticated release declaration row above routes keeps that row, and a manifest refused '
    'here never reaches HelloAck, closure selection or spawn')
CARRIER = (
    '`PAYLOAD-NOT-ADMISSIBLE`, security S12\'s admission row for a signed document that is not admissible, '
    'carried as `domainDetail` with subject `excluded-form:<class>:<manifestDigest>` (the refused manifest\'s '
    'identity `closure.manifestDigest`, 64 hex): the refused manifest least by `manifestDigest`, with its first '
    'class in the order above; remedy "' + REMEDY + '"; the failure envelope\'s `errors` is exactly that '
    'detail; every `ExcludedForm` goes to the operational record; no runId and no executionId')
ROW = '| %s | | `request-rejected` (2) | `EXTENSION.ADMISSION_REJECTED` | %s |' % (CONDITION, CARRIER)

EXPECT_BEFORE = (
    '| **invalid authenticated RELEASE DECLARATION**: a row naming a capability the matrix does not register, a '
    'mode outside the registered set, a mode whose cell is `NOT-SELECTED`, a duplicate `capabilityId`, or a '
    '`preview-*` spelling (`native.release-capability-unregistered`, `…-mode-unregistered`, `…-mode-not-selected`, '
    '`…-duplicate`) | | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | request detail (before PlanId; no '
    'worker is spawned) |')

ne_raw = raw(NE)
ne_lines = ne_raw.decode('utf-8').splitlines()
parent = pin_bytes(NE, ne_raw)
assert parent == {'path': NE, 'bytes': 329013,
                  'sha256': '83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0'}, parent
assert ne_lines[LINE - 1] == EXPECT_BEFORE
assert ne_lines[3522] == '| Condition | Cause (`nativeCause`) | D9 class (host-owned) | Existing code | Typed detail carrier |'
assert ROW.count('|') == ne_lines[3522].count('|') == 6, 'the row must keep the five columns'
assert REMEDY.isascii() and len(REMEDY) <= 1024 and len('excluded-form:EE-3b:') + 64 <= 1024
override = {'parent': parent, 'selector': {'line': LINE}, 'before': ne_lines[LINE - 1],
            'after': ne_lines[LINE - 1] + '\n' + ROW}

# ---- assertions against the product lock and the unbound drafts ------------------------------
lock = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', LOCK_REV + ':design-lock.json'],
                                 check=True, capture_output=True).stdout)
assert parent in lock['inputs'], 'NE is not an accepted base input at its pinned bytes'
assert len(lock['contractSuccessors']) == 82, len(lock['contractSuccessors'])
mine = (NE, json.dumps(override['selector'], sort_keys=True))
bound_ne = []
for b in lock['contractSuccessors']:
    assert pin(b['record']['path']) == b['record'], b['record']['path']
    rec = json.loads(raw(b['record']['path']))
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert (e['parent']['path'], json.dumps(e['selector'], sort_keys=True)) != mine, b['record']['path']
        if e['parent']['path'] == NE:
            bound_ne.append(e['selector']['line'])
draft_ne = {}
for p in DRAFTS:
    if not (A / p).exists():
        continue
    rec = json.loads(raw(p))
    lines = sorted(e['selector']['line'] for e in rec.get('passageOverrides', []) if e['parent']['path'] == NE)
    assert LINE not in lines, (p, lines)
    draft_ne[p] = lines

# ---- generated files ----------------------------------------------------------------------------


def render():
    out = ['# SD-5 passage (generated)', '',
           'Generated by `evidence/build_sd5.py` from the same data as `successor.json`; do not edit by hand. It '
           'gives the parent, the selector, the exact accepted `before` and the candidate `after`, then the '
           'effective rows of native-evidence section 10\'s admission and event route table around the insertion '
           '(the header, NE:3539 and NE:3540, the new row, NE:3541).', '', '## Passage override', '',
           '### `%s` line %d' % (NE, LINE), '', 'Before:', '', '```text', override['before'], '```', '', 'After:', '',
           '```text', override['after'], '```', '', '## Effective table rows after SD-5', '',
           ne_lines[3522], ne_lines[3523], ne_lines[3538], override['after'], ne_lines[3540], '',
           '## The new row, cell by cell', '']
    cells = [c.strip() for c in ROW.split('|')[1:-1]]
    assert len(cells) == 5
    for name, cell in zip(['Condition', 'Cause (`nativeCause`)', 'D9 class (host-owned)', 'Existing code',
                           'Typed detail carrier'], cells):
        out += ['- **%s:** %s' % (name, cell if cell else '(empty)')]
    out += ['']
    return '\n'.join(out).encode('utf-8')


files = {D + 'PASSAGES.md': render()}
candidates = sorted([pin(p) for p in HAND] + [pin_bytes(D + 'PASSAGES.md', files[D + 'PASSAGES.md'])],
                    key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED SD-5 contract successor (law M3-D r3 successor SD-5, its ExcludedForm half; law M3-J1 r4 '
                 'successor S20): the public route of a manifest-class excluded form (DR-117 EE-1, EE-3b, EE-4\'s '
                 'manifest part, EE-5a) refused at pre-draw component admission, R10a and its ephemeral '
                 'counterpart ER10a, as one row inserted in native-evidence section 10\'s admission and event route '
                 'table after the authenticated release declaration row: request-rejected 2, '
                 'EXTENSION.ADMISSION_REJECTED, domainDetail PAYLOAD-NOT-ADMISSIBLE with subject '
                 'excluded-form:<class>:<manifestDigest> and one fixed remedy; distinct from the not-installed golden '
                 '(M3-J1 r4 outcome-matrix row 27, indeterminate 3). One line override of native-evidence.md. '
                 'Existing class, code and detail only: no new public code, D9 member, schema, workflows byte or '
                 'product change. The exact frozen candidate requires actual independent review and root assent.'),
    'parents': [parent],
    'passageOverrides': [override],
    'candidates': candidates,
}
files[D + 'successor.json'] = dumps(record)
rpin = pin_bytes(D + 'successor.json', files[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [rpin], key=lambda r: r['path'])}
files[B + 'sd-5-subject.json'] = dumps(subject)
spin = pin_bytes(B + 'sd-5-subject.json', files[B + 'sd-5-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'supervisor-d-sd-5',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': spin,
    'independentReview': {'path': 'docs/implementation/m3/reviews/grok-sd-5-r1/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': rpin,
    'rootAssessment': ('DRAFT. Completed by the lead after Grok\'s review: status ACCEPTED-DESIGN-UNIT, the review '
                       'pin, rootSubstantiveAssent true. SD-5 is M3-D r3\'s successor SD-5 for R10a\'s route (M3-J1 '
                       'r4 S20): one row in native-evidence section 10\'s admission and event route table routes a '
                       'manifest-class ExcludedForm (EE-1, EE-3b, EE-4 manifest part, EE-5a) to request-rejected 2, '
                       'EXTENSION.ADMISSION_REJECTED, PAYLOAD-NOT-ADMISSIBLE with subject '
                       'excluded-form:<class>:<manifestDigest>, with no runId or executionId, distinct from the '
                       'not-installed golden (J1 row 27, indeterminate 3). Existing codes only. Bound in '
                       'design-lock.json in a binding-only product commit after acceptance; J1\'s next revision '
                       'records the matrix row.'),
    'fullM2Complete': False,
    'productQualification': False,
}
files[B + 'sd-5-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode('utf-8')

differ = []
for p, b in files.items():
    if CHECK:
        if not (A / p).exists() or raw(p) != b:
            differ.append(p)
    else:
        (A / p).write_bytes(b)
assert not differ, ('differs from disk', differ)
print(json.dumps({'mode': 'check' if CHECK else 'write', 'override': LINE, 'lockRev': LOCK_REV,
                  'lockContractSuccessors': len(lock['contractSuccessors']), 'boundNeLines': sorted(bound_ne),
                  'draftNeLines': draft_ne, 'rowChars': len(ROW), 'remedyChars': len(REMEDY),
                  'successor': rpin, 'subject': spin}, indent=1))
