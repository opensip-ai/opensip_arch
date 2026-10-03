"""Transcribe X9-4's rows of law X9 r14 item 9 into required-runs.v1.json.

Unit X9-4 (locks and live revocation): F06, F18, F19, F26, F30, F34, F38,
F39's storage half, F40 and F41, with C5 per r3's G5 resolution, and r12's
moved F14 `x3d.finish.settle.before` kill.

Inputs, all made before any kill run:
- the reviewed required runs as X9-3 leaves them (X9-2's and X9-3's rows),
  which are carried over byte for byte (the script refuses an input that
  does not re-serialize to its own bytes, or that already holds an X9-4 row);
- X9-4's unarmed census (`census.json` of `x9_4_matrix` with
  `OPENSIP_X9_CENSUS_ONLY`; X9 r15). Only kill points come from it: F19's
  end-path `REV` points and F14's `x3d.finish.settle.before`.

Every expected value is the law's row (item 9, C5, r3, r12, r13), written
here before any run and never read back from one.

Law X9 r15 decides the questions X9-4's preparation raised (its census's
refused-end run, F14's moved row carrying `"unit": "X9-4"` with R2 refused at
admission, the timing guard's end, F30's distinct second B, project-state
comparison and (b)'s refused sweep, F26's "no grant reused", F18's mixed view
elsewhere, and F34's run A). Every row below is r15's.

usage: transcribe_x94.py <required-runs.json> <x94-census.json> <out>
Standard library only.
"""
import json
import re
import sys

LABELS = ['scripted-clock', 'synthetic']
LABELS_KILL = ['process-death', 'scripted-clock', 'synthetic']
LABELS_INJ = ['injected', 'scripted-clock', 'synthetic']
LABELS_MUT = ['mutation', 'scripted-clock', 'synthetic']
COMMITTED = 'Committed(latched=false)'
LATCHED = 'Committed(latched=true)'
UAO = 'unknown-attempt-open'
TNC = 'terminal-not-committed'
CH = 'committed-historically:*'
CH_PENDING = 'committed-historically:pendingSettlement:*'
CH_SETTLED = 'committed-historically:settled:*'
UNDETERMINED_END = 'end(rev=false,cln=false,settlement=None,step=false,stepFailure=None)'
# X4 r7 item 8: the revoked-during-operation row (subject trust-revoked: the
# revocation names the core closure's `release`, X9 r12) and the observer
# fail-stop row (subject the stop reason: the view unreadable).
REVOKED = 'Refused(RevokedDuringOperation { subject: "trust-revoked" })'
FAIL_STOP = 'Refused(ObserverFailStop { subject: "unreadable" })'
# C5: after a revocation of a closure subject, R2 is refused at X4T's
# admission. The exact row is not scored (as X9 r13 does for X9-5's F39).
REFUSED_AT_ADMISSION = 'operation:*'
TICK = 'x4.observer.tick'
LATCH = 'x4.gate.latch.after#1'
ADMISSION_HOLD = 'x3c.evidence.commit.before#1'  # X9 r12
SETTLE = 'x3d.finish.settle.before'
LADDER = {'ladder': 'R1,R2,R3,R4', 'of': 'writer'}
# The gate's state sequences that stay in 0..3 and never reset (X3d item 5).
GATE_IN_RANGE = ['0', '0,1', '0,2', '0,1,3']
X94_CASES = ('F06', 'F18', 'F19', 'F26', 'F30', 'F34', 'F38', 'F39', 'F40', 'F41')


def variant(prefix, point):
    name, k = point.rsplit('#', 1)
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return f'{prefix}-{slug}-{k}'


def kill_set_names(points):
    return {p['name'] for p in points if p['durability']}


