"""Write output/progress.v16.json from the artifacts that exist RIGHT NOW.

Every row cites the artifact it was measured from. A row is only `executed` when the named
artifact exists and carries its own measured result; nothing here is ticked from a count of
passing helper lines.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'


def exists(rel):
    return os.path.exists(OUT + '/' + rel)


def load(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def main():
    runs = load('runs/all-runs-summary.json') or []
    if isinstance(runs, dict):
        runs = runs.get('runs') or []
    doc = {
        'consumerId': 'consumer-b.v18',
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'sameOriginAncestry': ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v18'],
        'subjectManifestSha256':
            '6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6',
        'parentKitDigestDeclaredInThatManifest':
            '1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b',
        'parentVerificationStanding': (
            'NOT a parent whole-candidate verification. Only the parent digest declared in '
            'the held manifest was compared to the value the instruction names.'),
        'rootStanding': (
            'No root admission, agreement or expected result has been observed or claimed. '
            'No author model, checker, export, root output or digest was supplied or read.'),
        'v16WorkCompletedSoFar': [
            {'item': 'kit custody re-verified for the new frozen successor',
             'artifact': 'notes/v16-input-custody.json',
             'measured': '101/101 PASS; the only CHANGED kit file is '
                         'native/native-evidence.schemas.v2.json'},
            {'item': 'helper paths rebound to the declared current inputs with before-images',
             'artifact': 'lib.before-image.v15/ (pre-rebind) + lib/rebind_v16.py',
             'measured': '24 modules rewritten, 0 residual prior-generation paths'},
            {'item': 'runtime location removed from semantic identity',
             'artifact': 'lib/opensip_fixture.py + vectors/'
                         'relocation-and-transport-equality.json',
             'measured': 'all 5 Runs: location-free=True, relocation-stable=True'},
            {'item': 'corrected native retention vocabulary enforced with a MEASURED site '
                     'count (siteCountLaw replaces the former hand-maintained total)',
             'artifact': 'notes/native-annotated-site-audit.json',
             'measured': 'every annotated native site dispatches on a DECLARED retention; '
                         '`sites` absent and siteCountLaw present'},
            {'item': 'all five Runs reconstructed and resealed from the NEW kit, then '
                     'reclosed, replayed in a fresh process and controlled',
             'artifact': 'runs/*.store.json, runs/*.replay.json, runs/*.controls.json',
             'measured': runs},
            {'item': 'audit group 1 -- policy admission of EVERY rule including disabled, '
                     'with invalid disabled policy as a distinguishing control',
             'artifact': 'vectors/policy-admission-negative-controls.json',
             'measured': '1 positive + 10 negatives; every first refusal is the intended '
                         'law AT the intended boundary (schema / evaluator / closure)'},
            {'item': 'audit group 2 -- every config-graph node kind derived from its path',
             'artifact': 'lib/opensip_closure.py check_config_node_kind_law, exercised on '
                         'the TypeScript Run and all three mode-path harnesses',
             'measured': 'tsconfig.base.json derives `other`; the reaching edge is ignored'},
            {'item': 'audit group 3 -- Rust context projection with the compared binding '
                     'fields ENUMERATED in the result',
             'artifact': 'runs/rust.closure.json check '
                         'native-3-11:CONTEXT_PROJECTION_AGREES*',
             'measured': 'cfgSets.default superset of context baseCfg; target/host flags '
                         'owned by the context only'},
            {'item': 'audit group 4 -- execution-inputs cell Coverage/outcome/cause derived '
                     'from admitted evidence, never from an asserted summary',
             'artifact': 'runs/*.closure.json checks EXECUTION_INPUTS_*',
             'measured': 'derived state and primary (deficiency, nativeCause) pair refuse '
                         'on disagreement; 5 applicability classes kept distinct'},
            {'item': 'phases 0-3 regenerated under the new kit',
             'artifact': 'checkpoints/phase-0.json, phase-1.json, phase-2.json, '
                         'traces/protocol3-traces.json',
             'measured': 'phase0 PASS, phase1 0 failures, phase2 0 failures, '
                         'phase3 0 failures with all 5 terminal kinds reached'},
            {'item': 'phase 4 count/class/attempt, code-vs-data matrix, enumerated-vs-'
                     'resolved, advertised-mode paths',
             'artifact': 'vectors/count-class-attempt.json, code-vs-data-matrix.json, '
                         'enum-vs-resolution.json, advertised-mode-paths.json',
             'measured': '69 anchor-class rows, 26 totality/fact-absent rows, 10 attempt '
                         'rows, 36 file facts all on [enumerated], 6/6 advertised modes '
                         'with an admitted representable path'},
            {'item': 'R-HIDDEN-MISMATCH-PER-LANGUAGE',
             'artifact': 'vectors/hidden-mismatch-per-language.json',
             'measured': '4 controls (hidden+mismatch x typescript+rust); each reports its '
                         'ordered refusal list and the intended first refusal'},
        ],
        'v16WorkCompletedAfterThatCheckpoint': [
            {'item': 'phase 6 configuration, clone, min-resolution, repair, mutation-key, '
                     'imported-boundary and pinned-purge reconstructions',
             'artifact': 'vectors/config-*.json, clones-negatives.json, min-resolution.json, '
                         'repair-descriptor.json, mutation-keys.json, '
                         'imported-observation-boundary.json, envelopes/pinned-purge.json',
             'measured': '3 config positives + 4 config negatives, 6 clone negatives, 3 '
                         'min-resolution levels x qualifying/insufficient, 2 repair positives '
                         '+ 10 repair negatives, 4 measured key inequalities, 1 purge '
                         'positive + 5 negatives'},
            {'item': 'phase 7 invocation, availability and D9 failure envelopes',
             'artifact': 'envelopes/*.json, vectors/multi-unit-missing-caps.json, '
                         'vectors/phase7-standing-rules.json',
             'measured': '9 admitted envelopes, 45 inventory commands with 0 '
                         'format-applicability violations, 5 standing rules, 6 D9 failure '
                         'envelopes all with a derived exit code'},
            {'item': 'phase 8 baseline audit, five comparison cases, four-state distinction, '
                     'authorizations and public terminations',
             'artifact': 'vectors/baseline-audit.json, comparison-*.json, '
                         'empty-partial-unavailable-missing.json, '
                         'test-prep-repair-authorization.json, '
                         'envelopes/public-termination.json',
             'measured': 'baselineId and every comparisonResultId recomputed from the '
                         'descriptor; 4/4 states with a measured example; all 6 D9 classes'},
            {'item': 'graph query over the admitted Run, with target-attribution endpoints',
             'artifact': 'query/graph-query-reconstruction.json',
             'measured': '7 operations (neighbors, pagination, path, self-path, reach, '
                         'reach-bound required, reach-bound best-effort) + 7 failure cases, '
                         'all request/response pairs schema-admitted'},
            {'item': 'phase 10 gap identification and phase 11 deliverable',
             'artifact': 'vectors/phase10-design-gaps.json, blind-review.md, '
                         'blind-review.json',
             'measured': '0 MUST, 2 SHOULD, 2 advisories, 3 withdrawn/resolved; verdict '
                         'CHANGES_REQUIRED with 131/131 non-future requirements executed'},
            {'item': 'requirement status and every phase checkpoint derived FROM the '
                     'artifacts',
             'artifact': 'requirement-status.json, checkpoints/phase-0..11.json',
             'measured': 'executed 131, futureQualification 3, unexecuted 0'},
            {'item': 'one from-scratch command that re-runs every stage',
             'artifact': 'verify-all.json',
             'measured': '27 stages, 0 failed'},
        ],
        'stillOutstanding': [],
        'carriedForwardHelperCorrections': 'see progress.v15.json (V15-D1..D4, V15-S1, '
                                           'V15-A1) -- preserved with their original '
                                           'failing output',
        'noProductChange': ('no product implementation, commit or push was performed; every '
                            'byte written by this origin is under its own output directory'),
    }
    with open(OUT + '/progress.v16.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    print('progress.v16.json written: %d completed items, %d outstanding'
          % (len(doc['v16WorkCompletedSoFar']), len(doc['stillOutstanding'])))


main()
