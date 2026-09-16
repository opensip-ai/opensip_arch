from pathlib import Path
import json,hashlib,shutil,ast
base=Path(__file__).parent
backup=base/'evidence-clarification-before.v1';backup.mkdir(exist_ok=False)
names=['assemble-records.py','prepare-validation.py','launch-application-review.py']
for n in names:shutil.copyfile(base/n,backup/n)
def replace(s,old,new):
 assert s.count(old)==1,(old,s.count(old))
 return s.replace(old,new)
p=base/'assemble-records.py';s=p.read_text()
s=replace(s,"v['effectiveWhen']=effective;evals.append(v)","v['effectiveWhen']=effective;v['independentDisposition']=design['inheritedResidualDispositions']['DR-011-R12'];v['gradeAuthority']='Fresh final application review must substantively assess this proposed design grade; the design review only carried this inherited account unchanged.';v['finalApplicationReviewBinding']=activation;evals.append(v)")
s=replace(s," if '-R' in rid:\n", " v['independentDisposition']=design['inheritedResidualDispositions'][rid];v['gradeAuthority']='Fresh final application review must substantively assess this proposed design grade; CARRIED-UNCHANGED does not grade or discharge an inherited residual.';v['finalApplicationReviewBinding']=activation\n if '-R' in rid:\n")
s=replace(s,"writej(dc+'application.v1.json',app)", """# Join the accepted historical summary with its exact count measurement without rewriting either.
summary_rel=dc+'validation-summary.v1.json';counts_rel=dc+f'reviews/codex-post-reset.v1/identity-check-counts.{dv}.json'
summary=load(summary_rel);counts=load(counts_rel)
assert summary['foundation']['components']['identity']==counts['passingCalls']
assert counts['passingCalls']==counts['distinctIds']+counts['duplicateExtraInstances']
app['referenceEvidenceSummary']={'validationSummary':ref(summary_rel),'identityCountMeasurement':ref(counts_rel),'foundationPassingCalls':summary['foundation']['checksPassed'],'identityPassingCalls':counts['passingCalls'],'identityDistinctIds':counts['distinctIds'],'identityDuplicateExtraInstances':counts['duplicateExtraInstances'],'standing':'Reference evidence counts, not a coverage or product-qualification claim. Historical pending-review labels describe the original frozen summary; actual accepted review is separately pinned above.'}
commands_rel=dc+f'reviews/codex-post-reset.v1/final-reference.{dv}/reference-checks.json'
original=load(commands_rel);reproduction=[]
for command in original['commands']:
 source=command['source'];assert accepted_files[source]['sha256']==command['sourceSha256']
 args=list(command['command']);assert args[1:3]==['-I','-B'] and args[3].endswith('/'+source)
 args[3]=source
 reproduction.append({'name':command['name'],'source':source,'sourceSha256':command['sourceSha256'],'argv':args})
app['acceptedDesignReproduction']={'originalExecutedCommandRecord':ref(commands_rel),'designManifest':manifest_ref,'workingDirectory':'A disposable full copy of the exact accepted snapshot, verified against every manifest entry before execution. Never execute these report-writing commands in the immutable accepted snapshot.','interpreter':'The recorded isolated Python environment includes jsonschema; an equivalent environment may replace argv[0]. Verify required imports before execution.','commands':reproduction,'standing':'Executable relative-source reproduction metadata; original absolute command records and reports remain immutable historical evidence. Application-stage reruns separately account for the two documentation-provenance pin changes.'}
writej(dc+'application.v1.json',app)""")
p.write_text(s)
p=base/'launch-application-review.py';s=p.read_text();s=replace(s,"Each grade must be justified by its actual contract and review, not merely a count or broad link.","Each grade must be justified by its actual contract and review, not merely a count or broad link. IMPORTANT: the v12 design reviewer explicitly records all27 inherited rows and all30 evaluation subresiduals as CARRIED-UNCHANGED and says it did NOT grade, close or discharge them; DR201..205 acceptance covers routing only. Applied wrappers preserve those literal dispositions and bind proposed grades to YOUR new final application review and eventual activation. Substantively assess each proposed grade using exact normative contracts and applicable prior review basis; never turn CARRIED-UNCHANGED or routing-only acceptance into a grade by inference. Assess the v12-A1 joined767/757/10 reference-count metadata and v12-A2 relative-source reproduction commands with exact source pins, preserving the original accepted evidence.")
p.write_text(s)
p=base/'prepare-validation.py';s=p.read_text();s=replace(s,"finalizer=files/(dc+'finalize-application.v1.py')", """for name in ['assemble-records.py','prepare-validation.py','launch-application-review.py','clarify-application-evidence.v1.py','evidence-clarification.v1.json','subject-envelope-adapter-custody.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['evidence-clarification-before.v1','subject-envelope-adapter.v1']:
 shutil.copytree(Path(__file__).with_name(name),support/name)
finalizer=files/(dc+'finalize-application.v1.py')""");p.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in names:ast.parse((base/n).read_text())
(base/'evidence-clarification.v1.json').write_text(json.dumps({'standing':'Prospective application tooling only; no candidate semantic source changed and no application performed. Subject-envelope adapter preceded this clarification; required-findings hardening remains earlier historical evidence.','changes':[{'path':n,'beforePath':'evidence-clarification-before.v1/'+n,'beforeSha256':sha(backup/n),'afterSha256':sha(base/n)} for n in names]},indent=2)+'\n')
# Preserve exact adapter inputs and outputs independently of subsequent clarification.
ad=base/'subject-envelope-adapter.v1';ad.mkdir(exist_ok=False);rows=[]
post=base.parent/'codex-post-reset.v1'
for owner,n,after in [(post,'retain-independent-v12.py',post/'retain-independent-v12.py'),(post,'launch-consumer-b-v2.py',post/'launch-consumer-b-v2.py'),(base,'assemble-records.py',backup/'assemble-records.py'),(base,'verify-applied.py',base/'verify-applied.py')]:
 before=owner/(Path(n).stem+'.before-subject-envelope-support.py')
 assert before.exists(),before
 for label,src in [('before',before),('after',after)]:shutil.copyfile(src,ad/(label+'-'+n))
 rows.append({'tool':n,'beforePath':'subject-envelope-adapter.v1/before-'+n,'beforeSha256':sha(before),'afterPath':'subject-envelope-adapter.v1/after-'+n,'afterSha256':sha(after)})
(base/'subject-envelope-adapter-custody.v1.json').write_text(json.dumps({'standing':'Actual review JSON untouched. Adapter permits a consistent exact top-level or nested subject digest, rejects absent/conflicting values. First retention failed before destination creation; later retention succeeded. These bytes precede separately recorded evidence clarification.','changes':rows},indent=2)+'\n')
print('Recorded prospective clarification and exact adapter custody; no live design/application edits.')
