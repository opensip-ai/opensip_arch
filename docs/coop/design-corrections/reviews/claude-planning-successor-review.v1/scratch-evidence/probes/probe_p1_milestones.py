import json, pathlib, sys
INPUTS = pathlib.Path(sys.argv[1])
C25 = pathlib.Path(sys.argv[2])
ARCH = INPUTS / "docs/v2/architecture"
DEFS = "$defs"
TREE_FENCE = "```text"
out = {}

cov = json.loads((ARCH / "implementation-coverage.v1.json").read_text())
cmds = json.loads((C25 / "docs/coop/design-corrections/workflows/command-inventory.v3.json").read_text())
fmts = {c["name"]: c["formats"] for c in cmds["commands"]}
rend = {x["id"]: x["milestone"] for x in cov["groups"]["renderers"]}
mfm = cov["moduleFirstMilestone"]
inv = []
for row in cov["groups"]["commands"]:
    need = max((rend[f] for f in fmts[row["id"]] if f in rend), default="M0")
    if row["milestone"] < need:
        inv.append({"command": row["id"], "commandMilestone": row["milestone"],
                    "advertisedFormats": fmts[row["id"]],
                    "latestRendererMilestone": need, "declaredOwners": row["owners"]})
out["P1_command_scheduled_before_its_renderers"] = {"count": len(inv), "rows": inv,
    "rendererMilestones": rend,
    "humanRendererOwnerFirstMilestone": mfm.get("crates/reporting/src/human_renderer.rs")}
print(json.dumps(out, indent=1))
