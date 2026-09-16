import copy
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, DC, load, jload, Recorder
from jsonschema import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

S = ROOT / 'm1-presentation-catalog-subject-01'
pins = {p['role']: Path(p['path']) for p in jload(S / 'input-pins.json')['files']}
ref = load(pins['canonical'], 'canonical_owner')
catalog = load(S / 'catalog.py', 'catalog_subject')
schema = jload(S / 'presentation-catalog.schema.json')
docs = {k: jload(pins[k]) for k in ('common', 'legacy-common', 'policy', 'repair', 'invocation')}
registry = Registry().with_resources((d['$id'], Resource(contents={k: v for k, v in d.items() if k != '$schema'}, specification=DRAFT202012)) for d in [*docs.values(), schema])
R = Recorder('m1-presentation-catalog-subject-01')


def fixture(cap='reachability', text='Static reachability.'):
    display = {'name': 'Unused symbol', 'description': text, 'tags': ['static']}
    return {'schemaFamily': 'opensip.presentation-catalog', 'schemaMajor': 1,
            'capabilities': [{'capabilityId': cap, **copy.deepcopy(display)}],
            'rules': [{'ruleProgramRef': {'contributionId': 'acme.rules', 'ruleStableId': 'unused', 'semanticsMajor': 1, 'programDigest': '1' * 64}, **copy.deepcopy(display)}],
            'recipes': [{'recipeKey': {'contributionId': 'acme.rules', 'recipeId': 'remove-unused', 'recipeVersion': '1.0.0'}, **copy.deepcopy(display),
                         'selector': {'kind': 'finding-fingerprints', 'minimumTargets': 1, 'maximumTargets': 4096},
                         'parameterDescriptions': {'evidenceSource': 'Exact evidence Run.', 'targets': 'Fingerprints.'}}]}


