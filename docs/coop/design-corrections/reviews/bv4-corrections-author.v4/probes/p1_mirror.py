"""Focused check that the three availability-carrier statements agree, without the 1200-call suite."""
import pathlib,sys,json
C=pathlib.Path(sys.argv[1])
def para(path,opening):
    hits=[b for b in (C/path).read_text().split('\n\n') if opening in b]
    assert len(hits)==1,(path,opening,len(hits))
    return ' '.join(hits[0].split())
A=para('admission-and-qualification.md','The registry states **availability**, never scope')
O=para('admission-and-qualification.md','The authenticated release declaration registry supplies')
N=para('native-evidence.md','**The public carrier, named')
W=para('workflows-and-surfaces.md','**Release-availability absence rides the invocation')
out={'admissionNamesSelected':all(t in A for t in ('CommandEnvelope.availability','CapabilityAvailabilityV1','workspaceRoot')),
 'admissionRepudiatesSuperseded':('Earlier revisions of this paragraph named' in A and 'neither can deliver this' in A),
 'admissionKeepsAdvisory':('advisory' in A and 'terminates nothing' in A),
 'admissionNamesEveryAnalysisSurface':('every' in A and 'requestClass: analysis' in A),
 'openingNoLongerFixesScope':('exact applicable TS/JS/Rust capabilities' not in O and 'does **not** fix the request' in O),
 'allThreeAgree':all(all(t in p for t in ('CommandEnvelope.availability','CapabilityAvailabilityV1')) for p in (A,N,W))}
print(json.dumps(out,indent=1))
