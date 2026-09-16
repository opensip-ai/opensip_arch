"""Assemble future-effective application records AFTER a bound independent receipt.

Does not apply documentation, write activation, or award grades.
Requires bind-review-receipts.v1.py output with readyForAssembly true.
Public envelopes are decoded by vendor; this is not a Claude-to-Grok rename.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E


def review_subject_digest(record):
    return E.review_subject_digest(record)


p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--bound-receipt', type=Path, required=True)
p.add_argument('--design-version', required=True)
p.add_argument('--consumer-version', required=True)
p.add_argument('--application-version', required=True)
p.add_argument('--draft', type=Path, required=True)
p.add_argument('--source-delta', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve()
out = a.out.resolve()
dc = 'docs/coop/design-corrections/'
bound = json.loads(a.bound_receipt.read_text())
assert bound.get('readyForAssembly') is True
assert bound['implementationAuthorized'] is False
assert bound['designVersion'] == a.design_version
assert bound['consumerVersion'] == a.consumer_version
assert bound['applicationVersion'] == a.application_version
assert Path(bound['root']).resolve() == root
vendor = bound['vendor']
reviewer_label = bound['reviewerPublicLabel']
assert 'coauthor' not in reviewer_label.lower()

accepted_files = {}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_path(rel):
    return Path(design_manifest['snapshotRoot']) / rel if rel in accepted_files else root / rel


def ref(rel, selector=None):
    v = {'path': rel, 'sha256': digest(source_path(rel))}
    if selector:
        v['selector'] = selector
    return v


def load(rel):
    return json.loads(source_path(rel).read_text())


dv = a.design_version
bv = a.consumer_version
av = a.application_version
manifest_ref = ref(bound['designSubject']['path'])
assert manifest_ref['sha256'] == bound['designSubject']['sha256']
design_manifest = load(manifest_ref['path'])
design_ref = ref(bound['independentDesignReview']['path'])
assert design_ref['sha256'] == bound['independentDesignReview']['sha256']
design = load(design_ref['path'])
assert design.get('verdict', design.get('overallVerdict')) == 'ACCEPT'
E.require_findings_none(design, 'independent design')
assert review_subject_digest(design) == manifest_ref['sha256']

blind_ref = ref(bound['freshBlindConsumerReview']['path'])
assert blind_ref['sha256'] == bound['freshBlindConsumerReview']['sha256']
blind = load(blind_ref['path'])
assert blind['verdict'] == 'ACCEPT-RECONSTRUCTABLE'
E.require_findings_none(blind, 'fresh blind')

blind_input_ref = ref(bound['freshBlindConsumerReview']['inputManifestPath'])
blind_input = load(blind_input_ref['path'])
assert blind_input['parentSubjectSha256'] == manifest_ref['sha256']

design_public = E.decode_public_file(root / bound['independentDesignReview']['publicResponsePath'], vendor)
blind_public = E.decode_public_file(root / bound['freshBlindConsumerReview']['publicResponsePath'], vendor)
assert design_public['sessionId'] == bound['independentDesignReview']['sessionId']
assert blind_public['sessionId'] == bound['freshBlindConsumerReview']['sessionId']
assert design_public['sessionId'] != blind_public['sessionId']
assert design_public['sessionId'] not in C.KNOWN_GROK_COAUTHOR_SESSIONS
assert blind_public['sessionId'] not in C.KNOWN_GROK_COAUTHOR_SESSIONS

blind_assessment_ref = ref(bound['codexBlindAssessment']['path'])
assert blind_assessment_ref['sha256'] == bound['codexBlindAssessment']['sha256']
blind_assessment = load(blind_assessment_ref['path'])
assert blind_assessment['rootBlindAssent'] is True and blind_assessment['fullRead'] is True
assert blind_assessment['actualSessionId'] == blind_public['sessionId']
assert blind_assessment['parentSubjectSha256'] == manifest_ref['sha256']
assert all(blind_assessment['review'][k] == blind_ref[k] for k in ('path', 'sha256'))
assert all(
    type(blind_assessment.get(k)) is list and not blind_assessment[k]
    for k in ('unresolvedRootMustIssues', 'unresolvedRootShouldIssues')
)
blind_new_advisories = blind.get('newAdvisories', blind.get('advisories', []))
assert type(blind_new_advisories) is list
blind_advisory_account = blind_assessment['newAdvisoryApplicationAccount']
assert type(blind_advisory_account) is list
assert len({x['id'] for x in blind_advisory_account}) == len(blind_advisory_account)
assert {x['id'] for x in blind_advisory_account} == {x['id'] for x in blind_new_advisories}

accepted_files = {r['path']: r for r in design_manifest['files']}
for row in design_manifest['files']:
    assert digest(Path(design_manifest['snapshotRoot']) / row['path']) == row['sha256'], (
        'Frozen design drift: ' + row['path']
    )

assert set(design.get('arDispositions') or {}) == set(C.AR_IDS)
assert set(design.get('fwDispositions') or {}) == set(C.FW_IDS)
assert set(design.get('inheritedResidualDispositions') or {}) == set(C.INHERITED_IDS)

draft_base = a.draft.resolve()
source_delta = json.loads(a.source_delta.read_text())
assert source_delta['designSubjectSha256'] == manifest_ref['sha256']
assert source_delta['unexpectedLiveDeltas'] == []
for row in source_delta['files']:
    rel = row['path']
    assert rel in accepted_files and accepted_files[rel]['sha256'] == row['afterSha256']
    current = digest(root / rel) if (root / rel).is_file() else None
    assert current == row['beforeSha256'], 'Preserve changed live source: ' + rel
for edit in json.loads((draft_base / 'documentation-proposal.json').read_text())['edits']:
    path = root / edit['path']
    current = digest(path) if path.exists() else None
    assert current == edit['beforeSha256'], 'Draft must be rebased to preserve later user changes: ' + edit['path']
assert not out.exists(), 'Never overwrite an earlier final application package'
out.mkdir()
files = out / 'files'
shutil.copytree(draft_base / 'files', files)
for row in source_delta['files']:
    rel = row['path']
    target = files / rel
    assert not target.exists(), 'Source delta overlaps documentation draft: ' + rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path(rel), target)
shutil.copyfile(a.source_delta, out / 'accepted-source-application-delta.json')
shutil.copyfile(a.bound_receipt, out / 'bound-review-receipt.json')
for rel in ['docs/operations/generate-current-design-catalog.py', dc + 'finalize-application.v1.py']:
    q = files / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path('/tmp/opensip-design-corrections/application-assembly.v1/files') / rel, q)
activation = dc + 'application-activation.v1.json'
effective = (
    'Effective only when D-372 activation binds the exact application manifest '
    'and actual independent final application ACCEPT; staged text alone grants no grade.'
)


def writej(rel, obj):
    q = files / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(json.dumps(obj, indent=2) + '\n')


def writet(rel, text):
    q = files / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(text)


def evidence(selector):
    return dict(design_ref, selector=selector)


scoped = {k: v for k, v in design['scopedReviewOwnerDispositions'].items() if k.startswith('DR-')}


def owner_scope_is_accounted(v):
    if v.get('disposition') in ('ACCEPT', 'ACCEPT_SCOPED'):
        return True
    if v.get('disposition') == 'ROUTED-ONLY':
        return (
            v.get('appliedByThisReview') is False
            and v.get('finalApplicationOutcomeGranted') is False
            and all(type(v.get(k)) is str and bool(v[k].strip()) for k in ('scope', 'basis'))
        )
    if v.get('disposition') != 'ROUTING-ASSESSED-ONLY-NOT-APPLIED':
        return False
    flags = [v[k] for k in ('finalApplicationOutcomeGranted', 'appliedByThisReview') if k in v]
    if not flags or any(x is not False for x in flags):
        return False
    if 'finalApplicationOutcomeGranted' in v:
        return True
    return (
        v.get('authority') in (
            'Five owner routing assessments do not grant a final application outcome.',
            'Five owner routing assessments do not grant a final application outcome and are not a grade.',
        )
        and all(type(v.get(k)) is str and bool(v[k].strip()) for k in ('scope', 'basis'))
    )


assert set(scoped) == set(C.OWNER_IDS) and all(owner_scope_is_accounted(v) for v in scoped.values())
writej(
    dc + 'review-owner-dispositions.v1.json',
    {
        'standing': effective,
        'historicalGradesExtended': False,
        'designSubject': manifest_ref,
        'independentReview': design_ref,
        'records': [
            dict(
                v,
                id=k,
                reviewEvidence=evidence('/scopedReviewOwnerDispositions/' + k),
                applicationDisposition='ACCEPT-DESIGN',
                gradeAuthority=(
                    'The design review accepted routing only. A new subject-specific '
                    'outcome requires substantive assessment by the fresh final application '
                    'reviewer; no historical grade is extended.'
                ),
                finalApplicationReviewBinding=activation,
            )
            for k, v in scoped.items()
        ],
        'activation': activation,
        'implementationAuthorized': False,
    },
)
register_rel = 'docs/v2/architecture/08-decision-and-readiness-register.md'
register = (files / register_rel).read_text()
old_owner = 'This is a new subject-specific design review.'
assert register.count(old_owner) == 5
register = register.replace(
    old_owner,
    'The new subject-specific outcome requires the fresh final application review '
    'bound by D-372 activation; the earlier independent design review accepted routing only.',
)
writet(register_rel, register)
rows = json.loads(Path('/tmp/opensip-design-corrections/application-assembly.v1/row-map-draft.json').read_text())['rows']
assert [r['id'] for r in rows] == list(C.CONDITION2_IDS)
for row in rows:
    row['designGrade'] = row.pop('proposedDesignGrade')
    row['independentGrade'] = 'ACCEPT-DESIGN'
    row['effectiveWhen'] = effective
    row['independentDesignReview'] = design_ref
    row['independentApplicationGradeBinding'] = activation
    row['resolveInheritedSourcesAgainst'] = manifest_ref
    for s in row['productSuccessors']:
        assert s['path'] in accepted_files, 'Successor absent from accepted subject: ' + s['path']
        s['sha256'] = accepted_files[s['path']]['sha256']
        assert digest(source_path(s['path'])) == s['sha256'], 'Frozen accepted source changed: ' + s['path']
writej(
    dc + 'readiness-row-map.v1.json',
    {
        'standing': effective,
        'authority': 'D-367/D-371/D-372 bounded complete intended product',
        'condition2AffectedSet': [r['id'] for r in rows],
        'excludedRows': C.CONDITION2_EXCLUDED,
        'rows': rows,
        'condition5': 'NOT MET',
        'productQualification': False,
    },
)
source = dc + 'correction-crosswalk.proposed.json'
old = load(source)
ars = []
for i, row in enumerate(old['items']):
    v = {k: row[k] for k in ['id', 'obligation', 'contract', 'selector', 'unit', 'ownerRows']}
    v.update(
        sourceItem=ref(source, '/items/' + str(i)),
        independentDisposition=design['arDispositions'][row['id']],
        reviewEvidence=evidence('/arDispositions/' + row['id']),
        contractSha256=digest(source_path(row['contract'])),
        referenceEvidence=[dict(ref(x), resolveAgainst='accepted design snapshot') for x in row['evidence']],
    )
    v.update(
        applicationDisposition='ACCEPT-DESIGN',
        gradeAuthority=(
            'The literal independent design disposition is preserved. CARRIED-UNCHANGED '
            'is not a new grade; the fresh final application reviewer must substantively '
            'assess this proposed outcome.'
        ),
        finalApplicationReviewBinding=activation,
    )
    ars.append(v)
assert [x['id'] for x in ars] == list(C.AR_IDS)
writej(
    dc + 'correction-crosswalk.applied.v1.json',
    {
        'standing': effective,
        'items': ars,
        'fallowDispositions': design['fwDispositions'],
        'fallowReviewEvidence': evidence('/fwDispositions'),
        'fallowApplicationDispositions': {
            k: {
                'applicationDisposition': 'ACCEPT-DESIGN',
                'gradeAuthority': (
                    'Preserved CARRIED-UNCHANGED is not a new grade. This outcome requires '
                    'substantive fresh final application review and activation.'
                ),
                'finalApplicationReviewBinding': activation,
            }
            for k in design['fwDispositions']
        },
        'sourceMap': ref(dc + 'current-source-map.proposed.md'),
        'activation': activation,
    },
)
assert set(design['fwDispositions']) == set(C.FW_IDS)
source = dc + 'evaluation-residual-dispositions.proposed.json'
old = load(source)
evals = []
for i, row in enumerate(old['items']):
    v = dict(row)
    v['reviewStatus'] = 'ACCEPT-DESIGN'
    v['sourceItem'] = ref(source, '/items/' + str(i))
    v['reviewEvidence'] = evidence('/inheritedResidualDispositions/DR-011-R12')
    v['effectiveWhen'] = effective
    v['independentDisposition'] = design['inheritedResidualDispositions']['DR-011-R12']
    v['gradeAuthority'] = (
        'Fresh final application review must substantively assess this proposed design '
        'grade; the design review only carried this inherited account unchanged.'
    )
    v['finalApplicationReviewBinding'] = activation
    evals.append(v)
assert len(evals) == C.EVALUATION_RESIDUAL_COUNT
writej(
    dc + 'evaluation-residual-dispositions.applied.v1.json',
    {
        'standing': effective,
        'items': evals,
        'historicalCandidateStandingChanged': False,
        'activation': activation,
    },
)
_d9_rel = dc + 'native/native-evidence.schemas.v2.json'
_d9_ob = load(_d9_rel)['x-opensip-public-route-registry']['successorArtifactObligation']
assert _d9_ob['standing'].startswith('MANDATORY, LIVE and CROSS-UNIT')
assert _d9_ob['owedBy'] == 'the D9 exit-contract unit'
assert 'host-invariant' not in load('docs/coop/artifacts/d9-exit-contract.v1.14.json')[
    'scenarioAxesSchema'
]['properties']['faultCause']['enum']
D9_CARRIED = {
    'id': 'D9-SUCCESSOR-ARTIFACT',
    'standing': 'LIVE, MANDATORY, CROSS-UNIT AND UNDISCHARGED AT APPLICATION',
    'owedBy': _d9_ob['owedBy'],
    'owed': _d9_ob['what'],
    'obligationSource': ref(_d9_rel, '/x-opensip-public-route-registry/successorArtifactObligation'),
    'selectedCompositionIsComplete': ref(dc + 'workflows/schemas/common.schema.json', '/$defs/D9FaultCause'),
    'inheritedArtifactUnchanged': ref(
        'docs/coop/artifacts/d9-exit-contract.v1.14.json',
        '/scenarioAxesSchema/properties/faultCause/enum',
    ),
    'enforcedInAcceptedSource': ref(dc + 'check-integration.py'),
    'whyStillOwed': (
        'A consumer validating against the inherited artifact alone would refuse a lawful '
        'host-invariant operational-failed termination that the selected composition emits. The product '
        'admission schema, the workflow mapper, the route registry and workflows-and-surfaces.md §9 all '
        'carry the twelfth cause, so no admitted current consumer is forced to the inherited eleven; the '
        'gap is confined to the historical artifact, which keeps its exact bytes as the evidence that this '
        'IS an extension.'
    ),
    'notDischargedBy': (
        'Condition 1 MET, ACCEPT-DESIGN on DR-007 or DR-011-R08, this application, its '
        'activation, or the final independent application review. Those grade the inherited residual at '
        'design level. Publishing the successor artifact is a separate act by the owning unit and needs its '
        'own independent review. Repinning or editing d9-exit-contract.v1.14.json would not discharge it '
        'either; it would destroy the inheritance evidence.'
    ),
    'phase': 'IMPLEMENTATION-PHASE ARTIFACT PUBLICATION BY THE D9 EXIT-CONTRACT UNIT',
    'qualification': 'Separate. Runtime qualification of the successor is release-gate work, not design work.',
    'finalApplicationReviewBinding': activation,
}
source = dc + 'inherited-residuals.proposed.md'
parents = []
residuals = []
for line in source_path(source).read_text().splitlines():
    if not line.startswith('| DR-'):
        continue
    c = line.split('|')
    rid = c[1].strip().split()[0]
    body = c[2].strip()
    v = {
        'id': rid,
        'dispositionText': body,
        'source': ref(source),
        'designGrade': 'ACCEPT-DESIGN',
        'effectiveWhen': effective,
    }
    v['independentDisposition'] = design['inheritedResidualDispositions'][rid]
    v['gradeAuthority'] = (
        'Fresh final application review must substantively assess this proposed design grade; '
        'CARRIED-UNCHANGED does not grade or discharge an inherited residual.'
    )
    v['finalApplicationReviewBinding'] = activation
    if rid in C.D9_CARRIED_ROWS:
        v['carriedCrossUnitObligation'] = D9_CARRIED
    if '-R' in rid:
        if rid == 'DR-011-R10':
            v['dispositionText'] = (
                'Fresh independent blind consumer B reconstructed the accepted current design '
                'with independently authored vectors; its exact result is the evidence below. '
                'Reviewer: ' + reviewer_label + '.'
            )
            v['reviewEvidence'] = dict(blind_ref, selector='/verdict')
        else:
            v['reviewEvidence'] = evidence('/inheritedResidualDispositions/' + rid)
        residuals.append(v)
    else:
        assert rid in design['inheritedResidualDispositions'], 'Actual review lacks individual inherited parent: ' + rid
        v['reviewEvidence'] = evidence('/inheritedResidualDispositions/' + rid)
        parents.append(v)
assert len(parents) == 11 and len(residuals) == 16
assert sum('carriedCrossUnitObligation' in v for v in parents + residuals) == 2
writej(
    dc + 'inherited-residuals.applied.v1.json',
    {
        'standing': effective,
        'parents': parents,
        'residuals': residuals,
        'evaluationSubresiduals': dc + 'evaluation-residual-dispositions.applied.v1.json',
        'DR012': 'Mandatory implementation/release qualification remains unperformed',
        'activation': activation,
    },
)
source = dc + 'qualification-gates.proposed.json'
gates = load(source)
gates['sourceArtifact'] = ref(source)
gates['standing'] = effective
for row in gates['items']:
    row['standing'] = 'DESIGN-CONTRACT-ACCEPTED; REQUIRED PRODUCT QUALIFICATION UNPERFORMED'
    row['activation'] = activation
    row['independentReview'] = design_ref
    if row['id'] == 'DR-G10':
        row['inheritedClaim'] = row['acceptance']
        row['acceptance'] = (
            'TS protocol major2 and Rust protocol major3 remain opaque, one-shot, fate-compatible '
            'native subprotocols with explicit source/fact/Coverage negotiation.'
        )
    if row['id'] == 'DR-G06':
        row['additionalCurrentContracts'] = [
            'docs/v2/contracts/product-v1/admission-and-qualification.md §2/§3',
            'docs/v2/contracts/product-v1/security-and-lifecycle.md S9.1/S11',
            'docs/v2/contracts/product-v1/native-evidence.md §3/§5',
        ]
    if row['id'] == 'DR-G11':
        row['additionalCurrentContracts'] = [
            'docs/v2/contracts/product-v1/security-and-lifecycle.md S3.1/S7/S9',
            'docs/v2/contracts/product-v1/workflows-and-surfaces.md §1/§9',
        ]
    assert row['qualified'] is False and row['demonstrated'] is False and row['implementationHarnessAuthored'] is False
assert [row['id'] for row in gates['items']] == list(C.GATE_IDS)
writej(dc + 'qualification-gates.applied.v1.json', gates)
assent = load(bound['codexDesignAssent']['path'])
writej(
    dc + 'accepted-review-advisories.v1.json',
    {
        'standing': effective,
        'review': design_ref,
        'items': assent['advisoryApplicationAccount'],
        'independentReviewFindings': design.get('newAdvisories', design.get('advisories', [])),
        'freshBlindReview': blind_ref,
        'codexBlindAssessment': blind_assessment_ref,
        'blindItems': blind_advisory_account,
        'independentBlindReviewFindings': blind_new_advisories,
        'bindingImplementationGates': ['DR-G17', 'DR-G20'],
        'note': (
            'These were independently nonblocking. No accepted model/schema/corpus is silently '
            'patched by this application; required implementation conformance remains mandatory.'
        ),
    },
)
act = source_path(dc + 'D-372-corrections.proposed.md').read_text()
act = act.replace(
    '# D-372 — proposed prospective product-contract correction',
    '## D-372 — complete intended-product design correction and application',
)
act = act.replace(
    'Standing: PROPOSED. No adoption or readiness change is made by this file.',
    f'''**Standing:** ADOPTED at design level only when the [D-372 activation](design-corrections/application-activation.v1.json) verifies. This exact applying body, the application record and the independent final application verdict are bound by that external receipt. A staged copy has no effect.

**Exact evidence:** design manifest `{manifest_ref['sha256']}`; {reviewer_label} design review `{design_ref['sha256']}`; fresh independent blind consumer review `{blind_ref['sha256']}`. [The application record](design-corrections/application.v1.json) pins their full paths and source closure. The independent final application review and application-content manifest are hash-bound by the activation receipt, avoiding any self-referential review hash. Conditions1–4 are met at design-contract level; condition5 remains NOT MET. No product qualification is claimed. D9 successor-artifact publication remains a carried implementation-unit obligation, not a design-level blocker. Historical Claude source21 review is not this subject.''',
)
act = act.replace("Workflow §9's declared parity fields", "Workflow §8's declared parity fields").replace(
    'Coverage and post-commit required-output failure law apply',
    'Coverage and the §8/§9 post-commit required-output failure law apply',
)
act += '''

### Current record application and historical custody

This act applies the exact application.v1.json, per-row map, review-owner map, AR/FW crosswalk, inherited/evaluation residual wrappers and32-gate map named by the activation-bound application subject. `.proposed` source files remain immutable reviewed sources; the applied wrappers and this act determine their current standing. Historical preview grades and rejected checker evidence retain their original scope. The31-file preapplication preservation report remains a statement about that frozen subject; the separately reviewed documentation deltas intentionally change current applicability text, without repinning old acceptance.

The current source-pin successors record only the three reviewed documentation applicability pointers and their transitive ledger hashes; all accepted original manifests and reports remain in the immutable design archive. The application records the actual rerun result. The integration checker is authenticated by its exact accepted whole-subject manifest entry and reproduced report, not by an invented unit launcher. The accepted-review advisories have explicit dispositions and retained evidence; real host/renderer/platform qualification is still required.

This working-tree delivery is reversible and preserves before-images. No commit, push, publication or product implementation is authorized.
'''
coord = 'docs/coop/COORDINATOR-DECISIONS.md'
writet(coord, source_path(coord).read_text().rstrip() + '\n\n' + act + '\n')
readme = dc + 'README.md'
history = (root / readme).read_text()
writet(
    readme,
    '# Applied complete product design correction — D-372\n\n'
    'The [application record](application.v1.json), effective through its [activation](application-activation.v1.json), '
    'binds ' + reviewer_label + ' independent design ACCEPT, Codex’s technical assent, the fresh blind consumer result '
    'and the independent final application review. [The product contracts](../../v2/contracts/product-v1/README.md) are '
    'the current complete intended-product design.\n\n'
    '[Current readiness](../../v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) '
    'records conditions1–4 at design level. Condition5 remains NOT MET: implementation requires separate user '
    'authorization. No supported-platform product qualification is claimed. D9 remains a carried implementation-unit '
    'obligation on DR-007 and DR-011-R08.\n\n'
    'The [applied corrections](correction-crosswalk.applied.v1.json), [28-row design map](readiness-row-map.v1.json), '
    '[inherited dispositions](inherited-residuals.applied.v1.json), '
    '[evaluation dispositions](evaluation-residual-dispositions.applied.v1.json), '
    '[review-owner records](review-owner-dispositions.v1.json), [32 release gates](qualification-gates.applied.v1.json), '
    'and [review advisories](accepted-review-advisories.v1.json) provide the exact account. Historical preview and '
    'interrupted/rejected review evidence remain intact. Historical Claude source21 ACCEPT does not accept these bytes.\n\n'
    '## Historical correction chronology (not current status)\n\n' + history,
)
records = [
    dc + n
    for n in [
        'readiness-row-map.v1.json',
        'review-owner-dispositions.v1.json',
        'correction-crosswalk.applied.v1.json',
        'inherited-residuals.applied.v1.json',
        'evaluation-residual-dispositions.applied.v1.json',
        'qualification-gates.applied.v1.json',
        'accepted-review-advisories.v1.json',
    ]
]
app = {
    'standing': effective,
    'decision': 'D-372',
    'implementationAuthorized': False,
    'qualificationClaimed': False,
    'conditions': {'1': 'MET-DESIGN', '2': 'MET-DESIGN', '3': 'MET-DESIGN', '4': 'MET-DESIGN', '5': 'NOT MET'},
    'designSubject': manifest_ref,
    'designSnapshotRoot': design_manifest['snapshotRoot'],
    'designSourceArchive': ref(dc + f'reviews/candidate-source.{dv}.tar.gz'),
    'independentDesignReview': design_ref,
    'independentDesignReviewVendor': vendor,
    'independentReviewerPublicLabel': reviewer_label,
    'codexCoauthorAssent': ref(bound['codexDesignAssent']['path']),
    'freshBlindConsumerReview': blind_ref,
    'codexBlindAssessment': blind_assessment_ref,
    'blindInputManifest': blind_input_ref,
    'blindInputCustody': ref(bound['freshBlindConsumerReview']['custodyPath'] or dc + f'reviews/consumer-b.{bv}/custody.json'),
    'acceptedContracts': assent['contracts'],
    'currentSourceMap': ref(dc + 'current-source-map.proposed.md'),
    'reviewedProposedAct': ref(dc + 'D-372-corrections.proposed.md'),
    'appliedRecords': [{'path': p, 'sha256': digest(files / p)} for p in records],
    'activation': activation,
    'finalIndependentApplicationReview': {
        'path': dc + f'reviews/application-review.{av}/review.json',
        'sha256Binding': 'external activation receipt; no future verdict or self-hash is fabricated',
    },
    'applicationSubject': {
        'path': dc + f'reviews/application-subject.{av}.json',
        'sha256Binding': 'external activation receipt',
    },
    'integrationCheckCustody': dict(
        ref(dc + 'check-integration.py'),
        report=ref(dc + 'integration-report.v1.json'),
        rule=(
            'Verify these entries against the accepted design manifest before execution; '
            'the checker is whole-subject pinned, not covered by a separate unit launcher.'
        ),
    ),
    'nativeRecordingDelta': (
        'native-recording-delta.v1.json in the reviewed application support evidence; '
        'no product contract/model/schema changes'
    ),
    'inventoryScope': (
        'Current scoped accounting at application-content freeze. Later final application '
        'review/activation, its manifest and mutable NEXT guide are bound separately, outside the inventory cutoff.'
    ),
    'historicalEvidence': (
        'All original frozen subjects remain immutable. Current documentation applicability '
        'changes and exact before-images are recorded separately; no retrospective repin. The prior D369 checker '
        'keeps its original inputs and its failure-set provenance is explicitly reported. Historical Claude '
        'source21 review remains historical.'
    ),
    'boundReceiptSha256': digest(a.bound_receipt),
    'd9CarriedImplementationUnitObligation': True,
    'productGatesUnperformed': True,
}
summary_rel = dc + 'validation-summary.v1.json'
counts_rel = dc + f'reviews/codex-post-reset.v1/identity-check-counts.{dv}.json'
summary = load(summary_rel)
counts = load(counts_rel)
assert summary['foundation']['components']['identity'] == counts['passingCalls']
assert counts['passingCalls'] == counts['distinctIds'] + counts['duplicateExtraInstances']
app['referenceEvidenceSummary'] = {
    'validationSummary': ref(summary_rel),
    'identityCountMeasurement': ref(counts_rel),
    'foundationPassingCalls': summary['foundation']['checksPassed'],
    'identityPassingCalls': counts['passingCalls'],
    'identityDistinctIds': counts['distinctIds'],
    'identityDuplicateExtraInstances': counts['duplicateExtraInstances'],
    'standing': (
        'Reference evidence counts, not a coverage or product-qualification claim. Historical '
        'pending-review labels describe the original frozen summary; actual accepted review is separately pinned above.'
    ),
}
commands_rel = dc + f'reviews/codex-post-reset.v1/final-reference.{dv}/reference-checks.json'
original = load(commands_rel)
reproduction = []
for command in original['commands']:
    source = command['source']
    assert accepted_files[source]['sha256'] == command['sourceSha256']
    args = list(command['command'])
    assert args[1:3] == ['-I', '-B'] and (args[3] == source or args[3].endswith('/' + source))
    args[3] = source
    reproduction.append(
        {'name': command['name'], 'source': source, 'sourceSha256': command['sourceSha256'], 'argv': args}
    )
app['acceptedDesignReproduction'] = {
    'originalExecutedCommandRecord': ref(commands_rel),
    'designManifest': manifest_ref,
    'workingDirectory': (
        'A disposable full copy of the exact accepted snapshot, verified against every manifest '
        'entry before execution. Never execute these report-writing commands in the immutable accepted snapshot.'
    ),
    'interpreter': (
        'The recorded isolated Python environment includes jsonschema; an equivalent environment may '
        'replace argv[0]. Verify required imports before execution.'
    ),
    'commands': reproduction,
    'standing': (
        'Executable relative-source reproduction metadata; original absolute command records and '
        'reports remain immutable historical evidence. Application-stage reruns separately account for the three '
        'documentation-provenance pin changes.'
    ),
}
# Preserve the two exact historical operational-guide variants. They are not
# normative source, and their live bytes must not be replaced by snapshot copies.
variant_paths = {dc+'reviews/resume-before-v23-next-review.v1.md', dc+'reviews/resume-source21-next-review.v1.md'}
variants=[]
for rel in sorted(variant_paths):
    assert rel in accepted_files
    before=digest(root/rel)
    assert before != accepted_files[rel]['sha256'], 'Reassess guide variance: '+rel
    variants.append({'path':rel,'liveSha256':before,'acceptedSnapshotSha256':accepted_files[rel]['sha256'],
        'basis':'Historical operational resume-guide variants, both preserved. Accepted snapshot remains exact; live variant is not overwritten or semantic authority.'})
for rel,row in accepted_files.items():
    if (files/rel).is_file() or rel == dc+'reviews/NEXT-REVIEW.md' or rel in variant_paths:
        continue
    assert (root/rel).is_file() and digest(root/rel)==row['sha256'], 'Unaccounted live/source divergence: '+rel
app['preservedHistoricalGuideVariants']=variants
writej(dc + 'application.v1.json', app)
(out / 'assembly-metadata.json').write_text(
    json.dumps(
        {
            'standing': 'FUTURE EFFECT ONLY; requires exact final independent application ACCEPT and activation',
            'designManifest': manifest_ref,
            'designReview': design_ref,
            'blindReview': blind_ref,
            'vendor': vendor,
            'implementationAuthorized': False,
            'boundReceiptSha256': digest(a.bound_receipt),
        },
        indent=2,
    )
    + '\n'
)
print('Assembled actual-evidence records and current documents; not applied or frozen yet:', out)
