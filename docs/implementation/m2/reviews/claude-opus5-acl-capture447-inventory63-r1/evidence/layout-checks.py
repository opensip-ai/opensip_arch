"""Read-only independent layout checks for proposed inventory63.

Reviewer-authored (actual Claude Opus 5). Reads the architecture repository,
the live product lock and the private447 tree; writes only its JSON report under
R/evidence. Every expected value is recomputed from the parent inventory and the
live lock, never copied from the successor record under review.
Run: python3 -I -B layout-checks.py
"""
import hashlib, json, pathlib, subprocess

A = pathlib.Path("/Users/sb/code/opensip-ai/opensip_arch")
P = pathlib.Path("/Users/sb/code/opensip-ai/opensip")
S = pathlib.Path("/tmp/opensip-implementation/native-acl447/product")
R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-acl-capture447-inventory63-r1")
M2 = "docs/implementation/m2"
V63DIR = f"{M2}/descriptor-acl-capture-inventory-v63"
V62DIR = f"{M2}/work-reader-inventory-v62"
ADDED = "crates/platform/src/filesystem/descriptor_acl_capture.rs"
PRODUCT_HEAD = "20d94ec9deb77e89688a556e424b2ff6281bffb2"

checks, facts = [], {}


def check(name, ok, detail=None):
    checks.append({"check": name, "pass": bool(ok), **({"detail": detail} if detail is not None else {})})


def raw(path):
    return (A / path).read_bytes()


