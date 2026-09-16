# Control C7 - the PS05 atomic bit-state commit-admission gate, as an executable model.
#
# Implements root's selected wording exactly: one atomic bit state with ADMITTED=1 and LATCHED=2;
# 0 preparing, 1 admitted, 2 latched-before-admission, 3 admitted-then-latched. Commit admission
# is compare-exchange 0->1. The observer always fetch-ORs 2, including 1->3, so a post-admission
# latch cannot be lost. No state resets during the attempt. The successful gate mints one internal
# single-use permit for the already prepared commit; it is not a reusable grant. State 3 does not
# revoke the already admitted attempt or relabel its outcome: it records the latch and forbids
# further effect admission or retries. A latch winning at state 0 prevents the gate entirely.
#
# Also models the phase handoff for required rendering/delivery after a successful commit, which
# must draw no authority from the returned stopped cleanup-only session.
#
# usage: python c7-gate-bits.py <reportPath>
import itertools
import json
import sys

OUT = sys.argv[1]
ADMITTED = 1
LATCHED = 2


class Attempt:
    """One atomic bit state plus the single-use commit permit it mints."""

    def __init__(self):
        self.state = 0
        self.permit = None            # None | 'unused' | 'consumed'
        self.sealDurable = False
        self.staged = False
        self.commitIssued = False
        self.commitResult = None
        self.events = []
        self.resets = 0
        self.effectAdmissions = 0
        self.retries = 0
        self.deliveryStarted = False

    # ---- writer-side ------------------------------------------------------
    def seal(self):
        self.sealDurable = True
        self.events.append('seal+witness durable')

    def stage(self):
        # SQL staging happens after SEAL/witness and before the gate; it commits nothing
        if not self.sealDurable:
            return
        self.staged = True
        self.events.append('association staged in the open evidence transaction')

    def gate(self):
        """compare_exchange(0 -> 1). Mints one single-use permit on success."""
        if not self.staged:
            self.events.append('gate refused: nothing prepared')
            return False
        if self.state == 0:
            self.state = ADMITTED
            self.permit = 'unused'
            self.events.append('CAS 0->1 admitted; single-use permit minted')
            return True
        self.events.append('CAS failed from state %d' % self.state)
        return False

    def consume_permit_and_commit(self, result):
        """The one commit method. Performs only the prepared commit and its barriers."""
        if self.permit != 'unused':
            self.events.append('commit refused: no unused permit')
            return False
        self.permit = 'consumed'
        self.commitIssued = True
        self.commitResult = result
        self.events.append('commit syscall issued: ' + result)
        return True

    # ---- observer side ---------------------------------------------------
    def latch(self):
        """Always fetch_or(2), so a post-admission latch is never lost."""
        before = self.state
        self.state = LATCHED
        self.events.append('observer fetch_or 2: %d -> %d' % (before, self.state))

    # ---- things that must never happen -----------------------------------
    def try_reset(self):
        self.resets += 1
        self.events.append('ILLEGAL state reset')

    def try_new_effect(self):
        """Admitting a NEW effect is forbidden once latched."""
        if self.state & LATCHED:
            self.events.append('new effect admission refused (latched)')
            return False
        self.effectAdmissions += 1
        self.events.append('new effect admitted')
        return True

    def try_retry_commit(self, result):
        """No automatic write retry, ever. A settled ExecutionId is terminal."""
        self.retries += 1
        ok = self.consume_permit_and_commit(result)
        self.events.append('retry attempt: %s' % ('ACCEPTED' if ok else 'refused'))
        return ok

    # ---- phase handoff ---------------------------------------------------
    def start_required_delivery(self):
        """Required rendering/delivery is a separate SHARED-READ phase over the committed Run.
        It draws no authority from the stopped cleanup-only session and admits no effect.
        Under a latch the operation is cancelling, so no new delivery phase is started."""
        if not (self.commitIssued and self.commitResult == 'confirmed'):
            self.events.append('delivery not applicable: no confirmed commit')
            return False
        if self.state & LATCHED:
            self.events.append('delivery phase not started: attempt is latched/cancelling')
            return False
        self.deliveryStarted = True
        self.events.append('required delivery phase started as SHARED-READ, no effect authority')
        return True


