"""Prepare successor recording to bind the cumulative source account; no recording or acceptance yet."""
from pathlib import Path
import shutil,hashlib,json,ast
b=Path(__file__).parent;before=b/'before-advisory-source.v15';before.mkdir(exist_ok=False)
names=['prepare-records-v15.py','record-technical-v15.py','launch-review-v15.py']
rows=[]
for name in names:
 p=b/name;shutil.copy2(p,before/name);s=p.read_text()
 s=s.replace("assessment=ev/'coauthor-assessment-bv4-v4.json'","assessment=ev/'successor-source-assessment.v15.json'")
 s=s.replace("assessment=dc/'reviews/codex-post-reset.v1/coauthor-assessment-bv4-v4.json'","assessment=dc/'reviews/codex-post-reset.v1/successor-source-assessment.v15.json'")
 if name=='record-technical-v15.py':
  s=s.replace("a=read(ev/'coauthor-assessment-bv4-v4.json')","a=read(ev/'successor-source-assessment.v15.json')")
  s=s.replace("'sourceAssessment':ref(ev/'coauthor-assessment-bv4-v4.json')","'sourceAssessment':ref(ev/'successor-source-assessment.v15.json')")
  s=s.replace('Original rejected source, initial test failures and later corrections remain distinguishable.', 'Original rejected source, initial test failures and later corrections remain distinguishable. The subsequent actual-Claude assessment in ../v14-advisory-clarification.v1/ covers two exact wording clarifications: existing result projection versus four refusal-code additions, and required producer enforcement versus the retained-closure call site exhibited by the reference. The cumulative successor-source-assessment.v15.json binds both phases without extending the earlier five-file assent to later bytes by inference.')
  s=s.replace("'launch-review-v15.py']", "'launch-review-v15.py','launch-v14-advisory-clarification.py','adapt-v15-for-advisory-source.py']")
 if name=='launch-review-v15.py':
  s=s.replace('Review this successor substantively:', 'Also read the actual retained v14-advisory-clarification.v1 assessment, both exact changes, and successor-source-assessment.v15.json. The v14 independent review accepted with zero MUST/SHOULD and two advisories; those advisories are addressed by source clarification, not silently treated as required findings or ignored. Independently assess that the public projection sentence preserves all four refusal-code additions and that anchorLaw.enforcedAt preserves the producer obligation while accurately limiting exhibited reference evidence to retained closure. No new producer implementation is claimed.\n\nReview this successor substantively:')
 assert s!=p.read_text();ast.parse(s);p.write_text(s)
 rows.append({'path':name,'beforeSha256':hashlib.sha256((before/name).read_bytes()).hexdigest(),'afterSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(before/'preparation.json').write_text(json.dumps({'standing':'Prepared successor tool edits only; no review, integration, validation, freeze or acceptance performed by this script.','files':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
