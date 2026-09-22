"""Read-only independent layout checks for proposed inventory64.

Reviewer-authored (actual Claude Opus 5.5). Adapted from my inventory63 checker.
Reads the architecture repository and the live product tree; writes only its JSON
report under R/evidence. Every expected value is recomputed from the parent
inventory and the live lock, never copied from the successor record under review.
Run: python3 -I -B layout-checks.py
"""
import hashlib, json, pathlib, subprocess

A = pathlib.Path("/Users/sb/code/opensip-ai/opensip_arch")
P = pathlib.Path("/Users/sb/code/opensip-ai/opensip")
R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-private-access448-inventory64-r1")
M2 = "docs/implementation/m2"
UNIT = f"{M2}/private-access-inventory-v64"
PARENT_UNIT = f"{M2}/descriptor-acl-capture-inventory-v63"
ADDED = "crates/security/src/private_access.rs"
PRODUCT_HEAD = "f8019ecb80c87bd6e0ba2e967ab293fd97b2eeb3"
SUBJECT_SHA = "c5ceb0f93efeb3216c177b7fc9d0510864df1d4d01d36fb91a08103c8b162306"

checks, facts = [], {}


def check(name, ok, detail=None):
    checks.append({"check": name, "pass": bool(ok), **({"detail": detail} if detail is not None else {})})


def raw(path, base=A):
    return (base / path).read_bytes()


