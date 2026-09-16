"""PROBE 07 (v31) — source29 item: the native retention catalog.

I measure rather than restate: the actual annotation site count, the actual `derived` uses and
whether they are exactly the SourceUnitOwnershipV1 unitId positions, whether `derived` reuses the
EXISTING UnitIdentityV1 recipe (no new retained fragment), whether every site's
representation/retention is declared, and whether identity-schemas.v3 is named current.
"""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
N = os.path.join(SRC, 'docs/coop/design-corrections/native')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {}

raw = open(os.path.join(N, 'native-evidence.schemas.v2.json'), encoding='utf-8').read()
sch = json.loads(raw)
law = sch['x-opensip-digest-law']
R['declaredRepresentations'] = law['representations']
R['declaredRetentions'] = sorted(law['retention'])
R['siteCountLaw'] = law['siteCountLaw']
R['lawStanding'] = law['standing']
print('declared representations:', R['declaredRepresentations'])
print('declared retentions     :', R['declaredRetentions'])

# ---- SYNTACTIC site count, exactly as siteCountLaw defines it ----
R['syntacticSiteCount'] = len(re.findall(r'"x-opensip-digest"\s*:', raw))
print('\nsyntactic x-opensip-digest occurrences :', R['syntacticSiteCount'])
R['staleCount68Present'] = bool(re.search(r'\b68\b\s*(sites|annotation)', raw, re.I))
R['anyHandMaintainedTotalField'] = [k for k in law if 'count' in k.lower() and k != 'siteCountLaw']
print('hand-maintained total fields besides siteCountLaw :', R['anyHandMaintainedTotalField'])

# ---- structural walk: every annotation object, its representation/retention ----
sites = []
def walk(o, path='$'):
    if isinstance(o, dict):
        if 'x-opensip-digest' in o:
            a = o['x-opensip-digest']
            sites.append({'path': path, 'annotation': a})
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
walk(sch)
R['structuralSiteCount'] = len(sites)
print('structural annotation objects          :', len(sites))
R['syntacticEqualsStructural'] = R['syntacticSiteCount'] == len(sites)

reps, rets = {}, {}
undeclared = []
for s in sites:
    a = s['annotation']
    rep = a.get('representation') if isinstance(a, dict) else None
    ret = a.get('retention') if isinstance(a, dict) else None
    reps[rep] = reps.get(rep, 0) + 1
    rets[ret] = rets.get(ret, 0) + 1
    if rep not in law['representations'] or ret not in law['retention']:
        undeclared.append({'path': s['path'], 'representation': rep, 'retention': ret})
R['representationCounts'] = reps
R['retentionCounts'] = rets
R['sitesWithUndeclaredRepresentationOrRetention'] = undeclared
print('\nrepresentation counts :', reps)
print('retention counts      :', rets)
print('undeclared sites      :', len(undeclared), undeclared[:3])

# ---- the three `derived` sites ----
der = [s for s in sites if isinstance(s['annotation'], dict)
       and s['annotation'].get('retention') == 'derived']
R['derivedSiteCount'] = len(der)
R['derivedSitePaths'] = [s['path'] for s in der]
print('\nderived sites (%d):' % len(der))
for s in der:
    print('   %s' % s['path'])
    print('      %s' % json.dumps(s['annotation'])[:260])
R['derivedAllUnitId'] = all(s['path'].endswith('unitId') or 'unitId' in s['path'] or
                            'UnitId' in s['path'] or 'selectedUnitIds' in s['path'] for s in der)
R['derivedAllUnderSourceUnitOwnership'] = all('SourceUnitOwnership' in s['path'] for s in der)
print('all derived sites are SourceUnitOwnershipV1 unitId positions :',
      R['derivedAllUnderSourceUnitOwnership'], '/ unitId-named:', R['derivedAllUnitId'])

# ---- does `derived` reuse an EXISTING recipe, or introduce a new retained fragment? ----
defs = sch.get('$defs', {})
R['unitIdentityV1Present'] = 'UnitIdentityV1' in defs
R['unitIdentityV1'] = defs.get('UnitIdentityV1')
R['compilationUnitDomainMentioned'] = 'native.compilation-unit.v1' in raw
print('\nUnitIdentityV1 already defined in this bundle :', R['unitIdentityV1Present'])
print('native.compilation-unit.v1 named              :', R['compilationUnitDomainMentioned'])
if R['unitIdentityV1Present']:
    print('UnitIdentityV1 =', json.dumps(defs['UnitIdentityV1'])[:400])
# any NEW retained-fragment retention kind added?
R['retentionKindsThatRetainNewBytes'] = [k for k in law['retention']
                                         if 'retained under this digest' in law['retention'][k]
                                         or 'preimage frame' in law['retention'][k] and k != 'derived']
R['derivedRetainsNoPreimage'] = 'no separately retained preimage frame' in law['retention']['derived']
print('derived retains no separate preimage frame    :', R['derivedRetainsNoPreimage'])

# ---- identity-schemas.v3 named current ----
R['namesIdentitySchemasV3'] = 'identity-schemas.v3' in raw
R['identitySchemasMentions'] = sorted(set(re.findall(r'identity-schemas\.v\d[\w.]*', raw)))
print('\nidentity-schemas references in the bundle     :', R['identitySchemasMentions'])

json.dump(R, open(os.path.join(OUT, 'p07-nativecatalog.json'), 'w'), indent=1, default=str)
print('\nwrote p07-nativecatalog.json')
