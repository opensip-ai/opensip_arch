# Control C6 - executable concurrency SCHEDULE controls for the bounded read-only recovery
# protocol.
#
# Not fixed coherent tuples. The reader is a coroutine that yields after EVERY observation, and a
# concurrent writer's steps are released between those yields. Every monotone assignment of writer
# steps to reader-yield slots is enumerated, so temporally skewed observations genuinely occur.
#
# Three families:
#   R  race 1 - the requested attempt is already committed and settled; a DIFFERENT lawful
#      APPEND-WRITE attempt advances the tail, witness and floor during the reader's capture.
#      This is root's schedule 1.
#   S  race 2 - the writer is performing the REQUESTED attempt and commits then settles around
#      the reader's ledger snapshot. This is root's schedule 2.
#   Q  quiescent positive controls - no writer at all, carrier genuinely and stably adverse.
#      These prove the stability gate did not silently disable the diagnosis.
#
# Coverage is asserted, not assumed: a control that never exercises the race proves nothing.
#
# usage: python c6-schedules.py <reportPath>
import itertools
import json
import sys

OUT = sys.argv[1]
PKD = 'e' * 64
REQ = 'exec1_' + '1' * 32      # the attempt the reader asks about
OTHER = 'exec1_' + '2' * 32    # a different, concurrent attempt


def bsha(seq):
    return '%064x' % seq


class World:
    def __init__(self, tail0, floor0, writerSeq, writerExec,
                 seedReceipt=None, seedPhase='admitted', corrupt=None):
        self.tail = tail0
        self.witness = {'witnessSchema': 1, 'projectKeyDigest': PKD, 'grantGeneration': 1,
                        'seq': tail0, 'state': 'COMMITTED', 'bodySha256': bsha(tail0)}
        self.floor = {'projectKeyDigest': PKD, 'grantGeneration': 1,
                      'lastSeq': floor0, 'tailSha256': bsha(floor0) if floor0 else None}
        self.receipts = {}
        self.attempts = {}
        if seedReceipt is not None:
            self.receipts[REQ] = seedReceipt
        if seedPhase == 'settled':
            # a seeded settled attempt must carry the outcome its receipt implies
            self.attempts[REQ] = ('settled', 'committed' if seedReceipt is not None else 'refused')
        elif seedPhase is not None:
            self.attempts[REQ] = seedPhase
        self.writerSeq = writerSeq
        self.writerExec = writerExec
        self.reqEverCommitted = seedReceipt is not None
        self.ledgerVersion = 0
        if corrupt == 'witnessBeyondTail':
            self.witness = dict(self.witness, seq=tail0 + 3, bodySha256=bsha(tail0 + 3))
        elif corrupt == 'tailBelowFloor':
            self.floor = {'projectKeyDigest': PKD, 'grantGeneration': 1,
                          'lastSeq': tail0 + 5, 'tailSha256': bsha(tail0 + 5)}
        elif corrupt == 'witnessForeign':
            self.witness = dict(self.witness, projectKeyDigest='9' * 64)
        elif corrupt == 'witnessMalformed':
            self.witness = dict(self.witness, seq=True)
        elif corrupt == 'floorHashMismatch':
            self.floor = {'projectKeyDigest': PKD, 'grantGeneration': 1,
                          'lastSeq': floor0, 'tailSha256': '7' * 64}

    # lawful writer steps for whichever attempt the writer is performing
    def w_witness_pending(self):
        self.witness = dict(self.witness, seq=self.writerSeq, state='PENDING',
                            bodySha256=bsha(self.writerSeq))

    def w_append_durable(self):
        self.tail = self.writerSeq

    def w_witness_committed(self):
        self.witness = dict(self.witness, seq=self.writerSeq, state='COMMITTED',
                            bodySha256=bsha(self.writerSeq))

    def w_ledger_commit(self):
        self.ledgerVersion += 1
        self.receipts[self.writerExec] = self.writerSeq
        if self.writerExec == REQ:
            self.reqEverCommitted = True

    def w_floor_copy(self):
        self.floor = {'projectKeyDigest': PKD, 'grantGeneration': 1,
                      'lastSeq': self.tail, 'tailSha256': bsha(self.tail)}

    def w_attempt_settle(self):
        # The settle write is ordered AFTER the receipt write, and it records the outcome it
        # actually observed. There is no undetermined custody outcome.
        self.ledgerVersion += 1
        outcome = 'committed' if self.writerExec in self.receipts else 'refused'
        self.attempts[self.writerExec] = ('settled', outcome)

    def snap_ledger(self):
        return {'version': self.ledgerVersion, 'receipts': dict(self.receipts),
                'attempts': dict(self.attempts)}

    def snap_journal(self):
        return {'tail': self.tail, 'tailSha256': bsha(self.tail) if self.tail else None}

    def read_witness(self):
        return dict(self.witness)

    def read_floor(self):
        return dict(self.floor)


