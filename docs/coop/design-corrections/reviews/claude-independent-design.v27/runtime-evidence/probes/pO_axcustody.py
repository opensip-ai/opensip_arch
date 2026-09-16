"""PROBE O (v27) — (a) which of the 30 rows preserve their original statement inline, and do the
unresolvable `source` artifacts appear anywhere in frozen27? (b) load my v26 disposition maps so
each can be individually re-decided for 27 rather than copied."""
import json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v27.json'
man = {r['path']: r for r in json.load(open(MAN))['files']}
prop = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json')))
R = {}

inline, titleonly, neither = [], [], []
for i in prop['items']:
    if i.get('original'):
        inline.append(i['id'])
    elif i.get('originalTitle'):
        titleonly.append(i['id'])
    else:
        neither.append(i['id'])
R.update(rowsWithInlineOriginal=inline, rowsWithTitleOnly=titleonly, rowsWithNeither=neither)
print('rows with full inline original (%d): %s' % (len(inline), inline))
print('rows with originalTitle only  (%d): %s' % (len(titleonly), titleonly))
print('rows with NEITHER             (%d): %s' % (len(neither), neither))

# do the cited historical artifacts appear anywhere in frozen27, under any path?
for nm in ('evaluation-proof.v13.json', 'ep13.review-independent.json'):
    hits = [p for p in man if p.endswith(nm)]
    R.setdefault('artifactPresence', {})[nm] = hits
    print('\n%-34s occurrences in frozen27: %d' % (nm, len(hits)))
    for h in hits[:8]:
        print('    ', h)
# are the four variant names at least named inline somewhere in the proposal?
txt = json.dumps(prop)
R['variantNamesMentionedInline'] = {v: txt.count(v) for v in ('AX6', 'AX9', 'MD5', 'RX2c')}
print('\nvariant-name mentions inside the proposal:', R['variantNamesMentionedInline'])

# ---- (b) my v26 disposition maps ----
v26 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v26/review.json'))
print('\nv26 review.json top keys (%d):' % len(v26))
for k in sorted(v26):
    v = v26[k]
    kind = type(v).__name__
    n = len(v) if isinstance(v, (list, dict)) else ''
    print('   %-44s %-6s %s' % (k, kind, n))
R['v26TopKeys'] = {k: (type(v26[k]).__name__, len(v26[k]) if isinstance(v26[k], (list, dict)) else None)
                   for k in sorted(v26)}
for key in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
            'scopedReviewOwnerDispositions'):
    v = v26.get(key)
    if v is None:
        print('\n%s: ABSENT in v26' % key)
        continue
    ids = list(v) if isinstance(v, dict) else [x.get('id') for x in v]
    print('\n%s (%d): %s' % (key, len(v), ids))
    sample = v[ids[0]] if isinstance(v, dict) else v[0]
    print('   row shape:', json.dumps(sample, default=str)[:600])
    R.setdefault('v26Maps', {})[key] = {'ids': ids, 'sample': sample}

json.dump(R, open(os.path.join(OUT, 'pO-axcustody.json'), 'w'), indent=1, default=str)
print('\nwrote pO-axcustody.json')
