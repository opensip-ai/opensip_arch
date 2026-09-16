"""Independent repair:2 constructor probe (workflow-projection-contract section 5; workflows-and-surfaces section 6).

Reuses the close_run-admitted retained Runs and adapters the owner checker check-workflow-projection.v3 builds (module
globals, stdout captured, final sys.exit caught), and calls workflows_model.v3.repair_preview / admit_repair_plan_v2 with
reviewer-authored adapters. The shared builder is spied to count descriptor construction. Writes only
receipts/probes/repair2.json."""
import contextlib, copy, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
WF = RT / 'work/source42-pkg/docs/coop/design-corrections/workflows'
OUT = RT / 'receipts/probes/repair2.json'
ROWS = []


def row(case, ok, observed=None, expected=None, kind=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if kind:
        r['kind'] = kind
    ROWS.append(r)


spec = importlib.util.spec_from_file_location('p40_cwp_repair', WF / 'check-workflow-projection.v3.py')
K = importlib.util.module_from_spec(spec)
sys.modules['p40_cwp_repair'] = K
saved, sys.argv = sys.argv, [str(WF / 'check-workflow-projection.v3.py')]
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(K)
except SystemExit:
    pass
finally:
    sys.argv = saved
WF3 = K.WF3
BUILDER = WF3._base.repair_preview


def outcome(adapter, targets=None, ephemeral=False):
    calls = []

    def spy(*a, **k):
        calls.append(1)
        return BUILDER(*a, **k)
    WF3._base.repair_preview = spy
    try:
        plan = WF3.repair_preview(K.CW_PROJECT, K.CW_TREE, adapter, K.CW_RECIPE, targets if targets is not None else K.CW_FPS[:1],
                                  K.CW_DELETE, K.CW_REQS, ['**'], K.CW_TRUST, ephemeral=ephemeral)
        return ['ADMIT', plan['descriptor']['schemaMajor'], len(calls)]
    except WF3.Refusal as exc:
        return ['REFUSE', exc.error_code, exc.detail, len(calls)]
    except Exception as exc:  # noqa: BLE001
        return ['PROPAGATE', type(exc).__name__, len(calls)]
    finally:
        WF3._base.repair_preview = BUILDER


def main():
    base = copy.copy(K._oc1_adapter)
    got = outcome(base)
    row('lawful-control-admits-a-repair-2-plan-with-one-descriptor-build', got == ['ADMIT', 2, 1], got)
    got = outcome(dict(base, authority='ephemeral', retained=None))
    row('non-authoritative-refuses-first-even-without-retained-closure', got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE'] and got[-1] == 0, got)
    got = outcome(dict(base, retained=None))
    row('missing-retained-closure-refuses-before-descriptor', got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'] and got[-1] == 0, got)
    got = outcome(dict(base, runId='run2:' + '0' * 64))
    row('run2-evidence-run-refuses-major-before-descriptor', got[:3] == ['REFUSE', 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED', 'EVALUATION.MIXED_OUTPUT_MAJOR'] and got[-1] == 0, got)
    got = outcome(dict(base, runId='run2:' + '0' * 64, planId='plan2:' + '9' * 64))
    row('run3-prefix-check-precedes-plan-join', got[:3] == ['REFUSE', 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED', 'EVALUATION.MIXED_OUTPUT_MAJOR'], got)
    got = outcome(dict(base, planId='plan2:' + '9' * 64))
    row('plan-of-another-run-refuses-before-descriptor', got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'] and got[-1] == 0, got)
    got = outcome(dict(base, runId='run3:' + 'b' * 64))
    row('well-formed-other-run3-id-refuses-before-descriptor', got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'] and got[-1] == 0, got)
    absent = K.hid('finding-key2', 'reviewer-absent-target')
    got = outcome(base, targets=[absent])
    row('target-not-a-matched-fingerprint-of-the-retained-run-refuses-before-descriptor',
        got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE'] and got[-1] == 0, got)

    SEL = K.SEL

    class Sub(SEL.RetainedEvidenceUnavailable):
        pass

    def raising(exc, declared=None):
        view = SEL.RetainedRunView(K.cw_pos_run, K.cw_pos_obj, K.cw_pos_blob)

        def boom(*a, **k):
            raise exc
        view.matched_findings = boom
        if declared is not None:
            cls = type('ReviewerDeclaredView', (SEL.RetainedRunView,), {'UNAVAILABLE': declared})
            v2 = cls(K.cw_pos_run, K.cw_pos_obj, K.cw_pos_blob)
            v2.matched_findings = boom
            return v2
        return view
    got = outcome(dict(base, retained=raising(SEL.RetainedEvidenceUnavailable('x'))))
    row('declared-unavailability-class-maps-to-evidence-run-unavailable', got[:3] == ['REFUSE', 'REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'], got)
    got = outcome(dict(base, retained=raising(Sub('x'))))
    row('subclass-of-the-declared-class-propagates-exact-identity-only', got[0] == 'PROPAGATE', got,
        'contract: exact class identity; a subclass is not the declared class')
    got = outcome(dict(base, retained=raising(KeyError('host defect'), declared=KeyError)))
    row('observation-a-trusted-view-declaring-a-builtin-class-maps-that-exact-class', True, got,
        'the retained view is a trusted host adapter; its declared class is the authority', 'observation')
    got = outcome(dict(base, retained=raising(OSError('io'))))
    row('undeclared-host-fault-propagates', got[0] == 'PROPAGATE', got)

    plan = WF3.repair_preview(K.CW_PROJECT, K.CW_TREE, base, K.CW_RECIPE, K.CW_FPS[:1], K.CW_DELETE, K.CW_REQS, ['**'], K.CW_TRUST)
    try:
        WF3.admit_repair_plan_v2(copy.deepcopy(plan))
        lawful = True
    except Exception:  # noqa: BLE001
        lawful = False
    row('owner-plan-admits', lawful)
    tampered = copy.deepcopy(plan)
    tampered['descriptor']['applicable'] = not tampered['descriptor']['applicable']
    tampered['repairPlanId'] = K.P.W.wid('repairplan2', 'workflow.repair-plan', tampered['descriptor'])
    try:
        WF3.admit_repair_plan_v2(tampered)
        got = 'ADMIT'
    except WF3.Refusal as exc:
        got = exc.error_code + '/' + exc.detail
    row('observation-admit-repair-plan-v2-is-schema-and-identity-admission-not-semantic-rederivation', True, got,
        'a reminted descriptor with flipped applicable is identity-consistent; semantic authority stays with the constructor and apply authorization', 'observation')
    relabel = copy.deepcopy(plan)
    relabel['descriptor']['schemaMajor'] = 1
    try:
        WF3.admit_repair_plan_v2(relabel)
        got = 'ADMIT'
    except WF3.Refusal as exc:
        got = exc.error_code + '/' + exc.detail
    row('major-1-descriptor-refuses-typed', got == 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED/EVALUATION.MIXED_OUTPUT_MAJOR', got)
    row('builder-restored', WF3._base.repair_preview is BUILDER)


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2000:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over owner-admitted retained Runs and a spied shared builder; trusted host adapters synthetic',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']],
                  'observations': [(r['case'], r['observed']) for r in ROWS if r.get('kind') == 'observation']}, indent=1, default=str))
