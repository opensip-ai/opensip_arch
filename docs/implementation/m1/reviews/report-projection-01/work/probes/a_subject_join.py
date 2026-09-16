from common import *
ids = docs["urn:opensip:product-v1:identity:v3"]
print("evaluation-subject def:", json.dumps(ids["$defs"]["evaluation-subject"])[:700])
dd = ids.get("x-opensip-digest-domains",{})
print("h-identity rule:", json.dumps({k:v for k,v in dd.items() if "h-identity" in json.dumps(v)[:4000] and k not in ("byDomain",)})[:1500])
G = docs["urn:opensip:product-v1:workflows:evaluator3:graph-query:3"]["$defs"]
print("StoredKind:", json.dumps(G["StoredKind"]))
print("Text:", json.dumps(ids["$defs"].get("Text")))
def endpoints(o, out):
    if isinstance(o, dict):
        if set(o) >= {"universe","kind","nativeSubjectId"} and len(set(o)-{"universe","kind","nativeSubjectId","packageManifestPath"})==0:
            out.append(o)
        for v in o.values(): endpoints(v,out)
    elif isinstance(o,list):
        for v in o: endpoints(v,out)
def subj(e):
    v = {"schemaVersion":3, **e}
    return "subject3:" + ref.identity("evaluation-subject", v)
base = fixture["bases"]["audit-full"]
eps=[]; endpoints(base["panels"], eps)
fids = {f["subjectId"] for f in base["envelope"]["findings"]}
print("fixture endpoints", len(eps), "finding subjectIds", fids)
print("computed", sorted({subj(e) for e in eps if e["kind"] in ("file","symbol","package")})[:6])
print("any endpoint joins a finding:", bool({subj(e) for e in eps if e["kind"] in ("file","symbol","package")} & fids))
# witnesses: look for any evaluation-subject preimage with its subject3 to confirm the recipe
w = json.loads(open("/tmp/opensip-implementation/m1-schema-witnesses-01/witnesses.json").read())
hits=[]
def scan(o):
    if isinstance(o, dict):
        if o.get("schemaVersion")==3 and set(o)>= {"universe","kind","nativeSubjectId"}: hits.append(o)
        for v in o.values(): scan(v)
    elif isinstance(o,list):
        for v in o: scan(v)
scan(w)
txt=json.dumps(w)
print("witness evaluation-subject preimages:", len(hits))
for h in hits[:5]:
    s = "subject3:"+ref.identity("evaluation-subject", h)
    print(" ", s, "appears in witnesses:", s in txt)
