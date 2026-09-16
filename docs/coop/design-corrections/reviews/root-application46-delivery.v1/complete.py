"""Retain completed application evidence; never changes reviewed after-images."""
from pathlib import Path
import hashlib
import json
import shutil

base = Path('/tmp/opensip-design-corrections')
root = Path('/Users/sb/code/opensip-ai/opensip_arch')
reviews = root / 'docs/coop/design-corrections/reviews'
out = base / 'root-application46-delivery.v1'

def load(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ref(path):
    return {'path': str(path.relative_to(root)), 'sha256': sha(path)}

activation_path = root / 'docs/coop/design-corrections/application-activation.v1.json'
activation = load(activation_path)
manifest_path = root / activation['applicationManifest']['path']
manifest = load(manifest_path)
assert sha(manifest_path) == activation['applicationManifest']['sha256'] == 'dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7'
review_path = root / activation['independentApplicationReview']['path']
assert sha(review_path) == activation['independentApplicationReview']['sha256'] == '375b2e9daa57a07c7e5e2bfb203c7bd94528f5d4bdda704c518de5085bfb5eb4'
assert load(review_path)['verdict'] == 'ACCEPT'
assent = reviews / 'root-application46-substantive-assessment.v1/assessment.json'
assert load(assent)['authority']['rootApplicationAssent'] is True
checks = load(base / 'applied-reference.v46/reference-checks.json')
assert checks['passed'] and checks['applicationManifestSha256'] == sha(manifest_path)
assert len(checks['commands']) == 7
for row in checks['commands']:
    assert row['exitCode'] == 0 and not row['timedOut']
    assert sha(root / row['source']) == row['sourceSha256']
    for stream in ('stdout', 'stderr'):
        if stream + 'Sha256' in row:
            assert sha(base / 'applied-reference.v46' / (row['name'] + '.' + stream)) == row[stream + 'Sha256']
evaluator = load(base / 'applied-reference.v46/evaluator3/report.json')
assert evaluator['passed'] and evaluator['sourcePinsValid'] and not evaluator['changedOrMissing']
assert len(evaluator['checks']) == 17
for row in evaluator['checks']:
    assert row['exitCode'] == 0 and not row['timedOut']
    for stream in ('stdout', 'stderr'):
        assert sha(base / 'applied-reference.v46/evaluator3' / (row['name'] + '.' + stream)) == row[stream + 'Sha256']
verification = load(base / 'applied-verification.v46/application-verification.json')
assert verification['passed'] and verification['appliedFilesVerified'] == 197
assert verification['frozenAcceptedFilesVerified'] == 12920
assert verification['unperformedQualificationGates'] == 32
for row in manifest['files']:
    assert sha(root / row['path']) == row['sha256']

retained = []
for name in ('applied-reference.v46', 'applied-verification.v46'):
    src, dst = base / name, reviews / name
    for path in sorted(src.rglob('*')):
        if not path.is_file():
            continue
        target = dst / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == path.read_bytes()
        else:
            shutil.copyfile(path, target)
        assert sha(target) == sha(path)
        retained.append({**ref(target), 'bytes': target.stat().st_size})

record = {
    'standing': 'Completed OpenSIP architecture/design/reference correction and accepted-document application. Design approved for implementation; product implementation is a separate next task.',
    'designApprovedForImplementation': True,
    'activation': ref(activation_path),
    'applicationManifest': ref(manifest_path),
    'actualClaudeApplicationReview': ref(review_path),
    'codexApplicationAssent': ref(assent),
    'appliedReferenceResults': ref(reviews / 'applied-reference.v46/reference-checks.json'),
    'appliedVerification': ref(reviews / 'applied-verification.v46/application-verification.json'),
    'historicalCheckerProvenance': ref(reviews / 'applied-verification.v46/historical-checker-provenance.json'),
    'remainingRequiredDesignFindings': [],
    'counts': {'appliedFilesVerified': 197, 'frozenAcceptedFilesVerified': 12920, 'referenceGroups': 6, 'observedCommandReceipts': 7, 'evaluatorChildren': 17, 'acceptedCondition2Rows': 28, 'unperformedProductGates': 32, 'plannedUnperformedRecoveryCases': 54},
    'nonblockingAdvisories': 'The three application46 advisories and reviewer support-count correction are dispositioned in the pinned Codex assent. Source/blind advisories and historical evidence retain their exact scope.',
    'continuingImplementationObligations': ['All32 product qualification gates and54 recovery cases remain unperformed.', 'D9-SUCCESSOR-ARTIFACT remains mandatory on DR-007/DR-011-R08; future owning-unit artifact publication remains owed.', 'TCB-SCOPE-01 is one accepted scope assumption with13 dependent evaluation rows plus DR-011-R12; a scope change reopens them jointly.', 'Host analysis receipt/view-producer verification and selected planning/build/feature obligations remain part of implementation.'],
    'authority': {'implementationAuthorized': False, 'productQualificationClaimed': False, 'productImplementationPerformed': False, 'commitPushPerformed': False},
    'retainedEvidenceFiles': retained,
    'passed': True,
}
(out / 'completion.json').write_text(json.dumps(record, indent=2) + '\n')
(out / 'README.md').write_text('''# Design approved for implementation

The OpenSIP design correction and review task is complete. Actual Claude accepted the final design and documentation application; Codex assessed the substantive reviews and independently validated the blind consumer exports. All required design findings are resolved.

The reviewed application is installed in the working tree. All six reference groups, including seventeen evaluator checks, passed after application. Final verification confirmed all197 applied files and all12920 accepted source files, current accounting, links and catalogue. Historical checker failures are retained with their specific reviewed-document divergence account; they are not relabelled as passes.

Use the [product contract index](../../../../v2/contracts/product-v1/README.md), [current readiness register](../../../../v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness), [repository layout](../../../../v2/architecture/14-repository-and-module-layout.md) and [implementation plan](../../../../v2/architecture/implementation-boundaries-and-build-plan.md). The central D-372 readiness account governs current approval; dated author/proposal statements and earlier review queues remain historical provenance, not pending new design reviews.

The [completion record](completion.json) pins the actual review, root assent, activation and applied verification. The [root application assessment](../root-application46-substantive-assessment.v1/assessment.json) accounts for the three nonblocking application advisories and corrects the review's support-file count without altering its bytes.

Implementation, platform qualification and release evidence remain future work. All32 product gates and54 planned recovery cases remain unperformed; the D9 publication obligation and shared trust assumption remain explicit. No product implementation, new commit or push was performed. Separate user authorization starts implementation.
''')
destination = reviews / out.name
for path in sorted(out.iterdir()):
    if path.is_file():
        target = destination / path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == path.read_bytes()
        else:
            shutil.copyfile(path, target)
print(json.dumps({'designApprovedForImplementation': True, 'completionSha256': sha(out / 'completion.json'), 'evidenceFilesRetained': len(retained), 'implementationAuthorized': False}))
