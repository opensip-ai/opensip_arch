"""Reference association AFTER existing signed closure, release and Run admission.

Dictionaries here are synthetic host preconditions, not authenticated handles.
The candidate introduces a singular release-selected presentation closure;
product release binding and historical retained custody remain unimplemented.
"""
import hashlib
import copy

CATALOG_PATH = '.opensip/presentation-catalog.v1.json'
ORIGINS = frozenset(('retained-generation', 'installed-signed-release', 'signed-closure-bundle'))
GROUPS = ('capabilities', 'rules', 'recipes')

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

def capability_authority(declarations, selection, reference, native_schema, registry, matrix):
    """Join an already authenticated release to its already admitted Run context.

    selection is host custody: the exact retained registry digest, single release
    presentation closure id, Run Plan.semanticClosures and same platform. Merely
    hashing an arbitrary caller registry does not authenticate this selection.
    """
    reference.validate({'$ref': native_schema['$id']+'#/$defs/ReleaseCapabilityRegistryV1'}, declarations, registry)
    cells = {(c['capability'], c['mode']): c['state'] for c in matrix['cells']}
    keys = [(row['capabilityId'],) for row in declarations]
    require(len(keys) == len(set(keys)), 'CATALOG.RELEASE-DUPLICATE')
    for row in declarations:
        for mode in row['languageModes']:
            require(cells.get((row['capabilityId'], mode)) not in (None, 'NOT-SELECTED'), 'CATALOG.RELEASE-CAPABILITY')
    digest = hashlib.sha256(reference.canonical(declarations)).hexdigest()
    require(digest == selection['registrySha256'], 'CATALOG.RELEASE-REGISTRY')
    require(selection['catalogClosureId'] in selection['semanticClosureIds'], 'CATALOG.RELEASE-PLAN-CLOSURE')
    return {'registrySha256': digest, 'closureId': selection['catalogClosureId'],
            'platform': selection['platform'], 'keys': set(keys)}

def admit_catalog(admitted, raw, declared, reference, schema, registry, authority=None):
    """Admit the listing, or return an explicit admitted absence receipt.

    Declaration keys and authority are admitted host indices, never user config.
    A closure without release authority may describe rules/recipes but no caps.
    """
    require(admitted['trustOrigin'] in ORIGINS, 'CATALOG.ORIGIN')
    closure = admitted['closure']
    require(closure['platform'] == admitted['selectedPlatform'], 'CATALOG.PLATFORM')
    base = {'closureId': admitted['closureId'], 'componentManifestDigest': closure['manifestDigest'],
            'tree': copy.deepcopy(closure['tree']), 'platform': closure['platform'],
            'protocolMajor': closure['protocolMajor'], 'trustOrigin': admitted['trustOrigin'],
            'declared': copy.deepcopy(declared), 'capabilityAuthority': None}
    if authority is not None:
        require(authority['closureId'] == admitted['closureId'], 'CATALOG.RELEASE-CLOSURE')
        require(authority['platform'] == closure['platform'], 'CATALOG.RELEASE-PLATFORM')
        require(declared['capabilities'] <= authority['keys'], 'CATALOG.RELEASE-DECLARATIONS')
        base['capabilityAuthority'] = {k: authority[k] for k in ('registrySha256', 'closureId', 'platform')}
    else:
        require(not declared['capabilities'], 'CATALOG.RELEASE-AUTHORITY-REQUIRED')
    entries = [entry for entry in admitted['tree'] if entry['path'] == CATALOG_PATH]
    blobs = [entry for entry in closure['tree'] if entry['path'] == CATALOG_PATH]
    if not entries:
        require(not blobs, 'CATALOG.CLOSURE-TREE')
        require(raw is None, 'CATALOG.UNASSOCIATED-BYTES')
        return {**base, 'state': 'no-catalogue-declared'}
    require(len(entries) == 1 and entries[0]['type'] == 'file', 'CATALOG.LISTING-TYPE')
    require(len(blobs) == 1, 'CATALOG.CLOSURE-TREE')
    require(type(raw) is bytes, 'CATALOG.BYTES-UNAVAILABLE')
    entry = entries[0]
    require(len(raw) == entry['length'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'CATALOG.BLOB')
    listing = {'path': CATALOG_PATH, 'sha256': entry['sha256'], 'bytes': entry['length']}
    require(listing == blobs[0], 'CATALOG.CLOSURE-TREE')
    data = reference.parse(raw)
    reference.validate(schema, data, registry)
    reference.canonical(data)
    for group in GROUPS:
        keys = [entry_key(group, row) for row in data[group]]
        require(len(keys) == len(set(keys)), 'CATALOG.DUPLICATE-KEY')
        require(set(keys) <= declared[group], 'CATALOG.UNDECLARED-KEY')
        encoded = [reference.canonical(row) for row in data[group]]
        require(encoded == sorted(encoded), 'CATALOG.ROW-ORDER')
        for row in data[group]:
            require(row['tags'] == sorted(row['tags'], key=lambda tag: tag.encode('utf-8')), 'CATALOG.TAG-ORDER')
    return {**base, 'state': 'present', 'listing': listing, 'catalog': data}

def select_descriptions(receipt, selected, expected_closure_id, run_selection, source_state='retained', expected_authority=None):
    """Select only exact Run-selected, declared keys; never consult latest state.

    source_state is the closed result of retained-source lookup. Missing a
    descriptor in a retained listing is not-declared, not a retention failure.
    """
    require(source_state in ('retained', 'not-retained', 'corrupt'), 'CATALOG.SOURCE-STATE')
    require(set(selected) == set(GROUPS) and set(run_selection) == set(GROUPS), 'CATALOG.SELECTION-SHAPE')
    for group in GROUPS:
        require(len(selected[group]) == len(set(selected[group])), 'CATALOG.SELECTED-DUPLICATE')
        require(set(selected[group]) <= set(run_selection[group]), 'CATALOG.RUN-SELECTION')
    if source_state != 'retained':
        require(receipt is None, 'CATALOG.SOURCE-STATE')
        return {'state': 'unavailable', 'closureId': expected_closure_id, 'reason': 'catalog-'+source_state}
    require(receipt is not None, 'CATALOG.RETAINED-RECEIPT')
    require(receipt['closureId'] == expected_closure_id, 'CATALOG.SELECTED-CLOSURE')
    require(receipt['capabilityAuthority'] == expected_authority, 'CATALOG.SELECTED-RELEASE')
    for group in GROUPS:
        require(set(selected[group]) <= receipt['declared'][group], 'CATALOG.SELECTED-UNDECLARED')
    out = {k: copy.deepcopy(receipt[k]) for k in ('state', 'closureId', 'componentManifestDigest', 'tree', 'platform', 'protocolMajor', 'trustOrigin', 'capabilityAuthority')}
    if receipt['state'] == 'no-catalogue-declared':
        return out
    require(receipt['state'] == 'present', 'CATALOG.RECEIPT-STATE')
    out['listing'] = dict(receipt['listing'])
    for group in GROUPS:
        by_key = {entry_key(group, row): row for row in receipt['catalog'][group]}
        out[group] = []
        for key in selected[group]:
            row = by_key.get(key)
            if row is None:
                out[group].append({'state': 'unavailable', 'key': list(key), 'reason': 'descriptor-not-declared'})
            else:
                out[group].append({'state': 'present', 'descriptor': copy.deepcopy(row)})
    return out
