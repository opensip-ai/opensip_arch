import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/native/native_evidence_model.v2.py')
s = P.read_text(encoding='utf-8')

OLD = '''def typescript_config_graph_faults(graph: dict) -> list[str]:
    """Membership, reachability and acyclicity of the retained extends graph, plus a `kind` that
    cannot contradict its own basename, so the entry cannot be relabelled."""
    faults: list[str] = []
    by_path = {n["path"]: n for n in graph["nodes"]}
    for node in graph["nodes"]:
        basename = node["path"].rpartition("/")[2]
        expected = basename.removesuffix(".json") if basename in ("tsconfig.json", "jsconfig.json") else "other"
        if node["kind"] != expected:
'''
NEW = '''def config_node_kind(path: str) -> str:
    """`TypeScriptConfigGraphV1.nodes[].kind` DERIVED from the node path, by the published law.

    The table is READ from `native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law`, not
    restated here, so the schema annotation, the prose and this derivation cannot drift apart.

    The comparison is the EXACT basename, case-SENSITIVE, on the retained CanonicalPath: no prefix,
    glob or stem matching and no case folding. It is a TOTAL function of the path alone and applies
    to EVERY node, entry and non-entry alike - `packages/web/tsconfig.json` reached as a base is
    `tsconfig`, `tsconfig.build.json` is `other`, and `TSConfig.json` is `other`. `configOrigin`
    reads only the ENTRY node's kind and therefore pins nothing here, which is precisely why the
    rule had to be published: `kind` is inside the hashed record, so two readings of one repository
    would mint two `tsconfigGraphHash` values and two RunIds."""
    basename = path.rpartition("/")[2]
    return CONFIG_NODE_KIND_LAW["basenames"].get(basename, CONFIG_NODE_KIND_LAW["otherwise"])


def typescript_config_graph_faults(graph: dict) -> list[str]:
    """Membership, reachability and acyclicity of the retained extends graph, plus a `kind` that
    cannot contradict its own path under the published derivation, so neither the entry nor any
    base can be relabelled."""
    faults: list[str] = []
    by_path = {n["path"]: n for n in graph["nodes"]}
    for node in graph["nodes"]:
        expected = config_node_kind(node["path"])
        if node["kind"] != expected:
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

# the law constant, beside the other registries read at import time
OLD2 = 'DEFICIENCY_CAUSE_REGISTRY = SCHEMAS["x-opensip-deficiency-cause-registry"]\n'
NEW2 = ('DEFICIENCY_CAUSE_REGISTRY = SCHEMAS["x-opensip-deficiency-cause-registry"]\n'
        '# The CLOSED path -> config-node-kind table, likewise read from the published law rather than\n'
        '# restated: which recognized configuration file each retained graph node is. It is a total\n'
        '# function of the node path, applies to every node including non-entry ones, and is an IDENTITY\n'
        '# rule because `kind` is inside C(TypeScriptConfigGraphV1).\n'
        'CONFIG_NODE_KIND_LAW = SCHEMAS["x-opensip-config-node-kind-law"]\n')
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)

P.write_text(s, encoding='utf-8')
print('ok')