def revocation_script(hold, *, change='revoke', resume='tick', arms=(), tail=()):
    """Item 11's revocation scripts, over one `commit` child named `writer`
    with `x4.observer.tick#*=hold` armed (item 11), and the timing guard
    from its first tick hold to its main hold (X9 r12 and r15).

    - `resume='tick'` (F38, F39, F40, F41, F14): the parent resumes one
      observer tick and awaits `x4.gate.latch.after` before resuming the main
      thread (item 11; X9 r12's F39 script).
    - `resume='main'` (F18, F19): the parent resumes the main thread, whose
      checkpoint observes the change itself (item 11). The held observer
      tick is resumed only after the end path's `x3d.finish.settle.before`,
      when the gate is already latched, so the observer can stop and the
      process can exit (X9 r15); a script that kills before that point
      never resumes it.
    `change` is `revoke` (the `revoke` child publishes the session's core
    closure's `release` revocation, X9 r12) or `unreadable` (the parent makes
    `state.v1` unreadable, labelled `mutation`; restored before the ladder).
    `tail` follows the resume of the main thread.
    """
    armed = ','.join([f'{TICK}#*=hold', f'{hold}=hold', *arms])
    script = [{'spawn': 'commit', 'name': 'writer', 'arm': armed},
              {'await': f'{TICK}#1', 'on': 'writer', 'then': 'hold'},
              {'await': hold, 'on': 'writer', 'then': 'hold'}]
    if change == 'revoke':
        script += [{'spawn': 'revoke', 'name': 'publisher', 'for': 'writer'}, {'finish': 'publisher'}]
    else:
        script += [{'mutate': 'trust-state-unreadable'}]
    if resume == 'tick':
        script += [{'resume': f'{TICK}#1', 'on': 'writer'},
                   {'await': LATCH, 'on': 'writer', 'then': 'pass'},
                   {'resume': hold, 'on': 'writer'}]
    else:
        script += [{'resume': hold, 'on': 'writer'}]
    script += list(tail)
    return script


def main_released(change):
    """F18 and F19's base end: the end path reached, the observer released,
    the writer finished; an unreadable view restored before the ladder."""
    steps = [{'await': f'{SETTLE}#1', 'on': 'writer', 'then': 'pass'},
             {'resume': f'{TICK}#1', 'on': 'writer'},
             {'finish': 'writer'}]
    if change == 'unreadable':
        steps.append({'mutate': 'trust-state-restored'})
    return steps


