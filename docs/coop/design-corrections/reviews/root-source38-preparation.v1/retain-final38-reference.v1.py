from pathlib import Path
from collections import Counter
import json,hashlib,shutil,argparse
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');L=R/'docs/coop/design-corrections/reviews';O=B/'root-final38-reference-binding.v1';mf=L/'candidate-subject.v38.json';m=json.loads(mf.read_bytes());S=Path(m['snapshotRoot']);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert h(mf)==a.manifest_sha256;members={r['path']:r for r in m['files']}
commands=json.loads((O/'reference-checks.json').read_bytes());assert commands['passed'] and len(commands['commands'])==7
for row in commands['commands']:
 assert row['sourceSha256']==members[row['source']]['sha256']==h(S/row['source']) and row['exitCode']==0 and not row['timedOut']
 if row['executedAs']=='top-level suite child':
  assert h(O/(row['name']+'.stdout'))==row['stdoutSha256'] and h(O/(row['name']+'.stderr'))==row['stderrSha256']
checks=[row for row in commands['commands'] if row['executedAs']=='top-level suite child'];assert len(checks)==6
for name,rel in [('native-report.json','docs/coop/design-corrections/native/native-evidence-report.v2.json'),('workflow-surface-report.json','docs/coop/design-corrections/workflows/workflows-report.v1.json')]:
 assert not (O/name).exists();assert h(B/'termination-exclusivity-successor.v1/source'/rel)==members[rel]['sha256'];shutil.copy2(S/rel,O/name)
assert json.loads((O/'workflows.json').read_bytes())['check']['reportSha256']==h(O/'workflow-surface-report.json')
report={'standing':'Derived six-group view of actual reference-checks.json execution; not a repeated run. Original runner receipt preserved. Generated native/workflow reports copied exactly from their executed source outputs, verified against frozen38.','passed':True,'checks':checks,'evaluatorChildren':commands['evaluatorBudget']['children'],'originalRunnerReceiptSha256':h(O/'reference-checks.json')};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
commands.update(subjectManifestSha256=h(mf),currentProfilePinsSha256=h(S/'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json'))
commands['standing']+=' Exact final38 subject binding added after verified freeze; no historical execution relabelled.'
(O/'reference-checks.bound.json').write_text(json.dumps(commands,indent=2)+'\n')
D=L/'codex-post-reset.v1/final-reference.v38';assert not D.exists();shutil.copytree(O,D);shutil.copy2(D/'reference-checks.json',D/'runner-original-reference-checks.json');shutil.copy2(D/'reference-checks.bound.json',D/'reference-checks.json')
i=json.loads((D/'foundation/identity-report.json').read_bytes());ids=[r['id'] for r in i['checks'] if r['passed']];count=Counter(ids);c={'standing':'Measured passing calls and distinct ids in actual final38 execution, not semantic coverage or product qualification.','passingCalls':len(ids),'distinctIds':len(count),'duplicateExtraInstances':len(ids)-len(count),'duplicates':{k:v for k,v in count.items() if v>1},'report':(D/'foundation/identity-report.json').relative_to(R).as_posix(),'reportSha256':h(D/'foundation/identity-report.json')};assert c['passingCalls']==i['passed'] and i['failed']==0
(L/'codex-post-reset.v1/identity-check-counts.v38.json').write_text(json.dumps(c,indent=2)+'\n')
assert (B/'root-final38-custody.v1/verification.json').read_bytes()==(L/'root-final38-custody.v1/verification.json').read_bytes()
print(json.dumps({'allGroupsPassed':True,'evaluatorChildren':report['evaluatorChildren'],'identity':c,'boundCommandsSha256':h(D/'reference-checks.json')}))
