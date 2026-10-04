"""Read-only, independent checks of contract successor S18 (law M3-J1 r4 successor S18).

It recomputes from the files, never from build_s18.py:
1. pins: the subject manifest, the record's candidates and parents, and each override's exact `before` line
   (Python splitlines, as verify_design reads a line selector);
2. WS and WSE: the three pairs carry the same before and after;
3. the lock at PRODUCT_REV, and every in-flight successor record under docs/implementation that the lock does
   not bind: none overrides or supersedes any (parent, selector) of S18's;
4. the operability-plan copy: a difflib alignment against PLAN-r3.md touches exactly r3 lines 293, 328, 335,
   336 and 433 and inserts one line, row O; the live PLAN.md is r3 plus its acceptance note;
5. content: J1 r4's S18 row and both CODEX2 observations (J1-R3-NB-01, -NB-02) are carried; no code is new;
   no exit is new; J1 r4's withdrawn readings ("O follows SOP2's freeze", the WS:1409 composition citation)
   are absent;
6. citations: every line S18 cites in WS, WSE, X7 r6, X3D r8, S-OP-2 r6, OPP r3, J1 r4, the run-termination
   contract, INV5 and bootstrap.rs at PRODUCT_REV says what S18 says it does.

Usage: check_s18.py [--rev REV]. Prints a JSON summary and exits nonzero on any failure."""
import difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
args = sys.argv[1:]
REV = args[args.index('--rev') + 1] if '--rev' in args else 'cd5958b'
J = 'docs/implementation/m3/host-pipeline-j/'
S = J + 's18/'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
OPP_R3 = 'docs/implementation/m3/operability/PLAN-r3.md'
OPP_LIVE = 'docs/implementation/m3/operability/PLAN.md'
OPP_COPY = S + 'operability/PLAN.md'
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
subject = json.loads(raw(J + 's18-subject.json'))
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
check('six overrides', len(ovs) == 6)
for o in ovs:
    n = o['selector']['line']
    check('before is the parent line %s:%d' % (o['parent']['path'].split('/')[-1], n),
          set(o['selector']) == {'line'} and lines(o['parent']['path'])[n - 1] == o['before'] and o['after'] != o['before'])

# 2. WS and WSE pairs ------------------------------------------------------------------------------------
ws = [o for o in ovs if o['parent']['path'] == WS]
wse = [o for o in ovs if o['parent']['path'] == WSE]
check('WS lines', [o['selector']['line'] for o in ws] == [225, 231, 1393])
check('WSE lines', [o['selector']['line'] for o in wse] == [225, 235, 1466])
check('pairs identical', [(o['before'], o['after']) for o in ws] == [(o['before'], o['after']) for o in wse])
check('WSE cancellation paragraph spans 224-235', lines(WSE)[223].startswith('**Cancellation.**')
      and lines(WSE)[236].startswith('**Aggregate termination'))

# 3. no collision with the lock or with in-flight records ----------------------------------------------
mine = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in ovs}
lock = json.loads(show('design-lock.json'))
bound_records = set()
collisions = []
for binding in lock['contractSuccessors']:
    bound_records.add(binding['record']['path'])
    rec = json.loads(raw(binding['record']['path']))
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        if (e['parent']['path'], json.dumps(e['selector'], sort_keys=True)) in mine:
            collisions.append(binding['record']['path'])
check('no bound entry on any S18 selector at ' + REV, not collisions, collisions)
in_flight, inflight_hits = [], []
for p in sorted((A / 'docs/implementation').rglob('successor.json')):
    rel = str(p.relative_to(A))
    if rel in bound_records or rel == S + 'successor.json' or '/reviews/' in rel:
        continue
    try:
        rec = json.loads(p.read_bytes())
    except ValueError:
        continue
    if not isinstance(rec, dict) or not isinstance(rec.get('passageOverrides'), list):
        continue   # not a v4 contract-successor record (older forms keep other shapes)
    in_flight.append(rel)
    entries = rec['passageOverrides'] + (rec.get('passageSupersessions') or [])
    for e in entries:
        if not isinstance(e, dict) or not isinstance(e.get('parent'), dict):
            continue
        if (e['parent'].get('path'), json.dumps(e.get('selector'), sort_keys=True)) in mine:
            inflight_hits.append(rel)
