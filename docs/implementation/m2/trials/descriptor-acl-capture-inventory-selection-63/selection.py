"""Select reviewed additive inventory63 only, after root substantive reading."""
from pathlib import Path, PurePosixPath
import argparse, json, hashlib, subprocess, tarfile, io

A = Path("/Users/sb/code/opensip-ai/opensip_arch")
P = A.parent / "opensip"
T = Path("/tmp/opensip-implementation")
M = A / "docs/implementation/m2"
U = M / "descriptor-acl-capture-inventory-v63"
R = T / "reviews/claude-opus5-acl-capture447-inventory63-r1"
S = T / "native-acl447/product"
D = M / "reviews" / R.name
E = M / "trials/descriptor-acl-capture-inventory-selection-63"
private = T / "inventory63-private"
args = argparse.ArgumentParser()
args.add_argument("--review-sha256", required=True)
args.add_argument("--root-assessment", type=Path, required=True)
a = args.parse_args()
root_assessment = a.root_assessment.read_text().strip()
assert len(root_assessment) > 100
assert D.is_dir() and {p.name for p in D.iterdir()} == {"REQUEST.md", "status.json"}
assert not E.exists() and not private.exists()

def dig(b):
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def pin(p):
    return dict(path=str(p.relative_to(A)), **dig(p.read_bytes()))

def save(p, v):
    p.write_text(json.dumps(v, indent=2) + "\n")

subject = M / "descriptor-acl-capture-inventory-v63-subject.json"
assert pin(subject)["sha256"] == "b0ba0f016c775740a6e933adb07702b43c91449bfe4d9a46bc5a7a76d7e32a36"
for row in json.loads(subject.read_text())["files"]:
    assert pin(A / row["path"]) == row
assert dig((R / "review.json").read_bytes())["sha256"] == a.review_sha256
review = json.loads((R / "review.json").read_text())
assert review["inventoryVerdict"] == "ACCEPT-UNIT"
assert review["sourceVerdict"] == "ACCEPT-UNIT"
assert review["requiredFindings"] == []
assert review["subjectManifestSha256"] == pin(subject)["sha256"]
record = json.loads((U / "successor.json").read_text())
parent = A / record["parent"]["path"]
candidate = A / record["candidate"]["path"]
old_inventory = json.loads(parent.read_text())
new_inventory = json.loads(candidate.read_text())
new_rows = {r["path"]: r for r in new_inventory["files"]}
assert len(old_inventory["files"]) == 710 and len(new_inventory["files"]) == 711
assert all(new_rows[r["path"]] == r for r in old_inventory["files"])
assert all(new_inventory[k] == old_inventory[k] for k in old_inventory if k not in ("files", "standing"))
peer = review["inventoryCandidateAssessment"]
assert peer["verdict"] == "ACCEPT" and peer["requiredFindings"] == []
assert {k: peer[k] for k in ("path", "bytes", "sha256")} == pin(candidate)
assert {k: peer["parent"][k] for k in ("path", "bytes", "sha256")} == pin(parent)
assert {k: peer["successorRecord"][k] for k in ("path", "bytes", "sha256")} == pin(U / "successor.json")
source_pins = {
    "crates/platform/src/filesystem/descriptor_acl_capture.rs": "7edfed520d4223d78b5f2546c684488082ffccc238984bf1d5ae970b3ddf8586",
    "crates/platform/src/filesystem.rs": "faad48d7e93fd25fc70cdf761e34bdbc1fa6fca3d3f04c5bc723c086bdfdae84",
    "crates/platform/src/lib.rs": "6418af156bc29fb68bee785c55705f5824b960e59e2b4384b9bddb25a186e5f3",
}
for rel, sha in source_pins.items():
    raw = (S / rel).read_bytes()
    assert dig(raw)["sha256"] == sha

