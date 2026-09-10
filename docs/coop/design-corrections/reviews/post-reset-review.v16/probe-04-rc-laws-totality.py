#!/usr/bin/env python3
"""Probe 04 (independent): RC-0/RC-1/RC-2 applicability over ALL registered
(relation, rung) pairs, plus unknown-pair fallback controls and the CX-BV5-09
state-specific class law.

Expected outcomes are authored in this file BEFORE reading any coauthor probe
result, and are derived from the published contract text (native-evidence 4.3),
not from the reference implementation's behaviour.

Run against copy-B-probes (disposable full exact copy).
"""
import hashlib, importlib.util, itertools, json, os, sys

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

NPATH = os.path.join(DC, 'native/native_evidence_model.v2.py')
N = load('rev16_native', NPATH)

BOUND = {
    'native_evidence_model.v2.py': sha256(NPATH),
    'identity-model.py': sha256(os.path.join(DC, 'foundation/identity-model.py')),
    'native-evidence.schemas.v2.json': sha256(os.path.join(DC, 'native/native-evidence.schemas.v2.json')),
    'capability-manifest-domains.v2.json': sha256(os.path.join(DC, 'native/capability-manifest-domains.v2.json')),
    'relation-payload-schemas.v2.json': sha256(os.path.join(DC, 'foundation/relation-payload-schemas.v2.json')),
}

LADDERS = N.LADDERS
RESOLVED = N.RESOLVED_RUNGS
registered = sorted((rel, rung) for rel, l in LADDERS.items() for rung in l)
all_rungs = sorted({r for l in LADDERS.values() for r in l})

# ---- my independent expectation, straight from the published RC-1/RC-0 text ----
def expected(rel, rung, rc):
    """True == the contract says this entry is admissible (no faults)."""
    if (rel, rung) not in registered:
        return False, 'RC-0 unregistered pair'
    if rc['state'] not in N.RC_STATES:
        return False, 'RC-0 state outside enum'
    if rung not in RESOLVED:
        ok = (rc['state'] == 'not-applicable' and rc['unresolvedEdgeCount'] == 0
              and rc.get('attempted') is False and not rc.get('unresolvedEdgeClasses'))
        return ok, 'RC-1 not-applicable minting law'
    if rc['state'] == 'not-applicable':
        return False, 'RC-1 resolved rung must not claim not-applicable'
    return None, 'RC-2 (fact-relative; assessed separately)'