check('no in-flight record touches an S18 selector', not inflight_hits, inflight_hits)

# 4. the operability-plan copy ---------------------------------------------------------------------------
r3, copy, live = lines(OPP_R3), lines(OPP_COPY), lines(OPP_LIVE)
check('PLAN-r3.md is the accepted r3', hashlib.sha256(raw(OPP_R3)).hexdigest()
      == 'b49035f27abac0b6c6e4eed88fef52de8efa33285f7a5cdb66bd95cad3170c46')
check('live PLAN.md is r3 plus its acceptance note', live[:1] + live[3:] == r3 and live[1] == ''
      and live[2].startswith('**r3 ACCEPTED'))
check('live 330-340 is r3 328-338', live[329:340] == r3[327:338])
ops = difflib.SequenceMatcher(None, r3, copy, autojunk=False).get_opcodes()
touched_r3 = sorted(i + 1 for tag, i1, i2, j1, j2 in ops if tag != 'equal' for i in range(i1, i2))
touched_copy = sorted(j + 1 for tag, i1, i2, j1, j2 in ops if tag != 'equal' for j in range(j1, j2))
check('copy touches exactly r3 293, 328, 335, 336, 433', touched_r3 == [293, 328, 335, 336, 433], touched_r3)
check('copy has exactly one inserted line', len(copy) == len(r3) + 1 and len(touched_copy) == 6, touched_copy)
check('row O is copy line 336, between D and E', copy[335].startswith('| O. Final output section')
      and copy[334].startswith('| D. ') and copy[336].startswith('| E. '))
check('copy keeps LF and a final newline', raw(OPP_COPY).endswith(b'\n') and b'\r' not in raw(OPP_COPY))
report = json.loads(raw(S + 'evidence/copies-report.json'))
check('copies-report pins the copy', report['operabilityPlan']['copy'] == {
    'path': OPP_COPY, 'bytes': len(raw(OPP_COPY)), 'sha256': hashlib.sha256(raw(OPP_COPY)).hexdigest()})
check('standing names the copy and its parent', OPP_COPY in record['standing']
      and 'b49035f27abac0b6c6e4eed88fef52de8efa33285f7a5cdb66bd95cad3170c46' in record['standing'])

# 5. content ---------------------------------------------------------------------------------------------
para = ws[1]['after']
opp_new = [copy[i - 1] for i in touched_copy]
new_text = '\n'.join([o['after'] for o in ws] + opp_new)
required_ws = {
    'step 1 terminal when its output returns': 'is terminal only when that required output returns',
    'settles there and not earlier': 'The invocation settles when the output returns and not earlier',
    'after-settle only then': '*after-settle* begins only then',
    'termination output in the section too': 'Either way the decision point fixes one envelope',
    'cancelled render step fails on a renderer failure': 'even where it was `cancelled` for a termination output',
    'output decision point': '**output decision point**',
    'final output section': '**final output section**',
    'deferred': 'is deferred',
    'decided envelope and exit unchanged': 'changes nothing the decision fixed',
    'exit code named': 'exit code',
    'durable and ephemeral alike': 'Durable and ephemeral analyses follow the same rule',
    'before any byte': 'before any byte of the decided envelope',
    'F16 with the runId': '`DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the `runId`',
    'no-Run row otherwise': '`DELIVERY.REQUIRED_PROJECTION_FAILED` with no `runId`',
    'aggregate decides': 'The aggregate below then decides',
    'write failure is final': 'exit 4, one coded standard-error line and no replacement envelope',
    'nothing added': 'No class, code, exit, field or step outcome is added',
    'NB-01 fault owners': 'commit-session law X3d r8 items 6 and 9; finalization law X7 r6 items 3 and 5',
    'NB-01 kept out of composition': 'not passed through verdict or closed-Run composition',
    'NB-01 disclosure whichever is primary': 'Whichever termination the aggregate selects as primary',
    'invocation record unchanged': 'whose `cancellation` stays as the decision point fixed it',
}
for name, phrase in required_ws.items():
    check('WS carries: ' + name, phrase in para, phrase)
