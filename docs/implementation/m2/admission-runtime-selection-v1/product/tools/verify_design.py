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


def reviewer_reference(assent, label):
    """Preserve legacy Claude pins; new records use reviewer-neutral attribution.

    Exactly one name is allowed. A duplicate is refused even if both pins agree,
    so a reader cannot select a different review by field precedence. The pin is
    still checked against the lock's exact reviewed bytes by same_reference.
    """
    keys = [key for key in ("actualClaudeReview", "independentReview") if key in assent]
    if len(keys) != 1:
        raise DesignError(label + " requires exactly one review reference")
    return assent[keys[0]]


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
    same_reference(reviewer_reference(assent, "root review"), binding["review"], "root review")
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
    same_reference(reviewer_reference(assent, "contract root review"), binding["review"], "contract root review", size=True)
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


def successor_chain(architecture, lock, effective):
    """Select ordered additive inventory history and reviewed contract units.

    Earlier immutable candidates remain accepted parents. No candidate can
    overwrite earlier selected bytes, and conflicting passage meanings refuse.
    Inventory description inheritance is explicit in the lock and checked by
    stable inventory file path, since sorted additions can change row indexes.
    """
    inventories, contracts = lock['inventorySuccessors'], lock['contractSuccessors']
    if not isinstance(inventories, list) or not inventories or not isinstance(contracts, list) or not contracts:
        raise DesignError('successor chains must be nonempty lists')
    accepted = dict(effective)
    inventory_pins = []
    inventory_results = []
    previous = None
    seen = set()
    for binding in inventories:
        binding = object_value(binding, 'inventory chain binding')
        if previous is not None and binding.get('parent') != previous:
            raise DesignError('inventory chain must extend its immediate predecessor')
        candidate = object_value(binding.get('candidate'), 'inventory chain candidate')
        if not isinstance(candidate.get('path'), str) or not candidate['path']:
            raise DesignError('inventory candidate path must be a nonempty string')
        if candidate.get('path') in accepted or candidate.get('path') in seen:
            raise DesignError('inventory candidate reuses an accepted path')
        parents = lock['inputs'] if previous is None else [previous]
        inventory_results.append(inventory_successor(architecture, binding, parents))
        if previous is None:
            inventory_pins.append(binding['parent'])
        previous = candidate
        inventory_pins.append(candidate)
        accepted[candidate['path']] = candidate
        seen.add(candidate['path'])
    overrides = {}
    contract_results = []
    for binding in contracts:
        result = contract_successor(architecture, binding, accepted)
        members = [binding['record'], *result['inputs']]
        if any(row['path'] in accepted or row['path'] in seen for row in members):
            raise DesignError('contract candidate reuses an accepted path')
        for override in result['passageOverrides']:
            if 'line' in override['selector']:
                try:
                    decode(pinned_bytes(architecture, override['parent']))
                except (ValueError, UnicodeError):
                    pass  # Text documents retain their reviewed line selectors.
                else:
                    raise DesignError('v4 JSON parent passages require JSON Pointer selectors')
            key = (override['parent']['path'], json.dumps(override['selector'], sort_keys=True))
            if key in overrides and overrides[key] != override:
                raise DesignError('conflicting contract passage overrides')
            overrides[key] = override
        for row in members:
            accepted[row['path']] = row
            seen.add(row['path'])
        contract_results.append(result)
    final_pin = inventory_pins[-1]
    final = decode(pinned_bytes(architecture, final_pin))
    final_rows = {row['path']: (index, row) for index, row in enumerate(final['files'])}
    ancestor_pins = {row['path']: row for row in inventory_pins[:-1]}
    inherited = {}
    for override in overrides.values():
        parent = override['parent']
        if parent['path'] not in ancestor_pins:
            continue
        # The initial profile only inherits row descriptions. Any other kind
        # needs an explicit separately reviewed profile instead of guessing.
        selector = override['selector']
        parts = selector.get('jsonPointer', '').split('/')
        if len(parts) != 4 or parts[1] != 'files' or not parts[2].isdigit() or parts[3] != 'description':
            raise DesignError('unsupported inherited inventory passage selector')
        document = decode(pinned_bytes(architecture, ancestor_pins[parent['path']]))
        row = document['files'][int(parts[2])]
        index, target = final_rows[row['path']]
        if target != row:
            raise DesignError('inherited inventory passage row changed')
        projected = {'parent': final_pin, 'selector': {'jsonPointer': f'/files/{index}/description'},
                     'before': override['before'], 'after': override['after']}
        key = (final_pin['path'], json.dumps(projected['selector'], sort_keys=True))
        if key in overrides:
            if overrides[key] != projected:
                raise DesignError('inherited inventory meaning conflicts with direct override')
            continue
        if key in inherited and inherited[key] != projected:
            raise DesignError('inherited inventory passage meanings conflict')
        inherited[key] = projected
    # Canonical order is parent path, then lexicographic selector JSON;
    # /files/10/description therefore sorts before /files/2/description.
    expected_inheritance = [inherited[key] for key in sorted(inherited)]
    if lock['inventoryPassageInheritance'] != expected_inheritance:
        raise DesignError('inventory passage inheritance differs from reviewed ancestor meaning')
    return {'inventorySuccessors': inventory_results, 'contractSuccessors': contract_results,
            'selectedInventory': final_pin, 'inventoryPassageInheritance': expected_inheritance}


