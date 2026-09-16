"""V99: validate this re-review's outputs and confirm both inputs trees are untouched."""
import hashlib
import json
import os

V2 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v2'
V1 = '/tmp/opensip-design-corrections/claude-application-tools-review.v1'

d = json.load(open(os.path.join(V2, 'review.json')))
print('review.json parses OK | verdict:', d['verdict'])
print('manifest digest recorded matches prompt:',
      d['inputManifestSha256'] == '8370a139d4ee7f449b0d39be011362618f8dfb1a17bc27b378586d16241d60a5')

fids = [f['id'] for f in d['priorFindingDispositions']]
print('F1-F11 all dispositioned:', fids == ['F%d' % i for i in range(1, 12)], fids)
print('dispositions:', sorted({f['disposition'].split(' (')[0] for f in d['priorFindingDispositions']}))
print('new findings:', [(g['id'], g['severity'], g['blocking']) for g in d['newFindings']])
print('probes:', len(d['probes']), '| limitations:', len(d['limitations']))

for label, base in (('v2', V2), ('v1', V1)):
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
    print(f'{label}: {len(m["files"])} inputs byte-identical:', not bad, bad,
          '| unlisted entries:', extra)

md = open(os.path.join(V2, 'review.md')).read()
print('review.md chars:', len(md),
      '| verdict present:', 'TOOLING_REVIEW_PASS' in md,
      '| not-ACCEPT stated:', 'not a final application ACCEPT' in md.lower()
      or 'Not a final application ACCEPT' in md)
print('top-level entries:', sorted(x for x in os.listdir(V2) if not x.startswith('.')))
