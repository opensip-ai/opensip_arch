"""Independent controls for CX-V19-PROTOCOL-INITIALIZATION-PUBLICATION.

The discriminating test of "directly consumable from the public kit" is whether an INDEPENDENT
interpreter written from the PUBLISHED DOCUMENT ALONE reproduces the reference model's behaviour.
This file implements one, reading nothing from native_evidence_model except to compare.
Disposable copy only.
"""
import importlib.util, itertools, json, random, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC = ROOT / 'docs/coop/design-corrections'
DOC = json.loads((DC / 'native/protocol3-transitions.v1.json').read_text())

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

N = load('nem', DC / 'native/native_evidence_model.v2.py')

R = []
def ck(cid, desc, got, want):
    R.append({'id': cid, 'desc': desc, 'pass': got == want, 'observed': got, 'expected': want})

# ---------------------------------------------------------------- independent interpreter
PRE = set(DOC['wildcards']['*PRE_COMPLETE']['phases'])
FAULTS = set(DOC['wildcards']['*PROCESS_FAULT']['frames'])
IDENTITY_TOKENS = N.IDENTITY_TOKENS  # prose-owned per ownedByProse; not a transition

def indep_run(events, stage_count=1, rules=None):
    """Written ONLY from initializationAndUpdateOrder / matchLaw / preMatchLaw / noMatchLaw /
    guardLaw / stateUpdates / stageDependentTransitions / terminalLaw."""
    rules = DOC['rules'] if rules is None else rules
    st = dict(DOC['initialState'])
    trace = []
    for ev in events:
        phase, frame = st['phase'], ev['frame']
        # preMatchLaw, in published order
        if phase == 'FAULT':
            trace.append('FAULT-absorb'); continue
        if phase in ('WAIT_ZERO_EXIT', 'WAIT_EOF', 'DONE') and frame not in ('zero-exit', 'eof') and frame not in FAULTS:
            st['phase'] = 'FAULT'; trace.append('post-terminal-frame'); continue
        if frame in FAULTS:
            st['phase'] = 'FAULT'; trace.append('P3-33'); continue
        # matchLaw: first match wins, skipping *ANY rows (applied by the two laws above/below)
        matched = None
        for rule in rules:
            rp = rule['phase']
            if rp == '*ANY':
                continue
            if not (rp == phase or (rp == '*PRE_COMPLETE' and phase in PRE)):
                continue
            if rule['frame'] != frame:
                continue
            if all(st.get(k) == v for k, v in (rule.get('guard') or {}).items()):
                matched = rule; break
        if matched is None:
            st['phase'] = 'FAULT'; trace.append('P3-34'); continue
        # (1) stateUpdates of the incoming frame
        if frame == 'HelloAck':
            st['identityNegotiated'] = all(t in ev.get('capabilities', []) for t in IDENTITY_TOKENS)
        elif frame == 'OpenUniverse':
            st['dependencyMode'] = bool(ev.get('dependencyMode'))
            st['preparedMode'] = bool(ev.get('preparedMode'))
        elif frame == 'Analyze':
            st['stageCount'] = stage_count; st['stageIndex'] = 0
        for upd in DOC['stateUpdates']:
            if frame in (upd.get('onFrames') or ()):
                st['sourceBytesSent'] = True
        # (2) resolve next, incl. the stage-dependent transition
        nxt = matched['next']
        if nxt == 'ANALYZING_OR_READY_COMPLETE':
            st['stageIndex'] += 1; st['stagesCompleted'] += 1
            nxt = 'READY_COMPLETE' if st['stageIndex'] == st['stageCount'] else 'ANALYZING'
        # (3) terminalKind
        if 'terminal' in matched:
            st['terminalKind'] = matched['terminal']
        # (4) phase + trace
        st['phase'] = nxt; trace.append(matched['id'])
    # project into the model's published return shape (the return projection is a code concern;
    # the document is transitions only, per ownedByProse)
    return {'finalPhase': st['phase'], 'terminalKind': st['terminalKind'],
            'sourceBytesSent': st['sourceBytesSent'], 'stagesCompleted': st['stagesCompleted'],
            'identityNegotiated': st['identityNegotiated'], 'trace': trace}

