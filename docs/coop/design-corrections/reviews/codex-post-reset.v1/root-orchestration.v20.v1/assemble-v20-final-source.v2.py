"""Apply actual Claude's precise sentinel correction to a new isolated proposal, preserving v1."""
from pathlib import Path
import json,hashlib,subprocess,shutil,difflib
B=Path('/tmp/opensip-design-corrections');P=B/'v20-final-source.v1';F=B/'v20-final-source.v2';assert not F.exists();F.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run(['cp','-Rc',str(P/'work'),str(F/'work')],check=True)
rel='docs/coop/design-corrections/foundation/check-identity.py';patch=B/'v20-final-delta-peer.v1/work/probe/patched-check-identity.py';old=(P/'work'/rel).read_text();new=patch.read_text()
a="""def _adopt_scope_detail(spec_rows,document):
    try:_adopt(spec_rows,document)
    except W.Refusal as exc:return exc.detail
    return None
check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',
      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) is None)"""
b="""_NO_REFUSAL=object()
def _adopt_scope_detail(spec_rows,document):
    # Sentinel rather than None: a Refusal may carry detail=None - adopt_baseline's OWN
    # duplicate-entry guard raises exactly that - so projecting to `.detail` alone cannot
    # distinguish "refused" from "returned", which is what this positive must assert.
    try:_adopt(spec_rows,document)
    except W.Refusal as exc:return exc.detail
    return _NO_REFUSAL
check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',
      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) is _NO_REFUSAL)"""
assert old.count(a)==1 and new==old.replace(a,b),'Exact Claude patch must be only change'
shutil.copyfile(patch,F/'work'/rel)
m=json.loads((P/'proposal.json').read_text());m['previousProposal']={'path':str(P/'proposal.json'),'sha256':sha(P/'proposal.json')};m['standing']='Final source20 composition with actual-Claude sentinel correction; requires final bounded confirmation before root assent and pin/check/freeze.';m['rootChanges'].append('Actual Claude sentinel correction distinguishes successful return from a Refusal whose detail is None. Prior is-None claim was too broad; historical v1 preserved.')
for row in m['files']:
 if row['path']==rel:row['beforeFinalPeerCorrectionSha256']=row['afterSha256'];row['afterSha256']=sha(F/'work'/rel)
 else:assert sha(F/'work'/row['path'])==row['afterSha256']
(F/'proposal.json').write_text(json.dumps(m,indent=2)+'\n')
(F/'final-peer-correction.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel)))
for row in m['files']:
 q=F/'complete-diffs'/(Path(row['path']).name+'.diff');q.parent.mkdir(exist_ok=True);q.write_text(''.join(difflib.unified_diff((B/'candidate-subject.v19'/row['path']).read_text().splitlines(True),(F/'work'/row['path']).read_text().splitlines(True),fromfile='a/'+row['path'],tofile='b/'+row['path'])))
print(json.dumps({'manifestSha256':sha(F/'proposal.json'),'correctedCheckerSha256':sha(F/'work'/rel),'files':len(m['files'])}))
