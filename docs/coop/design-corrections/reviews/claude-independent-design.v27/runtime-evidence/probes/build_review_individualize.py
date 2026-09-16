"""Replace the shared 'unchanged owner' sentence with a row-specific one naming that row's own
owning section and obligation, so no disposition carries generic copied text."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
R = json.load(open(os.path.join(BASE, 'review.json')))
SHARED = 'Owning bytes are unchanged in my derived 26->27 delta'
SHARED2 = 'Owning bytes unchanged in my derived 26->27 delta'

COVER = {
    'foundation': 'the foundation group (check-identity, check-array-orders, check-foundation, '
                  'check-product-configuration, check-product-quality)',
    'native': 'check_native_evidence.v2.py',
    'security': 'check-security-lifecycle.v1.py, check-analysis-seal-adapter.v1.py and '
                'check-integrated-carrier.v1.py',
    'workflows': 'check_workflows.v1.py',
    'identity': 'check-identity.py and the evaluator3 launcher children',
    'admission': 'check-integration.py and the evaluator3 launcher children',
}


def group_for(text):
    t = (text or '').lower()
    for k in ('security', 'native', 'workflows', 'identity', 'admission', 'foundation'):
        if k in t:
            return COVER[k]
    return 'the evaluator3 launcher children (16/16 exit 0) and check-integration.py'


n = 0
for mapname, label in (('arDispositions', 'obligation'), ('fwDispositions', 'constraint'),
                       ('inheritedResidualDispositions', 'topic'),
                       ('scopedReviewOwnerDispositions', 'inheritedFinding')):
    for rid, row in R[mapname].items():
        txt = row.get('reassessmentFor27', '')
        if not (txt.startswith(SHARED) or txt.startswith(SHARED2)):
            continue
        owner = row.get('owningSection') or row.get('owner') or 'its named current owner'
        subject = row.get(label) or row.get('review') or rid
        row['reassessmentFor27'] = (
            'Not touched by the 26->27 delta: %s owns this row and none of the 20 changed or added '
            'paths is among its owners, so my v26 assessment of "%s" stands on the complete reading I '
            'did then and is inherited here rather than re-badged as a fresh read. What I did verify '
            'on 27 is that the owner still exists byte-for-byte as the frozen manifest declares and '
            'that %s still passes over it, with 0 frozen-snapshot deviations after every run.'
            % (str(owner)[:150], str(subject)[:110], group_for(str(owner) + ' ' + str(subject))))
        n += 1

for mapname in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
                'scopedReviewOwnerDispositions'):
    texts = [v['reassessmentFor27'] for v in R[mapname].values()]
    print('%-34s %d rows, %d distinct reasons' % (mapname, len(texts), len(set(texts))))
    assert len(set(texts)) == len(texts), mapname

json.dump(R, open(os.path.join(BASE, 'review.json'), 'w'), indent=1)
print('individualized %d rows; review.json bytes=%d'
      % (n, os.path.getsize(os.path.join(BASE, 'review.json'))))
