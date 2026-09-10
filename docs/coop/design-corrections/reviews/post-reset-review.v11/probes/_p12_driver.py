
import json,sys,runpy
target=sys.argv[1]; model=sys.argv[2]; out=sys.argv[3]
# locate the statements of interest by TEXT in identity-model.py
src=open(model).read().splitlines()
want={}
for i,line in enumerate(src,1):
    s=line.strip()
    if s.startswith("previous=seen.get(path)"):want[i]="record.lookupPrevious"
    if s.startswith("missing=previous['missing'] or missing"):want[i]="record.mergeBranch.missingMonotonic"
    if s.startswith("annotations=previous['annotations']+[a for a in annotations"):want[i]="record.mergeBranch.v10merge"
    if s.startswith("if not previous['annotations'] or not annotations:annotations=[]"):want[i]="record.mergeBranch.v10poisonTest"
    if s.startswith("merged=list(previous['annotations'])"):want[i]="record.mergeBranch.v11merge"
    if s.startswith("missing=not annotations"):want[i]="record.missingFromIncoming"
    if s.startswith("if uncovered:raise"):want[i]="law.uncoveredRaise"
    if s.startswith("raise C.AdmissionError('RELATION_DIGEST_ANNOTATION_CONFLICT"):want[i]="law.conflictRaise"
    if s.startswith("if sighting.get('missing'):continue"):want[i]="law.skipMissingSighting"
counts={v:0 for v in want.values()}
mabs=__import__("os").path.abspath(model)
def tracer(frame,event,arg):
    if event=="call":
        return tracer if __import__("os").path.abspath(frame.f_code.co_filename)==mabs else None
    if event=="line":
        n=want.get(frame.f_lineno)
        if n:counts[n]+=1
    return tracer
sys.argv=[target]
sys.settrace(tracer)
try:
    runpy.run_path(target,run_name="__main__")
except SystemExit:
    pass
finally:
    sys.settrace(None)
open(out,"w").write(json.dumps(counts,indent=2))
