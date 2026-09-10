"""p13: close the render context. M.render is also called outside any try, so sweep the call
index until the injected detail-None Refusal lands inside the guarded renderCases try."""
import ast, json, os, re, shutil, subprocess

BASE = '/tmp/opensip-design-corrections/post-reset-review.v18'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
OLD_CHECKER = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
               'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py')
D = 'docs/coop/design-corrections/workflows/'
PY = '/tmp/opensip-architecture-review-env/bin/python'
FAIL_RE = re.compile(r'^FAIL (\S+)(?: (.*))?$')


def patch(src, nth):
    tree = ast.parse(src)
    hits = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == 'render':
            code = ("globals().setdefault('_CTRLN', [0]); _CTRLN[0] += 1\n"
                    "if _CTRLN[0] == %d: raise Refusal('CTRL.INJECT', None, 'control-injection')" % nth)
            n.body = ast.parse(code).body + n.body
            hits += 1
    assert hits == 1, hits
    return ast.unparse(ast.fix_missing_locations(tree))


def run(work, checker, tag):
    shutil.copyfile(checker, os.path.join(work, D, 'check_workflows.v1.py'))
    p = subprocess.run([PY, '-I', '-B', os.path.join(D, 'check_workflows.v1.py'),
                        '--report', os.path.join(D, 'workflows-report.%s.json' % tag)],
                       cwd=work, capture_output=True, text=True)
    fails = {m.group(1): m.group(2) for m in
             (FAIL_RE.match(l) for l in p.stdout.splitlines()) if m}
    return {'exit': p.returncode, 'fails': fails, 'crashed': 'Traceback' in p.stderr,
            'stderrTail': p.stderr[-200:]}


model_src = open(os.path.join(FROZEN, D, 'workflows_model.v1.py')).read()
NEW = os.path.join(FROZEN, D, 'check_workflows.v1.py')
attempts, found = [], None
work = os.path.join(BASE, 'controls-v2', 'ctl-render-sweep')

for nth in range(1, 61):
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(FROZEN, work)
    open(os.path.join(work, D, 'workflows_model.v1.py'), 'w').write(patch(model_src, nth))
    old = run(work, OLD_CHECKER, 'old')
    new = run(work, NEW, 'new')
    if old['crashed'] or new['crashed']:
        attempts.append({'nth': nth, 'outcome': 'ESCAPED-UNCAUGHT'})
        continue
    fp = sorted(set(new['fails']) - set(old['fails']))
    oo = sorted(set(old['fails']) - set(new['fails']))
    attempts.append({'nth': nth, 'outcome': 'LANDED', 'falsePassesRemoved': fp, 'oldOnly': oo})
    print('nth=%-3d LANDED oldFails=%d newFails=%d falsePassesRemoved=%s oldOnly=%s'
          % (nth, len(old['fails']), len(new['fails']), fp, oo))
    if fp and found is None:
        found = {'nth': nth, 'falsePassesRemoved': fp, 'oldOnly': oo,
                 'detail': {k: new['fails'][k] for k in fp}}
        break

print('\nescapedUncaughtAttempts=%d' % sum(1 for a in attempts if a['outcome'] == 'ESCAPED-UNCAUGHT'))
print('renderFalsePassDemonstrated=%s' % json.dumps(found))
json.dump({'attempts': attempts, 'found': found},
          open(os.path.join(BASE, 'logs', 'p13-render-control.json'), 'w'), indent=1)
