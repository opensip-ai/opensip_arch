from pathlib import Path
import json,hashlib,shutil
r=Path.cwd();dc=r/'docs/coop/design-corrections';rev=dc/'reviews/post-reset-review.v10';author=dc/'reviews/digest-corrections-author.v9';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (rev/'custody.json').is_file() and (author/'custody.json').is_file()
for p in [rev,author]:assert json.loads((p/'response.json').read_text())['is_error'] is False
review=json.loads((rev/'review.json').read_text());assert review['verdict']=='CHANGES_REQUIRED'
# Root must have read the final review and explicitly accounted every required finding before applying.
account=dc/'post-reset-dispositions.v11.proposed.json';d=json.loads(account.read_text());assert d['actualPredecessorReview']['sha256']==sha(rev/'review.json')
required={x['id'] for k in ('newMustIssues','newShouldIssues') for x in review[k]};assert {x['id'] for x in d['items']}==required
mp=dc/'reviews/candidate-subject.v10.json';assert sha(mp)=='82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd';m=json.loads(mp.read_text());by={x['path']:x for x in m['files']}
for row in m['files']:
 assert sha(Path(m['snapshotRoot'])/row['path'])==row['sha256']
 if row['path']!='docs/coop/design-corrections/reviews/NEXT-REVIEW.md':assert sha(r/row['path'])==row['sha256'],row['path']
h=json.loads((author/'handoff.json').read_text());owned=h['ownedFilesChanged'];assert {x['path'] for x in owned}=={'docs/coop/design-corrections/foundation/identity-model.py','docs/coop/design-corrections/foundation/check-identity.py'}
out=dc/'reviews/codex-post-reset.v1/released-coauthor-delta.v11';assert not out.exists();out.mkdir();rows=[]
for row in owned:
 src=author/'author-source'/row['path'];assert sha(src)==row['sha256'];assert sha(r/row['path'])==by[row['path']]['sha256']
 q=out/'before'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/row['path'],q)
 rows.append({'path':row['path'],'beforeSha256':sha(q),'afterSha256':row['sha256'],'actualReleasedSource':str(src.relative_to(r))})
# All checks precede the reviewed two-file update; captured before-images preserve exact candidate bytes.
for row in owned:shutil.copyfile(author/'author-source'/row['path'],r/row['path']);assert sha(r/row['path'])==row['sha256']
shutil.copyfile(__file__,out/'apply.py');(out/'custody.json').write_text(json.dumps({'standing':'Codex applies exact released actual-Claude disposable correction after completed v10 review and coauthor handoff. Proposed successor only; new independent review/blind/application still required.','baseManifestSha256':sha(mp),'actualReviewSha256':sha(rev/'review.json'),'actualCoauthorHandoffSha256':sha(author/'handoff.json'),'files':rows,'implementationAuthorized':False},indent=2)+'\n')
print('Applied exact two-file released coauthor delta; before-images retained. No readiness change.')