row_o = copy[335]
required_o = {
    'CancelPhase O by ordinary registration': '`CancelPhase` member added by S-OP-2\'s ordinary registration',
    'registration lines': 'lines 226-230',
    'NB-02 before cutoff admitted': 'before finalization\'s producer cutoff (its step 1), the record is admitted',
    'NB-02 abandonment after cutoff': 'commits `drain-abandoned` in the producer drop tally',
    'NB-02 in-flight disclosure': '`in_flight_at_freeze`',
    'NB-02 post-freeze': 'goes only to the post-freeze tally',
    'no sink reopened': 'No sink is reopened',
    'frozen summary unchanged': 'the frozen summary never changes',
    'deadline of the decided termination': 'finalization keeps the deadline of the decided termination',
    'F16 when a Run committed': 'X7\'s F16 row with the runId (X7:99; WS:1376)',
    'no-Run row otherwise': 'WS:1377\'s row with no runId',
    'NB-01 owners in OPP': '(X3D:176, :283; X7:101, :120)',
    'second signal waits': 'A second signal is deferred the same way',
}
for name, phrase in required_o.items():
    check('row O carries: ' + name, phrase in row_o, phrase)
check('withdrawn: O follows the freeze', 'follows SOP2' not in new_text and 'follows S-OP-2' not in new_text)
check('withdrawn: WS:1409 composition citation', '1409' not in new_text and '1411' not in new_text)
check('row D answers S-OP-12\'s open question', 'S-OP-12 decides' not in copy[334] and 'row O' in copy[334])
ws_text, opp_text = raw(WS).decode('utf-8'), raw(OPP_R3).decode('utf-8')
codes = sorted(set(re.findall(r'\b[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]*\b', new_text)))
check('no new code: every dotted code already in WS or OPP r3',
      all(c in ws_text or c in opp_text for c in codes), [c for c in codes if c not in ws_text and c not in opp_text])
exits = sorted(set(re.findall(r'\bexit (\d+)', new_text)))
check('no new exit', set(exits) <= {'0', '1', '2', '3', '4', '130'}, exits)

# 6. citations -------------------------------------------------------------------------------------------
def at(path, n, phrase, text=None):
    got = (text if text is not None else lines(path))[n - 1]
    check('cite %s:%d' % (path.split('/')[-1], n), phrase in got, got[:120])