COMMITTING = ['w_witness_pending', 'w_append_durable', 'w_witness_committed',
              'w_ledger_commit', 'w_floor_copy', 'w_attempt_settle']
REFUSED = ['w_witness_pending', 'w_append_durable', 'w_witness_committed',
           'w_floor_copy', 'w_attempt_settle']
EARLY_REFUSED = ['w_attempt_settle']
QUIESCENT = []


def witness_shape_ok(w):
    keys = {'witnessSchema', 'projectKeyDigest', 'grantGeneration', 'seq', 'state', 'bodySha256'}
    if not isinstance(w, dict) or set(w.keys()) != keys:
        return False
    if w['witnessSchema'] != 1 or type(w['seq']) is bool or not isinstance(w['seq'], int):
        return False
    if w['state'] not in ('PENDING', 'COMMITTED'):
        return False
    if w['state'] == 'PENDING' and w['seq'] < 1:
        return False
    return True


def classify(cap, k):
    """(anchorClass, adverseCondition, adverseIsCorruptionClaim)."""
    J, W, H = cap['J'], cap['W'], cap['H']
    t = J['tail']
    if not witness_shape_ok(W):
        return None, 'witnessMalformed', True
    if W['projectKeyDigest'] != PKD or W['grantGeneration'] != 1:
        return None, 'witnessForeignCarrier', True
    if H['lastSeq'] > t:
        return None, 'tailBelowObservedFloor', True
    if H['lastSeq'] != 0 and H['tailSha256'] != bsha(H['lastSeq']):
        return None, 'floorContradictsTail', True
    if W['state'] == 'COMMITTED' and W['seq'] == t and W['bodySha256'] == bsha(t):
        return 'witness-committed-tail', None, False
    if W['state'] == 'PENDING' and W['seq'] == t and W['bodySha256'] == bsha(t):
        return 'witness-pending-at-tail', None, False
    if W['state'] == 'PENDING' and W['seq'] == t + 1:
        if k is not None and k <= H['lastSeq']:
            return 'sc-trust-floor', None, False
        return None, 'aboveFloorUnderPendingNextSlot', False
    return None, 'witnessStateUnreconciled', True


def usable(anchorClass, cap):
    if anchorClass in ('witness-committed-tail', 'witness-pending-at-tail'):
        return cap['stableW']
    if anchorClass == 'sc-trust-floor':
        return cap['stableH']
    return False


def reader(world, counters, cover):
    """Bounded read-only recovery. Yields after every observation; returns the conclusion."""
    def obs(kind, value):
        counters[kind] += 1
        return value

    L = obs('ledger', world.snap_ledger())
    yield 'ledger-snapshot'

    k = L['receipts'].get(REQ)
    cust = L['attempts'].get(REQ)
    phase = cust[0] if isinstance(cust, tuple) else cust
    outcome = cust[1] if isinstance(cust, tuple) else None

    if k is None:
        if cust is None:
            return 'unknown-attempt-unobserved'
        if phase == 'admitted':
            return 'unknown-attempt-open'
        if outcome == 'refused':
            return 'terminal-not-committed'
        return 'unknown-custody'
    # A joined receipt with the attempt still admitted is the LAWFUL pre-settle interval, because
    # the settle write is ordered after the receipt write. It continues to the capture and the
    # caller discloses pendingSettlement. Only settled+refused beside a receipt is contradictory.
    if outcome == 'refused' or phase == 'admitted':
        return 'unknown-custody'

    caps = []
    for attempt in (1, 2):
        w1 = obs('witness', world.read_witness())
        yield 'witness-before'
        h1 = obs('floor', world.read_floor())
        yield 'floor-before'
        J = obs('journal', world.snap_journal())
        yield 'journal-snapshot'
        w2 = obs('witness', world.read_witness())
        yield 'witness-after'
        h2 = obs('floor', world.read_floor())
        yield 'floor-after'
        cap = {'J': J, 'W': w2, 'H': h2, 'stableW': w1 == w2, 'stableH': h1 == h2}
        caps.append(cap)
        if not cap['stableW']:
            cover['witnessUnstable'] = True
        if not cap['stableH']:
            cover['floorUnstable'] = True
        a, adverse, isCorruptionClaim = classify(cap, k)
        hazard = k > J['tail']
        if hazard:
            cover['hazard'] = True
        if adverse is not None:
            cover['adverseSeen'] = True
        if a is not None and usable(a, cap) and not hazard:
            if attempt == 2:
                cover['confirmedOnRetry'] = True
            return 'committed-historically:' + a
        if attempt == 1:
            cover['retried'] = True
            continue

        stableTail = (caps[0]['J']['tail'] == caps[1]['J']['tail']
                      and caps[0]['J']['tailSha256'] == caps[1]['J']['tailSha256'])
        if hazard:
            if cap['stableH'] and cap['H']['lastSeq'] >= k and stableTail:
                return 'unknown-quarantine-condition'
            return 'unavailable-busy'
        if adverse == 'aboveFloorUnderPendingNextSlot':
            return 'unknown-custody'
        if adverse is not None:
            if isCorruptionClaim and not (cap['stableW'] and cap['stableH'] and stableTail):
                cover['skewSuppressedCorruptionClaim'] = True
                return 'unavailable-busy'
            return 'unknown-quarantine-condition'
        return 'unavailable-busy'


