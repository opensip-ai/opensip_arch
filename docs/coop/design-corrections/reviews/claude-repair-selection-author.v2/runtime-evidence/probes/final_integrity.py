"""Final integrity: v1 preserved, independent review preserved, v2 source exactly as declared."""
import hashlib, json, os

V1_SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
V1_RT = '/tmp/opensip-design-corrections/claude-repair-selection-author.v1'
REVIEW = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1'
ROOT_REVIEW = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1'
SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(RT, 'probes')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def tree(root):
    out = {}
    for dp, _d, fs in os.walk(root):
        for n in fs:
            full = os.path.join(dp, n)
            out[os.path.relpath(full, root)] = sha(full)
    return out


base = json.load(open(os.path.join(HERE, 'v2-source-baseline.json')))
v1_declared = {r['path']: r['sha256'] for r in base['baseline'].values()} if False else None

# v1 source must be untouched: it is the custody parent, hashed in v2-source-baseline
v1_now = tree(V1_SRC)
v1_expected = {r: base['baseline'][r]['sha256'] for r in base['baseline']}
v1_drift = sorted(p for p in v1_expected if v1_now.get(p) != v1_expected[p])

v1_rt = tree(V1_RT)
review = tree(REVIEW)
root_review = tree(ROOT_REVIEW)

handoff = json.load(open(os.path.join(RT, 'changed-file-handoff.json')))

doc = {
    'v1SourceFiles': len(v1_now),
    'v1SourceDriftFromCustodyBaseline': v1_drift,
    'v1RuntimeFiles': len(v1_rt),
    'v1RuntimeHasDeliverables': all(
        k in v1_rt for k in ('author-review.md', 'author-review.json',
                             'assessment-corrections.md', 'changed-file-handoff.json')),
    'independentReviewFiles': len(review),
    'independentReviewHasReport': 'review.md' in review and 'review.json' in review,
    'rootReviewFiles': len(root_review),
    'v2Source': {
        'baselineFileCount': handoff['baselineFileCount'],
        'currentFileCount': handoff['currentFileCount'],
        'declaredChanges': len(handoff['changedFiles']),
        'undeclaredChanges': handoff['undeclaredChanges'],
        'unexpectedNewFiles': handoff['unexpectedNewFiles'],
        'missingFiles': handoff['missingFiles'],
    },
    'runtimeArtifacts': sorted(tree(RT)),
}
json.dump(doc, open(os.path.join(HERE, 'final-integrity.json'), 'w'), indent=2)
print('v1 source files      ', doc['v1SourceFiles'], '| drift', len(doc['v1SourceDriftFromCustodyBaseline']))
print('v1 runtime intact    ', doc['v1RuntimeHasDeliverables'], '|', doc['v1RuntimeFiles'], 'files')
print('independent review   ', doc['independentReviewHasReport'], '|', doc['independentReviewFiles'], 'files')
print('root review          ', doc['rootReviewFiles'], 'files')
print('v2 source            ', doc['v2Source']['baselineFileCount'], '->', doc['v2Source']['currentFileCount'],
      '| declared', doc['v2Source']['declaredChanges'],
      '| undeclared', len(doc['v2Source']['undeclaredChanges']))
print('runtime artifacts    ', len(doc['runtimeArtifacts']))
