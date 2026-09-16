"""Phase 3 -- provider protocol traces.

The sequencing/state law is derived from its published normative inputs only:
  native/protocol3-transitions.v1.json  phases, initialState, initializationAndUpdateOrder,
      matchLaw, preMatchLaw, guardLaw, stateUpdates, terminalLaw, noMatchLaw, wildcards,
      stageDependentTransitions, the 34 rules
  native-evidence.md section 9.1 (versions and identity negotiation), 9.2 (frames),
      9.3 (ProtocolLimitsV3 exact equality in Hello)

IDs: R-TRACE-COMPLETE, R-TRACE-UNAVAILABLE, R-TRACE-CANCEL, R-TRACE-FAULT,
     R-TRACE-IDENTITY-BEFORE-SOURCE, R-TRACE-TERMINAL, R-TRACE-EXECUTED-VS-HOST
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'
TR = json.load(open(S.KIT + '/docs/coop/design-corrections/native/'
                    'protocol3-transitions.v1.json'))
fails = []


def expect(c, label, detail=''):
    if not c:
        fails.append('%s :: %s' % (label, detail))


SOURCE_FRAMES = None
for u in TR['stateUpdates']:
    if 'onFrames' in u:
        SOURCE_FRAMES = set(u['onFrames'])
PROCESS_FAULT = set(TR['wildcards']['*PROCESS_FAULT']['frames'])
PRE_COMPLETE = set(TR['wildcards']['*PRE_COMPLETE']['phases'])


class Machine:
    """Independently implemented from initializationAndUpdateOrder. No author model read."""

    def __init__(self, stage_count=1, identity_tokens=('snapshot2', 'plan2', 'fact2',
                                                       'coverage2', 'scope2')):
        self.state = dict(TR['initialState'])
        self.trace = []
        self.log = []
        self.stage_count = stage_count
        self.identity_tokens = set(identity_tokens)

    def _match(self, frame):
        for r in TR['rules']:
            if r['phase'] == '*ANY':
                continue                      # applied only by preMatchLaw / noMatchLaw
            if r['phase'] == '*PRE_COMPLETE':
                if self.state['phase'] not in PRE_COMPLETE:
                    continue
            elif r['phase'] != self.state['phase']:
                continue
            if r['frame'] != frame:
                continue
            if any(self.state.get(k) != v for k, v in (r.get('guard') or {}).items()):
                continue
            return r
        return None

    def _apply_state_updates(self, frame, payload):
        if frame == 'HelloAck':
            caps = set((payload or {}).get('capabilities') or [])
            self.state['identityNegotiated'] = self.identity_tokens <= caps
        if frame == 'OpenUniverse':
            self.state['dependencyMode'] = bool((payload or {}).get('dependencyMode'))
            self.state['preparedMode'] = bool((payload or {}).get('preparedMode'))
        if frame == 'Analyze':
            self.state['stageCount'] = self.stage_count
            self.state['stageIndex'] = 0
        if SOURCE_FRAMES and frame in SOURCE_FRAMES:
            self.state['sourceBytesSent'] = True

    def event(self, frame, payload=None):
        before = dict(self.state)
        # preMatchLaw, in the published order
        if self.state['phase'] == 'FAULT':
            self.trace.append('FAULT-absorb')
            self._record(frame, before, 'FAULT-absorb', 'preMatchLaw[0]')
            return self
        if frame in PROCESS_FAULT:
            # entry [2]: from ANY phase. Listed AFTER the post-terminal entry, but the
            # post-terminal entry explicitly EXCLUDES *PROCESS_FAULT members, so the order
            # between [1] and [2] is not load-bearing for these frames.
            self.state['phase'] = 'FAULT'
            self.trace.append('P3-33')
            self._record(frame, before, 'P3-33', 'preMatchLaw[2]')
            return self
        if self.state['phase'] in ('WAIT_ZERO_EXIT', 'WAIT_EOF', 'DONE') \
                and frame not in ('zero-exit', 'eof'):
            self.state['phase'] = 'FAULT'
            self.trace.append('post-terminal-frame')
            self._record(frame, before, 'post-terminal-frame', 'preMatchLaw[1]')
            return self
        row = self._match(frame)
        if row is None:
            self.state['phase'] = 'FAULT'
            self.trace.append('P3-34')
            self._record(frame, before, 'P3-34', 'noMatchLaw')
            return self
        self._apply_state_updates(frame, payload)
        nxt = row['next']
        if nxt == 'ANALYZING_OR_READY_COMPLETE':
            self.state['stageIndex'] += 1
            self.state['stagesCompleted'] += 1
            nxt = ('READY_COMPLETE' if self.state['stageIndex'] >= self.state['stageCount']
                   else 'ANALYZING')
        if row.get('terminal'):
            self.state['terminalKind'] = row['terminal']
        self.state['phase'] = nxt
        self.trace.append(row['id'])
        self._record(frame, before, row['id'], 'matchLaw')
        return self

    def _record(self, frame, before, rule, law):
        self.log.append({'frame': frame, 'appliedBy': law, 'rule': rule,
                         'phaseBefore': before['phase'], 'phaseAfter': self.state['phase'],
                         'identityNegotiated': self.state['identityNegotiated'],
                         'sourceBytesSent': self.state['sourceBytesSent'],
                         'terminalKind': self.state['terminalKind'],
                         'stageIndex': self.state['stageIndex'],
                         'stagesCompleted': self.state['stagesCompleted']})


HELLO_ACK_FULL = {'capabilities': ['snapshot2', 'plan2', 'fact2', 'coverage2', 'scope2',
                                   'view2']}


def disjointness_control():
    """matchLaw: "The rows are in fact PAIRWISE DISJOINT ... a control asserts the
    disjointness, so such a row would be caught rather than silently resolved by where it
    happened to be written." Executed here over every (phase, frame) pair."""
    overlaps = []
    rows = [r for r in TR['rules'] if r['phase'] != '*ANY']
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            pa = PRE_COMPLETE if a['phase'] == '*PRE_COMPLETE' else {a['phase']}
            pb = PRE_COMPLETE if b['phase'] == '*PRE_COMPLETE' else {b['phase']}
            if not (pa & pb) or a['frame'] != b['frame']:
                continue
            ga, gb = a.get('guard') or {}, b.get('guard') or {}
            shared = set(ga) & set(gb)
            exclusive = any(ga[k] != gb[k] for k in shared)
            if not exclusive:
                overlaps.append((a['id'], b['id'], sorted(pa & pb), a['frame']))
    expect(not overlaps, 'protocol3 rows must be pairwise disjoint', str(overlaps))
    return {'check': 'matchLaw.PAIRWISE_DISJOINT', 'overlaps': overlaps,
            'rowsCompared': len(rows), 'result': 'PASS' if not overlaps else 'FAIL',
            'classification': 'valid'}