base = None
own_files = {}
checked = 0
for line in (R / "hashes.txt").read_text().splitlines():
    if line.startswith("##"):
        if "R-relative" in line:
            base = R
        elif "S-relative" in line:
            base = S
        elif "P-relative" in line:
            base = P
        elif "A-relative" in line:
            base = A
        continue
    if not line or line.startswith("#"):
        continue
    sha, n, name = line.split(None, 2)
    q = PurePosixPath(name)
    assert not q.is_absolute() and ".." not in q.parts
    assert base is not None
    path = base / name
    assert path.is_file() and not path.is_symlink(), name
    raw = path.read_bytes()
    assert dig(raw) == {"bytes": int(n), "sha256": sha}, name
    checked += 1
    if base == R:
        own_files[name] = raw
assert checked == 194
assert "REVIEW.md" in own_files and "review.json" in own_files
assert len(own_files) < 1000 and sum(map(len, own_files.values())) < 50 * 1024 * 1024
assert a.review_sha256 in root_assessment and pin(subject)["sha256"] in root_assessment
assert subprocess.check_output(["git", "status", "--porcelain"], cwd=P) == b""
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=P).strip() == b"20d94ec9deb77e89688a556e424b2ff6281bffb2"
before = (P / "design-lock.json").read_bytes()
lock = json.loads(before)
assert len(lock["inventorySuccessors"]) == 37 and len(lock["contractSuccessors"]) == 65
assert lock["inventorySuccessors"][-1]["candidate"] == pin(parent)
effective = {}
for row in lock["inventoryPassageInheritance"]:
    assert row["parent"] == pin(parent)
    i = int(row["selector"]["jsonPointer"].split("/")[2])
    effective[old_inventory["files"][i]["path"]] = row
for binding in lock["contractSuccessors"]:
    for row in json.loads((A / binding["record"]["path"]).read_bytes())["passageOverrides"]:
        if row["parent"] == pin(parent):
            i = int(row["selector"]["jsonPointer"].split("/")[2])
            n = old_inventory["files"][i]["path"]
            assert n not in effective or effective[n] == row
            effective[n] = row
assert len(effective) == 5
expected = []
idx = {r["path"]: i for i, r in enumerate(new_inventory["files"])}
for n, row in sorted(effective.items()):
    i = int(row["selector"]["jsonPointer"].split("/")[2])
    old_row = old_inventory["files"][i]
    assert new_rows[n] == old_row and old_row["description"] == row["before"]
    expected.append({
        "filePath": n,
        "parentSelector": row["selector"],
        "candidateSelector": {"jsonPointer": f"/files/{idx[n]}/description"},
        "before": row["before"],
        "effectiveDescription": row["after"],
    })
assert record["descriptionOverrideProjection"] == expected and len(expected) == 5
baseline = []
for n in subprocess.check_output(["git", "ls-files", "-z"], cwd=P).decode().split("\0"):
    if n:
        baseline.append(dict(path=n, **dig((P / n).read_bytes())))
assert len(baseline) == 596
E.mkdir()
private.mkdir()
files = {**own_files, "hashes.txt": (R / "hashes.txt").read_bytes()}
for n, b in files.items():
    dest = D / n
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)
rows = [dict(path=n, **dig(b)) for n, b in sorted(files.items())]
with tarfile.open(D / "subject.tar.xz", "w:xz") as tf:
    for n, b in sorted(files.items()):
        h = tarfile.TarInfo(n)
        h.size = len(b)
        h.mode = 0o644
        h.mtime = 0
        tf.addfile(h, io.BytesIO(b))
