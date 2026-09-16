"""Disposable synthetic fixture builder for bind/retain boundary probes.

Every ACCEPT/verdict string here is SYNTHETIC and is not project review evidence.
Nothing is written outside the caller-supplied temporary directory.
"""
import hashlib
import json
from pathlib import Path

INPUTS = Path('/private/tmp/opensip-design-corrections/claude-application-tools-review.v1/inputs')
DC = 'docs/coop/design-corrections/'
EVAL_REL = DC + 'evaluation-residual-dispositions.proposed.json'

AR = tuple(f'AR-{i:02d}' for i in range(1, 17))
FW = tuple(f'FW-{i:02d}' for i in range(1, 16))
INHERITED = tuple(f'DR-{i:03d}' for i in range(1, 12)) + tuple(f'DR-011-R{i:02d}' for i in range(1, 17))
OWNERS = tuple(f'DR-{i}' for i in range(201, 206))
EVAL_IDS = tuple(f'EV-{i:02d}' for i in range(1, 31))

FRESH_DESIGN_SESSION = 'aaaaaaaa-0000-4000-8000-000000000001'
FRESH_BLIND_SESSION = 'bbbbbbbb-0000-4000-8000-000000000002'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def wj(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + '\n')
    return sha(p)


def build(base, *, vendor='claude', design_session=FRESH_DESIGN_SESSION,
          blind_session=FRESH_BLIND_SESSION, blind_parent=None, assent_subject=None,
          assent_session=None, drop_assent=False, design_process=None,
          receipt_overrides=None, design_spec_overrides=None):
    """Return (receipt_path, out_path). All synthetic."""
    base = Path(base)
    root = base / 'root'
    snap = base / 'snapshot'
    (root).mkdir(parents=True, exist_ok=True)

    wj(snap / EVAL_REL, {'items': [{'id': i} for i in EVAL_IDS]})
    manifest_rel = DC + 'reviews/candidate-subject.v22.json'
    manifest_sha = wj(root / manifest_rel, {
        'standing': 'SYNTHETIC FIXTURE ONLY',
        'snapshotRoot': str(snap),
        'files': [{'path': EVAL_REL, 'sha256': sha(snap / EVAL_REL),
                   'bytes': (snap / EVAL_REL).stat().st_size}],
    })

    design_rel = DC + 'reviews/post-reset-review.v22/review.json'
    design_sha = wj(root / design_rel, {
        'standing': 'SYNTHETIC FIXTURE ONLY. Not actual review evidence.',
        'verdict': 'ACCEPT',
        'subjectManifestSha256': manifest_sha,
        'newMustIssues': [], 'newShouldIssues': [], 'newAdvisories': [],
        'arDispositions': {k: 'CARRIED-UNCHANGED' for k in AR},
        'fwDispositions': {k: 'CARRIED-UNCHANGED' for k in FW},
        'inheritedResidualDispositions': {k: 'CARRIED-UNCHANGED' for k in INHERITED},
        'scopedReviewOwnerDispositions': {
            k: {'disposition': 'ROUTED-ONLY', 'appliedByThisReview': False,
                'finalApplicationOutcomeGranted': False, 'scope': 'routing', 'basis': 'synthetic'}
            for k in OWNERS},
        'evaluationResidualDispositions': {k: 'CARRIED-UNCHANGED' for k in EVAL_IDS},
    })

    blind_rel = DC + 'reviews/consumer-b.v10/output/blind-review.json'
    blind_sha = wj(root / blind_rel, {
        'standing': 'SYNTHETIC FIXTURE ONLY.',
        'verdict': 'ACCEPT-RECONSTRUCTABLE',
        'subjectManifestSha256': manifest_sha,
        'newMustIssues': [], 'newShouldIssues': [], 'newAdvisories': [],
    })

    kit_rel = DC + 'reviews/consumer-b.v10/subject/consumer-input-manifest.json'
    wj(root / kit_rel, {'parentSubjectSha256': blind_parent or manifest_sha})

    if vendor == 'claude':
        dpub_rel, bpub_rel = 'pub/design-response.json', 'pub/blind-response.json'
        dpub = {'is_error': False, 'session_id': design_session, 'result': 'synthetic'}
        bpub = {'is_error': False, 'session_id': blind_session, 'result': 'synthetic'}
    else:
        dpub_rel, bpub_rel = 'pub/design-response.public.json', 'pub/blind-response.public.json'
        dpub = {'text': 'synthetic', 'stopReason': 'end_turn', 'sessionId': design_session}
        bpub = {'text': 'synthetic', 'stopReason': 'end_turn', 'sessionId': blind_session}
    dpub_sha = wj(root / dpub_rel, dpub)
    bpub_sha = wj(root / bpub_rel, bpub)

    assent_rel = DC + 'reviews/codex-post-reset.v1/design-assent.v22.json'
    assent_sha = wj(root / assent_rel, {
        'rootDesignAssent': True,
        'subjectManifestSha256': assent_subject or manifest_sha,
        'actualSessionId': assent_session or design_session,
        'independentReview': {'path': design_rel, 'sha256': design_sha},
        'unresolvedRootMustIssues': [], 'unresolvedRootShouldIssues': [],
        'advisoryApplicationAccount': [], 'contracts': [{'path': 'docs/x.md', 'sha256': 'd' * 64}],
    })
    if drop_assent:
        (root / assent_rel).unlink()

    assess_rel = DC + 'reviews/codex-post-reset.v1/blind-assessment.v10.json'
    assess_sha = wj(root / assess_rel, {
        'rootBlindAssent': True, 'fullRead': True, 'actualSessionId': blind_session,
        'parentSubjectSha256': manifest_sha,
        'review': {'path': blind_rel, 'sha256': blind_sha},
        'unresolvedRootMustIssues': [], 'unresolvedRootShouldIssues': [],
        'newAdvisoryApplicationAccount': [],
    })

    design_spec = {
        'role': 'independent-design', 'manifestPath': manifest_rel,
        'manifestSha256': manifest_sha, 'reviewPath': design_rel, 'reviewSha256': design_sha,
        'requiredVerdict': 'ACCEPT', 'publicResponsePath': dpub_rel,
        'publicResponseSha256': dpub_sha,
    }
    if design_process is not None:
        design_spec['processPath'] = 'pub/design-process.json'
        wj(root / 'pub/design-process.json', design_process)
    if design_spec_overrides:
        design_spec.update(design_spec_overrides)

    receipt = {
        'standing': 'SYNTHETIC disposable probe receipt. Not acceptance.',
        'designVersion': 'v22', 'consumerVersion': 'v10', 'applicationVersion': 'v3',
        'vendor': vendor, 'root': str(root),
        'reviewerPublicLabel': 'actual ' + vendor + ' independent reviewer',
        'design': design_spec,
        'blind': {
            'role': 'independent-blind', 'reviewPath': blind_rel, 'reviewSha256': blind_sha,
            'requiredVerdict': 'ACCEPT-RECONSTRUCTABLE', 'publicResponsePath': bpub_rel,
            'publicResponseSha256': bpub_sha, 'inputManifestPath': kit_rel,
            'parentSubjectSha256': manifest_sha,
        },
        'codexDesignAssent': {'path': assent_rel, 'sha256': assent_sha},
        'codexBlindAssessment': {'path': assess_rel, 'sha256': assess_sha},
    }
    if receipt_overrides:
        receipt.update(receipt_overrides)
    rp = base / 'receipt.json'
    wj(rp, receipt)
    return rp, base / 'bound.json', manifest_sha
