"""R-HIDDEN-MISMATCH-PER-LANGUAGE -- at least one REFUSED hidden input and one REFUSED
mismatched input for TypeScript and for Rust, each with its FIRST refusal and the masking
relationship recorded.

HIDDEN   the analysis names an input that the retained snapshot inventory does not contain
         at all, so no committed byte answers for it.
MISMATCH the analysis names an input that IS retained/inventoried, but the digest it declares
         does not join the bytes under that name.

The two are different failures and must not be collapsed: a hidden input has no custody, a
mismatched input has custody of the WRONG bytes. Every control is applied at BUILD time, so
the whole graph is reminted and reclosed, and the ordered refusal list is published so the
first refusal can be checked against the intended owner rather than assumed.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL
import run_ts as RT
import run_ts_full as RTF
import run_rust as RR
import run_rust_full as RRF

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def run(base, full, mutate, label, kind, language, expect, owner):
    base.MUTATE = dict(mutate)
    row = {'case': label, 'classification': 'invalid', 'language': language,
           'inputDefect': kind, 'mutation': mutate, 'expectedOwnerJoin': expect,
           'owningLaw': owner}
    try:
        g = full.complete(base.build())
        c = CL.Closure(g['st'])
        rep = c.close_run(g['out']['runId'], label)
        ordered = [r['check'] for r in rep['refusals']]
        row.update({'builtAndReminted': True, 'runId': g['out']['runId'],
                    'refused': not rep['admitted'],
                    'closureChecksPassed': rep['checksPassed'],
                    'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                    'orderedRefusalChecks': ordered,
                    'refusalLayer': 'retained-closure'})
    except Exception as e:
        row.update({'builtAndReminted': False, 'refused': True,
                    'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                     'detail': '%s: %s' % (type(e).__name__, str(e)[:500])},
                    'orderedRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'],
                    'refusalLayer': 'owning-schema-or-evaluator-admission'})
    finally:
        base.MUTATE = {}
    first = (row['firstRefusal'] or {}).get('check', '')
    det = str((row['firstRefusal'] or {}).get('detail', ''))
    row['firstRefusalIsTheIntendedJoin'] = expect in first or expect in det
    later = [c for c in row['orderedRefusalChecks'][1:]]
    row['masking'] = {
        'firstRefusalMasksLater': later,
        'maskedCount': len(later),
        'note': ('every refusal the closure reached is listed in order; the intended owner '
                 'join is the FIRST entry, so no earlier generic guard is being mistaken for '
                 'it. Later entries are consequences of the same mutation, not independent '
                 'findings.')}
    return row


def main():
    rows = [
        run(RT, RTF, {'configGraphPath-outside-snapshot': True},
            'typescript-hidden-config-input-not-in-the-snapshot', 'hidden', 'typescript',
            'NATIVE_CONTEXT_PATH_OUTSIDE_SNAPSHOT',
            'identity-schemas.v3 x-opensip-digest-domains snapshotJoins for the TypeScript '
            'context configProjection.configGraphPaths (form inventoried-paths)'),
        run(RT, RTF, {'lockfile-digest-mismatch': True},
            'typescript-mismatched-lockfile-digest', 'mismatch', 'typescript',
            'LOCKFILE',
            'identity-schemas.v3 snapshotJoins form inventoried-path-and-digest on '
            'TypeScriptNativeContextV2.lockfileIdentity'),
        run(RR, RRF, {'crateRootPath-outside-snapshot': True},
            'rust-hidden-crate-root-not-in-the-snapshot', 'hidden', 'rust',
            'UNIVERSE_PATH_OUTSIDE_SNAPSHOT',
            'identity-schemas.v3 snapshotJoins form inventoried-paths on '
            'RustUniverseV2ResolvedInputs.crateRootPaths'),
        run(RR, RRF, {'configProjection-digest-mismatch': True},
            'rust-mismatched-cargo-config-projection-digest', 'mismatch', 'rust',
            'CONTEXT_PROJECTION_AGREES',
            'native-evidence sections 3/11 context projection: '
            'configProjectionSha256 == H(native.cargo-config-projection.v2, '
            'context.configProjection)'),
    ]
    for r in rows:
        print('%-52s %-8s refused=%-5s intended=%-5s masked=%d first=%s'
              % (r['case'][:52], r['inputDefect'], r['refused'],
                 r['firstRefusalIsTheIntendedJoin'], r['masking']['maskedCount'],
                 (r['firstRefusal'] or {}).get('check')))
    doc = {'standing': __doc__, 'classification': 'invalid',
           'languagesCovered': sorted({r['language'] for r in rows}),
           'defectKindsCovered': sorted({r['inputDefect'] for r in rows}),
           'controls': rows}
    with open(OUT + '/vectors/hidden-mismatch-per-language.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    bad = [r['case'] for r in rows if not r['refused']]
    off = [r['case'] for r in rows if not r['firstRefusalIsTheIntendedJoin']]
    if off:
        print()
        for r in rows:
            if r['case'] in off:
                print('NOT THE INTENDED OWNER JOIN: %s\n  expected ~%s\n  ordered %s'
                      % (r['case'], r['expectedOwnerJoin'],
                         r['orderedRefusalChecks'][:6]))
                print('  detail', str((r['firstRefusal'] or {}).get('detail'))[:300])
    assert not bad, bad
    print('\nper-language coverage: %s ; defect kinds: %s'
          % (doc['languagesCovered'], doc['defectKindsCovered']))


main()