def pin(path, base=A):
    b = raw(path, base)
    return {"path": path, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def load(path, base=A):
    return json.loads(raw(path, base))


def git(*args):
    return subprocess.run(["git", "-C", str(P), *args], capture_output=True, text=True)


# A. Subject manifest -------------------------------------------------------
subject_path = f"{M2}/private-access-inventory-v64-subject.json"
subject = load(subject_path)
facts["subjectManifest"] = pin(subject_path)
members = subject["files"]
paths = [m["path"] for m in members]
check("A0 subject manifest SHA-256 equals the request pin", facts["subjectManifest"]["sha256"] == SUBJECT_SHA)
check("A1 subject schemaVersion 1 and exactly 8 members", subject["schemaVersion"] == 1 and len(members) == 8)
check("A2 subject members sorted and unique", paths == sorted(paths) and len(set(paths)) == len(paths))
check("A3 every member pin matches live bytes and SHA-256", all(pin(m["path"]) == m for m in members))
dir_listing = sorted(f"{UNIT}/{p.name}" for p in (A / UNIT).iterdir())
check("A4 members are exactly the unit directory plus candidate inventory",
      sorted(paths) == sorted(dir_listing + [f"{M2}/repository-file-inventory.v64.json"]), {"unitDirectory": dir_listing})
parent_subject = load(f"{M2}/descriptor-acl-capture-inventory-v63-subject.json")
shape = lambda ps: sorted(pathlib.PurePosixPath(p).name if "-inventory-v6" in p and "/repository-file-inventory" not in p else "INVENTORY" for p in ps)
check("A5 member shape equals accepted inventory63 subject shape", shape(paths) == shape([m["path"] for m in parent_subject["files"]]))
check("A6 subject contains no Rust source", not any(p.endswith(".rs") for p in paths))

# B. Successor record -------------------------------------------------------
record = load(f"{UNIT}/successor.json")
record63 = load(f"{PARENT_UNIT}/successor.json")
lock_bytes = raw("design-lock.json", P)
lock = json.loads(lock_bytes)
facts["lockSha256"] = hashlib.sha256(lock_bytes).hexdigest()
facts["lockInventorySuccessors"] = len(lock["inventorySuccessors"])
facts["lockContractSuccessors"] = len(lock["contractSuccessors"])
selected = lock["inventorySuccessors"][-1]["candidate"]
check("B1 record key set and order equal accepted v63 record", list(record) == list(record63))
check("B2 record standing is PROPOSED and requires review and root assent",
      record["standing"].startswith("PROPOSED") and "review" in record["standing"] and "root assent" in record["standing"], record["standing"])
check("B3 parent pin equals live lock's selected inventory63", record["parent"] == selected, selected)
check("B4 parent pin matches live parent bytes", pin(record["parent"]["path"]) == record["parent"])
cand_pin = next(m for m in members if m["path"].endswith("repository-file-inventory.v64.json"))
check("B5 candidate pin equals subject pin and live bytes", record["candidate"] == cand_pin == pin(record["candidate"]["path"]))
check("B6 addedFiles is exactly the one predicate module", record["addedFiles"] == [ADDED])
check("B7 carried obligations equal accepted v63 record by value",
      record["carriedUnresolvedObligations"] == record63["carriedUnresolvedObligations"])
check("B8 projectionRule text equal to accepted v63 record", record["projectionRule"] == record63["projectionRule"])
check("B9 all four preservation booleans are true",
      all(record[k] is True for k in ("parentArtifactBytesUnchanged", "inheritedRowsEqualByValue",
                                      "packageDependencyGraphUnchanged", "pendingDecisionsInheritedUnchanged")))
check("B10 candidate is not already in lock", all(s["candidate"]["path"] != record["candidate"]["path"] for s in lock["inventorySuccessors"]))

# C. Candidate inventory versus parent -------------------------------------
parent = load(record["parent"]["path"])
cand = load(record["candidate"]["path"])
check("C1 top-level keys identical in order", list(cand) == list(parent), list(cand))
check("C2 schemaVersion, packages, pendingDecisions equal by value",
      all(cand[k] == parent[k] for k in ("schemaVersion", "packages", "pendingDecisions")))
facts["standing"] = {"parent": parent["standing"], "candidate": cand["standing"]}
check("C3 candidate standing disclaims absence/profile/custody/creator",
      all(w in cand["standing"] for w in ("absence", "profile", "custody", "creator")), cand["standing"])
cp = [r["path"] for r in cand["files"]]
check("C4 712 unique candidate rows sorted by path (parent 711)",
      len(cand["files"]) == 712 and len(parent["files"]) == 711 and cp == sorted(cp) and len(set(cp)) == 712)
idx = cp.index(ADDED)
facts["addedIndex"] = idx
check("C5 added row is at the requested index 248", idx == 248)
without = cand["files"][:idx] + cand["files"][idx + 1:]
check("C6 removing the added row yields parent files exactly (all 711 rows equal by value and order)", without == parent["files"])
row = cand["files"][idx]
sib = [r for r in cand["files"] if r["path"].startswith("crates/security/src/") and r["path"] != ADDED]
roles = sorted({s["role"] for s in sib})
check("C7 added row keys, package, generated, standing match security siblings; role in existing security vocabulary",
      all(list(row) == list(s) for s in sib) and all(s["package"] == row["package"] == "opensip-security" for s in sib)
      and row["generated"] is False and row["standing"] == "proposed" and row["role"] in roles,
      {"role": row["role"], "securityRoles": roles, "validatorSiblings": [s["path"] for s in sib if s["role"] == "validator"][:6]})
pkg = {p["id"]: p for p in cand["packages"]}
check("C8 20 packages; opensip-security at crates/security already depends on opensip-platform; 9 pending decisions",
      len(cand["packages"]) == 20 and pkg["opensip-security"]["path"] == "crates/security"
      and "opensip-platform" in pkg["opensip-security"]["dependencies"] and len(cand["pendingDecisions"]) == 9,
      {"securityPurpose": pkg["opensip-security"]["purpose"], "securityDependencies": pkg["opensip-security"]["dependencies"],
       "platformPurpose": pkg["opensip-platform"]["purpose"]})
check("C9 neighbours are metadata_versions.rs and revocation.rs",
      cp[idx - 1] == "crates/security/src/metadata_versions.rs" and cp[idx + 1] == "crates/security/src/revocation.rs")
in_head = git("cat-file", "-e", f"{PRODUCT_HEAD}:{ADDED}").returncode == 0
check("C10 planned file exists untracked in the live product tree and not in HEAD or the parent inventory",
      (P / ADDED).is_file() and not in_head and ADDED not in [r["path"] for r in parent["files"]])
check("C11 file name is ordinary snake_case.rs", all(c.islower() or c == "_" for c in "private_access"))
facts["addedRow"] = row

# D. Projection, recomputed from the live lock ------------------------------
overrides = {}
for o in lock["inventoryPassageInheritance"]:
    assert o["parent"] == record["parent"]
    overrides[parent["files"][int(o["selector"]["jsonPointer"].split("/")[2])]["path"]] = o
direct = 0
for binding in lock["contractSuccessors"]:
    b = raw(binding["record"]["path"])
    assert hashlib.sha256(b).hexdigest() == binding["record"]["sha256"]
    for o in json.loads(b).get("passageOverrides", []):
        if o["parent"] == record["parent"]:
            direct += 1
            overrides[parent["files"][int(o["selector"]["jsonPointer"].split("/")[2])]["path"]] = o
facts["inheritedOverridesInLock"] = len(lock["inventoryPassageInheritance"])
facts["directContractOverridesOnV63"] = direct
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
    "crates/host/src/installation_lineage.rs": "104 -> 104", "package.json": "508 -> 509",
    "schemas/sources/imported-v1.schema.json": "575 -> 576"})
