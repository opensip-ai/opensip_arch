"""Prepare v18 application summary routing and historical v13 advisory clarification.
Run AFTER actual accepted design+blind assembly, BEFORE validation/inventory/freeze.
Only writes the prospective application stage. Grants no grade or activation.
"""
from pathlib import Path
import argparse,json,hashlib,copy,shutil
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',type=Path,required=True);a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();files=stage/'files';support=stage/'support';support.mkdir(exist_ok=True)
dc='docs/coop/design-corrections/';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
app_path=files/(dc+'application.v1.json');app=load(app_path)
assert app['designSubject']['path']==dc+'reviews/candidate-subject.v18.json'
# Its exact SHA is bound by the completed independent review, application and manifest equality checks below.
review_path=root/app['independentDesignReview']['path'];review=load(review_path)
assert sha(review_path)==app['independentDesignReview']['sha256'] and review['subjectManifestSha256']==app['designSubject']['sha256']
assert review.get('verdict',review.get('overallVerdict'))=='ACCEPT' and all(type(review.get(k)) is list and not review[k] for k in ('newMustIssues','newShouldIssues'))
assert load(review_path.with_name('response.json'))['is_error'] is False
assert sha(root/app['designSubject']['path'])==app['designSubject']['sha256']
assert app['implementationAuthorized'] is False
blind=load(root/app['freshBlindConsumerReview']['path']);assert sha(root/app['freshBlindConsumerReview']['path'])==app['freshBlindConsumerReview']['sha256']
assert blind['verdict']=='ACCEPT-RECONSTRUCTABLE' and all(type(blind.get(k)) is list and not blind[k] for k in ('newMustIssues','newShouldIssues'))
manifest=load(root/app['designSubject']['path']);snapshot=Path(app['designSnapshotRoot']);expected={r['path']:r for r in manifest['files']}
sources=[]
def accepted(rel):
 p=snapshot/rel;assert sha(p)==expected[rel]['sha256'];sources.append({'path':rel,'sha256':sha(p),'resolveAgainst':app['designSubject']});return load(p)
