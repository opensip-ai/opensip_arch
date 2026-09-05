"""Executable architecture models; deliberately not a product implementation.

Checks retained, independently reviewable expected outcomes. OS durability,
native binary qualification, full Unicode tables and crypto are not simulated
as passed. All model quantities are explicit fixture inputs.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import struct
import tarfile
import unicodedata


def installed_size(nodes):
    logical = 0
    allocated = 0
    seen = set()
    for n in nodes:
        if not n.get("measurable", True):
            return {"status": "NON-PASS"}
        xattr = sum(len(k.encode()) + len(bytes.fromhex(v)) for k, v in n.get("xattrs", {}).items())
        size = n.get("length", 0) if n["type"] == "file" else len(n.get("target", "").encode())
        logical += size + xattr
        key = (n["device"], n["inode"])
        if key not in seen:
            allocated += n["blocks"] * 512 + xattr
            seen.add(key)
    total = max(logical, allocated)
    if any(x > 2**64 - 1 for x in (logical, allocated, total)):
        return {"status": "NON-PASS"}
    return {"logical": logical, "allocated": allocated, "budgetBytes": total,
            "status": "PASS" if total <= 80_000_000 else "FAIL"}


def metadata_admission(value):
    limits = {"manifestBytes": 4_194_304, "treeEntries": 100_000,
              "pathBytes": 1024, "aliases": 64, "commands": 4096,
              "commandDepth": 32, "jsonDepth": 64}
    for key, limit in limits.items():
        x = value.get(key, 0)
        if type(x) is not int or x < 0 or x > limit:
            return "REFUSE_LIMIT:" + key
    return "ACCEPT"


def path_admission(paths):
    seen = set()
    reserved = {"con", "prn", "aux", "nul"} | {f"{p}{i}" for p in ("com", "lpt") for i in range(1, 10)}
    for p in paths:
        if len(p.encode()) > 1024 or "\\" in p or "\0" in p or p.startswith("/") or ":" in p:
            return "REFUSE_PATH"
        segments = p.split("/")
        if any(s in ("", ".", "..") or s.endswith((".", " ")) or s.split(".")[0].casefold() in reserved for s in segments):
            return "REFUSE_PATH"
        if unicodedata.normalize("NFC", p) != p:
            return "REFUSE_NON_NFC"
        folded = unicodedata.normalize("NFC", p.casefold())
        if folded in seen:
            return "REFUSE_COLLISION"
        seen.add(folded)
    return "ACCEPT"


def compatible_lock(data):
    """Exact-major cases only; general SemVer solver is an implementation gate."""
    if not data["authenticatedIndex"] or not data["inputsPresent"]:
        return "REFUSE"
    common = set(data["hostMajors"]) & set(data["componentMajors"])
    if not common or data["pinnedMajor"] not in common:
        return "REFUSE"
    if data.get("observedMajor", data["pinnedMajor"]) != data["pinnedMajor"]:
        return "REFUSE"
    return "ACCEPT"


def lifecycle(data):
    """Recovery observations, not a claim about SQLite or filesystem durability."""
    if not data.get("databaseReadable", True):
        return {"selection": None, "action": "REFUSE"}
    phase = data["phase"]
    if phase == "COMMITTED":
        if not data.get("treeVerified", True) or not data.get("currentTrustAllows", True):
            return {"selection": None, "action": "REFUSE"}
        return {"selection": "new", "action": "USE"}
    return {"selection": "old", "action": "QUARANTINE" if phase in ("PREPARING", "VERIFIED") else "RETAIN_FOR_RETRY"}


def can_gc(data):
    return "KEEP" if any(data.values()) else "DELETE"


def ci_select(data):
    components = set(data["previousComponents"]) | set(data["currentComponents"])
    shared = {f"SL-{i}" for i in range(1, 7)}
    universe = components | shared
    invalid = data.get("refuseOnly", [])
    if invalid:
        return {"ambiguity": "refuse-only", "selected": [], "skipped": sorted(universe)}
    owners = data["owners"]
    if any(not owners.get(unit) or any(o not in universe for o in owners[unit]) for unit in data["changed"]):
        return {"ambiguity": "refuse-only", "selected": [], "skipped": sorted(universe)}
    if any(len(owners[u]) > 1 for u in data["changed"]):
        return {"ambiguity": "conflict-universe", "selected": sorted(universe), "skipped": []}
    selected = {o for u in data["changed"] for o in owners[u]}
    while True:
        before = selected.copy()
        for consumer, dependencies in data["dependencies"].items():
            if set(dependencies) & selected:
                selected.add(consumer)
        for lane, consumers in data["sharedConsumers"].items():
            if lane in selected:
                selected.update(consumers)
        if len(selected & components) >= 2:
            selected.update({"SL-2", "SL-3", "SL-4"})
        if selected == before:
            break
    return {"ambiguity": "none", "selected": sorted(selected), "skipped": sorted(universe - selected)}


def archive_encode(entries):
    """Profile.1 byte construction for small actual-payload design vectors."""
    result = bytearray()
    for entry in sorted(entries, key=lambda e: e["path"]):
        path = entry["path"].encode()
        target = entry.get("target", "").encode()
        if len(path) > 100 or len(target) > 100:
            raise ValueError("USTAR_CAPACITY")
        payload = bytes.fromhex(entry.get("hex", ""))
        h = bytearray(512)
        h[:len(path)] = path
        for off, width, number in ((100, 8, int(entry["mode"], 8)), (108, 8, 0),
                                   (116, 8, 0), (124, 12, len(payload)),
                                   (136, 12, 0), (329, 8, 0), (337, 8, 0)):
            octets = f"{number:0{width-1}o}".encode() + b"\0"
            if len(octets) != width:
                raise ValueError("USTAR_NUMERIC_CAPACITY")
            h[off:off+width] = octets
        h[156] = {"file": ord("0"), "dir": ord("5"), "symlink": ord("2")}[entry["type"]]
        h[157:157+len(target)] = target
        h[257:263] = b"ustar\0"
        h[263:265] = b"00"
        h[148:156] = b" " * 8
        h[148:156] = f"{sum(h):06o}".encode() + b"\0 "
        result.extend(h)
        result.extend(payload)
        result.extend(b"\0" * (-len(payload) % 512))
    result.extend(b"\0" * 1024)
    return bytes(result)


def archive_result(data):
    try:
        raw = archive_encode(data["entries"])
    except ValueError as e:
        return {"status": str(e)}
    # A separately implemented standard-library decoder checks actual payloads.
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tf:
        decoded = [{"path": m.name, "type": "file" if m.isfile() else "dir" if m.isdir() else "symlink",
                    "hex": tf.extractfile(m).read().hex() if m.isfile() else ""} for m in tf.getmembers()]
    return {"status": "ENCODED", "length": len(raw), "decoded": decoded}


MODELS = {"installed_size": installed_size, "metadata": metadata_admission,
          "path": path_admission, "lock": compatible_lock, "lifecycle": lifecycle,
          "gc": can_gc, "ci": ci_select, "archive": archive_result}


def run():
    folder = Path(__file__).parent
    cases_path = folder / "distribution-design-cases.v1.json"
    corpus = json.loads(cases_path.read_text())
    results = []
    for case in corpus["cases"]:
        actual = MODELS[case["model"]](case["input"])
        results.append({"id": case["id"], "passed": actual == case["expected"],
                        "actual": actual, "expected": case["expected"]})
    report = {"kind": "architecture-reference-model-evidence", "productQualification": False,
              "subject": {"casesSha256": hashlib.sha256(cases_path.read_bytes()).hexdigest(),
                          "modelSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              "limitations": ["No product binary executed", "No OS crash or process isolation qualification",
                              "Unicode examples only, not exhaustive frozen-table qualification",
                              "Exact-major compatibility examples, not full SemVer solver qualification"],
              "count": len(results), "passed": sum(r["passed"] for r in results), "results": results}
    (folder / "distribution-model-report.v1.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"count": report["count"], "passed": report["passed"], "productQualification": False}))
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(run())
