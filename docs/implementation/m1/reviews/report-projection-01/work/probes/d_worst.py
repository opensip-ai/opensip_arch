import sys; sys.path.insert(0,'.')
from common import *
C="urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
G="urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
W = "\U0001F600"  # 4-byte UTF-8 scalar, 1 code point
def seg_path(ch, total=4096):
    segs=[]; n=0
    while True:
        need = 255 if not segs else 256
        if n+need > total: break
        segs.append(ch*255); n+=need
    return "/".join(segs)
out={}
# FindingSurface worst case (matched correspondence carries partialFingerprints)
f = copy.deepcopy(fixture["measurementSamples"]["finding"])
f["qualifiedName"] = W*4096; f["messageCode"] = W*4096; f["subjectPath"] = seg_path(W)
f["ruleId"] = "a"*128
ref.validate({"$ref": C+"FindingSurface"}, f, registry)
fb = len(chk.canonical(f)); out["FindingSurfaceWorstBytes"]=fb
out["envelope100kFindingsWorstBytes"]=fb*100000
out["envelopeMaxCanonicalBytes"]=83886080
out["findingsFitEnvelopeCeilingWorst"]=83886080//fb
# GraphEndpoint worst case (package kind carries packageManifestPath)
ep = {"universe":"a"*64,"kind":"package","nativeSubjectId":W*4096,"packageManifestPath":seg_path(W)}
ref.validate({"$ref": G+"GraphEndpoint"}, ep, registry)
row = copy.deepcopy(fixture["measurementSamples"]["neighborRow"]); row["source"]=ep; row["target"]=ep; row["relation"]="a"*128; row["resolution"]="b"*128
ref.validate({"$ref": G+"GraphNeighborRow"}, row, registry)
rb=len(chk.canonical(row)); out["GraphNeighborRowWorstBytes"]=rb
out["neighborPage1000WorstBytes"]=rb*1000
out["neighborRowsFitExplorationWorst"]=4194304//rb
path={"hopCount":64,"start":ep,"target":ep,"nodes":[ep]*65,"edges":[{"factId":"fact2:"+"a"*64,"source":ep,"target":ep}]*64}
ref.validate({"$ref": G+"GraphPathRow"}, path, registry)
out["GraphPathRow64HopWorstBytes"]=len(chk.canonical(path))
# Same identities with realistic ASCII lengths, for contrast
ep2={"universe":"a"*64,"kind":"symbol","nativeSubjectId":"ts:src/x.ts#f"}
p2={"hopCount":64,"start":ep2,"target":ep2,"nodes":[ep2]*65,"edges":[{"factId":"fact2:"+"a"*64,"source":ep2,"target":ep2}]*64}
out["GraphPathRow64HopShortIdsBytes"]=len(chk.canonical(p2))
print(json.dumps(out, indent=1))
json.dump(out, open("d_worst.json","w"), indent=1)
