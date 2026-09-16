"""p02 <tree>: execute the tree's ACTUAL workflow checker (full stdout retained), then owner controls over its closed Runs.

Checker: exec'd exactly as the root probe does (sys.argv = [checker], stdout/stderr to receipts). Its exit and failed ids
are recorded; a failing checker is never relabelled as passing.

Controls, all through WF3.repair_preview of THIS tree with the checker's own fixture inputs:
- the cw_pos full Run re-admitted by a SEPARATE identity-model.v3 instance (close_run == adapter runId, identifier too);
- lawful preview; the same retained closure and Plan with an arbitrary well-formed run3 id; a SECOND ACTUALLY ADMITTED Run
  of the checker whose Plan is shared (re-admitted here via close_run) named with the first Run's retained closure, and the
  reverse; that second Run's own lawful preview;
- declared retained unavailability (a finding record, the evaluation-subject records) on views built by the checker's
  reference selection instance AND by the owner's own instance;
- a probe-local exception class also named RetainedEvidenceUnavailable raised from matched_findings and from a
  selector-read method, and an OSError host fault: must propagate as the exact object;
- an undeclared duck-typed stub adapter raising the reference class (protocol boundary, recorded).
The shared major-1/2 builder (_base.repair_preview) is spied: sharedBuilderCalls == 0 means refused before any descriptor.
Output: receipts/p02-<tree>.json.
"""
import contextlib, hashlib, importlib.util, json, sys, time
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1')
tree = sys.argv[1]
T = BASE / 'work' / tree
R = BASE / 'receipts'
WFD = T / 'docs/coop/design-corrections/workflows'
f = WFD / 'check-workflow-projection.v3.py'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
OWNED = [WFD / n for n in ('workflows_model.v3.py', 'repair_closed_world_selection.v1.py', 'check-workflow-projection.v3.py',
                           'workflow-projection-contract.v3.md', 'workflows_model.v1.py')]
before = {str(p.relative_to(T)): sha(p) for p in OWNED}
started = time.time()
g = {'__file__': str(f), '__name__': '__main__'}
sys.argv = [str(f)]
checker_exit = None
stdout_path, stderr_path = R / ('p02-%s-checker-stdout.json' % tree), R / ('p02-%s-checker-stderr.txt' % tree)
with stdout_path.open('w') as out, stderr_path.open('w') as err, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
    try:
        exec(compile(f.read_bytes(), str(f), 'exec'), g)
    except SystemExit as exc:
        checker_exit = exc.code
report_doc = json.loads(stdout_path.read_text())
checker = {'exit': checker_exit, 'count': report_doc['count'], 'passed': report_doc['passed'],
           'failed': [c['id'] for c in report_doc['failed']], 'failedDetails': {c['id']: c['detail'] for c in report_doc['failed']},
           'stdoutSha256': sha(stdout_path), 'stderrBytes': stderr_path.stat().st_size, 'loadedChecker': str(f.resolve())}

W, SEL = g['WF3'], g['SEL']
S = W.closed_world_selection()
ms = importlib.util.spec_from_file_location('p02_run_admission', T / 'docs/coop/design-corrections/foundation/identity-model.v3.py')
M = importlib.util.module_from_spec(ms)
ms.loader.exec_module(M)
adapter = g['_oc1_adapter']
runs = {n: tuple(g['cw_%s_%s' % (n, k)] for k in ('id', 'run', 'obj', 'blob')) for n in ('pos', 'neg', 'dyn', 'asym')}
pos_id, pos_run, pos_obj, pos_blob = runs['pos']
facts = {'loadedOwner': str(Path(W.__file__).resolve()), 'loadedIdentity': str(Path(M.__file__).resolve()),
         'adapterRunIdIsCwPos': adapter['runId'] == pos_id,
         'closeRunEqualsAdapterRunId': M.close_run(pos_run, pos_obj, pos_blob) == adapter['runId'],
         'identifierEqualsAdapterRunId': M.identifier('run', pos_run) == adapter['runId'],
         'referenceSelectionIsASeparateModuleInstance': SEL is not S and SEL.RetainedEvidenceUnavailable is not S.RetainedEvidenceUnavailable,
         'runs': {n: {'runId': v[0], 'planId': v[1]['planId']} for n, v in runs.items()}}
shared = [n for n in ('dyn', 'neg', 'asym') if runs[n][1]['planId'] == pos_run['planId'] and runs[n][0] != pos_id]
facts['runsSharingThePosPlan'] = shared
second = shared[0] if shared else None
if second:
    s_id, s_run, s_obj, s_blob = runs[second]
    facts['secondRun'] = {'name': second, 'runId': s_id, 'closeRunReadmits': M.close_run(s_run, s_obj, s_blob) == s_id,
                          'identifier': M.identifier('run', s_run) == s_id, 'evidenceDiffers': s_run['evidenceId'] != pos_run['evidenceId']}

calls = []


