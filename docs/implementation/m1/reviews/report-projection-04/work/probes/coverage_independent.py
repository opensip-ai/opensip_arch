"""Reviewer-independent coverage probe (review-04). Applies the frozen overlay with reviewer code (not build_owner.apply_overlay),
applies only the recorded scoped workaround in memory, runs the owned validate_coverage on base and overlay, then the C2 control."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-subject-04")
pins = {p["path"]: p for p in json.loads((SUBJ / "source-pins.json").read_bytes())["files"]}
def pinned_bytes(path):
    raw = Path(path).read_bytes()
    pin = pins[str(path)]
    assert hashlib.sha256(raw).hexdigest() == pin["sha256"] and len(raw) == pin["bytes"], path
    return raw
def load_source(name, path):
    raw = pinned_bytes(path)
    module = type(sys)(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module
planning = load_source("planning", ARCH / "docs/operations/check_implementation_planning.py")
overlay = json.loads((SUBJ / "owner/implementation-coverage-successor.v1.json").read_bytes())
base = json.loads(pinned_bytes(ARCH / overlay["base"]["path"]))
assert hashlib.sha256((ARCH / overlay["base"]["path"]).read_bytes()).hexdigest() == overlay["base"]["sha256"]
accepted = json.loads(Path("/tmp/opensip-implementation/m1-metadata-subject-02.json").read_bytes())
acc = next(f for f in accepted["files"] if f["path"].endswith("implementation-coverage.v2.json"))
out = {"historicalCoverageEqualsAcceptedSubject02": acc["sha256"] == overlay["base"]["sha256"]}
applied = copy.deepcopy(base)
for ch in overlay["rowChanges"]:
    row = applied["groups"][ch["group"]][ch["index"]]
    assert row["id"] == ch["id"]
    row["source"] = ch["source"]
    for k in ("owners", "reviewIssues"):
        if k in ch:
            row[k] = ch[k]
    if "verificationMethod" in ch:
        row["verification"]["method"] = ch["verificationMethod"]
    for k, v in ch.get("fields", {}).items():
        row[k] = v
    unknown = set(ch) - {"group", "index", "id", "source", "owners", "reviewIssues", "verificationMethod", "fields"}
    assert not unknown, unknown
for ad in overlay["rowAdditions"]:
    applied["groups"][ad["group"]].append(ad["row"])
applied["reviewIssues"] = applied["reviewIssues"] + overlay["reviewIssueAdditions"]
sources = {}
for key, pin in base["sources"].items():
    raw = pinned_bytes(ARCH / pin["path"])
    sources[key] = json.loads(raw) if pin["path"].endswith(".json") else raw.decode()
inv5 = json.loads((SUBJ / "owner/command-inventory.v5.json").read_bytes())
wf_path = base["sources"]["workflows-and-surfaces"]["path"]
text = sources["workflows-and-surfaces"]
ov = next(o for o in json.loads((SUBJ / "owner/passage-overrides.v1.json").read_bytes())["overrides"] if o["path"] == wf_path)
lines = text.split("\n")
assert lines[ov["line"] - 1] == ov["before"]
lines[ov["line"] - 1] = ov["after"]
sources_next = dict(sources, commands=inv5, **{"workflows-and-surfaces": "\n".join(lines)})
inventory = json.loads(pinned_bytes(ARCH / "docs/implementation/m1/repository-file-inventory.v3.json"))
def run(data, srcs):
    try:
        planning.validate_coverage(data, srcs, inventory)
        return "valid"
    except ValueError as exc:
        return str(exc)
delivery = ("commands", "queryOperations", "renderers", "capabilityCells", "workflowGoldens")
owners = {o for g in delivery for r in base["groups"][g] for o in r["owners"]}
out["baseDeliveryOwnersMissingFromModuleFirstMilestone"] = sorted(owners - set(base["moduleFirstMilestone"]))
out["baseExtraModuleFirstMilestoneKeys"] = sorted(set(base["moduleFirstMilestone"]) - owners)
assets_rows = [(g, r["id"], r["milestone"]) for g in delivery for r in base["groups"][g] if "crates/reporting/src/assets.rs" in r["owners"]]
out["assetsRsDeliveryRows"] = assets_rows
out["unscoped"] = {"base": run(base, sources), "overlay": run(applied, sources_next)}
def scoped(data, value="M1"):
    d = copy.deepcopy(data)
    d["moduleFirstMilestone"]["crates/reporting/src/assets.rs"] = value
    return d
out["scopedM1"] = {"base": run(scoped(base), sources), "overlay": run(scoped(applied), sources_next)}
out["scopedM0"] = {"base": run(scoped(base, "M0"), sources), "overlay": run(scoped(applied, "M0"), sources_next)}
out["scopedM6"] = {"base": run(scoped(base, "M6"), sources), "overlay": run(scoped(applied, "M6"), sources_next)}
c2 = scoped(applied)
fit = next(r for r in c2["groups"]["commands"] if r["id"] == "fit")
fit["parityFields"] = fit["parityFields"][:5]
out["C2-fit-parity-reverted"] = run(c2, sources_next)
c2b = scoped(applied)
next(r for r in c2b["groups"]["reportFeatures"] if r["id"] == "R03")["reviewIssues"] = ["RP-DO-99"]
out["C2b-untracked-review-issue"] = run(c2b, sources_next)
c2c = scoped(applied)
c2c["groups"]["commands"].pop()
out["C2c-row-removed"] = run(c2c, sources_next)
out["reportFeatureReviewIssues"] = {r["id"]: r["reviewIssues"] for r in applied["groups"]["reportFeatures"] if r["reviewIssues"]}
Path(__file__).with_name("coverage_independent.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
