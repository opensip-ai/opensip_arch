#!/usr/bin/env python3
"""Validate the proposed product inventory and render its owning design chapter.

--write updates only the generated section in chapter 14. It creates no product
directories or source files. With no flag (or --check), require exact agreement.
"""
import argparse
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs/v2/architecture/repository-file-inventory.v1.json"
CHAPTER = ROOT / "docs/v2/architecture/14-repository-and-module-layout.md"
START = "<!-- BEGIN GENERATED FILE INVENTORY -->"
END = "<!-- END GENERATED FILE INVENTORY -->"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(data):
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1,
            "Unknown inventory version")
    packages = {p["id"]: p for p in data["packages"]}
    require(len(packages) == len(data["packages"]), "Duplicate package IDs")
    paths = set()
    roles = {"manifest", "lockfile", "configuration", "documentation", "entrypoint",
             "public-api", "parser", "composition", "adapter", "model", "codec",
             "algorithm", "validator", "compiler", "builder", "service", "store",
             "factory", "renderer", "template", "view", "style", "registry",
             "fixture", "test"}
    for row in data["files"]:
        path = row["path"]
        p = PurePosixPath(path)
        require(path == str(p) and not p.is_absolute() and ".." not in p.parts
                and "\\" not in path and "\0" not in path, "Noncanonical path: " + path)
        require(path not in paths, "Duplicate path: " + path)
        paths.add(path)
        require(row["package"] in packages, "Unknown package: " + path)
        package_path = packages[row["package"]]["path"]
        require(not package_path or path.startswith(package_path + "/"),
                "File outside its owning package: " + path)
        owners = [p for p in packages.values()
                  if not p["path"] or path.startswith(p["path"] + "/")]
        require(row["package"] == max(owners, key=lambda p: len(p["path"]))["id"],
                "File assigned outside its most specific package: " + path)
        require(row["role"] in roles and bool(row["description"].strip()),
                "Missing or unknown file responsibility: " + path)
        require(type(row["generated"]) is bool and row["standing"] == "proposed",
                "Unexpected file standing: " + path)
        if p.suffix == ".rs":
            require(re.fullmatch(r"[a-z][a-z0-9_]*\.rs", p.name), "Rust filename: " + path)
        if p.suffix == ".ts":
            require(re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.test)?\.ts", p.name),
                    "TypeScript filename: " + path)
        for folder in p.parts[:-1]:
            require(re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", folder),
                    "Directory naming: " + path)
        if p.suffix == ".json":
            require(re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.schema)?\.json", p.name),
                    "JSON filename: " + path)
        if row["role"] in {"factory", "renderer", "store"}:
            ending = ("_" if p.suffix == ".rs" else "-") + row["role"] + p.suffix
            require(p.name.endswith(ending), "Role suffix mismatch: " + path)
        if p.name.endswith(("_factory.rs", "-factory.ts")):
            require(row["role"] == "factory", "Factory filename has a different role: " + path)
        if row["role"] == "test":
            require(p.name.endswith("_tests.rs") or p.name.endswith(".test.ts"),
                    "Test filename: " + path)
        if row["generated"]:
            require("generated" in p.parts, "Generated file outside generated/: " + path)
    visited, active = set(), set()
    pure_layers = {
        "opensip-contracts": set(),
        "opensip-identity": {"opensip-contracts"},
        "opensip-evaluator": {"opensip-contracts", "opensip-identity"},
    }
    for package_id, allowed in pure_layers.items():
        require(package_id in packages, "Missing pure package: " + package_id)
        require(set(packages[package_id]["dependencies"]) <= allowed,
                "Forbidden pure-package dependency direction: " + package_id)

    def visit(package_id):
        require(package_id in packages, "Unknown dependency: " + package_id)
        require(package_id not in active, "Dependency cycle: " + package_id)
        if package_id in visited:
            return
        active.add(package_id)
        for dependency in packages[package_id]["dependencies"]:
            visit(dependency)
        active.remove(package_id)
        visited.add(package_id)

    for package_id in packages:
        visit(package_id)
    return packages


def render(data):
    lines = [START, "", "### Proposed package boundaries", "",
             "Package names and dependency edges below are proposals except for the agreed",
             "`opensip-cli` name. Non-Rust group IDs are inventory labels, not selected npm",
             "package names. Dependencies list proposed direct Rust source edges;",
             "generated-schema inputs, process protocols and asset delivery are separate",
             "build/runtime relationships. This table grants no component authority.", "",
             "| Package/group | Directory | Responsibility | Proposed direct dependencies |",
             "|---|---|---|---|"]
    for p in data["packages"]:
        deps = ", ".join("`" + dep + "`" for dep in p["dependencies"]) or "None declared"
        lines.append(f"| `{p['id']}` | `{p['path'] or '.'}/` | {p['purpose']} | {deps} |")
    lines += ["", "### Proposed filenames and responsibilities", "",
              f"The inventory currently contains **{len(data['files'])} proposed files**. Each",
              "row names one target file. Generated rows are owned outputs of schema",
              "generation; their schemas and semantic validators remain distinct owners.",
              "This is a planning inventory, not an instruction to create empty files.", ""]
    for package in data["packages"]:
        rows = [r for r in data["files"] if r["package"] == package["id"]]
        lines += ["#### " + package["id"], "", "| Target path | Role | Contents/responsibility |",
                  "|---|---|---|"]
        for r in rows:
            role = r["role"] + ("; generated" if r["generated"] else "")
            lines.append(f"| `{r['path']}` | {role} | {r['description']} |")
        lines.append("")
    lines += ["### Explicit gaps in this first inventory", ""]
    lines += ["- " + item for item in data["pendingDecisions"]]
    lines += ["", END]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(INVENTORY.read_text())
    validate(data)
    chapter = CHAPTER.read_text()
    require(chapter.count(START) == chapter.count(END) == 1, "Missing/duplicate section markers")
    start = chapter.index(START)
    end = chapter.index(END) + len(END)
    require(start < end, "Reversed section markers")
    expected = chapter[:start] + render(data) + chapter[end:]
    if args.write:
        CHAPTER.write_text(expected)
    else:
        require(chapter == expected, "Chapter differs from inventory; run with --write")
    print(f"PASS: {len(data['files'])} unique paths, naming/ownership checks, acyclic package dependencies, chapter {'rendered' if args.write else 'matches'}")


if __name__ == "__main__":
    main()
