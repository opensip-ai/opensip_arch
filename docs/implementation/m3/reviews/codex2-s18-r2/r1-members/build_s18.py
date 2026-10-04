"""Build contract successor S18 of law M3-J1 r4: the final output section.

S18 is a passage successor to workflows-and-surfaces section 1's cancellation paragraph (WS:224-231) and to
the operability plan's section 5.5 phase table (OPP:330-340, live numbering; r3 lines 328-338).

Form:
- WS and its selected effective copy WSE are accepted parents with no bound override on the selected lines,
  so they take line-selector passage overrides (insert or replace one line each).
- The operability plan is not a verify_design input, so it cannot be a parent. Its accepted r3 bytes
  (PLAN-r3.md) are copied whole to a new path with the S18 edits, and the record's standing selects the copy
  (the selection form of B-S9 and CR-1).

Writes, deterministically: s18/operability/PLAN.md, s18/PASSAGES.md, s18/evidence/copies-report.json,
s18/successor.json, ../s18-subject.json and ../s18-unit.json (the lead's DRAFT-PENDING-REVIEW record).
With --check it builds everything in memory and compares it with the files on disk, writing nothing.
It reads the architecture repository, and the product lock at PRODUCT_REV through read-only `git show`.
Run with python3.14 -I -B at nice -n 19."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
PRODUCT_REV = 'cd5958b'
J = 'docs/implementation/m3/host-pipeline-j/'
S = J + 's18/'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
OPP_R3 = 'docs/implementation/m3/operability/PLAN-r3.md'
OPP_LIVE = 'docs/implementation/m3/operability/PLAN.md'
OPP_COPY = S + 'operability/PLAN.md'
OPP_R3_SHA256 = 'b49035f27abac0b6c6e4eed88fef52de8efa33285f7a5cdb66bd95cad3170c46'   # Codex's r3 acceptance
HAND = [S + 'README.md', S + 'evidence/build_s18.py', S + 'evidence/check_s18.py', S + 'evidence/verify_scratch.py']
GENERATED = [S + 'PASSAGES.md', S + 'evidence/copies-report.json', OPP_COPY]
CHECK = '--check' in sys.argv[1:]

# ---------------------------------------------------------------------------------------------------------
# The WS and WSE passages. WSE carries WS's lines 225, 231 and 1393 at 225, 235 and 1466 (its cancellation
# paragraph has four more lines, from the M1 interruption owner). Each pair has the same before and after.
# ---------------------------------------------------------------------------------------------------------
LINES = {WS: {'before-settle': 225, 'paragraph-end': 231, 'golden': 1393},
         WSE: {'before-settle': 225, 'paragraph-end': 235, 'golden': 1466}}
BEFORE = {
    'before-settle': '*before-settle* (some required step not yet terminal): remaining steps are',
    'paragraph-end': 'the bounded rename loop the journal, not the signal, decides (§6).',
    'golden': '| SIGINT before / after settle | interrupted 130 / settled class | — | after-settle is never reclassified |',
}
FINAL_OUTPUT_SECTION = (
    '**Final output section (contract successor S18 of law M3-J1 r4).** This applies to an invocation whose last '
    'required step is the `render` step that renders and writes its one required envelope. The **output decision '
    'point** is the one cancellation check made after every other required step is terminal and the render step\'s '
    'projection of them is done. A signal observed no later than that check is before-settle: the render step is '
    '`cancelled`, its projection is discarded, and the termination the rule above gives is the invocation\'s '
    'termination output. Otherwise the decision point fixes the envelope that the aggregate below decides. Either '
    'way the decision point fixes one envelope, and from it until that envelope\'s output returns is the **final '
    'output section**, in which the envelope is rendered and written. A render step that was not cancelled is '
    'terminal only when that required output returns: it completes when the whole envelope has been written and '
    'flushed, and it fails when its projection, its renderer, the write or the flush fails. The invocation settles '
    'when the output returns and not earlier, so *after-settle* begins only then. A signal observed in the section '
    'is *final-output* and is deferred. '
    'It changes nothing the decision fixed (the envelope\'s kind, termination, class, exit code, `runId`, errors and '
    'results), selects no interrupted form and cancels no step. It is recorded neither in the envelope nor in an '
    'invocation record the envelope carries, whose `cancellation` stays as the decision point fixed it: the host '
    'classifies it in memory, and its only record is the operational one, under S-OP-2 and the operability plan\'s '
    '§5.5 (successor S18\'s copy, `docs/implementation/m3/host-pipeline-j/s18/operability/PLAN.md`). Durable '
    'and ephemeral analyses follow the same rule. A failure in the section is not a signal. If the renderer fails '
    'before any byte of the decided envelope is written, the render step fails, even where it was `cancelled` for a '
    'termination output, and §8\'s required-output law chooses its detail by committed evidence: '
    '`DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the `runId` when an '
    'earlier step committed a Run, and otherwise `DELIVERY.REQUIRED_PROJECTION_FAILED` with no `runId`. The '
    'aggregate below then decides the termination over the required steps, and the resulting failure envelope replaces the '
    'decided one. An uncertain analysis attempt keeps its own termination, with its ExecutionId and namespace '
    'disclosure, under its fault owners (commit-session law X3d r8 items 6 and 9; finalization law X7 r6 items 3 '
    'and 5); like every fault termination it stays with those owners and is not passed through verdict or '
    'closed-Run composition (§9). Whichever termination the aggregate selects as primary, that ExecutionId and '
    'namespace stay disclosed, and they are never the render attempt\'s identity or a Run\'s. A failed write or '
    'flush of the decided envelope ends the invocation with exit 4, one coded standard-error line and no '
    'replacement envelope, whether or not any byte was written; so does a failure envelope that cannot itself be '
    'rendered. No class, code, exit, field or step outcome is added.')
AFTER = {
    'before-settle': ('*before-settle* (some required step not yet terminal and, where the final output section '
                      'below applies, the signal observed no later than its output decision point): remaining '
                      'steps are'),
    'paragraph-end': BEFORE['paragraph-end'] + '\n\n' + FINAL_OUTPUT_SECTION,
    'golden': ('| SIGINT before / after settle | interrupted 130 / settled class | — | after-settle is never '
               'reclassified; a signal in the final output section (§1) is deferred and the decided class '
               'stands |'),
}
ROLE = {'before-settle': 'the before-settle definition (WS §1)',
        'paragraph-end': 'the end of the cancellation paragraph: the final-output-section rule is appended',
        'golden': '§9\'s SIGINT golden row'}

# ---------------------------------------------------------------------------------------------------------
# The operability-plan copy: PLAN-r3.md with these edits (r3 numbering; live = r3 + 2 from line 4).
# ---------------------------------------------------------------------------------------------------------
ROW_O = (
    '| O. Final output section (successor S18): from the output decision point until the required output '
    'returns; durable and ephemeral alike | **Deferred.** The host cancellation source classifies the signal as O '
    'in memory. It changes nothing the decision point fixed (kind, termination, class, exit, runId, errors, '
    'results), selects no interrupted form and cancels no step. A second signal is deferred the same way; while the '
    'envelope\'s write is in flight it waits for the write, with no elapsed bound (the second-stage bullet below). '
    '**The operational record:** `host.signal.received` is attempted with `arrival_phase` `O`, a `CancelPhase` '
    'member added by S-OP-2\'s ordinary registration (S-OP-2 r6, `s-op-2/PROPOSAL-r6.md`, lines 226-230). '
    'S-OP-2\'s finalization (S-OP-2 r6:652-683) runs inside O, so the record\'s fate depends on when the signal '
    'arrives: before finalization\'s producer cutoff (its step 1), the record is admitted like any other; after the '
    'cutoff, the call commits `drain-abandoned` in the producer drop tally, which the frozen summary counts if the '
    'commit precedes the freeze\'s reads (step 4), and a call still uncommitted at the freeze is disclosed through '
    '`in_flight_at_freeze`; anything committed after those reads goes only to the post-freeze tally, which no '
    'carrier reports (S-OP-2 r6:682, :704). A loss so counted reaches the envelope only as S-OP-2\'s loss line in '
    '`diagnostics` (S-OP-2 r6:766), never in termination or exit. No sink is reopened, the frozen summary never '
    'changes, and finalization keeps the deadline of the decided termination: the §3.3 cancellation drain '
    'only when the decided envelope is `interrupted`, otherwise the normal-exit drain. | The decided envelope and '
    'its exit (WS §1 as S18 succeeds it). A renderer failure before any byte of it: the failure envelope chosen '
    'by committed evidence, X7\'s F16 row with the runId (X7:99; WS:1376) when an earlier step committed a Run, '
    'otherwise WS:1377\'s row with no runId; an uncertain analysis attempt keeps its ExecutionId and namespace '
    'disclosure under its fault owners (X3D:176, :283; X7:101, :120); WS:233-240 aggregates. A failed write or '
    'flush of the envelope: exit 4, one coded standard-error line, no replacement envelope. |')
OPP_EDITS = [
    {'r3Line': 293, 'kind': 'replace', 'why': '§5.2\'s user-interrupt outcome row (consequential)',
     'before': ('| User interrupt, any phase | per §5.5 | the phase-specific join in §5.5: `interrupted` 130 '
                'only before FinalGate admission or before settle; X7\'s exit-4 projections after FinalGate '
                'admission; settled class after settle | per §5.5 |'),
     'after': ('| User interrupt, any phase | per §5.5 | the phase-specific join in §5.5: `interrupted` 130 '
               'only for a signal observed no later than the output decision point (successor S18), and there only '
               'before FinalGate admission or after an unlatched commit; X7\'s exit-4 projections after FinalGate '
               'admission; the decided class in the final output section (row O); settled class after settle | per '
               '§5.5 |')},
    {'r3Line': 328, 'kind': 'replace', 'why': 'the phase table\'s lead-in: the output decision point',
     'before': ('- **The cancellation join by phase (OP-R2-02; S-OP-12).** The signal is recorded with the phase in '
                'which it arrived (WS:224).'),
     'after': ('- **The cancellation join by phase (OP-R2-02; S-OP-12; successor S18).** The signal is recorded with '
               'the phase in which it arrived (WS:224). Phases A to D end at the **output decision point** '
               '(successor S18 of law M3-J1 r4; WS §1 as S18 succeeds it): the one cancellation check after every '
               'other required step is terminal and the render step\'s projection is done, which fixes the envelope '
               'to be written. A signal observed no later than that check takes the row of its phase, and one '
               'observed after it, until the required output returns, takes row O. An ephemeral request, or any '
               'request that admits no attempt, stays in phase A until the decision point and then takes rows O '
               'and E.')},
    {'r3Line': 335, 'kind': 'replace', 'why': 'row D: its end, and the question S-OP-12 left open',
     'before': ('| D. Commit returned unlatched; some required step not yet terminal | WS\'s before-settle rule: '
                'remaining steps are cancelled | `interrupted` 130 with `signal`, naming the committed runId '
                '(WS:224-227). S-OP-12 decides, with the X7 owner, whether a signal during the same step\'s required '
                'delivery takes this row or X7\'s latched row. |'),
     'after': ('| D. Commit returned unlatched; some required step not yet terminal, until the output decision point '
               '| WS\'s before-settle rule: remaining steps are cancelled. At the output decision point the render '
               'step is `cancelled` and its projection discarded (successor S18). | `interrupted` 130 with `signal`, '
               'naming the committed runId (WS:224-227). That envelope is the invocation\'s termination output and '
               'is written in its own final output section (row O). Decided by S-OP-12 with the X7 owner (law M3-J1 '
               'r4 item 8.4): a signal during the render step\'s projection takes this row, X7\'s latched row is only '
               'for a commit that `publish` sampled as latched (row C), and from the output decision point row O '
               'applies. |')},
    {'r3Line': 335, 'kind': 'insert-after', 'why': 'row O, the final output section', 'before': None, 'after': ROW_O},
    {'r3Line': 336, 'kind': 'replace', 'why': 'row E: settlement is the required output\'s return',
     'before': '| E. Every required step terminal | nothing is reclassified | the settled class stands (WS:227-228, 1393) |',
     'after': ('| E. Every required step terminal and the required output returned (successor S18) | nothing is '
               'reclassified | the settled class stands (WS:227-228, 1393) |')},
    {'r3Line': 433, 'kind': 'replace', 'why': '§10\'s cancellation control row (consequential)',
     'before': ('| Cancellation (OP-R2-02, OP-R2-03) | A signal in each of phases A–E of §5.5, with the expected '
                'projection, including Committed-with-latch → exit 4 with runId and CommitUndetermined → exit 4 '
                'with executionId. Stalled native operation plus a second signal (injected stall in the evidence '
                'COMMIT and in a barrier): the process keeps waiting, invents no refusal, and projects per X7 after '
                'return; SIGKILL during the stall leaves M2 recovery evidence. Operation-count exhaustion is never '
                'treated as an elapsed timeout. |'),
     'after': ('| Cancellation (OP-R2-02, OP-R2-03) | A signal in each of phases A–E and O of §5.5, with the '
               'expected projection, including Committed-with-latch → exit 4 with runId and CommitUndetermined '
               '→ exit 4 with executionId; in O, the decided envelope and its exit for a signal before S-OP-2\'s '
               'producer cutoff, between the cutoff and the freeze, and after the freeze, with the signal classified '
               'O in memory and its record admitted, counted `drain-abandoned` or post-freeze respectively (successor '
               'S18). Stalled native operation plus a second signal (injected stall in the evidence COMMIT and in a '
               'barrier): the process keeps waiting, invents no refusal, and projects per X7 after return; SIGKILL '
               'during the stall leaves M2 recovery evidence. Operation-count exhaustion is never treated as an '
               'elapsed timeout. |')},
]

STANDING = (
    'PROPOSED S18 contract successor (law M3-J1 r4 successor S18, the final output section; J1 r4 accepted by '
    'GROK2, sha256 c18c0d3c92ec9a1c029456aaa68e2785f0a17840aab93024f265e1789843fa32): a passage successor to '
    'workflows-and-surfaces section 1\'s cancellation paragraph (WS:224-231) and to the operability plan\'s section '
    '5.5 phase table (OPP:330-340). Six line overrides, three on WS and the same three on its selected effective '
    'copy WSE: the before-settle definition (WS:225, WSE:225), the end of the cancellation paragraph, where the '
    'final-output-section rule is appended (WS:231, WSE:235), and section 9\'s SIGINT golden row (WS:1393, '
    'WSE:1466). The operability plan is not a verify_design input, so it cannot be a parent: a complete successor '
    'copy of its accepted r3 bytes (docs/implementation/m3/operability/PLAN-r3.md, 70544 bytes, sha256 '
    + OPP_R3_SHA256 + ') at docs/implementation/m3/host-pipeline-j/s18/operability/PLAN.md, changed only at r3 '
    'lines 293, 328, 335 (row O inserted after it), 336 and 433, is selected by this record as the operability '
    'plan\'s successor text; PLAN-r3.md and the live PLAN.md become historical for those passages, and the plan\'s '
    'next revision starts from the copy. It carries CODEX2\'s J1-R3-NB-01 and J1-R3-NB-02. No code, class, exit, '
    'field, step outcome, route, public code, schema, inventory or product change. The exact frozen candidate '
    'requires actual independent review and root assent.')


def git_show(rev, path):
    return subprocess.run(['git', '-C', str(PRODUCT), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


OUT = {}


def emit(path, b):
    OUT[path] = b


def current(path):
    return OUT[path] if path in OUT else (A / path).read_bytes()


def pin(path):
    return pin_bytes(path, current(path))


def jbytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def lines_of(raw):
    text = raw.decode('utf-8')
    assert text.endswith('\n') and '\r' not in text and text.split('\n')[:-1] == text.splitlines()
    return text.split('\n')[:-1]


# --- the product lock: the accepted set, and the entries bound to each parent ---------------------------
lock = json.loads(git_show(PRODUCT_REV, 'design-lock.json'))
accepted = {}
for name in ('sourceManifest', 'applicationManifest'):
    for row in json.loads((A / lock['approvals'][name]['path']).read_bytes())['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for binding in lock['inventorySuccessors']:
    accepted[binding['candidate']['path']] = binding['candidate']
bound = {}
for binding in lock['contractSuccessors']:
    for row in json.loads((A / binding['subjectManifest']['path']).read_bytes())['files']:
        accepted[row['path']] = row
    record = json.loads((A / binding['record']['path']).read_bytes())
    for kind in ('passageOverrides', 'passageSupersessions'):
        for entry in record.get(kind, []):
            bound.setdefault(entry['parent']['path'], []).append(
                {'record': binding['record']['path'], 'kind': kind, 'selector': entry['selector']})

# --- the six overrides ----------------------------------------------------------------------------------
parents, overrides, ws_report = [], [], []
for path in (WS, WSE):
    raw = (A / path).read_bytes()
    parent = pin_bytes(path, raw)
    assert accepted.get(path) == parent, ('parent is not the accepted pin', path)
    lines = lines_of(raw)
    taken = {e['selector'].get('line') for e in bound.get(path, [])}
    for key in ('before-settle', 'paragraph-end', 'golden'):
        n = LINES[path][key]
        assert n not in taken, ('line already overridden', path, n)
        assert lines[n - 1] == BEFORE[key], (path, n, lines[n - 1])
        overrides.append({'parent': parent, 'selector': {'line': n}, 'before': BEFORE[key], 'after': AFTER[key]})
        ws_report.append({'parent': path, 'line': n, 'role': ROLE[key]})
    parents.append(parent)
    ws_report.append({'parent': path, 'boundEntries': bound.get(path, [])})
assert len(set(AFTER.values())) == 3 and all(BEFORE[k] != AFTER[k] for k in BEFORE)

# --- the operability-plan copy --------------------------------------------------------------------------
r3_raw, live_raw = (A / OPP_R3).read_bytes(), (A / OPP_LIVE).read_bytes()
assert hashlib.sha256(r3_raw).hexdigest() == OPP_R3_SHA256 and OPP_R3 not in accepted and OPP_LIVE not in accepted
r3, live = lines_of(r3_raw), lines_of(live_raw)
assert live[:1] + live[3:] == r3 and live[1] == '' and live[2].startswith('**r3 ACCEPTED 2026-10-03 by Codex**')
copy, report_edits, inserted = list(r3), [], 0
for edit in sorted(OPP_EDITS, key=lambda e: (e['r3Line'], e['kind'] == 'insert-after')):
    n = edit['r3Line']
    if edit['kind'] == 'replace':
        assert r3[n - 1] == edit['before'], (n, r3[n - 1])
        copy[n - 1 + inserted] = edit['after']
        copy_line = n + inserted
    else:
        copy.insert(n + inserted, edit['after'])
        inserted += 1
        copy_line = n + inserted
    report_edits.append({'kind': edit['kind'], 'r3Line': n, 'liveLine': n + 2, 'copyLine': copy_line,
                         'why': edit['why'], 'before': edit['before'], 'after': edit['after']})
copy_raw = ('\n'.join(copy) + '\n').encode('utf-8')
emit(OPP_COPY, copy_raw)
unchanged = [i for i in range(len(r3)) if (i + 1) not in {e['r3Line'] for e in OPP_EDITS if e['kind'] == 'replace'}]
for i in unchanged:   # every other r3 line sits in the copy unchanged, shifted by the one inserted row
    assert copy[i + (1 if i + 1 > 335 else 0)] == r3[i]
assert len(copy) == len(r3) + 1

report = {
    'schemaVersion': 1, 'productRev': PRODUCT_REV,
    'wsOverrides': ws_report,
    'operabilityPlan': {
        'parent': pin_bytes(OPP_R3, r3_raw),
        'parentStanding': 'Codex accepted the operability plan r3 (b49035f2); not a verify_design input, not in the '
                          'accepted set of the lock at ' + PRODUCT_REV,
        'live': pin_bytes(OPP_LIVE, live_raw),
        'liveRelation': 'the live PLAN.md is PLAN-r3.md with two lines inserted after line 1 (a blank line and the '
                        'r3 acceptance note), so live line n is r3 line n-2 from line 4; live 330-340 is r3 328-338',
        'copy': pin(OPP_COPY),
        'selection': 'the copy is the selected successor text of the operability plan for the edited passages; '
                     'PLAN-r3.md and the live PLAN.md become historical there',
        'edits': report_edits,
        'r3LinesReplaced': sorted(e['r3Line'] for e in OPP_EDITS if e['kind'] == 'replace'),
        'linesInserted': 1,
        'linesUnchanged': len(unchanged),
    },
}
emit(S + 'evidence/copies-report.json', jbytes(report))


# --- PASSAGES.md ----------------------------------------------------------------------------------------
def block(text):
    return '```text\n' + text + '\n```\n'


md = ['# S18 passages (generated by `evidence/build_s18.py`; do not edit)\n',
      'Every `before` is the parent\'s exact line; every `after` replaces that one line. The three WS overrides and '
      'the three WSE overrides are pairwise identical. The operability-plan edits are applied to `PLAN-r3.md` to '
      'make the complete successor copy `operability/PLAN.md`.\n']
for i, o in enumerate(overrides, 1):
    md.append('## %d. `%s`, line %d\n' % (i, o['parent']['path'], o['selector']['line']))
    md.append('Before:\n\n' + block(o['before']) + '\nAfter:\n\n' + block(o['after']))
md.append('## Operability plan copy\n')
md.append('Parent `%s` (%d bytes, `%s`). Copy `%s` (%d bytes, `%s`).\n' % (
    OPP_R3, len(r3_raw), OPP_R3_SHA256, OPP_COPY, len(copy_raw), hashlib.sha256(copy_raw).hexdigest()))
for e in report_edits:
    md.append('### r3 line %d (live %d, copy %d): %s, %s\n' % (e['r3Line'], e['liveLine'], e['copyLine'], e['kind'],
                                                               e['why']))
    if e['before'] is not None:
        md.append('Before:\n\n' + block(e['before']))
    md.append('After:\n\n' + block(e['after']))
emit(S + 'PASSAGES.md', '\n'.join(md).encode('utf-8'))

# --- the record, the subject and the unit draft --------------------------------------------------------
candidates = sorted([pin(p) for p in HAND + GENERATED], key=lambda r: r['path'])
record = {'schemaVersion': 1, 'standing': STANDING, 'parents': sorted(parents, key=lambda r: r['path']),
          'passageOverrides': overrides, 'candidates': candidates}
emit(S + 'successor.json', jbytes(record))
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(S + 'successor.json')], key=lambda r: r['path'])}
emit(J + 's18-subject.json', jbytes(subject))
unit = {
    'schemaVersion': 1, 'unit': 'host-pipeline-j-s18', 'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': pin(J + 's18-subject.json'),
    'independentReview': {'path': 'docs/implementation/m3/reviews/codex2-s18-r1/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False, 'requiredUnitFindings': [],
    'acceptedSuccessor': pin(S + 'successor.json'),
    'rootAssessment': ('DRAFT. Completed by the lead after CODEX2\'s review: status ACCEPTED-DESIGN-UNIT, the review '
                       'pin, rootSubstantiveAssent true. S18 is law M3-J1 r4\'s final-output-section successor: six '
                       'line overrides of WS and WSE (the before-settle definition, the final-output-section rule '
                       'after the cancellation paragraph, and the SIGINT golden row) and a complete successor copy of '
                       'the operability plan r3 with section 5.5\'s rows D, O and E, its lead-in, the section 5.2 '
                       'interrupt row and the section 10 cancellation control, selected by the record. It carries '
                       'CODEX2\'s J1-R3-NB-01 and NB-02. It binds on the verify_design at product cd5958b on top of 82 '
                       'contract successors.'),
    'fullM2Complete': False, 'productQualification': False,
}
emit(J + 's18-unit.json', jbytes(unit))

if CHECK:
    diffs = [p for p, b in OUT.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not diffs else 'DIFFERENT', 'differing': diffs}, indent=1))
    sys.exit(1 if diffs else 0)
for p, b in OUT.items():
    (A / p).parent.mkdir(parents=True, exist_ok=True)
    (A / p).write_bytes(b)
print(json.dumps({'overrides': len(overrides), 'oppCopy': pin(OPP_COPY), 'successor': pin(S + 'successor.json'),
                  'subject': pin(J + 's18-subject.json')}, indent=1))