def x94_rows(census, row):
    names = kill_set_names(census['points'])

    def point(name, k=1):
        assert name in names, name
        return f'{name}#{k}'

    # ---------------------------------------------------------------- F06
    # The parent holds a raw `BEGIN IMMEDIATE` on the carrier, or on the
    # ledger, while the child runs `publish` (labelled `mutation`). The
    # writer is held at the end of `prepare_commit` while the parent takes
    # the lock; the product's level-3 `BEGIN IMMEDIATE` never waits (X3d
    # item 4 steps 1 and 2), and the holder ends after the writer exits.
    hold = point('x3c.attempt.commit.after')
    for store in ('carrier', 'ledger'):
        row('F06', f'foreign-{store}-holder', ['X3b', 'X3c', 'X3d'], LABELS_MUT,
            [{'spawn': 'commit', 'name': 'writer', 'arm': f'{hold}=hold'},
             {'await': hold, 'on': 'writer', 'then': 'hold'},
             {'sqlite-hold': store},
             {'resume': hold, 'on': 'writer'},
             {'finish': 'writer'},
             {'sqlite-release': store},
             LADDER],
            {'writer': 'Refused(Busy)', 'seals': '0', 'orphansPresent': 'true',
             'R1': UAO, 'R2.outcome': COMMITTED, 'R3': 'refused', 'R4': TNC})

    # ---------------------------------------------------------- F18, F19
    # F18: held at the first checkpoint, before the SEAL. F19: at the
    # repeated checkpoint after the SEAL (#2). Each: a revoking update, or
    # the view made unreadable (X9 r15: "mixed" is elsewhere, X4a's
    # a_replacement_during_the_first_attempt_is_absorbed_and_a_second_is_mixed). C5 (r3): R2 refused at
    # admission (revoked) or Committed after the view is restored (F18's
    # fail-stop variant); R3 refused; R4 TNC.
    for case, k, units in (('F18', 1, ['X4', 'X3d']), ('F19', 2, ['X3b', 'X3d', 'X4'])):
        hold = point('x4.checkpoint.before-observation', k)
        for change, outcome, labels in (('revoke', REVOKED, LABELS), ('unreadable', FAIL_STOP, LABELS_MUT)):
            expected = {'writer': outcome, 'writer.rev': 'true', 'writer.settlement': 'None',
                        'R1': UAO, 'R3': 'refused', 'R4': TNC}
            if case == 'F18':
                # No SEAL; `finish` appends `REV` from the settlement reserve.
                expected.update({'seals': '0', 'writer.cln': 'false'})
                expected['R2.outcome'] = REFUSED_AT_ADMISSION if change == 'revoke' else COMMITTED
            else:
                # The SEAL survives, the evidence transaction rolled back; the
                # trace shows level 4, then level 3, then a fresh `REV`, then
                # `CLN` (owed for the SEAL without its commit, X3d item 7).
                expected.update({'seals': '1', 'receipts': '0', 'writer.cln': 'true',
                                 'writer.releaseOrder': 'seal.L4,seal.L3,rev,cln'})
                if change == 'revoke':
                    expected['R2.outcome'] = REFUSED_AT_ADMISSION
            name = 'revoked' if change == 'revoke' else 'unreadable'
            row(case, f'{name}-at-checkpoint-{k}', units, labels,
                revocation_script(hold, change=change, resume='main', tail=main_released(change)) + [LADDER],
                expected)
    # F19: a kill at each point of the end-path `REV` append, after the
    # revocation at checkpoint #2. The killed `REV` leaves X3b's append crash
    # state; R2 is refused at admission, so it never reaches the start.
    hold = point('x4.checkpoint.before-observation', 2)
    rev = sorted(n for n in names if n.startswith('x3b.append.rev.'))
    assert rev, 'X9-4 census has no end-path REV append (X9 r15)'
    for name in rev:
        k = point(name)
        row('F19', variant('kill', k) + '-after-revoke', ['X3b', 'X3d', 'X4'], LABELS_KILL,
            revocation_script(hold, change='revoke', resume='main', arms=(f'{k}=hold',),
                              tail=[{'await': k, 'on': 'writer', 'then': 'kill'}]) + [LADDER],
            {'writer': 'killed', 'R1': UAO, 'R2.outcome': REFUSED_AT_ADMISSION, 'R3': 'refused', 'R4': TNC})

    # ---------------------------------------------------------------- F26
    # Commit, then the parent publishes a revocation. R1 CH; R2 refused at
    # admission; no grant reused (X9 r15: R2 leaves the project's own state
    # unchanged).
    row('F26', 'revoked-after-commit', ['X4', 'X6'], list(LABELS),
        [{'spawn': 'commit', 'name': 'writer'}, {'finish': 'writer'},
         {'spawn': 'revoke', 'name': 'publisher', 'for': 'writer'}, {'finish': 'publisher'},
         {**LADDER, 'observe': 'R2.projectUnchanged'}],
        {'writer': COMMITTED, 'R1': CH, 'R2.outcome': REFUSED_AT_ADMISSION, 'R2.projectUnchanged': 'true'})

    # ---------------------------------------------------------------- F30
    # Writer A holds (a) under its lease after the fence is released (at its
    # admitted attempt row) and (b) while it holds the fence (with the lease
    # just taken). B competes; C sweeps; A resumes; a second B succeeds.
    # X9 r15: the second B commits r12's distinct variant; (a) compares the
    # project's own state (B's trust-floor publication is recorded in the
    # ladder, unscored); in (b) C is refused at its own admission on the busy
    # row (X6 r4 item 7 step 1) and writes nothing.
    # The second B is item 8's R2, a next writer's full lawful commit on the
    # same namespace, so it runs as the ladder's R2 with the distinct
    # variant. The post state is then captured before it, at the ladder
    # (item 7), as in every other row. Captured after it, the post state
    # would hold two Runs whose shared and new blob digests interleave at
    # drawn positions in `blobDigests` (dev runs x94-dev1/2; X9-4 call).
    for name, hold, c_report, unchanged in (
            ('writer-held-under-lease', point('x3c.attempt.commit.after'), 'busy', 'projectUnchanged'),
            ('writer-holds-fence', point('x2.lease.writer/lock.after'), 'admission:Busy', 'stateUnchanged')):
        row('F30', name, ['X2', 'X6c'], list(LABELS),
            [{'spawn': 'commit', 'name': 'writer', 'arm': f'{hold}=hold'},
             {'await': hold, 'on': 'writer', 'then': 'hold'},
             {'spawn': 'competitor-writer', 'name': 'b', 'unchanged': True},
             {'finish': 'b'},
             # (b): A is held before its ExecutionId draw, so C names no
             # attempt; C's report for N is scored.
             {'spawn': 'sweep', 'name': 'c', **({'for': 'writer'} if name == 'writer-held-under-lease' else {})},
             {'finish': 'c'},
             {'resume': hold, 'on': 'writer'},
             {'finish': 'writer'},
             {'ladder': 'R2', 'of': 'writer', 'r2': 'distinct'}],
            {'b': 'operation:Busy', f'b.{unchanged}': 'true',
             'c': 'nothing', 'c.report': c_report,
             'writer': COMMITTED, 'R2.outcome': COMMITTED})

    # ---------------------------------------------------------------- F34
    # Run A: `inject-id` with a previous run's ExecutionId (writer `first`,
    # a lawful commit). Run B: a separate `recover`, once with A's disclosed
    # requested binding and once with the earlier attempt's own binding.
    draw = point('x3d.session.execution-draw')
    row('F34', 'existing-attempt', ['X3d', 'X6'], LABELS_INJ,
        [{'spawn': 'commit', 'name': 'first'}, {'finish': 'first'},
         {'spawn': 'commit', 'name': 'a', 'arm': f'{draw}=inject-id:@first', 'unchanged': True},
         {'finish': 'a'},
         {'spawn': 'recover', 'name': 'b-disclosed', 'for': 'first', 'binding': 'disclosed:a', 'unchanged': True},
         {'finish': 'b-disclosed'},
         {'spawn': 'recover', 'name': 'b-own', 'for': 'first', 'binding': 'own', 'unchanged': True},
         {'finish': 'b-own'}],
        {'first': COMMITTED,
         'a': 'not-prepared:ExistingAttempt', 'a.subject': 'first',
         'a.ledgerUnchanged': 'true', 'a.sealsAdded': '0',
         'b-disclosed': 'binding-unusable:operation', 'b-disclosed.stateUnchanged': 'true',
         'b-own': CH_PENDING, 'b-own.stateUnchanged': 'true'})

    # ---------------------------------------------------------------- F38
    # Held at `x3d.publish.after-staging`; revoke; one tick latches 0→2;
    # resume. No permit, the staged transaction rolled back, `REV` and `CLN`
    # from the reserve. C5: R2 refused at admission, R3 refused, R4 TNC.
    hold = point('x3d.publish.after-staging')
    row('F38', 'revoked-after-staging', ['X3d', 'X4'], list(LABELS),
        revocation_script(hold, tail=[{'finish': 'writer'}]) + [LADDER],
        {'writer': REVOKED, 'writer.gate': '0,2', 'writer.rev': 'true', 'writer.cln': 'true',
         'writer.settlement': 'None', 'receipts': '0',
         'R1': UAO, 'R2.outcome': REFUSED_AT_ADMISSION, 'R3': 'refused', 'R4': TNC})

    # ---------------------------------------------------------------- F39
    # X9 r12's script (admission hold at `x3c.evidence.commit.before#1`).
    # Committed with `latchedAfterAdmission`, gate 1→3; R1 CH; R2 refused at
    # admission (C5). The host's DELIVERY.REQUIRED_FAILED is X9-5's.
    assert ADMISSION_HOLD == point('x3c.evidence.commit.before')
    row('F39', 'latch-after-admission', ['X3d', 'X4', 'X7'], list(LABELS),
        revocation_script(ADMISSION_HOLD, tail=[{'finish': 'writer'}]) + [LADDER],
        {'writer': LATCHED, 'writer.gate': '0,1,3', 'R1': CH, 'R2.outcome': REFUSED_AT_ADMISSION})

    # ---------------------------------------------------------------- F40
    # As F12, without the latch (landed and not landed), and (X9 r13) with
    # F39's latch, landed only. The latch does not convert the outcome;
    # nothing is appended; the ladder as F12.
    for phase, action, landed in (('after', 'fail-after', True), ('before', 'fail-before', False)):
        arm = f"{point(f'x3c.evidence.commit.{phase}')}={action}"
        row('F40', f'{action}-evidence-commit', ['X3d', 'X7'], LABELS_INJ, [{'arm': arm}],
            {'scripted': 'CommitUndetermined', 'scripted.end': UNDETERMINED_END,
             'R1': CH_PENDING if landed else UAO, 'R3': 'committed' if landed else 'refused',
             'R4': CH_SETTLED if landed else TNC})
    arm = f"{point('x3c.evidence.commit.after')}=fail-after"
    row('F40', 'fail-after-evidence-commit-latched', ['X3d', 'X7'], LABELS_INJ,
        revocation_script(ADMISSION_HOLD, arms=(arm,), tail=[{'finish': 'writer'}]) + [LADDER],
        {'writer': 'CommitUndetermined', 'writer.end': UNDETERMINED_END, 'writer.gate': '0,1,3',
         'R1': CH_PENDING, 'R3': 'committed', 'R4': CH_SETTLED})

    # ---------------------------------------------------------------- F41
    # The two process-level orders: the latch before admission (held at the
    # final checkpoint's `before-observation`, outside the shared monitor),
    # and admission before the latch (F39's script). At most one evidence
    # `COMMIT`; the gate stays in 0..3.
    for name, hold in (('latch-before-admission', point('x4.checkpoint.before-observation', 3)),
                       ('admission-before-latch', ADMISSION_HOLD)):
        row('F41', name, ['X4', 'X3d'], list(LABELS),
            revocation_script(hold, tail=[{'finish': 'writer'}]) + [LADDER],
            {'writer.evidenceCommits': ['0', '1'], 'writer.gate': list(GATE_IN_RANGE)})

    # ------------------------------------------------------- F14 (X9 r12)
    # F39's script, then a kill at `x3d.finish.settle.before` (a `REV` is
    # owed: the gate latched after admission), with F13's expectations; R2
    # commits r12's distinct variant. X9 r15: the row is X9-4's
    # (`"unit": "X9-4"`), and its R2 is refused at admission (C5), unscored.
    k = point(SETTLE)
    row('F14', variant('kill', k) + '-after-latch', ['X3d', 'X6'], LABELS_KILL,
        revocation_script(ADMISSION_HOLD, arms=(f'{k}=hold',),
                          tail=[{'await': k, 'on': 'writer', 'then': 'kill'}])
        + [{**LADDER, 'r2': 'distinct'}],
        {'writer': 'killed', 'R1': CH_PENDING, 'R2.outcome': REFUSED_AT_ADMISSION, 'R3': 'committed', 'R4': CH_SETTLED},
        unit='X9-4')