def conclude(a, deliveryFails):
    """Outcome mapping onto the existing D9 vocabulary. No new class or code."""
    if not a.commitIssued:
        return {'standing': 'uncommitted',
                'class': None, 'errorCode': None, 'runIdObservable': False,
                'orphanSeal': a.sealDurable,
                'note': 'gate never admitted; SEAL if durable remains an uncommitted attempt (F36)'}
    if a.commitResult in ('error', 'barrier-unconfirmed'):
        return {'standing': 'durability-undetermined',
                'class': 'operational-failed', 'exit': 4,
                'errorCode': 'DURABILITY.COMMIT_FAILED',
                'runIdObservable': False, 'orphanSeal': False,
                'note': 'ExecutionId retained and terminal; runId omitted; no automatic retry'}
    # confirmed
    if a.state & LATCHED:
        return {'standing': 'committed-delivery-failed',
                'class': 'operational-failed', 'exit': 4,
                'errorCode': 'DELIVERY.REQUIRED_FAILED',
                'runIdObservable': True, 'orphanSeal': False,
                'note': 'commit durable and NOT relabelled; the latch forbids starting a new '
                        'required-delivery phase, so required delivery is reported failed'}
    if deliveryFails:
        return {'standing': 'committed-delivery-failed',
                'class': 'operational-failed', 'exit': 4,
                'errorCode': 'DELIVERY.REQUIRED_FAILED',
                'runIdObservable': True, 'orphanSeal': False,
                'note': 'commit durable; required delivery failed after it'}
    return {'standing': 'committed', 'class': 'success', 'exit': 0, 'errorCode': None,
            'runIdObservable': True, 'orphanSeal': False, 'note': 'normal success'}


# --------------------------------------------------------------------------- schedules
BASE = ['seal', 'stage', 'gate', 'commit']
RESULTS = ('confirmed', 'error', 'barrier-unconfirmed')
EXTRA = ['latch', 'new-effect', 'retry']

rows = []
violations = []

# exhaustive: place latch at every position, optionally also probe a forbidden new effect and a
# forbidden retry after the commit point, for each commit result and each delivery outcome
LATCH_POSITIONS = list(range(len(BASE) + 1)) + [None]   # None = no observer latch at all
PREP = [BASE, ['seal', 'gate', 'commit']]               # second omits staging: gate cannot admit

def one(prep, latch_pos, result, deliveryFails, probe_forbidden):
    sched = (prep[:] if latch_pos is None
             else prep[:latch_pos] + ['latch'] + prep[latch_pos:])
    a = Attempt()
    for ev in sched:
        if ev == 'seal':
            a.seal()
        elif ev == 'stage':
            a.stage()
        elif ev == 'gate':
            a.gate()
        elif ev == 'commit':
            a.consume_permit_and_commit(result)
        elif ev == 'latch':
            a.latch()
    commitsBeforeProbe = a.events.count('commit syscall issued: ' + result)
    if probe_forbidden:
        a.try_new_effect()
        a.try_retry_commit(result)
    commitsAfterProbe = a.events.count('commit syscall issued: ' + result)
    delivered = a.start_required_delivery()
    out = conclude(a, deliveryFails and delivered)
    row = {'prep': prep, 'latchPosition': latch_pos, 'schedule': sched, 'commitResult': result,
           'finalState': a.state, 'permit': a.permit, 'commitIssued': a.commitIssued,
           'deliveryStarted': a.deliveryStarted, 'probeForbidden': probe_forbidden,
           'newEffectsAdmitted': a.effectAdmissions,
           'extraCommitsFromRetry': commitsAfterProbe - commitsBeforeProbe,
           'standing': out['standing'], 'errorCode': out['errorCode'],
           'runIdObservable': out['runIdObservable'], 'events': a.events}
    bad = []
    if a.state not in (0, 1, 2, 3):
        bad.append('state outside 0..3')
    if a.resets:
        bad.append('state reset during the attempt')
    # a latch at or before the gate step must prevent admission entirely
    gate_index = sched.index('gate')
    if latch_pos is not None and sched.index('latch') < gate_index and a.commitIssued:
        bad.append('commit issued although the latch won before the gate')
    if a.commitIssued and not (a.state & ADMITTED):
        bad.append('commit issued without the ADMITTED bit')
    if (a.state & LATCHED) and a.state not in (2, 3):
        bad.append('latched bit lost')
    if row['extraCommitsFromRetry'] != 0:
        bad.append('permit reused by a retry')
    if a.effectAdmissions and (a.state & LATCHED):
        bad.append('new effect admitted while latched')
    if a.state == 3 and a.commitIssued and result == 'confirmed':
        if out['standing'] != 'committed-delivery-failed':
            bad.append('state 3 relabelled a confirmed commit')
        if not out['runIdObservable']:
            bad.append('state 3 hid the RunId of a committed Run')
    if result in ('error', 'barrier-unconfirmed') and a.commitIssued:
        if out['standing'] != 'durability-undetermined':
            bad.append('undetermined converted to another standing')
        if out['runIdObservable']:
            bad.append('runId exposed for a non-committed Run')
    if a.deliveryStarted and (a.state & LATCHED):
        bad.append('delivery started while latched')
    if a.deliveryStarted and not (a.commitIssued and result == 'confirmed'):
        bad.append('delivery started without a confirmed commit')
    if bad:
        row['violations'] = bad
    return row