def na(**over):
    d = {'state': 'not-applicable', 'attempted': False, 'unresolvedEdgeCount': 0,
         'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True}
    d.update(over)
    return d

def entry(rel, rung, rc, examined=('a.ts',)):
    return {'relation': rel, 'resolution': rung, 'resolutionCompleteness': rc,
            'examinedSubjects': list(examined)}

rows = []
def case(cid, group, rel, rung, rc, facts, exp_admit, why, examined=('a.ts',)):
    faults = N.coverage_bijection([entry(rel, rung, rc, examined)], list(facts))
    got = (faults == [])
    rows.append({'id': cid, 'group': group, 'pair': f'{rel}@{rung}',
                 'completeness': rc, 'unresolvedFacts': list(facts),
                 'expectedAdmit': exp_admit, 'observedAdmit': got,
                 'agrees': got == exp_admit, 'faults': faults, 'why': why})

# --- A. RC-1 totality: every registered pair, minted per the published law ---
for rel, rung in registered:
    if rung in RESOLVED:
        rc = {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
              'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True}
        case(f'A-resolved-{rel}@{rung}', 'RC-1 totality: resolved rung admits a non-NA state',
             rel, rung, rc, [], True, 'resolved rung, RC-2 complete with zero facts')
        case(f'A-resolved-NA-{rel}@{rung}', 'RC-1 totality: resolved rung refuses not-applicable',
             rel, rung, na(), [], False, 'RC-1: a resolved rung must never claim not-applicable')
    else:
        case(f'A-na-{rel}@{rung}', 'RC-1 totality: non-resolved rung admits the minted NA record',
             rel, rung, na(), [], True, 'RC-1 minting law satisfied')
        case(f'A-na-attempted-{rel}@{rung}', 'RC-1 totality: attempted=true refused on every NA pair',
             rel, rung, na(attempted=True), [], False, 'RC-1: NA makes no resolution claim')
        case(f'A-na-classes-{rel}@{rung}', 'RC-1 totality: nonempty class set refused on every NA pair',
             rel, rung, na(unresolvedEdgeClasses=['computed-member-access']), [], False,
             'RC-1: NA class list must be empty')
        case(f'A-na-complete-{rel}@{rung}', 'RC-1 totality: complete refused on every NA pair',
             rel, rung, {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
                         'unresolvedEdgeClasses': [], 'stageTerminal': 'complete',
                         'examinedExhaustive': True}, [], False,
             'RC-1: non-resolved rung must be not-applicable')

# --- B. unknown pairs cannot become not-applicable by fallback ---
for rel, rung in itertools.product(sorted(LADDERS), all_rungs):
    if (rel, rung) in registered:
        continue
    rows_before = len(rows)
    case(f'B-unknown-{rel}@{rung}', 'RC-0: unregistered pair is refused, never NA by fallback',
         rel, rung, na(), [], False,
         'RC-0 runs first; not-applicable is a claim about a REGISTERED pair only')

# --- C. free fields on not-applicable (must stay free) ---
for st in ('complete', 'budget-exhausted', 'unavailable', 'provider-fault', 'cancelled', 'crash', None):
    case(f'C-stage-{st}', 'RC-1: stageTerminal stays FREE on not-applicable',
         'unresolved-edge', 'observed', na(stageTerminal=st), [], True,
         'published: stageTerminal deliberately not constrained by RC-1')
for ex in (True, False):
    case(f'C-examined-{ex}', 'RC-1: examinedExhaustive stays INDEPENDENT on not-applicable',
         'unresolved-edge', 'observed', na(examinedExhaustive=ex), [], True,
         'published: examinedExhaustive remains the independent 4.1 partition claim')

# --- D. CX-BV5-09 state-specific class law on RESOLVED rungs ---
REL, RUNG = 'imports', 'resolved-target'
complete_ok = {'state': 'complete', 'attempted': True, 'unresolvedEdgeCount': 0,
               'unresolvedEdgeClasses': [], 'stageTerminal': 'complete', 'examinedExhaustive': True}
case('D-complete-clean', 'CX-BV5-09 valid control', REL, RUNG, complete_ok, [], True,
     'zero facts, zero count, empty class list')
case('D-complete-classes', 'CX-BV5-09: complete + zero count + nonempty classes REFUSED',
     REL, RUNG, dict(complete_ok, unresolvedEdgeClasses=['computed-member-access']), [], False,
     'a resolved COMPLETE record with zero unresolved facts/count cannot retain a nonempty class set')
na_att = {'state': 'not-attempted', 'attempted': False, 'unresolvedEdgeCount': 0,
          'unresolvedEdgeClasses': [], 'stageTerminal': 'unavailable', 'examinedExhaustive': False}
case('D-notattempted-clean', 'CX-BV5-09 valid control (not-attempted)', REL, RUNG, na_att, [], True,
     'skipped stage observed nothing')
case('D-notattempted-classes', 'CX-BV5-09: not-attempted + nonempty classes REFUSED',
     REL, RUNG, dict(na_att, unresolvedEdgeClasses=['dynamic-import-expression']), [], False,
     'a skipped stage observed nothing, so it can report no class')

# --- E. incomplete / partial PRESERVED (must still carry their honest classes) ---
F1 = {'relation': 'imports', 'referrer': 'a.ts', 'edgeKind': 'computed-member-access'}
F2 = {'relation': 'imports', 'referrer': 'a.ts', 'edgeKind': 'dynamic-import-expression'}
inc = {'state': 'incomplete', 'attempted': True, 'unresolvedEdgeCount': 2,
       'unresolvedEdgeClasses': ['computed-member-access', 'dynamic-import-expression'],
       'stageTerminal': 'complete', 'examinedExhaustive': True}
case('E-incomplete-honest', 'RC-2 preserved: honest incomplete keeps its classes',
     REL, RUNG, inc, [F1, F2], True, 'exact count and class equality against admitted facts')
case('E-incomplete-classmismatch', 'RC-2 preserved: incomplete class mismatch still refuses',
     REL, RUNG, dict(inc, unresolvedEdgeClasses=['computed-member-access']), [F1, F2], False,
     'incomplete requires exact class equality')
par = {'state': 'partial', 'attempted': True, 'unresolvedEdgeCount': 1,
       'unresolvedEdgeClasses': ['computed-member-access'], 'stageTerminal': 'budget-exhausted',
       'examinedExhaustive': False}
case('E-partial-honest', 'RC-2 preserved: honest partial keeps its classes',
     REL, RUNG, par, [F1], True, 'partial carries its observed class')
case('E-incomplete-zero-edges', 'RC-2 preserved: incomplete needs >=1 edge',
     REL, RUNG, dict(inc, unresolvedEdgeCount=0, unresolvedEdgeClasses=[]), [], False,
     'incomplete with zero edges must be partial/complete instead')
case('E-complete-with-facts', 'RC-2 preserved: complete with admitted facts refuses',
     REL, RUNG, complete_ok, [F1], False, 'a zero count never implies complete')

# --- F. RC-4 derived relation: reachability counts calls edges ---
FC = {'relation': 'calls', 'referrer': 'a.ts', 'edgeKind': 'computed-member-access'}
case('F-reachability-inherits-calls', 'RC-4 preserved: reachability counts calls edges',
     'reachability', 'from-resolved-calls',
     {'state': 'incomplete', 'attempted': True, 'unresolvedEdgeCount': 1,
      'unresolvedEdgeClasses': ['computed-member-access'], 'stageTerminal': 'complete',
      'examinedExhaustive': True}, [FC], True, 'reachability inherits the calls edge')

# --- G. fact-free entry with a bad pair is judged the same way ---
case('G-factfree-badpair', 'CX-BV5-08: a FACT-FREE entry over an empty examined scope is judged the same',
     'unresolved-edge', 'enumerated', na(), [], False,
     'RC-0 is independent of unresolved_facts', examined=())
case('G-factfree-goodpair', 'CX-BV5-08 control: fact-free VALID pair still admits',
     'unresolved-edge', 'observed', na(), [], True, 'valid observed control', examined=())

# --- H. subject_scope_descriptor mint-time pair check ---
mint_rows = []
for rel, rung, exp in [('unresolved-edge', 'observed', True),
                       ('unresolved-edge', 'enumerated', False),
                       ('declares', 'resolved-callee', False),
                       ('reachability', 'from-resolved-calls', True),
                       ('file', 'enumerated', True),
                       ('file', 'observed', False)]:
    try:
        N.subject_scope_descriptor('sha256:' + '0' * 64, rel, rung, 'sha256:' + '1' * 64,
                                   'sha256:' + '1' * 64, 'closure2:' + '2' * 64, ['a.ts'])
        got, err = True, None
    except Exception as e:
        got, err = False, type(e).__name__ + ':' + str(e)[:200]
    mint_rows.append({'pair': f'{rel}@{rung}', 'expectedMint': exp, 'observedMint': got,
                      'agrees': got == exp, 'error': err})

summary = {
    'probe': 'probe-04-rc-laws-totality',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': BOUND,
    'registeredPairCount': len(registered),
    'registeredPairs': [f'{a}@{b}' for a, b in registered],
    'resolvedRungs': sorted(RESOLVED),
    'distinctRungVocabulary': all_rungs,
    'unregisteredPairsTested': sum(1 for r in rows if r['group'].startswith('RC-0: unregistered')),
    'cases': len(rows),
    'agree': sum(1 for r in rows if r['agrees']),
    'disagree': [r for r in rows if not r['agrees']],
    'mintCases': mint_rows,
    'mintAgree': sum(1 for r in mint_rows if r['agrees']),
    'rows': rows,
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-04-rc-laws-totality.result.json'), 'w') as f:
    json.dump(summary, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in summary.items() if k not in ('rows', 'registeredPairs')},
                 indent=2, sort_keys=True)[:4000])