def pin(path, base=A):
    b = (base / path).read_bytes()
    return {"path": path, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def load(path):
    return json.loads(raw(path))


# A. Subject manifest -------------------------------------------------------
subject_path = f"{M2}/descriptor-acl-capture-inventory-v63-subject.json"
subject = load(subject_path)
facts["subjectManifest"] = pin(subject_path)
members = subject["files"]
paths = [m["path"] for m in members]
check("A1 subject schemaVersion 1 and exactly 8 members", subject["schemaVersion"] == 1 and len(members) == 8)
check("A2 subject members sorted and unique", paths == sorted(paths) and len(set(paths)) == len(paths))
check("A3 every member pin matches live bytes and SHA-256", all(pin(m["path"]) == m for m in members))
dir_listing = sorted(f"{V63DIR}/{p.name}" for p in (A / V63DIR).iterdir())
check("A4 members are exactly the unit directory plus candidate inventory",
      sorted(paths) == sorted(dir_listing + [f"{M2}/repository-file-inventory.v63.json"]),
      {"unitDirectory": dir_listing})
v62_subject = load(f"{M2}/work-reader-inventory-v62-subject.json")
shape = lambda ps: sorted(pathlib.PurePosixPath(p).name if "/work-reader-inventory-v62/" in p or "/descriptor-acl-capture-inventory-v63/" in p else "INVENTORY" for p in ps)
check("A5 member shape equals accepted inventory62 subject shape",
      shape(paths) == shape([m["path"] for m in v62_subject["files"]]))
check("A6 subject contains no Rust source", not any(p.endswith(".rs") for p in paths))

# B. Successor record -------------------------------------------------------
record = load(f"{V63DIR}/successor.json")
record62 = load(f"{V62DIR}/successor.json")
lock_bytes = (P / "design-lock.json").read_bytes()
lock = json.loads(lock_bytes)
facts["lockSha256"] = hashlib.sha256(lock_bytes).hexdigest()
facts["lockInventorySuccessors"] = len(lock["inventorySuccessors"])
facts["lockContractSuccessors"] = len(lock["contractSuccessors"])
selected = lock["inventorySuccessors"][-1]["candidate"]
check("B1 record key set and order equal accepted v62 record", list(record) == list(record62))
check("B2 record standing is PROPOSED and requires review and root assent",
      record["standing"].startswith("PROPOSED") and "review" in record["standing"] and "root assent" in record["standing"],
      record["standing"])
check("B3 parent pin equals live lock's selected inventory62", record["parent"] == selected, selected)
check("B4 parent pin matches live parent bytes", pin(record["parent"]["path"]) == record["parent"])
cand_pin = next(m for m in members if m["path"].endswith("repository-file-inventory.v63.json"))
check("B5 candidate pin equals subject pin and live bytes",
      record["candidate"] == cand_pin == pin(record["candidate"]["path"]))
check("B6 addedFiles is exactly the one capture module", record["addedFiles"] == [ADDED])
check("B7 carried obligations equal accepted v62 record by value",
      record["carriedUnresolvedObligations"] == record62["carriedUnresolvedObligations"])
check("B8 projectionRule text equal to accepted v62 record", record["projectionRule"] == record62["projectionRule"])
check("B9 candidate is not already in lock", all(s["candidate"]["path"] != record["candidate"]["path"] for s in lock["inventorySuccessors"]))

# C. Candidate inventory versus parent -------------------------------------
parent = load(record["parent"]["path"])
cand = load(record["candidate"]["path"])
check("C1 top-level keys identical in order", list(cand) == list(parent), list(cand))
check("C2 schemaVersion, packages, pendingDecisions equal by value",
      all(cand[k] == parent[k] for k in ("schemaVersion", "packages", "pendingDecisions")))
facts["standing"] = {"parent": parent["standing"], "candidate": cand["standing"]}
check("C3 candidate standing disclaims absence/profile/custody/authority",
      all(w in cand["standing"] for w in ("absence", "profile", "custody", "authority")), cand["standing"])
cp = [r["path"] for r in cand["files"]]
check("C4 711 unique candidate rows sorted by path (parent 710)",
      len(cand["files"]) == 711 and len(parent["files"]) == 710 and cp == sorted(cp) and len(set(cp)) == 711)
idx = cp.index(ADDED)
facts["addedIndex"] = idx
without = cand["files"][:idx] + cand["files"][idx + 1:]
check("C5 removing the added row yields parent files exactly (all 710 rows equal by value and order)", without == parent["files"])
check("C6 parent has no row for the added path; no earlier live product file", ADDED not in [r["path"] for r in parent["files"]] and not (P / ADDED).exists())
row = cand["files"][idx]
sib = [r for r in cand["files"] if r["path"].startswith("crates/platform/src/filesystem/") and r["path"] != ADDED]
check("C7 added row keys, package, role, generated, standing match filesystem siblings",
      all(list(row) == list(s) for s in sib) and all(row[k] == sib[0][k] for k in ("package", "role", "generated", "standing"))
      and all(s["package"] == "opensip-platform" and s["role"] == "adapter" for s in sib),
      {"package": row["package"], "role": row["role"], "siblings": [s["path"] for s in sib]})
pkg = {p["id"]: p for p in cand["packages"]}
check("C8 20 packages, owning package exists at crates/platform, 9 pending decisions",
      len(cand["packages"]) == 20 and pkg["opensip-platform"]["path"] == "crates/platform" and len(cand["pendingDecisions"]) == 9,
      {"platformPurpose": pkg["opensip-platform"]["purpose"], "platformDependencies": pkg["opensip-platform"]["dependencies"]})
check("C9 added path neighbours are filesystem.rs and descriptor_filesystem.rs",
      cp[idx - 1] == "crates/platform/src/filesystem.rs" and cp[idx + 1] == "crates/platform/src/filesystem/descriptor_filesystem.rs")
check("C10 planned file exists in private447 tree and not in product HEAD",
      (S / ADDED).is_file() and subprocess.run(["git", "-C", str(P), "cat-file", "-e", f"{PRODUCT_HEAD}:{ADDED}"],
                                                 capture_output=True).returncode != 0)
check("C11 file name is ordinary snake_case.rs under the existing filesystem module directory",
      pathlib.PurePosixPath(ADDED).name == "descriptor_acl_capture.rs"
      and all(c.islower() or c == "_" for c in "descriptor_acl_capture"))
facts["addedRow"] = row

# D. Projection, recomputed from the live lock ------------------------------
overrides = {}
for o in lock["inventoryPassageInheritance"]:
    assert o["parent"] == record["parent"]
    overrides[parent["files"][int(o["selector"]["jsonPointer"].split("/")[2])]["path"]] = o
direct = 0
for binding in lock["contractSuccessors"]:
    b = (A / binding["record"]["path"]).read_bytes()
    assert hashlib.sha256(b).hexdigest() == binding["record"]["sha256"]
    for o in json.loads(b).get("passageOverrides", []):
        if o["parent"] == record["parent"]:
            direct += 1
            overrides[parent["files"][int(o["selector"]["jsonPointer"].split("/")[2])]["path"]] = o
facts["inheritedOverridesInLock"] = len(lock["inventoryPassageInheritance"])
facts["directContractOverridesOnV62"] = direct
mine, moves = [], {}
for path, o in sorted(overrides.items()):
    pi = int(o["selector"]["jsonPointer"].split("/")[2])
    ci = cp.index(path)
    assert parent["files"][pi]["description"] == o["before"] == cand["files"][ci]["description"]
    moves[path] = f"{pi} -> {ci}"
    mine.append({"filePath": path, "parentSelector": o["selector"],
                 "candidateSelector": {"jsonPointer": f"/files/{ci}/description"},
                 "before": o["before"], "effectiveDescription": o["after"]})
facts["indexMoves"] = moves
check("D1 exactly five effective overrides", len(mine) == 5)
check("D2 record projection equals independent recomputation", record["descriptionOverrideProjection"] == mine)
check("D3 expected index moves", moves == {
    "apps/cli/src/bootstrap.rs": "7 -> 7", "apps/report/package.json": "13 -> 13",
    "crates/host/src/installation_lineage.rs": "104 -> 104", "package.json": "507 -> 508",
    "schemas/sources/imported-v1.schema.json": "574 -> 575"})
check("D4 moves follow the insertion index",
      all((int(v.split()[0]) < idx) == (v.split()[0] == v.split()[2]) for v in moves.values()))
check("D5 candidate keeps base descriptions; overrides stay projected", all(
    cand["files"][int(r["candidateSelector"]["jsonPointer"].split("/")[2])]["description"] == r["before"] != r["effectiveDescription"] for r in mine))

# E. Helper and verifier anchor ---------------------------------------------
helpers = {d: pin(f"{d}/verify_projection.py")["sha256"] for d in
           (V63DIR, V62DIR, f"{M2}/shared-work-ledger-inventory-v61")}
check("E1 helper byte-identical to inventory61 and inventory62 helpers", len(set(helpers.values())) == 1, helpers)
run = subprocess.run(["python3", "-I", "-B", str(A / V63DIR / "verify_projection.py"), "--architecture", str(A),
                      "--lock", str(P / "design-lock.json")], capture_output=True)
facts["helperReplay"] = {"exitCode": run.returncode, "stdout": run.stdout.decode(), "stderr": run.stderr.decode()}
check("E2 helper replay exit 0 and stdout byte-equal to recorded stdout",
      run.returncode == 0 and run.stdout == raw(f"{V63DIR}/verification.stdout") and run.stderr == b"")
vj = load(f"{V63DIR}/verification.json")
check("E3 recorded run used -I -B, the live lock, exit 0", vj["command"][:3] == ["python3", "-I", "-B"] and vj["exitCode"] == 0
      and vj["command"][-1] == str(P / "design-lock.json"))
anchor = load(f"{V63DIR}/verifier-anchor.json")
head = subprocess.run(["git", "-C", str(P), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
clean = subprocess.run(["git", "-C", str(P), "status", "--porcelain"], capture_output=True, text=True).stdout == ""
check("E4 verifier anchor head equals clean live product head", anchor["head"] == head == PRODUCT_HEAD and clean)
check("E5 anchored verifier and lock byte-identical live", all(pin(f["path"], P) == f for f in anchor["files"]))
check("E6 anchor scope disclaims selection", "does not select inventory63" in anchor["scope"])

# G. Five-pin lock successor shape -------------------------------------------
FIVE = ["parent", "candidate", "record", "review", "assent"]
succ = lock["inventorySuccessors"]
check("G1 every live lock inventory successor has exactly the five pins parent/candidate/record/review/assent",
      all(sorted(s) == sorted(FIVE) and all(set(s[k]) == {"path", "bytes", "sha256"} for k in FIVE) for s in succ),
      {"entries": len(succ)})
check("G2 live successor chain is continuous (each parent equals previous candidate)",
      all(succ[i]["parent"] == succ[i - 1]["candidate"] for i in range(1, len(succ))))
last = succ[-1]
check("G3 selected v62 entry's record/review/assent pins match live bytes",
      all(pin(last[k]["path"]) == last[k] for k in ("record", "review", "assent")))
future = {"parent": record["parent"], "candidate": record["candidate"], "record": pin(f"{V63DIR}/successor.json")}
review_rel = f"{M2}/reviews/claude-opus5-acl-capture447-inventory63-r1/review.json"
facts["fivePinShapeForV63"] = {**future, "review": {"path": review_rel, "state": "PENDING - this review, archived by root"},
                               "assent": {"state": "PENDING - root unit record not yet written"}}
check("G4 v63 supplies parent, candidate and record pins now; parent equals the selected v62 candidate",
      future["parent"] == last["candidate"] and future["candidate"] == cand_pin
      and future["record"] in members and not (A / review_rel).exists())

# F. README claims ------------------------------------------------------------
readme = raw(f"{V63DIR}/README.md").decode()
check("F1 README counts match (711 files, 20 packages, 9 pending decisions)",
      "711 planned files" in readme and "20 packages" in readme and "9 pending decisions" in readme)
check("F2 README disclaims source approval, absence, observe_descriptor replacement and completion",
      all(s in readme for s in ("not source approval", "not absence", "does not replace observe_descriptor", "No M2")))

report = {"reviewerAuthored": True, "readOnly": True, "checks": checks,
          "passed": sum(c["pass"] for c in checks), "total": len(checks), "facts": facts}
(R / "evidence/layout-checks.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({"passed": report["passed"], "total": report["total"],
                  "failed": [c["check"] for c in checks if not c["pass"]]}))