def generation_sources(architecture, implementation, accepted):
    """Bind generator schema inputs to a separately verified architecture checkout.

    This read-only developer preflight executes no generator/package code.
    The reviewed checkout/tool is the trust anchor, not these local self hashes.
    Generator options, executable closure and output drift remain separate checks.
    """
    mapping = object_value(decode(relative_file(implementation, 'schemas/source-map.json').read_bytes()), 'source map')
    if set(mapping) != {'schemaVersion', 'sources'} or type(mapping['schemaVersion']) is not int or mapping['schemaVersion'] != 1:
        raise DesignError('unsupported generation source map')
    rows = mapping['sources']
    if not isinstance(rows, list) or not rows:
        raise DesignError('generation sources must be a nonempty list')
    registry = object_value(decode(relative_file(implementation, 'schemas/registry.json').read_bytes()), 'generation registry')
    if type(registry.get('schemaVersion')) is not int or registry['schemaVersion'] != 1 or not isinstance(registry.get('sources'), list):
        raise DesignError('unsupported generation registry sources')
    registered = {}
    for row in registry['sources']:
        row = object_value(row, 'registered generation source')
        path = row.get('sourcePath')
        if not isinstance(path, str) or not path or path in registered:
            raise DesignError('invalid or duplicate registered source path')
        registered[path] = row
    selected = []
    for row in rows:
        row = object_value(row, 'generation source mapping')
        path = row.get('implementationPath')
        if not isinstance(path, str) or not path or path in selected:
            raise DesignError('invalid or duplicate mapped source path')
        selected.append(path)
        pin = object_value(row.get('architectureSource'), 'generation architecture source')
        if not isinstance(pin.get('path'), str):
            raise DesignError('generation architecture source path must be a string')
        expected = accepted.get(pin['path'])
        if expected is None or any(pin.get(key) != expected.get(key) for key in ('path', 'sha256', 'bytes')):
            raise DesignError('generation source is not selected by accepted design')
        raw = pinned_bytes(architecture, pin)
        if relative_file(implementation, path).read_bytes() != raw:
            raise DesignError('generation source bytes differ from accepted architecture')
        source = registered.get(path)
        if source is None or source.get('sourceSha256') != pin['sha256']:
            raise DesignError('generation registry digest differs from accepted source')
        if any(source.get(key) != row.get(key) for key in ('schemaId', 'declaredMajor', 'profile', 'semanticValidatorOwner')):
            raise DesignError('generation source mapping differs from registry owner')
        if object_value(decode(raw), 'generation source document').get('$id') != source.get('schemaId'):
            raise DesignError('generation schema ID differs from accepted source')
    if set(selected) != set(registered):
        raise DesignError('generation source map and registry coverage differ')
    return {'sourcesVerified': len(selected), 'executedGeneratorCode': False,
            'productQualification': False}



