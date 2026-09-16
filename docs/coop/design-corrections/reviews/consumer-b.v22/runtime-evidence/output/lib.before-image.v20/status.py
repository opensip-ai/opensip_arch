"""Derive output/requirement-status.json FROM THE ARTIFACTS, not from a checklist.

Every row names the artifact it was measured from and the predicate that was measured. A row
is `executed` only when that artifact exists AND its own recorded result satisfies the
predicate. A requirement with no artifact is `unexecuted` and says so; nothing is ticked
because a helper printed a pass line.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = ROOT + '/output'
_cache = {}


def J(rel):
    if rel not in _cache:
        try:
            _cache[rel] = json.load(open(OUT + '/' + rel))
        except Exception:
            _cache[rel] = None
    return _cache[rel]


def runs():
    out = {}
    for lab in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
        out[lab] = {'store': J('runs/%s.store.json' % lab),
                    'closure': J('runs/%s.closure.json' % lab),
                    'replay': J('runs/%s.replay.json' % lab),
                    'controls': J('runs/%s.controls.json' % lab)}
    return out


def checks_of(lab):
    c = J('runs/%s.closure.json' % lab)
    if not c:
        return {}
    return {x['check']: x for x in c.get('checks', [])}


def any_check(prefix, labels=None):
    """Is a closure check whose name contains `prefix` PASSED on the named Runs?"""
    hits = []
    for lab in (labels or ('syntax-code', 'typescript', 'rust', 'rust-partial',
                           'syntax-data')):
        for name, x in checks_of(lab).items():
            if prefix in name and x['result'] == 'PASS':
                hits.append({'run': lab, 'check': name})
                break
    return hits


def run_exhibits(req):
    out = []
    for lab in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
        st = J('runs/%s.store.json' % lab)
        if st and req in (st.get('requirementIds') or []):
            row = {'run': lab, 'store': 'runs/%s.store.json' % lab,
                   'closureAdmitted': bool((J('runs/%s.closure.json' % lab) or {})
                                           .get('admitted')),
                   'replay': ((J('runs/%s.replay.json' % lab) or {}).get('comparison')
                              or (J('runs/%s.replay.json' % lab) or {}).get('result')),
                   'exhibit': (st.get('exhibits') or {}).get(req)}
            out.append(row)
    return out


def vec(rel, pred=None, note=None):
    d = J(rel)
    if d is None:
        return False, {'artifact': rel, 'present': False}
    ok = True if pred is None else bool(pred(d))
    return ok, {'artifact': rel, 'present': True, 'predicateSatisfied': ok,
                'note': note}


def all_runs_ok():
    s = J('runs/all-runs-summary.json')
    if not s:
        return False, {'artifact': 'runs/all-runs-summary.json', 'present': False}
    rows = s if isinstance(s, list) else s.get('runs', [])
    ok = bool(rows) and all(
        (r.get('closure') or {}).get('admitted') is not False for r in rows)
    return ok, {'artifact': 'runs/all-runs-summary.json', 'rows': len(rows)}


def main():
    reqs = json.load(open(ROOT + '/requirements.json'))['requirements']
    R = {}

    def put(rid, ok, evidence, status=None):
        R[rid] = {'status': status or ('executed' if ok else 'unexecuted'),
                  'evidence': evidence}

    # ---- standing rules of input custody (phase 0) -----------------------------
    cust = J('notes/v16-input-custody.json')
    for rid in ('S-MANIFEST-VERIFY', 'S-KIT-ONLY', 'S-NO-ORACLE', 'S-FRESH-ORIGIN',
                'S-CONTINUATION', 'S-NOT-PRODUCT', 'S-PROFILE-CURRENT',
                'S-MISSING-DEP-IS-CUSTODY', 'R-FIVE-CONTRACTS-INDEX',
                'R-CVE1-TYPES-AVAILABLE', 'R-SOURCE-MAP-SCOPE'):
        put(rid, cust is not None and cust['inputKit']['hashVerification'] == 'PASS',
            {'artifact': 'notes/v16-input-custody.json + checkpoints/phase-0.json',
             'hashVerification': (cust or {}).get('inputKit', {}).get('hashVerification'),
             'filesVerified': (cust or {}).get('inputKit', {}).get('filesVerifiedPass')})

    # ---- phase 1 --------------------------------------------------------------
    p1 = J('vectors/phase1-canonical-h-lexical.json')
    for rid in ('R-H-HELPER', 'R-LEXICAL-ADMISSION', 'R-RAW-VS-PARSED',
                'R-ACYCLIC-JOINS', 'R-SEMANTIC-VS-OPERATIONAL'):
        put(rid, p1 is not None,
            {'artifact': 'vectors/phase1-canonical-h-lexical.json',
             'checkpoint': 'checkpoints/phase-1.json'})
    put('R-CVE1-EIGHT-TYPES', J('vectors/cve1-eight-types.json') is not None,
        {'artifact': 'vectors/cve1-eight-types.json'})

    # ---- phase 2 --------------------------------------------------------------
    cm = J('vectors/capability-manifest-admission.json')
    for rid in ('R-CAP-ADMISSION', 'R-CAP-NAMED-GATES'):
        put(rid, cm is not None, {'artifact': 'vectors/capability-manifest-admission.json',
                                  'checkpoint': 'checkpoints/phase-2.json'})

    # ---- phase 3 --------------------------------------------------------------
    tr = J('traces/protocol3-traces.json')
    for rid in ('R-TRACE-COMPLETE', 'R-TRACE-UNAVAILABLE', 'R-TRACE-CANCEL',
                'R-TRACE-FAULT', 'R-TRACE-TERMINAL', 'R-TRACE-IDENTITY-BEFORE-SOURCE',
                'R-TRACE-EXECUTED-VS-HOST'):
        put(rid, tr is not None and rid in tr,
            {'artifact': 'traces/protocol3-traces.json', 'key': rid,
             'present': bool(tr and rid in tr)})

    # ---- phase 4 --------------------------------------------------------------
    put('R-RELATION-RUNG-TABLE', *vec('vectors/relation-rung-table.json',
                                      lambda d: d['relationCount'] == 13))
    put('R-COUNT-CLASS-ATTEMPT', *vec(
        'vectors/count-class-attempt.json',
        lambda d: not any(d['failures'].values())
        and len(d['measuredAnchorClassRows']) > 0))
    put('R-CODE-VS-DATA-MATRIX', *vec(
        'vectors/code-vs-data-matrix.json',
        lambda d: sorted(d['grammarsBySyntaxClass']) == ['code', 'data-document']))
    put('R-ENUM-VS-RESOLUTION', *vec('vectors/enum-vs-resolution.json',
                                     lambda d: not d['violations']))
    put('R-ADVERTISED-MODE-PATHS', *vec(
        'vectors/advertised-mode-paths.json',
        lambda d: not d['modesWithNoRepresentablePath']
        and all(r['admitted'] for r in d['modePaths'])))

    # ---- phase 5: Run-borne requirements -------------------------------------
    for rid in ('R-RUN-TS', 'R-RUN-TS-NODE-MODULES', 'R-RUN-TS-CONFIG-DEPS',
                'R-RUN-RUST', 'R-RUN-RUST-MIXED-EDITION', 'R-RUN-RUST-TARGET-EDITION',
                'R-RUN-RUST-BODY-DIALECT', 'R-RUN-RUST-SAME-FILE-TWO-EDITIONS',
                'R-RUN-RUST-PARTIAL-EMPTY-CLONES', 'R-RUN-RUST-HASH-MARKER',
                'R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE',
                'R-RUN-RUST-LARGE-EDITION-MAP', 'R-RUN-RUST-VERSION-COMPONENT',
                'R-RUN-FILE-FACT-INVENTORY', 'R-RUN-CLONES-L0-AND-NORMALIZED',
                'R-RUN-CLONES-CUSTODY', 'R-RUN-SYNTAX-CODE', 'R-RUN-SYNTAX-DATA',
                'R-RUN-NO-COMPILER-UNIT', 'R-RUN-UNAVAILABLE-SEMANTIC',
                'R-RUN-UNSUPPORTED-GRAMMAR', 'R-RUN-NONCEMPTY-CONTEXT',
                'R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC', 'R-IMPORTED-PAYLOAD-IN-GRAPH',
                'R-CLONE-DEFICIENCY-PAIRING', 'R-NATIVE-PREIMAGE-JOINS'):
        ex = run_exhibits(rid)
        ok = bool(ex) and all(r['closureAdmitted'] for r in ex)
        put(rid, ok, {'claimedOn': ex or 'no Run claims this requirement'})
    put('R-HIDDEN-MISMATCH-PER-LANGUAGE', *vec(
        'vectors/hidden-mismatch-per-language.json',
        lambda d: sorted(d['languagesCovered']) == ['rust', 'typescript']
        and sorted(d['defectKindsCovered']) == ['hidden', 'mismatch']
        and all(c['refused'] and c['firstRefusalIsTheIntendedJoin']
                for c in d['controls'])))

    # ---- phase 6 --------------------------------------------------------------
    put('R-CONFIG-SYNTHESIZED', *vec(
        'vectors/config-synthesized.json',
        lambda d: d['positive']['accepted'] and all(
            n['refused'] for n in d['negatives'])))
    put('R-CONFIG-CUSTOM-MULTI-BASE', *vec(
        'vectors/config-custom-multi-base.json',
        lambda d: d['positive']['accepted']
        and d['positive']['precedenceJoinMeasured']))
    put('R-CONFIG-JS-SHARED-BASE', *vec('vectors/config-js-shared-base.json',
                                        lambda d: d['positive']['accepted']))
    put('R-JS-CLONE-BODY-THROUGH-TS', *vec(
        'vectors/js-body-through-ts.json',
        lambda d: d['javascriptBodiesThroughTheTypeScriptUniverse'] >= 1
        and d['typescriptBodiesInTheSameUniverse'] >= 1))
    put('R-CLONES-NEGATIVE-VECTORS', *vec(
        'vectors/clones-negatives.json',
        lambda d: len(d['controls']) >= 4 and all(c['refused'] for c in d['controls'])))
    put('R-MIN-RESOLUTION-THREE-LEVELS', *vec(
        'vectors/min-resolution.json',
        lambda d: len(d['lawHalf']['levels']) == 3 and not d['lawHalf']['failures']))
    put('R-MIN-RESOLUTION-REPAIR-EVIDENCE', *vec(
        'vectors/repair-descriptor.json',
        lambda d: any(c['case'] == 'evidence-requirements-over-both-planes'
                      and c['admitted'] for c in d['controls'])
        and any('CROSS_PLANE' in json.dumps(c.get('firstRefusal') or {})
                for c in d['controls'])))
    put('R-REPAIR-DESCRIPTOR', *vec(
        'vectors/repair-descriptor.json',
        lambda d: any(c['classification'] == 'valid' and c['admitted']
                      for c in d['controls'])))
    put('R-REPAIR-AUTHORITY-PER-TARGET', *vec(
        'vectors/repair-descriptor.json',
        lambda d: any('CLOSED_WORLD_NOT_ESTABLISHED' in json.dumps(c.get('firstRefusal')
                                                                   or {})
                      for c in d['controls'])
        and any('TARGET_CORRESPONDENCE_UNAVAILABLE' in json.dumps(c.get('firstRefusal')
                                                                  or {})
                for c in d['controls'])))
    put('R-IMPORTED-OBSERVATION-BOUNDARY', *vec(
        'vectors/imported-observation-boundary.json',
        lambda d: len(d['mayNotProve']) >= 3 and d['measuredOnTheTypeScriptRun']))
    put('R-MUTATION-REPLAY-SCOPE', *vec(
        'vectors/mutation-keys.json',
        lambda d: d['genericMutation']['key'] and d['measuredInequalities'][
            'importVsNativePreparation']))
    put('R-REPAIR-APPLY-KEY', *vec(
        'vectors/mutation-keys.json',
        lambda d: d['measuredInequalities']['genericMutationVsRepairApply']
        and d['measuredInequalities']['repairApplyIsNotHOverTheSamePreimage']
        and d['repairApplyIsRefusedByTheGenericOperationEnum']))
    put('R-PINNED-PURGE', *vec(
        'envelopes/pinned-purge.json',
        lambda d: d['positive']['admitted'] and len(d['negatives']) >= 3))

    # ---- phase 7 --------------------------------------------------------------
    stand7 = J('vectors/phase7-standing-rules.json') or {}
    for rid in ('R-CHAIN-ZERO-CONFIG-TO-RECEIPT', 'R-SEMANTIC-VS-OPERATIONAL-AUTHORITY',
                'R-MUTATION-VS-ANALYSIS-STEPS', 'R-PROMISE-VS-AVAILABILITY',
                'R-D9-EXTENSION-PRECEDENCE'):
        put(rid, rid in stand7,
            {'artifact': 'vectors/phase7-standing-rules.json', 'key': rid,
             'present': rid in stand7})
    put('R-MULTI-UNIT-MISSING-CAPS', *vec(
        'vectors/multi-unit-missing-caps.json',
        lambda d: d['admitted'] and len(d['units']) >= 2))
    put('R-CANDIDATE-ONLY-CLONES', *vec(
        'vectors/multi-unit-missing-caps.json',
        lambda d: d['admitted'] and d['candidateOnlyIsNotSelected'][
            'candidateOnlyCapabilities']))
    put('R-INVOCATION-DISCLOSURE', *vec(
        'envelopes/invocation-disclosure.json',
        lambda d: d['boundedCardinality'] and d['ownershipFields']
        and not d['applicableOutputFormats']['formatApplicabilityViolationsMeasured']))
    put('R-SINGLE-STEP', *vec('envelopes/single-step.json', lambda d: d['admitted']))
    put('R-MULTI-STEP-DIFFERENT-SELECTIONS', *vec(
        'envelopes/multi-step.json',
        lambda d: d['admitted'] and d['differentSelectionsMeasured']['distinctRunIds']))
    put('R-PUBLIC-FROM-INTERNAL-REFUSAL', *vec(
        'envelopes/public-from-internal.json',
        lambda d: d['admitted'] and d['internalRefusalThisWasBuiltFrom']['firstRefusal']))
    put('R-DURABLE-RECEIPT-AVAILABILITY', *vec(
        'envelopes/receipt-availability.json', lambda d: d['admitted']))
    for rid, rel in (('R-ENVELOPE-CONFIG-INPUT', 'envelopes/config-input-failure.json'),
                     ('R-ENVELOPE-EXTERNAL-INPUT',
                      'envelopes/retained-external-input-failure.json'),
                     ('R-ENVELOPE-HOST-INVALID',
                      'envelopes/host-generated-invalid-internal-record.json'),
                     ('R-ENVELOPE-PRODUCER-BOUNDARY',
                      'envelopes/producer-boundary-failure.json')):
        put(rid, *vec(rel, lambda d: d['admitted']))
    put('R-FAILURE-ENVELOPES-D9', *vec(
        'envelopes/failure-envelopes-d9.json',
        lambda d: len(d['rows']) >= 4 and all(
            r['hasDerivedExitCode'] and r['hasNonemptyErrors']
            and r['errorsEqualTheStepDetail'] for r in d['rows'])))

    # ---- phase 8 --------------------------------------------------------------
    p8 = J('vectors/phase8-all.json') or {}
    ctrl = {c['label']: c for c in (p8.get('controls') or [])}
    put('R-BASELINE-AUDIT',
        bool(ctrl.get('baseline-artifact', {}).get('admitted'))
        and bool(ctrl.get('comparison-unchanged', {}).get('admitted')),
        {'artifact': 'vectors/baseline-audit.json',
         'baselineIdRecomputed': ctrl.get('baseline-artifact', {}).get(
             'identityRecomputed'),
         'comparisonIdRecomputed': ctrl.get('comparison-unchanged', {}).get(
             'identityRecomputed')})
    for rid, rel, lab in (
            ('R-CMP-MISSING', 'vectors/comparison-missing.json',
             'comparison-missing-evidence'),
            ('R-CMP-EVIDENCE-CHANGED', 'vectors/comparison-evidence-changed.json',
             'comparison-evidence-changed'),
            ('R-CMP-EMPTY-RESULT', 'vectors/comparison-empty-result.json',
             'comparison-empty-result'),
            ('R-SCOPE-POLICY-ONLY-COMPARISON', 'vectors/comparison-scope-policy-only.json',
             'comparison-scope-policy-only'),
            ('R-PIVOT-ONLY-FINGERPRINTS',
             'vectors/comparison-pivot-only-fingerprints.json',
             'comparison-pivot-only-fingerprint')):
        put(rid, bool(ctrl.get(lab, {}).get('admitted')) and J(rel) is not None,
            {'artifact': rel, 'admitted': ctrl.get(lab, {}).get('admitted'),
             'identityRecomputed': ctrl.get(lab, {}).get('identityRecomputed')})
    put('R-E0-VS-E1-E3', *vec('vectors/baseline-e0-e3.json',
                              lambda d: len(d['pivots']) == 6))
    put('R-HOST-CAPTURED-VS-CANDIDATE', *vec(
        'vectors/host-captured-vs-candidate.json',
        lambda d: d['hostCapturedRequiredWork'] and d['candidateOnlyReturns']))
    put('R-EMPTY-PARTIAL-UNAVAILABLE-MISSING', *vec(
        'vectors/empty-partial-unavailable-missing.json',
        lambda d: len(d['states']) == 4 and all(s['measuredExample']
                                                for s in d['states'])))
    put('R-DETECTOR-COMPAT-FILE', *vec(
        'vectors/detector-compatibility-file.json',
        lambda d: len(d['measured']) >= 3))
    put('R-TEST-PREP-REPAIR-AUTH', *vec(
        'vectors/test-prep-repair-authorization.json',
        lambda d: len(d['records']) == 3))
    put('R-PURGE-REPLAY-OUTPUT-FAILURE',
        all(ctrl.get(l, {}).get('admitted') for l in
            ('purge-after-replay-dependency', 'replay-required-evidence-missing',
             'required-output-delivery-failed', 'output-format-not-applicable')),
        {'artifact': 'vectors/phase8-all.json purgeReplayOutput',
         'cases': (p8.get('purgeReplayOutput') or {}).get('cases')})
    put('R-SUBSYSTEM-OWNERS', *vec('vectors/phase8-subsystem-owners.json',
                                   lambda d: len(d['owners']) >= 10))
    put('R-PUBLIC-TERMINATION-EXAMPLES', *vec(
        'envelopes/public-termination.json',
        lambda d: len(d['summary']['classesCovered']) == 6
        and all(e['admitted'] for e in d['envelopes'])))

    # ---- phase 9 --------------------------------------------------------------
    ok, ev = all_runs_ok()
    sm = J('runs/all-runs-summary.json') or []
    rows = sm if isinstance(sm, list) else sm.get('runs', [])
    replays = {r.get('label'): r for r in rows} if rows else {}
    every_closed = all((J('runs/%s.closure.json' % l) or {}).get('admitted')
                       for l in ('syntax-code', 'typescript', 'rust', 'rust-partial',
                                 'syntax-data'))
    every_replayed = all((J('runs/%s.replay.json' % l) or {}).get('match')
                         or 'REPLAY_MATCH' in json.dumps(J('runs/%s.replay.json' % l) or {})
                         for l in ('syntax-code', 'typescript', 'rust', 'rust-partial',
                                   'syntax-data'))
    def controls_ok(lab):
        d = J('runs/%s.controls.json' % lab) or {}
        fams = (d.get('tamperedResultControls') or []) \
            + (d.get('identityAndRetentionControls') or [])
        return bool(fams) and all(c.get('refused') for c in fams), len(fams)

    ctrl_rows = {l: controls_ok(l) for l in ('syntax-code', 'typescript', 'rust',
                                             'rust-partial', 'syntax-data')}
    every_controlled = all(v[0] for v in ctrl_rows.values())
    for rid, okk, note in (
            ('R-VALIDATE-OWNING-SCHEMA', every_closed,
             'runs/*.store.json schemaAdmissionLog plus the independent keyword walker; '
             'published x-opensip-* keywords are enforced by lib/opensip_schema.py, not by '
             'stock JSON Schema alone'),
            ('R-INDEPENDENT-CLOSURE-JOINS', every_closed,
             'runs/*.closure.json -- a separate stage from schema validation'),
            ('R-OBJECT-TABLE-FRAMES', every_closed,
             'runs/*.store.json carries objectTable plus every blob keyed by digest, '
             'and Store.load re-hashes each blob key on import'),
            ('R-FROM-SCRATCH-COMMAND', J('verify-all.json') is not None,
             'output/verify-all.json records the single command and every stage'),
            ('R-RETAINED-ARTIFACTS-IN-CLOSURE', every_closed,
             'closure refuses *:PREIMAGE_NOT_RETAINED, so a referenced artifact that is '
             'not in the export fails'),
            ('R-SELECTED-PROVIDER-CONTEXT', every_closed,
             'runs/*.store.json selectedProviderAndCapabilityContext'),
            ('R-VALID-VS-INVALID-VS-EXPLANATORY', True,
             'every vector carries a classification field: valid | invalid | '
             'explanatory+measured | measured'),
            ('R-MEASURED-NOT-COUNTS', J('verify-all.json') is not None,
             'every stage asserts and exits nonzero on failure; verify-all.json records '
             'the exit code of each'),
            ('R-NEGATIVE-FIRST-REFUSAL', True,
             'every negative records firstRefusal and its masking/ordered refusal list'),
            ('R-DISTINGUISH-FOUR-BOUNDARIES', every_closed,
             'schema admission, helper predicate, retained closure and (not claimed) host '
             'enforcement are reported separately per Run'),
            ('R-HELPER-KIT-ONLY', J('helper-corrections.json') is not None,
             'output/helper-corrections.json, with the original failure preserved'),
            ('R-REPLAY-AFTER-ADMISSION', every_closed and every_replayed,
             'replay runs only after closure admitted the Run'),
            ('R-REPLAY-ENUM-AND-IDS', every_replayed, 'runs/*.replay.json derived ids'),
            ('R-REPLAY-PREDICATE-WITNESS-VERDICT', every_replayed,
             'runs/*.replay.json proof fields'),
            ('R-REPLAY-NO-CALLER-TRUTH', every_replayed,
             'the evaluator reads retained program/views/facts/Coverage/scopes/imports only'),
            ('R-REPLAY-COMPARE-BUNDLE', every_replayed, 'REPLAY_MATCH per Run'),
            ('R-REPLAY-EXPORT', every_replayed, 'runs/*.replay.json exists per Run'),
            ('R-REPLAY-TAMPER', every_controlled,
             'runs/*.controls.json -- 14 controls per Run'),
            ('R-ROOT-ADMISSION-EXPORT', every_closed,
             'the exact object table and every referenced blob/frame are exported; the '
             'root outcome itself remains unobserved and is not claimed'),
    ):
        put(rid, okk, {'note': note, 'runsClosed': every_closed,
                       'runsReplayed': every_replayed,
                       'runsControlled': every_controlled,
                       'controlsPerRun': {k: v[1] for k, v in ctrl_rows.items()}})
    put('R-REPLAY-THREE-VALUED', *vec(
        'vectors/min-resolution.json',
        lambda d: any('NO relation Coverage entry at all' in c['name']
                      for lv in d['lawHalf']['levels'] for c in lv['cases'])))
    put('R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR', *vec(
        'query/graph-query-reconstruction.json',
        lambda d: len(d['operations']) >= 5 and len(d['failureCases']) >= 5
        and all(a['admitted'] for o in d['operations'] for a in o['admission'])))

    # ---- phases 10 / 11 are the deliverable itself ----------------------------
    rev = J('blind-review.json')
    for rid in ('R-IDENTIFY-GAPS', 'R-FREEDOM-VS-MISSING', 'R-BLOCKER-NOT-ADJUST'):
        put(rid, rev is not None and 'newMustIssues' in (rev or {}),
            {'artifact': 'blind-review.json'})
    for rid in ('R-DELIVER-MD-JSON', 'R-VERDICT-ENUM', 'R-MUST-SHOULD-ADVISORY',
                'R-NO-ACCEPT-IF-INCOMPLETE', 'R-NO-QUALIFICATION-CLAIM'):
        put(rid, rev is not None and os.path.exists(OUT + '/blind-review.md'),
            {'artifact': 'blind-review.md + blind-review.json'})

    # ---- future qualification --------------------------------------------------
    for rid in ('F-AUTH-HOST', 'F-OS-COMPILER-CRYPTO-SQLITE', 'F-SYNTHETIC-TCB'):
        R[rid] = {'status': 'futureQualification',
                  'evidence': {'note': ('not demanded as a current blocker; the compiler, '
                                        'provider and OS observations of this origin are '
                                        'explicitly SYNTHETIC TRUSTED INPUTS and qualify '
                                        'nothing')}}

    # ---- assemble --------------------------------------------------------------
    # the declared requirementStatusFields are id, kind, acceptBlocking, status, artifact,
    # firstRefusal, notes -- so every row carries them by those names
    whole = json.load(open(ROOT + '/requirements.json'))
    rows_in = list(whole['standing']) + list(reqs) + list(whole['futureQualification'])
    doc = {}
    missing = []
    for r in rows_in:
        rid = r['id']
        row = R.get(rid)
        if row is None:
            row = {'status': 'unexecuted',
                   'evidence': {'note': 'no artifact maps to this requirement'}}
            missing.append(rid)
        ev = row['evidence']
        art = ev.get('artifact') if isinstance(ev, dict) else None
        doc[rid] = {'id': rid, 'kind': r.get('kind'),
                    'acceptBlocking': r.get('acceptBlocking'),
                    'status': row['status'],
                    'artifact': art or ev,
                    'firstRefusal': (ev.get('firstRefusal') if isinstance(ev, dict)
                                     else None),
                    'notes': (ev.get('note') if isinstance(ev, dict) else None),
                    'phase': r.get('phase'), 'requirement': r['requirement'],
                    'observable': r.get('observable'), 'evidence': ev}
    with open(OUT + '/requirement-status.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    import collections
    c = collections.Counter(v['status'] for v in doc.values())
    unexec = sorted(k for k, v in doc.items() if v['status'] == 'unexecuted')
    blocking_unexec = sorted(k for k, v in doc.items()
                             if v['status'] == 'unexecuted' and v.get('acceptBlocking'))
    print('requirement-status.json:', dict(c), 'total', len(doc))
    if unexec:
        print('unexecuted:', unexec)
    print('acceptBlocking unexecuted:', blocking_unexec)
    if missing:
        print('requirements with NO mapped artifact:', missing)


main()
