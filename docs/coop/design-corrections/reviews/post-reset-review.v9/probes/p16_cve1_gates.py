"""v9 probe 16 - the four inherited CVE1 capability-manifest gates, driven independently.

Also corrects three p15 harness errors (NOT product defects):
  (a) p15 compared the registry's payloadSchemaDigest to a hash; that field is a DESCRIPTION
      ("raw SHA-256 of the exact full bytes of that file"), because a document cannot carry its
      own digest. No self-hash cycle is required or expected.
  (b) p15 matched 'POST-CONSTRUCTION' in upper case; the shipped docstring says "post-construction
      conformance check".
  (c) p15 counted x-opensip-order in the relation document, which legitimately carries none.

The four inherited gates are ADM-TYPE, ADM-CLOSED, ADM-DOMAIN and ADM-ORDER. Each is driven with
a positive control plus negatives that must refuse.
"""
import copy, hashlib, inspect, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
SUB = harness.SUBJECT
out = {'probe': 'p16_cve1_gates', 'standing': 'independent reviewer probe; design/reference only',
       'harnessCorrections': [
           'p15 treated the registry payloadSchemaDigest description string as a digest; no self-hash cycle exists or is wanted.',
           "p15 matched 'POST-CONSTRUCTION' in the wrong case.",
           'p15 counted typed order annotations in the relation document, which legitimately carries none.']}

# ---- corrections restated as measurements
reldoc = json.loads((SUB / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json').read_text())
reg = reldoc['x-opensip-relation-registry']
out['registryDigestField'] = {
    'value': reg.get('payloadSchemaDigest'),
    'isADescriptionNotADigest': not (isinstance(reg.get('payloadSchemaDigest'), str)
                                     and len(reg['payloadSchemaDigest']) == 64),
    'standing': reg.get('standing'),
    'closedAt13': '13 relations' in (reg.get('standing') or ''),
    'twelveInheritedPlusUnresolvedEdge': 'unresolved-edge' in (reg.get('standing') or ''),
}
adm = M.admit_cache_entry
src = inspect.getsource(adm)
out['cacheLookupVersusHit'] = {
    'saysPostConstructionConformance': 'post-construction conformance check' in src,
    'saysFindingBytesIsNotAuthority': 'Finding bytes under a matching' in src,
    'excludesSchedulingApi': 'pre-analysis cache scheduling API' in src,
}

# ---- the current capability manifest
cur_bytes = ns['CURRENT_CAPABILITY_MANIFEST_BYTES']
cur = json.loads(cur_bytes.decode())
out['currentManifest'] = {'relationCount': None, 'declaresUnresolvedEdge': 'unresolved-edge' in cur_bytes.decode()}

def admit(manifest):
    """Drive the shipped capability-manifest admission over a candidate manifest."""
    fn = None
    for name in ('admit_capability_manifest', 'capability_manifest_admit', 'admit_capability'):
        if hasattr(N, name):
            fn = getattr(N, name); break
    if fn is None:
        for name in dir(N):
            if 'capability' in name.lower() and 'admit' in name.lower():
                fn = getattr(N, name); break
    return fn, fn(manifest) if fn else None

fn, positive = admit(copy.deepcopy(cur))
out['admissionFunction'] = fn.__name__ if fn else None
out['positiveControl'] = positive

def gate(label, mutate):
    m = copy.deepcopy(cur)
    try:
        mutate(m)
    except Exception as e:
        return {'gate': label, 'mutationFailed': str(e)}
    try:
        res = fn(m)
        ok = res if not isinstance(res, dict) else res
        refused = bool(isinstance(res, dict) and (res.get('refusals') or res.get('result') == 'REFUSE'))
        return {'gate': label, 'refused': refused, 'result': res if not isinstance(res, dict) else
                {k: res[k] for k in list(res)[:6]}}
    except Exception as e:
        return {'gate': label, 'refused': True, 'cause': str(e), 'exception': type(e).__name__}

providers = cur.get('providers') or []
rows = []
# ADM-TYPE: a boolean where an integer schemaVersion belongs
rows.append(gate('ADM-TYPE boolean schemaVersion', lambda m: m.update(schemaVersion=True)))
# ADM-CLOSED: an undeclared extra property
rows.append(gate('ADM-CLOSED undeclared property', lambda m: m.update(unexpectedKey='x')))
# ADM-DOMAIN: an unregistered relation id / rung / platform
def bad_relation(m):
    m['providers'][0]['relationIds'][0] = 'not-a-registered-relation'
def bad_platform(m):
    m['providers'][0]['platformIds'][0] = 'not-a-registered-platform'
rows.append(gate('ADM-DOMAIN unregistered relation', bad_relation))
rows.append(gate('ADM-DOMAIN unregistered platform', bad_platform))
# ADM-ORDER: duplicate and unsorted members
def dup_platform(m):
    m['providers'][0]['platformIds'].append(m['providers'][0]['platformIds'][0])
def unsorted_platform(m):
    m['providers'][0]['platformIds'] = sorted(m['providers'][0]['platformIds'], reverse=True) \
        if len(m['providers'][0]['platformIds']) > 1 else m['providers'][0]['platformIds'] + ['aaa']
def dup_provider(m):
    m['providers'].append(copy.deepcopy(m['providers'][0]))
rows.append(gate('ADM-ORDER duplicate platform', dup_platform))
rows.append(gate('ADM-ORDER unsorted platform', unsorted_platform))
rows.append(gate('ADM-ORDER duplicate provider', dup_provider))
out['gates'] = rows
out['allNegativesRefuse'] = all(r.get('refused') for r in rows if 'mutationFailed' not in r)

# ---- the CVE1 identity recipe recomputes independently
delivery = json.loads((SUB / 'docs/coop/artifacts/delivery.v4.json').read_text())
recipe = next(v['value'] for v in delivery['derivedFrom']['operations']
              if v['path'] == 'capabilityManifestIdentity')
inherited = bytes.fromhex(recipe['vectors']['byId']['DCM-1-core']['committedBytesHex'])
expected = recipe['vectors']['byId']['DCM-1-core'].get('identity') or \
           recipe['vectors']['byId']['DCM-1-core'].get('capabilityManifestId')
mine = hashlib.sha256(b'opensip.capability-manifest.v1\0' + inherited).hexdigest()
out['cve1RecipeRecomputation'] = {
    'inheritedGoldenBytes': len(inherited),
    'reviewerRecomputed': mine,
    'committedExpectation': expected,
    'agrees': (expected or '').endswith(mine),
    'currentManifestIdentity': hashlib.sha256(b'opensip.capability-manifest.v1\0' + cur_bytes).hexdigest(),
    'currentDiffersFromInherited': cur_bytes != inherited,
}
print(json.dumps(out, indent=1, default=str))
