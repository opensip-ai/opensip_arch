#!/usr/bin/env python3
"""Independent custody verification for typescript-boundary04. Writes only under review/."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

PY = sys.executable
REVIEW = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-review-04/review")
SUBJECT = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-04")
OUTER = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-04.manifest.json")
ADJACENT = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-review-04/subject-manifest.json")
DECLARED = "4e1598dc24fa39900b60a1d9a61b11e90f53832813c8697bf03a25a60a33740b"
NODE = Path("/Users/sb/.nvm/versions/node/v24.16.0/bin/node")
NODE_SHA = "1ee75375e33b94fc34b3b19aede049e11dae90efb63b374dc96d6bdace70c4b8"
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"

LAUNCHER = {
    "launch-public.py",
    "process.json",
    "prompt.md",
    "public-events.jsonl",
    "result.json",
    "response.json",
    "final-response.md",
    "process-completion.json",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mode_octal(st: os.stat_result) -> str:
    return format(st.st_mode & 0o7777, "o")


def entry_kind(st: os.stat_result) -> str:
    if stat.S_ISLNK(st.st_mode):
        return "symlink"
    if stat.S_ISDIR(st.st_mode):
        return "directory"
    if stat.S_ISREG(st.st_mode):
        return "file"
    return "other"


def walk_tree(root: Path) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        dirnames.sort()
        filenames.sort()
        for name in dirnames + filenames:
            rel = name if not rel_dir else f"{rel_dir}/{name}"
            abs_path = root / rel
            st = abs_path.lstat()
            kind = entry_kind(st)
            rec: dict = {"path": rel, "type": kind, "mode": mode_octal(st)}
            if kind == "symlink":
                rec["target"] = os.readlink(abs_path)
            elif kind == "file":
                rec["bytes"] = st.st_size
                rec["sha256"] = sha256_file(abs_path)
            found[rel] = rec
    return found


def compare(listed: list[dict], found: dict[str, dict]) -> dict:
    problems: list[str] = []
    by_path = {row["path"]: row for row in listed}
    if len(by_path) != len(listed):
        problems.append("duplicate paths in manifest")
    extra = sorted(set(found) - set(by_path))
    missing = sorted(set(by_path) - set(found))
    mismatches: list[dict] = []
    symlink_ok = 0
    for path, row in by_path.items():
        now = found.get(path)
        if now is None:
            continue
        expect_type = row["type"]
        if now["type"] != expect_type:
            mismatches.append({"path": path, "field": "type", "expected": expect_type, "actual": now["type"]})
            continue
        if now["mode"] != row["mode"]:
            mismatches.append({"path": path, "field": "mode", "expected": row["mode"], "actual": now["mode"]})
        if expect_type == "file":
            if now["bytes"] != row.get("bytes"):
                mismatches.append({"path": path, "field": "bytes", "expected": row.get("bytes"), "actual": now["bytes"]})
            if now["sha256"] != row.get("sha256"):
                mismatches.append({"path": path, "field": "sha256", "expected": row.get("sha256"), "actual": now["sha256"]})
        elif expect_type == "symlink":
            if now.get("target") != row.get("target"):
                mismatches.append({"path": path, "field": "target", "expected": row.get("target"), "actual": now.get("target")})
            else:
                symlink_ok += 1
    return {
        "listed": len(listed),
        "found": len(found),
        "extra": extra,
        "missing": missing,
        "mismatches": mismatches[:50],
        "mismatchCount": len(mismatches),
        "symlinksListed": sum(1 for r in listed if r["type"] == "symlink"),
        "symlinksMatched": symlink_ok,
        "exactFileSet": not extra and not missing and not mismatches,
    }


def pin_file(architecture: Path, pin: dict, label: str) -> dict:
    rel = pin["path"]
    current = architecture
    symlink_in_path = False
    for part in rel.split("/"):
        current = current / part
        if current.is_symlink():
            symlink_in_path = True
            break
    raw = (architecture / rel).read_bytes() if (architecture / rel).is_file() and not symlink_in_path else b""
    digest = sha256_bytes(raw) if raw else None
    return {
        "label": label,
        "path": rel,
        "declaredBytes": pin["bytes"],
        "declaredSha256": pin["sha256"],
        "present": (architecture / rel).exists(),
        "symlinkInPath": symlink_in_path,
        "actualBytes": len(raw) if digest else None,
        "actualSha256": digest,
        "ok": digest == pin["sha256"] and len(raw) == pin["bytes"] and not symlink_in_path,
    }


def freeze_aggregate(subject: Path, freeze: dict) -> dict:
    rows = []
    for dirpath, dirnames, filenames in os.walk(subject, followlinks=False):
        rel_dir = os.path.relpath(dirpath, subject)
        if rel_dir == ".":
            rel_dir = ""
        names = sorted(dirnames + filenames)
        dirnames.sort()
        for name in names:
            if not rel_dir and (name in {"work"} or name in LAUNCHER or name == "freeze-manifest.json"):
                continue
            rel = name if not rel_dir else f"{rel_dir}/{name}"
            if rel == "work" or rel.startswith("work/"):
                continue
            abs_path = subject / rel
            st = abs_path.lstat()
            kind = entry_kind(st)
            mode = mode_octal(st)
            if kind == "symlink":
                rows.append(("symlink", rel, mode, "", os.readlink(abs_path)))
            elif kind == "directory":
                rows.append(("directory", rel, mode, "", ""))
            elif kind == "file":
                digest = sha256_file(abs_path)
                rows.append(("file", rel, mode, str(st.st_size), digest))
            else:
                rows.append(("other", rel, mode, "", ""))
    rows.sort(key=lambda r: r[1])
    # freeze-manifest.mjs walks readdir order (sorted names) recursively, not a global sort.
    # Re-walk in the same order as the JS walker.
    return recompute_freeze_walk(subject, freeze)


def recompute_freeze_walk(subject: Path, freeze: dict) -> dict:
    def walk(relative: str = "") -> list[tuple]:
        names = sorted(os.listdir(subject / relative if relative else subject))
        out = []
        for name in names:
            rel = name if not relative else f"{relative}/{name}"
            if not relative and (name in {"work"} or name in LAUNCHER or name == "freeze-manifest.json"):
                continue
            abs_path = subject / rel
            st = abs_path.lstat()
            kind = entry_kind(st)
            mode = mode_octal(st)
            if kind == "symlink":
                out.append((kind, rel, mode, "", os.readlink(abs_path)))
            elif kind == "directory":
                out.append((kind, rel, mode, "", ""))
                out.extend(walk(rel))
            elif kind == "file":
                out.append((kind, rel, mode, str(st.st_size), sha256_file(abs_path)))
            else:
                out.append((kind, rel, mode, "", ""))
        return out

    rows = walk()
    blob = "\n".join(f"{t}\0{p}\0{m}\0{b}\0{s}" for t, p, m, b, s in rows).encode()
    digest = sha256_bytes(blob)
    return {
        "recomputedEntries": len(rows),
        "recomputedAggregateSha256": digest,
        "declaredAggregateSha256": freeze.get("aggregateSha256"),
        "ok": digest == freeze.get("aggregateSha256"),
    }


def archive_pins(subject: Path, freeze: dict) -> list[dict]:
    rows = []
    for name, closure in freeze["toolClosures"].items():
        for pkg in closure.get("packages", []):
            archive = pkg.get("archive")
            if not isinstance(archive, dict):
                continue
            rel = archive.get("archive")
            if not rel:
                continue
            path = subject / rel
            present = path.is_file()
            sha512 = None
            if present:
                digest = hashlib.sha512(path.read_bytes()).digest()
                import base64

                sha512 = "sha512-" + base64.b64encode(digest).decode("ascii")
            rows.append({
                "closure": name,
                "package": pkg["package"],
                "archive": rel,
                "present": present,
                "declaredSha512": archive.get("sha512"),
                "actualSha512": sha512,
                "matchesDeclared": sha512 == archive.get("sha512"),
                "matchesLock": archive.get("matchesLock"),
            })
    return rows


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    outer_raw = OUTER.read_bytes()
    adj_raw = ADJACENT.read_bytes()
    outer_sha = sha256_bytes(outer_raw)
    adj_sha = sha256_bytes(adj_raw)
    manifest = json.loads(outer_raw)
    freeze = json.loads((SUBJECT / "freeze-manifest.json").read_text())
    found = walk_tree(SUBJECT)
    comparison = compare(manifest["files"], found)

    node_present = NODE.is_file()
    node_sha = sha256_file(NODE) if node_present else None
    node_version = subprocess.check_output([str(NODE), "-p", "process.version"], text=True).strip() if node_present else None

    architecture = SUBJECT / "inputs" / "architecture"
    lock = json.loads((SUBJECT / "inputs" / "product" / "design-lock.json").read_text())
    binding = lock["inventorySuccessors"][-1]
    inventory_pins = [pin_file(architecture, binding[k], k) for k in ("parent", "candidate", "record", "review", "assent")]

    freeze_agg = recompute_freeze_walk(SUBJECT, freeze)
    archives = archive_pins(SUBJECT, freeze)

    groups = Counter(row.get("group") for row in manifest["files"])
    result = {
        "schemaVersion": 1,
        "standing": "independent Grok custody; not product selection",
        "outerManifest": str(OUTER),
        "outerSha256": outer_sha,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": outer_sha == DECLARED,
        "adjacentSha256": adj_sha,
        "adjacentMatchesOuter": adj_sha == outer_sha,
        "entriesDeclared": len(manifest["files"]),
        "groups": dict(groups),
        "tree": comparison,
        "node": {
            "path": str(NODE),
            "present": node_present,
            "version": node_version,
            "sha256": node_sha,
            "declaredSha256": NODE_SHA,
            "freezeSha256": freeze["pinnedRuntime"]["sha256"],
            "ok": node_sha == NODE_SHA == freeze["pinnedRuntime"]["sha256"] and node_version == "v24.16.0",
        },
        "inventoryPins": inventory_pins,
        "inventoryPinsOk": all(p["ok"] for p in inventory_pins),
        "freezeAggregate": freeze_agg,
        "archives": archives,
        "archivesOk": all(a["matchesDeclared"] for a in archives),
        "fixtureInventoryStanding": json.loads((architecture / "fixture-boundary-inventory.v1.json").read_text())["standing"],
        "ok": (
            outer_sha == DECLARED
            and adj_sha == outer_sha
            and comparison["exactFileSet"]
            and node_sha == NODE_SHA
            and all(p["ok"] for p in inventory_pins)
            and freeze_agg["ok"]
            and all(a["matchesDeclared"] for a in archives)
        ),
    }
    (RESULTS / "custody-before.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("outerSha256", "outerMatchesDeclared", "adjacentMatchesOuter", "entriesDeclared", "ok", "inventoryPinsOk", "archivesOk") }, indent=2))
    print("tree", json.dumps({k: comparison[k] for k in ("listed", "found", "exactFileSet", "mismatchCount", "symlinksListed", "symlinksMatched")}))
    print("node", result["node"]["ok"], result["node"]["version"], result["node"]["sha256"])
    print("freezeAggregate", freeze_agg)
    if comparison["extra"]:
        print("EXTRA", comparison["extra"][:20])
    if comparison["missing"]:
        print("MISSING", comparison["missing"][:20])
    if comparison["mismatches"]:
        print("MISMATCH", comparison["mismatches"][:10])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