def origin(cls):
    if cls is SEL.RetainedEvidenceUnavailable: return 'reference-selection-instance-class'
    if cls is S.RetainedEvidenceUnavailable: return 'owner-selection-instance-class'
    return None if cls is None else cls.__module__ + '.' + cls.__qualname__


def call(label, a, marker=None, spy=None):
    seen = {'builder': 0}
    base = W._base
    orig = base.repair_preview

    def builder(*args, **kw):
        seen['builder'] += 1
        return orig(*args, **kw)
    base.repair_preview = builder
    row = {'label': label}
    try:
        p = W.repair_preview(g['CW_PROJECT'], g['CW_TREE'], a, g['CW_RECIPE'], g['CW_FPS'][:1], g['CW_DELETE'], g['CW_REQS'], ['**'], g['CW_TRUST'])
        row.update(outcome='ADMIT', repairPlanId=p['repairPlanId'], evidenceRunId=p['descriptor']['evidenceRunId'],
                   applicable=p['descriptor']['applicable'], unmet=p['descriptor']['unmetPreconditions'])
    except W.Refusal as exc:
        row.update(outcome='REFUSE', errorCode=exc.error_code, detail=exc.detail, message=str(exc.remedy)[:200],
                   cause=origin(type(exc.__cause__)) if exc.__cause__ is not None else None)
    except Exception as exc:
        row.update(outcome='PROPAGATE', cls=origin(type(exc)), message=str(exc)[:200],
                   exactObject=(exc is marker) if marker is not None else None)
    finally:
        base.repair_preview = orig
    row['sharedBuilderCalls'] = seen['builder']
    if spy is not None: row['injectedCalled'] = spy['called']
    calls.append(row)
    return row


call('lawful', adapter)
call('same-retained-closure-and-plan-arbitrary-wrong-run3-id', dict(adapter, runId='run3:' + 'a' * 64))
if second:
    call('second-admitted-run-own-lawful-preview', dict(adapter, runId=s_id, planId=s_run['planId'], retained=SEL.RetainedRunView(s_run, s_obj, s_blob)))
    call('second-admitted-run-id-with-first-run-retained-closure-shared-plan', dict(adapter, runId=s_id))
    call('first-run-id-with-second-admitted-run-retained-closure-shared-plan', dict(adapter, retained=SEL.RetainedRunView(s_run, s_obj, s_blob)))
call('retained-closure-of-another-plan-still-refuses', dict(adapter, planId='plan2:' + 'b' * 64))

fid0 = pos_run and SEL.RetainedRunView(pos_run, pos_obj, pos_blob)._evidence['findingIds'][0]
no_finding = {k: v for k, v in pos_obj.items() if k != fid0}
no_subject = {k: v for k, v in pos_obj.items() if v[0] != 'evaluation-subject'}
for inst_name, inst in (('reference', SEL), ('owner', S)):
    call('declared-missing-finding-record-%s-instance-view' % inst_name, dict(adapter, retained=inst.RetainedRunView(pos_run, no_finding, pos_blob)))
    call('declared-missing-subject-records-selector-path-%s-instance-view' % inst_name, dict(adapter, retained=inst.RetainedRunView(pos_run, no_subject, pos_blob)))


class RetainedEvidenceUnavailable(Exception):
    """Probe-local and unrelated: same class name as the owner's, not the owner's class."""


def injected(view, method, exc):
    spy = {'called': False}

    def fn(*args, **kw):
        spy['called'] = True
        raise exc
    setattr(view, method, fn)
    return spy


for method in ('matched_findings', 'coverage_records'):
    marker = RetainedEvidenceUnavailable('foreign host defect')
    view = SEL.RetainedRunView(pos_run, pos_obj, pos_blob)
    call('foreign-same-name-exception-from-%s' % method, dict(adapter, retained=view), marker, injected(view, method, marker))
marker = OSError('host read fault')
view = SEL.RetainedRunView(pos_run, pos_obj, pos_blob)
call('host-oserror-from-matched_findings', dict(adapter, retained=view), marker, injected(view, 'matched_findings', marker))


class UndeclaredStub:
    """Duck-typed view with no declared unavailability class."""
    def __init__(self, run, exc):
        self.run, self._exc = run, exc

    def matched_findings(self):
        raise self._exc


marker = SEL.RetainedEvidenceUnavailable('finding:undeclared-stub')
call('undeclared-stub-adapter-raising-the-reference-class', dict(adapter, retained=UndeclaredStub(pos_run, marker)), marker)

after = {str(p.relative_to(T)): sha(p) for p in OWNED}
out = {'tree': str(T), 'checker': checker, 'facts': facts, 'calls': calls, 'before': before, 'after': after,
       'stable': before == after, 'seconds': round(time.time() - started, 1)}
(R / ('p02-%s.json' % tree)).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'checker'} | {'checker': {k: checker[k] for k in ('exit', 'count', 'failed')}}, indent=1))
sys.exit(0 if out['stable'] else 1)