def run(make_world, writer_steps, slots):
    world = make_world()
    counters = {'ledger': 0, 'journal': 0, 'witness': 0, 'floor': 0}
    cover = {}
    gen = reader(world, counters, cover)
    wi, n, yielded = 0, len(writer_steps), 0
    while wi < n and slots[wi] == 0:
        getattr(world, writer_steps[wi])()
        wi += 1
    conclusion, ledgerSnap = None, None
    while True:
        try:
            label = next(gen)
        except StopIteration as e:
            conclusion = e.value
            break
        if label == 'ledger-snapshot':
            ledgerSnap = world.snap_ledger()
        yielded += 1
        while wi < n and slots[wi] == yielded:
            getattr(world, writer_steps[wi])()
            wi += 1
    while wi < n:
        getattr(world, writer_steps[wi])()
        wi += 1
    return world, counters, conclusion, ledgerSnap, cover


MAX_SLOT = 11

CONFIGS = [
    # family R - race 1: requested attempt already committed and settled at k=9,
    # a DIFFERENT lawful attempt advances the carrier during the capture
    ('R1 root schedule 1: receipt k=9, tail 10, concurrent attempt appends 11',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled'), COMMITTING, False),
    ('R2 race 1 with the floor already at the tail',
     lambda: World(10, 10, 11, OTHER, seedReceipt=9, seedPhase='settled'), COMMITTING, False),
    ('R3 race 1 with a far lagging floor',
     lambda: World(10, 2, 11, OTHER, seedReceipt=9, seedPhase='settled'), COMMITTING, False),
    ('R4 race 1 where the requested receipt IS the tail',
     lambda: World(10, 9, 11, OTHER, seedReceipt=10, seedPhase='settled'), COMMITTING, False),
    ('R5 race 1 ordering hazard: receipt k=12 above the observed tail',
     lambda: World(10, 9, 12, OTHER, seedReceipt=12, seedPhase='settled'), COMMITTING, False),
    # family S - race 2: the writer performs the REQUESTED attempt
    ('S1 race 2: writer commits and settles the requested attempt',
     lambda: World(9, 9, 10, REQ, seedReceipt=None, seedPhase='admitted'), COMMITTING, False),
    ('S2 race 2: requested attempt refused, orphan SEAL durable (F36)',
     lambda: World(9, 9, 10, REQ, seedReceipt=None, seedPhase='admitted'), REFUSED, False),
    ('S3 race 2: requested attempt refused before any append',
     lambda: World(9, 9, 10, REQ, seedReceipt=None, seedPhase='admitted'), EARLY_REFUSED, False),
    ('S4 race 2: attempt never reserved in this store generation',
     lambda: World(9, 9, 10, REQ, seedReceipt=None, seedPhase=None), EARLY_REFUSED, False),
    # family Q - quiescent positive controls for the diagnosis itself
    ('Q1 quiescent corrupt: witness COMMITTED beyond the tail',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled',
                   corrupt='witnessBeyondTail'), QUIESCENT, True),
    ('Q2 quiescent corrupt: tail below the observed floor',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled',
                   corrupt='tailBelowFloor'), QUIESCENT, True),
    ('Q3 quiescent corrupt: witness names a foreign carrier',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled',
                   corrupt='witnessForeign'), QUIESCENT, True),
    ('Q4 quiescent corrupt: malformed witness sequence',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled',
                   corrupt='witnessMalformed'), QUIESCENT, True),
    ('Q5 quiescent corrupt: floor digest contradicts the tail',
     lambda: World(10, 9, 11, OTHER, seedReceipt=9, seedPhase='settled',
                   corrupt='floorHashMismatch'), QUIESCENT, True),
]

