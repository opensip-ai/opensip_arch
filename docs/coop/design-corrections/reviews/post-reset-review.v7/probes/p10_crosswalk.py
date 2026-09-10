"""NEW-SHOULD-2: verify the crosswalk's three-way separation is real, that
latestCompletedReview pins the ACTUAL accepted-or-completed predecessor bytes and
an EXISTING source row, that no future review is hash-embedded in its own frozen
subject, and that no stale review is presented as current."""
import json, hashlib, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v7')
DC = ROOT / 'docs/coop/design-corrections'
c = json.loads((DC / 'correction-crosswalk.proposed.json').read_text())
items = c['items']
R = {'itemCount': len(items), 'standing': c['standing']}

def sha(p):
    p = ROOT / p
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

def ptr(doc, sel):
    cur = doc
    for part in [x for x in sel.split('/') if x]:
        if isinstance(cur, dict):
            if part not in cur: return None
            cur = cur[part]
        elif isinstance(cur, list):
            try: cur = cur[int(part)]
            except Exception: return None
        else: return None
    return cur

problems = []
lat_ok = hist_ok = cur_ok = 0
for it in items:
    i = it['id']
    if set(['historicalReviews', 'latestCompletedReview', 'currentReviewBinding']) - set(it):
        problems.append((i, 'missing one of the three sections')); continue
    lat = it['latestCompletedReview']
    got = sha(lat['path'])
    if got != lat['sha256']:
        problems.append((i, 'latestCompletedReview sha mismatch %s vs %s' % (got, lat['sha256'])))
    else:
        rev = json.loads((ROOT / lat['path']).read_bytes())
        if rev['subject']['manifestSha256'] != lat['subjectManifestSha256']:
            problems.append((i, 'latestCompletedReview subject manifest mismatch'))
        elif ptr(rev, lat['selector']) is None:
            problems.append((i, 'latestCompletedReview selector %s absent' % lat['selector']))
        elif rev['overallVerdict'] != lat['overallVerdict']:
            problems.append((i, 'latestCompletedReview verdict mismatch'))
        else:
            lat_ok += 1
    for h in it['historicalReviews']:
        if sha(h['path']) is None:
            problems.append((i, 'historical review file absent: ' + h['path']))
        else:
            hist_ok += 1
    cb = it['currentReviewBinding']
    if cb.get('standing') != 'PENDING-INDEPENDENT-REVIEW':
        problems.append((i, 'currentReviewBinding not pending: ' + str(cb.get('standing'))))
    elif any(k in cb for k in ('sha256', 'overallVerdict', 'verdict', 'subjectManifestSha256')):
        problems.append((i, 'currentReviewBinding asserts a future verdict/hash'))
    else:
        cur_ok += 1

R['latestCompletedVerified'] = lat_ok
R['historicalReviewFilesPresent'] = hist_ok
R['currentBindingPendingAndUnhashed'] = cur_ok
R['problems'] = problems

# the pinned predecessor must be the v6 manifest, which is v7's declared predecessor
man = json.loads((ROOT / 'docs/coop/design-corrections/reviews/candidate-subject.v6.json').read_bytes()) \
    if (ROOT / 'docs/coop/design-corrections/reviews/candidate-subject.v6.json').is_file() else None
v7man = json.loads(Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/'
                        'reviews/candidate-subject.v7.json').read_bytes())
R['v7PredecessorManifestSha256'] = v7man['predecessorManifestSha256']
R['crosswalkPinsThatSamePredecessor'] = {
    it['latestCompletedReview']['subjectManifestSha256'] for it in items}
R['pinsExactlyThePredecessor'] = (R['crosswalkPinsThatSamePredecessor']
                                  == {v7man['predecessorManifestSha256']})
R['embeddedV6ManifestSha'] = sha('docs/coop/design-corrections/reviews/candidate-subject.v6.json')
R['embeddedV6ManifestMatchesPredecessor'] = (R['embeddedV6ManifestSha']
                                             == v7man['predecessorManifestSha256'])
# no row may reference this (v7) manifest hash - that would be a self-hash cycle
blob = json.dumps(c)
R['noSelfHashCycle'] = 'b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b' not in blob
# stale v1 pointer must no longer appear as a CURRENT binding
R['v1AppearsOnlyAsHistorical'] = all(
    'post-reset-review.v1' not in json.dumps(it['latestCompletedReview'])
    and 'post-reset-review.v1' not in json.dumps(it['currentReviewBinding'])
    for it in items)
R['statuses'] = sorted({it['status'] for it in items})
R['unitsCovered'] = sorted({it['unit'] for it in items})
R['idsCovered'] = [it['id'] for it in items]

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
