"""Check proposed source joins without fabricating or applying an approval.

The actual base lock is verified separately. The low-level generation preflight
then checks a temporary proposed materialization; its success is not source
acceptance. No product file is written and no schema implementation is executed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(architecture, product, unit):
    spec = importlib.util.spec_from_file_location("design_verifier", unit / "reference-tools/verify_design.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    lock = read(unit / "base-design-lock.json")
    for row in read(unit / "base-snapshot-provenance.json")["files"]:
        snapshot = unit / row["snapshot"]
        assert snapshot.stat().st_size == row["bytes"] and digest(snapshot) == row["sha256"]
    base = verifier.verify(architecture, lock)
    assert base["passed"]
    rows = read(unit / "source-map.json")["sources"]
    assert len(rows) == 40
    assert len({r["schemaId"] for r in rows}) == len(rows)
    assert len({r["implementationPath"] for r in rows}) == len(rows)
    schemas = {}
    for row in rows:
        raw = verifier.pinned_bytes(architecture, row["architectureSource"])
        doc = verifier.decode(raw)
        assert doc["$id"] == row["schemaId"]
        assert row["profile"] == "opensip-exact-schema-reference-1"
        assert type(row["declaredMajor"]) is int and row["declaredMajor"] > 0
        schemas[row["schemaId"]] = doc
    current = read(unit / "current-dispatch.json")["currentSources"]
    assert len(current) == 14 and len({r["schemaId"] for r in current}) == 14
    by_id = {r["schemaId"]: r for r in rows}
    for row in current:
        assert row["architectureSource"] == by_id[row["schemaId"]]["architectureSource"]
    auxiliaries = read(unit / "auxiliary-input-map.json")["inputs"]
    assert len(auxiliaries) == 3
    assert len({r["implementationPath"] for r in auxiliaries}) == 3
    assert not {r["implementationPath"] for r in auxiliaries} & {r["implementationPath"] for r in rows}
    for row in auxiliaries:
        verifier.pinned_bytes(architecture, row["architectureSource"])
    inventory = read(architecture / lock["inventorySuccessors"][-1]["candidate"]["path"])
    paths = {r["path"] for r in inventory["files"]}
    owners = read(unit / "semantic-owner-joins.json")["rows"]
    assert len(owners) == 40 and {r["schemaId"] for r in owners} == set(by_id)
    for row in owners:
        assert row["semanticValidatorOwner"] == by_id[row["schemaId"]]["semanticValidatorOwner"]
        for owner in [row["semanticValidatorOwner"], *row.get("requiredOwnerJoins", [])]:
            assert owner in paths, owner
    adapter_spec = importlib.util.spec_from_file_location(
        "generator_adapter", unit / "reference-tools/generator_adapter.py")
    adapter = importlib.util.module_from_spec(adapter_spec)
    adapter_spec.loader.exec_module(adapter)
    options = read(unit / "generation-options.json")
    generation_map = read(unit / "generation-source-map.json")
    basis_fields = set(rows[0])
    assert [{key: row[key] for key in basis_fields} for row in generation_map["sources"]] == rows
    generator_sources = {}
    for row in rows:
        raw = verifier.pinned_bytes(architecture, row["architectureSource"])
        registered = {key: row[key] for key in ["schemaId", "declaredMajor", "profile", "semanticValidatorOwner"]}
        registered.update(sourcePath=row["implementationPath"], sourceSha256=row["architectureSource"]["sha256"])
        generator_sources[row["schemaId"]] = (registered, raw, schemas[row["schemaId"]])
    adapter.validate_options(options, generator_sources)
    adapter.validate_source_map(generation_map, generator_sources, options)
    assert len(options["entryPoints"]) == 857 and len(options["sourceMappings"]) == 40
    proposed = read(unit / ("successor.json" if (unit / "successor.json").exists() else "draft-successor-inputs.json"))
    accepted = {}
    for name in ["sourceManifest", "applicationManifest"]:
        for row in read(architecture / lock["approvals"][name]["path"])["files"]:
            accepted[row["path"]] = {key: row[key] for key in ["path", "sha256", "bytes"]}
    for binding in lock["inventorySuccessors"]:
        accepted[binding["candidate"]["path"]] = binding["candidate"]
    for binding in lock["contractSuccessors"]:
        for row in read(architecture / binding["subjectManifest"]["path"])["files"]:
            accepted[row["path"]] = row
    for row in proposed["parents"]:
        assert accepted[row["path"]] == row
        verifier.pinned_bytes(architecture, row)
    for override in proposed["passageOverrides"]:
        raw = verifier.pinned_bytes(architecture, override["parent"])
        assert verifier.selected_passage(raw, override["selector"]) == override["before"]
        assert override["before"] != override["after"]
    scoped = read(unit / "scoped-owner-succession.json")
    interruption = read(unit / scoped["interruptionPassages"])["overrides"]
    assert len(interruption) == 3
    for override in interruption:
        parent = accepted[override["source"]]
        assert parent["sha256"] == override["sourceSha256"]
        lines = verifier.pinned_bytes(architecture, parent).decode().splitlines()
        span = override["selector"]
        assert 1 <= span["startLine"] <= span["endLine"] <= len(lines)
        assert "\n".join(lines[span["startLine"] - 1:span["endLine"]]) == override["before"]
    for override in read(unit / scoped["reportPassages"])["overrides"]:
        parent = accepted[override["path"]]
        raw = verifier.pinned_bytes(architecture, parent)
        assert verifier.selected_passage(raw, {"line": override["line"]}) == override["before"]
    old = read(architecture / "docs/coop/artifacts/d9-exit-contract.v1.14.json")
    new = read(unit / "reference/composed-owners/d9-exit-contract.proposed.v1.15.json")
    assert set(new) - set(old) == {"jointOutputSuccession"}
    changed = {key for key in old if old[key] != new[key]}
    assert changed == {"invariants", "purpose", "status", "supersedes", "version"}
    assert len(old["invariants"]) == len(new["invariants"])
    assert [i for i, (a, b) in enumerate(zip(old["invariants"], new["invariants"])) if a != b] == [1]
    assert new["invariants"][1]["text"] == proposed["passageOverrides"][0]["after"]
    profile = read(unit / "report-codec-profile.json")
    report = by_id[profile["schemaId"]]
    assert profile["rawSchemaSha256"] == report["architectureSource"]["sha256"]
    assert profile["reportRoot"] == profile["schemaId"] + "#"
    budget = read(unit / "evidence/joint-budget-derivation.json")
    depth = read(unit / "evidence/joint-depth-derivation.json")
    assert profile["documentMaxBytes"] == budget["documentMaxBytes"] == 27829365
    assert profile["maxContainerDepth"] == depth["documentMaxContainerDepth"] == 39
    assert budget["envelopeMaxCanonicalBytes"] == 4194304
    pins = read(unit / "evidence-pins.json")
    for row in [*pins["reviews"], *pins["checkpoints"]]:
        verifier.pinned_bytes(architecture, row)
    planning_spec = importlib.util.spec_from_file_location(
        "planning_validator", unit / "reference-tools/check_implementation_planning.py")
    planning = importlib.util.module_from_spec(planning_spec)
    planning_spec.loader.exec_module(planning)
    coverage = read(unit / "implementation-coverage.v4.json")
    composition = read(unit / "coverage-composition.json")
    prerequisite = verifier.decode(verifier.pinned_bytes(architecture, composition["base"]))
    predecessor = read(architecture / "docs/implementation/m1/metadata-v2/implementation-coverage.v2.json")
    expected_prerequisite = copy.deepcopy(predecessor)
    expected_prerequisite["moduleFirstMilestone"]["crates/reporting/src/assets.rs"] = "M1"
    assert prerequisite == expected_prerequisite
    coverage_sources = {}
    for key, row in coverage["sources"].items():
        source = architecture / row["path"]
        assert digest(source) == row["sha256"]
        coverage_sources[key] = read(source) if source.suffix == ".json" else source.read_text()
    planning.validate_coverage(coverage, coverage_sources, inventory)
    assert all(row["verification"]["standing"] == "not-executed"
               for group in coverage["groups"].values() for row in group)
    stale = copy.deepcopy(coverage)
    stale["groups"]["commands"][0]["source"] = predecessor["groups"]["commands"][0]["source"]
    try:
        planning.validate_coverage(stale, coverage_sources, inventory)
    except ValueError as exc:
        assert "Source selector/value drift" in str(exc)
    else:
        raise AssertionError("Stale command coverage binding accepted")
    absent = copy.deepcopy(coverage)
    del absent["moduleFirstMilestone"]["crates/reporting/src/assets.rs"]
    try:
        planning.validate_coverage(absent, coverage_sources, inventory)
    except ValueError as exc:
        assert "Missing/extra module milestone prerequisite" in str(exc)
    else:
        raise AssertionError("Missing assets prerequisite accepted")
    # This isolated call checks candidate mapping/registry coherence. Its input
    # map is explicitly proposed, not a synthetic accepted design lock.
    with tempfile.TemporaryDirectory(prefix="opensip-source-selection-") as tmp:
        staged = Path(tmp)
        (staged / "schemas").mkdir()
        (staged / "schemas/source-map.json").write_bytes((unit / "generation-source-map.json").read_bytes())
        registry = []
        for row in rows:
            path = staged / row["implementationPath"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(verifier.pinned_bytes(architecture, row["architectureSource"]))
            registry.append({key: row[key] for key in ["schemaId", "declaredMajor", "profile", "semanticValidatorOwner"]}
                            | {"sourcePath": row["implementationPath"], "sourceSha256": row["architectureSource"]["sha256"]})
        (staged / "schemas/registry.json").write_text(json.dumps({"schemaVersion": 1, "sources": registry}))
        candidate_pins = {r["architectureSource"]["path"]: r["architectureSource"] for r in rows}
        result = verifier.generation_sources(architecture, staged, candidate_pins)
        assert result["sourcesVerified"] == 40
        # A candidate cannot pass with the actual accepted map before approval.
        try:
            verifier.generation_sources(architecture, staged, accepted)
        except verifier.DesignError as exc:
            assert "not selected by accepted design" in str(exc)
        else:
            raise AssertionError("Unapproved source entered accepted base")
        # A copied file drift is refused even with the proposed candidate map.
        path.write_bytes(path.read_bytes() + b"\n")
        try:
            verifier.generation_sources(architecture, staged, candidate_pins)
        except verifier.DesignError as exc:
            assert "bytes differ" in str(exc)
        else:
            raise AssertionError("Materialized source drift accepted")
    return {"passed": True, "baseInputsVerified": base["inputsVerified"],
            "proposedSources": len(rows), "currentSources": len(current),
            "baseRefusesUnapprovedSelection": True, "materializedDriftRefused": True,
            "planningRowsVerified": sum(len(group) for group in coverage["groups"].values()),
            "staleCoverageAndMissingPrerequisiteRefused": True,
            "selectionApproved": False, "productModified": False,
            "semanticAdmissionOrGeneratorExecuted": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--product", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.architecture.resolve(), args.product.resolve(), Path(__file__).resolve().parent), indent=2))
