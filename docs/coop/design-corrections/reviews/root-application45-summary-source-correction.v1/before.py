"""Prospective application summary routing after assembly, before validation/freeze.

Writes only the prospective stage. Grants no grade or activation.
Design subject path comes from the assembled application record, not hardcoded v21.
Historical CLAUDE-V13-ADV-1/2 and v13 SHA remain historical evidence; they are
not renamed. Current matrix cell count is measured from the accepted snapshot.
The accepted frozen validation summary keeps its own evidence vintage; current counts come only from the
source-bound reference receipts (current_reference_summary.accepted_summary_boundary).
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C
import review_envelope as E
from current_reference_summary import accepted_summary_boundary

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--stage', type=Path, required=True)
p.add_argument('--bound-receipt', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve()
stage = a.stage.resolve()
files = stage / 'files'
support = stage / 'support'
support.mkdir(exist_ok=True)
dc = 'docs/coop/design-corrections/'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
bound = load(a.bound_receipt)
assert bound.get('readyForAssembly') is True
assert bound['implementationAuthorized'] is False
vendor = bound['vendor']
app_path = files / (dc + 'application.v1.json')
app = load(app_path)
assert app['designSubject']['path'] == bound['designSubject']['path']
assert app['designSubject']['sha256'] == bound['designSubject']['sha256']
assert app['designSubject']['sha256'] != C.HISTORICAL_V21_SUBJECT_SHA256 or bound['designVersion'] == 'v21'
review_path = root / app['independentDesignReview']['path']
review = load(review_path)
assert sha(review_path) == app['independentDesignReview']['sha256']
assert review['subjectManifestSha256'] == app['designSubject']['sha256']
assert review.get('verdict', review.get('overallVerdict')) == 'ACCEPT'
E.require_findings_none(review, 'independent design')
E.decode_public_file(root / bound['independentDesignReview']['publicResponsePath'], vendor)
assert sha(root / app['designSubject']['path']) == app['designSubject']['sha256']
assert app['implementationAuthorized'] is False
blind = load(root / app['freshBlindConsumerReview']['path'])
assert sha(root / app['freshBlindConsumerReview']['path']) == app['freshBlindConsumerReview']['sha256']
assert blind['verdict'] == 'ACCEPT-RECONSTRUCTABLE'
E.require_findings_none(blind, 'fresh blind')
snapshot = Path(app['designSnapshotRoot'])
# Two evidence vintages meet here. The accepted subject may retain an older validation summary byte-for-byte while
# its generated reports and the bound reference receipts are current. The summary is checked only as itself; every
# current count and every presented generated report is bound to the source-bound receipts. Historical counts are
# recorded beside current ones, never equated with them.
boundary = accepted_summary_boundary(root, app['designSubject'], app['designSnapshotRoot'],
    app['acceptedDesignReproduction']['originalExecutedCommandRecord'],
    app['referenceEvidenceSummary']['identityCountMeasurement'])
old = boundary['acceptedSummary']
measured_cells = boundary['measuredCells']
sources = boundary['sources']
historical_manifest_path = root / (dc + 'reviews/candidate-subject.v13.json')
historical_manifest = load(historical_manifest_path)
assert sha(historical_manifest_path) == C.HISTORICAL_V13_MANIFEST_SHA256
historical_path = Path(historical_manifest['snapshotRoot']) / (dc + 'validation-summary.v1.json')
historical_row = next(r for r in historical_manifest['files'] if r['path'] == dc + 'validation-summary.v1.json')
assert sha(historical_path) == historical_row['sha256']
assert load(historical_path)['native']['matrixCells'] == C.HISTORICAL_V13_MATRIX_CELLS
current = boundary['current']
assert current['native']['matrixCells'] == measured_cells and current['native']['qualifiedCells'] == 0
current['standing'] = (
    'Current reference summary effective only through the independently reviewed D372 '
    'application activation. Synthetic reference evidence; no product qualification or '
    'implementation authorization.'
)
current['activation'] = app['activation']
current['acceptedOriginalSummary'] = {
    'path': dc + 'validation-summary.v1.json',
    'sha256': sha(snapshot / (dc + 'validation-summary.v1.json')),
    'resolveAgainst': app['designSubject'],
    'meaning': (
        'The accepted frozen summary as recorded by its own evidence vintage; not current execution. Its counts '
        'are listed beside the receipt-bound current counts; a difference is not a correction of it.'
    ),
    'recordedCountsVersusCurrent': boundary['acceptedSummaryCounts'],
}
# Preserve historical Claude routing keys as historical. Do not write a Grok
# review path into claudeFinalReview.
current['acceptedOriginalReviewRouting'] = {
    k: old[k]
    for k in (
        'claudePriorReview',
        'claudeFinalReview',
        'priorReviewLimitation',
        'latestCompletedBlindReview',
        'latestBlindClarification',
    )
    if k in old
}
current.pop('latestBlindClarification', None)
current.pop('claudeFinalReview', None)
current['actualIndependentReview'] = app['independentDesignReview']
current['independentReviewVendor'] = vendor
current['latestCompletedBlindReview'] = app['freshBlindConsumerReview']['path']
current['actualBlindReview'] = app['freshBlindConsumerReview']
current['priorReviewLimitation'] = (
    'Earlier accepted and rejected candidates retain their historical scope. Actual '
    'accepted design and fresh blind evidence are pinned here; this current summary '
    'becomes effective only through the separately reviewed application activation. '
    'Historical Claude source21 review does not accept a changed successor.'
)
current['recordingCorrections'] = [
    {
        'field': 'native.matrixCells',
        'acceptedOriginalValue': old['native']['matrixCells'],
        'currentMeasuredValue': measured_cells,
        'historicalV13Value': C.HISTORICAL_V13_MATRIX_CELLS,
        'historicalSummary': {
            'path': historical_row['path'],
            'sha256': historical_row['sha256'],
            'resolveAgainst': {
                'path': str(historical_manifest_path.relative_to(root)),
                'sha256': sha(historical_manifest_path),
            },
        },
        'finding': 'CLAUDE-V13-ADV-1',
        'status': 'HISTORICAL-FINDING-ID-PRESERVED; CURRENT-COUNT-MEASURED-FROM-ACCEPTED-SNAPSHOT',
        'authority': (
            'Current accepted matrix/report/summary equality verified. Historical v13 and '
            'later accepted summaries remain immutable; only actual current review routing '
            'becomes effective through application. Finding id CLAUDE-V13-ADV-1 is not renamed.'
        ),
    }
]
current['countSources'] = sources
rel = dc + 'validation-summary.applied.v1.json'
q = files / rel
assert not q.exists()
q.write_text(json.dumps(current, indent=2) + '\n')
current_ref = {'path': rel, 'sha256': sha(q)}
before = support / 'successor-advisory-before.v1'
assert not before.exists()
before.mkdir()
changed = [
    dc + 'application.v1.json',
    dc + 'accepted-review-advisories.v1.json',
    'docs/coop/COORDINATOR-DECISIONS.md',
    dc + 'README.md',
]
for rel0 in changed:
    q0 = before / rel0
    q0.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(files / rel0, q0)
frozen_ref = app['referenceEvidenceSummary']['validationSummary']
assert sha(root / frozen_ref['path']) == frozen_ref['sha256']
assert app['referenceEvidenceSummary']['foundationPassingCalls'] == load(root / frozen_ref['path'])['foundation']['checksPassed']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary'] = app['referenceEvidenceSummary']['validationSummary']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']['resolveAgainst'] = app['designSubject']
app['referenceEvidenceSummary']['validationSummary'] = current_ref
# The assembled foundation count came from the frozen summary; keep it under that name and state the current count.
app['referenceEvidenceSummary']['acceptedFrozenFoundationPassingCalls'] = app['referenceEvidenceSummary']['foundationPassingCalls']
app['referenceEvidenceSummary']['foundationPassingCalls'] = current['foundation']['checksPassed']
app['referenceEvidenceSummary']['standing'] = (
    'Current applied summary verifies the already corrected accepted matrix count and '
    'updates actual review routing; both historical v13 and accepted design summaries '
    'remain separately pinned. Counts are synthetic reference evidence, not product qualification.'
)
app['appliedRecords'].append(current_ref)
advice_path = files / (dc + 'accepted-review-advisories.v1.json')
advice = load(advice_path)
ids = {r['id']: r for r in advice['items']}
# Historical finding IDs stay those ids. If the successor assent still carries
# them, annotate those rows. If not, append historical-only application notes.
measurement = dc + 'reviews/codex-post-reset.v1/v13-crate-illustration-recheck.v1.json'
measure = load(root / measurement)
assert [r['bytes'] for r in measure['rows']] == [222, 400, 946]
historical_v13 = {
    'currentSummary': current_ref,
    'historicalV13Value': C.HISTORICAL_V13_MATRIX_CELLS,
    'currentMeasuredValue': measured_cells,
    'alreadyCorrectedBeforeCurrentDesignFreeze': True,
    'historicalSummary': current['recordingCorrections'][0]['historicalSummary'],
    'equalityGuard': (
        'accepted summary.native.matrixCells == len(native-capability-matrix.cells) '
        '== native-evidence-report.matrix.cells'
    ),
    'effectiveWhen': app['standing'],
    'findingIdUnchanged': 'CLAUDE-V13-ADV-1',
}
if 'CLAUDE-V13-ADV-1' in ids:
    ids['CLAUDE-V13-ADV-1']['applicationCorrection'] = historical_v13
else:
    advice['items'].append(
        {
            'id': 'CLAUDE-V13-ADV-1',
            'standing': 'HISTORICAL finding id preserved at application; not a new Grok advisory.',
            'applicationCorrection': historical_v13,
        }
    )
    ids = {r['id']: r for r in advice['items']}
clarification = {
    'meaning': (
        'The historical723-byte example is illustrative and depends on crate names and '
        'representation. Twenty-one crates is not a threshold. The raw32-byte digest rule remains unchanged.'
    ),
    'measuredCanonicalIntegerEditionMaps': [
        {'naming': r['label'], 'bytes': r['bytes'], 'exceeds255': r['exceeds255']} for r in measure['rows']
    ],
    'measurement': {'path': measurement, 'sha256': sha(root / measurement)},
    'effectiveWhen': app['standing'],
    'findingIdUnchanged': 'CLAUDE-V13-ADV-2',
}
if 'CLAUDE-V13-ADV-2' in ids:
    ids['CLAUDE-V13-ADV-2']['applicationClarification'] = clarification
else:
    advice['items'].append(
        {
            'id': 'CLAUDE-V13-ADV-2',
            'standing': 'HISTORICAL finding id preserved at application; not a new Grok advisory.',
            'applicationClarification': clarification,
        }
    )
assert set(C.HISTORICAL_V13_ADVISORY_IDS) <= {r['id'] for r in advice['items']}
advice_path.write_text(json.dumps(advice, indent=2) + '\n')
coord = files / 'docs/coop/COORDINATOR-DECISIONS.md'
coord.write_text(
    coord.read_text()
    + f'''

### Reference evidence corrections applied by D-372

The [current reference summary](design-corrections/validation-summary.applied.v1.json) verifies that the accepted summary, native matrix and generated report all agree on {measured_cells} cells and names the actual accepted reviews. The historical v13 summary recorded {C.HISTORICAL_V13_MATRIX_CELLS}; that count was corrected before later freezes. Both original summaries remain exact historical evidence under their own manifests. Finding ids CLAUDE-V13-ADV-1 and CLAUDE-V13-ADV-2 remain those historical ids. No cell is product-qualified.

The historical illustration of twenty-one crates and 723 bytes depends on the crate names and representation. The crate count is not a threshold. Canonical integer edition maps with the three explicitly recorded namings occupy 222, 400 and 946 bytes. These measurements are retained in the [advisory record](design-corrections/accepted-review-advisories.v1.json); none measures a real workspace. The normative body-language-version component remains the raw 32 bytes of its canonical-record SHA-256. This clarification changes no contract, schema, model or public product behavior and is effective through this act's exact application activation.
'''
)
readme = files / (dc + 'README.md')
text = readme.read_text()
needle = '## Historical correction chronology (not current status)'
assert text.count(needle) == 1
text = text.replace(
    needle,
    'The [current reference summary](validation-summary.applied.v1.json) and [advisory clarifications](accepted-review-advisories.v1.json) verify the measured matrix count and qualify the historical crate-size illustration.\n\n'
    + f"Current reference evidence records {current['native']['casesPassed']} native cases, {current['workflows']['checksPassed']} workflow controls and {current['evaluator3']['suiteCount']} current evaluator suites. Counts describe their retained reference scope, not product qualification. Full semantic Run admission uses `close_run`; `open_run_closure` provides structural owner admission only. The exact accepted contracts and their current review dispositions govern these boundaries. Historical source23 recording corrections are not presented as unresolved current advisories.\n\n"
    + needle,
)
readme.write_text(text)
for row in app['appliedRecords']:
    row['sha256'] = sha(files / row['path'])
app_path.write_text(json.dumps(app, indent=2) + '\n')
shutil.copyfile(__file__, support / Path(__file__).name)
for name in [
    'coverage_contract.py',
    'review_envelope.py',
    'bind-review-receipts.v1.py',
    'assemble-records.successor.v1.py',
    'current_reference_summary.py',
]:
    shutil.copyfile(HERE / name, support / name)
# Historical apply-v21 chain remains evidence; copied from the guarded assembly dir, not rewritten.
hist = Path('/tmp/opensip-design-corrections/application-assembly.v1')
for name in [
    'apply-v21-advisory-records.py',
    'prepare-v21-advisory-updater.v1.json',
    'recheck-v13-illustration.py',
]:
    src = hist / name
    if src.is_file():
        shutil.copyfile(src, support / name)
(support / 'successor-advisory-corrections.v1.json').write_text(
    json.dumps(
        {
            'standing': 'Prospective application-only reporting corrections. No product contract/schema/model change, acceptance or activation.',
            'beforeImages': 'successor-advisory-before.v1',
            'currentSummary': current_ref,
            'changedFiles': [{'path': p, 'beforeSha256': sha(before / p), 'afterSha256': sha(files / p)} for p in changed],
            'sourceMeasurement': {'path': measurement, 'sha256': sha(root / measurement)},
            'designSubject': app['designSubject'],
            'historicalFindingIdsPreserved': list(C.HISTORICAL_V13_ADVISORY_IDS),
            'measuredMatrixCells': measured_cells,
            'acceptedSummaryCountsVersusCurrent': boundary['acceptedSummaryCounts'],
            'vendor': vendor,
        },
        indent=2,
    )
    + '\n'
)
print('Prepared current applied summary and historical v13 illustration clarification; original accepted design unchanged.')
