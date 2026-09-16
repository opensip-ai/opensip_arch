"""P99: validate this review's own outputs and confirm the inputs were never modified."""
import hashlib
import json
import os

BASE = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v1'
d = json.load(open(os.path.join(BASE, 'review.json')))
m = json.load(open(os.path.join(BASE, 'input-manifest.json')))

print('review.json parses OK')
print('verdict:', d['verdict'])
print('manifestSha matches prompt:',
      d['inputManifestSha256'] == 'e25995b7b649f2376e28caae4d5b06cbf8cdbae8e9ddaa6e7b26b7bbf5ecf32a')
print('filesReadCompletely count:', len(d['filesReadCompletely']))
print('covers exactly the manifest file set:',
      sorted(d['filesReadCompletely']) == sorted(r['path'] for r in m['files']))
print('findings:', [(f['id'], f['severity']) for f in d['findings']])
print('probes:', len(d['probes']), '| limitations:', len(d['limitations']),
      '| strengths:', len(d['confirmedStrengths']))

bad = []
for r in m['files']:
    p = os.path.join(BASE, 'inputs', r['path'])
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != r['sha256'] or os.path.getsize(p) != r['bytes']:
        bad.append(r['path'])
print('inputs byte-identical after all probing:', not bad, bad)
print('inputs dir entry count:', len(os.listdir(os.path.join(BASE, 'inputs'))))
print('top-level entries:', sorted(x for x in os.listdir(BASE) if not x.startswith('.')))
md = open(os.path.join(BASE, 'review.md')).read()
print('review.md chars:', len(md), '| verdict line present:', 'CHANGES_REQUIRED' in md)
