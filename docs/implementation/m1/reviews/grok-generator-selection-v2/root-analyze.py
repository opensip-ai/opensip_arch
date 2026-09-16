"""Independent Grok controls for inventory6 and generator-selection v2.

Read-only against architecture/product/frozen subjects. Writes only under this review tree.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

REVIEW = Path("/tmp/opensip-implementation/m1-root-generator05-selection-reproduction")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
CAND05 = Path("/tmp/opensip-implementation/m1-combined-generation-candidate-05")
COPY = REVIEW / "copy"
PROBES = REVIEW / "probes"
RESULTS = REVIEW / "results"
PY = Path("/tmp/opensip-implementation/metadata-reference-env/bin/python")

INV_MANIFEST = "docs/implementation/m1/tooling-inventory-v6-subject.json"
GEN_MANIFEST = "docs/implementation/m1/generator-selection-v2-subject.json"
EXPECTED_INV = "3f0e683d88795ef8bb8667106c567deeb2a3106480c02a0286fd5594fa59be2f"
EXPECTED_GEN = "4f2e473e8bbfa278a8054bc3697542cddb824bf1bd8a6a3766b0a8f0f8aae4c7"
EXPECTED_CLOSURE = "e1b498d0c678d2b0fef2ec735286e4f4223f6b5f0a2dd0016720caab9ad91b6b"
EXPECTED_V1 = "224029710644805c04486de173e64dc08a613ef5bed9433233d336702ece342b"
EXPECTED_INV5 = "87689124f9538b906bd521929d696bd7460913c0a5b2dcfb4c6a007bb1c00b27"
EXPECTED_INV5_CAND = "ec7292f6545e564bae77a8b56ca34ee51af94b70ab3b7484feaecb6df2f22687"
EXPECTED_INV5_REVIEW = "c5607c5fca925515c72079fef24bcade2d22d4ccc3cf8d0a08243cdb15391f93"
RESOURCES = Path(
    "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python"
)
LAUNCHERS = [
    Path("/opt/homebrew/opt/python@3.14/bin/python3.14"),
    Path("/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14"),
    Path("/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"),
]
PINNED_PY = {
    "bytes": 51392,
    "sha256": "0c9a985712bb1235d8fe474a6a99810dc118bcae0dfb429a237aac0c907fa3af",
}
LAUNCHER_PIN = {
    "bytes": 52448,
    "sha256": "b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf",
}


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(path: Path):
    return json.loads(path.read_text())


def pin_rows(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty pin list")
    paths = [row.get("path") for row in value]
    if any(not isinstance(p, str) for p in paths) or paths != sorted(set(paths)):
        raise ValueError(f"{label} paths must be sorted and unique")
    return value


def copy_subject(rel: str) -> None:
    manifest = load(ARCH / rel)
    dest_manifest = COPY / rel
    dest_manifest.parent.mkdir(parents=True, exist_ok=True)
    dest_manifest.write_bytes((ARCH / rel).read_bytes())
    for row in manifest["files"]:
        src = ARCH / row["path"]
        dst = COPY / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())


def custody(rel: str, expected: str) -> dict:
    raw = (ARCH / rel).read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    manifest = json.loads(raw)
    listed = manifest["files"]
    paths = [row["path"] for row in listed]
    mismatches = []
    for row in listed:
        actual = pin(ARCH / row["path"])
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
            mismatches.append({"path": row["path"], "actual": actual, "pin": row})
    return {
        "rel": rel,
        "outer": outer,
        "expected": expected,
        "match": outer == expected,
        "listed": len(listed),
        "sorted": paths == sorted(set(paths)),
        "mismatches": mismatches,
        "ok": outer == expected and not mismatches and paths == sorted(set(paths)),
    }


def inventory_analysis() -> dict:
    v5 = load(ARCH / "docs/implementation/m1/repository-file-inventory.v5.json")
    v6 = load(ARCH / "docs/implementation/m1/repository-file-inventory.v6.json")
    successor = load(ARCH / "docs/implementation/m1/tooling-inventory-v6/successor.json")
    parent_pin = pin(ARCH / "docs/implementation/m1/repository-file-inventory.v5.json")
    cand_pin = pin(ARCH / "docs/implementation/m1/repository-file-inventory.v6.json")
    rec_pin = pin(ARCH / "docs/implementation/m1/tooling-inventory-v6/successor.json")
    v5_map = {row["path"]: row for row in v5["files"]}
    v6_map = {row["path"]: row for row in v6["files"]}
    inherited = sorted(set(v5_map) & set(v6_map))
    added = sorted(set(v6_map) - set(v5_map))
    removed = sorted(set(v5_map) - set(v6_map))
    inherited_equal = all(v5_map[p] == v6_map[p] for p in inherited)
    other_keys = sorted((set(v5) | set(v6)) - {"standing", "files"})
    other_equal = {k: v5.get(k) == v6.get(k) for k in other_keys}
    files7_v5 = v5["files"][7]
    files7_v6 = v6["files"][7]
    tsconfig = v6_map.get("tools/contracts/tsconfig.json")
    v5_paths = [row["path"] for row in v5["files"]]
    v6_paths = [row["path"] for row in v6["files"]]
    unit = load(ARCH / "docs/implementation/m1/tooling-inventory-v5-unit.json")
    review = pin(ARCH / "docs/implementation/m1/reviews/grok-tooling-inventory-v5/review.json")
    return {
        "v5Files": len(v5["files"]),
        "v6Files": len(v6["files"]),
        "inherited": len(inherited),
        "inheritedEqual": inherited_equal,
        "added": added,
        "removed": removed,
        "packagesV5": len(v5["packages"]),
        "packagesV6": len(v6["packages"]),
        "packagesEqual": v5["packages"] == v6["packages"],
        "otherKeys": other_keys,
        "otherEqual": other_equal,
        "allOtherEqual": all(other_equal.values()),
        "v5SortedUnique": v5_paths == sorted(set(v5_paths)),
        "v6SortedUnique": v6_paths == sorted(set(v6_paths)),
        "files7v5": files7_v5,
        "files7v6": files7_v6,
        "files7Equal": files7_v5 == files7_v6,
        "files7Path": files7_v6.get("path"),
        "tsconfig": tsconfig,
        "parentPin": parent_pin,
        "parentExpected": {"bytes": 118054, "sha256": EXPECTED_INV5_CAND},
        "parentMatch": parent_pin == {"bytes": 118054, "sha256": EXPECTED_INV5_CAND},
        "candidatePin": cand_pin,
        "candidateExpected": {
            "bytes": 118433,
            "sha256": "52e75edc8a30aa304d2f3e42f541a5ece1c00d9e1f21435651ac29776d0b81c1",
        },
        "candidateMatch": cand_pin
        == {
            "bytes": 118433,
            "sha256": "52e75edc8a30aa304d2f3e42f541a5ece1c00d9e1f21435651ac29776d0b81c1",
        },
        "successorPin": rec_pin,
        "successorExpected": {
            "bytes": 799,
            "sha256": "f407718ae537ebca4e736a5b75387a4b4f22eaec3c101894ecc53f1973e571ab",
        },
        "successorMatch": rec_pin
        == {
            "bytes": 799,
            "sha256": "f407718ae537ebca4e736a5b75387a4b4f22eaec3c101894ecc53f1973e571ab",
        },
        "successorAddedFiles": successor.get("addedFiles"),
        "successorParent": successor.get("parent"),
        "successorCandidate": successor.get("candidate"),
        "inventory5Unit": {
            "status": unit.get("status"),
            "rootSubstantiveAssent": unit.get("rootSubstantiveAssent"),
            "requiredUnitFindings": unit.get("requiredUnitFindings"),
            "reviewSha": unit.get("independentReview", {}).get("sha256"),
            "reviewPin": review,
            "reviewMatch": review["sha256"] == EXPECTED_INV5_REVIEW,
            "acceptedInventory": unit.get("acceptedInventory"),
        },
        "nodeModulesRows": [p for p in v6_paths if "node_modules" in p or "python-packages/" in p],
    }


def generator_analysis() -> dict:
    subject = load(ARCH / GEN_MANIFEST)
    successor = load(ARCH / "docs/implementation/m1/generator-selection-v2/successor.json")
    mmap = load(ARCH / "docs/implementation/m1/generator-selection-v2/materialization-map.json")
    policy = load(ARCH / "docs/implementation/m1/generator-selection-v2/generator-loader-policy.json")
    validation = load(ARCH / "docs/implementation/m1/generator-selection-v2/selection-validation.json")
    v6 = load(ARCH / "docs/implementation/m1/repository-file-inventory.v6.json")
    inv6_paths = {row["path"] for row in v6["files"]}
    members = pin_rows(subject["files"], "contract subject")
    member_map = {row["path"]: row for row in members}
    record_path = "docs/implementation/m1/generator-selection-v2/successor.json"
    candidates = pin_rows(successor["candidates"], "contract candidates")
    parents = pin_rows(successor["parents"], "contract parents")
    cover = {row["path"] for row in candidates} == set(member_map) - {record_path}
    candidate_pins_equal = all(member_map[row["path"]] == row for row in candidates)
    parent_actual = []
    for row in parents:
        actual = pin(ARCH / row["path"])
        parent_actual.append(
            {
                "path": row["path"],
                "pin": {"bytes": row["bytes"], "sha256": row["sha256"]},
                "actual": actual,
                "match": actual == {"bytes": row["bytes"], "sha256": row["sha256"]},
            }
        )
    owned = []
    for row in mmap["files"]:
        src = ARCH / row["candidatePath"]
        actual = pin(src)
        cand05 = CAND05 / row["productPath"]
        cand_pin = pin(cand05) if cand05.is_file() else None
        owned.append(
            {
                "productPath": row["productPath"],
                "pinMatch": actual == {"bytes": row["bytes"], "sha256": row["sha256"]},
                "cand05Match": cand_pin == actual if cand_pin else False,
                "inInventory6": row["productPath"] in inv6_paths,
            }
        )
    closure = load(ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/generator-closure.json")
    closure_pin = pin(ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/generator-closure.json")
    cand_closure_pin = pin(CAND05 / "tools/contracts/generator-closure.json")
    v1_closure = load(ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/generator-closure.json")
    v2_paths = [row["path"] for row in closure["files"]]
    v1_paths = [row["path"] for row in v1_closure["files"]]
    product_root = ARCH / "docs/implementation/m1/generator-selection-v2/product"
    v1_product = ARCH / "docs/implementation/m1/generator-selection-v1/product"
    owned_rel = [row["productPath"] for row in mmap["files"]]
    vs_v1 = []
    for rel in owned_rel:
        a = product_root / rel
        b = v1_product / rel
        if not b.exists():
            vs_v1.append({"rel": rel, "status": "new", "sha": pin(a)["sha256"][:12]})
        elif a.read_bytes() != b.read_bytes():
            vs_v1.append(
                {
                    "rel": rel,
                    "status": "changed",
                    "v1": pin(b)["sha256"][:12],
                    "v2": pin(a)["sha256"][:12],
                }
            )
        else:
            vs_v1.append({"rel": rel, "status": "same"})
    live = load(PROD / "design-lock.json")
    live_inv = [row.get("candidate", {}).get("path") or row.get("selected") for row in live.get("inventorySuccessors", [])]
    # inventorySuccessors in lock may use nested candidate
    if live_inv and live_inv[0] is None:
        live_inv = []
        for row in live.get("inventorySuccessors", []):
            cand = row.get("candidate")
            if isinstance(cand, dict):
                live_inv.append(cand.get("path"))
            elif isinstance(cand, str):
                live_inv.append(cand)
    live_contracts = [row.get("record", {}).get("path") for row in live.get("contractSuccessors", [])]
    accepted_live_paths = set()
    for row in live.get("inputs", []):
        accepted_live_paths.add(row["path"])
    reused = [row["path"] for row in candidates if row["path"] in accepted_live_paths]
    reused += [record_path] if record_path in accepted_live_paths else []
    src = (ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/generate_contracts.py").read_text()
    tree = ast.parse(src)
    assigns_sys_executable = False
    python_required = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            text = ast.get_source_segment(src, node) or ""
            if "sys.executable" in text and "args.python" in text:
                assigns_sys_executable = True
        if isinstance(node, ast.Call):
            func = ast.get_source_segment(src, node.func) if node.func else ""
            if func and "add_argument" in func:
                args = [ast.literal_eval(a) if isinstance(a, ast.Constant) else None for a in node.args]
                if "--python" in args:
                    for kw in node.keywords:
                        if kw.arg == "required" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            python_required = True
    assemble = (ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/assemble-native.cjs").read_text()
    v1_assemble = (ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/assemble-native.cjs").read_text()
    tsconfig = load(ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/tsconfig.json")
    pipeline_same = pin(
        ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/pipeline.py"
    ) == pin(ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/pipeline.py")
    py_profile_same = pin(
        ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/python-profile.json"
    ) == pin(ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/python-profile.json")
    native_profile_same = pin(
        ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/native-python-profile.json"
    ) == pin(ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/native-python-profile.json")
    toolchain_same = pin(
        ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/toolchain.json"
    ) == pin(ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/contracts/toolchain.json")
    return {
        "subjectFiles": len(members),
        "pinRowsCandidates": True,
        "pinRowsParents": True,
        "recordInSubject": member_map.get(record_path) is not None
        and member_map[record_path]
        == {
            "path": record_path,
            "bytes": 12258,
            "sha256": "aee8e370867160b1c421c4879549492d2b686d12e73b79515b18241d124de5a1",
        },
        "candidatesCover": cover,
        "candidateCount": len(candidates),
        "candidatePinsEqual": candidate_pins_equal,
        "passageOverrides": successor.get("passageOverrides"),
        "parents": parent_actual,
        "ownedCount": len(owned),
        "ownedPinMismatches": [r["productPath"] for r in owned if not r["pinMatch"]],
        "ownedCand05Mismatches": [r["productPath"] for r in owned if not r["cand05Match"]],
        "ownedMissingFromInv6": [r["productPath"] for r in owned if not r["inInventory6"]],
        "closureFiles": len(closure["files"]),
        "closurePin": closure_pin,
        "cand05ClosurePin": cand_closure_pin,
        "closureMatchExpected": closure_pin["sha256"] == EXPECTED_CLOSURE and closure_pin["bytes"] == 68280,
        "architectureOwnsCandidate05Closure": closure_pin == cand_closure_pin,
        "v1ClosureFiles": len(v1_closure["files"]),
        "closureAddedPaths": sorted(set(v2_paths) - set(v1_paths)),
        "closureRemovedPaths": sorted(set(v1_paths) - set(v2_paths)),
        "closureInheritedEqual": all(
            next(r for r in closure["files"] if r["path"] == p) == next(r for r in v1_closure["files"] if r["path"] == p)
            for p in set(v1_paths) & set(v2_paths)
        ),
        "vsV1Changed": [r for r in vs_v1 if r["status"] != "same"],
        "vsV1Same": sum(1 for r in vs_v1 if r["status"] == "same"),
        "liveInventory": live_inv,
        "liveContracts": live_contracts,
        "liveLockPin": pin(PROD / "design-lock.json"),
        "reusedAcceptedPaths": reused,
        "assignsSysExecutable": assigns_sys_executable,
        "pythonArgRequired": python_required,
        "assembleRequireTypescript": "require('typescript')" in assemble or 'require("typescript")' in assemble,
        "assembleNodeModulesPath": "./node_modules/typescript" in assemble,
        "v1AssembleNodeModulesPath": "./node_modules/typescript" in v1_assemble,
        "tsconfig": tsconfig,
        "pipelineUnchangedVsV1": pipeline_same,
        "pythonProfileUnchangedVsV1": py_profile_same,
        "nativeProfileUnchangedVsV1": native_profile_same,
        "toolchainUnchangedVsV1": toolchain_same,
        "policyLaneTrustedUsages": policy["lane"]["trustedUsages"],
        "policyTrustedUsagesCount": len(policy["trustedUsages"]),
        "policyFiles": len(policy["files"]),
        "policyHasStaticClosureComplete": "staticClosureComplete" in json.dumps(policy)
        or "static-closure-complete" in json.dumps(policy),
        "policyGeneralPlugin": "plugin" in json.dumps(policy).lower() and "repository plugins" in json.dumps(policy),
        "validation": validation,
        "v1SubjectPin": pin(ARCH / "docs/implementation/m1/generator-selection-v1-subject.json"),
        "inv5SubjectPin": pin(ARCH / "docs/implementation/m1/tooling-inventory-v5-subject.json"),
        "v1Unit": load(ARCH / "docs/implementation/m1/generator-selection-v1-unit.json").get("status"),
    }


def policy_against_code() -> dict:
    policy = load(ARCH / "docs/implementation/m1/generator-selection-v2/generator-loader-policy.json")
    validate = (ARCH / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/validate-schemas.cjs").read_text().splitlines()
    ts_path = CAND05 / "tools/contracts/node_modules/typescript/lib/typescript.js"
    ts_pin = pin(ts_path)
    ts_lines = ts_path.read_text(errors="replace").splitlines()
    usages = []
    for u in policy["trustedUsages"]:
        if u["file"].endswith("validate-schemas.cjs"):
            line = validate[u["line"] - 1]
            col = u["column"] - 1
            snippet = line[col : col + len(u["text"])]
            usages.append(
                {
                    "file": u["file"],
                    "lineText": line,
                    "snippet": snippet,
                    "textMatch": snippet == u["text"],
                    "targets": u["targets"],
                    "reasonMentionsThreeRuntime": "three exact selected runtime source files" in u["reason"],
                }
            )
        elif u["file"].endswith("typescript.js"):
            line = ts_lines[u["line"] - 1]
            col = u["column"] - 1
            snippet = line[col : col + len(u["text"])]
            guarded = False
            if u["kind"] == "optional-unresolved":
                window = "\n".join(ts_lines[u["line"] - 8 : u["line"] + 8])
                guarded = "try" in window and "catch" in window
            usages.append(
                {
                    "file": "typescript.js",
                    "kind": u["kind"],
                    "lineNo": u["line"],
                    "lineText": line.strip()[:200],
                    "snippet": snippet,
                    "textMatch": snippet == u["text"],
                    "targets": u.get("targets"),
                    "guardedTryCatch": guarded,
                    "emptyTargets": u.get("targets") == [],
                }
            )
    unfollowed = policy["unfollowedDynamicLoaders"]
    file_pins = []
    for row in policy["files"]:
        if row["path"].endswith("typescript.js"):
            actual = ts_pin
        else:
            actual = pin(ARCH / "docs/implementation/m1/generator-selection-v2/product" / row["path"])
        file_pins.append({"path": row["path"], "match": actual == {"bytes": row["bytes"], "sha256": row["sha256"]}})
    discovery03 = load(ARCH / "docs/implementation/m1/generator-selection-v2/evidence/generator-discovery03.json")
    return {
        "tsPin": ts_pin,
        "tsPinMatchesPolicy": ts_pin
        == {
            "bytes": 9144216,
            "sha256": "569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39",
        },
        "usages": usages,
        "unfollowedLimitation": unfollowed[0]["limitation"] if unfollowed else None,
        "filePinsOk": all(r["match"] for r in file_pins),
        "filePinFailures": [r["path"] for r in file_pins if not r["match"]],
        "discovery03": {
            "passed": discovery03.get("passed"),
            "selectedToolPolicy": discovery03.get("selectedToolPolicy"),
            "standing": discovery03.get("lane", {}).get("standing"),
            "refusals": discovery03.get("refusals"),
            "trustedUsagesApplied": len(discovery03.get("trustedUsagesApplied") or []),
        },
        "laneTrustedUsagesEmpty": policy["lane"]["trustedUsages"] == [],
        "doesNotClaimStaticClosureComplete": "statically-enumerated-closure" in json.dumps(policy)
        and "complete" not in policy["unfollowedDynamicLoaders"][0]["limitation"],
    }


def python_hosts() -> dict:
    res = pin(RESOURCES)
    launch = []
    for p in LAUNCHERS:
        actual = pin(p.resolve())
        launch.append(
            {
                "path": str(p),
                "resolved": str(p.resolve()),
                "pin": actual,
                "isLauncherPin": actual == LAUNCHER_PIN,
                "isResourcesPin": actual == PINNED_PY,
            }
        )
    return {
        "resources": {"path": str(RESOURCES), "pin": res, "match": res == PINNED_PY},
        "launchers": launch,
        "allLaunchersDiffer": all(x["isLauncherPin"] and not x["isResourcesPin"] for x in launch),
    }


def argparse_probes() -> dict:
    wrapper = COPY / "docs/implementation/m1/generator-selection-v2/product/tools/generate_contracts.py"
    help_p = subprocess.run(
        [str(PY), "-I", "-B", str(wrapper), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    missing = subprocess.run(
        [
            str(PY),
            "-I",
            "-B",
            str(wrapper),
            "--architecture",
            str(ARCH),
            "--output",
            str(PROBES / "no-python-out"),
            "--node",
            "/Users/sb/.nvm/versions/node/v24.16.0/bin/node",
            "--generator",
            "/tmp/opensip-implementation/m1-generator-build-05/opensip-contract-generator",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    v1_wrapper = ARCH / "docs/implementation/m1/generator-selection-v1/product/tools/generate_contracts.py"
    v1_help = subprocess.run(
        [str(PY), "-I", "-B", str(v1_wrapper), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    no_python_dir = PROBES / "no-python-out"
    return {
        "helpExit": help_p.returncode,
        "helpListsPython": "--python" in help_p.stdout and "framework launcher aliases are not interchangeable" in help_p.stdout,
        "missingPythonExit": missing.returncode,
        "missingPythonStderr": missing.stderr.strip()[-400:],
        "missingPythonIsArgparse": missing.returncode == 2 and "--python" in missing.stderr,
        "noPythonDirCreated": no_python_dir.exists(),
        "v1HelpListsPython": "--python" in v1_help.stdout,
        "isolated": sys.flags.isolated if False else True,
    }


def pipeline_pin_probe() -> dict:
    """Refuse launcher before snapshot/output; do not run children."""
    sys.path.insert(0, str(COPY / "docs/implementation/m1/generator-selection-v2/product/tools/contracts"))
    import pipeline as selected_pipeline  # type: ignore

    probe_root = PROBES / "pin-root"
    if probe_root.exists():
        shutil.rmtree(probe_root)
    (probe_root / "tools/contracts").mkdir(parents=True)
    shutil.copy2(
        COPY / "docs/implementation/m1/generator-selection-v2/product/tools/contracts/toolchain.json",
        probe_root / "tools/contracts/toolchain.json",
    )
    tools = load(CAND05 / "local-tools.json")
    out = PROBES / "pin-launcher-out"
    if out.exists():
        shutil.rmtree(out)
    args = SimpleNamespace(
        root=probe_root,
        output=out,
        node=Path(tools["node"]),
        generator=Path(tools["generator"]),
        python=LAUNCHERS[2],  # framework bin launcher
    )
    error = None
    try:
        selected_pipeline.run(args)
    except ValueError as exc:
        error = str(exc)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    resources_pin = selected_pipeline.pin(RESOURCES)
    launcher_pin = selected_pipeline.pin(LAUNCHERS[2].resolve())
    expected = load(probe_root / "tools/contracts/toolchain.json")["executables"]["python"]
    return {
        "launcherError": error,
        "launcherRefused": error == "tool bytes differ: python",
        "outputCreated": out.exists(),
        "resourcesMatchesToolchain": resources_pin == expected,
        "launcherDiffersToolchain": launcher_pin != expected,
        "pipelinePinFunctionUsed": True,
    }


def activation_evidence() -> dict:
    trial_err = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/generator-activation-01/drift.stderr")
    if not trial_err.exists():
        # architecture path may differ; use subject copy of evidence plus known trial dir
        trial_err = Path("/tmp/opensip-implementation/m1-generator-activation-01")
        candidates = list(Path("/tmp/opensip-implementation/m1-generator-activation-01").glob("**/drift.stderr"))
        trial_pin = pin(candidates[0]) if candidates else None
        trial_path = str(candidates[0]) if candidates else None
    else:
        trial_pin = pin(trial_err)
        trial_path = str(trial_err)
    v2_err = pin(ARCH / "docs/implementation/m1/generator-selection-v2/evidence/activation04-drift.stderr")
    exercise = (CAND05 / "activation04-failure/exercise_public.py").read_text()
    pipeline02 = load(ARCH / "docs/implementation/m1/generator-selection-v2/evidence/internal-pipeline02.json")
    cand_result = load(CAND05 / "generation-internal-02/result.json")
    out04 = Path("/tmp/opensip-implementation/m1-root-generator04-reproduction/generation-internal-01/assembly/output")
    out05 = CAND05 / "generation-internal-02/assembly/output"
    outputs = []
    for row in cand_result["outputs"]:
        a = out05 / row["path"]
        b = out04 / row["path"]
        pa, pb = pin(a), pin(b)
        equal = pa == pb
        if row["path"].endswith("report.ts"):
            t5 = a.read_text().splitlines()[:4]
            t4 = b.read_text().splitlines()[:4]
            body_equal = a.read_bytes().split(b"\n", 3)[-1] == b.read_bytes().split(b"\n", 3)[-1]
            outputs.append(
                {
                    "path": row["path"],
                    "equal": equal,
                    "bytesEqual": pa["bytes"] == pb["bytes"],
                    "head04": t4[:3],
                    "head05": t5[:3],
                    "bodyAfterLine3Equal": body_equal,
                    "sha05": pa["sha256"],
                    "sha04": pb["sha256"],
                }
            )
        else:
            outputs.append({"path": row["path"], "equal": equal, "sha05": pa["sha256"]})
    return {
        "trialPath": trial_path,
        "trialPin": trial_pin,
        "v2EvidencePin": v2_err,
        "stderrMatch": trial_pin == v2_err if trial_pin else False,
        "exerciseHasPythonFlag": "--python" in exercise,
        "exerciseInvokesResourcesParent": "Resources/Python.app/Contents/MacOS/Python" in exercise,
        "pipeline02SourceApproved": pipeline02.get("sourceApproved"),
        "pipeline02Passed": pipeline02.get("passed"),
        "pipeline02ProductModified": pipeline02.get("productModified"),
        "pipeline02MatchesCandidate": pipeline02 == cand_result,
        "outputs": outputs,
        "sevenExactExceptReport": all(o["equal"] for o in outputs if not o["path"].endswith("report.ts"))
        and any(o.get("bodyAfterLine3Equal") and not o["equal"] for o in outputs if o["path"].endswith("report.ts")),
    }


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    RESULTS.mkdir(parents=True, exist_ok=True)
    COPY.mkdir(parents=True, exist_ok=True)
    before = {"inventory": custody(INV_MANIFEST, EXPECTED_INV), "generator": custody(GEN_MANIFEST, EXPECTED_GEN)}
    (RESULTS / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")
    copy_subject(INV_MANIFEST)
    copy_subject(GEN_MANIFEST)
    inv = inventory_analysis()
    gen = generator_analysis()
    pol = policy_against_code()
    hosts = python_hosts()
    args = argparse_probes()
    pinp = pipeline_pin_probe()
    act = activation_evidence()
    out = {
        "inventory": inv,
        "generator": gen,
        "policy": pol,
        "pythonHosts": hosts,
        "argparse": args,
        "pipelinePin": pinp,
        "activation": act,
    }
    (RESULTS / "independent-controls.json").write_text(json.dumps(out, indent=2) + "\n")
    summary = {
        "inventoryOk": inv["inherited"] == 323
        and inv["added"] == ["tools/contracts/tsconfig.json"]
        and inv["removed"] == []
        and inv["inheritedEqual"]
        and inv["packagesEqual"]
        and inv["allOtherEqual"]
        and inv["parentMatch"]
        and inv["candidateMatch"]
        and inv["successorMatch"]
        and inv["files7Path"] == "apps/cli/src/bootstrap.rs"
        and inv["inventory5Unit"]["status"] == "ACCEPTED-UNIT"
        and inv["inventory5Unit"]["rootSubstantiveAssent"] is True,
        "generatorOk": gen["subjectFiles"] == 52
        and gen["candidatesCover"]
        and gen["ownedCount"] == 38
        and not gen["ownedPinMismatches"]
        and not gen["ownedCand05Mismatches"]
        and not gen["ownedMissingFromInv6"]
        and gen["closureFiles"] == 349
        and gen["closureMatchExpected"]
        and gen["architectureOwnsCandidate05Closure"]
        and gen["pythonArgRequired"]
        and not gen["assignsSysExecutable"]
        and gen["assembleRequireTypescript"]
        and not gen["assembleNodeModulesPath"]
        and gen["pipelineUnchangedVsV1"]
        and gen["toolchainUnchangedVsV1"]
        and gen["pythonProfileUnchangedVsV1"],
        "policyOk": pol["filePinsOk"]
        and pol["tsPinMatchesPolicy"]
        and pol["laneTrustedUsagesEmpty"]
        and pol["discovery03"]["selectedToolPolicy"] is None
        and pol["discovery03"]["passed"] is True
        and all(u.get("textMatch") for u in pol["usages"]),
        "pythonFixOk": hosts["resources"]["match"]
        and hosts["allLaunchersDiffer"]
        and args["missingPythonIsArgparse"]
        and not args["noPythonDirCreated"]
        and not args["v1HelpListsPython"]
        and pinp["launcherRefused"]
        and not pinp["outputCreated"]
        and pinp["resourcesMatchesToolchain"],
        "activationOk": act["sevenExactExceptReport"]
        and act["pipeline02SourceApproved"] is False
        and not act["exerciseHasPythonFlag"],
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("DONE analysis")


if __name__ == "__main__":
    main()
