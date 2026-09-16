"""Custody, coverage and correspondence for bootstrap-selection-v1. Read-only vs arch/product."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-bootstrap-selection-v1-review/review")
MANIFEST = "docs/implementation/m1/bootstrap-selection-v1-subject.json"
EXPECTED = "410bfd59ed87392598f8329d591ed24545b59bb56d814c04fc0617659d6cd9d5"
SEL = ARCH / "docs/implementation/m1/bootstrap-selection-v1"
FROZEN10 = Path("/tmp/opensip-implementation/m1-typescript-boundary-package-subject-10/tools/typescript-boundary")
CARGO = ARCH / "docs/implementation/m1/trials/package-boundaries-02/subject"


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def pin_rows(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty pin list")
    paths = [row.get("path") for row in value]
    if any(not isinstance(p, str) for p in paths) or paths != sorted(set(paths)):
        raise ValueError(f"{label} paths must be sorted and unique")
    return value


def custody(label: str) -> dict:
    raw = (ARCH / MANIFEST).read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    manifest = json.loads(raw)
    listed = manifest["files"]
    paths = [row["path"] for row in listed]
    mismatches = []
    for row in listed:
        actual = pin(ARCH / row["path"])
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
            mismatches.append(row["path"])
    copy_root = REVIEW / "copy"
    if label == "before":
        if copy_root.exists():
            shutil.rmtree(copy_root)
        copy_root.mkdir(parents=True)
        dest = copy_root / MANIFEST
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        for row in listed:
            dst = copy_root / row["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((ARCH / row["path"]).read_bytes())
    return {
        "label": label,
        "outerSha256": outer,
        "expected": EXPECTED,
        "match": outer == EXPECTED,
        "listed": len(listed),
        "sorted": paths == sorted(set(paths)),
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:20],
        "ok": outer == EXPECTED and not mismatches and len(listed) == 106 and paths == sorted(set(paths)),
    }


def selected_passage(raw: bytes, selector: dict):
    if set(selector) == {"line"}:
        lines = raw.decode("utf-8").splitlines()
        return lines[selector["line"] - 1]
    pointer = selector["jsonPointer"]
    value = json.loads(raw)
    for token in pointer[1:].split("/"):
        key = token.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    results.mkdir(parents=True, exist_ok=True)
    before = custody("before")
    (results / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")

    subject = json.loads((ARCH / MANIFEST).read_text())
    successor = json.loads((SEL / "successor.json").read_text())
    mmap = json.loads((SEL / "materialization-map.json").read_text())
    registry = json.loads((SEL / "product/tools/typescript-lanes.json").read_text())
    inv8 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v8.json").read_text())
    lock = json.loads((PROD / "design-lock.json").read_text())

    members = pin_rows(subject["files"], "contract subject")
    member_map = {row["path"]: row for row in members}
    record_path = "docs/implementation/m1/bootstrap-selection-v1/successor.json"
    candidates = pin_rows(successor["candidates"], "contract candidates")
    parents = pin_rows(successor["parents"], "contract parents")
    cover = {row["path"] for row in candidates} == set(member_map) - {record_path}
    candidate_pins_equal = all(member_map[row["path"]] == row for row in candidates)

    parent_actual = []
    for row in parents:
        actual = pin(ARCH / row["path"])
        parent_actual.append({"path": row["path"], "match": actual == {"bytes": row["bytes"], "sha256": row["sha256"]}})

    inv8_paths = {row["path"] for row in inv8["files"]}
    owned = []
    for row in mmap["files"]:
        src = ARCH / row["candidatePath"]
        actual = pin(src)
        owned.append({
            "productPath": row["productPath"],
            "pinMatch": actual == {"bytes": row["bytes"], "sha256": row["sha256"]},
            "inInventory8": row["productPath"] in inv8_paths,
        })

    registry_files = registry["files"]
    reg_paths = [row["path"] for row in registry_files]
    first_party = [p for p in reg_paths if "node_modules" not in p.split("/")]
    owned_set = {row["productPath"] for row in mmap["files"]}

    # checker10 correspondence (exclude README)
    checker_rel = []
    checker_root = SEL / "product/tools/typescript-boundary"
    for dirpath, dirnames, filenames in os.walk(checker_root):
        dirnames[:] = [d for d in dirnames if d != "node_modules"]
        rel_dir = Path(dirpath).relative_to(checker_root)
        for name in filenames:
            rel = (rel_dir / name).as_posix() if str(rel_dir) != "." else name
            checker_rel.append(rel)
    checker_changed = []
    missing10 = []
    for rel in sorted(checker_rel):
        a = checker_root / rel
        b = FROZEN10 / rel
        if not b.is_file():
            missing10.append(rel)
            continue
        if a.read_bytes() != b.read_bytes():
            checker_changed.append(rel)

    cargo = {
        "check": pin(SEL / "product/tools/check_package_edges.py") == pin(CARGO / "tools/check_package_edges.py"),
        "test": pin(SEL / "product/tools/tests/test_package_edges.py") == pin(CARGO / "tools/tests/test_package_edges.py"),
    }

    overrides = []
    for row in successor["passageOverrides"]:
        raw = (ARCH / row["parent"]["path"]).read_bytes()
        parent_pin = pin(ARCH / row["parent"]["path"])
        actual = selected_passage(raw, row["selector"])
        overrides.append({
            "selector": row["selector"],
            "parentMatch": parent_pin == {"bytes": row["parent"]["bytes"], "sha256": row["parent"]["sha256"]},
            "beforeMatch": actual == row["before"],
            "afterDiffers": row["after"] != row["before"],
        })

    live_contracts = [row["record"]["path"] for row in lock.get("contractSuccessors", [])]
    live_inv = [row["candidate"]["path"] for row in lock.get("inventorySuccessors", [])]
    accepted_live = {row["path"] for row in lock.get("inputs", [])}
    reused = [row["path"] for row in candidates if row["path"] in accepted_live]

    files7 = inv8["files"][7]
    files13 = inv8["files"][13]
    files157 = inv8["files"][157]

    out = {
        "custodyOk": before["ok"],
        "subjectFiles": len(members),
        "candidateCount": len(candidates),
        "candidatesCover": cover,
        "candidatePinsEqual": candidate_pins_equal,
        "passageOverrides": len(successor["passageOverrides"]),
        "passageOverrideChecks": overrides,
        "passagesOk": all(r["parentMatch"] and r["beforeMatch"] and r["afterDiffers"] for r in overrides),
        "parents": parent_actual,
        "ownedCount": len(owned),
        "ownedPinMismatches": [r["productPath"] for r in owned if not r["pinMatch"]],
        "ownedMissingFromInv8": [r["productPath"] for r in owned if not r["inInventory8"]],
        "registryFiles": len(registry_files),
        "registrySortedUnique": reg_paths == sorted(set(reg_paths)),
        "registryFirstParty": first_party,
        "registryNodePin": registry["node"],
        "lanes": [{"name": lane["name"], "toolPolicy": lane["toolPolicy"], "inputs": lane["record"]["inputs"]} for lane in registry["lanes"]],
        "checkerAuthored": len(checker_rel),
        "checkerChangedVsFrozen10": checker_changed,
        "checkerMissingFromFrozen10": missing10,
        "cargoUnchanged": cargo,
        "liveInventory": live_inv,
        "liveContracts": live_contracts,
        "liveLockPin": pin(PROD / "design-lock.json"),
        "reusedAcceptedPaths": reused,
        "files7": files7["path"],
        "files13": files13["path"],
        "files157": files157["path"],
        "inventory8Packages": len(inv8["packages"]),
        "wrapperRequiresNode": "--node" in (SEL / "product/tools/check_typescript.py").read_text(),
        "wrapperNoSysExecutable": "sys.executable" not in (SEL / "product/tools/check_typescript.py").read_text().split("args.python")[0],
    }
    (results / "analysis.json").write_text(json.dumps(out, indent=2) + "\n")
    summary = {
        "custodyOk": before["ok"],
        "joinsOk": cover and candidate_pins_equal and len(members) == 106 and len(candidates) == 105,
        "owned52": len(owned) == 52 and not out["ownedPinMismatches"] and not out["ownedMissingFromInv8"],
        "registry160": len(registry_files) == 160 and out["registrySortedUnique"] and len(registry["lanes"]) == 3,
        "passages6": len(overrides) == 6 and out["passagesOk"],
        "checker10ReadmeOnly": checker_changed == ["README.md"] and not missing10,
        "cargoUnchanged": cargo["check"] and cargo["test"],
        "packages20": len(inv8["packages"]) == 20,
        "liveFourInvFiveContract": len(live_inv) == 4 and len(live_contracts) == 5,
        "inventory8NotLive": "docs/implementation/m1/repository-file-inventory.v8.json" not in live_inv,
        "genv2Live": "docs/implementation/m1/generator-selection-v2/successor.json" in live_contracts,
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