results, violations = [], []
per_config, coverage = {}, {}
for label, mk, steps, isCorrupt in CONFIGS:
    n = len(steps)
    slot_space = ([()] if n == 0
                  else list(itertools.combinations_with_replacement(range(MAX_SLOT + 1), n)))
    agg = {}
    cov = {}
    for slots in slot_space:
        world, counters, conclusion, ledgerSnap, cover = run(mk, steps, slots)
        for key in cover:
            cov[key] = True
        receiptInSnapshot = ledgerSnap is not None and REQ in ledgerSnap['receipts']
        base = conclusion.split(':')[0]
        agg[base] = agg.get(base, 0) + 1
        bad = []
        if not isCorrupt and base == 'unknown-quarantine-condition':
            bad.append('false-quarantine-from-lawful-writer')
        if base == 'terminal-not-committed' and world.reqEverCommitted:
            bad.append('false-terminal-not-committed')
        if base == 'terminal-not-committed':
            cu = ledgerSnap['attempts'].get(REQ) if ledgerSnap else None
            if not (isinstance(cu, tuple) and cu == ('settled', 'refused')):
                bad.append('negative-without-settled-refused')
            if ledgerSnap and REQ in ledgerSnap['receipts']:
                bad.append('negative-with-a-receipt-in-the-snapshot')
        if base == 'committed-historically' and not receiptInSnapshot:
            bad.append('committed-without-receipt-in-snapshot')
        if counters['ledger'] != 1:
            bad.append('ledger-snapshot-count')
        if counters['journal'] > 2:
            bad.append('journal-snapshot-bound')
        if counters['witness'] > 4 or counters['floor'] > 4:
            bad.append('observation-bound')
        row = {'config': label, 'slots': list(slots), 'conclusion': conclusion,
               'receiptInSnapshot': receiptInSnapshot, 'counters': dict(counters)}
        if bad:
            row['violations'] = bad
            violations.append(row)
        results.append(row)
    per_config[label] = agg
    coverage[label] = sorted(cov)

hist = {}
for r_ in results:
    b = r_['conclusion'].split(':')[0]
    hist[b] = hist.get(b, 0) + 1

race1 = [c[0] for c in CONFIGS if c[0].startswith('R')]
quiesc = [c[0] for c in CONFIGS if c[0].startswith('Q')]
coverage_ok = {
    'race1_witness_instability_exercised':
        any('witnessUnstable' in coverage[c] for c in race1),
    'race1_floor_instability_exercised':
        any('floorUnstable' in coverage[c] for c in race1),
    'race1_adverse_observation_seen':
        any('adverseSeen' in coverage[c] for c in race1),
    'race1_skew_suppressed_a_corruption_claim':
        any('skewSuppressedCorruptionClaim' in coverage[c] for c in race1),
    'race1_confirmed_on_the_single_retry':
        any('confirmedOnRetry' in coverage[c] for c in race1),
    'ordering_hazard_exercised': any('hazard' in coverage[c] for c in coverage),
    'pending_settlement_interval_exercised':
        any('pendingSettlementInterval' in coverage[c] for c in coverage),
    'every_quiescent_corrupt_config_reports_the_condition':
        all(per_config[c].get('unknown-quarantine-condition', 0) > 0 for c in quiesc),
}

rep = {
    'control': 'c6-schedules',
    'model': ('reader coroutine yielding after every observation; writer steps released into '
              'reader-yield slots; every monotone slot assignment enumerated'),
    'maxReaderYields': MAX_SLOT,
    'totalSchedules': len(results),
    'conclusionHistogram': hist,
    'perConfigHistogram': per_config,
    'coverageFlagsPerConfig': coverage,
    'coverageAssertions': coverage_ok,
    'allCoverageAssertionsHeld': all(coverage_ok.values()),
    'violationCount': len(violations),
    'violations': violations[:20],
    'allInvariantsHeld': not violations,
    'invariants': [
        'I1 no quarantine/corruption conclusion from a lawful writer, in any schedule',
        'I2 no terminal not-committed conclusion for an attempt that committed at any point',
        'I3 no committed conclusion unless the receipt was in the single ledger snapshot',
        'I4 read-only and bounded: exactly 1 ledger snapshot, at most 2 journal snapshots, '
        'at most 4 witness and 4 floor reads, 0 mutations',
        'I5 every quiescent genuinely corrupt carrier is still diagnosable',
    ],
}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('schedules', len(results), 'violations', len(violations))
print('histogram', json.dumps(hist, sort_keys=True))
print()
for c in CONFIGS:
    print(' %-62s %s' % (c[0][:62], json.dumps(per_config[c[0]], sort_keys=True)))
print()
print('coverage assertions:', json.dumps(coverage_ok, indent=1, sort_keys=True))
for v in violations[:8]:
    print('  VIOLATION', v['violations'], v['config'], v['slots'])