save(D / "subject.json", dict(standing="Actual additive inventory63 and capture447 review only", files=rows))
save(D / "archive-pin.json", dict(path="subject.tar.xz", **dig((D / "subject.tar.xz").read_bytes()), members=len(rows)))
assent = M / "descriptor-acl-capture-inventory-v63-unit.json"
assert not assent.exists()
save(assent, dict(
    schemaVersion=1,
    unit="descriptor-acl-capture-inventory-v63",
    status="ACCEPTED-UNIT",
    subjectManifest=pin(subject),
    independentReview=pin(D / "review.json"),
    rootSubstantiveAssent=True,
    requiredUnitFindings=[],
    acceptedInventory=pin(candidate),
    sourceBoundary={
        "verdict": "ACCEPT-UNIT",
        "productBase": "20d94ec9deb77e89688a556e424b2ff6281bffb2",
        "paths": source_pins,
        "integratedByThisSelector": False,
    },
    rootAssessment=root_assessment,
    fullM2Complete=False,
    productQualification=False,
))
assert json.loads(assent.read_text())["rootAssessment"] == root_assessment and isinstance(root_assessment, str)
(D / "root-assessment.md").write_text(root_assessment + "\n")
save(D / "status.json", {
    "status": "ACCEPT-UNIT",
    "actualReviewer": "Claude Opus 5.5 via Herdr wF:p1",
    "rootSubstantiveAssent": True,
    "review": pin(D / "review.json"),
})
lock["inventorySuccessors"].append(dict(
    parent=pin(parent),
    candidate=pin(candidate),
    record=pin(U / "successor.json"),
    review=pin(D / "review.json"),
    assent=pin(assent),
))
projected = [{
    "parent": pin(candidate),
    "selector": row["candidateSelector"],
    "before": row["before"],
    "after": row["effectiveDescription"],
} for row in expected]
assert len(projected) == 5
lock["inventoryPassageInheritance"] = sorted(projected, key=lambda row: json.dumps(row["selector"], sort_keys=True))
after = (json.dumps(lock, indent=2) + "\n").encode()
(private / "design-lock.json").write_bytes(after)
checks = []

def check(name, path):
    cmd = [
        str(T / "source-audit364-env/bin/python"), "-I", "-B",
        str(P / "tools/verify_design.py"),
        "--architecture", str(A),
        "--implementation", str(P),
        "--lock", str(path),
    ]
    r = subprocess.run(cmd, capture_output=True)
    (E / (name + ".stdout")).write_bytes(r.stdout)
    (E / (name + ".stderr")).write_bytes(r.stderr)
    checks.append(dict(name=name, command=cmd, exitCode=r.returncode))
    save(E / "checks.json", checks)
    assert r.returncode == 0, r.stderr.decode()
    value = json.loads(r.stdout)
    assert value["passed"] and len(value["inventorySuccessors"]) == 38 and len(value["contractSuccessors"]) == 65 and len(value["inventoryPassageInheritance"]) == 5

check("private-design", private / "design-lock.json")
for row in baseline:
    assert dig((P / row["path"]).read_bytes()) == {k: row[k] for k in ("bytes", "sha256")}
(E / "before-design-lock.json").write_bytes(before)
(E / "after-design-lock.json").write_bytes(after)
save(E / "baseline.json", baseline)
(P / "design-lock.json").write_bytes(after)
check("live-design", P / "design-lock.json")
for row in baseline:
    if row["path"] != "design-lock.json":
        assert dig((P / row["path"]).read_bytes()) == {k: row[k] for k in ("bytes", "sha256")}
assert subprocess.check_output(["git", "diff", "--name-only"], cwd=P).decode().splitlines() == ["design-lock.json"]
save(E / "receipt.json", dict(
    inventorySuccessors=38,
    contractSuccessors=65,
    plannedFiles=711,
    packages=20,
    inheritedOverrides=5,
    unchangedNonLockProductFiles=595,
    lock=dig(after),
    checks=checks,
    hashRowsChecked=checked,
    scope="Additive layout only. Reviewed source bytes are accepted and not yet copied. No absence, custody, creator, or M2 acceptance.",
))
(E / "selection.py").write_bytes(Path(__file__).read_bytes())
print("PASS38/65,711planned,595nonlockunchanged", dig(after))
