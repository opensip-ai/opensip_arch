"""Prepare reviewed-application corrections for the two actual v13 advisories.
Run AFTER actual accepted design+blind assembly, BEFORE validation/inventory/freeze.
Only writes the prospective application stage. Grants no grade or activation.
"""
from pathlib import Path
import argparse,json,hashlib,copy,shutil
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',type=Path,required=True);a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();files=stage/'files';support=stage/'support';support.mkdir(exist_ok=True)
dc='docs/coop/design-corrections/';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
app_path=files/(dc+'application.v1.json');app=load(app_path)
assert app['designSubject']['sha256']=='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
assert app['independentDesignReview']['sha256']=='5d7623f4762aef7c966b631346d6d8fe17e48324c9e1cfc88a39fa9a79fcdd00'
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
assert old['native']['matrixCells']==60
current=copy.deepcopy(old);current['native']['matrixCells']=len(matrix['cells']);current['native']['qualifiedCells']=native['matrix']['qualifiedCells']
current['standing']='Current reference summary effective only through the independently reviewed D372 application activation. Synthetic reference evidence; no product qualification or implementation authorization.'
current['activation']=app['activation'];current['acceptedOriginalSummary']={'path':dc+'validation-summary.v1.json','sha256':sha(snapshot/(dc+'validation-summary.v1.json')),'resolveAgainst':app['designSubject']}
current['claudeFinalReview']=app['independentDesignReview']['path'];current['actualIndependentReview']=app['independentDesignReview']
current['acceptedOriginalReviewRouting']={k:old[k] for k in ('claudePriorReview','claudeFinalReview','priorReviewLimitation','latestCompletedBlindReview') if k in old}
current['latestCompletedBlindReview']=app['freshBlindConsumerReview']['path'];current['actualBlindReview']=app['freshBlindConsumerReview']
current['priorReviewLimitation']='Earlier accepted and rejected candidates retain their historical scope. Actual accepted design and fresh blind evidence are pinned here; this current summary becomes effective only through the separately reviewed application activation.'
current['recordingCorrections']=[{'field':'native.matrixCells','acceptedOriginalValue':60,'currentMeasuredValue':66,'finding':'CLAUDE-V13-ADV-1','authority':'Actual matrix/report equality verified during application assembly; accepted original remains immutable historical evidence.'}]
current['countSources']=sources
rel=dc+'validation-summary.applied.v1.json';q=files/rel;assert not q.exists();q.write_text(json.dumps(current,indent=2)+'\n');current_ref={'path':rel,'sha256':sha(q)}
before=support/'v13-advisory-before.v1';assert not before.exists();before.mkdir()
changed=[dc+'application.v1.json',dc+'accepted-review-advisories.v1.json','docs/coop/COORDINATOR-DECISIONS.md',dc+'README.md']
for rel0 in changed:
 q0=before/rel0;q0.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(files/rel0,q0)
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']=app['referenceEvidenceSummary']['validationSummary']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']['resolveAgainst']=app['designSubject']
app['referenceEvidenceSummary']['validationSummary']=current_ref
app['referenceEvidenceSummary']['standing']='Current applied summary corrects the recorded matrix count with actual matrix/report equality; the exact accepted original remains separately pinned. Counts are synthetic reference evidence, not product qualification.'
app['appliedRecords'].append(current_ref)
advice_path=files/(dc+'accepted-review-advisories.v1.json');advice=load(advice_path);ids={r['id']:r for r in advice['items']};assert {'CLAUDE-V13-ADV-1','CLAUDE-V13-ADV-2'}<=set(ids)
ids['CLAUDE-V13-ADV-1']['applicationCorrection']={'currentSummary':current_ref,'before':60,'after':66,'equalityGuard':'len(native-capability-matrix.cells) == native-evidence-report.matrix.cells','effectiveWhen':app['standing']}
measurement=dc+'reviews/codex-post-reset.v1/v13-crate-illustration-recheck.v1.json';measure=load(root/measurement);assert [r['bytes'] for r in measure['rows']]==[222,400,946]
ids['CLAUDE-V13-ADV-2']['applicationClarification']={'meaning':'The historical723-byte example is illustrative and depends on crate names and representation. Twenty-one crates is not a threshold. The raw32-byte digest rule remains unchanged.','measuredCanonicalIntegerEditionMaps':[{'naming':r['label'],'bytes':r['bytes'],'exceeds255':r['exceeds255']} for r in measure['rows']],'measurement':{'path':measurement,'sha256':sha(root/measurement)},'effectiveWhen':app['standing']}
advice_path.write_text(json.dumps(advice,indent=2)+'\n')
coord=files/'docs/coop/COORDINATOR-DECISIONS.md';coord.write_text(coord.read_text()+'''\n\n### Reference evidence corrections applied by D-372\n\nThe [current reference summary](design-corrections/validation-summary.applied.v1.json) corrects the historical summary's native matrix count from 60 to 66 by checking the actual matrix against its generated report. The accepted original summary remains exact historical evidence in the bound design snapshot. No cell is product-qualified.\n\nThe historical illustration of twenty-one crates and 723 bytes depends on the crate names and representation. The crate count is not a threshold. Canonical integer edition maps with the three explicitly recorded namings occupy 222, 400 and 946 bytes. These measurements are retained in the [advisory record](design-corrections/accepted-review-advisories.v1.json); none measures a real workspace. The normative body-language-version component remains the raw 32 bytes of its canonical-record SHA-256. This clarification changes no contract, schema, model or public product behavior and is effective through this act's exact application activation.\n''')
readme=files/(dc+'README.md');text=readme.read_text();needle='## Historical correction chronology (not current status)';assert text.count(needle)==1;text=text.replace(needle,'The [current reference summary](validation-summary.applied.v1.json) and [advisory clarifications](accepted-review-advisories.v1.json) correct the recorded matrix count and qualify the historical crate-size illustration.\n\n'+needle);readme.write_text(text)
for row in app['appliedRecords']:row['sha256']=sha(files/row['path'])
app_path.write_text(json.dumps(app,indent=2)+'\n')
shutil.copyfile(__file__,support/Path(__file__).name)
shutil.copyfile(Path(__file__).with_name('recheck-v13-illustration.py'),support/'recheck-v13-illustration.py')
(support/'v13-advisory-corrections.v1.json').write_text(json.dumps({'standing':'Prospective application-only reporting corrections. No product contract/schema/model change, acceptance or activation.','beforeImages':'v13-advisory-before.v1','currentSummary':current_ref,'changedFiles':[{'path':p,'beforeSha256':sha(before/p),'afterSha256':sha(files/p)} for p in changed],'sourceMeasurement':{'path':measurement,'sha256':sha(root/measurement)},'designSubject':app['designSubject']},indent=2)+'\n')
print('Prepared current applied summary and D372 illustration clarification; original accepted design unchanged.')