def limits_control():
    """section 9.3: ProtocolLimitsV3, exact equality in Hello."""
    lim = json.load(open(S.KIT + '/' + S.doc_path(
        'native/native-evidence.schemas.v2.json')))['$defs']['ProtocolLimitsV3']
    consts = {}

    def walk(n, p=''):
        if isinstance(n, dict):
            if 'const' in n:
                consts[p] = n['const']
            for k, v in n.items():
                walk(v, p + '/' + k)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                walk(v, p + '/%d' % i)
    walk(lim)
    hello_ok = {'schemaVersion': 3, 'protocolMajor': 3, 'limits': {}}
    props = lim.get('properties', {})
    for k, v in props.items():
        if isinstance(v, dict) and 'const' in v:
            hello_ok['limits'][k] = v['const']
    r_ok = S.admit('native/native-evidence.schemas.v2.json', '#/$defs/ProtocolLimitsV3',
                   hello_ok['limits'] if set(hello_ok['limits']) == set(props) else None,
                   'ProtocolLimitsV3-exact')
    mutated = dict(hello_ok['limits'])
    if mutated:
        k0 = sorted(mutated)[0]
        if isinstance(mutated[k0], int):
            mutated[k0] = mutated[k0] + 1
    r_bad = S.admit('native/native-evidence.schemas.v2.json', '#/$defs/ProtocolLimitsV3',
                    mutated, 'ProtocolLimitsV3-off-by-one')
    expect(bool(r_bad['stockSchemaErrors']),
           'a limits value differing from the declared const must refuse')
    return {'check': 'section9.3:PROTOCOL_LIMITS_EXACT_EQUALITY_IN_HELLO',
            'declaredConstFields': {k: v['const'] for k, v in props.items()
                                    if isinstance(v, dict) and 'const' in v},
            'exactLimitsAdmitted': r_ok['admitted'] if r_ok['stockSchemaErrors'] == [] else
                                   'not-all-fields-const',
            'offByOneRefused': bool(r_bad['stockSchemaErrors']),
            'offByOneErrors': r_bad['stockSchemaErrors'][:2],
            'classification': 'valid + invalid control'}


