"""Explicit final application wording/output correction; no frozen source mutation."""
from pathlib import Path
import hashlib,json,shutil
B=Path('/tmp/opensip-design-corrections'); R=B/'root-application45-final-records.v1'
S=B/'application-stage.v45.2'; F=S/'files'; H=B/'application-successor-root.v2'
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
def change(rel, replacements=None, data=None):
 p=F/rel; before=R/'before'/rel; before.parent.mkdir(parents=True,exist_ok=True); assert not before.exists(); shutil.copyfile(p,before)
 text=p.read_text()
 for old,new in replacements or []:
  assert text.count(old)==1,(rel,old,text.count(old));text=text.replace(old,new)
 if data is not None:text=json.dumps(data,indent=2)+'\n'
 p.write_text(text);rows.append({'path':rel,'beforeSha256':sha(before),'afterSha256':sha(p)})
dc='docs/coop/design-corrections/'
change('docs/coop/COORDINATOR-DECISIONS.md',[
 ('A fresh actual Claude session\nindependently reviews all final units and the mixed integrated subject, including\ncurrent documentation and obligation coverage.',
 'An actual Claude reviewer that authored none of these bytes independently\nreviews all final units and the mixed integrated design. A separate fresh actual\nClaude session reviews the final application, including current documentation\nand obligation coverage.'),
 ('- Explicit product major-two semantic identities, acyclic proof/evidence/seal\n  closure, complete retained inputs, independent deterministic replay, immutable',
 '- Explicit selected identity versions: evaluator output profile 3 and unchanged\n  declared native/input profile-2 recipes; acyclic proof/evidence/seal closure,\n  complete retained inputs, independent deterministic replay, immutable')])
change('docs/v2/architecture/08-decision-and-readiness-register.md',[
 ('retained fresh independent design review of the exact final bytes','retained independent design review of the exact final bytes')])
change(dc+'README.md',[
 ('actual Claude independent reviewer independent design ACCEPT','Claude’s independent design ACCEPT')])
app=json.loads((F/dc/'application.v1.json').read_text())
app['acceptedDesignReproduction']=json.loads((B/'root-application45-reproduction-correction.v1/corrected-reproduction.json').read_text())
change(dc+'application.v1.json',data=app)
for name in ['root-application45-review-shape-correction.v1','root-application45-summary-source-correction.v1','root-application45-reproduction-correction.v1']:
 shutil.copytree(B/name,S/'support'/name)
assert sha(H/'assemble-records.successor.v1.py')==sha(S/'support/assemble-records.successor.v1.py')
report={'standing':'Root final application-only corrections before freeze. Exact source45 and historical decisions remain immutable. Identity wording follows the already accepted selected contract; actual design review continuation distinguished from fresh application origin; output reproduction uses fresh disposable relative destinations. No new normative selection or reference execution claimed.','files':rows,'passed':True}
(R/'corrections.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copytree(R,L/R.name);shutil.copytree(R,S/'support'/R.name)
print(json.dumps(report))