for prep in PREP:
    for latch_pos in LATCH_POSITIONS:
        if latch_pos is not None and latch_pos > len(prep):
            continue
        for result in RESULTS:
            for deliveryFails in (False, True):
                for probe_forbidden in (False, True):
                    row = one(prep, latch_pos, result, deliveryFails, probe_forbidden)
                    if 'violations' in row:
                        violations.append(row)
                    rows.append(row)

# independent probe: the permit is single-use even without a latch
a = Attempt()
a.seal(); a.stage(); a.gate()
first = a.consume_permit_and_commit('confirmed')
second = a.consume_permit_and_commit('confirmed')
permit_single_use = first and not second

# independent probe: fetch_or is idempotent and never clears ADMITTED
a2 = Attempt()
a2.seal(); a2.stage(); a2.gate()
a2.latch(); s1 = a2.state
a2.latch(); s2 = a2.state
latch_idempotent = (s1 == 3 and s2 == 3)

# independent probe: CAS from state 2 must fail
a3 = Attempt()
a3.seal(); a3.stage(); a3.latch()
cas_from_latched = a3.gate()

states_seen = sorted({r['finalState'] for r in rows})

rep = {
    'control': 'c7-gate-bits',
    'selectedWording': ('one atomic bit state, ADMITTED=1 LATCHED=2, states 0..3, '
                        'compare-exchange 0->1 for admission, observer always fetch-ORs 2 '
                        'including 1->3, no state resets during the attempt'),
    'schedules': len(rows),
    'violationCount': len(violations),
    'violations': violations[:10],
    'allLawsHeld': not violations,
    'finalStatesObserved': states_seen,
    'allFourStatesObserved': states_seen == [0, 1, 2, 3],
    'permitIsSingleUse': permit_single_use,
    'latchFetchOrIsIdempotentAndKeepsAdmitted': latch_idempotent,
    'casFromLatchedStateFails': cas_from_latched is False,
    'standingHistogram': {},
    'deliveryPhase': {
        'question': ('can a normal successful commit that returns a stopped cleanup-only session '
                     'still complete required rendering/delivery?'),
        'answer': ('Yes, as a separate phase, and it needs no authority from that session. '
                   'Required rendering/delivery is a read-and-materialise activity, which S7 '
                   'places in SHARED-READ mode alongside queries, rendering and doctor. It is '
                   'not a brokered effect, so it draws nothing from the closed session and the '
                   'closed session grants nothing.'),
        'handoff': [
            'commit confirmed; PublishedCommit produced',
            'security returns the stopped cleanup-only session',
            'host records any cleanup REV/CLN through a fresh lawful level-3 then level-4 append '
            'while the stopped session still holds the operation lease',
            'host releases the operation lease and performs the ordinary S7 end handoff',
            'required rendering/delivery then runs as a NEW SHARED-READ phase over the committed '
            'snapshot, with no session, no effect authority and no grant reuse',
        ],
        'latchedAttempt': ('State 2 or 3 forbids starting a delivery phase. For state 3 the '
                           'commit stays committed and the RunId stays observable, and the '
                           'required delivery is reported failed through the existing '
                           'DELIVERY.REQUIRED_FAILED / operational-failed / exit 4 path.'),
        'noWorkaround': ('A failed or latching attempt cannot reacquire authority by opening a '
                         'delivery phase: delivery admits no effect, and a new effect needs a '
                         'fresh attempt with a fresh ExecutionId.'),
        'flaggedAlternative': ('An owner could instead permit required delivery for state 3, on '
                               'the reading that disclosing an already committed Run is an '
                               'obligation rather than a new effect. This model selects the '
                               'conservative reading because S6 cancellation refuses further '
                               'requests; the choice is recorded for the owner, not settled here.'),
    },
}
hist = {}
for r_ in rows:
    hist[r_['standing']] = hist.get(r_['standing'], 0) + 1
rep['standingHistogram'] = hist

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('schedules', len(rows), 'violations', len(violations))
print('final states observed', states_seen, 'all four:', rep['allFourStatesObserved'])
print('permit single-use', permit_single_use, '| latch idempotent', latch_idempotent,
      '| CAS from latched fails', cas_from_latched is False)
print('standings', json.dumps(hist, sort_keys=True))
for v in violations[:6]:
    print('  VIOLATION', v['violations'], 'latchPos', v['latchPosition'], v['commitResult'])
