"""p06: reproduce all six canonical reference commands in the DISPOSABLE FULL copy.
No repinning. Capture command/exit/stdout/stderr; compare generated reports to frozen bytes."""
import hashlib, json, os, subprocess, sys

COPY = '/tmp/opensip-design-corrections/post-reset-review.v18/disposable-copy'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
REFDIR = 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v18'
refs = json.load(open(os.path.join(FROZEN, REFDIR, 'reference-checks.json')))

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else None

# report path is the argument after --report, if any
out = {'commands': [], 'copyRoot': COPY}
for c in refs['commands']:
    src = os.path.join(COPY, c['source'])
    src_sha = sha(src)
    rep_rel = None
    if '--report' in c['command']:
        rep_rel = c['command'][c['command'].index('--report') + 1]
    pre = sha(os.path.join(COPY, rep_rel)) if rep_rel else None
    r = subprocess.run(c['command'], cwd=COPY, capture_output=True, text=True)
    post = sha(os.path.join(COPY, rep_rel)) if rep_rel else None
    frozen_rep = sha(os.path.join(FROZEN, rep_rel)) if rep_rel else None
    # frozen log bytes for this command
    log_frozen = os.path.join(FROZEN, REFDIR, c['log'])
    frozen_log = open(log_frozen).read() if os.path.isfile(log_frozen) else None
    row = {
        'name': c['name'],
        'declaredSourceSha256': c['sourceSha256'],
        'actualSourceSha256': src_sha,
        'sourceShaMatches': src_sha == c['sourceSha256'],
        'declaredExit': c['exitCode'],
        'actualExit': r.returncode,
        'exitMatches': r.returncode == c['exitCode'],
        'reportPath': rep_rel,
        'reportShaInFrozenSnapshot': frozen_rep,
        'reportShaBeforeRun': pre,
        'reportShaAfterRun': post,
        'regeneratedReportEqualsFrozenBytes': (post == frozen_rep) if rep_rel else None,
        'stdoutLen': len(r.stdout), 'stderrLen': len(r.stderr),
        'stdoutTail': r.stdout[-600:],
        'stderrTail': r.stderr[-600:],
        'frozenLogEqualsStdout': (frozen_log == r.stdout) if frozen_log is not None else None,
        'frozenLogSha256': hashlib.sha256(frozen_log.encode()).hexdigest() if frozen_log is not None else None,
        'actualStdoutSha256': hashlib.sha256(r.stdout.encode()).hexdigest(),
    }
    out['commands'].append(row)
    print('%-18s exit=%s(decl %s) srcSha=%s reportBytesEqFrozen=%s logEqStdout=%s'
          % (c['name'], r.returncode, c['exitCode'], row['sourceShaMatches'],
             row['regeneratedReportEqualsFrozenBytes'], row['frozenLogEqualsStdout']))

out['allExitsMatch'] = all(x['exitMatches'] for x in out['commands'])
out['allSourceShasMatch'] = all(x['sourceShaMatches'] for x in out['commands'])
out['allReportsByteIdentical'] = all(x['regeneratedReportEqualsFrozenBytes'] is not False for x in out['commands'])
print('\nallExitsMatch=%s allSourceShasMatch=%s allReportsByteIdentical=%s'
      % (out['allExitsMatch'], out['allSourceShasMatch'], out['allReportsByteIdentical']))
json.dump(out, open('/tmp/opensip-design-corrections/post-reset-review.v18/logs/p06-six-commands.json', 'w'), indent=1)
