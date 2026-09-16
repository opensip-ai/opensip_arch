#!/usr/bin/env python3
"""Check source-bound planning coverage and render its owning document.

This validates design bookkeeping, not product behavior or qualification.
Use --source for the materialized selected source snapshot. --write changes only
the two generated sections in the implementation plan; no product scaffolding.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs/v2/architecture"
PLAN = ARCH / "implementation-boundaries-and-build-plan.md"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode())


def load(path):
    return json.loads(path.read_text())


def section_values(text):
    lines = text.splitlines(keepends=True)
    heads = [i for i, line in enumerate(lines) if line.startswith("## ")]
    return [(i + 1, {"heading": lines[start].strip(), "firstLine": start + 1,
                     "lastLine": end}, "".join(lines[start:end]))
            for i, (start, end) in enumerate(zip(heads, heads[1:] + [len(lines)]))]


def expected_groups(sources):
    result = {}

    def rows(group, key, values, id_fn, prefix):
        result[group] = {id_fn(v): (key, f"{prefix}/{i}", v)
                         for i, v in enumerate(values)}

    commands = sources["commands"]
    rows("commands", "commands", commands["commands"], lambda x: x["name"], "/commands")
    rows("sharedFlags", "commands", commands["sharedFlags"], lambda x: x["flag"], "/sharedFlags")
    rows("renderers", "commands", commands["renderers"], lambda x: x["format"], "/renderers")
    rows("workflowGoldens", "commands", commands["goldens"], lambda x: x["id"], "/goldens")
    rows("queryOperations", "query", sources["query"]["$defs"]["Operation"]["enum"],
         lambda x: x, "/$defs/Operation/enum")
    rows("capabilityCells", "nativeMatrix", sources["nativeMatrix"]["cells"],
         lambda x: x["capability"] + "/" + x["mode"], "/cells")
    rows("qualificationGates", "gates", sources["gates"]["items"], lambda x: x["id"], "/items")
    result["contractSections"] = {}
    for key in ("identity-and-evidence", "security-and-lifecycle", "native-evidence",
                "workflows-and-surfaces", "admission-and-qualification"):
        for i, selector, value in section_values(sources[key]):
            result["contractSections"][key + ":" + str(i)] = (key, selector, value)
    result["fallowConstraints"] = {}
    for line in sources["sourceMap"].splitlines():
        if re.match(r"\| FW-\d\d ", line):
            result["fallowConstraints"][re.search(r"FW-\d\d", line)[0]] = (
                "sourceMap", {"lineText": line}, line)
    result["hydraProposals"] = {}
    for line in sources["hydra"].splitlines():
        match = re.match(r"\| ([1-8])\. ", line)
        if match:
            result["hydraProposals"]["HYDRA-" + match[1]] = (
                "hydra", {"lineText": line}, line)
    report = sources["report"]
    heads = list(re.finditer(r"^### (R\d\d) — (.+)$", report, re.M))
    result["reportFeatures"] = {}
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else report.index(
            "\n## Proposed implementation owners", head.end())
        result["reportFeatures"][head[1]] = (
            "report", {"feature": head[1]}, report[head.start():end])
    return result


def validate_coverage(data, sources, inventory):
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1,
            "Unknown coverage version")
    expected = expected_groups(sources)
    require(set(data["groups"]) == set(expected), "Coverage group mismatch")
    files = {r["path"]: r for r in inventory["files"]}
    paths = set(files)
    require(data["milestoneOrder"] == [f"M{i}" for i in range(7)],
            "Milestone prerequisite order changed")
    delivery_groups = {"commands", "queryOperations", "renderers", "capabilityCells",
                       "workflowGoldens"}
    module_first = data["moduleFirstMilestone"]
    delivery_owners = {owner for group in delivery_groups for row in data["groups"][group]
                       for owner in row["owners"]}
    require(set(module_first) == delivery_owners
            and all(m in data["milestoneOrder"] for m in module_first.values()),
            "Missing/extra module milestone prerequisite")
    issues = {r["id"] for r in data["reviewIssues"]}
    for group, expected_rows in expected.items():
        rows = data["groups"][group]
        require(len(rows) == len({r["id"] for r in rows}), "Duplicate mapping: " + group)
        require({r["id"] for r in rows} == set(expected_rows),
                "Missing/extra source mapping: " + group)
        for row in rows:
            key, selector, value = expected_rows[row["id"]]
            require(row["source"] == {"key": key, "selector": selector,
                                      "valueSha256": digest(value)},
                    "Source selector/value drift: " + row["id"])
            require(row["milestone"] in {f"M{i}" for i in range(7)}, "Invalid milestone")
            require(row["owners"] and set(row["owners"]) <= paths,
                    "Missing inventory owner: " + row["id"])
            if group in {"commands", "queryOperations", "renderers"}:
                require(all(files[p]["role"] != "documentation" for p in row["owners"]),
                        "Runtime responsibility assigned to documentation: " + row["id"])
            if group in delivery_groups:
                require(all(row["milestone"] >= module_first[p] for p in row["owners"]),
                        "Delivery precedes module prerequisite: " + row["id"])
            verification = row["verification"]
            require(verification["owner"] in paths and verification["method"].strip(),
                    "Missing verification responsibility: " + row["id"])
            require(verification["standing"] == "not-executed",
                    "Planning cannot assert execution: " + row["id"])
            if verification["kind"] == "planned-behavioral-test":
                require(files[verification["owner"]]["role"] == "test",
                        "Behavioral verification requires a test owner: " + row["id"])
            elif files[verification["owner"]]["role"] == "documentation":
                require(verification["kind"] in {"qualification-harness-specification",
                        "section-owner-routing", "independent-review-scope"},
                        "Documentation is not an executable verification owner: " + row["id"])
            require(set(row["reviewIssues"]) <= issues, "Untracked review issue")
            if group == "capabilityCells":
                for field in ("state", "limitations", "deficiency", "corpusCases"):
                    require(row[field] == value[field], "Native matrix metadata drift")
                require(row["platformFamilies"] == sources["nativeMatrix"]["platformFamilies"],
                        "Missing platform population")
                require(row["qualificationMilestone"] == "M6", "Qualification milestone")
            if group == "commands":
                for field in ("requestClass", "authorizationClass", "formats", "parityFields"):
                    require(row[field] == value[field], "Command metadata drift")
            if group == "qualificationGates":
                for field in ("harness", "thresholdDisposition", "productExpansion"):
                    require(row[field] == value[field], "Gate metadata drift")
                require(row["qualificationMilestone"] == "M6", "Qualification milestone")
                require(row["inheritedAcceptance"] == value["acceptance"]
                        and row["gateOwner"] == value["owner"], "Gate standing/owner drift")
            if group == "workflowGoldens":
                require(row["command"] == value["command"]
                        and row["sourceClass"] == value["class"]
                        and row["sourceExitCode"] == value["exitCode"], "Golden source drift")
    renderer_milestones = {r["id"]: r["milestone"] for r in data["groups"]["renderers"]}
    command_milestones = {r["id"]: r["milestone"] for r in data["groups"]["commands"]}
    for row in data["groups"]["commands"]:
        require(all(row["milestone"] >= renderer_milestones[f] for f in row["formats"]),
                "Command delivery precedes an advertised renderer: " + row["id"])
    for row in data["groups"]["workflowGoldens"]:
        require(row["milestone"] >= command_milestones[row["command"]],
                "Golden delivery precedes its command: " + row["id"])
    return expected


def validate_recovery(data, inventory, security_schema):
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1,
            "Unknown recovery plan version")
    schema = data["recordSchema"]
    binding = data["storeGenerationBindingSchema"]
    require(binding["additionalProperties"] is False
            and set(binding["required"]) == set(binding["properties"])
            == {"schemaVersion", "namespaceId", "storeInstanceId", "storeGeneration", "stateSchema"},
            "Private store binding is not the closed lifecycle-linked record")
    require(binding["properties"]["storeGeneration"] == security_schema["$defs"]["I64NonNegative"]
            and binding["properties"]["stateSchema"]["enum"] == security_schema["$defs"]["StateSchema"]["enum"],
            "Private store binding widens the admitted lifecycle domain")
    require(schema["additionalProperties"] is False, "Recovery record must be closed")
    require(set(schema["required"]) == set(schema["properties"]) == set(data["fieldKinds"]),
            "Recovery fields not accounted")
    require(len(schema["required"]) == len(set(schema["required"])), "Duplicate required field")
    require(schema["properties"]["journalSeq"]["maximum"] == 9007199254740990,
            "Ordinary SEAL may not use reserved terminal slot")
    require(schema["properties"]["commitSequence"]["type"] == "string",
            "Private SQL uint64 binding must preserve exact decimal")
    for key in [data["primaryKey"], *data["uniqueKeys"]]:
        require(key and set(key) <= set(schema["required"]), "Invalid recovery key")
    cases = data["cases"]
    require([c["id"] for c in cases] == [f"F{i:02}" for i in range(54)],
            "Recovery checkpoint missing/duplicate/out of order")
    paths = {r["path"] for r in inventory["files"]}
    for case in cases:
        require(case["executionStanding"] == "not-executed", "Unexecuted crash plan only")
        require(case["verificationOwner"] in paths and case["expectedBehavior"].strip(),
                "Missing crash verification owner/behavior")


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_coverage(data):
    lines = ["<!-- BEGIN GENERATED IMPLEMENTATION COVERAGE -->", "",
             "| Source population | Mapped entries | Standing |", "|---|---:|---|"]
    for key, rows in data["groups"].items():
        lines.append(f"| `{key}` | {len(rows)} | Ownership/verification routing; not executed |")
    lines += ["", "### Command routing", "",
              "| Command | Milestone | Main owner |", "|---|---|---|"]
    for r in data["groups"]["commands"]:
        lines.append(f"| `{r['id']}` | {r['milestone']} | " +
                     ", ".join(f"`{p}`" for p in r["owners"]) + " |")
    lines += ["", "### Qualification routing", "",
              "Every gate still requires actual M6 qualification. Earlier milestones name",
              "the implementation owner; source thresholds and full-product expansion stay",
              "in the pinned gate account and the machine-readable mapping.", "",
              "| Gate | Implementation milestone | Main owners |", "|---|---|---|"]
    for r in data["groups"]["qualificationGates"]:
        lines.append(f"| {r['id']} | {r['milestone']} | " +
                     ", ".join(f"`{p}`" for p in r["owners"]) + " |")
    lines += ["", "<!-- END GENERATED IMPLEMENTATION COVERAGE -->"]
    return "\n".join(lines)


def render_recovery(data):
    lines = ["<!-- BEGIN GENERATED COMMIT RECOVERY -->", "",
             "| Private field | Representation | Exact binding |", "|---|---|---|"]
    for name, prop in data["recordSchema"]["properties"].items():
        lines.append(f"| `{name}` | `{data['fieldKinds'][name]}` | {cell(prop['description'])} |")
    lines += ["", "### Ordered failure matrix", "",
              "Conclusions below are internal scenario expectations, not new public D9",
              "codes. An unreadable or contradictory observation always prevents an",
              "uncommitted/committed conclusion. A missing receipt alone is not terminal",
              "absence: that requires settled+refused and both receipt and association",
              "absent in one coherent snapshot. No crash case has been executed.", "",
              "| Case / interruption | Possible stored state | Expected conclusion and action |",
              "|---|---|---|"]
    for c in data["cases"]:
        lines.append(f"| {c['id']} — {cell(c['checkpoint'])} | {cell(c['possibleStoredState'])} | "
                     f"{c['initialConclusion']}: {cell(c['expectedBehavior'])} |")
    lines += ["", "<!-- END GENERATED COMMIT RECOVERY -->"]
    return "\n".join(lines)


def replace_section(text, name, rendered):
    start, end = f"<!-- BEGIN GENERATED {name} -->", f"<!-- END GENERATED {name} -->"
    require(text.count(start) == text.count(end) == 1, "Missing/duplicate generated markers")
    a, b = text.index(start), text.index(end)
    require(a < b, "Reversed generated markers")
    return text[:a] + rendered + text[b + len(end):]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    coverage = load(ARCH / "implementation-coverage.v1.json")
    manifest_bytes = (ROOT / coverage["subjectManifest"]).read_bytes()
    require(sha(manifest_bytes) == coverage["subjectManifestSha256"], "Subject manifest mismatch")
    members = {r["path"]: r for r in json.loads(manifest_bytes)["files"]}
    sources = {}
    for key, record in coverage["sources"].items():
        working = record.get("location") == "working-tree"
        data = ((ROOT if working else args.source) / record["path"]).read_bytes()
        require(sha(data) == record["sha256"] and len(data) == record["bytes"],
                "Planning source changed: " + key)
        if not working:
            require(record == members[record["path"]], "Source not bound by selected input manifest")
        sources[key] = json.loads(data) if record["path"].endswith(".json") else data.decode()
    inventory = load(ARCH / "repository-file-inventory.v1.json")
    validate_coverage(coverage, sources, inventory)
    recovery = load(ARCH / "commit-recovery-plan.v1.json")
    validate_recovery(recovery, inventory, sources["securitySchema"])
    original = PLAN.read_text()
    expected = replace_section(original, "IMPLEMENTATION COVERAGE", render_coverage(coverage))
    expected = replace_section(expected, "COMMIT RECOVERY", render_recovery(recovery))
    if args.write:
        PLAN.write_text(expected)
    else:
        require(original == expected, "Generated plan differs; run with --write")
    count = sum(len(rows) for rows in coverage["groups"].values())
    print(f"PASS: {count} source-bound mappings, 54 planned failure cases, private schema, owners and generated plan")


if __name__ == "__main__":
    main()
