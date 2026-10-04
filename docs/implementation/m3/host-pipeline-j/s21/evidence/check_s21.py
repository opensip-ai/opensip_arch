"""Read-only, independent checks of contract successor S21 (law M3-J1 r5 successor S21, LD-r5-2).

It recomputes from the files, never from build_s21.py:
1. pins: the subject manifest, the record's candidates and parents, and each override's exact `before` line
   (Python splitlines, as verify_design reads a line selector);
2. WS and WSE: line 226 on each, with the same before and after; and (r2, Grok r1 RF-1) the per-kind sentence,
   WS:229 and WSE:233, with Grok's replacement text on both;
3. the lock at REV: S18 is bound; no bound entry is on any of S21's four lines; every line S18 binds is outside
   S21's record; and no unbound successor record under docs/implementation touches line 226;
4. the reading: with S18's bound lines and S21 applied, the paragraph's before-settle sentence runs from WS:225
   through S21's line into S18's WS:227 (and WSE:227), and states the exception and the interrupted case;
5. content: J1 r5's S21 row (8.3 rules 1 and 2, IE:1680-1681, SL:551-554, operational-failed 4, nothing added);
   no new code (every dotted code already in WS, IE or SL); no new exit; no new fault cause;
6. citations: every line S21 or its README cites in J1 r5, IE, SL, X3D, X7, WS and WSE says what S21 says.

Usage: check_s21.py [--rev REV]. Prints a JSON summary and exits nonzero on any failure."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
args = sys.argv[1:]
REV = args[args.index('--rev') + 1] if '--rev' in args else '6190e66'
J = 'docs/implementation/m3/host-pipeline-j/'
S = J + 's21/'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
S18 = J + 's18/successor.json'
FAILURES, PASSED = [], []


def check(name, condition, detail=''):
    (PASSED if condition else FAILURES).append(name if condition else '%s: %s' % (name, detail))


def raw(path):
    return (A / path).read_bytes()


def lines(path):
    return raw(path).decode('utf-8').splitlines()


def show(path):
    return subprocess.run(['git', '-C', str(PRODUCT), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pinned(row):
    b = raw(row['path'])
    return len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']


# 1. pins ------------------------------------------------------------------------------------------------
subject = json.loads(raw(J + 's21-subject.json'))
record = json.loads(raw(S + 'successor.json'))
check('subject members pinned', all(pinned(r) for r in subject['files']))
check('record in subject', any(r['path'] == S + 'successor.json' for r in subject['files']))
check('candidates are the subject minus the record',
      record['candidates'] == [r for r in subject['files'] if r['path'] != S + 'successor.json'])
check('candidates pinned', all(pinned(r) for r in record['candidates']))
check('parents are WSE and WS', [p['path'] for p in record['parents']] == [WSE, WS])
check('parents pinned', all(pinned(p) for p in record['parents']))
check('no supersession', 'passageSupersessions' not in record)
ovs = record['passageOverrides']
check('four overrides', len(ovs) == 4)
for o in ovs:
    n = o['selector']['line']
    check('before is the parent line %s:%d' % (o['parent']['path'].split('/')[-1], n),
          set(o['selector']) == {'line'} and lines(o['parent']['path'])[n - 1] == o['before'] and o['after'] != o['before'])

# 2. the pair --------------------------------------------------------------------------------------------
check('WS 226 and 229, then WSE 226 and 233', [(o['parent']['path'], o['selector']['line']) for o in ovs]
      == [(WS, 226), (WS, 229), (WSE, 226), (WSE, 233)])
check('line-226 pair identical', (ovs[0]['before'], ovs[0]['after']) == (ovs[2]['before'], ovs[2]['after']))
check('per-kind pair identical', (ovs[1]['before'], ovs[1]['after']) == (ovs[3]['before'], ovs[3]['after']))
after = ovs[0]['after']
per_kind = ovs[1]
check('per-kind after is Grok\'s RF-1 text verbatim',
      per_kind['after'] == 'Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its')
check('per-kind is one replacement inside the line',
      per_kind['before'].replace('an analysis attempt aborts and leaves no Run',
                                 'an analysis attempt that the signal aborts leaves no Run', 1) == per_kind['after'])
check('after keeps the line\'s own opening and closing words',
      after.startswith('`cancelled`, ') and after.endswith('a Run committed by an earlier'))

# 3. the lock, S18 and in-flight records ----------------------------------------------------------------
lock = json.loads(show('design-lock.json'))
bound_records = {b['record']['path'] for b in lock['contractSuccessors']}
check('S18 bound at ' + REV, S18 in bound_records)
mine = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in ovs}
bound_lines = {WS: {}, WSE: {}}
for binding in lock['contractSuccessors']:
    rec = json.loads(raw(binding['record']['path']))
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        if e['parent']['path'] in bound_lines and 'line' in e['selector']:
            bound_lines[e['parent']['path']][e['selector']['line']] = (binding['record']['path'], e)
check('no bound entry on WS:226, WS:229, WSE:226 or WSE:233 at ' + REV,
      not {226, 229} & set(bound_lines[WS]) and not {226, 233} & set(bound_lines[WSE]))
s18 = json.loads(raw(S18))
s18_lines = {p: sorted(o['selector']['line'] for o in s18['passageOverrides'] if o['parent']['path'] == p)
             for p in (WS, WSE)}
check('S18 binds WS 225, 227, 228, 231, 1393', s18_lines[WS] == [225, 227, 228, 231, 1393], s18_lines[WS])
check('S18 binds WSE 225, 229, 230, 235, 1466', s18_lines[WSE] == [225, 229, 230, 235, 1466], s18_lines[WSE])
check('S21 selects no S18 line', all(o['selector']['line'] not in s18_lines[o['parent']['path']] for o in ovs))
in_flight, hits = [], []
for p in sorted((A / 'docs/implementation').rglob('successor.json')):
    rel = str(p.relative_to(A))
    if rel in bound_records or rel == S + 'successor.json' or '/reviews/' in rel:
        continue
    try:
        rec = json.loads(p.read_bytes())
    except ValueError:
        continue
    if not isinstance(rec, dict) or not isinstance(rec.get('passageOverrides'), list):
        continue
    in_flight.append(rel)
    for e in rec['passageOverrides'] + (rec.get('passageSupersessions') or []):
        if isinstance(e, dict) and isinstance(e.get('parent'), dict) and \
                (e['parent'].get('path'), json.dumps(e.get('selector'), sort_keys=True)) in mine:
            hits.append(rel)
check('no unbound record touches an S21 selector', not hits, hits)

# 4. the reading -----------------------------------------------------------------------------------------
for path, first in ((WS, 225), (WSE, 225)):
    texts = []
    for n in (first, first + 1, first + 2):
        if n == 226:
            texts.append(after)
        elif n in bound_lines[path]:
            texts.append(bound_lines[path][n][1]['after'])
        else:
            texts.append(lines(path)[n - 1])
    sentence = ' '.join(texts)
    side = path.split('/')[-1]
    check('%s 225 is S18\'s and 227 continues the sentence' % side,
          bound_lines[path].get(225, (None,))[0] == S18 and texts[2].startswith('step is named in the termination\'s `runId`.'))
    check('%s reads: before-settle, then the exception' % side,
          ('): remaining steps are `cancelled`, and the aggregate is `interrupted` (130) unless a required analysis or '
           'verify step\'s commit returned one of two outcomes, which govern instead') in sentence, sentence[:300])
    check('%s reads: the interrupted case names the earlier Run' % side,
          'In the `interrupted` case, a Run committed by an earlier step is named in the termination\'s `runId`.'
          in sentence)
    pk = {WS: 229, WSE: 233}[path]
    pk_reading = per_kind['after'] + ' ' + lines(path)[pk]
    check('%s per-kind reads into the next line' % side,
          pk not in bound_lines[path] and pk + 1 not in bound_lines[path] and pk_reading.startswith(
              'Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its staged bytes;'),
          pk_reading[:160])

# 5. content ---------------------------------------------------------------------------------------------
required = {
    'interrupted stays the rule': 'the aggregate is `interrupted` (130) unless',
    'scope: a required analysis or verify step': 'a required analysis or verify step\'s commit',
    'rule 1: undetermined, operational-failed 4': 'an undetermined commit is `operational-failed` (4)',
    'rule 1: code and fault cause': '`DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`',
    'rule 1: no runId, ExecutionId disclosed': 'no `runId` and the attempt\'s ExecutionId disclosed for read-only recovery',
    'rule 1: IE basis': 'identity-and-evidence §5\'s `durability-undetermined`',
    'rule 2: latched after admission': 'a commit whose FinalGate was latched after admission stays committed',
    'rule 2: operational-failed 4 through DELIVERY.REQUIRED_FAILED': '`operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId`',
    'rule 2: SL basis': 'security-and-lifecycle S6\'s selected law',
    'matched on the returned outcome': 'The outcome the commit returned decides, never the gate\'s latch state alone',
    'attribution': 'contract successor S21 of law M3-J1 r5',
}
for name, phrase in required.items():
    check('carries: ' + name, phrase in after, phrase)
corpus = raw(WS).decode('utf-8') + raw(IE).decode('utf-8') + raw(SL).decode('utf-8')
codes = sorted(set(re.findall(r'\b[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]*\b', after)))
check('no new code (each in WS, IE or SL)', codes and all(c in corpus for c in codes), codes)
causes = sorted(set(re.findall(r'`([a-z]+-[a-z-]+)`', after)) - {'durability-undetermined', 'operational-failed'})
check('fault causes are WS\'s', all(c in lines(WS)[1359] or c in lines(WS)[1360] for c in causes), causes)
exits = sorted(set(re.findall(r'\((\d+)\)', after)))
check('no new exit', set(exits) <= {'0', '1', '2', '3', '4', '130'}, exits)
check('per-kind adds no code, exit or class', not re.findall(r'[A-Z]\.[A-Z]|\(\d+\)|`', per_kind['after']))
check('no S18 wording restated', '*after-settle*' not in after and 'final output section' not in after
      and 'output decision point' not in after)


# 6. citations -------------------------------------------------------------------------------------------
def at(path, n, phrase, text=None):
    got = (text if text is not None else lines(path))[n - 1]
    check('cite %s:%d' % (path.split('/')[-1], n), phrase in got, got[:140])


J1 = J + 'PROPOSAL-r5.md'
check('J1 r5 is the accepted bytes', hashlib.sha256(raw(J1)).hexdigest()
      == '4ccb23204b9d072464c3daa63eba8238c0f0425d38ea0da6c93df21711877599')
at(J1, 588, '**8.3 Precedence'); at(J1, 589, '1. **Any `CommitUndetermined`**')
at(J1, 590, '2. **A `Committed(PublishedCommit)` whose `latchedAfterAdmission` is set.**')
at(J1, 591, '3. **A `Committed(PublishedCommit)` not latched'); at(J1, 592, '4. **Otherwise:**')
at(J1, 600, '**Rules 1 and 2 against WS:226 (r5; lead decision LD-r5-2')
at(J1, 605, 'S21 is to override WS:226 and WSE:226 to state the exception, adding no class, code or exit')
at(J1, 606, '**Until S21 is accepted,**'); at(J1, 868, '| S21 |')
at(J1, 868, 'leaves S18\'s lines (WS:225, :227-228, :231) as they are'); at(J1, 938, 'WS gains that exception through successor S21')
at(IE, 1680, '`durability-undetermined` to the caller,'); at(IE, 1681, 'exit 4, with an ExecutionId for read-only recovery')
at(IE, 1631, '## 5. Durable custody and failure protocol'); at(IE, 96, '`DURABILITY.COMMIT_FAILED`')
at(SL, 465, '## S6.'); at(SL, 551, 'A latched attempt (state `2` or `3`)')
at(SL, 554, 'through the existing `DELIVERY.REQUIRED_FAILED` path'); at(SL, 555, 'open choice.')
X3D = 'docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md'
at(X3D, 170, '**State 3 after admission (F39).** The commit\'s own outcome stands')
at(X3D, 283, 'DURABILITY.COMMIT_FAILED`, `durability-commit`, with the ExecutionId and no RunId')
X7 = 'docs/implementation/m2/finalization-x7/PROPOSAL-r6.md'
at(X7, 100, '(F39)'); at(X7, 101, 'CommitUndetermined { executionId }')
at(WS, 224, '**Cancellation.**'); at(WS, 233, '**Aggregate termination'); at(WS, 235, 'An optional step\'s rejection or failure never changes the aggregate')
at(WS, 1133, '`faultCause=delivery-required`, `DELIVERY.REQUIRED_FAILED`'); at(WS, 1360, 'durability-commit')
at(WS, 1393, 'SIGINT before / after settle'); at(WSE, 1466, 'SIGINT before / after settle')
at(WSE, 227, 'step is named in the termination\'s `runId`. This includes optional analysis/verify')
at(WS, 229, 'Per kind: an analysis attempt aborts and leaves no Run; an import discards its')
at(WSE, 233, 'Per kind: an analysis attempt aborts and leaves no Run; an import discards its')
at(SL, 553, 'stays committed with its RunId observable')
inv5 = json.loads(show('schemas/sources/invocation-v5.schema.json'))
desc = inv5['$defs']['Cancellation']['properties']['phase']['description']
check('INV5 before-settle description says interrupted (cross-law item)', 'aggregate is interrupted (130)' in desc, desc)
cinv = json.loads(raw('docs/coop/design-corrections/workflows/command-inventory.v3.json'))
golden = [g for g in cinv['goldens'] if g['id'] == 'interrupted-before-settle']
check('CINV interrupted-before-settle is the no-commit case', golden and 'had not committed' in golden[0]['remedy'], golden)

print(json.dumps({'rev': REV, 'passed': not FAILURES, 'checks': len(PASSED) + len(FAILURES), 'failures': FAILURES,
                  'inFlightRecordsScanned': len(in_flight), 'codesInNewText': codes, 'faultCauses': causes,
                  'exitsInNewText': exits}, indent=1))
sys.exit(1 if FAILURES else 0)
