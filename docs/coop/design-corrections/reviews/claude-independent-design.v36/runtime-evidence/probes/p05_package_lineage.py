"""P05 — corrects r05's lineage assumption. r05 treated package13's predecessor-artifact-manifest.json as package12's
manifest; its digest is not fb35036f, so r05's package12To13 member delta and construction-account comparison are void.
This measures lineage against the package12 I verified on source35 (claude-author-package-successor.v12, manifest
fb35036f, re-hashed here), and identifies what predecessor-artifact-manifest.json and every historical-*/artifact-manifest.json
in package13 actually are. Custody hashing only; consumer-custody members are hashed, never parsed."""
import hashlib, json, os

P12 = '/tmp/opensip-design-corrections/claude-author-package-successor.v12'
P13 = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v36/receipts'
R05 = os.path.join(OUT, 'r05-package13.json')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rows(path):
    am = json.load(open(path))
    return {r['path']: r['sha256'] for r in (am['files'] if isinstance(am, dict) else am)}


R = {'package12ManifestSha256': sha(os.path.join(P12, 'artifact-manifest.json'))}
R['package12IsTheOneIVerified'] = R['package12ManifestSha256'] == 'fb35036f2fc9646b5bb5e03d460f46324ecf455af5f86d3f05bd9217b758cd32'
m12 = rows(os.path.join(P12, 'artifact-manifest.json'))
m13 = rows(os.path.join(P13, 'artifact-manifest.json'))
R['package12MembersStillVerify'] = sum(1 for p, d in m12.items() if os.path.isfile(os.path.join(P12, p)) and sha(os.path.join(P12, p)) == d)
R['package12Members'] = len(m12)
cands = {}
for d, _, fs in os.walk(P13):
    for fn in fs:
        if fn.endswith('artifact-manifest.json'):
            p = os.path.join(d, fn)
            cands[os.path.relpath(p, P13)] = sha(p)
R['manifestLikeFilesInPackage13'] = cands
R['whichEqualsPackage12Manifest'] = sorted(k for k, v in cands.items() if v == R['package12ManifestSha256'])
pred = os.path.join(P13, 'predecessor-artifact-manifest.json')
R['predecessorArtifactManifestSha256'] = sha(pred)
try:
    pj = json.load(open(pred))
    R['predecessorShape'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + '[%d]' % len(v)) for k, v in (pj.items() if isinstance(pj, dict) else [('list', pj)])}
    pm = rows(pred)
    R['predecessorMembers'] = len(pm)
    R['predecessorEqualsPackage12Rows'] = pm == m12
    known = {'package11': '38f7ce94ee0ee9a2de9eecd36777e25b336d2ff3c231445032a8afc7df3fd871'}
    R['predecessorIsKnownManifest'] = [k for k, v in known.items() if v == R['predecessorArtifactManifestSha256']]
except Exception as ex:  # noqa: BLE001
    R['predecessorParseError'] = str(ex)
R['package12To13'] = {'added': sorted(p for p in m13 if p not in m12), 'removed': sorted(p for p in m12 if p not in m13),
                      'changedCommon': sorted(p for p in m13 if p in m12 and m12[p] != m13[p]),
                      'identicalCommon': sum(1 for p in m13 if p in m12 and m12[p] == m13[p])}
sb = json.load(open(os.path.join(P13, 'source-binding.v36.json')))
R['constructionAccountsIdenticalToPackage12'] = {a: {'inPackage12': a in m12, 'inPackage13': a in m13, 'equal': a in m12 and a in m13 and m12[a] == m13[a]}
                                                 for a in sb.get('constructionAccounts') or []}
GROUPS = ('checkpoint3', 'normalized-examples6', 'rust-selection-examples1', 'semantic-controls1', 'binding-controls')
exp = {}
for g in GROUPS:
    for c in json.load(open(os.path.join(P13, g, 'claims.json'))):
        rel = g + '/' + c['path']
        exp[c['name']] = {'path': rel, 'inPackage12': rel in m12, 'bytesEqualPackage12File': os.path.isfile(os.path.join(P12, rel)) and sha(os.path.join(P12, rel)) == sha(os.path.join(P13, rel))}
R['exportsByteEqualPackage12Files'] = exp
R['allExportsByteEqualPackage12Files'] = all(v['bytesEqualPackage12File'] for v in exp.values())
R['claimsFilesEqualPackage12'] = {g: sha(os.path.join(P13, g, 'claims.json')) == sha(os.path.join(P12, g, 'claims.json')) for g in GROUPS}
v12b = os.path.join(P12, 'source-binding.v35.json')
R['package12BindingV35'] = json.load(open(v12b)) if os.path.isfile(v12b) else None
R['provenanceUnchangedFrom12'] = R['package12BindingV35'] is not None and all(
    R['package12BindingV35'].get(k) == sb.get(k) for k in ('constructionAccounts', 'constructionSourceVersion', 'exportsChanged', 'productQualification'))
r05 = json.load(open(R05))
R['r05Superseded'] = {'r05PredecessorIsPackage12': r05.get('predecessorIsPackage12IVerified'), 'r05ConstructionAccounts': r05.get('constructionAccountsIdenticalToPackage12'),
                      'r05Package12To13Counts': {k: (v if isinstance(v, int) else len(v)) for k, v in r05['package12To13'].items()}}
print('package12 manifest fb35036f %s | members still verify %d/%d' % (R['package12IsTheOneIVerified'], R['package12MembersStillVerify'], R['package12Members']))
print('predecessor-artifact-manifest.json sha %s | equals package12 rows %s | known %s | shape %s' % (
    R['predecessorArtifactManifestSha256'][:12], R.get('predecessorEqualsPackage12Rows'), R.get('predecessorIsKnownManifest'), R.get('predecessorShape')))
print('package13 manifest-like files equal to package12 manifest:', R['whichEqualsPackage12Manifest'])
print('TRUE package12->13:', {k: (v if isinstance(v, int) else len(v)) for k, v in R['package12To13'].items()})
print('  added:', R['package12To13']['added'])
print('  removed:', R['package12To13']['removed'])
print('  changedCommon:', R['package12To13']['changedCommon'])
print('construction accounts vs package12:', R['constructionAccountsIdenticalToPackage12'])
print('exports byte-equal package12 files:', R['allExportsByteEqualPackage12Files'], '| claims equal:', R['claimsFilesEqualPackage12'])
print('provenance fields unchanged from package12 binding v35:', R['provenanceUnchangedFrom12'])
json.dump(R, open(os.path.join(OUT, 'p05-package-lineage.json'), 'w'), indent=1, default=str)
print('wrote p05-package-lineage.json')
