"""Relation payload path law beyond dot segments, through identity-model.v3 validate_registered_record (pinned vs scoped)."""
import sys, os, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); COPY = os.path.join(HERE, "copy")
sys.pycache_prefix = os.path.join(HERE, "tmp", "pycache"); sys.path.insert(0, os.path.join(COPY, "tools"))
import common as CM, owner_successor as OS
arch = CM.arch_root()
succ = json.load(open(os.path.join(COPY, "owner-pattern-successor.v1.json")))
pin = OS.load_models(arch, None, "p5_")["IM3"]; sco = OS.load_models(arch, succ, "s5_")["IM3"]
rel = json.load(open(os.path.join(arch, CM.ARCH_PINS["relationRegistry2"][0])))
fp = rel["$defs"]["FilePayloadV1"]
def res(m, sel, v):
    try:
        m.validate_registered_record("foundation/relation-payload-schemas.v2.json", sel, v); return "admitted"
    except Exception as e:
        return "refused:" + str(e)[:60]
out = {"FilePayloadV1": json.dumps(fp)[:600], "cases": {}}
base = {}
for k, sch in fp.get("properties", {}).items():
    base[k] = "src/a.rs" if k == "path" else None
req = fp.get("required", [])
for v in ["src/a.rs", "a//b.rs", "a/", "a" + "\n" + "b.rs", "a" + chr(7) + "b.rs", "a/.." + "\n"]:
    out["cases"][json.dumps(v)] = {"CanonicalPath": [res(pin, "#/$defs/CanonicalPath", v), res(sco, "#/$defs/CanonicalPath", v)]}
json.dump(out, open(os.path.join(HERE, "probe_05b.out.json"), "w"), indent=1, ensure_ascii=True)
print(json.dumps(out, indent=1, ensure_ascii=True))
