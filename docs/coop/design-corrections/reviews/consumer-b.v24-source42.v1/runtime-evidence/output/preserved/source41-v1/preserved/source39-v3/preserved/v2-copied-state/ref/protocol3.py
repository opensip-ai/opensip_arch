"""Host-side Rust protocol major-3 transition interpreter.

Normative sources: docs/coop/design-corrections/native/protocol3-transitions.v1.json (rows, order,
guards, wildcards, pre-match/no-match laws, state updates, stage-dependent transition, terminal
law) READ AT RUNTIME, and native-evidence.md section 9.1 (identity token set, exact Hello/HelloAck
echo) and section 10 (terminal authority and D9 mapping). The table is not copied into this file.
"""
import copy
import json

KIT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/subject/docs/'
TABLE_PATH = KIT + 'coop/design-corrections/native/protocol3-transitions.v1.json'

# native-evidence.md section 9.1: the four identity tokens.
IDENTITY_TOKENS = ["source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"]
IDENTITY_VERSIONS = {"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}


def load_table():
    with open(TABLE_PATH, 'rb') as fh:
        return json.loads(fh.read())


class Protocol3:
    def __init__(self, table=None):
        self.t = table or load_table()
        self.rules = self.t['rules']
        self.pre_complete = set(self.t['wildcards']['*PRE_COMPLETE']['phases'])
        self.process_fault = set(self.t['wildcards']['*PROCESS_FAULT']['frames'])
        # derivation check: *PRE_COMPLETE == phases[1:17]
        assert self.t['wildcards']['*PRE_COMPLETE']['phases'] == self.t['phases'][1:17]
        assert len(self.rules) == self.t['ruleCount'] == 34

    def run(self, events, hello=None):
        state = copy.copy(self.t['initialState'])
        trace = []
        hello_frame = None
        for ev in events:
            frame = ev['frame']
            # preMatchLaw, in listed order
            if state['phase'] == 'FAULT':
                trace.append({'frame': frame, 'rule': 'FAULT-absorb', 'phase': 'FAULT'})
                continue
            if state['phase'] in ('WAIT_ZERO_EXIT', 'WAIT_EOF', 'DONE') and frame not in (
                    'zero-exit', 'eof') and frame not in self.process_fault:
                state['phase'] = 'FAULT'
                trace.append({'frame': frame, 'rule': 'post-terminal-frame', 'phase': 'FAULT'})
                continue
            if frame in self.process_fault:
                state['phase'] = 'FAULT'
                trace.append({'frame': frame, 'rule': 'P3-33', 'phase': 'FAULT'})
                continue
            # section 9.1 step 2: exact echo of Hello tokens and identity versions (prose-owned
            # payload validation; a mismatch is FAULT before any source byte).
            if frame == 'Hello':
                hello_frame = ev
            if frame == 'HelloAck' and hello_frame is not None:
                if (ev.get('capabilities') != hello_frame.get('expectedCapabilities')
                        or ev.get('identityVersions') != hello_frame.get('identityVersions')):
                    state['phase'] = 'FAULT'
                    trace.append({'frame': frame, 'rule': 'payload:hello-ack-echo-mismatch(s9.1-step2)',
                                  'phase': 'FAULT'})
                    continue
            row = self._match(state, frame)
            if row is None:
                state['phase'] = 'FAULT'
                trace.append({'frame': frame, 'rule': 'P3-34', 'phase': 'FAULT'})
                continue
            self._updates(state, ev)
            nxt = row['next']
            if nxt == 'ANALYZING_OR_READY_COMPLETE':
                state['stageIndex'] += 1
                state['stagesCompleted'] += 1
                nxt = 'READY_COMPLETE' if state['stageIndex'] == state['stageCount'] else 'ANALYZING'
            if 'terminal' in row:
                state['terminalKind'] = row['terminal']
            state['phase'] = nxt
            trace.append({'frame': frame, 'rule': row['id'], 'phase': nxt})
        return {'state': state, 'trace': trace}

    def _match(self, state, frame):
        for row in self.rules:
            if row['phase'] == '*ANY':
                continue
            if row['phase'] == '*PRE_COMPLETE':
                if state['phase'] not in self.pre_complete:
                    continue
            elif row['phase'] != state['phase']:
                continue
            if row['frame'] != frame:
                continue
            if all(state.get(k) == v for k, v in row.get('guard', {}).items()):
                return row
        return None

    def _updates(self, state, ev):
        frame = ev['frame']
        if frame == 'HelloAck':
            caps = ev.get('capabilities') or []
            state['identityNegotiated'] = all(tok in caps for tok in IDENTITY_TOKENS)
        if frame == 'OpenUniverse':
            state['dependencyMode'] = bool(ev.get('dependencyMode'))
            state['preparedMode'] = bool(ev.get('preparedMode'))
        if frame == 'Analyze':
            state['stageCount'] = ev['stageCount']
            state['stageIndex'] = 0
        if frame in ('DependencySourceChunk', 'DependencySourceManifest', 'OpenUniverse',
                     'PreparedOutputChunk', 'PreparedOutputManifest', 'SnapshotFileChunk', 'SnapshotManifest'):
            state['sourceBytesSent'] = True

    def pairwise_disjoint(self):
        """Control: no two non-wildcard rows can match one (phase, frame, state)."""
        overlaps = []
        rows = [r for r in self.rules if r['phase'] != '*ANY']
        for i, a in enumerate(rows):
            for b in rows[i + 1:]:
                pa = self.pre_complete if a['phase'] == '*PRE_COMPLETE' else {a['phase']}
                pb = self.pre_complete if b['phase'] == '*PRE_COMPLETE' else {b['phase']}
                if not (pa & pb) or a['frame'] != b['frame']:
                    continue
                ga, gb = a.get('guard', {}), b.get('guard', {})
                if any(k in gb and gb[k] != v for k, v in ga.items()):
                    continue
                overlaps.append((a['id'], b['id']))
        return overlaps


# native-evidence.md section 10 fault law / StageAuthorityV1 projection of a terminal kind.
def stage_authority(terminal_kind, faulted):
    if faulted:
        return {"terminalKind": "fault", "factsAdmitted": "none", "coverageEntriesAdmitted": False,
                "runMayBeSealed": False, "authority": "none", "diagnosticsCarrier": "operational-record-only",
                "d9": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION"}}
    if terminal_kind == 'complete':
        return {"terminalKind": "complete", "factsAdmitted": "all", "coverageEntriesAdmitted": True,
                "runMayBeSealed": True, "authority": "authoritative", "diagnosticsCarrier": "operational-record-only",
                "d9": {"class": "success", "exitCode": 0, "code": None}}
    if terminal_kind in ('unavailable', 'budget-exhausted'):
        code = 'COVERAGE.PROVIDER_UNAVAILABLE' if terminal_kind == 'unavailable' else 'COVERAGE.BUDGET_EXHAUSTED'
        return {"terminalKind": terminal_kind, "factsAdmitted": "before-terminal", "coverageEntriesAdmitted": True,
                "runMayBeSealed": True, "authority": "authoritative", "diagnosticsCarrier": "operational-record-only",
                "d9": {"class": "indeterminate", "exitCode": 3, "code": code}}
    if terminal_kind == 'cancelled':
        return {"terminalKind": "cancelled", "factsAdmitted": "none", "coverageEntriesAdmitted": False,
                "runMayBeSealed": False, "authority": "none", "diagnosticsCarrier": "operational-record-only",
                "d9": {"class": "interrupted", "exitCode": 130, "code": None}}
    if terminal_kind == 'provider-fault':
        return {"terminalKind": "provider-fault", "factsAdmitted": "none", "coverageEntriesAdmitted": False,
                "runMayBeSealed": False, "authority": "none", "diagnosticsCarrier": "operational-record-only",
                "d9": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION"}}
    raise ValueError(terminal_kind)
