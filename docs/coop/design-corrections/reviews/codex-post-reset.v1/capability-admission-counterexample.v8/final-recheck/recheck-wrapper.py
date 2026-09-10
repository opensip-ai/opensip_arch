"""Execute only after actual author handoff/source retention; preserve original counterexamples."""
from pathlib import Path
import json
root=Path.cwd();dc=root/'docs/coop/design-corrections';assert (dc/'reviews/digest-corrections-author.v3/custody.json').is_file()
original=dc/'reviews/codex-post-reset.v1/capability-admission-counterexample.v8';out=original/'final-recheck';assert not out.exists()
src=(original/'probe.py').read_text();old="out=dc/'reviews/codex-post-reset.v1/capability-admission-counterexample.v8'";assert old in src
src=src.replace(old,"out=dc/'reviews/codex-post-reset.v1/capability-admission-counterexample.v8/final-recheck'")
# The full original vectors and source-capture procedure are retained, with one output-path change.
exec(compile(src,str(original/'probe.py'),'exec'),{'__file__':str(original/'probe.py'),'__name__':'final_capability_probe'})
(out/'adapted-probe.py').write_text(src);(out/'recheck-wrapper.py').write_bytes(Path(__file__).read_bytes())
report=json.loads((out/'result.json').read_text());assert report['positive']['result']=='ADMIT'
assert len(report['vectors'])==3
for row in report['vectors']:assert row['outcome']['result']=='REFUSE',row
(out/'recheck-provenance.json').write_text(json.dumps({'standing':'Codex final-source re-execution of its own original exact vectors; not independent acceptance. Original in-progress result wording remains verbatim; these captured source images are the final coauthor bytes.','originalEvidencePreserved':True,'allOriginalInvalidValuesRefused':True,'controlAdmitted':True,'productQualification':False},indent=2)+'\n');print('all three originally admitted invalid capability manifests now refuse; control admits')
