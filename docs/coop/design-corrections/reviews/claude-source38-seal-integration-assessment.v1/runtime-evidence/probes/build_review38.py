"""Assemble review.json for the source38 SEAL integration assessment from this runtime's actual receipts."""
import glob, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1'
R = RT + '/receipts'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(p):
    return json.load(open(p))


runs = []
for f in sorted(glob.glob(R + '/runs/*.run.json')):
    d = load(f)
    base = f[:-len('.run.json')]
    parsed = None
    try:
        j = json.loads(open(base + '.stdout').read())
        if isinstance(j, dict):
            parsed = {k: j[k] for k in ('passed', 'count', 'counts', 'failedCount', 'sourcePinsValid', 'changedOrMissing') if k in j}
            if 'failed' in j:
                parsed['failed'] = len(j['failed']) if isinstance(j['failed'], list) else j['failed']
    except ValueError:
        parsed = 'no JSON stdout (see stderr receipt)'
    report = glob.glob(R + '/runs/' + d['name'] + '.' + d['tree'] + '.report.json')
    runs.append({'name': d['name'], 'tree': d['tree'], 'command': d['command'], 'exitCode': d['exitCode'], 'seconds': d['seconds'],
                 'scriptSha256': d['scriptSha256'], 'treeUnchanged': d['treeUnchanged'], 'stdoutSha256': d['stdoutSha256'],
                 'stderrSha256': d['stderrSha256'], 'parsed': parsed, 'receipt': os.path.relpath(f, RT),
                 'report': {'path': os.path.relpath(report[0], RT), 'sha256': sha(report[0])} if report else None})

authored = load(RT + '/review.authored.json')
review = dict(authored)
review['inputs'] = {
    'setup': load(R + '/setup38.json'),
    'readOnlyImmutability': {'root': load(R + '/read-only-inventory.verify.successor-sealCorrection-faultCorrection-final38Reference.json'),
                             'ownV1V2': load(R + '/read-only-inventory.verify.v1-v2.json')},
    'rootProposalFileSha256': {os.path.relpath(p, '/tmp/opensip-design-corrections'): sha(p) for p in sorted(
        glob.glob('/tmp/opensip-design-corrections/root-final38-seal-correction.v1/**/*', recursive=True)
        + glob.glob('/tmp/opensip-design-corrections/root-source38-fault-check-correction.v1/*')) if os.path.isfile(p)},
    'final38FailureEvidence': {'analysisSealStderrSha256': sha('/tmp/opensip-design-corrections/root-final38-reference.v1/evaluator3/analysis-seal.stderr'),
                               'referenceChecksSha256': sha('/tmp/opensip-design-corrections/root-final38-reference.v1/reference-checks.json')},
}
review['probes'] = {
    'sealBoundary': {t: load(R + '/probe-seal-boundary.' + t + '.json')['rows'] for t in ('source38-integrated', 'source38-seal-before')},
    'faultParity': load(R + '/probe-fault-parity.source38-integrated.json'),
    'securityAnalysisSealCaseScan': load(R + '/security-analysis-seal-case-scan.json'),
    'scriptSha256': {os.path.basename(p): sha(p) for p in sorted(glob.glob(RT + '/probes/*.py'))},
}
review['focusedReceipts'] = runs
json.dump(review, open(RT + '/review.json', 'w'), indent=1)
print(json.dumps({'reviewJsonSha256': sha(RT + '/review.json'), 'runs': [(r['name'], r['tree'], r['exitCode']) for r in runs]}, indent=1))