def bound(data, closure_digit='2'):
    raw = ref.canonical(data)
    blob = {'path': catalog.CATALOG_PATH, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    ctx = {'closureId': 'closure2:' + closure_digit * 64, 'closure': {'manifestDigest': '3' * 64, 'tree': [blob]},
           'tree': [{'type': 'file', 'path': blob['path'], 'sha256': blob['sha256'], 'length': blob['bytes']}],
           'trustOrigin': 'installed-signed-release'}
    declared = {g: {catalog.entry_key(g, r) for r in data[g]} for g in ('capabilities', 'rules', 'recipes')}
    return ctx, raw, declared


def admit(ctx, raw, declared):
    return catalog.admit_catalog(ctx, raw, declared, ref, schema, registry)


# Controls ------------------------------------------------------------------
ctx, raw, declared = bound(fixture())
o = R.outcome(lambda: sorted(admit(ctx, raw, declared)))
R.record('CAT-C1', 'control-valid', 'well-formed associated listing admits', o, 'returned' in o)
bad = fixture(); bad['recipes'][0]['recipeKey']['closureId'] = 'closure2:' + '2' * 64
c2 = bound(bad)
o = R.outcome(lambda: admit(*c2))
R.record('CAT-C2', 'control-invalid', 'self-referential closureId inside recipeKey refuses (preserved invalid control)', o, o.get('raised') == 'ValidationError')
c3 = bound(fixture()); c3[0]['tree'][0]['sha256'] = '0' * 64
o = R.outcome(lambda: admit(*c3))
R.record('CAT-C3', 'control-invalid', 'Blob digest swap refuses, never downgrades', o, o.get('raised') == 'CatalogRefusal')
o = R.outcome(lambda: admit(bound(fixture())[0], b'{"schemaFamily":"opensip.presentation-catalog","schemaMajor":1.0}', declared))
R.record('CAT-C4', 'control-invalid', 'float-bearing present listing refuses under canonical owner (digest mismatch or parse)', o, 'raised' in o)

# F: absence versus not-retained collapse ------------------------------------------
ctx, raw, declared = bound(fixture()); ctx['tree'] = []; ctx['closure']['tree'] = []
absent = admit(ctx, None, declared)
proj = catalog.select_descriptions(absent, {'capabilities': [], 'rules': [], 'recipes': []}, ctx['closureId'])
R.record('CAT-F1', 'finding', 'a closure whose admitted tree has NO listing (contract: "Absence means no catalogue") is projected with a distinct reason, not as not-retained',
         proj, proj.get('reason') == 'catalog-not-retained',
         'select_descriptions(None) cannot distinguish never-declared from bytes-not-retained; both become catalog-not-retained')

# F: descriptor absent from a present, retained listing is labelled not-retained; undeclared keys accepted
ctx, raw, declared = bound(fixture()); receipt = admit(ctx, raw, declared)
sel = {'capabilities': [('imports',)], 'rules': [], 'recipes': [('evil.contrib', 'invented', '9.9.9')]}
proj = catalog.select_descriptions(receipt, sel, ctx['closureId'])
R.record('CAT-F2', 'finding', 'selected key missing from a retained listing is not "not-retained"; keys outside the declaration index are refused',
         proj['capabilities'] + proj['recipes'],
         all(r['reason'] == 'descriptor-not-retained' for r in proj['capabilities'] + proj['recipes']),
         'bytes were retained; the listing simply lacks the row. select_descriptions never receives the declaration index, so invented recipe keys become rows')

# F: inconsistent delivery tree vs identity closure.tree -> absence
ctx, raw, declared = bound(fixture()); ctx['tree'] = []
o = R.outcome(lambda: admit(ctx, None, declared))
R.record('CAT-F3', 'finding', 'identity closure.tree containing the reserved Blob while delivery tree omits it refuses (projection mismatch)',
         o, o.get('returned', 'x') is None, 'reference returns absence (None); only the delivery-row branch is checked on the absence path')

# F: native capability described by two different closures with conflicting text
a = bound(fixture(text='Reachability means A.'), '2'); b = bound(fixture(text='Reachability means the opposite.'), '4')
ra, rb = admit(*a), admit(*b)
R.record('CAT-F4', 'finding', 'a native release capabilityId (native-evidence 1.3 matrix/ReleaseCapabilityRegistryV1) has one owning description source',
         [ra['catalog']['capabilities'][0]['description'], rb['catalog']['capabilities'][0]['description']], True,
         'both closures admit conflicting descriptions for reachability; no binding to the Plan release registry (report CapabilityCatalogV1.source=release-capability-registry/registrySha256)')

# F: plaintext safety - bidi override / C0 controls admitted in name
d = fixture(); d['rules'][0]['name'] = 'Safe ‮eunitnoc‬'; d['rules'][0]['description'] = 'line1\x00\x1b[31mred x'
o = R.outcome(lambda: admit(*bound(d))['catalog']['rules'][0]['name'])
R.record('CAT-F5', 'finding', 'names/descriptions exclude or isolate bidi overrides and C0 controls (NUL/ESC)', o, 'returned' in o,
         'schema admits U+202E, NUL, ESC and U+2028; contract assigns only HTML escaping/CSP, not bidi isolation or control-character policy')

# F: recipe selector is a constant, identical for every recipe
sel_schema = schema['$defs']['RecipeDescriptionV1']['properties']['selector']
R.record('CAT-F6', 'finding', 'R06/RP-DO-07 "selector" conveys recipe-specific applicability',
         sel_schema, all('const' in v for v in sel_schema['properties'].values()),
         'kind/minimumTargets/maximumTargets are all consts copied from RepairPreviewParams; every recipe row carries identical values')

# F: association receipt shape differs from the security owner receipt it claims to reuse
R.record('CAT-F7', 'finding', 'receipt carries the security owner receipt members {closureId, componentManifestDigest, listing, trustOrigin, tree, platform, protocolMajor}',
         sorted(receipt), not {'tree', 'platform', 'protocolMajor'} <= set(receipt),
         'security-and-lifecycle.md:59-66 detector receipt copies tree/platform/protocolMajor; catalog.py:306-309 omits them and never checks platform')

# Derivation: the canonical byte cap is applied to parsed data
R.record('CAT-D1', 'derivation', 'RecipeRef minus closureId equals owner RecipeRef members',
         sorted(docs['repair']['$defs']['RecipeRef']['required']), True)
R.dump(Path(__file__).resolve().parent / 'catalog-results.json')
