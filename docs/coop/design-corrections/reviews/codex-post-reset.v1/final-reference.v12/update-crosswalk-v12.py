"""Update the pinned current crosswalk BEFORE refreshing pins or running final commands."""
from pathlib import Path
import json,hashlib
r=Path.cwd();dc=r/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rp=dc/'reviews/post-reset-review.v11/review.json';review=json.loads(rp.read_text());response=json.loads(rp.with_name('response.json').read_text());assert response['is_error'] is False
account=json.loads((dc/'post-reset-dispositions.v12.proposed.json').read_text());assert account['actualPredecessorReview']['sha256']==sha(rp)
assert (dc/'reviews/codex-post-reset.v1/released-coauthor-delta.v12/custody.json').is_file()
assert not Path('/tmp/opensip-design-corrections/final-reference-v12').exists(),'Pinned edits must precede final commands'
ref={'path':str(rp.relative_to(r)),'sha256':sha(rp),'subjectManifestSha256':'a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf','overallVerdict':review.get('verdict',review.get('overallVerdict')),'unresolvedMustIds':[x['id'] for x in review['newMustIssues']],'unresolvedShouldIds':[x['id'] for x in review['newShouldIssues']]}
p=dc/'correction-crosswalk.proposed.json';d=json.loads(p.read_text())
for row in d['items']:
 assert row['id'] in review['arDispositions']
 assert row['latestCompletedReview']['path']!=ref['path'],'Never duplicate this recording step'
 row.setdefault('historicalReviews',[]).append(row['latestCompletedReview'])
 row['latestCompletedReview']=dict(ref,selector='/arDispositions/'+row['id'],standing='Completed frozen-v11 predecessor review. Its exact required findings remain historical; v12 corrections require a new independent review, new blind consumer and complete application before readiness can change.')
p.write_text(json.dumps(d,indent=2)+'\n')
print('Updated all16 latest-completed-review links BEFORE fixture/pin refresh; no current independent acceptance.')
