import hashlib, json, os, sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
EXPECTED = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v37/receipts/manifest-verification.json'

raw = open(MANIFEST, 'rb').read()
msha = hashlib.sha256(raw).hexdigest()
m = json.loads(raw)
root = m['snapshotRoot']
bad, missing, total = [], [], 0
listed = set()
for f in m['files']:
    p = os.path.join(root, f['path'])
    listed.add(f['path'])
    if not os.path.isfile(p):
        missing.append(f['path']); continue
    b = open(p, 'rb').read()
    total += len(b)
    h = hashlib.sha256(b).hexdigest()
    if h != f['sha256'] or len(b) != f['bytes']:
        bad.append({'path': f['path'], 'sha': h, 'len': len(b), 'exp': f})
extra = []
for d, _, fs in os.walk(root):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), root)
        if rel not in listed:
            extra.append(rel)
res = {
    'manifestSha256': msha, 'manifestBytes': len(raw), 'manifestMatchesExpected': msha == EXPECTED,
    'fileCountDeclared': m['fileCount'], 'fileEntries': len(m['files']), 'distinctPaths': len(listed),
    'totalBytesDeclared': m['totalBytes'], 'totalBytesMeasured': total,
    'mismatches': bad, 'missing': missing, 'unlistedFilesInSnapshot': extra[:200], 'unlistedCount': len(extra),
    'parentManifestSha256': m.get('parentManifestSha256'),
}
res['verified'] = (res['manifestMatchesExpected'] and not bad and not missing and not extra
                   and total == m['totalBytes'] and len(m['files']) == m['fileCount'] == len(listed))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT, 'w'), indent=2)
print(json.dumps({k: v for k, v in res.items() if k not in ('unlistedFilesInSnapshot',)}, indent=1)[:3000])
print('unlisted sample', extra[:20])
