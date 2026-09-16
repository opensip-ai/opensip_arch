"""Rebuilds check.py's admission context over the augmented review copy (frozen 9 files + the two pinned build scripts)."""
import copy, hashlib, importlib.util, json, re, sys
from pathlib import Path
from referencing import Resource
from referencing.jsonschema import DRAFT202012
sys.setrecursionlimit(20000)
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-review-02/work/augmented-copy")
sys.path.insert(0, str(SUBJ))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
chk = load("chk", SUBJ / "check.py")
ctx = chk.Context()
cm = load("check_metadata", ARCH / "docs/implementation/m1/metadata-v2/check_metadata.py")
ctx.reference, registry, documents = cm.load(ARCH)
ctx.qsp = load("qsp", ARCH / "docs/coop/design-corrections/workflows/query_surface_projection.v3.py")
owner = load("build_owner", SUBJ / "build_owner.py")
ctx.builder = load("build_fixtures", SUBJ / "build_fixtures.py")
new = {}
for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "report-projection.schema.json"):
    doc = ctx.reference.parse((SUBJ / name).read_bytes()); new[doc["$id"]] = doc
    registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
documents = dict(documents, **new)
ctx.registry, ctx.documents = registry, documents
ctx.schema = documents[chk.RID]
ctx.budget = {k: v["const"] if "const" in v else {kk: vv["const"] for kk, vv in v["properties"].items()} for k, v in ctx.schema["$defs"]["BudgetProfileV1"]["properties"].items()}
ctx.provenance = owner.PROVENANCE
ctx.inventory5 = json.loads((SUBJ / "owner/command-inventory.v5.json").read_bytes())
ctx.worst = ctx.builder.worst_values(ctx.builder.material())
fixture = json.loads((SUBJ / "fixtures.json").read_bytes())
B = fixture["bases"]
def admit_doc(doc):
    raw = doc if isinstance(doc, bytes) else chk.canonical(doc)
    try:
        chk.admit_document(ctx, raw); return "accept"
    except chk.Refused as e:
        return str(e)[:160]
    except Exception as e:
        return "UNCAUGHT " + type(e).__name__ + ": " + str(e)[:160]
def admit_env(env, command):
    try:
        chk.admit_envelope(ctx, env, command); return "accept"
    except chk.Refused as e:
        return str(e)[:160]
    except Exception as e:
        return "UNCAUGHT " + type(e).__name__ + ": " + str(e)[:160]