# ---------------------------------------------------------------- structural controls
ck('D1:row-count', 'exactly 34 ordered rows', [len(DOC['rules']), DOC['ruleCount']], [34, 34])
ck('D1:ids-ordered', 'row ids are P3-01..P3-34 in declaration order',
   [r['id'] for r in DOC['rules']], ['P3-%02d' % i for i in range(1, 35)])
ck('D1:initial-nine', 'initialState publishes exactly nine fields',
   sorted(DOC['initialState']),
   sorted(['phase', 'dependencyMode', 'preparedMode', 'identityNegotiated', 'stageIndex',
           'stageCount', 'terminalKind', 'sourceBytesSent', 'stagesCompleted']))
ck('D1:phases', 'phase list has 22 entries and starts at START',
   [len(DOC['phases']), DOC['phases'][0]], [22, 'START'])

# --- consumption: the model IS the document, not a copy --------------------
ck('D2:rules-consumed', 'model PROTOCOL3_RULES equals published rows',
   N.PROTOCOL3_RULES, [dict(r) for r in DOC['rules']])
ck('D2:phases-consumed', 'model phases equal published phases', N.PROTOCOL3_PHASES, DOC['phases'])
ck('D2:precomplete-derivation', 'published *PRE_COMPLETE equals its published derivation phases[1:17]',
   DOC['wildcards']['*PRE_COMPLETE']['phases'], DOC['phases'][1:17])
ck('D2:precomplete-model', 'model _PRE_COMPLETE is the published list', N._PRE_COMPLETE, DOC['wildcards']['*PRE_COMPLETE']['phases'])
ck('D2:no-restated-rows', 'no P3-xx row literal remains in the model source',
   sum(1 for i in range(1, 35) if ('"id": "P3-%02d"' % i) in (DC / 'native/native_evidence_model.v2.py').read_text()), 0)

# --- pairwise disjointness (the claim first-match-wins currently rests on) --
def overlaps():
    out = []
    real = [r for r in DOC['rules'] if r['phase'] != '*ANY']
    for a, b in itertools.combinations(real, 2):
        if a['frame'] != b['frame']:
            continue
        pa = set(DOC['wildcards']['*PRE_COMPLETE']['phases']) if a['phase'] == '*PRE_COMPLETE' else {a['phase']}
        pb = set(DOC['wildcards']['*PRE_COMPLETE']['phases']) if b['phase'] == '*PRE_COMPLETE' else {b['phase']}
        if not (pa & pb):
            continue
        ga, gb = a.get('guard') or {}, b.get('guard') or {}
        if any(k in gb and ga[k] != gb[k] for k in ga):
            continue  # separated by mutually exclusive guards
        out.append((a['id'], b['id']))
    return out
ck('D3:disjoint', 'no two rows can match one (phase, frame, state)', overlaps(), [])

