"""Post-reset author v2 (Claude): native schema additions for the admitted boundary inventory (P3) and P22.
Round-trip verified: json.dumps(indent=2, ensure_ascii=True) + newline reproduces the current bytes."""
import json
from pathlib import Path

P = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
raw = P.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=True) + '\n').encode() == raw
D = doc['$defs']

REL_DIR = {"type": "string", "minLength": 1, "maxLength": 4096,
           "pattern": "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])"}
REL_DIR_OR_ROOT = {"type": "string", "maxLength": 4096,
                   "pattern": "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]*(?![\\s\\S])"}

D['CustodyExcludedUnitV1'] = {
    "type": "object", "additionalProperties": False, "required": ["path", "reason"],
    "properties": {"path": REL_DIR_OR_ROOT,
                   "reason": {"type": "string", "minLength": 1, "maxLength": 256,
                              "pattern": "^(DIRECTORY_CUSTODY:[A-Z_]+|MARKER_CUSTODY:(Cargo\\.toml|package\\.json|tsconfig\\.json|jsconfig\\.json):[A-Z_]+|DEPTH)(?![\\s\\S])"}},
    "description": "a security excludedUnits row (relative form) whose reason is a custody/depth exclusion; DIRECTORY_CUSTODY/DEPTH exclude the directory and everything below it, MARKER_CUSTODY excludes exactly that marker file"}
D['AdmittedBoundaryInventoryV1'] = {
    "type": "object", "additionalProperties": False,
    "required": ["schemaVersion", "source", "selectedRoot", "nestedRepositories", "nestedProjects", "custodyExcludedUnits", "prunedTrees"],
    "properties": {
        "schemaVersion": {"const": 1},
        "source": {"const": "security.discovery"},
        "selectedRoot": {"type": "string", "minLength": 1, "maxLength": 4096},
        "nestedRepositories": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "nestedProjects": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "custodyExcludedUnits": {"type": "array", "maxItems": 4096, "items": {"$ref": "#/$defs/CustodyExcludedUnitV1"}},
        "prunedTrees": {"type": "array", "maxItems": 65536, "items": {"$ref": "#/$defs/PrunedTreeV1"}}},
    "description": "TRUSTED ADMITTED INPUT (P3): the security discovery instrument's authority boundaries for the selected root, converted once by discovery-defaults.boundary_inventory_from_provenance from the ACCEPTed DiscoveryProvenanceV1 (absolute custody locators -> relative scope paths). Never authored by a caller; an operational host composition passes it to discover_units/assign_membership/unit_scope_descriptor."}
D['BoundaryExcludedUnitV1'] = {
    "type": "object", "additionalProperties": False, "required": ["path", "marker", "reason", "anchor"],
    "properties": {"path": REL_DIR_OR_ROOT,
                   "marker": {"type": "string", "enum": ["Cargo.toml", "package.json", "tsconfig.json", "jsconfig.json"]},
                   "reason": {"type": "string", "enum": ["nested-repository", "nested-project", "custody-excluded"]},
                   "anchor": REL_DIR_OR_ROOT}}
D['UnitBoundariesV1'] = {
    "type": "object", "additionalProperties": False,
    "required": ["source", "nestedRepositories", "nestedProjects", "custodyExcludedUnits", "excludedUnits", "disclosure"],
    "properties": {
        "source": {"type": "string", "enum": ["security.discovery", "none"]},
        "nestedRepositories": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "nestedProjects": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "custodyExcludedUnits": {"type": "array", "maxItems": 4096, "items": {"$ref": "#/$defs/CustodyExcludedUnitV1"}},
        "excludedUnits": {"type": "array", "maxItems": 8192, "items": {"$ref": "#/$defs/BoundaryExcludedUnitV1"}},
        "disclosure": {"type": "string", "minLength": 1, "maxLength": 1024}},
    "description": "boundary provenance of a unit discovery: source `security.discovery` when the admitted inventory was applied, `none` for the standalone pure instrument (not an operational host composition)"}

ud = D['UnitDiscoveryV1']
ud['required'] = ["units", "prunedTrees", "boundaries", "refused"]
ud['properties'] = {"units": ud['properties']['units'], "prunedTrees": ud['properties']['prunedTrees'],
                    "boundaries": {"$ref": "#/$defs/UnitBoundariesV1"}, "refused": ud['properties']['refused']}

row = D['FileMembershipRowV1']
row['properties']['membership']['enum'] = ["program-member", "syntax-only", "unsupported-file", "outside-project-boundary"]
row['properties']['reason']['enum'] = ["deepest-unit-in-language", "no-program-unit-for-language", "grammar-only", "no-bundled-grammar",
                                       "host-ignore-convention", "nested-repository", "nested-project", "custody-excluded"]

um = D['UnitMembershipV1']
um['required'] = ["schemaVersion", "units", "rows", "unsupportedFiles", "outsideBoundaryFiles", "erasedFiles"]
props = um['properties']
um['properties'] = {"schemaVersion": props['schemaVersion'], "units": props['units'], "rows": props['rows'], "unsupportedFiles": props['unsupportedFiles'],
                    "outsideBoundaryFiles": {"type": "array", "items": dict(props['unsupportedFiles']['items']), "maxItems": 10000000, "uniqueItems": True,
                                             "description": "files at or below an admitted boundary (P3): another project's or uncustodied source, disclosed, never scanned and never erased"},
                    "erasedFiles": props['erasedFiles']}

P.write_bytes((json.dumps(doc, indent=2, ensure_ascii=True) + '\n').encode())
print('defs now', len(D))