def admission_sources(architecture, implementation, accepted):
    """Bind admission-only inputs and current aliases without executing code.

    The complete registry (including aliases) is an accepted architecture input.
    A local rehash cannot grant a different schema or alias current authority.
    Runtime ownership, codec profiles and retained historical joins are separate.
    """
    mapping = object_value(decode(relative_file(implementation, 'schemas/admission-source-map.json').read_bytes()), 'admission source map')
    if set(mapping) != {'schemaVersion', 'registryArchitectureSource', 'sources'} or type(mapping['schemaVersion']) is not int or mapping['schemaVersion'] != 1:
        raise DesignError('unsupported admission source map')
    def selected_bytes(pin):
        pin = object_value(pin, 'admission architecture pin')
        if set(pin) != {'path', 'bytes', 'sha256'} or not isinstance(pin['path'], str):
            raise DesignError('invalid admission architecture pin')
        if accepted.get(pin['path']) != pin:
            raise DesignError('admission source is not selected by accepted design')
        return pinned_bytes(architecture, pin)
    registry_raw = selected_bytes(mapping['registryArchitectureSource'])
    if relative_file(implementation, 'schemas/admission-registry.json').read_bytes() != registry_raw:
        raise DesignError('admission registry differs from accepted architecture')
    registry = object_value(decode(registry_raw), 'admission registry')
    if set(registry) != {'schemaVersion', 'profile', 'sources', 'aliases'} or type(registry['schemaVersion']) is not int or registry['schemaVersion'] != 1 or registry['profile'] != 'opensip-exact-schema-reference-1':
        raise DesignError('unsupported admission registry')
    if not isinstance(registry['sources'], list) or not registry['sources'] or not isinstance(mapping['sources'], list):
        raise DesignError('invalid admission source rows')
    by_id, by_path = {}, {}
    for row in registry['sources']:
        row = object_value(row, 'admission source')
        if set(row) != {'schemaId', 'sourcePath', 'bytes', 'sha256'} or not isinstance(row['schemaId'], str) or not row['schemaId'] or not isinstance(row['sourcePath'], str):
            raise DesignError('invalid admission source')
        if row['schemaId'] in by_id or row['sourcePath'] in by_path:
            raise DesignError('duplicate admission source')
        by_id[row['schemaId']] = row
        by_path[row['sourcePath']] = row
    if list(by_id) != sorted(by_id):
        raise DesignError('admission sources are not sorted by schema ID')
    seen = set()
    for row in mapping['sources']:
        row = object_value(row, 'admission source mapping')
        if set(row) != {'schemaId', 'implementationPath', 'architectureSource'} or not isinstance(row['implementationPath'], str):
            raise DesignError('invalid admission source mapping')
        path = row['implementationPath']
        if path in seen or path not in by_path:
            raise DesignError('duplicate or unregistered admission source mapping')
        seen.add(path)
        pin = row['architectureSource']
        raw = selected_bytes(pin)
        source = by_path[path]
        if row['schemaId'] != source['schemaId'] or any(pin[k] != source[k] for k in ('bytes', 'sha256')):
            raise DesignError('admission source pin differs from accepted registry')
        if relative_file(implementation, path).read_bytes() != raw:
            raise DesignError('admission source bytes differ from accepted architecture')
        if object_value(decode(raw), 'admission schema').get('$id') != source['schemaId']:
            raise DesignError('admission schema ID differs from registry')
    if seen != set(by_path):
        raise DesignError('admission source map coverage differs')
    if not isinstance(registry['aliases'], list):
        raise DesignError('invalid admission aliases')
    aliases = []
    for row in registry['aliases']:
        row = object_value(row, 'admission alias')
        if set(row) != {'logicalDocument', 'schemaId', 'sourcePath', 'bytes', 'sha256'} or not isinstance(row['logicalDocument'], str) or not isinstance(row['schemaId'], str):
            raise DesignError('invalid admission alias')
        if {k:v for k,v in row.items() if k != 'logicalDocument'} != by_id.get(row['schemaId']):
            raise DesignError('admission alias differs from exact current source')
        aliases.append(row['logicalDocument'])
    if aliases != sorted(set(aliases)):
        raise DesignError('admission aliases must be sorted and unique')
    return {'sourcesVerified': len(seen), 'aliasesVerified': len(aliases), 'executedRuntimeCode': False, 'productQualification': False}


def verify(architecture: Path, lock: dict, implementation: Path | None = None) -> dict:
    object_value(lock, "design lock")
    version = lock.get("schemaVersion")
    fields = {"schemaVersion", "architectureRepository", "approvals", "inputs"}
    if type(version) is not int or version not in (1, 2, 3, 4):
        raise DesignError("unsupported design lock")
    if version in (2, 3):
        fields.add("inventorySuccessor")
    if version == 3:
        fields.add("contractSuccessor")
    if version == 4:
        fields.update(("inventorySuccessors", "contractSuccessors", "inventoryPassageInheritance"))
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
    if version in (2, 3):
        result["inventorySuccessor"] = inventory_successor(architecture, lock["inventorySuccessor"], lock["inputs"])
    if version == 3:
        accepted = {**effective, lock["inventorySuccessor"]["candidate"]["path"]: lock["inventorySuccessor"]["candidate"]}
        result["contractSuccessor"] = contract_successor(architecture, lock["contractSuccessor"], accepted)
    if version == 4:
        result.update(successor_chain(architecture, lock, effective))
    if implementation is not None:
        selected = dict(effective)
        units = result.get('contractSuccessors', [])
        if 'contractSuccessor' in result:
            units = [result['contractSuccessor']]
        for unit in units:
            selected.update({row['path']: row for row in unit['inputs']})
        result['generationSources'] = generation_sources(architecture, implementation, selected)
        if any(path.endswith('/schemas/admission-registry.json') for path in selected):
            result['admissionSources'] = admission_sources(architecture, implementation, selected)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--lock", type=Path, default=Path(__file__).resolve().parents[1] / "design-lock.json")
    parser.add_argument('--implementation', type=Path, help='Optional read-only generator source preflight against the accepted design')
    args = parser.parse_args()
    try:
        result = verify(args.architecture.resolve(), decode(args.lock.read_bytes()), args.implementation.resolve() if args.implementation else None)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Design verification failed: {exc}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
