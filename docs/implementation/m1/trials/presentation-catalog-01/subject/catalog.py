"""Reference metadata association AFTER existing signed closure admission.

The reference dictionaries do not prove authenticity. The host supplies the
already admitted same-platform closure, manifest/tree and its declaration index.
No component code, path lookup, network or signature verification occurs here.
"""
import hashlib
import copy

CATALOG_PATH = '.opensip/presentation-catalog.v1.json'
ORIGINS = frozenset(('retained-generation', 'installed-signed-release', 'signed-closure-bundle'))


class CatalogRefusal(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise CatalogRefusal(code)


def entry_key(group, row):
    if group == 'capabilities':
        return (row['capabilityId'],)
    if group == 'rules':
        ref = row['ruleProgramRef']
        return tuple(ref[k] for k in ('contributionId', 'ruleStableId', 'semanticsMajor', 'programDigest'))
    ref = row['recipeKey']
    return tuple(ref[k] for k in ('contributionId', 'recipeId', 'recipeVersion'))


def admit_catalog(admitted, raw, declared, reference, schema, registry):
    """Associate a reserved listing with an already-admitted closure tree.

    declared has exact capability/program/recipe keys owned by THIS closure's
    admitted host declaration index. Caller cannot supply an arbitrary set.
    Other closure content and security trust have already been admitted.
    """
    require(admitted['trustOrigin'] in ORIGINS, 'CATALOG.ORIGIN')
    entries = [entry for entry in admitted['tree'] if entry['path'] == CATALOG_PATH]
    if not entries:
        require(raw is None, 'CATALOG.UNASSOCIATED-BYTES')
        return None
    require(len(entries) == 1 and entries[0]['type'] == 'file', 'CATALOG.LISTING-TYPE')
    require(type(raw) is bytes, 'CATALOG.BYTES-UNAVAILABLE')
    entry = entries[0]
    require(len(raw) == entry['length'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'CATALOG.BLOB')
    listing = {'path': CATALOG_PATH, 'sha256': entry['sha256'], 'bytes': entry['length']}
    require(listing in admitted['closure']['tree'], 'CATALOG.CLOSURE-TREE')
    # Decoder and shape rules are the existing canonical owner, not a second
    # serializer. Unknown fields, floats, duplicates and oversized bytes refuse.
    data = reference.parse(raw)
    reference.validate(schema, data, registry)
    # Cap the canonical representation too, without requiring published bytes
    # to be canonical. The exact raw bytes remain the tree/signature binding.
    reference.canonical(data)
    for group in ('capabilities', 'rules', 'recipes'):
        keys = [entry_key(group, row) for row in data[group]]
        require(len(keys) == len(set(keys)), 'CATALOG.DUPLICATE-KEY')
        require(set(keys) <= declared[group], 'CATALOG.UNDECLARED-KEY')
    return {'closureId': admitted['closureId'],
            'componentManifestDigest': admitted['closure']['manifestDigest'],
            'trustOrigin': admitted['trustOrigin'], 'listing': listing,
            'catalog': data}


def select_descriptions(receipt, selected, expected_closure_id):
    """Project selected exact keys with the associated immutable provenance.

    Missing data is an explicit historical/optional catalogue state. A new core
    release's metadata completeness gate is a separate admission requirement.
    No fallback to another/current closure is performed.
    """
    if receipt is None:
        return {'state': 'unavailable', 'closureId': expected_closure_id, 'reason': 'catalog-not-retained'}
    require(receipt['closureId'] == expected_closure_id, 'CATALOG.SELECTED-CLOSURE')
    out = {'state': 'present', 'closureId': receipt['closureId'],
           'componentManifestDigest': receipt['componentManifestDigest'],
           'listing': dict(receipt['listing']), 'trustOrigin': receipt['trustOrigin']}
    for group in ('capabilities', 'rules', 'recipes'):
        by_key = {entry_key(group, row): row for row in receipt['catalog'][group]}
        out[group] = []
        for key in selected[group]:
            row = by_key.get(key)
            if row is None:
                out[group].append({'state': 'unavailable', 'key': list(key), 'reason': 'descriptor-not-retained'})
            else:
                out[group].append({'state': 'present', 'descriptor': copy.deepcopy(row)})
    return out