# ---------------------------------------------------------------- behavioural equivalence
def seqs():
    hello = {'frame': 'Hello'}
    ack_ok = {'frame': 'HelloAck', 'capabilities': list(IDENTITY_TOKENS)}
    ack_bad = {'frame': 'HelloAck', 'capabilities': []}
    ou = lambda d, p: {'frame': 'OpenUniverse', 'dependencyMode': d, 'preparedMode': p}
    base = [hello, ack_ok]
    S = []
    # complete happy paths across all four mode combinations
    for dep, prep in itertools.product([False, True], repeat=2):
        ev = base + [ou(dep, prep), {'frame': 'UniverseAccepted'}, {'frame': 'SnapshotManifest'},
                     {'frame': 'SnapshotFileChunk'}, {'frame': 'SnapshotSeal'},
                     {'frame': 'SnapshotAccepted'}]
        if dep:
            ev += [{'frame': 'DependencySourceManifest'}, {'frame': 'DependencySourceChunk'},
                   {'frame': 'DependencySourceSeal'}, {'frame': 'DependencySourceAccepted'}]
        if prep:
            ev += [{'frame': 'PreparedOutputManifest'}, {'frame': 'PreparedOutputChunk'},
                   {'frame': 'PreparedOutputSeal'}, {'frame': 'PreparedOutputAccepted'}]
        ev += [{'frame': 'NativeContextVerified'}, {'frame': 'Analyze'},
               {'frame': 'FactBatch'}, {'frame': 'CoverageV3'}, {'frame': 'Complete'},
               {'frame': 'zero-exit'}, {'frame': 'eof'}]
        S.append((ev, 1))
    # identity not negotiated -> OpenUniverse must not be admitted
    S.append((base[:1] + [ack_bad, ou(False, False)], 1))
    S.append(([ou(False, False)], 1))          # source frame before any negotiation
    # multi-stage CoverageV3 resolution
    for n in (1, 2, 3):
        ev = base + [ou(False, False), {'frame': 'UniverseAccepted'}, {'frame': 'SnapshotManifest'},
                     {'frame': 'SnapshotSeal'}, {'frame': 'SnapshotAccepted'},
                     {'frame': 'NativeContextVerified'}, {'frame': 'Analyze'}]
        ev += [{'frame': 'CoverageV3'}] * n + [{'frame': 'Complete'}, {'frame': 'zero-exit'}, {'frame': 'eof'}]
        S.append((ev, n))
        S.append((ev, n + 1))   # one stage short: Complete must not be admitted
    # every terminal kind
    for term in ('Unavailable', 'BudgetExhausted', 'ProviderFault', 'Cancel'):
        ev = base + [ou(False, False), {'frame': 'UniverseAccepted'}, {'frame': 'SnapshotManifest'},
                     {'frame': 'SnapshotSeal'}, {'frame': 'SnapshotAccepted'},
                     {'frame': 'NativeContextVerified'}, {'frame': 'Analyze'}, {'frame': term}]
        if term == 'Cancel':
            ev.append({'frame': 'Cancelled'})
        ev += [{'frame': 'zero-exit'}, {'frame': 'eof'}]
        S.append((ev, 1))
    # every process fault from an arbitrary mid-phase, and FAULT absorption
    for f in sorted(FAULTS):
        S.append((base + [{'frame': f}, {'frame': 'Hello'}, {'frame': 'eof'}], 1))
    # post-terminal frames
    S.append((base + [ou(False, False), {'frame': 'UniverseAccepted'}, {'frame': 'SnapshotManifest'},
                      {'frame': 'SnapshotSeal'}, {'frame': 'SnapshotAccepted'},
                      {'frame': 'NativeContextVerified'}, {'frame': 'Analyze'}, {'frame': 'Unavailable'},
                      {'frame': 'FactBatch'}], 1))
    # unknown frames and out-of-order frames
    S.append(([{'frame': 'NotAFrame'}], 1))
    S.append((base + [{'frame': 'Complete'}], 1))
    # fuzz over the published frame vocabulary
    vocab = sorted({r['frame'] for r in DOC['rules'] if not r['frame'].startswith('*')} | FAULTS |
                   {'zero-exit', 'eof', 'NotAFrame'})
    rnd = random.Random(20260907)
    for _ in range(400):
        n = rnd.randint(1, 12)
        S.append(([{'frame': rnd.choice(vocab), 'capabilities': list(IDENTITY_TOKENS),
                    'dependencyMode': rnd.choice([True, False]),
                    'preparedMode': rnd.choice([True, False])} for _ in range(n)],
                  rnd.randint(1, 3)))
    return S

CASES = seqs()
mismatch = []
for i, (ev, sc) in enumerate(CASES):
    a = N.protocol3_run([dict(e) for e in ev], sc)
    b = indep_run([dict(e) for e in ev], sc)
    if a != b:
        mismatch.append({'case': i, 'events': [e['frame'] for e in ev], 'stageCount': sc,
                         'model': a, 'independent': b})