def trace(name, events, expect_phase, expect_terminal, notes, executed_vs_host, stage_count=1):
    m = Machine(stage_count=stage_count)
    for ev in events:
        if isinstance(ev, tuple):
            m.event(ev[0], ev[1])
        else:
            m.event(ev)
    expect(m.state['phase'] == expect_phase,
           '%s final phase' % name, '%s != %s' % (m.state['phase'], expect_phase))
    expect(m.state['terminalKind'] == expect_terminal,
           '%s terminalKind' % name, '%s != %s' % (m.state['terminalKind'], expect_terminal))
    return {'trace': name, 'events': [e[0] if isinstance(e, tuple) else e for e in events],
            'ruleTrace': m.trace, 'finalPhase': m.state['phase'],
            'terminalKind': m.state['terminalKind'],
            'identityNegotiated': m.state['identityNegotiated'],
            'sourceBytesSent': m.state['sourceBytesSent'],
            'stagesCompleted': m.state['stagesCompleted'],
            'stepLog': m.log, 'notes': notes,
            'executedVsHost': executed_vs_host,
            'classification': 'valid' if expect_terminal in ('complete',) else 'invalid'}


EXECUTED = ('EXECUTED in this reconstruction: the phase/rule/guard/state sequence is '
            'computed by this origin\'s own implementation of the published transition '
            'table over synthetic frame events.')
HOST = ('FUTURE-HOST ASSUMPTION, not executed here: that a real worker process emits these '
        'frames, that its exit status and EOF are really observed, and that its payload '
        'bytes are what it claims. No process was spawned and no provider executed.')


