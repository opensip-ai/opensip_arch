import json, pathlib, collections

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
assert 'x-opensip-config-node-kind-law' not in d

law = collections.OrderedDict()
law['standing'] = (
    "Normative and CLOSED. THE authority for TypeScriptConfigGraphV1 node `kind`. The schema enum "
    "publishes the three admissible values; this law publishes which one each node's path takes, "
    "which the prose previously delegated to `the schema and native admission` while neither stated "
    "it. It adds no enum member, no field and no record."
)
law['selector'] = "#/$defs/TypeScriptConfigGraphV1/properties/nodes/items/properties/kind"
law['appliesTo'] = (
    "EVERY node of the retained graph - the selected entry AND every non-entry node reached through "
    "`extendsResolved`. There is no entry-only rule and no default for the rest. A non-entry node's "
    "kind affects no derived value (see derivedValueScope), which is exactly WHY it needed a "
    "published rule: nothing else pins it and it is still committed to the identity."
)
law['rule'] = (
    "kind is a total function of `node.path` alone. Take the BASENAME - the final `/`-separated "
    "segment of the path - and compare it BYTE-EXACTLY against the closed table below. A match takes "
    "the table's value; anything else is `other`. Nothing else is consulted: not the file's content, "
    "not its position in the graph, not whether it is the entry, not the directory, and not any "
    "caller assertion."
)
law['basenames'] = collections.OrderedDict([("tsconfig.json", "tsconfig"), ("jsconfig.json", "jsconfig")])
law['otherwise'] = "other"
law['comparison'] = (
    "EXACT and case-SENSITIVE over the whole basename, on the UTF-8 bytes of the CanonicalPath as "
    "retained. No prefix, suffix, glob or stem matching; no case folding; no Unicode normalization "
    "beyond what CanonicalPath already requires; no extension-only test. `TSConfig.json`, "
    "`.tsconfig.json` and `tsconfig.jsonc` are each `other`, and a host that lowercases the basename "
    "on a case-insensitive filesystem before comparing has produced a different graph and a "
    "different identity."
)
law['examples'] = [
    collections.OrderedDict([("path", "tsconfig.json"), ("kind", "tsconfig"),
                             ("note", "the ordinary entry")]),
    collections.OrderedDict([("path", "jsconfig.json"), ("kind", "jsconfig"),
                             ("note", "a jsconfig entry stays a jsconfig program even when its bases are not")]),
    collections.OrderedDict([("path", "packages/web/tsconfig.json"), ("kind", "tsconfig"),
                             ("note", "NON-ENTRY, reached as a base: the basename decides, the depth does not")]),
    collections.OrderedDict([("path", "tsconfig.build.json"), ("kind", "other"),
                             ("note", "THE DISCRIMINATING CASE. The widespread tsconfig*.json convention is NOT the rule here; see whyExactAndNotThePrefixConvention")]),
    collections.OrderedDict([("path", "tsconfig.base.json"), ("kind", "other"),
                             ("note", "same, as a shared base of the entry")]),
    collections.OrderedDict([("path", "TSConfig.json"), ("kind", "other"),
                             ("note", "case variant: the comparison is case-sensitive")]),
    collections.OrderedDict([("path", "configs/app.build.json"), ("kind", "other"),
                             ("note", "an explicitly selected custom-named TypeScript configuration; its ENTRY kind is other and it still derives configOrigin tsconfig")]),
]
law['derivedValueScope'] = (
    "`configOrigin` is derived from the SELECTED ENTRY node's kind only: `jsconfig` for a jsconfig "
    "entry, otherwise `tsconfig`, and `synthesized` exactly when there is no entry. So `other` and "
    "`tsconfig` both derive `tsconfig` at the entry, and a non-entry node's kind derives nothing at "
    "all. That is the whole reason this law is owed: `configOrigin` does NOT pin `kind`, so without "
    "a published rule two conforming hosts could disagree on a value that no derived field would "
    "ever contradict."
)
law['identityConsequence'] = (
    "kind sits INSIDE the hashed record. `tsconfigGraphHash` is the raw SHA-256 of "
    "C(TypeScriptConfigGraphV1); TypeScriptUniverseV2ResolvedInputs REQUIRES it and the binding "
    "checks equality; the universe H identity is fact.sourceUniverse and subject-scope.sourceUniverse, "
    "hence fact2, scope2, coverage2, view2, evidence2, seal2 and RunId. Two readings of one "
    "repository containing `tsconfig.build.json` would therefore mint two RunIds and defeat "
    "independent replay across machines - the same defect class the analysis-spec `capabilityId` "
    "vocabulary was closed for, and closed the same way: by naming the authority beside the field."
)
law['whyExactAndNotThePrefixConvention'] = (
    "Both readings are natural and they disagree on real files, so one had to be chosen and written "
    "down. Exact basenames are chosen because `kind` records WHICH RECOGNIZED CONFIGURATION FILE "
    "this node is, not what a project chose to name a base. `tsconfig.build.json` is an ordinary "
    "config file that happens to be named after a convention no specification defines; TypeScript "
    "itself gives the prefix no meaning, and `tsconfig.json` / `jsconfig.json` are the only two "
    "basenames it recognizes by name. A prefix rule would also be asymmetric - it would have to "
    "decide `jsconfig.build.json`, `tsconfig` with no extension and `tsconfig.jsonc` - whereas the "
    "exact table is total, decidable from the retained path alone, and identical on every "
    "filesystem. `other` is not a defect classification: it is the honest statement that this node "
    "is a config file the graph read whose basename is neither recognized name, which is exactly the "
    "case an explicitly selected custom-named configuration presents."
)
law['notARecognitionRule'] = (
    "This law decides the `kind` of a node ALREADY IN the retained graph. Which config file is "
    "SELECTED as the entry, and which markers make a workspace unit at all, are section 1.4 U-1 and "
    "the shared discovery rule; nothing here mints a node, a unit or a program."
)
law['enforcedAt'] = (
    "native_evidence_model.typescript_config_graph_faults, which READS this table rather than "
    "restating it and refuses `native.config-graph-kind-contradicts-path:<path>` for any node whose "
    "declared kind is not the derived one - so a relabelled entry, a relabelled base and an asserted "
    "`tsconfig` on `tsconfig.build.json` all refuse before the graph digest is used."
)

