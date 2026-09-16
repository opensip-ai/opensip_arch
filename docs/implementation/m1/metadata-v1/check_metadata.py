"""Reference validation of the scoped metadata correction; no product qualification."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from referencing import Registry, Resource
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def load(arch):
    sources = read(HERE / "sources.json")
    def checked(pin):
        raw = (arch / pin["path"]).read_bytes()
        assert len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"], pin["path"]
        return raw
    lexical = sources["lexicalReference"]
    checked(lexical)
    spec = importlib.util.spec_from_file_location("canonical_reference", arch / lexical["path"])
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    documents = {}
    for pin in sources["schemas"]:
        schema = reference.parse(checked(pin))
        Draft202012Validator.check_schema(schema)
        assert schema["$id"] not in documents
        documents[schema["$id"]] = schema
    # No retrieval hook: any unregistered document reference refuses offline.
    registry = Registry().with_resources((key, Resource.from_contents(schema)) for key, schema in documents.items())
    return reference, registry, documents


def admit(reference, registry, envelope_schema, value, catalogue, build):
    reference.validate(envelope_schema, value, registry)
    exit_codes = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
    assert value["exitCode"] == exit_codes[value["termination"]["class"]], "termination/exit mismatch"
    if value["kind"] != "meta":
        return
    meta = value["meta"]
    if meta["command"] == "help":
        selected = catalogue if meta["topic"] is None else [row for row in catalogue if row["name"] == meta["topic"]]
        assert selected and reference.equal_typed(meta["commands"], selected), "metadata differs from compiled catalogue"
    else:
        expected = {"command": "version", **{key: val for key, val in build.items() if key != "schemaVersion"}}
        assert reference.equal_typed(meta, expected), "metadata differs from admitted compiled build selection"


def compatibility(arch, current):
    base = read(arch / "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json")
    restored = copy.deepcopy(current)
    for key in ("$id", "title", "description"):
        restored[key] = base[key]
    restored["properties"]["schemaMajor"]["const"] = 3
    restored["properties"]["kind"]["enum"].remove("meta")
    del restored["properties"]["meta"]
    restored["properties"]["errors"]["minItems"] = 1
    assert len(restored["allOf"]) == len(base["allOf"]) + 2
    restored["allOf"] = restored["allOf"][:-2]
    assert restored == base, "unexpected existing envelope constraint change"
    allowed = {"schemaFamily", "schemaMajor", "kind", "requestId", "clientCorrelationId", "termination", "exitCode", "meta"}
    excluded = {row["required"][0] for row in current["allOf"][-2]["then"]["not"]["anyOf"]}
    assert excluded == set(current["properties"]) - allowed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    args = parser.parse_args()
    reference, registry, documents = load(args.architecture)
    eid = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"
    envelope = documents[eid]
    compatibility(args.architecture, envelope)
    fixture = read(HERE / "fixtures.json")
    metadata_id = "urn:opensip:product-v1:workflows:metadata:1"
    reference.validate({"$ref": metadata_id + "#/$defs/BuildMetadataV1"}, fixture["build"], registry)
    catalogue_names = [row["name"] for row in fixture["catalogue"]]
    assert catalogue_names == sorted(set(catalogue_names))
    results = []
    for case in fixture["cases"]:
        reason = None
        try:
            admit(reference, registry, envelope, case["value"], fixture["catalogue"], fixture["build"])
        except Exception as exc:
            # Record exact exception; unexpected exceptions are not accepted refusals.
            from jsonschema import ValidationError
            if not isinstance(exc, (ValidationError, AssertionError, reference.AdmissionError)):
                raise
            reason = type(exc).__name__ + ": " + str(exc).splitlines()[0]
        assert (reason is None) == case["accepted"], (case["id"], reason)
        results.append({"id": case["id"], "accepted": reason is None, "reason": reason})
    # All old valid branches still select major3, and reject any major4 wire value.
    old = documents[eid.replace(":4", ":3")]
    for case in fixture["cases"]:
        if case["accepted"]:
            assert not reference.ExactValidator(old, registry=registry).is_valid(case["value"])
    inventory = read(HERE / "command-inventory.v4.json")
    reference.validate(documents["urn:opensip:product-v1:workflows:evaluator3:command-inventory:4"], inventory, registry)
    coverage = read(HERE / "implementation-coverage.v2.json")
    for group in coverage["groups"].values():
        for row in group:
            source = row.get("source", {})
            if source.get("key") == "commands":
                selected = inventory
                for key in source["selector"].strip("/").split("/"):
                    selected = selected[int(key)] if isinstance(selected, list) else selected[key]
                assert hashlib.sha256(reference.canonical(selected)).hexdigest() == source["valueSha256"]
    # Selected old failure behavior survives unchanged after the major advance.
    format_failure = next(case["value"] for case in fixture["cases"] if case["id"] == "completion-format-refusal")
    reference.validate(old, {**format_failure, "schemaMajor": 3}, registry)
    assert not reference.ExactValidator(envelope, registry=registry).is_valid({**format_failure, "schemaMajor": 3})
    # Private record cannot smuggle host/signature identities or development closures.
    build_schema = {"$ref": metadata_id + "#/$defs/BuildMetadataV1"}
    for field, value in [("hostClosureId", "closure2:" + "a" * 64), ("signatureVerified", True), ("closureIds", ["closure2:" + "a" * 64]), ("schemaVersion", True)]:
        assert not reference.ExactValidator(build_schema, registry=registry).is_valid({**fixture["build"], field: value})
    for version in ("1.2.3", "1.2.3-alpha.0", "0.0.0-dev+build.17", "12.0.3-0a.1-2"):
        reference.validate(build_schema, {**fixture["build"], "hostRelease": version}, registry)
    release_shape = {**fixture["build"], "buildChannel": "release", "closureIds": ["closure2:" + "1" * 64, "closure2:" + "2" * 64]}
    reference.validate(build_schema, release_shape, registry)
    assert not reference.ExactValidator(build_schema, registry=registry).is_valid({**release_shape, "closureIds": list(reversed(release_shape["closureIds"]))})
    assert not reference.ExactValidator(build_schema, registry=registry).is_valid({**release_shape, "closureIds": release_shape["closureIds"] * 2})
    # Inventory compatibility: only two command rows and the JSON renderer change.
    base_inventory = read(args.architecture / "docs/coop/design-corrections/workflows/command-inventory.v3.json")
    restored_inventory = copy.deepcopy(inventory)
    restored_inventory["schemaMajor"] = 3
    restored_inventory["standing"] = base_inventory["standing"]
    for command in restored_inventory["commands"]:
        if command["name"] in ("help", "version"):
            del command["metaDispatch"]
        if command["name"] == "version":
            command["parityFields"].remove("build-channel")
    restored_inventory["renderers"][1] = base_inventory["renderers"][1]
    assert restored_inventory == base_inventory
    for command in inventory["commands"]:
        if command["name"] in ("help", "version"):
            assert set(command["metaDispatch"]["paritySelectors"]) == set(command["parityFields"])
    lexical_negatives = [b'{"schemaMajor":4.0}', b'{"schemaMajor":4e0}', b'{"schemaMajor":-0}', b'{"x":1,"x":2}', b'{"x":"\\ud800"}']
    for raw in lexical_negatives:
        try:
            reference.parse(raw)
        except reference.AdmissionError:
            pass
        else:
            raise AssertionError("forbidden lexical input accepted")
    print(json.dumps({"passed": True, "schemasVerified": len(documents), "cases": results, "lexicalNegatives": len(lexical_negatives), "envelopeCompatibility": True, "productQualification": False}, indent=2))


if __name__ == "__main__":
    main()
