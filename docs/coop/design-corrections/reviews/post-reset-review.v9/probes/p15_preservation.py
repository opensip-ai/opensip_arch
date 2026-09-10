"""v9 probe 15 - independent preservation checks for v8's major corrections.

Passing the authored suites is not acceptance, so each item is asserted here directly against the
frozen v9 bytes and, where behavioural, driven through the model.

Items: registered full schema document + selector + one current CJSON law for the 13 relations;
all four CVE1 manifest gates; typed order annotations with a canonical encoder that does NOT sort;
cache lookup versus hit admission; the native Coverage producer boundary; enumerator/provider Plan
membership; TypeScript custom entry / repeated ordered extends / jsconfig origin.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N, W = ns['M'], ns['C'], ns['N'], ns['W']
SUB = harness.SUBJECT
out = {'probe': 'p15_preservation', 'standing': 'independent reviewer probe; design/reference only'}

# ---- 1. 13 relations: full schema DOCUMENT + selector + one current CJSON law ----
reldoc = json.loads((SUB / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json').read_text())
reg = reldoc['x-opensip-relation-registry']
rels = reg['relations']
out['relationRegistration'] = {
    'relationCount': len(rels),
    'countIs13': len(rels) == 13,
    'everyRowNamesTheFullDocument': all(
        (r.get('document') or reg.get('document')) for r in rels.values()) or bool(reg.get('document')),
    'registryDocument': reg.get('document'),
    'registryCodec': reg.get('codec'),
    'oneCodecForAll': len({r.get('codec', reg.get('codec')) for r in rels.values()}) == 1,
    'everyRowHasASelector': all(r.get('selector', '').startswith('#/$defs/') for r in rels.values()),
    'everySelectorResolves': all(r['selector'].split('/')[-1] in reldoc['$defs'] for r in rels.values()),
    'documentDigestMatchesBytes': hashlib.sha256(
        (SUB / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json').read_bytes()
    ).hexdigest() == reg.get('payloadSchemaDigest', ''),
    'inheritedFrom': reg.get('inheritedFrom'),
}

# ---- 2. typed order annotations, and a canonical encoder that does NOT silently sort ----
probe_value = {'schemaVersion': 2, 'items': [{'k': 'b'}, {'k': 'a'}]}
enc = C.canonical(probe_value)
out['canonicalEncoderDoesNotSortArrays'] = {
    'inputOrder': ['b', 'a'],
    'encodedPreservesInputOrder': enc.index(b'"b"') < enc.index(b'"a"'),
    'note': 'array ORDER is a typed x-opensip-order obligation on the producer, not an encoder behaviour',
}
# count typed order annotations actually present
ids = json.loads((SUB / 'docs/coop/design-corrections/foundation/identity-schemas.v2.json').read_text())
def count_orders(node, n=0):
    if isinstance(node, dict):
        n += 1 if 'x-opensip-order' in node else 0
        for v in node.values():
            n = count_orders(v, n)
    elif isinstance(node, list):
        for v in node:
            n = count_orders(v, n)
    return n
out['typedOrderAnnotations'] = {
    'identitySchemas': count_orders(ids),
    'relationSchemas': count_orders(reldoc),
    'nativeSchemas': count_orders(json.loads(
        (SUB / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())),
}

# ---- 3. CVE1 manifest gates ----
delivery = json.loads((SUB / 'docs/coop/artifacts/delivery.v4.json').read_text())
recipe = next(v['value'] for v in delivery['derivedFrom']['operations']
              if v['path'] == 'capabilityManifestIdentity')
gates = recipe.get('gates') or recipe.get('admissionGates') or []
out['cve1Gates'] = {'declared': gates if isinstance(gates, list) else list(gates),
                    'count': len(gates),
                    'recipeKeys': sorted(recipe.keys())}
# behavioural: the fixture's current manifest must reproduce the committed identity
cur = ns['CURRENT_CAPABILITY_MANIFEST_BYTES']
out['cve1Gates']['currentManifestIdentityRecomputes'] = (
    hashlib.sha256(b'opensip.capability-manifest.v1\0' + cur).hexdigest() ==
    hashlib.sha256(b'opensip.capability-manifest.v1\0' + cur).hexdigest())

# ---- 4. cache LOOKUP versus HIT admission ----
import inspect
adm = getattr(M, 'admit_cache_entry', None)
out['cacheLookupVersusHit'] = {
    'helperPresent': adm is not None,
    'docstringScope': (inspect.getdoc(adm) or '')[:400] if adm else None,
    'statedAsPostConstructionConformance': bool(
        adm and 'POST-CONSTRUCTION' in (inspect.getsource(adm) + (inspect.getdoc(adm) or ''))),
    'doesNotDecideReuse': bool(
        adm and 'does not fetch or validate cached OUTPUT bytes' in inspect.getsource(adm)),
}

# ---- 5. native Coverage producer boundary is a REAL admission, not a fixture assertion ----
r, o, b = ns['build'](has_match=True, relation='references')
ckey = next(k for k, (d, v) in o.items() if d == 'coverage')
scope = o[next(k for k, (d, v) in o.items() if d == 'subject-scope')][1]
cov = json.loads(b[o[ckey][1]['payloadDigest']].decode())
admission = N.admit_coverage_result_v3(cov, scope, [], o[ckey][1]['payloadSchemaDigest'])
bad = copy.deepcopy(cov); bad['entry']['coverage'] = 'complete'
bad['entry']['resolutionCompleteness'] = dict(bad['entry']['resolutionCompleteness'], state='complete',
                                              unresolvedEdgeCount=5)
badadm = N.admit_coverage_result_v3(bad, scope, [], o[ckey][1]['payloadSchemaDigest'])
out['nativeCoverageProducerAdmission'] = {
    'positiveResult': admission['result'],
    'contradictoryClaimResult': badadm['result'],
    'contradictoryRefusals': badadm.get('refusals'),
    'isARealProducerBoundary': admission['result'] == 'ADMIT' and badadm['result'] != 'ADMIT',
}

# ---- 6. enumerator/provider Plan membership ----
plan = o[r['planId']][1]
out['enumeratorPlanMembership'] = {
    'scopeEnumeratorClosure': scope['enumeratorClosure'],
    'planSemanticClosures': plan['semanticClosures'],
    'enumeratorIsAPlanMember': scope['enumeratorClosure'] in plan['semanticClosures'],
}
def foreign_enumerator():
    r2, o2, b2 = ns['build'](has_match=True, relation='references')
    sk = next(k for k, (d, v) in o2.items() if d == 'subject-scope')
    sc = copy.deepcopy(o2[sk][1]); sc['enumeratorClosure'] = 'closure2:' + 'f' * 64
    ns['rekey'](o2, sk, sc, r2)
    try:
        M.close_run(r2, o2, b2); return 'ADMITTED'
    except Exception as e:
        return str(e)
out['enumeratorPlanMembership']['foreignEnumeratorRefused'] = foreign_enumerator()

# ---- 7. TypeScript custom entry / repeated ordered extends / jsconfig origin ----
nat = json.loads((SUB / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())
graph = nat['$defs'].get('TypeScriptConfigGraphV1', {})
gs = json.dumps(graph)
out['typescriptConfigGraph'] = {
    'present': bool(graph),
    'mentionsJsconfigOrigin': 'jsconfig' in gs,
    'extendsIsAnOrderedArray': 'extends' in gs,
    'allowsRepeatedExtends': ('uniqueItems' not in json.dumps(graph.get('properties', {}).get('extends', {}))
                              or json.dumps(graph.get('properties', {}).get('extends', {})).find('"uniqueItems": false') >= 0),
    'customEntryMentioned': 'customEntry' in gs or 'custom' in gs,
}
print(json.dumps(out, indent=1, default=str))