def main():
    required_path, census_path, out_path = sys.argv[1:]
    raw = open(required_path, 'rb').read()
    document = json.loads(raw)
    again = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    assert again == raw, 'the input required runs do not re-serialize to their own bytes'
    present = {(r['case'], r['variant']) for r in document['runs']}
    assert not any(c in X94_CASES for c, _ in present), 'the input already holds X9-4 rows'
    census = json.load(open(census_path))
    rows = []

    def row(case, var, units, labels, script, expected, unit=None):
        assert (case, var) not in present and all((case, var) != (r['case'], r['variant']) for r in rows), (case, var)
        entry = {'case': case, 'variant': var, 'units': units, 'labels': labels,
                 'script': script, 'expected': expected}
        if unit:
            entry['unit'] = unit  # X9 r15: a row a law moved to another unit
        rows.append(entry)

    x94_rows(census, row)
    earlier = list(document['runs'])
    document['runs'] = earlier + rows
    out = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    assert json.loads(out)['runs'][:len(earlier)] == json.loads(raw)['runs'], 'earlier rows changed'
    open(out_path, 'wb').write(out)
    counts = {}
    for r in rows:
        counts[r['case']] = counts.get(r['case'], 0) + 1
    print(json.dumps({'added': len(rows), 'total': len(document['runs']), 'byCase': counts}, sort_keys=True))


if __name__ == '__main__':
    main()
