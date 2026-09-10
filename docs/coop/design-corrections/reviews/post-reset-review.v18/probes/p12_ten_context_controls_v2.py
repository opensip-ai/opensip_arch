"""p12: ten-context discriminating control, v2.

Fix from failed-attempt-01: FAIL rows are emitted on stdout as 'FAIL <id> <detail>'; parse those.
For contexts where unconditional injection breaks the checker's own setup (uncaught KeyError),
fall back to an Nth-call conditional injection so only one invocation is diverted.
"""
import ast, json, os, re, shutil, subprocess

BASE = '/tmp/opensip-design-corrections/post-reset-review.v18'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
OLD_CHECKER = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
               'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py')
D = 'docs/coop/design-corrections/workflows/'
PY = '/tmp/opensip-architecture-review-env/bin/python'

CONTEXTS = [('invocation', 'run_invocation', 171), ('import', 'build_import', 384),
            ('source-mapping', 'admit_source_mapping', 407), ('repair-preview', 'repair_preview', 1112),
            ('repair-recover', 'repair_recover', 1158), ('repair-apply', 'repair_apply', 1171),
            ('repair-verify', 'repair_verify', 1203), ('test-execution', 'admit_test_execution', 1226),
            ('render', 'render', 1320), ('review', 'review_join', 1360)]

FAIL_RE = re.compile(r'^FAIL (\S+)(?: (.*))?$')


def parse_fails(stdout):
    out = {}
    for line in stdout.splitlines():
        m = FAIL_RE.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def patch(src, fnname, nth):
    """Inject a detail-None Refusal. nth=None -> unconditional; else fire only on call #nth."""
    tree = ast.parse(src)
    hits = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == fnname:
            if nth is None:
                code = "raise Refusal('CTRL.INJECT', None, 'control-injection')"
            else:
                code = ("globals().setdefault('_CTRLN', [0]); _CTRLN[0] += 1\n"
                        "if _CTRLN[0] == %d: raise Refusal('CTRL.INJECT', None, 'control-injection')" % nth)
            inj = ast.parse(code).body
            body = n.body
            at = 1 if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                       and isinstance(body[0].value.value, str)) else 0
            n.body = body[:at] + inj + body[at:]
            hits += 1
    return (ast.unparse(ast.fix_missing_locations(tree)), hits) if hits == 1 else (None, hits)


def run(work, checker, tag):
    shutil.copyfile(checker, os.path.join(work, D, 'check_workflows.v1.py'))
    rep = os.path.join(D, 'workflows-report.%s.json' % tag)
    p = subprocess.run([PY, '-I', '-B', os.path.join(D, 'check_workflows.v1.py'), '--report', rep],
                       cwd=work, capture_output=True, text=True)
    crashed = 'Traceback' in p.stderr
    return {'exit': p.returncode, 'fails': parse_fails(p.stdout), 'crashed': crashed,
            'stderrTail': p.stderr[-300:], 'stdoutHead': p.stdout[:200]}


model_src = open(os.path.join(FROZEN, D, 'workflows_model.v1.py')).read()
NEW_CHECKER = os.path.join(FROZEN, D, 'check_workflows.v1.py')
results, attempts = [], []

for name, fn, line in CONTEXTS:
    row = None
    for nth in [None, 1, 2, 3]:
        work = os.path.join(BASE, 'controls-v2', 'ctl-%s-%s' % (name, nth))
        if os.path.exists(work):
            shutil.rmtree(work)
        shutil.copytree(FROZEN, work)
        src, hits = patch(model_src, fn, nth)
        if src is None:
            attempts.append({'context': name, 'nth': nth, 'outcome': 'ABORT-defcount', 'defs': hits})
            break
        open(os.path.join(work, D, 'workflows_model.v1.py'), 'w').write(src)
        old = run(work, OLD_CHECKER, 'old')
        new = run(work, NEW_CHECKER, 'new')
        if old['crashed'] or new['crashed']:
            attempts.append({'context': name, 'nth': nth, 'outcome': 'CHECKER-CRASH',
                             'oldStderr': old['stderrTail'], 'newStderr': new['stderrTail']})
            shutil.rmtree(work)
            continue
        fp = sorted(set(new['fails']) - set(old['fails']))
        oo = sorted(set(old['fails']) - set(new['fails']))
        row = {'context': name, 'fn': fn, 'checkerLine': line, 'injection': ('unconditional' if nth is None else 'call#%d' % nth),
               'oldExit': old['exit'], 'newExit': new['exit'],
               'oldFailCount': len(old['fails']), 'newFailCount': len(new['fails']),
               'falsePassesRemoved': fp, 'oldOnlyFails': oo,
               'sampleNewlyCaught': {k: new['fails'][k] for k in fp[:4]}}
        break
    if row is None:
        print('%-16s NO USABLE INJECTION (all attempts crashed the checker) - preserved' % name)
        continue
    results.append(row)
    print('%-16s inj=%-12s oldFails=%-3d newFails=%-3d falsePassesRemoved=%-3d oldOnly=%d'
          % (name, row['injection'], row['oldFailCount'], row['newFailCount'],
             len(row['falsePassesRemoved']), len(row['oldOnlyFails'])))
    for k, v in row['sampleNewlyCaught'].items():
        print('        + newly caught: %s  detail=%s' % (k, v))

json.dump({'results': results, 'preservedFailedAttempts': attempts},
          open(os.path.join(BASE, 'logs', 'p12-ten-context-controls.json'), 'w'), indent=1)
print('\ncontextsWithUsableInjection=%d/10' % len(results))
print('TOTAL falsePassesRemoved=%d  regressions=%d'
      % (sum(len(r['falsePassesRemoved']) for r in results), sum(len(r['oldOnlyFails']) for r in results)))
print('preservedFailedAttempts=%d' % len(attempts))
