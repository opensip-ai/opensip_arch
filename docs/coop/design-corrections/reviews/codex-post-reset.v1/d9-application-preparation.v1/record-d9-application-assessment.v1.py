from pathlib import Path
import ast, datetime, hashlib, json, shutil

root = Path('/Users/sb/code/opensip-ai/opensip_arch')
base = Path('/tmp/opensip-design-corrections/application-assembly.v1')
dc = 'docs/coop/design-corrections/'
peer = root / (dc+'reviews/v20-d9-application-assessment.v1')
record = root / (dc+'reviews/codex-post-reset.v1/coauthor-assessment.v20-d9-application.v1.json')
assert not record.exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':str(p.relative_to(root)), 'sha256':sha(p)}
receipt = json.loads((peer/'response.json').read_text())
assert receipt['session_id']=='9a209c44-b765-43a0-bef9-044e308f57fc' and receipt['is_error'] is False
before = base/'d9-support-before.v1'
before.mkdir(exist_ok=False)
for name in ('launch-application-review.py','prepare-validation.py'):
    shutil.copyfile(base/name, before/name)
launcher = base/'launch-application-review.py'
text = launcher.read_text()
needle = '\nReview every staged current Markdown edit'
assert text.count(needle)==1
addition = '''
Explicitly assess D9-APP-1 against the bounded actual-Claude D9 assessment and Codex's qualified assessment retained in support/d9-obligation-evidence. The broad claim that no application record carries the obligation was incorrect: CB-ADV-4 in the accepted advisory account is dynamically copied by the assembler. The added row-specific carriedCrossUnitObligation on exactly DR-007 and DR-011-R08 must preserve the mandatory live D9 successor-artifact obligation, its owner, exact host-invariant to SYSTEM.OUTCOME.ILLEGAL_STATE mapping and inherited artifact hash. Determine whether the selected current composition is complete from actual normative selectors; distinguish that from the undisclosed completion of future owning-unit artifact integration or qualification. Condition 1 MET, ACCEPT-DESIGN, activation and your application review must not discharge that obligation. The phase label is a planning classification, not a verbatim normative phase requirement or a new restriction on the user's architecture authorization. Assess the actual generated records, not only static strings in the builder. Do not infer a prospective grade from a historical HARD-BLOCKED table. The bounded assessor did not execute integration checks or conduct final application review.
'''
launcher.write_text(text.replace(needle, '\n'+addition+needle))
validation = base/'prepare-validation.py'
text = validation.read_text()
needle = "finalizer=files/(dc+'finalize-application.v1.py')"
assert text.count(needle)==1
addition = """for name in ['d9-obligation-preparation.v1.json','d9-support-preparation.v1.json']:
 shutil.copyfile(Path(__file__).with_name(name),support/name)
for name in ['d9-obligation-before.v1','d9-support-before.v1','d9-obligation-evidence']:
 shutil.copytree(Path(__file__).with_name(name),support/name)
"""
validation.write_text(text.replace(needle,addition+needle))
for p in (launcher,validation,base/'assemble-records.py'): ast.parse(p.read_text())
assessment = {
 'standing':'Bounded application preparation only; no source/design/blind/application acceptance or activation.',
 'actualSessionId':receipt['session_id'],'fullRead':True,'boundedApplicationRemedyAssent':True,
 'review':ref(peer/'assessment.json'),'narrative':ref(peer/'assessment.md'),
 'receipt':ref(peer/'response.json'),'patch':ref(peer/'proposed-addendum/assemble-records.d9-obligation.patch'),
 'subjectManifest':ref(root/(dc+'reviews/candidate-subject.v20.json')),
 'findingDisposition':{'id':'D9-APP-1','severity':'SHOULD','disposition':'Accepted narrowly for row-specific visibility; prepared exact proposed insertion, pending real guarded assembly and fresh final application review.'},
 'rootQualifications':[
  'The broad no-applied-record / invisible premise is false for the generated application as a whole: existing CB-ADV-4 explicitly carries the obligation and assemble-records dynamically copies the actual advisoryApplicationAccount.',
  'The valid improvement attaches the live obligation directly to DR-007 and DR-011-R08 and prevents design acceptance being confused with artifact publication.',
  'The current selected D9FaultCause has twelve members, the inherited artifact eleven; host-invariant maps to the existing SYSTEM.OUTCOME.ILLEGAL_STATE. Current workflows supersede historical field closure while retaining compatible class/code/exit tables. No new product behavior decision is open.',
  'Historical HARD-BLOCKED and candidate wording alone does not establish the clarity of prospective accepted application grades.',
  'IMPLEMENTATION-PHASE ARTIFACT PUBLICATION is a planning classification, not verbatim source phase authority. The source assigns future owning-unit integration/qualification. User authorization already permits architecture/reference corrections; the proposal header is not a permission rule.',
  'Publishing a new normative D9 artifact would require a new source freeze and actual review. The application-only carry record does not discharge its mandatory obligation.',
  'The narrative abbreviated native schema hash suffix is incorrect. Use the exact full JSON/manifest digest f20b8353a7be50d7a0c24f413df74e35d23a4e9fc2a4ecc661235655c43c51be.',
  'The assessor read integration assertions and bounded selectors but did not execute integration. Token-presence observations alone do not establish mapper behavior; earlier actual root/route checks provide separate evidence.',
  'The exact authored patch was prepared in the builder only. AST parsing is not a successful assembly or actual application. Real accepted source, fresh blind and root assents remain mandatory.'
 ],
 'actualAssemblyTested':False,'independentReview':False,'implementationAuthorized':False,
 'preparation':json.loads((base/'d9-obligation-preparation.v1.json').read_text()),
 'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()
}
record.write_text(json.dumps(assessment,indent=2)+'\n')
evidence=base/'d9-obligation-evidence';evidence.mkdir(exist_ok=False)
shutil.copytree(peer,evidence/'actual-claude')
shutil.copyfile(record,evidence/record.name)
prep={'standing':'Prepared support custody and explicit fresh application-review scope only; no application execution.',
      'rootAssessment':ref(record),'syntaxParsed':True,'actualAssemblyTested':False,
      'changes':[{'path':str(base/n),'beforeSha256':sha(before/n),'afterSha256':sha(base/n)} for n in ('launch-application-review.py','prepare-validation.py')]}
(base/'d9-support-preparation.v1.json').write_text(json.dumps(prep,indent=2)+'\n')
retained=record.parent/'d9-application-preparation.v1';retained.mkdir(exist_ok=False)
for name in ('assemble-records.py','launch-application-review.py','prepare-validation.py','d9-obligation-preparation.v1.json','d9-support-preparation.v1.json'):
    shutil.copyfile(base/name,retained/name)
for name in ('d9-obligation-before.v1','d9-support-before.v1'):
    shutil.copytree(base/name,retained/name)
shutil.copyfile(Path(__file__),retained/Path(__file__).name)
print(json.dumps(prep,indent=2))
