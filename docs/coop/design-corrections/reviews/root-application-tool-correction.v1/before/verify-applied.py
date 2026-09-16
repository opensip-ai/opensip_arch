"""Verify actual completed documentation application and report old-checker provenance honestly.
Requires real external activation; never applies files or awards a new grade.
"""
from pathlib import Path

def review_subject_digest(record):
 values=[record.get('subjectManifestSha256')]
 if isinstance(record.get('subject'),dict):values.append(record['subject'].get('manifestSha256'))
 values=[v for v in values if v is not None]
 assert values and all(type(v) is str and v==values[0] for v in values), 'Absent or conflicting review subject digests'
 return values[0]
import argparse,hashlib,importlib.util,json,subprocess,re
p=argparse.ArgumentParser()
for name in ('root','stage','out'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--reference-results',type=Path,required=True)
a=p.parse_args();root=a.root.resolve();stage=a.stage.resolve();out=a.out.resolve();out.mkdir(exist_ok=False)
dc='docs/coop/design-corrections/';py='/tmp/opensip-architecture-review-env/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def checked_ref(ref):
 p=root/ref['path'];assert sha(p)==ref['sha256'],ref['path'];return load(p)
def write(name,data):(out/name).write_text(json.dumps(data,indent=2)+'\n')
activation=load(root/(dc+'application-activation.v1.json'));manifest=checked_ref(activation['applicationManifest']);review=checked_ref(activation['independentApplicationReview'])
assert review['verdict']=='ACCEPT' and review['subjectManifestSha256']==activation['applicationManifest']['sha256']
assert all(isinstance(review.get(k),list) and not review[k] for k in ('newMustIssues','newShouldIssues'))
assert activation['implementationAuthorized'] is False and activation['qualificationClaimed'] is False
reference_checks=load(a.reference_results)
assert reference_checks['passed'] and reference_checks['applicationManifestSha256']==activation['applicationManifest']['sha256']
assert len(reference_checks['commands'])==7 and all(r['exitCode']==0 for r in reference_checks['commands'])
for row in reference_checks['commands']:assert sha(root/row['source'])==row['sourceSha256']

assert manifest['implementationAuthorized'] is False and manifest['qualificationClaimed'] is False
for row in manifest['files']:
 q=root/row['path'];assert sha(q)==row['sha256'] and q.stat().st_size==row['bytes'],row['path']
app=load(root/(dc+'application.v1.json'));assert app['conditions']['5']=='NOT MET';assert app['implementationAuthorized'] is False and app['qualificationClaimed'] is False
accepted=checked_ref(app['designSubject']);design=checked_ref(app['independentDesignReview']);blind=checked_ref(app['freshBlindConsumerReview'])
assert design.get('verdict',design.get('overallVerdict'))=='ACCEPT' and review_subject_digest(design)==app['designSubject']['sha256']
assert blind['verdict']=='ACCEPT-RECONSTRUCTABLE'
assert checked_ref(app['blindInputManifest'])['parentSubjectSha256']==app['designSubject']['sha256']
assert sha(root/app['designSourceArchive']['path'])==app['designSourceArchive']['sha256']
for row in accepted['files']:
 q=Path(accepted['snapshotRoot'])/row['path'];assert sha(q)==row['sha256'] and q.stat().st_size==row['bytes'],row['path']
applied_paths={row['path'] for row in manifest['files']}
variants={v['path']:v for v in app['preservedHistoricalGuideVariants']}
assert set(variants)=={row['path'] for row in accepted['files'] if re.fullmatch(re.escape(dc) + r'reviews/(?:resume-before-v[1-9][0-9]*-next-review\.v1|resume-source21-next-review\.v1)\.md', row['path'])}
accepted_by_path={v['path']:v for v in accepted['files']}
for rel,v in variants.items():
 assert rel not in applied_paths
 if v['liveState']=='absent':
  assert v['liveSha256'] is None and not (root/rel).exists()
 else:
  assert v['liveState']=='exactDigest' and sha(root/rel)==v['liveSha256']
 assert accepted_by_path[rel]['sha256']==v['acceptedSnapshotSha256']
for row in accepted['files']:
 if row['path'] not in applied_paths and row['path']!=dc+'reviews/NEXT-REVIEW.md' and row['path'] not in variants:
  assert sha(root/row['path'])==row['sha256'],'Unreviewed live candidate drift: '+row['path']
for row in app['acceptedContracts']:assert sha(root/row['path'])==row['sha256'],row['path']
for row in app['appliedRecords']:checked_ref(row)
rows=load(root/(dc+'readiness-row-map.v1.json'))['rows'];assert len(rows)==28
owners=load(root/(dc+'review-owner-dispositions.v1.json'))['records'];assert {v['id'] for v in owners}=={'DR-'+str(n) for n in range(201,206)}
gates=load(root/(dc+'qualification-gates.applied.v1.json'))['items'];assert len(gates)==32
assert all(row['qualified'] is False and row['demonstrated'] is False and row['implementationHarnessAuthored'] is False for row in gates)
assert len(load(root/(dc+'evaluation-residual-dispositions.applied.v1.json'))['items'])==30
# The current summary must agree with both its accepted-source measurements and current reports.
current_summary=checked_ref(app['referenceEvidenceSummary']['validationSummary'])
assert current_summary['activation']==dc+'application-activation.v1.json'
for source in current_summary['countSources']:
 assert source['resolveAgainst']==app['designSubject']
 assert sha(Path(accepted['snapshotRoot'])/source['path'])==source['sha256']
native_report=load(root/(dc+'native/native-evidence-report.v2.json'))
matrix=load(root/(dc+'native/native-capability-matrix.v2.json'))
assert current_summary['native']['matrixCells']==len(matrix['cells'])==native_report['matrix']['cells']
assert current_summary['native']['qualifiedCells']==native_report['matrix']['qualifiedCells']==0
assert current_summary['native']['casesPassed']==native_report['cases']['passed']
assert current_summary['foundation']['components']['identity']==load(root/(dc+'foundation/identity-report.json'))['passed']
assert current_summary['foundation']['checksPassed']==sum(current_summary['foundation']['components'].values())
assert current_summary['workflows']['checksPassed']==load(root/(dc+'workflows/workflows-report.v1.json'))['passed']
assert current_summary['integration']['checksPassed']==load(root/(dc+'integration-report.v1.json'))['passed']
security_report=load(root/(dc+'security/security-lifecycle-report.v1.json'))
assert current_summary['security']['casesPassed']==security_report['counts']['pass']
assert current_summary['security']['invariantSweepsPassed']==len(security_report['sweeps'])
assert current_summary['actualIndependentReview']==app['independentDesignReview'] and current_summary['actualBlindReview']==app['freshBlindConsumerReview']
original_summary=current_summary['acceptedOriginalSummary']
assert original_summary['resolveAgainst']==app['designSubject']
assert sha(Path(accepted['snapshotRoot'])/original_summary['path'])==original_summary['sha256']
write('current-reference-summary.json',{'standing':'Current applied reference counts independently compared with current reports and exact accepted-source evidence. No product qualification.','currentSummary':app['referenceEvidenceSummary']['validationSummary'],'acceptedOriginal':original_summary,'matrixCells':len(matrix['cells']),'qualifiedCells':0,'passed':True})
# Current generated accounting is checked within its explicitly recorded cutoff only.
inv=load(root/'docs/operations/document-inventory.v1.json');by_path={v['path']:v for v in inv['files']}
for rel in inv['workingTreeDelta']['contentPaths']:assert sha(root/rel)==by_path[rel]['sha256'],rel
r=subprocess.run([py,'-I','-B',str(root/'docs/operations/generate-current-design-catalog.py'),'--check'],capture_output=True,text=True);(out/'catalog.log').write_text(r.stdout+r.stderr);assert r.returncode==0
spec=importlib.util.spec_from_file_location('applied_links',stage/'support/check-links.py');links=importlib.util.module_from_spec(spec);spec.loader.exec_module(links)
assessment=load(stage/'support/application-link-assessment.v1.json');actual_links=links.check(root,None,assessment['paths'])
key=lambda v:(v['from'],v['target'],v['reason'])
assert {key(v) for v in actual_links['failures']} <= {key(v) for v in assessment['inheritedFailures']}
write('current-links.json',actual_links)
# Run the UNCHANGED old D369 checker; never update its old pins to manufacture a PASS.
legacy=out/'legacy-after.json';command=[py,'-I','-B',str(root/'docs/coop/completion/check-architecture-application.v1.py'),'--application',str(root/'docs/coop/completion/architecture-application.v1.json'),'--snapshot-manifest',str(root/'docs/coop/completion/architecture-publication-before.v1/snapshot-manifest.json'),'--whole-review',str(root/'docs/coop/completion/architecture-whole-review.v6.json'),'--mode','final','--report',str(legacy)]
r=subprocess.run(command,cwd=root,capture_output=True,text=True);(out/'legacy-after.log').write_text(r.stdout+r.stderr);assert legacy.is_file(),r.stderr
after=load(legacy);before=load(stage/'support/legacy-current-before.json');assert after['checkerSha256']==before['checkerSha256']
failed=lambda d:{v['id']:v for v in d['checks'] if v['status']=='FAIL'}
old=failed(before);new=failed(after);changes={row['path']:row for row in manifest['files'] if row['beforeSha256']!=row['sha256']};account=[]
for ident,row in new.items():
 if ident in old and row==old[ident]:account.append({'id':ident,'disposition':'Exact preexisting failure unchanged','failure':row});continue
 if ident=='register/current-custody':path='docs/v2/architecture/08-decision-and-readiness-register.md'
 elif ident.startswith('documents/') and ident.endswith('/current-custody'):path=ident[len('documents/'):-len('/current-custody')]
 else:raise AssertionError('Unexplained new historical-checker failure: '+ident)
 assert path in changes and row['detail']=={'phase':'DIVERGED'},row
 account.append({'id':ident,'disposition':'Expected historical whole-document custody divergence from exact independently reviewed D372 after-image; old acceptance/pins unchanged','path':path,'beforeSha256':changes[path]['beforeSha256'],'afterSha256':changes[path]['sha256'],'applicationManifestSha256':activation['applicationManifest']['sha256']})
write('historical-checker-provenance.json',{'standing':'Old checker results retained literally, never relabelled PASS; all new failures require exact reviewed documentation-delta provenance.','exitCode':r.returncode,'beforeCounts':before['counts'],'afterCounts':after['counts'],'failures':account,'disappearedFailures':sorted(set(old)-set(new)),'checkerUnchanged':True})
# Every application after-image still matches after validation.
assert all(sha(root/row['path'])==row['sha256'] for row in manifest['files'])
write('application-verification.json',{'standing':'Actual applied-documentation verification only; existing independently accepted design grades remain scoped; no product qualification or implementation authorization.','activation':activation,'appliedFilesVerified':len(manifest['files']),'frozenAcceptedFilesVerified':len(accepted['files']),'condition2Rows':len(rows),'scopedReviewOwners':len(owners),'unperformedQualificationGates':len(gates),'legacyCheckerCounts':after['counts'],'legacyFailuresProvenanceAccounted':len(account),'inheritedLinkFailures':len(actual_links['failures']),'implementationAuthorized':False,'passed':True})
print(json.dumps({'appliedFilesVerified':len(manifest['files']),'frozenAcceptedFilesVerified':len(accepted['files']),'unperformedQualificationGates':len(gates),'legacyCheckerCounts':after['counts'],'legacyFailuresProvenanceAccounted':len(account),'passed':True}))