def main():
    full = ['Hello', ('HelloAck', HELLO_ACK_FULL),
            ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
            'UniverseAccepted', 'SnapshotManifest', 'SnapshotFileChunk', 'SnapshotFileChunk', 'SnapshotSeal',
            'SnapshotAccepted', 'NativeContextVerified', 'Analyze',
            'FactBatch', 'FactBatch', 'CoverageV3', 'Complete', 'zero-exit', 'eof']
    traces = [
        trace('complete', full, 'DONE', 'complete',
              ['the full exchange: identity negotiation, sealed snapshot transfer, native '
               'context verification, one analyze stage, Complete, then the SEPARATE '
               'process observations zero-exit and eof (terminalLaw: reaching a terminal '
               'does not end the exchange)',
               'dependencyMode=false and preparedMode=false select P3-10, so the exchange '
               'goes straight from SnapshotAccepted to WAIT_NATIVE_CONTEXT_VERIFIED'],
              EXECUTED + ' ' + HOST),
        trace('complete-dependency-and-prepared',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': True, 'preparedMode': True}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'DependencySourceManifest', 'DependencySourceChunk', 'DependencySourceSeal',
               'DependencySourceAccepted', 'PreparedOutputManifest', 'PreparedOutputChunk',
               'PreparedOutputSeal', 'PreparedOutputAccepted', 'NativeContextVerified',
               'Analyze', 'CoverageV3', 'Complete', 'zero-exit', 'eof'],
              'DONE', 'complete',
              ['exercises the guarded branches P3-08 and P3-14 that the default trace skips'],
              EXECUTED + ' ' + HOST),
        trace('complete-two-stages',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'CoverageV3', 'FactBatch', 'CoverageV3',
               'Complete', 'zero-exit', 'eof'],
              'DONE', 'complete',
              ['stageDependentTransitions: the first CoverageV3 increments stageIndex to 1 '
               'and stays in ANALYZING because stageCount is 2; the second reaches '
               'READY_COMPLETE'],
              EXECUTED + ' ' + HOST, stage_count=2),
        trace('unavailable-before-analyze',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'Unavailable', 'zero-exit', 'eof'],
              'DONE', 'unavailable',
              ['P3-21: Unavailable in WAIT_NATIVE_CONTEXT_VERIFIED. Discriminating against '
               'the complete trace: the terminalKind is `unavailable` and NO Analyze, '
               'FactBatch or CoverageV3 frame ever occurred, so the exchange contributes no '
               'fact and no Coverage'],
              EXECUTED + ' ' + HOST),
        trace('unavailable-during-analyze',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'FactBatch', 'Unavailable',
               'zero-exit', 'eof'],
              'DONE', 'unavailable',
              ['P3-25: a partial exchange. Facts were sent but no CoverageV3 closed a '
               'stage, so stagesCompleted is 0 -- the discriminator against `complete`'],
              EXECUTED + ' ' + HOST),
        trace('budget-exhausted',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'BudgetExhausted', 'zero-exit', 'eof'],
              'DONE', 'budget-exhausted',
              ['P3-26, the fifth terminal kind; distinct from the evaluator\'s own '
               'EVALUATION.WORK_BUDGET_EXHAUSTED, which is a semantic disclosure'],
              EXECUTED + ' ' + HOST),
        trace('cancellation',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'FactBatch', 'Cancel', 'Cancelled',
               'zero-exit', 'eof'],
              'DONE', 'cancelled',
              ['P3-29 then P3-30: Cancel is accepted anywhere in *PRE_COMPLETE and the '
               'worker must still answer Cancelled, then be observed at zero-exit and eof'],
              EXECUTED + ' ' + HOST),
        trace('cancellation-not-acknowledged',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'Cancel', 'FactBatch'],
              'FAULT', None,
              ['in WAIT_CANCELLED only Cancelled is admissible; a FactBatch matches no row '
               'and noMatchLaw sends it to FAULT with trace P3-34. terminalKind stays null: '
               'a fault is NOT a terminal kind'],
              EXECUTED + ' ' + HOST),
        trace('provider-fault',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'ProviderFault', 'zero-exit', 'eof'],
              'DONE', 'provider-fault',
              ['P3-28: an in-band provider fault is a TERMINAL kind and still requires '
               'zero-exit and eof, which is what distinguishes it from an out-of-band '
               'process fault'],
              EXECUTED + ' ' + HOST),
        trace('process-fault-signal-death',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'FactBatch', 'signal-death'],
              'FAULT', None,
              ['P3-33 via preMatchLaw[2]: an out-of-band *PROCESS_FAULT observation goes to '
               'FAULT from ANY phase and records NO terminalKind. Contrast provider-fault '
               'above, which is in-band and terminal'],
              EXECUTED + ' (the frame is a synthetic observation) ' + HOST),
        trace('process-fault-nonzero-exit',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'CoverageV3', 'Complete',
               'nonzero-exit'],
              'FAULT', 'complete',
              ['a terminal was recorded and then the PROCESS failed: terminalKind stays '
               '`complete` while the phase is FAULT. "complete protocol transaction PLUS '
               'successful process exit AND EOF before facts are admitted" -- this trace '
               'never reaches DONE, so no fact is admitted'],
              EXECUTED + ' ' + HOST),
        trace('stdout-byte-is-a-process-fault',
              ['Hello', ('HelloAck', HELLO_ACK_FULL), 'stdout-byte'],
              'FAULT', None,
              ['a byte on stdout is an out-of-band process observation, not a frame'],
              EXECUTED + ' ' + HOST),
        trace('fault-is-absorbing',
              ['Hello', ('HelloAck', HELLO_ACK_FULL), 'signal-death', 'FactBatch',
               'zero-exit', 'eof'],
              'FAULT', None,
              ['preMatchLaw[0]: once FAULT, every further event is `FAULT-absorb` and '
               'nothing transitions -- including zero-exit and eof, so a faulted exchange '
               'can never be laundered into DONE'],
              EXECUTED + ' ' + HOST),
        trace('post-terminal-frame',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'CoverageV3', 'Complete', 'FactBatch'],
              'FAULT', 'complete',
              ['preMatchLaw[1]: in WAIT_ZERO_EXIT any frame other than zero-exit/eof/'
               '*PROCESS_FAULT is a post-terminal frame and faults'],
              EXECUTED + ' ' + HOST),
        trace('eof-before-zero-exit',
              ['Hello', ('HelloAck', HELLO_ACK_FULL),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False}),
               'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted',
               'NativeContextVerified', 'Analyze', 'CoverageV3', 'Complete', 'eof'],
              'FAULT', 'complete',
              ['the ORDER of the two process observations is load-bearing: eof in '
               'WAIT_ZERO_EXIT matches no row, so noMatchLaw faults it (P3-34). zero-exit '
               'must precede eof'],
              EXECUTED + ' ' + HOST),
        # ---- identity negotiation BEFORE source disclosure
        trace('source-before-identity-negotiation-refused',
              ['Hello', ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False})],
              'FAULT', None,
              ['R-TRACE-IDENTITY-BEFORE-SOURCE, negative half: OpenUniverse is attempted in '
               'WAIT_HELLO_ACK. No row matches (P3-03 requires phase READY_OPEN_UNIVERSE), '
               'so the exchange faults with sourceBytesSent still FALSE -- not one source '
               'byte was disclosed'],
              EXECUTED + ' ' + HOST),
        trace('incomplete-identity-token-set-refused',
              ['Hello', ('HelloAck', {'capabilities': ['snapshot2', 'plan2']}),
               ('OpenUniverse', {'dependencyMode': False, 'preparedMode': False})],
              'FAULT', None,
              ['R-TRACE-IDENTITY-BEFORE-SOURCE, guard half: HelloAck advertises only part '
               'of the identity token set, so identityNegotiated stays FALSE, the guard of '
               'P3-03 fails, no row matches and the run faults with NO source byte sent -- '
               'exactly what guardLaw states'],
              EXECUTED + ' ' + HOST),
    ]
    # identity-before-source invariant, measured across every trace
    inv = []
    for t in traces:
        first_src = None
        first_neg = None
        for i, s in enumerate(t['stepLog']):
            if first_neg is None and s['identityNegotiated']:
                first_neg = i
            if first_src is None and s['sourceBytesSent']:
                first_src = i
        ok = (first_src is None) or (first_neg is not None and first_neg < first_src)
        inv.append({'trace': t['trace'], 'firstStepWithIdentityNegotiated': first_neg,
                    'firstStepWithSourceBytesSent': first_src,
                    'identityPrecededSource': ok})
        expect(ok, 'identity negotiated before any source byte: ' + t['trace'],
               '%s / %s' % (first_neg, first_src))
    # terminal-kind coverage: every terminal kind the table declares must be reached
    declared = sorted({r['terminal'] for r in TR['rules'] if r.get('terminal')})
    reached = sorted({t['terminalKind'] for t in traces if t['terminalKind']})
    expect(set(declared) == set(reached), 'every declared terminal kind exercised',
           '%s vs %s' % (declared, reached))

    res = {
        'consumerId': 'consumer-b.v18', 'phase': 3,
        'law': {'document': 'docs/coop/design-corrections/native/protocol3-transitions.v1.json',
                'documentSha256': K.raw_sha256(open(
                    S.KIT + '/docs/coop/design-corrections/native/'
                    'protocol3-transitions.v1.json', 'rb').read()),
                'phases': TR['phases'], 'ruleCount': TR['ruleCount'],
                'declaredTerminalKinds': declared,
                'processFaultFrames': sorted(PROCESS_FAULT),
                'sourceBytesSentFrames': sorted(SOURCE_FRAMES or []),
                'ownedByProse': TR['ownedByProse']},
        'R-TRACE-COMPLETE': [t for t in traces if t['trace'].startswith('complete')],
        'R-TRACE-UNAVAILABLE': [t for t in traces if 'unavailable' in t['trace']],
        'R-TRACE-CANCEL': [t for t in traces if 'cancel' in t['trace']],
        'R-TRACE-FAULT': [t for t in traces
                          if 'fault' in t['trace'] or t['trace'] in
                          ('post-terminal-frame', 'eof-before-zero-exit',
                           'stdout-byte-is-a-process-fault')],
        'R-TRACE-TERMINAL': {
            'terminalLaw': TR['terminalLaw'],
            'declaredTerminalKinds': declared, 'reachedTerminalKinds': reached,
            'allDeclaredKindsReached': set(declared) == set(reached),
            'postTerminalAndAbsorbingTraces': [
                {'trace': t['trace'], 'ruleTrace': t['ruleTrace'],
                 'finalPhase': t['finalPhase'], 'terminalKind': t['terminalKind']}
                for t in traces if t['trace'] in
                ('post-terminal-frame', 'fault-is-absorbing', 'eof-before-zero-exit',
                 'process-fault-nonzero-exit')],
            'onlyDoneAdmitsFacts': (
                'Inherited unchanged constraint (identity-and-evidence section 1): '
                '"complete protocol transaction plus successful process exit and EOF before '
                'facts are admitted." Measured: only the DONE traces satisfy all three.')},
        'R-TRACE-IDENTITY-BEFORE-SOURCE': {
            'guardLaw': TR['guardLaw'], 'perTrace': inv,
            'holdsForEveryTrace': all(x['identityPrecededSource'] for x in inv)},
        'R-TRACE-EXECUTED-VS-HOST': [
            {'trace': t['trace'], 'executedVsHost': t['executedVsHost']} for t in traces],
        'controls': [disjointness_control(), limits_control()],
        'allTraces': traces,
    }
    os.makedirs(OUT + '/traces', exist_ok=True)
    with open(OUT + '/traces/protocol3-traces.json', 'w') as f:
        json.dump(res, f, indent=1)
    for nm, key in (('complete', 'R-TRACE-COMPLETE'), ('unavailable', 'R-TRACE-UNAVAILABLE'),
                    ('cancel', 'R-TRACE-CANCEL'), ('fault', 'R-TRACE-FAULT')):
        with open(OUT + '/traces/%s.json' % nm, 'w') as f:
            json.dump(res[key], f, indent=1)
    print('traces:', len(traces))
    for t in traces:
        print('  %-40s -> %-8s terminal=%-16s trace=%s'
              % (t['trace'], t['finalPhase'], t['terminalKind'], ','.join(t['ruleTrace'])))
    print()
    print('declared terminal kinds:', declared)
    print('reached terminal kinds :', reached)
    print('identity-before-source holds for every trace:',
          res['R-TRACE-IDENTITY-BEFORE-SOURCE']['holdsForEveryTrace'])
    print('disjointness control:', res['controls'][0]['result'])
    print('limits off-by-one refused:', res['controls'][1]['offByOneRefused'])
    print('failures:', len(fails))
    for f_ in fails:
        print('  FAIL', f_)
    if fails:
        sys.exit(1)


main()
