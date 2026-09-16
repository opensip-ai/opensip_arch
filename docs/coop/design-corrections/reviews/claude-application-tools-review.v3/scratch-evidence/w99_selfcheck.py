"""W99: confirm the v1/v2/v3 inputs trees are untouched and validate this review's outputs."""
import hashlib
import json
import os

BASES = {
    'v1': '/tmp/opensip-design-corrections/claude-application-tools-review.v1',
    'v2': '/tmp/opensip-design-corrections/claude-application-tools-review.v2',
    'v3': '/private/tmp/opensip-design-corrections/claude-application-tools-review.v3',
}
for label, base in BASES.items():
    m = json.load(open(os.path.join(base, 'input-manifest.json')))
    bad = []
    for r in m['files']:
        p = os.path.join(base, 'inputs', r['path'])
        if (not os.path.isfile(p)
                or hashlib.sha256(open(p, 'rb').read()).hexdigest() != r['sha256']
                or os.path.getsize(p) != r['bytes']):
            bad.append(r['path'])
    top = {x['path'].split('/')[0] for x in m['files']}
    extra = sorted(set(os.listdir(os.path.join(base, 'inputs'))) - top)
    print('%s: %d inputs byte-identical=%s %s | unlisted entries=%s'
          % (label, len(m['files']), not bad, bad, extra))

V3 = BASES['v3']
rj = os.path.join(V3, 'review.json')
if os.path.isfile(rj):
    d = json.load(open(rj))
    print()
    print('review.json parses OK | verdict:', d['verdict'])
    print('manifest digest matches prompt:',
          d['inputManifestSha256'] == '7e1e0165c9800c8c937b40598056a4f18fa056efaa700952dcb57711bd4fd47f')
    print('G dispositions:', [(g['id'], g['disposition'].split(' (')[0]) for g in d['followUpDispositions']])
    print('residual observations:', [(o['id'], o['severity']) for o in d.get('residualObservations', [])])
    print('probes:', len(d['probes']), '| limitations:', len(d['limitations']))
    md = open(os.path.join(V3, 'review.md')).read()
    print('review.md chars:', len(md), '| verdict present:', d['verdict'] in md)
print()
print('v3 top-level entries:', sorted(x for x in os.listdir(V3) if not x.startswith('.')))
