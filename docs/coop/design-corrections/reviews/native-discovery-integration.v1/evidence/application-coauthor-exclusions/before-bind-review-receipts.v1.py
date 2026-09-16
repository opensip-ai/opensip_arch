"""Bind an external input receipt. Does not assemble, freeze, launch, or grade.

Root runs this only after frozen evaluator3 + actual independent review + NEW
blind + Codex assessments. A missing or historical-source21 receipt must refuse.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def require_sha(path, expected, label):
    actual = sha(path)
    assert actual == expected, label + ' digest mismatch: ' + actual
    return actual


def require_coverage(design, expected_evaluation_ids):
    ar = design.get('arDispositions') or {}
    fw = design.get('fwDispositions') or {}
    inherited = design.get('inheritedResidualDispositions') or {}
    owners = design.get('scopedReviewOwnerDispositions') or {}
    assert set(ar) == set(C.AR_IDS), 'Design review must dispose all 16 AR ids'
    assert set(fw) == set(C.FW_IDS), 'Design review must dispose all 15 FW ids'
    assert set(inherited) == set(C.INHERITED_IDS), (
        'Design review must dispose all 27 inherited ids (11 parents + 16 residuals)'
    )
    assert set(owners) == set(C.OWNER_IDS), 'Design review must account DR-201..205'
    assert set(design.get('evaluationResidualDispositions') or {}) == expected_evaluation_ids, 'Design review must preserve all30 individual evaluation dispositions'
    return {
        'evaluationResiduals':len(expected_evaluation_ids),
        'ar': 16,
        'fw': 15,
        'inherited': 27,
        'owners': 5,
    }


def require_root_design_assent(assent, expected_subject, review_spec, session_id):
    assert assent.get('rootDesignAssent') is True, 'Explicit root design assent required'
    assert assent.get('subjectManifestSha256') == expected_subject, 'Root assent subject mismatch'
    assert assent.get('actualSessionId') == session_id, 'Root assent reviewer session mismatch'
    assert assent.get('independentReview') == {
        'path': review_spec['reviewPath'], 'sha256': review_spec['reviewSha256']
    }, 'Root assent names different independent review'
    for key in ('unresolvedRootMustIssues', 'unresolvedRootShouldIssues'):
        assert type(assent.get(key)) is list and not assent[key], 'Unresolved root design findings: ' + key


def bind_one(root, spec, vendor, expected_subject, label):
    review_path = root / spec['reviewPath']
    require_sha(review_path, spec['reviewSha256'], label + ' review')
    review = load(review_path)
    E.require_verdict(review, spec['requiredVerdict'], label)
    E.require_findings_none(review, label)
    digest = E.review_subject_digest(review)
    assert digest == expected_subject, label + ' subjectManifestSha256 mismatch'
    public_path = root / spec['publicResponsePath']
    require_sha(public_path, spec['publicResponseSha256'], label + ' public envelope')
    decoded = E.decode_public_file(public_path, vendor)
    process = None
    if spec.get('processPath'):
        process = load(root / spec['processPath'])
        E.refuse_coauthor_process(process, spec['role'])
        proc_session = process.get('sessionId') or process.get('session_id')
        if proc_session:
            assert proc_session == decoded['sessionId'], (
                label + ' process session does not match public envelope'
            )
    assert decoded['sessionId'] not in C.KNOWN_GROK_COAUTHOR_SESSIONS, (
        label + ' session is a known Grok coauthor session'
    )
    if vendor == 'claude':
        assert decoded['sessionId'] != C.HISTORICAL_CLAUDE_EXCLUDED_SESSION
    return {'review': review, 'decoded': decoded, 'path': spec['reviewPath']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--receipt', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    receipt = load(a.receipt)
    assert a.out.resolve() != a.receipt.resolve()
    assert not a.out.exists(), 'Never overwrite a bound receipt'
    standing = receipt.get('standing', '')
    assert receipt.get('readyForAssembly') is not True, (
        'Input receipt must not claim readyForAssembly; bind writes that on success'
    )
    assert 'SHAPE ONLY' not in standing, 'Example/shape receipt is not bindable'
    vendor = receipt['vendor']
    assert vendor in ('grok', 'claude')
    root = Path(receipt['root']).resolve()
    design_spec = receipt['design']
    blind_spec = receipt['blind']
    assert design_spec['role'] == 'independent-design'
    assert blind_spec['role'] == 'independent-blind'
    assert design_spec['requiredVerdict'] == 'ACCEPT'
    assert blind_spec['requiredVerdict'] == 'ACCEPT-RECONSTRUCTABLE'
    assert design_spec['manifestSha256'] == blind_spec['parentSubjectSha256']
    dv = receipt['designVersion']
    if dv != 'v21':
        assert design_spec['manifestSha256'] != C.HISTORICAL_V21_SUBJECT_SHA256, (
            'Evaluator3 successor must not bind historical frozen source21 bytes'
        )
    manifest_path = root / design_spec['manifestPath']
    require_sha(manifest_path, design_spec['manifestSha256'], 'design manifest')
    expected = design_spec['manifestSha256']
    design = bind_one(root, design_spec, vendor, expected, 'independent design')
    blind = bind_one(root, blind_spec, vendor, expected, 'fresh blind')
    assert design['decoded']['sessionId'] != blind['decoded']['sessionId'], (
        'Blind consumer must be a fresh session'
    )
    manifest=load(manifest_path)
    eval_rel='docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'
    eval_entry=next(r for r in manifest['files'] if r['path']==eval_rel)
    eval_source=Path(manifest['snapshotRoot'])/eval_rel
    require_sha(eval_source,eval_entry['sha256'],'accepted evaluation residual inventory')
    expected_evaluation_ids={r['id'] for r in load(eval_source)['items']}
    assert len(expected_evaluation_ids)==30
    coverage = require_coverage(design['review'], expected_evaluation_ids)
    input_manifest = load(root / blind_spec['inputManifestPath'])
    assert input_manifest['parentSubjectSha256'] == expected
    assent = load(root / receipt['codexDesignAssent']['path'])
    require_sha(
        root / receipt['codexDesignAssent']['path'],
        receipt['codexDesignAssent']['sha256'],
        'codex design assent',
    )
    require_root_design_assent(assent, expected, design_spec, design['decoded']['sessionId'])
    assert isinstance(assent.get('advisoryApplicationAccount'), list)
    assert isinstance(assent.get('contracts'), list) and assent['contracts']
    assessment = load(root / receipt['codexBlindAssessment']['path'])
    require_sha(
        root / receipt['codexBlindAssessment']['path'],
        receipt['codexBlindAssessment']['sha256'],
        'codex blind assessment',
    )
    assert assessment.get('rootBlindAssent') is True
    assert assessment.get('fullRead') is True
    assert assessment.get('actualSessionId') == blind['decoded']['sessionId']
    assert assessment.get('parentSubjectSha256') == expected
    assert all(assessment['review'][k] == {'path': blind_spec['reviewPath'], 'sha256': blind_spec['reviewSha256']}[k] for k in ('path', 'sha256'))
    assert all(
        type(assessment.get(k)) is list and not assessment[k]
        for k in ('unresolvedRootMustIssues', 'unresolvedRootShouldIssues')
    )
    blind_advisories = blind['review'].get('newAdvisories', blind['review'].get('advisories', []))
    assert type(blind_advisories) is list
    account = assessment['newAdvisoryApplicationAccount']
    assert type(account) is list
    assert {x['id'] for x in account} == {x['id'] for x in blind_advisories}
    label = receipt.get('reviewerPublicLabel')
    assert isinstance(label, str) and 'independent' in label.lower()
    assert 'coauthor' not in label.lower()
    if vendor == 'grok':
        assert 'actual grok' in label.lower()
        assert 'claude' not in label.lower()
    if vendor == 'claude':
        assert 'actual claude' in label.lower()
    bound = {
        'standing': 'BOUND RECEIPT ONLY. Not application, not activation, not a grade.',
        'readyForAssembly': True,
        'vendor': vendor,
        'reviewerPublicLabel': label,
        'designVersion': dv,
        'consumerVersion': receipt['consumerVersion'],
        'applicationVersion': receipt['applicationVersion'],
        'root': str(root),
        'designSubject': {
            'path': design_spec['manifestPath'],
            'sha256': expected,
        },
        'independentDesignReview': {
            'path': design_spec['reviewPath'],
            'sha256': design_spec['reviewSha256'],
            'verdict': 'ACCEPT',
            'sessionId': design['decoded']['sessionId'],
            'publicResponsePath': design_spec['publicResponsePath'],
        },
        'freshBlindConsumerReview': {
            'path': blind_spec['reviewPath'],
            'sha256': blind_spec['reviewSha256'],
            'verdict': 'ACCEPT-RECONSTRUCTABLE',
            'sessionId': blind['decoded']['sessionId'],
            'publicResponsePath': blind_spec['publicResponsePath'],
            'inputManifestPath': blind_spec['inputManifestPath'],
            'custodyPath': blind_spec.get('custodyPath'),
        },
        'codexDesignAssent': receipt['codexDesignAssent'],
        'codexBlindAssessment': receipt['codexBlindAssessment'],
        'coveragePresent': coverage,
        'historicalSource21NotBound': expected != C.HISTORICAL_V21_SUBJECT_SHA256,
        'implementationAuthorized': False,
        'qualificationClaimed': False,
        'd9DesignLevelBlocker': False,
        'productGatesUnperformed': True,
        'inputReceiptSha256': sha(a.receipt),
        'launch': receipt.get('launch', {}),
    }
    a.out.write_text(json.dumps(bound, indent=2) + '\n')
    print(json.dumps({
        'readyForAssembly': True,
        'vendor': vendor,
        'designSession': design['decoded']['sessionId'],
        'blindSession': blind['decoded']['sessionId'],
        'subject': expected,
        'out': str(a.out),
    }))


if __name__ == '__main__':
    main()