W = lines(WS)
at(WS, 224, '**Cancellation.**'); at(WS, 233, '**Aggregate termination'); at(WS, 1393, 'SIGINT before / after settle')
at(WS, 1376, 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT'); at(WS, 1377, 'DELIVERY.REQUIRED_PROJECTION_FAILED')
at(WS, 1412, 'Fault, rejection and interruption terminations stay with their')
at(WS, 1133, 'If a Run was already'); at(WS, 1135, 'DELIVERY.REQUIRED_PROJECTION_FAILED')
check('WS 1128-1145 is in section 8', W[1088].startswith('## 8.') and W[1352].startswith('## 9.'))
X7 = 'docs/implementation/m2/finalization-x7/PROPOSAL-r6.md'
at(X7, 99, '(F16)'); at(X7, 100, '(F39)'); at(X7, 101, 'CommitUndetermined { executionId }')
at(X7, 120, 'namespace id is disclosed beside the row'); at(X7, 94, '3. **Outcome projection.**')
at(X7, 120, '5. **`CommitUndetermined`')
X3D = 'docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md'
at(X3D, 174, '6. **Outcomes returned to callers.**'); at(X3D, 176, '**`CommitUndetermined { executionId }`.**')
at(X3D, 276, '9. **Refusal rows'); at(X3D, 283, 'DURABILITY.COMMIT_FAILED')
SOP2 = 'docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md'
at(SOP2, 226, '**Ordinary registration.**'); at(SOP2, 229, 'a code table or member of one of the three provenance')
at(SOP2, 652, '**Finalization (lead decision).**'); at(SOP2, 657, '**Cutoff.**'); at(SOP2, 664, '**Read, in this order:**')
at(SOP2, 672, '**Derive and freeze.**'); at(SOP2, 682, 'post-freeze tally'); at(SOP2, 683, '**Deliver.**')
at(SOP2, 704, '**After the freeze.**'); at(SOP2, 766, '**Visibility.**')
at(SOP2, 871, '`host.signal.received`'); at(SOP2, 871, 'CancelPhase: A–E, OPP §5.5')
check('S-OP-2 r6 is the accepted bytes', hashlib.sha256(raw(SOP2)).hexdigest()
      == 'ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d')
at(OPP_R3, 195, 'drain on normal exit | 200 ms'); at(OPP_R3, 196, 'drain on cancellation | 100 ms')
at(OPP_R3, 339, '**The second stage inside a native effect')
J1 = J + 'PROPOSAL-r4.md'
check('J1 r4 is the accepted bytes', hashlib.sha256(raw(J1)).hexdigest()
      == 'c18c0d3c92ec9a1c029456aaa68e2785f0a17840aab93024f265e1789843fa32')
at(J1, 772, '| S18 |'); at(J1, 535, '| **O.** Final output section'); at(J1, 382, '**5.3 Settlement')
at(J1, 550, '**8.4 Phase D, the output decision point and phase O'); at(J1, 595, '**J-C14b')
at(J1, 601, '**J-C14c'); at(J1, 746, '**S12-O'); at(J1, 548, 'When another stop came first')
at(J1, 535, 'through WS:1409-1411\'s composition'); at(J1, 535, 'that event is post-freeze loss (SOP2:663)')
REV3 = 'docs/implementation/m3/reviews/codex2-host-pipeline-j-r3/review.json'
nbs = [o['id'] for o in json.loads(raw(REV3))['nonBlockingObservations']]
check('CODEX2 r3 observations', nbs == ['J1-R3-NB-01', 'J1-R3-NB-02'], nbs)
RTC = 'docs/coop/design-corrections/foundation/run-termination-contract.v1.md'
at(RTC, 216, '### 7.1'); at(RTC, 220, '**Not composed here, and never passed through verdict derivation:**')
boot = show('apps/cli/src/bootstrap.rs').decode('utf-8').splitlines()
at('bootstrap.rs', 45, 'DELIVERY.REQUIRED_FAILED: required metadata projection failed.', boot)
at('bootstrap.rs', 58, 'never append a replacement envelope', boot)
inv5 = json.loads(show('schemas/sources/invocation-v5.schema.json'))
check('INV5 Cancellation.phase is closed {none, before-settle, after-settle}',
      inv5['$defs']['Cancellation']['properties']['phase']['enum'] == ['none', 'before-settle', 'after-settle'])
env7 = show('schemas/sources/command-envelope-v7.schema.json').decode('utf-8')
check('ENV7 carries the invocation record only as its `invocation` member',
      '"invocation": {\n      "$ref": "urn:opensip:product-v1:workflows:evaluator3:invocation:5"' in env7)

print(json.dumps({'rev': REV, 'passed': not FAILURES, 'checks': len(PASSED) + len(FAILURES),
                  'failures': FAILURES, 'inFlightRecordsScanned': len(in_flight), 'codesInNewText': codes,
                  'exitsInNewText': exits}, indent=1))
sys.exit(1 if FAILURES else 0)
