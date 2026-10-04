"""Build native contract successor FA-1 (law M3-H r3: cross-law item X-H2 and successor row FA-1).

Writes, deterministically:
- fa-1/PASSAGES.md, a readable rendering of every override and of the effective section 10 text;
- fa-1/successor.json and ../fa-1-subject.json;
- ../fa-1-unit.json, the lead's DRAFT-PENDING-REVIEW assent record (not part of the subject).
Hand-written inputs it pins but never writes: README.md and the three evidence scripts.

Usage: build_fa1.py [--check]
--check builds everything in memory and compares it with the files on disk; it writes nothing.

Run with python3 -I -B from any directory; a rerun reproduces the same bytes. It reads the
architecture repository and, read-only through `git show`, the product lock at LOCK_REV. The lock is
used only for assertions; no output byte depends on it."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = 'cd5958b'
B = 'docs/implementation/m3/native-successors-fa/'
D = B + 'fa-1/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
HAND = [D + 'README.md', D + 'evidence/build_fa1.py', D + 'evidence/check_fa1.py', D + 'evidence/verify_scratch.py']
# Unbound drafts that also override NE lines; FA-1 must stay disjoint from every one of them.
DRAFTS = [B + 'fa-2/successor.json', B + 'rust3-lim/successor.json',
          'docs/implementation/m3/syntax-e/syn-1/successor.json',
          'docs/implementation/m3/supervisor-d/sd-5/successor.json']
CHECK = '--check' in sys.argv[1:]


def raw(p):
    return (A / p).read_bytes()


def pin_bytes(p, b):
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, raw(p))


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


# ---- the passages -----------------------------------------------------------------------------
ANCHOR_3529 = '`native.coverage-subject-scope-outside-view`)'
INSERT_3529 = (
    '; **a Coverage entry whose `closedWorld` contradicts a §4.5 record law at the producer boundary** '
    '(`native.coverage-closed-world-mismatch`, contract successor FA-1): `deadCodeRepairEligible` true while '
    '`exportsClosed` is not `closed`, `entryPointsRecognized` is not `all` or `nonliteralLoading` is not `none`; or '
    '`nonliteralLoading=none` beside an `unresolved-edge` fact of class `require-nonliteral`, '
    '`dynamic-import-nonliteral`, `reflective-access` or `indirect-eval` admitted from the entry\'s own stage')
AFTER_3849 = ('`BudgetExhausted` and `Unavailable` are clean typed terminals (contract successor FA-1). On a')
AFTER_3850 = (
    '`BudgetExhausted` or a post-Analyze `Unavailable`, every fact candidate of that Analyze, and every occupancy '
    'companion it carried, is discarded, and only the terminal\'s exhaustive Coverage is admitted, at the producer '
    'boundary after a clean settlement (the valid terminal with its exhaustive Coverage and matching '
    '`coverageCommitment`, zero exit, EOF); a pre-Analyze `Unavailable` has no candidates, and its Coverage is the '
    'host conversion of §9.7. The Run is authoritative with the stage `partial`. The retained candidate '
    'dispositions govern, and §0 supersedes none of them: `docs/coop/artifacts/delivery.v2.json` '
    '`$.typescriptSemanticSubstrate.supervision.factBatchAtomicity.onUnavailable` and `.onBudgetExhausted`, '
    '`$.typescriptSemanticSubstrate.supervision.cleanUnavailable.candidateDisposition` and '
    '`$.typescriptSemanticSubstrate.supervision.deterministicBudget.candidateDisposition` '
    '(`DISCARD_ALL_CANDIDATES`), and `docs/coop/artifacts/rust-provider-protocol.v2.json` '
    '`$.candidateAtomicity.discardAllOn` and '
    '`$.candidateAtomicity.unavailableAndBudgetCoverage` ("candidates remain discarded"). Only `Complete` carries '
    '`factStreamCommitment` (`CompleteV1`, `CompleteV2`); these two terminals commit their Coverage alone, so '
    'nothing verifies a candidate streamed before them. For these two terminals `StageAuthorityV1.factsAdmitted` '
    'is `none`; where the reference `stage_authority` returns `before-terminal`, this text governs and the '
    'reference is the defect.')

EXPECT_BEFORE = {
    3529: ("| capability/identity mismatch at HelloAck; OpenUniverse before negotiation; coverage bijection faults, "
           "including an RC-0 pair whose rung is not on that relation's own ladder, an RC-1 not-applicable entry "
           "carrying a resolution claim, or an RC-2 precondition mismatch; **subject-scope commitment, coverage key "
           "or examined-partition mismatch at the producer boundary** (§4.1a: "
           "`native.subject-scope-commitment-mismatch`, `native.coverage-key-scope-mismatch:<field>`, "
           "`native.examined-universe-commitment-mismatch`, `native.examined-universe-subject-count-mismatch`, "
           "`native.coverage-entry-key-mismatch`); a `view2` naming a `coverage2` that was never admitted at that "
           "boundary or whose subject scope is outside the view (`native.coverage-not-admitted-at-producer-boundary`, "
           "`native.coverage-subject-scope-outside-view`); **worker fault** (process fault, ProviderFault, crash) | "
           "| `operational-failed` (4) | `PROVIDER.PROTOCOL_VIOLATION` | operational record |"),
    3849: '`BudgetExhausted` and `Unavailable` are clean typed terminals: facts before the',
    3850: 'terminal are admitted and the Run is authoritative with the stage `partial`.',
}

ne_raw = raw(NE)
ne_lines = ne_raw.decode('utf-8').splitlines()
parent = pin_bytes(NE, ne_raw)
assert parent == {'path': NE, 'bytes': 329013,
                  'sha256': '83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0'}, parent
for line, text in EXPECT_BEFORE.items():
    assert ne_lines[line - 1] == text, line
assert ne_lines[3528].count(ANCHOR_3529) == 1
afters = {3529: ne_lines[3528].replace(ANCHOR_3529, ANCHOR_3529 + INSERT_3529), 3849: AFTER_3849, 3850: AFTER_3850}
overrides = [{'parent': parent, 'selector': {'line': n}, 'before': ne_lines[n - 1], 'after': afters[n]}
             for n in sorted(afters)]
for o in overrides:
    assert o['after'] and o['after'] != o['before'] and '\n' not in o['after']
# NE:3529 is insert-only: the row keeps every byte of its accepted text, and the inserted cell text has no '|'.
cut = ne_lines[3528].index(ANCHOR_3529) + len(ANCHOR_3529)
assert afters[3529] == ne_lines[3528][:cut] + INSERT_3529 + ne_lines[3528][cut:] and '|' not in INSERT_3529

# ---- assertions against the product lock and the unbound drafts ------------------------------
lock = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', LOCK_REV + ':design-lock.json'],
                                 check=True, capture_output=True).stdout)
assert parent in lock['inputs'], 'NE is not an accepted base input at its pinned bytes'
assert len(lock['contractSuccessors']) == 82, len(lock['contractSuccessors'])
mine = {(NE, json.dumps(o['selector'], sort_keys=True)) for o in overrides}
bound_ne = []
for b in lock['contractSuccessors']:
    assert pin(b['record']['path']) == b['record'], b['record']['path']
    rec = json.loads(raw(b['record']['path']))
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        key = (e['parent']['path'], json.dumps(e['selector'], sort_keys=True))
        assert key not in mine, ('bound successor already overrides', b['record']['path'], key)
        if e['parent']['path'] == NE:
            bound_ne.append(e['selector']['line'])
draft_ne = {}
for p in DRAFTS:
    if not (A / p).exists():
        continue
    rec = json.loads(raw(p))
    lines = sorted(e['selector']['line'] for e in rec.get('passageOverrides', []) if e['parent']['path'] == NE)
    assert not set(lines) & set(afters), (p, lines)
    draft_ne[p] = lines

# ---- generated files ----------------------------------------------------------------------------
effective = list(ne_lines)
for o in overrides:
    effective[o['selector']['line'] - 1] = o['after']


def render():
    out = ['# FA-1 passages (generated)', '',
           'Generated by `evidence/build_fa1.py` from the same data as `successor.json`; do not edit by hand. Each '
           'entry gives the parent, the selector, the exact accepted `before` and the candidate `after`. The last '
           'section shows the effective text of native-evidence section 10\'s fault-law paragraph (lines 3837 to '
           '3855) with the two overrides applied.', '', '## Passage overrides', '']
    for o in overrides:
        out += ['### `%s` line %d' % (o['parent']['path'], o['selector']['line']), '', 'Before:', '', '```text',
                o['before'], '```', '', 'After:', '', '```text', o['after'], '```', '']
    out += ['## Effective fault-law paragraph (NE:3837-3855 after FA-1)', '', '```text'] + effective[3836:3855] + \
           ['```', '']
    return '\n'.join(out).encode('utf-8')


files = {D + 'PASSAGES.md': render()}
candidates = sorted([pin(p) for p in HAND] + [pin_bytes(D + 'PASSAGES.md', files[D + 'PASSAGES.md'])],
                    key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED FA-1 native contract successor (law M3-H r3, cross-law item X-H2 and successor row FA-1; '
                 'items 4 and 13): native-evidence section 10. A clean BudgetExhausted or post-Analyze Unavailable '
                 'discards every fact candidate and occupancy companion of its Analyze and admits only the '
                 'terminal\'s exhaustive Coverage, as the retained delivery.v2 and rust-provider-protocol.v2 '
                 'candidate dispositions require; the clause "facts before the terminal are admitted" is withdrawn, '
                 'and StageAuthorityV1.factsAdmitted for those terminals is none. The producer-boundary route row '
                 'gains the internal key native.coverage-closed-world-mismatch. Three line overrides of '
                 'native-evidence.md. No code, class, exit, public code, schema, frame, protocol, reference-model or '
                 'product change. The exact frozen candidate requires actual independent review and root assent.'),
    'parents': [parent],
    'passageOverrides': overrides,
    'candidates': candidates,
}
files[D + 'successor.json'] = dumps(record)
rpin = pin_bytes(D + 'successor.json', files[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [rpin], key=lambda r: r['path'])}
files[B + 'fa-1-subject.json'] = dumps(subject)
spin = pin_bytes(B + 'fa-1-subject.json', files[B + 'fa-1-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'native-successor-fa-1',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': spin,
    'independentReview': {'path': 'docs/implementation/m3/reviews/grok-fa-1-r1/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': rpin,
    'rootAssessment': ('DRAFT. Completed by the lead after Grok\'s review: status ACCEPTED-DESIGN-UNIT, the review '
                       'pin, rootSubstantiveAssent true. FA-1 is the native contract successor for M3-H r3\'s X-H2 '
                       'and successor row FA-1: native-evidence section 10 withdraws "facts before the terminal are '
                       'admitted" (a clean BudgetExhausted or post-Analyze Unavailable discards every candidate and '
                       'admits only its exhaustive terminal Coverage, under the retained delivery.v2 and '
                       'rust-provider-protocol.v2 dispositions), and the producer-boundary row gains '
                       'native.coverage-closed-world-mismatch for H2\'s closed-world wiring. Three line overrides of '
                       'native-evidence.md, disjoint from every bound successor and from FA-2. Bound in '
                       'design-lock.json in a binding-only product commit after acceptance.'),
    'fullM2Complete': False,
    'productQualification': False,
}
files[B + 'fa-1-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode('utf-8')

differ = []
for p, b in files.items():
    if CHECK:
        if not (A / p).exists() or raw(p) != b:
            differ.append(p)
    else:
        (A / p).write_bytes(b)
assert not differ, ('differs from disk', differ)
print(json.dumps({'mode': 'check' if CHECK else 'write', 'overrides': [o['selector']['line'] for o in overrides],
                  'lockRev': LOCK_REV, 'lockContractSuccessors': len(lock['contractSuccessors']),
                  'boundNeLines': sorted(bound_ne), 'draftNeLines': draft_ne,
                  'successor': rpin, 'subject': spin}, indent=1))