check("D4 moves follow the insertion index",
      all((int(v.split()[0]) < idx) == (v.split()[0] == v.split()[2]) for v in moves.values()))
check("D5 candidate keeps base descriptions; overrides stay projected", all(
    cand["files"][int(r["candidateSelector"]["jsonPointer"].split("/")[2])]["description"] == r["before"] != r["effectiveDescription"] for r in mine))

# E. Helper and verifier anchor ---------------------------------------------
helpers = {d: pin(f"{d}/verify_projection.py")["sha256"] for d in
           (UNIT, PARENT_UNIT, f"{M2}/work-reader-inventory-v62", f"{M2}/shared-work-ledger-inventory-v61")}
check("E1 helper byte-identical to inventory61/62/63 helpers", len(set(helpers.values())) == 1, helpers)
run = subprocess.run(["python3", "-I", "-B", str(A / UNIT / "verify_projection.py"), "--architecture", str(A),
                      "--lock", str(P / "design-lock.json")], capture_output=True)
facts["helperReplay"] = {"exitCode": run.returncode, "stdout": run.stdout.decode(), "stderr": run.stderr.decode()}
check("E2 helper replay exit 0 and stdout byte-equal to recorded stdout",
      run.returncode == 0 and run.stdout == raw(f"{UNIT}/verification.stdout") and run.stderr == b"")
vj = load(f"{UNIT}/verification.json")
check("E3 recorded run used -I -B, the live lock, exit 0",
      vj["command"][:3] == ["python3", "-I", "-B"] and vj["exitCode"] == 0 and vj["command"][-1] == str(P / "design-lock.json"))
anchor = load(f"{UNIT}/verifier-anchor.json")
head = git("rev-parse", "HEAD").stdout.strip()
dirty = sorted(git("status", "--porcelain").stdout.splitlines())
facts["productDirtyEntries"] = dirty
check("E4 anchor head equals live product head; the only dirty entries are the two source paths",
      anchor["head"] == head == PRODUCT_HEAD and dirty == sorted([" M crates/security/src/lib.rs", "?? " + ADDED]))
check("E5 anchored verifier and lock byte-identical live and unmodified in the working tree",
      all(pin(f["path"], P) == f for f in anchor["files"]) and not any("design-lock" in d or "verify_design" in d for d in dirty))
check("E6 anchor scope excludes the uncommitted source", "outside this anchor" in anchor["scope"])

# G. Five-pin lock successor shape -------------------------------------------
FIVE = ["parent", "candidate", "record", "review", "assent"]
succ = lock["inventorySuccessors"]
check("G1 every live lock inventory successor has exactly the five pins",
      all(sorted(s) == sorted(FIVE) and all(set(s[k]) == {"path", "bytes", "sha256"} for k in FIVE) for s in succ), {"entries": len(succ)})
check("G2 live successor chain is continuous", all(succ[i]["parent"] == succ[i - 1]["candidate"] for i in range(1, len(succ))))
last = succ[-1]
check("G3 selected v63 entry's record/review/assent pins match live bytes",
      all(pin(last[k]["path"]) == last[k] for k in ("record", "review", "assent")),
      {"review": last["review"]})
review_rel = f"{M2}/reviews/claude-opus5-private-access448-inventory64-r1/review.json"
future = {"parent": record["parent"], "candidate": record["candidate"], "record": pin(f"{UNIT}/successor.json")}
facts["fivePinShapeForV64"] = {**future, "review": {"path": review_rel, "state": "PENDING - this review, archived by root"},
                               "assent": {"state": "PENDING - root unit record not yet written"}}
check("G4 v64 supplies parent, candidate and record pins now; parent equals the selected v63 candidate",
      future["parent"] == last["candidate"] and future["candidate"] == cand_pin and future["record"] in members
      and not (A / review_rel).exists())

# F. README claims ------------------------------------------------------------
readme = raw(f"{UNIT}/README.md").decode()
check("F1 README counts match (711 retained, 712 files, 20 packages, 9 pending decisions)",
      all(s in readme for s in ("711 existing rows", "712 planned files", "20 packages", "9 pending decisions")))
check("F2 README disclaims source approval, absence authority, creator completion and replacement",
      all(s in readme for s in ("not source approval", "absence authority", "creator completion", "does not replace directory_policy")))

report = {"reviewerAuthored": True, "readOnly": True, "checks": checks,
          "passed": sum(c["pass"] for c in checks), "total": len(checks), "facts": facts}
(R / "evidence/layout-checks.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({"passed": report["passed"], "total": report["total"],
                  "failed": [c["check"] for c in checks if not c["pass"]]}))
