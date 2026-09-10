"""p11: independent discriminating control across ALL TEN guarded contexts.

For each context, patch the model entry point called inside that try-block so it raises a
detail-None Refusal, then run the OLD (v17) and NEW (v18) checker against the SAME patched
tree. Rows that PASS under old and FAIL under new are actual false passes the guard removes.

Both checkers see identical inputs; the delta isolates the guard's effect. No repinning.
"""
import ast, json, os, shutil, subprocess, sys

BASE = '/tmp/opensip-design-corrections/post-reset-review.v18'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
OLD_CHECKER = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
               'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py')
D = 'docs/coop/design-corrections/workflows/'
PY = '/tmp/opensip-architecture-review-env/bin/python'

CONTEXTS = [
    ('invocation', 'run_invocation', 171),
    ('import', 'build_import', 384),
    ('source-mapping', 'admit_source_mapping', 407),
    ('repair-preview', 'repair_preview', 1112),
    ('repair-recover', 'repair_recover', 1158),
    ('repair-apply', 'repair_apply', 1171),
    ('repair-verify', 'repair_verify', 1203),
    ('test-execution', 'admit_test_execution', 1226),
    ('render', 'render', 1320),
    ('review', 'review_join', 1360),
]


def patched_model(src, fnname):
    tree = ast.parse(src)
    hits = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == fnname:
            inj = ast.parse("raise Refusal('CTRL.INJECT', None, 'control-injection')").body[0]
            body = n.body
            # keep a leading docstring if present, then inject
            at = 1 if (body and isinstance(body[0], ast.Expr)
                       and isinstance(body[0].value, ast.Constant)
                       and isinstance(body[0].value.value, str)) else 0
            n.body = body[:at] + [inj] + body[at:]
            hits += 1
    if hits != 1:
        return None, hits
    return ast.unparse(ast.fix_missing_locations(tree)), hits


def failing_ids(report_path):
    """set of check ids that are not ok, plus overall ok flag"""
    try:
        rep = json.load(open(report_path))
    except Exception as e:
        return None, 'unreadable:%s' % e
    rows = rep.get('failures', rep.get('checks', []))
    ids = set()
    for r in rows:
        if isinstance(r, dict) and r.get('ok') is False:
            ids.add(r.get('id'))
    return ids, rep


def run_variant(work, checker_src_path, tag):
    shutil.copyfile(checker_src_path, os.path.join(work, D, 'check_workflows.v1.py'))
    rep = os.path.join(D, 'workflows-report.%s.json' % tag)
    p = subprocess.run([PY, '-I', '-B', os.path.join(D, 'check_workflows.v1.py'), '--report', rep],
                       cwd=work, capture_output=True, text=True)
    ids, raw = failing_ids(os.path.join(work, rep))
    return {'exit': p.returncode, 'stdoutTail': p.stdout[-400:], 'stderrTail': p.stderr[-400:],
            'failIds': sorted(ids) if ids is not None else None,
            'reportReadable': ids is not None}


model_src = open(os.path.join(FROZEN, D, 'workflows_model.v1.py')).read()
results = []
attempts = []
for name, fn, line in CONTEXTS:
    work = os.path.join(BASE, 'controls', 'ctl-' + name)
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(FROZEN, work)
    newsrc, hits = patched_model(model_src, fn)
    if newsrc is None:
        attempts.append({'context': name, 'fn': fn, 'outcome': 'ABORTED', 'defSites': hits})
        print('%-16s ABORT: %d defs named %s' % (name, hits, fn))
        continue
    open(os.path.join(work, D, 'workflows_model.v1.py'), 'w').write(newsrc)
    old = run_variant(work, OLD_CHECKER, 'old')
    new = run_variant(work, os.path.join(FROZEN, D, 'check_workflows.v1.py'), 'new')
    row = {'context': name, 'fn': fn, 'checkerLine': line, 'old': old, 'new': new}
    if old['failIds'] is not None and new['failIds'] is not None:
        row['falsePassIds'] = sorted(set(new['failIds']) - set(old['failIds']))
        row['onlyOldFails'] = sorted(set(old['failIds']) - set(new['failIds']))
    results.append(row)
    print('%-16s oldExit=%s newExit=%s oldFails=%s newFails=%s falsePassesRemoved=%s'
          % (name, old['exit'], new['exit'],
             len(old['failIds']) if old['failIds'] is not None else 'n/a',
             len(new['failIds']) if new['failIds'] is not None else 'n/a',
             len(row.get('falsePassIds', [])) if 'falsePassIds' in row else 'n/a'))
    if row.get('falsePassIds'):
        for i in row['falsePassIds'][:6]:
            print('        + newly-caught:', i)
    if row.get('onlyOldFails'):
        for i in row['onlyOldFails'][:6]:
            print('        - REGRESSION? old-only fail:', i)

json.dump({'results': results, 'abortedAttempts': attempts},
          open(os.path.join(BASE, 'logs', 'p11-ten-context-controls.json'), 'w'), indent=1)
tot = sum(len(r.get('falsePassIds', [])) for r in results)
reg = sum(len(r.get('onlyOldFails', [])) for r in results)
print('\nTOTAL falsePassesRemovedAcrossContexts=%d  regressions(old-only fails)=%d' % (tot, reg))