old=accepted(dc+'validation-summary.v1.json');matrix=accepted(dc+'native/native-capability-matrix.v2.json');native=accepted(dc+'native/native-evidence-report.v2.json')
identity=accepted(dc+'foundation/identity-report.json');security=accepted(dc+'security/security-lifecycle-report.v1.json');workflow=accepted(dc+'workflows/workflows-report.v1.json');integration=accepted(dc+'integration-report.v1.json')
assert old['foundation']['checksPassed']==sum(old['foundation']['components'].values())
assert old['foundation']['components']['identity']==identity['passed']
assert old['security']['casesPassed']==security['counts']['pass'] and old['security']['invariantSweepsPassed']==len(security['sweeps'])
assert old['native']['casesPassed']==native['cases']['passed']
assert old['workflows']['checksPassed']==workflow['passed'] and old['integration']['checksPassed']==integration['passed']
assert len(matrix['cells'])==native['matrix']['cells']==66 and native['matrix']['qualifiedCells']==0
assert old['native']['matrixCells']==len(matrix['cells'])==66
# Preserve historical v13's stale60 and show this was corrected BEFORE accepted v18, not by silently changing accepted source.
historical_manifest_path=root/(dc+'reviews/candidate-subject.v13.json');historical_manifest=load(historical_manifest_path)
assert sha(historical_manifest_path)=='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
historical_path=Path(historical_manifest['snapshotRoot'])/(dc+'validation-summary.v1.json')
historical_row=next(r for r in historical_manifest['files'] if r['path']==dc+'validation-summary.v1.json')
assert sha(historical_path)==historical_row['sha256'] and load(historical_path)['native']['matrixCells']==60
current=copy.deepcopy(old);current['native']['matrixCells']=len(matrix['cells']);current['native']['qualifiedCells']=native['matrix']['qualifiedCells']
current['standing']='Current reference summary effective only through the independently reviewed D372 application activation. Synthetic reference evidence; no product qualification or implementation authorization.'
current['activation']=app['activation'];current['acceptedOriginalSummary']={'path':dc+'validation-summary.v1.json','sha256':sha(snapshot/(dc+'validation-summary.v1.json')),'resolveAgainst':app['designSubject']}
current['claudeFinalReview']=app['independentDesignReview']['path'];current['actualIndependentReview']=app['independentDesignReview']
current['acceptedOriginalReviewRouting']={k:old[k] for k in ('claudePriorReview','claudeFinalReview','priorReviewLimitation','latestCompletedBlindReview') if k in old}
current['latestCompletedBlindReview']=app['freshBlindConsumerReview']['path'];current['actualBlindReview']=app['freshBlindConsumerReview']
current['priorReviewLimitation']='Earlier accepted and rejected candidates retain their historical scope. Actual accepted design and fresh blind evidence are pinned here; this current summary becomes effective only through the separately reviewed application activation.'
current['recordingCorrections']=[{'field':'native.matrixCells','acceptedOriginalValue':old['native']['matrixCells'],'currentMeasuredValue':66,'historicalV13Value':60,'historicalSummary':{'path':historical_row['path'],'sha256':historical_row['sha256'],'resolveAgainst':{'path':str(historical_manifest_path.relative_to(root)),'sha256':sha(historical_manifest_path)}},'finding':'CLAUDE-V13-ADV-1','status':'ALREADY-CORRECTED-BEFORE-ACCEPTED-V18; REVERIFIED-AT-APPLICATION','authority':'Current accepted matrix/report/summary equality verified. Historical v13 and accepted v18 summaries remain immutable; only actual current review routing becomes effective through application.'}]
current['countSources']=sources
rel=dc+'validation-summary.applied.v1.json';q=files/rel;assert not q.exists();q.write_text(json.dumps(current,indent=2)+'\n');current_ref={'path':rel,'sha256':sha(q)}
before=support/'v18-advisory-before.v1';assert not before.exists();before.mkdir()
changed=[dc+'application.v1.json',dc+'accepted-review-advisories.v1.json','docs/coop/COORDINATOR-DECISIONS.md',dc+'README.md']
for rel0 in changed:
 q0=before/rel0;q0.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(files/rel0,q0)
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']=app['referenceEvidenceSummary']['validationSummary']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']['resolveAgainst']=app['designSubject']
app['referenceEvidenceSummary']['validationSummary']=current_ref
app['referenceEvidenceSummary']['standing']='Current applied summary verifies the already corrected accepted matrix count and updates actual review routing; both historical v13 and accepted v18 summaries remain separately pinned. Counts are synthetic reference evidence, not product qualification.'
app['appliedRecords'].append(current_ref)
advice_path=files/(dc+'accepted-review-advisories.v1.json');advice=load(advice_path);ids={r['id']:r for r in advice['items']};assert {'CLAUDE-V13-ADV-1','CLAUDE-V13-ADV-2'}<=set(ids)
ids['CLAUDE-V13-ADV-1']['applicationCorrection']={'currentSummary':current_ref,'historicalV13Value':60,'acceptedV18Value':66,'currentMeasuredValue':66,'alreadyCorrectedBeforeCurrentDesignFreeze':True,'historicalSummary':current['recordingCorrections'][0]['historicalSummary'],'equalityGuard':'accepted summary.native.matrixCells == len(native-capability-matrix.cells) == native-evidence-report.matrix.cells','effectiveWhen':app['standing']}
measurement=dc+'reviews/codex-post-reset.v1/v13-crate-illustration-recheck.v1.json';measure=load(root/measurement);assert [r['bytes'] for r in measure['rows']]==[222,400,946]
ids['CLAUDE-V13-ADV-2']['applicationClarification']={'meaning':'The historical723-byte example is illustrative and depends on crate names and representation. Twenty-one crates is not a threshold. The raw32-byte digest rule remains unchanged.','measuredCanonicalIntegerEditionMaps':[{'naming':r['label'],'bytes':r['bytes'],'exceeds255':r['exceeds255']} for r in measure['rows']],'measurement':{'path':measurement,'sha256':sha(root/measurement)},'effectiveWhen':app['standing']}
advice_path.write_text(json.dumps(advice,indent=2)+'\n')
coord=files/'docs/coop/COORDINATOR-DECISIONS.md';coord.write_text(coord.read_text()+'''\n\n### Reference evidence corrections applied by D-372\n\nThe [current reference summary](design-corrections/validation-summary.applied.v1.json) verifies that the accepted v18 summary, native matrix and generated report all agree on 66 cells and names the actual accepted reviews. The historical v13 summary recorded 60; that count was corrected before v18 was frozen. Both original summaries remain exact historical evidence under their own manifests. No cell is product-qualified.\n\nThe historical illustration of twenty-one crates and 723 bytes depends on the crate names and representation. The crate count is not a threshold. Canonical integer edition maps with the three explicitly recorded namings occupy 222, 400 and 946 bytes. These measurements are retained in the [advisory record](design-corrections/accepted-review-advisories.v1.json); none measures a real workspace. The normative body-language-version component remains the raw 32 bytes of its canonical-record SHA-256. This clarification changes no contract, schema, model or public product behavior and is effective through this act's exact application activation.\n''')
readme=files/(dc+'README.md');text=readme.read_text();needle='## Historical correction chronology (not current status)';assert text.count(needle)==1;text=text.replace(needle,'The [current reference summary](validation-summary.applied.v1.json) and [advisory clarifications](accepted-review-advisories.v1.json) verify the corrected matrix count and qualify the historical crate-size illustration.\n\n'+needle);readme.write_text(text)
for row in app['appliedRecords']:row['sha256']=sha(files/row['path'])
app_path.write_text(json.dumps(app,indent=2)+'\n')
shutil.copyfile(__file__,support/Path(__file__).name)
for name in ['v14-advisory-preparation.v1.json','v15-advisory-preparation.v1.json','prepare-v15-advisory-updater.py','apply-v14-advisory-records.py','apply-v15-advisory-records.before-support-custody.py','prepare-v15-support-custody.py','v15-support-custody-preparation.v1.json','apply-v15-advisory-records.before-v16.py','prepare-v16-advisory-updater.py','v16-advisory-preparation.v1.json','apply-v16-advisory-records.py','prepare-v17-advisory-updater.v1.json','apply-v17-advisory-records.py','prepare-v18-advisory-updater.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
shutil.copyfile(Path(__file__).with_name('recheck-v13-illustration.py'),support/'recheck-v13-illustration.py')
(support/'v18-advisory-corrections.v1.json').write_text(json.dumps({'standing':'Prospective application-only reporting corrections. No product contract/schema/model change, acceptance or activation.','beforeImages':'v18-advisory-before.v1','currentSummary':current_ref,'changedFiles':[{'path':p,'beforeSha256':sha(before/p),'afterSha256':sha(files/p)} for p in changed],'sourceMeasurement':{'path':measurement,'sha256':sha(root/measurement)},'designSubject':app['designSubject']},indent=2)+'\n')
print('Prepared current applied summary and D372 illustration clarification; original accepted design unchanged.')
