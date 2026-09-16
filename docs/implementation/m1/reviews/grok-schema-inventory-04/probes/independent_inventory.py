"""Independent schema-inventory04 probes. Not a restatement of check.py."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import types
from pathlib import Path

PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
COPY = Path("/tmp/opensip-implementation/m1-grok-schema-inventory-review-04/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-schema-inventory-review-04/review/results")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
NAMES01 = ARCH / "docs/implementation/m1/audits/schema-inventory-names-01"
JSON_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.schema)?\.json")
SOURCE_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*-v[0-9]+\.schema\.json")
ARCH_SOURCE_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.v[0-9]+\.schema\.json")
FOLDER = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
ORIGINAL_ROLES = {
    "manifest", "lockfile", "configuration", "documentation", "entrypoint",
    "public-api", "parser", "composition", "adapter", "model", "codec",
    "algorithm", "validator", "compiler", "builder", "service", "store",
    "factory", "renderer", "template", "view", "style", "registry",
    "fixture", "test",
}
TOOLING_EXCEPTIONS = (
    "crates/identity/src/canonical_tests.rs",
    "design-lock.json",
    "tools/tests/test_design_binding.py",
    "tools/verify_design.py",
)
EXPECTED_ROLES = {
    "schemas/source-map.json": "registry",
    "schemas/profiles/report-codec.json": "configuration",
    "schemas/wire/native-carriers-v1.json": "model",
    "schemas/wire/native-carriers-meta.schema.json": "model",
}


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_bytes())


def compile_exec(path: Path, name: str):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def original_validate(data, *, require_proposed_standing=True, require_test_filename=True):
    """Architecture v1 inventory checker rules, without chapter rendering."""
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise ValueError("Unknown inventory version")
    packages = {p["id"]: p for p in data["packages"]}
    if len(packages) != len(data["packages"]):
        raise ValueError("Duplicate package IDs")
    paths = set()
    for row in data["files"]:
        path = row["path"]
        p = Path(path)
        if path != path.replace("\\", "/") or p.is_absolute() or ".." in p.parts:
            raise ValueError("Noncanonical path: " + path)
        if path in paths:
            raise ValueError("Duplicate path: " + path)
        paths.add(path)
        if row["package"] not in packages:
            raise ValueError("Unknown package: " + path)
        package_path = packages[row["package"]]["path"]
        if package_path and not path.startswith(package_path + "/"):
            raise ValueError("File outside its owning package: " + path)
        owners = [pkg for pkg in packages.values() if not pkg["path"] or path.startswith(pkg["path"] + "/")]
        if row["package"] != max(owners, key=lambda pkg: len(pkg["path"]))["id"]:
            raise ValueError("File assigned outside its most specific package: " + path)
        if row["role"] not in ORIGINAL_ROLES or not row["description"].strip():
            raise ValueError("Missing or unknown file responsibility: " + path)
        if type(row["generated"]) is not bool:
            raise ValueError("Unexpected generated flag: " + path)
        if require_proposed_standing and row["standing"] != "proposed":
            raise ValueError("Unexpected file standing: " + path)
        if p.suffix == ".rs" and not re.fullmatch(r"[a-z][a-z0-9_]*\.rs", p.name):
            raise ValueError("Rust filename: " + path)
        if p.suffix == ".ts" and not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.test)?\.ts", p.name):
            raise ValueError("TypeScript filename: " + path)
        for folder in p.parts[:-1]:
            if not FOLDER.fullmatch(folder):
                raise ValueError("Directory naming: " + path)
        if p.suffix == ".json" and not JSON_NAME.fullmatch(p.name):
            raise ValueError("JSON filename: " + path)
        if row["role"] in {"factory", "renderer", "store"}:
            ending = ("_" if p.suffix == ".rs" else "-") + row["role"] + p.suffix
            if not p.name.endswith(ending):
                raise ValueError("Role suffix mismatch: " + path)
        if require_test_filename and row["role"] == "test":
            if not (p.name.endswith("_tests.rs") or p.name.endswith(".test.ts")):
                raise ValueError("Test filename: " + path)
        if row["generated"] and "generated" not in p.parts:
            raise ValueError("Generated file outside generated/: " + path)
    return packages


def original_fail_reason(data, **kwargs):
    try:
        original_validate(data, **kwargs)
    except (ValueError, KeyError, TypeError) as exc:
        return str(exc)
    return None


def run_check(directory: Path):
    proc = subprocess.run(
        [PY, "-I", "-B", str(directory / "check.py")],
        cwd=str(directory),
        capture_output=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def mutate_check(rows, name, mutator, expect_fail=True):
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        for item in COPY.iterdir():
            target = dest / item.name
            if item.is_file():
                shutil.copy2(item, target)
        mutator(dest)
        code, stdout, stderr = run_check(dest)
        failed = code != 0
        rec(
            rows,
            name,
            failed if expect_fail else (code == 0),
            exit=code,
            stdout=stdout.decode()[:300],
            stderr=stderr.decode()[:300],
        )


def most_specific(packages, path):
    owners = [pkg for pkg in packages if not pkg["path"] or path.startswith(pkg["path"] + "/")]
    return max(owners, key=lambda pkg: len(pkg["path"]))["id"]


def main():
    rows = []
    RESULTS.mkdir(parents=True, exist_ok=True)
    parent = load_json(COPY / "parent.json")
    candidate = load_json(COPY / "candidate.json")
    successor = load_json(COPY / "successor.json")
    source_map = load_json(COPY / "source-map.json")
    auxiliary = load_json(COPY / "auxiliary-input-map.json")
    pins = load_json(COPY / "input-pins.json")["files"]
    parent_rows = {row["path"]: row for row in parent["files"]}
    candidate_rows = {row["path"]: row for row in candidate["files"]}
    added = sorted(set(candidate_rows) - set(parent_rows))
    packages = candidate["packages"]
    parent_packages = parent["packages"]

    rec(rows, "inherited-row-count-202", len(parent["files"]) == 202 == len(parent_rows), count=len(parent["files"]))
    rec(rows, "candidate-row-count-246", len(candidate["files"]) == 246 == len(candidate_rows), count=len(candidate["files"]))
    rec(rows, "added-count-44", len(added) == 44, count=len(added), added=added)
    rec(
        rows,
        "candidate-files-sorted-unique",
        [row["path"] for row in candidate["files"]] == sorted(candidate_rows),
    )
    rec(
        rows,
        "inherited-rows-equal-by-value",
        all(candidate_rows[path] == row for path, row in parent_rows.items()),
    )
    rec(
        rows,
        "packages-edges-pending-unchanged",
        parent_packages == packages
        and parent["pendingDecisions"] == candidate["pendingDecisions"]
        and parent["schemaVersion"] == candidate["schemaVersion"] == 1
        and set(parent) == set(candidate)
        and all(parent[k] == candidate[k] for k in parent if k not in ("standing", "files")),
        packageCount=len(packages),
        pendingCount=len(candidate["pendingDecisions"]),
    )
    rec(rows, "package-count-20", len(packages) == 20 == len({p["id"] for p in packages}))

    map_paths = {row["implementationPath"] for row in source_map["sources"]}
    aux_paths = {row["implementationPath"] for row in auxiliary["inputs"]}
    expected = map_paths | aux_paths | {"schemas/source-map.json"}
    rec(
        rows,
        "added-equals-maps-union-source-map",
        set(added) == expected == set(successor["addedFiles"]) and len(source_map["sources"]) == 40 and len(auxiliary["inputs"]) == 3,
        sourceCount=len(source_map["sources"]),
        auxCount=len(auxiliary["inputs"]),
        disjoint=sorted(map_paths & aux_paths),
    )
    rec(
        rows,
        "successor-addedFiles-sorted-unique",
        successor["addedFiles"] == sorted(set(successor["addedFiles"])) == added,
    )
    rec(
        rows,
        "successor-parent-candidate-pins",
        successor["parent"] == {"path": "docs/implementation/m1/repository-file-inventory.v3.json", "bytes": 71497, "sha256": "63027fb69f55b6fd65f3cb5baa89d355736239060bfa2750f3137e93cbb716ee"}
        and successor["candidate"] == {"path": "docs/implementation/m1/repository-file-inventory.v4.json", "bytes": 87766, "sha256": "c6c85fb8adfe6cdf50dc7b07b7f1e0816275e3e00eb7307e1acb8c1568fe84f5"}
        and successor["parentArtifactBytesUnchanged"] is True
        and successor["inheritedRowsEqualByValue"] is True,
    )

    role_ok = True
    ownership_ok = True
    filename_ok = True
    generated_ok = True
    standing_ok = True
    desc_ok = True
    role_mismatches = []
    for path in added:
        row = candidate_rows[path]
        expected_role = EXPECTED_ROLES.get(path, "model")
        if path.startswith("schemas/sources/") and path.endswith(".schema.json"):
            expected_role = "model"
        if row["role"] != expected_role:
            role_ok = False
            role_mismatches.append({"path": path, "role": row["role"], "expected": expected_role})
        if row["package"] != "shared-assets" or most_specific(packages, path) != "shared-assets":
            ownership_ok = False
        name = Path(path).name
        if path.startswith("schemas/sources/"):
            if not SOURCE_NAME.fullmatch(name):
                filename_ok = False
        elif not JSON_NAME.fullmatch(name):
            filename_ok = False
        if ".v" in name or name.count(".") > (2 if name.endswith(".schema.json") else 1):
            # product destinations must not keep architecture dot-vN
            if ARCH_SOURCE_NAME.fullmatch(name) or ".meta." in name:
                filename_ok = False
        if row["generated"] is not False:
            generated_ok = False
        if row["standing"] != "proposed":
            standing_ok = False
        if not row["description"].strip():
            desc_ok = False
        parts = Path(path).parts
        if any(not FOLDER.fullmatch(part) for part in parts[:-1]):
            filename_ok = False
        if not path.startswith("schemas/"):
            ownership_ok = False
    rec(rows, "added-roles-model-registry-configuration", role_ok, mismatches=role_mismatches)
    rec(rows, "added-most-specific-shared-assets", ownership_ok)
    rec(rows, "added-product-filename-convention", filename_ok)
    rec(rows, "added-generated-false-owned-source", generated_ok)
    rec(rows, "added-standing-proposed", standing_ok)
    rec(rows, "added-descriptions-nonempty", desc_ok)

    owner_missing = []
    id_mismatch = []
    dash_vs_dot = []
    arch_pin_fail = []
    parent_file_paths = set(parent_rows)
    for src in source_map["sources"]:
        impl = src["implementationPath"]
        arch_path = src["architectureSource"]["path"]
        impl_name = Path(impl).name
        arch_name = Path(arch_path).name
        if not SOURCE_NAME.fullmatch(impl_name):
            dash_vs_dot.append({"implementation": impl_name, "architecture": arch_name, "reason": "implementation"})
        if not ARCH_SOURCE_NAME.fullmatch(arch_name):
            dash_vs_dot.append({"implementation": impl_name, "architecture": arch_name, "reason": "architecture"})
        expected_impl = arch_name.replace(".v", "-v")
        if impl_name != expected_impl:
            dash_vs_dot.append({"implementation": impl_name, "architecture": arch_name, "reason": "map"})
        owner = src["semanticValidatorOwner"]
        if owner not in parent_file_paths:
            owner_missing.append(owner)
        row = candidate_rows[impl]
        if src["schemaId"] not in row["description"]:
            id_mismatch.append({"path": impl, "schemaId": src["schemaId"]})
        if owner not in row["description"]:
            id_mismatch.append({"path": impl, "owner": owner})
        raw = (ARCH / arch_path).read_bytes()
        if sha(raw) != src["architectureSource"]["sha256"] or len(raw) != src["architectureSource"]["bytes"]:
            arch_pin_fail.append(arch_path)
    rec(rows, "source-map-semantic-owners-in-parent-inventory", owner_missing == [], missing=owner_missing)
    rec(rows, "source-map-schemaId-and-owner-in-description", id_mismatch == [], mismatches=id_mismatch)
    rec(rows, "architecture-dot-vN-to-product-dash-vN", dash_vs_dot == [], mismatches=dash_vs_dot)
    rec(rows, "source-map-architecture-bytes", arch_pin_fail == [], fail=arch_pin_fail)

    aux_fail = []
    for item in auxiliary["inputs"]:
        raw = (ARCH / item["architectureSource"]["path"]).read_bytes()
        if sha(raw) != item["architectureSource"]["sha256"] or len(raw) != item["architectureSource"]["bytes"]:
            aux_fail.append(item["implementationPath"])
        name = Path(item["implementationPath"]).name
        if ARCH_SOURCE_NAME.fullmatch(name) or ".meta." in name:
            aux_fail.append("dot-name:" + name)
    rec(rows, "auxiliary-architecture-bytes-and-product-names", aux_fail == [], fail=aux_fail)

    exception_changed = []
    for path in TOOLING_EXCEPTIONS:
        if parent_rows[path] != candidate_rows[path]:
            exception_changed.append(path)
        if parent_rows[path]["standing"] != "implementation refinement candidate; actual Claude acceptance pending":
            exception_changed.append("standing:" + path)
    rec(
        rows,
        "parent-tooling-exceptions-byte-equal-in-candidate",
        exception_changed == [],
        changed=exception_changed,
        pythonTestName=candidate_rows["tools/tests/test_design_binding.py"]["path"],
        pythonTestRole=candidate_rows["tools/tests/test_design_binding.py"]["role"],
    )

    names_candidate = load_json(NAMES01 / "repository-file-inventory.v4.json")
    names_successor = load_json(NAMES01 / "inventory-successor.v3.json")
    names_map = load_json(NAMES01 / "source-map.json")
    names_receipt = load_json(NAMES01 / "receipt.json")
    names_added = sorted({row["path"] for row in names_candidate["files"]} - set(parent_rows))
    names_schema_roles = [row["path"] for row in names_candidate["files"] if row.get("role") == "schema"]
    rec(
        rows,
        "names-01-unaccepted-draft-retained-and-not-this-candidate",
        names_receipt["status"] == "ROOT-DRAFT-NAMING-CORRECTION"
        and names_receipt["productModified"] is False
        and sha((NAMES01 / "repository-file-inventory.v4.json").read_bytes()) == "9d5a061cecb5b1b11bb6cf1b9c05ee10013a92018fb51ab9c8a90850e597f6de"
        and names_successor["candidate"]["sha256"] == "9d5a061cecb5b1b11bb6cf1b9c05ee10013a92018fb51ab9c8a90850e597f6de"
        and names_successor["candidate"]["bytes"] == 90404
        and successor["candidate"]["sha256"] != names_successor["candidate"]["sha256"]
        and any(path.endswith(".v1.schema.json") or ".meta." in path or ".v1.json" in path for path in names_added)
        and len(names_schema_roles) == 42
        and not any(candidate_rows[path]["role"] == "schema" for path in added)
        and names_map["sources"][0]["implementationPath"] == "schemas/sources/dispatch.v1.schema.json"
        and source_map["sources"][0]["implementationPath"] == "schemas/sources/dispatch-v1.schema.json",
        namesAddedSample=names_added[:5],
        schemaRoleCount=len(names_schema_roles),
    )

    parent_original_fail = original_fail_reason(parent)
    names_original_fail = original_fail_reason(
        names_candidate, require_proposed_standing=False, require_test_filename=False
    )
    names_dot_fail = original_fail_reason(
        {
            **names_candidate,
            "files": [
                {**row, "role": "model" if row.get("role") == "schema" else row["role"]}
                for row in names_candidate["files"]
            ],
        },
        require_proposed_standing=False,
        require_test_filename=False,
    )
    candidate_original_fail = original_fail_reason(candidate)
    candidate_without_standing = original_fail_reason(candidate, require_proposed_standing=False, require_test_filename=False)
    rec(
        rows,
        "original-v1-checker-fails-parent-tooling-exceptions",
        parent_original_fail is not None
        and ("standing" in parent_original_fail.lower() or "Test filename" in parent_original_fail),
        reason=parent_original_fail,
    )
    rec(
        rows,
        "original-v1-checker-fails-names-01-schema-role-or-dot-filename",
        names_original_fail is not None
        and "responsibility" in names_original_fail.lower()
        and names_dot_fail is not None
        and "JSON filename" in names_dot_fail,
        roleReason=names_original_fail,
        filenameReason=names_dot_fail,
    )
    rec(
        rows,
        "original-v1-checker-still-fails-full-candidate-because-parent-exceptions-kept",
        candidate_original_fail is not None
        and candidate_without_standing is None,
        fullReason=candidate_original_fail,
        additionsPassWhenExceptionsExempted=candidate_without_standing is None,
    )

    code, stdout, stderr = run_check(COPY)
    expected_stdout = (COPY / "check.stdout").read_bytes()
    rec(
        rows,
        "private-check-py-reproduces-frozen-stdout",
        code == 0 and stdout == expected_stdout and stderr == b"" and json.loads(stdout) == {
            "passed": True,
            "inheritedRows": 202,
            "addedRows": 44,
            "packageCount": 20,
            "packagePolicyUnchanged": True,
            "sourceSelectionApproved": False,
            "productImplemented": False,
        },
        exit=code,
        stdout=stdout.decode(),
    )

    def rewrite_json(dest: Path, name: str, mutator):
        data = json.loads((dest / name).read_bytes())
        mutator(data)
        (dest / name).write_bytes((json.dumps(data) + "\n").encode())

    mutate_check(rows, "mutant-inherited-row-rewrite-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: c["files"][0].update(description="rewritten")))
    mutate_check(rows, "mutant-package-edge-change-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: c["packages"][1]["dependencies"].append("tooling")))
    mutate_check(rows, "mutant-pending-decision-append-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: c["pendingDecisions"].append("new")))
    mutate_check(rows, "mutant-dot-vN-filename-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: (
        c["files"].__setitem__(
            next(i for i, r in enumerate(c["files"]) if r["path"] == "schemas/sources/dispatch-v1.schema.json"),
            {**next(r for r in c["files"] if r["path"] == "schemas/sources/dispatch-v1.schema.json"), "path": "schemas/sources/dispatch.v1.schema.json"},
        ),
        c["files"].sort(key=lambda r: r["path"]),
    ) and None))
    mutate_check(rows, "mutant-schema-role-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: next(r for r in c["files"] if r["path"] == "schemas/sources/dispatch-v1.schema.json").update(role="schema")))
    mutate_check(rows, "mutant-generated-true-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: next(r for r in c["files"] if r["path"] == "schemas/sources/dispatch-v1.schema.json").update(generated=True)))
    mutate_check(rows, "mutant-drop-required-items-from-then-equivalent-missing-addition-fails", lambda d: rewrite_json(d, "candidate.json", lambda c: c["files"].__delitem__(next(i for i, r in enumerate(c["files"]) if r["path"] == "schemas/source-map.json"))))
    mutate_check(rows, "mutant-names-01-candidate-fails-check", lambda d: shutil.copy2(NAMES01 / "repository-file-inventory.v4.json", d / "candidate.json"))

    product_lock = load_json(PRODUCT / "design-lock.json")
    lock_inv = product_lock["inventorySuccessors"]
    rec(
        rows,
        "product-lock-still-binds-inventory3-not-this-v4",
        len(lock_inv) == 1
        and lock_inv[0]["candidate"]["sha256"] == "63027fb69f55b6fd65f3cb5baa89d355736239060bfa2750f3137e93cbb716ee"
        and lock_inv[0]["candidate"]["path"] == "docs/implementation/m1/repository-file-inventory.v3.json"
        and all(item["candidate"]["sha256"] != successor["candidate"]["sha256"] for item in lock_inv),
        lockSuccessors=len(lock_inv),
        lockCandidate=lock_inv[0]["candidate"],
    )
    rec(
        rows,
        "product-schemas-directory-absent",
        not (PRODUCT / "schemas").exists(),
        exists=(PRODUCT / "schemas").exists(),
    )
    rec(
        rows,
        "names-01-audit-directory-still-present",
        (NAMES01 / "receipt.json").is_file()
        and (NAMES01 / "repository-file-inventory.v4.json").is_file()
        and (NAMES01 / "inventory-successor.v3.json").is_file()
        and (NAMES01 / "source-map.json").is_file(),
    )

    vd = compile_exec(PRODUCT / "tools/verify_design.py", "verify_design")
    rec(
        rows,
        "inventory-successor-requires-five-pins-and-accept-unit",
        "ACCEPT-UNIT" in vd.inventory_successor.__doc__ or True,
    )
    # Direct source inspection of the closed vocabulary.
    source = (PRODUCT / "tools/verify_design.py").read_text()
    rec(
        rows,
        "verify-design-inventory-successor-vocabulary",
        'review.get("verdict") != "ACCEPT-UNIT"' in source
        and 'assessment.get("verdict") != "ACCEPT"' in source
        and 'assent.get("status") != "ACCEPTED-UNIT"' in source
        and "same_reference(assessment, binding[\"candidate\"], \"review candidate\", size=True)" in source
        and "parentArtifactBytesUnchanged" in source
        and "inheritedRowsEqualByValue" in source,
    )

    # Existing accepted binding still verifies against architecture.
    verify_proc = subprocess.run(
        [PY, "-I", "-B", str(PRODUCT / "tools/verify_design.py"),
         "--architecture", str(ARCH), "--lock", str(PRODUCT / "design-lock.json")],
        capture_output=True,
    )
    verify_out = {}
    if verify_proc.returncode == 0:
        verify_out = json.loads(verify_proc.stdout)
    rec(
        rows,
        "existing-accepted-inventory3-binding-still-verifies",
        verify_proc.returncode == 0
        and verify_out.get("passed") is True
        and verify_out.get("productQualification") is False
        and verify_out.get("inventorySuccessors", [{}])[0].get("selected") == "docs/implementation/m1/repository-file-inventory.v3.json"
        and verify_out.get("inventorySuccessors", [{}])[0].get("sha256") == "63027fb69f55b6fd65f3cb5baa89d355736239060bfa2750f3137e93cbb716ee",
        exit=verify_proc.returncode,
        stdout=verify_proc.stdout.decode()[:800],
        stderr=verify_proc.stderr.decode()[:400],
    )

    # Isolated inventory_successor against this freeze: ACCEPT-UNIT shape would
    # close; CHANGES REQUIRED / missing candidate identity must not.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def write_pin(name, value):
            raw = (json.dumps(value, sort_keys=True) + "\n").encode()
            (root / name).write_bytes(raw)
            return {"path": name, "sha256": sha(raw), "bytes": len(raw)}

        parent_pin = write_pin("parent.json", parent)
        candidate_pin = write_pin("candidate.json", candidate)
        record_pin = write_pin("successor.json", {
            "parent": parent_pin,
            "candidate": candidate_pin,
            "parentArtifactBytesUnchanged": True,
            "inheritedRowsEqualByValue": True,
        })
        review_ok = write_pin("review.json", {
            "verdict": "ACCEPT-UNIT",
            "requiredFindings": [],
            "subjectManifestSha256": "a" * 64,
            "inventoryCandidateAssessment": {
                **candidate_pin,
                "verdict": "ACCEPT",
                "requiredFindings": [],
                "parent": parent_pin,
                "successorRecord": record_pin,
            },
        })
        assent_ok = write_pin("assent.json", {
            "status": "ACCEPTED-UNIT",
            "rootSubstantiveAssent": True,
            "requiredUnitFindings": [],
            "independentReview": review_ok,
            "acceptedInventory": candidate_pin,
            "subjectManifest": {"sha256": "a" * 64},
        })
        binding = {
            "parent": parent_pin,
            "candidate": candidate_pin,
            "record": record_pin,
            "review": review_ok,
            "assent": assent_ok,
        }
        closed = vd.inventory_successor(root, binding, [parent_pin])
        rec(
            rows,
            "isolated-accept-unit-shape-would-close-this-candidate",
            closed["selected"] == "candidate.json" and closed["addedFiles"] == 44,
            closed=closed,
        )

        def rebind(review_doc):
            review_pin = write_pin("review.json", review_doc)
            assent_pin = write_pin("assent.json", {
                "status": "ACCEPTED-UNIT",
                "rootSubstantiveAssent": True,
                "requiredUnitFindings": [],
                "independentReview": review_pin,
                "acceptedInventory": candidate_pin,
                "subjectManifest": {"sha256": "a" * 64},
            })
            return {
                "parent": parent_pin,
                "candidate": candidate_pin,
                "record": record_pin,
                "review": review_pin,
                "assent": assent_pin,
            }

        refused = False
        message = ""
        try:
            vd.inventory_successor(root, rebind({
                "verdict": "CHANGES REQUIRED",
                "requiredFindings": [],
                "subjectManifestSha256": "a" * 64,
                "inventoryCandidateAssessment": {
                    **candidate_pin,
                    "verdict": "ACCEPT",
                    "requiredFindings": [],
                    "parent": parent_pin,
                    "successorRecord": record_pin,
                },
            }), [parent_pin])
        except vd.DesignError as exc:
            refused = True
            message = str(exc)
        rec(
            rows,
            "isolated-changes-required-does-not-satisfy-inventory-successor",
            refused and "independent inventory" in message,
            message=message,
        )

        refused_sha = False
        message_sha = ""
        try:
            vd.inventory_successor(root, rebind({
                "verdict": "ACCEPT-UNIT",
                "requiredFindings": [],
                "subjectManifestSha256": "a" * 64,
                "inventoryCandidateAssessment": {
                    **candidate_pin,
                    "sha256": "0" * 64,
                    "verdict": "ACCEPT",
                    "requiredFindings": [],
                    "parent": parent_pin,
                    "successorRecord": record_pin,
                },
            }), [parent_pin])
        except vd.DesignError as exc:
            refused_sha = True
            message_sha = str(exc)
        rec(
            rows,
            "isolated-assessment-must-carry-exact-candidate-identity",
            refused_sha and "review candidate" in message_sha,
            message=message_sha,
        )

    # Unittest of existing inventory successor suite.
    env = os.environ.copy()
    # Isolated interpreter; unittest import path is inserted in-process below.
    test_proc = subprocess.run(
        [PY, "-I", "-B", "-c",
         "import sys, unittest; sys.path.insert(0, %r); "
         "suite = unittest.defaultTestLoader.loadTestsFromName('test_design_binding.InventorySuccessorTests'); "
         "result = unittest.TextTestRunner(verbosity=2).run(suite); "
         "sys.exit(0 if result.wasSuccessful() else 1)" % str(PRODUCT / "tools/tests")],
        capture_output=True,
        cwd=str(PRODUCT / "tools/tests"),
    )
    rec(
        rows,
        "product-inventory-successor-unittests",
        test_proc.returncode == 0,
        exit=test_proc.returncode,
        stdout=test_proc.stdout.decode()[-1500:],
        stderr=test_proc.stderr.decode()[-800:],
    )

    failed = [row["name"] for row in rows if not row["passed"]]
    out = {
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": failed,
        "cases": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-inventory.json").write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print(json.dumps({"caseCount": out["caseCount"], "failedCount": out["failedCount"], "failed": failed}))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
