import importlib.util, json, sys, copy, hashlib
from pathlib import Path
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-review-01/work/subject-copy")
spec = importlib.util.spec_from_file_location("cm", ARCH/"docs/implementation/m1/metadata-v2/check_metadata.py")
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
ref, registry, docs = cm.load(ARCH)
spec = importlib.util.spec_from_file_location("chk", SUBJ/"check.py")
chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
from referencing import Resource
from referencing.jsonschema import DRAFT202012
schema_raw = (SUBJ/"report-projection.schema.json").read_bytes()
schema = ref.parse(schema_raw)
registry = registry.with_resource(chk.RID, Resource(contents={k:v for k,v in schema.items() if k!="$schema"}, specification=DRAFT202012))
inventory = json.loads((ARCH/"docs/implementation/m1/metadata-v2/command-inventory.v4.json").read_bytes())
fixture = json.loads((SUBJ/"fixtures.json").read_bytes())
def admit(doc):
    try:
        chk.admit(ref, registry, schema, inventory, doc); return "accept"
    except chk.Refused as e:
        return str(e)[:220]
sys.setrecursionlimit(10000)
