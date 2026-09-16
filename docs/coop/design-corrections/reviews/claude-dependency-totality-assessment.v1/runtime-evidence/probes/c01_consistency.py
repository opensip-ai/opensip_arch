"""C01 — MD vs JSON vs receipts consistency for this bounded assessment; records final digests."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
J = json.load(open(os.path.join(BASE, 'review.json')))
MD = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
C, bad = {}, []


def chk(name, cond):
    C[name] = bool(cond)
    print('%-80s %s' % (name, 'OK' if cond else 'FAIL'))
    if not cond:
        bad.append(name)


d = J['dependencyTotality']
chk('decision states required + reference defect', d['decision'].startswith('REQUIRED BY CURRENT LAW') and 'REFERENCE DEFECT' in d['decision'])
chk('law derivations written before their probes ran', all(v['writtenBeforeProbeRan'] for v in J['lawDerivedBeforeTesting'].values()))
m = d['measured']['incomingTwoSubjectPrimary']
for case in ('partial-f-only', 'partial-g-scope-wrong-universe', 'partial-g-scope-without-coverage'):
    chk('md/json: %s true on 35+successor, unknown on remedy' % case,
        m[case]['frozen35'] == m[case]['successor'] == 'true' and m[case]['remedy'] == 'indeterminate')
chk('disjoint lawful true everywhere', set(m['disjoint-two-scopes'].values()) == {'true'})
att = d['measured']['attestationView']['attestation-two-subjects/calls-f-only']
chk('attestation partial: true on A, unknown on A+B', att['remedyA'] == 'true' and att['remedyA+B'] == 'indeterminate')
chk('check-atoms 95/95 under A and A+B', d['measured']['checkAtomsRegression']['successor95WithRemedyA']['cases'] == 95
    and not d['measured']['checkAtomsRegression']['successor95WithRemedyA']['failed']
    and not d['measured']['checkAtomsRegression']['successor95WithRemedyAplusB']['failed'])
cc = d['smallestRemedy']['crossOwnerEffects']['consumerCheckers']
chk('consumer checkers: all exit 0; only execution-inputs path strings differ',
    all(v['bothExitZero'] for v in cc['comparison'].values()) and all(p.endswith('].path') for p in cc['executionInputsDiffPaths']))
chk('reachability table does not claim a full Run', 'NOT CONSTRUCTED' in d['reachabilityByStanding']['closedEnumerationOrRetainedRun'])
chk('history + runtime corrections recorded', J['textConsistency']['historySubjectOrder']['decision'].startswith('ROOT PROPOSAL ALIGNS')
    and J['textConsistency']['importQuantifiersRuntimeProse']['decision'].startswith('ROOT PROPOSAL ALIGNS'))
chk('grants nothing', not any(J['grantsNothing'].values()))
for tok in ('Totality over every current source subject is required by current law', 'reference defect', 'RC-4', 'remedy A', 'Variant **B**',
            '95/95', 'All 8 atom-model consumer checkers', 'ownedHashes[*].path', 'Not constructed', 'historySubjectOrder', 'targetSubjectProjection',
            'admitted but matches nothing', '**not** source36 acceptance'):
    chk('md states %r' % tok, tok in MD)
for rel, dg in J['receipts'].items():
    if sha(os.path.join(BASE, rel)) != dg:
        chk('receipt digest %s' % rel, False)
C['reviewJsonSha256'] = sha(os.path.join(BASE, 'review.json'))
C['reviewMdSha256'] = sha(os.path.join(BASE, 'review.md'))
C['failed'] = bad
json.dump(C, open(os.path.join(BASE, 'consistency.json'), 'w'), indent=1)
print('\nchecks %d failed %d | review.json %s | review.md %s' % (len([v for v in C.values() if isinstance(v, bool)]), len(bad), C['reviewJsonSha256'], C['reviewMdSha256']))