ck('D4:equivalence', 'independent interpreter from the DOCUMENT ALONE matches the model on %d cases' % len(CASES),
   mismatch[:3], [])
ck('D4:case-count', 'behavioural cases executed', len(CASES) > 400, True)

# --- permutation control: disjointness means order cannot change outcomes ---
rnd = random.Random(7)
perm_mismatch = []
for k in range(25):
    perm = list(DOC['rules']); rnd.shuffle(perm)
    for ev, sc in CASES[:60]:
        if N.protocol3_run([dict(e) for e in ev], sc, [dict(r) for r in perm]) != N.protocol3_run([dict(e) for e in ev], sc):
            perm_mismatch.append(k); break
ck('D5:permutation', 'permuting the published rows preserves every outcome (disjointness holds)',
   perm_mismatch, [])

# --- no silently altered transition behaviour vs the PRE-v19 inline table ---
BEFORE = DC / 'reviews/codex-post-reset.v1/source-before-v19/docs/coop/design-corrections/native/native_evidence_model.v2.py'
before_src = BEFORE.read_text()
ns = {}
seg = before_src[before_src.index('PROTOCOL3_PHASES = ['):before_src.index('_PRE_COMPLETE = PROTOCOL3_PHASES')]
exec(seg, ns)
ck('D6:rows-identical', 'published rows are byte-equal to the pre-v19 inline rows',
   ns['PROTOCOL3_RULES'], [dict(r) for r in DOC['rules']])
ck('D6:phases-identical', 'published phases are identical to the pre-v19 inline phases',
   ns['PROTOCOL3_PHASES'], DOC['phases'])
ck('D6:precomplete-identical', 'pre-v19 phases[1:17] equals the published wildcard',
   ns['PROTOCOL3_PHASES'][1:17], DOC['wildcards']['*PRE_COMPLETE']['phases'])
ck('D6:faults-identical', 'process-fault frame set unchanged',
   sorted(FAULTS), sorted({'nonzero-exit', 'signal-death', 'deadline', 'stdout-byte'}))
# the pre-v19 _SOURCE_FRAMES literal vs the value now DERIVED from stateUpdates
before_sf = {'OpenUniverse', 'SnapshotManifest', 'SnapshotFileChunk', 'DependencySourceManifest',
             'DependencySourceChunk', 'PreparedOutputManifest', 'PreparedOutputChunk'}
ck('D6:source-frames-identical', 'derived _SOURCE_FRAMES equals the pre-v19 literal set',
   sorted(N._SOURCE_FRAMES), sorted(before_sf))

# --- the document is self-contained for a kit reader -----------------------
ck('D7:same-class-as-kit', 'the table is a .json artifact in native/, the class the blind kit already carries',
   [(DC / 'native/protocol3-transitions.v1.json').suffix,
    sorted(p.suffix for p in (ROOT / 'docs/coop/design-corrections/reviews/consumer-b.v7/subject/docs/coop/design-corrections/native').iterdir())],
   ['.json', ['.json', '.json', '.json']])
ck('D7:declares-consumer', 'the document names its consumer', 'native_evidence_model.v2.py' in DOC['consumedBy'], True)
ck('D7:declares-prose-owned', 'the document declares what it does NOT own', len(DOC['ownedByProse']) >= 5, True)

fails = [r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-d.json').write_text(
    json.dumps({'controls': len(R), 'failed': len(fails), 'behaviouralCases': len(CASES),
                'failures': fails, 'results': R}, indent=1))
print('CTRL-D controls=%d failed=%d behaviouralCases=%d' % (len(R), len(fails), len(CASES)))
for f in fails:
    print('  FAIL', f['id'], f['desc'], '\n   observed=', repr(f['observed'])[:500],
          '\n   expected=', repr(f['expected'])[:500])
