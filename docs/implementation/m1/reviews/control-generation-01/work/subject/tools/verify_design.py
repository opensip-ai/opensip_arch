"""Verify the implementation's pinned design against an explicit checkout.

This developer tool is not an OpenSIP runtime input or product admission API.
The accepted application overlays the frozen source. Dated pending-review fields
in historical manifests do not override the pinned final acceptance evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


class DesignError(ValueError):
    """The selected design cannot be verified."""


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise DesignError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


def relative_file(root, value):
    if not isinstance(value, str) or not value:
        raise DesignError("expected a nonempty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value or any(x in (".", "..") for x in value.split("/")) or "\\" in value:
        raise DesignError(f"noncanonical path: {value}")
    result = root.joinpath(*path.parts)
    if not result.resolve().is_relative_to(root.resolve()) or result.is_symlink() or not result.is_file():
        raise DesignError(f"missing or escaping regular file: {value}")
    return result


def pinned_bytes(root, row):
    if not isinstance(row, dict) or set(row) != {"path", "sha256", "bytes"}:
        raise DesignError("pin must contain exactly path, sha256 and bytes")
    if not isinstance(row["sha256"], str) or len(row["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in row["sha256"]):
        raise DesignError("pin must contain a lowercase SHA-256")
    if type(row["bytes"]) is not int or row["bytes"] < 0:
        raise DesignError("pin byte length must be a nonnegative integer")
    raw = relative_file(root, row["path"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != row["sha256"]:
        raise DesignError(f"design digest mismatch: {row['path']}")
    if len(raw) != row["bytes"]:
        raise DesignError(f"design length mismatch: {row['path']}")
    return raw



def object_value(value, label):
    if not isinstance(value, dict):
        raise DesignError(f"{label} must be an object")
    return value


def same_reference(actual, expected, label, *, size=False):
    actual = object_value(actual, label)
    keys = ("path", "sha256", "bytes") if size else ("path", "sha256")
    if any(actual.get(key) != expected[key] for key in keys):
        raise DesignError(f"{label} names a different subject")


def inventory_successor(architecture, binding, selected_inputs):
    """Verify the bounded, additive inventory successor selected by lock v2.

    The checked-in lock is the trust anchor, not a signature or runtime grant.
    Historical review records are authenticated by exact pins and explicit joins.
    This profile admits additions only; it cannot change package edges or owners.
    """
    fields = {"parent", "candidate", "record", "review", "assent"}
    if not isinstance(binding, dict) or set(binding) != fields:
        raise DesignError("inventory successor requires five closed pin bindings")
    documents = {key: object_value(decode(pinned_bytes(architecture, pin)), key)
                 for key, pin in binding.items()}
    parent_pin = binding["parent"]
    if parent_pin not in selected_inputs:
        raise DesignError("inventory parent is not a selected base input")
    if binding["candidate"]["path"] == parent_pin["path"]:
        raise DesignError("inventory successor must preserve its parent artifact")
    record, review, assent = (documents[key] for key in ("record", "review", "assent"))
    same_reference(record.get("parent"), parent_pin, "successor parent", size=True)
    same_reference(record.get("candidate"), binding["candidate"], "successor candidate", size=True)
    if record.get("parentArtifactBytesUnchanged") is not True or record.get("inheritedRowsEqualByValue") is not True:
        raise DesignError("successor must preserve parent bytes and inherited rows")
    assessment = object_value(review.get("inventoryCandidateAssessment"), "inventory assessment")
    if review.get("verdict") != "ACCEPT-UNIT" or review.get("requiredFindings") != [] or assessment.get("verdict") != "ACCEPT" or assessment.get("requiredFindings") != []:
        raise DesignError("independent inventory acceptance missing or findings remain")
    same_reference(assessment, binding["candidate"], "review candidate", size=True)
    same_reference(assessment.get("parent"), parent_pin, "review parent", size=True)
    same_reference(assessment.get("successorRecord"), binding["record"], "review successor record")
    if assent.get("status") != "ACCEPTED-UNIT" or assent.get("rootSubstantiveAssent") is not True or assent.get("requiredUnitFindings") != []:
        raise DesignError("root inventory assent missing or findings remain")
    same_reference(assent.get("actualClaudeReview"), binding["review"], "root review")
    same_reference(assent.get("acceptedInventory"), binding["candidate"], "root inventory")
    subject = object_value(assent.get("subjectManifest"), "root subject")
    if not isinstance(subject.get("sha256"), str) or subject["sha256"] != review.get("subjectManifestSha256"):
        raise DesignError("root and independent review subjects differ")
    parent, candidate = documents["parent"], documents["candidate"]
    if set(parent) != set(candidate) or any(parent[key] != candidate[key] for key in parent if key not in ("standing", "files")):
        raise DesignError("additive inventory successor changed package or inventory policy")
    def rows(document):
        values = document.get("files")
        if not isinstance(values, list) or not values:
            raise DesignError("inventory files must be a nonempty list")
        result = {}
        for row in values:
            row = object_value(row, "inventory row")
            path = row.get("path")
            if not isinstance(path, str) or not path or path in result:
                raise DesignError("invalid or duplicate inventory path")
            result[path] = row
        return result
    inherited, current = rows(parent), rows(candidate)
    if list(current) != sorted(current) or not set(inherited) < set(current):
        raise DesignError("inventory successor must contain sorted unique additions")
    if any(current.get(path) != row for path, row in inherited.items()):
        raise DesignError("inventory successor changed or removed an inherited row")
    return {"parent": parent_pin["path"], "selected": binding["candidate"]["path"],
            "sha256": binding["candidate"]["sha256"], "addedFiles": len(current) - len(inherited)}



def pin_rows(value, label):
    if not isinstance(value, list) or not value:
        raise DesignError(f"{label} must be a nonempty pin list")
    paths = [object_value(row, label).get("path") for row in value]
    if any(not isinstance(path, str) for path in paths) or paths != sorted(set(paths)):
        raise DesignError(f"{label} paths must be sorted and unique")
    return value


def selected_passage(raw, selector):
    selector = object_value(selector, "passage selector")
    if set(selector) == {"line"}:
        line = selector["line"]
        lines = raw.decode("utf-8").splitlines()
        if type(line) is not int or not 1 <= line <= len(lines):
            raise DesignError("passage line outside document")
        return lines[line - 1]
    if set(selector) != {"jsonPointer"}:
        raise DesignError("unsupported passage selector")
    pointer = selector["jsonPointer"]
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise DesignError("passage pointer must start with slash")
    value = decode(raw)
    for token in pointer[1:].split("/"):
        # RFC6901 escaping; a malformed escape is not another spelling of a key.
        for i, char in enumerate(token):
            if char == "~" and (i + 1 == len(token) or token[i + 1] not in "01"):
                raise DesignError("invalid passage pointer escape")
        key = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not key.isascii() or not key.isdigit() or (len(key) > 1 and key[0] == "0") or int(key) >= len(value):
                raise DesignError("passage array index outside document")
            value = value[int(key)]
        elif isinstance(value, dict) and key in value:
            value = value[key]
        else:
            raise DesignError("passage pointer does not resolve")
    return value


def contract_successor(architecture, binding, accepted):
    """Bind one reviewed contract unit and its exact base passage overrides.

    Its immutable review and root assent authenticate the frozen member set. This
    does not run the reference checker, alter parent files, or grant runtime trust.
    """
    fields = {"record", "subjectManifest", "review", "assent"}
    if not isinstance(binding, dict) or set(binding) != fields:
        raise DesignError("contract successor requires four closed pin bindings")
    documents = {key: object_value(decode(pinned_bytes(architecture, pin)), key)
                 for key, pin in binding.items()}
    review, assent = documents["review"], documents["assent"]
    if review.get("verdict") != "ACCEPT-DESIGN-UNIT" or review.get("requiredFindings") != []:
        raise DesignError("independent contract acceptance missing or findings remain")
    if review.get("subjectManifestSha256") != binding["subjectManifest"]["sha256"]:
        raise DesignError("contract review names a different manifest")
    if assent.get("status") != "ACCEPTED-DESIGN-UNIT" or assent.get("rootSubstantiveAssent") is not True or assent.get("requiredUnitFindings") != []:
        raise DesignError("root contract assent missing or findings remain")
    same_reference(assent.get("subjectManifest"), binding["subjectManifest"], "contract root subject", size=True)
    same_reference(assent.get("actualClaudeReview"), binding["review"], "contract root review", size=True)
    same_reference(assent.get("acceptedSuccessor"), binding["record"], "contract root successor", size=True)
    members = pin_rows(documents["subjectManifest"].get("files"), "contract subject")
    for row in members:
        pinned_bytes(architecture, row)
    member_map = {row["path"]: row for row in members}
    if member_map.get(binding["record"]["path"]) != binding["record"]:
        raise DesignError("successor record is not in the reviewed subject")
    record = documents["record"]
    candidates = pin_rows(record.get("candidates"), "contract candidates")
    if {row["path"] for row in candidates} != set(member_map) - {binding["record"]["path"]}:
        raise DesignError("contract candidates do not cover the reviewed subject")
    for row in candidates:
        if member_map[row["path"]] != row:
            raise DesignError("contract candidate pin differs from reviewed subject")
        pinned_bytes(architecture, row)
    parents = pin_rows(record.get("parents"), "contract parents")
    parent_bytes = {}
    for row in parents:
        selected = accepted.get(row["path"])
        if selected is None or any(selected.get(key) != row.get(key) for key in ("sha256", "bytes")):
            raise DesignError("contract parent is not an accepted base or selected inventory")
        if row["path"] in member_map:
            raise DesignError("contract successor would overwrite its parent")
        parent_bytes[row["path"]] = pinned_bytes(architecture, row)
    if "previousCandidate" in record:
        pinned_bytes(architecture, record["previousCandidate"])
    overrides = record.get("passageOverrides")
    if not isinstance(overrides, list):
        raise DesignError("contract passage overrides must be a list")
    parent_map = {row["path"]: row for row in parents}
    seen = set()
    for override in overrides:
        if not isinstance(override, dict) or set(override) != {"parent", "selector", "before", "after"}:
            raise DesignError("contract passage override has unknown or missing fields")
        parent = object_value(override["parent"], "override parent")
        if parent_map.get(parent.get("path")) != parent:
            raise DesignError("passage override parent is outside the accepted parent set")
        selector_key = (parent["path"], json.dumps(override["selector"], sort_keys=True))
        if selector_key in seen:
            raise DesignError("duplicate passage override")
        seen.add(selector_key)
        before, after = override["before"], override["after"]
        if not isinstance(before, str) or not isinstance(after, str) or not after or before == after:
            raise DesignError("passage override must change one text value")
        if selected_passage(parent_bytes[parent["path"]], override["selector"]) != before:
            raise DesignError("passage override before text differs from accepted parent")
    return {"selected": binding["record"]["path"], "sha256": binding["record"]["sha256"],
            "inputs": candidates, "passageOverrides": overrides}


def verify(architecture: Path, lock: dict) -> dict:
    object_value(lock, "design lock")
    version = lock.get("schemaVersion")
    fields = {"schemaVersion", "architectureRepository", "approvals", "inputs"}
    if type(version) is not int or version not in (1, 2, 3):
        raise DesignError("unsupported design lock")
    if version >= 2:
        fields.add("inventorySuccessor")
    if version == 3:
        fields.add("contractSuccessor")
    if set(lock) != fields:
        raise DesignError("unsupported design lock")
    expected = {"sourceManifest", "applicationManifest", "activation", "applicationReview", "rootAssent", "completion"}
    if not isinstance(lock["approvals"], dict) or set(lock["approvals"]) != expected:
        raise DesignError("incomplete approval bindings")
    approvals = {name: decode(pinned_bytes(architecture, row)) for name, row in lock["approvals"].items()}
    if any(not isinstance(document, dict) for document in approvals.values()):
        raise DesignError("approval documents must be objects")
    manifest = approvals["applicationManifest"]
    activation = approvals["activation"]
    review = approvals["applicationReview"]
    pins = lock["approvals"]
    for actual, expected_ref in ((activation["applicationManifest"], pins["applicationManifest"]), (activation["independentApplicationReview"], pins["applicationReview"]), (manifest["designSubject"], pins["sourceManifest"])):
        same_reference(actual, expected_ref, "approval")
    if review.get("verdict") != "ACCEPT" or review.get("subjectManifestSha256") != pins["applicationManifest"]["sha256"]:
        raise DesignError("application acceptance missing")
    if any(review.get(key) != [] for key in ("newMustIssues", "newShouldIssues")):
        raise DesignError("required application findings remain")
    assent = approvals["rootAssent"]
    if object_value(assent.get("authority"), "root authority").get("rootApplicationAssent") is not True or assent.get("subjectManifestSha256") != pins["applicationManifest"]["sha256"] or object_value(assent.get("review"), "root review").get("sha256") != pins["applicationReview"]["sha256"]:
        raise DesignError("root application assent does not match")
    completion = approvals["completion"]
    if completion.get("designApprovedForImplementation") is not True or completion.get("passed") is not True:
        raise DesignError("design approval is incomplete")
    if completion.get("remainingRequiredDesignFindings", []) != []:
        raise DesignError("required design findings remain")
    for field, key in (("applicationManifest", "applicationManifest"), ("activation", "activation"), ("actualClaudeApplicationReview", "applicationReview"), ("codexApplicationAssent", "rootAssent")):
        same_reference(completion.get(field), pins[key], "completion")
    effective = {}
    for document in (approvals["sourceManifest"], manifest):
        paths = set()
        for row in document["files"]:
            if row["path"] in paths:
                raise DesignError("duplicate manifest path")
            paths.add(row["path"])
            effective[row["path"]] = row
    if not isinstance(lock["inputs"], list):
        raise DesignError("design inputs must be a list")
    paths = [object_value(row, "design input").get("path") for row in lock["inputs"]]
    if any(not isinstance(path, str) for path in paths):
        raise DesignError("design input paths must be strings")
    if not paths or paths != sorted(set(paths)):
        raise DesignError("design inputs must be sorted, unique and nonempty")
    for row in lock["inputs"]:
        if set(row) != {"path", "sha256", "bytes"}:
            raise DesignError("unknown design input field")
        selected = effective.get(row["path"])
        if selected is None or any(selected[k] != row[k] for k in ("sha256", "bytes")):
            raise DesignError(f"input is not selected by accepted application: {row['path']}")
        pinned_bytes(architecture, row)
    result = {"passed": True, "inputsVerified": len(paths), "applicationManifestSha256": pins["applicationManifest"]["sha256"], "productQualification": False}
    if version >= 2:
        result["inventorySuccessor"] = inventory_successor(architecture, lock["inventorySuccessor"], lock["inputs"])
    if version == 3:
        accepted = {**effective, lock["inventorySuccessor"]["candidate"]["path"]: lock["inventorySuccessor"]["candidate"]}
        result["contractSuccessor"] = contract_successor(architecture, lock["contractSuccessor"], accepted)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--lock", type=Path, default=Path(__file__).resolve().parents[1] / "design-lock.json")
    args = parser.parse_args()
    try:
        result = verify(args.architecture.resolve(), decode(args.lock.read_bytes()))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Design verification failed: {exc}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