# insert beside the other top-level registries, after the deficiency-cause registry
out = collections.OrderedDict()
for k, v in d.items():
    out[k] = v
    if k == 'x-opensip-deficiency-cause-registry':
        out['x-opensip-config-node-kind-law'] = law
d = out

# annotate the field itself
node = d['$defs']['TypeScriptConfigGraphV1']['properties']['nodes']['items']['properties']['kind']
assert 'x-opensip-vocabulary' not in node
node['description'] = (
    "Which recognized configuration file this node is. DERIVED from node.path by the closed table at "
    "#/x-opensip-config-node-kind-law, never asserted: exact case-sensitive basename `tsconfig.json` "
    "-> tsconfig, `jsconfig.json` -> jsconfig, every other basename -> other. The rule is total and "
    "applies to EVERY node, entry and non-entry alike. `other` is an ordinary value, not a defect: "
    "`tsconfig.build.json` reached as a base is `other`, and an explicitly selected custom-named "
    "configuration is an `other` ENTRY that still derives configOrigin tsconfig. This field is "
    "inside the hashed record, so the rule is an identity rule."
)
node['x-opensip-vocabulary'] = collections.OrderedDict([
    ("authority", "native/native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law"),
    ("law", "native/native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law/rule"),
    ("admittedBy", "native_evidence_model.typescript_config_graph_faults "
                   "(native.config-graph-kind-contradicts-path), which reads the table above"),
    ("movesIdentity", "tsconfigGraphHash -> TypeScriptUniverseV2ResolvedInputs -> sourceUniverse -> "
                      "fact2 / scope2 / coverage2 / view2 / evidence2 / seal2 / run2"),
])

# and the record description, which is where a reader looks first
rec = d['$defs']['TypeScriptConfigGraphV1']
assert rec['description'].endswith("derives configOrigin tsconfig.")
rec['description'] += (
    " Every node's `kind` is derived from its path by the closed exact-basename table at "
    "#/x-opensip-config-node-kind-law - entry and non-entry alike - and a node whose declared kind "
    "is not the derived one refuses."
)

P.write_text(json.dumps(d, indent=1, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')
